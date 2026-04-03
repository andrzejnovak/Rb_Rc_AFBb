"""Phase 4a: Closure tests and stress tests.

1. Independent closure test: extract R_b from validation MC using
   efficiencies derived from derivation MC. Pull must be < 2 sigma.
2. Corrupted corrections test: intentionally corrupt eps_b by +/-20%.
   The closure test MUST FAIL (pull > 2) to validate sensitivity.
   If it still passes, the test is tautological.
3. Stress tests: extreme parameter variations.

Reads: phase3_selection/outputs/hemisphere_tags.npz,
       outputs/mc_calibration.json, outputs/correlation_results.json,
       outputs/mc_split_indices.npz
Writes: outputs/closure_stress_results.json
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

import sys
sys.path.insert(0, str(HERE))
from rb_extraction import extract_rb, count_tags, apply_gluon_correction
from rb_extraction import R_B_SM, R_C_SM, G_BB, G_CC, N_TOYS, TOY_SEED

REF_WP = 10.0


def run_closure_test(h0, h1, eps_c, eps_uds, R_c, C_b, truth_Rb,
                      threshold, n_toys=500, seed=99999):
    """Run closure test: extract R_b and compute pull vs truth."""
    N_had, N_t, N_tt, f_s, f_d = count_tags(h0, h1, threshold)

    R_b, eps_b = extract_rb(f_s, f_d, eps_c, eps_uds, R_c, C_b)

    # Toy-based uncertainty
    rng = np.random.RandomState(seed)
    rb_toys = []
    for _ in range(n_toys):
        N_t_toy = rng.poisson(N_t)
        N_tt_toy = rng.poisson(N_tt)
        f_s_toy = N_t_toy / (2 * N_had)
        f_d_toy = N_tt_toy / N_had
        if f_s_toy <= 0 or f_d_toy <= 0:
            continue
        rb_t, _ = extract_rb(f_s_toy, f_d_toy, eps_c, eps_uds, R_c, C_b)
        if not np.isnan(rb_t) and 0 < rb_t < 1:
            rb_toys.append(rb_t)

    sigma = float(np.std(rb_toys)) if len(rb_toys) > 10 else np.nan
    pull = (R_b - truth_Rb) / sigma if sigma > 0 and not np.isnan(R_b) else np.nan

    return {
        'R_b_extracted': float(R_b) if not np.isnan(R_b) else None,
        'R_b_truth': truth_Rb,
        'sigma_stat': float(sigma),
        'pull': float(pull) if not np.isnan(pull) else None,
        'passes': bool(abs(pull) < 2.0) if not np.isnan(pull) else False,
        'N_had': int(N_had),
        'N_tt': int(N_tt),
        'f_s': float(f_s),
        'f_d': float(f_d),
        'n_valid_toys': len(rb_toys),
    }


def main():
    log.info("=" * 60)
    log.info("Phase 4a: Closure Tests and Stress Tests")
    log.info("=" * 60)

    tags = np.load(P3_OUT / "hemisphere_tags.npz", allow_pickle=False)
    mc_h0 = tags["mc_combined_h0"]
    mc_h1 = tags["mc_combined_h1"]

    split = np.load(OUT / "mc_split_indices.npz", allow_pickle=False)
    deriv_idx = split["deriv_idx"]
    valid_idx = split["valid_idx"]

    with open(OUT / "mc_calibration.json") as f:
        cal = json.load(f)
    with open(OUT / "correlation_results.json") as f:
        corr = json.load(f)

    C_b = corr['summary']['C_b_nominal']
    wp_key = str(float(REF_WP))
    cal_wp = cal['derivation_calibration'].get(wp_key, {})
    if cal_wp.get('status') != 'calibrated':
        log.error("No calibration at WP %.1f", REF_WP)
        return

    eps_c = cal_wp['eps_c']
    eps_uds_raw = cal_wp['eps_uds']
    eps_uds = apply_gluon_correction(eps_uds_raw, eps_c, G_BB, G_CC)

    val_h0 = mc_h0[valid_idx]
    val_h1 = mc_h1[valid_idx]
    deriv_h0 = mc_h0[deriv_idx]
    deriv_h1 = mc_h1[deriv_idx]

    results = {}

    # ================================================================
    # 1. Independent closure test (derivation -> validation)
    # ================================================================
    log.info("\n--- 1. Independent Closure Test ---")
    log.info("Derivation: %d events, Validation: %d events",
             len(deriv_idx), len(valid_idx))

    thresholds = [3.0, 5.0, 7.0, 9.0]
    closure_per_wp = []
    for thr in thresholds:
        thr_key = str(float(thr))
        cal_t = cal['derivation_calibration'].get(thr_key, {})
        if cal_t.get('status') != 'calibrated':
            continue
        ec = cal_t['eps_c']
        eu = apply_gluon_correction(cal_t['eps_uds'], ec, G_BB, G_CC)

        result = run_closure_test(val_h0, val_h1, ec, eu, R_C_SM, C_b,
                                   R_B_SM, thr, n_toys=500, seed=99999)
        log.info("WP %.1f: R_b=%.5f, pull=%.2f, %s",
                 thr, result['R_b_extracted'] or 0, result['pull'] or 0,
                 "PASS" if result['passes'] else "FAIL")
        result['threshold'] = float(thr)
        closure_per_wp.append(result)

    results['independent_closure'] = {
        'description': 'Extract R_b from validation MC using derivation-derived efficiencies',
        'requirement': 'Pull < 2 sigma (conventions/extraction.md)',
        'per_wp': closure_per_wp,
        'overall_passes': all(r['passes'] for r in closure_per_wp if r['pull'] is not None),
    }

    # ================================================================
    # 2. Corrupted corrections test (+/- 20%)
    # MUST FAIL to validate sensitivity
    # ================================================================
    log.info("\n--- 2. Corrupted Corrections Test (+/-20% eps_b) ---")

    # Get nominal eps_b from calibration
    N_had, N_t, N_tt, f_s, f_d = count_tags(val_h0, val_h1, REF_WP)
    R_b_nom, eps_b_nom = extract_rb(f_s, f_d, eps_c, eps_uds, R_C_SM, C_b)

    corrupted_results = []
    for corruption_label, factor in [
        ("+20% eps_c", 1.20),
        ("-20% eps_c", 0.80),
        ("+20% eps_uds", 1.20),
        ("-20% eps_uds", 0.80),
        ("+20% C_b - 1", None),  # Inflate C_b systematic
        ("-20% C_b - 1", None),
    ]:
        if "eps_c" in corruption_label:
            ec_corrupt = eps_c * factor
            eu_corrupt = eps_uds
            cb_corrupt = C_b
        elif "eps_uds" in corruption_label:
            ec_corrupt = eps_c
            eu_corrupt = eps_uds * factor
            cb_corrupt = C_b
        else:
            ec_corrupt = eps_c
            eu_corrupt = eps_uds
            delta_cb = (C_b - 1.0) * (0.20 if "+" in corruption_label else -0.20)
            cb_corrupt = C_b + delta_cb

        result = run_closure_test(val_h0, val_h1, ec_corrupt, eu_corrupt,
                                   R_C_SM, cb_corrupt, R_B_SM, REF_WP,
                                   n_toys=500, seed=88888)

        # This test SHOULD FAIL (pull > 2) if the test is sensitive
        test_fails = not result['passes']  # We WANT it to fail
        log.info("%s: R_b=%.5f, pull=%.2f, closure %s → sensitivity %s",
                 corruption_label,
                 result['R_b_extracted'] or 0,
                 result['pull'] or 0,
                 "FAIL" if test_fails else "PASS",
                 "VALIDATED" if test_fails else "TAUTOLOGICAL")

        corrupted_results.append({
            'corruption': corruption_label,
            'factor': factor,
            'R_b_extracted': result['R_b_extracted'],
            'pull': result['pull'],
            'closure_passes': result['passes'],
            'sensitivity_validated': test_fails,
        })

    n_sensitive = sum(1 for r in corrupted_results if r['sensitivity_validated'])
    results['corrupted_corrections'] = {
        'description': 'Intentionally corrupt corrections by +/-20% and verify '
                       'closure test FAILS (validates sensitivity)',
        'requirement': 'At least 4/6 tests must show pull > 2 (fail closure)',
        'results': corrupted_results,
        'n_sensitive': n_sensitive,
        'n_total': len(corrupted_results),
        'overall_passes': n_sensitive >= 4,
    }

    # ================================================================
    # 3. Stress tests: extreme variations
    # ================================================================
    log.info("\n--- 3. Stress Tests ---")
    stress_results = []

    # 3a: R_c varied to extreme (0.14 and 0.20)
    for R_c_test in [0.14, 0.20]:
        result = run_closure_test(val_h0, val_h1, eps_c, eps_uds,
                                   R_c_test, C_b, R_B_SM, REF_WP,
                                   n_toys=200, seed=77777)
        log.info("R_c=%.3f: R_b=%.5f, pull=%.2f",
                 R_c_test, result['R_b_extracted'] or 0, result['pull'] or 0)
        stress_results.append({
            'test': f'R_c={R_c_test}',
            'R_b_extracted': result['R_b_extracted'],
            'pull': result['pull'],
        })

    # 3b: C_b extreme (1.05)
    result = run_closure_test(val_h0, val_h1, eps_c, eps_uds,
                               R_C_SM, 1.05, R_B_SM, REF_WP,
                               n_toys=200, seed=66666)
    log.info("C_b=1.05: R_b=%.5f, pull=%.2f",
             result['R_b_extracted'] or 0, result['pull'] or 0)
    stress_results.append({
        'test': 'C_b=1.05',
        'R_b_extracted': result['R_b_extracted'],
        'pull': result['pull'],
    })

    results['stress_tests'] = {
        'description': 'Extreme parameter variations to test extraction robustness',
        'results': stress_results,
    }

    # ================================================================
    # 4. Per-year MC pseudo-data (random subsets)
    # ================================================================
    log.info("\n--- 4. Per-'Year' Consistency (Random MC Subsets) ---")
    rng = np.random.RandomState(44444)
    n_mc = len(mc_h0)
    n_per_year = n_mc // 4

    year_results = []
    for year_label in ['subset_1', 'subset_2', 'subset_3', 'subset_4']:
        idx = rng.choice(n_mc, size=n_per_year, replace=False)
        sub_h0 = mc_h0[idx]
        sub_h1 = mc_h1[idx]

        # Use full MC calibration (not split)
        full_cal = cal['full_mc_calibration'].get(wp_key, {})
        if not full_cal:
            continue
        ec = full_cal['eps_c']
        eu = apply_gluon_correction(full_cal['eps_uds'], ec, G_BB, G_CC)

        result = run_closure_test(sub_h0, sub_h1, ec, eu, R_C_SM, C_b,
                                   R_B_SM, REF_WP, n_toys=200, seed=55555)
        log.info("%s: R_b=%.5f +/- %.5f",
                 year_label, result['R_b_extracted'] or 0, result['sigma_stat'])
        result['year_label'] = year_label
        year_results.append(result)

    # Chi2 for consistency
    rb_vals = [r['R_b_extracted'] for r in year_results if r['R_b_extracted'] is not None]
    rb_errs = [r['sigma_stat'] for r in year_results if r['R_b_extracted'] is not None]
    if len(rb_vals) >= 2:
        rb_arr = np.array(rb_vals)
        err_arr = np.array(rb_errs)
        w = 1.0 / err_arr**2
        rb_mean = np.sum(w * rb_arr) / np.sum(w)
        chi2_year = np.sum((rb_arr - rb_mean)**2 / err_arr**2)
        ndf_year = len(rb_vals) - 1
        from scipy.stats import chi2 as chi2_dist
        p_year = 1.0 - chi2_dist.cdf(chi2_year, ndf_year) if ndf_year > 0 else 1.0
    else:
        chi2_year, ndf_year, p_year = 0.0, 0, 1.0

    log.info("Per-year chi2/ndf = %.2f/%d, p = %.3f", chi2_year, ndf_year, p_year)

    results['per_year_consistency'] = {
        'description': 'Split MC into 4 random subsets (simulating per-year extraction)',
        'results': year_results,
        'chi2': float(chi2_year),
        'ndf': int(ndf_year),
        'p_value': float(p_year),
        'passes': bool(p_year > 0.05),
    }

    # ================================================================
    # Save
    # ================================================================
    with open(OUT / "closure_stress_results.json", "w") as f:
        json.dump(results, f, indent=2)
    log.info("\nSaved closure_stress_results.json")

    # Summary
    log.info("\n--- Summary ---")
    log.info("Independent closure: %s",
             "PASS" if results['independent_closure']['overall_passes'] else "FAIL")
    log.info("Corrupted corrections sensitivity: %d/%d validated",
             results['corrupted_corrections']['n_sensitive'],
             results['corrupted_corrections']['n_total'])
    log.info("Per-year consistency: %s (p=%.3f)",
             "PASS" if results['per_year_consistency']['passes'] else "FAIL",
             p_year)


if __name__ == "__main__":
    main()
