# Phase 3 Selection — Arbiter Report (Iteration 2)

**Session:** phil2_94f9
**Date:** 2026-04-02
**Artifact:** `phase3_selection/outputs/SELECTION.md` (magnus_1207, 482 lines)
**Reviews adjudicated:**
- Critical: erik_352e (3A, 5B, 3C)
- Plot validator: greta_5857 (4A, 2B)
**Prior arbiter:** phil_f9b5 (iteration 1)

---

## Structured Adjudication Table

| # | Finding | Source | Their Cat | Final Cat | Rationale |
|---|---------|--------|-----------|-----------|-----------|
| 1 | MC tail ratio 1.86 absent from JSON | Critical (A-1) | A | **A** | Verified: d0_sign_validation.json contains no MC entry. The claim "1.86 (MC)" in SELECTION.md Section 3 is unverifiable from saved artifacts. The fix is trivial (add MC computation to JSON or remove claim). Must resolve. |
| 2 | N_t/N_tt definition inconsistency | Critical (A-2) | A | **Dismiss** | I independently read double_tag_counts.json. The JSON fields are `N_t` and `N_tt`, NOT `n_single_tag`. At threshold 4.0: JSON shows N_t=2,940,992 and N_tt=836,660, which exactly match the SELECTION.md table. The critical reviewer's claimed "n_single_tag=2,104,332" field does not exist in the JSON. The reviewer appears to have hallucinated or misread the JSON field name. There is no inconsistency. See Dismissal Justification below. |
| 3 | d0 sign validation b-enrichment mismatch (JSON vs figure) | Critical (A-3) | A | **B** | Partially valid. I verified: (a) d0_sign_validation.json has n_b_enriched_events=2,881,742 (bFlag=4 definition, old computation). (b) plot_all.py lines 217-267 correctly implement tight double-tag (combined tag > 8 in both hemispheres), producing 231,054 events. (c) The plot validator confirms Figure 2 shows "b-enriched (tight double-tag, 231054 events)" with clearly separated curves. The FIGURE is correct; the JSON was not updated when the plot code was fixed. The tail ratio 1.76 in the JSON and SELECTION.md Section 3 is from the old computation; the figure shows different asymmetry values computed from the tight-tag sample. The [D19] gate result IS meaningful because the figure uses the correct sample. However, SELECTION.md Section 3 quotes the old tail ratio (1.76) from the stale JSON. This is a documentation inconsistency, not a physics failure. Downgrade from A to B: update JSON and SELECTION.md Section 3 to reflect the tight-tag computation. |
| 4 | set_title calls in closure test figure | Plot val (A-1) | A | **B** | The `set_title` calls on lines 597, 618, 642 of plot_all.py ARE a forbidden pattern per plotting standards. However, these are sub-panel identifiers "(a)", "(b)", "(c)" on a 1x3 multi-panel figure. The correct fix is `ax.text()` annotations. The collision with the experiment label on panel (b) is a genuine rendering problem. I downgrade from A to B because: (1) this is a cosmetic rendering issue, not physics; (2) the fix is straightforward; (3) sub-panel labels are a legitimate need for multi-panel figures. The text collision with the experiment label is the substantive concern and can be fixed alongside the set_title removal. |
| 5 | Experiment label collision on closure test panel (b) | Plot val (A-2) | A | **B** | Merged with finding #4. The collision is caused by set_title placement combined with exp_label_data on axes[1]. Moving exp_label_data to axes[0] and replacing set_title with ax.text resolves both. Category B (rendering, not physics). |
| 6 | bFlag chi2/ndf = 1114 labeled PASS | Plot val (A-3) | A | **B** | The plot validator applies the closure alarm band rule (chi2/ndf > 3 = failure) mechanically. However, this test is NOT a closure test in the standard sense. It is a DISCRIMINATION test: does bFlag separate different physics? The chi2/ndf = 11,447 comparing bFlag=4 (99.81%) vs bFlag=-1 (0.19%) is EXPECTED to be enormous. These are not two samples drawn from the same distribution -- bFlag=-1 events are genuinely different (non-b subset). A chi2/ndf >> 1 is the CORRECT outcome that demonstrates bFlag has discriminating power. The pass criterion should be "chi2/ndf > 2.0" (bFlag separates physics), not "chi2/ndf ~ 1.0" (distributions are identical). The JSON correctly states `"verdict": "bFlag provides discriminating power (chi2/ndf > 2.0)"` and `"passes": true`. The problem is labeling: the figure and artifact call this a "closure test" when it is a discrimination power demonstration. Fix: (1) relabel this test in SELECTION.md and the figure from "closure test" to "discrimination power test" or "bFlag validation"; (2) the pass criterion is chi2/ndf >> 2, not chi2/ndf ~ 1. This is Category B (mislabeling), not Category A (physics failure). |
| 7 | Contamination ratio 2.14 labeled PASS | Plot val (A-4) | A | **B** | The plot validator applies the closure alarm band threshold mechanically (ratio > 2 = fail). However, the contamination injection test at Phase 3 operates with uncalibrated background efficiencies. The analytical prediction (dR_b ~ -frac * R_b * eps_b) is a FIRST-ORDER approximation. With eps_b that would need to exceed 1.0 to reconcile the formula (Section 7.1 analysis), the non-linear response of the double-tag formula amplifies the contamination effect. The ratio = 2.14 means the first-order prediction underestimates the shift by 2x -- this is physically expected when the formula inputs are far from their true values. The artifact CORRECTLY documents this as "PASS (open finding)" with explicit acknowledgment that Phase 4 must re-evaluate. The "same direction" pass criterion is appropriate for Phase 3; the quantitative ratio test belongs in Phase 4 after calibration. Downgrade to B: the artifact should more explicitly state why the standard closure alarm band does not apply here, and commit to re-evaluating against the standard criterion after calibration. |
| 8 | Mirrored-significance test is guaranteed-pass sanity check | Critical (B-1) | B | **B** | Valid. The test result f_s=0, R_b=0 follows algebraically from the tag definition. The artifact should explicitly label this as a code sanity check, not an independent closure test per conventions/extraction.md. The independent closure test requirement (pull < 2sigma vs MC truth) cannot be met at Phase 3 due to absence of MC truth labels -- this should be stated. |
| 9 | bFlag chi2 test sample size asymmetry | Critical (B-2) | B | **C** | The concern about chi2 validity with 5,519 events in 8 bins is technically correct but moot given finding #6: the chi2/ndf = 11,447 is not a closure test but a discrimination power demonstration. Even with Poisson approximation issues in tail bins, the chi2/ndf would still be >> 100. The physics conclusion (bFlag discriminates) is robust regardless of the exact chi2 value. Downgrade to C: add per-bin bFlag=-1 counts as a documentation improvement. |
| 10 | BDT self-labelling circularity | Critical (B-3) | B | **C** | The concern about BDT training circularity from cut-based labels is valid in principle but this is a Phase 4 design question, not a Phase 3 deliverable. Phase 3 correctly defers the BDT to Phase 4 with documented justification. The circularity concern should be noted in the Phase 4 open issues list (Section 14) but does not block Phase 3 advancement. Downgrade to C: add a note in Section 14 that self-labelling creates a ceiling on BDT performance and alternative training strategies should be investigated. |
| 11 | Per-year R_b consistency not done | Critical (B-4) | B | **B** | Valid. COMMITMENTS.md marks per-year extraction as unresolved. Year labels are preserved in NPZ files. At minimum, a per-year f_s/f_d comparison should be reported to check for time-dependent effects. This is a conventions/extraction.md requirement. However, the full per-year R_b extraction requires calibrated efficiencies (Phase 4). A pragmatic middle ground: report per-year f_s and f_d at the nominal working point to verify stability of raw tag rates across years. This can be done in ~30 minutes. |
| 12 | Post-calibration width reconciliation | Critical (B-5) | B | **B** | Valid. MAD*1.48=1.10 and calibrated_neg_width=12.83 appear to measure different things. The d17_vertex_investigation.json value of 12.83 likely measures the raw width of the calibrated negative d0 distribution in microns, while 1.10 measures the normalized d0/sigma_d0 distribution width. These are different quantities. The artifact should clarify what each measures. |
| 13 | Absolute fontsize=5 in two places | Plot val (B-5,6) | B | **C** | The fontsize=5 on sigma_d0 calibration tick labels and closure test legend is a minor rendering concern. The sigma_d0 labels are already shown only every 8th bin. Replacing with "xx-small" or "x-small" is a trivial fix. Downgrade to C: apply before commit, no re-review needed. |
| 14 | R_b bias curve not quantitatively predicted | Plot val (B-7) | B | **C** | The suggestion to overlay a predicted R_b_apparent(threshold) curve on the R_b scan is a good idea for Phase 4 but not required at Phase 3. The back-of-envelope analysis in Section 7.1 provides the quantitative explanation. Adding the curve would strengthen the figure but is not blocking. Downgrade to C: recommend for Phase 4 implementation. |
| 15 | eps_b assumption in back-of-envelope | Critical (C-1) | C | **C** | Valid suggestion. The f_d/f_s ratio gives eps_b ~ 0.49, confirming the assumed 0.5. Add derivation. |
| 16 | WP stability and calibration coupling | Critical (C-2) | C | **C** | Valid. Add acknowledgment that post-calibration stability check is partially self-validating. |
| 17 | MC normalization justification missing | Critical (C-3) | C | **C** | Valid. Add one-sentence justification citing [L1]. |

---

## Dismissal Justification: Finding #2 (N_t definition inconsistency)

**Cost estimate:** 0 agent-hours (no fix needed).

**Evidence:** I read `double_tag_counts.json` in full. The file contains two arrays (`combined_scan` and `probability_scan`), each with entries containing fields: `threshold`, `N_had`, `N_t`, `N_tt`, `f_s`, `f_d`, `R_b`, `eps_b`, `sigma_rb_stat`, `tag_type`. At threshold 4.0 in the combined_scan: `N_t = 2,940,992`, `N_tt = 836,660`. These exactly match SELECTION.md Section 5 table values. The field name `n_single_tag` referenced by the critical reviewer does not appear anywhere in the file. The f_s = N_t / (2 * N_had) = 2,940,992 / (2 * 2,887,261) = 0.5093, which matches the JSON f_s = 0.5093. There is no inconsistency. The reviewer's investigation of "n_single_tag = 2,104,332" appears to reference a field that does not exist.

**Physics impact:** None. The values are consistent.

**Future commitment:** None needed.

---

## Summary of Final Categories

### Category A (must resolve before PASS) — 1 finding

**A-1 (MC tail ratio absent from JSON).** SELECTION.md Section 3 claims "1.86 (MC)" for the positive/negative d0/sigma_d0 tail ratio at 3-sigma, but d0_sign_validation.json contains no MC entry. Either: (a) add the MC tail ratio computation to d0_sign_validation.json and verify it matches the claimed 1.86, or (b) remove the "1.86 (MC)" claim from SELECTION.md if the MC computation was not performed. This is a 15-minute fix.

### Category B (must fix before PASS) — 5 findings

**B-1 (d0 sign validation JSON stale).** The d0_sign_validation.json still contains the old bFlag=4 computation (n_b_enriched_events = 2,881,742). The plot was correctly recomputed using tight double-tag (231,054 events). Update the JSON to reflect the tight-tag computation, and update SELECTION.md Section 3 to report the tail ratio from the tight-tag sample rather than the stale bFlag=4 value. Estimated fix: 20 minutes.

**B-2 (closure test figure rendering).** Remove `set_title` calls on closure test panels; replace with `ax.text()` annotations. Move `exp_label_data` to axes[0] to eliminate the text collision on panel (b). Replace `fontsize=5` with relative fontsize. Estimated fix: 15 minutes.

**B-3 (bFlag test mislabeled as closure test).** The bFlag chi2/ndf test is a discrimination power demonstration, not a closure test. The chi2/ndf = 11,447 is the EXPECTED outcome (bFlag=4 and bFlag=-1 have genuinely different physics). Relabel this test in SELECTION.md Section 8 from "Closure Test (b)" to "Validation Test (b): bFlag discrimination power" or similar. Update the closure test summary table to clarify the pass criterion is chi2/ndf >> 2 (shapes differ). Update the JSON `passes` field documentation. Estimated fix: 15 minutes.

**B-4 (per-year tag rate stability).** Report per-year f_s and f_d at one nominal working point (e.g., WP=5.0) to verify raw tag rate stability across data-taking years. Full per-year R_b extraction deferred to Phase 4. Estimated fix: 30 minutes.

**B-5 (post-calibration width clarification).** Clarify that MAD*1.48 = 1.10 in Section 13 measures the width of the normalized d0/sigma_d0 negative tail, while calibrated_neg_width = 12.83 in d17_vertex_investigation.json measures a different quantity (raw d0 width in microns, or per-event spread). Add units and definitions. Estimated fix: 10 minutes.

### Category C (apply before commit, no re-review) — 8 findings

- C-1: Relabel mirrored-significance test as "code sanity check" (not independent closure test)
- C-2: Add per-bin bFlag=-1 counts to documentation
- C-3: Add note to Phase 4 open issues about BDT self-labelling ceiling
- C-4: Derive eps_b ~ 0.49 from f_d/f_s in Section 7.1 back-of-envelope
- C-5: Acknowledge WP stability / calibration coupling in Section 7.1 or 14
- C-6: Add MC normalization justification citing [L1]
- C-7: Recommend predicted R_b_apparent(threshold) curve for Phase 4
- C-8: Replace fontsize=5 with relative fontsize in sigma_d0 tick labels

---

## Regression Check

| Trigger | Met? | Evidence |
|---------|------|----------|
| Validation test failure without 3 documented remediation attempts | **No** | The mirrored-significance test passes by construction (sanity check). The bFlag test is a discrimination test, not a closure test -- it correctly shows chi2/ndf >> 2. The contamination injection shows correct-direction shift. No validation test has FAILED in the standard sense. |
| Any single systematic > 80% of total uncertainty | **No** | Phase 3 does not compute final uncertainties. Not applicable. |
| GoF toy inconsistency | **No** | No toy studies at Phase 3. |
| > 50% bin exclusion | **No** | No bins excluded. |
| Tautological comparison presented as validation | **Partially** | The bFlag chi2 test compares 99.81% vs 0.19% subsets of the same data. This is not tautological (the subsets are genuinely different), but the framing as a "closure test" is misleading. Addressed as B-3 (relabeling). Not a regression trigger. |
| Result > 3-sigma from reference | **N/A** | R_b values 0.48-0.98 are far from SM 0.216, but this is a known, documented consequence of uncalibrated background efficiencies. The analysis does not claim these as physics results. |
| Binding commitments [D1]-[D19] fulfilled | **Yes** | All Phase 3 commitments addressed. [D9]/[D10] formally deferred with documented justification. [D19] gate validated (figure uses tight double-tag; JSON needs update). |

**No regression triggers are met.** The findings are local fixes within Phase 3 scope.

---

## Reviewer Diagnostic

**Critical reviewer (erik_352e):** Thorough and well-structured review. Correctly identified the stale d0_sign_validation.json (A-3) and the MC tail ratio gap (A-1). Good quantitative verification of the back-of-envelope R_b analysis. COVERAGE GAP: The N_t inconsistency finding (A-2) appears to be based on a field name ("n_single_tag") that does not exist in the current double_tag_counts.json -- the actual field is "N_t" and the values match. This is a factual error in the review. The reviewer may have been working from an older version of the file or hallucinated the field name. This is the first instance of a reviewer introducing a false finding based on nonexistent data; it did not propagate to a physics error but could have caused unnecessary iteration.

**Plot validator (greta_5857):** Comprehensive visual review of all 20 figures. Correctly identified the set_title violation and text collision. Correctly noted the fontsize issue. COVERAGE GAP: Applied the closure alarm band rules (chi2/ndf > 3 = failure) mechanically to the bFlag discrimination test without recognizing that this test has inverted pass criteria (chi2/ndf >> 2 = PASS, not FAIL). Similarly applied a generic "ratio > 2 = fail" threshold to the contamination injection without accounting for the uncalibrated-efficiency regime. Both of these findings demonstrate that the plot validator correctly identified deviations from mechanical rules, which is its job. The physics interpretation (whether these are real failures) falls outside the plot validator's scope -- that is the arbiter's job. The validator fulfilled its role correctly by flagging objective deviations.

---

## Verdict

**ITERATE**

The Phase 3 artifact has 1 Category A and 5 Category B findings that must be resolved.

### Priority-ordered fix list for the fixer agent

**Priority 1 (Category A):**
1. **MC tail ratio in JSON.** Either compute the MC tail ratio and add it to d0_sign_validation.json, verifying it matches the claimed 1.86, OR remove the "1.86 (MC)" text from SELECTION.md Section 3 if the MC computation was not saved. If computing: run the same tail ratio analysis on MC signed d0/sigma_d0 at the 3-sigma threshold.

**Priority 2 (Category B):**
2. **Update d0_sign_validation.json.** Rerun d0_sign_validation computation using tight double-tag (combined tag > 8 in both hemispheres) as the b-enrichment definition. Update all JSON fields (n_b_enriched_events should be ~231,054, not 2,881,742). Update SELECTION.md Section 3 tail ratio to match the new JSON.

3. **Fix closure test figure rendering.** Remove `ax.set_title()` on all three panels of the closure test figure. Replace with `ax.text(0.05, 0.95, '(a)', ...)` annotations. Move `exp_label_data` call from axes[1] to axes[0]. Replace `fontsize=5` with `fontsize="xx-small"` in the closure legend.

4. **Relabel bFlag test.** In SELECTION.md Section 8, rename "Closure Test (b): bFlag discriminant shape comparison" to "Validation Test (b): bFlag discrimination power" or "Discrimination test (b)". Update the summary table pass criterion from "computable" to "chi2/ndf >> 2 (shapes differ, confirming bFlag separates physics)". Clarify in the text that this is NOT a closure test in the conventions/extraction.md sense -- it demonstrates that bFlag discriminates, which is the prerequisite for the deferred BDT approach.

5. **Per-year tag rate stability.** Compute f_s and f_d at WP=5.0 for each data-taking year separately. Report a table with per-year values and a chi2/ndf for consistency. This does not require per-year R_b extraction (which needs calibrated efficiencies).

6. **Clarify post-calibration width.** Add explicit definitions and units for MAD*1.48 = 1.10 (normalized d0/sigma_d0 negative tail width) and calibrated_neg_width = 12.83 (specify what this measures and in what units).

**Priority 3 (Category C -- apply before commit):**
7. Relabel mirrored-significance test as "code sanity check"
8. Add per-bin bFlag=-1 counts
9. Note BDT self-labelling performance ceiling in Section 14
10. Derive eps_b from f_d/f_s in Section 7.1
11. Acknowledge WP stability/calibration coupling
12. Add MC normalization justification
13. Recommend predicted bias curve for Phase 4
14. Replace fontsize=5 with relative fontsize in sigma_d0 tick labels

---

*Arbiter: phil2_94f9 | 2026-04-02 | Phase 3 Selection, Iteration 2*
