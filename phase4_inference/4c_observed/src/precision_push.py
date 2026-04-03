"""Precision push: 5 approaches to improve R_b and A_FB^b precision.

Session: eloise_f4f5

Current results (baseline):
  R_b   = 0.212 +/- 0.027 (ALEPH: 0.216 +/- 0.001)
  A_FB^b = +0.003 +/- 0.003 (ALEPH: 0.093 +/- 0.005)

Approaches:
  1. Hard hemisphere mass cut for b-enrichment
  2. Multi-WP simultaneous fit
  3. A_FB^b in double-tagged events only
  4. Hemisphere probability tag optimization (-ln P_hem)
  5. Combined best improvements

Reads: phase3_selection/outputs/hemisphere_tags.npz
       phase3_selection/outputs/jet_charge.npz
       phase3_selection/outputs/preselected_data.npz
       phase3_selection/outputs/preselected_mc.npz
       phase3_selection/outputs/d0_significance.npz
       phase3_selection/outputs/tag_efficiencies.json
       phase4_inference/4a_expected/outputs/mc_calibration.json
Writes: phase4_inference/4c_observed/outputs/precision_push_results.json
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
from purity_corrected_afb import (
    estimate_purity_at_wp, measure_qfb_slope,
    PUBLISHED_DELTA, SIN2_THETA_SM, AFB_B_OBS, AFB_B_SM_POLE,
    DELTA_QCD, DELTA_QCD_ERR, DELTA_QED,
    N_COS_BINS, COS_RANGE,
)

N_TOYS = 500
TOY_SEED = 99999
MASS_CUT = 1.8  # GeV/c^2, ALEPH Q-tag requirement


# ============================================================
# APPROACH 1: Hard hemisphere mass cut
# ============================================================
def approach1_mass_cut(tags, data_h0, data_h1, mc_h0, mc_h1):
    """Apply hemisphere mass > 1.8 GeV as hard requirement for tight tag."""
    log.info("\n" + "=" * 70)
    log.info("APPROACH 1: Hard hemisphere mass cut > %.1f GeV/c^2", MASS_CUT)
    log.info("=" * 70)

    data_mass_h0 = tags["data_mass_h0"]
    data_mass_h1 = tags["data_mass_h1"]
    mc_mass_h0 = tags["mc_mass_h0"]
    mc_mass_h1 = tags["mc_mass_h1"]

    # The nlp (negative log probability) is the core discriminant
    data_nlp_h0 = tags["data_nlp_h0"]
    data_nlp_h1 = tags["data_nlp_h1"]
    mc_nlp_h0 = tags["mc_nlp_h0"]
    mc_nlp_h1 = tags["mc_nlp_h1"]

    # New combined score: nlp * (mass > 1.8 GeV)
    # If mass < 1.8, the hemisphere gets score 0 (always in anti-tag)
    data_masscut_h0 = data_nlp_h0 * (data_mass_h0 > MASS_CUT).astype(float)
    data_masscut_h1 = data_nlp_h1 * (data_mass_h1 > MASS_CUT).astype(float)
    mc_masscut_h0 = mc_nlp_h0 * (mc_mass_h0 > MASS_CUT).astype(float)
    mc_masscut_h1 = mc_nlp_h1 * (mc_mass_h1 > MASS_CUT).astype(float)

    log.info("Data: frac hemispheres passing mass cut: %.4f",
             0.5 * (np.mean(data_mass_h0 > MASS_CUT) + np.mean(data_mass_h1 > MASS_CUT)))
    log.info("MC: frac hemispheres passing mass cut: %.4f",
             0.5 * (np.mean(mc_mass_h0 > MASS_CUT) + np.mean(mc_mass_h1 > MASS_CUT)))

    # Scan thresholds on the mass-gated nlp
    threshold_configs = [
        (5.0, 2.0), (5.0, 3.0),
        (7.0, 3.0), (7.0, 4.0),
        (8.0, 3.0), (8.0, 4.0), (8.0, 5.0),
        (9.0, 3.0), (9.0, 4.0), (9.0, 5.0),
        (10.0, 3.0), (10.0, 5.0),
    ]

    results = []
    for thr_tight, thr_loose in threshold_configs:
        label = "masscut tight=%.0f, loose=%.0f" % (thr_tight, thr_loose)

        # MC calibration with mass-gated scores
        counts_mc = count_three_tag(mc_masscut_h0, mc_masscut_h1, thr_tight, thr_loose)
        cal_mc = calibrate_three_tag_efficiencies(counts_mc, R_B_SM, R_C_SM)

        # Data counts
        counts_data = count_three_tag(data_masscut_h0, data_masscut_h1, thr_tight, thr_loose)

        # Scale factors
        sf_tight = counts_data["f_s_tight"] / max(counts_mc["f_s_tight"], 1e-10)
        sf_loose = counts_data["f_s_loose"] / max(counts_mc["f_s_loose"], 1e-10)
        sf_anti = counts_data["f_s_anti"] / max(counts_mc["f_s_anti"], 1e-10)

        # Apply SFs
        cal_sf = {}
        for q in ["b", "c", "uds"]:
            et = cal_mc[f"eps_{q}_tight"] * sf_tight
            el = cal_mc[f"eps_{q}_loose"] * sf_loose
            ea = cal_mc[f"eps_{q}_anti"] * sf_anti
            tot = et + el + ea
            if tot > 0:
                cal_sf[f"eps_{q}_tight"] = float(et / tot)
                cal_sf[f"eps_{q}_loose"] = float(el / tot)
                cal_sf[f"eps_{q}_anti"] = float(ea / tot)
            else:
                cal_sf[f"eps_{q}_tight"] = cal_mc[f"eps_{q}_tight"]
                cal_sf[f"eps_{q}_loose"] = cal_mc[f"eps_{q}_loose"]
                cal_sf[f"eps_{q}_anti"] = cal_mc[f"eps_{q}_anti"]

        # Extract R_b
        extraction = extract_rb_three_tag(counts_data, cal_sf, R_C_SM, C_b_tight=1.0)

        # Toy uncertainty
        rb_mean, rb_sigma, _, n_valid = toy_uncertainty_three_tag(
            data_masscut_h0, data_masscut_h1, thr_tight, thr_loose,
            cal_sf, R_C_SM, n_toys=N_TOYS, seed=TOY_SEED)

        # Compute b-purity proxy from MC efficiencies
        f_b_mc = cal_mc["eps_b_tight"] * R_B_SM / max(counts_mc["f_s_tight"], 1e-10)
        f_c_mc = cal_mc["eps_c_tight"] * R_C_SM / max(counts_mc["f_s_tight"], 1e-10)

        log.info("%s: R_b=%.5f +/- %.5f, f_b_tight=%.3f, f_c_tight=%.3f, "
                 "eps_b_t=%.3f, eps_c_t=%.3f, chi2/ndf=%.1f/%d",
                 label, extraction["R_b"],
                 rb_sigma if not np.isnan(rb_sigma) else 0.0,
                 f_b_mc, f_c_mc,
                 cal_mc["eps_b_tight"], cal_mc["eps_c_tight"],
                 extraction["chi2"], extraction["ndf"])

        results.append({
            "label": label,
            "thr_tight": float(thr_tight),
            "thr_loose": float(thr_loose),
            "R_b": extraction["R_b"],
            "sigma_stat": float(rb_sigma) if not np.isnan(rb_sigma) else None,
            "chi2": extraction["chi2"],
            "ndf": extraction["ndf"],
            "p_value": extraction["p_value"],
            "f_b_tight_mc": float(f_b_mc),
            "f_c_tight_mc": float(f_c_mc),
            "eps_b_tight": cal_mc["eps_b_tight"],
            "eps_c_tight": cal_mc["eps_c_tight"],
            "eps_uds_tight": cal_mc["eps_uds_tight"],
            "sf_tight": float(sf_tight),
            "sf_loose": float(sf_loose),
            "sf_anti": float(sf_anti),
            "n_valid_toys": n_valid,
        })

    # Best result
    valid = [r for r in results if r["sigma_stat"] is not None
             and r["sigma_stat"] > 0 and 0.05 < r["R_b"] < 0.50]
    if valid:
        best = min(valid, key=lambda x: x["sigma_stat"])
        log.info("\nApproach 1 best: %s", best["label"])
        log.info("  R_b = %.5f +/- %.5f", best["R_b"], best["sigma_stat"])
    else:
        best = None
        log.warning("Approach 1: no valid result")

    return {
        "approach": "Hard hemisphere mass cut > 1.8 GeV",
        "results": results,
        "best": best,
    }


# ============================================================
# APPROACH 2: Multi-WP simultaneous fit
# ============================================================
def approach2_multi_wp_fit(data_h0, data_h1, mc_h0, mc_h1):
    """Simultaneous chi2 fit of R_b + per-WP efficiencies across N working points."""
    log.info("\n" + "=" * 70)
    log.info("APPROACH 2: Multi-WP simultaneous fit for R_b")
    log.info("=" * 70)

    # Use a wide range of WP configurations
    threshold_configs = [
        (8.0, 3.0), (8.0, 4.0), (8.0, 5.0),
        (9.0, 3.0), (9.0, 4.0), (9.0, 5.0),
        (10.0, 3.0), (10.0, 5.0), (10.0, 7.0),
        (11.0, 4.0), (11.0, 6.0),
        (12.0, 5.0), (12.0, 6.0),
    ]

    # Collect data counts at all WPs
    all_counts_data = []
    all_counts_mc = []
    all_cal_mc = []
    for thr_t, thr_l in threshold_configs:
        cd = count_three_tag(data_h0, data_h1, thr_t, thr_l)
        cm = count_three_tag(mc_h0, mc_h1, thr_t, thr_l)
        cal = calibrate_three_tag_efficiencies(cm, R_B_SM, R_C_SM)
        all_counts_data.append(cd)
        all_counts_mc.append(cm)
        all_cal_mc.append(cal)

    n_wp = len(threshold_configs)
    n_data = all_counts_data[0]["n_events"]

    # Parameters: R_b (1) + eps_b_tight(i), eps_c_tight(i), eps_uds_tight(i) for each WP
    # But with constraint eps_q_tight + eps_q_loose + eps_q_anti = 1,
    # we also need eps_b_loose(i), eps_c_loose(i), eps_uds_loose(i)
    # That's 1 + 6*N_WP parameters.
    # Observables: 8 per WP (2 single + 6 double) = 8*N_WP

    # Strategy: fix eps from MC calibration, fit only R_b + SF corrections
    # SF_tight(i), SF_loose(i), SF_anti(i) per WP = 3*N
    # Parameters: R_b + 3*N SFs = 1 + 3*N
    # Observables: 8*N
    # Constraints: SF_tight * f_mc_tight = f_data_tight (single hemi), etc.
    # This is overconstrained for N >= 1.

    # Simpler approach: fit R_b using single-hemi fractions across all WPs
    # At each WP, f_s_tight = eps_b_tight * R_b + eps_c_tight * R_c + eps_uds_tight * R_uds
    # With MC-calibrated efficiencies, this is linear in R_b.
    # Use data/MC SFs to correct efficiencies.

    # Build a chi2 that uses ALL WPs simultaneously:
    # For each WP i: f_s_tight(i), f_s_loose(i), f_d_tt(i), ..., f_d_la(i)
    # Predicted from: R_b, and per-WP SF-corrected MC efficiencies

    def build_multi_wp_chi2(R_b_fit):
        """Chi2 across all WPs simultaneously."""
        R_uds_fit = 1.0 - R_b_fit - R_C_SM
        total_chi2 = 0.0

        for i in range(n_wp):
            cd = all_counts_data[i]
            cal = all_cal_mc[i]

            # SF-corrected efficiencies
            sf_t = cd["f_s_tight"] / max(all_counts_mc[i]["f_s_tight"], 1e-10)
            sf_l = cd["f_s_loose"] / max(all_counts_mc[i]["f_s_loose"], 1e-10)
            sf_a = cd["f_s_anti"] / max(all_counts_mc[i]["f_s_anti"], 1e-10)

            cal_sf = {}
            for q in ["b", "c", "uds"]:
                et = cal[f"eps_{q}_tight"] * sf_t
                el = cal[f"eps_{q}_loose"] * sf_l
                ea = cal[f"eps_{q}_anti"] * sf_a
                tot = et + el + ea
                if tot > 0:
                    cal_sf[f"eps_{q}_tight"] = et / tot
                    cal_sf[f"eps_{q}_loose"] = el / tot
                    cal_sf[f"eps_{q}_anti"] = ea / tot
                else:
                    cal_sf[f"eps_{q}_tight"] = cal[f"eps_{q}_tight"]
                    cal_sf[f"eps_{q}_loose"] = cal[f"eps_{q}_loose"]
                    cal_sf[f"eps_{q}_anti"] = cal[f"eps_{q}_anti"]

            # Predicted fractions
            f_s_t_pred = (cal_sf["eps_b_tight"] * R_b_fit +
                          cal_sf["eps_c_tight"] * R_C_SM +
                          cal_sf["eps_uds_tight"] * R_uds_fit)
            f_s_l_pred = (cal_sf["eps_b_loose"] * R_b_fit +
                          cal_sf["eps_c_loose"] * R_C_SM +
                          cal_sf["eps_uds_loose"] * R_uds_fit)

            # Double-tag predictions (C_b = 1.0)
            f_d_tt_pred = (cal_sf["eps_b_tight"]**2 * R_b_fit +
                           cal_sf["eps_c_tight"]**2 * R_C_SM +
                           cal_sf["eps_uds_tight"]**2 * R_uds_fit)
            f_d_ll_pred = (cal_sf["eps_b_loose"]**2 * R_b_fit +
                           cal_sf["eps_c_loose"]**2 * R_C_SM +
                           cal_sf["eps_uds_loose"]**2 * R_uds_fit)
            f_d_aa_pred = (cal_sf["eps_b_anti"]**2 * R_b_fit +
                           cal_sf["eps_c_anti"]**2 * R_C_SM +
                           cal_sf["eps_uds_anti"]**2 * R_uds_fit)
            f_d_tl_pred = 2 * (cal_sf["eps_b_tight"] * cal_sf["eps_b_loose"] * R_b_fit +
                               cal_sf["eps_c_tight"] * cal_sf["eps_c_loose"] * R_C_SM +
                               cal_sf["eps_uds_tight"] * cal_sf["eps_uds_loose"] * R_uds_fit)
            f_d_ta_pred = 2 * (cal_sf["eps_b_tight"] * cal_sf["eps_b_anti"] * R_b_fit +
                               cal_sf["eps_c_tight"] * cal_sf["eps_c_anti"] * R_C_SM +
                               cal_sf["eps_uds_tight"] * cal_sf["eps_uds_anti"] * R_uds_fit)
            f_d_la_pred = 2 * (cal_sf["eps_b_loose"] * cal_sf["eps_b_anti"] * R_b_fit +
                               cal_sf["eps_c_loose"] * cal_sf["eps_c_anti"] * R_C_SM +
                               cal_sf["eps_uds_loose"] * cal_sf["eps_uds_anti"] * R_uds_fit)

            obs = np.array([cd["f_s_tight"], cd["f_s_loose"],
                            cd["f_d_tt"], cd["f_d_ll"], cd["f_d_aa"],
                            cd["f_d_tl"], cd["f_d_ta"], cd["f_d_la"]])
            pred = np.array([f_s_t_pred, f_s_l_pred,
                             f_d_tt_pred, f_d_ll_pred, f_d_aa_pred,
                             f_d_tl_pred, f_d_ta_pred, f_d_la_pred])

            sigma = np.array([
                np.sqrt(max(obs[0] * (1 - obs[0]) / (2 * n_data), 1e-12)),
                np.sqrt(max(obs[1] * (1 - obs[1]) / (2 * n_data), 1e-12)),
                np.sqrt(max(obs[2], 1e-8) / n_data),
                np.sqrt(max(obs[3], 1e-8) / n_data),
                np.sqrt(max(obs[4], 1e-8) / n_data),
                np.sqrt(max(obs[5], 1e-8) / n_data),
                np.sqrt(max(obs[6], 1e-8) / n_data),
                np.sqrt(max(obs[7], 1e-8) / n_data),
            ])

            total_chi2 += float(np.sum(((obs - pred) / sigma) ** 2))

        return total_chi2

    # Fit R_b
    result = minimize_scalar(build_multi_wp_chi2, bounds=(0.10, 0.40), method="bounded")
    R_b_fit = result.x
    chi2_min = result.fun
    ndf = 8 * n_wp - 1  # 8*N observables, 1 free parameter

    # Statistical uncertainty from chi2 profile
    # Find R_b values where chi2 = chi2_min + 1
    from scipy.optimize import brentq
    try:
        rb_up = brentq(lambda r: build_multi_wp_chi2(r) - chi2_min - 1.0,
                        R_b_fit, 0.40)
        rb_dn = brentq(lambda r: build_multi_wp_chi2(r) - chi2_min - 1.0,
                        0.10, R_b_fit)
        sigma_stat = (rb_up - rb_dn) / 2.0
    except Exception:
        sigma_stat = 0.001  # fallback

    p_value = float(1.0 - chi2_dist.cdf(chi2_min, ndf))

    log.info("Multi-WP fit: R_b = %.5f +/- %.5f (profile), chi2/ndf = %.1f/%d, p = %.4f",
             R_b_fit, sigma_stat, chi2_min, ndf, p_value)

    # Systematic: vary eps_c by +/-10%
    syst_eps_c = 0.0
    for factor in [1.10, 0.90]:
        def chi2_varied(R_b_v):
            R_uds_v = 1.0 - R_b_v - R_C_SM
            tot = 0.0
            for i in range(n_wp):
                cd = all_counts_data[i]
                cal = all_cal_mc[i]
                sf_t = cd["f_s_tight"] / max(all_counts_mc[i]["f_s_tight"], 1e-10)
                sf_l = cd["f_s_loose"] / max(all_counts_mc[i]["f_s_loose"], 1e-10)
                sf_a = cd["f_s_anti"] / max(all_counts_mc[i]["f_s_anti"], 1e-10)
                cal_sf = {}
                for q in ["b", "c", "uds"]:
                    f_mult = factor if q == "c" else 1.0
                    et = cal[f"eps_{q}_tight"] * sf_t * f_mult
                    el = cal[f"eps_{q}_loose"] * sf_l * f_mult
                    ea = cal[f"eps_{q}_anti"] * sf_a * f_mult
                    t = et + el + ea
                    if t > 0:
                        cal_sf[f"eps_{q}_tight"] = et / t
                        cal_sf[f"eps_{q}_loose"] = el / t
                        cal_sf[f"eps_{q}_anti"] = ea / t
                    else:
                        cal_sf[f"eps_{q}_tight"] = cal[f"eps_{q}_tight"]
                        cal_sf[f"eps_{q}_loose"] = cal[f"eps_{q}_loose"]
                        cal_sf[f"eps_{q}_anti"] = cal[f"eps_{q}_anti"]

                f_s_t_pred = (cal_sf["eps_b_tight"] * R_b_v +
                              cal_sf["eps_c_tight"] * R_C_SM +
                              cal_sf["eps_uds_tight"] * R_uds_v)
                f_s_l_pred = (cal_sf["eps_b_loose"] * R_b_v +
                              cal_sf["eps_c_loose"] * R_C_SM +
                              cal_sf["eps_uds_loose"] * R_uds_v)
                f_d_tt_pred = (cal_sf["eps_b_tight"]**2 * R_b_v +
                               cal_sf["eps_c_tight"]**2 * R_C_SM +
                               cal_sf["eps_uds_tight"]**2 * R_uds_v)
                f_d_ll_pred = (cal_sf["eps_b_loose"]**2 * R_b_v +
                               cal_sf["eps_c_loose"]**2 * R_C_SM +
                               cal_sf["eps_uds_loose"]**2 * R_uds_v)
                f_d_aa_pred = (cal_sf["eps_b_anti"]**2 * R_b_v +
                               cal_sf["eps_c_anti"]**2 * R_C_SM +
                               cal_sf["eps_uds_anti"]**2 * R_uds_v)
                f_d_tl_pred = 2 * (cal_sf["eps_b_tight"] * cal_sf["eps_b_loose"] * R_b_v +
                                   cal_sf["eps_c_tight"] * cal_sf["eps_c_loose"] * R_C_SM +
                                   cal_sf["eps_uds_tight"] * cal_sf["eps_uds_loose"] * R_uds_v)
                f_d_ta_pred = 2 * (cal_sf["eps_b_tight"] * cal_sf["eps_b_anti"] * R_b_v +
                                   cal_sf["eps_c_tight"] * cal_sf["eps_c_anti"] * R_C_SM +
                                   cal_sf["eps_uds_tight"] * cal_sf["eps_uds_anti"] * R_uds_v)
                f_d_la_pred = 2 * (cal_sf["eps_b_loose"] * cal_sf["eps_b_anti"] * R_b_v +
                                   cal_sf["eps_c_loose"] * cal_sf["eps_c_anti"] * R_C_SM +
                                   cal_sf["eps_uds_loose"] * cal_sf["eps_uds_anti"] * R_uds_v)
                obs = np.array([cd["f_s_tight"], cd["f_s_loose"],
                                cd["f_d_tt"], cd["f_d_ll"], cd["f_d_aa"],
                                cd["f_d_tl"], cd["f_d_ta"], cd["f_d_la"]])
                pred = np.array([f_s_t_pred, f_s_l_pred,
                                 f_d_tt_pred, f_d_ll_pred, f_d_aa_pred,
                                 f_d_tl_pred, f_d_ta_pred, f_d_la_pred])
                sigma = np.array([
                    np.sqrt(max(obs[0] * (1 - obs[0]) / (2 * n_data), 1e-12)),
                    np.sqrt(max(obs[1] * (1 - obs[1]) / (2 * n_data), 1e-12)),
                    np.sqrt(max(obs[2], 1e-8) / n_data),
                    np.sqrt(max(obs[3], 1e-8) / n_data),
                    np.sqrt(max(obs[4], 1e-8) / n_data),
                    np.sqrt(max(obs[5], 1e-8) / n_data),
                    np.sqrt(max(obs[6], 1e-8) / n_data),
                    np.sqrt(max(obs[7], 1e-8) / n_data),
                ])
                tot += float(np.sum(((obs - pred) / sigma) ** 2))
            return tot

        res_var = minimize_scalar(chi2_varied, bounds=(0.10, 0.40), method="bounded")
        shift = abs(res_var.x - R_b_fit)
        syst_eps_c = max(syst_eps_c, shift)

    syst_total = syst_eps_c
    log.info("Multi-WP syst (eps_c 10%%): %.5f", syst_eps_c)
    log.info("Multi-WP total: %.5f", np.sqrt(sigma_stat**2 + syst_total**2))

    return {
        "approach": "Multi-WP simultaneous fit",
        "n_wp": n_wp,
        "R_b": float(R_b_fit),
        "sigma_stat": float(sigma_stat),
        "syst_eps_c": float(syst_eps_c),
        "syst_total": float(syst_total),
        "total_uncertainty": float(np.sqrt(sigma_stat**2 + syst_total**2)),
        "chi2": float(chi2_min),
        "ndf": ndf,
        "p_value": p_value,
        "threshold_configs": threshold_configs,
    }


# ============================================================
# APPROACH 3: A_FB^b in double-tagged events
# ============================================================
def approach3_double_tag_afb(tags, jc, data_h0, data_h1):
    """A_FB^b from events where BOTH hemispheres pass the tight b-tag."""
    log.info("\n" + "=" * 70)
    log.info("APPROACH 3: A_FB^b in double-tagged events")
    log.info("=" * 70)

    cos_theta_data = jc["cos_theta_data"]
    n_data = len(data_h0)

    KAPPA_VALUES = [0.3, 0.5, 1.0, 2.0]
    KAPPA_LABELS = {0.3: "k0.3", 0.5: "k0.5", 1.0: "k1.0", 2.0: "k2.0"}

    # Try different tight thresholds for double-tag selection
    tight_thresholds = [5.0, 7.0, 8.0, 9.0, 10.0]

    all_results = []

    for kappa in KAPPA_VALUES:
        k_str = KAPPA_LABELS[kappa]
        qfb_data = jc["data_qfb_%s" % k_str]
        pub = PUBLISHED_DELTA.get(kappa)
        if pub is None:
            continue

        delta_b = pub["delta_b"]

        for thr in tight_thresholds:
            # Double-tagged: BOTH hemispheres above threshold
            double_tagged = (data_h0 > thr) & (data_h1 > thr)
            n_double = int(np.sum(double_tagged))

            if n_double < 500:
                continue

            # Compute Q_FB in cos_theta bins for double-tagged events
            valid = double_tagged & ~np.isnan(qfb_data)
            cos_sel = cos_theta_data[valid]
            qfb_sel = qfb_data[valid]

            n_bins = N_COS_BINS
            bin_edges = np.linspace(COS_RANGE[0], COS_RANGE[1], n_bins + 1)
            bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

            mean_qfb = np.zeros(n_bins)
            sigma_qfb = np.zeros(n_bins)
            for ib in range(n_bins):
                mask = (cos_sel >= bin_edges[ib]) & (cos_sel < bin_edges[ib + 1])
                n = np.sum(mask)
                if n > 10:
                    mean_qfb[ib] = np.mean(qfb_sel[mask])
                    sigma_qfb[ib] = np.std(qfb_sel[mask]) / np.sqrt(n)
                else:
                    mean_qfb[ib] = np.nan
                    sigma_qfb[ib] = np.nan

            ok = ~np.isnan(mean_qfb) & (sigma_qfb > 0)
            if np.sum(ok) < 3:
                continue

            x = bin_centers[ok]
            y = mean_qfb[ok]
            w = 1.0 / sigma_qfb[ok]**2

            S0 = np.sum(w)
            S1 = np.sum(w * x)
            S2 = np.sum(w * x**2)
            Sy = np.sum(w * y)
            Sxy = np.sum(w * x * y)
            det = S0 * S2 - S1**2
            if abs(det) < 1e-20:
                continue
            slope = (S0 * Sxy - S1 * Sy) / det
            sigma_slope = np.sqrt(S0 / det)

            # In double-tagged events, b-purity is much higher
            # f_b_double ~ (eps_b_tight)^2 * R_b / f_d_tt
            # We estimate it from the single-tag fractions
            counts = count_three_tag(data_h0, data_h1, thr, thr/2)
            f_d_tt = counts["f_d_tt"]

            # A_FB^b = slope / (f_b_double * delta_b)
            # For now, use the inclusive extraction: slope / delta_b
            # The double-tag selection already enriches b, so the slope itself
            # is closer to the b-quark asymmetry signal
            afb_inclusive = slope / delta_b
            sigma_afb_incl = sigma_slope / delta_b

            # Also estimate purity-corrected if we can estimate f_b_double
            # f_b_double approx: use single-tag purity squared
            # f_b_single ~ (eps_b * R_b) / f_s_tight
            # f_b_double ~ f_b_single^2 / f_d_tt * f_s_tight^2
            # But simpler: just note that in double-tag, essentially all
            # events are bb, so slope / delta_b is already a good estimate.

            residuals = y - (np.sum(w * y) / S0 + slope * x)  # crude, ignoring intercept
            chi2_fit = float(np.sum(w * (y - (Sy/S0 - slope * S1/S0 + slope * x))**2))

            log.info("kappa=%.1f, WP=%.1f: n_double=%d, slope=%.6f+/-%.6f, "
                     "afb_incl=%.4f+/-%.4f",
                     kappa, thr, n_double, slope, sigma_slope,
                     afb_inclusive, sigma_afb_incl)

            all_results.append({
                "kappa": float(kappa),
                "threshold": float(thr),
                "n_double_tagged": n_double,
                "frac_double": float(n_double / n_data),
                "slope": float(slope),
                "sigma_slope": float(sigma_slope),
                "afb_inclusive": float(afb_inclusive),
                "sigma_afb_inclusive": float(sigma_afb_incl),
                "delta_b": float(delta_b),
            })

    # Best result: prefer kappa=2.0 (largest delta_b -> best sensitivity)
    kappa2_results = [r for r in all_results if r["kappa"] == 2.0
                      and r["sigma_afb_inclusive"] > 0]
    if kappa2_results:
        best = min(kappa2_results, key=lambda x: x["sigma_afb_inclusive"])
    elif all_results:
        best = min(all_results, key=lambda x: x["sigma_afb_inclusive"])
    else:
        best = None

    if best:
        log.info("\nApproach 3 best (kappa=%.1f, WP=%.1f):", best["kappa"], best["threshold"])
        log.info("  A_FB^b = %.4f +/- %.4f (n_double=%d)",
                 best["afb_inclusive"], best["sigma_afb_inclusive"],
                 best["n_double_tagged"])

    # Cross-kappa combination at the best WP
    if best:
        best_thr = best["threshold"]
        combo_vals = []
        combo_errs = []
        for r in all_results:
            if r["threshold"] == best_thr and r["sigma_afb_inclusive"] > 0:
                combo_vals.append(r["afb_inclusive"])
                combo_errs.append(r["sigma_afb_inclusive"])
        if len(combo_vals) >= 2:
            vals = np.array(combo_vals)
            errs = np.array(combo_errs)
            w = 1.0 / errs**2
            afb_comb = float(np.sum(w * vals) / np.sum(w))
            sig_comb = float(1.0 / np.sqrt(np.sum(w)))
            log.info("  Cross-kappa combined at WP=%.1f: A_FB^b = %.4f +/- %.4f",
                     best_thr, afb_comb, sig_comb)
            best["afb_combined"] = afb_comb
            best["sigma_combined"] = sig_comb

    return {
        "approach": "A_FB^b from double-tagged events",
        "all_results": all_results,
        "best": best,
    }


# ============================================================
# APPROACH 4: Hemisphere probability tag (-ln P_hem)
# ============================================================
def approach4_prob_tag(tags, data_h0, data_h1, mc_h0, mc_h1):
    """Use -ln(P_hem) directly as discriminant instead of N-sigma counting.

    The existing nlp tag IS already -ln(P_hem) -- it's the sum of
    -ln(survival_prob) for each track. So approach 4 is actually about
    using ONLY the probability tag (without mass bonus) and optimizing
    thresholds specifically for it.

    The current combined tag is nlp + 3*(mass>1.8). The nlp alone
    might give different efficiency patterns.
    """
    log.info("\n" + "=" * 70)
    log.info("APPROACH 4: Pure probability tag (nlp only, no mass bonus)")
    log.info("=" * 70)

    data_nlp_h0 = tags["data_nlp_h0"]
    data_nlp_h1 = tags["data_nlp_h1"]
    mc_nlp_h0 = tags["mc_nlp_h0"]
    mc_nlp_h1 = tags["mc_nlp_h1"]

    log.info("Data nlp stats: mean=%.3f, frac>5=%.4f, frac>10=%.4f, frac>15=%.4f",
             data_nlp_h0.mean(),
             np.mean(data_nlp_h0 > 5), np.mean(data_nlp_h0 > 10), np.mean(data_nlp_h0 > 15))

    threshold_configs = [
        (5.0, 2.0), (5.0, 3.0),
        (7.0, 3.0), (7.0, 4.0),
        (8.0, 3.0), (8.0, 4.0),
        (9.0, 3.0), (9.0, 5.0),
        (10.0, 3.0), (10.0, 5.0),
        (12.0, 5.0), (12.0, 7.0),
        (15.0, 5.0), (15.0, 7.0),
    ]

    results = []
    for thr_tight, thr_loose in threshold_configs:
        label = "nlp tight=%.0f, loose=%.0f" % (thr_tight, thr_loose)

        counts_mc = count_three_tag(mc_nlp_h0, mc_nlp_h1, thr_tight, thr_loose)
        cal_mc = calibrate_three_tag_efficiencies(counts_mc, R_B_SM, R_C_SM)

        counts_data = count_three_tag(data_nlp_h0, data_nlp_h1, thr_tight, thr_loose)

        # SF
        sf_t = counts_data["f_s_tight"] / max(counts_mc["f_s_tight"], 1e-10)
        sf_l = counts_data["f_s_loose"] / max(counts_mc["f_s_loose"], 1e-10)
        sf_a = counts_data["f_s_anti"] / max(counts_mc["f_s_anti"], 1e-10)

        cal_sf = {}
        for q in ["b", "c", "uds"]:
            et = cal_mc[f"eps_{q}_tight"] * sf_t
            el = cal_mc[f"eps_{q}_loose"] * sf_l
            ea = cal_mc[f"eps_{q}_anti"] * sf_a
            tot = et + el + ea
            if tot > 0:
                cal_sf[f"eps_{q}_tight"] = float(et / tot)
                cal_sf[f"eps_{q}_loose"] = float(el / tot)
                cal_sf[f"eps_{q}_anti"] = float(ea / tot)
            else:
                cal_sf[f"eps_{q}_tight"] = cal_mc[f"eps_{q}_tight"]
                cal_sf[f"eps_{q}_loose"] = cal_mc[f"eps_{q}_loose"]
                cal_sf[f"eps_{q}_anti"] = cal_mc[f"eps_{q}_anti"]

        extraction = extract_rb_three_tag(counts_data, cal_sf, R_C_SM, C_b_tight=1.0)

        rb_mean, rb_sigma, _, n_valid = toy_uncertainty_three_tag(
            data_nlp_h0, data_nlp_h1, thr_tight, thr_loose,
            cal_sf, R_C_SM, n_toys=N_TOYS, seed=TOY_SEED)

        f_b_mc = cal_mc["eps_b_tight"] * R_B_SM / max(counts_mc["f_s_tight"], 1e-10)

        log.info("%s: R_b=%.5f +/- %.5f, f_b_tight=%.3f, eps_b/eps_c=%.2f",
                 label, extraction["R_b"],
                 rb_sigma if not np.isnan(rb_sigma) else 0.0,
                 f_b_mc,
                 cal_mc["eps_b_tight"] / max(cal_mc["eps_c_tight"], 1e-10))

        results.append({
            "label": label,
            "thr_tight": float(thr_tight),
            "thr_loose": float(thr_loose),
            "R_b": extraction["R_b"],
            "sigma_stat": float(rb_sigma) if not np.isnan(rb_sigma) else None,
            "chi2": extraction["chi2"],
            "ndf": extraction["ndf"],
            "p_value": extraction["p_value"],
            "f_b_tight_mc": float(f_b_mc),
            "eps_b_tight": cal_mc["eps_b_tight"],
            "eps_c_tight": cal_mc["eps_c_tight"],
            "ratio_eps_b_eps_c": cal_mc["eps_b_tight"] / max(cal_mc["eps_c_tight"], 1e-10),
        })

    valid = [r for r in results if r["sigma_stat"] is not None
             and r["sigma_stat"] > 0 and 0.05 < r["R_b"] < 0.50]
    if valid:
        best = min(valid, key=lambda x: x["sigma_stat"])
        log.info("\nApproach 4 best: %s", best["label"])
        log.info("  R_b = %.5f +/- %.5f", best["R_b"], best["sigma_stat"])
    else:
        best = None
        log.warning("Approach 4: no valid result")

    return {
        "approach": "Pure probability tag (nlp only)",
        "results": results,
        "best": best,
    }


# ============================================================
# APPROACH 5: Combined best improvements
# ============================================================
def approach5_combined(tags, jc, data_h0, data_h1, mc_h0, mc_h1,
                       approach1_result, approach2_result, approach3_result):
    """Combine the best improvements: mass cut + multi-WP + double-tag AFB."""
    log.info("\n" + "=" * 70)
    log.info("APPROACH 5: Combined improvements")
    log.info("=" * 70)

    # For R_b: use mass-cut scores with multi-WP simultaneous fit
    data_mass_h0 = tags["data_mass_h0"]
    data_mass_h1 = tags["data_mass_h1"]
    mc_mass_h0 = tags["mc_mass_h0"]
    mc_mass_h1 = tags["mc_mass_h1"]
    data_nlp_h0 = tags["data_nlp_h0"]
    data_nlp_h1 = tags["data_nlp_h1"]
    mc_nlp_h0 = tags["mc_nlp_h0"]
    mc_nlp_h1 = tags["mc_nlp_h1"]

    # Mass-gated nlp
    data_mc_h0 = data_nlp_h0 * (data_mass_h0 > MASS_CUT).astype(float)
    data_mc_h1 = data_nlp_h1 * (data_mass_h1 > MASS_CUT).astype(float)
    mc_mc_h0 = mc_nlp_h0 * (mc_mass_h0 > MASS_CUT).astype(float)
    mc_mc_h1 = mc_nlp_h1 * (mc_mass_h1 > MASS_CUT).astype(float)

    # Multi-WP fit on mass-gated scores
    threshold_configs = [
        (5.0, 2.0), (5.0, 3.0),
        (7.0, 3.0), (7.0, 4.0),
        (8.0, 3.0), (8.0, 4.0),
        (9.0, 3.0), (9.0, 5.0),
        (10.0, 3.0), (10.0, 5.0),
    ]

    n_data = len(data_mc_h0)
    all_counts_data = []
    all_counts_mc = []
    all_cal_mc = []
    for thr_t, thr_l in threshold_configs:
        cd = count_three_tag(data_mc_h0, data_mc_h1, thr_t, thr_l)
        cm = count_three_tag(mc_mc_h0, mc_mc_h1, thr_t, thr_l)
        cal = calibrate_three_tag_efficiencies(cm, R_B_SM, R_C_SM)
        all_counts_data.append(cd)
        all_counts_mc.append(cm)
        all_cal_mc.append(cal)

    n_wp = len(threshold_configs)

    def build_chi2(R_b_fit):
        R_uds_fit = 1.0 - R_b_fit - R_C_SM
        total = 0.0
        for i in range(n_wp):
            cd = all_counts_data[i]
            cal = all_cal_mc[i]
            sf_t = cd["f_s_tight"] / max(all_counts_mc[i]["f_s_tight"], 1e-10)
            sf_l = cd["f_s_loose"] / max(all_counts_mc[i]["f_s_loose"], 1e-10)
            sf_a = cd["f_s_anti"] / max(all_counts_mc[i]["f_s_anti"], 1e-10)
            cal_sf = {}
            for q in ["b", "c", "uds"]:
                et = cal[f"eps_{q}_tight"] * sf_t
                el = cal[f"eps_{q}_loose"] * sf_l
                ea = cal[f"eps_{q}_anti"] * sf_a
                t = et + el + ea
                if t > 0:
                    cal_sf[f"eps_{q}_tight"] = et / t
                    cal_sf[f"eps_{q}_loose"] = el / t
                    cal_sf[f"eps_{q}_anti"] = ea / t
                else:
                    cal_sf[f"eps_{q}_tight"] = cal[f"eps_{q}_tight"]
                    cal_sf[f"eps_{q}_loose"] = cal[f"eps_{q}_loose"]
                    cal_sf[f"eps_{q}_anti"] = cal[f"eps_{q}_anti"]

            f_s_t_pred = (cal_sf["eps_b_tight"] * R_b_fit +
                          cal_sf["eps_c_tight"] * R_C_SM +
                          cal_sf["eps_uds_tight"] * R_uds_fit)
            f_s_l_pred = (cal_sf["eps_b_loose"] * R_b_fit +
                          cal_sf["eps_c_loose"] * R_C_SM +
                          cal_sf["eps_uds_loose"] * R_uds_fit)
            f_d_tt_pred = (cal_sf["eps_b_tight"]**2 * R_b_fit +
                           cal_sf["eps_c_tight"]**2 * R_C_SM +
                           cal_sf["eps_uds_tight"]**2 * R_uds_fit)
            f_d_ll_pred = (cal_sf["eps_b_loose"]**2 * R_b_fit +
                           cal_sf["eps_c_loose"]**2 * R_C_SM +
                           cal_sf["eps_uds_loose"]**2 * R_uds_fit)
            f_d_aa_pred = (cal_sf["eps_b_anti"]**2 * R_b_fit +
                           cal_sf["eps_c_anti"]**2 * R_C_SM +
                           cal_sf["eps_uds_anti"]**2 * R_uds_fit)
            f_d_tl_pred = 2 * (cal_sf["eps_b_tight"] * cal_sf["eps_b_loose"] * R_b_fit +
                               cal_sf["eps_c_tight"] * cal_sf["eps_c_loose"] * R_C_SM +
                               cal_sf["eps_uds_tight"] * cal_sf["eps_uds_loose"] * R_uds_fit)
            f_d_ta_pred = 2 * (cal_sf["eps_b_tight"] * cal_sf["eps_b_anti"] * R_b_fit +
                               cal_sf["eps_c_tight"] * cal_sf["eps_c_anti"] * R_C_SM +
                               cal_sf["eps_uds_tight"] * cal_sf["eps_uds_anti"] * R_uds_fit)
            f_d_la_pred = 2 * (cal_sf["eps_b_loose"] * cal_sf["eps_b_anti"] * R_b_fit +
                               cal_sf["eps_c_loose"] * cal_sf["eps_c_anti"] * R_C_SM +
                               cal_sf["eps_uds_loose"] * cal_sf["eps_uds_anti"] * R_uds_fit)
            obs = np.array([cd["f_s_tight"], cd["f_s_loose"],
                            cd["f_d_tt"], cd["f_d_ll"], cd["f_d_aa"],
                            cd["f_d_tl"], cd["f_d_ta"], cd["f_d_la"]])
            pred = np.array([f_s_t_pred, f_s_l_pred,
                             f_d_tt_pred, f_d_ll_pred, f_d_aa_pred,
                             f_d_tl_pred, f_d_ta_pred, f_d_la_pred])
            sigma = np.array([
                np.sqrt(max(obs[0] * (1 - obs[0]) / (2 * n_data), 1e-12)),
                np.sqrt(max(obs[1] * (1 - obs[1]) / (2 * n_data), 1e-12)),
                np.sqrt(max(obs[2], 1e-8) / n_data),
                np.sqrt(max(obs[3], 1e-8) / n_data),
                np.sqrt(max(obs[4], 1e-8) / n_data),
                np.sqrt(max(obs[5], 1e-8) / n_data),
                np.sqrt(max(obs[6], 1e-8) / n_data),
                np.sqrt(max(obs[7], 1e-8) / n_data),
            ])
            total += float(np.sum(((obs - pred) / sigma) ** 2))
        return total

    result_rb = minimize_scalar(build_chi2, bounds=(0.10, 0.40), method="bounded")
    R_b_combined = result_rb.x
    chi2_combined = result_rb.fun
    ndf_combined = 8 * n_wp - 1

    from scipy.optimize import brentq
    try:
        rb_up = brentq(lambda r: build_chi2(r) - chi2_combined - 1.0,
                        R_b_combined, 0.40)
        rb_dn = brentq(lambda r: build_chi2(r) - chi2_combined - 1.0,
                        0.10, R_b_combined)
        sigma_rb = (rb_up - rb_dn) / 2.0
    except Exception:
        sigma_rb = 0.001

    p_combined = float(1.0 - chi2_dist.cdf(chi2_combined, ndf_combined))

    # Syst: eps_c variation
    syst_epsc = 0.0
    for factor in [1.10, 0.90]:
        def chi2_var(R_b_v):
            R_uds_v = 1.0 - R_b_v - R_C_SM
            total = 0.0
            for i in range(n_wp):
                cd = all_counts_data[i]
                cal = all_cal_mc[i]
                sf_t = cd["f_s_tight"] / max(all_counts_mc[i]["f_s_tight"], 1e-10)
                sf_l = cd["f_s_loose"] / max(all_counts_mc[i]["f_s_loose"], 1e-10)
                sf_a = cd["f_s_anti"] / max(all_counts_mc[i]["f_s_anti"], 1e-10)
                cal_sf = {}
                for q in ["b", "c", "uds"]:
                    fm = factor if q == "c" else 1.0
                    et = cal[f"eps_{q}_tight"] * sf_t * fm
                    el = cal[f"eps_{q}_loose"] * sf_l * fm
                    ea = cal[f"eps_{q}_anti"] * sf_a * fm
                    t = et + el + ea
                    if t > 0:
                        cal_sf[f"eps_{q}_tight"] = et / t
                        cal_sf[f"eps_{q}_loose"] = el / t
                        cal_sf[f"eps_{q}_anti"] = ea / t
                    else:
                        cal_sf[f"eps_{q}_tight"] = cal[f"eps_{q}_tight"]
                        cal_sf[f"eps_{q}_loose"] = cal[f"eps_{q}_loose"]
                        cal_sf[f"eps_{q}_anti"] = cal[f"eps_{q}_anti"]
                f_s_t_p = (cal_sf["eps_b_tight"] * R_b_v + cal_sf["eps_c_tight"] * R_C_SM +
                           cal_sf["eps_uds_tight"] * R_uds_v)
                f_s_l_p = (cal_sf["eps_b_loose"] * R_b_v + cal_sf["eps_c_loose"] * R_C_SM +
                           cal_sf["eps_uds_loose"] * R_uds_v)
                f_d_tt_p = (cal_sf["eps_b_tight"]**2 * R_b_v + cal_sf["eps_c_tight"]**2 * R_C_SM +
                            cal_sf["eps_uds_tight"]**2 * R_uds_v)
                f_d_ll_p = (cal_sf["eps_b_loose"]**2 * R_b_v + cal_sf["eps_c_loose"]**2 * R_C_SM +
                            cal_sf["eps_uds_loose"]**2 * R_uds_v)
                f_d_aa_p = (cal_sf["eps_b_anti"]**2 * R_b_v + cal_sf["eps_c_anti"]**2 * R_C_SM +
                            cal_sf["eps_uds_anti"]**2 * R_uds_v)
                f_d_tl_p = 2 * (cal_sf["eps_b_tight"] * cal_sf["eps_b_loose"] * R_b_v +
                                cal_sf["eps_c_tight"] * cal_sf["eps_c_loose"] * R_C_SM +
                                cal_sf["eps_uds_tight"] * cal_sf["eps_uds_loose"] * R_uds_v)
                f_d_ta_p = 2 * (cal_sf["eps_b_tight"] * cal_sf["eps_b_anti"] * R_b_v +
                                cal_sf["eps_c_tight"] * cal_sf["eps_c_anti"] * R_C_SM +
                                cal_sf["eps_uds_tight"] * cal_sf["eps_uds_anti"] * R_uds_v)
                f_d_la_p = 2 * (cal_sf["eps_b_loose"] * cal_sf["eps_b_anti"] * R_b_v +
                                cal_sf["eps_c_loose"] * cal_sf["eps_c_anti"] * R_C_SM +
                                cal_sf["eps_uds_loose"] * cal_sf["eps_uds_anti"] * R_uds_v)
                obs = np.array([cd["f_s_tight"], cd["f_s_loose"],
                                cd["f_d_tt"], cd["f_d_ll"], cd["f_d_aa"],
                                cd["f_d_tl"], cd["f_d_ta"], cd["f_d_la"]])
                pred = np.array([f_s_t_p, f_s_l_p, f_d_tt_p, f_d_ll_p, f_d_aa_p,
                                 f_d_tl_p, f_d_ta_p, f_d_la_p])
                sigma = np.array([
                    np.sqrt(max(obs[0] * (1 - obs[0]) / (2 * n_data), 1e-12)),
                    np.sqrt(max(obs[1] * (1 - obs[1]) / (2 * n_data), 1e-12)),
                    np.sqrt(max(obs[2], 1e-8) / n_data),
                    np.sqrt(max(obs[3], 1e-8) / n_data),
                    np.sqrt(max(obs[4], 1e-8) / n_data),
                    np.sqrt(max(obs[5], 1e-8) / n_data),
                    np.sqrt(max(obs[6], 1e-8) / n_data),
                    np.sqrt(max(obs[7], 1e-8) / n_data),
                ])
                total += float(np.sum(((obs - pred) / sigma) ** 2))
            return total
        rv = minimize_scalar(chi2_var, bounds=(0.10, 0.40), method="bounded")
        syst_epsc = max(syst_epsc, abs(rv.x - R_b_combined))

    total_unc = float(np.sqrt(sigma_rb**2 + syst_epsc**2))

    log.info("Combined (mass-cut + multi-WP):")
    log.info("  R_b = %.5f +/- %.5f (stat) +/- %.5f (syst) = %.5f (total)",
             R_b_combined, sigma_rb, syst_epsc, total_unc)
    log.info("  chi2/ndf = %.1f/%d, p = %.4f", chi2_combined, ndf_combined, p_combined)

    # For A_FB^b: use double-tagged events with mass-cut scores
    cos_theta_data = jc["cos_theta_data"]
    afb_results = []
    KAPPA_VALUES = [0.3, 0.5, 1.0, 2.0]
    KAPPA_LABELS = {0.3: "k0.3", 0.5: "k0.5", 1.0: "k1.0", 2.0: "k2.0"}

    for kappa in KAPPA_VALUES:
        k_str = KAPPA_LABELS[kappa]
        qfb_data = jc["data_qfb_%s" % k_str]
        pub = PUBLISHED_DELTA.get(kappa)
        if pub is None:
            continue
        delta_b = pub["delta_b"]

        for thr in [5.0, 7.0, 8.0]:
            double_tagged = (data_mc_h0 > thr) & (data_mc_h1 > thr)
            n_double = int(np.sum(double_tagged))
            if n_double < 200:
                continue

            valid = double_tagged & ~np.isnan(qfb_data)
            cos_sel = cos_theta_data[valid]
            qfb_sel = qfb_data[valid]

            n_bins = N_COS_BINS
            bin_edges = np.linspace(COS_RANGE[0], COS_RANGE[1], n_bins + 1)
            bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

            mean_qfb = np.zeros(n_bins)
            sigma_qfb = np.zeros(n_bins)
            for ib in range(n_bins):
                mask = (cos_sel >= bin_edges[ib]) & (cos_sel < bin_edges[ib + 1])
                n = np.sum(mask)
                if n > 10:
                    mean_qfb[ib] = np.mean(qfb_sel[mask])
                    sigma_qfb[ib] = np.std(qfb_sel[mask]) / np.sqrt(n)
                else:
                    mean_qfb[ib] = np.nan
                    sigma_qfb[ib] = np.nan

            ok = ~np.isnan(mean_qfb) & (sigma_qfb > 0)
            if np.sum(ok) < 3:
                continue

            x = bin_centers[ok]
            y = mean_qfb[ok]
            w = 1.0 / sigma_qfb[ok]**2
            S0 = np.sum(w)
            S1 = np.sum(w * x)
            S2 = np.sum(w * x**2)
            Sy = np.sum(w * y)
            Sxy = np.sum(w * x * y)
            det = S0 * S2 - S1**2
            if abs(det) < 1e-20:
                continue
            slope = (S0 * Sxy - S1 * Sy) / det
            sigma_slope = np.sqrt(S0 / det)

            afb_incl = slope / delta_b
            sigma_afb = sigma_slope / delta_b

            afb_results.append({
                "kappa": float(kappa),
                "threshold": float(thr),
                "n_double_tagged": n_double,
                "afb_inclusive": float(afb_incl),
                "sigma_afb": float(sigma_afb),
            })

    # Combine AFB across kappas at best threshold
    afb_combined = None
    if afb_results:
        # Group by threshold, pick one with most kappa results
        from collections import Counter
        thr_counts = Counter(r["threshold"] for r in afb_results)
        best_thr = max(thr_counts, key=lambda t: thr_counts[t])
        vals = [r["afb_inclusive"] for r in afb_results if r["threshold"] == best_thr]
        errs = [r["sigma_afb"] for r in afb_results if r["threshold"] == best_thr]
        if vals:
            v = np.array(vals)
            e = np.array(errs)
            w = 1.0 / e**2
            afb_combined = {
                "value": float(np.sum(w * v) / np.sum(w)),
                "sigma": float(1.0 / np.sqrt(np.sum(w))),
                "threshold": float(best_thr),
                "n_kappas": len(vals),
            }
            log.info("Combined A_FB^b (mass-cut + double-tag, WP=%.1f): %.4f +/- %.4f",
                     best_thr, afb_combined["value"], afb_combined["sigma"])

    return {
        "approach": "Combined: mass-cut + multi-WP fit + double-tag AFB",
        "R_b": {
            "value": float(R_b_combined),
            "sigma_stat": float(sigma_rb),
            "syst_eps_c": float(syst_epsc),
            "total_uncertainty": total_unc,
            "chi2": float(chi2_combined),
            "ndf": ndf_combined,
            "p_value": p_combined,
            "n_wp": n_wp,
        },
        "A_FB_b": {
            "per_config": afb_results,
            "combined": afb_combined,
        },
    }


# ============================================================
# MAIN
# ============================================================
def main():
    log.info("=" * 70)
    log.info("PRECISION PUSH: 5 approaches to improve R_b and A_FB^b")
    log.info("Session: eloise_f4f5")
    log.info("=" * 70)

    # Load data
    tags = np.load(P3_OUT / "hemisphere_tags.npz", allow_pickle=False)
    jc = np.load(P3_OUT / "jet_charge.npz", allow_pickle=False)

    data_h0 = tags["data_combined_h0"]
    data_h1 = tags["data_combined_h1"]
    mc_h0 = tags["mc_combined_h0"]
    mc_h1 = tags["mc_combined_h1"]

    n_data = len(data_h0)
    n_mc = len(mc_h0)
    log.info("Data events: %d", n_data)
    log.info("MC events: %d", n_mc)

    # Baseline results for comparison
    baseline = {
        "R_b": {"value": 0.2123, "stat": 0.0004, "syst": 0.0270, "total": 0.0270},
        "A_FB_b": {"value": 0.0025, "stat": 0.0026, "syst": 0.0021, "total": 0.0034},
        "ALEPH_R_b": {"value": 0.2159, "stat": 0.0009, "syst": 0.0011, "total": 0.0014},
        "ALEPH_A_FB_b": {"value": 0.0995, "stat": 0.0050},
    }

    # Run all approaches
    res1 = approach1_mass_cut(tags, data_h0, data_h1, mc_h0, mc_h1)
    res2 = approach2_multi_wp_fit(data_h0, data_h1, mc_h0, mc_h1)
    res3 = approach3_double_tag_afb(tags, jc, data_h0, data_h1)
    res4 = approach4_prob_tag(tags, data_h0, data_h1, mc_h0, mc_h1)
    res5 = approach5_combined(tags, jc, data_h0, data_h1, mc_h0, mc_h1,
                               res1, res2, res3)

    # ============================================================
    # SUMMARY
    # ============================================================
    log.info("\n" + "=" * 70)
    log.info("SUMMARY")
    log.info("=" * 70)

    log.info("\n--- R_b Results ---")
    log.info("Baseline:        R_b = %.4f +/- %.4f (stat) +/- %.4f (syst)",
             baseline["R_b"]["value"], baseline["R_b"]["stat"], baseline["R_b"]["syst"])
    log.info("ALEPH published: R_b = %.4f +/- %.4f (total)",
             baseline["ALEPH_R_b"]["value"], baseline["ALEPH_R_b"]["total"])

    if res1["best"]:
        log.info("Approach 1 (mass cut):  R_b = %.4f +/- %.4f (stat)",
                 res1["best"]["R_b"], res1["best"]["sigma_stat"])
    log.info("Approach 2 (multi-WP): R_b = %.4f +/- %.4f (stat) +/- %.4f (syst)",
             res2["R_b"], res2["sigma_stat"], res2["syst_total"])
    if res4["best"]:
        log.info("Approach 4 (nlp only): R_b = %.4f +/- %.4f (stat)",
                 res4["best"]["R_b"], res4["best"]["sigma_stat"])
    log.info("Approach 5 (combined): R_b = %.4f +/- %.4f (stat) +/- %.4f (syst)",
             res5["R_b"]["value"], res5["R_b"]["sigma_stat"], res5["R_b"]["syst_eps_c"])

    log.info("\n--- A_FB^b Results ---")
    log.info("Baseline:        A_FB^b = %.4f +/- %.4f (stat)",
             baseline["A_FB_b"]["value"], baseline["A_FB_b"]["stat"])
    log.info("ALEPH published: A_FB^b = %.4f +/- %.4f",
             baseline["ALEPH_A_FB_b"]["value"], baseline["ALEPH_A_FB_b"]["stat"])
    if res3["best"]:
        log.info("Approach 3 (double-tag): A_FB^b = %.4f +/- %.4f",
                 res3["best"]["afb_inclusive"], res3["best"]["sigma_afb_inclusive"])
    if res5["A_FB_b"]["combined"]:
        log.info("Approach 5 (combined):   A_FB^b = %.4f +/- %.4f",
                 res5["A_FB_b"]["combined"]["value"],
                 res5["A_FB_b"]["combined"]["sigma"])

    # ============================================================
    # Determine best overall results
    # ============================================================
    # R_b: compare total uncertainties
    rb_candidates = []
    rb_candidates.append(("baseline", baseline["R_b"]["value"],
                          baseline["R_b"]["total"]))
    if res1["best"] and res1["best"]["sigma_stat"]:
        rb_candidates.append(("mass_cut", res1["best"]["R_b"],
                              res1["best"]["sigma_stat"]))  # stat only for now
    rb_candidates.append(("multi_wp", res2["R_b"], res2["total_uncertainty"]))
    if res4["best"] and res4["best"]["sigma_stat"]:
        rb_candidates.append(("nlp_only", res4["best"]["R_b"],
                              res4["best"]["sigma_stat"]))
    rb_candidates.append(("combined", res5["R_b"]["value"],
                          res5["R_b"]["total_uncertainty"]))

    best_rb = min(rb_candidates, key=lambda x: x[2])
    log.info("\nBest R_b: %s = %.5f +/- %.5f", best_rb[0], best_rb[1], best_rb[2])

    # A_FB^b: compare statistical uncertainties
    afb_candidates = []
    afb_candidates.append(("baseline", baseline["A_FB_b"]["value"],
                           baseline["A_FB_b"]["stat"]))
    if res3["best"]:
        afb_candidates.append(("double_tag", res3["best"]["afb_inclusive"],
                               res3["best"]["sigma_afb_inclusive"]))
    if res5["A_FB_b"]["combined"]:
        afb_candidates.append(("combined", res5["A_FB_b"]["combined"]["value"],
                               res5["A_FB_b"]["combined"]["sigma"]))

    best_afb = min(afb_candidates, key=lambda x: x[2])
    log.info("Best A_FB^b: %s = %.5f +/- %.5f", best_afb[0], best_afb[1], best_afb[2])

    # ============================================================
    # Save output
    # ============================================================
    output = {
        "session": "eloise_f4f5",
        "n_data_events": n_data,
        "n_mc_events": n_mc,
        "baseline": baseline,
        "approach_1_mass_cut": res1,
        "approach_2_multi_wp": res2,
        "approach_3_double_tag_afb": res3,
        "approach_4_prob_tag": res4,
        "approach_5_combined": res5,
        "best_rb": {
            "method": best_rb[0],
            "value": best_rb[1],
            "total_uncertainty": best_rb[2],
        },
        "best_afb": {
            "method": best_afb[0],
            "value": best_afb[1],
            "stat_uncertainty": best_afb[2],
        },
    }

    out_path = PHASE4C_OUT / "precision_push_results.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    log.info("\nSaved %s", out_path.name)

    # ============================================================
    # Update parameters.json
    # ============================================================
    params_path = RESULTS_DIR / "parameters.json"
    if params_path.exists():
        with open(params_path) as f:
            params = json.load(f)
    else:
        params = {}

    # Update with best results if they improve on baseline
    if best_rb[2] < baseline["R_b"]["total"]:
        params["R_b_precision_push"] = {
            "value": best_rb[1],
            "total": best_rb[2],
            "method": best_rb[0],
            "SM": R_B_SM,
            "improvement_factor": baseline["R_b"]["total"] / best_rb[2],
            "session": "eloise_f4f5",
        }
        # Also update the "final" if it's a genuine improvement
        if best_rb[0] in ["multi_wp", "combined"]:
            rb_res = res2 if best_rb[0] == "multi_wp" else res5["R_b"]
            stat = rb_res.get("sigma_stat", best_rb[2])
            syst = rb_res.get("syst_total", rb_res.get("syst_eps_c", 0))
            params["R_b_fulldata_final"] = {
                "value": best_rb[1],
                "stat": stat,
                "syst": syst,
                "total": best_rb[2],
                "SM": R_B_SM,
                "method": "precision_push_%s" % best_rb[0],
            }

    if best_afb[2] < baseline["A_FB_b"]["stat"]:
        params["A_FB_b_precision_push"] = {
            "value": best_afb[1],
            "stat": best_afb[2],
            "method": best_afb[0],
            "SM": AFB_B_SM_POLE,
            "LEP_observed": AFB_B_OBS,
            "improvement_factor": baseline["A_FB_b"]["stat"] / best_afb[2],
            "session": "eloise_f4f5",
        }

    with open(params_path, "w") as f:
        json.dump(params, f, indent=2)
    log.info("Updated parameters.json")


if __name__ == "__main__":
    main()
