# Investigator Session: nikolai_164a

## Date: 2026-04-03

## Bug: Spurious A_FB^b = -0.078 on symmetric MC (15-sigma from zero)

### Root Cause

The `extract_afb_purity_corrected()` function in `purity_corrected_afb.py`
hardcoded `AFB_C_OBS = 0.0682` (the observed charm forward-backward
asymmetry from LEP data) in the charm correction term. This value is
correct for data, but on symmetric MC there is NO electroweak asymmetry
for any quark flavour -- A_FB^c = A_FB^b = A_FB^uds = 0 by construction.

The charm correction formula:
```
charm_correction = f_c * delta_c * AFB_C_OBS
```

With f_c ~ 0.40, delta_c ~ 0.10-0.28 (depending on kappa), and
AFB_C_OBS = 0.0682, this produces a nonzero correction of order 0.003.
Since the raw slope on symmetric MC is ~0, subtracting this correction
and dividing by the small denominator f_b * delta_b ~ 0.03 amplifies it
to ~-0.08.

### The Fix

Made `afb_c` and `afb_uds` explicit parameters of `extract_afb_purity_corrected()`
and `toy_uncertainty_afb()` (default: 0.0). In `main()`, explicitly set
`MC_AFB_C = 0.0` and `MC_AFB_UDS = 0.0` with a comment explaining why.

For data extraction (Phase 4b/4c), callers should pass `afb_c=AFB_C_OBS`.

### Verification

- Before fix: A_FB^b = -0.078 +/- 0.005 (15-sigma from zero)
- After fix: A_FB^b = -0.0001 +/- 0.0052 (0.02-sigma from zero)

Per-kappa combined values after fix:
- kappa=0.3: +0.0199 +/- 0.0122
- kappa=0.5: +0.0070 +/- 0.0101
- kappa=1.0: -0.0055 +/- 0.0103
- kappa=2.0: -0.0144 +/- 0.0124

All consistent with zero within 1-2 sigma (statistical fluctuations).

### Files Modified

- `phase4_inference/4a_expected/src/purity_corrected_afb.py` -- parameterized afb_c/afb_uds
- `phase4_inference/4a_expected/outputs/purity_corrected_afb_results.json` -- regenerated
- `analysis_note/results/parameters.json` -- regenerated via write_results_json_v2.py

### Other Hypotheses Investigated

1. **Published delta_b values** -- These are charge separation values, not
   asymmetry-dependent. They are properties of the detector response to
   quark charge, valid for both MC and data. Not the bug.

2. **Sign convention / hemisphere charge offset** -- The raw slopes are
   ~0.0005, consistent with statistical noise. No systematic offset. Not
   the bug.

3. **delta_b MC vs published mismatch** -- Could cause a scale error but
   not a sign-wrong offset from zero. Not the primary bug.

### Impact on Phase 4b

The Phase 4b `delta_b_calibration.py` correctly uses `AFB_C_OBS` because
it runs on real data where the charm asymmetry exists. No fix needed there.
