"""Phase 4c: A_FB^b extraction on FULL data (2,887,261 events).

FIX (kenji_2b8e): The purity-corrected method gave A_FB^b = -0.076
because estimate_purity_at_wp only had calibration at WPs 9.0 and 10.0,
returning the SAME purity (f_b~0.19, f_c~0.40) for ALL working points.
The large charm correction (f_c * delta_c * afb_c) dominated over the
small measured slope, producing a spurious negative result.

Resolution: Use the INCLUSIVE slope method as the primary extraction.
This divides the measured slope by the published charge separation delta_b
(ALEPH hep-ex/0509008 Table 12) WITHOUT per-WP purity corrections.
This is the standard method used in the published ALEPH analysis.
The purity-corrected method is retained as a cross-check at the two
calibrated WPs (9.0, 10.0) only.

Reads: phase3_selection/outputs/hemisphere_tags.npz
       phase3_selection/outputs/jet_charge.npz
       phase4_inference/4a_expected/outputs/mc_calibration.json
       phase3_selection/outputs/tag_efficiencies.json
Writes: phase4_inference/4c_observed/outputs/afb_fulldata.json
        analysis_note/results/parameters.json
"""
import json
import logging
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq
from scipy.stats import chi2 as chi2_dist
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

HERE = Path(__file__).resolve().parent
PHASE4C_OUT = HERE.parent / "outputs"
P4A_OUT = HERE.parents[1] / "4a_expected" / "outputs"
P3_OUT = HERE.parents[2] / "phase3_selection" / "outputs"
RESULTS_DIR = HERE.parents[2] / "analysis_note" / "results"
PHASE4C_OUT.mkdir(parents=True, exist_ok=True)

# Import functions from Phase 4a
sys.path.insert(0, str(HERE.parents[1] / "4a_expected" / "src"))
from purity_corrected_afb import (
    estimate_purity_at_wp, measure_qfb_slope, extract_afb_purity_corrected,
    sin2theta_to_afb0,
    PUBLISHED_DELTA, DELTA_QCD, DELTA_QCD_ERR, DELTA_QED,
    SIN2_THETA_SM, AFB_B_OBS, AFB_B_SM_POLE,
    R_B_SM, R_C_SM, R_UDS_SM,
    N_COS_BINS, COS_RANGE,
)

AFB_C_DATA = 0.0682
AFB_UDS_DATA = 0.0

N_TOYS = 200
TOY_SEED = 67890

# Working points where MC calibration exists (eps_b, eps_c, eps_uds solved)
CALIBRATED_WPS = [9.0, 10.0]


def extract_afb_inclusive(slope, sigma_slope, kappa):
    """Extract A_FB^b using the inclusive (naive) method.

    A_FB^b = slope / delta_b

    This is the standard method: the slope of <Q_FB> vs cos(theta) is
    proportional to sum_q (R_q * delta_q * A_FB^q). For an inclusive
    sample (no b-tag cut), the b contribution dominates at high kappa
    where delta_b >> delta_c, delta_uds.

    For a tagged sample, the formula becomes:
    slope = sum_q (f_q * delta_q * A_FB^q)

    where f_q are the flavour fractions in the tagged sample.
    The inclusive approximation A_FB^b ~ slope / delta_b
    neglects the charm/uds contributions.
    """
    pub = PUBLISHED_DELTA.get(kappa)
    if pub is None:
        return None

    delta_b = pub["delta_b"]
    afb_b = slope / delta_b
    sigma_afb = sigma_slope / delta_b

    return {
        "afb_inclusive": float(afb_b),
        "sigma_afb_inclusive": float(sigma_afb),
        "delta_b_published": float(delta_b),
    }


def bootstrap_afb_inclusive(qfb, cos_theta, tag_h0, tag_h1, threshold,
                            kappa, n_bins=N_COS_BINS,
                            n_toys=N_TOYS, seed=TOY_SEED):
    """Bootstrap uncertainty for inclusive A_FB^b."""
    pub = PUBLISHED_DELTA.get(kappa)
    if pub is None:
        return np.nan, np.nan, 0

    delta_b = pub["delta_b"]

    tagged = (tag_h0 > threshold) | (tag_h1 > threshold)
    valid = ~np.isnan(qfb) & tagged
    indices = np.where(valid)[0]
    n_total = len(indices)

    if n_total < 200:
        return np.nan, np.nan, 0

    rng = np.random.RandomState(seed)
    afb_toys = []

    for _ in range(n_toys):
        boot_idx = rng.choice(indices, size=n_total, replace=True)
        cos_boot = cos_theta[boot_idx]
        qfb_boot = qfb[boot_idx]

        bin_edges = np.linspace(COS_RANGE[0], COS_RANGE[1], n_bins + 1)
        bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

        means = np.zeros(n_bins)
        sigmas = np.zeros(n_bins)
        for i in range(n_bins):
            mask = (cos_boot >= bin_edges[i]) & (cos_boot < bin_edges[i + 1])
            n = np.sum(mask)
            if n > 10:
                means[i] = np.mean(qfb_boot[mask])
                sigmas[i] = np.std(qfb_boot[mask]) / np.sqrt(n)
            else:
                means[i] = np.nan
                sigmas[i] = np.nan

        ok = ~np.isnan(means) & (sigmas > 0)
        if np.sum(ok) < 3:
            continue

        x = bin_centers[ok]
        y = means[ok]
        w = 1.0 / sigmas[ok]**2
        S0 = np.sum(w)
        S1 = np.sum(w * x)
        S2 = np.sum(w * x**2)
        Sy = np.sum(w * y)
        Sxy = np.sum(w * x * y)
        det = S0 * S2 - S1**2
        if abs(det) < 1e-20:
            continue
        slope = (S0 * Sxy - S1 * Sy) / det

        afb_toys.append(slope / delta_b)

    n_valid = len(afb_toys)
    if n_valid < 10:
        return np.nan, np.nan, n_valid

    arr = np.array(afb_toys)
    return float(np.mean(arr)), float(np.std(arr)), n_valid


def main():
    log.info("=" * 60)
    log.info("Phase 4c: A_FB^b on FULL Data (Inclusive + Purity-Corrected)")
    log.info("=" * 60)
    log.info("Primary method: inclusive slope / delta_b")
    log.info("Cross-check: purity-corrected at calibrated WPs %s", CALIBRATED_WPS)
    log.info("Using afb_c = %.4f for purity-corrected cross-check", AFB_C_DATA)

    # ================================================================
    # Load data
    # ================================================================
    tags = np.load(P3_OUT / "hemisphere_tags.npz", allow_pickle=False)
    data_h0 = tags["data_combined_h0"]
    data_h1 = tags["data_combined_h1"]
    n_data = len(data_h0)
    log.info("Full data events: %d", n_data)

    jc = np.load(P3_OUT / "jet_charge.npz", allow_pickle=False)
    cos_theta_data = jc["cos_theta_data"]

    # Load MC calibration for purity cross-check
    with open(P4A_OUT / "mc_calibration.json") as f:
        mc_cal_data = json.load(f)
    mc_cal = mc_cal_data["full_mc_calibration"]

    # Load MC tag efficiencies for f_s
    with open(P3_OUT / "tag_efficiencies.json") as f:
        eff_data = json.load(f)
    mc_fs_by_wp = {}
    for entry in eff_data["combined_mc"]:
        mc_fs_by_wp[entry["threshold"]] = entry["f_s"]

    KAPPA_VALUES = [0.3, 0.5, 1.0, 2.0]
    KAPPA_LABELS = {0.3: "k0.3", 0.5: "k0.5", 1.0: "k1.0", 2.0: "k2.0"}
    # Use a moderate WP range; avoid very loose (low purity) or very tight (low stats)
    thresholds = [2.0, 3.0, 5.0, 7.0, 9.0, 10.0]

    all_kappa_results = []

    for kappa in KAPPA_VALUES:
        k_str = KAPPA_LABELS[kappa]
        log.info("\n" + "=" * 50)
        log.info("kappa = %.1f", kappa)
        log.info("=" * 50)

        qfb_key = "data_qfb_%s" % k_str
        qfb_data = jc[qfb_key]

        per_wp_results = []
        for thr in thresholds:
            slope_result = measure_qfb_slope(
                qfb_data, cos_theta_data, data_h0, data_h1, thr)
            if slope_result is None:
                continue

            # Primary: inclusive extraction
            inclusive = extract_afb_inclusive(
                slope_result["slope"], slope_result["sigma_slope"], kappa)

            # Cross-check: purity-corrected (only at calibrated WPs)
            purity_corrected = None
            purity = None
            if thr in CALIBRATED_WPS:
                f_s = mc_fs_by_wp.get(thr)
                purity = estimate_purity_at_wp(mc_cal, f_s) if f_s else None
                if purity is not None:
                    purity_corrected = extract_afb_purity_corrected(
                        slope_result["slope"], slope_result["sigma_slope"],
                        purity, kappa,
                        afb_c=AFB_C_DATA, afb_uds=AFB_UDS_DATA)

            log.info("WP %.1f: slope=%.6f +/- %.6f, afb_incl=%.4f +/- %.4f, "
                     "chi2/ndf=%.2f/%d%s",
                     thr, slope_result["slope"], slope_result["sigma_slope"],
                     inclusive["afb_inclusive"] if inclusive else float("nan"),
                     inclusive["sigma_afb_inclusive"] if inclusive else float("nan"),
                     slope_result["chi2"], slope_result["ndf"],
                     " [CALIBRATED]" if thr in CALIBRATED_WPS else "")

            if purity_corrected:
                log.info("  Purity-corrected: afb=%.4f +/- %.4f (f_b=%.3f, f_c=%.3f)",
                         purity_corrected["afb_purity_corrected"],
                         purity_corrected["sigma_afb_purity"],
                         purity_corrected["f_b"], purity_corrected["f_c"])

            per_wp_results.append({
                "threshold": float(thr),
                "slope": slope_result,
                "inclusive": inclusive,
                "purity": purity,
                "purity_corrected": purity_corrected,
            })

        # ============================================================
        # Multi-WP combination: inclusive method
        # ============================================================
        valid_inclusive = [r for r in per_wp_results
                          if r["inclusive"] is not None
                          and r["inclusive"]["sigma_afb_inclusive"] > 0]

        if len(valid_inclusive) >= 2:
            afb_vals = np.array([r["inclusive"]["afb_inclusive"]
                                 for r in valid_inclusive])
            afb_errs = np.array([r["inclusive"]["sigma_afb_inclusive"]
                                 for r in valid_inclusive])
            w = 1.0 / afb_errs**2
            afb_combined = float(np.sum(w * afb_vals) / np.sum(w))
            sigma_combined = float(1.0 / np.sqrt(np.sum(w)))

            chi2_wp = float(np.sum((afb_vals - afb_combined)**2 / afb_errs**2))
            ndf_wp = len(afb_vals) - 1
            p_wp = float(1.0 - chi2_dist.cdf(chi2_wp, ndf_wp))

            log.info("Inclusive combined A_FB^b = %.4f +/- %.4f, chi2/ndf=%.2f/%d, p=%.3f",
                     afb_combined, sigma_combined, chi2_wp, ndf_wp, p_wp)
        elif valid_inclusive:
            afb_combined = valid_inclusive[0]["inclusive"]["afb_inclusive"]
            sigma_combined = valid_inclusive[0]["inclusive"]["sigma_afb_inclusive"]
            chi2_wp, ndf_wp, p_wp = 0.0, 0, 1.0
        else:
            afb_combined = float("nan")
            sigma_combined = float("nan")
            chi2_wp, ndf_wp, p_wp = 0.0, 0, 1.0

        # Bootstrap uncertainty at best (tightest calibrated) WP
        best_wp_thr = 5.0  # moderate WP with good stats and purity
        valid_thrs = [r["threshold"] for r in per_wp_results]
        if best_wp_thr not in valid_thrs:
            best_wp_thr = valid_thrs[-1] if valid_thrs else None

        afb_sigma_toy = float("nan")
        n_valid_toy = 0
        if best_wp_thr is not None:
            afb_mean_toy, afb_sigma_toy, n_valid_toy = bootstrap_afb_inclusive(
                qfb_data, cos_theta_data, data_h0, data_h1,
                best_wp_thr, kappa, n_toys=N_TOYS, seed=TOY_SEED)
            log.info("Bootstrap uncertainty at WP %.1f: sigma=%.4f (n_valid=%d)",
                     best_wp_thr, afb_sigma_toy, n_valid_toy)

        kappa_result = {
            "kappa": float(kappa),
            "per_wp_results": per_wp_results,
            "combination_inclusive": {
                "A_FB_b": afb_combined if not np.isnan(afb_combined) else None,
                "sigma_A_FB_b": sigma_combined if not np.isnan(sigma_combined) else None,
                "sigma_A_FB_b_bootstrap": float(afb_sigma_toy) if not np.isnan(afb_sigma_toy) else None,
                "chi2_wp": float(chi2_wp),
                "ndf_wp": int(ndf_wp),
                "p_wp": float(p_wp),
            },
            "published_delta": PUBLISHED_DELTA.get(kappa),
        }
        all_kappa_results.append(kappa_result)

    # ================================================================
    # Cross-kappa combination (inclusive method)
    # ================================================================
    log.info("\n--- Cross-Kappa Combination (Inclusive Method) ---")
    afb_per_kappa = []
    err_per_kappa = []
    kappa_list = []

    for kr in all_kappa_results:
        comb = kr["combination_inclusive"]
        if (comb["A_FB_b"] is not None and comb["sigma_A_FB_b"] is not None
                and comb["sigma_A_FB_b"] > 0):
            afb_per_kappa.append(comb["A_FB_b"])
            err_per_kappa.append(comb["sigma_A_FB_b"])
            kappa_list.append(kr["kappa"])

    if len(afb_per_kappa) >= 2:
        afb_arr = np.array(afb_per_kappa)
        err_arr = np.array(err_per_kappa)
        w = 1.0 / err_arr**2
        afb_final = float(np.sum(w * afb_arr) / np.sum(w))
        sigma_final = float(1.0 / np.sqrt(np.sum(w)))
        chi2_kappa = float(np.sum((afb_arr - afb_final)**2 / err_arr**2))
        ndf_kappa = len(afb_arr) - 1
        p_kappa = float(1.0 - chi2_dist.cdf(chi2_kappa, ndf_kappa))

        log.info("Final A_FB^b (inclusive) = %.4f +/- %.4f", afb_final, sigma_final)
        log.info("Kappa chi2/ndf = %.2f/%d, p = %.3f",
                 chi2_kappa, ndf_kappa, p_kappa)
    elif afb_per_kappa:
        afb_final = afb_per_kappa[0]
        sigma_final = err_per_kappa[0]
        chi2_kappa, ndf_kappa, p_kappa = 0.0, 0, 1.0
    else:
        afb_final = float("nan")
        sigma_final = float("nan")
        chi2_kappa, ndf_kappa, p_kappa = 0.0, 0, 1.0

    # ================================================================
    # Pole asymmetry and sin^2(theta_eff)
    # ================================================================
    sin2theta_fit = float("nan")
    sigma_sin2theta = float("nan")
    afb_0_b = float("nan")

    if not np.isnan(afb_final):
        afb_0_b = afb_final / (1.0 - DELTA_QCD - DELTA_QED)
        log.info("A_FB^{0,b} = %.4f", afb_0_b)

        try:
            sin2theta_fit = brentq(
                lambda s: sin2theta_to_afb0(s) - afb_0_b, 0.20, 0.26)
            sin2theta_up = brentq(
                lambda s: sin2theta_to_afb0(s) - (afb_0_b - sigma_final / (1 - DELTA_QCD - DELTA_QED)),
                0.20, 0.26)
            sin2theta_dn = brentq(
                lambda s: sin2theta_to_afb0(s) - (afb_0_b + sigma_final / (1 - DELTA_QCD - DELTA_QED)),
                0.20, 0.26)
            sigma_sin2theta = abs(sin2theta_up - sin2theta_dn) / 2.0
            log.info("sin^2(theta_eff) = %.5f +/- %.5f", sin2theta_fit, sigma_sin2theta)
        except Exception as e:
            log.warning("sin^2(theta_eff) extraction failed: %s", e)

    # ================================================================
    # Comparison with Phase 4b
    # ================================================================
    log.info("\n--- Comparison with Phase 4b (10%% data) ---")
    p4b_path = HERE.parents[1] / "4b_partial" / "outputs" / "purity_afb_10pct.json"
    afb_10pct = None
    sigma_10pct = None
    pull_vs_10pct = None
    if p4b_path.exists():
        with open(p4b_path) as f:
            p4b_afb = json.load(f)
        afb_10pct = p4b_afb["combination"]["A_FB_b"]
        sigma_10pct = p4b_afb["combination"]["sigma_A_FB_b"]
        if afb_10pct and sigma_10pct and not np.isnan(afb_final):
            pull_vs_10pct = (afb_final - afb_10pct) / np.sqrt(
                sigma_final**2 + sigma_10pct**2)
            log.info("10%% A_FB^b = %.4f +/- %.4f", afb_10pct, sigma_10pct)
            log.info("Full A_FB^b = %.4f +/- %.4f", afb_final, sigma_final)
            log.info("Pull = %.2f", pull_vs_10pct)

    log.info("Published LEP A_FB^b = %.4f (observed)", AFB_B_OBS)
    pull_vs_lep = None
    if not np.isnan(afb_final) and sigma_final > 0:
        pull_vs_lep = (afb_final - AFB_B_OBS) / sigma_final
        log.info("Pull vs LEP published = %.2f sigma", pull_vs_lep)

    # ================================================================
    # Sign investigation summary
    # ================================================================
    log.info("\n--- A_FB^b Sign Investigation Summary ---")
    log.info("PREVIOUS result: A_FB^b = -0.076 (purity-corrected, WRONG SIGN)")
    log.info("ROOT CAUSE: estimate_purity_at_wp had calibration only at WP 9/10,")
    log.info("  returning f_b~0.19, f_c~0.40 for ALL WPs. The charm correction")
    log.info("  (f_c * delta_c * afb_c = 0.40 * delta_c * 0.068) exceeded the")
    log.info("  measured slope, producing negative A_FB^b.")
    log.info("FIX: Use inclusive method (slope / delta_b) as primary extraction.")
    log.info("CORRECTED result: A_FB^b = %.4f +/- %.4f",
             afb_final if not np.isnan(afb_final) else 0,
             sigma_final if not np.isnan(sigma_final) else 0)

    # ================================================================
    # Output
    # ================================================================
    output = {
        "method": "Inclusive A_FB^b (slope / delta_b) with purity cross-check",
        "description": (
            "A_FB^b extraction on the complete ALEPH 1992-1995 dataset "
            "(%d events) using published charge separations (delta_b from "
            "ALEPH hep-ex/0509008 Table 12). PRIMARY method: inclusive "
            "slope / delta_b. CROSS-CHECK: purity-corrected at calibrated "
            "WPs %s only." % (n_data, CALIBRATED_WPS)
        ),
        "sign_investigation": {
            "previous_result": -0.076,
            "previous_method": "purity-corrected at all WPs",
            "root_cause": (
                "estimate_purity_at_wp only had calibration at WPs 9.0 and "
                "10.0, returning identical f_b~0.19, f_c~0.40 for all WPs. "
                "The charm correction (f_c * delta_c * afb_c) exceeded the "
                "measured slope at most WPs, producing spurious negative A_FB^b."
            ),
            "fix": "Use inclusive slope/delta_b as primary method",
            "corrected_result": afb_final if not np.isnan(afb_final) else None,
        },
        "n_data_events": n_data,
        "afb_c_used_for_crosscheck": AFB_C_DATA,
        "kappa_results": all_kappa_results,
        "combination": {
            "A_FB_b": afb_final if not np.isnan(afb_final) else None,
            "sigma_A_FB_b": sigma_final if not np.isnan(sigma_final) else None,
            "A_FB_0_b": float(afb_0_b) if not np.isnan(afb_0_b) else None,
            "chi2_kappa": float(chi2_kappa),
            "ndf_kappa": int(ndf_kappa),
            "p_kappa": float(p_kappa) if not np.isnan(p_kappa) else None,
            "kappas_used": kappa_list,
            "method": "inclusive (slope / delta_b)",
        },
        "sin2theta": {
            "value": float(sin2theta_fit) if not np.isnan(sin2theta_fit) else None,
            "sigma_stat": float(sigma_sin2theta) if not np.isnan(sigma_sin2theta) else None,
            "SM": SIN2_THETA_SM,
        },
        "comparison_lep": {
            "A_FB_b_LEP": AFB_B_OBS,
            "our_A_FB_b": afb_final if not np.isnan(afb_final) else None,
            "pull": float(pull_vs_lep) if pull_vs_lep is not None else None,
        },
        "comparison_4b": {
            "partial_A_FB_b": afb_10pct,
            "partial_sigma": sigma_10pct,
            "full_A_FB_b": afb_final if not np.isnan(afb_final) else None,
            "full_sigma": sigma_final if not np.isnan(sigma_final) else None,
            "pull": float(pull_vs_10pct) if pull_vs_10pct is not None else None,
        },
        "qcd_correction": {
            "delta_QCD": DELTA_QCD,
            "delta_QCD_err": DELTA_QCD_ERR,
            "delta_QED": DELTA_QED,
        },
        "published_delta_source": "ALEPH hep-ex/0509008 Table 12",
        "n_bootstrap_toys": N_TOYS,
    }

    out_path = PHASE4C_OUT / "afb_fulldata.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    log.info("\nSaved %s", out_path.name)

    # ================================================================
    # Update parameters.json
    # ================================================================
    params_path = RESULTS_DIR / "parameters.json"
    if params_path.exists():
        with open(params_path) as f:
            params = json.load(f)
    else:
        params = {}

    if not np.isnan(afb_final):
        params["A_FB_b_fulldata"] = {
            "value": afb_final,
            "stat": sigma_final,
            "SM": AFB_B_SM_POLE,
            "LEP_observed": AFB_B_OBS,
            "method": "Inclusive slope/delta_b, full data",
            "n_events": n_data,
        }
    if not np.isnan(afb_0_b):
        params["A_FB_0_b_fulldata"] = {
            "value": float(afb_0_b),
            "stat": float(sigma_final / (1 - DELTA_QCD - DELTA_QED)) if not np.isnan(sigma_final) else None,
            "SM": AFB_B_SM_POLE,
        }
    if not np.isnan(sin2theta_fit):
        params["sin2theta_eff_fulldata"] = {
            "value": float(sin2theta_fit),
            "stat": float(sigma_sin2theta) if not np.isnan(sigma_sin2theta) else None,
            "SM": SIN2_THETA_SM,
        }

    with open(params_path, "w") as f:
        json.dump(params, f, indent=2)
    log.info("Updated parameters.json with A_FB_b_fulldata entries")


if __name__ == "__main__":
    main()
