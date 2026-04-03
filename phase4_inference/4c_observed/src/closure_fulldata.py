"""Phase 4c: Independent closure test on full data.

Splits the full dataset 60/40 and extracts A_FB^b on each half
independently. Checks consistency.

Also: operating point stability with chi2/ndf.
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
P3_OUT = HERE.parents[2] / "phase3_selection" / "outputs"

sys.path.insert(0, str(HERE.parents[1] / "4a_expected" / "src"))
from purity_corrected_afb import (
    measure_qfb_slope, PUBLISHED_DELTA, N_COS_BINS, COS_RANGE,
)


def extract_afb_inclusive(slope, sigma_slope, kappa):
    """Extract A_FB^b using inclusive slope/delta_b."""
    pub = PUBLISHED_DELTA.get(kappa)
    if pub is None:
        return None, None
    delta_b = pub["delta_b"]
    return float(slope / delta_b), float(sigma_slope / delta_b)


def main():
    log.info("=" * 60)
    log.info("Phase 4c: Closure Test on Full Data")
    log.info("=" * 60)

    tags = np.load(P3_OUT / "hemisphere_tags.npz", allow_pickle=False)
    jc = np.load(P3_OUT / "jet_charge.npz", allow_pickle=False)

    data_h0 = tags["data_combined_h0"]
    data_h1 = tags["data_combined_h1"]
    cos_theta = jc["cos_theta_data"]
    n_data = len(data_h0)

    log.info("Full data events: %d", n_data)

    # ================================================================
    # 60/40 split
    # ================================================================
    rng = np.random.RandomState(42)
    perm = rng.permutation(n_data)
    split = int(0.6 * n_data)
    idx_a = perm[:split]
    idx_b = perm[split:]
    log.info("Split A: %d events (60%%)", len(idx_a))
    log.info("Split B: %d events (40%%)", len(idx_b))

    KAPPA_VALUES = [0.3, 0.5, 1.0, 2.0]
    KAPPA_LABELS = {0.3: "k0.3", 0.5: "k0.5", 1.0: "k1.0", 2.0: "k2.0"}
    thresholds = [3.0, 5.0, 7.0]

    closure_results = []

    for kappa in KAPPA_VALUES:
        k_str = KAPPA_LABELS[kappa]
        qfb_full = jc["data_qfb_" + k_str]

        for thr in thresholds:
            # Full data
            slope_full = measure_qfb_slope(
                qfb_full, cos_theta, data_h0, data_h1, thr)
            if slope_full is None:
                continue

            # Split A
            slope_a = measure_qfb_slope(
                qfb_full[idx_a], cos_theta[idx_a],
                data_h0[idx_a], data_h1[idx_a], thr)
            # Split B
            slope_b = measure_qfb_slope(
                qfb_full[idx_b], cos_theta[idx_b],
                data_h0[idx_b], data_h1[idx_b], thr)

            if slope_a is None or slope_b is None:
                continue

            afb_full, sig_full = extract_afb_inclusive(
                slope_full["slope"], slope_full["sigma_slope"], kappa)
            afb_a, sig_a = extract_afb_inclusive(
                slope_a["slope"], slope_a["sigma_slope"], kappa)
            afb_b, sig_b = extract_afb_inclusive(
                slope_b["slope"], slope_b["sigma_slope"], kappa)

            if sig_a > 0 and sig_b > 0:
                pull_ab = (afb_a - afb_b) / np.sqrt(sig_a**2 + sig_b**2)
            else:
                pull_ab = float("nan")

            log.info("k=%.1f, WP=%.1f: A=%.4f+/-%.4f, B=%.4f+/-%.4f, "
                     "pull=%.2f, full=%.4f+/-%.4f",
                     kappa, thr, afb_a, sig_a, afb_b, sig_b,
                     pull_ab, afb_full, sig_full)

            closure_results.append({
                "kappa": float(kappa),
                "threshold": float(thr),
                "afb_full": afb_full,
                "sigma_full": sig_full,
                "afb_split_a": afb_a,
                "sigma_split_a": sig_a,
                "afb_split_b": afb_b,
                "sigma_split_b": sig_b,
                "pull_ab": float(pull_ab),
            })

    # ================================================================
    # Summary: all pulls
    # ================================================================
    pulls = [r["pull_ab"] for r in closure_results
             if not np.isnan(r["pull_ab"])]
    log.info("\n--- Closure Summary ---")
    log.info("N tests: %d", len(pulls))
    if pulls:
        pulls_arr = np.array(pulls)
        log.info("Mean pull: %.3f", np.mean(pulls_arr))
        log.info("RMS pull: %.3f", np.sqrt(np.mean(pulls_arr**2)))
        log.info("Max |pull|: %.3f", np.max(np.abs(pulls_arr)))
        n_fail = np.sum(np.abs(pulls_arr) > 3.0)
        log.info("|pull| > 3: %d / %d", n_fail, len(pulls))
        passes = n_fail == 0
    else:
        passes = False

    # ================================================================
    # Operating point stability
    # ================================================================
    log.info("\n--- Operating Point Stability ---")
    for kappa in [2.0]:  # Best kappa
        k_str = KAPPA_LABELS[kappa]
        qfb_data = jc["data_qfb_" + k_str]

        afb_vals = []
        afb_errs = []
        wp_labels = []

        for thr in [2.0, 3.0, 5.0, 7.0, 9.0]:
            slope_result = measure_qfb_slope(
                qfb_data, cos_theta, data_h0, data_h1, thr)
            if slope_result is None:
                continue
            afb, sig = extract_afb_inclusive(
                slope_result["slope"], slope_result["sigma_slope"], kappa)
            if sig > 0:
                afb_vals.append(afb)
                afb_errs.append(sig)
                wp_labels.append("WP %.1f" % thr)

        if len(afb_vals) >= 2:
            afb_arr = np.array(afb_vals)
            err_arr = np.array(afb_errs)
            w = 1.0 / err_arr**2
            mean = np.sum(w * afb_arr) / np.sum(w)
            chi2_stab = float(np.sum((afb_arr - mean)**2 / err_arr**2))
            ndf_stab = len(afb_arr) - 1
            p_stab = float(1.0 - chi2_dist.cdf(chi2_stab, ndf_stab))

            log.info("kappa=%.1f: chi2/ndf = %.2f/%d, p = %.4f",
                     kappa, chi2_stab, ndf_stab, p_stab)
            for label, val, err in zip(wp_labels, afb_vals, afb_errs):
                log.info("  %s: %.4f +/- %.4f", label, val, err)

    # ================================================================
    # Output
    # ================================================================
    output = {
        "method": "60/40 split closure + operating point stability",
        "n_data": n_data,
        "split_seed": 42,
        "split_a_size": len(idx_a),
        "split_b_size": len(idx_b),
        "closure_results": closure_results,
        "closure_passes": bool(passes),
        "n_tests": len(pulls),
        "mean_pull": float(np.mean(pulls)) if pulls else None,
        "rms_pull": float(np.sqrt(np.mean(np.array(pulls)**2))) if pulls else None,
        "max_abs_pull": float(np.max(np.abs(pulls))) if pulls else None,
        "n_pulls_above_3": int(np.sum(np.abs(np.array(pulls)) > 3.0)) if pulls else 0,
    }

    out_path = PHASE4C_OUT / "closure_fulldata.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    log.info("\nSaved %s", out_path.name)


if __name__ == "__main__":
    main()
