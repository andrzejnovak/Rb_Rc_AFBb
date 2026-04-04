# Physics Review: ANALYSIS_NOTE_doc4c_v7

**Reviewer:** viktor_cc74 (physics reviewer)
**Date:** 2026-04-02
**Document:** Doc 4c v7 — Complete rewrite, 30 pages
**Classification:** B

---

## Executive Summary

This is a well-structured, honest analysis note that measures R_b and
A_FB^b from archived ALEPH open data without MC truth flavour labels.
The central values are credible (R_b = 0.2155, A_FB^b = 0.094), the
cross-checks are meaningful, and the limitations are stated without
evasion. The narrative is coherent from start to finish. The document
reads as one piece, not a patchwork.

I would not yet approve this for publication, but the issues are
addressable within the current framework. The classification is **B**:
no showstopper physics errors, but several findings that must be fixed
before I would sign off.

---

## 1. Overall Narrative Assessment

The story is logical and flows well: data description, event selection,
tagging progression (impact parameter to combined tag to BDT),
calibration, extraction, systematics, cross-checks, results, comparison.
The key architectural choice — self-calibrating techniques because truth
labels are absent — is established in the introduction and carried through
consistently. The calibration progression table (Table 5, raw 0.163 to
SF-corrected 0.2155) is the strongest single element of the note: it
demonstrates that the method works and that each correction step is
necessary and quantified.

The 30-page length is at the minimum threshold. The main body is
adequate but the appendices (C through G) are stubs — section headers
with no content. This is addressed as a finding below.

---

## 2. Figure-by-Figure Inspection

**Figure 1 (cutflow bar chart):** Functional. Shows the dominant track
loss from nvdet > 0. Data/MC comparison is qualitative (bar heights).
Adequate for its purpose.

**Figure 2 (data/MC kinematic comparisons — thrust, N_ch, cos_theta,
sphericity):** MC normalized to data integral. Pull panels centered on
zero, within +/-2.5 sigma across the bulk. The thrust distribution shows
a slight shape tension at high thrust (pulls trending positive near 1.0),
but within 2 sigma. Acceptable. The normalization method (data integral)
is documented in the text ("MC is normalized to the data integral").

**Figure 3 (d_0, track p_T, signed significance, combined tag):**
The d_0 distribution shows good data/MC agreement in the core. The
significance distribution (bottom left) shows the expected positive tail
excess from displaced decays. The combined tag (bottom right) shows
reasonable agreement at low values but visible data excess above MC at
high tag scores (above ~10). This is qualitatively expected (data has
more b-enrichment than the uncorrected MC) but is not discussed in the
text. The pull panel shows pulls in the 1-2 sigma range at high tag
values. Not alarming, but worth noting.

**Figure 4 (sigma_d0 scale factors):** Shows the calibration scale
factors ranging 1.3-7.6. The data points are clearly higher than MC
across the board. The large scale factors (up to 7.6) for 1-VDET-hit
low-momentum tracks are concerning — they indicate the MC resolution is
off by nearly an order of magnitude in those bins. The text explains
this as beam spot size and track-in-vertex bias not captured by the
two-parameter model. This is honest but raises the question: are the
calibrated significances actually correct, or is a multiplicative
correction on a wrong functional form still wrong? The systematic for
this (delta R_b = 0.001) may be underestimated. **Finding B1.**

**Figure 5 (sign convention validation):** Shows the positive/negative
tail asymmetry in b-enriched events. Data ratio 3.34, MC 3.62 at 3
sigma. Good validation of the sign convention. The ~8% difference
between data and MC ratios is not discussed — is this absorbed by the
SF calibration? **Finding C1.**

**Figure 6 (hemisphere probability tag and displaced-track mass):**
Good data/MC agreement. The mass distribution shows the expected
enhancement above 1.8 GeV/c^2. Pull panels clean.

**Figure 7 (R_b vs BDT threshold):** The key stability plot. R_b is
flat across all 15+ configurations, clustering around 0.2155. The
error bars are large but the flatness is convincing. The cut-based
result (0.215) and SM value (0.21578) are shown as reference lines.
This is a strong demonstration figure.

**Figure 8 (calibration progression):** Shows R_b and A_FB^b
evolving across MC/10%/full phases. R_b converges to the SM region.
A_FB^b shows the expected pattern. This is a useful narrative figure
but the left panel y-axis is compressed — the MC(4a) point at ~0.17
dominates the scale, making the 10% and full data points hard to
distinguish.

**Figure 9 (Q_FB charge flow distributions):** Good data/MC agreement
at both kappa values. Wider distribution at kappa = 2.0 as expected.
Pull panels clean.

**Figure 10 (mean charge asymmetry vs cos_theta):** This is the
A_FB^b extraction figure. The linear fit looks reasonable, chi2/ndf =
7.1/9 (p = 0.63). The data points have large error bars but the slope
is visibly positive, consistent with a positive asymmetry. However:
the figure title says "ALEPH Open Simulation" and "MC pseudo-data
(kappa = 0.5)" — but kappa = 0.3 is the primary result. Is this the
MC validation or the data extraction? If MC, where is the corresponding
data figure? If data, why does it say "Simulation"? **Finding A1.**

**Figure 11 (systematic breakdown bars):** Clear visualization of the
systematic budget. R_b dominated by charm efficiency, A_FB^b by charge
model. Useful.

**Figure 12 (per-year extraction):** R_b and A_FB^b by year with
combined band. The chi2/ndf values (3.6/3, 3.8/3) indicate good
year-to-year consistency. 1995 A_FB^b is slightly low but within
uncertainties. Convincing.

**Figure 13 (R_b vs working point — cut-based and BDT):** The
cut-based result (left) shows residual working-point dependence; the
BDT (right) is impressively flat. This directly demonstrates the BDT's
advantage. The cut-based plot has chi2/ndf = 0.0/1 which is suspicious
— is this really 0.0? **Finding C2.**

**Figure 14 (A_FB^b vs kappa):** Shows the expected decrease at higher
kappa due to multi-flavour contamination. The combined value band and
chi2/ndf = 0.7/4 are shown. The decrease from kappa = 0.3 (0.094) to
kappa = 2.0 (0.023) is dramatic but the text explains this as a known
effect. The figure demonstrates the contamination pattern convincingly.

**Figure 15 (R_b vs BDT score threshold — appendix):** Similar to
Figure 7 but shows the full BDT scan including low thresholds where
results deviate. The cut-based reference line at 0.1878 is well below
the BDT plateau, reinforcing the BDT's superiority.

**Figure 16 (closure test + stability on MC pseudo-data):** Left panel
shows perfect recovery of R_b^SM across configurations — all within
the shaded band. Right panel shows closure test pulls all within 1
sigma. This is genuine validation (60/40 MC split, not same-sample).
Convincing.

**Figure 17 (efficiency pattern + C_b vs threshold):** Left shows the
three-tag efficiency structure. Right shows C_b increasing with
threshold for both data and MC, with the expected data-MC offset.
The published ALEPH C_b = 1.01 reference line is puzzling — the measured
values are all above 1.1 and reach ~1.5. The text says C_b^MC = 1.392
and C_b^data = 1.365 at the primary WP, which are consistent with this
figure. The published C_b = 1.01 presumably applies to the 5-tag system,
not the 3-tag system used here. This should be clarified. **Finding C3.**

**Figure 18 (SF calibration + f_d vs f_s):** Left shows the scale
factor pattern across categories. Right shows the expected quadratic
relationship between double-tag and single-tag fractions for data and
MC at different R_b values. Clean diagnostic figure.

---

## 3. Narrative Consistency Check

The early data/MC figures (Figures 2-3) show good agreement after
normalization-to-data, with pulls within 2 sigma. The calibration
section (Section 5) identifies and quantifies the resolution mismatch
(mean SF = 1.075) and corrects it. The correction progression (Table 5)
shows the impact quantitatively. The final result is built on the
corrected efficiencies. The journey from raw (R_b = 0.163) to calibrated
(R_b = 0.2155) is fully traced. There is no "broken journey, perfect
destination" problem — the repair is visible and quantified.

The BDT achieving AUC = 1.000 on the test sample is a red flag per the
reviewer protocol. However, the BDT is trained on self-labelled samples
(tight double-tag vs. loose anti-tag), not truth labels. AUC = 1.0 on
these proxy labels does not imply truth leak — it means the BDT perfectly
separates the training proxies, which is plausible given the extreme
purity difference. The closure test (Table 9) with an independent MC
split confirms unbiased extraction. I accept this but note it deserves
a sentence of explanation in the text. **Finding B2.**

---

## 4. Results Credibility

**R_b = 0.2155 +/- 0.0004 (stat) +/- 0.027 (syst):**
- Pull vs ALEPH: -0.01 sigma. Essentially perfect agreement.
- Pull vs LEP combined: -0.03 sigma. Perfect agreement.
- Pull vs SM: -0.01 sigma. Perfect agreement.
- Total uncertainty: 0.027 (12.5% relative). Precision ratio vs ALEPH:
  19x. vs LEP combined: 41x.

The central value is credible. The uncertainty is large but honestly
dominated by the charm efficiency systematic (0.017), which is a genuine
limitation of the 3-tag system without truth labels. The statistical
precision (0.0004) demonstrates the power of the 2.89M event sample;
the systematic limitation is real.

**A_FB^b = 0.094 +/- 0.005 (stat) +/- 0.027 (syst):**
- Pull vs ALEPH: +0.05 sigma. Excellent agreement.
- Pull vs LEP combined (A_FB^0,b): -0.2 sigma.
- Pull vs SM: -0.3 sigma.
- Total uncertainty: 0.028 (30% relative). Precision ratio vs ALEPH: 5.4x.

The central value is credible. The dominant systematic is the charge
separation model (kappa dependence, 0.024), which is a genuine limitation
of using published delta_b values rather than a self-calibrating fit.

**Resolving power:** The total uncertainties (~0.03 on both observables)
are sufficient to confirm the SM predictions and published LEP results
but insufficient to probe the A_FB^b - A_l tension at the few-permille
level. The conclusions section states this honestly. The measurement
demonstrates that electroweak observables can be extracted from open data
with self-calibrating techniques — this is the genuine contribution.

---

## 5. Statistical Methodology

**R_b extraction:** chi2 minimization over 8 tag-fraction observables
with 1 free parameter and 7 dof. The fit chi2/ndf = 377/7 at the primary
BDT working point is explicitly flagged as poor, indicating the linear
SF correction does not fully capture data/MC differences. The text
correctly notes that the extracted R_b is nevertheless stable across
working points (chi2/ndf = 1.1/12 for the stability test). This is an
important nuance — the per-fraction fit is poor but the R_b extraction
is robust because the simultaneous fit averages over the mismodelling.
I accept this interpretation but it should be stated more clearly: the
GoF test fails, and the reason is identified. **Finding B3.**

**A_FB^b extraction:** Linear fit of <Q_FB> vs |cos theta| in 10 bins.
chi2/ndf = 7.1/9 (p = 0.63). Good fit quality. Division by published
delta_b to obtain A_FB^b.

**Uncertainty propagation:** Systematic uncertainties evaluated by
varying each source and re-extracting. Quadrature sum for total. This
is standard practice.

**Covariance matrix:** The chi2 in equation (10) uses diagonal
uncertainties only (sigma_{f_k}^2). For the tag fractions, which are
correlated (they share the same events and the same normalization), a
diagonal chi2 is potentially problematic. This may contribute to the
poor GoF. **Finding B4.**

---

## 6. Systematic Treatment

The systematic budget is comprehensive and well-organized. 14 sources
for R_b, 9 for A_FB^b. The dominant sources are physically motivated:

- **Charm efficiency (delta R_b = 0.017):** The largest systematic, from
  varying epsilon_c by +/-10%. The 10% range is justified by the three-tag
  system's constraint power. The BDT improves epsilon_c/epsilon_b from 0.7
  to 0.172, which should reduce this systematic substantially — yet the
  conservative cut-based value is assigned to the primary result. This is
  a defensible choice (the BDT systematic was not independently evaluated)
  but potentially over-conservative. **Finding C4.**

- **Charge model kappa dependence (delta A_FB^b = 0.024):** Evaluated
  as the difference between kappa = 0.3 and kappa = 0.5. The kappa = 1.0
  and 2.0 values show much larger deviations but are correctly excluded
  due to known multi-flavour contamination. The 0.024 assignment is
  reasonable.

- **Working point dependence (delta A_FB^b = 0.011):** Maximum deviation
  across WP in {3,4,5,6,7}. Reasonable.

- **Hemisphere correlation (delta R_b = 0.007):** Doubled data-MC
  difference following ALEPH convention. Standard approach.

The remaining systematics are sub-dominant and appropriately sized.

**Missing systematic check:** Is there a systematic for the BDT training
sample definition? The b-enriched sample uses combined tag > 10 (tight
double-tag), which depends on the very efficiencies the BDT is meant to
improve. If the training labels are contaminated, the BDT learns a
biased boundary. The closure test (Table 9) mitigates this concern but
uses the same labelling scheme — it is self-consistent by construction
on the labelling. An independent cross-check (e.g., varying the training
threshold) would strengthen the case. **Finding B5.**

---

## 7. Cross-Checks Assessment

**Per-year consistency (Section 8.1):** chi2/ndf = 3.6/3 and 3.8/3.
Good. Demonstrates robustness against year-dependent detector effects
despite single-year MC.

**Operating point stability (Section 8.2):** chi2/ndf = 4.4/14 (p=0.99)
for the cut-based tag with SF correction. This is suspiciously good —
p = 0.99 suggests possible overcounting of uncertainties or correlated
configurations. For the BDT, chi2/ndf = 1.1/12 (p = 1.0). Again very
good. The near-unity chi2/ndf for the BDT is more plausible given the
BDT's design to absorb working-point dependence through the
self-calibrating 3-tag system. The cut-based p = 0.99 deserves a
sentence of discussion. **Finding C5.**

**Independent closure test (Section 8.3):** 60/40 MC split, all pulls
within 1 sigma. Four configurations tested. Genuine independence (different
MC events for calibration and validation). This is the strongest
validation in the note.

**Kappa consistency (Section 8.4):** Demonstrates the expected kappa
dependence pattern. The chi2/ndf = 0.7/4 at the bottom of Figure 14
tests consistency of the combined value, not kappa-independence — which
is correctly not claimed.

**BDT cross-check (Section 8.5):** R_b = 0.2155 +/- 0.0004 from BDT
vs 0.2159 +/- 0.0004 from cut-based at tight=12. Excellent agreement.
This is the independent validation that promotes the BDT to primary.

---

## 8. Input Provenance

Table 21 (Limitation Index) provides a clear accounting of constraints,
limitations, and decisions with their impacts. The key external inputs
are:

- R_c constrained to SM value 0.17223 +/- 0.0030 [3] — justified because
  no lepton/charm tag is available to measure R_c independently.
- delta_b (charge separation) from published ALEPH values [3] — justified
  because self-calibrating delta_b fit requires per-WP flavour fractions
  not available without truth labels.
- QCD correction delta_QCD = 0.0356 +/- 0.0029 [3].
- Various physics parameters from PDG [10].

This is not a meta-analysis disguised as a measurement. R_b is genuinely
measured from data (the three-tag extraction), and A_FB^b is genuinely
measured from the angular distribution. The external inputs constrain
nuisance parameters, not the observables of interest.

---

## 9. Future Directions Assessment

Three items listed:
1. Per-hemisphere primary vertex reconstruction — requires infrastructure
   not available in the open data.
2. Self-calibrating A_FB^b fit — requires truth labels or more
   sophisticated multi-tag calibration.
3. Five-tag system — requires particle ID not in the data.

All three genuinely require capabilities beyond the current dataset.
None is a "should have done" item. This passes the Future Directions
red-flag test.

---

## 10. Commitment Traceability

The abstract commits to measuring R_b and A_FB^b. Both are delivered
with quantitative results and comparisons to published values with pull
calculations. The introduction mentions R_c but the note correctly
downgrades this to a constrained input rather than a measurement. The
prompt requested R_c measurement; the note explains why this is not
feasible (no lepton/charm tag) — this is acceptable if the limitation
is documented, which it is (Known Limitations, Section 14).

---

## Classified Findings

### Category A (must resolve)

**A1. Figure 10 labelling ambiguity.** The primary A_FB^b extraction
figure (Figure 10) is labelled "ALEPH Open Simulation" and "MC
pseudo-data (kappa = 0.5)" — but the primary measurement uses kappa = 0.3
on real data. If this figure shows the MC validation, the corresponding
data extraction figure is missing. If it shows data, the labels are
wrong. Either way, the reader cannot tell what the primary A_FB^b
extraction looks like on data. This is the single most important figure
for A_FB^b and it must unambiguously show the data result.

### Category B (must fix before PASS)

**B1. Sigma_d0 scale factor uncertainty may be underestimated.** Scale
factors up to 7.6 indicate the two-parameter resolution model is
qualitatively wrong for low-momentum 1-VDET tracks. A multiplicative
correction on a misspecified functional form propagates residual shape
differences. The assigned systematic (delta R_b = 0.001 from +/-10%
variation) does not cover the possibility of a wrong functional form.
Consider: what happens if the scale factors are varied by +/-50% for
the bins where SF > 3? Or varied bin-by-bin independently? If the
result is stable, this finding is resolved. If not, the systematic
needs enlarging.

**B2. BDT AUC = 1.000 needs explicit discussion.** The note states
AUC = 1.000 without commenting on whether this is concerning. Add a
sentence explaining that this refers to separation of self-labelled
proxy samples, not truth-labelled flavours, and that the closure test
on an independent MC split confirms unbiased extraction. Without this
explanation, a referee will flag it.

**B3. Fit GoF chi2/ndf = 377/7 needs clearer discussion.** The note
mentions this but buries it: "indicating that the linear SF correction
does not fully capture data/MC differences at the per-mille level."
This deserves its own paragraph. The fit formally fails badly. The
reader needs to understand: (a) why R_b is still trustworthy despite
the poor GoF, (b) that the stability test (chi2/ndf = 1.1/12)
demonstrates the extracted value is insensitive to the fit quality,
and (c) what would improve the GoF (presumably a non-linear SF
correction or floating efficiencies).

**B4. Diagonal chi2 for correlated tag fractions.** Equation (10) sums
over 8 observables with statistical uncertainties in the denominator but
no covariance matrix. The single-tag and double-tag fractions share the
same events (f_s and f_d are computed from the same sample; double-tag
fractions are products of single-tag efficiencies). This introduces
correlations that the diagonal chi2 ignores. This likely contributes to
the pathological GoF. At minimum, state that a diagonal approximation is
used and discuss the expected effect. Ideally, compute the covariance
matrix from Poisson counting statistics and re-fit.

**B5. BDT training sample systematic.** The BDT is trained on
self-labelled data (combined tag > 10 = b-enriched, combined tag < 2 =
light-enriched). The purity of these labels depends on the efficiencies
being measured. If epsilon_c is varied by +/-10% (as in the charm
efficiency systematic), the training sample composition changes. Is the
BDT retrained or is the same BDT applied with varied efficiencies? If
the latter, the training sample definition is an unvaried nuisance.
Document this and either vary it or explain why the impact is negligible.

**B6. Stub appendices.** Appendices C (Per-Systematic Impact Tables),
D (Tag Fraction Comparison), E (Extended Cutflow), F (Auxiliary Plots),
and G (Limitation Index) are listed in the table of contents but have
no content beyond a section header. These stubs inflate the page count
without adding information. Either populate them with the material their
titles promise or remove them from the table of contents. A referee
will view empty appendices dimly. The effective content of the note is
closer to 25 pages than 30, which is thin.

### Category C (suggestions)

**C1.** The sign convention validation (Figure 5) shows data positive/
negative ratio of 3.34 vs MC 3.62 (8% difference). Add a sentence noting
whether this is absorbed by the SF calibration or represents residual
disagreement.

**C2.** Figure 13 left panel shows chi2/ndf = 0.0/1 for the cut-based
result. Is this literally zero? If so, with only 2 points (tight=8 and
tight=12?) and 1 free parameter, 1 dof makes chi2 = 0 possible but
should be stated as such.

**C3.** Figure 17 right panel shows published ALEPH C_b = 1.01 reference
line that appears inconsistent with the measured values (1.1-1.5).
Clarify that the published value applies to the 5-tag system, not the
3-tag system.

**C4.** The charm efficiency systematic uses the cut-based cross-check
value (delta R_b = 0.017) even for the BDT primary result. If the BDT's
own epsilon_c variation gives a smaller systematic, it would be more
accurate (and still conservative) to quote both and use the BDT value
as primary.

**C5.** The operating point stability chi2/ndf = 4.4/14 (p = 0.99) is
very good. Consider whether the uncertainties at different working points
are correlated (they share the same data and largely the same events in
the looser categories). If correlated, the effective ndf is smaller and
the p-value is less extreme.

---

## 11. Length Assessment

At 30 pages, the document is at the stated minimum threshold of the
analysis note format specification (30-100 pages target, under 30 is
Category A). The main body (Sections 1-14, pages 5-25) is 20 pages of
substantive content. The appendices add 5 pages but appendices C-G are
stubs. The effective content is approximately 25 pages.

For the scope of this analysis (two observables, one tagging method with
BDT extension, one extraction framework), 25 pages of content is
sufficient to tell the story. The note does not feel padded or
incomplete in its main body. However, the stub appendices create an
impression of incompleteness. Populating or removing them (Finding B6)
would resolve this concern.

---

## 12. Verdict

**Classification: B**

The physics is sound. The central values are credible and the analysis
demonstrates a genuine measurement capability from open data. The
narrative is coherent and the limitations are honestly stated. The
dominant issues are:

1. One Category A finding (Figure 10 labelling — is this data or MC?)
   that must be resolved to establish what the A_FB^b extraction
   actually looks like on data.

2. Five Category B findings that individually are fixable but
   collectively indicate the note needs one more revision pass: the fit
   GoF discussion, diagonal chi2 acknowledgment, BDT AUC explanation,
   sigma_d0 systematic investigation, and stub appendices.

After addressing A1 and B1-B6, I would expect to classify this as a
conditional A (approvable with minor revisions). The measurement itself
is correct — the issues are primarily about the presentation and
completeness of the documentation, not the physics.
