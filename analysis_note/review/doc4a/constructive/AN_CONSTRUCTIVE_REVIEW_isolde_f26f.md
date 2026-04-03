# Constructive Review — Doc 4a Analysis Note (v2, Iteration 2)

**Reviewer:** isolde_f26f (Constructive)
**Date:** 2026-04-02
**Session:** FRESH review — no carryover from v1 constructive
**Artifact:** `analysis_note/ANALYSIS_NOTE_doc4a_v2.tex` (.pdf)
**Inputs read:** v2 .tex in full; results/*.json; COMMITMENTS.md; conventions/extraction.md; TOGGLES.md; REVIEW_CONCERNS.md; v1 constructive review (odette_aaf4); v1 arbiter verdict (zelda_65ac); verification report (vera3_fbef)

**MCP_LEP_CORPUS = true.** Corpus calls made (3 queries executed).

---

## Overall Assessment

The v2 AN is a substantially improved document. The 17 Category A and 16 Category B findings from the v1 arbiter have been addressed at the textual level. The most critical physics additions — quantitative circular calibration bias decomposition, three-attempt INFEASIBLE documentation for operating-point stability and WP 10.0 closure, intercept-inclusive chi2 in the per-kappa table, parameter sensitivity table, and kappa=infinity row — are present and correct.

The analysis remains honest: the R_b result is labeled a self-consistency diagnostic, A_FB^b is correctly zero on symmetric MC, and no physics result is overstated. The honest framing test is passed without reservation.

**However, I identify the following new or residual findings that require attention:**

- **Two Category A items:** (1) the intercept chi2/ndf values (25--34/8) indicate the accepted fit model has chi2/ndf ~ 3--4 and this is not adequately investigated; (2) the angular efficiency systematic for A_FB^b is stated as a "flat borrowed estimate" with no citation and no derivation, violating the uncited-constant rule.
- **Three Category B items:** (1) the high-scale-factor track investigation is present but does not quantify the bias contribution to R_b; (2) the multi-WP eps_uds constraint argument assumes smooth efficiency curves but never validates this assumption even on MC; (3) Section 3.2 claims "no systematic trends in pull distributions" without reporting pull distributions or chi2/ndf values.
- **Several Category C items** for clarity and depth.

**Classification: B** — the AN has no unresolved Category A items from v1, but two new Category A findings emerge from a fresh read of v2. These must be resolved before PASS.

---

## Cross-Phase Concern Review (from REVIEW_CONCERNS.md)

### [CP1] Closure test tautology
**Status: RESOLVED in v2.** The validation summary table (Table 6) now carries the caption "independence is partial (not full)" with explicit language. The three-attempt INFEASIBLE documentation for WP 10.0 is thorough. The v2 correctly distinguishes the mirrored-significance test (code sanity check, not closure) from the 60/40 split closure (partial independence). No further action needed at this phase.

### [CP2] A_FB^b extraction formula
**Status: RESOLVED.** The intercept-inclusive linear regression is clearly the governing extraction. The four-quantity chi2 fit downscoping [D12b] is documented with a Phase 4b risk note (lines 2065--2074). CP2 resolved for Phase 4a.

### [CP3] sigma_d0 angular dependence
**Status: RESOLVED.** Equation 5 states "sin(theta) dependence (not sin^{3/2}theta) is the correct form for the Rphi-projected impact parameter." The ALEPH:VDET citation is present. Corpus search did not find a contradicting reference. CP3 resolved.

### [CP4] PDG inputs not yet fetched
**Status: RESOLVED.** B hadron lifetimes are cited to PDG 2024 with values to 4 significant figures. CP4 resolved.

---

## Category A Findings — Must Resolve (Blocks PASS)

### [A1] Intercept-model chi2/ndf of 25--34/8 (chi2/ndf ~ 3--4) is not investigated

**Location:** Table `tab:afb_perkappa` (lines 1779--1790); Section 7.2 (lines 1579--1595); Section 7.4 (lines 1655--1665).

The v2 correctly adds the intercept chi2/ndf column to the per-kappa table. Values range from 17.0/8 (kappa=inf) to 34.4/8 (kappa=1.0), giving chi2/ndf ~ 2.1 to 4.3 across kappa values. Section 7.5 notes: "The residual chi2/ndf ~ 3--4 in the intercept model likely reflects bin-level data/MC shape differences in Q_FB not fully absorbed by the linear model."

This is not a resolution — it is an acknowledgment without investigation. A chi2/ndf of 3--4 in the governing extraction model is a GoF failure (criterion: chi2/ndf < 5 is the hard stop from CLAUDE.md, but < 2 is required for a well-fitting model). The accepted model fits are significantly worse than one would expect for a well-specified linear model with correct error bars. The plausible causes are:

1. The error bars on Q_FB per bin are underestimated (e.g., bin-to-bin correlations not accounted for in the linear regression).
2. The linear model is the wrong functional form (the true angular distribution includes a 1 + cos^2(theta) acceptance term that modifies the Q_FB vs cos(theta) relationship at large |cos(theta)|).
3. There is a genuine data/MC shape difference in Q_FB not accounted for by the systematic budget.

The ALEPH reference analysis (inspire_433746, corpus hit [1]) explicitly accounts for the acceptance degradation at high cos(theta) by fitting the hemisphere tagging efficiencies and charge calculation together. The linear approximation to Q_FB vs cos(theta) is a simplification that may break down at the angular boundaries.

This chi2/ndf situation does not satisfy the validation target rule: the governing extraction model fails a 3-sigma-quality threshold across all kappa values, and the AN offers only a "likely reflects" narrative without a quantitative test. Per `methodology/06-review.md` §6.8, a GoF failure in the governing extraction requires: (1) quantitative explanation, (2) demonstrated magnitude match, (3) no simpler explanation ruled out.

**Actionable fix:** Investigate the residual chi2/ndf ~ 3--4 in the intercept model. At minimum: (a) plot the Q_FB residuals as a function of cos(theta) to identify the pattern (forward/backward excess? edge bins?); (b) test whether including a cos^2(theta) term (from the angular acceptance) improves chi2; (c) check whether the bin-by-bin statistical errors on Q_FB are correctly propagated (not underestimated). Report the investigation in Section 7.4 or as a cross-check subsection. If the chi2 failure is understood and demonstrably non-biasing, state this with evidence. If it is not understood, it is a method failure that blocks advancing.

**Category: A** — the governing extraction model fails chi2/ndf < 2 at all kappa values without a demonstrated explanation. Per the validation target rule and the DEPTH MANDATE for method failures, this is Category A.

---

### [A2] Angular efficiency systematic for A_FB^b has no citation and no derivation

**Location:** Section 7.3.4 (lines 1194--1203); systematics.json field `A_FB_b.angular_efficiency`.

The angular efficiency systematic is reported as delta_AFB(angular) = 0.002. The text states: "Estimated from the VDET coverage limitations." The systematics.json source field reads "STRATEGY.md Section 7.4."

This is an internal document (STRATEGY.md) citing to an internal document, with no published measurement, no numerical derivation, and no MC study supporting the 0.002 value. The conventions rule ("At review, any uncited numeric constant is Category A") applies here. The ALEPH reference analysis (inspire_433746) quantifies the angular efficiency systematic from the measured degradation of tagging efficiency and charge calculation in the high-cos(theta) region and propagates it through the 4-quantity fit. Our AN claims a comparable systematic (0.002) without any calculation.

Note: this systematic is not negligible. It is the second-largest A_FB^b systematic (0.002 vs charm asymmetry 0.0027). At Phase 4b when the real asymmetry (~0.09) is measured, this systematic will be ~2% of the signal. It cannot remain an uncited estimate.

**Actionable fix:** Either (a) derive delta_AFB(angular) = 0.002 analytically from the VDET acceptance and propagate through the extraction formula, citing the formula and input values; or (b) cite a published ALEPH or LEP value for this systematic (inspire_433746 Section 6 gives the angular efficiency systematic as a fraction of the total). Add the derivation or citation to Section 7.3.4.

**Category: A** — uncited numeric constant in a systematic evaluation, per CLAUDE.md and conventions/extraction.md.

---

## Category B Findings — Must Fix Before PASS

### [B1] High-scale-factor track investigation present but bias contribution not quantified

**Location:** Lines 590--610 (sigma_d0 calibration, high-scale-factor investigation).

The v2 correctly adds a paragraph investigating high-scale-factor tracks (bins with scale factors > 5). The discussion identifies that these are 1-VDET tracks at low momentum and large |cos(theta)|, constituting ~8% of the tagged sample. The investigation concludes: "their contribution to the total tag value is small."

However, the bias contribution is never quantified. "Small" is not a number. The relevant question for the systematic budget is: what fraction of the tag value (not just the sample) do these tracks contribute, and what is the resulting delta_R_b from setting them aside vs including them? The 8% sample fraction does not directly translate to an 8% tag-value fraction because low-momentum, large-angle tracks have low impact parameter significances and contribute little to the probability product.

The v1 Category B finding (#22) asked for this investigation. The v2 addresses the qualitative characterization but not the quantitative bias.

**Actionable fix:** Add a sentence with the quantitative contribution: "Tracks with scale factors > 5 contribute X% of the total tag value (sum of -ln P_hem) at WP 10.0. Removing them shifts R_b by delta_R_b = Y, which is Z% of the sigma_d0 systematic (0.00075)." If the contribution is genuinely negligible, state the magnitude.

**Category: B** — investigation present but quantitative conclusion missing. A physicist cannot verify "small" without the number.

---

### [B2] Multi-WP eps_uds constraint argument relies on unvalidated smoothness assumption

**Location:** Section 12.2 (lines 2244--2250); Section 10 (Outlook item 1, lines 2051--2055).

The AN argues that the multi-working-point simultaneous fit will constrain eps_uds from "requiring consistency across working points," reducing the systematic from ~0.387 to ~0.02. The mitigation description states: "With 4 working points (WP = 7, 8, 9, 10), there are 8 measured quantities ... reducing the effective number of unknowns [because] efficiency curves are smooth functions of the working point."

The smoothness assumption is the critical one — if efficiency curves are smooth, the multi-WP system is over-determined and constrains eps_uds. But: (1) WP 7, 8, and 9 have no valid extractions at Phase 4a (solver failure). If the system has no solutions at these WPs, the "smooth curves" constraint cannot be applied — there is no efficiency to interpolate between. (2) The expected reduction from 0.387 to 0.02 is a factor-of-19 improvement, equivalent to constraining eps_uds to +/-0.005. This is a strong claim based on an unvalidated assumption.

The v1 arbiter flagged the "20x improvement claim has not been tested even with a toy study" (motivated reasoning section). The v2 does not add the toy study but also does not escalate the caveat.

**Actionable fix:** Add a sentence to Section 12.2 acknowledging that the smoothness assumption is unvalidated at Phase 4a: "The claim that the multi-WP fit will constrain eps_uds to ~0.005 relies on efficiency curves being smooth functions of working point. At Phase 4a, only WP 10.0 yields valid extractions; the efficiency values at other WPs are ill-defined. The constraint argument will be validated at Phase 4b when data-driven efficiencies at multiple WPs are available." This is an honesty and framing issue — the argument is plausible but presented as more solid than it is.

**Category: B** — the projected 20x systematic reduction is the central promise for Phase 4b; overstating its certainty at this stage is a framing issue that a journal referee would flag.

---

### [B3] Data/MC agreement claims in Section 3.2 are unquantified

**Location:** Section 3.2 (lines 429--451); captions to Figures datamc_event and datamc_track.

Section 3.2 states: "Agreement is generally good, with no systematic trends in the pull distributions." The caption to Figure datamc_event states "Agreement is within 5% across all variables." The caption to Figure datamc_track states "good agreement over three orders of magnitude."

The v1 constructive review (odette_aaf4, finding C2) flagged this as a Category C item. The v2 did not add chi2/ndf or KS p-values to these captions. Since the v1 arbiter listed this as a Category C item, it was not required. However, on a fresh read, the situation is more problematic than Category C:

Section 3.2 says "no systematic trends in the pull distributions" — but no pull distributions are shown or quantified anywhere in the AN. This is a claim without evidence. The data/MC comparisons are shown in figures, but the figures show the raw distributions, not the pulls. A reader cannot verify "no systematic trends" from a ratio plot without the statistical uncertainty on the ratio.

Furthermore, the caption "within 5%" is not a formal statement of agreement — it is a visual estimate. The ALEPH reference analysis (hep-ex/9609005) quantifies data/MC agreement with chi2 values for the variables entering the analysis. The absence of quantitative data/MC agreement metrics means the "Selection" section fails to demonstrate that the data and MC are drawn from the same distribution — a prerequisite for the MC-derived corrections (Section 4) to be valid.

**Actionable fix:** For the primary input variables (d0, pT, and tag variables entering the extraction), add chi2/ndf or KS test p-values to Table 3 (cutflow) or as a dedicated data/MC summary table. The claim "no systematic trends" needs a specific chi2 value for at least the tag discriminant distribution (combined tag), since this is the variable whose data/MC agreement determines whether the MC-derived eps_c and eps_uds are reliable.

**Category: B** — the data/MC agreement claim for the primary analysis variable (combined tag distribution) is unquantified. The extraction conventions require that MC-derived corrections be validated against data. The tag discriminant is the direct input to the extraction. A "good agreement" caption is insufficient.

---

## Category C Findings — Suggestions

### [C1] The circular calibration bias decomposition (Section 8.1) could benefit from a cross-check figure

**Location:** Lines 1709--1735 (bias decomposition).

The decomposition into eps_uds mis-calibration (~0.06) + C_b inflation (~0.005) + residual (<0.001) is well-reasoned and adds significant value. However, a one-panel figure showing the extracted R_b as a function of assumed R_b input (varied from 0.15 to 0.25) would make the circular dependency visually obvious and quantify the self-consistency loop directly. This is a ~30-minute analysis task using existing infrastructure.

Adding this figure would: (1) visually demonstrate the circularity rather than only stating it; (2) provide an independent cross-check of the bias decomposition; (3) answer the question "how sensitive is the extracted R_b to the assumed calibration input?"

**Category: C** — potentially feasible within Phase 4a scope; would substantially strengthen the methodology section.

---

### [C2] The eps_uds 50% variation bound is not connected to the alpha scan range

**Location:** Section 5.1 (lines 924--953); Table `tab:sensitivity`.

The text explains that eps_uds is varied by +/-50% (0.0913 * 0.5 = 0.046) because "in the absence of a data-driven calibration." The v1 finding C3 asked for motivation of the 50% choice. The v2 adds a STRATEGY.md reference but the key physical motivation is not stated.

The more illuminating motivation: the alpha scan ranges from 0.20 to 0.50, corresponding to eps_uds varying from 0.086 to 0.216 (a factor of 2.5). The +/-50% variation is consistent with this scan range uncertainty. Stating this connection explicitly would make the 50% choice self-motivated rather than arbitrary.

**Suggested addition:** "The ±50% variation covers the range of physical solutions found in the alpha scan (alpha = 0.20 to 0.50), which corresponds to eps_uds varying from 0.086 to 0.216 at WP 10.0 — a factor of 2.5 range. The ±50% is a conservative but motivated bound on the physical uncertainty."

**Category: C**

---

### [C3] Working-point selection criterion is still not stated explicitly

**Location:** Section 8.1 (lines 1690--1706); Appendix H (lines 2832--2855).

The v1 constructive finding C10 asked why WP 10.0 was chosen over WP 9.0. Appendix H lists detailed WP statistics but does not state the selection criterion. The text says WP 10.0 "provides the highest b purity" but purity is not defined and the WP 9.0 purity is not shown. Adding one sentence — "WP 10.0 is selected as the primary operating point because it provides the highest estimated b purity (f_d/f_s^2 = 1.50, vs 1.37 at WP 8.0, the next valid WP with physical solutions)" — and explicitly stating that WP 9.0 has only 305/1000 valid toys (making it less stable than WP 10.0 with 200/1000, noting the convergence comparison) would complete this discussion.

**Category: C**

---

### [C4] Future Directions item 3 (z0 impact parameter) underestimates feasibility

**Location:** Section 11, item 4 (lines 2159--2165).

The text states: "The z0 branch is available but its sign convention and resolution properties were not fully characterized in this analysis." The v1 finding C5 (odette_aaf4) flagged this as potentially feasible within Phase 4b. The v2 does not move this or add a feasibility estimate.

Characterizing z0 (applying the same negative-tail calibration protocol, verifying the positive-tail excess in b-enriched hemispheres) is a ~2-hour task. If it is feasible but the decision is to defer it, state explicitly: "The z0 characterization is feasible within Phase 4b scope but is deferred to reduce Phase 4b complexity. Implementing a 3D impact parameter significance would require (a) verifying the z0 sign convention, (b) calibrating sigma_z0 in comparable bins, and (c) building a 3D combined significance. This is planned for Phase 4b if the simplified 2D analysis fails its data quality gates."

**Category: C**

---

### [C5] Systematic table fraction column is still incomplete

**Location:** Table `tab:syst_summary_rb` (lines 1229--1253).

The v1 finding C6 (odette_aaf4) noted the Fraction column shows only 99.5% for eps_uds and "---" for all other sources. The v2 does not add fractions for the remaining rows. For eps_c: 0.078/0.395 = 19.7%. For C_b: 0.010/0.395 = 2.5%. For R_c: 0.008/0.395 = 2.0%. These are all less than the quadrature sum precision, so they individually sum to more than 100% when combined with the dominant eps_uds, but the individual fractions (computed as delta_Rb_i / syst_total) are informative for a reader assessing the budget structure.

**Category: C**

---

### [C6] Figure F4 (f_d vs f_s) should identify the WP 10.0 data point

**Location:** Caption to Figure F4 (lines 1869--1882).

The v1 finding C4 suggested identifying which R_b curve the WP 10.0 data point falls on. The v2 caption does not add this. The caption describes the diagnostic but leaves "the intersection of the data trajectory with the R_b prediction curves determines the extracted R_b" without stating the specific R_b value visible at WP 10.0. Adding "The data at WP 10.0 (rightmost point on the trajectory) falls near the R_b = 0.280 curve, consistent with the extracted value" completes the figure's diagnostic narrative.

**Category: C**

---

### [C7] Corpus comparison: the residual intercept chi2/ndf of 3--4 requires a comparison baseline

**Corpus note from this review.** The DELPHI AFBb measurement (inspire_1661115, corpus hit [3]) uses a chi2-fit to 5 event categories in bins of polar angle, with number of DOF = 15--17 per year and reported chi2 probabilities of 0.05--0.69. The ALEPH reference (inspire_433746) uses a 4-quantity simultaneous fit without reporting intermediate chi2/ndf values for individual kappa fits.

Neither reference uses the simplified linear regression of Q_FB vs cos(theta). The chi2/ndf values of 2.1--4.3 for the intercept model have no published baseline to compare against. This is an additional reason why [A1] above requires investigation — the chi2 values cannot be dismissed by comparison to published results because the method is novel.

**Category: C** — informational for the fixer; supports the A-level finding.

---

## Honest Framing Check

**PASSES.** The v2 maintains and strengthens the v1's honest framing. Key evidence:

1. The abstract explicitly labels R_b as "a self-consistency diagnostic of the circular calibration procedure."
2. The circular calibration bias decomposition (new in v2) adds quantitative honesty about the mechanism.
3. The INFEASIBLE documentation for operating-point stability (3 remediation attempts, each documented with root cause) is exemplary.
4. The D12b risk note (Phase 4b must implement AND validate the four-quantity fit simultaneously) correctly flags an unresolved Phase 4b risk.

The one framing tension remains the multi-WP constraint argument [B2] — this is documented but the strength of the claim relative to the evidence should be moderated.

---

## Resolving Power Evaluation

**R_b:** No resolving power at Phase 4a. Total uncertainty 0.396 >> R_b^SM = 0.216. The 283x precision ratio is correctly quantified and decomposed. The resolving power section (lines 2084--2115) correctly distinguishes Phase 4a from Phase 4b/4c expectations. The new Section 10.2 note about the multi-WP eps_uds constraint path is appropriate.

**A_FB^b:** Method validated at Phase 4a. The total uncertainty (0.0045) is comparable to ALEPH (0.0052). The governing fit has residual chi2/ndf of 2.1--4.3 — see [A1]. If this chi2 reflects genuine shape differences that bias A_FB^b, the resolving power claim for Phase 4b/4c is weakened.

**sin2theta_eff:** Correctly identified as a formula-validation exercise at Phase 4a. No resolving power.

---

## Does the Measurement Discriminate Between Physics Models?

At Phase 4a: No, for R_b. The total uncertainty dwarfs the measurement.

For A_FB^b: The method is validated and structurally sound. But the residual chi2/ndf of 3--4 in the intercept model ([A1]) indicates the model does not fully describe the angular distribution. If this is a bias from angular acceptance effects, the Phase 4b measurement of the real ~0.09 asymmetry could be biased. The expected sensitivity for sin2theta_eff from Phase 4b/4c (delta_sin2theta ~ 0.0004) is comparable to individual LEP measurements — this is a meaningful physics goal. The chi2 failure therefore matters for the physics case.

---

## Depth Check: Per-Section Assessment

| Section | Depth | Most Impactful Missing Element |
|---------|-------|-------------------------------|
| 1. Introduction | Good | — |
| 2. Data Samples | Good | MC event count 771K (cutflow) vs ~7.8M (description) — see critical review v1 item C3; still present in v2 |
| 3. Event Selection | Adequate | Quantitative data/MC chi2 for combined tag distribution [B3] |
| 4. Corrections | Very good | High-scale-factor bias quantification [B1] |
| 5. Systematics | Good | Angular efficiency citation [A2]; multi-WP argument caveat [B2] |
| 6. Cross-checks | Good | — |
| 7. Statistical Method | Good | Intercept chi2/ndf investigation [A1] |
| 8. Results | Honest | The circular-bias figure would substantially strengthen [C1] |
| 9. Comparison | Appropriate for 4a | — |
| 10. Conclusions | Good | — |
| 11. Future Directions | Good | z0 feasibility estimate [C4] |
| 12. Known Limitations | Very good | Multi-WP caveat [B2] |
| Appendices | Good | — |

---

## Summary Table

| ID | Category | Brief Description | Section |
|----|----------|-------------------|---------|
| A1 | **A** | Intercept chi2/ndf ~ 3--4 not investigated; governing model fails GoF without explanation | §7.4, Table 4b-kappa |
| A2 | **A** | Angular efficiency systematic for A_FB^b has no citation and no derivation | §5.4.3, systematics.json |
| B1 | **B** | High-scale-factor track bias contribution not quantified (present but "small" without magnitude) | §4.1 |
| B2 | **B** | Multi-WP eps_uds constraint argument assumes unvalidated smoothness; claim overstated | §12.2, §10 |
| B3 | **B** | Data/MC agreement for combined tag distribution unquantified (chi2/ndf absent) | §3.2 |
| C1 | C | Circular bias decomposition would benefit from a "R_b extracted vs R_b assumed" cross-check figure | §8.1 |
| C2 | C | eps_uds 50% variation should be connected to alpha scan range | §5.1 |
| C3 | C | WP 10.0 selection criterion still not stated explicitly | §8.1, App H |
| C4 | C | Future Directions: z0 characterization feasibility should be estimated | §11 |
| C5 | C | Fraction column in systematic summary table still incomplete | Table syst_summary_rb |
| C6 | C | Figure F4 caption should identify WP 10.0 data point on R_b curve | Fig F4 |

---

## Priority Order for Fixer

1. **[A1] Investigate intercept chi2/ndf ~ 3--4.** Run pull-vs-cos(theta) diagnostic. Test cos^2(theta) modification. Minimum deliverable: a figure showing residuals and a statement of whether the chi2 is uniform in cos(theta) or edge-concentrated.
2. **[A2] Add citation and derivation for angular efficiency systematic (0.002).** Derive from VDET acceptance geometry or cite inspire_433746 Section 6 for the comparable ALEPH value.
3. **[B3] Add chi2/ndf for combined tag data/MC comparison.** At minimum, one KS test p-value for the combined tag distribution.
4. **[B1] Quantify the high-scale-factor track bias contribution.**
5. **[B2] Add caveat to multi-WP smoothness argument.**
6. **C1--C6 as time permits.**

---

## Corpus Evidence Summary

**Corpus query 1** (angular fit chi2, intercept, Q_FB):
- ALEPH (inspire_433746): uses 4-quantity simultaneous fit in each cos(theta) bin, not a linear regression. The chi2 is plotted as a function of m_t (Figure 2 of that paper). No direct comparison to our chi2/ndf values is possible, but the method difference (4-quantity fit vs linear regression) explains why ALEPH achieved well-defined chi2 behavior while our simplified method shows residual chi2/ndf ~ 3--4.
- DELPHI (inspire_1661115): uses chi2-fit to 5 event categories, 15--17 DOF per year, chi2 probabilities of 0.05--0.69 (acceptable range). The DELPHI chi2 probabilities are all acceptable; our chi2/ndf ~ 3--4 would correspond to chi2 probability < 0.01, which is outside the DELPHI range. This supports treating the intercept chi2/ndf as a genuine GoF concern.

**Corpus query 2** (eps_uds constraint, multi-WP):
- LEP combination paper (inspire_1660886): confirms that the multi-WP simultaneous fit requires smooth efficiency functions and is used in the LEP combination context with well-calibrated MC. The constraint argument is standard, but the published implementations (DELPHI, ALEPH) always have MC truth labels and thus well-defined efficiency curves at all WPs. Our Phase 4b situation (no truth labels, circular calibration) is novel and the constraint benefit is less guaranteed.

**Corpus query 3** (intercept chi2 residual angular bins):
- DELPHI (inspire_1661397): hemisphere charge correlations beta and delta enter the chi2 fit and are validated against data. The systematic from correlations is 50% of the QCD correction uncertainty. This suggests that unaccounted hemisphere charge correlations could explain residual chi2 in our linear model — another candidate for [A1] investigation.

---

*Reviewer: isolde_f26f (Constructive) | Date: 2026-04-02*
*MCP_LEP_CORPUS: true | Corpus queries: 3 executed*
