# Physics Review: AN Doc 4a v5

**Reviewer:** joe_a13d (physics reviewer)
**Document:** ANALYSIS_NOTE_doc4a_v5.pdf (48 pages)
**Date:** 2026-04-02
**Classification:** B

---

## Overall Assessment

This v5 complete rewrite is a substantial, well-organised analysis note
that presents a three-tag hemisphere counting measurement of R_b and a
purity-corrected jet charge extraction of A_FB^b using ALEPH open data.
The document is notable for its honesty: every limitation is catalogued,
every shortfall relative to published ALEPH is quantified, and the
calibration story is told progressively (raw -> smeared -> SF-corrected).
The 10% data validation results are preliminary but physically sensible.

The R_b result of 0.212 +/- 0.001 (stat) +/- 0.015 (syst) is credible.
The three-tag method with SF calibration demonstrably recovers R_b to
within 2% of the SM value, a dramatic improvement over the raw (24% low)
and smeared (8% low) extractions. The operating point stability
(chi2_stab/ndf = 0.38/14) is the strongest evidence that the method works.

The A_FB^b result of 0.074 +/- 0.031 at kappa = 2.0 is consistent with
but imprecise relative to the LEP combined value (0.0992 +/- 0.0016).
The purity-corrected extraction is methodologically sound but operates
in a low-purity regime (f_b ~ 0.18-0.20) that amplifies systematics.

I classify as **B**: the analysis is publishable in principle for R_b
(with reservations about charm systematics), the A_FB^b is a valid
cross-check but not competitive, and several physics issues need
attention before final results. No Category A showstoppers remain in
this v5 rewrite -- the previous reviewers' A-level concerns (operating
point stability, closure tests) have been substantially addressed.

---

## Detailed Physics Evaluation

### 1. Three-tag method with SF calibration for R_b

**The method is sound.** The extension from the standard two-tag
(single/double) system to three categories (tight/loose/anti-b) is a
genuine improvement. The key advantage is the anti-b tag providing a
direct data constraint on epsilon_uds (purity 79.1%), which was
previously unconstrained. The overconstrained system (8 observables,
6 free parameters, 2 dof) enables internal consistency checks.

**The SF calibration is the critical innovation.** The progression
documented in Appendix M is convincing:
- Raw MC efficiencies: R_b = 0.163 (24% low), chi2_stab = 1187/7
- Smeared MC efficiencies: R_b = 0.199 (8% low), chi2_stab = 759/12
- SF-corrected efficiencies: R_b = 0.212 (2% low), chi2_stab = 0.38/14

Each calibration step brings R_b closer to the SM value AND improves
the stability chi2 by orders of magnitude. This is not a tuning artefact
-- the SF method uses data tag fractions to correct the MC template, and
the fact that it simultaneously improves both the central value and
stability is strong evidence that it correctly addresses the data/MC
efficiency mismatch.

**The C_b = 1.0 assumption in the SF extraction deserves scrutiny.**
Section 6.3 explains that the SF method sidesteps the large measured
C_b (1.5-1.54) by absorbing the correlation into the per-category scale
factors. This is equivalent to assuming decorrelated hemispheres after
SF correction. The systematic is evaluated as 2 x |C_b^data - C_b^MC|
= 0.061, giving Delta_R_b = 0.003. This is a reasonable approach given
that per-hemisphere vertex reconstruction is unavailable, but the factor
of 2 inflation is arbitrary. The true C_b after SF correction is not
measured -- it is assumed to be unity. This assumption should be tested
by comparing the double-tag excess (f_d - f_s^2) in data versus the
SF-corrected MC prediction.

**Charm efficiency dominance is the fundamental limitation.** Table 24
(Appendix N) quantifies this precisely: epsilon_c has a 13x ratio of
systematic to statistical contribution. The root cause is
epsilon_c^tight = 0.276 (SF-corrected) versus epsilon_b^tight = 0.371,
giving epsilon_b/epsilon_c = 1.34. The published ALEPH Q tag achieved
epsilon_b/epsilon_c ~ 15. This order-of-magnitude difference in b/c
discrimination propagates directly into the R_b sensitivity. The
three-tag system reduces the epsilon_c uncertainty from ~30% (two-tag)
to ~10%, but 10% of 0.285 is still 0.029, producing Delta_R_b = 0.013.
This is a hard floor set by the available tagging variables.

### 2. Purity-corrected A_FB^b

**The extraction method is standard and correctly implemented.** The
linear fit of <Q_FB> vs cos(theta) with explicit charm subtraction
(Eq. 15) follows the published ALEPH methodology. Using published
delta_b values from Ref. [1] Table 12 is legitimate -- these are
precisely measured quantities from the same detector.

**The choice of kappa = 2.0 at the loosest threshold is well-motivated.**
Table 22 (Appendix L) shows the per-threshold, per-kappa breakdown.
At threshold 2.0, f_b = 0.195 and the denominator f_b * delta_b =
0.195 x 0.579 = 0.113, giving an amplification factor of ~9. At
kappa = 0.3, the denominator is 0.195 x 0.162 = 0.032, amplification
~30. The loosest threshold and highest kappa minimise the purity
correction and give the most stable result. This is the correct
strategy.

**The cross-kappa consistency is marginal.** chi2/ndf = 6.51/3
(p = 0.089) for the four kappa values at fixed threshold. Table 23
shows charm-corrected A_FB^b values ranging from -0.032 (kappa = 0.3)
to +0.005 (kappa = 2.0). The sign flip is driven by the purity
correction: at low kappa, the small delta_b amplifies uncertainties
in f_b and the charm subtraction term. While p = 0.089 is not a
formal failure, it indicates tension that warrants investigation on
full data. A self-calibrating fit (simultaneously extracting A_FB^b
and delta_b) on the full sample, as suggested in Section 13 item 5,
would resolve whether the tension is from delta_b uncertainties or
a genuine non-linearity.

**The intercept term in the linear fit is necessary but concerning.**
Section 8.2 states that fits forced through the origin give
chi2/ndf >> 5 due to a consistent negative offset <Q_FB> ~ -0.003
across all cos(theta) bins. The intercept-inclusive fit (Eq. 20) is
the correct remedy. However, a non-zero intercept in <Q_FB> vs
cos(theta) is physically unexpected -- the charge difference should
vanish at cos(theta) = 0 by symmetry. The offset could arise from:
(a) a detector-level forward-backward asymmetry in track reconstruction
efficiency, (b) a charge-dependent acceptance effect, or (c) a residual
MC/data charge bias. The note attributes it to "bin-level data/MC
shape differences" but does not identify the root cause. This should
be investigated on the full sample.

### 3. Calibration story

**The d_0 smearing calibration (Section 5.2) is well-executed.** The
40-bin calibration in (VDET hits, momentum, cos(theta)) captures the
dominant resolution effects. The mean data/MC ratio of 1.075 (7.5%
worse resolution in data) is physically expected from beam spot effects,
alignment degradation, and the shared-vertex d_0 computation. The
smearing procedure (adding Gaussian noise to MC d_0 values) is the
standard ALEPH technique from Ref. [6]. The residual ratio after
smearing drops to within 1% of unity for all but 3 bins, demonstrating
that the Gaussian model is adequate.

**The tag-rate scale factors are the key innovation.** The SF = f_data /
f_smeared_MC formulation (Eq. 12) absorbs residual efficiency mismatches
that smearing alone cannot capture -- specifically, the mass tag
component of the combined score and any non-Gaussian resolution tails.
The SFs are applied per-category (tight/loose/anti-b) but not per-flavour.
This flavour-independence assumption is the leading limitation
(documented in Known Limitations item 5). The estimated residual bias
of ~0.004 on R_b from flavour-dependent SFs is consistent with the
observed 0.212 vs 0.21578 difference.

**The calibration chain is convincing overall.** The fact that three
independent calibration steps (smearing, SF, three-tag constraint) each
improve R_b monotonically and demonstrably, rather than oscillating or
overshooting, builds confidence that the method is correcting real
effects rather than fitting noise.

### 4. Closure and validation tests

**Independent closure (Section 7.6, Table 8) is the strongest validation.**
Four configurations tested on a 60/40 MC split all recover R_b within
+/- 1 sigma of the SM input. The pulls (0.06 to 0.59) are small. This
demonstrates that the three-tag extraction is unbiased when the
calibration and extraction samples are independent (within the same MC).

**Operating point stability (Section 7.4) is excellent after SF correction.**
chi2_stab/ndf = 0.38/14 across 15 configurations. R_b ranges from 0.211
to 0.213. Compare this to chi2_stab = 389/7 (raw) and 759/12 (smeared).
This is the most convincing evidence in the document.

**The contamination injection test (Section 7.3) shows a factor-of-2
discrepancy** between predicted and observed shifts. The predicted
Delta_R_b = -0.021 versus observed -0.044 (ratio 2.14). The note
attributes this to the first-order approximation breaking down. This is
plausible but the 2x discrepancy means the extraction has non-linear
response to background contamination. For a 2% measurement this is
acceptable; for a sub-percent measurement it would need to be resolved.

**The Q_FB linear fit chi2/ndf (Section 8.4) is 0.3-0.5 per 6 dof on
data.** This is acceptable. The cross-kappa chi2/ndf = 6.51/3 shows
marginal consistency as discussed above.

### 5. Systematic uncertainties

**The R_b systematic budget (Table 7) is dominated by epsilon_c (0.013)
and epsilon_uds (0.006).** Together these account for 85% of the total
systematic (0.015). The next largest source is C_b (0.003). All other
sources are sub-dominant at 0.001 or below. The budget is complete --
all standard LEP R_b systematics (hadronisation, B-physics parameters,
gluon splitting, R_c constraint, sigma_d0) are included with appropriate
references.

**The A_FB^b systematic budget (Table 6) is dominated by the charge model
(kappa spread) at 0.021.** This reflects the fundamental limitation of
operating at low b-purity. The purity uncertainty (0.010) from the
three-tag efficiency constraint is the second largest. The total
systematic (0.024) is 3x the statistical uncertainty (0.008), meaning
this measurement is systematics-limited even on 10% data.

**One concern: the A_FB^b systematic does not include an explicit term
for the linear-model inadequacy.** The chi2/ndf of the Q_FB fit on data
is reported as 0.3-0.5 per 6 dof (Section 8.4), which is good. But the
cross-kappa chi2/ndf = 6.51/3 (p = 0.089) suggests residual model
tension. If a quadratic term were included in the fit, the extracted
slope (and hence A_FB^b) could shift. This should be evaluated as a
systematic.

### 6. Comparison with published results

**R_b:** The result 0.212 +/- 0.015 is consistent with the SM (0.21578),
ALEPH (0.2158 +/- 0.0014), and LEP combined (0.21629 +/- 0.00066).
The total uncertainty is 10.7x the published ALEPH uncertainty, well-
explained by the four precision deficit factors in Section 10.1:
tag quality (epsilon_c/epsilon_b), number of tag categories, MC
statistics/truth labels, and vertex reconstruction. This decomposition
is quantitative and convincing.

**A_FB^b:** The result 0.074 +/- 0.031 is 0.8 sigma below the LEP
combined pole value (0.0992 +/- 0.0016). The 6x precision deficit
relative to ALEPH (0.0052) is primarily from the low b-purity and
reliance on published delta_b values. This is correctly identified.

---

## Specific Findings

### Category A (Must Resolve)

None. The v5 rewrite has addressed the critical issues from previous
review rounds. The operating point stability now passes convincingly,
the closure tests are performed and documented, and the calibration
chain is demonstrated step by step.

### Category B (Should Fix)

**B1. The flavour-independence of SFs is unvalidated on data.**

The SF method applies a single scale factor per tag category (tight,
loose, anti-b), independent of quark flavour. Known Limitation 5
estimates the residual bias at ~0.004 on R_b. However, this estimate
comes from the difference between the measured R_b (0.212) and SM
(0.216), which conflates the SF bias with all other biases. Without
truth labels, the SF flavour-independence cannot be directly tested.

Recommendation: Compare the SF-corrected tag fractions in b-enriched
(tight double-tag) and light-enriched (anti-anti double-tag) subsamples.
If the SFs are flavour-independent, the model should describe both
subsamples equally well. A significant chi2 difference would indicate
flavour-dependent SF residuals.

**B2. The A_FB^b systematic budget should include a fit-model uncertainty.**

The linear model <Q_FB> = a + b cos(theta) is adopted without testing
alternatives. While chi2/ndf ~ 0.3-0.5 per dof on data is good, the
cross-kappa tension (p = 0.089) and the unexplained intercept suggest
the model may be incomplete. A quadratic term (c cos^2(theta)) would
test for charge-dependent acceptance effects.

Recommendation: Fit <Q_FB> = a + b cos(theta) + c cos^2(theta) on
the 10% data. If |c| is significant, include the slope shift
|b_linear - b_quadratic| as a systematic. If |c| is consistent with
zero, document the test as a cross-check.

**B3. The correlation coefficient rho ~ 0.15 between R_b and A_FB^b
(Eq. 23) is stated but not derived.**

The covariance matrix in Eq. (23) quotes rho ~ 0.15 from "shared
epsilon_c systematic." The derivation is not shown. Given that
epsilon_c enters both measurements very differently (multiplicatively
in R_b, through the purity correction in A_FB^b), the correlation
should be derived explicitly from the partial derivatives.

Recommendation: Show the calculation:
rho = (dR_b/deps_c)(dA_FB/deps_c) sigma_eps_c^2 /
(sigma_Rb sigma_AFB). This is a straightforward but important
bookkeeping check.

**B4. The contamination injection ratio (2.14) should be better
understood.**

The factor-of-2 discrepancy between predicted (-0.021) and observed
(-0.044) shifts is attributed to the first-order approximation
breaking down. But the overconstrained three-tag system should have
better-than-linear response (the additional constraints should
stabilise the extraction). A 2x non-linearity suggests either the
prediction formula is wrong (it uses a two-tag approximation for a
three-tag system) or the response is genuinely non-linear.

Recommendation: Derive the expected shift for the three-tag system
explicitly, accounting for the anti-b fraction changing when light
events are injected. If the corrected prediction matches the observed
shift, the discrepancy is methodological, not physical.

**B5. Table 10 shows A_FB^b values at kappa = 0.3 and 0.5 are
significantly negative (-0.032 and -0.031), while kappa = 2.0 gives
+0.005.**

The sign flip from negative at low kappa to positive at high kappa is
physically unexpected. A_FB^b is a property of the physics, not of
the kappa weighting. The charm-corrected values should be kappa-
independent if the method is working correctly. The note attributes
the kappa dependence to the amplification factor in the denominator
(f_b * delta_b), which is correct for the UNCERTAINTY, but should not
affect the CENTRAL VALUE systematically.

The fact that the chi2/ndf = 6.51/3 has p = 0.089 means this tension
is marginally significant. On full data (3x more statistics), the
tension will either resolve or sharpen. If the sign flip persists, it
indicates a systematic bias in the published delta_b values or the
purity correction at low kappa.

Recommendation: Flag this as a validation gate for the full data
analysis. If the cross-kappa chi2 on full data has p < 0.01, the
A_FB^b extraction method needs revision.

### Category C (Suggestions)

**C1.** The abstract quotes A_FB^b = 0.074 +/- 0.031 "(stat+syst)" but
Table 6 gives stat = 0.008, syst = 0.024. The "stat+syst" label should
be replaced with the breakdown, or the quadrature combination should
be stated explicitly. As written, the reader cannot reconstruct the
individual components from the abstract alone.

**C2.** Figure 8 (<Q_FB> vs cos(theta)) would benefit from showing the
expected ALEPH slope (delta_b * A_FB / (1 - delta_QCD)) for comparison,
to give the reader a visual sense of where the measurement falls
relative to the published value.

**C3.** The Reproduction Contract (Appendix X) is excellent. Consider
adding expected output file sizes to help users verify successful
execution.

**C4.** Section 11 (Comparison of Analysis Methodology) is one of the
strongest sections in the document. The systematic comparison of the
five-tag ALEPH system versus the three-tag system used here provides
genuine insight into the precision gap. This section should be
preserved and expanded in the full-data version.

---

## Would I Approve for Publication?

Not at this stage, but the path is clear.

**For R_b:** The three-tag SF-corrected method produces a credible result
(0.212 +/- 0.015) that is consistent with the SM and published values.
The calibration story is convincing. The dominant limitation (epsilon_c ~
epsilon_b) is fundamental to the available tagging variables and is
honestly documented. On full data, the statistical uncertainty will shrink
by ~3x but the systematic floor (0.015) will remain unless b/c
discrimination improves. As a demonstration of self-calibrating
electroweak measurements from archived open data, this is publishable.
As a competitive R_b measurement, it is not (10.7x worse than ALEPH).

**For A_FB^b:** The purity-corrected extraction at kappa = 2.0 gives a
result consistent with the LEP combined value. The 6x precision deficit
is driven by the low b-purity and the use of published delta_b values.
On full data with a self-calibrating fit, the precision could improve to
~3x ALEPH, which would be a useful independent cross-check. The
cross-kappa sign flip (B5) needs to be resolved first.

**For the analysis note itself:** The document is thorough, transparent,
and well-structured. At 48 pages with 29 figures, extensive appendices,
and a clear limitation index, it meets the standard of a complete
internal note. The v5 rewrite has eliminated the workflow artifacts and
patched appendices of earlier versions.

**Verdict:** Proceed to Phase 4c (full data) with the B-level findings
above as action items. The analysis infrastructure is validated. The
results will improve with full statistics but the systematic floor
is understood and honestly documented.

---

## Classification: B

The analysis note demonstrates a working, self-calibrating measurement
framework for R_b and A_FB^b from archived open data. The calibration
chain is convincing, the closure tests pass, and the operating point
stability is excellent. Five Category B findings require attention
(SF flavour-independence validation, A_FB^b fit-model systematic,
covariance derivation, contamination injection understanding,
cross-kappa sign flip). No Category A issues remain in this v5 rewrite.
