# Constructive Review — Phase 2 Strategy (Iteration 2)
# R_b, R_c, A_FB^b Analysis

**Reviewer session:** lena_389c
**Date:** 2026-04-02
**Artifact:** `phase2_strategy/outputs/STRATEGY.md` (post-fix by felix_d976)
**Iteration:** 2 (fresh full-artifact evaluation after fixer pass)
**MCP_LEP_CORPUS:** true — corpus queries performed; see §RAG Evidence
**REVIEW_CONCERNS.md:** Four cross-phase concerns carried forward (CP1–CP4);
all four evaluated against the updated artifact.

---

## HONEST FRAMING CHECK

Before proceeding: is this strategy telling the truth about what it can
measure and how well?

The fundamental premise — extracting R_b from ~3M ALEPH hadronic events
using the double-tag method without MC truth — is sound and well-precedented
(hep-ex/9609005, inspire_433306). The strategy's constraints [A1]–[A6] are
documented honestly. The precision estimates are conservative and correctly
reference the published ALEPH values. The mitigation strategies for [A1] (no
MC truth) are technically coherent. The analysis is not hiding a structural
problem behind large uncertainties; the documented limitations are genuine
and the workarounds are standard LEP practice.

The fixer pass resolved all 7 Category A and 13 Category B findings from
iteration 1. The document is materially improved. This review finds ONE
residual Category A concern (a logical inconsistency in the A_FB^b governing
extraction that survived the fix pass) and several Category B/C items that
strengthen the analysis's resilience to Phase 3/4 scrutiny.

---

## Classification: **(B)**

One Category A finding plus four Category B findings prevent a PASS. The
Category A finding is specific and fixable without restructuring the strategy.
After resolution, the strategy is of publication quality.

---

## Prior Review Concerns (REVIEW_CONCERNS.md)

### CP1 — Closure test tautology [previously Category A]

**Status: RESOLVED.** Section 9.1 now commits to three operationally
independent closure tests: (a) negative-d0 pseudo-data test (return of
R_b ~ 0 by construction), (b) bFlag consistency check, (c) artificial
contamination injection with a known predicted shift. The MC-split tautology
has been removed. The new tests are genuinely diagnostic. No further action
required here.

### CP2 — A_FB^b extraction formula [previously Category A]

**Status: PARTIALLY RESOLVED — see Category A finding [A1] below.**

The simplified formula (Section 4.2 bold text) is now correctly labelled
"approximation, valid only for 100% pure b sample." The self-calibrating fit
is designated the governing extraction in [D12]. However, a residual logical
inconsistency remains between the fit formulation in Section 4.2 and the fit
formulation in Section 6.3 that the fixer did not address. This becomes the
sole Category A finding.

### CP3 — sigma_d0 angular form [previously Category A]

**Status: RESOLVED.** Section 5.1 and Section 9.3 now use sin(theta)
(not sin^{3/2}(theta)) for the Rphi d0 parameterization. Decision [D7]
correctly specifies calibration from the negative d0 tail in bins of
(nvdet, momentum, cos(theta)) with 40 calibration bins specified. The
systematic variation between sin(theta) and sin^{3/2}(theta) is committed
in Section 7.1. The angular form is now self-consistent with the d0 branch
being Rphi-projected.

### CP4 — PDG inputs not yet fetched [previously Category A]

**Status: RESOLVED.** M_Z = 91.1880 +/- 0.0020 GeV, Gamma_Z = 2.4955 +/-
0.0023 GeV, B+ = 1.638 ps, B0 = 1.517 ps, Bs0 = 1.516 ps, Lambda_b = 1.468
ps, and B meson charged decay multiplicity = 5.36 are now listed with PDG 2024
citations in INPUT_INVENTORY.md. All B-physics systematic variations now have
citable input values.

---

## Findings

---

### [A1] A_FB^b self-calibrating fit: governing formulation conflict — Category A

**Section:** 4.2, 6.3

**Issue:** The fixer correctly designated the self-calibrating fit as the
governing extraction in [D12] and in Section 4.2. However, the two sections
describe the governing extraction using different mathematical frameworks that
are not equivalent, and neither matches the five-category chi2 fit used in the
reference paper.

Section 4.2 (governing extraction paragraph) states:

> "<Q_FB>(cos theta) = sum_q f_q * delta_q * A_FB^q * cos(theta)"

This is the mean-charge formulation — a linear regression of the charge
asymmetry in cos(theta), extracting the product delta_b * A_FB^b from the
slope. This approach requires knowing the flavour fractions f_q and charge
separations delta_q.

Section 6.3 (extraction method) describes fitting A_FB^b and delta_b
simultaneously "using multiple b-tag purities (working points) and multiple
kappa values." This is a profile fit structure: at each purity, the fraction
f_b changes, and the joint constraint from multiple purities pins down the
combination.

Neither of these is the five-event-category chi2 fit from inspire_433746
Section 4, which explicitly constructs five quantities:
N (single-tagged forward), N-bar (single-tagged backward), N^D (double-tagged
unlike-sign), N^D-bar (double-tagged unlike-sign, other orientation), and
N^same (double-tagged like-sign), and fits A_FB^b and the charge separation
probability w_b simultaneously. This five-category structure is also confirmed
by both DELPHI references (inspire_1661115 and inspire_1661252):

> "Technically the b quark forward-backward asymmetry A_FB^b is extracted
> from a chi2-fit to the five independent event categories N, N-bar, N^D,
> N^D-bar and N^same in bins of polar angle."
> (inspire_1661252, Section: "The fit of the b quark forward-backward asymmetry")

The mean-charge formulation in Section 4.2 and the working-point profile fit
in Section 6.3 are approximations to this exact structure. The strategy does
not state which of these three approaches is the actual governing extraction,
and they would produce different numerical results with different
statistical properties.

**Why Category A:** This ambiguity will cause Phase 3/4 to implement
whichever version the executor reads first, without a clear specification.
If the mean-charge fit is implemented instead of the five-category chi2 fit,
the statistical correlations between the charge separation calibration and the
asymmetry extraction are not accounted for, inflating the statistical
uncertainty and potentially biasing the result (as documented explicitly in
inspire_1661115, which notes these correlations change the result meaningfully).

**Required resolution:**

1. Designate one of the three formulations as the governing extraction with
   an explicit [D] label. The five-category chi2 fit (inspire_433746 Section 4;
   inspire_1661115 Section 6) is strongly recommended because it is the most
   complete statistical treatment and is implemented in both reference analyses.

2. Update Section 6.3 to describe this fit precisely: the five event-rate
   observables as functions of A_FB^b, the single charge-assignment probability
   w_b (the probability that the hemisphere charge correctly identifies the b
   quark), and two overall normalisation factors per polar-angle bin. State
   the number of degrees of freedom (the DELPHI analysis gets 15 for 1992-93
   and 17 for 1994-2000 per working-point interval).

3. If the mean-charge formulation is retained as the governing extraction
   (simpler to implement), add a concrete justification: under what conditions
   (purity, statistics) does it converge to the five-category result, and
   what is the expected precision penalty?

---

### [B1] [D17] primary vertex investigation deferred — consequence for C_b not committed — Category B

**Section:** 5.1, 7.1

**Issue:** Decision [D17] correctly flags that the stored d0 branch's reference
vertex must be investigated at Phase 3. The strategy documents three possible
scenarios (global event-level vertex, beam-spot only, per-hemisphere vertex)
and the corresponding consequences for sigma_d0 and C_b. This is good.

However, the strategy does not commit to a concrete protocol for what happens
at each scenario. Specifically: if d0 is found to be relative to a global
event-level vertex that includes the track (the "track-in-vertex" problem),
the strategy does not specify whether the analysis will (a) recompute d0
excluding the track from the vertex fit, (b) apply a correction factor derived
from the bias magnitude, or (c) assign an inflated systematic covering the
range. Option (a) is the correct approach but requires implementing a primary
vertex refit in Phase 3, which is a substantial code commitment. Option (c)
is a fallback.

The ALEPH reference analysis (hep-ex/9609005) solved this by using
per-hemisphere primary vertex reconstruction from the start. The DELPHI
reference (inspire_1660341, Section 4.2.1) uses a beam-spot-constrained
iterative per-hemisphere vertex fit. The corpus confirms that per-hemisphere
vertex reconstruction is standard practice specifically because the global
vertex is biased by displaced tracks.

**The consequence for C_b:** If the analysis uses a global primary vertex,
the hemisphere correlation C_b is inflated by the shared vertex — two
hemispheres that both contain displaced tracks both pull the shared primary
vertex in the same direction, creating a spurious correlation. This is the
mechanism the per-hemisphere vertex was designed to break.

**Required resolution (Category B):** Add the following to [D17] and
COMMITMENTS.md:

  - If d0 is relative to a global event vertex: commit to option (a)
    (per-hemisphere vertex refit) as the default, with option (c)
    (inflated systematic) as fallback if Phase 3 proves the refit
    computationally infeasible within the pixi environment.
  - Add a concrete C_b investigation: if the per-hemisphere vertex
    scenario is triggered, re-derive C_b at the operating point and
    compare to the global-vertex C_b. The difference is the scale of
    the systematic.

This prevents Phase 3 from finding the track-in-vertex problem and making
an ad-hoc decision that is not auditable against the strategy.

---

### [B2] Precision estimate for A_FB^b uses an inconsistent formula — Category B

**Section:** 8.3

**Issue:** The statistical precision estimate for A_FB^b in Section 8.3
derives sigma ~ 1 / (delta_b * sqrt(N_tagged)), using delta_b ~ 0.23 for
kappa = 0.5 from inspire_433746. The derivation produces sigma ~ 0.0075 from
simple counting, then states the self-calibrating fit improves this to
~0.005-0.007 by "using information from the full angular distribution and
multiple working points/kappa values."

The improvement factor (0.0075 -> 0.005) corresponds to sqrt(0.0075/0.005)^2
= 2.25x improvement in effective statistics. This is plausible but unverified.
The ALEPH reference achieved 0.0039 (stat) with 4.1M events. Scaling to our
2.87M events: sigma ~ 0.0039 * sqrt(4.1/2.87) ~ 0.0047. This is better than
the strategy's conservative estimate (0.005-0.007) but consistent with the
lower end.

The problem: the scaling formula used ("sigma ~ 0.0039 * sqrt(4.1/2.87) *
sqrt(5/4) ~ 0.0052") includes a sqrt(5/4) penalty for having 4 kappa values
instead of 5. This is not how precision scales. The improvement from multiple
kappa values comes from combining their information — which increases effective
delta_b, not N_tagged. If the kappa values have correlated charge information
(they share track charges, differing only in momentum weighting), the
information gain from adding a 5th kappa is much smaller than sqrt(5/4) ~ 1.12.

**Why Category B:** The precision estimate, while conservative, uses an
incorrect scaling for kappa values. When Phase 4a reviews this against
the actual fit result, a precision significantly different from 0.005-0.007
could trigger unnecessary concern. The estimate should use the correct scaling.

**Required resolution (Category B):**

Remove the sqrt(5/4) penalty factor and replace with: "The improvement from
using multiple kappa values is sub-linear because the kappa values share the
same track charges. The dominant improvement comes from the self-calibrating
fit structure itself (knowing delta_b at each purity removes the need to assume
it). The expected precision at our statistics is ~0.0047 (from direct scaling
of the ALEPH result), with the range 0.004-0.006 covering MC modelling
uncertainty in delta_b." Update Section 8.3 accordingly.

---

### [B3] BDT label contamination diagnostic — action on positive result is unspecified — Category B

**Section:** 5.2 [D10]

**Issue:** Decision [D10] includes the label contamination diagnostic: scan
the BDT working point vs extracted R_b; a slope > 1-sigma/range while the
cut-based scan is flat indicates bFlag label contamination. The diagnostic is
well-defined. But the strategy does not specify what happens when the diagnostic
fires.

The strategy says "document slope magnitude and significance. If slope is
detected, revert to cut-based as primary." This is correct but incomplete:

1. What constitutes "detected"? A 1-sigma slope? 2-sigma? The diagnostic
   threshold should be specified.

2. "Revert to cut-based as primary" means the BDT becomes only a cross-check.
   But the cross-check role requires the BDT to still function — and if bFlag
   labels are contaminated, the BDT trained on contaminated labels may still
   provide information relative to the cut-based tagger. The strategy should
   specify whether the BDT cross-check is retained (with the contamination
   documented as a systematic) or dropped entirely.

3. There is a missed opportunity to exploit the contamination diagnostic
   positively: if the slope magnitude can be measured precisely, it constrains
   the contamination fraction of bFlag=4. This is itself useful physics
   information that should feed into the bFlag interpretation (Section 9.6).

**Required resolution (Category B):** Add to [D10]:
  - Threshold for "detected": slope significance > 2 sigma in the working
    point range covering 2x the nominal cut.
  - If detected: drop BDT from physics use; retain as a systematic cross-check
    only. Document the estimated contamination fraction.
  - Note that the contamination fraction (from the slope magnitude) feeds back
    into the bFlag interpretation in Section 9.6.

---

### [B4] The flaghip figure F4 (f_d vs f_s scatter) needs a chi2 iso-curve — Category B

**Section:** 12, Figure F4

**Issue:** F4 is described as "f_d vs f_s at multiple working points, with
the double-tag prediction curve for different R_b values." This is a strong
diagnostic figure — the standard way to visualise the double-tag self-calibrating
extraction. It is the right flagship figure.

However, the description specifies only "prediction curves for different R_b
values" without committing to overlay the chi2 contours (or equivalent) that
show the confidence region. A referee looking at F4 will ask: "How tight is
the constraint from the (f_d, f_s) curve? What is the 1-sigma band on R_b
from this figure?" Without chi2 contours or uncertainty bands, the figure
shows the method but not the measurement's precision.

The published ALEPH R_b papers show this plot with the fitted working points
and error bars, together with the prediction curve at the best-fit R_b and
at +/- 1 sigma. The DELPHI reference (inspire_1661462) shows a similar figure
(Figure 2) with the single- and double-tag fractions and their uncertainties.

**Required resolution (Category B):** Update F4 description to include:
  - Data points with statistical error bars at each working point
  - Best-fit R_b prediction curve
  - +/- 1-sigma uncertainty band on the prediction curve (from the
    fit uncertainty propagated into (f_d, f_s) space)

This makes F4 a measurement figure, not just a method illustration.

---

### [C1] bFlag interpretation note is scientifically important — promote to an investigation — Category C

**Section:** 9.6

**Issue:** The strategy now correctly notes (after fixer pass) that bFlag=4
for 94% of events "is more likely an event quality or selection flag rather
than a b-identification flag" and commits to investigating this at Phase 3 by
checking the correlation between bFlag and the b-tag output.

This is the right conclusion. However, it creates a hidden consistency risk:
the BDT Approach B uses bFlag=4 as signal training labels [D9]. If bFlag=4 is
NOT a b-tag (as Section 9.6 suspects), training a BDT on it produces a
classifier that learns to identify event-quality variables, not b quarks. The
strategy does not connect the bFlag interpretation in Section 9.6 to the BDT
training label choice in Section 5.2.

**Suggestion (C):** Add a cross-reference in [D9]: "The validity of bFlag=4
as training labels is contingent on the Phase 3 bFlag interpretation
investigation (Section 9.6). If bFlag=4 is found to be a quality flag rather
than a b-tag, the BDT training will use only the self-labelling option (option 2
from Section 5.2), as the bFlag proxy labels would be uninformative for
b-tagging purposes." This makes the dependency explicit and prevents Phase 3
from discovering a training paradigm problem mid-execution.

---

### [C2] C_b systematic propagation method is ambiguous — Category C

**Section:** 7.1

**Issue:** The hemisphere correlation C_b systematic is evaluated via
"data-MC comparison of correlation-inducing variables: cos(theta), primary
vertex error, jet momentum, y_3." The systematic on R_b is then propagated
by "propagating and adding their contributions linearly" (quoting
hep-ex/9609005, Section: "Hemisphere-hemisphere correlation uncertainties").

The "propagating and adding linearly" prescription is the ALEPH convention
for C_b uncertainties specifically because the four correlation sources are
physically independent mechanisms (detector inhomogeneity, interaction region
size, B momentum coupling, gluon radiation) and the sum could be either
coherent or incoherent depending on which mechanism dominates. The published
ALEPH total from this procedure was delta_R_b = 0.00050.

The strategy does not commit to whether the combination is linear (as ALEPH
did) or in quadrature. It also does not specify the magnitude of the systematic
it expects for each source — making the precision estimate in Table 8.2
("hemisphere correlations: ~0.00100") unverifiable at review.

**Suggestion (C):** Add to the C_b systematic in Section 7.1 and/or the
precision table in Section 8.2: "Following hep-ex/9609005, the four correlation
sources are combined linearly (not in quadrature) because they share systematic
drivers (the published total 0.00050 linear combination decomposes as
approximately 0.00020 from each of detector and momentum correlation plus
smaller contributions from interaction region and y_3). Our expected total
is doubled (~0.00100) due to simplified tag system and missing per-hemisphere
primary vertex; the multiplier will be updated at Phase 3 after C_b is
measured from data." This makes the propagation prescription auditable.

---

### [C3] VDET year-to-year change is identified but its impact on d0 sentinel fraction is not estimated — Category C

**Section:** 9.4 [A4], 9.2 [A2]

**Issue:** Section 9.4 mentions the VDET change between 1993 and 1994 in the
context of angular acceptance. Section 9.2 documents the ~36% d0 sentinel
fraction (tracks without VDET hits). These two facts are connected: the VDET
acceptance change between years affects how many tracks have VDET hits, which
directly affects the sentinel fraction and therefore the effective tagging
efficiency per year.

The strategy treats the 36% sentinel fraction as a fixed constant derived from
the 1994 MC. But if the sentinel fraction varies significantly between years
(e.g., because VDET coverage was different in 1992 vs 1994), the tagging
efficiency is year-dependent in a way not captured by the 1994 MC alone.

**Suggestion (C):** Add to Section 9.2 or 9.4: "The d0 sentinel fraction
(~36%) is derived from 1994 MC. Phase 3 must verify whether the sentinel
fraction differs between data years by computing nvdet > 0 fractions per year
in data. A year-to-year variation > 3% would indicate a year-dependent VDET
coverage effect that must be included in the per-year systematic. [Action in
Phase 3: per-year sentinel fraction table.]" This is a one-line computation
in Phase 3 that prevents a blind spot.

---

### [C4] Analytical cross-check for toy-based uncertainty not scheduled for the dominant systematic — Category C

**Section:** 7.3, conventions/extraction.md

**Issue:** Decision [D13] commits to toy-based uncertainty propagation as
primary with "analytical propagation as cross-check." The conventions file
(`conventions/extraction.md`) specifies: "if analytical, verify against toys
for at least the dominant sources." The strategy inverts this — toys are
primary, analytics are cross-check — which is more robust. However, neither
the strategy nor COMMITMENTS.md specifies WHICH systematics receive the
analytical cross-check.

For the hemisphere correlation C_b, the analytical Jacobian dR_b/dC_b is
straightforward to derive from the double-tag equations and could serve as an
important sanity check. For the detector simulation (sigma_d0) systematic, the
analytical form is more complex but can be approximated. Without specifying
which sources get the analytical cross-check, there is a risk that Phase 4
skips it entirely ("the toys are primary, so we'll skip the analytics").

**Suggestion (C):** Add to [D13]: "Analytical cross-checks are required for
at minimum: (i) C_b (straightforward Jacobian from double-tag equations;
expected magnitude from hep-ex/9609005 Table: 0.00050), and (ii) R_c
constraint (dR_b/dR_c ~ -0.05 from Section 4.3, giving delta_R_b ~
0.05 * 0.0030 = 0.00015). Document the analytic vs toy agreement for these
two dominant sources in the Phase 4a artifact."

---

## DEPTH MANDATE Evaluation

Per-section probe, as required:

**Section 4 (Technique Selection):**
- Strongest figure missing: a resolving power plot comparing the double-tag
  extraction precision as a function of b-tag working point and statistics.
  This would show the "knee" where increasing efficiency no longer improves
  total uncertainty. Not required for Phase 2, but the strategy should note
  this as a Phase 3 optimisation task.

**Section 5 (Selection Approaches):**
- Systematic descriptions: flowing prose, not checklist. No downgrade needed.
- The comparison plan in Section 5.3 (cut-based vs BDT) is well-specified.

**Section 7 (Systematic Plan):**
- Per-source impact figures: the scaling table in Section 8.2 provides this
  for R_b. For A_FB^b, Section 7.4 has tabular descriptions but no per-source
  magnitude estimate. The angular dependence of b-tag efficiency is listed as
  "one of the dominant A_FB^b systematics" without an estimate. From the
  published ALEPH paper (inspire_433746), the dominant A_FB^b systematic is
  the b hemisphere charge modelling at ~0.0034 total systematic. The strategy
  should add a rough magnitude estimate analogous to the R_b table in 8.2.

**Section 9 (Mitigation Strategies):**
- Future Directions items: none explicitly deferred. Section 9.1 closures
  are all Phase 3/4 tasks. No evidence of feasible work left undone.

**Section 12 (Flagship Figures):**
- All seven planned figures are well-described.
- The P_hem discriminant plot is relegated to "supporting figures" — given
  the importance of validating the tagger output (not just the input variable),
  this deserves more prominence. A referee will request it as a matter of
  course. At minimum, it should be promoted to a numbered supplementary figure
  with a commitment to its production in COMMITMENTS.md. This overlaps with
  the [C6] finding from the previous review (nora_766f), which was
  categorised as C but not resolved in the fixer pass. It remains advisory.

---

## RAG Evidence (corpus findings used in this review)

| Query | Key finding | Used in |
|-------|-------------|---------|
| "hemisphere correlation factor C_b double tag R_b bias" | hep-ex/9609005: 4 correlation-inducing variables combined linearly; published total 0.00050 | [C2], [B1] |
| "primary vertex per hemisphere track-in-vertex bias" | hep-ex/9609005: per-hemisphere vertex explicitly stated; DELPHI inspire_1660341: beam-spot-constrained iterative fit per hemisphere | [B1] |
| "self-calibrating fit charge asymmetry A_FB five event categories chi2" | inspire_1661115 and inspire_1661252 (DELPHI): chi2-fit to exactly 5 event categories N, N-bar, N^D, N^D-bar, N^same; correlations accounted for in the combined fit | [A1] |
| "BDT MVA hemisphere correlation C_b inflation double tag" | No published evidence of BDT-C_b inflation found in LEP corpus (LEP analyses used cut-based tags); conventions/extraction.md Pitfalls section documents the mechanism | mentioned in [B1] context |
| "negative impact parameter tail resolution calibration sigma_d0" | DELPHI inspire_1660379: fine tuning of track IP resolution from negative-tail Rφ and Rz distributions; confirms bin-by-bin correction approach | [CP3 check] |

---

## Summary Table

| ID | Section | Category | Description |
|----|---------|----------|-------------|
| A1 | 4.2, 6.3 | **A** | A_FB^b governing fit formulation inconsistent between sections; five-category chi2 fit not explicitly adopted |
| B1 | 5.1, 7.1 | **B** | [D17] primary vertex investigation deferred without committing to remediation path for each scenario |
| B2 | 8.3 | **B** | A_FB^b precision estimate uses incorrect sqrt(kappa_N) scaling |
| B3 | 5.2 | **B** | BDT diagnostic action on positive result incompletely specified |
| B4 | 12, F4 | **B** | Flagship figure F4 missing chi2 contours / uncertainty bands |
| C1 | 9.6, 5.2 | **C** | bFlag interpretation and BDT training label validity cross-reference missing |
| C2 | 7.1 | **C** | C_b systematic combination prescription (linear vs quadrature) unspecified |
| C3 | 9.2, 9.4 | **C** | Per-year d0 sentinel fraction variation not committed as Phase 3 check |
| C4 | 7.3 | **C** | Analytical cross-check targets unspecified despite convention requirement |

---

## Resolving Power Verdict

The measurement retains genuine resolving power. The statistical precision
estimate (~0.0009 on R_b, ~0.005-0.007 on A_FB^b) is consistent with the
published ALEPH benchmarks at our dataset size. The dominant systematic risks
(C_b from hemisphere correlations, sigma_d0 calibration, eps_c uncertainty)
are documented and mitigated with literature-standard methods.

The single Category A finding (A_FB^b fit formulation) is surgically specific
and does not alter the physics strategy — it requires one sentence designating
the five-category chi2 fit as the governing extraction and one paragraph in
Section 6.3 specifying its structure. This would not expose the analysis to a
fundamental methodological challenge from a referee.

**After resolving [A1] and [B1]–[B4]:** This strategy is of Phase 3 advancing
quality. The analysis is telling the truth about what it can measure.
