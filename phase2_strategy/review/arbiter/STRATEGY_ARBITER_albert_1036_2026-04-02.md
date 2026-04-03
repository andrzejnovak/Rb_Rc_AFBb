# Arbiter Adjudication: Phase 2 Strategy — R_b, R_c, A_FB^b

**Arbiter session:** albert_1036
**Date:** 2026-04-02
**Artifact:** `phase2_strategy/outputs/STRATEGY.md` (peter_b030, 2026-04-02)
**Reviews adjudicated:**
- Physics: andrzej_e80c (2 A, 6 B, 4 C)
- Critical: sigrid_16b8 (5 A, 5 B, 4 C)
- Constructive: nora_766f (2 A, 4 B, 6 C)

**Conventions:** `conventions/extraction.md`
**Methodology:** `methodology/06-review.md`

---

## Adjudication Framework Applied

For each finding below, I verified the claim against the artifact
(STRATEGY.md) and the applicable conventions/methodology. Findings
are grouped by topic where multiple reviewers raised the same or
overlapping issues.

---

## Structured Adjudication Table

| # | Finding | Source(s) | Their Cat | Final Cat | Rationale |
|---|---------|-----------|-----------|-----------|-----------|
| 1 | Gluon splitting correction formula wrong | Physics A1, Critical A3 | A, A | **A** | Both reviewers independently identified the same error. Verified: STRATEGY.md Section 10.2 writes `R_b(corrected) = R_b(measured) - g_bb * (eps_g / eps_b)^2`. This is not the standard prescription. The LEP EWWG (hep-ex/0509008 Section 5.4) and published analyses fold g_bb into the modified double-tag equations through the effective uds efficiency, not as a direct R_b subtraction. The formula as written is dimensionally suspect (the (eps_g/eps_b)^2 ratio does not yield a correction to R_b without additional factors). A wrong gluon splitting correction biases R_b by O(0.001), which is comparable to the total systematic. Must be rewritten. |
| 2 | A_FB^b angular-dependent tag efficiency missing from systematics | Physics A2 | A | **A** | Verified: STRATEGY.md Section 7.1 and 7.4 list systematic sources for A_FB^b. Neither table includes the angular dependence of the b-tag efficiency. The tag efficiency must drop at high |cos(theta)| due to reduced VDET coverage (fewer silicon hits at forward angles), changing the effective b-purity f_b across the angular range. This is one of the dominant A_FB^b systematics in published analyses. Its absence from the systematic plan is a genuine gap. The self-calibrating fit absorbs some of this, but only if the angular dependence is parameterized — and the strategy does not commit to this parameterization. |
| 3 | Closure test is tautological with single MC sample | Critical A1 | A | **A** | Verified: COMMITMENTS.md describes "Independent closure test: extract R_b from independent MC split (derivation vs validation halves, fixed seed). Pull < 2 sigma." With a single MC sample split in two, both halves share the same generator, fragmentation, and detector model. Efficiencies eps_c and eps_uds derived from one half will perfectly describe the other half. The extraction will recover the correct R_b by algebraic construction. The conventions/extraction.md Pitfalls section explicitly warns: "A self-consistent extraction always recovers the correct answer by construction — this is an algebra check, not a closure test." The strategy does not acknowledge this risk or propose a meaningful alternative. The critical reviewer's proposed alternatives (negative-tail pseudo-data test, bFlag split, artificial contamination injection) are all reasonable. |
| 4 | A_FB^b formula normalization inconsistency | Critical A2 | A | **A** | Verified: STRATEGY.md Section 4.2 gives `A_FB^b = (8/3) * <Q_FB> / (R_b * delta_b)` (from literature survey). Section 6.3 gives `<Q_FB>(cos theta) = sum_q f_q * delta_q * A_FB^q * cos(theta)`. These are indeed inconsistent as written. The first formula applies to the inclusive hadronic sample; the second applies to the tagged sample where f_q are the tagged sample fractions. If the executor at Phase 4 implements the simplified formula on the tagged sample without the purity correction, A_FB^b will be biased by 1/f_b. The strategy must clearly designate the self-calibrating fit (inspire_433746 Section 4) as the governing extraction and label the simplified formula as an approximation. |
| 5 | sigma_d0 parameterization: sin^{3/2}(theta) vs correct angular form | Physics B4, Critical A4 | B, A | **A** | The physics reviewer rated this B; the critical reviewer rated it A with a more detailed argument. I side with the critical reviewer. Verified: STRATEGY.md Section 5.1 uses `sigma_d0 = sqrt(A^2 + (B / (p * sin^{3/2}(theta)))^2)`. The critical reviewer documents that for the Rphi d0 (which is what the d0 branch stores, per DATA_RECONNAISSANCE.md), the standard ALEPH parameterization uses B/(p sin(theta)), not sin^{3/2}(theta). The sin^{3/2} form arises for 3D impact parameters. If sigma_d0 is overestimated for forward tracks, the significance is underestimated, reducing b-tag efficiency at high |cos(theta)| — directly biasing the angular distribution used for A_FB^b. The negative-tail calibration will partially correct this, but starting from a wrong functional form means larger and more momentum-dependent corrections. This is consequential for both R_b (systematic) and A_FB^b (angular bias). Elevating to A because the wrong functional form propagates to two observables and the critical reviewer's argument is well-grounded in the ALEPH detector papers. |
| 6 | PDG inputs not fetched — "NEEDS FETCH" unresolved | Critical A5 | A | **A** | Verified: INPUT_INVENTORY.md lists M_Z, Gamma_Z, B hadron lifetimes, and decay multiplicities as "NEEDS FETCH." STRATEGY.md Section 7.1 commits to using these quantities for systematics but provides no values or citations. CLAUDE.md Numeric Constants policy: "At review, any uncited numeric constant is Category A." The strategy cannot be considered complete while mandatory numerical inputs remain unresolved. The fix is straightforward: fetch values from PDG 2024 and cite them. |
| 7 | Primary vertex definition unspecified | Physics B5, Constructive A1 | B, A | **A** | The physics reviewer rated this B; the constructive reviewer rated it A with a thorough argument. I side with the constructive reviewer. Verified: STRATEGY.md Section 5.1 describes the signed impact parameter computation relative to the primary vertex but never specifies what primary vertex is used. The constructive reviewer correctly identifies that the choice (global event vertex vs per-hemisphere vertex vs beam spot) changes the numerical value of d0/sigma_d0 and therefore the tag discriminant and hemisphere correlation C_b. The ALEPH reference (hep-ex/9609005) explicitly uses per-hemisphere primary vertex reconstruction. If d0 in the stored branches is relative to a vertex that includes the track under test, there is a systematic bias (the "track-in-vertex" problem). This is not a detail — it is a fundamental input to the tagger. Elevating to A. |
| 8 | Mass tag component of ALEPH Q tag not committed | Constructive A2, Physics C1 | A, C | **B** | The constructive reviewer rates this A (scope ambiguity); the physics reviewer mentions it as C (suggestion). Verified: STRATEGY.md [D8] commits to "Primary: probability tag P_hem." The ALEPH Q tag combines P_hem with a hemisphere invariant mass cut. The strategy lists mass as a BDT input (Section 5.2) but not as part of the cut-based Approach A. The constructive reviewer's concern that [D3] is ambiguous about whether the mass component is included or excluded is valid — but the strategy explicitly states "simplified two-tag system" and lists P_hem as primary. This is a deliberate simplification, not an ambiguity. The mass tag would improve purity and is implementable from available branches (4-vectors available), so it should be addressed in the strategy revision. However, the cut-based approach with P_hem alone is a valid physics choice, and the BDT approach includes mass as an input variable. Downgrading to B: the strategy should explicitly commit to implementing the combined probability-mass tag in Approach A (or justify its exclusion), but this is an improvement opportunity, not a blocking ambiguity. |
| 9 | R_c constraint impact on R_b not quantified | Physics B1 | B | **B** | Verified: STRATEGY.md Section 4.3 states R_c will be constrained with +/- 0.0030 systematic, but Section 8 does not include a numerical estimate of the resulting systematic on R_b. The sensitivity dR_b/dR_c is calculable from the double-tag equations and should be included to verify this is not a dominant systematic. |
| 10 | C_b measurement strategy unclear without MC truth | Physics B2 | B | **B** | Verified: STRATEGY.md Section 7.1 says "Evaluate C_b from MC" but with no truth labels [A1], the executor cannot isolate bb events in MC to compute C_b for b quarks specifically. The strategy must describe how C_b will actually be determined. The physics reviewer's three options (bFlag=4 proxy, geometric/kinematic estimation, published value with inflated uncertainty) are all viable — one must be committed to. |
| 11 | A_FB^b statistical precision estimate not derived | Physics B3 | B | **B** | Verified: STRATEGY.md Section 8.3 states "sigma(A_FB^b)_stat ~ 0.004-0.005" without showing the calculation. The physics reviewer derives sigma ~ 0.0065 from a simple counting estimate, which is larger than quoted. The self-calibrating fit may improve this, but the strategy should show the calculation explicitly. |
| 12 | Thrust axis sign convention for A_FB^b not addressed | Physics B6 | B | **B** | Verified: The strategy does not discuss how "forward" (toward the electron beam) is defined. The thrust axis is unsigned — a convention must be chosen. If the beam direction is not recoverable from the ntuple, A_FB^b cannot be measured. This is a prerequisite that must be addressed. |
| 13 | Data-derived calibration for eps_c missing | Critical B1 | B | **B** | Verified: conventions/extraction.md requires data-derived calibration or documented justification for using uncalibrated MC. STRATEGY.md Section 7.2 states eps_c uses "MC values with inflated systematic covering data-implied range" but does not define the range or explain why a charm-enriched control region is infeasible. The phrase "data-implied range" is operationally empty. Must document specifically why a charm control region is not feasible, or propose one. |
| 14 | cos(theta) binning chi2/ndf not committed | Critical B2 | B | **B** | Verified: STRATEGY.md [D12] commits to 8-10 uniform bins without justification and without committing to report chi2/ndf of the angular fit. conventions/extraction.md validation check 3 requires reporting GoF at each scan point. Add this commitment. |
| 15 | BDT label circularity diagnostic underspecified | Critical B3 | B | **B** | Verified: The strategy acknowledges bFlag contamination but does not commit to a specific diagnostic for BDT working point slope as evidence of label contamination. The critical reviewer's proposed diagnostic (slope > 1-sigma/range triggers documentation) is concrete and should be adopted. |
| 16 | g_bb uncertainty two-component form | Critical B4 | B | **C** | The critical reviewer requests writing g_bb as two-component (+/- 0.04 stat +/- 0.09 syst) and switching to the LEP combined value (0.29 +/- 0.06). Verified: STRATEGY.md uses 0.26 +/- 0.10, consistent with the ALEPH measurement quadrature combination. The two-component form is better practice but the single total uncertainty is not wrong. Switching to the LEP combined value is a reasonable suggestion. Downgrading to C: this is a presentation improvement, not a physics error. The strategy should adopt the LEP combined value with citation, but this does not block Phase 3. |
| 17 | kappa = infinity exclusion misstated | Critical B5 | B | **B** | Verified: STRATEGY.md [D5] states kappa = infinity "requires particle identification for optimal performance." The critical reviewer correctly notes that kappa = infinity (leading particle charge) does not require PID — it uses the highest-momentum track's charge, which is available. PID improves it but is not required. The justification should be corrected, and kappa = infinity should be included as an additional working point. |
| 18 | R_c cross-check sensitivity not estimated | Constructive B1 | B | **B** | Verified: [D6] commits to floating R_c as a cross-check but does not estimate sensitivity. The constructive reviewer calculates ~0.004-0.007 statistical precision on R_c from the cross-check. Adding this estimate prevents the cross-check from being silently dropped at Phase 4 as "insensitive." |
| 19 | Angular binning year-dependence not addressed | Constructive B2 | B | **B** | Verified: The VDET changed between 1993 and 1994 (documented in Phase 1). The strategy commits to per-year extraction but does not address whether angular binning should differ per year. This should be explicitly decided. |
| 20 | y_3 omitted from hemisphere correlation check | Constructive B3 | B | **B** | Verified: STRATEGY.md Section 7.1 lists "cos(theta), primary vertex error, jet momentum" for correlation evaluation. The ALEPH reference (hep-ex/9609005 Section 7) uses four variables including y_3 (gluon radiation). The ktN2 jet tree provides y_3-equivalent. This is a one-line addition. |
| 21 | A_FB^b flagship figure missing kappa comparison | Constructive B4 | B | **B** | Verified: F2 shows <Q_FB> vs cos(theta) for one kappa value. The strategy commits to kappa = {0.3, 0.5, 1.0, 2.0} but has no figure showing A_FB^b consistency across kappa values. This is a key cross-check that should be a flagship figure. |
| 22 | Systematic decomposition for precision estimate | Critical C1 | C | **C** | The systematic precision estimate (Section 8.2) borrows the ALEPH total without decomposition. A per-systematic table showing expected scaling would improve transparency. |
| 23 | bFlag = 4 meaning not resolved | Critical C2 | C | **C** | bFlag = 4 for 94% of events is too high to be a b-tag (R_b ~ 21%). The strategy should investigate its meaning before Phase 3. |
| 24 | REF2 MC sample size not quantified | Critical C3 | C | **C** | Minor documentation gap. |
| 25 | Cite primary QCD theory source for delta_QCD | Physics C2 | C | **C** | The strategy cites the experimental combination (hep-ex/0509008) rather than the primary theoretical calculation. |
| 26 | Define chi2/ndf threshold for per-year consistency | Physics C2, Constructive C5 | C, C | **C** | Reasonable suggestion. Specify chi2/ndf > 2.0 as investigation threshold. |
| 27 | Add delta_b vs kappa to flagship figures | Physics C3 | C | **C** | Good suggestion; partially overlaps with finding #21 (B). |
| 28 | |cos(theta)| vs signed cos(theta) ambiguity | Constructive C3 | C | **C** | [D12] writes "|cos(theta)|" for bins but the fit requires signed cos(theta). A clarification is needed but the intent (fold both hemispheres, use signed cos for Q_FB) is standard and inferable. |
| 29 | R_c SM vs LEP-measured constraint value | Constructive C4 | C | **C** | The difference (0.00013) is negligible vs the 0.0030 systematic. Document the choice. |
| 30 | Stability scan conflates robustness with bias | Constructive C1 | C | **C** | Valid observation. The stability scan tests self-consistency, not absolute bias. The strategy should document this distinction. |
| 31 | sigma_d0 calibration binning not specified | Constructive C2 | C | **C** | The binning granularity should be specified for reproducibility. |
| 32 | Missing P_hem discriminant data/MC figure | Constructive C6 | C | **C** | A data/MC comparison on the tagger output (not just the input d0/sigma_d0) should be a flagship figure. |

---

## Regression Trigger Check (Section 6.7)

Independently evaluating each trigger from methodology/06-review.md Section 6.7:

| Trigger | Status | Evidence |
|---------|--------|----------|
| Validation test failure without 3 remediation attempts? | N/A at Phase 2 | No validation tests run yet |
| Single systematic > 80% of total uncertainty? | N/A at Phase 2 | No systematics evaluated yet |
| GoF toy inconsistency? | N/A at Phase 2 | No fits run yet |
| > 50% bin exclusion? | N/A at Phase 2 | No binning applied yet |
| Tautological comparison presented as validation? | **YES** | Finding #3: the committed closure test (MC split) is tautological by construction. The conventions file explicitly warns against this pattern. While this is Phase 2 (strategy, not execution), the tautological test is COMMITTED in COMMITMENTS.md and will be implemented at Phase 3 if not corrected now. This is a prospective regression trigger — fixing it now prevents a guaranteed regression at Phase 3/4 review. |

**Regression trigger assessment:** One prospective trigger identified (tautological closure test). This does not require regression (we are at Phase 2, not downstream), but it absolutely requires correction before Phase 3 begins.

---

## Motivated Reasoning Check

- **Is the result dressed up as agreement due to inflated uncertainties?** N/A at Phase 2 (no result yet). However, the precision estimates (Section 8) are plausible and grounded in reference analysis values. No concern.
- **Is any calibration circular?** The d0 resolution calibration (negative tail) is genuinely independent of R_b. The eps_c and eps_uds come from MC without independent calibration, but the strategy acknowledges this and assigns inflated systematics. No circularity detected at the strategy level.
- **Is a limitation acknowledged but not reflected in the result?** The single MC sample [L1] is acknowledged and the systematic is stated as "1.5-2x published." This is appropriate.
- **Will anything "be addressed later" that could change the result?** The PDG inputs (finding #6) and primary vertex definition (finding #7) could affect the result. These must be resolved before Phase 3.

---

## Verdict: ITERATE

**Rationale:** Seven Category A findings and fourteen Category B findings are unresolved. No Phase 2 strategy can pass review with this many blocking items.

The strategy is fundamentally sound — the physics choices (double-tag for R_b, hemisphere jet charge for A_FB^b, constrained R_c) are correct and well-justified. The constraint mitigations are thoughtful. The systematic plan is comprehensive in scope. The reference analysis table is well-populated. The document reflects serious engagement with the literature.

However, the strategy contains:
- A wrong formula (gluon splitting correction)
- A missing dominant systematic (angular-dependent tag efficiency for A_FB^b)
- A tautological validation test committed without acknowledgment
- An inconsistent extraction formula pair (A_FB^b)
- A potentially wrong functional form for sigma_d0 that directly affects both observables
- Unresolved mandatory numerical inputs
- An unspecified fundamental analysis input (primary vertex definition)

These must be corrected before Phase 3 can proceed with confidence.

---

## Priority-Ordered Fix List for Fixer Agent

### Category A (must resolve — listed in priority order)

1. **Gluon splitting formula (Finding #1).** Replace the ad hoc formula in Section 10.2 (`R_b(corrected) = R_b(measured) - g_bb * (eps_g/eps_b)^2`) with the correct treatment from hep-ex/0509008 Section 5.4. The correction enters through the modified double-tag equations (effective eps_uds = eps_uds(direct) + g_bb * eps_g), not through direct R_b subtraction. Update COMMITMENTS.md to specify that g_bb enters through the corrected double-tag formula.

2. **A_FB^b angular-dependent tag efficiency (Finding #2).** Add an explicit systematic source to Section 7.4: "Angular dependence of b-tag efficiency" — the tag efficiency varies with |cos(theta)| due to VDET hit coverage, changing the effective b-purity across the angular range. Commit to measuring or parameterizing this dependence. This is one of the dominant A_FB^b systematics in published analyses.

3. **Closure test redesign (Finding #3).** Rewrite the closure test commitment in COMMITMENTS.md. The current "independent MC split" test is tautological by construction (same generator, same detector model in both halves). Replace with a meaningful test. Options: (a) negative-d0 pseudo-data test (extraction should give R_b = 0 for zero-lifetime signal), (b) bFlag=4 vs bFlag=-1 split to check tagger consistency, (c) artificial contamination injection with known analytical shift. Explicitly state in STRATEGY.md Section 9.1 that a simple MC half-split is an algebra check, not a closure test.

4. **A_FB^b formula normalization (Finding #4).** Resolve the inconsistency between the simplified formula (`A_FB^b = (8/3) * <Q_FB> / (R_b * delta_b)`) in Section 4.2 and the tagged-sample formula in Section 6.3. Designate the self-calibrating fit (inspire_433746 Section 4) as the governing extraction method. Label the simplified formula as an approximation valid only for 100% pure samples. The COMMITMENTS.md extraction formula entry must reference the self-calibrating fit, not the simplified formula.

5. **sigma_d0 angular dependence (Finding #5).** Verify the functional form against the ALEPH detector paper (537303). For d0 in the Rphi plane, the standard form is B/(p sin(theta)), not B/(p sin^{3/2}(theta)). If the d0 branch is the Rphi projection, correct the formula. If it is a 3D quantity, justify sin^{3/2}(theta) with an explicit derivation. Add "sigma_d0 functional form" as a systematic: vary between sin(theta) and the alternative and propagate to both R_b and A_FB^b.

6. **PDG inputs (Finding #6).** Fetch and cite the required numerical inputs: M_Z, Gamma_Z, B hadron lifetime averages, B meson decay multiplicities from PDG 2024. Resolve all "NEEDS FETCH" entries in INPUT_INVENTORY.md with actual values and citations. The values do not need to appear in STRATEGY.md itself, but they must be resolved in INPUT_INVENTORY.md before review can pass.

7. **Primary vertex definition (Finding #7).** Add a [D] decision label specifying the primary vertex strategy. Investigate what the stored d0 is relative to (global event vertex, beam spot, or per-hemisphere vertex). Document the finding and its implications for sigma_d0 and C_b. If d0 is relative to a global vertex including the track under test, acknowledge the bias and plan mitigation. Update COMMITMENTS.md.

### Category B (must fix before PASS — listed in priority order)

8. **Mass tag commitment (Finding #8).** Clarify whether Approach A uses P_hem only or the combined probability-mass tag. Recommend committing to the combined tag (implementable from available 4-vectors). Update [D3] and [D8] accordingly.

9. **C_b measurement strategy (Finding #10).** Describe how C_b will be determined without MC truth. Commit to one of: (a) bFlag=4 proxy for bb events, (b) geometric/kinematic estimation, (c) published value with inflated uncertainty.

10. **A_FB^b precision estimate derivation (Finding #11).** Show the statistical precision calculation explicitly. If the true expected precision is 0.005-0.007 (worse than the quoted 0.004-0.005), update the resolving power assessment.

11. **Thrust axis sign convention (Finding #12).** Specify how "forward" (toward the electron beam) is defined. Verify that the beam direction is recoverable from the ntuple.

12. **R_c impact on R_b quantified (Finding #9).** Compute dR_b/dR_c from the double-tag equations and include the resulting systematic in Section 8.

13. **eps_c control region justification (Finding #13).** Document why a charm-enriched control region is not feasible, or propose one. Specify the eps_c uncertainty range concretely.

14. **cos(theta) binning chi2/ndf (Finding #14).** Commit to reporting chi2/ndf of the angular fit at each configuration. Justify 8-10 uniform bins or add a bin-count scan.

15. **BDT label contamination diagnostic (Finding #15).** Add a specific diagnostic to [D10]: if BDT working point scan shows slope > 1-sigma/range while cut-based is flat, document as evidence of label contamination.

16. **kappa = infinity (Finding #17).** Correct [D5]: kappa = infinity is feasible without PID. Include as an additional working point and measure its delta_b.

17. **R_c cross-check sensitivity (Finding #18).** Add a sensitivity estimate for the R_c float cross-check in Section 4.3.

18. **Year-dependent angular binning (Finding #19).** Add a sub-decision under [D12] on whether angular binning is uniform across years or year-dependent.

19. **y_3 in hemisphere correlation check (Finding #20).** Add y_3 (from ktN2 jet tree) to the list of correlation-inducing variables in Section 7.1.

20. **A_FB^b kappa comparison figure (Finding #21).** Add a flagship figure showing A_FB^b extracted at each kappa value.

### Category C (apply before commit, no re-review required)

Findings #16, #22-32 as listed in the adjudication table.

---

## Reviewer Diagnostic

### Physics Reviewer (andrzej_e80c)

**Role fulfillment:** Strong. Caught the gluon splitting formula error (A1) independently. Identified the missing angular-dependent efficiency systematic (A2) which is a key physics insight that the other reviewers did not raise with the same specificity. The six Category B findings are thorough and well-grounded in the published literature.

**Coverage gaps:** Did not identify the tautological closure test (Critical A1) — this is within scope for a physics reviewer since it concerns the validity of a physics validation. Did not flag the primary vertex definition (Constructive A1) — understandable as this is more of a technical reconstruction detail than a physics judgment.

**Assessment:** Good physics review. The findings are precise and actionable.

### Critical Reviewer (sigrid_16b8)

**Role fulfillment:** Excellent. The most thorough review of the three. Caught the tautological closure test (A1), the A_FB^b formula inconsistency (A2), the gluon splitting formula (A3), the sigma_d0 parameterization (A4), and the unresolved PDG inputs (A5). The conventions coverage check was systematic (B1, B2). The RAG evidence section documents corpus queries used to verify claims.

**Coverage gaps:** Did not raise the primary vertex definition (Constructive A1), which is surprising given the detailed sigma_d0 analysis — the primary vertex is the reference point for d0. Did not raise the angular-dependent tag efficiency (Physics A2) as a systematic gap.

**Assessment:** Strong critical review with good use of corpus queries.

### Constructive Reviewer (nora_766f)

**Role fulfillment:** Good. Identified the primary vertex definition gap (A1), which both other reviewers missed or underweighted. The mass tag finding (A2) is valid but overcategorized — I downgraded it to B. The B findings on R_c sensitivity (B1), angular binning (B2), y_3 (B3), and A_FB^b figure (B4) are concrete and actionable.

**Coverage gaps:** Did not catch the gluon splitting formula error — this is within scope since it affects the resolving power assessment. The A_FB^b formula inconsistency was also not flagged. These are more naturally physics/critical reviewer territory, but a constructive reviewer assessing methodology should ideally catch formula errors that affect the extraction.

**Assessment:** Good constructive review. The primary vertex finding was a genuine catch that improved the adjudication.

### Cross-Reviewer Coverage

The three reviewers provided good complementary coverage:
- Gluon splitting formula: Physics + Critical (2/3)
- Closure test tautology: Critical only (1/3)
- A_FB^b formula inconsistency: Critical only (1/3)
- sigma_d0 parameterization: Physics + Critical (2/3)
- PDG inputs: Critical only (1/3)
- Angular-dependent efficiency: Physics only (1/3)
- Primary vertex: Constructive only (1/3, Physics as B)

No finding was raised by all three reviewers, which suggests the reviews were genuinely independent. The critical reviewer was the most productive, catching 5 of the 7 final Category A findings.

---

## Summary

| Category | Count |
|----------|-------|
| A (must resolve) | 7 |
| B (must fix before PASS) | 13 |
| C (suggestions) | 11 |

**Verdict: ITERATE.** The fixer must address all 7 Category A and 13 Category B findings listed above in priority order before the strategy can be re-reviewed.
