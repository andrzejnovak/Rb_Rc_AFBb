# Physics Review: Doc 4a Analysis Note

**Reviewer:** wolfgang_8bad (Physics Reviewer)
**Document:** ANALYSIS_NOTE_doc4a_v1.pdf
**Date:** 2026-04-02
**Classification: B**

---

## Executive Summary

This analysis note documents the infrastructure for measuring R_b, R_c,
and A_FB^b in hadronic Z decays using archived ALEPH open data. At
Phase 4a, only MC pseudo-data results are presented. The document is
thorough, well-structured, and unusually honest about its limitations.
The A_FB^b method is properly validated (zero on symmetric MC, kappa
consistency confirmed). The R_b extraction is correctly identified as
a circular self-consistency diagnostic rather than a measurement, which
is honest framing. However, the R_b result has a total uncertainty of
0.396 -- nearly twice the value of R_b itself -- rendering it physically
meaningless at this stage. The analysis faces a fundamental structural
problem: an underdetermined calibration system that may not be fully
resolvable even with data.

I classify this as **B** rather than A because the document is candid
about all of these issues, the Phase 4a scope is explicitly limited to
infrastructure validation, and the path to a meaningful measurement
(multi-working-point fit on data) is concrete and plausible. However,
several findings must be addressed before this framework can produce
publishable results.

---

## Detailed Findings

### F1. R_b "self-consistency diagnostic" framing [Category B]

**Assessment: Honest framing, but the implication needs scrutiny.**

The note correctly labels R_b = 0.280 +/- 0.031 (stat) +/- 0.395 (syst)
as a "circular calibration self-consistency diagnostic" (Section 8.1).
This is honest. The calibration assumes R_b = R_b^SM = 0.21578 to
derive efficiencies, then extracts R_b using those efficiencies. The
extracted value of 0.280 deviates from the input 0.216 by 0.064 -- a
30% residual bias from the circular procedure. This is documented
transparently.

However, there is a concern: the note presents this 0.064 deviation as
"quantifying the residual bias of the circular procedure" but does not
adequately explain WHY the circular procedure produces a 30% bias. If
the method were perfectly self-calibrating, the circular extraction
should return the input value. A 30% residual bias suggests that the
"self-calibrating" property of the double-tag method is substantially
degraded by the external inputs (R_c, C_b, epsilon_c, epsilon_uds).
The note should quantify which external input is responsible for the
0.064 shift and whether this bias cancels or persists when moving to
data.

**Recommendation:** Add a breakdown of the 0.064 bias by source.
Demonstrate that the multi-WP fit is expected to reduce this bias,
not merely the uncertainty.

---

### F2. The 278x precision ratio for R_b [Category B]

**Assessment: The decomposition is convincing but the prognosis is
uncertain.**

The Precision Investigation (Appendix F) decomposes the 283x ratio
vs ALEPH into four factors:
1. epsilon_uds unconstrained (283x -> 9x)
2. No truth-label calibration (9x -> 3x)
3. Simplified 1-tag system (3x -> 1.5x)
4. MC statistics (1.5x -> 1x)

This decomposition is quantitative and well-argued. The dominant factor
is the unconstrained epsilon_uds, which contributes delta_R_b = 0.387
(99.5% of the systematic budget). The note claims the multi-WP fit in
Phase 4b will reduce this from ~0.387 to ~0.02, a ~20x improvement.

**Concern:** This 20x improvement is a projection, not a demonstration.
The operating point stability scan (Table 12, Figure 16) shows that
only WP 10.0 yields a valid extraction; WPs 7.0, 8.0, and 9.0 all
return null (solver failure or unphysical solutions). A multi-WP fit
requires multiple valid working points. The note acknowledges this
(Section 12.4) and argues that on data the circular constraint is
relaxed, making more WPs viable. This is plausible but unproven.

The projected 10-20x final precision ratio is honest given the
structural limitations (no truth labels, 1-tag system, no per-hemisphere
vertex). The question is whether the multi-WP fit will actually work on
data. If it does not, R_b is not a measurement but a diagnostic.

**Recommendation:** In Phase 4b, demonstrate the multi-WP fit
explicitly. If only one WP produces a valid extraction on data, this
must be escalated as a fundamental limitation, not deferred further.

---

### F3. A_FB^b being zero on MC [Category C]

**Assessment: Expected and properly validated.**

The MC does not embed an electroweak forward-backward asymmetry (the
cos_theta distribution is symmetric at generator level). Therefore
A_FB^b approximately 0 on MC is the correct result, not a failure.

The method validation is solid:
- Combined A_FB^b = -0.0001 +/- 0.0022 (stat) +/- 0.0040 (syst),
  consistent with zero.
- Kappa consistency: chi2/ndf = 0.71/4 (p = 0.95), excellent.
- The intercept-inclusive fit model correctly handles the hemisphere
  charge bias (Section 7.3), which would otherwise produce catastrophic
  chi2 values (80-115/9).
- The charge separation delta_b increases with kappa as expected
  (0.165 to 0.562).

The sin2_theta_eff = 0.2500 +/- 0.0004 corresponds to A_e = 0 (maximum
parity violation point), which is the correct mapping of A_FB approximately
0. This confirms the formula works.

**One concern:** The chi2/ndf values in Table 13 (80-115/9 for origin-only
fits) are from the fit WITHOUT the intercept. The note explains that
the intercept-inclusive model fixes this, but the actual chi2/ndf of
the intercept-inclusive fit is not quoted. It should be, to demonstrate
the improvement quantitatively. Figure 17 shows chi2/ndf = 31.9/8
for kappa = 0.5, which is still poor (p approximately 0.0001). This
deserves comment -- is this from the origin-only or intercept-inclusive
model?

**Recommendation:** Quote the chi2/ndf of the intercept-inclusive fit
explicitly for each kappa value. If chi2/ndf = 31.9/8 is from the
intercept-inclusive fit, this is a poor fit and requires explanation.

---

### F4. Circular calibration produces biased R_b [Category A]

The efficiency calibration (Section 4.5) assumes R_b = R_b^SM and
R_c = R_c^SM as MC generation truth, then inverts the double-tag
equations to find epsilon_b, epsilon_c, epsilon_uds. The extracted
R_b = 0.280, not 0.216. This 30% bias is not small.

The note frames this as expected from the circular procedure. But
consider: the double-tag method's self-calibrating property is
supposed to mean that epsilon_b is measured from data (via f_d/f_s),
making the result insensitive to MC modelling. If this property
actually worked, the circular extraction should return approximately
0.216. It does not because the external inputs (epsilon_c = 0.431,
epsilon_uds = 0.0913, C_b = 1.179) are NOT self-calibrated -- they
are taken from MC assuming SM truth.

The 0.064 bias is entirely driven by these external inputs. This means
the R_b extraction is NOT self-calibrating in any meaningful sense at
the current level of precision. It is a measurement of R_b that depends
heavily on assumed epsilon_c and epsilon_uds values.

**The critical question for Phase 4b:** When epsilon_uds is constrained
from data via multi-WP fit, does the R_b bias reduce proportionally?
The answer depends on whether the multi-WP fit can break the degeneracy
between epsilon_uds and epsilon_c. The note does not demonstrate this.

**Recommendation:** Run a toy study: generate pseudo-data at multiple
working points with known R_b, epsilon_b, epsilon_c, epsilon_uds; fit
simultaneously; verify that R_b is recovered without bias. This is
essential before claiming the multi-WP fit will work on data.

---

### F5. Operating point stability failure [Category A]

Only 1 of 4 tested working points (WP 10.0) yields a valid R_b
extraction. WPs 7.0, 8.0, and 9.0 all fail (solver failure or
unphysical epsilon_b > 1). This is documented in Table 12 and
Section 12.4.

The validation test summary (Table 12) explicitly marks this as
**FAIL** (operating_point_stability.passes = false). This is honest.
But the analysis proceeds despite this failure, with the argument
that the circular calibration constrains the system to a narrow
parameter space, and data will relax this.

**Problem:** A measurement that works at only one operating point
cannot have its systematic uncertainties validated. The standard
approach is to verify that the extracted value is stable across
working points. Here, there is no stability to check. The systematic
from epsilon_uds (which dominates at 99.5%) is evaluated by a +/-50%
variation at the single working point, producing a shift of 0.387.
But this is not a meaningful systematic evaluation -- it is an
acknowledgment that the parameter is unconstrained.

**Recommendation:** This failure must not be carried forward silently
into Phase 4b. The multi-WP fit must demonstrate stability across at
least 3 working points, or R_b cannot be reported as a measurement.

---

### F6. epsilon_c assumed too small in Phase 3 [Category B]

The Phase 3 nominal assumption was epsilon_c = 0.05. The calibrated
value from MC (Section 4.5) is epsilon_c = 0.431 at WP 10.0. This is
a factor of 8.6 error. The note acknowledges this (Section 4.5:
"10-100x too low").

This matters because the entire operating point scan and closure test
infrastructure was built on the assumption of small charm contamination.
The large epsilon_c (charm hadrons with c*tau approximately 100-300 um
producing significant lifetime signatures) means the tagger does not
cleanly separate b from c. At WP 10.0, the charm efficiency is 43% of
the b efficiency -- this is not b-tagging with charm background; this
is b+c tagging with light-quark background.

**Impact:** The double-tag equations are mathematically correct regardless
of epsilon_c, but the sensitivity to epsilon_c at delta_R_b = 0.078
(for +/-30%) is the second-largest systematic after epsilon_uds. The
+30% direction produces solver failure, indicating the system is near
a physical boundary.

**Recommendation:** Discuss whether the combined tag working point
should be optimized for b/c separation rather than overall b purity.
The mass component (M_displaced > 1.8 GeV/c^2) was designed for this,
but its effectiveness at rejecting charm should be demonstrated with
a charm-enriched validation sample (if constructible without truth
labels).

---

### F7. Hemisphere correlation C_b is anomalously large [Category B]

C_b approximately 1.2-1.5 across working points, compared to the published
ALEPH value of approximately 1.01. The note provides a quantitative
decomposition (Section 4.6):
- Shared thrust axis and event vertex: Delta_C_b approximately 0.30
- Gluon radiation: Delta_C_b approximately 0.15
- Resolution correlation: Delta_C_b approximately 0.05
- Total: approximately 0.50, consistent with C_b - 1 = 0.537 at WP 10.0.

The explanation is physically sound. The dominant source (shared vertex)
is a known consequence of using a global event vertex rather than
per-hemisphere vertex reconstruction. The data/MC agreement on C_b
(Delta_C_b < 0.01) validates the MC estimation.

However, C_b = 1.54 means the double-tag fraction is inflated by 54%
relative to the uncorrelated expectation. This substantially degrades
the statistical power of the double-tag method, because the excess
double-tags are correlation artifacts, not independent b-tags.

**Recommendation:** Quantify the effective statistical power loss from
the inflated C_b. The statistical uncertainty on R_b (0.031) may be
artificially small because the large C_b inflates f_d, making the
double-tag sample larger than it should be for independent hemispheres.

---

### F8. Closure test at WP 10.0 not performed [Category A]

The independent derivation-validation closure test (Section 6.6.2) was
performed at WP 7.0 (null extraction, 97.5% toy failure) and WP 9.0
(pull = 1.93, pass). WP 10.0 -- the actual operating point used for
the measurement -- was NOT tested on the validation split. The note
documents this as a "documented gap."

This is a significant omission. The primary extraction point must be
validated. The note does not explain why WP 10.0 was excluded from
the closure test. If the 60/40 derivation/validation split leaves
insufficient statistics at WP 10.0, this should be stated explicitly
with the relevant numbers.

**Recommendation:** Perform the closure test at WP 10.0. If this is
infeasible due to statistics, document the specific numbers (how many
events pass the tag at WP 10.0 in the 40% validation set) and perform
a bootstrap closure test instead.

---

### F9. chi2 of Q_FB fit (Figure 17) [Category B]

Figure 17 shows the mean forward-backward charge asymmetry <Q_FB> vs
cos_theta_thrust for kappa = 0.5, with chi2/ndf = 31.9/8. This
p-value is approximately 10^{-4}, which is a very poor fit. The note
does not comment on this.

If this is the intercept-inclusive fit (a_0 + a_1 cos_theta), a
chi2/ndf of 4.0 with 8 bins and 2 parameters (6 dof) would already
be concerning. chi2/ndf = 31.9/8 is pathological.

Possible explanations: (a) the uncertainties are purely statistical
and the data/MC disagreement produces genuine scatter; (b) there is a
non-linear dependence of <Q_FB> on cos_theta that the linear model
does not capture; (c) the fit is to the wrong model (origin-only).

**Recommendation:** Clarify whether chi2/ndf = 31.9/8 is from the
origin-only or intercept-inclusive fit. If intercept-inclusive, this
is a physics problem (non-linear cos_theta dependence) and must be
investigated. Add the actual chi2/ndf for the intercept-inclusive model
to Table 13 and Figure 17.

---

### F10. Systematic uncertainties: several are borrowed, not measured [Category B]

Several systematics are scaled from published ALEPH values rather than
evaluated from this analysis:
- sigma_d0 parameterization: scaled from ALEPH (0.00050) with 1.5x
  inflation factor -> 0.00075
- Hadronization model: scaled from ALEPH (0.00030) with 1.5x factor
  -> 0.00045
- Angular efficiency for A_FB^b: "estimated from VDET coverage
  limitations" -> 0.002

These are guesses, not measurements. The 1.5x inflation factor is
arbitrary. However, these are all subdominant (total contribution
approximately 0.001, negligible compared to the 0.387 from epsilon_uds).
At Phase 4b/4c, when epsilon_uds is constrained and these become
relatively more important, they should be properly evaluated.

**Recommendation:** Flag the borrowed systematics explicitly in Table 9
with a distinct marker. When the multi-WP fit reduces the epsilon_uds
systematic, re-evaluate whether the borrowed systematics need proper
measurement.

---

### F11. R_c is not measured [Category C]

R_c is constrained to the SM value (0.17223 +/- 0.003) and propagated
as a systematic. This is stated clearly in Section 8.4 and Table 1.
The physics prompt requested measurement of R_c, but the analysis
correctly identifies that R_c cannot be independently measured with
the available tagging system (no charm-enriched tag independent of the
b-tag). This is an honest acknowledgment.

However, the note does not discuss whether R_c could be extracted from
the multi-WP fit as a by-product. The charm efficiency epsilon_c varies
strongly with working point (0.62 at WP 7.0 to 0.43 at WP 10.0). If
the multi-WP fit constrains epsilon_c from data, it might be possible
to extract R_c simultaneously rather than constraining it. This would
fulfill the physics prompt more completely.

**Recommendation:** Assess whether R_c extraction from the multi-WP fit
is feasible in Phase 4b.

---

### F12. Data/MC normalization method [Category C]

All data/MC comparison plots use MC "normalized to data" (integral
normalization). This is stated in figure captions. For shape comparisons
this is appropriate, but it hides any overall normalization disagreement
(luminosity x cross-section mismatch). Since this analysis uses
count-based fractions (f_s, f_d) rather than absolute cross-sections,
the normalization method does not affect the physics result. Noted
for completeness.

---

### F13. Future Directions: multi-WP fit is critical, not optional [Category B]

The Outlook (Section 10.1) lists the multi-WP simultaneous fit as
item 1. The Conclusions (Section 10) state the infrastructure is
"complete and validated." But R_b with sigma_total = 0.396 is not a
measurement -- it is a proof of concept. The multi-WP fit is not a
"future improvement"; it is a prerequisite for any physics result.

**Recommendation:** Reframe the Conclusions to state clearly that Phase
4a demonstrates feasibility but does NOT produce a physics result for
R_b. The analysis is in a "methods development" state until the
multi-WP fit is demonstrated on data.

---

### F14. Narrative consistency check [PASS with caveats]

The quality of early figures (data/MC comparisons, selection plots)
is consistent with the quality of the final result. Early plots show
generally good data/MC agreement (within 5% after integral normalization)
with some known discrepancies (d0 tails, ~10% resolution difference).
The final R_b result is poor (0.280 vs 0.216 input, total uncertainty
0.396). This is CONSISTENT -- bad inputs (underdetermined calibration)
produce a bad result. There is no "broken journey, perfect destination"
pattern. The note does not hide problems behind good-looking results.

The one concern is that the kappa consistency test for A_FB^b gives
chi2/ndf = 0.71/4 (p = 0.95). This is suspiciously good -- on 4 dof,
this p-value means all kappa extractions are remarkably close to each
other. However, on symmetric MC where the true A_FB = 0, all kappa
values SHOULD give zero, so perfect consistency is expected. This is
not suspicious in context.

---

## Figure-by-Figure Assessment

**Figure 1 (cutflow):** Clear, informative. Data/MC comparison in bar
chart format is readable. PASS.

**Figure 2 (event-level variables):** Four-panel layout. Pull distributions
centered on zero, within +/-2 sigma for thrust, cos_theta, N_ch. Sphericity
shows some structure at low values. Overall adequate. PASS.

**Figure 3 (track variables):** Track p_T shows good agreement over 3
orders of magnitude. d0 core agrees; tails show known resolution
discrepancy. PASS.

**Figures 4-6 (Phase 1 data/MC):** Early exploration comparisons on 5000
events. Large statistical errors as expected. No red flags. PASS.

**Figure 7 (sigma_d0 calibration):** Scale factors 1.3-7.6, wide spread.
Data systematically higher than MC (worse resolution in data). This is
the expected direction. PASS.

**Figure 8 (signed impact parameter validation):** Shows positive/negative
asymmetry in b-enriched sample. Clear validation of sign convention.
The "Gate: PASS" annotation is appropriate. PASS.

**Figure 9 (hemisphere tagging variables):** Combined tag and -ln P_hem
distributions. Good data/MC agreement. Two-peak structure in -ln P_hem
physically expected. PASS.

**Figure 10 (displaced mass and signed significance):** Mass threshold at
1.8 GeV/c^2 clearly visible. Good agreement. PASS.

**Figure 11 (calibrated efficiencies):** epsilon_b, epsilon_c, epsilon_uds
vs working point. Smooth trends. Note epsilon_c panel is missing axis
label at right edge (appears cropped). Minor cosmetic issue. PASS.

**Figure 12 (C_b vs working point):** Shows C_b for MC and data, with
published ALEPH value (1.01) for reference. The large discrepancy
(1.1-1.5 vs 1.01) is clearly visible and honestly presented. PASS.

**Figure 13 (systematic breakdown):** Log-scale bar chart. epsilon_uds
dominance is immediately visible. Effective communication. PASS.

**Figure 14 (kappa consistency):** A_FB^b at each kappa, all consistent
with zero. chi2 annotation present. PASS.

**Figure 15 (Phase 3 closure diagnostics):** Three-panel diagnostic.
Information-dense but readable. PASS.

**Figure 16 (R_b stability scan):** Shows extraction at WP 9.6-10.4.
Only WP 10.0 yields a value. ALEPH and LEP bands shown. Honest
presentation of a poor result. PASS.

**Figure 17 (Q_FB angular distribution):** chi2/ndf = 31.9/8 is
concerning (see F9). The slope is consistent with zero as expected.
CONDITIONAL PASS -- needs clarification of fit model.

**Figure 18 (f_d vs f_s diagnostic):** Elegant double-tag method
diagnostic showing prediction curves for different R_b values. Good
physics visualization. PASS.

**Figures 19-20 (Phase 1 auxiliary):** |d0| and track weight comparisons.
Adequate. PASS.

**Figures 21-22 (Q_FB data/MC at all kappa):** Good agreement across
all kappa values. PASS.

**Figure 23 (Phase 3 operating point scan):** Pre-calibration R_b scan
showing the bias from uncalibrated efficiencies. Useful context. PASS.

**Figure 24 (Phase 4a closure tests):** Two-panel composite. Independent
closure at WP 9.0 and corrupted-correction sensitivity. Informative.
PASS.

---

## Statistical Methodology Check

1. **Chi2 with full covariance:** The statistical covariance matrix
   (Eq. 18) is diagonal, which is correct because R_b, A_FB^b, and
   sin2_theta_eff are extracted from independent data subsets (counting
   vs angular fit). The systematic covariance (Eq. 19) includes a 10%
   R_b-A_FB^b correlation through shared b-tag efficiency. Reasonable.

2. **Toy-based statistical propagation:** 1000 toys for R_b with only
   200/1000 convergence rate at WP 10.0. This low convergence rate
   means the statistical uncertainty is estimated from a subset of
   toys where the solver happened to converge. This could bias the
   uncertainty estimate if convergence correlates with the fluctuation
   direction. The note should check whether the converged-toy R_b
   distribution is symmetric.

3. **Closure test independence:** The derivation-validation split
   (60/40 on the same MC sample) provides partial independence. The
   calibration truth (R_b = R_b^SM) is assumed in both subsets, so
   the closure test is self-consistent by construction for the
   calibration aspect. This is acknowledged (Section 12.1, item 2).

4. **Arbitrary systematics:** The 1.5x inflation factor on sigma_d0
   and hadronization model systematics is not derived from data. This
   is flagged in F10.

---

## Input Provenance Assessment

Table 1 provides a clear provenance table with color-coded entries
(measured in blue, external in red). This is excellent practice. The
analysis measures f_s, f_d, epsilon_b, C_b, and delta_b from data/MC;
takes R_c, g_bb, g_cc, A_FB^c, delta_QCD from external sources. The
balance is reasonable for a double-tag method.

The note does NOT disguise a meta-analysis as a measurement. The
measured quantities are genuinely extracted from the data sample. The
external inputs are parameters that cannot be measured from the available
data (no truth labels for epsilon_c, no charm tagger for R_c, no higher-
order QCD calculation capability).

---

## Commitment Traceability

The abstract commits to measuring R_b, R_c, and A_FB^b. At Phase 4a:
- R_b: self-consistency diagnostic (not yet a measurement) -- PARTIAL
- R_c: constrained to SM, not measured -- ACKNOWLEDGED
- A_FB^b: method validated at zero -- ON TRACK

The introduction mentions the 2.8-sigma tension in the LEP/SLD combined
A_FB value, which is the physics motivation. The analysis is positioned
to contribute to this with data.

No commitments appear silently dropped. The downscoping of the BDT
tagger (D9, D10) is documented in Appendix I with justification.

---

## Overall Assessment

**Strengths:**
- Exceptional transparency about limitations and failures
- Quantitative decomposition of the precision gap (Appendix F)
- Input provenance table (Table 1) and systematic completeness
  cross-reference (Table 25)
- Proper validation of the A_FB^b method on symmetric MC
- Comprehensive appendix structure documenting all investigations

**Weaknesses:**
- R_b is not a measurement at this stage (total uncertainty 183% of
  the SM value)
- Operating point stability fails (1/4 valid extractions)
- Closure test missing at the primary working point (WP 10.0)
- chi2/ndf of the Q_FB fit (31.9/8) is unexplained
- Several systematics are borrowed rather than measured
- The 30% R_b bias from circular calibration is not decomposed by source

**Would I approve this for publication?**

Not in its current state. This is a methods paper / technical note, not
a physics measurement. It demonstrates that the infrastructure works
for A_FB^b (where the method validation is clean) but not yet for R_b
(where the circular calibration and underdetermined system create
fundamental problems).

For publication, the analysis needs:
1. Multi-WP fit demonstrated on data (Phase 4b)
2. R_b stability across at least 3 working points
3. Closure test at the primary working point
4. R_b total uncertainty reduced to at most 10-20x the ALEPH precision
   (currently 283x)

The A_FB^b measurement on data (Phase 4b/4c) could be publishable
independently if the statistical precision is competitive with
individual LEP measurements. The projected uncertainty of 0.0045
compares to the ALEPH published value of 0.0052, suggesting this
is achievable.

---

## Finding Summary

| ID  | Category | Finding |
|-----|----------|---------|
| F1  | B | R_b bias from circular calibration not decomposed by source |
| F2  | B | 278x precision ratio: multi-WP improvement is projected, not demonstrated |
| F3  | C | A_FB^b zero on MC: properly validated, minor chi2 clarification needed |
| F4  | A | Circular calibration produces 30% R_b bias; toy study needed for multi-WP |
| F5  | A | Operating point stability FAIL: only 1/4 valid extractions |
| F6  | B | epsilon_c = 0.431 vs Phase 3 assumption of 0.05: impact on tag optimization |
| F7  | B | C_b = 1.2-1.5 vs published 1.01: effective statistical power loss unquantified |
| F8  | A | Closure test at WP 10.0 (primary extraction point) not performed |
| F9  | B | chi2/ndf = 31.9/8 for Q_FB fit unexplained; fit model ambiguous |
| F10 | B | Borrowed systematics (sigma_d0, hadronization): not measured, 1.5x arbitrary |
| F11 | C | R_c not measured; assess multi-WP extraction feasibility |
| F12 | C | Data/MC integral normalization: appropriate for shape comparisons |
| F13 | B | Multi-WP fit is prerequisite, not optional improvement |
| F14 | -- | Narrative consistency: PASS (bad inputs produce bad result, honestly presented) |

**Category A findings (3):** F4, F5, F8
**Category B findings (7):** F1, F2, F6, F7, F9, F10, F13
**Category C findings (3):** F3, F11, F12
