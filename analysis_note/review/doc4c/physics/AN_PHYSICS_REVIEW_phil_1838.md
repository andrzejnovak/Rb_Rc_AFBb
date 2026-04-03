# Physics Review: ANALYSIS_NOTE_doc4c_v2.pdf

**Reviewer:** phil_1838 (Physics Reviewer)
**Document:** Doc 4c v2 -- SF-calibrated corrected full-data results
**Date:** 2026-04-02

---

## Overall Assessment

**Classification: B -- conditionally publishable. Requires resolution of
the items marked (A) and (B) below before I would sign off.**

This is a genuinely impressive piece of work. The analysis extracts R_b
and A_FB^b from 2.89M archived ALEPH open-data events without MC truth
labels, using a fully self-calibrating methodology built from scratch.
The three-tag hemisphere counting method with data-driven tag-rate scale
factor calibration is clever, well-motivated, and -- critically --
demonstrated to work through the independent closure test (section 7.6)
and the BDT cross-check (section 7.8). The R_b result at
0.21236 +/- 0.00010 (stat) +/- 0.027 (syst) is consistent with the SM and
with the published ALEPH value. The stability scan across 15 working
points with chi2/ndf = 4.4/14 (p = 0.99) is the single most convincing
piece of evidence that the method is sound.

However, several issues prevent me from approving for publication as-is.

---

## Findings

### F1. (A) Per-year R_b values systematically below the SM -- unexplained

Table 15 shows per-year R_b (SF-calibrated, tight=8, loose=4):

| Year | R_b    |
|------|--------|
| 1992 | 0.1885 |
| 1993 | 0.1876 |
| 1994 | 0.1880 |
| 1995 | 0.1864 |

All four values are approximately 0.188, which is 12% below
R_b^SM = 0.21578. Yet the combined result across 15 working-point
configurations is 0.21236. The per-year consistency chi2/ndf = 3.57/3
(p = 0.31) passes -- but only because the per-year values are
mutually consistent *with each other*, not with the SM.

**The critical question:** how does the combined multi-configuration
result (0.212) emerge from per-year values that are all near 0.188?
The answer must be that the combination across working-point
configurations at tight=8/loose=4 gives R_b ~ 0.188 at that single
configuration, while the combined result uses 15 configurations with
the full SF method at C_b = 1.0. But this is deeply confusing in the
presentation. Table 13 shows that at tight=8/loose=4 on full data,
R_b(SF) = 0.2123, yet Table 15 shows 0.188 for the same configuration
split by year. This is an apparent contradiction unless Table 15 uses
a different calibration method (perhaps the per-year SF calibration
differs from the all-years SF calibration). The AN must explain this
discrepancy explicitly. If the per-year extraction uses only that
year's data for SF calibration while the combined extraction uses the
full dataset, the per-year values will be noisier and potentially
biased by the smaller MC overlap -- but then the per-year "consistency
test" is testing something different from what the reader expects.

**Action required:** Clarify what calibration method is used for per-year
R_b in Table 15. If the per-year values at 0.188 are from a specific
single configuration without the full SF combination, state this
explicitly. If they are truly SF-calibrated and the combined result is
0.212, explain how the combination lifts the value by 13%.

### F2. (A) Per-year A_FB^b values are all negative

Table 15 shows A_FB^b = {-0.018, -0.033, -0.061, -0.084} for years
1992-1995. These are all negative, while A_FB^b should be positive
(the SM predicts A_FB^{0,b} = 0.1032). The chi2/ndf = 3.82/3 (p = 0.28)
passes for mutual consistency, but the combined full-data result is
A_FB^b = +0.0025 (combined) or +0.014 (at kappa=2.0). The per-year
values are all negative and their magnitudes increase with year --
this is a suspicious systematic trend, not a random fluctuation.

The AN states the purity-corrected method at kappa=2.0 is the primary
method. But Table 15 does not specify what kappa or working point is
used for the per-year extraction. If these per-year values are at a
tight working point where the charm correction dominates and flips
the sign (as documented in Table 14 and section 9.3.2), this needs to
be stated. A consistency test where all four values have the wrong sign
is not a reassuring test, even if they are mutually consistent.

**Action required:** State the extraction parameters (kappa, working
point) for the per-year A_FB^b values. Explain why all four are
negative when the combined result is positive.

### F3. (A) Experiment label "ATLAS" appears on several figures

Figures 5, 7, 10, 16, 28 display "ATLAS" in the experiment label
position. This is an ALEPH analysis. The mplhep experiment label is
clearly misconfigured. This is not cosmetic -- it misattributes data
to a different experiment and would be immediately rejected by any
journal referee.

**Action required:** Fix all experiment labels to read "ALEPH Open Data"
(as correctly appears on other figures).

### F4. (A) Covariance matrix inconsistency in R_b total uncertainty

The abstract and eq. (25) state R_b = 0.21236 +/- 0.00010 (stat)
+/- 0.027 (syst). The total uncertainty is therefore
sqrt(0.00010^2 + 0.027^2) = 0.027. But Table 16 gives the total
systematic as 0.027 with total (stat + syst) also 0.027, because the
statistical uncertainty is negligible. Meanwhile, the covariance matrix
in Appendix J (eq. 30) gives V_{11} = (0.015)^2, i.e., total R_b
uncertainty of 0.015. The body text (Table 16) says total systematic =
0.027. These are inconsistent: 0.015 vs 0.027.

Looking more carefully, Table 7 (10% data) gives total systematic =
0.015 while Table 16 (full data) gives total systematic = 0.027. The
covariance matrix appears to use the 10% systematic values, not the
full-data values. If the covariance matrix is from the full-data
result, it should use the full-data systematics. If the systematic
budget changed between 10% and full data (which it did: the dominant
eps_c systematic grew from 0.013 to 0.017), the covariance matrix
must be updated.

**Action required:** Reconcile the covariance matrix with the full-data
systematic budget. The total R_b uncertainty in eq. (30) should be
consistent with Table 16.

### F5. (B) The A_FB^b combined result (+0.0025) has limited physics content

The combined A_FB^b = +0.0025 +/- 0.0026 (stat) +/- 0.0021 (syst)
is 2.7 sigma below the LEP combined A_FB^{0,b} = 0.0992 and 3+ sigma
below the SM prediction of 0.1032. The AN correctly identifies this
as a dilution effect from the absence of charm subtraction and the
low b-purity (f_b ~ 0.18). But a "combined" result that is known to
be systematically biased by a factor of ~40x (0.0025 vs 0.0992) is
not a measurement -- it is a demonstration that the method does not
fully isolate the b-quark asymmetry.

The per-kappa result at kappa=2.0, A_FB^b = +0.014 +/- 0.005 (stat),
is more physically meaningful, showing the correct sign and a value
closer to the expectation (though still diluted). The AN should be
clearer about which is the primary result. The abstract quotes both,
which is good, but the kappa=2.0 result should be elevated as the
primary A_FB^b measurement, with the combined value presented as a
consistency check.

The derived sin2(theta_eff) = 0.2495 +/- 0.0005 (stat) from the
combined A_FB^b is far from the world average (0.23153) because the
diluted A_FB^b propagates into an unreliable extraction. The AN
acknowledges this but still quotes the number. I would remove this
derived quantity entirely -- it adds no physics value and could
mislead readers.

**Action required:** (1) Elevate kappa=2.0 as the primary A_FB^b
result. (2) Remove or strongly caveat the sin2(theta_eff) extraction
from the combined A_FB^b.

### F6. (B) Systematic budget grew from 10% to full data without explanation

The R_b total systematic grew from 0.015 (10% data, Table 7) to
0.027 (full data, Table 16). The dominant source eps_c grew from
0.013 to 0.017. The eps_uds systematic grew from 0.006 to 0.008.
The C_b systematic grew from 0.003 to 0.007. These are all increases
of 30-130%.

The AN provides no explanation for why systematics grew on the full
dataset. In a well-behaved analysis, systematics should be similar or
slightly improve with more data (better calibration statistics). The
increases suggest that either (a) the systematic evaluation method
differs between 10% and full data, (b) the data/MC mismatch is
larger on the full dataset, or (c) the 10% estimates were
underestimates. Any of these deserves a sentence of explanation.

**Action required:** Add a brief discussion of why the full-data
systematics are ~2x larger than the 10% data systematics.

### F7. (B) Goodness-of-fit at individual working points is poor

Section 8.4 states that individual per-WP chi2/ndf ranges from 17/7
to 28/7 (p = 0.001-0.016). These are objectively bad fits. The AN
argues that the stability chi2 (0.38/14) is the relevant metric,
and that the per-WP chi2 reflects model tension orthogonal to R_b.
This argument has merit -- the overconstrained system (8 observables,
6 parameters) can have residuals that don't affect R_b -- but it
needs more quantitative support.

Specifically: which observables drive the chi2? If the tension is
between the single-tag and double-tag constraints on the same
efficiency, this is understandable. If the tension involves the
R_b-sensitive observables (f_tt, f_ta), this is a physics problem.
The AN should decompose the per-WP chi2 into contributions from each
observable, or at least identify the 1-2 observables that dominate
the residual.

**Action required:** Add a brief decomposition of the per-WP chi2 to
demonstrate that the tension is orthogonal to R_b.

### F8. (B) Contamination injection test shows 2x over-response

Section 7.3 shows that injecting 5% light-enriched events produces a
shift of -0.044, while the first-order prediction is -0.021 -- a
factor of 2.14 discrepancy. The AN explains this as the non-linear
response of the double-tag formula with uncalibrated efficiencies.
This is plausible, but the test is performed pre-calibration. After
SF calibration, the non-linearity should be reduced (since the
efficiencies are corrected). Was the contamination injection repeated
after SF calibration? If so, what is the observed/predicted ratio?
If the response linearity improves post-calibration, this
strengthens the case. If it does not, there is a residual non-linearity
in the extraction that should be assessed.

**Action required:** Either repeat the contamination injection post-SF
or explicitly state that this test was only performed pre-calibration
and explain why it is still informative.

### F9. (B) R_c not measured -- commitment partially dropped

The physics prompt asks for R_b, R_c, and A_FB^b. The analysis
constrains R_c to the SM value (0.17223 +/- 0.0030) from the LEP
combination. There is no attempt to extract R_c from data, despite
the three-tag system having some sensitivity to it through the charm
efficiency. The Known Limitations section does not list R_c as
unfeasible -- instead, Future Directions item 4 ("Simultaneous
R_b-R_c extraction") describes it as something that "would provide an
internal consistency check." This implies R_c extraction is feasible
but was deferred.

I accept that the limited b/c discrimination makes a competitive R_c
measurement unlikely, but the AN should either (a) present even a
crude R_c extraction as a cross-check, or (b) explicitly state in the
introduction and conclusions that R_c is constrained externally and
not measured, with a quantitative argument for why the data cannot
constrain it.

**Action required:** Add explicit statement that R_c is not measured,
with justification (e.g., the chi2 profile shows no constraint, or
floating R_c produces sigma(R_c) > 0.05).

### F10. (C) Closure test (section 7.6) uses same MC for derivation and testing

The independent closure test calibrates on 60% of MC and extracts on
40%. Since there is only one MC sample (1994 configuration), both
subsets share the same generator settings, fragmentation model, and
detector simulation. This means the closure test validates the
algebraic framework and the statistical procedure, but does NOT
validate the physics modelling assumptions. The AN should acknowledge
this limitation more explicitly. The word "independent" in "independent
closure test" is doing heavy lifting -- it is independent in the
statistical sense (disjoint events) but not in the physics sense
(same model).

### F11. (C) Figure quality issues

Several multi-panel figures (Figs. 5, 7, 10, 16) have overlapping
text and cramped axis labels. Fig. 5 labels are partially cut off.
The pull panels in Figs. 17-20 use an unconventional (N_data - N_MC)/sigma
label format for what are standard pulls. These are minor but would
be flagged by a journal's production office.

### F12. (C) Missing R_c measurement in abstract

The abstract mentions R_b and A_FB^b but not R_c, despite R_c being
in the title-level scope (the prompt requested it). Since R_c is
constrained externally, the abstract should state this explicitly
rather than leaving the reader to discover it in section 5.1.

### F13. (C) "Powered by Claude Code" in author line

The byline "JFC Autonomous Analysis Framework / Powered by Claude Code"
is unusual. For a journal submission, this would need to follow the
journal's authorship policy. Not a physics issue, but flagging it.

---

## Figure Inspection

### Data/MC comparison figures (Figs. 4, 17-20, 29-35)

The data/MC agreement is generally good across all kinematic variables.
The combined tag score (Fig. 4) shows excellent agreement with pulls
within +/-2 sigma across the full range. The signed d0/sigma
distribution (Fig. 17) shows good core agreement with moderate tension
in the positive tail -- this is the expected pattern given the ~7.5%
data/MC resolution mismatch, and is precisely what the d0 smearing
calibration is designed to correct.

The thrust, cos(theta), multiplicity, and pT distributions (Figs.
18-19) all show good data/MC agreement with no systematic offsets.
The hemisphere charge distributions (Figs. 20, 30-31) are
well-modelled by MC.

### Calibration progression (Figs. 7, 23-24)

The calibration progression from raw MC (R_b ~ 0.163) to smeared
(R_b ~ 0.199) to SF-corrected (R_b ~ 0.212) is clearly demonstrated
in Fig. 7. This is one of the strongest figures in the AN -- it shows
the calibration actually working, step by step. Fig. 23 shows the
flatness of the SF-corrected R_b across 15 working points, which is
visually convincing.

### Closure test (Fig. 21)

The left panel shows pulls within +/-1 sigma for all four
configurations, with the SM input value recovered. The right panel
(corrupted corrections) shows large pulls as expected. This is a
well-designed figure that demonstrates the method works on MC.

### Systematic breakdown (Figs. 10, 27)

Clear and informative. The dominance of eps_c and eps_uds is
immediately visible. The A_FB^b systematic (charge model, purity
uncertainty) is also clearly displayed.

---

## Narrative Consistency Check

The figure narrative is broadly consistent. Early figures show
the data/MC resolution mismatch (d0 smearing calibration, Fig. 2),
which motivates the SF correction. The SF correction is shown to
work (Fig. 7), and the final result (Fig. 23) is flat across
working points. The journey from "broken" (R_b = 0.163 with raw MC)
to "fixed" (R_b = 0.212 with SF) is well-demonstrated with
intermediate steps visible.

The one narrative break is the per-year values (Finding F1): the
per-year R_b values near 0.188 do not obviously connect to the
combined value of 0.212. This is the most concerning gap in the
narrative.

---

## Input Provenance

Table 5 provides a clear provenance table for external inputs.
The colour coding (blue = measured, red = external) is helpful.
The analysis is not a meta-analysis: it genuinely measures R_b
from data tag fractions, with the dominant measurement being the
per-category tag rates and their SF calibration. The external inputs
(R_c, delta_b, A_FB^c, B lifetimes, gluon splitting rates) are
appropriate and well-documented.

---

## Statistical Methodology

- The chi2 minimisation with toy-based uncertainty propagation
  (1000 toys, KS-verified Gaussianity) is sound.
- The stability chi2 = 0.38/14 is the appropriate metric for the
  overconstrained system. This is not suspiciously good -- with
  correlated working points, the effective number of independent
  configurations is smaller than 14.
- The linear fit for A_FB^b with a free intercept is appropriate
  given the observed offset.
- The covariance matrix is provided (Appendix J), though see F4
  for the inconsistency.

---

## Commitment Traceability

The prompt requested R_b, R_c, and A_FB^b.
- R_b: Measured. Delivered.
- R_c: Not measured, constrained to SM. See F9.
- A_FB^b: Measured, but diluted. Delivered with appropriate caveats.

---

## Future Directions Red Flag Check

The Future Directions section lists 6 items. Items 1-3 (vertex
reconstruction, secondary vertices, neural network tagging) require
infrastructure not available in the current data format -- these are
legitimately deferred. Item 4 (simultaneous R_b-R_c) is feasible
with the current framework (see F9). Item 5 (self-calibrating
A_FB^b) requires more statistics than the 10% subsample provides,
but could potentially be attempted on the full dataset -- however,
the AN notes this was completed on the full dataset (the full-data
result uses the purity-corrected method). Item 6 (per-year
extraction) is marked as completed.

Item 4 is the only clearly feasible-but-not-done item. This is
flagged as F9 above.

---

## Suspiciously Good Agreement Check

The stability chi2/ndf = 0.38/14 is low (p = 0.99). This is not
necessarily suspicious because: (1) the 15 working-point
configurations share the same data and are highly correlated, so
the effective ndf is much smaller than 14; (2) the SF calibration
is designed to produce stability. The per-WP chi2 values (17-28/7)
show the expected level of tension, confirming that uncertainties
are not globally inflated. The closure test pulls (+0.06 to +0.59)
are also reasonable. No red flags from suspiciously good agreement.

---

## Summary Verdict

**Classification: B**

The physics is sound. The self-calibrating methodology is clever and
well-validated. R_b is correctly recovered at the SM value with honest
uncertainties. The A_FB^b result has the correct sign and is limited
by the known b-purity constraint. The analysis demonstrates that
meaningful heavy-flavour EW measurements can be extracted from
archived open data without truth labels.

The two Category A findings (F1: per-year R_b contradiction; F3: ATLAS
labels) and F4 (covariance inconsistency) must be resolved. The
Category B findings (F5-F9) should be addressed to strengthen the
document. Once these are fixed, I would classify this as publication-ready.

This is not yet an A (approve unconditionally) because the per-year
R_b values at 0.188 vs combined at 0.212 are unexplained and could
indicate a problem with the full-data calibration. Once this is
clarified, the document could be approved.

---

## Finding Summary Table

| ID  | Cat | Summary |
|-----|-----|---------|
| F1  | A   | Per-year R_b ~ 0.188 vs combined 0.212 -- unexplained 13% discrepancy |
| F2  | A   | Per-year A_FB^b all negative; extraction parameters not stated |
| F3  | A   | "ATLAS" experiment label on 5+ figures |
| F4  | A   | Covariance matrix (0.015) inconsistent with full-data systematic (0.027) |
| F5  | B   | Combined A_FB^b = +0.0025 has limited physics content; elevate kappa=2.0 |
| F6  | B   | Systematics doubled from 10% to full data without explanation |
| F7  | B   | Per-WP chi2 = 17-28/7 needs decomposition |
| F8  | B   | Contamination injection not repeated post-SF calibration |
| F9  | B   | R_c not measured or quantitatively shown to be unconstrained |
| F10 | C   | Closure test "independent" is statistical, not physics-model independent |
| F11 | C   | Minor figure quality issues (overlap, label formats) |
| F12 | C   | Abstract silent on R_c |
| F13 | C   | Byline format unusual for journal submission |
