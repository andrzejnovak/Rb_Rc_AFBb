"""Phase 3: Hemisphere jet charge Q_h for A_FB^b [D4, D5].

Fully vectorized implementation.

Q_h(kappa) = sum_i q_i * |p_{L,i}|^kappa / sum_i |p_{L,i}|^kappa
kappa=infinity: charge of highest-|p_L| track (leading particle charge).

Source: inspire_433746, STRATEGY.md Section 6.2.

Reads: outputs/preselected_data.npz, outputs/preselected_mc.npz
Writes: outputs/jet_charge.npz, outputs/jet_charge.json
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

KAPPA_VALUES = [0.3, 0.5, 1.0, 2.0]


def compute_jet_charge_vectorized(charge, pL, offsets, hem, cos_theta, kappa):
    """Compute hemisphere jet charge for a given kappa, fully vectorized.

    Returns qh_h0, qh_h1, qfb arrays of shape (n_events,).
    """
    n_events = len(offsets) - 1
    n_tracks = len(charge)

    # Event index per track
    counts = np.diff(offsets)
    event_idx = np.repeat(np.arange(n_events), counts)

    # Exclude charge=0 tracks
    charged = charge != 0
    if not np.any(charged):
        return (np.full(n_events, np.nan),
                np.full(n_events, np.nan),
                np.full(n_events, np.nan))

    q = charge[charged].astype(np.float64)
    pL_abs = np.abs(pL[charged])
    h = hem[charged]
    evt = event_idx[charged]

    pL_k = pL_abs ** kappa

    # Hemisphere-event index
    hem_evt = 2 * evt + h.astype(np.int64)

    # Numerator: sum(q * |pL|^kappa) per hemisphere
    numer = np.zeros(2 * n_events)
    np.add.at(numer, hem_evt, q * pL_k)

    # Denominator: sum(|pL|^kappa) per hemisphere
    denom = np.zeros(2 * n_events)
    np.add.at(denom, hem_evt, pL_k)

    # Q_h = numerator / denominator
    qh = np.where(denom > 0, numer / denom, np.nan)
    qh_h0 = qh[0::2]
    qh_h1 = qh[1::2]

    # Q_FB: Forward = direction of cos_theta > 0 (electron beam)
    forward_is_h1 = cos_theta > 0
    q_f = np.where(forward_is_h1, qh_h1, qh_h0)
    q_b = np.where(forward_is_h1, qh_h0, qh_h1)
    qfb = q_f - q_b

    return qh_h0, qh_h1, qfb


def compute_leading_charge_vectorized(charge, pL, offsets, hem, cos_theta):
    """Compute kappa=infinity (leading particle charge), vectorized."""
    n_events = len(offsets) - 1
    n_tracks = len(charge)

    counts = np.diff(offsets)
    event_idx = np.repeat(np.arange(n_events), counts)

    charged = charge != 0
    q = charge[charged].astype(np.float64)
    pL_abs = np.abs(pL[charged])
    h = hem[charged]
    evt = event_idx[charged]

    hem_evt = 2 * evt + h.astype(np.int64)

    # For each hemisphere, find the track with maximum |pL|
    # Use numpy: sort by hem_evt, then within each group take the argmax of pL
    qh = np.full(2 * n_events, np.nan)

    # For each hemisphere-event, find the track with max |pL|
    # Approach: set pL to -inf for tracks not in each group, then argmax
    # More efficient: use np.maximum.at with structured approach
    max_pL = np.full(2 * n_events, -1.0)
    best_q = np.full(2 * n_events, np.nan)

    # Update max: iterate only once using the fact that np.maximum.at
    # handles duplicates. But we need the CHARGE at the max pL.
    # Use a sort-based approach: sort by (hem_evt, -pL), take first per group
    sort_key = hem_evt.astype(np.float64) * 1e6 - pL_abs
    order = np.argsort(sort_key)

    # After sorting, the first occurrence of each hem_evt has max pL
    sorted_he = hem_evt[order]
    sorted_q = q[order]

    # Find first occurrence of each hem_evt
    diff = np.diff(sorted_he, prepend=-1)
    first = diff != 0
    unique_he = sorted_he[first]
    unique_q = sorted_q[first]

    qh[unique_he] = unique_q

    qh_h0 = qh[0::2]
    qh_h1 = qh[1::2]

    forward_is_h1 = cos_theta > 0
    q_f = np.where(forward_is_h1, qh_h1, qh_h0)
    q_b = np.where(forward_is_h1, qh_h0, qh_h1)
    qfb = q_f - q_b

    return qh_h0, qh_h1, qfb


def process_sample(sample, prefix):
    """Process one sample for jet charge computation."""
    charge = sample["alltrk_charge"]
    offsets = sample["alltrk_charge_offsets"]
    hem = sample["alltrk_hem"]
    dot_thrust = sample["alltrk_dot_thrust"]
    cos_theta = sample["cos_theta_thrust"]

    n_events = len(offsets) - 1
    log.info("Processing %s: %d events, %d tracks", prefix, n_events, len(charge))

    pL = dot_thrust  # Longitudinal momentum = dot product with thrust

    results = {}

    for kappa in KAPPA_VALUES:
        log.info("  kappa=%.1f", kappa)
        qh_h0, qh_h1, qfb = compute_jet_charge_vectorized(
            charge, pL, offsets, hem, cos_theta, kappa
        )
        k_str = f"k{kappa:.1f}"
        results[f"qh_h0_{k_str}"] = qh_h0
        results[f"qh_h1_{k_str}"] = qh_h1
        results[f"qfb_{k_str}"] = qfb

    # kappa=infinity
    log.info("  kappa=infinity (leading particle)")
    qh_h0_inf, qh_h1_inf, qfb_inf = compute_leading_charge_vectorized(
        charge, pL, offsets, hem, cos_theta
    )
    results["qh_h0_kinf"] = qh_h0_inf
    results["qh_h1_kinf"] = qh_h1_inf
    results["qfb_kinf"] = qfb_inf

    return results


def main():
    log.info("=" * 60)
    log.info("Phase 3: Hemisphere Jet Charge [D4, D5]")
    log.info("=" * 60)

    data = np.load(OUT / "preselected_data.npz", allow_pickle=False)
    mc = np.load(OUT / "preselected_mc.npz", allow_pickle=False)

    data_results = process_sample(data, "data")
    mc_results = process_sample(mc, "mc")

    np.savez_compressed(
        OUT / "jet_charge.npz",
        **{f"data_{k}": v for k, v in data_results.items()},
        **{f"mc_{k}": v for k, v in mc_results.items()},
        cos_theta_data=data["cos_theta_thrust"],
        cos_theta_mc=mc["cos_theta_thrust"],
        bflag_data=data["bflag"],
    )
    log.info("Saved jet_charge.npz")

    # Summary
    bflag = data["bflag"]
    summary = {"kappa_values": KAPPA_VALUES + [float("inf")]}

    log.info("\n--- Jet Charge Summary (Data) ---")
    log.info("%-10s  %-12s  %-12s", "kappa", "mean(Q_FB)", "sigma(Q_h)")

    for kappa in KAPPA_VALUES:
        k_str = f"k{kappa:.1f}"
        qfb = data_results[f"qfb_{k_str}"]
        qh0 = data_results[f"qh_h0_{k_str}"]
        valid = ~np.isnan(qfb)
        mean_qfb = float(np.nanmean(qfb)) if np.any(valid) else np.nan
        sigma_qh = float(np.nanstd(qh0)) if np.any(~np.isnan(qh0)) else np.nan

        log.info("%-10.1f  %-12.5f  %-12.4f", kappa, mean_qfb, sigma_qh)
        summary[f"kappa_{kappa}"] = {
            "mean_qfb": mean_qfb,
            "sigma_qh": sigma_qh,
        }

    # kappa=infinity
    qfb_inf = data_results["qfb_kinf"]
    qh0_inf = data_results["qh_h0_kinf"]
    mean_qfb_inf = float(np.nanmean(qfb_inf))
    sigma_inf = float(np.nanstd(qh0_inf))
    log.info("%-10s  %-12.5f  %-12.4f", "inf", mean_qfb_inf, sigma_inf)
    summary["kappa_inf"] = {"mean_qfb": mean_qfb_inf, "sigma_qh": sigma_inf}

    with open(OUT / "jet_charge.json", "w") as f:
        json.dump(summary, f, indent=2)
    log.info("Saved jet_charge.json")


if __name__ == "__main__":
    main()
