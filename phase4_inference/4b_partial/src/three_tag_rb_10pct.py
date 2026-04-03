"""Phase 4b REGRESSION: 3-tag R_b extraction on 10% data.

Adapts the Phase 4a three_tag_rb_extraction.py for 10% real data.
Calibration is performed on full MC; extraction on 10% data subsample.

The 3-tag system defines:
  Tag 1 (tight): combined score > thr_tight  (b-enriched)
  Tag 2 (loose): thr_loose < score <= thr_tight  (b+c enriched)
  Tag 3 (anti):  score <= thr_loose  (uds-enriched)

Reads: phase4_inference/4b_partial/outputs/data_10pct_tags.npz
       phase3_selection/outputs/hemisphere_tags.npz
       phase4_inference/4a_expected/outputs/correlation_results.json
Writes: phase4_inference/4b_partial/outputs/three_tag_rb_10pct.json
        analysis_note/results/parameters.json (updates R_b_10pct_3tag)
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
PHASE4B_OUT = HERE.parent / "outputs"
P4A_OUT = HERE.parents[1] / "4a_expected" / "outputs"
P3_OUT = HERE.parents[2] / "phase3_selection" / "outputs"
RESULTS_DIR = HERE.parents[2] / "analysis_note" / "results"
PHASE4B_OUT.mkdir(parents=True, exist_ok=True)

# Import 3-tag functions from Phase 4a
sys.path.insert(0, str(HERE.parents[1] / "4a_expected" / "src"))
from three_tag_rb_extraction import (
    count_three_tag, calibrate_three_tag_efficiencies,
    extract_rb_three_tag, toy_uncertainty_three_tag,
    R_B_SM, R_C_SM, R_UDS_SM,
)

N_TOYS = 1000
TOY_SEED = 54321


def main():
    log.info("=" * 60)
    log.info("Phase 4b REGRESSION: 3-Tag R_b on 10%% Data")
    log.info("=" * 60)

    # ================================================================
    # Load data
    # ================================================================
    data_tags = np.load(PHASE4B_OUT / "data_10pct_tags.npz", allow_pickle=False)
    data_h0 = data_tags["data_combined_h0"]
    data_h1 = data_tags["data_combined_h1"]
    n_data = len(data_h0)
    log.info("10%% data events: %d", n_data)

    # Load MC tags for calibration
    mc_tags = np.load(P3_OUT / "hemisphere_tags.npz", allow_pickle=False)
    mc_h0 = mc_tags["mc_combined_h0"]
    mc_h1 = mc_tags["mc_combined_h1"]
    n_mc = len(mc_h0)
    log.info("MC events for calibration: %d", n_mc)

    # Load correlation results for C_b values
    with open(P4A_OUT / "correlation_results.json") as f:
        corr = json.load(f)
    cb_mc_by_wp = {entry["threshold"]: entry["C"]
                   for entry in corr["mc_vs_wp"]}
    cb_data_by_wp = {entry["threshold"]: entry["C"]
                     for entry in corr.get("data_vs_wp", [])}

    # ================================================================
    # Threshold configurations (same as Phase 4a)
    # ================================================================
    threshold_configs = [
        (10.0, 5.0), (10.0, 3.0), (8.0, 4.0), (8.0, 3.0),
        (12.0, 6.0), (7.0, 3.0), (9.0, 4.0), (9.0, 5.0),
    ]

    # ================================================================
    # 1. Calibrate efficiencies on full MC
    # ================================================================
    log.info("\n--- MC Calibration (full MC) ---")
    calibrations = {}
    for thr_tight, thr_loose in threshold_configs:
        label = "tight=%.0f, loose=%.0f" % (thr_tight, thr_loose)
        counts_mc = count_three_tag(mc_h0, mc_h1, thr_tight, thr_loose)
        cal = calibrate_three_tag_efficiencies(counts_mc, R_B_SM, R_C_SM)
        calibrations[(thr_tight, thr_loose)] = cal
        log.info("%s: eps_b_t=%.4f, eps_c_t=%.4f, eps_uds_t=%.5f, chi2=%.2e",
                 label, cal["eps_b_tight"], cal["eps_c_tight"],
                 cal["eps_uds_tight"], cal["chi2_calibration"])

    # ================================================================
    # 2. Extract R_b from 10% data at each configuration
    # ================================================================
    log.info("\n--- R_b Extraction from 10%% Data ---")

    all_results = []
    for thr_tight, thr_loose in threshold_configs:
        label = "tight=%.0f, loose=%.0f" % (thr_tight, thr_loose)
        cal = calibrations[(thr_tight, thr_loose)]

        # Count tags in 10% data
        counts_data = count_three_tag(data_h0, data_h1, thr_tight, thr_loose)

        # Get C_b at the tight WP (MC value; data-MC diff handled as systematic)
        C_b_tight = cb_mc_by_wp.get(thr_tight, 1.0)

        # Extract R_b
        extraction = extract_rb_three_tag(
            counts_data, cal, R_C_SM,
            C_b_tight=C_b_tight,
        )

        # Toy-based statistical uncertainty
        rb_mean, rb_sigma, rb_toys, n_valid = toy_uncertainty_three_tag(
            data_h0, data_h1, thr_tight, thr_loose,
            cal, R_C_SM, n_toys=N_TOYS, seed=TOY_SEED)

        log.info("%s: R_b=%.5f +/- %.5f (toys=%d/%d), chi2/ndf=%.2f/%d, p=%.3f",
                 label, extraction["R_b"], rb_sigma if not np.isnan(rb_sigma) else 0.0,
                 n_valid, N_TOYS,
                 extraction["chi2"], extraction["ndf"],
                 extraction["p_value"])

        all_results.append({
            "thr_tight": float(thr_tight),
            "thr_loose": float(thr_loose),
            "label": label,
            "counts_data": counts_data,
            "calibration": cal,
            "C_b_tight": float(C_b_tight),
            "R_b": extraction["R_b"],
            "chi2": extraction["chi2"],
            "ndf": extraction["ndf"],
            "p_value": extraction["p_value"],
            "R_b_toy_mean": float(rb_mean) if not np.isnan(rb_mean) else None,
            "sigma_stat": float(rb_sigma) if not np.isnan(rb_sigma) else None,
            "n_valid_toys": n_valid,
        })

    # ================================================================
    # 3. Select best and combined
    # ================================================================
    valid_results = [r for r in all_results
                     if r["sigma_stat"] is not None and r["sigma_stat"] > 0
                     and 0.05 < r["R_b"] < 0.50]

    if valid_results:
        best = min(valid_results, key=lambda x: x["sigma_stat"])
        log.info("\n--- Best Configuration ---")
        log.info("Config: %s", best["label"])
        log.info("R_b = %.5f +/- %.5f (stat)", best["R_b"], best["sigma_stat"])
        log.info("SM R_b = %.5f", R_B_SM)
        if best["sigma_stat"] > 0:
            log.info("Pull = %.2f",
                     abs(best["R_b"] - R_B_SM) / best["sigma_stat"])
    else:
        best = None
        log.warning("No valid extraction found!")

    # Operating point stability (weighted average)
    stable = [r for r in all_results
              if r["sigma_stat"] is not None and r["sigma_stat"] > 0
              and 0.05 < r["R_b"] < 0.50]

    if len(stable) >= 2:
        rb_vals = np.array([r["R_b"] for r in stable])
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
        rb_combined = best["R_b"] if best else None
        sigma_combined = best["sigma_stat"] if best else None
        chi2_stab, ndf_stab, p_stab = 0.0, 0, 1.0
        stability_passes = True

    # ================================================================
    # 4. Comparison with Phase 4a MC expected
    # ================================================================
    log.info("\n--- Comparison with Phase 4a (MC expected) ---")
    with open(P4A_OUT / "three_tag_rb_results.json") as f:
        mc_results = json.load(f)

    mc_rb = mc_results["stability"]["R_b_combined"]
    mc_sigma = mc_results["stability"]["sigma_combined"]
    if best and mc_sigma and best["sigma_stat"]:
        pull_vs_mc = (best["R_b"] - mc_rb) / np.sqrt(
            best["sigma_stat"]**2 + mc_sigma**2)
        log.info("Data R_b = %.5f +/- %.5f", best["R_b"], best["sigma_stat"])
        log.info("MC R_b   = %.5f +/- %.5f", mc_rb, mc_sigma)
        log.info("Pull (data - MC) = %.2f sigma", pull_vs_mc)
    else:
        pull_vs_mc = None

    # ================================================================
    # 5. Output
    # ================================================================
    output = {
        "method": "3-tag system (tight/loose/anti-b), 10% data",
        "description": (
            "R_b extraction using the 3-tag system on 10% data subsample "
            "(seed=42, 288627 events). Efficiencies calibrated on full MC. "
            "This is the PRIMARY R_b method per REGRESSION_TICKET.md."
        ),
        "n_data_events": n_data,
        "subsample_seed": 42,
        "subsample_fraction": 0.10,
        "all_results": all_results,
        "best_config": best,
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
            "data_R_b": best["R_b"] if best else None,
            "data_sigma": best["sigma_stat"] if best else None,
            "pull": float(pull_vs_mc) if pull_vs_mc is not None else None,
        },
        "sm_values": {
            "R_b": R_B_SM,
            "R_c": R_C_SM,
        },
        "n_toys": N_TOYS,
    }

    out_path = PHASE4B_OUT / "three_tag_rb_10pct.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    log.info("\nSaved %s", out_path.name)

    # ================================================================
    # 6. Update parameters.json
    # ================================================================
    params_path = RESULTS_DIR / "parameters.json"
    if params_path.exists():
        with open(params_path) as f:
            params = json.load(f)
    else:
        params = {}

    if best:
        params["R_b_10pct_3tag"] = {
            "value": best["R_b"],
            "stat": best["sigma_stat"],
            "SM": R_B_SM,
            "working_point": best["label"],
            "method": "3-tag system (tight/loose/anti-b), 10% data",
            "subsample_seed": 42,
            "subsample_fraction": 0.10,
            "n_events": n_data,
        }
    if rb_combined is not None:
        params["R_b_10pct_3tag_combined"] = {
            "value": rb_combined,
            "stat": sigma_combined,
            "SM": R_B_SM,
            "method": "3-tag combined across WPs, 10% data",
            "n_configs": len(stable),
            "stability_chi2_ndf": chi2_stab / ndf_stab if ndf_stab > 0 else None,
            "stability_p": p_stab,
        }

    with open(params_path, "w") as f:
        json.dump(params, f, indent=2)
    log.info("Updated parameters.json with R_b_10pct_3tag entries")


if __name__ == "__main__":
    main()
