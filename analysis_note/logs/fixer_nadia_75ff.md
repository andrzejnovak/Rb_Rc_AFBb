# Fixer Session Log: nadia_75ff

Session: nadia_75ff
Date: 2026-04-02
Task: Fix all Category A + B findings from arbiter verdict AN_ARBITER_tomas_f1ad.md

## Findings Resolved

### Category A

**A-FIX-1: Full numerical consistency sweep** -- RESOLVED
- Covariance matrix V_syst[0,0]: 0.156 -> 0.043 (from covariance.json)
- Covariance matrix V_syst[0,1]: 1.58e-4 -> 8.30e-5
- V_stat[0,0]: 9.31e-4 -> 8.52e-4
- V_total[0,0]: 0.157 -> 0.044
- Correlation: 0.088 -> 0.087
- R_b.value field citation: 0.2798 -> 0.3099 (parameters.json)
- eps_b at WP 10.0: 0.238 -> 0.132 (rb_results.json best_wp.eps_b)
- eps_b at WP 9.0: 0.243 -> 0.164 (rb_results.json extraction_results)
- eps_uds at WP 10.0: 0.086 -> 0.120
- eps_uds at WP 9.0: 0.116 -> 0.138
- eps_uds_nominal: 0.0913 -> 0.1195 (systematics.json)
- eps_c_nominal: 0.431 -> 0.440
- Closure WP 9.0 pull: 1.03 -> 1.93 (validation.json)
- Closure WP 9.0 R_b: 0.371 -> 0.347 (validation.json)
- Corrupted corrections: 5/6 -> 4/6 (validation.json)
- eps_uds fraction: 96% -> 92% (quadrature convention, 6 instances fixed)
- Per-year consistency chi2: 0.76/3 -> 0.94/3 (validation.json)
- Angular fit intercept chi2 criterion: FAIL -> PASS (3-4 < 5 is PASS)
- Precision ratio 283x -> 150x (validation.json ratio = 149.77)
- Precision ratio 278x -> 150x (3 instances)

**A-FIX-2: sin2theta_eff removal** -- RESOLVED
- Abstract: removed sin2theta numeric value, added "N/A due to delta_b bias"
- Table 4 (results summary): replaced 10% value with "N/A (delta_b bias)"
- sin2theta comparison table: replaced 10% values with "N/A (delta_b bias)"
- Section 8.7: rewritten to say "Not reported (N/A)"

**A-FIX-3: 13.5-sigma pull recomputation** -- RESOLVED
- Recomputed: sigma = sqrt(0.0056^2 + 0.0052^2) = 0.0076
- Pull = (0.0927 - 0.0085)/0.0076 = 11.0 sigma
- Fixed all 4 instances of "13.5 sigma" to "11.0 sigma"
- Added explicit denominator documentation

**A-FIX-4: Figure fixes** -- RESOLVED
- F5b: Replaced code variable names (eps_uds, g_cc, etc.) with publication labels
- F5b: fontsize=8 -> fontsize='x-small'
- S2b: figsize=(10,10) -> figsize=(20,20)
- S2b: Added exp_label_data to all 4 panels
- S2b: fontsize=12 -> fontsize='small', repositioned kappa text to 0.85
- S2b: 'MC (norm.)' -> 'MC (norm. to data)'
- S1b: Reclassified as 'diagnostic' (line plot, pull panels impractical)
- S2b: Reclassified as 'diagnostic' (2x2 subplot, pull panels impractical)
- F3b: Fixed pull panel masking (OR instead of AND), fixed yticks to [-2,0,2]
- All figures regenerated via pixi run p4b-plots
- PDFs copied to analysis_note/figures/

### Category B

**B-FIX-1: A_FB^b framing** -- RESOLVED
- Abstract reframed as "2.4 sigma slope detection"
- Added "absolute value requires delta_b correction (Phase 4c)"

**B-FIX-2: 10% R_b stat uncertainty** -- RESOLVED (already correct)
- Table uses combined 2-WP value 0.053 (correctly labeled)
- WP 7.0-only value 0.066 appears in text where appropriate

**B-FIX-3: Precision ratio consistency** -- RESOLVED
- Phase 4a ratio consistently 150x
- Phase 4b ratio consistently 373x
- All stale 278x/283x references corrected

**B-FIX-4: Title/abstract R_c claim** -- RESOLVED
- Title changed from "Measurement of R_b, R_c, and A_FB^b" to
  "Measurement of R_b and A_FB^b" with subtitle "(R_c constrained to SM)"

**B-FIX-5: Delta_b feasibility paragraph** -- RESOLVED
- Added feasibility assessment paragraph in Section 10.1 outlook

**B-FIX-6: Validation table additions** -- RESOLVED
- Added angular fit GoF entry (kappa=1.0, chi2=18.4/8, p=0.018)
- Fixed chi2 criterion: intercept chi2/ndf 3-4 now PASS (< 5)

**B-FIX-7: eps_uds solver WP-dependence** -- RESOLVED
- Added explanation paragraph before Phase 4b error budget narrative

**B-FIX-8: eps_c one-sided systematic** -- RESOLVED
- Added sentence flagging +1sigma as lower bound

**B-FIX-9: Appendix D Phase 4b update** -- RESOLVED
- Added paragraph noting shift from eps_c to eps_uds dominance

**B-FIX-10: Table 4 distinction** -- RESOLVED
- Added footnote marking Phase 4a as "circular MC diagnostic"

**B-FIX-11: Analytical vs toy cross-check** -- RESOLVED
- Added formal deferral section with justification

**B-FIX-12: Sentence fragment** -- RESOLVED
- Fixed "The dominant systematic is now eps_c (0.201).\nand -0.256 (when increased)."

**B-FIX-13: Figure caption improvements** -- PARTIALLY RESOLVED
- S2b: 'MC (norm.)' -> 'MC (norm. to data)' in code
- F3b: pull panel tick labels fixed

## Compilation

- v2.tex compiles with tectonic (warnings only, no errors)
- PDF: analysis_note/ANALYSIS_NOTE_doc4b_v2.pdf (1.18 MiB)

## Files Modified

- analysis_note/ANALYSIS_NOTE_doc4b_v2.tex (created from v1, all fixes applied)
- phase4_inference/4b_partial/src/plot_phase4b.py (figure fixes)
- analysis_note/figures/*.pdf (regenerated from plot script)
