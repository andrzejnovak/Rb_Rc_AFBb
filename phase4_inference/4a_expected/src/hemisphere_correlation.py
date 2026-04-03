"""Phase 4a: Hemisphere correlation C_b estimation from MC.

Estimates the hemisphere-hemisphere tagging efficiency correlation C_b
from MC. C_b != 1 because:
1. Event-level properties (thrust, multiplicity) affect both hemispheres
2. Gluon radiation (hard gluon → y_3) distorts hemisphere independence
3. Geometric acceptance correlates via cos(theta)

Following STRATEGY.md Section 7.1: three-pronged approach using
kinematic estimation from MC (prong b, primary).

Reads: phase3_selection/outputs/hemisphere_tags.npz,
       phase3_selection/outputs/preselected_mc.npz
Writes: outputs/correlation_results.json
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
P3_OUT = HERE.parents[2] / "phase3_selection" / "outputs"
OUT = HERE.parent / "outputs"


def compute_correlation(h0, h1, threshold):
    """Compute hemisphere tagging correlation factor C_q.

    C_q = P(both tagged) / P(h0 tagged) * P(h1 tagged)
        = f_d / (f_h0 * f_h1)

    where f_h0, f_h1 are per-hemisphere tag rates and f_d is the
    double-tag rate. If hemispheres are independent, C_q = 1.
    """
    tagged_h0 = h0 > threshold
    tagged_h1 = h1 > threshold
    n = len(h0)

    f_h0 = np.mean(tagged_h0)
    f_h1 = np.mean(tagged_h1)
    f_d = np.mean(tagged_h0 & tagged_h1)

    if f_h0 * f_h1 > 0:
        C = f_d / (f_h0 * f_h1)
    else:
        C = np.nan

    # Statistical uncertainty on C: propagate Poisson errors
    N_h0 = np.sum(tagged_h0)
    N_h1 = np.sum(tagged_h1)
    N_d = np.sum(tagged_h0 & tagged_h1)

    if N_h0 > 0 and N_h1 > 0 and N_d > 0:
        # delta_C/C = sqrt(1/N_d + 1/N_h0 + 1/N_h1) approximately
        sigma_C = C * np.sqrt(1.0/N_d + 1.0/N_h0 + 1.0/N_h1 - 2.0/n)
        sigma_C = max(sigma_C, C * 1e-4)
    else:
        sigma_C = np.nan

    return float(C), float(sigma_C), int(N_d)


def correlation_in_bins(h0, h1, bin_var, bin_edges, threshold):
    """Compute C_q in bins of a variable."""
    results = []
    for i in range(len(bin_edges) - 1):
        mask = (bin_var >= bin_edges[i]) & (bin_var < bin_edges[i+1])
        if np.sum(mask) < 100:
            results.append({'bin_lo': float(bin_edges[i]),
                           'bin_hi': float(bin_edges[i+1]),
                           'C': None, 'sigma_C': None, 'N': 0})
            continue
        C, sigma_C, N_d = compute_correlation(h0[mask], h1[mask], threshold)
        results.append({
            'bin_lo': float(bin_edges[i]),
            'bin_hi': float(bin_edges[i+1]),
            'C': float(C) if not np.isnan(C) else None,
            'sigma_C': float(sigma_C) if not np.isnan(sigma_C) else None,
            'N': int(N_d),
        })
    return results


def main():
    log.info("=" * 60)
    log.info("Phase 4a: Hemisphere Correlation C_b Estimation")
    log.info("=" * 60)

    tags = np.load(P3_OUT / "hemisphere_tags.npz", allow_pickle=False)
    mc = np.load(P3_OUT / "preselected_mc.npz", allow_pickle=False)

    mc_h0 = tags["mc_combined_h0"]
    mc_h1 = tags["mc_combined_h1"]
    cos_theta = mc["cos_theta_thrust"]

    n_mc = len(mc_h0)
    log.info("MC events: %d", n_mc)

    # Compute C at multiple working points
    thresholds = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]

    log.info("\n--- Hemisphere Correlation vs Working Point ---")
    log.info("%-8s  %-10s  %-10s  %-8s", "WP", "C", "sigma_C", "N_tt")

    wp_results = []
    for thr in thresholds:
        C, sigma_C, N_d = compute_correlation(mc_h0, mc_h1, thr)
        log.info("%-8.1f  %-10.4f  %-10.4f  %-8d", thr, C, sigma_C, N_d)
        wp_results.append({
            'threshold': float(thr),
            'C': float(C),
            'sigma_C': float(sigma_C),
            'N_tt': int(N_d),
        })

    # Correlation vs cos(theta) at reference WP = 5.0
    cos_bins = np.linspace(0, 0.9, 10)
    abs_cos = np.abs(cos_theta)
    cos_results = correlation_in_bins(mc_h0, mc_h1, abs_cos, cos_bins, 5.0)

    # Also compute for data (from P3 tags) to compare
    data_h0 = tags["data_combined_h0"]
    data_h1 = tags["data_combined_h1"]
    data_mc = np.load(P3_OUT / "preselected_data.npz", allow_pickle=False)
    data_cos = data_mc["cos_theta_thrust"]
    data_abs_cos = np.abs(data_cos)

    data_wp_results = []
    for thr in thresholds:
        C, sigma_C, N_d = compute_correlation(data_h0, data_h1, thr)
        data_wp_results.append({
            'threshold': float(thr),
            'C': float(C),
            'sigma_C': float(sigma_C),
            'N_tt': int(N_d),
        })

    data_cos_results = correlation_in_bins(data_h0, data_h1,
                                            data_abs_cos, cos_bins, 5.0)

    # Summary: C_b at the reference working point
    ref_wp = 5.0
    C_ref, sigma_ref, _ = compute_correlation(mc_h0, mc_h1, ref_wp)
    C_data_ref, sigma_data_ref, _ = compute_correlation(data_h0, data_h1, ref_wp)

    log.info("\n--- Summary ---")
    log.info("C_b (MC, WP=%.1f):   %.4f +/- %.4f", ref_wp, C_ref, sigma_ref)
    log.info("C_b (Data, WP=%.1f): %.4f +/- %.4f", ref_wp, C_data_ref, sigma_data_ref)
    log.info("Data-MC difference: %.4f", abs(C_data_ref - C_ref))

    # Published ALEPH C_b for Q-tag: 1.01 (hep-ex/9609005)
    # Our estimate should be in the same ballpark
    log.info("Published ALEPH C_b (Q-tag): 1.01 (hep-ex/9609005)")

    # The systematic on C_b: use the larger of MC statistical uncertainty
    # and data-MC difference, inflated by 2x per STRATEGY.md
    data_mc_diff = abs(C_data_ref - C_ref)
    C_b_syst = 2.0 * max(sigma_ref, data_mc_diff)
    C_b_nominal = C_ref

    log.info("C_b systematic (2x inflation): %.4f", C_b_syst)
    log.info("delta(R_b) from C_b: ~ %.5f", C_b_syst * 0.217 * 0.45)
    # Impact coefficient 0.45 from hep-ex/9609005 Table 1

    output = {
        'mc_vs_wp': wp_results,
        'data_vs_wp': data_wp_results,
        'mc_vs_cos_theta': cos_results,
        'data_vs_cos_theta': data_cos_results,
        'summary': {
            'C_b_nominal': float(C_b_nominal),
            'C_b_stat_mc': float(sigma_ref),
            'C_b_data_mc_diff': float(data_mc_diff),
            'C_b_syst': float(C_b_syst),
            'C_b_data': float(C_data_ref),
            'C_b_data_stat': float(sigma_data_ref),
            'reference_wp': ref_wp,
            'published_aleph': 1.01,
            'published_source': 'hep-ex/9609005 Table 1',
            'inflation_factor': 2.0,
            'inflation_reason': 'Simpler tag, no per-hemisphere vertex [D17]',
        },
    }

    with open(OUT / "correlation_results.json", "w") as f:
        json.dump(output, f, indent=2)
    log.info("\nSaved correlation_results.json")


if __name__ == "__main__":
    main()
