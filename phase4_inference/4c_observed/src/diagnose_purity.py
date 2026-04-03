"""Diagnostic: Check MC truth flavour fractions at each working point.

This script computes the true b/c/uds fractions among tagged events at each
WP threshold using MC truth (bflag), and compares to what
estimate_purity_at_wp returns.
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
from purity_corrected_afb import estimate_purity_at_wp


def main():
    log.info("=" * 60)
    log.info("DIAGNOSTIC: MC Truth Purity at Each WP")
    log.info("=" * 60)

    tags = np.load(P3_OUT / "hemisphere_tags.npz", allow_pickle=False)
    mc_data = np.load(P3_OUT / "preselected_mc.npz", allow_pickle=False)

    mc_h0 = tags["mc_combined_h0"]
    mc_h1 = tags["mc_combined_h1"]
    bflag = mc_data["bflag"]  # MC truth: 1=b, 0=non-b

    log.info("MC events: %d", len(bflag))
    log.info("bflag=1 fraction: %.4f", np.mean(bflag == 1))

    # Check if there's a cflag or flavor flag
    keys = list(mc_data.files)
    log.info("MC keys: %s", keys)

    # Load calibration
    with open(P4A_OUT / "mc_calibration.json") as f:
        mc_cal_data = json.load(f)
    mc_cal = mc_cal_data["full_mc_calibration"]

    with open(P3_OUT / "tag_efficiencies.json") as f:
        eff_data = json.load(f)
    mc_fs_by_wp = {}
    for entry in eff_data["combined_mc"]:
        mc_fs_by_wp[entry["threshold"]] = entry["f_s"]

    thresholds = [2.0, 3.0, 5.0, 7.0, 9.0, 10.0]

    log.info("\n%-8s %-8s %-8s %-8s %-8s %-8s %-8s",
             "WP", "N_tag", "f_b_MC", "f_b_est", "f_c_est", "f_uds_est", "f_s")
    log.info("-" * 70)

    for thr in thresholds:
        tagged = (mc_h0 > thr) | (mc_h1 > thr)
        n_tagged = np.sum(tagged)

        if n_tagged > 0:
            f_b_truth = np.mean(bflag[tagged] == 1)
        else:
            f_b_truth = 0.0

        f_s = mc_fs_by_wp.get(thr)
        purity = estimate_purity_at_wp(mc_cal, f_s) if f_s else None

        f_b_est = purity["f_b"] if purity else float("nan")
        f_c_est = purity["f_c"] if purity else float("nan")
        f_uds_est = purity["f_uds"] if purity else float("nan")

        log.info("%-8.1f %-8d %-8.4f %-8.4f %-8.4f %-8.4f %-8.4f",
                 thr, n_tagged, f_b_truth, f_b_est, f_c_est, f_uds_est,
                 f_s if f_s else 0.0)

    # Now show what estimate_purity_at_wp returns for each calibration point
    log.info("\n--- Calibration points available ---")
    for thr_str, v in mc_cal.items():
        log.info("Threshold %s: f_s=%.4f, eps_b=%.4f, eps_c=%.4f, eps_uds=%.4f",
                 thr_str, v["f_s"], v.get("eps_b", 0), v.get("eps_c", 0),
                 v.get("eps_uds", 0))


if __name__ == "__main__":
    main()
