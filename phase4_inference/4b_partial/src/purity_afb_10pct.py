"""Phase 4b REGRESSION: Purity-corrected A_FB^b on 10% data.

Adapts Phase 4a purity_corrected_afb.py for 10% real data.
CRITICAL: uses afb_c=0.0682 (published charm asymmetry) for data,
NOT 0.0 (which is for symmetric MC only).

The governing formula:
  slope = f_b * delta_b * A_FB^b + f_c * delta_c * A_FB^c + ...
  A_FB^b = (slope - f_c * delta_c * A_FB^c) / (f_b * delta_b)

Reads: phase4_inference/4b_partial/outputs/data_10pct_tags.npz
       phase4_inference/4b_partial/outputs/data_10pct_jetcharge.npz
       phase3_selection/outputs/hemisphere_tags.npz
       phase3_selection/outputs/jet_charge.npz
       phase4_inference/4a_expected/outputs/mc_calibration.json
       phase3_selection/outputs/tag_efficiencies.json
Writes: phase4_inference/4b_partial/outputs/purity_afb_10pct.json
        analysis_note/results/parameters.json (updates A_FB_b_10pct)
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
PHASE4B_OUT = HERE.parent / "outputs"
P4A_OUT = HERE.parents[1] / "4a_expected" / "outputs"
P3_OUT = HERE.parents[2] / "phase3_selection" / "outputs"
RESULTS_DIR = HERE.parents[2] / "analysis_note" / "results"

# Import functions from Phase 4a
sys.path.insert(0, str(HERE.parents[1] / "4a_expected" / "src"))
from purity_corrected_afb import (
    estimate_purity_at_wp, measure_qfb_slope, extract_afb_purity_corrected,
    toy_uncertainty_afb, sin2theta_to_afb0,
    PUBLISHED_DELTA, DELTA_QCD, DELTA_QCD_ERR, DELTA_QED,
    SIN2_THETA_SM, AFB_B_OBS, AFB_B_SM_POLE,
    R_B_SM, R_C_SM, R_UDS_SM,
    N_COS_BINS, COS_RANGE,
)

# CRITICAL: For DATA, use observed charm asymmetry, NOT 0.0
AFB_C_DATA = 0.0682   # observed A_FB^c at LEP (hep-ex/0509008)
AFB_UDS_DATA = 0.0    # negligible for light quarks

N_TOYS = 1000
TOY_SEED = 67890


def main():
    log.info("=" * 60)
    log.info("Phase 4b REGRESSION: Purity-Corrected A_FB^b on 10%% Data")
    log.info("=" * 60)
    log.info("IMPORTANT: Using afb_c = %.4f for data (NOT 0.0)", AFB_C_DATA)

    # ================================================================
    # Load data
    # ================================================================
    data_tags = np.load(PHASE4B_OUT / "data_10pct_tags.npz", allow_pickle=False)
    data_h0 = data_tags["data_combined_h0"]
    data_h1 = data_tags["data_combined_h1"]
    n_data = len(data_h0)
    log.info("10%% data events: %d", n_data)

    jc_data = np.load(PHASE4B_OUT / "data_10pct_jetcharge.npz", allow_pickle=False)
    cos_theta_data = jc_data["cos_theta"]

    # Load MC calibration for purities
    with open(P4A_OUT / "mc_calibration.json") as f:
        mc_cal_data = json.load(f)
    mc_cal = mc_cal_data["full_mc_calibration"]

    # Load MC tag efficiencies for f_s
    with open(P3_OUT / "tag_efficiencies.json") as f:
        eff_data = json.load(f)
    # Build f_s lookup: need data f_s for 10% data WPs
    # Use MC f_s as approximation (data/MC f_s are very close)
    mc_fs_by_wp = {}
    for entry in eff_data["combined_mc"]:
        mc_fs_by_wp[entry["threshold"]] = entry["f_s"]

    KAPPA_VALUES = [0.3, 0.5, 1.0, 2.0]
    KAPPA_LABELS = {0.3: "k0.3", 0.5: "k0.5", 1.0: "k1.0", 2.0: "k2.0"}
    thresholds = [2.0, 3.0, 5.0, 7.0, 9.0, 10.0]

    all_kappa_results = []

    for kappa in KAPPA_VALUES:
        k_str = KAPPA_LABELS[kappa]
        log.info("\n" + "=" * 50)
        log.info("kappa = %.1f", kappa)
        log.info("=" * 50)

        qfb_key = "data_qfb_%s" % k_str
        qfb_data = jc_data[qfb_key]

        per_wp_results = []
        for thr in thresholds:
            slope_result = measure_qfb_slope(
                qfb_data, cos_theta_data, data_h0, data_h1, thr)
            if slope_result is None:
                continue

            f_s = mc_fs_by_wp.get(thr)
            purity = estimate_purity_at_wp(mc_cal, f_s) if f_s else None
            if purity is None:
                continue

            # CRITICAL: pass afb_c=AFB_C_DATA for data extraction
            extraction = extract_afb_purity_corrected(
                slope_result["slope"], slope_result["sigma_slope"],
                purity, kappa,
                afb_c=AFB_C_DATA, afb_uds=AFB_UDS_DATA)
            if extraction is None:
                continue

            log.info("WP %.1f: slope=%.6f +/- %.6f, afb_purity=%.4f +/- %.4f, "
                     "f_b=%.3f, charm_corr=%.6f, chi2/ndf=%.2f/%d",
                     thr, slope_result["slope"], slope_result["sigma_slope"],
                     extraction["afb_purity_corrected"],
                     extraction["sigma_afb_purity"],
                     extraction["f_b"],
                     extraction["charm_correction"],
                     slope_result["chi2"], slope_result["ndf"])

            per_wp_results.append({
                "threshold": float(thr),
                "slope": slope_result,
                "purity": purity,
                "extraction": extraction,
            })

        # Multi-WP combination
        if len(per_wp_results) >= 2:
            afb_vals = np.array([r["extraction"]["afb_purity_corrected"]
                                 for r in per_wp_results])
            afb_errs = np.array([r["extraction"]["sigma_afb_purity"]
                                 for r in per_wp_results])
            w = 1.0 / afb_errs**2
            afb_combined = float(np.sum(w * afb_vals) / np.sum(w))
            sigma_combined = float(1.0 / np.sqrt(np.sum(w)))

            chi2_wp = float(np.sum((afb_vals - afb_combined)**2 / afb_errs**2))
            ndf_wp = len(afb_vals) - 1
            p_wp = float(1.0 - chi2_dist.cdf(chi2_wp, ndf_wp))

            log.info("Combined A_FB^b = %.4f +/- %.4f, chi2/ndf=%.2f/%d, p=%.3f",
                     afb_combined, sigma_combined, chi2_wp, ndf_wp, p_wp)
        else:
            if per_wp_results:
                afb_combined = per_wp_results[0]["extraction"]["afb_purity_corrected"]
                sigma_combined = per_wp_results[0]["extraction"]["sigma_afb_purity"]
            else:
                afb_combined = float("nan")
                sigma_combined = float("nan")
            chi2_wp, ndf_wp, p_wp = 0.0, 0, 1.0

        # Toy uncertainty at best WP
        best_wp = (min(per_wp_results,
                       key=lambda r: r["extraction"]["sigma_afb_purity"])
                   if per_wp_results else None)
        if best_wp:
            afb_mean_toy, afb_sigma_toy, _, n_valid_toy = toy_uncertainty_afb(
                qfb_data, cos_theta_data, data_h0, data_h1,
                best_wp["threshold"], best_wp["purity"], kappa,
                afb_c=AFB_C_DATA, afb_uds=AFB_UDS_DATA,
                n_toys=N_TOYS, seed=TOY_SEED)
            log.info("Toy uncertainty at WP %.1f: sigma=%.4f (n_valid=%d)",
                     best_wp["threshold"], afb_sigma_toy, n_valid_toy)
        else:
            afb_sigma_toy = float("nan")
            n_valid_toy = 0

        kappa_result = {
            "kappa": float(kappa),
            "per_wp_results": per_wp_results,
            "combination": {
                "A_FB_b": afb_combined if not np.isnan(afb_combined) else None,
                "sigma_A_FB_b": sigma_combined if not np.isnan(sigma_combined) else None,
                "sigma_A_FB_b_toy": float(afb_sigma_toy) if not np.isnan(afb_sigma_toy) else None,
                "chi2_wp": float(chi2_wp),
                "ndf_wp": int(ndf_wp),
                "p_wp": float(p_wp),
            },
            "published_delta": PUBLISHED_DELTA.get(kappa),
        }
        all_kappa_results.append(kappa_result)

    # ================================================================
    # Cross-kappa combination
    # ================================================================
    log.info("\n--- Cross-Kappa Combination ---")
    afb_per_kappa = []
    err_per_kappa = []
    kappa_list = []

    for kr in all_kappa_results:
        comb = kr["combination"]
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

        log.info("Final A_FB^b = %.4f +/- %.4f", afb_final, sigma_final)
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
    # Comparison with Phase 4a (MC expected)
    # ================================================================
    log.info("\n--- Comparison with Phase 4a (MC expected) ---")
    log.info("NOTE: Phase 4a MC has A_FB=0 by construction (symmetric MC).")
    log.info("Data A_FB^b should be non-zero (~0.10 at LEP).")
    log.info("Published LEP A_FB^b = %.4f (observed)", AFB_B_OBS)
    if not np.isnan(afb_final) and sigma_final > 0:
        pull_vs_lep = (afb_final - AFB_B_OBS) / sigma_final
        log.info("Our A_FB^b = %.4f +/- %.4f", afb_final, sigma_final)
        log.info("Pull vs LEP published = %.2f sigma", pull_vs_lep)
    else:
        pull_vs_lep = None

    # ================================================================
    # Output
    # ================================================================
    output = {
        "method": "Purity-corrected A_FB^b with published delta_b, 10% data",
        "description": (
            "A_FB^b extraction on 10% data using published ALEPH charge "
            "separations (hep-ex/0509008 Table 12) and MC-calibrated flavour "
            "fractions. Uses afb_c=0.0682 (published charm asymmetry). "
            "This is the PRIMARY A_FB^b method per REGRESSION_TICKET.md."
        ),
        "n_data_events": n_data,
        "subsample_seed": 42,
        "subsample_fraction": 0.10,
        "afb_c_used": AFB_C_DATA,
        "afb_uds_used": AFB_UDS_DATA,
        "kappa_results": all_kappa_results,
        "combination": {
            "A_FB_b": afb_final if not np.isnan(afb_final) else None,
            "sigma_A_FB_b": sigma_final if not np.isnan(sigma_final) else None,
            "A_FB_0_b": float(afb_0_b) if not np.isnan(afb_0_b) else None,
            "chi2_kappa": float(chi2_kappa),
            "ndf_kappa": int(ndf_kappa),
            "p_kappa": float(p_kappa) if not np.isnan(p_kappa) else None,
            "kappas_used": kappa_list,
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
        "qcd_correction": {
            "delta_QCD": DELTA_QCD,
            "delta_QCD_err": DELTA_QCD_ERR,
            "delta_QED": DELTA_QED,
        },
        "published_delta_source": "ALEPH hep-ex/0509008 Table 12",
        "n_toys": N_TOYS,
    }

    out_path = PHASE4B_OUT / "purity_afb_10pct.json"
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
        params["A_FB_b_10pct"] = {
            "value": afb_final,
            "stat": sigma_final,
            "SM": AFB_B_SM_POLE,
            "LEP_observed": AFB_B_OBS,
            "method": "Purity-corrected, published delta_b, afb_c=0.0682, 10% data",
            "subsample_seed": 42,
            "subsample_fraction": 0.10,
            "n_events": n_data,
            "afb_c_used": AFB_C_DATA,
        }
    if not np.isnan(afb_0_b):
        params["A_FB_0_b_10pct"] = {
            "value": float(afb_0_b),
            "stat": float(sigma_final / (1 - DELTA_QCD - DELTA_QED)) if not np.isnan(sigma_final) else None,
            "SM": AFB_B_SM_POLE,
        }
    if not np.isnan(sin2theta_fit):
        params["sin2theta_eff_10pct"] = {
            "value": float(sin2theta_fit),
            "stat": float(sigma_sin2theta) if not np.isnan(sigma_sin2theta) else None,
            "SM": SIN2_THETA_SM,
        }

    with open(params_path, "w") as f:
        json.dump(params, f, indent=2)
    log.info("Updated parameters.json with A_FB_b_10pct entries")


if __name__ == "__main__":
    main()
