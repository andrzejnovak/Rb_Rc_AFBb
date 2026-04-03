"""Data-driven MC efficiency calibration via d0 smearing.

Implements the standard ALEPH approach (inspire_433306): calibrate MC
tracking resolution to match data using the negative impact parameter
tail, then re-derive all efficiencies from calibrated MC.

Root cause: the 3-tag R_b extraction gives R_b ~ 0.163 on 10% data
vs 0.21578 on MC. The MC-derived efficiencies don't match data because
the tracking resolution differs between data and MC.

Approach:
  Step 1: Measure data/MC resolution mismatch from sigma_d0 calibration
  Step 2: Derive d0 smearing to make MC match data resolution
  Step 3: Re-derive hemisphere tags from smeared MC
  Step 4: Re-extract R_b with calibrated efficiencies
  Step 5: Tag-rate scale factor approach (cross-check)
  Step 6: Re-extract A_FB^b with calibrated purities
  Step 7: Compare all approaches

Source: inspire_433306 Section 7.1 — negative tail calibration method.

Reads:
  phase3_selection/outputs/sigma_d0_params.json      (calibration scale factors)
  phase3_selection/outputs/preselected_mc.npz         (MC tracks)
  phase3_selection/outputs/preselected_data.npz       (data tracks)
  phase3_selection/outputs/d0_significance.npz        (significances)
  phase3_selection/outputs/signed_d0.npz              (signed significances)
  phase3_selection/outputs/hemisphere_tags.npz         (original tags)
  phase4_inference/4b_partial/outputs/data_10pct_tags.npz  (10% data tags)
  phase4_inference/4a_expected/outputs/correlation_results.json

Writes:
  phase4_inference/4b_partial/outputs/d0_smearing_results.json
  phase4_inference/4b_partial/outputs/smeared_mc_tags.npz
  analysis_note/results/parameters.json (updates)
"""
import json
import logging
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.stats import chi2 as chi2_dist
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

HERE = Path(__file__).resolve().parent
PHASE4B_OUT = HERE.parent / "outputs"
P4A_OUT = HERE.parents[1] / "4a_expected" / "outputs"
P3_OUT = HERE.parents[2] / "phase3_selection" / "outputs"
P3_SRC = HERE.parents[2] / "phase3_selection" / "src"
RESULTS_DIR = HERE.parents[2] / "analysis_note" / "results"
PHASE4B_OUT.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(P3_SRC))
sys.path.insert(0, str(HERE.parents[1] / "4a_expected" / "src"))

from sigma_d0_calibration import (
    compute_sigma_d0, A_INIT, B_INIT,
    P_BINS, COSTHETA_BINS, NVDET_CLASSES
)
from hemisphere_tag import (
    build_resolution_cdf, compute_hemisphere_tags_vectorized
)
from three_tag_rb_extraction import (
    count_three_tag, calibrate_three_tag_efficiencies,
    extract_rb_three_tag, toy_uncertainty_three_tag,
    R_B_SM, R_C_SM, R_UDS_SM,
)

N_TOYS = 1000
TOY_SEED = 54321
SMEAR_SEED = 98765

# 10% subsample parameters (same as run_phase4b.py)
SUBSAMPLE_SEED = 42
SUBSAMPLE_FRACTION = 0.10


# ======================================================================
# Step 1: Measure data/MC resolution mismatch
# ======================================================================

def measure_resolution_mismatch():
    """Load sigma_d0 calibration and compute per-bin data/MC scale ratios.

    The sigma_d0 calibration from Phase 3 already has per-bin scale
    factors for both data and MC. The ratio data_sf / mc_sf gives the
    resolution mismatch.

    Returns dict of bin_label -> {data_sf, mc_sf, ratio, ...}
    """
    with open(P3_OUT / "sigma_d0_params.json") as f:
        params = json.load(f)

    data_cal = params["data_calibration"]
    mc_cal = params["mc_calibration"]

    mismatch = {}
    ratios = []

    log.info("\n--- Step 1: Data/MC Resolution Mismatch ---")
    log.info("%-15s  %-8s  %-8s  %-8s  %-8s",
             "Bin", "SF_data", "SF_mc", "Ratio", "N_trk")

    for key in sorted(data_cal.keys()):
        d = data_cal[key]
        m = mc_cal[key]

        sf_data = d["scale_factor"]
        sf_mc = m["scale_factor"]

        # Ratio > 1 means data has worse resolution than MC
        ratio = sf_data / sf_mc if sf_mc > 0.01 else 1.0

        mismatch[key] = {
            "nvdet": d["nvdet"],
            "p_range": d["p_range"],
            "costheta_range": d["costheta_range"],
            "scale_factor_data": sf_data,
            "scale_factor_mc": sf_mc,
            "ratio_data_mc": ratio,
            "n_tracks_data": d["n_tracks"],
            "n_tracks_mc": m["n_tracks"],
        }
        ratios.append(ratio)

        log.info("%-15s  %-8.3f  %-8.3f  %-8.3f  %-8d",
                 key, sf_data, sf_mc, ratio, d["n_tracks"])

    ratios = np.array(ratios)
    log.info("\nMismatch summary:")
    log.info("  Mean ratio (data/MC): %.3f", np.mean(ratios))
    log.info("  Median ratio: %.3f", np.median(ratios))
    log.info("  Range: [%.3f, %.3f]", np.min(ratios), np.max(ratios))

    return mismatch


# ======================================================================
# Step 2: Smear MC d0 to match data resolution
# ======================================================================

def smear_mc_d0(mismatch):
    """Apply d0 smearing to MC tracks to match data resolution.

    For each (nvdet, p, cos_theta) bin:
      sigma_smear = sigma_d0_mc * sqrt(ratio^2 - 1)
      d0_smeared = d0_mc + Gaussian(0, sigma_smear)

    where ratio = scale_factor_data / scale_factor_mc.

    Returns smeared d0, smeared significance, and the signed significance.
    """
    log.info("\n--- Step 2: Smearing MC d0 ---")

    mc = np.load(P3_OUT / "preselected_mc.npz", allow_pickle=False)
    d0_sig = np.load(P3_OUT / "d0_significance.npz", allow_pickle=False)
    signed = np.load(P3_OUT / "signed_d0.npz", allow_pickle=False)

    d0_flat = mc["trk_d0"]
    offsets = mc["trk_d0_offsets"]
    pmag = mc["trk_pmag"]
    theta = mc["trk_theta"]
    nvdet = mc["trk_nvdet"]
    cos_theta_thrust = mc["cos_theta_thrust"]

    # Get MC sigma_d0 (nominal * MC scale factor)
    mc_sigma_d0 = d0_sig["mc_sigma_d0"]
    mc_scale_factors = d0_sig["mc_scale_factors"]

    # Broadcast cos_theta_thrust to track level
    n_events = len(offsets) - 1
    trk_cos_thrust = np.empty_like(d0_flat)
    for i in range(n_events):
        start, end = offsets[i], offsets[i + 1]
        trk_cos_thrust[start:end] = cos_theta_thrust[i]

    # Build bin assignment for each MC track
    rng = np.random.RandomState(SMEAR_SEED)
    d0_smeared = d0_flat.copy()
    n_smeared = 0
    n_total = len(d0_flat)

    smear_diagnostics = {}

    for key, info in sorted(mismatch.items()):
        nv = info["nvdet"]
        p_lo, p_hi = info["p_range"]
        ct_lo, ct_hi = info["costheta_range"]
        ratio = info["ratio_data_mc"]

        # Build bin mask
        if nv == 1:
            nv_mask = nvdet == 1
        else:
            nv_mask = nvdet >= 2

        p_mask = (pmag >= p_lo) & (pmag < p_hi)
        ct_mask = (np.abs(trk_cos_thrust) >= ct_lo) & (np.abs(trk_cos_thrust) < ct_hi)
        bin_mask = nv_mask & p_mask & ct_mask

        n_in_bin = int(np.sum(bin_mask))
        if n_in_bin == 0:
            continue

        if ratio > 1.0:
            # Data has worse resolution: need to smear MC
            # sigma_smear^2 = sigma_data^2 - sigma_mc^2
            # = (ratio * sigma_mc)^2 - sigma_mc^2
            # = sigma_mc^2 * (ratio^2 - 1)
            # sigma_smear = sigma_mc * sqrt(ratio^2 - 1)
            sigma_smear_factor = np.sqrt(ratio**2 - 1.0)
            sigma_smear = mc_sigma_d0[bin_mask] * sigma_smear_factor
            noise = rng.normal(0, 1, size=n_in_bin) * sigma_smear
            d0_smeared[bin_mask] = d0_flat[bin_mask] + noise
            n_smeared += n_in_bin
        else:
            # MC already broader than data — no smearing needed
            # (Could in principle sharpen, but that's not physical)
            pass

        smear_diagnostics[key] = {
            "ratio": ratio,
            "n_tracks": n_in_bin,
            "smeared": ratio > 1.0,
            "sigma_smear_factor": float(np.sqrt(max(ratio**2 - 1.0, 0.0))),
        }

    log.info("Smeared %d / %d MC tracks (%.1f%%)",
             n_smeared, n_total, 100.0 * n_smeared / n_total)

    # Recompute sigma_d0 for smeared MC (same parametrization, same MC scale factors)
    sigma_d0_nom = compute_sigma_d0(pmag, theta, A_INIT, B_INIT)
    # Use the data scale factors instead of MC ones (since we smeared to match data)
    # Actually, after smearing the MC d0, the correct sigma_d0 should use
    # the data-calibrated values. But to keep the same framework, we
    # recalibrate from the smeared MC negative tail.
    smeared_sig_uncalibrated = d0_smeared / (sigma_d0_nom * mc_scale_factors)

    # Recalibrate from smeared MC negative tail (should now match data)
    log.info("Recalibrating smeared MC from negative tail...")
    smeared_scale_factors = np.ones_like(d0_flat)

    for nv in NVDET_CLASSES:
        if nv == 1:
            nv_mask = nvdet == 1
        else:
            nv_mask = nvdet >= 2

        for ip, (p_lo, p_hi) in enumerate(zip(P_BINS[:-1], P_BINS[1:])):
            p_mask = (pmag >= p_lo) & (pmag < p_hi)
            for ic, (ct_lo, ct_hi) in enumerate(zip(COSTHETA_BINS[:-1], COSTHETA_BINS[1:])):
                ct_mask = (np.abs(trk_cos_thrust) >= ct_lo) & (np.abs(trk_cos_thrust) < ct_hi)
                bin_mask = nv_mask & p_mask & ct_mask
                n_in_bin = int(np.sum(bin_mask))
                if n_in_bin < 50:
                    continue

                sig_bin = d0_smeared[bin_mask] / sigma_d0_nom[bin_mask]
                neg = sig_bin[sig_bin < 0]
                if len(neg) < 50:
                    continue
                mad = np.median(np.abs(neg - np.median(neg)))
                neg_width = mad * 1.4826
                if neg_width > 0.01:
                    smeared_scale_factors[bin_mask] = neg_width

    sigma_d0_smeared = sigma_d0_nom * smeared_scale_factors
    smeared_significance = d0_smeared / sigma_d0_smeared

    # Compute signed d0 for smeared MC using the same convention as Phase 3
    # Phase 3 signed_d0.npz has mc_signed_sig
    # The sign depends on the PCA-jet angle, which doesn't change with smearing
    # So we can just apply the same sign as the original
    mc_original_sig = signed["mc_signed_sig"]
    mc_original_unsig = d0_sig["mc_significance"]

    # The sign is sign(signed_sig / abs(significance))
    # Or equivalently, sign(signed_sig) where significance != 0
    sign_mask = np.abs(mc_original_unsig) > 1e-10
    signs = np.ones_like(d0_flat)
    signs[sign_mask] = np.sign(mc_original_sig[sign_mask])

    smeared_signed_sig = np.abs(smeared_significance) * signs

    # Validate: check negative tail width after smearing
    neg_smeared = smeared_signed_sig[smeared_signed_sig < 0]
    neg_data_signed = signed["data_signed_sig"]
    neg_data = neg_data_signed[neg_data_signed < 0]

    log.info("\nNegative tail width comparison:")
    log.info("  Original MC: %.3f", np.std(signed["mc_signed_sig"][signed["mc_signed_sig"] < 0]))
    log.info("  Smeared MC:  %.3f", np.std(neg_smeared))
    log.info("  Data:        %.3f", np.std(neg_data))

    return (d0_smeared, smeared_signed_sig, mc, smear_diagnostics)


# ======================================================================
# Step 3: Re-derive hemisphere tags from smeared MC
# ======================================================================

def recompute_mc_tags(smeared_signed_sig, mc):
    """Recompute hemisphere probability + mass tags on smeared MC.

    Uses the same tagging algorithm as Phase 3 hemisphere_tag.py,
    but with smeared significances.
    """
    log.info("\n--- Step 3: Recomputing MC Tags from Smeared MC ---")

    offsets = mc["trk_d0_offsets"]
    hem = mc["trk_hem"]
    pmag = mc["trk_pmag"]
    theta = mc["trk_theta"]
    phi = mc["trk_phi"]

    n_events = len(offsets) - 1
    log.info("MC events: %d", n_events)

    # Build resolution CDF from negative tail of smeared MC
    neg_sig = smeared_signed_sig[smeared_signed_sig < 0]
    log.info("Smeared MC negative tail: %d tracks", len(neg_sig))
    bin_edges, survival = build_resolution_cdf(neg_sig)

    # Compute tags
    tags = compute_hemisphere_tags_vectorized(
        smeared_signed_sig, offsets, hem, pmag, theta, phi,
        bin_edges, survival
    )

    # Save smeared tags
    np.savez_compressed(
        PHASE4B_OUT / "smeared_mc_tags.npz",
        **{f"mc_{k}": v for k, v in tags.items()},
    )
    log.info("Saved smeared_mc_tags.npz")

    return tags


# ======================================================================
# Step 4: Re-extract R_b with smeared MC efficiencies
# ======================================================================

def extract_rb_smeared(smeared_mc_tags, data_10pct_tags):
    """Extract R_b using efficiencies calibrated on smeared MC.

    This is the key test: if data/MC resolution mismatch was the cause
    of the R_b bias, smeared MC efficiencies should give R_b closer to SM.
    """
    log.info("\n--- Step 4: R_b Extraction with Smeared MC Efficiencies ---")

    mc_h0 = smeared_mc_tags["combined_h0"]
    mc_h1 = smeared_mc_tags["combined_h1"]

    data_h0 = data_10pct_tags["data_combined_h0"]
    data_h1 = data_10pct_tags["data_combined_h1"]

    n_mc = len(mc_h0)
    n_data = len(data_h0)
    log.info("Smeared MC: %d events, 10%% data: %d events", n_mc, n_data)

    threshold_configs = [
        (8.0, 3.0), (8.0, 4.0), (8.0, 5.0),
        (9.0, 3.0), (9.0, 4.0), (9.0, 5.0),
        (10.0, 3.0), (10.0, 5.0), (10.0, 7.0),
        (11.0, 4.0), (11.0, 6.0),
        (12.0, 5.0), (12.0, 6.0),
    ]

    all_results = []
    for thr_tight, thr_loose in threshold_configs:
        label = "tight=%.0f, loose=%.0f" % (thr_tight, thr_loose)

        # Calibrate on smeared MC
        counts_mc = count_three_tag(mc_h0, mc_h1, thr_tight, thr_loose)
        cal = calibrate_three_tag_efficiencies(counts_mc, R_B_SM, R_C_SM)

        # Count on 10% data
        counts_data = count_three_tag(data_h0, data_h1, thr_tight, thr_loose)

        # Extract R_b (C_b=1.0: no hemisphere correlation assumed)
        extraction = extract_rb_three_tag(
            counts_data, cal, R_C_SM, C_b_tight=1.0)

        # Toy uncertainty
        rb_mean, rb_sigma, _, n_valid = toy_uncertainty_three_tag(
            data_h0, data_h1, thr_tight, thr_loose,
            cal, R_C_SM, n_toys=N_TOYS, seed=TOY_SEED)

        log.info("%s: R_b=%.5f +/- %.5f, chi2/ndf=%.2f/%d, p=%.3f",
                 label, extraction["R_b"],
                 rb_sigma if not np.isnan(rb_sigma) else 0.0,
                 extraction["chi2"], extraction["ndf"],
                 extraction["p_value"])

        all_results.append({
            "thr_tight": float(thr_tight),
            "thr_loose": float(thr_loose),
            "label": label,
            "counts_data": counts_data,
            "calibration": cal,
            "R_b": extraction["R_b"],
            "chi2": extraction["chi2"],
            "ndf": extraction["ndf"],
            "p_value": extraction["p_value"],
            "sigma_stat": float(rb_sigma) if not np.isnan(rb_sigma) else None,
            "n_valid_toys": n_valid,
        })

    # Find best and combined
    valid = [r for r in all_results
             if r["sigma_stat"] is not None and r["sigma_stat"] > 0
             and 0.05 < r["R_b"] < 0.50]

    if valid:
        best = min(valid, key=lambda x: x["sigma_stat"])
        log.info("\nBest smeared: %s, R_b = %.5f +/- %.5f",
                 best["label"], best["R_b"], best["sigma_stat"])

        rb_vals = np.array([r["R_b"] for r in valid])
        rb_errs = np.array([r["sigma_stat"] for r in valid])
        w = 1.0 / rb_errs**2
        rb_combined = float(np.sum(w * rb_vals) / np.sum(w))
        sigma_combined = float(1.0 / np.sqrt(np.sum(w)))
        chi2_stab = float(np.sum((rb_vals - rb_combined)**2 / rb_errs**2))
        ndf_stab = len(valid) - 1
        p_stab = float(1.0 - chi2_dist.cdf(chi2_stab, ndf_stab)) if ndf_stab > 0 else 1.0
    else:
        best = None
        rb_combined = None
        sigma_combined = None
        chi2_stab = 0.0
        ndf_stab = 0
        p_stab = 1.0

    return {
        "all_results": all_results,
        "best_config": best,
        "stability": {
            "R_b_combined": rb_combined,
            "sigma_combined": sigma_combined,
            "chi2": chi2_stab,
            "ndf": ndf_stab,
            "p_value": p_stab,
        },
    }


# ======================================================================
# Step 5: Tag-rate scale factor approach (simpler cross-check)
# ======================================================================

def _apply_sf_and_extract(mc_h0, mc_h1, data_h0, data_h1,
                          thr_tight, thr_loose, C_b_tight=1.0):
    """Helper: apply SF correction and extract R_b for one config."""
    counts_mc = count_three_tag(mc_h0, mc_h1, thr_tight, thr_loose)
    counts_data = count_three_tag(data_h0, data_h1, thr_tight, thr_loose)

    sf_tight = counts_data["f_s_tight"] / max(counts_mc["f_s_tight"], 1e-8)
    sf_loose = counts_data["f_s_loose"] / max(counts_mc["f_s_loose"], 1e-8)
    sf_anti = counts_data["f_s_anti"] / max(counts_mc["f_s_anti"], 1e-8)

    cal_orig = calibrate_three_tag_efficiencies(counts_mc, R_B_SM, R_C_SM)

    cal_sf = {}
    for q in ["b", "c", "uds"]:
        et = cal_orig[f"eps_{q}_tight"] * sf_tight
        el = cal_orig[f"eps_{q}_loose"] * sf_loose
        ea = cal_orig[f"eps_{q}_anti"] * sf_anti
        tot = et + el + ea
        if tot > 0:
            cal_sf[f"eps_{q}_tight"] = float(et / tot)
            cal_sf[f"eps_{q}_loose"] = float(el / tot)
            cal_sf[f"eps_{q}_anti"] = float(ea / tot)
        else:
            cal_sf[f"eps_{q}_tight"] = cal_orig[f"eps_{q}_tight"]
            cal_sf[f"eps_{q}_loose"] = cal_orig[f"eps_{q}_loose"]
            cal_sf[f"eps_{q}_anti"] = cal_orig[f"eps_{q}_anti"]

    for k in ["chi2_calibration", "ndf_calibration", "converged"]:
        cal_sf[k] = cal_orig[k]

    extraction = extract_rb_three_tag(
        counts_data, cal_sf, R_C_SM, C_b_tight=C_b_tight)

    return extraction, cal_sf, sf_tight, sf_loose, sf_anti


def tag_rate_scale_factors(data_10pct_tags):
    """Compute tag-rate scale factors and apply to MC efficiencies.

    SF(WP) = f_s(data) / f_s(MC) at each working point.
    Then eps_corrected = eps_MC * SF (renormalized).

    Uses C_b = 1.0 (no hemisphere correlation), which is the correct
    choice for the 3-tag system where the double-tag equations already
    have 6 independent constraints (the SF correction absorbs the
    data/MC mismatch that would otherwise be attributed to C_b).
    """
    log.info("\n--- Step 5: Tag-Rate Scale Factor Approach ---")

    mc_tags = np.load(P3_OUT / "hemisphere_tags.npz", allow_pickle=False)
    mc_h0 = mc_tags["mc_combined_h0"]
    mc_h1 = mc_tags["mc_combined_h1"]

    data_h0 = data_10pct_tags["data_combined_h0"]
    data_h1 = data_10pct_tags["data_combined_h1"]

    # Wide threshold scan: the SF approach should give consistent R_b
    # across all configurations
    threshold_configs = [
        (8.0, 3.0), (8.0, 4.0), (8.0, 5.0),
        (9.0, 3.0), (9.0, 4.0), (9.0, 5.0),
        (10.0, 3.0), (10.0, 5.0), (10.0, 7.0),
        (11.0, 4.0), (11.0, 6.0),
        (12.0, 5.0), (12.0, 6.0),
        (13.0, 5.0), (14.0, 5.0),
    ]

    all_results = []
    for thr_tight, thr_loose in threshold_configs:
        label = "tight=%.0f, loose=%.0f" % (thr_tight, thr_loose)

        # C_b = 1.0: the SF correction handles the data/MC mismatch
        extraction, cal_sf, sf_t, sf_l, sf_a = _apply_sf_and_extract(
            mc_h0, mc_h1, data_h0, data_h1, thr_tight, thr_loose, C_b_tight=1.0)

        # Toy uncertainty
        rb_mean, rb_sigma, _, n_valid = toy_uncertainty_three_tag(
            data_h0, data_h1, thr_tight, thr_loose,
            cal_sf, R_C_SM, n_toys=N_TOYS, seed=TOY_SEED)

        log.info("%s: SF=(%.4f, %.4f, %.4f) -> R_b=%.5f +/- %.5f, chi2/ndf=%.1f/%d",
                 label, sf_t, sf_l, sf_a,
                 extraction["R_b"],
                 rb_sigma if not np.isnan(rb_sigma) else 0.0,
                 extraction["chi2"], extraction["ndf"])

        all_results.append({
            "thr_tight": float(thr_tight),
            "thr_loose": float(thr_loose),
            "label": label,
            "sf_tight": float(sf_t),
            "sf_loose": float(sf_l),
            "sf_anti": float(sf_a),
            "calibration_sf": cal_sf,
            "C_b_used": 1.0,
            "R_b": extraction["R_b"],
            "chi2": extraction["chi2"],
            "ndf": extraction["ndf"],
            "p_value": extraction["p_value"],
            "sigma_stat": float(rb_sigma) if not np.isnan(rb_sigma) else None,
            "n_valid_toys": n_valid,
        })

    # Find best (minimum stat uncertainty)
    valid = [r for r in all_results
             if r["sigma_stat"] is not None and r["sigma_stat"] > 0
             and 0.05 < r["R_b"] < 0.50]

    if valid:
        best = min(valid, key=lambda x: x["sigma_stat"])
        log.info("\nBest SF config: %s, R_b = %.5f +/- %.5f",
                 best["label"], best["R_b"], best["sigma_stat"])

        # Weighted average across configs (should be very consistent)
        rb_vals = np.array([r["R_b"] for r in valid])
        rb_errs = np.array([r["sigma_stat"] for r in valid])
        w = 1.0 / rb_errs**2
        rb_combined = float(np.sum(w * rb_vals) / np.sum(w))
        sigma_combined = float(1.0 / np.sqrt(np.sum(w)))
        chi2_stab = float(np.sum((rb_vals - rb_combined)**2 / rb_errs**2))
        ndf_stab = len(valid) - 1
        p_stab = float(1.0 - chi2_dist.cdf(chi2_stab, ndf_stab)) if ndf_stab > 0 else 1.0

        log.info("Combined: R_b = %.5f +/- %.5f", rb_combined, sigma_combined)
        log.info("Stability: chi2/ndf = %.1f/%d, p = %.4f",
                 chi2_stab, ndf_stab, p_stab)
    else:
        best = None
        rb_combined = None
        sigma_combined = None
        chi2_stab = 0.0
        ndf_stab = 0
        p_stab = 1.0

    return {
        "all_results": all_results,
        "best_config": best,
        "combined": {
            "R_b": rb_combined,
            "sigma_stat": sigma_combined,
        },
        "stability": {
            "chi2": chi2_stab,
            "ndf": ndf_stab,
            "p_value": p_stab,
        },
    }


# ======================================================================
# Step 6: Re-extract A_FB^b with calibrated purities
# ======================================================================

def extract_afb_calibrated(smeared_mc_tags, data_10pct_tags):
    """Estimate b-purity changes from smeared MC for A_FB^b correction.

    The MC truth flavour (bflag) is not available in this dataset (sentinel
    -999 for all events). Instead, compute purity from the calibrated
    efficiencies: f_b = eps_b * R_b / f_s.
    """
    log.info("\n--- Step 6: A_FB^b Purity Estimation ---")

    mc_h0 = smeared_mc_tags["combined_h0"]
    mc_h1 = smeared_mc_tags["combined_h1"]

    mc_orig = np.load(P3_OUT / "hemisphere_tags.npz", allow_pickle=False)
    mc_orig_h0 = mc_orig["mc_combined_h0"]
    mc_orig_h1 = mc_orig["mc_combined_h1"]

    thresholds = [3.0, 5.0, 7.0, 8.0, 10.0]
    purity_results = {}

    for thr in thresholds:
        # Compute tag rates and efficiency-based purity
        # f_s = eps_b * R_b + eps_c * R_c + eps_uds * R_uds
        # f_b = eps_b * R_b / f_s
        # Use the 3-tag calibration to get eps_b at this threshold

        # Original MC
        f_s_orig = (np.sum(mc_orig_h0 > thr) + np.sum(mc_orig_h1 > thr)) / (2 * len(mc_orig_h0))
        # Smeared MC
        f_s_smeared = (np.sum(mc_h0 > thr) + np.sum(mc_h1 > thr)) / (2 * len(mc_h0))

        # Get efficiencies from 3-tag calibration at (thr, thr-3)
        thr_l = max(thr - 3.0, 2.0)
        counts_orig = count_three_tag(mc_orig_h0, mc_orig_h1, thr, thr_l)
        cal_orig = calibrate_three_tag_efficiencies(counts_orig, R_B_SM, R_C_SM)
        counts_smeared = count_three_tag(mc_h0, mc_h1, thr, thr_l)
        cal_smeared = calibrate_three_tag_efficiencies(counts_smeared, R_B_SM, R_C_SM)

        f_b_orig = cal_orig["eps_b_tight"] * R_B_SM / f_s_orig if f_s_orig > 0 else 0
        f_b_smeared = cal_smeared["eps_b_tight"] * R_B_SM / f_s_smeared if f_s_smeared > 0 else 0

        purity_results[str(thr)] = {
            "f_b_original": float(f_b_orig),
            "f_b_smeared": float(f_b_smeared),
            "f_s_original": float(f_s_orig),
            "f_s_smeared": float(f_s_smeared),
            "eps_b_tight_orig": float(cal_orig["eps_b_tight"]),
            "eps_b_tight_smeared": float(cal_smeared["eps_b_tight"]),
        }

        log.info("WP=%.1f: f_b_orig=%.4f, f_b_smeared=%.4f "
                 "(f_s: %.5f -> %.5f, eps_b: %.4f -> %.4f)",
                 thr, f_b_orig, f_b_smeared,
                 f_s_orig, f_s_smeared,
                 cal_orig["eps_b_tight"], cal_smeared["eps_b_tight"])

    return purity_results


# ======================================================================
# Step 7: Compare all approaches
# ======================================================================

def compare_approaches(raw_results, smeared_results, sf_results):
    """Compare R_b from all approaches."""
    log.info("\n" + "=" * 60)
    log.info("Step 7: Comparison of All Approaches")
    log.info("=" * 60)

    # Load existing results
    existing_path = PHASE4B_OUT / "three_tag_rb_10pct.json"
    if existing_path.exists():
        with open(existing_path) as f:
            existing = json.load(f)
        raw_rb = existing.get("best_config", {}).get("R_b")
        raw_sigma = existing.get("best_config", {}).get("sigma_stat")
    else:
        raw_rb = None
        raw_sigma = None

    # Also load 2-tag result if available
    rb_2tag_path = PHASE4B_OUT / "rb_results_10pct.json"
    if rb_2tag_path.exists():
        with open(rb_2tag_path) as f:
            rb_2tag = json.load(f)
        # Find published C_b result
        strategies = rb_2tag.get("strategies", {})
        pub_strat = strategies.get("published_Cb", {})
        rb_2tag_val = pub_strat.get("stability", {}).get("R_b_combined")
        rb_2tag_sigma = pub_strat.get("stability", {}).get("sigma_combined")
    else:
        rb_2tag_val = None
        rb_2tag_sigma = None

    smeared_rb = smeared_results.get("stability", {}).get("R_b_combined")
    smeared_sigma = smeared_results.get("stability", {}).get("sigma_combined")
    smeared_best = smeared_results.get("best_config")

    sf_rb = sf_results.get("combined", {}).get("R_b")
    sf_sigma = sf_results.get("combined", {}).get("sigma_stat")
    sf_best = sf_results.get("best_config")

    comparison = {
        "SM_R_b": R_B_SM,
        "approaches": [],
    }

    approaches = [
        ("3-tag raw MC eff", raw_rb, raw_sigma),
        ("3-tag smeared MC eff", smeared_rb, smeared_sigma),
        ("3-tag SF-corrected eff", sf_rb, sf_sigma),
        ("2-tag C_b=1.01", rb_2tag_val, rb_2tag_sigma),
    ]

    log.info("\n%-30s  %-10s  %-10s  %-10s", "Approach", "R_b", "sigma", "Pull(SM)")
    log.info("-" * 70)

    for name, rb, sigma in approaches:
        if rb is not None:
            pull = abs(rb - R_B_SM) / sigma if sigma and sigma > 0 else float('inf')
            log.info("%-30s  %-10.5f  %-10.5f  %-10.2f", name, rb, sigma or 0, pull)
        else:
            log.info("%-30s  %-10s  %-10s  %-10s", name, "N/A", "N/A", "N/A")

        comparison["approaches"].append({
            "name": name,
            "R_b": float(rb) if rb is not None else None,
            "sigma_stat": float(sigma) if sigma is not None else None,
            "pull_from_SM": float(abs(rb - R_B_SM) / sigma) if rb is not None and sigma and sigma > 0 else None,
        })

    # Summary
    log.info("\n--- Summary ---")
    if smeared_rb is not None and raw_rb is not None:
        improvement = abs(raw_rb - R_B_SM) - abs(smeared_rb - R_B_SM)
        log.info("Smearing improvement: %.5f (bias reduction)", improvement)
        if improvement > 0:
            log.info("  -> Smearing REDUCES the bias toward SM")
        else:
            log.info("  -> Smearing does NOT reduce the bias")

    return comparison


# ======================================================================
# Main
# ======================================================================

def main():
    log.info("=" * 60)
    log.info("Data-Driven MC Efficiency Calibration via d0 Smearing")
    log.info("=" * 60)

    # Step 1: Measure mismatch
    mismatch = measure_resolution_mismatch()

    # Step 2: Smear MC d0
    d0_smeared, smeared_signed_sig, mc, smear_diag = smear_mc_d0(mismatch)

    # Step 3: Recompute tags
    smeared_mc_tags = recompute_mc_tags(smeared_signed_sig, mc)

    # Load 10% data tags
    data_10pct_tags = np.load(
        PHASE4B_OUT / "data_10pct_tags.npz", allow_pickle=False)

    # Step 4: Extract R_b with smeared efficiencies
    smeared_results = extract_rb_smeared(smeared_mc_tags, data_10pct_tags)

    # Step 5: Tag-rate scale factors
    sf_results = tag_rate_scale_factors(data_10pct_tags)

    # Step 6: A_FB^b with calibrated purities
    purity_results = extract_afb_calibrated(smeared_mc_tags, data_10pct_tags)

    # Step 7: Compare all approaches
    comparison = compare_approaches(None, smeared_results, sf_results)

    # ================================================================
    # Save comprehensive output
    # ================================================================
    output = {
        "description": (
            "Data-driven MC efficiency calibration via d0 smearing. "
            "Standard ALEPH approach (inspire_433306): calibrate MC "
            "tracking resolution to match data, re-derive efficiencies."
        ),
        "step1_mismatch": {
            "mean_ratio": float(np.mean([v["ratio_data_mc"] for v in mismatch.values()])),
            "median_ratio": float(np.median([v["ratio_data_mc"] for v in mismatch.values()])),
            "per_bin": mismatch,
        },
        "step2_smearing": smear_diag,
        "step4_smeared_extraction": smeared_results,
        "step5_scale_factor_extraction": sf_results,
        "step6_purity_calibration": purity_results,
        "step7_comparison": comparison,
    }

    out_path = PHASE4B_OUT / "d0_smearing_results.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    log.info("\nSaved %s", out_path.name)

    # Update parameters.json
    params_path = RESULTS_DIR / "parameters.json"
    if params_path.exists():
        with open(params_path) as f:
            params = json.load(f)
    else:
        params = {}

    if smeared_results.get("best_config"):
        best = smeared_results["best_config"]
        params["R_b_10pct_3tag_smeared"] = {
            "value": best["R_b"],
            "stat": best["sigma_stat"],
            "SM": R_B_SM,
            "method": "3-tag smeared MC efficiencies, 10% data",
            "working_point": best["label"],
        }
    if smeared_results.get("stability", {}).get("R_b_combined") is not None:
        params["R_b_10pct_3tag_smeared_combined"] = {
            "value": smeared_results["stability"]["R_b_combined"],
            "stat": smeared_results["stability"]["sigma_combined"],
            "SM": R_B_SM,
            "method": "3-tag smeared MC combined, 10% data",
        }
    if sf_results.get("best_config"):
        best_sf = sf_results["best_config"]
        params["R_b_10pct_3tag_sf"] = {
            "value": best_sf["R_b"],
            "stat": best_sf["sigma_stat"],
            "SM": R_B_SM,
            "method": "3-tag SF-corrected efficiencies, 10% data",
            "working_point": best_sf["label"],
        }

    with open(params_path, "w") as f:
        json.dump(params, f, indent=2)
    log.info("Updated parameters.json")

    log.info("\n" + "=" * 60)
    log.info("DONE: d0 smearing calibration complete")
    log.info("=" * 60)


if __name__ == "__main__":
    main()
