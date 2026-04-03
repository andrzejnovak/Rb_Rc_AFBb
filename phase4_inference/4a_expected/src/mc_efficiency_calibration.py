"""Phase 4a: MC efficiency calibration for double-tag R_b extraction.

Calibrates eps_b, eps_c, eps_uds from MC pseudo-data at multiple working
points. Since we have no MC truth labels [A1], we use the SM values of
R_b and R_c as the known MC truth (the MC was generated with SM parameters)
to solve for the per-WP efficiencies from the observed f_s and f_d.

This is NOT circular: we derive efficiencies from MC (where SM is truth),
then apply them to data (where R_b is unknown) via the double-tag method.
The self-calibrating property of the double-tag method means eps_b is
extracted from data; eps_c and eps_uds are the MC-derived inputs.

Also splits MC into derivation (60%) and validation (40%) halves for
independent closure test (conventions/extraction.md requirement).

Reads: phase3_selection/outputs/hemisphere_tags.npz,
       phase3_selection/outputs/preselected_mc.npz
Writes: outputs/mc_calibration.json, outputs/mc_split_tags.npz
"""
import json
import logging
import sys
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
OUT.mkdir(parents=True, exist_ok=True)

# SM values — these are the MC truth parameters
# Source: hep-ex/0509008
R_B_SM = 0.21578
R_C_SM = 0.17223

# Gluon splitting rates
# Source: LEP average (inspire_416138), world average (hep-ex/0302003)
G_BB = 0.00251  # g_bb = 0.251%
G_CC = 0.0296   # g_cc = 2.96%

# Hemisphere correlations (nominal)
# C_B is now loaded per-WP from correlation_results.json (fix for A1 WP mismatch)
C_B_PUBLISHED = 1.01  # ALEPH published value (used as fallback)
C_C = 1.00
C_UDS = 1.00

SPLIT_SEED = 12345  # Fixed seed for MC split (documented, reproducible)


def count_tags_from_arrays(h0, h1, threshold):
    """Count single-tag and double-tag fractions."""
    tagged_h0 = h0 > threshold
    tagged_h1 = h1 > threshold
    N_had = len(h0)
    N_t = int(np.sum(tagged_h0)) + int(np.sum(tagged_h1))
    N_tt = int(np.sum(tagged_h0 & tagged_h1))
    f_s = N_t / (2 * N_had) if N_had > 0 else 0.0
    f_d = N_tt / N_had if N_had > 0 else 0.0
    return N_had, N_t, N_tt, f_s, f_d


def calibrate_efficiencies(f_s, f_d, R_b, R_c, C_b=1.01, C_c=1.0, C_uds=1.0):
    """Derive eps_b, eps_c, eps_uds from observed fractions + known R_b, R_c.

    This inverts the double-tag equations assuming we KNOW R_b and R_c (MC truth).
    The system is underdetermined (3 unknowns from 2 equations), so we solve
    for eps_b from the quadratic and estimate eps_c/eps_uds from their ratio.

    Strategy: use the double-tag equations directly.
    f_s = eps_b * R_b + eps_c * R_c + eps_uds * (1 - R_b - R_c)
    f_d = C_b * eps_b^2 * R_b + C_c * eps_c^2 * R_c + C_uds * eps_uds^2 * (1-R_b-R_c)

    With 3 unknowns and 2 equations, we need one constraint.
    Use: eps_uds = alpha * eps_c where alpha = eps_uds/eps_c is the
    light-to-charm efficiency ratio. From MC studies at LEP, typically
    alpha ~ 0.05-0.15 (light flavours are much less likely to fake a b-tag
    than charm). We scan alpha and find the value that gives consistent
    extraction.

    Alternative: directly solve for eps_b given f_s and f_d with the
    constraint eps_c = beta * eps_b (charm-to-b efficiency ratio).
    At each WP, beta varies but is typically 0.05-0.30.
    """
    # Approach: Scan eps_c values and for each, solve for eps_b and eps_uds
    R_uds = 1.0 - R_b - R_c

    best_result = None
    best_consistency = float('inf')

    for eps_c_trial in np.linspace(0.001, 0.6, 600):
        for alpha in [0.01, 0.03, 0.05, 0.10, 0.15, 0.20]:
            eps_uds_trial = alpha * eps_c_trial

            # From f_s equation:
            # eps_b = (f_s - eps_c * R_c - eps_uds * R_uds) / R_b
            eps_b_from_fs = (f_s - eps_c_trial * R_c - eps_uds_trial * R_uds) / R_b

            if eps_b_from_fs <= 0 or eps_b_from_fs > 1.0:
                continue

            # Check f_d consistency
            f_d_pred = (C_b * eps_b_from_fs**2 * R_b
                       + C_c * eps_c_trial**2 * R_c
                       + C_uds * eps_uds_trial**2 * R_uds)

            consistency = abs(f_d_pred - f_d) / max(f_d, 1e-10)

            if consistency < best_consistency:
                best_consistency = consistency
                best_result = {
                    'eps_b': eps_b_from_fs,
                    'eps_c': eps_c_trial,
                    'eps_uds': eps_uds_trial,
                    'alpha': alpha,
                    'f_d_pred': f_d_pred,
                    'f_d_obs': f_d,
                    'consistency': consistency,
                }

    return best_result


def calibrate_efficiencies_quadratic(f_s, f_d, R_b, R_c,
                                      C_b=1.01, C_c=1.0, C_uds=1.0):
    """More robust calibration using analytical quadratic solution.

    Fix eps_uds/eps_c ratio from physics (light quarks fake b-tags much
    less than charm), then solve the 2-equation system exactly.
    """
    R_uds = 1.0 - R_b - R_c
    results = []

    for alpha in np.linspace(0.01, 0.30, 30):
        # eps_uds = alpha * eps_c
        # f_s = eps_b * R_b + eps_c * R_c + alpha * eps_c * R_uds
        #      = eps_b * R_b + eps_c * (R_c + alpha * R_uds)
        # f_d = C_b * eps_b^2 * R_b + C_c * eps_c^2 * R_c + C_uds * alpha^2 * eps_c^2 * R_uds
        #      = C_b * eps_b^2 * R_b + eps_c^2 * (C_c * R_c + C_uds * alpha^2 * R_uds)

        A_coeff = R_c + alpha * R_uds  # coefficient of eps_c in f_s
        B_coeff = C_c * R_c + C_uds * alpha**2 * R_uds  # coefficient of eps_c^2 in f_d

        # eps_b = (f_s - eps_c * A_coeff) / R_b
        # Substitute into f_d:
        # C_b * ((f_s - eps_c * A_coeff) / R_b)^2 * R_b + eps_c^2 * B_coeff = f_d
        # C_b * (f_s - eps_c * A_coeff)^2 / R_b + eps_c^2 * B_coeff = f_d

        # Let x = eps_c
        # C_b/R_b * (f_s^2 - 2*f_s*x*A + x^2*A^2) + x^2*B = f_d
        # x^2 * (C_b*A^2/R_b + B) - x * 2*C_b*f_s*A/R_b + C_b*f_s^2/R_b - f_d = 0

        qa = C_b * A_coeff**2 / R_b + B_coeff
        qb = -2 * C_b * f_s * A_coeff / R_b
        qc = C_b * f_s**2 / R_b - f_d

        disc = qb**2 - 4 * qa * qc
        if disc < 0:
            continue

        sqrt_disc = np.sqrt(disc)
        x1 = (-qb + sqrt_disc) / (2 * qa)
        x2 = (-qb - sqrt_disc) / (2 * qa)

        for eps_c_sol in [x1, x2]:
            if eps_c_sol <= 0 or eps_c_sol > 0.8:
                continue
            eps_uds_sol = alpha * eps_c_sol
            eps_b_sol = (f_s - eps_c_sol * A_coeff) / R_b

            if eps_b_sol <= 0 or eps_b_sol > 1.0:
                continue

            # Verify
            f_s_check = eps_b_sol * R_b + eps_c_sol * R_c + eps_uds_sol * R_uds
            f_d_check = (C_b * eps_b_sol**2 * R_b
                        + C_c * eps_c_sol**2 * R_c
                        + C_uds * eps_uds_sol**2 * R_uds)

            results.append({
                'eps_b': float(eps_b_sol),
                'eps_c': float(eps_c_sol),
                'eps_uds': float(eps_uds_sol),
                'alpha': float(alpha),
                'f_s_check': float(f_s_check),
                'f_d_check': float(f_d_check),
                'f_s_residual': float(abs(f_s_check - f_s)),
                'f_d_residual': float(abs(f_d_check - f_d)),
            })

    return results


def main():
    log.info("=" * 60)
    log.info("Phase 4a: MC Efficiency Calibration")
    log.info("=" * 60)

    # Load Phase 3 MC tags
    tags = np.load(P3_OUT / "hemisphere_tags.npz", allow_pickle=False)
    mc_h0 = tags["mc_combined_h0"]
    mc_h1 = tags["mc_combined_h1"]
    n_mc = len(mc_h0)
    log.info("MC events: %d", n_mc)

    # Split MC into derivation (60%) and validation (40%)
    rng = np.random.RandomState(SPLIT_SEED)
    indices = np.arange(n_mc)
    rng.shuffle(indices)
    n_deriv = int(0.6 * n_mc)
    deriv_idx = indices[:n_deriv]
    valid_idx = indices[n_deriv:]

    log.info("Derivation set: %d events", len(deriv_idx))
    log.info("Validation set: %d events", len(valid_idx))

    # Save split indices for downstream use
    np.savez_compressed(
        OUT / "mc_split_indices.npz",
        deriv_idx=deriv_idx,
        valid_idx=valid_idx,
        split_seed=SPLIT_SEED,
    )

    # Load per-WP C_b from correlation results (fix A1: WP mismatch)
    corr_path = OUT / "correlation_results.json"
    if corr_path.exists():
        with open(corr_path) as f:
            corr = json.load(f)
        cb_by_wp = {entry['threshold']: entry['C'] for entry in corr['mc_vs_wp']}
        log.info("Loaded per-WP C_b from correlation_results.json")
    else:
        cb_by_wp = {}
        log.warning("correlation_results.json not found; using C_B_PUBLISHED=%.2f", C_B_PUBLISHED)

    # Calibrate at multiple working points using derivation set
    thresholds = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    calibration = {}

    log.info("\n--- Efficiency Calibration from MC (Derivation Set) ---")
    log.info("%-8s  %-8s  %-8s  %-8s  %-8s  %-8s  %-8s",
             "WP", "f_s", "f_d", "eps_b", "eps_c", "eps_uds", "alpha")

    for thr in thresholds:
        h0 = mc_h0[deriv_idx]
        h1 = mc_h1[deriv_idx]
        N_had, N_t, N_tt, f_s, f_d = count_tags_from_arrays(h0, h1, thr)

        if f_s <= 0 or f_d <= 0:
            log.warning("WP %.1f: f_s=%.6f, f_d=%.6f — skipping", thr, f_s, f_d)
            continue

        # Use per-WP C_b (fix A1: WP mismatch)
        C_b_wp = cb_by_wp.get(thr, C_B_PUBLISHED)
        log.info("WP %.1f: Using C_b = %.4f", thr, C_b_wp)

        # Get all solutions
        solutions = calibrate_efficiencies_quadratic(
            f_s, f_d, R_B_SM, R_C_SM, C_b_wp, C_C, C_UDS
        )

        if not solutions:
            log.warning("WP %.1f: no valid solution", thr)
            calibration[str(thr)] = {
                'f_s': float(f_s), 'f_d': float(f_d),
                'N_had': N_had, 'N_t': N_t, 'N_tt': N_tt,
                'solutions': [], 'status': 'no_solution',
            }
            continue

        # Select the solution with eps_c in the most physical range
        # Prefer alpha ~ 0.05-0.15 (typical LEP values)
        best = min(solutions, key=lambda s: abs(s['alpha'] - 0.10))

        log.info("%-8.1f  %-8.4f  %-8.6f  %-8.4f  %-8.4f  %-8.5f  %-8.3f",
                 thr, f_s, f_d, best['eps_b'], best['eps_c'],
                 best['eps_uds'], best['alpha'])

        calibration[str(thr)] = {
            'f_s': float(f_s),
            'f_d': float(f_d),
            'N_had': N_had,
            'N_t': N_t,
            'N_tt': N_tt,
            'eps_b': best['eps_b'],
            'eps_c': best['eps_c'],
            'eps_uds': best['eps_uds'],
            'alpha': best['alpha'],
            'n_solutions': len(solutions),
            'all_solutions': solutions[:5],  # Save top 5
            'status': 'calibrated',
        }

    # Also do full MC (not split) for primary calibration
    log.info("\n--- Full MC Calibration ---")
    full_calibration = {}
    for thr in thresholds:
        N_had, N_t, N_tt, f_s, f_d = count_tags_from_arrays(mc_h0, mc_h1, thr)
        if f_s <= 0 or f_d <= 0:
            continue
        # Use per-WP C_b (fix A1)
        C_b_wp = cb_by_wp.get(thr, C_B_PUBLISHED)
        solutions = calibrate_efficiencies_quadratic(
            f_s, f_d, R_B_SM, R_C_SM, C_b_wp, C_C, C_UDS
        )
        if not solutions:
            log.warning("WP %.1f: no solution with C_b=%.4f", thr, C_b_wp)
            continue
        best = min(solutions, key=lambda s: abs(s['alpha'] - 0.10))
        full_calibration[str(thr)] = {
            'f_s': float(f_s), 'f_d': float(f_d),
            'N_had': N_had, 'N_t': N_t, 'N_tt': N_tt,
            'eps_b': best['eps_b'], 'eps_c': best['eps_c'],
            'eps_uds': best['eps_uds'], 'alpha': best['alpha'],
            'C_b_used': float(C_b_wp),
        }
        log.info("WP %.1f: C_b=%.4f, eps_b=%.4f, eps_c=%.4f, eps_uds=%.5f",
                 thr, C_b_wp, best['eps_b'], best['eps_c'], best['eps_uds'])

    output = {
        'derivation_calibration': calibration,
        'full_mc_calibration': full_calibration,
        'sm_inputs': {
            'R_b_SM': R_B_SM,
            'R_c_SM': R_C_SM,
            'source': 'hep-ex/0509008',
        },
        'split': {
            'seed': SPLIT_SEED,
            'n_deriv': len(deriv_idx),
            'n_valid': len(valid_idx),
            'total': n_mc,
        },
        'correlation_inputs': {
            'C_b': 'per-WP from correlation_results.json (fix A1)',
            'C_b_published_fallback': C_B_PUBLISHED,
            'C_c': C_C, 'C_uds': C_UDS,
            'source': 'MC-measured per-WP C_b from hemisphere_correlation.py',
        },
        'gluon_splitting': {
            'g_bb': G_BB, 'g_bb_err': 0.00063,
            'g_cc': G_CC, 'g_cc_err': 0.0038,
            'g_bb_source': 'LEP average, inspire_416138',
            'g_cc_source': 'world average, hep-ex/0302003',
        },
    }

    with open(OUT / "mc_calibration.json", "w") as f:
        json.dump(output, f, indent=2)
    log.info("\nSaved mc_calibration.json")


if __name__ == "__main__":
    main()
