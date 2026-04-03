"""Phase 4b: Full analysis chain on 10% data subsample.

Reuses Phase 3 and Phase 4a infrastructure. Runs:
1. 10% data subsample selection (seed 42)
2. Preselection + track quality
3. sigma_d0 calibration on 10% data
4. Signed d0 computation
5. Hemisphere tagging
6. Jet charge computation
7. Hemisphere correlation on 10% data
8. R_b extraction (using MC-calibrated efficiencies from Phase 4a)
9. A_FB^b extraction
10. Systematic re-evaluation on 10% data
11. Comparison to Phase 4a expected

Reads: Phase 3 outputs (NPZ), Phase 4a outputs (JSON), raw data ROOT files
Writes: outputs/*.json, outputs/*.npz
"""
import json
import logging
import sys
from pathlib import Path

import numpy as np
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

HERE = Path(__file__).resolve().parent
PHASE4B_OUT = HERE.parent / "outputs"
PHASE4B_OUT.mkdir(parents=True, exist_ok=True)

P3_ROOT = HERE.parents[2] / "phase3_selection"
P3_SRC = P3_ROOT / "src"
P3_OUT = P3_ROOT / "outputs"

P4A_OUT = HERE.parents[1] / "4a_expected" / "outputs"

RESULTS_DIR = HERE.parents[2] / "analysis_note" / "results"

# Add Phase 3 and Phase 4a source directories to path for imports
sys.path.insert(0, str(P3_SRC))
sys.path.insert(0, str(HERE.parents[1] / "4a_expected" / "src"))

DATA_DIR = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPH/")
MC_DIR = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPHMC/")

# 10% subsample parameters
SUBSAMPLE_SEED = 42
SUBSAMPLE_FRACTION = 0.10

# SM values (same as Phase 4a)
R_B_SM = 0.21578
R_C_SM = 0.17223
R_C_ERR = 0.0030
G_BB = 0.00251
G_BB_ERR = 0.00063
G_CC = 0.0296
G_CC_ERR = 0.0038

N_TOYS = 1000
TOY_SEED = 54321

KAPPA_VALUES = [0.3, 0.5, 1.0, 2.0]
N_COS_BINS = 10
COS_RANGE = (-0.9, 0.9)

# QCD/QED corrections (same as Phase 4a)
DELTA_QCD = 0.0356
DELTA_QCD_ERR = 0.0029
DELTA_QED = 0.001


def subsample_events(n_events, fraction, seed):
    """Select a random fraction of events with fixed seed.

    Returns boolean mask of selected events.
    """
    rng = np.random.RandomState(seed)
    mask = rng.random(n_events) < fraction
    log.info("Subsample: %d / %d events selected (%.1f%%)",
             np.sum(mask), n_events, 100.0 * np.sum(mask) / n_events)
    return mask


def load_preselected_10pct():
    """Load Phase 3 preselected data and select 10% subsample."""
    log.info("Loading Phase 3 preselected data...")
    data = np.load(P3_OUT / "preselected_data.npz", allow_pickle=False)
    mc = np.load(P3_OUT / "preselected_mc.npz", allow_pickle=False)

    n_data = len(data["thrust"])
    log.info("Full data: %d events", n_data)

    # Select 10% subsample with seed 42
    mask_10pct = subsample_events(n_data, SUBSAMPLE_FRACTION, SUBSAMPLE_SEED)

    return data, mc, mask_10pct


def subsample_track_arrays(data, mask, track_prefix="trk"):
    """Subsample track-level jagged arrays given an event-level mask.

    Returns new flat arrays and offsets for the subsampled events.
    """
    result = {}
    # Event-level arrays
    for key in data.files:
        if key.startswith(f"{track_prefix}_") and key.endswith("_offsets"):
            continue
        if key.startswith(f"{track_prefix}_"):
            continue
        if key.startswith("alltrk_") and key.endswith("_offsets"):
            continue
        if key.startswith("alltrk_"):
            continue
        # Event-level array
        arr = data[key]
        if len(arr) == len(mask):
            result[key] = arr[mask]

    # Track-level jagged arrays
    for prefix in [track_prefix, "alltrk"]:
        # Find all track branches by looking for _offsets keys
        offset_keys = [k for k in data.files if k.startswith(f"{prefix}_") and k.endswith("_offsets")]
        for off_key in offset_keys:
            base = off_key[:-len("_offsets")]
            if base not in data.files:
                continue
            offsets = data[off_key]
            flat = data[base]

            # Build new offsets and flat arrays for subsampled events
            event_indices = np.where(mask)[0]
            new_counts = []
            new_flat_parts = []
            for idx in event_indices:
                start, end = offsets[idx], offsets[idx + 1]
                new_counts.append(end - start)
                new_flat_parts.append(flat[start:end])

            if new_flat_parts:
                new_flat = np.concatenate(new_flat_parts)
            else:
                new_flat = np.array([], dtype=flat.dtype)

            new_offsets = np.zeros(len(new_counts) + 1, dtype=np.int64)
            np.cumsum(new_counts, out=new_offsets[1:])

            result[base] = new_flat
            result[off_key] = new_offsets

    return result


def run_sigma_d0_calibration(data_10pct):
    """Run sigma_d0 calibration on 10% data subsample.

    Reuses Phase 3 calibration code/infrastructure.
    """
    from sigma_d0_calibration import (
        compute_sigma_d0, calibrate_bin, A_INIT, B_INIT,
        P_BINS, COSTHETA_BINS, NVDET_CLASSES
    )

    d0_flat = data_10pct["trk_d0"]
    offsets = data_10pct["trk_d0_offsets"]
    pmag_flat = data_10pct["trk_pmag"]
    theta_flat = data_10pct["trk_theta"]
    nvdet_flat = data_10pct["trk_nvdet"]
    cos_theta_thrust = data_10pct["cos_theta_thrust"]

    n_events = len(offsets) - 1
    trk_cos_thrust = np.empty_like(d0_flat)
    for i in range(n_events):
        start, end = offsets[i], offsets[i + 1]
        trk_cos_thrust[start:end] = cos_theta_thrust[i]

    sigma_d0_nom = compute_sigma_d0(pmag_flat, theta_flat, A_INIT, B_INIT)
    scale_factors = np.ones_like(d0_flat)
    calibration_results = {}

    for nv in NVDET_CLASSES:
        nv_mask = nvdet_flat >= nv if nv == 2 else nvdet_flat == nv
        for ip, (p_lo, p_hi) in enumerate(zip(P_BINS[:-1], P_BINS[1:])):
            p_mask = (pmag_flat >= p_lo) & (pmag_flat < p_hi)
            for ic, (ct_lo, ct_hi) in enumerate(zip(COSTHETA_BINS[:-1], COSTHETA_BINS[1:])):
                ct_mask = (np.abs(trk_cos_thrust) >= ct_lo) & (np.abs(trk_cos_thrust) < ct_hi)
                bin_mask = nv_mask & p_mask & ct_mask
                n_in_bin = int(np.sum(bin_mask))
                label = f"nv{nv}_p{ip}_ct{ic}"
                if n_in_bin < 50:
                    calibration_results[label] = {
                        "nvdet": nv, "p_range": [p_lo, p_hi],
                        "costheta_range": [ct_lo, ct_hi],
                        "n_tracks": n_in_bin, "scale_factor": 1.0,
                    }
                    continue
                scale, neg_width, n_neg = calibrate_bin(
                    d0_flat[bin_mask], sigma_d0_nom[bin_mask], label=label)
                scale_factors[bin_mask] = scale
                calibration_results[label] = {
                    "nvdet": nv, "p_range": [p_lo, p_hi],
                    "costheta_range": [ct_lo, ct_hi],
                    "n_tracks": n_in_bin, "scale_factor": float(scale),
                    "neg_width": float(neg_width) if not np.isnan(neg_width) else None,
                }

    sigma_d0_corrected = sigma_d0_nom * scale_factors
    significance = d0_flat / sigma_d0_corrected

    return calibration_results, sigma_d0_corrected, significance


def compute_signed_d0(data_10pct, significance):
    """Compute signed d0 significance for 10% data.

    Reuses Phase 3 sign convention: PCA-jet angle method.
    """
    d0 = data_10pct["trk_d0"]
    phi = data_10pct["trk_phi"]
    dot_thrust = data_10pct["trk_dot_thrust"]

    # Sign = sign of (PCA direction dot jet direction)
    # PCA direction is (d0*sin(phi), -d0*cos(phi)) in the transverse plane
    # For the sign, we use dot_thrust (dot product of track momentum with thrust)
    # as a proxy for hemisphere assignment, and the PCA-jet angle.
    # The signed significance is |d0/sigma| * sign(dot_PCA . jet)
    # Simplified: sign based on dot product of track with thrust axis
    # Positive = track displaced along jet direction (b/c decay signature)

    # Following Phase 3 d0_sign_validation.py approach:
    # signed_d0 = |d0| * sign(PCA_direction dot jet_direction)
    # For tracks in positive thrust hemisphere (dot_thrust > 0):
    #   PCA_direction ~ (d0*sin(phi), -d0*cos(phi))
    #   jet_direction ~ thrust direction in that hemisphere
    # Simplified: use the sign from d0 * sign(cos(track_angle_to_jet))

    # Actually, for the Phase 3 pipeline, signed d0 was computed in
    # debug_sign_d0_v4.py. Let's replicate that approach.
    # The key insight: d0 from the ntuple has an angular-momentum sign.
    # The physics sign is determined by whether the track's PCA lies
    # on the same side as the jet direction.

    # From debug_sign_d0_v4.py, the sign is:
    # sign_factor = np.sign(d0 * np.sin(phi) * thrust_x - d0 * np.cos(phi) * thrust_y)
    # where (thrust_x, thrust_y) is the thrust axis transverse direction in the hemisphere

    # For simplicity and consistency with Phase 3, we just sign by
    # the product of d0 and the dot product with thrust
    # This works because d0 > 0 for tracks displaced along the jet
    # after the angular-momentum sign is absorbed.

    abs_sig = np.abs(significance)
    # Use the Phase 3 convention: positive significance means displaced vertex
    # The Phase 3 signed_d0.npz already computed this correctly.
    # For the 10% subsample, we recompute from the same formula.

    # Phase 3 debug_sign_d0_v4.py uses:
    # For each track: signed_d0 = |d0| * sign(PCA . jet)
    # where PCA = (d0*sin(phi), -d0*cos(phi)), jet = thrust axis in hemisphere

    # Since we have the preselected data with hemisphere assignments,
    # we can compute this directly.
    # The trk_dot_thrust gives us which hemisphere the track is in,
    # and its projection onto the thrust axis.

    # Actually for b-tagging the sign convention is already embedded in
    # Phase 3's signed_d0.npz through the full procedure. Let's load
    # Phase 3's signed significances and subsample them.

    return significance  # Will be overridden below


def compute_hemisphere_tags_10pct(signed_sig, data_10pct):
    """Compute hemisphere probability and mass tags for 10% data.

    Reuses Phase 3 hemisphere_tag.py infrastructure.
    """
    from hemisphere_tag import (
        build_resolution_cdf, compute_hemisphere_tags_vectorized
    )

    offsets = data_10pct["trk_d0_offsets"]
    hem = data_10pct["trk_hem"]
    pmag = data_10pct["trk_pmag"]
    theta = data_10pct["trk_theta"]
    phi = data_10pct["trk_phi"]

    # Build resolution function from negative tail of 10% data
    neg_sig = signed_sig[signed_sig < 0]
    log.info("10%% data negative tail: %d tracks", len(neg_sig))
    bin_edges, survival = build_resolution_cdf(neg_sig)

    tags = compute_hemisphere_tags_vectorized(
        signed_sig, offsets, hem, pmag, theta, phi, bin_edges, survival
    )
    return tags


def compute_jet_charge_10pct(data_10pct):
    """Compute hemisphere jet charge for 10% data.

    Reuses Phase 3 jet_charge.py infrastructure.
    """
    from jet_charge import (
        compute_jet_charge_vectorized, compute_leading_charge_vectorized
    )

    charge = data_10pct["alltrk_charge"]
    offsets = data_10pct["alltrk_charge_offsets"]
    hem = data_10pct["alltrk_hem"]
    dot_thrust = data_10pct["alltrk_dot_thrust"]
    cos_theta = data_10pct["cos_theta_thrust"]
    pL = dot_thrust

    results = {}
    for kappa in KAPPA_VALUES:
        k_str = f"k{kappa:.1f}"
        qh_h0, qh_h1, qfb = compute_jet_charge_vectorized(
            charge, pL, offsets, hem, cos_theta, kappa)
        results[f"qh_h0_{k_str}"] = qh_h0
        results[f"qh_h1_{k_str}"] = qh_h1
        results[f"qfb_{k_str}"] = qfb

    # kappa = infinity
    qh_h0_inf, qh_h1_inf, qfb_inf = compute_leading_charge_vectorized(
        charge, pL, offsets, hem, cos_theta)
    results["qh_h0_kinf"] = qh_h0_inf
    results["qh_h1_kinf"] = qh_h1_inf
    results["qfb_kinf"] = qfb_inf

    return results, cos_theta


def compute_hemisphere_correlation_10pct(data_tags):
    """Compute C_b on 10% data."""
    from hemisphere_correlation import compute_correlation

    h0 = data_tags["combined_h0"]
    h1 = data_tags["combined_h1"]

    thresholds = [5.0, 7.0, 8.0, 10.0]
    corr_results = []
    for thr in thresholds:
        C, sigma_C, N_d = compute_correlation(h0, h1, thr)
        corr_results.append({
            'threshold': float(thr),
            'C': float(C) if not np.isnan(C) else None,
            'sigma_C': float(sigma_C) if not np.isnan(sigma_C) else None,
            'N_tt': int(N_d),
        })
        log.info("C_b(WP=%.1f) = %.4f +/- %.4f (N_tt=%d)",
                 thr, C, sigma_C, N_d)

    return corr_results


def extract_rb_10pct(data_tags, mc_cal, corr_4a):
    """Extract R_b from 10% data using Phase 4a MC calibration.

    This is the CRITICAL test: with real data, the double-tag self-calibrating
    property should produce a less biased result than the circular MC calibration.
    """
    from rb_extraction import extract_rb, count_tags, apply_gluon_correction, toy_uncertainty

    h0 = data_tags["combined_h0"]
    h1 = data_tags["combined_h1"]

    # Use C_b from Phase 4a (MC-estimated)
    C_b = corr_4a['summary']['C_b_nominal']
    C_b_syst = corr_4a['summary']['C_b_syst']

    thresholds = [7.0, 8.0, 9.0, 10.0]
    full_cal = mc_cal['full_mc_calibration']

    extraction_results = []
    log.info("\n--- R_b Extraction from 10%% Data ---")
    log.info("%-8s  %-10s  %-10s  %-10s  %-10s  %-10s  %-10s",
             "WP", "R_b", "sigma_stat", "eps_b", "f_s", "f_d", "N_had")

    for thr in thresholds:
        thr_str = str(float(thr))
        if thr_str not in full_cal:
            log.warning("WP %.1f: no MC calibration available", thr)
            continue

        cal_wp = full_cal[thr_str]
        eps_c = cal_wp['eps_c']
        eps_uds = cal_wp['eps_uds']
        eps_uds_eff = apply_gluon_correction(eps_uds, eps_c, G_BB, G_CC)

        N_had, N_t, N_tt, f_s, f_d = count_tags(h0, h1, thr)
        R_b, eps_b = extract_rb(f_s, f_d, eps_c, eps_uds_eff, R_C_SM, C_b)

        # Toy-based uncertainty
        rb_mean, rb_sigma, _, n_valid = toy_uncertainty(
            h0, h1, thr, eps_c, eps_uds_eff, R_C_SM, C_b,
            n_toys=N_TOYS, seed=TOY_SEED)

        if not np.isnan(R_b):
            log.info("%-8.1f  %-10.5f  %-10.5f  %-10.4f  %-10.5f  %-10.6f  %-10d",
                     thr, R_b, rb_sigma if not np.isnan(rb_sigma) else 0.0,
                     eps_b, f_s, f_d, N_had)
        else:
            log.info("%-8.1f  null      --         --         %-10.5f  %-10.6f  %-10d",
                     thr, f_s, f_d, N_had)

        extraction_results.append({
            'threshold': float(thr),
            'R_b': float(R_b) if not np.isnan(R_b) else None,
            'sigma_stat': float(rb_sigma) if not np.isnan(rb_sigma) else None,
            'eps_b': float(eps_b) if not np.isnan(eps_b) else None,
            'eps_c': float(eps_c),
            'eps_uds_eff': float(eps_uds_eff),
            'f_s': float(f_s),
            'f_d': float(f_d),
            'N_had': N_had,
            'N_t': N_t,
            'N_tt': N_tt,
            'C_b': float(C_b),
            'n_valid_toys': n_valid,
        })

    # Select best working point
    valid_extractions = [r for r in extraction_results
                         if r['R_b'] is not None and r['sigma_stat'] is not None
                         and 0.05 < r['R_b'] < 0.5]
    if valid_extractions:
        best = min(valid_extractions, key=lambda x: x['sigma_stat'])
        log.info("\n--- Best WP for 10%% data ---")
        log.info("WP = %.1f", best['threshold'])
        log.info("R_b = %.5f +/- %.5f (stat)", best['R_b'], best['sigma_stat'])
        log.info("SM R_b = %.5f", R_B_SM)
        dev = abs(best['R_b'] - R_B_SM) / best['sigma_stat'] if best['sigma_stat'] > 0 else float('inf')
        log.info("Deviation from SM: %.2f sigma", dev)
    else:
        best = None
        log.warning("No valid R_b extraction on 10%% data!")

    # Operating point stability
    valid_rb = [r for r in extraction_results
                if r['R_b'] is not None and r['sigma_stat'] is not None
                and r['sigma_stat'] > 0]
    if len(valid_rb) >= 2:
        rb_vals = np.array([r['R_b'] for r in valid_rb])
        rb_errs = np.array([r['sigma_stat'] for r in valid_rb])
        w = 1.0 / rb_errs**2
        rb_combined = float(np.sum(w * rb_vals) / np.sum(w))
        sigma_combined = float(1.0 / np.sqrt(np.sum(w)))
        chi2 = float(np.sum((rb_vals - rb_combined)**2 / rb_errs**2))
        ndf = len(valid_rb) - 1
        from scipy.stats import chi2 as chi2_dist
        p_value = float(1.0 - chi2_dist.cdf(chi2, ndf))
        stability_passes = p_value > 0.05
    else:
        rb_combined = best['R_b'] if best else None
        sigma_combined = best['sigma_stat'] if best else None
        chi2, ndf, p_value = 0.0, 0, None
        stability_passes = False

    return {
        'extraction_results': extraction_results,
        'best_wp': best,
        'stability': {
            'R_b_combined': rb_combined,
            'sigma_combined': sigma_combined,
            'chi2': chi2,
            'ndf': ndf,
            'p_value': p_value,
            'passes': stability_passes,
            'n_valid_wp': len(valid_rb),
        },
    }


def extract_afb_10pct(jc_results, cos_theta, data_tags):
    """Extract A_FB^b from 10% data.

    With real data, the forward-backward asymmetry should be nonzero
    (expected ~0.09 from published ALEPH result).
    """
    from afb_extraction import (
        extract_afb_simple, self_calibrating_fit, extract_delta_b,
        afb_measured_to_pole, sin2theta_to_afb0
    )

    h0 = data_tags["combined_h0"]
    h1 = data_tags["combined_h1"]

    ref_threshold = 5.0
    fit_thresholds = [3.0, 5.0, 7.0, 9.0]

    all_kappa_results = []

    for kappa in KAPPA_VALUES:
        k_str = f"k{kappa:.1f}"
        log.info("\n--- kappa = %.1f (10%% data) ---", kappa)

        qfb = jc_results[f"qfb_{k_str}"]
        qh0 = jc_results[f"qh_h0_{k_str}"]
        qh1 = jc_results[f"qh_h1_{k_str}"]

        simple = extract_afb_simple(
            qfb, cos_theta, h0, h1, ref_threshold)

        if simple:
            log.info("Simple fit: slope = %.6f +/- %.6f, "
                     "intercept = %.6f, chi2/ndf = %.2f/%d, p = %.3f",
                     simple['slope'], simple['sigma_slope'],
                     simple.get('intercept', 0.0),
                     simple['chi2'], simple['ndf'], simple['p_value'])

        selfcal = self_calibrating_fit(
            qfb, cos_theta, h0, h1, fit_thresholds, k_str)

        delta_info = extract_delta_b(qh0, qh1, h0, h1, ref_threshold)

        kappa_result = {
            'kappa': float(kappa),
            'simple_fit': simple,
            'self_calibrating_fit': selfcal,
            'delta_b_info': delta_info,
        }

        if simple and delta_info and delta_info['delta_b_estimate'] > 0:
            delta_b = delta_info['delta_b_estimate']
            afb_b = simple['slope'] / delta_b
            sigma_afb = simple['sigma_slope'] / delta_b
            afb_0_b = afb_measured_to_pole(afb_b)

            kappa_result['A_FB_b'] = float(afb_b)
            kappa_result['sigma_A_FB_b'] = float(sigma_afb)
            kappa_result['A_FB_0_b'] = float(afb_0_b)
            kappa_result['delta_b'] = float(delta_b)

            log.info("A_FB^b = %.4f +/- %.4f, delta_b = %.3f",
                     afb_b, sigma_afb, delta_b)

        all_kappa_results.append(kappa_result)

    # kappa = infinity
    log.info("\n--- kappa = infinity (10%% data) ---")
    qfb_inf = jc_results["qfb_kinf"]
    qh0_inf = jc_results["qh_h0_kinf"]
    qh1_inf = jc_results["qh_h1_kinf"]

    simple_inf = extract_afb_simple(
        qfb_inf, cos_theta, h0, h1, ref_threshold)
    delta_inf = extract_delta_b(qh0_inf, qh1_inf, h0, h1, ref_threshold)

    inf_result = {
        'kappa': float('inf'),
        'simple_fit': simple_inf,
        'self_calibrating_fit': None,
        'delta_b_info': delta_inf,
    }
    if simple_inf and delta_inf and delta_inf['delta_b_estimate'] > 0:
        delta_b = delta_inf['delta_b_estimate']
        afb_b = simple_inf['slope'] / delta_b
        sigma_afb = simple_inf['sigma_slope'] / delta_b
        afb_0_b = afb_measured_to_pole(afb_b)
        inf_result['A_FB_b'] = float(afb_b)
        inf_result['sigma_A_FB_b'] = float(sigma_afb)
        inf_result['A_FB_0_b'] = float(afb_0_b)
        inf_result['delta_b'] = float(delta_b)
        if delta_b < 0.1:
            inf_result['demoted'] = True
        else:
            inf_result['demoted'] = False

    all_kappa_results.append(inf_result)

    # Kappa consistency
    afb_vals = []
    afb_errs = []
    kappa_list = []
    for kr in all_kappa_results:
        if 'A_FB_b' in kr and kr.get('sigma_A_FB_b', 0) > 0:
            if kr.get('demoted', False):
                continue
            afb_vals.append(kr['A_FB_b'])
            afb_errs.append(kr['sigma_A_FB_b'])
            kappa_list.append(kr['kappa'])

    if len(afb_vals) >= 2:
        afb_arr = np.array(afb_vals)
        err_arr = np.array(afb_errs)
        w = 1.0 / err_arr**2
        afb_combined = float(np.sum(w * afb_arr) / np.sum(w))
        sigma_combined = float(1.0 / np.sqrt(np.sum(w)))
        chi2_kappa = float(np.sum((afb_arr - afb_combined)**2 / err_arr**2))
        ndf_kappa = len(afb_vals) - 1
        from scipy.stats import chi2 as chi2_dist
        p_kappa = float(1.0 - chi2_dist.cdf(chi2_kappa, ndf_kappa)) if ndf_kappa > 0 else None
        afb_0_combined = float(afb_measured_to_pole(afb_combined))
    else:
        afb_combined = afb_vals[0] if afb_vals else None
        sigma_combined = afb_errs[0] if afb_errs else None
        afb_0_combined = float(afb_measured_to_pole(afb_combined)) if afb_combined else None
        chi2_kappa, ndf_kappa, p_kappa = 0.0, 0, None

    log.info("\n--- Kappa Consistency (10%% data) ---")
    if afb_combined is not None:
        log.info("Combined A_FB^b = %.4f +/- %.4f", afb_combined, sigma_combined)
        log.info("A_FB^{0,b} = %.5f", afb_0_combined)
        if p_kappa is not None:
            log.info("Kappa chi2/ndf = %.2f / %d, p = %.3f",
                     chi2_kappa, ndf_kappa, p_kappa)

    # sin^2(theta_eff) from A_FB^{0,b}
    sin2theta_fit = None
    sigma_sin2theta = None
    if afb_0_combined is not None and afb_0_combined != 0.0:
        from scipy.optimize import brentq
        try:
            sin2theta_fit = float(brentq(
                lambda s: sin2theta_to_afb0(s) - afb_0_combined, 0.20, 0.26))
            # Propagate uncertainty
            pole_sigma = sigma_combined / (1.0 - DELTA_QCD - DELTA_QED)
            sin2theta_up = float(brentq(
                lambda s: sin2theta_to_afb0(s) - (afb_0_combined - pole_sigma),
                0.20, 0.26))
            sin2theta_dn = float(brentq(
                lambda s: sin2theta_to_afb0(s) - (afb_0_combined + pole_sigma),
                0.20, 0.26))
            sigma_sin2theta = abs(sin2theta_up - sin2theta_dn) / 2.0
            log.info("sin^2(theta_eff) = %.5f +/- %.5f",
                     sin2theta_fit, sigma_sin2theta)
        except Exception as e:
            log.warning("sin^2(theta_eff) inversion failed: %s", e)

    return {
        'kappa_results': all_kappa_results,
        'combination': {
            'A_FB_b': afb_combined,
            'sigma_A_FB_b': sigma_combined,
            'A_FB_0_b': afb_0_combined,
            'chi2_kappa': chi2_kappa,
            'ndf_kappa': ndf_kappa,
            'p_kappa': p_kappa,
            'kappas_used': kappa_list,
        },
        'sin2theta': {
            'value': sin2theta_fit,
            'sigma_stat': sigma_sin2theta,
            'SM': 0.23153,
        },
    }


def evaluate_systematics_10pct(rb_results, afb_results, data_tags, mc_cal, corr_4a):
    """Re-evaluate systematics on 10% data."""
    from rb_extraction import extract_rb, count_tags, apply_gluon_correction

    h0 = data_tags["combined_h0"]
    h1 = data_tags["combined_h1"]

    best = rb_results['best_wp']
    if best is None:
        log.warning("No valid R_b extraction; cannot evaluate systematics")
        return None

    REF_WP = best['threshold']
    R_b_nom = best['R_b']
    eps_c_nom = best['eps_c']
    eps_uds_nom = best['eps_uds_eff']
    C_b_nom = best['C_b']

    N_had, N_t, N_tt, f_s, f_d = count_tags(h0, h1, REF_WP)

    def shift_rb(eps_c, eps_uds, R_c, C_b):
        R_b_var, _ = extract_rb(f_s, f_d, eps_c, eps_uds, R_c, C_b)
        if np.isnan(R_b_var):
            return None
        return float(R_b_var - R_b_nom)

    systematics = {}

    # sigma_d0 (borrowed, scaled)
    systematics['sigma_d0'] = {
        'delta_Rb': 0.00075,
        'method': 'Scaled from ALEPH (0.00050) x1.5',
        'source': 'hep-ex/9609005',
    }

    # sigma_d0 form
    systematics['sigma_d0_form'] = {
        'delta_Rb': 0.00040,
        'method': 'sin(theta) vs sin^{3/2}(theta)',
        'source': 'STRATEGY.md 5.1',
    }

    # C_b
    C_b_syst = corr_4a['summary']['C_b_syst']
    shift_up = shift_rb(eps_c_nom, eps_uds_nom, R_C_SM, C_b_nom + C_b_syst)
    shift_down = shift_rb(eps_c_nom, eps_uds_nom, R_C_SM, C_b_nom - C_b_syst)
    delta_Cb = max(abs(shift_up or 0), abs(shift_down or 0))
    systematics['C_b'] = {
        'delta_Rb': delta_Cb,
        'shift_up': shift_up, 'shift_down': shift_down,
        'method': 'Re-extraction with varied C_b',
    }

    # eps_c (+/- 30%)
    eps_c_var = 0.30 * eps_c_nom
    shift_up = shift_rb(eps_c_nom + eps_c_var, eps_uds_nom, R_C_SM, C_b_nom)
    shift_down = shift_rb(eps_c_nom - eps_c_var, eps_uds_nom, R_C_SM, C_b_nom)
    systematics['eps_c'] = {
        'delta_Rb': max(abs(shift_up or 0), abs(shift_down or 0)),
        'shift_up': shift_up, 'shift_down': shift_down,
    }

    # eps_uds (+/- 50%)
    eps_uds_var = 0.50 * eps_uds_nom
    shift_up = shift_rb(eps_c_nom, eps_uds_nom + eps_uds_var, R_C_SM, C_b_nom)
    shift_down = shift_rb(eps_c_nom, eps_uds_nom - eps_uds_var, R_C_SM, C_b_nom)
    systematics['eps_uds'] = {
        'delta_Rb': max(abs(shift_up or 0), abs(shift_down or 0)),
        'shift_up': shift_up, 'shift_down': shift_down,
    }

    # R_c (+/- 0.0030)
    shift_up = shift_rb(eps_c_nom, eps_uds_nom, R_C_SM + R_C_ERR, C_b_nom)
    shift_down = shift_rb(eps_c_nom, eps_uds_nom, R_C_SM - R_C_ERR, C_b_nom)
    systematics['R_c'] = {
        'delta_Rb': max(abs(shift_up or 0), abs(shift_down or 0)),
        'shift_up': shift_up, 'shift_down': shift_down,
    }

    # Borrowed systematics (same as Phase 4a)
    systematics['hadronization'] = {'delta_Rb': 0.00045}
    systematics['physics_params'] = {'delta_Rb': 0.00020}
    systematics['g_bb'] = {'delta_Rb': G_BB_ERR * 0.5 * 0.217 / 0.612}
    systematics['g_cc'] = {'delta_Rb': G_CC_ERR * 0.3 * eps_c_nom * 0.217 / 0.612}
    systematics['tau_contamination'] = {'delta_Rb': 0.00005}
    systematics['selection_bias'] = {'delta_Rb': 0.00010}
    systematics['mc_statistics'] = {'delta_Rb': 0.00040}

    total_syst = np.sqrt(sum(s['delta_Rb']**2 for s in systematics.values()))
    stat_unc = rb_results['stability']['sigma_combined'] or best['sigma_stat']
    total_unc = np.sqrt(stat_unc**2 + total_syst**2)

    # A_FB^b systematics (same as Phase 4a)
    afb_systematics = {}
    afb_nom = afb_results['combination']['A_FB_b']
    afb_systematics['delta_QCD'] = {'delta_AFB': DELTA_QCD_ERR * abs(afb_nom or 0.09)}
    afb_systematics['charge_model'] = {'delta_AFB': afb_results['combination']['sigma_A_FB_b'] or 0.005}
    afb_systematics['charm_asymmetry'] = {'delta_AFB': 0.0035 * 0.17 / 0.22}
    afb_systematics['angular_efficiency'] = {'delta_AFB': 0.0020}

    afb_total_syst = np.sqrt(sum(s['delta_AFB']**2 for s in afb_systematics.values()))
    afb_stat = afb_results['combination']['sigma_A_FB_b'] or 0.005

    log.info("\n--- Systematic Summary (10%% data) ---")
    log.info("R_b:")
    for name, s in sorted(systematics.items(), key=lambda x: -x[1]['delta_Rb']):
        log.info("  %-25s  %.5f", name, s['delta_Rb'])
    log.info("  %-25s  %.5f", "Total systematic", total_syst)
    log.info("  %-25s  %.5f", "Statistical", stat_unc)
    log.info("  %-25s  %.5f", "Total", total_unc)

    log.info("\nA_FB^b:")
    for name, s in sorted(afb_systematics.items(), key=lambda x: -x[1]['delta_AFB']):
        log.info("  %-25s  %.5f", name, s['delta_AFB'])
    log.info("  %-25s  %.5f", "Total systematic", afb_total_syst)
    log.info("  %-25s  %.5f", "Statistical", afb_stat)

    return {
        'rb_systematics': systematics,
        'afb_systematics': afb_systematics,
        'rb_total': {
            'stat': float(stat_unc),
            'syst': float(total_syst),
            'total': float(total_unc),
        },
        'afb_total': {
            'stat': float(afb_stat),
            'syst': float(afb_total_syst),
            'total': float(np.sqrt(afb_stat**2 + afb_total_syst**2)),
        },
    }


def compare_to_4a(rb_10pct, afb_10pct, syst_10pct):
    """Compare 10% results to Phase 4a expected."""
    with open(RESULTS_DIR / "parameters.json") as f:
        p4a = json.load(f)

    comparison = {
        'R_b': {
            'data_10pct': rb_10pct['best_wp']['R_b'] if rb_10pct['best_wp'] else None,
            'phase_4a': p4a['R_b']['value'],
            'SM': R_B_SM,
            'stat_10pct': rb_10pct['best_wp']['sigma_stat'] if rb_10pct['best_wp'] else None,
            'stat_4a': p4a['R_b']['stat'],
        },
        'A_FB_b': {
            'data_10pct': afb_10pct['combination']['A_FB_b'],
            'phase_4a': p4a['A_FB_b']['value'],
            'SM': 0.1032,
            'stat_10pct': afb_10pct['combination']['sigma_A_FB_b'],
            'stat_4a': p4a['A_FB_b']['stat'],
        },
    }

    # Check compatibility
    for obs, comp in comparison.items():
        if comp['data_10pct'] is not None and comp['stat_10pct'] is not None:
            diff = abs(comp['data_10pct'] - comp['phase_4a'])
            combined_err = np.sqrt((comp['stat_10pct'])**2 + (comp['stat_4a'])**2)
            if combined_err > 0:
                pull = diff / combined_err
            else:
                pull = None
            comp['difference'] = float(diff)
            comp['combined_stat_error'] = float(combined_err)
            comp['pull'] = float(pull) if pull is not None else None
            comp['compatible'] = bool(pull < 2.0) if pull is not None else None

            log.info("\n%s: 10%%=%.5f, 4a=%.5f, diff=%.5f, pull=%.2f %s",
                     obs, comp['data_10pct'], comp['phase_4a'], diff,
                     pull or 0.0, "PASS" if comp.get('compatible') else "CHECK")

    return comparison


def write_results_json(rb_results, afb_results, syst_results, comparison,
                       corr_10pct, subsample_info):
    """Write 10% results to analysis_note/results/ (update, don't overwrite)."""

    # Update parameters.json with 10% entries
    params_path = RESULTS_DIR / "parameters.json"
    with open(params_path) as f:
        params = json.load(f)

    best = rb_results['best_wp']
    if best:
        params['R_b_10pct'] = {
            'value': best['R_b'],
            'stat': best['sigma_stat'],
            'syst': syst_results['rb_total']['syst'] if syst_results else None,
            'total': syst_results['rb_total']['total'] if syst_results else None,
            'SM': R_B_SM,
            'working_point': best['threshold'],
            'method': 'Double-tag hemisphere counting, 10% data subsample',
            'subsample_seed': SUBSAMPLE_SEED,
            'subsample_fraction': SUBSAMPLE_FRACTION,
        }

    afb_comb = afb_results['combination']
    params['A_FB_b_10pct'] = {
        'value': afb_comb['A_FB_b'],
        'stat': afb_comb['sigma_A_FB_b'],
        'syst': syst_results['afb_total']['syst'] if syst_results else None,
        'total': syst_results['afb_total']['total'] if syst_results else None,
        'SM': 0.1032,
        'method': 'Self-calibrating hemisphere jet charge, 10% data subsample',
    }

    if afb_results['sin2theta']['value'] is not None:
        params['sin2theta_eff_10pct'] = {
            'value': afb_results['sin2theta']['value'],
            'stat': afb_results['sin2theta']['sigma_stat'],
            'SM': 0.23153,
            'method': 'Inverted from A_FB^{0,b}, 10% data',
        }

    params['phase_4b_info'] = {
        'data_type': '10% data subsample',
        'subsample_seed': SUBSAMPLE_SEED,
        'subsample_fraction': SUBSAMPLE_FRACTION,
    }

    with open(params_path, 'w') as f:
        json.dump(params, f, indent=2)
    log.info("Updated parameters.json with 10%% results")

    # Write Phase 4b specific results
    with open(PHASE4B_OUT / "rb_results_10pct.json", 'w') as f:
        json.dump(rb_results, f, indent=2)

    with open(PHASE4B_OUT / "afb_results_10pct.json", 'w') as f:
        json.dump(afb_results, f, indent=2, default=str)

    if syst_results:
        with open(PHASE4B_OUT / "systematics_10pct.json", 'w') as f:
            json.dump(syst_results, f, indent=2)

    with open(PHASE4B_OUT / "comparison_4a_vs_4b.json", 'w') as f:
        json.dump(comparison, f, indent=2)

    with open(PHASE4B_OUT / "correlation_10pct.json", 'w') as f:
        json.dump(corr_10pct, f, indent=2)

    with open(PHASE4B_OUT / "subsample_info.json", 'w') as f:
        json.dump(subsample_info, f, indent=2)

    # Update validation.json
    val_path = RESULTS_DIR / "validation.json"
    with open(val_path) as f:
        validation = json.load(f)

    validation['phase_4b'] = {
        'rb_stability_10pct': rb_results['stability'],
        'kappa_consistency_10pct': {
            'chi2': afb_results['combination']['chi2_kappa'],
            'ndf': afb_results['combination']['ndf_kappa'],
            'p_value': afb_results['combination']['p_kappa'],
            'passes': (afb_results['combination']['p_kappa'] or 0) > 0.05,
        },
        'comparison_to_4a': comparison,
    }

    with open(val_path, 'w') as f:
        json.dump(validation, f, indent=2)
    log.info("Updated validation.json with 10%% results")


def main():
    log.info("=" * 70)
    log.info("Phase 4b: Full Analysis Chain on 10%% Data Subsample")
    log.info("Subsample fraction: %.0f%%, Seed: %d", SUBSAMPLE_FRACTION * 100, SUBSAMPLE_SEED)
    log.info("=" * 70)

    # ================================================================
    # Step 1: Load Phase 3 preselected data and select 10% subsample
    # ================================================================
    log.info("\n" + "=" * 60)
    log.info("Step 1: Loading data and selecting 10%% subsample")
    log.info("=" * 60)

    data_full, mc, mask_10pct = load_preselected_10pct()
    n_10pct = int(np.sum(mask_10pct))
    n_full = len(mask_10pct)
    log.info("10%% subsample: %d events from %d total (%.2f%%)",
             n_10pct, n_full, 100.0 * n_10pct / n_full)

    # Subsample event-level and track-level arrays
    data_10pct = subsample_track_arrays(data_full, mask_10pct)
    log.info("Subsampled data arrays: %d event-level keys",
             len([k for k in data_10pct if not k.startswith("trk_") and not k.startswith("alltrk_")]))

    subsample_info = {
        'seed': SUBSAMPLE_SEED,
        'fraction': SUBSAMPLE_FRACTION,
        'n_selected': n_10pct,
        'n_total': n_full,
        'actual_fraction': float(n_10pct / n_full),
        'method': 'Random selection with np.random.RandomState(42).random(n) < 0.10',
    }

    # ================================================================
    # Step 2: sigma_d0 calibration on 10% data
    # ================================================================
    log.info("\n" + "=" * 60)
    log.info("Step 2: sigma_d0 calibration on 10%% data")
    log.info("=" * 60)

    cal_results, sigma_d0, significance = run_sigma_d0_calibration(data_10pct)
    log.info("sigma_d0 calibration: %d bins, significance range [%.1f, %.1f]",
             len(cal_results), np.percentile(significance, 0.1),
             np.percentile(significance, 99.9))

    # ================================================================
    # Step 3: Compute signed d0 significance
    # ================================================================
    log.info("\n" + "=" * 60)
    log.info("Step 3: Signed d0 computation")
    log.info("=" * 60)

    # Load Phase 3 signed d0 and subsample
    signed_d0_full = np.load(P3_OUT / "signed_d0.npz", allow_pickle=False)
    data_signed_sig_full = signed_d0_full["data_signed_sig"]

    # We need to subsample the signed significance at track level
    # The signed_d0.npz has flat track arrays corresponding to the
    # preselected_data.npz tracks
    offsets_full = data_full["trk_d0_offsets"]
    event_indices_10pct = np.where(mask_10pct)[0]

    signed_sig_parts = []
    for idx in event_indices_10pct:
        start, end = offsets_full[idx], offsets_full[idx + 1]
        signed_sig_parts.append(data_signed_sig_full[start:end])

    if signed_sig_parts:
        signed_sig_10pct = np.concatenate(signed_sig_parts)
    else:
        signed_sig_10pct = np.array([])

    log.info("Signed significance: %d tracks, positive fraction: %.3f",
             len(signed_sig_10pct),
             np.mean(signed_sig_10pct > 0) if len(signed_sig_10pct) > 0 else 0)

    # ================================================================
    # Step 4: Hemisphere tagging on 10% data
    # ================================================================
    log.info("\n" + "=" * 60)
    log.info("Step 4: Hemisphere tagging on 10%% data")
    log.info("=" * 60)

    data_tags = compute_hemisphere_tags_10pct(signed_sig_10pct, data_10pct)
    log.info("Tags computed: combined_h0 range [%.2f, %.2f]",
             np.min(data_tags["combined_h0"]), np.max(data_tags["combined_h0"]))

    # Tag fractions at representative WPs
    for wp in [5.0, 7.0, 8.0, 10.0]:
        tagged_h0 = data_tags["combined_h0"] > wp
        tagged_h1 = data_tags["combined_h1"] > wp
        n_single = int(np.sum(tagged_h0 | tagged_h1))
        n_double = int(np.sum(tagged_h0 & tagged_h1))
        f_s = (int(np.sum(tagged_h0)) + int(np.sum(tagged_h1))) / (2 * n_10pct)
        f_d = n_double / n_10pct
        log.info("WP %.1f: f_s=%.4f, f_d=%.6f, N_single=%d, N_double=%d",
                 wp, f_s, f_d, n_single, n_double)

    # ================================================================
    # Step 5: Jet charge on 10% data
    # ================================================================
    log.info("\n" + "=" * 60)
    log.info("Step 5: Jet charge on 10%% data")
    log.info("=" * 60)

    jc_results, cos_theta_10pct = compute_jet_charge_10pct(data_10pct)
    for kappa in KAPPA_VALUES:
        k_str = f"k{kappa:.1f}"
        qfb = jc_results[f"qfb_{k_str}"]
        valid = ~np.isnan(qfb)
        log.info("kappa=%.1f: mean(Q_FB)=%.5f, sigma(Q_h)=%.4f",
                 kappa, np.nanmean(qfb), np.nanstd(jc_results[f"qh_h0_{k_str}"]))

    # ================================================================
    # Step 6: Hemisphere correlation on 10% data
    # ================================================================
    log.info("\n" + "=" * 60)
    log.info("Step 6: Hemisphere correlation on 10%% data")
    log.info("=" * 60)

    corr_10pct = compute_hemisphere_correlation_10pct(data_tags)

    # ================================================================
    # Step 7: Load Phase 4a MC calibration
    # ================================================================
    log.info("\n" + "=" * 60)
    log.info("Step 7: R_b extraction from 10%% data")
    log.info("=" * 60)

    with open(P4A_OUT / "mc_calibration.json") as f:
        mc_cal = json.load(f)
    with open(P4A_OUT / "correlation_results.json") as f:
        corr_4a = json.load(f)

    rb_results = extract_rb_10pct(data_tags, mc_cal, corr_4a)

    # ================================================================
    # Step 8: A_FB^b extraction from 10% data
    # ================================================================
    log.info("\n" + "=" * 60)
    log.info("Step 8: A_FB^b extraction from 10%% data")
    log.info("=" * 60)

    afb_results = extract_afb_10pct(jc_results, cos_theta_10pct, data_tags)

    # ================================================================
    # Step 9: Systematic re-evaluation
    # ================================================================
    log.info("\n" + "=" * 60)
    log.info("Step 9: Systematic evaluation on 10%% data")
    log.info("=" * 60)

    syst_results = evaluate_systematics_10pct(
        rb_results, afb_results, data_tags, mc_cal, corr_4a)

    # ================================================================
    # Step 10: Comparison to Phase 4a
    # ================================================================
    log.info("\n" + "=" * 60)
    log.info("Step 10: Comparison to Phase 4a expected")
    log.info("=" * 60)

    comparison = compare_to_4a(rb_results, afb_results, syst_results)

    # ================================================================
    # Step 11: Critical diagnostic — R_b bias test
    # ================================================================
    log.info("\n" + "=" * 60)
    log.info("CRITICAL DIAGNOSTIC: R_b bias with real data")
    log.info("=" * 60)

    if rb_results['best_wp']:
        rb_data = rb_results['best_wp']['R_b']
        rb_4a = 0.280  # Phase 4a circular calibration value
        rb_sm = R_B_SM

        log.info("R_b (10%% data):  %.5f", rb_data)
        log.info("R_b (Phase 4a):  %.5f (circular MC calibration)", rb_4a)
        log.info("R_b (SM):        %.5f", rb_sm)
        log.info("Bias (data):     %.5f (deviation from SM)", rb_data - rb_sm)
        log.info("Bias (4a):       %.5f (deviation from SM)", rb_4a - rb_sm)

        if abs(rb_data - rb_sm) < abs(rb_4a - rb_sm):
            log.info("RESULT: R_b bias IMPROVED with real data (%.3f vs %.3f)",
                     abs(rb_data - rb_sm), abs(rb_4a - rb_sm))
        else:
            log.info("RESULT: R_b bias NOT improved (%.3f vs %.3f). "
                     "The circular calibration dominates even with data.",
                     abs(rb_data - rb_sm), abs(rb_4a - rb_sm))

    # ================================================================
    # Step 12: Write results
    # ================================================================
    log.info("\n" + "=" * 60)
    log.info("Step 12: Writing results")
    log.info("=" * 60)

    write_results_json(rb_results, afb_results, syst_results, comparison,
                       corr_10pct, subsample_info)

    # Save tags and intermediate data for plotting
    np.savez_compressed(
        PHASE4B_OUT / "data_10pct_tags.npz",
        **{f"data_{k}": v for k, v in data_tags.items()},
        cos_theta=cos_theta_10pct,
        bflag=data_10pct["bflag"],
        year=data_10pct["year"],
    )
    log.info("Saved data_10pct_tags.npz")

    # Save jet charge for plotting
    np.savez_compressed(
        PHASE4B_OUT / "data_10pct_jetcharge.npz",
        **{f"data_{k}": v for k, v in jc_results.items()},
        cos_theta=cos_theta_10pct,
    )
    log.info("Saved data_10pct_jetcharge.npz")

    log.info("\n" + "=" * 70)
    log.info("Phase 4b analysis complete.")
    log.info("=" * 70)

    # Print summary
    log.info("\n--- SUMMARY ---")
    if rb_results['best_wp']:
        log.info("R_b = %.4f +/- %.4f (stat) +/- %.4f (syst)",
                 rb_results['best_wp']['R_b'],
                 rb_results['best_wp']['sigma_stat'],
                 syst_results['rb_total']['syst'] if syst_results else 0)
    if afb_results['combination']['A_FB_b'] is not None:
        log.info("A_FB^b = %.4f +/- %.4f (stat) +/- %.4f (syst)",
                 afb_results['combination']['A_FB_b'],
                 afb_results['combination']['sigma_A_FB_b'],
                 syst_results['afb_total']['syst'] if syst_results else 0)
    if afb_results['sin2theta']['value'] is not None:
        log.info("sin^2(theta_eff) = %.5f +/- %.5f (stat)",
                 afb_results['sin2theta']['value'],
                 afb_results['sin2theta']['sigma_stat'])


if __name__ == "__main__":
    main()
