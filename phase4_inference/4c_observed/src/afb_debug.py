"""AFB debug: systematic investigation of suppressed A_FB^b.

Session: yuki_d474

We measure A_FB^b ~ 0.003, ALEPH measured 0.093. This script investigates:
  Task 1: Beam direction / thrust axis sign convention
  Task 2: Sign convention in Q_FB -> A_FB formula
  Task 5: Q_FB computation verification
  Task 6: Simple counting method (sign-independent)
  CRITICAL TEST: A_FB separately for cos>0 and cos<0

Physics recap:
  - At ALEPH, +z = electron beam direction
  - A_FB^b > 0 means more b quarks go forward (toward e-)
  - b quark has charge -1/3
  - When b goes forward: forward hemisphere has b -> Q_F more negative
  - <Q_FB> = <Q_F - Q_B> should be negative when A_FB > 0
  - slope d<Q_FB>/d(cos theta) = sum_q R_q * delta_q * A_FB^q
  - For b: delta_b > 0 (published), A_FB^b > 0 -> slope contribution positive

Reads: phase3_selection/outputs/hemisphere_tags.npz
       phase3_selection/outputs/jet_charge.npz
       phase4_inference/4a_expected/outputs/mc_calibration.json
Writes: phase4_inference/4c_observed/outputs/afb_debug_results.json
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
PHASE4C_OUT = HERE.parent / "outputs"
P4A_OUT = HERE.parents[1] / "4a_expected" / "outputs"
P3_OUT = HERE.parents[2] / "phase3_selection" / "outputs"

sys.path.insert(0, str(HERE.parents[1] / "4a_expected" / "src"))
from purity_corrected_afb import (
    measure_qfb_slope, PUBLISHED_DELTA, N_COS_BINS, COS_RANGE,
)

# Reference values
AFB_B_ALEPH = 0.0927  # ALEPH result (inspire_433746)
AFB_B_LEP = 0.0995    # LEP combination


def main():
    results = {}

    log.info("=" * 70)
    log.info("AFB DEBUG: Investigating suppressed A_FB^b (yuki_d474)")
    log.info("=" * 70)

    # ================================================================
    # Load data
    # ================================================================
    jc = np.load(P3_OUT / "jet_charge.npz", allow_pickle=False)
    tags = np.load(P3_OUT / "hemisphere_tags.npz", allow_pickle=False)

    cos_data = jc["cos_theta_data"]
    data_h0 = tags["data_combined_h0"]
    data_h1 = tags["data_combined_h1"]
    n_events = len(cos_data)
    log.info("Data events: %d", n_events)

    # Also load preselected data for raw TTheta
    pre_data = np.load(P3_OUT / "preselected_data.npz", allow_pickle=False)
    ttheta = pre_data["ttheta"]

    # ================================================================
    # TASK 1: Beam direction / thrust axis convention
    # ================================================================
    log.info("\n" + "=" * 70)
    log.info("TASK 1: BEAM DIRECTION & THRUST AXIS CONVENTION")
    log.info("=" * 70)

    # Check TTheta distribution
    log.info("\n--- TTheta (raw polar angle of thrust axis) ---")
    log.info("min=%.4f, max=%.4f, mean=%.4f", ttheta.min(), ttheta.max(), ttheta.mean())
    log.info("TTheta range should be [0, pi]")

    cos_tt = np.cos(ttheta)
    log.info("\ncos(TTheta): min=%.4f, max=%.4f, mean=%.6f",
             cos_tt.min(), cos_tt.max(), cos_tt.mean())
    n_pos = np.sum(cos_tt > 0)
    n_neg = np.sum(cos_tt < 0)
    log.info("N(cos>0) = %d (%.2f%%)", n_pos, 100*n_pos/len(cos_tt))
    log.info("N(cos<0) = %d (%.2f%%)", n_neg, 100*n_neg/len(cos_tt))
    log.info("Ratio pos/neg = %.4f", n_pos / max(n_neg, 1))

    results["ttheta_stats"] = {
        "min": float(ttheta.min()),
        "max": float(ttheta.max()),
        "mean": float(ttheta.mean()),
        "cos_mean": float(cos_tt.mean()),
        "n_cos_pos": int(n_pos),
        "n_cos_neg": int(n_neg),
        "ratio_pos_neg": float(n_pos / max(n_neg, 1)),
    }

    # Key insight: if TTheta is symmetric around pi/2, then the thrust
    # axis sign is physical (not just always pointing to one hemisphere).
    # If N(cos>0) ~ N(cos<0), the axis is randomly oriented.
    # If heavily asymmetric, the axis always points one way.

    log.info("\nINTERPRETATION:")
    if abs(n_pos - n_neg) / (n_pos + n_neg) < 0.01:
        log.info("cos(TTheta) is nearly symmetric -> thrust axis has physical sign")
        log.info("(Likely: TTheta encodes the polar angle of a SIGNED thrust axis)")
    else:
        log.info("cos(TTheta) is ASYMMETRIC -> thrust axis may always point one way")
        log.info("This could cause AFB cancellation!")

    # ================================================================
    # CRITICAL TEST: A_FB in forward vs backward halves
    # ================================================================
    log.info("\n" + "=" * 70)
    log.info("CRITICAL TEST: A_FB separately for cos>0 vs cos<0")
    log.info("=" * 70)
    log.info("If beam direction is correct:")
    log.info("  Both halves should give same-sign A_FB")
    log.info("If beam direction is wrong:")
    log.info("  Opposite-sign A_FB in each half -> cancellation")

    kappa = 1.0
    k_str = "k1.0"
    qfb_data = jc["data_qfb_" + k_str]
    thr = 3.0  # moderate b-tag
    tagged = (data_h0 > thr) | (data_h1 > thr)
    valid = ~np.isnan(qfb_data) & tagged

    cos_sel = cos_data[valid]
    qfb_sel = qfb_data[valid]

    # Full range
    mean_qfb_all = np.mean(qfb_sel)
    log.info("\nFull sample (kappa=1.0, WP>3.0):")
    log.info("  <Q_FB> = %.6f (N=%d)", mean_qfb_all, len(qfb_sel))

    # Forward half only (cos > 0)
    fwd_mask = cos_sel > 0
    mean_qfb_fwd = np.mean(qfb_sel[fwd_mask])
    log.info("  <Q_FB>(cos>0) = %.6f (N=%d)", mean_qfb_fwd, np.sum(fwd_mask))

    # Backward half only (cos < 0)
    bwd_mask = cos_sel < 0
    mean_qfb_bwd = np.mean(qfb_sel[bwd_mask])
    log.info("  <Q_FB>(cos<0) = %.6f (N=%d)", mean_qfb_bwd, np.sum(bwd_mask))

    log.info("\n  Difference: <Q_FB>(cos>0) - <Q_FB>(cos<0) = %.6f",
             mean_qfb_fwd - mean_qfb_bwd)
    log.info("  This should be nonzero and its sign tells us about AFB")

    results["critical_test_qfb_halves"] = {
        "mean_qfb_all": float(mean_qfb_all),
        "mean_qfb_fwd": float(mean_qfb_fwd),
        "mean_qfb_bwd": float(mean_qfb_bwd),
        "diff_fwd_minus_bwd": float(mean_qfb_fwd - mean_qfb_bwd),
    }

    # ================================================================
    # TASK 5: Verify Q_FB computation
    # ================================================================
    log.info("\n" + "=" * 70)
    log.info("TASK 5: Q_FB COMPUTATION VERIFICATION")
    log.info("=" * 70)

    # Check hemisphere charges
    qh0_data = jc["data_qh_h0_k1.0"]
    qh1_data = jc["data_qh_h1_k1.0"]

    valid_h = ~np.isnan(qh0_data) & ~np.isnan(qh1_data)
    log.info("\nHemisphere charges (kappa=1.0):")
    log.info("  <Q_h0> = %.6f", np.mean(qh0_data[valid_h]))
    log.info("  <Q_h1> = %.6f", np.mean(qh1_data[valid_h]))
    log.info("  (h0 and h1 are arbitrary -> should be ~equal)")

    # For b-tagged events, check which hemisphere is more negative
    btag_h0 = data_h0 > 5.0
    btag_h1 = data_h1 > 5.0
    btag_any = btag_h0 | btag_h1
    valid_btag = valid_h & btag_any

    log.info("\nFor b-tagged events (any hem > 5.0):")
    log.info("  <Q_h0> = %.6f (N=%d)", np.mean(qh0_data[valid_btag]), np.sum(valid_btag))
    log.info("  <Q_h1> = %.6f", np.mean(qh1_data[valid_btag]))

    # Check Q_FB = Q_F - Q_B construction
    # In jet_charge.py: forward_is_h1 = cos_theta > 0
    # q_f = h1 if cos>0 else h0
    # q_b = h0 if cos>0 else h1
    # qfb = q_f - q_b
    forward_is_h1 = cos_data > 0
    q_f_manual = np.where(forward_is_h1, qh1_data, qh0_data)
    q_b_manual = np.where(forward_is_h1, qh0_data, qh1_data)
    qfb_manual = q_f_manual - q_b_manual

    # Compare to stored Q_FB
    diff = qfb_data - qfb_manual
    valid_diff = ~np.isnan(diff)
    log.info("\nQ_FB verification (stored vs manual):")
    log.info("  max|diff| = %.10f", np.max(np.abs(diff[valid_diff])))
    log.info("  Q_FB computation is %s",
             "CORRECT" if np.max(np.abs(diff[valid_diff])) < 1e-10 else "WRONG!")

    results["qfb_verification"] = {
        "max_abs_diff": float(np.max(np.abs(diff[valid_diff]))),
        "correct": bool(np.max(np.abs(diff[valid_diff])) < 1e-10),
    }

    # ================================================================
    # TASK 5b: Slope sign analysis
    # ================================================================
    log.info("\n" + "=" * 70)
    log.info("TASK 5b: SLOPE SIGN ANALYSIS")
    log.info("=" * 70)

    log.info("\nPhysics expectation:")
    log.info("  <Q_FB>(cos theta) = sum_q R_q * delta_q * A_FB^q * cos(theta)")
    log.info("  For b quarks: delta_b ~ +0.37 (kappa=1.0), A_FB^b ~ +0.10")
    log.info("  Expected slope ~ R_b * delta_b * A_FB^b ~ 0.216 * 0.374 * 0.10 ~ +0.008")
    log.info("  (Plus contributions from c and uds)")

    for kappa in [0.3, 0.5, 1.0, 2.0]:
        k_str = "k%.1f" % kappa
        qfb_k = jc["data_qfb_" + k_str]
        delta_b = PUBLISHED_DELTA[kappa]["delta_b"]

        for thr in [2.0, 5.0, 9.0]:
            result = measure_qfb_slope(qfb_k, cos_data, data_h0, data_h1, thr)
            if result is None:
                continue
            slope = result["slope"]
            sigma = result["sigma_slope"]
            afb_naive = slope / delta_b

            log.info("kappa=%.1f, WP=%.1f: slope=%.6f +/- %.6f, "
                     "A_FB(naive)=%.4f +/- %.4f, N_tagged=%d",
                     kappa, thr, slope, sigma, afb_naive, sigma/delta_b,
                     result["n_tagged"])

    # ================================================================
    # TASK 6: COUNTING METHOD (sign-unambiguous)
    # ================================================================
    log.info("\n" + "=" * 70)
    log.info("TASK 6: COUNTING METHOD A_FB")
    log.info("=" * 70)
    log.info("Using b-tag to identify b hemispheres.")
    log.info("Forward = cos(theta_thrust) > 0 = electron direction (+z at ALEPH)")
    log.info("N_F = b-tagged forward, N_B = b-tagged backward")
    log.info("A_FB_raw = (N_F - N_B) / (N_F + N_B)")

    for thr in [2.0, 3.0, 5.0, 7.0, 9.0]:
        # Count events where the b-tagged hemisphere is forward vs backward
        # An event contributes to N_F if the tagged hemisphere is in cos>0
        # and to N_B if it's in cos<0

        # Method A: use the higher-score hemisphere as the b hemisphere
        h0_is_b = data_h0 > data_h1
        tagged_mask = (np.maximum(data_h0, data_h1) > thr)

        # b hemisphere is h0 or h1?
        # If h0 is b: the b is in the h0 direction
        # h0 = hemisphere with dot(p, thrust) < 0 (see preselection.py line 149)
        # Actually, hem_assign = (dot > 0), so hem=1 means positive dot with thrust
        # h0 tracks have dot < 0 -> h0 is opposite to thrust direction
        # h1 tracks have dot > 0 -> h1 is along thrust direction

        # If cos(TTheta) > 0: thrust points forward (+z)
        #   h1 = forward, h0 = backward
        # If cos(TTheta) < 0: thrust points backward (-z)
        #   h1 = backward, h0 = forward

        # So: b hemisphere direction in terms of cos_theta:
        # If h0_is_b and cos>0: b is backward (h0 is backward when thrust is forward)
        # If h0_is_b and cos<0: b is forward (h0 is forward when thrust is backward)
        # If h1_is_b and cos>0: b is forward (h1 is forward when thrust is forward)
        # If h1_is_b and cos<0: b is backward

        # Simpler: b_is_forward = (h1_is_b & cos>0) | (h0_is_b & cos<0)
        h1_is_b = ~h0_is_b
        b_is_forward = tagged_mask & ((h1_is_b & (cos_data > 0)) | (h0_is_b & (cos_data < 0)))
        b_is_backward = tagged_mask & ((h0_is_b & (cos_data > 0)) | (h1_is_b & (cos_data < 0)))

        N_F = np.sum(b_is_forward)
        N_B = np.sum(b_is_backward)
        N_tot = N_F + N_B
        if N_tot > 0:
            afb_raw = (N_F - N_B) / N_tot
            sigma_afb = np.sqrt(4 * N_F * N_B / N_tot**3)
        else:
            afb_raw = 0
            sigma_afb = 0

        log.info("WP=%.1f: N_F=%d, N_B=%d, A_FB_raw=%.4f +/- %.4f",
                 thr, N_F, N_B, afb_raw, sigma_afb)

    results["counting_method"] = {}

    # Method B: per cos_theta bin counting
    log.info("\n--- Counting method per cos_theta bin (WP>5.0) ---")
    thr = 5.0
    tagged_mask = (np.maximum(data_h0, data_h1) > thr)
    h0_is_b = data_h0 > data_h1
    h1_is_b = ~h0_is_b

    bins = np.linspace(-0.9, 0.9, 11)
    for i in range(10):
        bin_mask = tagged_mask & (cos_data >= bins[i]) & (cos_data < bins[i+1])
        bfwd = bin_mask & ((h1_is_b & (cos_data > 0)) | (h0_is_b & (cos_data < 0)))
        bbwd = bin_mask & ((h0_is_b & (cos_data > 0)) | (h1_is_b & (cos_data < 0)))
        nf = np.sum(bfwd)
        nb = np.sum(bbwd)
        nt = nf + nb
        afb = (nf - nb) / nt if nt > 0 else 0
        log.info("  cos=[%.2f,%.2f]: N_F=%d, N_B=%d, A_FB=%.4f",
                 bins[i], bins[i+1], nf, nb, afb)

    # ================================================================
    # TASK 1b: Check if thrust axis is truly signed
    # ================================================================
    log.info("\n" + "=" * 70)
    log.info("TASK 1b: IS THE THRUST AXIS TRULY SIGNED?")
    log.info("=" * 70)
    log.info("The thrust axis T is physically unsigned (nematic).")
    log.info("TTheta from ALEPH ntuple encodes a polar angle.")
    log.info("Question: does the sign of cos(TTheta) carry physics information?")
    log.info("")
    log.info("Test: flip the sign of cos_theta for ALL events.")
    log.info("If the slope changes sign, the axis IS signed.")
    log.info("If the slope stays the same, the axis is NOT signed (random).")

    # Original slope
    result_orig = measure_qfb_slope(
        jc["data_qfb_k1.0"], cos_data, data_h0, data_h1, 3.0)

    # Flipped: recompute Q_FB with -cos_theta
    # Q_FB_flipped: forward becomes backward and vice versa
    # q_f_flipped = np.where(-cos_data > 0, qh1_data, qh0_data)
    # = np.where(cos_data < 0, qh1_data, qh0_data)
    # = q_b_manual (the old backward is now forward!)
    # So Q_FB_flipped = q_b_manual - q_f_manual = -Q_FB_original
    qfb_flipped = -jc["data_qfb_k1.0"]
    result_flip = measure_qfb_slope(
        qfb_flipped, cos_data, data_h0, data_h1, 3.0)

    if result_orig and result_flip:
        log.info("\nOriginal slope: %.6f +/- %.6f", result_orig["slope"], result_orig["sigma_slope"])
        log.info("Flipped slope:  %.6f +/- %.6f", result_flip["slope"], result_flip["sigma_slope"])
        log.info("Sum (should be ~0 if axis is signed): %.6f",
                 result_orig["slope"] + result_flip["slope"])
        results["flip_test"] = {
            "slope_original": result_orig["slope"],
            "slope_flipped": result_flip["slope"],
            "sum": result_orig["slope"] + result_flip["slope"],
        }

    # ================================================================
    # TASK 1c: Test with NEGATED cos_theta (swap beam convention)
    # ================================================================
    log.info("\n" + "=" * 70)
    log.info("TASK 1c: WHAT IF WE NEGATE cos_theta?")
    log.info("=" * 70)
    log.info("If the beam direction is wrong, negating cos_theta fixes it.")
    log.info("This is equivalent to fitting slope vs -cos_theta.")

    # Recompute Q_FB with swapped forward/backward:
    # New: forward_is_h1 = (-cos_data) > 0 = cos_data < 0
    q_f_neg = np.where(cos_data < 0, qh1_data, qh0_data)
    q_b_neg = np.where(cos_data < 0, qh0_data, qh1_data)
    qfb_negcos = q_f_neg - q_b_neg  # = -Q_FB_original

    # Now measure slope vs (-cos_theta):
    result_negcos = measure_qfb_slope(
        qfb_negcos, -cos_data, data_h0, data_h1, 3.0)

    if result_negcos:
        log.info("Slope with negated cos_theta: %.6f +/- %.6f",
                 result_negcos["slope"], result_negcos["sigma_slope"])
        afb_neg = result_negcos["slope"] / PUBLISHED_DELTA[1.0]["delta_b"]
        log.info("A_FB(negated) = %.4f (vs original %.4f)",
                 afb_neg, result_orig["slope"] / PUBLISHED_DELTA[1.0]["delta_b"] if result_orig else 0)

    # Actually the simplest test: just fit slope of Q_FB vs (-cos_theta)
    # without recomputing Q_FB at all
    result_negcos2 = measure_qfb_slope(
        jc["data_qfb_k1.0"], -cos_data, data_h0, data_h1, 3.0)
    if result_negcos2:
        log.info("\nSimplest test: original Q_FB, fit vs -cos_theta:")
        log.info("Slope = %.6f (should be -original = %.6f)",
                 result_negcos2["slope"],
                 -result_orig["slope"] if result_orig else 0)

    # ================================================================
    # TASK 1d: Check per-year asymmetry (beam direction may flip by year)
    # ================================================================
    log.info("\n" + "=" * 70)
    log.info("TASK 1d: PER-YEAR ANALYSIS")
    log.info("=" * 70)

    if "year" in pre_data:
        year_data = pre_data["year"]
        unique_years = np.unique(year_data)
        log.info("Years in data: %s", unique_years)

        for yr in unique_years:
            yr_mask = year_data == yr
            n_yr = np.sum(yr_mask)

            # Subset
            cos_yr = cos_data[yr_mask]
            qfb_yr = jc["data_qfb_k1.0"][yr_mask]
            h0_yr = data_h0[yr_mask]
            h1_yr = data_h1[yr_mask]

            result_yr = measure_qfb_slope(qfb_yr, cos_yr, h0_yr, h1_yr, 3.0)
            if result_yr:
                afb_yr = result_yr["slope"] / PUBLISHED_DELTA[1.0]["delta_b"]
                log.info("Year %d: N=%d, slope=%.6f +/- %.6f, A_FB(naive)=%.4f",
                         yr, n_yr, result_yr["slope"], result_yr["sigma_slope"], afb_yr)

                # Also check cos_theta mean per year
                log.info("  <cos_theta> = %.6f, N(cos>0)/N(cos<0) = %.4f",
                         np.mean(cos_yr),
                         np.sum(cos_yr > 0) / max(np.sum(cos_yr < 0), 1))
    else:
        log.info("No year information in preselected data")

    # ================================================================
    # TASK 1e: Check if bflag (MC truth) aligns with expectation
    # ================================================================
    log.info("\n" + "=" * 70)
    log.info("TASK 1e: MC TRUTH CROSS-CHECK (bflag)")
    log.info("=" * 70)

    # Load MC data
    cos_mc = jc["cos_theta_mc"]
    mc_h0 = tags["mc_combined_h0"]
    mc_h1 = tags["mc_combined_h1"]
    pre_mc = np.load(P3_OUT / "preselected_mc.npz", allow_pickle=False)
    bflag_mc = pre_mc["bflag"]

    log.info("MC events: %d", len(cos_mc))
    log.info("bflag values: %s", np.unique(bflag_mc))
    log.info("N(bflag=5) = %d [b quarks]", np.sum(bflag_mc == 5))
    log.info("N(bflag=4) = %d [c quarks]", np.sum(bflag_mc == 4))
    log.info("N(bflag=0) = %d [other/uds]", np.sum(bflag_mc == 0))

    # On symmetric MC, there should be NO A_FB. Check:
    qfb_mc = jc["mc_qfb_k1.0"]
    result_mc = measure_qfb_slope(qfb_mc, cos_mc, mc_h0, mc_h1, 3.0)
    if result_mc:
        log.info("\nMC (all flavours, WP>3.0):")
        log.info("  slope = %.6f +/- %.6f", result_mc["slope"], result_mc["sigma_slope"])
        log.info("  slope/sigma = %.2f (should be ~0 for symmetric MC)",
                 result_mc["slope"] / result_mc["sigma_slope"])

    # MC b-events only
    b_mask_mc = bflag_mc == 5
    qfb_mc_b = jc["mc_qfb_k1.0"][b_mask_mc]
    cos_mc_b = cos_mc[b_mask_mc]
    mc_h0_b = mc_h0[b_mask_mc]
    mc_h1_b = mc_h1[b_mask_mc]
    result_mc_b = measure_qfb_slope(qfb_mc_b, cos_mc_b, mc_h0_b, mc_h1_b, 3.0)
    if result_mc_b:
        log.info("\nMC (b quarks only, WP>3.0):")
        log.info("  slope = %.6f +/- %.6f", result_mc_b["slope"], result_mc_b["sigma_slope"])
        log.info("  slope/sigma = %.2f",
                 result_mc_b["slope"] / result_mc_b["sigma_slope"])

    # ================================================================
    # DEEP DIVE: Profile <Q_FB> vs cos_theta in fine bins
    # ================================================================
    log.info("\n" + "=" * 70)
    log.info("DEEP DIVE: <Q_FB> vs cos_theta profile")
    log.info("=" * 70)

    for kappa in [1.0, 2.0]:
        k_str = "k%.1f" % kappa
        qfb_k = jc["data_qfb_" + k_str]
        delta_b = PUBLISHED_DELTA[kappa]["delta_b"]

        for thr in [0.0, 3.0, 7.0]:  # 0.0 = no b-tag
            if thr > 0:
                tagged = (data_h0 > thr) | (data_h1 > thr)
            else:
                tagged = np.ones(len(qfb_k), dtype=bool)
            valid = ~np.isnan(qfb_k) & tagged

            n_bins = 20
            bin_edges = np.linspace(-0.9, 0.9, n_bins + 1)
            bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

            means = np.zeros(n_bins)
            sigmas = np.zeros(n_bins)
            counts = np.zeros(n_bins, dtype=int)

            for i in range(n_bins):
                mask = valid & (cos_data >= bin_edges[i]) & (cos_data < bin_edges[i+1])
                n = np.sum(mask)
                counts[i] = n
                if n > 50:
                    means[i] = np.mean(qfb_k[mask])
                    sigmas[i] = np.std(qfb_k[mask]) / np.sqrt(n)
                else:
                    means[i] = np.nan
                    sigmas[i] = np.nan

            ok = ~np.isnan(means)
            if np.sum(ok) >= 3:
                x = bin_centers[ok]
                y = means[ok]
                w = 1.0 / sigmas[ok]**2
                S0 = np.sum(w)
                S1 = np.sum(w * x)
                S2 = np.sum(w * x**2)
                Sy = np.sum(w * y)
                Sxy = np.sum(w * x * y)
                det = S0 * S2 - S1**2
                slope = (S0 * Sxy - S1 * Sy) / det
                intercept = (S2 * Sy - S1 * Sxy) / det
                sigma_slope = np.sqrt(S0 / det)

                afb_naive = slope / delta_b
                log.info("\nkappa=%.1f, WP=%.1f (N_tagged=%d):",
                         kappa, thr, np.sum(valid))
                log.info("  slope = %.6f +/- %.6f, intercept = %.6f",
                         slope, sigma_slope, intercept)
                log.info("  A_FB(naive) = %.4f +/- %.4f",
                         afb_naive, sigma_slope / delta_b)
                log.info("  Profile (cos_theta, <Q_FB>):")
                for i in range(n_bins):
                    if ok[i]:
                        log.info("    cos=%.3f: <Q_FB>=%.6f +/- %.6f (N=%d)",
                                 bin_centers[i], means[i], sigmas[i], counts[i])

    # ================================================================
    # KEY DIAGNOSTIC: What is delta_b empirically?
    # ================================================================
    log.info("\n" + "=" * 70)
    log.info("DIAGNOSTIC: Empirical charge separation from MC truth")
    log.info("=" * 70)

    qh0_mc = jc["mc_qh_h0_k1.0"]
    qh1_mc = jc["mc_qh_h1_k1.0"]

    # For b-events in MC:
    # We need to know which hemisphere has the b quark
    # The thrust axis is along the quark direction
    # For symmetric MC, the b can go in either hemisphere
    # delta_b = <Q_F>(b_forward) - <Q_F>(b_backward) averaged over events

    # Simpler: for b events, <Q_FB> should be zero on symmetric MC
    # But the RMS of Q_FB gives sigma(Q_h), related to delta_b via:
    # sigma^2(Q_FB) = sigma^2(Q_F) + sigma^2(Q_B) = 2*sigma^2(Q_h)
    # And delta_b^2 ~ <Q_h(b_hem)>^2 but sign-averaged

    # Actually, delta_b is defined differently:
    # delta_f = <Q_F - Q_B>_f / (sum_f R_f * <Q_F - Q_B>_f)
    # In ALEPH: delta_b is the PUBLISHED charge separation

    b_mc = bflag_mc == 5
    valid_b_mc = b_mc & ~np.isnan(qh0_mc) & ~np.isnan(qh1_mc)

    log.info("\nMC b-events: <Q_h0>=%.6f, <Q_h1>=%.6f, <Q_FB>=%.6f",
             np.mean(qh0_mc[valid_b_mc]),
             np.mean(qh1_mc[valid_b_mc]),
             np.mean(jc["mc_qfb_k1.0"][valid_b_mc]))
    log.info("MC b-events: sigma(Q_h0)=%.4f, sigma(Q_FB)=%.4f",
             np.std(qh0_mc[valid_b_mc]),
             np.std(jc["mc_qfb_k1.0"][valid_b_mc]))

    # ================================================================
    # SMOKING GUN TEST: Use bflag on DATA to verify counting method
    # ================================================================
    log.info("\n" + "=" * 70)
    log.info("SMOKING GUN: bflag on DATA (MC truth label stored with data?)")
    log.info("=" * 70)

    if "bflag_data" in jc.files:
        bflag_data = jc["bflag_data"]
        log.info("bflag_data available! Values: %s", np.unique(bflag_data))

        # Check if it's all zeros (data has no truth) or has physics values
        if np.any(bflag_data > 0):
            log.info("bflag_data has nonzero values - this may be from MC-matched data?")
            n_b = np.sum(bflag_data == 5)
            log.info("N(bflag=5) = %d", n_b)
        else:
            log.info("bflag_data is all zero - no MC truth for data (expected)")
    else:
        log.info("No bflag_data in jet_charge.npz")

    # ================================================================
    # DIRECT COMPARISON: Our slope vs expected
    # ================================================================
    log.info("\n" + "=" * 70)
    log.info("SUMMARY: Expected vs observed slopes")
    log.info("=" * 70)

    for kappa in [0.3, 0.5, 1.0, 2.0]:
        delta_b = PUBLISHED_DELTA[kappa]["delta_b"]
        delta_c = PUBLISHED_DELTA[kappa]["delta_c"]
        # Expected slope for inclusive sample:
        # slope = R_b * delta_b * A_FB^b + R_c * delta_c * A_FB^c
        R_b = 0.21578
        R_c = 0.17223
        AFB_c = 0.0682
        expected_slope = R_b * delta_b * AFB_B_LEP + R_c * delta_c * AFB_c
        log.info("kappa=%.1f: expected inclusive slope = %.6f (delta_b=%.3f)",
                 kappa, expected_slope, delta_b)

    log.info("\nFor tagged sample (enhanced b purity ~70-90%%):")
    log.info("slope ~ f_b * delta_b * A_FB^b")
    log.info("At WP=5.0, f_b~0.8:")
    for kappa in [1.0, 2.0]:
        delta_b = PUBLISHED_DELTA[kappa]["delta_b"]
        expected = 0.8 * delta_b * AFB_B_LEP
        log.info("  kappa=%.1f: expected ~ %.6f", kappa, expected)

    # Get our actual slopes
    for kappa in [1.0, 2.0]:
        k_str = "k%.1f" % kappa
        delta_b = PUBLISHED_DELTA[kappa]["delta_b"]
        result = measure_qfb_slope(
            jc["data_qfb_" + k_str], cos_data, data_h0, data_h1, 5.0)
        if result:
            log.info("  kappa=%.1f: MEASURED slope = %.6f +/- %.6f (%.1f%% of expected)",
                     kappa, result["slope"], result["sigma_slope"],
                     100 * result["slope"] / (0.8 * delta_b * AFB_B_LEP))

    # ================================================================
    # HYPOTHESIS: Hemisphere assignment mismatch
    # ================================================================
    log.info("\n" + "=" * 70)
    log.info("HYPOTHESIS: Is the BDT tag assigned to the RIGHT hemisphere?")
    log.info("=" * 70)
    log.info("If h0/h1 labeling in hemisphere_tags.npz does NOT match")
    log.info("h0/h1 in jet_charge.npz, the counting method will fail.")

    # Check: for events where h0 has a much higher b-tag than h1,
    # does h0 also have more negative charge? (expected for b hemisphere)
    h0_much_higher = (data_h0 > 7.0) & (data_h1 < 2.0)
    h1_much_higher = (data_h1 > 7.0) & (data_h0 < 2.0)

    valid_h0b = h0_much_higher & ~np.isnan(qh0_data) & ~np.isnan(qh1_data)
    valid_h1b = h1_much_higher & ~np.isnan(qh0_data) & ~np.isnan(qh1_data)

    if np.sum(valid_h0b) > 100:
        log.info("\nEvents where h0 is strongly b-tagged (N=%d):", np.sum(valid_h0b))
        log.info("  <Q_h0> = %.6f (should be more negative = b hemisphere)",
                 np.mean(qh0_data[valid_h0b]))
        log.info("  <Q_h1> = %.6f", np.mean(qh1_data[valid_h0b]))
        diff_h0b = np.mean(qh0_data[valid_h0b]) - np.mean(qh1_data[valid_h0b])
        log.info("  <Q_h0> - <Q_h1> = %.6f (should be negative)", diff_h0b)

    if np.sum(valid_h1b) > 100:
        log.info("\nEvents where h1 is strongly b-tagged (N=%d):", np.sum(valid_h1b))
        log.info("  <Q_h0> = %.6f", np.mean(qh0_data[valid_h1b]))
        log.info("  <Q_h1> = %.6f (should be more negative = b hemisphere)",
                 np.mean(qh1_data[valid_h1b]))
        diff_h1b = np.mean(qh1_data[valid_h1b]) - np.mean(qh0_data[valid_h1b])
        log.info("  <Q_h1> - <Q_h0> = %.6f (should be negative)", diff_h1b)

    results["hemisphere_consistency"] = {
        "n_h0_btag_strong": int(np.sum(valid_h0b)),
        "n_h1_btag_strong": int(np.sum(valid_h1b)),
    }

    # ================================================================
    # NUCLEAR OPTION: Recompute Q_FB from scratch using raw track data
    # ================================================================
    log.info("\n" + "=" * 70)
    log.info("NUCLEAR OPTION: Verify Q_FB from raw track data")
    log.info("=" * 70)

    # Load raw preselected data
    charge = pre_data["alltrk_charge"]
    offsets = pre_data["alltrk_charge_offsets"]
    hem = pre_data["alltrk_hem"]
    dot_thrust = pre_data["alltrk_dot_thrust"]
    cos_theta_raw = pre_data["cos_theta_thrust"]

    log.info("N events: %d", len(offsets) - 1)
    log.info("N tracks: %d", len(charge))

    # Verify cos_theta matches
    max_diff_cos = np.max(np.abs(cos_theta_raw - cos_data))
    log.info("max|cos_theta_raw - cos_theta_jc| = %.10f", max_diff_cos)

    # Recompute Q_FB for kappa=1.0 manually
    kappa = 1.0
    n_events = len(offsets) - 1
    qh0_manual = np.full(n_events, np.nan)
    qh1_manual = np.full(n_events, np.nan)

    for evt in range(min(n_events, 50000)):  # Check first 50k events
        start = offsets[evt]
        end = offsets[evt + 1]
        if end <= start:
            continue

        q = charge[start:end].astype(np.float64)
        pL = np.abs(dot_thrust[start:end])
        h = hem[start:end]

        charged = q != 0
        if not np.any(charged):
            continue

        q_c = q[charged]
        pL_c = pL[charged]
        h_c = h[charged]

        pL_k = pL_c ** kappa

        # Hemisphere 0
        m0 = h_c == 0
        if np.any(m0) and np.sum(pL_k[m0]) > 0:
            qh0_manual[evt] = np.sum(q_c[m0] * pL_k[m0]) / np.sum(pL_k[m0])

        # Hemisphere 1
        m1 = h_c == 1
        if np.any(m1) and np.sum(pL_k[m1]) > 0:
            qh1_manual[evt] = np.sum(q_c[m1] * pL_k[m1]) / np.sum(pL_k[m1])

    # Compare to stored values
    n_check = min(n_events, 50000)
    valid_check = ~np.isnan(qh0_manual[:n_check]) & ~np.isnan(qh0_data[:n_check])
    if np.sum(valid_check) > 0:
        diff_h0 = np.max(np.abs(qh0_manual[:n_check][valid_check] - qh0_data[:n_check][valid_check]))
        diff_h1_arr = np.abs(qh1_manual[:n_check][~np.isnan(qh1_manual[:n_check]) & ~np.isnan(qh1_data[:n_check])] -
                             qh1_data[:n_check][~np.isnan(qh1_manual[:n_check]) & ~np.isnan(qh1_data[:n_check])])
        diff_h1 = np.max(diff_h1_arr) if len(diff_h1_arr) > 0 else np.nan
        log.info("Manual vs stored Q_h0: max|diff| = %.10f (N_valid=%d)", diff_h0, np.sum(valid_check))
        log.info("Manual vs stored Q_h1: max|diff| = %.10f", diff_h1)

    # Manual Q_FB
    forward_is_h1_manual = cos_theta_raw[:n_check] > 0
    qf_manual = np.where(forward_is_h1_manual, qh1_manual[:n_check], qh0_manual[:n_check])
    qb_manual = np.where(forward_is_h1_manual, qh0_manual[:n_check], qh1_manual[:n_check])
    qfb_manual_recomp = qf_manual - qb_manual

    valid_qfb = ~np.isnan(qfb_manual_recomp) & ~np.isnan(qfb_data[:n_check])
    if np.sum(valid_qfb) > 0:
        diff_qfb = np.max(np.abs(qfb_manual_recomp[valid_qfb] - qfb_data[:n_check][valid_qfb]))
        log.info("Manual vs stored Q_FB: max|diff| = %.10f", diff_qfb)

    # ================================================================
    # FINAL SUMMARY
    # ================================================================
    log.info("\n" + "=" * 70)
    log.info("FINAL DIAGNOSTIC SUMMARY")
    log.info("=" * 70)

    result_final = measure_qfb_slope(
        jc["data_qfb_k1.0"], cos_data, data_h0, data_h1, 3.0)
    if result_final:
        slope = result_final["slope"]
        expected = 0.8 * PUBLISHED_DELTA[1.0]["delta_b"] * AFB_B_LEP
        log.info("Measured slope (kappa=1.0, WP=3.0): %.6f +/- %.6f",
                 slope, result_final["sigma_slope"])
        log.info("Expected slope (f_b~0.8):           %.6f", expected)
        log.info("Ratio measured/expected:              %.3f", slope / expected)
        log.info("ALEPH A_FB^b = %.4f", AFB_B_ALEPH)
        log.info("Our naive A_FB^b = %.4f",
                 slope / PUBLISHED_DELTA[1.0]["delta_b"])
        log.info("")
        log.info("Suppression factor: %.1f%%", 100 * slope / expected)

    # Save results
    out_path = PHASE4C_OUT / "afb_debug_results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    log.info("\nSaved %s", out_path)


if __name__ == "__main__":
    main()
