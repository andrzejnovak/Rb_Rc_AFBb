# Phase 4a Plan — Expected Results (theo_cb0e)

Session: theo_cb0e | Date: 2026-04-02

## Goal

Compute expected R_b, R_c, A_FB^b, sin^2(theta_eff) results using MC
pseudo-data only. Calibrate background efficiencies, estimate C_b,
apply gluon splitting corrections, evaluate systematics, run closure
tests, produce all figures and machine-readable JSON.

## Scripts to write

### 1. `src/mc_efficiency_calibration.py`
- Load MC hemisphere tags and preselected MC data
- Since we have no MC truth labels, use a split-MC approach:
  split MC into two halves (derivation + validation) with fixed seed
- Derive eps_b, eps_c, eps_uds from MC at multiple working points
  by solving the double-tag equations using known SM R_b, R_c as MC truth
  (the MC was generated with SM values)
- This is the key calibration that was missing in Phase 3
- Output: mc_calibration.json with eps_b, eps_c, eps_uds per WP

### 2. `src/hemisphere_correlation.py`
- Estimate C_b from MC hemisphere tag correlations
- Compute correlation in 4 variables: cos(theta), vertex error, jet p, y_3
- Use all-flavour MC (no truth labels)
- Output: correlation_results.json

### 3. `src/rb_extraction.py`
- Full R_b extraction with calibrated efficiencies
- Multi-working-point extraction [D14]
- Operating point stability scan
- Gluon splitting correction via effective eps_uds
- Independent closure test (derivation vs validation MC halves)
- Output: rb_results.json

### 4. `src/afb_extraction.py`
- A_FB^b from self-calibrating fit [D12b]
- At kappa = {0.3, 0.5, 1.0, 2.0, infinity}
- Bin in cos(theta): 10 uniform bins in [-0.9, 0.9]
- Extract sin^2(theta_eff) as direct fit parameter
- Multiple b-tag purities (working points)
- Output: afb_results.json

### 5. `src/systematics.py`
- Evaluate ALL systematic sources from COMMITMENTS.md
- Per-systematic shift computation
- Full covariance matrix (stat + syst + total)
- Output: systematics_results.json

### 6. `src/closure_and_stress.py`
- Independent closure test (MC split derivation/validation)
- Corrupted corrections test (+/-20% eps_b, eps_c variations)
  Must FAIL to validate sensitivity
- Stress tests
- Output: closure_results.json

### 7. `src/plot_phase4a.py`
- All Phase 4a figures:
  F1: R_b operating point stability scan
  F2: A_FB^b angular distribution
  F4: f_d vs f_s with R_b prediction curves
  F5: Systematic uncertainty breakdown
  F7: A_FB^b kappa consistency
  Plus supporting figures

### 8. `src/write_results_json.py`
- Aggregate all results into analysis_note/results/ JSON files:
  parameters.json, systematics.json, validation.json, covariance.json

## Key physics

### MC pseudo-data approach
The MC was generated with SM parameters. For Phase 4a (expected results),
we treat the MC counts as our pseudo-data and extract parameters that
should recover SM values. The critical insight: since we have no truth
labels, we must use the double-tag self-calibrating property plus the
known SM input values to bootstrap the calibration.

### Background efficiency calibration
The Phase 3 R_b was biased (0.83 vs 0.22) because eps_c=0.05 and
eps_uds=0.005 were nominal guesses. The MC is generated at SM values,
so at each working point the true eps_b, eps_c, eps_uds can be
back-calculated from the observed f_s and f_d using the SM R_b, R_c
as inputs. This calibrates the efficiencies for use on data.

### Gluon splitting
g_bb = (0.251 +/- 0.063)%, g_cc = (2.96 +/- 0.38)%
Enter through effective eps_uds:
  eps_uds(eff) = eps_uds(direct) + g_bb * eps_g + g_cc * eps_gc

## Figures planned

1. R_b vs working point (stability scan) with ALEPH band [F1]
2. A_FB^b angular distribution (<Q_FB> vs cos theta) [F2]
3. f_d vs f_s scatter with R_b prediction curves [F4]
4. Systematic breakdown bar chart [F5]
5. A_FB^b kappa consistency [F7]
6. MC closure test results
7. Per-WP eps_b, eps_c, eps_uds calibration curves
8. C_b estimation from MC
9. Corrupted corrections test (sensitivity validation)
10. Parameter sensitivity table figure
