"""Phase 3: d0 sign convention validation [D19] — BLOCKING GATE.

Verifies that the stored d0 carries physics-meaningful sign by checking
that positive d0 tail is enhanced in b-enriched hemispheres relative to
inclusive or negative-d0 tail.

Source: STRATEGY.md Section 5.1, item 4 [D19].
Method: Tight double-tag (combined tag > 8 in both hemispheres) as
b-enrichment proxy in data. MC validation uses the same tight-tag
definition on MC hemisphere tags.

Reads: outputs/preselected_data.npz, outputs/preselected_mc.npz,
       outputs/signed_d0.npz, outputs/hemisphere_tags.npz
Writes: outputs/d0_sign_validation.json
"""
import json
import logging
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
OUT = HERE.parent / "outputs"


def _compute_tail_stats(sig_all, sig_b, n_b_enriched, label, thresholds):
    """Compute asymmetry and tail ratio for a sample (data or MC).

    Returns a dict with thresholds, mean_significance, tail_ratio_3sigma.
    """
    result_thresholds = {}
    gate_passed = False

    log.info("\n--- %s d0/sigma_d0 Asymmetry Test ---", label)
    log.info("%-8s  %-12s  %-12s  %-12s  %-12s", "Thresh",
             "N(+,b)", "N(-,b)", "Asym(b)", "Asym(all)")

    for thr in thresholds:
        n_pos_b = int(np.sum(sig_b > thr))
        n_neg_b = int(np.sum(sig_b < -thr))
        n_pos_all = int(np.sum(sig_all > thr))
        n_neg_all = int(np.sum(sig_all < -thr))

        asym_b = (n_pos_b - n_neg_b) / max(n_pos_b + n_neg_b, 1)
        asym_all = (n_pos_all - n_neg_all) / max(n_pos_all + n_neg_all, 1)

        log.info("%-8.1f  %-12d  %-12d  %-12.4f  %-12.4f",
                 thr, n_pos_b, n_neg_b, asym_b, asym_all)

        result_thresholds[str(thr)] = {
            "n_pos_b": n_pos_b,
            "n_neg_b": n_neg_b,
            "n_pos_all": n_pos_all,
            "n_neg_all": n_neg_all,
            "asymmetry_b": float(asym_b),
            "asymmetry_all": float(asym_all),
        }

        if thr == 3.0 and asym_b > 0.05:
            gate_passed = True

    # Mean significance
    mean_pos_all = float(np.mean(sig_all[sig_all > 0]))
    mean_neg_all = float(np.mean(sig_all[sig_all < 0]))
    mean_pos_b = float(np.mean(sig_b[sig_b > 0]))
    mean_neg_b = float(np.mean(sig_b[sig_b < 0]))

    log.info("\n%s mean significance:", label)
    log.info("  All tracks: pos=%.3f, neg=%.3f", mean_pos_all, mean_neg_all)
    log.info("  b-enriched: pos=%.3f, neg=%.3f", mean_pos_b, mean_neg_b)

    # Tail ratio at 3-sigma
    frac_pos_3_b = np.sum(sig_b > 3) / max(len(sig_b), 1)
    frac_neg_3_b = np.sum(sig_b < -3) / max(len(sig_b), 1)
    ratio_3 = frac_pos_3_b / max(frac_neg_3_b, 1e-10)

    log.info("\n%s 3-sigma tail ratio in b-enriched:", label)
    log.info("  Positive: %.4f, Negative: %.4f, Ratio: %.2f",
             frac_pos_3_b, frac_neg_3_b, ratio_3)

    return {
        "thresholds": result_thresholds,
        "mean_significance": {
            "positive_all": mean_pos_all,
            "negative_all": mean_neg_all,
            "positive_b_enriched": mean_pos_b,
            "negative_b_enriched": mean_neg_b,
        },
        "tail_ratio_3sigma": {
            "frac_positive_b": float(frac_pos_3_b),
            "frac_negative_b": float(frac_neg_3_b),
            "ratio_pos_over_neg": float(ratio_3),
        },
        "gate_passed": gate_passed,
        "ratio_3": float(ratio_3),
    }


def main():
    log.info("=" * 60)
    log.info("Phase 3: d0 Sign Convention Validation [D19] — BLOCKING GATE")
    log.info("=" * 60)

    # Load data
    data = np.load(OUT / "preselected_data.npz", allow_pickle=False)
    mc = np.load(OUT / "preselected_mc.npz", allow_pickle=False)
    signed = np.load(OUT / "signed_d0.npz", allow_pickle=False)
    tags = np.load(OUT / "hemisphere_tags.npz", allow_pickle=False)

    # Data arrays
    data_sig = signed["data_signed_sig"]
    data_offsets = data["trk_d0_offsets"]
    n_data_events = len(data_offsets) - 1

    # MC arrays
    mc_sig = signed["mc_signed_sig"]
    mc_offsets = mc["trk_d0_offsets"]
    n_mc_events = len(mc_offsets) - 1

    log.info("Loaded data: %d events, %d tracks", n_data_events, len(data_sig))
    log.info("Loaded MC:   %d events, %d tracks", n_mc_events, len(mc_sig))

    # ---- b-enrichment via tight double-tag (combined tag > 8 both hems) ----
    # Data
    data_tight = (tags["data_combined_h0"] > 8) & (tags["data_combined_h1"] > 8)
    n_data_tight = int(np.sum(data_tight))
    log.info("Data tight-tag b-enriched: %d events (%.2f%%)",
             n_data_tight, 100 * n_data_tight / n_data_events)

    data_counts = np.diff(data_offsets)
    trk_data_tight = np.repeat(data_tight, data_counts)
    sig_b_data = data_sig[trk_data_tight]

    # MC
    mc_tight = (tags["mc_combined_h0"] > 8) & (tags["mc_combined_h1"] > 8)
    n_mc_tight = int(np.sum(mc_tight))
    log.info("MC   tight-tag b-enriched: %d events (%.2f%%)",
             n_mc_tight, 100 * n_mc_tight / n_mc_events)

    mc_counts = np.diff(mc_offsets)
    trk_mc_tight = np.repeat(mc_tight, mc_counts)
    sig_b_mc = mc_sig[trk_mc_tight]

    thresholds = [1.0, 2.0, 3.0, 5.0, 7.0, 10.0]

    # Compute stats for data
    data_stats = _compute_tail_stats(
        data_sig, sig_b_data, n_data_tight, "Data", thresholds)

    # Compute stats for MC
    mc_stats = _compute_tail_stats(
        mc_sig, sig_b_mc, n_mc_tight, "MC", thresholds)

    # Build output JSON
    results = {
        "b_enrichment_method": "tight_double_tag",
        "b_enrichment_definition": "combined_tag > 8 in both hemispheres",
        "data": {
            "n_events": n_data_events,
            "n_b_enriched_events": n_data_tight,
            "n_tracks_b_enriched": int(np.sum(trk_data_tight)),
            "n_tracks_total": len(data_sig),
            "thresholds": data_stats["thresholds"],
            "mean_significance": data_stats["mean_significance"],
            "tail_ratio_3sigma": data_stats["tail_ratio_3sigma"],
        },
        "mc": {
            "n_events": n_mc_events,
            "n_b_enriched_events": n_mc_tight,
            "n_tracks_b_enriched": int(np.sum(trk_mc_tight)),
            "n_tracks_total": len(mc_sig),
            "thresholds": mc_stats["thresholds"],
            "mean_significance": mc_stats["mean_significance"],
            "tail_ratio_3sigma": mc_stats["tail_ratio_3sigma"],
        },
    }

    # Gate decision (based on data)
    gate_passed = data_stats["gate_passed"]
    ratio_3 = data_stats["ratio_3"]

    if gate_passed and ratio_3 > 1.5:
        results["gate_passed"] = True
        results["gate_message"] = (
            "PASS: d0 sign convention is physics-meaningful. "
            "Positive tail is enhanced in tight-tag b-enriched sample "
            "as expected for displaced decay vertices."
        )
        log.info("\n*** GATE PASSED: d0 sign convention validated ***")
    elif ratio_3 > 1.5:
        results["gate_passed"] = True
        results["gate_message"] = (
            "PASS (marginal): Positive/negative ratio > 1.5 at 3-sigma, "
            "but asymmetry metric was marginal."
        )
        log.info("\n*** GATE PASSED (marginal) ***")
    else:
        results["gate_passed"] = False
        results["gate_message"] = (
            "FAIL: d0 sign convention may be inverted or unsigned. "
            "Positive tail is NOT enhanced in b-enriched sample. "
            "BLOCKING: Cannot proceed with lifetime tagger."
        )
        log.error("\n*** GATE FAILED: d0 sign convention NOT validated ***")
        log.error("The strategy must be revised before proceeding.")

    with open(OUT / "d0_sign_validation.json", "w") as f:
        json.dump(results, f, indent=2)
    log.info("Saved d0_sign_validation.json")

    log.info("\nSummary:")
    log.info("  Data tail ratio (3-sigma): %.2f", ratio_3)
    log.info("  MC   tail ratio (3-sigma): %.2f", mc_stats["ratio_3"])


if __name__ == "__main__":
    main()
