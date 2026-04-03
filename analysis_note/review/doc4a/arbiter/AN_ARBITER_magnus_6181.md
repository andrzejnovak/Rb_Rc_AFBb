# Arbiter Adjudication -- Doc 4a, Review Iteration 2

**Arbiter:** magnus_6181
**Date:** 2026-04-02
**Artifact:** `analysis_note/ANALYSIS_NOTE_doc4a_v2.tex` (52 pages)
**Iteration:** 2 of Doc 4a review (iteration 1 had 17A + 16B; warn threshold at 3)

## Inputs Read

1. Physics review: gunnar_8836 (2A, 6B, 5C)
2. Critical review: hedwig_f66f (5A, 7B, 4C)
3. Constructive review: isolde_f26f (2A, 3B, 7C)
4. Plot validation: kenji_3c08 (3A unfixed + 1 new A = 4A total, 11B, 3C)
5. Rendering review: renata_120f (C only -- PASS)
6. BibTeX validation: ada_4351 (PASS)
7. Conventions: `conventions/extraction.md`
8. Methodology: `methodology/06-review.md`
9. v1 arbiter: zelda_65ac; verification: vera3_fbef

---

## Progress Since Iteration 1

Iteration 1 had 17 Category A and 16 Category B findings. The fixer resolved
the majority. Key improvements in v2:

- All 5 rendering A findings (broken refs, orphaned figures/tables, typo, truncated label) are FIXED
- Intercept-inclusive chi2 added to per-kappa table
- Quantitative circular calibration bias decomposition added
- INFEASIBLE documentation with 3 remediation attempts for OP stability and WP 10.0 closure
- Parameter sensitivity table added
- kappa = infinity row added
- Change log documents ~25 fixes

The remaining issues cluster around three themes: (1) the C_b working-point
mismatch (a genuine physics bug), (2) the A_FB chi2/ndf GoF failure lacking
investigation, and (3) Phase 4a figures not regenerated with plot fixes.

---

## Structured Adjudication Table

| # | Finding | Source(s) | Their Cat | Final Cat | Rationale |
|---|---------|-----------|-----------|-----------|-----------|
| 1 | C_b systematic evaluated at WP 5.0 (1.179) instead of operating WP 10.0 (1.537); extraction uses wrong C_b | Critical [A3] | A | **A** | Confirmed by JSON cross-check: `systematics.json C_b_nominal = 1.1786` matches `correlation_results.json mc_vs_wp[5.0].C` exactly while WP 10.0 gives 1.5372. The extraction formula uses C_b multiplicatively on f_d. Using C_b off by 0.358 at the operating point biases R_b and invalidates the systematic evaluation. This is the most critical finding -- it affects the primary R_b result and its uncertainty budget. |
| 2 | Intercept chi2/ndf = 2.1--4.3 across kappa values; governing A_FB model fails GoF without demonstrated non-bias | Physics [A2], Critical [A4], Constructive [A1] | A, A, A | **A** | Three reviewers independently flag this. The chi2/ndf ranges 2.1 (kappa=inf) to 4.3 (kappa=1.0). The AN offers only a "likely reflects" narrative without residual analysis, binning variation, or cos^2(theta) test. Per validation target rule, a GoF failure in the governing extraction model requires quantitative explanation with demonstrated magnitude match. Not met. However, I note the severity is moderated by the fact that A_FB = 0 on symmetric MC and the chi2 failure at Phase 4a cannot bias a zero result. The concern is forward-looking: if this chi2 persists on data, A_FB^b could be biased. **Action: investigate (residual plot, binning variation), but this is a documented limitation for Phase 4a, not a regression trigger. Classify as A requiring textual investigation, not re-extraction.** |
| 3 | rb_results.json shows WP 10.0 closure pull = 0.97 (PASSES) while AN declares INFEASIBLE | Critical [A2] | A | **A** | The JSON and AN text contradict each other. The critical reviewer's analysis is thorough: the rb_results.json entry (R_b = 0.246, pull = 0.97) does not match the AN's bootstrap description (R_b = 0.280, pull = 0.94). This requires clarification: either the JSON entry is a genuine 60/40 split closure (in which case INFEASIBLE is wrong and must be corrected), or it is a mislabeled bootstrap (in which case the JSON must be fixed). The fixer must identify which and correct the inconsistency. |
| 4 | sigma_d0_form systematic: JSON method says "Scaled from MC statistics" but AN text says "re-running calibration with each form"; magnitude 0.0004 unsupported by cited source | Critical [A1] | A | **B** | The sigma_d0_form systematic (delta_Rb = 0.0004) is subdominant (0.1% of total systematic budget). The conventions rule on uncited constants is clear, but the practical impact is negligible -- even if the true value were 10x larger (0.004), it would not change the total systematic (0.395). The self-contradiction between JSON method field and AN text is a documentation bug, not a physics bug. **Downgrade to B**: fix the JSON/AN contradiction and either derive the magnitude or cite it properly, but this does not block advancement. Cost estimate: ~20 min to clarify. Does not affect physics conclusion at any level. |
| 5 | Angular efficiency systematic for A_FB^b (0.002) has no citation or derivation | Constructive [A2] | A | **B** | The value 0.002 is the second-largest A_FB systematic, representing ~44% of the systematic variance for A_FB. The constructive reviewer correctly flags the uncited-constant rule. However, at Phase 4a where A_FB = 0 on symmetric MC, the systematic evaluation is a structural placeholder -- the actual impact assessment occurs at Phase 4b when the real asymmetry is measured. The 0.002 is borrowed from ALEPH's comparable systematic (~0.002 from their angular acceptance, documented in inspire_433746 Section 6). **Downgrade to B**: add the explicit ALEPH citation with section number and note "to be re-evaluated with data at Phase 4b." This is a documentation gap, not a physics error. Cost: ~15 min. |
| 6 | Table tab:working_points displays DATA counts (N_t = 991,373 > 730,365 MC events) | Critical [A5] | A | **A** | The critical reviewer's arithmetic is unambiguous: 991,373 tagged hemispheres cannot come from 730,365 MC events (max MC N_t ~ 263,000 at 18% tag rate). The table displays data-derived counts. The extraction itself uses N_had = 730,365 (MC) per rb_results.json, suggesting the extraction IS on MC but the table is mislabeled. This is likely a display error (data counts shown for reference alongside MC-derived fractions), not a blinding violation. But the AN text must clarify definitively. **A -- requires clarification that the extraction used MC counts, and the table must be corrected or annotated to distinguish data reference counts from MC extraction inputs.** |
| 7 | OP stability: only 1/4 WPs valid for R_b | Physics [A1] | A | **B** | The stability scan fails (1/4 valid WPs). The document provides 3 documented INFEASIBLE remediation attempts and a concrete Phase 4b mitigation path (multi-WP fit). At Phase 4a with circular calibration, this is an expected structural limitation. The physics reviewer agrees this is not a showstopper requiring regression but requires re-evaluation on data as a blocking gate at Phase 4b. **Downgrade to B**: the finding is correctly documented with INFEASIBLE evidence. Add an explicit Phase 4b blocking-gate commitment in the conclusions. |
| 8 | efficiency_calibration.png: figsize=(30,10), text unreadable at AN rendering | Plot validator [A5] | A (RED FLAG equivalent) | **A** | Plot validator finding based on objective measurement: the figure source is 30x10, rendered at 0.45 linewidth gives ~0.15 linewidth per panel. Text is below readable threshold. The source code was not modified between iterations. This is a mechanical fix (change figsize, regenerate). |
| 9 | F7 kappa consistency: combined A_FB band invisible at AN rendering | Plot validator [A2] | A | **A** | The combined result band (~5 pixels, alpha=0.2) is the primary physics content of this figure. At AN rendering size it will print as a hairline or disappear. The fix is mechanical (zoom y-axis or increase alpha). Source unchanged between iterations. |
| 10 | F2 angular distribution: chi2/ndf = 31.9/8 displayed without context | Plot validator [A1] | A | **B** | The figure shows chi2 = 31.9/8 which is from the origin-only fit (kappa=0.5). The intercept fit (chi2 = 31.9/8 is the SAME as the intercept fit at kappa=0.5 per afb_results.json) -- so the figure IS showing the intercept model. The poor chi2 is a real feature of the data. The figure itself is not incorrect; what is missing is context (either an overlay of the origin-only fit for comparison, or a caption note). This is a presentation issue, not a data error. **Downgrade to B**: add a caption sentence explaining the chi2 context. The figure itself does not contain wrong information. |
| 11 | Phase 3 closure figure: 3-panel 10x10 produces illegible x-tick labels at AN rendering | Plot validator [NA1] | A | **B** | The content of this figure was FIXED (A3 from iteration 1 -- mirrored bar corrected). The readability concern is valid but the physics content is correct and the caption provides all necessary information. The figure is legible at screen resolution and the AN is currently a working document under review, not a journal submission. At Doc 4c (final), figure readability will be re-evaluated. **Downgrade to B**: improve label readability before Doc 4c. |
| 12 | High-scale-factor track bias not quantified (only "small") | Constructive [B1] | B | **B** | Valid finding. The investigation is present but the quantitative conclusion is missing. One sentence with a number is needed. |
| 13 | Multi-WP eps_uds constraint argument assumes unvalidated smoothness | Constructive [B2], Physics (implicit) | B | **B** | Valid. The 20x systematic reduction claim is the central promise for Phase 4b. Adding a caveat sentence acknowledging the assumption is unvalidated at Phase 4a is appropriate. |
| 14 | Data/MC agreement for combined tag distribution unquantified | Constructive [B3] | B | **C** | The data/MC figures show good visual agreement with pull panels. The combined tag distribution (Figure datamc_tag in Phase 3) has a pull panel that provides the quantitative diagnostic. Adding a formal chi2/ndf to the caption is a C-level improvement. The tag distribution enters the extraction only through the efficiency measurement, not directly -- and the efficiency systematic (eps_uds +/-50%) already dwarfs any data/MC shape effect. **Downgrade to C.** |
| 15 | Toy convergence rate 20% raises questions about stat uncertainty | Physics [B1] | B | **B** | Valid concern about boundary effects on the confidence interval. Document the boundary effect explicitly. |
| 16 | eps_c systematic is one-sided | Physics [B2], Critical [B2] | B, B | **B** | Two reviewers agree. The total systematic should note the asymmetric component. |
| 17 | C_b systematic prescription (2x inflation) is ad hoc | Physics [B3] | B | **Subsumed by #1** | The C_b systematic is evaluated at the wrong working point (finding #1). Once #1 is fixed, the prescription must be re-evaluated with correct WP 10.0 values. This finding is subsumed. |
| 18 | No before/after figure for sigma_d0 calibration | Physics [B4] | B | **B** | Valid. This is the key diagnostic for the impact parameter resolution model. |
| 19 | Angular fit chi2 FAIL entries in validation table insufficiently discussed | Physics [B5] | B | **Subsumed by #2** | The chi2 discussion requirement is part of finding #2. |
| 20 | MC normalization to data integral should be more prominently flagged | Physics [B6] | B | **C** | The normalization is stated in Section 3.3. This is adequate for a working document. Promote the note at Doc 4c. |
| 21 | kappa=inf excluded from kappa systematic | Critical [B1] | B | **B** | Valid. Include all 5 kappa values in the systematic calculation. Quick fix. |
| 22 | C_b analytical cross-check uses WP-mismatched values | Critical [B3] | B | **Subsumed by #1** | Follows from the C_b WP mismatch. Will be resolved when #1 is fixed. |
| 23 | Rationale for C_b reference WP 5.0 undocumented | Critical [B4] | B | **Subsumed by #1** | The "reference WP 5.0" choice is the root cause of #1. Once corrected to WP 10.0, this finding is moot. |
| 24 | Stress test results not reported in AN | Critical [B5] | B | **B** | The R_c = 0.14 (pull = 2.46) and C_b = 1.05 (pull = -2.09) stress test failures should be documented. Particularly the C_b = 1.05 failure is informative in the context of finding #1. |
| 25 | eps_uds fraction reported as 99.5% but correct value is ~96% | Critical [B6] | B | **B** | Confirmed by arithmetic: 0.387^2 / 0.395^2 = 96.0%, not 99.5%. The 99.5% likely came from treating eps_c as negligible. Fix the number. |
| 26 | R_c analytical vs toy cross-check absent; 50x discrepancy in dR_b/dR_c | Critical [B7] | B | **B** | The COMMITMENTS.md requires this cross-check. The 50x discrepancy (strategy claimed ~-0.05, systematics show 2.53) must be explained. This is likely because the double-tag extraction amplifies R_c sensitivity through the underdetermined system. Document the explanation. |
| 27 | closure_test_phase4a.png non-square (20x10) | Plot validator [B1] | B | **B** | Valid but non-blocking. Fix at Doc 4c. |
| 28 | Various plot B findings (B2-B11 from plot validator) | Plot validator | B | **C (batch)** | These are annotation readability, color coding, and minor presentation items. None affect physics content. Batch as C for Doc 4c. |

---

## Findings Raised by Arbiter (Missed by All Reviewers)

None. The reviewer panel was thorough. The C_b working-point mismatch (#1) is
the most consequential finding and was caught by the critical reviewer
(hedwig_f66f). The chi2 GoF issue was caught by all three prose reviewers.
The figure issues were caught by the plot validator.

---

## Regression Check

| Trigger | Status | Evidence |
|---------|--------|---------|
| Validation test failure without 3 documented remediation attempts | **NO** | OP stability: 3 attempts documented, INFEASIBLE. WP 10.0 closure: 3 attempts documented (but see finding #3 -- JSON contradicts). Angular chi2: acknowledged, intercept model adopted. |
| Single systematic > 80% of total uncertainty | **YES (documented)** | eps_uds = 96% of systematic variance. Documented with investigation in Appendix A.5 (Precision Investigation). Phase 4b mitigation documented. |
| GoF toy inconsistency | **NO** | No toy-based GoF. The chi2/ndf = 3-4 is from the angular fit, not from toys. |
| > 50% bin exclusion | **NO** | No bins excluded. |
| Tautological comparison as validation | **NO** | The circular calibration is correctly labeled as a self-consistency diagnostic, not a measurement. The closure test uses a 60/40 split with partial independence, correctly documented. |

The C_b WP mismatch (#1) is a genuine physics bug that affects the R_b
extraction result. However, at Phase 4a this is a self-consistency diagnostic
on MC pseudo-data -- the R_b result is already acknowledged as biased (0.280
vs input 0.216) due to circular calibration. Correcting C_b will change the
magnitude of the bias but not the qualitative conclusion. This does NOT
trigger regression to Phase 3 -- it requires a fix-and-re-extract cycle
within Phase 4a scope (update C_b, re-run extraction, update systematic
budget, update AN text).

**No regression triggered.** The fix is within Phase 4a / Doc 4a scope.

---

## Motivated Reasoning Check

1. **"R_b is a self-consistency diagnostic" framing:** Appropriate at Phase 4a.
   The 0.064 residual bias is quantitatively decomposed. However, the C_b
   mismatch (#1) means the decomposition is wrong -- some of the "eps_uds"
   attributed bias may actually be C_b error. The fixer must redo the
   decomposition after correcting C_b.

2. **"Will be addressed in Phase 4b" for eps_uds constraint:** The 20x
   improvement claim is unvalidated. Noted as B (#13). Not dismissing it,
   but the claim must be caveated.

3. **Chi2/ndf = 3-4 "likely reflects bin-level shape differences":** This is
   an unsubstantiated narrative explanation for a GoF failure. The fixer must
   investigate (residual plot, binning variation) even if the Phase 4a result
   (A_FB = 0) is unaffected.

4. **Inflated uncertainties making validation trivial:** The R_b total
   uncertainty (0.396) makes the pull vs ALEPH trivially small (0.16 sigma).
   The document correctly labels this as "uninformative." No inflation
   deception detected.

5. **Independence of calibration:** The circular calibration is the known
   structural issue, honestly documented. No hidden circularity beyond what
   is declared.

---

## Consolidated Fix List (Priority Order)

### Category A (Must Resolve -- Blocks PASS)

**A1. C_b working-point mismatch (CRITICAL).** [Source: Critical A3]
- Correct `systematics.json` C_b_nominal from 1.1786 (WP 5.0) to 1.5372 (WP 10.0)
- Re-run the R_b extraction at WP 10.0 with correct C_b
- Recompute C_b systematic using WP 10.0 data-MC difference (0.031), giving
  delta_Rb(C_b) ~ 0.062 (6x larger than current 0.010)
- Update the total systematic budget
- Redo the bias decomposition (Section 8.1) with corrected C_b contribution
- Update all downstream numbers (abstract, results table, comparison section)

**A2. Intercept chi2/ndf investigation.** [Source: Physics A2, Critical A4, Constructive A1]
- Plot Q_FB residuals vs cos(theta) to identify the pattern
- Test whether binning variation (6, 8, 10, 12 bins) changes chi2
- Report whether the chi2 excess is edge-concentrated or uniform
- If the failure cannot be explained, declare it as a method limitation with
  explicit forward reference to Phase 4b investigation
- Minimum deliverable: one diagnostic figure + one paragraph of investigation

**A3. WP 10.0 closure JSON vs AN contradiction.** [Source: Critical A2]
- Determine whether rb_results.json closure_test[threshold=10.0] is:
  (a) the 60/40 independent split, or (b) the bootstrap
- If (a): correct the AN -- WP 10.0 closure PASSES, remove INFEASIBLE
- If (b): fix the JSON label to "bootstrap (not independent)" and reconcile
  the parameter values (R_b = 0.246 vs AN's 0.280; pull = 0.97 vs AN's 0.94)
- Either outcome requires updating Section 6.4 and Table tab:validation_summary

**A4. Table tab:working_points data vs MC count clarification.** [Source: Critical A5]
- Confirm the extraction used MC counts (N_had = 730,365 from rb_results.json)
- Correct the table: either show MC counts for the extraction, or clearly
  annotate that data counts are shown for reference while the extraction
  used MC values
- Add a sentence to Section 4.3 distinguishing data and MC count sources

**A5. efficiency_calibration.png: fix figsize and regenerate.** [Source: Plot validator A5]
- Change figsize=(30,10) to three separate 10x10 figures, or to a properly
  scaled 3-panel composite with adequate text size
- Regenerate and restage into analysis_note/figures/

**A6. F7 kappa consistency: combined band visibility.** [Source: Plot validator A2]
- Zoom y-axis to the data region (e.g., [-0.015, +0.015]) and show ALEPH as
  an off-plot annotation, OR increase alpha and use drawn lines instead of
  filled span
- Regenerate and restage

### Category B (Must Fix Before PASS)

**B1.** sigma_d0_form systematic: clarify JSON method vs AN text contradiction;
add proper citation or derivation for magnitude. [Critical A1, downgraded]

**B2.** Angular efficiency systematic for A_FB (0.002): add ALEPH citation
(inspire_433746, Section 6) with note "to be re-evaluated at Phase 4b."
[Constructive A2, downgraded]

**B3.** OP stability: add explicit Phase 4b blocking-gate commitment in
conclusions. [Physics A1, downgraded]

**B4.** Include kappa=infinity in kappa systematic calculation; report
revised delta_AFB. [Critical B1]

**B5.** eps_c one-sided systematic: note in budget table that eps_c is
one-sided and total systematic has asymmetric component. [Physics B2, Critical B2]

**B6.** eps_uds fraction: correct 99.5% to ~96% (variance fraction) or
~98% (linear fraction). Apply consistently. [Critical B6]

**B7.** R_c analytical cross-check: provide dR_b/dR_c from double-tag formula.
Explain the 50x discrepancy with strategy estimate. [Critical B7]

**B8.** Stress test results: report R_c = 0.14 and C_b = 1.05 failures in
validation table or dedicated subsection. [Critical B5]

**B9.** Quantify high-scale-factor track bias contribution with a number.
[Constructive B1]

**B10.** Multi-WP smoothness argument: add caveat that assumption is
unvalidated at Phase 4a. [Constructive B2]

**B11.** Toy convergence rate boundary effect: document explicitly. [Physics B1]

**B12.** Before/after figure for sigma_d0 calibration. [Physics B4]

**B13.** F2 angular distribution: add caption context for chi2 = 31.9/8
(explain intercept model, note this is a known limitation). [Plot validator A1, downgraded]

**B14.** Phase 3 closure figure: improve label readability. [Plot validator NA1, downgraded]

**B15.** closure_test_phase4a.png: fix to square figsize. [Plot validator B1]

### Category C (Apply Before Commit, No Re-review)

- Data/MC chi2 for combined tag caption (Constructive B3, downgraded)
- MC normalization note promotion (Physics B6, downgraded)
- Plot validator B2-B11 batch (annotation readability, color coding)
- Physics C1-C5, Constructive C1-C7, Critical C1-C4
- Rendering C items (whitespace, figure sizing inconsistency, stale filename)
- Closure figure provenance filename (Registry-1 from plot validator)

---

## Verdict

**ITERATE.**

Six Category A findings block advancement. The most critical is **A1 (C_b
working-point mismatch)**, which is a genuine physics bug affecting the
primary R_b extraction, its systematic budget, and the bias decomposition.
This requires re-extraction and propagation through all downstream numbers.

The figure fixes (A5, A6) are mechanical but were not applied in the
previous iteration despite being flagged. The fixer must prioritize these
alongside the C_b fix.

**Iteration count: 2.** This is the second iteration. The warn threshold
is at iteration 3. The fix list is focused: 6 A items (1 requiring
re-extraction, 2 requiring figure regeneration, 3 requiring text/JSON
clarification) and 15 B items (mostly text additions and minor corrections).
A focused fix cycle should resolve all A items. The orchestrator should
ensure the fixer addresses ALL A items and at least the first 10 B items
before the next review.

**Estimated fix effort:** ~3 hours agent time (1 hour for C_b re-extraction
and propagation, 30 min for figure fixes, 30 min for chi2 investigation,
1 hour for remaining A+B text fixes).

---

## Reviewer Diagnostic

### Physics (gunnar_8836)
- Thorough figure inspection covering all 24 figures with substantive
  physics commentary. Strong on narrative consistency and statistical
  methodology. Good resolving power assessment.
- Caught the chi2/ndf issue (A2) and OP stability (A1).
- Did NOT catch the C_b working-point mismatch -- this is the most
  consequential finding and falls squarely within the physics reviewer's
  scope (checking that correction values correspond to the operating point).
  **COVERAGE GAP on C_b.**
- Did NOT catch the data vs MC count ambiguity in the working points table.
  **COVERAGE GAP on input provenance.**
- Overall: strong review with two significant gaps.

### Critical (hedwig_f66f)
- Exceptional. Caught the C_b mismatch (A3), the closure JSON contradiction
  (A2), the data count ambiguity (A5), the sigma_d0_form contradiction (A1),
  and the chi2 failure (A4). Five Category A findings, all substantiated
  with JSON evidence and arithmetic.
- The eps_uds fraction error (B6) demonstrates careful numerical verification.
- The dR_b/dR_c discrepancy (B7) is a valuable catch.
- Correctly identified the stress test failures not reported in the AN (B5).
- No coverage gaps identified.

### Constructive (isolde_f26f)
- Thorough fresh review with corpus queries. Good use of DELPHI and ALEPH
  references to contextualize the chi2/ndf finding.
- Caught the angular efficiency citation gap (A2) and the chi2 investigation
  need (A1).
- Cross-phase concern review is well-structured.
- Depth check table is useful.
- Did NOT independently catch the C_b mismatch -- this affects the
  constructive review's "Does the measurement discriminate?" assessment.
  **Partial COVERAGE GAP** -- the constructive role focuses on improvement
  opportunities, not numerical verification, so this is understandable.

### Plot Validator (kenji_3c08)
- Thorough registry check, code lint, and visual inspection of all figures.
- Correctly identified 3 unfixed A findings from iteration 1 (A1, A2, A5)
  and 1 new A (NA1 -- closure panel compression).
- MD5 verification of the closure figure provenance is excellent practice.
- Cross-figure consistency analysis is valuable.
- Did NOT catch the C_b value mismatch visible in the hemisphere_correlation
  figure (C at WP 10 ~ 1.55) vs the extraction value (1.179) -- this is at
  the boundary of the plot validator role (they check visual quality, not
  parameter consistency). **Not a coverage gap** for this role.

### Rendering (renata_120f)
- All v1 A and B findings verified as FIXED. Thorough cross-reference check.
- Correctly passed the document. No gaps.

### BibTeX (ada_4351)
- Comprehensive validation of all 12 cited keys and 15 bib entries.
- Correctly noted 3 unused entries. No gaps.

---

*Arbiter: magnus_6181 | Date: 2026-04-02 | Iteration 2 of Doc 4a review*
*Verdict: ITERATE (6A, 15B, batch C)*
