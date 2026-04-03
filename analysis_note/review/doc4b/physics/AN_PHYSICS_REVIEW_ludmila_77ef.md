# Physics Review: Doc 4b v1

**Reviewer session:** ludmila_77ef
**Document:** ANALYSIS_NOTE_doc4b_v1.pdf (63 pages, 44 figures)
**Date:** 2026-04-02
**Classification: B** -- conditionally ready for Phase 4c with mandatory actions

---

## Executive Summary

This analysis note documents a measurement of R_b, R_c, and A_FB^b
using archived ALEPH open data at sqrt(s) = 91.2 GeV. The document is
thorough, honest about its limitations, and demonstrates genuine physics
judgment. The R_b extraction on 10% data yields 0.208 +/- 0.066 (stat)
+/- 0.520 (syst), consistent with the SM at 0.12 sigma. The A_FB^b
extraction detects a non-zero asymmetry at 2.4 sigma, but the absolute
value (0.0085) is suppressed 10x relative to the ALEPH published result
(0.0927) due to a clearly identified delta_b overestimation. The analysis
is honest about this failure and proposes concrete fixes for Phase 4c.

The note is well above the threshold for proceeding to Phase 4c, provided
the critical items below are addressed. The delta_b problem is
methodological, not a bug -- the fix (multi-purity fitting) is
well-defined and feasible.

---

## 1. R_b = 0.208 +/- 0.066 on 10% data: does this validate the method?

**Verdict: Yes, with caveats.**

The central value is 0.12 sigma from the SM (0.21578), which is
reassuring. The 10% data result is dramatically better than the Phase 4a
MC diagnostic (R_b = 0.310, biased by 0.094 from the circular
calibration). The improvement from 0.310 to 0.208 when switching from
SM-assumed calibration to the published C_b = 1.01 confirms that the
circular calibration was the dominant Phase 4a bias, and that using
external C_b removes it.

However, the total uncertainty is 0.523 -- 2.5x the central value. The
systematic budget is dominated by epsilon_uds (delta_R_b = 0.499, 96%
of variance), which is a structural consequence of the underdetermined
calibration system with +/-50% conservative variations. This is not a
measurement -- it is a validation that the extraction infrastructure
works on real data. The note states this clearly (Section 8.6: "the R_b
central value is not an independent measurement").

The operating point stability scan (Figure 23) shows valid extractions at
WP 7.0 and WP 10.0, with chi2/ndf = 0.30/1 (p = 0.586). Only 2 of 4
tested WPs yield valid extractions, reflecting the structural limitation
of the large per-WP C_b. This is adequately documented.

**Finding 1 (B): The R_b validation passes, but the precision ratio of
373x vs ALEPH is dominated by the epsilon_uds systematic. The Phase 4c
multi-WP fit is essential for reducing this. The note should state
explicitly what precision is EXPECTED after the multi-WP fit (the
"10-20x" estimate in Section 9.3 should be promoted to a quantitative
projection with assumptions stated).**

---

## 2. A_FB^b = 0.0085 vs ALEPH 0.0927: is the delta_b investigation convincing?

**Verdict: Yes, the investigation is thorough and the root cause is
correctly identified.**

The delta_b overestimation investigation (Section 8.8) is the strongest
part of this note. The analysis correctly identifies that:

- delta_b = sigma(Q_h) overestimates the physical charge separation by
  8-22x across kappa values (Table 19)
- sigma^2(Q_h) = delta_b^2/4 + sigma_res^2, and since sigma_res >> delta_b
  for jet charges, sigma(Q_h) >> delta_b
- The suppression is quantified per kappa, the "needed" delta_b values are
  physically reasonable (0.0075-0.101), and the suppression factors
  (7.5-22x) explain the 10.9x observed ratio

The comparison to the ALEPH method (Section 8.8, "Comparison to ALEPH
method") correctly explains why the published analysis avoids this problem:
ALEPH fits at multiple b-tag purities simultaneously, disentangling
delta_b and A_FB^b without needing an independent delta_b estimate.

The fitted slopes ARE positive and increase with kappa as expected. The
kappa consistency is excellent (chi2/ndf = 0.66/4, p = 0.957). The
intercept model (Section 7.3) correctly absorbs the hemisphere charge
bias. These are genuine validations that the extraction machinery is
correct -- only the normalization (delta_b) is wrong.

**Finding 2 (A): The delta_b investigation is convincing, but the note
should not report sin2(theta_eff) = 0.248 +/- 0.0007 even with a
footnote. This number is derived from a suppressed A_FB^b and is
physically meaningless -- reporting it with a statistical-only uncertainty
invites misinterpretation. Remove Table 24 row for 10% data or replace
the value with "N/A (delta_b bias)" rather than a number.**

**Finding 3 (B): The note correctly identifies two approaches for Phase 4c
(multi-purity fit or MC-truth delta_b calibration). The multi-purity
approach is preferred as it is self-calibrating. However, no feasibility
assessment is given for either approach on the existing data. How many
purity bins are available? What is the expected statistical power of a
simultaneous fit? A brief quantitative estimate (even back-of-envelope)
should be added to Section 10.1.**

---

## 3. Is the analysis ready for Phase 4c?

**Verdict: Yes, conditionally.**

The infrastructure validation is successful:
- R_b extraction works on real data (correct central value, validating
  the double-tag method and calibration chain)
- A_FB^b extraction detects the electroweak asymmetry (positive slopes,
  correct sign convention, kappa consistency)
- Tag fractions agree between data and MC within 3-5% (Table 20)
- C_b agrees between data and MC within Delta_C_b < 0.02 (Table 20)
- The sigma_d0 calibration transfers correctly to data
- All infrastructure validation tests pass (Table 15)

The analysis has correctly identified all critical items for Phase 4c
(Section 10.1) and the Known Limitations section (Section 12) is
admirably honest.

---

## Figure Inspection

### Data/MC comparisons (Figures 2-6, 9-10, 30-34)
Event-level variables (thrust, cos_theta, N_ch, sphericity) show
agreement within 5%, with pull panels centered on zero. No systematic
trends visible. The track-level p_T and d_0 comparisons (Figure 3)
show good agreement over three orders of magnitude. The d_0 tails show
some data-MC discrepancy consistent with the documented 10% resolution
difference. PASS.

### Tagging variables (Figures 9-10)
Combined tag and hemisphere probability show good data/MC agreement.
The two-peak structure in -ln P_hem is physically expected and
well-modeled. Displaced-track mass shows the characteristic b-hadron
peak. PASS.

### Calibration (Figures 7, 11-14)
The sigma_d0 scale factors (Figure 7) range from 1.3 to 7.6, with
data consistently higher than MC. The high-scale-factor bins (>5) are
discussed in the text. The efficiency calibration curves (Figures 11-13)
show smooth behavior. C_b vs WP (Figure 14) shows excellent data/MC
agreement. PASS.

### 10% data results (Figures 23-27, 29-30)
The R_b stability scan (Figure 23) overlays data and MC correctly.
The A_FB^b kappa scan (Figure 25) clearly shows the suppression relative
to ALEPH. The Q_h distributions (Figure 27) show the expected shape
agreement with a slight mean offset in data. The f_d vs f_s diagnostic
(Figure 29) shows data tracking the MC trajectory closely. PASS.

### Closure tests (Figures 18-20, 36)
Mirrored significance correctly gives R_b = 0. Contamination injection
shows directional agreement. Phase 4a closure test (Figure 36) shows
independent closure at WP 9.0 (pull = 1.93). PASS.

**Finding 4 (B): Figure 22 (Q_FB vs cos_theta on MC) shows chi2/ndf =
31.9/8, which is labeled as reflecting "bin-level data/MC shape
differences in Q_FB not fully absorbed by the linear model." This is a
substantial GoF failure. While the intercept model improves over the
origin model dramatically (from chi2/ndf ~ 80-115/9), the residual
chi2/ndf ~ 3-4 suggests the linear model is inadequate. The note
should discuss whether a quadratic term was tested and rejected, or
whether the GoF failure propagates into a systematic on A_FB^b.**

---

## Narrative Consistency Check

The narrative is internally consistent. Early data/MC plots show good
agreement. The C_b inflation is identified, explained physically, and
its impact propagated. The delta_b problem is discovered, investigated,
and correctly flagged as a blocking issue for A_FB^b interpretation.
The circular calibration bias on R_b is explained and resolved by using
published C_b. There is no "broken journey, perfect destination" pattern
-- the R_b result carries honestly large uncertainties, and the A_FB^b
result is honestly flagged as suppressed.

---

## Statistical Methodology Check

**Finding 5 (B): The toy-based statistical uncertainty propagation
(Section 7.5) has a low convergence rate: only ~200/1000 toys produce
valid extractions at WP 10.0. This means the statistical uncertainty
is estimated from a subsample that passes physical constraints. This
is methodologically acceptable (the non-converging toys represent
unphysical fluctuations), but the note should state explicitly whether
the R_b distribution from valid toys is Gaussian. If it is significantly
non-Gaussian, the quoted sigma_stat may not capture the true coverage.
A pull distribution or coverage test should be added for Phase 4c.**

**Finding 6 (C): The covariance matrices (Appendix B) are presented
for Phase 4a. They should be updated with Phase 4b values, or it
should be stated explicitly that Phase 4b covariance is deferred to
Phase 4c (where the delta_b fix changes the A_FB^b covariance
structure).**

---

## Systematic Treatment

The systematic program is comprehensive: 12 sources for R_b, 4 for
A_FB^b, with a completeness cross-reference against the ALEPH reference
(Table 32). The evaluation methods are clearly described.

**Finding 7 (A): The epsilon_c systematic is one-sided (downward shift
only, because +30% causes solver failure). This means the +1sigma
uncertainty on R_b from epsilon_c is formally unbounded. The note
acknowledges this (Section 5.4) but does not propagate it correctly:
Table 9 lists delta_R_b(epsilon_c) = 0.201, which is the -30% shift
only. The total systematic of 0.208 therefore UNDERSTATES the true
uncertainty because the upward direction is missing. This should be
flagged more prominently -- either as an asymmetric uncertainty or with
a statement that the systematic is a lower bound.**

**Finding 8 (B): The epsilon_uds systematic evaluates to zero because
the solver fails at varied values (Table 11: delta_R_b = 0.499 at
+/-50%). This is a legitimate evaluation of the +/-50% variation, but
the zero at Phase 4a (Table 9) and the 0.499 at Phase 4b are
qualitatively different results that arise from different C_b values.
The note discusses this but could make the physics clearer: the C_b
correction moves the operating point from a region where epsilon_uds
variation kills the solver (WP 10.0, C_b = 1.537) to one where it
dominates the budget (WP 7.0, C_b = 1.01).**

---

## Input Provenance

Table 1 provides a clear provenance table. The color coding
(measured/calibrated/external) is useful. The analysis measures f_s,
f_d, epsilon_b, delta_b from data; takes R_c, g_bb, g_cc, A_FB^c,
delta_QCD from external sources; and calibrates epsilon_c, epsilon_uds
from MC.

**Finding 9 (C): The A_FB^c input (0.0707 +/- 0.0035) is taken from
the LEP combined value. This enters through the charm contamination
systematic. The note should verify that the A_FB^c value used is
pole-corrected (A_FB^{0,c}) vs the measured A_FB^c -- these differ by
the QCD correction factor.**

---

## Commitment Traceability

The abstract commits to measuring R_b, R_c, and A_FB^b. The strategy
commits to the double-tag method for R_b, hemisphere jet charge for
A_FB^b, and constrained R_c. All three are delivered:
- R_b: measured (with caveats on precision)
- R_c: constrained to SM (as committed)
- A_FB^b: measured but suppressed (known issue, fix planned)

The strategy decision [D6] to constrain R_c to SM rather than measure
it is justified by the sensitivity analysis (dR_b/dR_c ~ -0.05).

---

## Future Directions Red Flag Check

The Future Directions (Section 11) lists 6 items, all of which require
data or infrastructure genuinely unavailable in the archived format:
per-hemisphere vertex reconstruction (vx/vy branches empty), full 5-tag
system (requires L, X tags needing pid), MC truth labels (bFlag = -999),
3D impact parameter (z0 sign convention uncharacterized), neural network
tag (requires truth for training), dE/dx (not stored). These are
legitimately infeasible. No red flag.

---

## Suspiciously Good Agreement Check

Not triggered. The analysis has substantial GoF failures (angular fit
chi2/ndf ~ 3-4), known biases (circular calibration), and an identified
methodological problem (delta_b). The results are not suspiciously good.

---

## Summary of Findings

### Category A (must resolve before PASS)

**A1.** Remove or clearly mark as "N/A" the sin2(theta_eff) = 0.248
value from the 10% data results. Reporting a number derived from a
10x-suppressed A_FB^b with a statistical-only uncertainty is misleading.
(Finding 2)

**A2.** The epsilon_c one-sided systematic must be flagged as a lower
bound on the upward R_b uncertainty. The total systematic of 0.208
understates the true uncertainty in the upward direction. Add an
asymmetric uncertainty or an explicit caveat in the abstract and results
summary. (Finding 7)

### Category B (should address before PASS)

**B1.** Add a quantitative precision projection for R_b after the
Phase 4c multi-WP fit. The "10-20x" estimate should be backed by
assumptions. (Finding 1)

**B2.** Add a brief feasibility assessment for the multi-purity A_FB^b
fit: how many purity bins, expected statistical power, whether the
existing data supports it. (Finding 3)

**B3.** Discuss whether a quadratic term in the Q_FB(cos theta) fit
was tested, and whether the chi2/ndf ~ 3-4 residual propagates as a
systematic on A_FB^b. (Finding 4)

**B4.** State whether the R_b distribution from valid toys is Gaussian
and whether the 200/1000 convergence rate biases the uncertainty
estimate. (Finding 5)

**B5.** Clarify the epsilon_uds systematic narrative: zero at Phase 4a
vs 0.499 at Phase 4b arises from different C_b values moving the
operating point. Make this transition explicit. (Finding 8)

### Category C (suggestions)

**C1.** Update covariance matrices to Phase 4b values or explicitly
defer. (Finding 6)

**C2.** Verify A_FB^c input is pole-corrected. (Finding 9)

---

## Overall Classification: B

The analysis demonstrates sound physics judgment, honest treatment of
limitations, and a working extraction infrastructure validated on real
data. The delta_b investigation is the highlight -- it correctly
identifies a genuine methodological problem, quantifies it, explains
the physics, and proposes a concrete fix. The R_b result validates the
double-tag method on data.

The two Category A findings are presentation issues (misleading
sin2(theta_eff) value and incomplete uncertainty characterization) rather
than fundamental physics problems. They can be resolved with text
changes.

**Recommendation:** Proceed to Phase 4c after addressing A1 and A2.
The B findings should be addressed in the Doc 4c iteration. The
delta_b fix is the critical path item for Phase 4c -- if the
multi-purity fit works, this analysis will produce a competitive
A_FB^b measurement. If it does not, the analysis still delivers a
valid R_b measurement with honest (if large) uncertainties.

The analysis is NOT ready for journal submission in its current form
(the A_FB^b is methodologically suppressed and R_b has 373x worse
precision than ALEPH). But it is a solid methods-validation document
that demonstrates the extraction infrastructure works on real data,
and it provides a clear path to a publishable Phase 4c result.
