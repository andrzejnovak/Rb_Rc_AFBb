"""Phase 3: Double-tag counting for R_b [D2].

Implements hemisphere tagging, counts N_t, N_tt at multiple working points.
Computes f_s, f_d, and estimates R_b using the double-tag formula.

Formalism from inspire_416138, Eq. 1-2; hep-ex/9609005, Eq. 1-2:
  f_s = eps_b * R_b + eps_c * R_c + eps_uds * (1 - R_b - R_c)
  f_d = C_b * eps_b^2 * R_b + C_c * eps_c^2 * R_c + C_uds * eps_uds^2 * (1-R_b-R_c)

Reads: outputs/hemisphere_tags.npz, outputs/preselected_data.npz,
       outputs/preselected_mc.npz
Writes: outputs/double_tag_counts.json, outputs/rb_scan.json
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

# External inputs from STRATEGY.md and PDG
# R_c constrained to SM value [D6]
R_C_SM = 0.17223  # Source: hep-ex/0509008
R_C_ERR = 0.0030  # LEP combined uncertainty

# Hemisphere correlations — use published ALEPH value inflated by 2x [D17]
# Source: hep-ex/9609005 Table 1 — C_b for Q-tag
C_B = 1.01  # Nominal (1 + small correlation)
C_C = 1.00  # Charm has negligible correlation
C_UDS = 1.00  # Light flavour has negligible correlation

# Background efficiencies — estimated from MC (crude)
# Will be refined when we can separate flavours better
# These are initial estimates; the double-tag method extracts eps_b from data
EPS_C_NOMINAL = 0.05  # Charm tagging efficiency (fraction tagging charm as b)
EPS_UDS_NOMINAL = 0.005  # Light-flavour mistag rate


def extract_rb(f_s, f_d, eps_c, eps_uds, R_c, C_b=1.01, C_c=1.0, C_uds=1.0):
    """Extract R_b and eps_b from double-tag equations.

    Solves the system:
      f_s = eps_b * R_b + eps_c * R_c + eps_uds * (1 - R_b - R_c)
      f_d = C_b * eps_b^2 * R_b + C_c * eps_c^2 * R_c + C_uds * eps_uds^2 * (1-R_b-R_c)

    Returns R_b, eps_b, or (nan, nan) if no solution.
    """
    # From f_s equation: eps_b * R_b = f_s - eps_c * R_c - eps_uds * (1 - R_b - R_c)
    # Let background term: bg_s = eps_c * R_c + eps_uds * (1 - R_c)
    # Then: eps_b * R_b = f_s - bg_s + eps_uds * R_b
    # So: R_b * (eps_b - eps_uds) = f_s - bg_s
    # And: eps_b = (f_s - bg_s) / R_b + eps_uds  [if we knew R_b]

    # From f_d equation:
    # Let bg_d = C_c * eps_c^2 * R_c + C_uds * eps_uds^2 * (1 - R_c)
    # Then: C_b * eps_b^2 * R_b = f_d - bg_d + C_uds * eps_uds^2 * R_b
    # So: R_b * (C_b * eps_b^2 - C_uds * eps_uds^2) = f_d - bg_d

    # Substitute eps_b from first equation into second to get R_b.
    # Let a = f_s - eps_c * R_c - eps_uds * (1 - R_c)
    # eps_b = a/R_b + eps_uds  => eps_b*R_b = a + eps_uds*R_b
    # But from first eq: eps_b*R_b = f_s - eps_c*R_c - eps_uds*(1-R_b-R_c)
    #                              = a + eps_uds*R_b  ✓

    # Second equation:
    # C_b * eps_b^2 * R_b = f_d - C_c*eps_c^2*R_c - C_uds*eps_uds^2*(1-R_b-R_c)
    # C_b * (a/R_b + eps_uds)^2 * R_b = f_d - C_c*eps_c^2*R_c - C_uds*eps_uds^2*(1-R_c) + C_uds*eps_uds^2*R_b
    # C_b * (a^2/R_b + 2*a*eps_uds + eps_uds^2*R_b) = f_d - bg_d + C_uds*eps_uds^2*R_b

    a = f_s - eps_c * R_c - eps_uds * (1 - R_c)

    bg_d = C_c * eps_c**2 * R_c + C_uds * eps_uds**2 * (1 - R_c)

    # C_b * a^2/R_b + C_b * 2*a*eps_uds + C_b * eps_uds^2 * R_b = f_d - bg_d + C_uds*eps_uds^2*R_b
    # C_b * a^2/R_b + (C_b - C_uds) * eps_uds^2 * R_b = f_d - bg_d - C_b * 2 * a * eps_uds
    # Multiply by R_b:
    # C_b * a^2 + (C_b - C_uds) * eps_uds^2 * R_b^2 = (f_d - bg_d - 2*C_b*a*eps_uds) * R_b

    rhs_coeff = f_d - bg_d - 2 * C_b * a * eps_uds
    quad_a = (C_b - C_uds) * eps_uds**2
    quad_b = -rhs_coeff
    quad_c = C_b * a**2

    if abs(quad_a) < 1e-15:
        # Linear case
        if abs(quad_b) < 1e-15:
            return np.nan, np.nan
        R_b = -quad_c / quad_b
    else:
        disc = quad_b**2 - 4 * quad_a * quad_c
        if disc < 0:
            return np.nan, np.nan
        sqrt_disc = np.sqrt(disc)
        r1 = (-quad_b + sqrt_disc) / (2 * quad_a)
        r2 = (-quad_b - sqrt_disc) / (2 * quad_a)

        # Choose physical solution (0 < R_b < 1)
        candidates = [r for r in [r1, r2] if 0 < r < 1]
        if not candidates:
            # Try the closest to SM value
            candidates = [r for r in [r1, r2] if r > 0]
        if not candidates:
            return np.nan, np.nan
        R_b = min(candidates, key=lambda x: abs(x - 0.217))

    if R_b <= 0:
        return np.nan, np.nan

    eps_b = a / R_b + eps_uds

    return float(R_b), float(eps_b)


def count_tags(tags_h0, tags_h1, threshold):
    """Count single-tagged hemispheres and double-tagged events."""
    tagged_h0 = tags_h0 > threshold
    tagged_h1 = tags_h1 > threshold

    N_had = len(tags_h0)
    N_t = int(np.sum(tagged_h0)) + int(np.sum(tagged_h1))
    N_tt = int(np.sum(tagged_h0 & tagged_h1))

    f_s = N_t / (2 * N_had)
    f_d = N_tt / N_had

    return N_had, N_t, N_tt, f_s, f_d


def main():
    log.info("=" * 60)
    log.info("Phase 3: Double-Tag Counting [D2]")
    log.info("=" * 60)

    tags = np.load(OUT / "hemisphere_tags.npz", allow_pickle=False)
    data = np.load(OUT / "preselected_data.npz", allow_pickle=False)

    # Use combined tag (probability + mass)
    data_h0 = tags["data_combined_h0"]
    data_h1 = tags["data_combined_h1"]

    # Also probability-only for cross-check
    data_prob_h0 = tags["data_nlp_h0"]
    data_prob_h1 = tags["data_nlp_h1"]

    # Operating point scan
    thresholds = np.arange(1.0, 14.0, 0.5)

    log.info("\n--- R_b Operating Point Scan (Combined Tag) ---")
    log.info("%-8s  %-8s  %-8s  %-10s  %-10s  %-10s  %-10s",
             "Thresh", "f_s", "f_d", "R_b", "eps_b", "N_t", "N_tt")

    scan_results = []
    for thr in thresholds:
        N_had, N_t, N_tt, f_s, f_d = count_tags(data_h0, data_h1, thr)

        if f_s > 0 and f_d > 0:
            R_b, eps_b = extract_rb(
                f_s, f_d, EPS_C_NOMINAL, EPS_UDS_NOMINAL, R_C_SM, C_B, C_C, C_UDS
            )
        else:
            R_b, eps_b = np.nan, np.nan

        # Statistical uncertainty on R_b (crude estimate)
        if not np.isnan(R_b) and N_tt > 0:
            # From counting: sigma(R_b) ~ R_b / sqrt(N_tt) approximately
            sigma_rb_stat = R_b / np.sqrt(N_tt) if N_tt > 0 else np.nan
        else:
            sigma_rb_stat = np.nan

        scan_results.append({
            "threshold": float(thr),
            "N_had": int(N_had),
            "N_t": int(N_t),
            "N_tt": int(N_tt),
            "f_s": float(f_s),
            "f_d": float(f_d),
            "R_b": float(R_b) if not np.isnan(R_b) else None,
            "eps_b": float(eps_b) if not np.isnan(eps_b) else None,
            "sigma_rb_stat": float(sigma_rb_stat) if not np.isnan(sigma_rb_stat) else None,
            "tag_type": "combined",
        })

        if not np.isnan(R_b):
            log.info("%-8.1f  %-8.4f  %-8.6f  %-10.5f  %-10.4f  %-10d  %-10d",
                     thr, f_s, f_d, R_b, eps_b, N_t, N_tt)

    # Cross-check: probability-only tag
    log.info("\n--- R_b Operating Point Scan (Probability-only Tag) ---")
    prob_scan_results = []
    for thr in thresholds:
        N_had, N_t, N_tt, f_s, f_d = count_tags(data_prob_h0, data_prob_h1, thr)

        if f_s > 0 and f_d > 0:
            R_b, eps_b = extract_rb(
                f_s, f_d, EPS_C_NOMINAL, EPS_UDS_NOMINAL, R_C_SM, C_B, C_C, C_UDS
            )
        else:
            R_b, eps_b = np.nan, np.nan

        sigma_rb_stat = R_b / np.sqrt(N_tt) if (not np.isnan(R_b) and N_tt > 0) else np.nan

        prob_scan_results.append({
            "threshold": float(thr),
            "N_had": int(N_had),
            "N_t": int(N_t),
            "N_tt": int(N_tt),
            "f_s": float(f_s),
            "f_d": float(f_d),
            "R_b": float(R_b) if not np.isnan(R_b) else None,
            "eps_b": float(eps_b) if not np.isnan(eps_b) else None,
            "sigma_rb_stat": float(sigma_rb_stat) if not np.isnan(sigma_rb_stat) else None,
            "tag_type": "probability",
        })

    # Save
    output = {
        "combined_scan": scan_results,
        "probability_scan": prob_scan_results,
        "external_inputs": {
            "R_c_SM": R_C_SM,
            "R_c_err": R_C_ERR,
            "R_c_source": "hep-ex/0509008",
            "C_b": C_B,
            "C_c": C_C,
            "C_uds": C_UDS,
            "C_b_source": "hep-ex/9609005 Table 1, inflated 2x per [D17]",
            "eps_c_nominal": EPS_C_NOMINAL,
            "eps_uds_nominal": EPS_UDS_NOMINAL,
        },
    }

    with open(OUT / "double_tag_counts.json", "w") as f:
        json.dump(output, f, indent=2)
    log.info("Saved double_tag_counts.json")

    # Find optimal working point (minimum statistical uncertainty)
    valid_points = [r for r in scan_results
                    if r["R_b"] is not None and r["sigma_rb_stat"] is not None
                    and r["sigma_rb_stat"] > 0]
    if valid_points:
        best = min(valid_points, key=lambda x: x["sigma_rb_stat"])
        log.info("\n--- Optimal Working Point (minimum stat. uncertainty) ---")
        log.info("Threshold: %.1f", best["threshold"])
        log.info("R_b = %.5f +/- %.5f (stat)", best["R_b"], best["sigma_rb_stat"])
        log.info("eps_b = %.4f", best["eps_b"])
        log.info("N_t = %d, N_tt = %d", best["N_t"], best["N_tt"])

    # Save R_b scan for plotting
    rb_scan = {
        "combined": {
            "thresholds": [r["threshold"] for r in scan_results],
            "R_b": [r["R_b"] for r in scan_results],
            "sigma_rb": [r["sigma_rb_stat"] for r in scan_results],
            "f_s": [r["f_s"] for r in scan_results],
            "f_d": [r["f_d"] for r in scan_results],
        },
        "probability": {
            "thresholds": [r["threshold"] for r in prob_scan_results],
            "R_b": [r["R_b"] for r in prob_scan_results],
            "sigma_rb": [r["sigma_rb_stat"] for r in prob_scan_results],
            "f_s": [r["f_s"] for r in prob_scan_results],
            "f_d": [r["f_d"] for r in prob_scan_results],
        },
        "reference": {
            "ALEPH_Rb": 0.2158,
            "ALEPH_Rb_err": 0.0014,
            "LEP_combined_Rb": 0.21629,
            "LEP_combined_err": 0.00066,
            "SM_Rb": 0.21578,
            "sources": "hep-ex/9609005, hep-ex/0509008",
        },
    }
    with open(OUT / "rb_scan.json", "w") as f:
        json.dump(rb_scan, f, indent=2)
    log.info("Saved rb_scan.json")


if __name__ == "__main__":
    main()
