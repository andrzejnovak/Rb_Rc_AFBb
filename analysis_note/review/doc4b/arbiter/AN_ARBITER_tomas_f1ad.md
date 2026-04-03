# Arbiter Adjudication — Doc 4b v1

**Session:** tomas_f1ad
**Date:** 2026-04-02
**Artifact:** ANALYSIS_NOTE_doc4b_v1.tex / .pdf (63 pages)
**Reviews adjudicated:** 6 (physics, critical, constructive, plot validation, rendering, BibTeX)

---

## Executive Assessment

The Doc 4b AN is fundamentally sound. The physics is honest: the R_b
extraction validates the method on real data, the A_FB^b suppression is
correctly diagnosed with a clear Phase 4c remediation path, and the
document does not hide its limitations. The critical reviewer explicitly
notes this honesty.

The dominant problem across all reviews is **stale values from the
doc4a-to-doc4b update cycle**. Multiple reviewers independently found the
same underlying issues (covariance appendix, closure pull values, eps_b
values, field citations) -- these are ONE systematic failure (incomplete
update pass), not 15 independent problems. The fixer needs ONE thorough
numbers-consistency sweep, not 15 separate fixes.

The figure quality issues from the plot validator are real but mechanical:
axis labels, fontsize, missing pull panels, experiment labels. These are
code fixes in `plot_phase4b.py`, not physics issues.

No regression to an earlier inference phase is triggered. All findings
are editorial/consistency issues within Doc scope.

---

## Structured Adjudication Table

### Group 1: Stale Values (doc4a residuals -- ONE consistency sweep)

These are all manifestations of the same root cause: the doc4a-to-doc4b
update cycle left stale pre-fix values in per-section tables, appendices,
and inline citations while updating the summary tables. Deduplicated into
a single fix action.

| # | Finding | Source(s) | Their Cat | Final Cat | Rationale |
|---|---------|-----------|-----------|-----------|-----------|
| 1 | Covariance matrix App B stale (3.6x wrong) | Critical F1, Constructive A2 | A, A | **A** | Two reviewers agree. JSON confirms discrepancy. The covariance appendix has pre-C_b-fix values. One fix: regenerate from JSON or mark as "Phase 4a only, Phase 4b deferred to Doc 4c." |
| 2 | Closure WP 9.0 pull = 1.03 in prose/table vs 1.93 in JSON/figure | Critical F2 | A | **A** | JSON = 1.93. Prose and Table 12 say 1.03. Stale value. Update to 1.93. |
| 3 | WP 10.0 closure claimed (pull=1.06, PASS) with no JSON evidence | Critical F3 | A | **A** | No JSON entry for WP 10.0 closure. Either the test was never run or the result was lost. Remove the claim or run the test and record it. |
| 4 | Corrupted corrections: Table 12 says 5/6, JSON+Table 8 say 4/6 | Critical F4 | A | **A** | Stale value in validation summary table. Fix to 4/6. |
| 5 | eps_b at WP 10.0: three values (0.238, 0.151, 0.132) | Critical F5 | A | **A** | Three locations, three numbers. Identify the correct current value from JSON; update all locations. |
| 6 | R_b.value field citation 0.2798 vs JSON 0.3099 | Critical F6, Constructive A1 | A, A | **A** | Two reviewers found this. Stale inline citation. Update to match JSON (0.3099). |
| 7 | eps_uds_nominal: AN 0.0913 vs JSON 0.1195 vs Table 5 0.086 | Critical F7 | A | **A** | Three values for the same quantity. Identify the correct value per working point; reconcile. |
| 8 | 10% R_b stat: 0.066 vs 0.053 (two valid but different quantities) | Critical F15 | A | **B** | Downgrade to B. Both values exist in JSON and are valid (WP 7.0 only vs 2-WP combined). The fix is to clarify which is primary and use it consistently. Not a stale-value error -- it is an ambiguity in which quantity is reported as THE result. The fixer should pick the combined 0.053 as primary (since the OP stability combination is the point) and state WP 7.0-only (0.066) as a secondary. |
| 9 | Precision ratio: 150x, 278x, 283x in different sections | Critical F8 | B | **B** | Different computations (total/total, syst-only, etc.) produce different ratios. Each may be valid for its context but they should be labeled or a single primary chosen. |
| 10 | Phase 4a R_b.value stale field citation (0.2798) | Constructive A1 | A | -- | **Deduplicated with #6 above.** |
| 11 | Three inconsistent eps_uds fraction claims (96%, 92.1%, 96%) | Constructive A3 | A | **A** | The quadrature fraction is 92%. The 96% is the linear fraction. Pick one convention and use consistently. Fix caption and prose to 92% (quadrature is standard). |

**Fixer action for Group 1:** Perform a single end-to-end numbers
consistency sweep. For EVERY number in the AN that cites a JSON source,
verify against the current JSON. Priority targets: covariance appendix,
validation Table 12, eps_b/eps_uds values, inline field citations, and
the eps_uds fraction percentages. This is approximately 1-2 hours of
methodical work.

---

### Group 2: A_FB^b Reporting and sin2theta_eff

| # | Finding | Source(s) | Their Cat | Final Cat | Rationale |
|---|---------|-----------|-----------|-----------|-----------|
| 12 | sin2theta_eff = 0.248 should be removed or marked N/A | Physics A1, Critical F9 (partial) | A, A | **A** | Both reviewers agree. A number derived from a 10x-suppressed A_FB^b with stat-only uncertainty is misleading. Replace with "N/A (delta_b bias)" in Table 4 / results. |
| 13 | Suppressed A_FB^b reported as central value in abstract/Table 4 | Critical F9 | A | **B** | Downgrade to B. The critical reviewer wants the A_FB^b value removed from the abstract and results table entirely. However, the AN already documents extensively that the value is suppressed, the physics reviewer notes the document is "honest about this failure," and removing the value entirely would eliminate the evidence that the extraction machinery detected a non-zero asymmetry (the 2.4-sigma slope detection IS a valid result). The correct fix: keep the A_FB^b value in the results but reframe as "slope significance" rather than "measurement," and ensure the abstract makes clear this is a detected signal, not a calibrated measurement. The sin2theta_eff derived from it (Finding 12) must go. |
| 14 | 13.5-sigma pull from ALEPH unverifiable (compute gives 11 or 15) | Critical F10 | A | **A** | The reported 13.5-sigma matches neither of the two reasonable computations. State the denominator used or recompute and fix. |
| 15 | eps_c one-sided systematic understates upward R_b uncertainty | Physics A2 | A | **B** | Downgrade to B. The physics reviewer is technically correct that the +1-sigma is unbounded (solver fails). But this is a structural limitation of the extraction at this phase, not a reporting error. The AN acknowledges the solver failure. The fix: add a sentence flagging the systematic as a lower bound, or quote an asymmetric uncertainty. This is a presentation improvement, not a physics error. |

---

### Group 3: Figure Quality (Mechanical Fixes in plot_phase4b.py)

| # | Finding | Source(s) | Their Cat | Final Cat | Rationale |
|---|---------|-----------|-----------|-----------|-----------|
| 16 | F5b: code variable names on y-axis (eps_uds, g_cc, etc.) | Plot V-6 | A | **A** | Plot validator RED FLAG equivalent -- raw code identifiers in a rendered figure. Replace with publication-quality labels. |
| 17 | F5b: absolute fontsize=8 at line 287 | Plot L-1, V-7 | A | **A** | Forbidden pattern per appendix-plotting.md. Use `fontsize='x-small'`. |
| 18 | S2b: absolute fontsize=12 at line 456 | Plot L-2 | A | **A** | Same rule. Use `fontsize='small'`. |
| 19 | S1b + S2b: data_mc type without pull panels (Phase 4 required) | Plot L-5, V-10, V-14 | A | **A** | Phase 4 data_mc figures require pull panels. Either add pull panels or re-classify as `diagnostic` with documented justification. Re-classification is acceptable if justified (S1b is a line plot of tag fractions, not a binned histogram -- pull panels may be impractical). |
| 20 | S2b: missing experiment labels on 3 of 4 panels | Plot V-11, V-13 | A (RED FLAG) | **A** | Automatic Category A per arbiter rules. Missing experiment label. Cannot downgrade. |
| 21 | S2b: text collision (exp_label + kappa + legend overlap) | Plot V-11, V-12 | A | **A** | Increase figsize to (20,20) for 2x2 grid, reposition annotations. |
| 22 | S2b: figsize=(10,10) for 2x2 subplot | Plot L-3, V-15 | B | **B** | Subsumed by fix for #21. Change to (20,20). |
| 23 | F3b: pull panel nearly empty (3 points) | Plot V-3 | A | **A** | A pull panel with only 3 populated points is defective. Investigate the masking logic. |
| 24 | F3b: ambiguous tick label "1" in pull panel | Plot V-4 | A | **B** | Downgrade to B. A stray tick label is a cosmetic issue, not a physics diagnostic failure. Fix with `rax.set_yticks([-2, 0, 2])`. |
| 25 | F7b: no annotation for 10-sigma gap from ALEPH | Plot V-8 | A | **B** | Downgrade to B. The discrepancy is extensively documented in the AN text (Section 8.8-8.9). Annotating inside the figure is good practice but the information IS available in the document. The figure caption should reference Section 8.8. |
| 26 | F2b: systematic negative offset in Q_FB unannotated | Plot V-2 | A | **B** | Downgrade to B. The negative offset is the intercept term that the intercept model (Section 7.2-7.3) is designed to absorb. The physics reviewer confirms the intercept model works (Finding 4 discusses the residual chi2). The offset is not unexplained -- it IS the hemisphere charge bias. The caption should reference Section 7.2. |
| 27 | V-16: cross-figure negative Q_FB not in systematic breakdown | Plot V-16 | A | **B** | Downgrade to B. The plot validator raises this as a potential unaccounted systematic. However, the intercept model explicitly absorbs this offset (it is the a_0 parameter in the linear fit). The A_FB^b is extracted from the slope, not the intercept, so the systematic offset does not bias the slope extraction. The physics reviewer confirms the intercept model is working. A sentence clarifying this in the figure caption or systematic section is sufficient. |
| 28 | MC normalization labels: 'MC (norm.)' -> 'MC (norm. to data)' | Plot L-6 | B | **B** | Agreed. Clarify the normalization method in legends. |
| 29 | mpl_magic not used for legend placement | Plot L-4 | B | **C** | Downgrade to C. Recommendation, not a violation. The current legends do not severely overlap data in most figures (S2b is the exception, handled by #21). |
| 30 | F4b: theory curves displaced from data/MC | Plot V-5 | B | **C** | Downgrade to C. The theory curves use reference efficiency parameters that differ from the actual working-point efficiencies. This is a known approximation. The figure still communicates data/MC agreement. A caption note would suffice. |
| 31 | F7b: kappa=infinity unlabeled at x=5 | Plot V-9 | B | **C** | Minor cosmetic. Relabel if convenient. |
| 32 | F1b: legend overlaps WP=7 error bar | Plot V-1 | B | **C** | Minor. mpl_magic or repositioning would fix. |

---

### Group 4: AN Structural/Presentation Issues

| # | Finding | Source(s) | Their Cat | Final Cat | Rationale |
|---|---------|-----------|-----------|-----------|-----------|
| 33 | Title/abstract claim R_c "measurement" but R_c is constrained | Critical F11 | B | **B** | Valid. R_c is an external constraint, not a measurement. Title should reflect this. |
| 34 | Table 12: chi2/ndf = 3-4 marked FAIL vs criterion < 5 | Critical F16 | A | **A** | Internal contradiction in the validation table. If criterion is < 5 and values are 3-4, it should be PASS (or the criterion should be stated differently). Fix the table to be self-consistent. |
| 35 | Table 4 does not distinguish Phase 4a diagnostic vs 4b measurement | Critical F17 | B | **B** | Valid. Add column headers or footnotes distinguishing the two. |
| 36 | Analytical vs toy uncertainty cross-check not performed | Critical F12 | B | **B** | COMMITMENTS.md minimum target not fulfilled. Either perform or formally defer with justification. |
| 37 | Simple counting A_FB^b cross-check not performed or deferred | Critical F14 | B | **C** | Downgrade to C. Given that A_FB^b is known to be suppressed by the delta_b issue, a cross-check of the suppressed value against a counting method provides limited additional information. Formally defer to Phase 4c (after delta_b fix). |
| 38 | Appendix D precision investigation not updated for Phase 4b | Critical F13/B | B | **B** | Valid. The dominant systematic shifted from eps_c to eps_uds. Appendix D should note this. |
| 39 | C_b=1.01 external assumption: no data-driven cross-check | Critical F20 | B | **C** | Downgrade to C. The C_b assumption is correctly documented and is a known structural limitation of the current extraction. A data-driven C_b bound is a good idea for Phase 4c but not required for the Doc 4b infrastructure validation. |
| 40 | delta_b fix path lacks feasibility verification | Critical F18, Physics B2, Constructive B1 | B, B, B | **B** | Three reviewers agree. Add a feasibility paragraph. |
| 41 | Sentence fragment in Section 5.1 | Rendering R3 | B | **B** | Prose error. Fix the sentence. |
| 42 | Two orphaned figure refs (range-only citation) | Rendering R1, R2 | B | **C** | Downgrade to C. The figures are covered by range notation and visible to the reader. Strictly orphaned in LaTeX sense but not in reader experience. |
| 43 | Four unused BibTeX entries | BibTeX B1, Rendering R4 | B, C | **C** | Housekeeping. Remove unused entries. |
| 44 | Q_FB fit chi2/ndf ~ 3-4: quadratic term tested? | Physics B3 | B | **C** | Downgrade to C for Doc 4b. The chi2/ndf ~ 3-4 is for the MC fits. On 10% data, the intercept-fit chi2/ndf values are 1.1-2.3 (Table 22). The MC residual is documented. A quadratic term investigation is a Phase 4c refinement. |
| 45 | Toy convergence rate 200/1000: Gaussianity check | Physics B4 | B | **C** | Downgrade to C for Doc 4b. Valid concern for Phase 4c where the result will be quoted as a measurement. At Doc 4b, this is an infrastructure validation. |
| 46 | eps_uds narrative: zero at 4a vs 0.499 at 4b | Physics B5 | B | **B** | Same as Constructive B3. Make the WP-dependent solver behavior explicit. |
| 47 | R_b precision projection for Phase 4c | Physics B1 | B | **C** | Downgrade to C. The "10-20x" estimate is in the text. A more quantitative projection would be nice but is speculative before Phase 4c runs. |
| 48 | Covariance matrices deferred to 4c | Physics C1 | C | **C** | Subsumed by Finding 1 (covariance appendix fix). |
| 49 | A_FB^c pole-correction verification | Physics C2 | C | **C** | Agreed. |
| 50 | Angular fit GoF on 10% data not in validation table | Constructive B2 | B | **B** | Valid. The kappa=1.0 p=0.018 warrants a validation table entry. |
| 51 | WP-dependent solver failure not explained | Constructive B3 | B | **B** | Same as #46. |
| 52 | 10% subsample lacks per-year breakdown | Constructive B4 | B | **C** | Downgrade to C. The random seed is documented, the sampling is reproducible. Per-year counts are derivable. Nice to have but not blocking. |

---

## Consolidated Fix List (Priority Order)

### Category A -- Must Resolve

**A-FIX-1: Numbers consistency sweep (stale values).**
Perform one end-to-end pass through the AN verifying every cited number
against its JSON source. Priority targets:
- Covariance matrix Appendix B: regenerate from `covariance.json` or mark as Phase 4a only
- Validation Table 12: fix closure pull (1.03 -> 1.93), remove WP 10.0 closure claim or provide evidence, fix corrupted corrections count (5/6 -> 4/6)
- eps_b at WP 10.0: reconcile three values (0.238, 0.151, 0.132)
- eps_uds_nominal: reconcile 0.0913 vs 0.1195 vs 0.086
- R_b.value field citation: 0.2798 -> 0.3099
- eps_uds fraction: 96% -> 92% in caption and prose (match table cell)
- Table 12 chi2 criterion vs FAIL mark: make self-consistent

**A-FIX-2: sin2theta_eff removal.**
Replace sin2theta_eff = 0.248 +/- 0.0007 in Table 4 and results with
"N/A (delta_b bias)." Do not report a number derived from a known-wrong
extraction.

**A-FIX-3: 13.5-sigma pull recomputation.**
Recompute the A_FB^b pull from ALEPH using stated uncertainties. Document
which denominator is used. Fix to the correct value.

**A-FIX-4: Figure fixes in plot_phase4b.py.**
- F5b: replace code variable names with publication labels on y-axis
- F5b: `fontsize=8` -> `fontsize='x-small'` (line 287)
- S2b: `fontsize=12` -> `fontsize='small'` (line 456)
- S2b: `figsize=(10,10)` -> `figsize=(20,20)` (line 428)
- S2b: add experiment labels to all 4 panels
- S2b: reposition kappa annotations to avoid legend collision
- S1b + S2b: add pull panels OR re-classify as `diagnostic` with documented rationale
- F3b: investigate and fix sparse pull panel (masking bug)

Regenerate all affected figures after code fixes. Update FIGURES.json.

### Category B -- Must Fix Before PASS

**B-FIX-1: A_FB^b framing in abstract/results.**
Reframe A_FB^b = 0.0085 as "slope detection at 2.4 sigma" rather than a
calibrated measurement. Keep the value but add context: "the absolute
A_FB^b value requires delta_b correction (Phase 4c)."

**B-FIX-2: 10% R_b stat uncertainty ambiguity.**
Choose the 2-WP combined value (0.053) as primary. State WP 7.0-only
(0.066) as secondary. Make consistent throughout.

**B-FIX-3: Precision ratio consistency.**
Pick one primary ratio (e.g., total/total = 150x at Phase 4a, 373x at
Phase 4b) and label all other ratios by what they compare.

**B-FIX-4: Title/abstract R_c claim.**
Remove "R_c" from the title or clarify it is constrained, not measured.

**B-FIX-5: Delta_b feasibility paragraph.**
Add 3-4 sentences to Section 8.9 assessing feasibility of the multi-purity
fit (architecturally feasible, estimated implementation effort, required
statistics).

**B-FIX-6: Validation table additions.**
- Add angular fit GoF on 10% data to validation table (note kappa=1.0 p=0.018)
- Fix the criterion vs FAIL inconsistency in Table 12

**B-FIX-7: eps_uds solver WP-dependence explanation.**
Add 2 sentences explaining why solver fails at WP 10.0 (eps_uds=0.086)
but succeeds at WP 7.0 (eps_uds=0.181).

**B-FIX-8: eps_c one-sided systematic flagging.**
Add a sentence noting the +1-sigma R_b uncertainty from eps_c is a lower
bound (solver fails in the upward direction).

**B-FIX-9: Appendix D Phase 4b update.**
Add a paragraph noting the shift in dominant systematic from eps_c (Phase 4a)
to eps_uds (Phase 4b).

**B-FIX-10: Table 4 diagnostic vs measurement distinction.**
Add column header or footnote distinguishing Phase 4a (diagnostic) from
Phase 4b (measurement).

**B-FIX-11: Analytical vs toy cross-check.**
Either perform the COMMITMENTS.md minimum target (C_b and R_c propagation
agree within 10%) or formally defer with documented justification.

**B-FIX-12: Sentence fragment in Section 5.1.**
Fix the broken sentence at lines 1038-1039.

**B-FIX-13: Figure caption improvements.**
- F2b: reference Section 7.2 for the systematic negative offset (intercept)
- F7b: reference Section 8.8 for the ALEPH discrepancy
- S2b: change 'MC (norm.)' to 'MC (norm. to data)'
- F3b: fix pull panel tick labels

### Category C -- Apply Before Commit (No Re-Review)

C-1. Remove 4 unused BibTeX entries.
C-2. Add explicit \ref{} for range-cited figures (fig:eff_cal_eps_c, fig:p3_closure_bflag).
C-3. Resolving power section: lead with Phase 4b numbers.
C-4. Add S-series figure nomenclature explanation.
C-5. Simple counting A_FB^b cross-check: formally defer to Phase 4c.
C-6. Per-year 10% subsample breakdown (nice-to-have table).
C-7. Verify A_FB^c is pole-corrected.
C-8. F4b theory curve caption note.
C-9. F7b kappa=infinity x-axis label.
C-10. C_b=1.01 abstract caveat.
C-11. Add multi-purity fit to Future Directions.
C-12. Validation table WP criterion footnote.
C-13. R_b precision projection quantification.

---

## Regression Check

| Trigger | Met? | Evidence |
|---------|------|----------|
| Validation test failure without 3 remediation attempts | No | All validation tests that failed have documented investigations (delta_b, chi2 residual). The chi2/ndf criterion FAIL in Table 12 is a table-level inconsistency, not a genuine test failure (values 3-4 vs criterion <5). |
| Single systematic > 80% of total uncertainty | Yes (known) | eps_uds = 92% of R_b variance. This is documented, investigated in Appendix D, and the multi-WP fit is the planned mitigation. Not a regression trigger because it is a documented structural limitation with a concrete Phase 4c plan. |
| GoF toy inconsistency | No | Toy convergence rate 200/1000 is documented but not a GoF inconsistency. |
| > 50% bin exclusion | No | Not applicable (no binned fit). |
| Tautological comparison as validation | No | The Phase 4a circular calibration is correctly labeled as a diagnostic. The 10% data uses external C_b. |
| Result > 2-sigma from well-measured reference | Yes (known) | A_FB^b = 0.0085 vs ALEPH 0.0927 (>10 sigma). Root cause identified (delta_b overestimation), investigation is the strongest part of the note (per physics reviewer). This is NOT an unexplained deviation -- it is a known methodological limitation with a concrete fix. Does not trigger regression because: (1) root cause is identified and quantified, (2) fix is planned for Phase 4c, (3) R_b validates on the same infrastructure. |

**No regression triggered.** All potential triggers are either documented
structural limitations with Phase 4c remediation plans, or table-level
inconsistencies fixable within Doc scope.

---

## Motivated Reasoning Check

**"Within N-sigma" rationalization:** R_b = 0.208 +/- 0.523, "consistent
at 0.12 sigma." With uncertainty 2.5x the central value, R_b = 0 would
also be consistent. The AN acknowledges this explicitly ("total uncertainty
is 2.5x the central value"). The physics reviewer confirms the framing is
honest. No motivated reasoning detected -- the result is correctly
described as infrastructure validation, not a measurement.

**Inflated uncertainties making validation trivial:** The eps_uds systematic
dominates at 92%. This is a genuine structural limitation (underdetermined
calibration system with +/-50% variations), not an inflated uncertainty.
The physics reviewer notes this is "a structural consequence of the
underdetermined calibration system." The planned multi-WP fit addresses it.

**"Will be addressed later" without consequences:** The delta_b fix is
deferred to Phase 4c. This DOES have consequences for the current verdict:
A_FB^b cannot be interpreted as a physics measurement at Doc 4b. The AN
is honest about this. The deferral is legitimate because the fix requires
code development (multi-purity fit), not a parameter change.

**Tautological validation:** The Phase 4a closure test uses SM-assumed
calibration -- acknowledged as circular. The 10% data uses external C_b
from ALEPH -- not circular but dependent on an external assumption. Both
are correctly labeled.

**No motivated reasoning detected.** The document is unusually honest
about its limitations.

---

## Reviewer Diagnostic

**Physics (ludmila_77ef):** Thorough physics assessment. Correctly
validated R_b method, identified delta_b investigation as the highlight,
caught the sin2theta_eff reporting issue and eps_c one-sided systematic.
Figure inspection was competent. Found 2A, 5B -- appropriate severity
calibration. No coverage gaps.

**Critical (sabine_4780):** Exceptional numerical cross-checking. Found
7 Category A stale-value inconsistencies by systematically comparing AN
text against JSON files. This is exactly what the critical reviewer
should do. The A_FB^b reporting finding (F9) overlaps with the physics
reviewer but is raised independently with a different emphasis (structural
framing vs sin2theta_eff). The 13.5-sigma verification (F10) is a
valuable independent computation. The Table 12 chi2 criterion contradiction
(F16) is a good catch. No coverage gaps. The severity calibration is
slightly aggressive (some B items classified as A), but the arbiter
adjusted where warranted.

**Constructive (sam_a0b1):** Good depth assessment across all sections.
The three Category A findings overlap with the critical reviewer (stale
field citation, covariance, eps_uds fraction) -- confirming the critical
reviewer's findings independently. The B findings (delta_b feasibility,
angular fit GoF, solver WP-dependence, per-year breakdown) are actionable
and well-motivated. The C findings are genuinely constructive. COVERAGE
GAP: did not independently check the validation Table 12 entries against
JSON (the critical reviewer's most productive activity). This is within
scope for the constructive role given its emphasis on depth and resolving
power rather than mechanical cross-checking.

**Plot Validator (felix_af10):** Thorough code linting and visual review
of all 8 Phase 4b figures. Found 10A, 6B findings. The code lint
(fontsize violations, figsize, pull panel requirements) is mechanical
and correct. The visual review caught real issues (S2b text collision,
F3b sparse pull panel, F5b code variable names). COVERAGE GAP: V-2
(systematic negative offset) and V-16 (cross-figure consistency) are
physics interpretations that exceed the plot validator's mandate -- the
negative offset IS the hemisphere charge bias absorbed by the intercept
model, which is documented. The plot validator should flag visual
anomalies but not make physics claims about their meaning. These were
correctly downgraded.

**Rendering (agnes_eff4):** Clean and focused review. Found 0A, 3B
findings. Correctly verified all cross-references, bibliography, float
environments, and compilation. The orphaned figure findings are technical
(range-citation) and low-severity. The sentence fragment catch (R3) is
valuable. No coverage gaps for the rendering role.

**BibTeX (sally_766b):** Complete validation of all 11 cite keys. Found
0A, 1B (unused entries). Correct and efficient. No coverage gaps.

---

## Verdict: ITERATE

**Rationale:** There are 4 groups of Category A findings (stale values,
sin2theta_eff, 13.5-sigma pull, figure quality) and 13 Category B
findings. PASS requires no unresolved A or B items.

The work is bounded and mechanical. The fixer should:
1. Run the numbers consistency sweep (A-FIX-1) -- this resolves ~7 stale-value findings in one pass
2. Remove sin2theta_eff from results (A-FIX-2) -- one table edit
3. Recompute the A_FB^b pull (A-FIX-3) -- one calculation
4. Fix plot_phase4b.py and regenerate figures (A-FIX-4) -- code edits + re-run
5. Address B-FIX-1 through B-FIX-13 -- prose edits and minor additions

Estimated fixer time: 3-4 hours. No regression to earlier phases required.
All fixes are within Doc scope.

After the fixer pass, run verification arbiter to confirm each fix, then
a fresh review panel before human gate.

---

*Adjudication by tomas_f1ad | Date: 2026-04-02*
