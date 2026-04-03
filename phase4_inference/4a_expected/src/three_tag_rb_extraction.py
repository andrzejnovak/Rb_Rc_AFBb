"""Phase 4a REGRESSION: 3-tag R_b extraction as PRIMARY method.

Implements the 3-tag system (tight/loose/anti-b hemispheres) for R_b
extraction from MC pseudo-data. This replaces the 2-tag system as the
primary method per REGRESSION_TICKET.md.

The 3-tag system defines:
  Tag 1 (tight): combined score > thr_tight  (b-enriched)
  Tag 2 (loose): thr_loose < score <= thr_tight  (b+c enriched)
  Tag 3 (anti):  score <= thr_loose  (uds-enriched)

This provides 3 single-hemisphere and 6 double-tag equations, enabling
simultaneous extraction of R_b, eps_c, eps_uds without external assumptions
about the eps_uds/eps_c ratio.

The anti-tag directly constrains eps_uds from data (finding from 4b
investigation: eps_uds_anti is large and well-measured).

Reads: phase3_selection/outputs/hemisphere_tags.npz
       outputs/mc_calibration.json
       outputs/correlation_results.json
Writes: outputs/three_tag_rb_results.json
"""
import json
import logging
from pathlib import Path

import numpy as np
from scipy.optimize import minimize, minimize_scalar
from scipy.stats import chi2 as chi2_dist
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
OUT.mkdir(parents=True, exist_ok=True)

# SM values — these are the MC truth parameters
# Source: hep-ex/0509008
R_B_SM = 0.21578
R_C_SM = 0.17223
R_UDS_SM = 1.0 - R_B_SM - R_C_SM

# Gluon splitting rates
# Source: LEP average (inspire_416138), world average (hep-ex/0302003)
G_BB = 0.00251
G_BB_ERR = 0.00063
G_CC = 0.0296
G_CC_ERR = 0.0038

N_TOYS = 1000
TOY_SEED = 54321


def assign_hemisphere_tags(h0, h1, thr_tight, thr_loose):
    """Assign each hemisphere to one of three categories.

    Returns per-hemisphere masks (not per-event).
    """
    h0_tight = h0 > thr_tight
    h0_loose = (h0 > thr_loose) & (h0 <= thr_tight)
    h0_anti = h0 <= thr_loose

    h1_tight = h1 > thr_tight
    h1_loose = (h1 > thr_loose) & (h1 <= thr_tight)
    h1_anti = h1 <= thr_loose

    return (h0_tight, h0_loose, h0_anti,
            h1_tight, h1_loose, h1_anti)


def count_three_tag(h0, h1, thr_tight, thr_loose):
    """Count hemisphere-level and double-tag fractions for the 3-tag system."""
    n_events = len(h0)
    (h0_tight, h0_loose, h0_anti,
     h1_tight, h1_loose, h1_anti) = assign_hemisphere_tags(
        h0, h1, thr_tight, thr_loose)

    # Single-hemisphere fractions (average over both hemispheres)
    f_s_tight = (np.sum(h0_tight) + np.sum(h1_tight)) / (2 * n_events)
    f_s_loose = (np.sum(h0_loose) + np.sum(h1_loose)) / (2 * n_events)
    f_s_anti = (np.sum(h0_anti) + np.sum(h1_anti)) / (2 * n_events)

    # Double-tag fractions (6 combinations)
    f_d_tt = np.sum(h0_tight & h1_tight) / n_events
    f_d_ll = np.sum(h0_loose & h1_loose) / n_events
    f_d_aa = np.sum(h0_anti & h1_anti) / n_events
    f_d_tl = np.sum((h0_tight & h1_loose) | (h0_loose & h1_tight)) / n_events
    f_d_ta = np.sum((h0_tight & h1_anti) | (h0_anti & h1_tight)) / n_events
    f_d_la = np.sum((h0_loose & h1_anti) | (h0_anti & h1_loose)) / n_events

    return {
        'n_events': n_events,
        'f_s_tight': float(f_s_tight),
        'f_s_loose': float(f_s_loose),
        'f_s_anti': float(f_s_anti),
        'f_d_tt': float(f_d_tt),
        'f_d_ll': float(f_d_ll),
        'f_d_aa': float(f_d_aa),
        'f_d_tl': float(f_d_tl),
        'f_d_ta': float(f_d_ta),
        'f_d_la': float(f_d_la),
    }


def calibrate_three_tag_efficiencies(counts, R_b, R_c):
    """Calibrate per-tag efficiencies from MC where R_b, R_c are known.

    For each tag category i in {tight, loose, anti}:
      f_s_i = eps_b_i * R_b + eps_c_i * R_c + eps_uds_i * R_uds

    Plus normalization: eps_q_tight + eps_q_loose + eps_q_anti = 1 for each q.

    And double-tag equations:
      f_d_ij = sum_q C_q * eps_q_i * eps_q_j * R_q

    We have 9 unknowns (3 per flavour) minus 3 normalization constraints = 6 free.
    We have 3 single-tag + 6 double-tag = 9 equations (but f_s sums to 1, f_d
    sums to 1, so effectively 2 + 5 = 7 independent). With C_q assumed = 1
    (simplified), this is overconstrained.

    Use chi2 minimization to find the best-fit efficiencies.
    """
    R_uds = 1.0 - R_b - R_c

    # Observables
    obs = np.array([
        counts['f_s_tight'], counts['f_s_loose'],  # f_s_anti follows
        counts['f_d_tt'], counts['f_d_ll'], counts['f_d_aa'],
        counts['f_d_tl'], counts['f_d_ta'], counts['f_d_la'],
    ])

    n_events = counts['n_events']
    # Uncertainties: Poisson-like for fractions
    sigma = np.array([
        np.sqrt(obs[0] * (1 - obs[0]) / (2 * n_events)),  # f_s_tight
        np.sqrt(obs[1] * (1 - obs[1]) / (2 * n_events)),  # f_s_loose
        np.sqrt(max(obs[2], 1e-8) / n_events),  # f_d_tt
        np.sqrt(max(obs[3], 1e-8) / n_events),  # f_d_ll
        np.sqrt(max(obs[4], 1e-8) / n_events),  # f_d_aa
        np.sqrt(max(obs[5], 1e-8) / n_events),  # f_d_tl
        np.sqrt(max(obs[6], 1e-8) / n_events),  # f_d_ta
        np.sqrt(max(obs[7], 1e-8) / n_events),  # f_d_la
    ])
    sigma = np.maximum(sigma, 1e-8)

    def chi2_func(params):
        eps_b_tight, eps_b_loose, eps_c_tight, eps_c_loose, \
            eps_uds_tight, eps_uds_loose = params

        eps_b_anti = 1.0 - eps_b_tight - eps_b_loose
        eps_c_anti = 1.0 - eps_c_tight - eps_c_loose
        eps_uds_anti = 1.0 - eps_uds_tight - eps_uds_loose

        # Check physicality
        for e in [eps_b_tight, eps_b_loose, eps_b_anti,
                  eps_c_tight, eps_c_loose, eps_c_anti,
                  eps_uds_tight, eps_uds_loose, eps_uds_anti]:
            if e < 0 or e > 1:
                return 1e10

        # Predicted single-tag fractions
        f_s_tight_pred = eps_b_tight * R_b + eps_c_tight * R_c + eps_uds_tight * R_uds
        f_s_loose_pred = eps_b_loose * R_b + eps_c_loose * R_c + eps_uds_loose * R_uds

        # Predicted double-tag fractions (assuming C_q = 1)
        f_d_tt_pred = eps_b_tight**2 * R_b + eps_c_tight**2 * R_c + eps_uds_tight**2 * R_uds
        f_d_ll_pred = eps_b_loose**2 * R_b + eps_c_loose**2 * R_c + eps_uds_loose**2 * R_uds
        f_d_aa_pred = eps_b_anti**2 * R_b + eps_c_anti**2 * R_c + eps_uds_anti**2 * R_uds
        f_d_tl_pred = 2 * (eps_b_tight * eps_b_loose * R_b +
                           eps_c_tight * eps_c_loose * R_c +
                           eps_uds_tight * eps_uds_loose * R_uds)
        f_d_ta_pred = 2 * (eps_b_tight * eps_b_anti * R_b +
                           eps_c_tight * eps_c_anti * R_c +
                           eps_uds_tight * eps_uds_anti * R_uds)
        f_d_la_pred = 2 * (eps_b_loose * eps_b_anti * R_b +
                           eps_c_loose * eps_c_anti * R_c +
                           eps_uds_loose * eps_uds_anti * R_uds)

        pred = np.array([f_s_tight_pred, f_s_loose_pred,
                         f_d_tt_pred, f_d_ll_pred, f_d_aa_pred,
                         f_d_tl_pred, f_d_ta_pred, f_d_la_pred])

        return np.sum(((obs - pred) / sigma) ** 2)

    # Initial guess from 2-tag calibration or reasonable values
    x0 = [0.20, 0.30, 0.15, 0.35, 0.05, 0.20]
    bounds = [(0.001, 0.99)] * 6

    result = minimize(chi2_func, x0, method='L-BFGS-B', bounds=bounds)

    if not result.success:
        # Try multiple starting points
        best = result
        for trial in range(20):
            rng = np.random.RandomState(42 + trial)
            x0_trial = rng.uniform(0.01, 0.5, 6)
            res = minimize(chi2_func, x0_trial, method='L-BFGS-B', bounds=bounds)
            if res.fun < best.fun:
                best = res
        result = best

    eps_b_tight, eps_b_loose, eps_c_tight, eps_c_loose, \
        eps_uds_tight, eps_uds_loose = result.x

    calibration = {
        'eps_b_tight': float(eps_b_tight),
        'eps_b_loose': float(eps_b_loose),
        'eps_b_anti': float(1.0 - eps_b_tight - eps_b_loose),
        'eps_c_tight': float(eps_c_tight),
        'eps_c_loose': float(eps_c_loose),
        'eps_c_anti': float(1.0 - eps_c_tight - eps_c_loose),
        'eps_uds_tight': float(eps_uds_tight),
        'eps_uds_loose': float(eps_uds_loose),
        'eps_uds_anti': float(1.0 - eps_uds_tight - eps_uds_loose),
        'chi2_calibration': float(result.fun),
        'ndf_calibration': len(obs) - 6,
        'converged': bool(result.success),
    }

    return calibration


def extract_rb_three_tag(counts_data, calibration, R_c,
                          C_b_tight=1.0, C_b_loose=1.0, C_b_anti=1.0):
    """Extract R_b from data using 3-tag system with calibrated efficiencies.

    Given MC-calibrated efficiencies and data tag fractions, fit for R_b.

    The single-hemisphere fraction at each tag level:
      f_s_i(R_b) = eps_b_i * R_b + eps_c_i * R_c + eps_uds_i * (1 - R_b - R_c)
                 = (eps_b_i - eps_uds_i) * R_b + eps_c_i * R_c + eps_uds_i * (1 - R_c)

    This is linear in R_b! So we can solve analytically or use chi2.
    With double-tag fractions, we get more constraints (quadratic in eps_b).
    """
    cal = calibration
    R_uds_base = 1.0 - R_c  # R_b + R_uds = 1 - R_c

    n_events = counts_data['n_events']

    # Build the chi2 as a function of R_b
    def chi2_func(R_b_fit):
        R_uds_fit = 1.0 - R_b_fit - R_c

        # Predicted single-hemisphere fractions
        f_s_tight_pred = (cal['eps_b_tight'] * R_b_fit +
                          cal['eps_c_tight'] * R_c +
                          cal['eps_uds_tight'] * R_uds_fit)
        f_s_loose_pred = (cal['eps_b_loose'] * R_b_fit +
                          cal['eps_c_loose'] * R_c +
                          cal['eps_uds_loose'] * R_uds_fit)

        # Predicted double-tag fractions
        # Using per-tag correlations (C_b_tight for tight-tight, etc.)
        f_d_tt_pred = (C_b_tight * cal['eps_b_tight']**2 * R_b_fit +
                       cal['eps_c_tight']**2 * R_c +
                       cal['eps_uds_tight']**2 * R_uds_fit)
        f_d_ll_pred = (C_b_loose * cal['eps_b_loose']**2 * R_b_fit +
                       cal['eps_c_loose']**2 * R_c +
                       cal['eps_uds_loose']**2 * R_uds_fit)
        f_d_aa_pred = (C_b_anti * cal['eps_b_anti']**2 * R_b_fit +
                       cal['eps_c_anti']**2 * R_c +
                       cal['eps_uds_anti']**2 * R_uds_fit)

        # Mixed double-tags: geometric mean of correlation factors
        C_tl = np.sqrt(C_b_tight * C_b_loose)
        C_ta = np.sqrt(C_b_tight * C_b_anti)
        C_la = np.sqrt(C_b_loose * C_b_anti)

        f_d_tl_pred = 2 * (C_tl * cal['eps_b_tight'] * cal['eps_b_loose'] * R_b_fit +
                           cal['eps_c_tight'] * cal['eps_c_loose'] * R_c +
                           cal['eps_uds_tight'] * cal['eps_uds_loose'] * R_uds_fit)
        f_d_ta_pred = 2 * (C_ta * cal['eps_b_tight'] * cal['eps_b_anti'] * R_b_fit +
                           cal['eps_c_tight'] * cal['eps_c_anti'] * R_c +
                           cal['eps_uds_tight'] * cal['eps_uds_anti'] * R_uds_fit)
        f_d_la_pred = 2 * (C_la * cal['eps_b_loose'] * cal['eps_b_anti'] * R_b_fit +
                           cal['eps_c_loose'] * cal['eps_c_anti'] * R_c +
                           cal['eps_uds_loose'] * cal['eps_uds_anti'] * R_uds_fit)

        # Observed
        obs = np.array([
            counts_data['f_s_tight'], counts_data['f_s_loose'],
            counts_data['f_d_tt'], counts_data['f_d_ll'], counts_data['f_d_aa'],
            counts_data['f_d_tl'], counts_data['f_d_ta'], counts_data['f_d_la'],
        ])
        pred = np.array([
            f_s_tight_pred, f_s_loose_pred,
            f_d_tt_pred, f_d_ll_pred, f_d_aa_pred,
            f_d_tl_pred, f_d_ta_pred, f_d_la_pred,
        ])

        # Uncertainties from data statistics
        sigma = np.array([
            np.sqrt(max(obs[0] * (1 - obs[0]) / (2 * n_events), 1e-12)),
            np.sqrt(max(obs[1] * (1 - obs[1]) / (2 * n_events), 1e-12)),
            np.sqrt(max(obs[2], 1e-8) / n_events),
            np.sqrt(max(obs[3], 1e-8) / n_events),
            np.sqrt(max(obs[4], 1e-8) / n_events),
            np.sqrt(max(obs[5], 1e-8) / n_events),
            np.sqrt(max(obs[6], 1e-8) / n_events),
            np.sqrt(max(obs[7], 1e-8) / n_events),
        ])

        return float(np.sum(((obs - pred) / sigma) ** 2))

    result = minimize_scalar(chi2_func, bounds=(0.10, 0.40), method='bounded')
    R_b_fit = result.x
    chi2_min = result.fun
    ndf = 8 - 1  # 8 observables, 1 parameter

    p_value = 1.0 - chi2_dist.cdf(chi2_min, ndf)

    return {
        'R_b': float(R_b_fit),
        'chi2': float(chi2_min),
        'ndf': int(ndf),
        'chi2_ndf': float(chi2_min / ndf) if ndf > 0 else None,
        'p_value': float(p_value),
    }


def toy_uncertainty_three_tag(h0, h1, thr_tight, thr_loose,
                               calibration, R_c, n_toys=1000, seed=54321):
    """Toy-based statistical uncertainty for 3-tag R_b extraction.

    Poisson-fluctuate the tag counts and re-extract R_b each time.
    """
    counts_nominal = count_three_tag(h0, h1, thr_tight, thr_loose)
    n_events = counts_nominal['n_events']

    # Convert fractions to counts for Poisson fluctuation
    # Single-tag counts (per hemisphere)
    n_h_tight = int(counts_nominal['f_s_tight'] * 2 * n_events)
    n_h_loose = int(counts_nominal['f_s_loose'] * 2 * n_events)
    # Double-tag counts
    n_d_tt = int(counts_nominal['f_d_tt'] * n_events)
    n_d_ll = int(counts_nominal['f_d_ll'] * n_events)
    n_d_aa = int(counts_nominal['f_d_aa'] * n_events)
    n_d_tl = int(counts_nominal['f_d_tl'] * n_events)
    n_d_ta = int(counts_nominal['f_d_ta'] * n_events)
    n_d_la = int(counts_nominal['f_d_la'] * n_events)

    rng = np.random.RandomState(seed)
    rb_toys = []

    for _ in range(n_toys):
        # Poisson-fluctuate
        toy_counts = {
            'n_events': n_events,
            'f_s_tight': rng.poisson(n_h_tight) / (2 * n_events),
            'f_s_loose': rng.poisson(n_h_loose) / (2 * n_events),
            'f_s_anti': None,  # Derived
            'f_d_tt': rng.poisson(n_d_tt) / n_events,
            'f_d_ll': rng.poisson(n_d_ll) / n_events,
            'f_d_aa': rng.poisson(n_d_aa) / n_events,
            'f_d_tl': rng.poisson(n_d_tl) / n_events,
            'f_d_ta': rng.poisson(n_d_ta) / n_events,
            'f_d_la': rng.poisson(n_d_la) / n_events,
        }
        toy_counts['f_s_anti'] = 1.0 - toy_counts['f_s_tight'] - toy_counts['f_s_loose']

        try:
            result = extract_rb_three_tag(toy_counts, calibration, R_c)
            rb = result['R_b']
            if 0.05 < rb < 0.50:
                rb_toys.append(rb)
        except Exception:
            continue

    n_valid = len(rb_toys)
    if n_valid < 10:
        return np.nan, np.nan, [], n_valid

    rb_arr = np.array(rb_toys)
    return float(np.mean(rb_arr)), float(np.std(rb_arr)), rb_arr.tolist(), n_valid


def main():
    log.info("=" * 60)
    log.info("Phase 4a REGRESSION: 3-Tag R_b Extraction (PRIMARY)")
    log.info("=" * 60)

    # Load Phase 3 MC tags
    tags = np.load(P3_OUT / "hemisphere_tags.npz", allow_pickle=False)
    mc_h0 = tags["mc_combined_h0"]
    mc_h1 = tags["mc_combined_h1"]
    n_mc = len(mc_h0)
    log.info("MC events: %d", n_mc)

    # Load per-WP C_b from correlation results
    corr_path = OUT / "correlation_results.json"
    if corr_path.exists():
        with open(corr_path) as f:
            corr = json.load(f)
        cb_by_wp = {entry['threshold']: entry['C']
                    for entry in corr['mc_vs_wp']}
        cb_data_by_wp = {entry['threshold']: entry['C']
                         for entry in corr['data_vs_wp']}
    else:
        cb_by_wp = {}
        cb_data_by_wp = {}
        log.warning("No correlation_results.json found")

    # Split MC for independent closure test
    SPLIT_SEED = 12345
    rng = np.random.RandomState(SPLIT_SEED)
    indices = np.arange(n_mc)
    rng.shuffle(indices)
    n_deriv = int(0.6 * n_mc)
    deriv_idx = indices[:n_deriv]
    valid_idx = indices[n_deriv:]

    # ================================================================
    # 1. Threshold scan: find optimal tight/loose thresholds
    # ================================================================
    log.info("\n--- Threshold Scan ---")
    threshold_configs = [
        (10.0, 5.0), (10.0, 3.0), (8.0, 4.0), (8.0, 3.0),
        (12.0, 6.0), (7.0, 3.0), (9.0, 4.0), (9.0, 5.0),
    ]

    scan_results = []

    for thr_tight, thr_loose in threshold_configs:
        label = f"tight={thr_tight:.0f}, loose={thr_loose:.0f}"

        # Calibrate efficiencies from derivation MC
        counts_deriv = count_three_tag(
            mc_h0[deriv_idx], mc_h1[deriv_idx], thr_tight, thr_loose)
        calibration = calibrate_three_tag_efficiencies(
            counts_deriv, R_B_SM, R_C_SM)

        # Extract R_b from validation MC (independent)
        counts_valid = count_three_tag(
            mc_h0[valid_idx], mc_h1[valid_idx], thr_tight, thr_loose)
        extraction = extract_rb_three_tag(
            counts_valid, calibration, R_C_SM)

        log.info("%s: R_b=%.5f, chi2/ndf=%.2f/%d, p=%.3f | "
                 "eps_b_t=%.3f, eps_c_t=%.3f, eps_uds_t=%.4f",
                 label, extraction['R_b'],
                 extraction['chi2'], extraction['ndf'], extraction['p_value'],
                 calibration['eps_b_tight'], calibration['eps_c_tight'],
                 calibration['eps_uds_tight'])

        scan_results.append({
            'thr_tight': float(thr_tight),
            'thr_loose': float(thr_loose),
            'label': label,
            'calibration': calibration,
            'extraction': extraction,
        })

    # ================================================================
    # 2. Full MC extraction at each config (with toys)
    # ================================================================
    log.info("\n--- Full MC Extraction with Toy Uncertainties ---")

    # Calibrate from full MC
    full_results = []
    for thr_tight, thr_loose in threshold_configs:
        label = f"tight={thr_tight:.0f}, loose={thr_loose:.0f}"
        counts_full = count_three_tag(mc_h0, mc_h1, thr_tight, thr_loose)
        calibration = calibrate_three_tag_efficiencies(
            counts_full, R_B_SM, R_C_SM)

        # Extract from full MC as pseudo-data
        extraction = extract_rb_three_tag(counts_full, calibration, R_C_SM)

        # Toy-based uncertainty
        rb_mean, rb_sigma, rb_toys, n_valid = toy_uncertainty_three_tag(
            mc_h0, mc_h1, thr_tight, thr_loose,
            calibration, R_C_SM, n_toys=N_TOYS, seed=TOY_SEED)

        log.info("%s: R_b=%.5f +/- %.5f (toys=%d/%d)",
                 label, extraction['R_b'], rb_sigma, n_valid, N_TOYS)

        full_results.append({
            'thr_tight': float(thr_tight),
            'thr_loose': float(thr_loose),
            'label': label,
            'counts': counts_full,
            'calibration': calibration,
            'R_b': extraction['R_b'],
            'chi2': extraction['chi2'],
            'ndf': extraction['ndf'],
            'p_value': extraction['p_value'],
            'R_b_toy_mean': float(rb_mean) if not np.isnan(rb_mean) else None,
            'sigma_stat': float(rb_sigma) if not np.isnan(rb_sigma) else None,
            'n_valid_toys': n_valid,
        })

    # ================================================================
    # 3. Select best configuration (minimum stat uncertainty)
    # ================================================================
    valid_results = [r for r in full_results
                     if r['sigma_stat'] is not None and r['sigma_stat'] > 0
                     and 0.1 < r['R_b'] < 0.4]

    if valid_results:
        best = min(valid_results, key=lambda x: x['sigma_stat'])
        log.info("\n--- Best Configuration ---")
        log.info("Config: %s", best['label'])
        log.info("R_b = %.5f +/- %.5f (stat)", best['R_b'], best['sigma_stat'])
        log.info("SM R_b = %.5f", R_B_SM)
        log.info("Pull = %.2f",
                 abs(best['R_b'] - R_B_SM) / best['sigma_stat'])
    else:
        best = None
        log.warning("No valid extraction found!")

    # ================================================================
    # 4. Operating point stability (chi2/ndf across configs)
    # ================================================================
    log.info("\n--- Operating Point Stability ---")
    stable = [r for r in full_results
              if r['sigma_stat'] is not None and r['sigma_stat'] > 0
              and 0.1 < r['R_b'] < 0.4]

    if len(stable) >= 2:
        rb_vals = np.array([r['R_b'] for r in stable])
        rb_errs = np.array([r['sigma_stat'] for r in stable])
        w = 1.0 / rb_errs**2
        rb_combined = np.sum(w * rb_vals) / np.sum(w)
        sigma_combined = 1.0 / np.sqrt(np.sum(w))
        chi2_stab = np.sum((rb_vals - rb_combined)**2 / rb_errs**2)
        ndf_stab = len(stable) - 1
        p_stab = 1.0 - chi2_dist.cdf(chi2_stab, ndf_stab)

        log.info("Combined R_b = %.5f +/- %.5f", rb_combined, sigma_combined)
        log.info("Stability chi2/ndf = %.2f/%d = %.3f, p = %.4f",
                 chi2_stab, ndf_stab, chi2_stab / ndf_stab, p_stab)
        stability_passes = p_stab > 0.05
    else:
        rb_combined = best['R_b'] if best else np.nan
        sigma_combined = best['sigma_stat'] if best else np.nan
        chi2_stab, ndf_stab, p_stab = 0.0, 0, 1.0
        stability_passes = True

    # ================================================================
    # 5. Independent closure test (derivation -> validation)
    # ================================================================
    log.info("\n--- Independent Closure Test ---")
    closure_results = []
    for thr_tight, thr_loose in threshold_configs[:4]:
        label = f"tight={thr_tight:.0f}, loose={thr_loose:.0f}"

        # Calibrate from derivation set
        counts_deriv = count_three_tag(
            mc_h0[deriv_idx], mc_h1[deriv_idx], thr_tight, thr_loose)
        cal = calibrate_three_tag_efficiencies(counts_deriv, R_B_SM, R_C_SM)

        # Extract from validation set
        counts_valid = count_three_tag(
            mc_h0[valid_idx], mc_h1[valid_idx], thr_tight, thr_loose)
        ext = extract_rb_three_tag(counts_valid, cal, R_C_SM)

        # Toy uncertainty on validation set
        rb_mean, rb_sigma, _, n_valid = toy_uncertainty_three_tag(
            mc_h0[valid_idx], mc_h1[valid_idx], thr_tight, thr_loose,
            cal, R_C_SM, n_toys=N_TOYS, seed=TOY_SEED + 1)

        pull = np.nan
        if not np.isnan(rb_sigma) and rb_sigma > 0:
            pull = (ext['R_b'] - R_B_SM) / rb_sigma

        passes = bool(abs(pull) < 2.0) if not np.isnan(pull) else False
        log.info("%s: R_b=%.5f +/- %.5f, pull=%.2f %s",
                 label, ext['R_b'], rb_sigma, pull,
                 "PASS" if passes else "FAIL")

        closure_results.append({
            'label': label,
            'R_b': ext['R_b'],
            'R_b_truth': R_B_SM,
            'sigma_stat': float(rb_sigma) if not np.isnan(rb_sigma) else None,
            'pull': float(pull) if not np.isnan(pull) else None,
            'passes': passes,
        })

    # ================================================================
    # 6. eps_uds constraint from anti-tag
    # ================================================================
    log.info("\n--- eps_uds Constraint from Anti-Tag ---")
    # The anti-tag (low score) is enriched in uds events.
    # From the calibrated efficiencies, eps_uds_anti is directly measured.
    if best:
        best_cal = best['calibration']
        eps_uds_anti = best_cal['eps_uds_anti']
        eps_uds_tight = best_cal['eps_uds_tight']
        eps_uds_loose = best_cal['eps_uds_loose']
        log.info("eps_uds_tight = %.5f, eps_uds_loose = %.5f, eps_uds_anti = %.5f",
                 eps_uds_tight, eps_uds_loose, eps_uds_anti)
        log.info("Anti-tag provides: eps_uds_anti = %.5f (constrained from 3-tag fit)",
                 eps_uds_anti)

        # The constraint: from the anti-tag fraction in data,
        # eps_uds_anti * R_uds should dominate f_s_anti.
        f_anti = best['counts']['f_s_anti']
        uds_fraction_anti = eps_uds_anti * R_UDS_SM / f_anti
        log.info("uds purity in anti-tag: %.3f", uds_fraction_anti)

    # ================================================================
    # Output
    # ================================================================
    output = {
        'method': '3-tag system (tight/loose/anti-b)',
        'description': (
            'R_b extraction using the 3-tag system as PRIMARY method. '
            'Defines tight (b-enriched), loose (b+c), and anti (uds-enriched) '
            'hemisphere categories. The system provides 8 observables '
            '(3 single + 6 double - 1 normalization) to constrain R_b. '
            'The anti-tag directly constrains eps_uds from data.'
        ),
        'threshold_scan': scan_results,
        'full_mc_results': full_results,
        'best_config': best,
        'stability': {
            'R_b_combined': float(rb_combined) if not np.isnan(rb_combined) else None,
            'sigma_combined': float(sigma_combined) if not np.isnan(sigma_combined) else None,
            'chi2': float(chi2_stab),
            'ndf': int(ndf_stab),
            'chi2_ndf': float(chi2_stab / ndf_stab) if ndf_stab > 0 else None,
            'p_value': float(p_stab),
            'passes': bool(stability_passes),
            'n_configs': len(stable),
        },
        'closure_test': closure_results,
        'sm_values': {
            'R_b': R_B_SM,
            'R_c': R_C_SM,
            'source': 'hep-ex/0509008',
        },
        'n_toys': N_TOYS,
    }

    with open(OUT / "three_tag_rb_results.json", "w") as f:
        json.dump(output, f, indent=2, default=str)
    log.info("\nSaved three_tag_rb_results.json")


if __name__ == "__main__":
    main()
