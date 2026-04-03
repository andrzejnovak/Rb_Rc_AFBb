"""Diagnostic script: Investigate A_FB^b sign convention.

Checks:
1. cos_theta distribution (signed vs unsigned?)
2. Q_FB forward vs backward pattern
3. hemisphere charge pattern for b-tagged events
4. MC validation (A_FB should be ~0 on symmetric MC)
5. Comparison to Phase 4b code
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
P3_OUT = HERE.parents[2] / "phase3_selection" / "outputs"
P4A_OUT = HERE.parents[1] / "4a_expected" / "outputs"

sys.path.insert(0, str(HERE.parents[1] / "4a_expected" / "src"))
from purity_corrected_afb import (
    estimate_purity_at_wp, measure_qfb_slope, extract_afb_purity_corrected,
    PUBLISHED_DELTA, R_B_SM, R_C_SM, R_UDS_SM,
)


def main():
    log.info("=" * 60)
    log.info("DIAGNOSTIC: A_FB^b Sign Convention Investigation")
    log.info("=" * 60)

    # Load data
    jc = np.load(P3_OUT / "jet_charge.npz", allow_pickle=False)
    tags = np.load(P3_OUT / "hemisphere_tags.npz", allow_pickle=False)

    cos_data = jc["cos_theta_data"]
    cos_mc = jc["cos_theta_mc"]

    # ============================================================
    # CHECK 1: cos_theta distribution
    # ============================================================
    log.info("\n--- CHECK 1: cos_theta distribution ---")
    log.info("DATA: min=%.4f, max=%.4f, mean=%.4f",
             cos_data.min(), cos_data.max(), cos_data.mean())
    log.info("DATA: N(cos>0)=%d, N(cos<0)=%d, frac_pos=%.4f",
             np.sum(cos_data > 0), np.sum(cos_data < 0),
             np.mean(cos_data > 0))
    log.info("MC:   min=%.4f, max=%.4f, mean=%.4f",
             cos_mc.min(), cos_mc.max(), cos_mc.mean())
    log.info("MC:   N(cos>0)=%d, N(cos<0)=%d, frac_pos=%.4f",
             np.sum(cos_mc > 0), np.sum(cos_mc < 0),
             np.mean(cos_mc > 0))

    # ============================================================
    # CHECK 2: Q_FB pattern (should have linear cos_theta dependence)
    # ============================================================
    log.info("\n--- CHECK 2: Q_FB pattern vs cos_theta ---")
    for kappa_str in ["k0.3", "k0.5", "k1.0", "k2.0"]:
        qfb_data = jc["data_qfb_" + kappa_str]
        valid = ~np.isnan(qfb_data)
        log.info("kappa=%s: mean(Q_FB)=%.6f, N_valid=%d",
                 kappa_str, np.nanmean(qfb_data), np.sum(valid))

        # Bin in cos_theta
        bins = np.linspace(-0.9, 0.9, 11)
        centers = 0.5 * (bins[:-1] + bins[1:])
        means = []
        for i in range(10):
            mask = valid & (cos_data >= bins[i]) & (cos_data < bins[i+1])
            if np.sum(mask) > 100:
                means.append(np.mean(qfb_data[mask]))
            else:
                means.append(np.nan)
        means = np.array(means)
        log.info("  <Q_FB> vs cos_theta bins: %s",
                 " ".join(["%.5f" % m if not np.isnan(m) else "NaN"
                           for m in means]))

    # ============================================================
    # CHECK 3: Hemisphere charge for b-tagged events
    # ============================================================
    log.info("\n--- CHECK 3: Q_h for forward vs backward hemispheres ---")
    log.info("(For b quarks: Q_F should be more negative than Q_B)")

    data_h0 = tags["data_combined_h0"]
    data_h1 = tags["data_combined_h1"]

    for kappa_str in ["k1.0"]:
        qh0 = jc["data_qh_h0_" + kappa_str]
        qh1 = jc["data_qh_h1_" + kappa_str]

        # b-tagged events (tight)
        btag = (data_h0 > 5.0) | (data_h1 > 5.0)
        valid_h = ~np.isnan(qh0) & ~np.isnan(qh1) & btag

        # Forward hemisphere = hemisphere in direction of cos_theta > 0
        fwd_is_h1 = cos_data > 0
        q_fwd = np.where(fwd_is_h1, qh1, qh0)
        q_bwd = np.where(fwd_is_h1, qh0, qh1)

        log.info("kappa=%s, b-tagged (thr>5):", kappa_str)
        log.info("  <Q_forward> = %.6f", np.mean(q_fwd[valid_h]))
        log.info("  <Q_backward> = %.6f", np.mean(q_bwd[valid_h]))
        log.info("  <Q_F - Q_B> = %.6f",
                 np.mean(q_fwd[valid_h]) - np.mean(q_bwd[valid_h]))
        log.info("  (Expected: Q_F more negative for b quarks -> Q_F - Q_B < 0)")

    # ============================================================
    # CHECK 4: MC validation (A_FB should be ~0)
    # ============================================================
    log.info("\n--- CHECK 4: MC A_FB extraction ---")
    mc_h0 = tags["mc_combined_h0"]
    mc_h1 = tags["mc_combined_h1"]

    with open(P4A_OUT / "mc_calibration.json") as f:
        mc_cal_data = json.load(f)
    mc_cal = mc_cal_data["full_mc_calibration"]

    with open(P3_OUT / "tag_efficiencies.json") as f:
        eff_data = json.load(f)
    mc_fs_by_wp = {}
    for entry in eff_data["combined_mc"]:
        mc_fs_by_wp[entry["threshold"]] = entry["f_s"]

    for kappa in [1.0]:
        k_str = "k%.1f" % kappa
        qfb_mc = jc["mc_qfb_" + k_str]

        for thr in [3.0, 5.0, 7.0]:
            slope_result = measure_qfb_slope(
                qfb_mc, cos_mc, mc_h0, mc_h1, thr)
            if slope_result is None:
                log.info("MC kappa=%.1f, thr=%.1f: no result", kappa, thr)
                continue

            f_s = mc_fs_by_wp.get(thr)
            purity = estimate_purity_at_wp(mc_cal, f_s) if f_s else None

            # MC with afb_c=0 (correct)
            ext_mc0 = extract_afb_purity_corrected(
                slope_result["slope"], slope_result["sigma_slope"],
                purity, kappa, afb_c=0.0, afb_uds=0.0)

            log.info("MC kappa=%.1f, thr=%.1f: slope=%.6f +/- %.6f, "
                     "A_FB^b(afb_c=0)=%.4f +/- %.4f",
                     kappa, thr,
                     slope_result["slope"], slope_result["sigma_slope"],
                     ext_mc0["afb_purity_corrected"] if ext_mc0 else float("nan"),
                     ext_mc0["sigma_afb_purity"] if ext_mc0 else float("nan"))

    # ============================================================
    # CHECK 5: Raw slope on data - does it have the right sign?
    # ============================================================
    log.info("\n--- CHECK 5: Raw Q_FB slope on data ---")
    log.info("Expected: NEGATIVE slope for b quarks")
    log.info("  (b has Q=-1/3 -> delta_b < 0 in signed convention)")
    log.info("  But ALEPH uses |delta_b| > 0, so slope should be POSITIVE")
    log.info("  because <Q_FB> = delta_b * A_FB^b * cos(theta)")
    log.info("  with A_FB^b ~ +0.10 and delta_b ~ +0.37 -> slope ~ +0.037")

    for kappa in [0.3, 0.5, 1.0, 2.0]:
        k_str = "k%.1f" % kappa
        qfb_data = jc["data_qfb_" + k_str]
        for thr in [3.0, 5.0]:
            slope_result = measure_qfb_slope(
                qfb_data, cos_data, data_h0, data_h1, thr)
            if slope_result is None:
                continue
            log.info("DATA kappa=%.1f, thr=%.1f: slope=%.6f +/- %.6f, "
                     "intercept=%.6f, chi2/ndf=%.2f/%d",
                     kappa, thr,
                     slope_result["slope"], slope_result["sigma_slope"],
                     slope_result["intercept"],
                     slope_result["chi2"], slope_result["ndf"])

    # ============================================================
    # CHECK 6: The CRITICAL check - is the thrust axis signed?
    # ============================================================
    log.info("\n--- CHECK 6: Thrust axis sign convention ---")
    log.info("TTheta is the polar angle of the thrust axis.")
    log.info("The thrust axis is UNSIGNED (nematic): +T and -T are equivalent.")
    log.info("ALEPH convention: TTheta in [0, pi], so cos(TTheta) can be + or -.")
    log.info("But what defines the SIGN of the thrust axis?")
    log.info("")
    log.info("Key question: Does cos_theta_thrust = cos(TTheta) give a")
    log.info("signed cos(theta) where + means forward (e- direction)?")
    log.info("Or is it just the polar angle of an unsigned axis?")

    # If thrust axis is signed by the highest-energy hemisphere,
    # then cos_theta_thrust is NOT the angle w.r.t. the e- beam
    # in the physics sense. It's the angle of one arbitrary choice.

    # Check: is the distribution of cos_theta symmetric?
    hist_pos = np.sum((cos_data > 0) & (cos_data < 0.9))
    hist_neg = np.sum((cos_data < 0) & (cos_data > -0.9))
    log.info("N(0 < cos < 0.9) = %d", hist_pos)
    log.info("N(-0.9 < cos < 0) = %d", hist_neg)
    log.info("Ratio pos/neg = %.4f", hist_pos / max(hist_neg, 1))
    log.info("(Should be ~1.0 for proper signed thrust axis)")

    # ============================================================
    # CHECK 7: Direct Q_h test - no thrust axis needed
    # ============================================================
    log.info("\n--- CHECK 7: Direct hemisphere charge test ---")
    log.info("For EACH event, one hemisphere has the b quark.")
    log.info("The b-quark hemisphere should have more negative charge.")
    log.info("Check: <Q_h0> vs <Q_h1> for b-tagged events:")

    for kappa_str in ["k1.0"]:
        qh0 = jc["data_qh_h0_" + kappa_str]
        qh1 = jc["data_qh_h1_" + kappa_str]
        btag = (data_h0 > 5.0) | (data_h1 > 5.0)
        valid_h = ~np.isnan(qh0) & ~np.isnan(qh1) & btag

        log.info("<Q_h0> = %.6f (b-tagged)", np.mean(qh0[valid_h]))
        log.info("<Q_h1> = %.6f (b-tagged)", np.mean(qh1[valid_h]))
        log.info("These should be ~equal (h0/h1 are arbitrary)")

        # Now check: for events where h0 is more b-like (higher tag score)
        h0_more_b = data_h0 > data_h1
        h0b = valid_h & h0_more_b
        h1b = valid_h & ~h0_more_b

        log.info("\nWhen h0 is more b-like (higher b-tag score):")
        log.info("  <Q_h0> = %.6f (should be more negative)", np.mean(qh0[h0b]))
        log.info("  <Q_h1> = %.6f", np.mean(qh1[h0b]))
        log.info("When h1 is more b-like:")
        log.info("  <Q_h0> = %.6f", np.mean(qh0[h1b]))
        log.info("  <Q_h1> = %.6f (should be more negative)", np.mean(qh1[h1b]))


if __name__ == "__main__":
    main()
