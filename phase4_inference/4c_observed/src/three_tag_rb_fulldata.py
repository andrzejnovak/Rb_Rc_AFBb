"""Phase 4c: 3-tag R_b extraction on FULL data (2,887,261 events).

The primary R_b measurement. Uses the 3-tag system (tight/loose/anti-b)
calibrated on full MC. Extracts R_b from the complete ALEPH 1992-1995 dataset.

Also computes scale-factor calibration: SF_i = f_s_i(data) / f_s_i(MC)
to correct for data/MC tagging efficiency mismatch.

Reads: phase3_selection/outputs/hemisphere_tags.npz (full data + MC)
       phase4_inference/4a_expected/outputs/correlation_results.json
       phase4_inference/4b_partial/outputs/three_tag_rb_10pct.json
Writes: phase4_inference/4c_observed/outputs/three_tag_rb_fulldata.json
        analysis_note/results/parameters.json
"""
import json
import logging
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize, minimize_scalar
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
P4B_OUT = HERE.parents[1] / "4b_partial" / "outputs"
P3_OUT = HERE.parents[2] / "phase3_selection" / "outputs"
RESULTS_DIR = HERE.parents[2] / "analysis_note" / "results"
PHASE4C_OUT.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Import 3-tag functions from Phase 4a
sys.path.insert(0, str(HERE.parents[1] / "4a_expected" / "src"))
from three_tag_rb_extraction import (
    count_three_tag, calibrate_three_tag_efficiencies,
    extract_rb_three_tag, toy_uncertainty_three_tag,
    R_B_SM, R_C_SM, R_UDS_SM,
)

N_TOYS = 1000
TOY_SEED = 54321


def compute_sf_calibrated_extraction(
    data_h0, data_h1, mc_h0, mc_h1,
    thr_tight, thr_loose, R_c, C_b_tight=1.0
):
    """Extract R_b with scale-factor calibration.

    Step 1: Calibrate efficiencies from MC (using known R_b^MC).
    Step 2: Compute data/MC tag-rate scale factors.
    Step 3: Correct MC efficiencies using SFs.
    Step 4: Extract R_b from data with SF-corrected efficiencies.
    """
    # MC calibration
    counts_mc = count_three_tag(mc_h0, mc_h1, thr_tight, thr_loose)
    cal_mc = calibrate_three_tag_efficiencies(counts_mc, R_B_SM, R_C_SM)

    # Data tag fractions
    counts_data = count_three_tag(data_h0, data_h1, thr_tight, thr_loose)

    # Scale factors: ratio of data to MC single-tag fractions
    sf_tight = counts_data["f_s_tight"] / max(counts_mc["f_s_tight"], 1e-10)
    sf_loose = counts_data["f_s_loose"] / max(counts_mc["f_s_loose"], 1e-10)
    sf_anti = counts_data["f_s_anti"] / max(counts_mc["f_s_anti"], 1e-10)

    # SF-corrected efficiencies
    cal_sf = dict(cal_mc)
    cal_sf["eps_b_tight"] = min(cal_mc["eps_b_tight"] * sf_tight, 0.999)
    cal_sf["eps_b_loose"] = min(cal_mc["eps_b_loose"] * sf_loose, 0.999)
    cal_sf["eps_b_anti"] = max(1.0 - cal_sf["eps_b_tight"] - cal_sf["eps_b_loose"], 0.001)

    cal_sf["eps_c_tight"] = min(cal_mc["eps_c_tight"] * sf_tight, 0.999)
    cal_sf["eps_c_loose"] = min(cal_mc["eps_c_loose"] * sf_loose, 0.999)
    cal_sf["eps_c_anti"] = max(1.0 - cal_sf["eps_c_tight"] - cal_sf["eps_c_loose"], 0.001)

    cal_sf["eps_uds_tight"] = min(cal_mc["eps_uds_tight"] * sf_tight, 0.999)
    cal_sf["eps_uds_loose"] = min(cal_mc["eps_uds_loose"] * sf_loose, 0.999)
    cal_sf["eps_uds_anti"] = max(1.0 - cal_sf["eps_uds_tight"] - cal_sf["eps_uds_loose"], 0.001)

    # Extract R_b with SF-corrected calibration
    extraction = extract_rb_three_tag(
        counts_data, cal_sf, R_c, C_b_tight=C_b_tight)

    return extraction, cal_mc, cal_sf, counts_data, counts_mc, {
        "sf_tight": sf_tight, "sf_loose": sf_loose, "sf_anti": sf_anti
    }


def main():
    log.info("=" * 60)
    log.info("Phase 4c: 3-Tag R_b on FULL Data (ALL years)")
    log.info("=" * 60)

    # ================================================================
    # Load data
    # ================================================================
    tags = np.load(P3_OUT / "hemisphere_tags.npz", allow_pickle=False)
    data_h0 = tags["data_combined_h0"]
    data_h1 = tags["data_combined_h1"]
    mc_h0 = tags["mc_combined_h0"]
    mc_h1 = tags["mc_combined_h1"]
    n_data = len(data_h0)
    n_mc = len(mc_h0)
    log.info("Full data events: %d", n_data)
    log.info("MC events for calibration: %d", n_mc)

    # Load correlation results for C_b values
    with open(P4A_OUT / "correlation_results.json") as f:
        corr = json.load(f)
    cb_mc_by_wp = {entry["threshold"]: entry["C"]
                   for entry in corr["mc_vs_wp"]}

    # ================================================================
    # Threshold configurations
    # ================================================================
    threshold_configs = [
        (10.0, 5.0), (10.0, 3.0), (8.0, 4.0), (8.0, 3.0),
        (12.0, 6.0), (7.0, 3.0), (9.0, 4.0), (9.0, 5.0),
    ]

    # ================================================================
    # 1. MC Calibration + SF-calibrated extraction at each config
    # ================================================================
    log.info("\n--- R_b Extraction from Full Data (SF-calibrated) ---")

    all_results = []
    for thr_tight, thr_loose in threshold_configs:
        label = "tight=%.0f, loose=%.0f" % (thr_tight, thr_loose)
        C_b_tight = cb_mc_by_wp.get(thr_tight, 1.0)

        # SF-calibrated extraction
        extraction, cal_mc, cal_sf, counts_data, counts_mc, sfs = \
            compute_sf_calibrated_extraction(
                data_h0, data_h1, mc_h0, mc_h1,
                thr_tight, thr_loose, R_C_SM, C_b_tight)

        # Also do raw MC-calibration extraction for comparison
        ext_raw = extract_rb_three_tag(
            counts_data, cal_mc, R_C_SM, C_b_tight=C_b_tight)

        # Toy-based statistical uncertainty (using SF-calibrated)
        rb_mean, rb_sigma, rb_toys, n_valid = toy_uncertainty_three_tag(
            data_h0, data_h1, thr_tight, thr_loose,
            cal_sf, R_C_SM, n_toys=N_TOYS, seed=TOY_SEED)

        log.info(
            "%s: R_b(SF)=%.5f +/- %.5f (toys=%d/%d), R_b(raw)=%.5f, "
            "chi2/ndf=%.2f/%d, p=%.3f, SF_t=%.3f, SF_l=%.3f, SF_a=%.3f",
            label, extraction["R_b"],
            rb_sigma if not np.isnan(rb_sigma) else 0.0,
            n_valid, N_TOYS,
            ext_raw["R_b"],
            extraction["chi2"], extraction["ndf"], extraction["p_value"],
            sfs["sf_tight"], sfs["sf_loose"], sfs["sf_anti"],
        )

        all_results.append({
            "thr_tight": float(thr_tight),
            "thr_loose": float(thr_loose),
            "label": label,
            "counts_data": counts_data,
            "counts_mc": counts_mc,
            "calibration_mc": cal_mc,
            "calibration_sf": cal_sf,
            "scale_factors": sfs,
            "C_b_tight": float(C_b_tight),
            "R_b_sf": extraction["R_b"],
            "R_b_raw": ext_raw["R_b"],
            "chi2_sf": extraction["chi2"],
            "ndf": extraction["ndf"],
            "p_value_sf": extraction["p_value"],
            "chi2_raw": ext_raw["chi2"],
            "p_value_raw": ext_raw["p_value"],
            "R_b_toy_mean": float(rb_mean) if not np.isnan(rb_mean) else None,
            "sigma_stat": float(rb_sigma) if not np.isnan(rb_sigma) else None,
            "n_valid_toys": n_valid,
        })

    # ================================================================
    # 2. Select best and combined
    # ================================================================
    valid_results = [r for r in all_results
                     if r["sigma_stat"] is not None and r["sigma_stat"] > 0
                     and 0.05 < r["R_b_sf"] < 0.50]

    if valid_results:
        best = min(valid_results, key=lambda x: x["sigma_stat"])
        log.info("\n--- Best Configuration (SF-calibrated) ---")
        log.info("Config: %s", best["label"])
        log.info("R_b(SF) = %.5f +/- %.5f (stat)", best["R_b_sf"], best["sigma_stat"])
        log.info("R_b(raw) = %.5f", best["R_b_raw"])
        log.info("SM R_b = %.5f", R_B_SM)
        if best["sigma_stat"] > 0:
            log.info("Pull(SF) = %.2f",
                     abs(best["R_b_sf"] - R_B_SM) / best["sigma_stat"])
    else:
        best = None
        log.warning("No valid extraction found!")

    # Operating point stability (weighted average)
    stable = [r for r in all_results
              if r["sigma_stat"] is not None and r["sigma_stat"] > 0
              and 0.05 < r["R_b_sf"] < 0.50]

    if len(stable) >= 2:
        rb_vals = np.array([r["R_b_sf"] for r in stable])
        rb_errs = np.array([r["sigma_stat"] for r in stable])
        w = 1.0 / rb_errs**2
        rb_combined = float(np.sum(w * rb_vals) / np.sum(w))
        sigma_combined = float(1.0 / np.sqrt(np.sum(w)))
        chi2_stab = float(np.sum((rb_vals - rb_combined)**2 / rb_errs**2))
        ndf_stab = len(stable) - 1
        p_stab = float(1.0 - chi2_dist.cdf(chi2_stab, ndf_stab))
        stability_passes = p_stab > 0.05

        log.info("\n--- Operating Point Stability ---")
        log.info("Combined R_b = %.5f +/- %.5f", rb_combined, sigma_combined)
        log.info("Stability chi2/ndf = %.2f/%d, p = %.4f %s",
                 chi2_stab, ndf_stab, p_stab,
                 "PASS" if stability_passes else "FAIL")
    else:
        rb_combined = best["R_b_sf"] if best else None
        sigma_combined = best["sigma_stat"] if best else None
        chi2_stab, ndf_stab, p_stab = 0.0, 0, 1.0
        stability_passes = True

    # ================================================================
    # 3. Comparison with Phase 4a and 4b
    # ================================================================
    log.info("\n--- Comparison with Phase 4a (MC expected) ---")
    with open(P4A_OUT / "three_tag_rb_results.json") as f:
        mc_results = json.load(f)
    mc_rb = mc_results["stability"]["R_b_combined"]
    mc_sigma = mc_results["stability"]["sigma_combined"]

    log.info("\n--- Comparison with Phase 4b (10%% data) ---")
    with open(P4B_OUT / "three_tag_rb_10pct.json") as f:
        partial_results = json.load(f)
    partial_rb = partial_results["stability"]["R_b_combined"]
    partial_sigma = partial_results["stability"]["sigma_combined"]

    pull_vs_mc = None
    pull_vs_10pct = None
    if best and best["sigma_stat"]:
        if mc_sigma:
            pull_vs_mc = (best["R_b_sf"] - mc_rb) / np.sqrt(
                best["sigma_stat"]**2 + mc_sigma**2)
            log.info("Pull vs MC = %.2f", pull_vs_mc)
        if partial_sigma:
            pull_vs_10pct = (best["R_b_sf"] - partial_rb) / np.sqrt(
                best["sigma_stat"]**2 + partial_sigma**2)
            log.info("Pull vs 10%% = %.2f", pull_vs_10pct)

    # ================================================================
    # 4. Output
    # ================================================================
    output = {
        "method": "3-tag system (tight/loose/anti-b), SF-calibrated, full data",
        "description": (
            "R_b extraction using the 3-tag system on the complete ALEPH "
            "1992-1995 dataset (%d events). Efficiencies calibrated on MC "
            "and corrected using data/MC scale factors. "
            "This is the PRIMARY R_b method." % n_data
        ),
        "n_data_events": n_data,
        "n_mc_events": n_mc,
        "all_results": all_results,
        "best_config": {
            "label": best["label"] if best else None,
            "R_b": best["R_b_sf"] if best else None,
            "sigma_stat": best["sigma_stat"] if best else None,
            "thr_tight": best["thr_tight"] if best else None,
            "thr_loose": best["thr_loose"] if best else None,
            "R_b_raw": best["R_b_raw"] if best else None,
            "chi2": best["chi2_sf"] if best else None,
            "ndf": best["ndf"] if best else None,
            "p_value": best["p_value_sf"] if best else None,
            "scale_factors": best["scale_factors"] if best else None,
        } if best else None,
        "stability": {
            "R_b_combined": rb_combined,
            "sigma_combined": sigma_combined,
            "chi2": float(chi2_stab),
            "ndf": int(ndf_stab),
            "p_value": float(p_stab),
            "passes": bool(stability_passes),
            "n_configs": len(stable),
        },
        "comparison_4a": {
            "mc_R_b": mc_rb,
            "mc_sigma": mc_sigma,
            "data_R_b": best["R_b_sf"] if best else None,
            "data_sigma": best["sigma_stat"] if best else None,
            "pull": float(pull_vs_mc) if pull_vs_mc is not None else None,
        },
        "comparison_4b": {
            "partial_R_b": partial_rb,
            "partial_sigma": partial_sigma,
            "full_R_b": best["R_b_sf"] if best else None,
            "full_sigma": best["sigma_stat"] if best else None,
            "pull": float(pull_vs_10pct) if pull_vs_10pct is not None else None,
        },
        "sm_values": {
            "R_b": R_B_SM,
            "R_c": R_C_SM,
        },
        "n_toys": N_TOYS,
    }

    out_path = PHASE4C_OUT / "three_tag_rb_fulldata.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    log.info("\nSaved %s", out_path.name)

    # ================================================================
    # 5. Update parameters.json
    # ================================================================
    params_path = RESULTS_DIR / "parameters.json"
    if params_path.exists():
        with open(params_path) as f:
            params = json.load(f)
    else:
        params = {}

    if best:
        params["R_b_fulldata_3tag"] = {
            "value": best["R_b_sf"],
            "stat": best["sigma_stat"],
            "SM": R_B_SM,
            "working_point": best["label"],
            "method": "3-tag system (SF-calibrated), full data",
            "n_events": n_data,
        }
    if rb_combined is not None:
        params["R_b_fulldata_3tag_combined"] = {
            "value": rb_combined,
            "stat": sigma_combined,
            "SM": R_B_SM,
            "method": "3-tag combined across WPs (SF-calibrated), full data",
            "n_configs": len(stable),
            "stability_chi2_ndf": chi2_stab / ndf_stab if ndf_stab > 0 else None,
            "stability_p": p_stab,
        }

    with open(params_path, "w") as f:
        json.dump(params, f, indent=2)
    log.info("Updated parameters.json with R_b_fulldata_3tag entries")


if __name__ == "__main__":
    main()
