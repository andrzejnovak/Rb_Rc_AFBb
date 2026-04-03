# Fixer Session Log — claude_0532

**Date:** 2026-04-03
**Task:** Fix Doc 4a v5 per arbiter verdict (rainer_9779)
**Input:** ANALYSIS_NOTE_doc4a_v5.tex
**Output:** ANALYSIS_NOTE_doc4a_v6.tex + compiled PDF

---

## Category A Fixes (2)

### A4: Per-WP chi2/ndf > 2.4 GoF interpretation
- **Section 8.4 (Goodness-of-fit assessment):** Added quantitative explanation
  that per-WP chi2 reflects the overconstrained 3-tag system tension (8 observables,
  6 free parameters, 2 dof), not a bias in R_b. The stability chi2/ndf = 0.38/14
  across 15 configurations is the relevant GoF metric. Added reference to independent
  closure test as supporting evidence.

### A6: "2sigma below LEP" claim
- **Abstract (line 67):** Changed "approximately 2sigma below" to "0.8 standard
  deviations below". Added clarification that comparison is A_FB^b (uncorrected)
  vs A_FB^{0,b} (pole-corrected).
- **Conclusions (line 2211):** Same fix, plus note about pull magnitude.

## Category B Fixes (18)

### B1 (petra): Covariance rho
- Changed rho from 0.15 to 0.092 (matching covariance.json correlation_matrix[0][1]).
- Added JSON field path citation.

### B4 (petra): SF calibration independence
- Added paragraph in Section 7.4 explaining why shared tag fractions don't bias R_b.
- Cited independent closure test (pulls < 1sigma) as direct evidence.

### B5 (petra): A_FB^b WP selection
- Added quantitative purity correction comparison: amplification factor 9 (kappa=2.0)
  vs 30 (kappa=0.3), and propagated f_b uncertainty at both kappa values.

### B7 (petra): sigma_d0 form inconsistency
- Clarified that sin(theta) is the single-layer parameterisation used in the
  calibration fit, while sin^{3/2}(theta) is the ALEPH detector description
  approximation. Both forms are evaluated as a systematic.

### B8 (petra): kappa=infinity excluded
- Added justification: delta_b(kappa=inf) = 1.000 implies zero charge separation
  uncertainty, making purity correction ill-conditioned at low f_b; discrete charge
  values violate continuous Q_h assumption of linear fit.

### B3 (petra, downgraded to C): C_b = 1.0 vs 1.01
- Added parenthetical noting ALEPH published C_b ~ 1.01, with propagated Delta_R_b
  ~ 0.0001, well below systematic floor.

### A1->B: JSON structure navigation
- Added SF stability chi2 to parameters.json and validation.json with source paths.

### A2->B: Stability chi2 traceability
- Added R_b_10pct_sf_stability to parameters.json with chi2=0.3787, ndf=14.
- Added operating_point_stability_sf_corrected to validation.json.

### A3->B: A_FB^b traceability
- Added A_FB_b_10pct_purity_corrected to parameters.json (value=0.07366,
  stat=0.03088, source path documented).

### F1 (sally): Fig 5 legend "From MC (SM truth)"
- Fixed in plot_phase4a.py -> "MC calibration (assuming R_b^SM)".
- Regenerated efficiency calibration figures.

### F2 (sally): Fig 6 Phase 3 annotation box
- Fixed in plot_all.py: removed internal phase references, replaced with
  "MC diagnostic" language.
- Phase 3 script rerun in progress.

### F3 (sally): Fig 14 caption
- Updated caption to describe actual 2x2 four-kappa panel content.

### F4, F5 (sally): "Phase 4a (MC)" legends
- Fixed in plot_phase4b.py: all instances -> "MC pseudo-data".
- Regenerated F1b_rb_stability_10pct and F7b_kappa_consistency_10pct.

### F6, F7 (sally): "Phase 4c" body text
- Replaced "planned for Phase~4c" with "planned for the full-data analysis".
- Replaced "(Phase~4c)" with "(~2.9M events)" in appendix.
- Rephrased tbd-wrapped Conclusions paragraph.

### F8 (sally): Multi-panel figsize
- Fixed 1x2 closure test figure: figsize=(10,10) -> (20,10).
- Composed efficiency calibration as 1x3 with figsize=(30,10).

## Category C Fixes (10)

### A5->C: Phase identification
- Added sentence in Introduction: "This document covers both the method
  validation on MC pseudo-data and the first application to a 10% data
  validation subsample."

### F10: Duplicate \label
- Merged \label{fig:datamc_sphericity} and \label{fig:datamc_d0} into
  single \label{fig:datamc_sphericity_d0}. Updated all references.

### F11: Change Log + header version
- Fixed header comment: "Doc 4b v5" -> "Doc 4a v6".
- Fixed Change Log: "Doc 4b v5" -> "Doc 4a v5". Added "Doc 4a v6" entry.

## Compilation
- tectonic compiles successfully.
- 0 unresolved \ref or \cite references.
- 0 remaining "Phase 4c" references in PDF.
- 0 remaining "2sigma" claims in PDF.

## Files Modified
- `analysis_note/ANALYSIS_NOTE_doc4a_v6.tex` (new, from v5)
- `analysis_note/ANALYSIS_NOTE_doc4a_v6.pdf` (compiled)
- `analysis_note/results/parameters.json` (added SF stability + A_FB purity-corrected)
- `analysis_note/results/validation.json` (added SF stability chi2)
- `phase4_inference/4a_expected/src/plot_phase4a.py` (F1 legend fix, F8 figsize)
- `phase4_inference/4b_partial/src/plot_phase4b.py` (F4, F5 legend fixes)
- `phase3_selection/src/plot_all.py` (F2 annotation box fix)
- `analysis_note/figures/efficiency_calibration.{pdf,png}` (regenerated)
- `analysis_note/figures/F1b_rb_stability_10pct.{pdf,png}` (regenerated)
- `analysis_note/figures/F7b_kappa_consistency_10pct.{pdf,png}` (regenerated)
- `analysis_note/figures/closure_test_phase4a.{pdf,png}` (regenerated)

## Pending
- F2: Phase 3 plot_all.py is running. The rb_operating_scan figure will be
  regenerated with the fixed annotation when the script completes. Will need
  to copy to analysis_note/figures/ after completion.
