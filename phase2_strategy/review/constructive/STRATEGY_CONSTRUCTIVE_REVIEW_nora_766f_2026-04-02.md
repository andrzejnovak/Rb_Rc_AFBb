# Constructive Review — Phase 2 Strategy
# R_b, R_c, A_FB^b Analysis

**Reviewer session:** nora_766f  
**Date:** 2026-04-02  
**Artifact:** `phase2_strategy/outputs/STRATEGY.md`  
**MCP_LEP_CORPUS:** true (searches performed — see §RAG Evidence)  
**REVIEW_CONCERNS.md:** empty at session start (no prior cross-phase concerns)

---

## Overall Assessment

The strategy document is strong. The core physics reasoning is sound, the
double-tag self-calibration is the right approach given the no-MC-truth
constraint [A1], and the kappa-scan plan for A_FB^b follows the published
ALEPH method faithfully. The COMMITMENTS.md is well-populated.

This review identifies two Category A findings (one is a genuine physics
methodology gap, one is an underspecified commitment that will cause
systematic ambiguity at Phase 4a), four Category B findings (missed
opportunities to strengthen the measurement), and several Category C
suggestions. Nothing here overturns the strategy — but the A findings
must be resolved before Phase 3 begins.

**Resolving power verdict:** The measurement has genuine resolving power.
3.05M events with a self-calibrating b-tag can reach statistical precision
comparable to the published ALEPH value. The strategy's primary weakness
is not the physics but the chain of approximations for hemisphere
correlations and sigma_d0 calibration, which together may push the
systematic floor above what is necessary.

---

## Findings

---

### [A1] Primary vertex reconstruction strategy is unspecified — Category A

**Section:** 5.1 Approach A (Cut-Based), and implicitly throughout.

**Issue:** The entire analysis depends on hemisphere-by-hemisphere tagging
using d0 measured relative to a primary vertex. The strategy never specifies
how the primary vertex will be reconstructed. This is not a minor detail: the
primary vertex position and its error directly set the impact parameter
significance, the tagging discriminant, and the hemisphere correlation C_b.

The ALEPH reference (hep-ex/9609005, Section: "The Five Hemisphere Tags")
explicitly states: "A new primary vertex finder is employed, which reconstructs
the Z decay point separately in each hemisphere." The DELPHI reference
(inspire_1661462, Section: "Reconstruction of hemisphere vertex") describes
a beam-spot-constrained iterative vertex fit per hemisphere.

Our data has: beam position stored as `bx`, `by`, `ebx`, `eby` (confirmed in
DATA_RECONNAISSANCE.md). Track 3D positions `vx`, `vy`, `vz` are available.
Track impact parameters d0 and z0 are available. But d0 is defined as "distance
of closest approach to the primary vertex" — which vertex? If d0 in the
stored branches is already relative to a global (event-level) primary vertex
fitted at ntuple production, then the hemisphere-by-hemisphere primary vertex
issue does not arise. If it is relative to the beam spot only, then we need
a per-hemisphere vertex fit.

**This is Category A because:** The choice of primary vertex definition changes
the numerical value of d0/sigma_d0 and therefore the tag discriminant. An
underspecified primary vertex creates an uncontrolled systematic that cannot
be assigned post-hoc. The hemisphere correlation C_b is also sensitive to
whether the primary vertex is shared across hemispheres (inflates correlation)
or reconstructed per hemisphere (reduces correlation).

**Required resolution:** Investigate what the stored d0 is relative to. Options:
1. If d0 is relative to a global event-level primary vertex (most likely for
   archived ntuples), document this explicitly. Then specify how the primary
   vertex error enters sigma_d0 (the bx/by error terms). The primary vertex
   position resolution (~60 micron transverse, from beam spot ~150 micron +
   vertex resolution) is typically the dominant contribution for low-purity tracks.
2. If d0 is relative to the beam spot only, a per-hemisphere vertex fit using
   the iterative trimming method (DELPHI: inspire_1661462) is required to
   reduce the primary vertex uncertainty.

Add a [D] decision label for the primary vertex strategy and update
COMMITMENTS.md with a corresponding investigation task.

---

### [A2] Hemisphere invariant mass tag is mentioned as BDT input but not defined as a standalone tag — Category A (ambiguity)

**Section:** 5.2 Approach B, BDT input variables; also Section 4.1 [D3].

**Issue:** The ALEPH Q tag (hep-ex/9609005, "The Five Hemisphere Tags") is
explicitly described as combining TWO algorithms: (1) the hemisphere track
probability product P_hem, and (2) a hemisphere invariant mass tag (tracks
ordered by probability, combined until mass > 1.8 GeV/c^2). The strategy's
Approach A uses only P_hem ([D8]: "Primary: probability tag P_hem") and
lists the mass tag only as a BDT input variable in Approach B.

This is a missed opportunity with a significant consequence: the combined
probability+mass tag is the strongest published single-lifetime-tag for R_b
at LEP, and its combination is what gives the Q tag its high purity. The
strategy commits to implementing only the probability component in Approach A,
calling this "simplified" [D3], but does not commit to implementing the mass
component as a standalone cross-check or as a combined tag.

**Specifically:** The invariant mass of the hemisphere up to the last track
added before exceeding 1.8 GeV/c^2 is a powerful discriminator because charm
hadrons rarely produce invariant masses above 1.8 GeV/c^2 while B hadron
decays commonly do. This does NOT require particle ID — only track 4-vectors,
which are available (px, py, pz, mass branches in DATA_RECONNAISSANCE.md).

This is Category A because [D3] as written ("simplified two-tag system rather
than full 5-tag system") does not specify whether the mass component of the
Q tag is included or excluded. If it is excluded, the efficiency plateau
will be lower than achievable and the systematic floor will be correspondingly
higher. If it is included but undocumented, Phase 4a will silently implement
a stronger tag than the strategy committed to, making STRATEGY.md
non-reproducible.

**Required resolution:** Clarify whether the primary approach (Approach A)
uses P_hem only, the mass tag only, or both combined. Given that the mass
tag is implementable from available branches (4-vectors available), the
recommendation is to implement both and combine them. If combined, add a
[D] label ("Combined probability-mass tag following ALEPH Q tag prescription")
and update the flag figure F3 description (impact parameter significance
distribution) to include a parallel mass tag discriminant plot.

---

### [B1] R_c sensitivity from the loose-working-point cross-check is underspecified — Category B

**Section:** 4.3, 6.3

**Issue:** Decision [D6] commits to treating R_c as a constrained parameter
with an "extended fit cross-check" that floats R_c using two working points
(tight = b-enriched, loose = c-sensitive). The strategy does not estimate
the actual sensitivity of this cross-check to R_c, nor does it specify what
defines the c-sensitive operating point.

From the corpus (inspire_416138, hep-ex/9609005): the charm tagging efficiency
epsilon_c at a loose lifetime cut is typically 5-15% while epsilon_b is 30-60%.
With epsilon_c ~ 0.10 and 3M events, the charm double-tag count is:
N_tt^cc ~ 3M * (0.10)^2 * 0.17 ~ 5,100 events. The fractional precision on
epsilon_c from data is ~1/sqrt(5100) ~ 1.4%, translating to dR_c/R_c ~
a few percent statistical. This suggests a ~0.004-0.007 statistical precision
on R_c from the cross-check — worse than the LEP combined systematic (0.0030)
but potentially useful as a self-consistency check.

**The missing piece:** The strategy commits to the cross-check but does not:
(a) estimate whether it has any sensitivity, (b) define the operating points
quantitatively (what epsilon_c target?), or (c) specify how the cross-check
passes or fails.

**Required resolution (Category B):** Add a brief sensitivity estimate for the
R_c cross-check in Section 4.3. Specify the target charm efficiency for the
loose working point (e.g., epsilon_c ~ 10-15% from MC) and a pass/fail
criterion (e.g., the fitted R_c should agree with LEP combined within 2 sigma).
This prevents the cross-check from being skipped at Phase 4 because it was
never concretely defined.

---

### [B2] The A_FB^b angular binning choice needs explicit justification — Category B

**Section:** 6.3 [D12]

**Issue:** Decision [D12] commits to "8-10 uniform bins in |cos(theta)|"
without justification. The DELPHI analyses (inspire_1661397, inspire_1660891)
use a cos(theta) range divided into 8 bins for 1992-1993 and 9 bins for 1994-2000,
motivated by the changed vertex detector acceptance between these periods. Our
dataset spans 1992-1995, crossing this boundary.

More importantly: the strategy discusses per-year extraction as a cross-check
[Section 9.4], but does not address whether the angular binning should differ
between years to account for the changing VDET acceptance (the VD setup changed
in 1994, affecting the |cos(theta)| acceptance at the edges). If the angular
efficiency is year-dependent and the same angular bins are used for all years,
a systematic bias could arise in the fitted asymmetry.

**Required resolution (Category B):** Add an explicit sub-decision under [D12]:
(a) whether the angular binning is uniform across all years or year-dependent,
(b) what the angular acceptance is as a function of year based on the available
cos(theta_thrust) distributions (these plots exist from Phase 1 figure F6),
(c) whether the |cos(theta)| cut of 0.9 (from the ALEPH reference) remains
appropriate for our reconstruction quality.

---

### [B3] Hemisphere correlation systematic needs quantitative grounding — Category B

**Section:** 7.1 (Efficiency Modeling — Efficiency Correlation)

**Issue:** The strategy commits to evaluating C_b from MC and assigning
a systematic from "data-MC comparison of correlation-inducing variables
(cos(theta), primary vertex error, jet momentum) following hep-ex/9609005 Section 7."

The ALEPH reference (hep-ex/9609005, Section: "Hemisphere-hemisphere
correlation uncertainties") specifies FOUR comparison variables: cos(thrust
axis angle), component of primary vertex error transverse to thrust, jet
momenta, and y_3 (for gluon radiation correlations). The corpus search
confirms this explicitly (search result [5], hep-ex/9609005). The published
systematic from hemisphere correlations was 0.00050 on R_b.

**The gap:** The strategy mentions this procedure but does not commit to
evaluating ALL FOUR of the published correlation-inducing variables. It says
"cos(theta), primary vertex error, jet momentum" — omitting y_3 (the kT jet
resolution parameter, related to gluon activity). Gluon splitting correlations
(g -> bb, g -> cc) are one of the three correlation sources, and y_3 is the
ALEPH-prescribed variable for checking them.

**Required resolution (Category B):** Add y_3 (or an equivalent 3-jet rate
variable computable from the available jet trees: akR4/akR8/ktN2) to the list
of correlation-inducing variables to be compared. The ktN2 jet tree from
DATA_RECONNAISSANCE.md directly provides a y_3-equivalent. Update Section 7.1
and COMMITMENTS.md accordingly.

---

### [B4] The A_FB^b figure (F2) is the right money plot but is missing a key component — Category B

**Section:** 12 Flagship Figures, Figure F2

**Issue:** F2 is described as "<Q_FB> vs cos(theta_thrust) in the b-tagged
sample, with fitted linear function. Published ALEPH result overlaid."

This is the correct figure. However, the strategy does not commit to also
showing the BACKGROUND-SUBTRACTED version of this figure (i.e., the pure
b-quark asymmetry after subtracting the charm and light-quark contributions).
The ALEPH paper (inspire_433746) shows the corrected angular distribution
explicitly. Without this, the reader cannot assess how large the background
correction was or whether it is under control.

**Additionally:** The strategy commits to kappa = {0.3, 0.5, 1.0, 2.0} but
F2 shows only one kappa value. A referee will ask: "What does the asymmetry
look like for the other kappa values? Do they agree?" Consider adding a
companion figure or panel showing A_FB^b(kappa) for all four values, which
directly tests the charge separation model dependence.

**Required resolution (Category B):** Promote F2 to include: (a) the raw
<Q_FB> vs cos(theta) for the dominant kappa value, and (b) a companion
summary showing A_FB^b extracted at each kappa = {0.3, 0.5, 1.0, 2.0}.
The kappa consistency plot is itself a cross-check committed to in
COMMITMENTS.md but has no corresponding flagship figure. This should be
either added as F7 or merged into F2 (two panels).

---

### [C1] The "pseudo-closure" operating point stability scan conflates two distinct checks — Category C

**Section:** 9.1 Mitigation for [A1], item 4; Validation test in COMMITMENTS.md

**Issue:** The strategy uses "operating point stability" as the proxy closure
test in place of an MC truth closure (not available due to [A1]). This is
a reasonable mitigation, but the document conflates two diagnostically
distinct things:

1. **Method robustness** (does R_b change as the working point moves?): tests
   whether the extraction is in a stable region and not sensitive to the
   exact cut. This is the stability scan.

2. **Background model validation** (does the extracted R_b agree with the true
   R_b?): tests whether the double-tag extraction is unbiased. This would
   normally be an MC truth closure.

The stability scan cannot substitute for a closure test — it only tests
self-consistency. A biased extraction can produce a perfectly flat stability
scan at the wrong value. The strategy acknowledges this implicitly ("a slope
would indicate bias") but does not propose a way to bound the absolute bias.

**Suggestion (C):** Add a partial closure test using the MC itself in the
following form: run the double-tag extraction on MC treating it as if it were
data (computing N_t and N_tt from MC), and compare the extracted R_b to the
known fraction of hemisphere-pairs in the MC that have both hemispheres from
Z->bb decays (which can be estimated from the bFlag=4 fraction in data as a
cross-check). This is not a full MC truth closure (no truth labels) but is
a self-consistency check at the MC level that the strategy currently lacks.
Document explicitly in Section 9.1 that the stability scan does NOT substitute
for a bias test.

---

### [C2] The sigma_d0 parameterization should adopt a 2D binning scheme from the start — Category C

**Section:** 5.1 [D7], 9.3

**Issue:** Decision [D7] commits to calibrating sigma_d0 in bins of (nvdet,
momentum, cos(theta)). The ALEPH reference (inspire_433306) uses two-dimensional
binning in (p_T, theta) with separate treatment by VDET hit count. The strategy
lists this as a 3D binning (nvdet * momentum * cos(theta)), but does not
specify the bin granularity.

The MC has ~7.8M events (1994 only). With ~64% of tracks having VDET hits,
~5M tracks have valid d0. If we bin in (nvdet={1,2}, p=[0.5,2,5,15,45] GeV,
cos(theta)=[0, 0.3, 0.6, 0.9]), that is 2 * 4 * 3 = 24 bins, each with
~200k tracks — adequate. But the momentum bins at high p (15-45 GeV) and low
occupancy (high cos(theta)) may have insufficient statistics for the calibration
of the non-Gaussian tails.

**Suggestion (C):** Specify the calibration binning in the strategy document
(add to Section 5.1). Commit to adaptive binning if any cell falls below 1000
tracks. Document the expected calibration precision (fractional width of the
negative-tail Gaussian) per bin using the available MC statistics.

---

### [C3] The A_FB^b extraction uses |cos(theta)| but the correction formula uses signed cos(theta) — Category C

**Section:** 6.2, 6.3 [D12]

**Issue:** Section 6.3 states bins of "|cos(theta_thrust)|" for the A_FB^b
fit. The physical differential cross-section (Section 2.2):

  d(sigma)/d(cos theta) ~ 1 + cos^2(theta) + (8/3) * A_FB^b * cos(theta)

requires SIGNED cos(theta) to extract A_FB^b, because the 8/3 * A_FB^b term
is odd in cos(theta). The DELPHI papers (inspire_1661397, inspire_1660891)
bin in signed cos(theta_thrust) ranging from [-0.925, +0.925] or similar.
The ALEPH reference (inspire_433746) uses the forward-backward difference
Q_F - Q_B where F and B are defined by the sign of cos(theta_thrust).

**The ambiguity:** The strategy writes "|cos(theta)|" in [D12] but then writes
"fitting the linear cos(theta) dependence" — which requires signed cos(theta).
This is an internal inconsistency that needs to be resolved before Phase 3
implements the angular binning.

**Suggestion (C):** Clarify in [D12]: the BINS are in |cos(theta_thrust)|
(both hemispheres contribute symmetrically), but for each bin the Q_FB
observable uses the signed cos(theta) to define the forward hemisphere.
The fit is to the differential asymmetry:
  A_FB^{b,diff}(cos(theta)) = (8/3) * A_FB^b * cos(theta) / (1 + cos^2(theta))
which is the DELPHI approach (inspire_1661397, Eq. 26). This should be
explicitly adopted as the fit formulation with a [D] label.

---

### [C4] The R_c SM value cited has an internal inconsistency that should be documented — Category C

**Section:** 4.3, 14

**Issue:** Section 4.3 states R_c^SM = 0.17223 from hep-ex/0509008.
INPUT_INVENTORY.md lists the LEP combined measurement as R_c = 0.1721 +/- 0.0030,
while listing R_c^SM = 0.17223. The measured value (0.1721) is slightly lower
than the SM prediction (0.17223), and the strategy uses 0.17223 as the central
value for the constraint.

In the double-tag formula, using the SM value rather than the measured value
as the constraint introduces a small bias if the true R_c departs from the SM.
The difference is only ~0.0001, well within the assigned systematic of 0.0030,
but the strategy should clarify: is R_c constrained to the SM value (0.17223)
or to the LEP measured value (0.1721)? The former tests EW physics; the latter
is more conservative.

**Suggestion (C):** Explicitly state which value is used for the constraint and
why. Add a note that the difference between the SM and LEP measured value
(0.00013) is negligible compared to the 0.0030 systematic, but document the
choice for reproducibility.

---

### [C5] The per-year stability figure (F6) should include a chi2/ndf test — Category C

**Section:** 12, Flagship Figure F6

**Issue:** F6 is described as "R_b (and A_FB^b) extracted per year, with
combined result and chi2/ndf." This is correct in spirit. The COMMITMENTS.md
also includes "Per-year consistency" as a validation test.

However, the strategy does not specify the chi2/ndf threshold that triggers
investigation. Given that the MC covers only 1994 [L1], a chi2/ndf >> 1
across years could indicate real detector effects OR could simply reflect
MC-driven systematics not captured for non-1994 years. The interpretation
is ambiguous without a prior specification.

**Suggestion (C):** Add to COMMITMENTS.md: "If chi2/ndf > 2 across the 4 years
in the per-year extraction, spawn a dedicated investigation into year-dependent
detector effects. If chi2/ndf < 0.5, investigate whether the year-to-year
correlations (same systematic sources in all years) are correctly accounted for."

---

### [C6] The flagship figure set is missing a data/MC comparison on the tagging discriminant — Category C

**Section:** 12 Flagship Figures

**Issue:** The six flagship figures are:
F1: R_b stability scan, F2: A_FB^b angular, F3: d0/sigma_d0 distribution,
F4: f_d vs f_s scatter, F5: systematic breakdown, F6: per-year stability.

F3 shows the input variable (signed impact parameter significance), which
is appropriate. However, there is no flagship figure showing the b-tag
DISCRIMINANT distribution (P_hem or BDT output) in data vs MC. This is the
one figure a referee will invariably ask for: "Does your tagger agree between
data and MC?" F3 (d0/sigma_d0) is the input, not the output.

**Suggestion (C):** Replace or augment F3 to include a panel showing the
hemisphere probability tag output (P_hem, log scale) for data and MC, with
a ratio panel. This is the direct validation of the tagger and is standard
in all LEP R_b papers (e.g., DELPHI inspire_1661462 shows the tagging
discriminant distributions explicitly). The signed d0/sigma_d0 can remain
as a supplementary figure.

---

## Additional Observations (informational, no action required)

**Resolving power check:** With 3.05M events and epsilon_b ~ 30%, we expect
N_tt ~ 56k double-tagged events. The fractional uncertainty on R_b from
the double-tag method scales as ~1/sqrt(N_tt) * (1/epsilon_b). The expected
statistical precision (~0.0009) is well-established and the strategy's estimate
is correct. The measurement has genuine discriminating power — it can
distinguish the SM prediction (0.21578) from the ALEPH measured value (0.2158)
to within 1 sigma, and would detect a ~1% deviation from SM at ~2 sigma.

**A_FB^b resolving power:** The 2.8-sigma tension between A_FB^b (LEP) and
A_l (SLD) in determining sin^2(theta_eff) is driven by the aggregate LEP
A_FB^b value. A new measurement from ALEPH data with explicit systematic
accounting could either confirm or add nuance to this tension. The strategy
is appropriately ambitious in targeting a comparison with the published value.

**bFlag investigation:** The strategy notes bFlag = 4 for ~94% of data events
and bFlag = -1 for ~6%. The analysis treats bFlag as a pre-existing b-tag
without fully resolving its definition. A 6% "untagged" fraction at the ntuple
level is unusual — it may indicate events that fail a quality cut (not a physics
tag) or events with no reconstructable primary vertex. Before Phase 3, the
definition of bFlag should be confirmed from ALEPH documentation. If bFlag = -1
corresponds to events without a reconstructable primary vertex, this has
implications for the primary vertex strategy raised in [A1].

**DELPHI neural network approach:** The corpus search found an advanced DELPHI
approach (inspire_1661252) using a neural network combining vertex charge, jet
charge, and identified leptons for A_FB^b charge tagging, achieving
sigma(syst) = 0.0017 vs our expected 0.004-0.005. This is a methodological
reference for future improvement. The current strategy's self-calibrating
hemisphere charge method is appropriate given our constraints, but the gap in
systematic performance (~2x) should be noted in the precision estimates section
as primarily driven by our lack of identified leptons [A5] (not a fixable
issue with available data).

---

## RAG Evidence

Searches executed:
1. "hemisphere correlation factor double tag R_b systematic" — confirms hep-ex/9609005
   four-variable protocol for C_b evaluation (cos(theta), PV error, jet momenta, y_3)
2. "A_FB b quark charge separation delta_b calibration systematic" — found DELPHI
   methods (inspire_1661252, inspire_1661397, inspire_1660891) for the self-calibrating
   fit formulation; differential asymmetry binning in signed cos(theta) confirmed
3. "R_c double tag charm efficiency extraction method" — confirmed R_c double-tag
   sensitivity estimates; charm efficiency ~5-15% at loose working points
4. "primary vertex reconstruction hemisphere b-tag ALEPH VDET impact parameter" —
   confirmed that hep-ex/9609005 uses per-hemisphere primary vertex reconstruction,
   not a global event vertex; beam-spot constraint procedure from inspire_1661462
5. "b fragmentation function Peterson Bowler systematic reweighting LEP" — confirmed
   reweighting procedure for Peterson/Bowler/Lund fragmentation functions; relevant
   for the hadronization systematic
6. "hemisphere mass tag b quark secondary vertex invariant mass" — confirmed the
   invariant mass tag (tracks combined until mass > 1.8 GeV/c^2) is a distinct
   algorithm from P_hem and is typically combined with it for the Q tag

---

## Summary Table

| ID | Category | Section | Finding |
|----|----------|---------|---------|
| A1 | **A** | 5.1, throughout | Primary vertex definition unspecified — fundamental to all d0 significances and correlations |
| A2 | **A** | 5.1, 5.2, 4.1 | Mass tag component of ALEPH Q tag not committed to in Approach A — scope ambiguity |
| B1 | B | 4.3, 6.3 | R_c cross-check sensitivity not estimated; operating point undefined |
| B2 | B | 6.3 [D12] | Angular binning strategy not year-dependent despite known VDET change in 1994 |
| B3 | B | 7.1 | y_3 omitted from hemisphere correlation check variables (required by hep-ex/9609005) |
| B4 | B | 12, F2 | A_FB^b money plot missing background-subtracted version and kappa comparison |
| C1 | C | 9.1 | Stability scan conflates robustness with bias bound; no MC-level self-consistency test |
| C2 | C | 5.1 [D7] | sigma_d0 calibration binning not specified; adaptive binning needed |
| C3 | C | 6.3 [D12] | "|cos(theta)|" vs signed cos(theta) ambiguity in fit formulation |
| C4 | C | 4.3, 14 | SM vs LEP-measured R_c constraint value choice undocumented |
| C5 | C | 12 F6 | Per-year chi2/ndf threshold not specified; ambiguous interpretation trigger |
| C6 | C | 12 | Missing discriminant (P_hem output) data/MC comparison as flagship figure |

**Blocking for Phase 3 advance:** Findings A1 and A2 must be resolved first.
B1-B4 should be addressed in STRATEGY.md before Phase 3 begins; they are not
blocking individually but collectively create scope gaps that will surface as
Category A findings in Phase 4a review if left unaddressed.

---

## Recommended Actions

1. **Immediately (A1):** Investigate what the stored d0 is relative to.
   Run a quick check: compute d0/sigma_d0 and verify the negative tail is
   approximately Gaussian with unit width. If the tail width is >> 1 without
   any sigma_d0 parameterization applied, the d0 is likely relative to the
   beam spot only (large sigma), not a fitted vertex. If the tail is roughly
   consistent with unit width, a global primary vertex was used. Add a [D]
   decision label covering the primary vertex choice.

2. **Before Phase 3 starts (A2):** Commit explicitly to the mass-tag component.
   Modify [D8] to: "Primary: combined probability-mass tag (following ALEPH Q tag);
   Cross-check: probability-only tag and N-sigma tag separately." The mass tag
   requires only: sort tracks by inverse probability, combine until invariant
   mass > 1.8 GeV/c^2, use the probability of the last added track as
   discriminant. Implementation cost is low; gain in purity is substantial.

3. **Before Phase 3 starts (B3):** Add y_3 (from ktN2 jet tree) to the hemisphere
   correlation evaluation variables in Section 7.1. This is a one-line addition
   to the systematic plan and a one-line addition to COMMITMENTS.md.

4. **Before Phase 3 starts (C3):** Resolve the |cos(theta)| vs signed cos(theta)
   ambiguity in [D12]. Adopt the DELPHI differential asymmetry formulation
   explicitly.

5. **Phase 4 preparation (B1, B2, B4):** Address the R_c cross-check sensitivity
   estimate, year-dependent angular binning, and A_FB^b figure set before
   Phase 4a planning begins.
