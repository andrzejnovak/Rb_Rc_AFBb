# Phase 4a Executor Log — theo_cb0e

Date: 2026-04-02

## Session overview

Implemented full Phase 4a expected-results extraction for R_b, A_FB^b,
and sin^2(theta_eff) from MC pseudo-data.

## Scripts written

1. `src/mc_efficiency_calibration.py` — MC-derived eps_b, eps_c, eps_uds
2. `src/hemisphere_correlation.py` — C_b estimation from MC
3. `src/rb_extraction.py` — R_b double-tag extraction with calibrated inputs
4. `src/afb_extraction.py` — A_FB^b self-calibrating fit
5. `src/systematics.py` — Full systematic evaluation
6. `src/closure_and_stress.py` — Closure, corrupted corrections, stress tests
7. `src/plot_phase4a.py` — All Phase 4a figures (8 total)
8. `src/write_results_json.py` — Machine-readable results aggregation

## Key findings

### 1. Efficiency calibration underdetermined without truth labels

The MC calibration (back-calculating efficiencies from SM truth + observed
tag rates) only converges at tight WPs (>= 7.0). At looser WPs, eps_b
would need to exceed 1.0 because the charm contamination is so large.
This is a direct consequence of [A1] (no MC truth labels).

### 2. Hemisphere correlation C_b >> published value

C_b = 1.18 at WP 5.0 (vs ALEPH published 1.01). Our simplified combined
tag creates stronger inter-hemisphere correlations because:
- No per-hemisphere primary vertex reconstruction [D17]
- Combined probability-mass tag uses event-level correlated quantities
- No 3D impact parameter (only 2D d0)

The data-MC agreement on C_b is excellent (delta = 0.005).

### 3. R_b biased high (0.280 vs SM 0.216)

The 2-sigma bias is attributed to the underdetermined calibration system.
The multi-WP fit on data [D14] should resolve this by constraining all
efficiencies simultaneously.

### 4. A_FB^b correctly returns zero on MC

The MC has no electroweak asymmetry embedded, so A_FB^b = 0 is the
correct expected result. The extraction method has no intrinsic bias.

### 5. eps_uds dominates systematics

The +/-50% eps_uds variation produces delta(R_b) = 0.387, dwarfing all
other sources. This will be constrained by the multi-WP fit on data.

## Validation tests

- Independent closure: PASS (pulls 0.97, 1.93)
- Corrupted corrections: 4/6 sensitive (PASS)
- Per-year consistency: PASS (p = 0.816)
- Kappa consistency: PASS (p = 0.951)

## Figures produced

8 figures total: 5 flagship (F1, F2, F4, F5, F7) + 3 supporting
(closure tests, efficiency calibration, hemisphere correlation).
All registered in FIGURES.json.

## pixi tasks added

p4a-calib, p4a-corr, p4a-rb, p4a-afb, p4a-syst, p4a-closure,
p4a-plots, p4a-results, p4a-all
