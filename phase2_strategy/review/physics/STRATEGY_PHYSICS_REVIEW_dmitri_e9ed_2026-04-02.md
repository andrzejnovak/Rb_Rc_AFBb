# Physics Review — STRATEGY.md (Phase 2, Iteration 2)

Reviewer: dmitri_e9ed | Date: 2026-04-02

Inputs: `prompt.md`, `phase2_strategy/outputs/STRATEGY.md`

---

## Overall Assessment

This is a thorough and well-structured strategy document. The physics motivation is sound, the observable definitions are correctly stated, the double-tag formalism is properly laid out, and the constraint mitigation plans are mostly sensible. The document demonstrates genuine understanding of the LEP R_b/A_FB^b analysis methodology and its adaptations to the available data constraints. Several issues remain that need attention, ranging from physics-critical to advisory.

---

## Findings

### (A1) — Circular reasoning risk in R_c constraint — Category B

**Section 4.3:** The strategy constrains R_c to the SM value (0.17223) rather than the LEP measured value (0.1721 +/- 0.0030), arguing this "avoids circular dependence on the measurement we are validating against." But the SM prediction for R_c is itself derived from the same electroweak framework that predicts R_b. If the goal is to test the SM at the Zbb vertex, fixing R_c to its SM value assumes the SM is correct for the Zcc vertex. This is a mild logical tension, not a fatal flaw — the sensitivity dR_b/dR_c ~ -0.05 makes the numerical impact small (~0.00015). However, the strategy should explicitly state that the LEP measured R_c (0.1721 +/- 0.0030) is used as a cross-check constraint, and that the difference between SM and measured R_c central values is propagated to verify the impact is negligible. The document partially addresses this but should commit to reporting R_b extracted with both constraints.

### (A2) — The sign convention for d0 needs a data-level validation plan — Category A

**Section 5.1, item 4:** The strategy describes the sign convention for d0 (positive = displaced toward jet axis) but does not commit to a concrete Phase 3 validation that the stored d0 branch actually follows this convention. If the sign convention is wrong (e.g., d0 is unsigned, or the sign is defined differently), the entire lifetime tag is invalidated — positive d0 tails would mix resolution and lifetime contributions, and the negative-tail calibration method breaks down.

**Required action:** Commit to a Phase 3 check: plot d0 for tracks in hemispheres tagged by bFlag (or at high thrust, where b enrichment is natural) and verify that the positive tail is enhanced relative to the negative tail. If the distribution is symmetric, d0 is unsigned and the strategy must be revised. This is a make-or-break check that should be elevated to a [D] decision.

### (A3) — Hemisphere correlation C_b estimation without truth labels is under-specified — Category A

**Section 7.1 (Efficiency correlation row):** The three-pronged C_b estimation plan is described at a high level, but the physics content is thin. Prong (a) uses bFlag=4 as a b-enriched proxy — but bFlag=4 tags 94% of events, which the document itself notes (Section 9.6) is far too inclusive to be a b-tag. Using a 94%-inclusive flag as a "b-enriched subsample" gives essentially the full sample, not a b-enriched one. Prong (b) ("compute from full MC and correct for non-b contamination using fitted f_b") is circular: f_b depends on C_b through the double-tag equations.

The only robust prong is (c) — using published C_b values with inflated uncertainties. But this makes C_b essentially an external input, not a measurement. Given that hemisphere correlations are one of the dominant systematics (estimated ~0.00100 on R_b, the single largest source), the strategy needs a more concrete plan. Specifically: what published C_b values will be used (numerical value + reference)? What inflation factor is applied to the uncertainty? Is C_b varied as a single number or decomposed into its physical sources (shared primary vertex, gluon radiation, detector geometry)?

### (A4) — Missing explicit sin^2(theta_eff) extraction strategy — Category B

**Prompt requirement:** The prompt explicitly asks to "extract sin^2(theta_eff)" from A_FB^b. The strategy mentions sin^2(theta_eff) = 0.2330 +/- 0.0009 as the published ALEPH value (Section 11.3) and the SM prediction 0.23149 (Section 14), but does not describe how sin^2(theta_eff) will be extracted from the measured A_FB^{0,b}. The extraction uses:

  A_FB^{0,b} = (3/4) * A_e * A_b

where A_f depends on sin^2(theta_eff). The inversion from A_FB^{0,b} to sin^2(theta_eff) requires either assuming lepton universality (A_e = A_b function of same sin^2(theta_eff)) or taking A_e from an external measurement. This choice affects the interpretation and uncertainty. The strategy should commit to a specific extraction path and document the external inputs needed.

### (A5) — Closure tests do not actually test closure — Category B

**Section 9.1, item 5:** The three proposed closure tests are creative workarounds for the absence of truth labels, but none of them is a genuine closure test in the standard sense (apply corrections derived from one sample to an independent sample and recover the input):

- **(a) Negative-d0 pseudo-data:** Tests the resolution model, not the full extraction chain. R_b = 0 for zero-lifetime events is a necessary condition but not sufficient — it doesn't test whether the extraction correctly separates b from c from uds.
- **(b) bFlag consistency:** Tests self-consistency but not accuracy. If bFlag is correlated with the tagger, R_b in bFlag=4 will agree with the full sample by construction.
- **(c) Artificial contamination injection:** Tests linearity of the extraction, which is good, but only for one type of contamination (resolution-like events added to the tagged sample).

None of these tests addresses the key question: does the double-tag extraction with parameterized sigma_d0 and MC-derived eps_c, eps_uds, C_b produce the correct R_b? The only genuine test available without truth labels is the comparison of the final result to the published ALEPH measurement. The strategy should acknowledge this limitation honestly and not overstate the closure tests as "replacing" traditional MC-split closure.

### (A6) — Gluon splitting treatment: g_cc value appears high — Category C

**Section 10.1:** The g_cc rate is listed as ~3.3% of hadronic Z events, citing hep-ex/0302003. The standard LEP value is g_cc = (2.96 +/- 0.38)% as stated in Section 7.1, which is the fraction of hadronic events containing gluon-splitting charm pairs. This is consistent. However, the table in Section 10.1 says "~3.3%" — this should be harmonized with the 2.96% value used in the systematic plan, or the 3.3% should be sourced. Minor inconsistency.

### (A7) — kappa = infinity requires clarification on practical implementation — Category C

**Section 4.2, [D5]:** kappa = infinity means "leading particle charge" — the charge of the highest-momentum track. This is well-defined. However, the hemisphere charge formula Q_h = sum q_i |p_L|^kappa / sum |p_L|^kappa in the limit kappa -> infinity is dominated by the single highest-|p_L| track. The practical implementation should use the explicit leading-track definition, not attempt to evaluate the formula at large kappa (numerical overflow). This is a coding detail but worth flagging for Phase 3.

### (A8) — No discussion of beam spot position stability — Category B

The d0 impact parameter is defined relative to some reference point (beam spot, reconstructed primary vertex, or per-hemisphere vertex — investigated under [D17]). If d0 in the ntuple is defined relative to the beam spot, year-to-year and fill-to-fill beam spot position variations could introduce systematic biases in d0 that the per-year sigma_d0 calibration partially absorbs but does not fully address. The strategy discusses per-year calibration (Section 9.4) but does not mention beam spot stability as a systematic source. For archival data, the beam spot position may not be perfectly reconstructed. This should be at least mentioned as an investigation item for Phase 3.

### (A9) — Precision estimate for A_FB^b uses inconsistent formulae — Category C

**Section 8.3:** The counting formula gives sigma ~ 0.0075, then the self-calibrating fit is argued to improve this to ~0.005. The scaling from the published result uses sqrt(4.1M/2.87M) * sqrt(5/4) ~ 1.34, giving 0.0039 * 1.34 ~ 0.0052. But the sqrt(5/4) factor for "reduced kappa set (4 values vs 5)" is incorrect: the strategy commits to kappa = {0.3, 0.5, 1.0, 2.0, infinity} which is 5 values, same as published. If 5 kappa values are used, this correction factor disappears and the estimate becomes 0.0039 * sqrt(4.1/2.87) ~ 0.0047. Not a critical issue for a precision estimate, but the inconsistency between the committed kappa set and the scaling formula should be corrected.

### (A10) — Track weight branch usage unclear — Category C

**Section 6.2:** "Apply per-track weights from weight[] branch." The strategy does not discuss what these weights represent (track quality? reconstruction efficiency? duplicate removal?). Blindly applying unknown weights to the jet charge could introduce bias. Phase 3 should investigate the meaning of the weight branch before using it. This should be flagged as an investigation item.

---

## Summary of Classifications

| ID | Finding | Category |
|----|---------|----------|
| A2 | d0 sign convention validation missing | A |
| A3 | C_b estimation plan under-specified for dominant systematic | A |
| A1 | R_c constraint circular reasoning risk | B |
| A4 | sin^2(theta_eff) extraction path not specified | B |
| A5 | Closure tests do not test what they claim | B |
| A8 | Beam spot stability not discussed | B |
| A6 | g_cc value inconsistency (3.3% vs 2.96%) | C |
| A7 | kappa = infinity implementation note | C |
| A9 | Precision estimate kappa scaling inconsistency | C |
| A10 | Track weight branch meaning unknown | C |

---

## Verdict

**ITERATE.** Two Category A findings (A2, A3) require resolution before this strategy can be considered sound. The d0 sign convention is a single-point-of-failure for the entire analysis — if the sign is wrong or undefined, nothing downstream works. The C_b estimation is the dominant systematic and the current plan has a logical gap (using 94% of events as "b-enriched"). The Category B items (A1, A4, A5, A8) weaken the strategy but are addressable with modest additions.

The document is otherwise strong: the double-tag formalism is correctly stated, the systematic plan is comprehensive, the reference analyses are well-tabulated, and the mitigation strategies for the data constraints are creative and mostly sound. The issues identified are fixable within the current framework.
