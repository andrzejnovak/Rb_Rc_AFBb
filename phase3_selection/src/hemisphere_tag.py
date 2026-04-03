"""Phase 3: Hemisphere probability tag P_hem and mass tag [D8, D18].

Fully vectorized implementation using numpy groupby operations.

Source: hep-ex/9609005 (ALEPH Q tag), inspire_433306.

Reads: outputs/preselected_data.npz, outputs/preselected_mc.npz,
       outputs/d0_significance.npz, outputs/signed_d0.npz
Writes: outputs/hemisphere_tags.npz, outputs/tag_efficiencies.json
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

MASS_THRESHOLD = 1.8  # GeV/c^2, hep-ex/9609005 [D18]
PION_MASS = 0.13957  # GeV/c^2, PDG 2024


def build_resolution_cdf(neg_sig, n_bins=1000):
    """Build resolution function from negative significance tail.

    Returns bin edges and survival function values for fast lookup.
    """
    abs_neg = np.abs(neg_sig)
    max_val = min(np.percentile(abs_neg, 99.99), 100.0)
    bin_edges = np.linspace(0, max_val, n_bins + 1)
    # Histogram of |negative significance|
    counts, _ = np.histogram(abs_neg, bins=bin_edges)
    # Survival function: P(|S| > s)
    cumsum = np.cumsum(counts[::-1])[::-1]
    survival = cumsum / len(abs_neg)
    return bin_edges, survival


def lookup_prob(values, bin_edges, survival):
    """Fast probability lookup using precomputed survival function."""
    idx = np.searchsorted(bin_edges[:-1], values, side="right") - 1
    idx = np.clip(idx, 0, len(survival) - 1)
    probs = survival[idx]
    return np.clip(probs, 1e-10, 1.0)


def compute_hemisphere_tags_vectorized(significance, offsets, hem,
                                       pmag, theta, phi, bin_edges, survival):
    """Compute hemisphere probability and mass tags, fully vectorized.

    Returns per-hemisphere tag values for all events.
    """
    n_events = len(offsets) - 1
    n_tracks = len(significance)

    # Event index for each track
    event_idx = np.repeat(np.arange(n_events), np.diff(offsets))

    # Hemisphere-event index: unique identifier for each (event, hemisphere) pair
    # hem=False -> 2*event_idx, hem=True -> 2*event_idx + 1
    hem_evt_idx = 2 * event_idx + hem.astype(np.int64)

    # --- Probability tag ---
    # Only positive significance tracks contribute
    pos_mask = significance > 0

    # Get probabilities for positive tracks
    probs = np.ones(n_tracks)
    if np.any(pos_mask):
        probs[pos_mask] = lookup_prob(significance[pos_mask], bin_edges, survival)

    # -log(prob) for positive tracks, 0 for negative
    neg_log_p = np.zeros(n_tracks)
    neg_log_p[pos_mask] = -np.log(probs[pos_mask])

    # Sum -log(P) per hemisphere
    nlp_per_hem = np.zeros(2 * n_events)
    np.add.at(nlp_per_hem, hem_evt_idx, neg_log_p)

    nlp_h0 = nlp_per_hem[0::2]
    nlp_h1 = nlp_per_hem[1::2]

    # Count positive tracks per hemisphere
    npos_per_hem = np.zeros(2 * n_events, dtype=np.int64)
    np.add.at(npos_per_hem, hem_evt_idx[pos_mask], 1)
    npos_h0 = npos_per_hem[0::2]
    npos_h1 = npos_per_hem[1::2]

    # --- Mass tag ---
    # Displaced tracks: significance > 2.0
    disp_mask = significance > 2.0

    # 4-vectors for displaced tracks (assuming pion mass)
    E = np.sqrt(pmag**2 + PION_MASS**2)
    px_trk = pmag * np.sin(theta) * np.cos(phi)
    py_trk = pmag * np.sin(theta) * np.sin(phi)
    pz_trk = pmag * np.cos(theta)

    # Sum 4-vectors per hemisphere (displaced tracks only)
    sum_E = np.zeros(2 * n_events)
    sum_px = np.zeros(2 * n_events)
    sum_py = np.zeros(2 * n_events)
    sum_pz = np.zeros(2 * n_events)
    n_disp = np.zeros(2 * n_events, dtype=np.int64)

    disp_idx = hem_evt_idx[disp_mask]
    np.add.at(sum_E, disp_idx, E[disp_mask])
    np.add.at(sum_px, disp_idx, px_trk[disp_mask])
    np.add.at(sum_py, disp_idx, py_trk[disp_mask])
    np.add.at(sum_pz, disp_idx, pz_trk[disp_mask])
    np.add.at(n_disp, disp_idx, 1)

    m2 = sum_E**2 - sum_px**2 - sum_py**2 - sum_pz**2
    hem_mass = np.sqrt(np.maximum(m2, 0))
    # Only meaningful if >= 2 displaced tracks
    hem_mass[n_disp < 2] = 0.0

    mass_h0 = hem_mass[0::2]
    mass_h1 = hem_mass[1::2]

    # --- N-sigma tag ---
    nsig3_per_hem = np.zeros(2 * n_events, dtype=np.int64)
    above3 = significance > 3.0
    np.add.at(nsig3_per_hem, hem_evt_idx[above3], 1)
    nsig3_h0 = nsig3_per_hem[0::2]
    nsig3_h1 = nsig3_per_hem[1::2]

    # --- Combined tag ---
    MASS_BONUS = 3.0
    combined_h0 = nlp_h0 + MASS_BONUS * (mass_h0 > MASS_THRESHOLD)
    combined_h1 = nlp_h1 + MASS_BONUS * (mass_h1 > MASS_THRESHOLD)

    return {
        "nlp_h0": nlp_h0, "nlp_h1": nlp_h1,
        "npos_h0": npos_h0, "npos_h1": npos_h1,
        "mass_h0": mass_h0, "mass_h1": mass_h1,
        "nsig3_h0": nsig3_h0, "nsig3_h1": nsig3_h1,
        "combined_h0": combined_h0, "combined_h1": combined_h1,
    }


def scan_working_points(tags_h0, tags_h1, bflag, thresholds):
    """Scan working points for a hemisphere tagger."""
    n_events = len(tags_h0)
    b_mask = bflag == 4
    n_b = int(np.sum(b_mask))

    results = []
    for thr in thresholds:
        tagged_h0 = tags_h0 > thr
        tagged_h1 = tags_h1 > thr

        single = tagged_h0 | tagged_h1
        double = tagged_h0 & tagged_h1

        n_single = int(np.sum(single))
        n_double = int(np.sum(double))
        n_hem_tagged = int(np.sum(tagged_h0)) + int(np.sum(tagged_h1))

        eff_b_single = int(np.sum(single & b_mask)) / max(n_b, 1)
        eff_b_double = int(np.sum(double & b_mask)) / max(n_b, 1)

        results.append({
            "threshold": float(thr),
            "n_single_tag": n_single,
            "n_double_tag": n_double,
            "f_s": n_hem_tagged / (2 * n_events),
            "f_d": n_double / n_events,
            "eff_b_single_proxy": float(eff_b_single),
            "eff_b_double_proxy": float(eff_b_double),
        })

    return results


def main():
    log.info("=" * 60)
    log.info("Phase 3: Hemisphere Tagging [D8, D18]")
    log.info("=" * 60)

    data = np.load(OUT / "preselected_data.npz", allow_pickle=False)
    mc = np.load(OUT / "preselected_mc.npz", allow_pickle=False)
    signed = np.load(OUT / "signed_d0.npz", allow_pickle=False)

    for prefix, sample in [("data", data), ("mc", mc)]:
        sig = signed[f"{prefix}_signed_sig"]
        offsets = sample["trk_d0_offsets"]
        hem = sample["trk_hem"]
        pmag = sample["trk_pmag"]
        theta = sample["trk_theta"]
        phi = sample["trk_phi"]

        n_events = len(offsets) - 1
        log.info("Processing %s: %d events, %d tracks", prefix, n_events, len(sig))

        # Build resolution function from negative tail
        neg_sig = sig[sig < 0]
        log.info("  Negative tail: %d tracks", len(neg_sig))
        bin_edges, survival = build_resolution_cdf(neg_sig)

        # Compute tags
        log.info("  Computing hemisphere tags (vectorized)...")
        tags = compute_hemisphere_tags_vectorized(
            sig, offsets, hem, pmag, theta, phi, bin_edges, survival
        )

        if prefix == "data":
            data_tags = tags
        else:
            mc_tags = tags

    # Save
    np.savez_compressed(
        OUT / "hemisphere_tags.npz",
        **{f"data_{k}": v for k, v in data_tags.items()},
        **{f"mc_{k}": v for k, v in mc_tags.items()},
    )
    log.info("Saved hemisphere_tags.npz")

    # Working point scan
    combined_thresholds = np.arange(0.5, 15.0, 0.5).tolist()
    prob_thresholds = np.arange(0.5, 12.0, 0.5).tolist()

    bflag = data["bflag"]
    mc_bflag = mc["bflag"]

    scan_combined = scan_working_points(
        data_tags["combined_h0"], data_tags["combined_h1"],
        bflag, combined_thresholds
    )
    scan_prob = scan_working_points(
        data_tags["nlp_h0"], data_tags["nlp_h1"],
        bflag, prob_thresholds
    )

    # N-sigma cross-check
    nsig_thresholds = [1, 2, 3, 4, 5]
    scan_nsig = scan_working_points(
        data_tags["nsig3_h0"].astype(float), data_tags["nsig3_h1"].astype(float),
        bflag, nsig_thresholds
    )

    scan_mc_combined = scan_working_points(
        mc_tags["combined_h0"], mc_tags["combined_h1"],
        mc_bflag, combined_thresholds
    )

    efficiencies = {
        "combined_data": scan_combined,
        "probability_data": scan_prob,
        "nsig3_data": scan_nsig,
        "combined_mc": scan_mc_combined,
        "mass_threshold_GeV": MASS_THRESHOLD,
        "mass_threshold_source": "hep-ex/9609005, STRATEGY.md [D18]",
    }

    with open(OUT / "tag_efficiencies.json", "w") as f:
        json.dump(efficiencies, f, indent=2)
    log.info("Saved tag_efficiencies.json")

    # Summary
    log.info("\n--- Representative Working Points (Data, Combined Tag) ---")
    log.info("%-10s  %-8s  %-8s  %-10s  %-10s",
             "Threshold", "f_s", "f_d", "eff_b(1)", "eff_b(2)")
    for r in scan_combined:
        if r["threshold"] in [2.0, 4.0, 6.0, 8.0, 10.0]:
            log.info("%-10.1f  %-8.4f  %-8.4f  %-10.4f  %-10.4f",
                     r["threshold"], r["f_s"], r["f_d"],
                     r["eff_b_single_proxy"], r["eff_b_double_proxy"])

    log.info("\n--- Cross-check: N-sigma Tag (Data) ---")
    for r in scan_nsig:
        log.info("N>=%d: f_s=%.4f, f_d=%.4f",
                 int(r["threshold"]), r["f_s"], r["f_d"])


if __name__ == "__main__":
    main()
