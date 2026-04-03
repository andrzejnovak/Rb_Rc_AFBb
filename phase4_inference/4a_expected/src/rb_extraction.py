"""Phase 4a: R_b extraction from MC pseudo-data with calibrated efficiencies.

Full double-tag R_b extraction using:
1. MC-calibrated eps_c, eps_uds (from mc_efficiency_calibration.py)
2. MC-estimated C_b (from hemisphere_correlation.py)
3. Gluon splitting correction (effective eps_uds)
4. Operating point stability scan
5. Independent closure test (derivation vs validation MC halves)
6. Toy-based statistical uncertainty propagation

Reads: phase3_selection/outputs/hemisphere_tags.npz,
       outputs/mc_calibration.json, outputs/correlation_results.json
Writes: outputs/rb_results.json
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

# SM values for comparison
R_B_SM = 0.21578  # hep-ex/0509008
R_C_SM = 0.17223  # hep-ex/0509008
R_C_ERR = 0.0030  # LEP combined

# Gluon splitting
G_BB = 0.00251
G_BB_ERR = 0.00063
G_CC = 0.0296
G_CC_ERR = 0.0038

N_TOYS = 1000
TOY_SEED = 54321


def extract_rb(f_s, f_d, eps_c, eps_uds, R_c, C_b=1.01, C_c=1.0, C_uds=1.0):
    """Extract R_b and eps_b from double-tag equations.

    Same as Phase 3 but with calibrated inputs.
    """
    R_uds_partial = 1.0 - R_c  # R_uds + R_b = 1 - R_c

    a = f_s - eps_c * R_c - eps_uds * (1.0 - R_c)

    bg_d = C_c * eps_c**2 * R_c + C_uds * eps_uds**2 * (1.0 - R_c)

    rhs_coeff = f_d - bg_d - 2 * C_b * a * eps_uds
    quad_a = (C_b - C_uds) * eps_uds**2
    quad_b = -rhs_coeff
    quad_c = C_b * a**2

    if abs(quad_a) < 1e-15:
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

        candidates = [r for r in [r1, r2] if 0 < r < 1]
        if not candidates:
            candidates = [r for r in [r1, r2] if r > 0]
        if not candidates:
            return np.nan, np.nan
        R_b = min(candidates, key=lambda x: abs(x - R_B_SM))

    if R_b <= 0:
        return np.nan, np.nan

    eps_b = a / R_b + eps_uds
    return float(R_b), float(eps_b)


def count_tags(h0, h1, threshold):
    """Count tags."""
    tagged_h0 = h0 > threshold
    tagged_h1 = h1 > threshold
    N_had = len(h0)
    N_t = int(np.sum(tagged_h0)) + int(np.sum(tagged_h1))
    N_tt = int(np.sum(tagged_h0 & tagged_h1))
    f_s = N_t / (2 * N_had)
    f_d = N_tt / N_had
    return N_had, N_t, N_tt, f_s, f_d


def apply_gluon_correction(eps_uds_direct, eps_c_direct, g_bb, g_cc,
                            eps_g_ratio=0.5, eps_gc_ratio=0.3):
    """Apply gluon splitting correction to effective efficiencies.

    eps_uds(eff) = eps_uds(direct) + g_bb * eps_g + g_cc * eps_gc

    eps_g_ratio = eps_g / eps_b_direct (gluon-splitting b quarks have
    softer kinematics, so lower efficiency)
    eps_gc_ratio = eps_gc / eps_c_direct
    """
    # We don't know eps_g directly. Estimate from eps_b scaled by
    # the softer kinematics of gluon splitting products.
    # At LEP, eps_g ~ 0.5 * eps_b (gluon splitting b quarks are softer).
    # We use this as a ratio to be varied.
    # For the correction, what matters is the effective change to eps_uds:
    eps_uds_eff = eps_uds_direct + g_bb * eps_g_ratio + g_cc * eps_gc_ratio * eps_c_direct
    return eps_uds_eff


def toy_uncertainty(h0, h1, threshold, eps_c, eps_uds, R_c, C_b,
                    n_toys=1000, seed=54321):
    """Toy-based statistical uncertainty propagation.

    Poisson-fluctuate N_t and N_tt, re-extract R_b each time.
    """
    N_had, N_t, N_tt, f_s, f_d = count_tags(h0, h1, threshold)
    rng = np.random.RandomState(seed)

    rb_toys = []
    for _ in range(n_toys):
        N_t_toy = rng.poisson(N_t)
        N_tt_toy = rng.poisson(N_tt)
        f_s_toy = N_t_toy / (2 * N_had)
        f_d_toy = N_tt_toy / N_had
        if f_s_toy <= 0 or f_d_toy <= 0:
            continue
        rb, eb = extract_rb(f_s_toy, f_d_toy, eps_c, eps_uds, R_c, C_b)
        if not np.isnan(rb) and 0 < rb < 1:
            rb_toys.append(rb)

    n_valid_toys = len(rb_toys)
    if n_valid_toys < 10:
        return np.nan, np.nan, [], n_valid_toys

    rb_toys = np.array(rb_toys)
    return float(np.mean(rb_toys)), float(np.std(rb_toys)), rb_toys.tolist(), n_valid_toys


def main():
    log.info("=" * 60)
    log.info("Phase 4a: R_b Extraction from MC Pseudo-Data")
    log.info("=" * 60)

    # Load calibration results
    with open(OUT / "mc_calibration.json") as f:
        cal = json.load(f)

    with open(OUT / "correlation_results.json") as f:
        corr = json.load(f)

    # Use C_b at the operating working point, NOT the reference WP 5.0
    # The summary C_b_nominal is at WP 5.0; we need WP-matched values.
    # Build a lookup from mc_vs_wp for per-WP C_b.
    cb_by_wp = {entry['threshold']: entry['C'] for entry in corr['mc_vs_wp']}
    cb_stat_by_wp = {entry['threshold']: entry['sigma_C'] for entry in corr['mc_vs_wp']}
    # Data-MC difference for systematic: use per-WP if available
    cb_data_by_wp = {entry['threshold']: entry['C'] for entry in corr['data_vs_wp']}

    # Default C_b from summary (WP 5.0) — only as fallback
    C_b_fallback = corr['summary']['C_b_nominal']
    C_b_syst_fallback = corr['summary']['C_b_syst']
    log.info("C_b at WP 5.0 (summary, for reference): %.4f", C_b_fallback)

    # Load tags
    tags = np.load(P3_OUT / "hemisphere_tags.npz", allow_pickle=False)
    mc_h0 = tags["mc_combined_h0"]
    mc_h1 = tags["mc_combined_h1"]

    # Load MC split
    split = np.load(OUT / "mc_split_indices.npz", allow_pickle=False)
    deriv_idx = split["deriv_idx"]
    valid_idx = split["valid_idx"]

    # ================================================================
    # 1. R_b extraction at multiple working points using MC pseudo-data
    # ================================================================
    thresholds = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    full_cal = cal['full_mc_calibration']

    log.info("\n--- R_b Extraction from MC (Full MC as pseudo-data) ---")
    log.info("%-8s  %-10s  %-10s  %-10s  %-10s  %-10s",
             "WP", "R_b", "sigma_stat", "eps_b", "eps_c", "eps_uds")

    extraction_results = []
    for thr in thresholds:
        thr_str = str(float(thr))
        if thr_str not in full_cal:
            continue

        cal_wp = full_cal[thr_str]
        eps_c = cal_wp['eps_c']
        eps_uds = cal_wp['eps_uds']

        # Apply gluon splitting correction
        eps_uds_eff = apply_gluon_correction(eps_uds, eps_c, G_BB, G_CC)

        # Use per-WP C_b (fix for A1: WP mismatch bug)
        C_b_wp = cb_by_wp.get(thr, C_b_fallback)
        C_b_data_wp = cb_data_by_wp.get(thr, C_b_wp)
        C_b_stat_wp = cb_stat_by_wp.get(thr, 0.01)
        # Systematic: 2x data-MC difference (inflated per [D17])
        C_b_syst_wp = 2.0 * abs(C_b_wp - C_b_data_wp)
        log.info("WP %.1f: C_b(MC)=%.4f, C_b(data)=%.4f, syst=%.4f",
                 thr, C_b_wp, C_b_data_wp, C_b_syst_wp)

        # Extract R_b from MC pseudo-data (full MC)
        N_had, N_t, N_tt, f_s, f_d = count_tags(mc_h0, mc_h1, thr)

        R_b, eps_b = extract_rb(f_s, f_d, eps_c, eps_uds_eff, R_C_SM, C_b_wp)

        # Toy-based uncertainty
        rb_mean, rb_sigma, _, n_valid = toy_uncertainty(
            mc_h0, mc_h1, thr, eps_c, eps_uds_eff, R_C_SM, C_b_wp,
            n_toys=N_TOYS, seed=TOY_SEED)

        if not np.isnan(R_b):
            log.info("%-8.1f  %-10.5f  %-10.5f  %-10.4f  %-10.4f  %-10.5f",
                     thr, R_b, rb_sigma, eps_b, eps_c, eps_uds_eff)

        extraction_results.append({
            'threshold': float(thr),
            'R_b': float(R_b) if not np.isnan(R_b) else None,
            'sigma_stat': float(rb_sigma) if not np.isnan(rb_sigma) else None,
            'eps_b': float(eps_b) if not np.isnan(eps_b) else None,
            'eps_c': float(eps_c),
            'eps_uds_direct': float(eps_uds),
            'eps_uds_eff': float(eps_uds_eff),
            'f_s': float(f_s),
            'f_d': float(f_d),
            'N_had': N_had,
            'N_t': N_t,
            'N_tt': N_tt,
            'C_b': float(C_b_wp),
            'C_b_data': float(C_b_data_wp),
            'C_b_syst': float(C_b_syst_wp),
            'n_valid_toys': n_valid,  # ARB-2: report convergence count
        })

    # ================================================================
    # 2. Independent closure test: extract from validation set using
    #    calibration derived from derivation set
    # ================================================================
    log.info("\n--- Independent Closure Test (Validation Set) ---")
    deriv_cal = cal['derivation_calibration']

    closure_results = []
    for thr in thresholds:
        thr_str = str(float(thr))
        if thr_str not in deriv_cal or deriv_cal[thr_str]['status'] != 'calibrated':
            continue

        cal_wp = deriv_cal[thr_str]
        eps_c = cal_wp['eps_c']
        eps_uds = cal_wp['eps_uds']
        eps_uds_eff = apply_gluon_correction(eps_uds, eps_c, G_BB, G_CC)

        # Use per-WP C_b (fix for A1: WP mismatch bug)
        C_b_wp = cb_by_wp.get(thr, C_b_fallback)

        # Extract from validation set
        val_h0 = mc_h0[valid_idx]
        val_h1 = mc_h1[valid_idx]
        N_had, N_t, N_tt, f_s, f_d = count_tags(val_h0, val_h1, thr)

        R_b_val, eps_b_val = extract_rb(f_s, f_d, eps_c, eps_uds_eff, R_C_SM, C_b_wp)

        # Uncertainty from toys on validation set
        rb_mean_val, rb_sigma_val, _, n_valid_val = toy_uncertainty(
            val_h0, val_h1, thr, eps_c, eps_uds_eff, R_C_SM, C_b_wp,
            n_toys=N_TOYS, seed=TOY_SEED + 1)

        # Pull = (extracted - truth) / sigma
        pull = np.nan
        if (not np.isnan(R_b_val) and not np.isnan(rb_sigma_val)
                and rb_sigma_val > 0):
            pull = (R_b_val - R_B_SM) / rb_sigma_val

        closure_results.append({
            'threshold': float(thr),
            'R_b_extracted': float(R_b_val) if not np.isnan(R_b_val) else None,
            'R_b_truth': R_B_SM,
            'sigma_stat': float(rb_sigma_val) if not np.isnan(rb_sigma_val) else None,
            'pull': float(pull) if not np.isnan(pull) else None,
            'passes': bool(abs(pull) < 2.0) if not np.isnan(pull) else False,
            'N_tt': N_tt,
        })

        if not np.isnan(R_b_val):
            log.info("WP %.1f: R_b=%.5f +/- %.5f, pull=%.2f %s",
                     thr, R_b_val, rb_sigma_val, pull,
                     "PASS" if abs(pull) < 2 else "FAIL")

    # ================================================================
    # 3. Select reference working point
    # ================================================================
    # Choose WP with best stat uncertainty and physical R_b
    valid_extractions = [r for r in extraction_results
                         if r['R_b'] is not None and r['sigma_stat'] is not None
                         and 0.1 < r['R_b'] < 0.4]
    if valid_extractions:
        best = min(valid_extractions, key=lambda x: x['sigma_stat'])
        log.info("\n--- Best Working Point ---")
        log.info("WP = %.1f", best['threshold'])
        log.info("R_b = %.5f +/- %.5f (stat)", best['R_b'], best['sigma_stat'])
        log.info("SM R_b = %.5f", R_B_SM)
        log.info("Deviation from SM: %.2f sigma",
                 abs(best['R_b'] - R_B_SM) / best['sigma_stat']
                 if best['sigma_stat'] > 0 else float('inf'))
    else:
        best = None
        log.warning("No valid extraction found!")

    # ================================================================
    # 4. Operating point stability (chi2/ndf)
    # ================================================================
    log.info("\n--- Operating Point Stability ---")
    valid_rb = [r for r in extraction_results
                if r['R_b'] is not None and r['sigma_stat'] is not None
                and r['sigma_stat'] > 0]

    if len(valid_rb) >= 2:
        rb_vals = np.array([r['R_b'] for r in valid_rb])
        rb_errs = np.array([r['sigma_stat'] for r in valid_rb])
        # Weighted mean
        w = 1.0 / rb_errs**2
        rb_combined = np.sum(w * rb_vals) / np.sum(w)
        sigma_combined = 1.0 / np.sqrt(np.sum(w))
        chi2 = np.sum((rb_vals - rb_combined)**2 / rb_errs**2)
        ndf = len(valid_rb) - 1

        from scipy.stats import chi2 as chi2_dist
        p_value = 1.0 - chi2_dist.cdf(chi2, ndf)

        log.info("Combined R_b = %.5f +/- %.5f", rb_combined, sigma_combined)
        log.info("Stability chi2/ndf = %.2f / %d = %.3f, p = %.4f",
                 chi2, ndf, chi2/ndf if ndf > 0 else 0, p_value)
        stability_passes = p_value > 0.05
        log.info("Stability: %s", "PASS" if stability_passes else "FAIL")
    else:
        rb_combined = best['R_b'] if best else np.nan
        sigma_combined = best['sigma_stat'] if best else np.nan
        chi2, ndf, p_value = 0.0, 0, 1.0
        stability_passes = True

    output = {
        'extraction_results': extraction_results,
        'closure_test': closure_results,
        'stability': {
            'R_b_combined': float(rb_combined) if not np.isnan(rb_combined) else None,
            'sigma_combined': float(sigma_combined) if not np.isnan(sigma_combined) else None,
            'chi2': float(chi2),
            'ndf': int(ndf),
            'chi2_ndf': float(chi2/ndf) if ndf > 0 else None,
            'p_value': float(p_value),
            'passes': bool(stability_passes),
        },
        'best_wp': best,
        'sm_values': {
            'R_b': R_B_SM,
            'R_c': R_C_SM,
            'source': 'hep-ex/0509008',
        },
        'gluon_correction': {
            'g_bb': G_BB, 'g_bb_err': G_BB_ERR,
            'g_cc': G_CC, 'g_cc_err': G_CC_ERR,
        },
        'n_toys': N_TOYS,
    }

    with open(OUT / "rb_results.json", "w") as f:
        json.dump(output, f, indent=2)
    log.info("\nSaved rb_results.json")


if __name__ == "__main__":
    main()
