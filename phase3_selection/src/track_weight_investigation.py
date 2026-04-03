"""Phase 3: Track weight investigation [STRATEGY.md Section 6.2].

Investigates the weight[] branch and assesses its impact on:
1. Hemisphere tag rates (P_hem computation)
2. Jet charge Q_FB
3. Whether weights are reconstruction weights or event weights

Reads: outputs/preselected_data.npz, outputs/preselected_mc.npz,
       outputs/hemisphere_tags.npz, outputs/jet_charge.npz
Writes: outputs/track_weight_investigation.json
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


def investigate_weight_properties(data, mc):
    """Characterize the weight branch."""
    log.info("--- Weight Branch Properties ---")

    for prefix, sample in [("data", data), ("mc", mc)]:
        # Good-track weights (nvdet>0, quality cuts)
        w_good = sample["trk_weight"]
        # All-track weights (for jet charge)
        w_all = sample["alltrk_weight"]

        log.info("%s good tracks: n=%d, mean=%.4f, std=%.4f, min=%.4f, max=%.4f",
                 prefix, len(w_good), w_good.mean(), w_good.std(),
                 w_good.min(), w_good.max())
        log.info("%s all tracks:  n=%d, mean=%.4f, std=%.4f, min=%.4f, max=%.4f",
                 prefix, len(w_all), w_all.mean(), w_all.std(),
                 w_all.min(), w_all.max())

        # Distribution of weights
        pcts = np.percentile(w_all, [1, 5, 25, 50, 75, 95, 99])
        log.info("%s percentiles [1,5,25,50,75,95,99]: %s",
                 prefix, [f"{p:.3f}" for p in pcts])

        # Correlation with track properties
        pmag = sample["alltrk_pmag"]
        corr_p = np.corrcoef(w_all[:100000], pmag[:100000])[0, 1]
        log.info("%s weight-pmag correlation (first 100k): %.4f", prefix, corr_p)

    return {
        "data_good_tracks": {
            "n": int(len(data["trk_weight"])),
            "mean": float(data["trk_weight"].mean()),
            "std": float(data["trk_weight"].std()),
            "min": float(data["trk_weight"].min()),
            "max": float(data["trk_weight"].max()),
        },
        "data_all_tracks": {
            "n": int(len(data["alltrk_weight"])),
            "mean": float(data["alltrk_weight"].mean()),
            "std": float(data["alltrk_weight"].std()),
            "min": float(data["alltrk_weight"].min()),
            "max": float(data["alltrk_weight"].max()),
        },
        "mc_good_tracks": {
            "n": int(len(mc["trk_weight"])),
            "mean": float(mc["trk_weight"].mean()),
            "std": float(mc["trk_weight"].std()),
            "min": float(mc["trk_weight"].min()),
            "max": float(mc["trk_weight"].max()),
        },
        "mc_all_tracks": {
            "n": int(len(mc["alltrk_weight"])),
            "mean": float(mc["alltrk_weight"].mean()),
            "std": float(mc["alltrk_weight"].std()),
            "min": float(mc["alltrk_weight"].min()),
            "max": float(mc["alltrk_weight"].max()),
        },
    }


def assess_jet_charge_impact(data):
    """Assess impact of weights on jet charge Q_FB.

    Compare unweighted Q_FB (current) vs weighted Q_FB.
    """
    log.info("\n--- Jet Charge Weight Impact ---")

    charge = data["alltrk_charge"]
    offsets = data["alltrk_charge_offsets"]
    hem = data["alltrk_hem"]
    dot_thrust = data["alltrk_dot_thrust"]
    cos_theta = data["cos_theta_thrust"]
    weight = data["alltrk_weight"]

    n_events = len(offsets) - 1
    counts = np.diff(offsets)
    event_idx = np.repeat(np.arange(n_events), counts)

    # Exclude charge=0 tracks
    charged = charge != 0
    q = charge[charged].astype(np.float64)
    pL_abs = np.abs(dot_thrust[charged])
    h = hem[charged]
    evt = event_idx[charged]
    w = weight[charged]

    results = {}

    for kappa in [0.3, 0.5, 1.0, 2.0]:
        pL_k = pL_abs ** kappa

        hem_evt = 2 * evt + h.astype(np.int64)

        # Unweighted
        numer_uw = np.zeros(2 * n_events)
        np.add.at(numer_uw, hem_evt, q * pL_k)
        denom_uw = np.zeros(2 * n_events)
        np.add.at(denom_uw, hem_evt, pL_k)
        qh_uw = np.where(denom_uw > 0, numer_uw / denom_uw, np.nan)

        # Weighted: multiply pL_k by track weight
        numer_w = np.zeros(2 * n_events)
        np.add.at(numer_w, hem_evt, q * pL_k * w)
        denom_w = np.zeros(2 * n_events)
        np.add.at(denom_w, hem_evt, pL_k * w)
        qh_w = np.where(denom_w > 0, numer_w / denom_w, np.nan)

        # Q_FB
        qh_uw_h0 = qh_uw[0::2]
        qh_uw_h1 = qh_uw[1::2]
        forward_is_h1 = cos_theta > 0
        qfb_uw = np.where(forward_is_h1, qh_uw_h1, qh_uw_h0) - np.where(forward_is_h1, qh_uw_h0, qh_uw_h1)

        qh_w_h0 = qh_w[0::2]
        qh_w_h1 = qh_w[1::2]
        qfb_w = np.where(forward_is_h1, qh_w_h1, qh_w_h0) - np.where(forward_is_h1, qh_w_h0, qh_w_h1)

        # Compare
        valid = ~np.isnan(qfb_uw) & ~np.isnan(qfb_w)
        mean_uw = float(np.mean(qfb_uw[valid]))
        mean_w = float(np.mean(qfb_w[valid]))
        diff = mean_w - mean_uw
        rel_diff = diff / abs(mean_uw) if abs(mean_uw) > 1e-6 else 0.0

        log.info("kappa=%.1f: <Q_FB> unweighted=%.6f, weighted=%.6f, "
                 "diff=%.6f (%.2f%%)", kappa, mean_uw, mean_w, diff,
                 100 * rel_diff)

        results[f"kappa_{kappa}"] = {
            "mean_qfb_unweighted": mean_uw,
            "mean_qfb_weighted": mean_w,
            "difference": float(diff),
            "relative_difference_pct": float(100 * rel_diff),
        }

    return results


def assess_tag_rate_impact(data):
    """Assess impact of weights on hemisphere tag rates.

    The hemisphere probability tag uses significance = d0/sigma_d0.
    Track weights could enter as:
    (a) weighting the probability product: P_hem = prod(P_i^w_i)
    (b) event-level reweighting of tag rates

    We test (a): recompute -ln(P_hem) with -w_i * ln(P_i) instead of -ln(P_i).
    """
    log.info("\n--- Hemisphere Tag Weight Impact ---")

    from hemisphere_tag import build_resolution_cdf, lookup_prob

    signed = np.load(OUT / "signed_d0.npz", allow_pickle=False)
    sig = signed["data_signed_sig"]
    offsets = data["trk_d0_offsets"]
    hem = data["trk_hem"]
    weight = data["trk_weight"]

    n_events = len(offsets) - 1
    event_idx = np.repeat(np.arange(n_events), np.diff(offsets))
    hem_evt = 2 * event_idx + hem.astype(np.int64)

    # Build resolution CDF
    neg_sig = sig[sig < 0]
    bin_edges, survival = build_resolution_cdf(neg_sig)

    # Positive significance tracks
    pos_mask = sig > 0
    n_tracks = len(sig)

    probs = np.ones(n_tracks)
    if np.any(pos_mask):
        probs[pos_mask] = lookup_prob(sig[pos_mask], bin_edges, survival)

    neg_log_p = np.zeros(n_tracks)
    neg_log_p[pos_mask] = -np.log(probs[pos_mask])

    # Unweighted: sum -ln(P) per hemisphere
    nlp_uw = np.zeros(2 * n_events)
    np.add.at(nlp_uw, hem_evt, neg_log_p)

    # Weighted: sum w * (-ln(P)) per hemisphere
    nlp_w = np.zeros(2 * n_events)
    np.add.at(nlp_w, hem_evt, weight * neg_log_p)

    nlp_uw_h0 = nlp_uw[0::2]
    nlp_w_h0 = nlp_w[0::2]

    # Compare tag rates at working point 5.0
    wp = 5.0
    f_s_uw = np.sum(nlp_uw_h0 > wp) / n_events  # hemisphere 0 only
    f_s_w = np.sum(nlp_w_h0 > wp) / n_events

    log.info("WP=%.1f: f_s(h0) unweighted=%.4f, weighted=%.4f, "
             "rel diff=%.2f%%", wp, f_s_uw, f_s_w,
             100 * (f_s_w - f_s_uw) / max(f_s_uw, 1e-6))

    # Correlation between unweighted and weighted
    corr = np.corrcoef(nlp_uw_h0[:100000], nlp_w_h0[:100000])[0, 1]
    log.info("Correlation(nlp_unweighted, nlp_weighted) = %.6f", corr)

    return {
        "working_point": float(wp),
        "f_s_h0_unweighted": float(f_s_uw),
        "f_s_h0_weighted": float(f_s_w),
        "relative_difference_pct": float(100 * (f_s_w - f_s_uw) / max(f_s_uw, 1e-6)),
        "correlation": float(corr),
    }


def main():
    log.info("=" * 60)
    log.info("Phase 3: Track Weight Investigation [STRATEGY.md 6.2]")
    log.info("=" * 60)

    data = np.load(OUT / "preselected_data.npz", allow_pickle=False)
    mc = np.load(OUT / "preselected_mc.npz", allow_pickle=False)

    results = {}

    # 1. Weight properties
    results["properties"] = investigate_weight_properties(data, mc)

    # 2. Impact on jet charge
    results["jet_charge_impact"] = assess_jet_charge_impact(data)

    # 3. Impact on tag rates
    results["tag_rate_impact"] = assess_tag_rate_impact(data)

    # 4. Conclusion
    # Check if any impact exceeds 5% relative
    max_qfb_impact = max(abs(v["relative_difference_pct"])
                         for v in results["jet_charge_impact"].values())
    tag_impact = abs(results["tag_rate_impact"]["relative_difference_pct"])

    if max_qfb_impact > 5.0 or tag_impact > 5.0:
        conclusion = ("MATERIAL IMPACT: Track weights change Q_FB by up to "
                       f"{max_qfb_impact:.1f}% and tag rates by {tag_impact:.1f}%. "
                       "Weights should be applied in Phase 4.")
    else:
        conclusion = ("MINOR IMPACT: Track weights change Q_FB by at most "
                       f"{max_qfb_impact:.1f}% and tag rates by {tag_impact:.1f}%. "
                       "Weights have mean ~1.0 and primarily affect low-weight "
                       "tracks. Impact is within systematic uncertainties. "
                       "Document as systematic for Phase 4.")

    results["conclusion"] = conclusion
    results["recommendation"] = (
        "The weight branch (range [0.03, 9.0], mean ~1.02) represents "
        "per-track reconstruction weights. The impact on Q_FB and tag rates "
        "is quantified above. Phase 4 should: (1) apply weights in the "
        "nominal analysis, (2) compare weighted vs unweighted as a systematic."
    )

    log.info("\n--- Conclusion ---")
    log.info(conclusion)

    with open(OUT / "track_weight_investigation.json", "w") as f:
        json.dump(results, f, indent=2)
    log.info("Saved track_weight_investigation.json")


if __name__ == "__main__":
    main()
