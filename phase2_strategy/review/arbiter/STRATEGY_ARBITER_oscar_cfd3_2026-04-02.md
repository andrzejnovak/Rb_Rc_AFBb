# Arbiter Adjudication — STRATEGY.md (Phase 2, Iteration 2)

Arbiter: oscar_cfd3 | Date: 2026-04-02

Inputs reviewed:
- `phase2_strategy/outputs/STRATEGY.md` (1111 lines, post-fix by felix_d976)
- Physics review: dmitri_e9ed (2A, 4B, 4C)
- Critical review: katya_2f50 (2A, 3B, 3C)
- Constructive review: lena_389c (1A, 4B, 4C)
- `conventions/extraction.md`
- `methodology/06-review.md`
- Iteration 1 arbiter: albert_1036 (7A + 13B, all resolved by fixer)

---

## Structured Adjudication Table

| # | Finding | Source(s) | Their Cat | Final Cat | Rationale |
|---|---------|-----------|-----------|-----------|-----------|
| 1 | A_FB^b governing fit formulation: Section 6.3 describes the mean-charge formula but does not commit to a specific fit implementation (five-category chi2 vs mean-charge regression vs ALEPH sin^2 fit) | Critical A1, Constructive A1, Physics (implicit in A4) | A, A, B | **A** | All three reviewers converge on this. The critical and constructive reviewers independently retrieved corpus evidence confirming the five-category chi2 structure from both ALEPH (inspire_433746) and DELPHI (inspire_1661115, inspire_1661252). The current Section 6.3 gives the expected-value model but not the operational fit procedure. Phase 3/4 executors need an unambiguous specification. This is the single most important fix. |
| 2 | Experiment log stale on kappa set (4 values vs 5) | Critical A2 | A | **C** | The experiment log is indeed stale — it records {0.3, 0.5, 1.0, 2.0} while STRATEGY.md and COMMITMENTS.md both correctly state {0.3, 0.5, 1.0, 2.0, infinity}. However, the experiment log is not the governing document for Phase 3 executors — STRATEGY.md and COMMITMENTS.md are. This is a documentation cleanup, not a physics blocker. A Phase 3 executor reads STRATEGY.md, not the experiment log. Downgrading from A to C. Fix: append correction entry to experiment_log.md. Cost: <5 minutes. |
| 3 | d0 sign convention validation plan missing | Physics A2 | A | **B** | The concern is valid — if d0 is unsigned, the lifetime tag breaks. However, I examined the artifact: Section 5.1 item 4 already documents the sign convention and Section 9.1 closure test (a) explicitly uses "negative-d0 pseudo-data" which requires and tests the sign convention. The Phase 3 executor implementing the negative-d0 test will necessarily discover if d0 is unsigned (the negative tail would be empty or symmetric). What is missing is an explicit [D]-labelled decision committing to the sign validation as a gate. This is Category B (should address) rather than A (blocks advancement), because the existing closure test implicitly requires and tests the sign, but an explicit commitment strengthens the audit trail. |
| 4 | C_b estimation plan under-specified for dominant systematic | Physics A3 | A | **B** | The physics reviewer correctly identifies that bFlag=4 at 94% is not a useful b-enrichment and that prong (b) is circular. However, the strategy already identifies prong (c) — published C_b values with inflated uncertainty — as the fallback, and the systematic table assigns 0.00100 to hemisphere correlations (2x the published ALEPH value, explicitly documented as conservative). The three-pronged approach is a Phase 3 investigation plan; the strategy's binding commitment is the 0.00100 systematic with published C_b as the baseline. The strategy should add specific published C_b values (numerical value + reference) and state the inflation factor explicitly. This is Category B — the approach is sound but the specification is incomplete for Phase 3 execution. |
| 5 | sin^2(theta_eff) extraction path not specified | Physics A4 | B | **B** | Accept at reviewer's category. The prompt asks for sin^2(theta_eff) extraction; the strategy mentions the published value but does not describe the inversion from A_FB^{0,b}. This is coupled to Finding #1 — if the five-category chi2 fit is adopted with sin^2(theta_eff) as the fit parameter (the ALEPH method), this is automatically resolved. If the simplified fit is adopted, the extraction path A_FB^{0,b} -> sin^2(theta_eff) must be specified separately. Resolution of Finding #1 will resolve or clarify this. |
| 6 | Closure tests do not test what they claim | Physics A5 | B | **C** | The physics reviewer's point is technically correct — none of the three tests is a genuine MC-split closure test. But the strategy already acknowledges this limitation (Section 9.1 states these are "proxy closure tests, not traditional MC-split closure which requires truth labels"). The reviewer asks the strategy to "not overstate" the tests, but the strategy does not overstate them. The tests are diagnostic and correctly described as such. The comparison to published ALEPH values is the de facto closure. Downgrade to C — add one sentence acknowledging that the published value comparison serves as the ultimate validation. |
| 7 | eps_c uncertainty bound of +/-30% relative is asserted, not derived | Critical B1 | B | **B** | Accept. The 30% figure needs grounding. The critical reviewer provides three concrete paths: (a) derive from spread across published working points, (b) cite typical LEP data/MC ratios, (c) use published eps_c spread. Any of these takes <30 minutes. |
| 8 | delta_b characteristics for kappa=infinity not discussed | Critical B2 | B | **B** | Accept. The strategy commits to kappa=infinity but does not discuss its expected information contribution. Adding a threshold for demotion to "cross-check only" (e.g., delta_b < 0.1) is a concrete improvement that prevents Phase 4 from wasting effort on a negligible-weight measurement. |
| 9 | bFlag=4 interpretation: no committed decision tree in COMMITMENTS.md | Critical B3 | B | **B** | Accept. The strategy correctly flags the issue (Section 9.6) but does not formalize the decision tree. Adding a COMMITMENTS.md entry with the chi2 test and fallback to self-labelling option 2 is <10 minutes and prevents an ad-hoc Phase 3 decision. |
| 10 | [D17] primary vertex investigation: remediation path for each scenario not committed | Constructive B1 | B | **C** | This is a Phase 3 implementation detail. The strategy correctly identifies [D17] as a deferred investigation with three scenarios documented. Committing to specific remediation paths (per-hemisphere vertex refit vs inflated systematic) at Phase 2 is premature — the Phase 3 executor needs to discover which scenario applies first. The strategy's current formulation ("investigate at Phase 3, three scenarios documented") is sufficient for Phase 2. The constructive reviewer's suggestion to add a concrete protocol is good but belongs in the Phase 3 CLAUDE.md or executor prompt, not in the Phase 2 strategy. Downgrade to C — add a cross-reference noting that Phase 3 must resolve [D17] with the specific remediation committed at that time. |
| 11 | A_FB^b precision estimate uses incorrect sqrt(5/4) scaling | Constructive B2, Physics A9 | B, C | **C** | Both reviewers flag the sqrt(5/4) factor as incorrect. The physics reviewer rates it C; the constructive reviewer rates it B. The precision estimate is explicitly labelled as an estimate with a range (0.005-0.007). The sqrt(5/4) factor is a minor error in an order-of-magnitude calculation that does not affect any Phase 3 decision. Correct it (remove the factor, state ~0.0047 from direct scaling), but this does not block advancement. Accept at C. |
| 12 | BDT diagnostic action on positive result incompletely specified | Constructive B3 | B | **C** | The strategy states "if slope detected, revert to cut-based as primary." The constructive reviewer wants a specific significance threshold and retention policy. This is reasonable but is a Phase 3 operational detail. The strategy's commitment to revert if contamination is detected is the binding decision. The threshold (1-sigma? 2-sigma?) is best determined in Phase 3 when the actual diagnostic is computed and the noise level is known. Downgrade to C — add "2-sigma threshold" as a guideline and note the contamination fraction feeds into bFlag interpretation. |
| 13 | Flagship figure F4 missing chi2 contours | Constructive B4 | B | **C** | This is a figure specification detail. The strategy defines the figure content; the exact overlays (chi2 contours, uncertainty bands) are Doc phase decisions. The constructive reviewer's suggestion is good and should be noted for the Doc phase executor, but it does not block Phase 3 advancement. Downgrade to C — add "with 1-sigma uncertainty band" to the F4 description. |
| 14 | Beam spot position stability not discussed | Physics A8 | B | **C** | This is a valid concern but is implicitly covered by the per-year sigma_d0 calibration (Section 9.4), which absorbs beam spot position variations into the per-year resolution model. The strategy should mention this explicitly in one sentence. Downgrade to C. |
| 15 | R_c constraint: SM vs measured, dual reporting | Physics A1 | B | **C** | The strategy already documents the sensitivity (dR_b/dR_c ~ -0.05, delta_R_b ~ 0.00015) and commits to a cross-check with floated R_c. The physics reviewer asks for explicit dual reporting (R_b with SM R_c and R_b with measured R_c). This is a Phase 4 reporting decision, not a strategy decision. The cross-check with floated R_c (Section 4.3, item 2) already achieves this. Downgrade to C — add one sentence: "Report R_b extracted with both SM and LEP-measured R_c central values as a cross-check." |
| 16 | g_cc value inconsistency (3.3% vs 2.96%) | Physics A6 | C | **C** | Accept at C. Harmonize the 3.3% in Section 10.1 with the 2.96% used elsewhere. |
| 17 | kappa = infinity implementation note | Physics A7 | C | **C** | Accept at C. Add note to use explicit leading-track definition, not large-kappa limit. |
| 18 | Track weight branch usage unclear | Physics A10 | C | **C** | Accept at C. Flag as Phase 3 investigation item. |
| 19 | bFlag interpretation and BDT training label cross-reference | Constructive C1 | C | **C** | Accept at C. Add cross-reference between Section 9.6 and [D9]. |
| 20 | C_b systematic combination prescription unspecified | Constructive C2 | C | **C** | Accept at C. Add "linear combination following hep-ex/9609005" to Section 7.1. |
| 21 | Per-year d0 sentinel fraction variation | Constructive C3 | C | **C** | Accept at C. Add per-year sentinel fraction check as Phase 3 action. |
| 22 | Analytical cross-check targets unspecified | Constructive C4 | C | **C** | Accept at C. Add C_b and R_c constraint as minimum analytical cross-check targets. |
| 23 | delta_QCD notation inconsistency (Section 6.4 omits delta_QED vs Section 2.2) | Critical C2 | C | **C** | Accept at C. Add clarifying note in Section 6.4. |
| 24 | g_bb source note in COMMITMENTS.md | Critical C1 | C | **C** | Accept at C. One sentence in COMMITMENTS.md. |

---

## Summary of Final Classifications

| Category | Count | Items |
|----------|-------|-------|
| **A** | 1 | #1 (A_FB^b fit formulation ambiguity) |
| **B** | 4 | #3 (d0 sign validation gate), #4 (C_b specification), #7 (eps_c 30% grounding), #8 (kappa=inf delta_b threshold), #9 (bFlag decision tree in COMMITMENTS.md) |
| **C** | 19 | #2, #5, #6, #10-#24 |

Note: Finding #5 (sin^2(theta_eff) extraction) is rated B but will be resolved as a consequence of fixing Finding #1. It does not require independent action if Finding #1 adopts the five-category chi2 fit with sin^2(theta_eff) as a derived quantity.

---

## Regression Trigger Check

Independently evaluating against methodology/06-review.md Section 6.7 triggers:

| Trigger | Applicable? | Assessment |
|---------|-------------|------------|
| Validation test failure without 3 remediation attempts | No | Phase 2 strategy — no validation tests run yet |
| Single systematic > 80% of total uncertainty | No | Systematic budget shows C_b at ~0.00100 out of ~0.0020 total = 50%, within range |
| GoF toy inconsistency | No | No fits run yet |
| >50% bin exclusion | No | Not applicable at Phase 2 |
| Tautological comparison as validation | No | Closure tests are correctly labelled as proxy tests, not claimed as independent closure |

**No regression triggers are met.** This is a Phase 2 strategy document; regression triggers primarily apply to implementation phases. No regression required.

---

## Motivated Reasoning Check

- The precision estimates are conservative (0.005-0.007 for A_FB^b vs published 0.0039 at higher statistics). Not inflated to trivialize validation.
- Limitations are documented honestly: [A1]-[A6] constraints acknowledged, [L1]-[L4] limitations listed.
- The strategy does not claim to replicate the published ALEPH method exactly — it documents simplifications and workarounds.
- No "will be addressed later" items that could change the physics result. Deferred items (D17, bFlag investigation) are operational, not physics-altering.

No motivated reasoning concerns identified.

---

## Reviewer Diagnostic

### Physics (dmitri_e9ed)
- **Strengths:** Identified the d0 sign convention risk (A2) — a genuine single-point-of-failure. Caught the C_b estimation logical gap (A3, bFlag=4 at 94% is not b-enriched). Good quantitative grounding throughout (sensitivity coefficients, numerical estimates).
- **Coverage gaps:** Did not identify the A_FB^b fit formulation ambiguity that was the dominant finding from the other two reviewers. The physics reviewer focused on the sin^2(theta_eff) extraction path (A4) which is downstream of the fit formulation issue but did not trace it to the root cause (the fit procedure itself is unspecified). This is within scope for a physics reviewer — the fit implementation is arguably more "critical review" territory, but the physics consequences (different statistical properties, correlation handling) are squarely physics.
- **Assessment:** GOOD coverage. The A_FB^b fit formulation was the main gap.

### Critical (katya_2f50)
- **Strengths:** Thorough prior-concern disposition table with explicit evidence for each. The A_FB^b fit formulation finding (A1) is the strongest finding in the review — well-sourced from corpus retrieval, correctly distinguishes the expected-value formula from the fit procedure, and provides concrete resolution options. The experiment log staleness catch (A2) demonstrates attention to audit trail integrity.
- **Coverage gaps:** None identified. The checklist is comprehensive and every item has a status. The "competing group" analysis is well-reasoned.
- **Assessment:** EXCELLENT coverage. The critical reviewer performed the role's core function (convention coverage, completeness, cross-reference to references) thoroughly.

### Constructive (lena_389c)
- **Strengths:** Independently confirmed the A_FB^b fit formulation issue (A1) with corpus evidence from DELPHI references. The honest framing check is genuine and substantive. The depth mandate evaluation identifies per-section probe points. RAG evidence table is well-organized.
- **Coverage gaps:** Several B findings (B1 primary vertex, B3 BDT diagnostic, B4 figure specification) are Phase 3 implementation details rather than Phase 2 strategy blockers. The constructive reviewer's role is to identify improvement opportunities, and these are genuine improvements, but the severity assessment conflates "would be better in the strategy" with "blocks Phase 3 advancement." This is not a gap in coverage — it is a calibration issue in severity assignment.
- **Assessment:** GOOD coverage. Severity calibration was slightly aggressive for a Phase 2 document.

---

## Verdict: **ITERATE**

One unresolved Category A finding and four Category B findings prevent PASS.

### Fix List (priority order)

**Category A (must resolve):**

1. **A_FB^b fit formulation (Finding #1).** Section 6.3 and [D12] must commit to a specific fit implementation. The recommended path (supported by all three reviewers and corpus evidence): adopt the five-event-category chi2 fit from inspire_433746 / inspire_1661115. Specifically:
   - Define the five event-rate observables: N_F (single-tagged forward), N_B (single-tagged backward), N_FF (double-tagged unlike-sign forward), N_BB (double-tagged unlike-sign backward), N_same (double-tagged like-sign).
   - State the fit parameters: A_FB^b (or sin^2(theta_eff)), the charge-assignment probability w_b, and normalisation factors.
   - State that this is fitted in bins of cos(theta) at each kappa value and working point.
   - If the simplified mean-charge fit is chosen instead, document it as a simplification with respect to inspire_433746 and justify why the correlation treatment difference is acceptable.
   - Add the sin^2(theta_eff) extraction as a derived quantity from the fitted A_FB^{0,b}: specify whether A_e is taken externally (from A_l at SLD) or computed from the same sin^2(theta_eff) assuming lepton universality.
   - Label as [D12b] or update [D12].
   - Estimated fix effort: 2-3 paragraphs added/revised in Sections 4.2, 6.3, and 8.3. ~30 minutes.

**Category B (must fix before PASS):**

2. **d0 sign convention validation gate (Finding #3).** Add an explicit [D]-labelled decision: "Phase 3 gate: verify d0 sign convention by plotting d0 in b-enriched hemispheres. If the positive tail is not enhanced relative to the negative tail, the lifetime tag is invalid and the strategy must be revised." Add to COMMITMENTS.md. ~10 minutes.

3. **C_b published values and inflation factor (Finding #4).** In Section 7.1 C_b row, add: specific published C_b value from hep-ex/9609005 (C_b at the operating point), the inflation factor applied (e.g., "2x published uncertainty"), and state whether C_b is varied as a single number or decomposed. ~15 minutes.

4. **eps_c 30% grounding (Finding #7).** Ground the 30% relative uncertainty using one of the three paths the critical reviewer provides. The simplest: cite the spread of published eps_c values across working points from hep-ex/9609005 as the basis. ~15 minutes.

5. **kappa=infinity delta_b threshold (Finding #8).** Add to Section 4.2 or 7.4: "If delta_b(kappa=infinity) < 0.1, use kappa=infinity as cross-check only, not in the primary combination." ~5 minutes.

6. **bFlag decision tree in COMMITMENTS.md (Finding #9).** Add validation test entry: "bFlag interpretation: if bFlag=4 b-tag discriminant distribution is indistinguishable from the full sample (chi2/ndf ~ 1.0), classify bFlag as non-b flag and default to self-labelling option 2 for BDT training." ~10 minutes.

**Category C items (apply before commit, no re-review):**

Apply all 19 Category C items. The largest are:
- Update experiment_log.md with kappa set correction (#2)
- Remove sqrt(5/4) from precision estimate (#11)
- Add "with 1-sigma uncertainty band" to F4 description (#13)
- Harmonize g_cc 3.3% vs 2.96% (#16)
- Add delta_QCD/delta_QED clarification in Section 6.4 (#23)
- Add cross-references: bFlag/BDT (#19), C_b combination method (#20), per-year sentinel fraction (#21), analytical cross-check targets (#22)

Total estimated fix effort: ~2 hours for all A + B + C items combined.
