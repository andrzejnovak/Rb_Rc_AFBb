# Arbiter Adjudication -- Doc 4a Analysis Note

**Arbiter:** zelda_65ac
**Date:** 2026-04-02
**Artifact:** `analysis_note/ANALYSIS_NOTE_doc4a_v1.tex` (.pdf)
**Review panel:** 6 reviewers (physics, critical, constructive, plot validator, rendering, BibTeX)

---

## Executive Summary

Six reviewers produced a total of 8+8+2+5+5+2 = 30 Category A findings,
7+8+5+10+2+8 = 40 Category B findings, and 3+5+10+3+1+3 = 25 Category C
findings. After deduplication and adjudication, I identify **17 unique
Category A findings**, **16 unique Category B findings**, and Category C
items deferred to the fixer. The AN is thorough and honest but has
significant gaps in validation coverage (no closure at WP 10.0, no
remediation attempts for OP stability failure, missing intercept-model
chi2) and several mechanical defects (A_FM typo, broken cross-ref,
orphaned floats, unreadable multi-panel figures).

**Verdict: ITERATE**

---

## Structured Adjudication Table

### Category A -- Must Resolve (Blocks Advancement)

| # | Finding | Sources | Their Cat | Final Cat | Rationale |
|---|---------|---------|-----------|-----------|-----------|
| 1 | **A_FM^b typo (3 occurrences)** -- lines 143, 1845, 2215 use `\mathrm{FM}` instead of `\mathrm{FB}` | Constructive A1, Critical A8, Rendering R4 | A, A, A | **A** | All three reviewers agree. Wrong observable name in abstract, conclusions, and appendix. Trivial fix but factual error. |
| 2 | **No independent closure test at WP 10.0** (primary operating point) | Physics F8, Critical A1 | A, A | **A** | Both agree. The primary extraction point was never validated by independent closure. `conventions/extraction.md` item 1 is explicit. This is the single most important validation gap. |
| 3 | **Operating point stability FAIL without 3 remediation attempts** -- only 1/4 WPs valid, no attempts documented to make more WPs work | Physics F5, Critical A4 | A, A | **A** | Both agree. The methodology requires 3 documented remediation attempts or an INFEASIBLE declaration. Neither exists. The deferral to Phase 4b is not a remediation. |
| 4 | **Circular calibration bias (0.064) unexplained quantitatively** -- R_b = 0.280 vs input 0.216, no breakdown by source | Physics F4, Critical A3 | A, A | **A** | Both agree. The 30% residual bias is acknowledged but not decomposed. A toy study varying assumed R_b input is needed to demonstrate the bias is understood. |
| 5 | **Per-kappa A_FB^b table reports chi2/ndf from the REJECTED origin-only fit model** -- intercept-inclusive chi2 never reported anywhere | Physics F9, Critical A7, Constructive B1 | B/B/B, A, B | **A** | Critical reviewer correctly escalated this to A. The governing extraction model's fit quality is unquantified in the entire AN. Reporting chi2 from a rejected model in the primary results table misleads readers. I side with Critical: this is A because the accepted model's chi2 is completely absent. |
| 6 | **delta_QED value uncited; systematic absent from Table 8** -- appears in Eq. 8 without a value or citation | Constructive A2 | A | **A** | Single reviewer, but verified against conventions: "any uncited numeric constant is Category A" per CLAUDE.md. delta_QED appears in a governing equation. Valid finding. |
| 7 | **kappa=infinity absent from per-kappa results table** -- abstract claims 5 kappas, Table 8.1 has 4 rows, systematic evaluation uses 4 kappas | Critical A5 | A | **A** | Single reviewer. Verified: [D5] commits to kappa={0.3, 0.5, 1.0, 2.0, infinity}. The kappa consistency chi2 uses ndf=4 (consistent with 5 kappas), but the results table omits one. Either add the row or formally document the exclusion. |
| 8 | **COMMITMENTS.md not updated for Phase 4a** -- all systematic checkboxes still [ ] despite completion | Critical A6 | A | **A** | Single reviewer. Verified: COMMITMENTS.md must reflect Phase 4a status. An unchecked COMMITMENTS.md makes regression audit impossible. The orchestrator checklist explicitly requires this. |
| 9 | **Parameter sensitivity table missing** -- COMMITMENTS.md binding; `conventions/extraction.md` item 2 mandatory | Critical A6 (sub-item), Constructive B3 | A, B | **A** | Two reviewers flagged this. The sensitivity table (|dR_b/dParam| * sigma_param) is a convention requirement and a COMMITMENTS.md binding. Its absence is A. |
| 10 | **Unresolved cross-reference `\ref{sec:jetcharge}` renders as `??`** on PDF p. 9 | Rendering R1 | A | **A** | Single reviewer. Verified: a visible `??` in the body text is an unambiguous rendering defect. Trivial fix. |
| 11 | **3 orphaned figures** (Figs. 3, 6, 10) -- `\label` exists but no `\ref` from body prose | Rendering R2 | A | **A** | Single reviewer. Orphaned figures are unreferenced floats that a reader encounters without context. Per rendering review spec, this is A. Each needs one sentence of prose referencing it. |
| 12 | **7 orphaned tables** (Tabs. 3, 5, 11, 17, 21, 22, 24) -- same issue | Rendering R3 | A | **A** | Same reasoning as #11. Seven tables appear without a single `\ref` from the body. |
| 13 | **Phase 3 closure panel (a) rendering bug** -- both R_b bars at y~0.83 while annotation says R_b = 0.0000 | Plot validator A3 (RED FLAG) | A | **A** | Plot validator RED FLAG -- cannot downgrade. Either the figure has a rendering bug (y-axis does not start at 0, making the bar at 0.0 invisible) or the mirrored-significance closure test genuinely returns R_b = 0.83 instead of 0. Both interpretations require investigation and figure regeneration. |
| 14 | **Phase 3 closure panel (b) chi2/ndf annotation discrepancy** -- figure says "1144", AN caption says "11,447" (10x mismatch) | Plot validator A4 (RED FLAG) | A | **A** | Plot validator RED FLAG -- cannot downgrade. A 10x numerical discrepancy between a figure annotation and its caption is a factual error. One of them is wrong. |
| 15 | **Truncated x-axis label in Fig. 11 right panel** -- "W" instead of "Working point" | Rendering R8 | A | **A** | Single reviewer. A truncated axis label in a key diagnostic figure is a rendering defect requiring figure regeneration. |
| 16 | **Efficiency calibration figure unreadable at AN rendering size** -- 3-panel 30x10 composite, each panel ~0.15 linewidth, text illegible | Plot validator A5 | A | **A** | Plot validator finding, confirmed by rendering review (R6 addresses sizing inconsistency). At 0.15 linewidth per panel, axis labels and tick marks are unreadable at print resolution. Must be split into three separate figures or properly composited per appendix-plotting.md. |
| 17 | **F2 (Q_FB angular fit) shows chi2/ndf = 31.9/8 without the better-fitting intercept model** -- reader sees a manifestly bad fit with no resolution shown | Plot validator A1, Physics F9 | A, B | **A** | Plot validator A1 is a physics diagnostic flag. The figure shows only the rejected (origin-only) fit model. The intercept-inclusive fit that "substantially improves chi2" is never shown in any figure. The reader sees a bad fit and must infer the fix from prose. The figure should show the accepted model or annotate both chi2 values. |

### Category B -- Must Fix Before PASS

| # | Finding | Sources | Their Cat | Final Cat | Rationale |
|---|---------|---------|-----------|-----------|-----------|
| 18 | **C_c and C_uds values unreported** -- appear in double-tag formula but never stated | Constructive B2 | B | **B** | Required inputs to the extraction formula must be reported for reproducibility. |
| 19 | **Closure test PASS label inconsistent with partial-independence caveat** in Section 12.1 | Constructive B4 | B | **B** | Table 14 says PASS; Section 12.1 says independence is only partial. Internal inconsistency. One-line fix to Table 14 caption. |
| 20 | **eps_c solver failure at +30% -- one-sided systematic not adequately motivated** | Constructive B5, Critical B3 | B, B | **B** | Both agree. Solver failure at a 1-sigma variation indicates the extraction is at the physical boundary. The one-sided treatment needs explicit motivation and acknowledgment that the upper uncertainty is effectively unbounded. |
| 21 | **sigma_d0_form systematic has no published measurement backing** -- source is internal STRATEGY.md, not a cited paper | Critical A2 | A | **B** | Critical reviewer rated A. I downgrade to B with reasoning: the flat-estimate exception in conventions requires a "cited measurement" backing the magnitude. STRATEGY.md is internal. However, the systematic is subdominant (0.00040 vs total 0.395); the fix is to either cite a published value or re-derive via propagation. This does not change the physics conclusion. The cost to fix is ~30 min. Retaining as B because it is subdominant and the overall systematic budget is dominated by eps_uds at 99.5%. |
| 22 | **sigma_d0 scale factors up to 7.6x -- high-scale-factor tracks not investigated for bias** | Critical B1 | B | **B** | Valid concern. Tracks with 7.6x miscalibrated impact parameters could introduce tagging bias. A sentence investigating or cross-checking their impact is needed. |
| 23 | **C_b systematic (0.010) not cross-checked against analytical derivative** | Critical B2 | B | **B** | The derivative delta_R_b/delta_C_b should be reported to verify the propagation. Quick calculation. |
| 24 | **Closure at WP 9.0: marginal pass (pull = 1.93) with only 305/1000 valid toys** -- uncertainty on pull not reported | Critical B4 | B | **B** | The pull of 1.93 +/- ~0.08 (from finite toy statistics) is within one sigma of the 2.0 threshold. Report the uncertainty and note the marginal pass. |
| 25 | **r_b and r_c undefined in gluon correction formula (Eq. 4.8)** | Critical B5 | B | **B** | Values used in a published equation must be stated. If r_b = r_c = 1, say so explicitly. |
| 26 | **Ambiguity: are f_s, f_d in R_b extraction from data or MC pseudo-data?** | Critical B6 | B | **B** | Important clarification for Phase 4a. If data f_s/f_d are used, this is premature unblinding. Must state explicitly which source is used. |
| 27 | **Validation table "FAIL (fixed w/ intercept)" without post-fix chi2** | Critical B7 | B | **B** | Related to finding #5 but specifically about Table 6.1 (validation summary, not results table). The validation table claims FAIL is fixed but does not show the evidence. |
| 28 | **D12b downscoping risk: four-quantity fit never validated on MC** | Critical B8 | B | **B** | The downscoping was formally accepted, but Phase 4b now carries implementation + validation simultaneously. Add a risk note. |
| 29 | **BibTeX: ALEPH:opendata missing author and year** | BibTeX A1 | A | **B** | BibTeX validator rated A. I downgrade to B: the missing metadata on a @misc entry does not affect physics content. The fix is a 1-minute edit. Still must be fixed before PASS. |
| 30 | **BibTeX: LEP:gcc missing author field** | BibTeX A2 | A | **B** | Same reasoning as #29. Missing author on a bibliography entry. 1-minute fix. |
| 31 | **BibTeX: LaTeX math in 8 entry titles** | BibTeX B (8 entries) | B | **B** | Formatting spec violation. Could cause compilation failures in strict processors. Batch fix, ~15 min. |
| 32 | **Large whitespace gaps** on pages 4, 5, 12, 14, 36 | Rendering R5 | B | **B** | Presentation quality. The page count is exactly 50 (minimum); compressing whitespace could drop below threshold. Fix carefully. |
| 33 | **F7 (kappa consistency): combined result band nearly invisible at AN rendering size** | Plot validator A2 | A | **B** | Plot validator rated A. I downgrade to B with reasoning: the figure correctly represents the physics (MC has no asymmetry). The combined band's invisibility is a presentation issue, not a physics error. The caption states the numerical values. However, the primary result being sub-pixel is a genuine readability problem. Must be fixed (zoom y-axis or increase band width) but does not block physics correctness. |

### Category C -- Applied Before Commit (No Re-Review)

Category C items are numerous (25+ across all reviews). Key ones for the fixer:

- Constructive C1-C10 (post-intercept chi2 in prose, figure captions quantify agreement, eps_uds 50% variation motivation, WP 10.0 selection criterion, DELPHI uncertainty notation, etc.)
- Critical C1-C5 (rounding inconsistency, MC event count 771K vs 7.8M, kappa=inf in systematic, C_b 2x inflation citation, kappa consistency uninformative on symmetric MC)
- Plot validator C1-C3 (cutflow mixed units, low-N_ch pulls, empty-bin pulls for kappa=inf)
- BibTeX C1-C3 (orphaned entries: ALEPH:gbb, DELPHI:AFBb, DELPHI:AFBb:2)
- Rendering R7 (tbd markers, expected for 4a)
- Plot validator B-level items that are presentation improvements (stability scan naming, annotation legibility, structured pull documentation, plot range truncation, d0 comb structure, C_b ALEPH WP annotation)

These are all legitimate improvements. The fixer should apply them as time permits after resolving all A and B items.

---

## Dismissals

| # | Finding | Source | Dismissed? | Rationale |
|---|---------|--------|------------|-----------|
| -- | Critical A2 (sigma_d0_form no cited measurement) | Critical | Downgraded A -> B (#21) | The systematic is subdominant (0.0004 vs total 0.395). The conventions exception requires a cited measurement, but the impact on the physics conclusion is nil. Cost to fix: ~30 min (cite a value or re-propagate). Does not affect the result. Will be re-evaluated at Phase 4b when eps_uds is constrained and this becomes relatively more important. |
| -- | BibTeX A1, A2 (missing fields) | BibTeX | Downgraded A -> B (#29, #30) | Missing BibTeX metadata does not affect physics. 2-minute fix. Still required before PASS. |
| -- | Plot validator A2 (F7 band invisible) | Plot validator | Downgraded A -> B (#33) | Presentation issue, not physics error. The numerical result is correctly stated in caption and text. The band invisibility needs fixing but is not a physics correctness blocker. |

All other findings are accepted at the reviewer's category or escalated. No findings are dismissed outright -- every finding from every reviewer appears in the table above or in the Category C list.

---

## Regression Check

Independently evaluating regression triggers (methodology 06-review.md, Section 6.7):

| Trigger | Status | Evidence |
|---------|--------|----------|
| Validation test failure without 3 documented remediation attempts? | **YES** | Operating point stability fails (1/4 valid). Zero remediation attempts documented. Independent closure at WP 10.0 not performed. |
| Single systematic > 80% of total uncertainty? | **YES** | eps_uds contributes 99.5% of R_b total systematic. Documented and investigated (Appendix F precision decomposition). Investigation exists but the underlying issue (unconstrained eps_uds) is structural and deferred to Phase 4b multi-WP fit. |
| GoF toy inconsistency? | No | Toy convergence is low (200/1000 at WP 10.0, 305/1000 at WP 9.0) but this is documented as a known consequence of the underdetermined system, not a GoF failure. |
| >50% bin exclusion? | No | Not applicable (counting extraction, not binned fit). |
| Tautological comparison presented as validation? | **Partial** | The closure test shares calibration assumptions (R_b = SM input) between derivation and validation sets. This is acknowledged in Section 12.1 but Table 14 does not caveat it. Addressed as finding #19. |

**Regression assessment:** The validation test failures (OP stability, missing WP 10.0 closure) are structural limitations of the Phase 4a circular calibration approach. They do NOT require regression to an earlier phase -- the Phase 4a infrastructure is correctly implemented; the failures reflect the underdetermined calibration system that is expected to improve with data (Phase 4b).

However, the required remediation attempts (finding #3) and closure test at WP 10.0 (finding #2) must be documented as INFEASIBLE (with 3 attempts) or performed. This is a Doc 4a fix, not a phase regression.

The eps_uds dominance (99.5%) is a real structural issue. The precision investigation (Appendix F) provides the required investigation. The multi-WP fit is the documented path forward. No regression trigger is met that would require returning to Phase 3 or earlier.

**Regression verdict: No phase regression required.** The findings are addressable within the Doc 4a iteration cycle.

---

## Motivated Reasoning Check

**R_b = 0.280 +/- 0.396:** The result "agrees with SM" only because the uncertainty is enormous (183% of the SM value). The central value deviates by 0.064 from the SM input -- a 30% residual bias. The AN is HONEST about this: it labels the result a "self-consistency diagnostic," not a measurement. The analysis does not claim a physics result for R_b at Phase 4a. **No motivated reasoning detected for R_b.**

**A_FB^b = -0.0001 +/- 0.0022 (stat):** Consistent with zero on symmetric MC. This is the expected result. The kappa consistency (chi2/ndf = 0.71/4, p = 0.95) is suspiciously good, but on symmetric MC where A_FB = 0 by construction, perfect consistency is expected. **No motivated reasoning detected for A_FB^b.**

**"The multi-WP fit will reduce eps_uds from 0.387 to ~0.02":** This is a projection, not a demonstration. The Phase 4a infrastructure provides no evidence that the multi-WP fit works (only 1/4 WPs yield valid extractions). The claim is hedged ("estimate," not "demonstrated") and the risk is documented. However, the 20x improvement claim has not been tested even with a toy study. This is addressed by finding #4 (toy study for multi-WP bias resolution).

**Inflated uncertainties making validation trivial:** The total R_b uncertainty (0.396) is so large that any pull test trivially passes. However, the AN does not present any pull test for R_b -- it correctly notes the result is a diagnostic. For A_FB^b, the uncertainties are comparable to ALEPH's published precision, so no inflation concern applies.

**Overall: The AN is unusually forthright.** No motivated reasoning or self-serving narrative detected. The main risk is deferred to Phase 4b (multi-WP fit), which is appropriate for Phase 4a scope.

---

## Reviewer Diagnostic

### Physics (wolfgang_8bad)
- **Role fulfillment:** Excellent. Thorough figure-by-figure assessment (24 figures individually reviewed), quantitative physics judgment on all key results, proper identification of the circular calibration problem, operating point stability failure, and closure test gap. Correctly identified the narrative consistency (bad inputs produce bad result, honestly presented).
- **Coverage gaps:** Did not flag the kappa=infinity absence from the results table (Critical A5). Did not flag the COMMITMENTS.md update issue (Critical A6). These are at the boundary of the physics reviewer's role (more critical/constructive territory), so this is a minor gap.
- **Quality:** HIGH. The physics reviewer operated as a genuine senior PI reviewer. All 14 findings are well-motivated.

### Critical (valentina_2dba)
- **Role fulfillment:** Excellent. Systematic JSON-vs-AN cross-check (Pass 1), convention coverage audit, COMMITMENTS.md traceability, adversarial probing, competing-group question. Caught the f_s/f_d data-vs-MC ambiguity (B6) that no other reviewer noticed. Caught the kappa=infinity gap (A5).
- **Coverage gaps:** None identified. The critical reviewer was the most comprehensive.
- **Quality:** HIGH. The critical review is the backbone of this review cycle.

### Constructive (odette_aaf4)
- **Role fulfillment:** Good. Cross-phase concern re-checks (CP1-CP4 all resolved or partially resolved), depth check per section, corpus cross-checks, honest framing assessment. Correctly identified delta_QED (A2) and C_c/C_uds (B2) gaps that other reviewers missed.
- **Coverage gaps:** Did not flag the f_s/f_d data-vs-MC ambiguity. Did not flag COMMITMENTS.md update status. These fall more in the critical reviewer's domain.
- **Quality:** HIGH. Well-structured review with actionable fixes.

### Plot Validator (jasper_5871)
- **Role fulfillment:** Thorough. Every figure individually reviewed with minimum 3-sentence descriptions. Code lint performed. Cross-figure consistency analysis performed (5 cross-checks). RED FLAG on closure panel rendering bug (A3) is the most important finding from any reviewer -- if the closure test genuinely returns R_b = 0.83 instead of 0, this is a fundamental validation failure.
- **Coverage gaps:** Did not quantify structured pull patterns (B6, B7) with chi2/ndf or KS p-values. The "structured pull" findings are qualitative descriptions of visual patterns without numerical backing. This is a minor gap given the visual review mandate.
- **Quality:** HIGH. The RED FLAG findings (A3, A4) are the most critical in the entire review.

### Rendering (quentin_b524)
- **Role fulfillment:** Good. Compilation status verified, cross-reference completeness checked, orphaned figures/tables identified (R2, R3), figure rendering assessed. The orphaned floats finding (10 items total) is a significant contribution.
- **Coverage gaps:** Did not flag the closure panel rendering bug (A3 from plot validator) -- this is within scope (figure rendering assessment) but the rendering reviewer may not have inspected figure content at the same level. Did not flag the efficiency calibration readability issue as strongly as the plot validator.
- **Quality:** GOOD. Comprehensive on structural/mechanical issues.

### BibTeX Validator (ulrich_aeb3)
- **Role fulfillment:** Complete. All 15 entries validated for field completeness, title formatting, arXiv IDs, INSPIRE cross-references, and spot-checks against known literature.
- **Coverage gaps:** None within scope. The orphaned entries (C1-C3) are correctly flagged as suggestions.
- **Quality:** HIGH within its specialized scope.

---

## Fixer Priority List

The fixer agent must address ALL Category A and B findings. Priority order:

### Priority 1: Category A (must resolve, ordered by impact)

1. **#2 -- Closure test at WP 10.0.** Run the independent closure test at WP 10.0, or document INFEASIBLE with 3 remediation attempts. This is the highest-priority physics gap.

2. **#3 -- OP stability: 3 remediation attempts.** Document 3 attempts to make additional WPs valid (e.g., vary alpha scan range, relax constraints, use alternative calibration). If all fail, document INFEASIBLE.

3. **#4 -- Circular calibration bias decomposition.** Run a toy study: vary assumed R_b input from 0.15 to 0.25, extract R_b at each, demonstrate the bias is understood. Alternatively, decompose the 0.064 bias by source (which external input drives it).

4. **#13 -- Phase 3 closure panel (a) rendering bug (RED FLAG).** Investigate whether the mirrored-significance closure test genuinely returns R_b = 0 or 0.83. If rendering bug, fix the figure (ensure y-axis starts at 0). If genuine failure, this escalates to a Phase 3 regression.

5. **#14 -- Phase 3 closure panel (b) chi2/ndf discrepancy (RED FLAG).** Verify the correct value (1144 or 11447) and fix whichever is wrong.

6. **#5 + #17 -- Add intercept-inclusive chi2/ndf to Table 13 and Figure F2.** Re-run intercept fits, extract chi2/ndf at each kappa, add column to Table 13. For F2, overlay the intercept-inclusive fit or replace the origin-only curve.

7. **#7 -- Add kappa=infinity row to Table 8.1** with A_FB^b, delta_b, slope, and chi2/ndf.

8. **#9 -- Parameter sensitivity table.** Add a 5-row table: param, sigma_param, |dR_b/dParam|, product, 5x-stat flag.

9. **#6 -- delta_QED: cite value, add to Table 8.**

10. **#1 -- A_FM^b typo.** Replace all 3 instances of `\mathrm{FM}` with `\mathrm{FB}`.

11. **#10 -- Fix `\ref{sec:jetcharge}`.** Add `\label{sec:jetcharge}` to the appropriate section or change the \ref target.

12. **#11 + #12 -- Add prose references for 3 orphaned figures and 7 orphaned tables.** One sentence each in surrounding prose.

13. **#8 -- Update COMMITMENTS.md** to reflect Phase 4a status.

14. **#15 -- Regenerate efficiency_calibration.pdf** with sufficient bottom margin (truncated x-axis label).

15. **#16 -- Split or recomposite efficiency calibration figure** for readability at AN rendering size.

### Priority 2: Category B (must fix, ordered by impact)

16. **#26 -- Clarify f_s/f_d source** (data vs MC pseudo-data) in Section 7.1 and 8.1.

17. **#20 -- eps_c solver failure motivation.** Add boundary analysis sentence to Section 5.4.

18. **#18 -- Report C_c and C_uds values** in Table 5 or nearby text.

19. **#25 -- State r_b and r_c values** in Eq. 4.8.

20. **#19 -- Closure test PASS label caveat** in Table 14.

21. **#27 -- Validation table post-fix chi2** in Table 6.1.

22. **#24 -- Pull uncertainty at WP 9.0** (305 valid toys).

23. **#23 -- C_b propagation derivative cross-check.**

24. **#22 -- sigma_d0 high-scale-factor tracks investigation.**

25. **#21 -- sigma_d0_form: cite a published measurement or re-derive.**

26. **#28 -- D12b risk note** for Phase 4b outlook.

27. **#29 + #30 -- BibTeX missing fields** (ALEPH:opendata, LEP:gcc).

28. **#31 -- BibTeX title formatting** (8 entries, remove LaTeX math).

29. **#32 -- Whitespace gaps** (careful not to drop below 50 pages).

30. **#33 -- F7 combined band visibility** (zoom y-axis or increase band width).

### Priority 3: Category C

Apply all Category C items after A and B are resolved. No re-review needed.

---

## Verdict

**ITERATE**

17 Category A findings and 16 Category B findings must be resolved. The AN cannot advance to Doc 4b review in its current state.

The most critical cluster is findings #2, #3, #4 (physics validation gaps: no WP 10.0 closure, no OP stability remediation, unexplained circular bias). These require either running additional analysis (closure test, toy study) or documenting INFEASIBLE with 3 attempts.

The RED FLAG findings (#13, #14) from the plot validator require immediate investigation -- if the Phase 3 closure test genuinely failed (R_b = 0.83 on mirrored data), this triggers a Phase 3 regression.

The remaining A findings are mechanical LaTeX/rendering fixes (typo, cross-ref, orphaned floats, figure regeneration) that are straightforward but numerous.

No phase regression is triggered at this time. All findings are addressable within the Doc 4a iteration cycle, contingent on the RED FLAG investigation (finding #13) confirming a rendering bug rather than a genuine closure failure.

---

*Arbiter: zelda_65ac | Date: 2026-04-02*
