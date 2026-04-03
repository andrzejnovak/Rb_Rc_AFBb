"""Phase 4c: Per-year R_b and A_FB^b extraction for consistency check.

Splits the full data by year (1992, 1993, 1994, 1995) and extracts
R_b and A_FB^b independently for each year.

Reads: phase3_selection/outputs/hemisphere_tags.npz
       phase3_selection/outputs/jet_charge.npz
       phase3_selection/outputs/preselected_data.npz (for year info)
       phase4_inference/4a_expected/outputs/correlation_results.json
       phase4_inference/4a_expected/outputs/mc_calibration.json
       phase3_selection/outputs/tag_efficiencies.json
Writes: phase4_inference/4c_observed/outputs/per_year_results.json
"""
import json
import logging
import sys
from pathlib import Path

import numpy as np
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
PHASE4C_OUT.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(HERE.parents[1] / "4a_expected" / "src"))
from three_tag_rb_extraction import (
    count_three_tag, calibrate_three_tag_efficiencies,
    extract_rb_three_tag, toy_uncertainty_three_tag,
    R_B_SM, R_C_SM,
)
from purity_corrected_afb import (
    estimate_purity_at_wp, measure_qfb_slope, extract_afb_purity_corrected,
    PUBLISHED_DELTA, R_B_SM, R_C_SM, AFB_B_OBS,
)

AFB_C_DATA = 0.0682
N_TOYS = 500
TOY_SEED = 12345


def main():
    log.info("=" * 60)
    log.info("Phase 4c: Per-Year Extraction")
    log.info("=" * 60)

    # Load data with year info
    data = np.load(P3_OUT / "preselected_data.npz", allow_pickle=False)
    year = data["year"]

    tags = np.load(P3_OUT / "hemisphere_tags.npz", allow_pickle=False)
    data_h0 = tags["data_combined_h0"]
    data_h1 = tags["data_combined_h1"]
    mc_h0 = tags["mc_combined_h0"]
    mc_h1 = tags["mc_combined_h1"]

    jc = np.load(P3_OUT / "jet_charge.npz", allow_pickle=False)
    cos_theta_data = jc["cos_theta_data"]

    # Load MC calibration
    with open(P4A_OUT / "correlation_results.json") as f:
        corr = json.load(f)
    cb_mc_by_wp = {entry["threshold"]: entry["C"]
                   for entry in corr["mc_vs_wp"]}

    with open(P4A_OUT / "mc_calibration.json") as f:
        mc_cal_data = json.load(f)
    mc_cal = mc_cal_data["full_mc_calibration"]

    with open(P3_OUT / "tag_efficiencies.json") as f:
        eff_data = json.load(f)
    mc_fs_by_wp = {}
    for entry in eff_data["combined_mc"]:
        mc_fs_by_wp[entry["threshold"]] = entry["f_s"]

    # Use the best config from the full extraction
    thr_tight, thr_loose = 10.0, 5.0  # Will be updated if full result says otherwise
    rb_full_path = PHASE4C_OUT / "three_tag_rb_fulldata.json"
    if rb_full_path.exists():
        with open(rb_full_path) as f:
            full_rb = json.load(f)
        if full_rb.get("best_config") and full_rb["best_config"].get("thr_tight"):
            thr_tight = full_rb["best_config"]["thr_tight"]
            thr_loose = full_rb["best_config"]["thr_loose"]
    log.info("Using WP: tight=%.0f, loose=%.0f", thr_tight, thr_loose)

    C_b_tight = cb_mc_by_wp.get(thr_tight, 1.0)

    # MC calibration (full MC, same for all years since MC is 1994 only)
    counts_mc = count_three_tag(mc_h0, mc_h1, thr_tight, thr_loose)
    cal_mc = calibrate_three_tag_efficiencies(counts_mc, R_B_SM, R_C_SM)

    years = sorted(set(year))
    log.info("Years found: %s", years)

    per_year_results = []

    for yr in years:
        yr_mask = year == yr
        n_yr = int(np.sum(yr_mask))
        log.info("\n--- Year %d: %d events ---", yr, n_yr)

        h0_yr = data_h0[yr_mask]
        h1_yr = data_h1[yr_mask]

        # R_b extraction (SF-calibrated)
        counts_data = count_three_tag(h0_yr, h1_yr, thr_tight, thr_loose)

        # Scale factors
        sf_tight = counts_data["f_s_tight"] / max(counts_mc["f_s_tight"], 1e-10)
        sf_loose = counts_data["f_s_loose"] / max(counts_mc["f_s_loose"], 1e-10)

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

        ext_sf = extract_rb_three_tag(counts_data, cal_sf, R_C_SM, C_b_tight=C_b_tight)
        ext_raw = extract_rb_three_tag(counts_data, cal_mc, R_C_SM, C_b_tight=C_b_tight)

        # Toy uncertainty
        rb_mean, rb_sigma, _, n_valid = toy_uncertainty_three_tag(
            h0_yr, h1_yr, thr_tight, thr_loose,
            cal_sf, R_C_SM, n_toys=N_TOYS, seed=TOY_SEED + yr)

        log.info("R_b(SF) = %.5f +/- %.5f, R_b(raw) = %.5f, chi2=%.2f",
                 ext_sf["R_b"], rb_sigma if not np.isnan(rb_sigma) else 0,
                 ext_raw["R_b"], ext_sf["chi2"])

        # A_FB^b at kappa=2.0 (best single kappa)
        qfb_data = jc["data_qfb_k2.0"][yr_mask]
        cos_yr = cos_theta_data[yr_mask]

        afb_yr = None
        sigma_afb_yr = None
        thr_afb = 5.0  # Use moderate WP for AFB
        slope_result = measure_qfb_slope(
            qfb_data, cos_yr, h0_yr, h1_yr, thr_afb)
        if slope_result is not None:
            f_s = mc_fs_by_wp.get(thr_afb)
            purity = estimate_purity_at_wp(mc_cal, f_s) if f_s else None
            if purity is not None:
                extraction = extract_afb_purity_corrected(
                    slope_result["slope"], slope_result["sigma_slope"],
                    purity, 2.0,
                    afb_c=AFB_C_DATA, afb_uds=0.0)
                if extraction is not None:
                    afb_yr = extraction["afb_purity_corrected"]
                    sigma_afb_yr = extraction["sigma_afb_purity"]
                    log.info("A_FB^b(k=2) = %.4f +/- %.4f",
                             afb_yr, sigma_afb_yr)

        per_year_results.append({
            "year": int(yr),
            "n_events": n_yr,
            "R_b_sf": ext_sf["R_b"],
            "R_b_raw": ext_raw["R_b"],
            "sigma_stat_rb": float(rb_sigma) if not np.isnan(rb_sigma) else None,
            "chi2_rb": ext_sf["chi2"],
            "ndf_rb": ext_sf["ndf"],
            "p_value_rb": ext_sf["p_value"],
            "sf_tight": float(sf_tight),
            "sf_loose": float(sf_loose),
            "A_FB_b": float(afb_yr) if afb_yr is not None else None,
            "sigma_stat_afb": float(sigma_afb_yr) if sigma_afb_yr is not None else None,
        })

    # Per-year consistency check
    log.info("\n--- Per-Year Consistency ---")
    valid_rb = [r for r in per_year_results
                if r["sigma_stat_rb"] is not None and r["sigma_stat_rb"] > 0
                and 0.05 < r["R_b_sf"] < 0.50]

    if len(valid_rb) >= 2:
        rb_vals = np.array([r["R_b_sf"] for r in valid_rb])
        rb_errs = np.array([r["sigma_stat_rb"] for r in valid_rb])
        w = 1.0 / rb_errs**2
        rb_avg = np.sum(w * rb_vals) / np.sum(w)
        chi2_yr = float(np.sum((rb_vals - rb_avg)**2 / rb_errs**2))
        ndf_yr = len(valid_rb) - 1
        p_yr = float(1.0 - chi2_dist.cdf(chi2_yr, ndf_yr))
        log.info("R_b per-year chi2/ndf = %.2f/%d, p = %.4f",
                 chi2_yr, ndf_yr, p_yr)
    else:
        chi2_yr, ndf_yr, p_yr = 0.0, 0, 1.0

    valid_afb = [r for r in per_year_results
                 if r["A_FB_b"] is not None and r["sigma_stat_afb"] is not None
                 and r["sigma_stat_afb"] > 0]

    if len(valid_afb) >= 2:
        afb_vals = np.array([r["A_FB_b"] for r in valid_afb])
        afb_errs = np.array([r["sigma_stat_afb"] for r in valid_afb])
        w = 1.0 / afb_errs**2
        afb_avg = np.sum(w * afb_vals) / np.sum(w)
        chi2_afb = float(np.sum((afb_vals - afb_avg)**2 / afb_errs**2))
        ndf_afb = len(valid_afb) - 1
        p_afb = float(1.0 - chi2_dist.cdf(chi2_afb, ndf_afb))
        log.info("A_FB per-year chi2/ndf = %.2f/%d, p = %.4f",
                 chi2_afb, ndf_afb, p_afb)
    else:
        chi2_afb, ndf_afb, p_afb = 0.0, 0, 1.0

    output = {
        "description": "Per-year R_b and A_FB^b extraction for consistency check",
        "working_point": {"thr_tight": thr_tight, "thr_loose": thr_loose},
        "per_year": per_year_results,
        "consistency_rb": {
            "chi2": chi2_yr,
            "ndf": ndf_yr,
            "p_value": p_yr,
            "passes": p_yr > 0.01,
        },
        "consistency_afb": {
            "chi2": chi2_afb,
            "ndf": ndf_afb,
            "p_value": p_afb,
            "passes": p_afb > 0.01,
        },
    }

    out_path = PHASE4C_OUT / "per_year_results.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    log.info("\nSaved %s", out_path.name)


if __name__ == "__main__":
    main()
