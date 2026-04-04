# Fixer Session: final_a535

**Date:** 2026-04-04
**Input:** AN_ARBITER_hugo_9256.md (PASS with 6B + 14C)
**Output:** ANALYSIS_NOTE_doc4c_v5.tex / .pdf

## Category B fixes applied (6)

1. **#3 A_FB stat-only labelling:** Added "(stat only, systematic evaluation
   pending)" to all occurrences of A_FB = 0.094 +/- 0.005: abstract,
   boxed equation (eq:afb_signed_fulldata), results summary table
   (tbl:results_summary with dagger footnote), comparison table
   (tbl:comparison_afb), conclusions. Added note about fully-evaluated
   cross-check baseline (purity-corrected, unsigned axis: 0.0025 +/- 0.0034).

2. **#4 parameters.json:** Added `R_b_BDT_primary` (0.2155 +/- 0.0004 stat,
   systematic_status: pending) and `A_FB_b_signed_primary` (0.094 +/- 0.005
   stat, systematic_status: pending) entries with metadata flags.

3. **#6 R_b systematic total 0.027 vs 0.020:** Added explicit quadrature
   computation showing subtotal = 0.020 at C_b=1.0, plus linear addition
   of C_b envelope (0.017) giving total 0.027. Added "Quadrature subtotal"
   and "C_b envelope" rows to tbl:rb_syst_fulldata. Added explanatory
   paragraph below the table.

4. **#8 Cross-kappa consistency:** Replaced the brief kappa-dependence
   paragraph with detailed explanation of the monotonic decrease via
   kappa-dependent delta_b and signing dilution. Added chi2/ndf = 168/5
   for constant fit, confirming the dependence is physical.

5. **#11 systematics_breakdown_fulldata label:** Added `exp_label_data(ax1)`
   to plot_phase4c.py and regenerated the figure.

6. **#12 calibration_progression header:** Added `fig.subplots_adjust(wspace=0.35)`
   to prevent header overlap in two-panel layout; regenerated figure.

7. **#13 closure_test_phase4a:** Replaced stale figure with
   `closure_tests_magnus_1207_20260403.pdf` (which shows all four
   configurations near SM value with pulls 0.06-0.59). Updated caption
   to match.

## Category C fixes applied (14)

- C1: Added sentence noting BDT GoF tension has same origin as cut-based,
  citing BDT stability chi2/ndf = 1.1/12.
- C2: Added note explaining that earlier Phase 4c diagnostic (INFERENCE_OBSERVED.md
  Diagnostic 1) incorrectly concluded axis was signed, with explanation of why.
- C5: Added "Review status" paragraph noting which results passed full inference
  review cycle (cut-based R_b, unsigned-axis A_FB) and which were developed
  subsequently (BDT R_b, signed-axis A_FB).
- C7: Added note that sin2(theta_eff) extraction requires complete A_FB
  uncertainty budget and is deferred.
- C9: Added clarification that eps_c/eps_b comparison is at different
  operating points / efficiencies.
- C10: Updated validation.json with BDT stability and signed-axis A_FB entries.
- C14: Changed reproduction contract from v3 to v5.
- C15: Updated Future Directions item 2 (SV reconstruction) to acknowledge
  partial completion in this analysis.
- C16: Fixed abstract "0.1 sigma" to "0.2 sigma" for A_FB; fixed conclusions
  "pull = -0.1 sigma" to "-0.2 sigma" for R_b vs SM.
- C18: Added footnotes to R_b and A_FB comparison tables clarifying
  stat-only vs total uncertainty conventions.
- C19: Added sentence clarifying BDT sigma_stat propagation method
  (analytical propagation from Poisson tag fractions).
- C20: Fixed per-year figure caption from "purity-corrected" to
  "inclusive slope/delta_b without purity correction" to match table caption.

## Compilation

tectonic compiled successfully. PDF: analysis_note/ANALYSIS_NOTE_doc4c_v5.pdf (1.13 MiB).
Warnings: overfull/underfull hboxes only (cosmetic).

## Files modified

- analysis_note/ANALYSIS_NOTE_doc4c_v5.tex (new, from v4)
- analysis_note/ANALYSIS_NOTE_doc4c_v5.pdf (compiled)
- analysis_note/results/parameters.json (added BDT R_b + signed-axis A_FB entries)
- analysis_note/results/validation.json (added BDT stability + signed-axis A_FB entries)
- phase4_inference/4c_observed/src/plot_phase4c.py (exp_label + spacing fixes)
- analysis_note/figures/systematics_breakdown_fulldata.{pdf,png} (regenerated)
- analysis_note/figures/calibration_progression.{pdf,png} (regenerated)
- analysis_note/figures/closure_test_phase4a.pdf (replaced with closure_tests_magnus_1207_20260403.pdf)
