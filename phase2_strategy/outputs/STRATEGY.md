# Analysis Strategy — R_b, R_c, and A_FB^b

Session: peter_b030 | Date: 2026-04-02

---

## 1. Summary

This document defines the analysis strategy for measuring R_b, R_c, and
A_FB^b in hadronic Z decays using archived ALEPH data at sqrt(s) = 91.2 GeV.
The strategy is grounded in Phase 1 data reconnaissance findings and the
published methodologies of ALEPH and the LEP/SLD EWWG combination. The
primary technique is the **double-tag hemisphere counting method** for R_b,
with the **hemisphere jet charge method** for A_FB^b and an **external-input
constrained extraction** for R_c. Every design decision cites the Phase 1
finding or literature reference that motivates it.

---

## 2. Physics Motivation

### 2.1 Why R_b, R_c, and A_FB^b

At the Z pole, the partial width ratios R_b = Gamma(Z -> bb) / Gamma(Z ->
hadrons) and R_c = Gamma(Z -> cc) / Gamma(Z -> hadrons) test the electroweak
vertex corrections coupling preferentially to heavy quarks. R_b is sensitive
to the top quark mass through vertex corrections (the large V_tb CKM
coupling), making it a probe of non-standard vertex corrections even with
m_top precisely known. Most QCD and electroweak radiative corrections cancel
in the ratio, leaving R_b sensitive to novel physics at the Zbb vertex
(hep-ex/9609005, Section: Introduction; hep-ex/0509008).

The forward-backward asymmetry A_FB^b measures the parity violation in Z ->
bb through the product of initial- and final-state couplings. At tree level:

  A_FB^{0,b} = (3/4) * A_e * A_b

where A_f = 2 * v_f * a_f / (v_f^2 + a_f^2) and v_f, a_f are the vector and
axial-vector couplings. A_FB^{0,b} provides a determination of the effective
weak mixing angle sin^2(theta_eff). The LEP combined value shows a 2.8-sigma
tension with the SLD A_l measurement (hep-ex/0509008, Table), making this
observable of particular interest.

### 2.2 Observable Definitions

**[D1] Observable definitions follow the LEP EWWG standard (hep-ex/0509008).**

**R_b** (verified against hep-ex/0509008 and inspire_416138):

  R_b^0 = Gamma(Z -> bb) / Gamma(Z -> hadrons)

Operationally measured as a hemisphere-tagged event fraction, corrected for
tagging efficiency, background, and hemisphere correlations via the double-tag
method. The "0" superscript denotes the pole quantity corrected for QED,
gamma exchange, and gamma-Z interference. In practice, these corrections are
small (~0.0003) and are taken from the LEP EWWG prescription
(hep-ex/0509008, Section 5.4).

**R_c** (verified against hep-ex/0509008 and inspire_483143):

  R_c^0 = Gamma(Z -> cc) / Gamma(Z -> hadrons)

The charm counting method (summing exclusive D meson rates) used by ALEPH
(inspire_483143) requires particle identification we lack [A5]. Instead, R_c
enters our extraction as a constrained parameter — see Section 5.

**A_FB^b** (verified against inspire_433746 and inspire_1661115):

  d(sigma)/d(cos theta) ~ 1 + cos^2(theta) + (8/3) * A_FB^b * cos(theta)

where theta is the angle between the incoming electron and outgoing b quark.
The pole asymmetry A_FB^{0,b} is extracted after QED and QCD corrections:

  A_FB^{0,b} = A_FB^b / (1 - delta_QCD - delta_QED)

where delta_QCD ~ alpha_s / pi ~ 0.038 (hep-ex/0509008, Section 5.5).
The quark direction is estimated from the thrust axis; the quark/antiquark
assignment uses hemisphere jet charge.

---

## 3. Sample Inventory

### 3.1 Data

From DATA_RECONNAISSANCE.md:

| Year | Events | Notes |
|------|--------|-------|
| 1992 | 551,474 | |
| 1993 | 538,601 | |
| 1994 P1 | 433,947 | |
| 1994 P2 | 447,844 | |
| 1994 P3 | 483,649 | |
| 1995 | 595,095 | |
| **Total** | **3,050,610** | Pre-selected (passesNTupleAfterCut=1) |

After applying passesAll: ~2.87M events (94% efficiency).

Cross-check: ALEPH published ~4.1M hadronic events for 1991-1995
(inspire_433746, Table 1). Our 3.05M for 1992-1995 is consistent given the
missing 1991 data (~249k events) and the pre-selection efficiency.

### 3.2 Monte Carlo

From DATA_RECONNAISSANCE.md:

- 41 files, 1994 only, ~7.8M events estimated
- Identical branch structure to data (151 branches)
- **No truth labels** [A1] — no generator-level flavour, no parton info,
  no truth matching variables
- bFlag = -999 in MC [A6]

**[L1] MC covers only 1994.** No MC for 1992, 1993, 1995. Year-dependent
detector effects (VDET alignment drift, module damage/repair) cannot be
modelled from MC. See mitigation in Section 9.

---

## 4. Technique Selection

### 4.1 R_b: Double-Tag Hemisphere Counting

**[D2] Use the double-tag hemisphere counting method for R_b.**

**Justification:** The double-tag method is the standard technique for R_b at
LEP (inspire_416138, hep-ex/9609005, inspire_433306). Its key advantage is
that the b-tagging efficiency epsilon_b is measured directly from data via the
ratio of double-tagged to single-tagged events, making the result largely
insensitive to MC modelling of b-hadron properties. This is critical given
our constraint [A1] (no MC truth labels).

**Alternative considered:** A single-tag method would require MC-calibrated
efficiency, which is impossible without truth labels. A template fit to the
tagging discriminant would also require truth-labelled MC templates. The
double-tag method's self-calibrating property is uniquely suited to our
constraints.

**Formalism** (from inspire_416138, Eq. 1-2; hep-ex/9609005, Eq. 1-2):

Events are divided into hemispheres by the plane perpendicular to the thrust
axis. For N_had hadronic Z decays:

Single-tag fraction:

  f_s = N_t / (2 * N_had) = eps_b * R_b + eps_c * R_c + eps_uds * (1 - R_b - R_c)

Double-tag fraction:

  f_d = N_tt / N_had = C_b * eps_b^2 * R_b + C_c * eps_c^2 * R_c
                       + C_uds * eps_uds^2 * (1 - R_b - R_c)

where:
- eps_q = hemisphere tagging efficiency for flavour q
- C_q = 1 + rho_q = hemisphere correlation factor
- rho_q = hemisphere-hemisphere efficiency correlation

The system of two equations with three unknowns (R_b, eps_b, and the
background term) is solved by:
1. Measuring f_s and f_d from data
2. Taking eps_c, eps_uds, C_b, C_c, C_uds from MC (with systematics)
3. Extracting R_b and eps_b simultaneously

**[D3] Use a simplified two-tag system (single b-tag at multiple working
points) rather than the full 5-tag system of hep-ex/9609005.** The 5-tag
system requires lepton identification (L tag) and particle ID (X tag for
kaons), both unavailable [A5]. We implement the lifetime-mass tag (Q tag
equivalent) at multiple working points to provide redundancy, with the
operating point stability scan serving as the cross-check equivalent of
multiple tags. The published 5-tag method is implemented as a cross-check
where feasible (using only lifetime-based tags).

### 4.2 A_FB^b: Hemisphere Jet Charge

**[D4] Use the hemisphere jet charge method for A_FB^b.**

**Justification:** This is the standard ALEPH method (inspire_433746) and
the most precise technique available with our data. It requires only track
charges and momenta (both available) and a b-enriched sample (from the
lifetime tag).

**Formalism** (from inspire_433746; inspire_1660289, Eq. 2):

The hemisphere charge is:

  Q_h = sum_i q_i * |p_{L,i}|^kappa / sum_i |p_{L,i}|^kappa

where the sum runs over tracks in a hemisphere, q_i is the track charge, and
p_{L,i} is the longitudinal momentum w.r.t. the thrust axis. The exponent
kappa controls the momentum weighting.

**[D5] Use multiple kappa values: kappa = {0.3, 0.5, 1.0, 2.0, infinity}.**
Following inspire_433746. Each kappa provides an independent measurement;
their comparison is a powerful systematic cross-check. kappa = infinity
(leading particle charge — the charge of the highest-momentum track in the
hemisphere) does NOT require particle identification; PID improves it but
is not required. Including kappa = infinity provides an additional working
point with maximally different sensitivity to fragmentation modelling,
strengthening the kappa consistency cross-check.

**kappa = infinity demotion threshold:** If the fitted charge separation
delta_b(kappa = infinity) < 0.1 (less than half the typical delta_b ~
0.20-0.25 for lower kappa values), use kappa = infinity as a cross-check
only, not in the primary combination. At delta_b < 0.1, the statistical
power of the leading-track charge is negligible and its inclusion in the
combination would add systematic uncertainty without meaningful statistical
weight. Note: kappa = infinity is implemented as the charge of the
highest-|p_L| track in the hemisphere (explicit leading-track definition),
not as a large-kappa numerical limit of the weighted sum formula.

The charge flow is Q_FB = Q_F - Q_B, where F/B are defined by the thrust
axis orientation relative to the incoming electron.

The mean charge separation delta_b = <Q_b> - <Q_bbar> is measured from data
using the lifetime-tagged sample.

**Simplified formula (approximation, valid only for 100% pure b sample):**

  A_FB^b = (8/3) * <Q_FB> / (R_b * delta_b)

This formula applies to the inclusive hadronic sample and assumes perfect
b purity. It is NOT the governing extraction method.

**Governing extraction: self-calibrating fit (inspire_433746, Section 4).**
In the tagged sample with finite purity f_b:

  <Q_FB>(cos theta) = sum_q f_q * delta_q * A_FB^q * cos(theta)

where f_q are the tagged-sample flavour fractions (not R_q). The self-
calibrating fit extracts delta_b and A_FB^b simultaneously from the angular
distribution of Q_FB in b-tagged events at multiple purities
(inspire_433746, Section 4; inspire_1661115, Section 5). This method
accounts for background contamination (f_c, f_uds) and avoids the 1/f_b
bias that would arise from using the simplified formula on a tagged sample.

### 4.3 R_c: External-Input Constrained Extraction

**[D6] R_c is extracted as a constrained parameter within the double-tag
framework, not measured independently.**

**Justification:** The charm counting method (inspire_483143) requires D
meson reconstruction with particle identification, which is unavailable [A5].
A double-tag measurement of R_c would require a charm-enriched tag with
sufficient purity to separate c from uds — this is feasible using a softer
lifetime cut (charm hadrons have shorter lifetimes than b hadrons, producing
smaller but nonzero impact parameter signatures).

**Strategy:**
1. Primary: Constrain R_c to the SM prediction (R_c^SM = 0.17223) in the
   R_b extraction, with the uncertainty on R_c (from LEP combined: +/- 0.0030)
   propagated as a systematic. Note: the LEP combined measurement is
   R_c = 0.1721 +/- 0.0030, differing from SM by 0.00013, which is
   negligible compared to the 0.0030 uncertainty. The SM value is used as
   the central constraint because it avoids circular dependence on the
   measurement we are validating against.
2. Cross-check: Float R_c in an extended fit using two working points
   (tight = b-enriched, loose = c-sensitive) to probe sensitivity.
   **Estimated R_c sensitivity from cross-check:** with ~56k double-tagged
   events and eps_c/eps_b ~ 0.05 (typical), the statistical precision on
   a floated R_c is ~0.004-0.007 (from inspire_416138 scaling). This is
   comparable to the LEP combined uncertainty and sufficient to detect a
   large deviation from SM.
3. Report the fitted R_c from the cross-check, but the primary result
   uses constrained R_c [D6]. Report R_b extracted with both SM R_c
   (0.17223) and LEP-measured R_c (0.1721) central values as a
   cross-check of R_c sensitivity.

**Sensitivity dR_b/dR_c:** From the double-tag equations (inspire_416138,
Eq. 1-2), differentiating at the nominal working point:
  dR_b/dR_c ~ -eps_c/eps_b ~ -0.05
Therefore delta(R_b) from R_c constraint = 0.05 * 0.0030 ~ 0.00015. This
is small compared to other systematics (~0.0015-0.0020 total), confirming
that the R_c constraint is not a dominant source of uncertainty.

---

## 5. Selection Approaches

### 5.1 Approach A: Cut-Based Signed Impact Parameter Significance

**Grounding:** d0 branch available (DATA_RECONNAISSANCE.md). ~36% sentinel
values [A2] correspond to tracks without VDET hits (nvdet <= 0). Non-sentinel
d0 core width ~0.02 cm with extended tails from heavy-flavour decays.

**Procedure:**

1. **Event preselection:** passesAll = 1 (DATA_RECONNAISSANCE.md: ~94% pass).
   Angular acceptance |cos(theta_thrust)| < 0.9 (following inspire_433746).

2. **Track quality:** Require nvdet > 0 (VDET hits, ensures d0 is meaningful),
   highPurity = 1, ntpc > 4 (TPC hits for momentum measurement). This
   removes the ~36% sentinel tracks [A2].

3. **Impact parameter significance computation [A3]:** sigma_d0 is not stored.
   Parameterize the d0 resolution as:

     sigma_d0 = sqrt(A^2 + (B / (p * sin(theta)))^2)

   where A ~ 25 micron (intrinsic resolution) and B ~ 70 micron*GeV/c
   (multiple scattering term). The sin(theta) dependence (not sin^{3/2})
   is the standard form for the Rphi-projected impact parameter d0, as
   documented in the ALEPH detector performance (537303, Section: Preamble:
   "impact parameter resolution of around 25 micron" for 45 GeV/c muons).
   The sin^{3/2}(theta) form applies to 3D impact parameters; since the
   stored d0 branch is the Rphi projection (DATA_RECONNAISSANCE.md), the
   sin(theta) form is correct.

   **Systematic: sigma_d0 functional form.** Vary between sin(theta) and
   sin^{3/2}(theta) and propagate to both R_b and A_FB^b. This covers the
   uncertainty in the angular dependence of the resolution model.

   The parameterization is calibrated by fitting the negative d0/sigma_d0
   distribution to a Gaussian — the negative tail arises purely from
   resolution and should have unit width after correct sigma_d0 estimation
   (inspire_433306, negative tail method).

   **[D7] Calibrate sigma_d0 from the negative impact parameter tail,
   separately for tracks with 1 and 2 VDET hits, and in bins of momentum
   and cos(theta).** Binning: 5 momentum bins (0.5-1, 1-2, 2-5, 5-15,
   15+ GeV/c) x 4 |cos(theta)| bins (0-0.25, 0.25-0.5, 0.5-0.7, 0.7-0.9)
   x 2 nvdet classes = 40 calibration bins. Each bin must contain > 1000
   negative-d0 tracks for a meaningful Gaussian fit.

4. **Signed impact parameter:** The sign of d0 is defined by the angle
   between the track direction and the vector from the primary vertex to the
   point of closest approach. Positive = track crosses the jet axis downstream
   of the vertex (displaced vertex signature). Negative = resolution only.

   **[D19] Phase 3 gate: d0 sign convention validation.** Before proceeding
   with tagger construction, verify the d0 sign convention by plotting the
   d0 distribution in b-enriched hemispheres (using a preliminary loose tag
   or bFlag=4 subsample). If the positive d0 tail is not enhanced relative
   to the negative tail (i.e., if the distribution is symmetric or the
   negative tail is enhanced), the sign convention is inverted or d0 is
   unsigned, and the lifetime tag is invalid. In that case, the strategy
   must be revised (either flip the sign or investigate unsigned d0
   treatment). This is a blocking gate — no tagger construction proceeds
   until the d0 sign is validated.

   **[D17] Primary vertex definition.** The ALEPH reference analysis
   (hep-ex/9609005, Section: The Five Hemisphere Tags) uses a per-hemisphere
   primary vertex reconstruction: "A new primary vertex finder is employed,
   which reconstructs the Z^0 decay point separately in each hemisphere."
   The stored d0 branch in our ntuple must be investigated at Phase 3 to
   determine whether it is defined relative to a global event vertex, a
   per-hemisphere vertex, or the beam spot. If d0 is relative to a global
   vertex that includes the track under test, there is a systematic bias
   (the "track-in-vertex" problem: tracks from the secondary vertex pull the
   primary vertex away from the true IP, reducing the apparent impact
   parameter). **Phase 3 action:** (a) check if the d0 branch changes when
   the event vertex is recomputed excluding the track; (b) if global vertex
   is used, either recompute d0 relative to a per-hemisphere vertex, or
   assign a systematic from the track-in-vertex bias. This choice affects
   both sigma_d0 calibration and the hemisphere correlation C_b.
   **Note:** Phase 3 must resolve [D17] with the specific remediation
   committed at that time (per-hemisphere vertex refit vs inflated
   systematic vs beam-spot reference).

5. **Hemisphere b-tag variable:** For each hemisphere, combine the signed
   impact parameter significances of all quality tracks. Options:
   - **Probability tag (P_hem):** Product of probabilities that each track
     originates from the primary vertex, using the significance distribution
     of light-flavour tracks (calibrated from the negative tail).
   - **N-sigma tag:** Count of tracks with signed significance > N_cut
     (e.g., N_cut = 3).

   **[D8] Primary: combined probability-mass tag (P_hem + hemisphere
   invariant mass cut at 1.8 GeV/c^2, following the ALEPH Q tag in
   hep-ex/9609005). [D18]** The mass component improves c-rejection
   because charm hadrons have lower invariant mass than b hadrons. The
   hemisphere invariant mass is computable from available track 4-vectors
   (pmag, theta, phi available per track). **Cross-check: N-sigma tag
   (without mass component).**

6. **Working point:** Scan the tag discriminant to find the operating point
   that minimizes total uncertainty on R_b. The stability scan (required by
   conventions/extraction.md, validation check 3) verifies the result is flat
   across a wide range of working points. **Note:** the stability scan tests
   self-consistency (robustness to the working point choice) but does NOT
   test for absolute bias. A common bias (e.g., from wrong sigma_d0
   parameterization) would shift all working points equally and be invisible
   in the scan. The closure tests in Section 9.1 address absolute bias.

### 5.2 Approach B: BDT-Based Hemisphere Tagger

**Grounding:** Multiple discriminating variables available per track
(DATA_RECONNAISSANCE.md): d0, z0, pt, pmag, theta, nvdet, ntpc, nitc, weight.
Event-level variables: nChargedHadrons, Thrust, Sphericity, missP.

**MVA feasibility assessment:**

The critical question is: what are the training labels? Given [A1] (no MC
truth), we cannot train on MC truth flavour. Three viable alternatives:

1. **bFlag from data as proxy labels [D9]:** bFlag = 4 tags ~94% of data
   events. While its exact definition is unknown, it is clearly a b-tag
   (DATA_RECONNAISSANCE.md). Train the BDT on data with bFlag = 4 as signal
   and bFlag = -1 as background. Caveat: contamination of non-b events in
   bFlag = 4 biases the training labels, but the double-tag method's
   self-calibrating property absorbs this bias into the measured efficiency.

2. **Self-labelling from cut-based tag:** Apply a tight cut on Approach A's
   probability tag to define a high-purity b sample; use the anti-tagged
   sample as background. Train BDT on these proxy labels.

3. **Unsupervised / semi-supervised:** Use the negative d0 tail shape
   (resolution-only) vs positive tail (resolution + lifetime) as implicit
   labels — not a standard BDT training paradigm but could be explored.

**[D10] Attempt BDT training with bFlag proxy labels (option 1) and
self-labelling (option 2). If BDT performance does not exceed cut-based
by > 10% in efficiency at fixed purity, default to cut-based as primary
with BDT as cross-check. Document the comparison with quantitative metrics
(AUC, efficiency at 90% and 98% purity).**

**Label contamination diagnostic:** Scan the BDT working point and plot the
extracted R_b vs BDT cut. If the BDT working point scan shows a slope
> 1-sigma/range while the cut-based scan is flat, this is evidence of
label contamination (bFlag=4 labels contain non-b events that the BDT
learns to exploit). Document slope magnitude and significance. If slope
exceeds 2-sigma significance, revert to cut-based as primary. The
contamination fraction from the slope diagnostic also feeds into the
bFlag interpretation (Section 9.6).

**BDT input variables (all available per DATA_RECONNAISSANCE.md):**

Per-track:
- Signed impact parameter significance (d0/sigma_d0)
- |z0| (longitudinal impact parameter)
- Track p_T
- Track momentum (pmag)
- Number of VDET hits (nvdet)
- Number of TPC hits (ntpc)

Per-hemisphere (aggregated):
- Track multiplicity (nChargedHadrons in hemisphere)
- Sum of signed significances
- Maximum track significance
- Hemisphere invariant mass (from track 4-vectors)

**MVA-induced hemisphere correlations [L2]:** BDT inputs correlated with
event-level properties (total multiplicity, thrust) can inflate the
hemisphere correlation C_b. Following conventions/extraction.md pitfalls,
we will check C_b at the working point and remove inputs that cause C_b to
deviate significantly from 1.0.

### 5.3 Selection Approach Comparison Plan

Phase 3 will implement both approaches and compare:
- Tagging efficiency vs purity curves
- Data/MC agreement on discriminant distributions
- Hemisphere correlation C_b magnitude
- R_b stability scan
- Total uncertainty (statistical + systematic)

The approach with lower total uncertainty and acceptable C_b becomes primary;
the other becomes the cross-check.

---

## 6. A_FB^b Measurement Strategy

### 6.1 Event Selection and Thrust Axis Convention

1. passesAll = 1
2. |cos(theta_thrust)| < 0.9 (angular acceptance, following inspire_433746)
3. b-enriched sample: apply the b-tag from Section 5 at a purity optimized
   for A_FB^b sensitivity (looser than R_b to maximize statistics)

**Thrust axis sign convention:** The thrust axis is unsigned by construction.
"Forward" is defined as the hemisphere with cos(theta_thrust) > 0, i.e.,
toward the positive z-axis, which is the electron beam direction at LEP.
The beam direction is encoded in the event coordinate system (z-axis
parallel to e- beam). Phase 3 must verify that the coordinate system
convention is preserved in the ntuple by checking that the cos(theta_thrust)
distribution shows the expected 1 + cos^2(theta) shape symmetric about 0
(confirming the beam axis is the z-axis). If the beam direction is not
recoverable, A_FB^b cannot be measured.

### 6.2 Hemisphere Charge Construction

For each hemisphere, compute:

  Q_h(kappa) = sum_i q_i * |p_{L,i}|^kappa / sum_i |p_{L,i}|^kappa

where:
- sum runs over all charged tracks in the hemisphere (including those without
  VDET hits — jet charge uses all tracks, not just those with d0)
- q_i = track charge (available, values {-1, 0, +1}; tracks with charge = 0
  are excluded)
- p_{L,i} = longitudinal momentum w.r.t. thrust axis = pmag * cos(angle to
  thrust)
- Apply per-track weights from weight[] branch. **Phase 3 investigation:**
  determine how the weight branch enters the jet charge computation —
  whether as a multiplicative correction to q_i (modifying the charge) or
  to |p_{L,i}|^kappa (modifying the momentum weight). The weight branch
  has mean ~1.02 with range [0.074, 1.833] (DATA_RECONNAISSANCE.md);
  test both prescriptions and compare delta_b sensitivity.

**[D11] Include tracks without VDET hits in jet charge computation.** These
tracks have valid charge and momentum but no d0 measurement. Excluding them
would reduce charge separation.

### 6.3 Extraction Method

**Self-calibrating fit** (following inspire_433746, Section 4):

In b-tagged events, the observed charge asymmetry is:

  <Q_FB>(cos theta) = sum_q f_q * delta_q * A_FB^q * cos(theta)

where f_q is the fraction of flavour q in the tagged sample and delta_q is
the charge separation for flavour q. For a high-purity b tag:

  <Q_FB>(cos theta) ~ f_b * delta_b * A_FB^b * cos(theta)
                     + f_c * delta_c * A_FB^c * cos(theta)
                     + ...

The fit extracts A_FB^b and delta_b simultaneously by using multiple b-tag
purities (working points) and multiple kappa values:
- At high purity: f_b -> 1, directly sensitive to delta_b * A_FB^b
- At lower purity: background fractions constrain f_c, delta_c

**[D12] Fit A_FB^b in bins of cos(theta_thrust) using the self-calibrating
method.** Use 8-10 uniform bins in signed cos(theta) (the fit requires
signed cos(theta) for the linear term; |cos(theta)| is used only for the
angular acceptance cut at 0.9). Report chi2/ndf of the angular fit at each
configuration (bin count, kappa value, working point). Perform a bin-count
scan (6, 8, 10, 12 bins) to verify stability. Compare to a simple counting
method (N_F - N_B) / (N_F + N_B) as cross-check.

**[D12b] Governing fit implementation: four-quantity simultaneous fit
(following inspire_433746, Section 4).** In each bin of cos(theta) and
hemisphere b-tag window (purity interval), four quantities are measured
for each kappa value:

1. **Q_FB** — the mean forward-backward charge asymmetry
2. **delta** — the mean hemisphere charge difference (charge separation)
3. **e^h** — the hemisphere b-tag efficiency
4. **epsilon^e** — the event b-tag efficiency

These four observables are fitted simultaneously as a function of three
independent parameters:

- **delta_b** — the b-quark charge separation
- **epsilon^h_b** — the hemisphere b-tag efficiency for b quarks
- **sin^2(theta_eff)** — the effective weak mixing angle

The fit uses the method of Lagrange multipliers (inspire_433746, Section 4),
leaving one effective degree of freedom per bin to test Standard Model
consistency. The simultaneous fit of tagging efficiency and charge
separation from data is what makes the method self-calibrating: the
precise degree of degradation at high |cos(theta)| is observed and
fitted, enabling extension into regions where both hemisphere tagging
and charge measurement are degraded (inspire_433746, Section 4).

**sin^2(theta_eff) extraction:** sin^2(theta_eff) is a direct fit parameter
(not derived post-fit). The fit varies sin^2(theta_eff) by altering the
top quark mass used to compute electroweak radiative corrections, testing
the hypothesis that the data are consistent with the Standard Model at
the fitted sin^2(theta_eff). The pole asymmetry A_FB^{0,b} is then
derived from sin^2(theta_eff) via:

  A_FB^{0,b} = (3/4) * A_e * A_b

where A_e is computed from sin^2(theta_eff) assuming lepton universality
(A_e = 2*(1 - 4*sin^2(theta_eff)) / (1 + (1 - 4*sin^2(theta_eff))^2)).
This follows the ALEPH approach (inspire_433746, Section 7) where the
result is reported as sin^2(theta_eff) = 0.2330 +/- 0.0009, from which
A_FB^b = 0.0927 +/- 0.0039 +/- 0.0034 is derived.

**Alternative (cross-check): DELPHI five-event-category chi2 fit
(inspire_1660891, inspire_1661252).** This method fits five event-rate
observables — N (single-tagged forward), N_bar (single-tagged backward),
N^D (double-tagged unlike-sign forward), N^D_bar (double-tagged unlike-sign
backward), N^same (double-tagged like-sign) — as a function of A_FB^b,
the charge-assignment probability w_b, and normalization factors. This
approach uses a binary charge classification (quark vs antiquark hemisphere)
rather than the continuous hemisphere charge Q_h. If the primary four-
quantity fit encounters convergence issues, the DELPHI five-category
method provides a well-validated alternative. In this case, sin^2(theta_eff)
would be extracted by inverting A_FB^{0,b} = (3/4)*A_e*A_b, taking A_e
from the LEP/SLD combined value (hep-ex/0509008).

**[D12a] Angular binning uniformity across years.** Given the VDET change
between 1993 and 1994 (DATA_RECONNAISSANCE.md), per-year angular
acceptance may differ. Use the same binning for all years (uniform in
cos theta) but verify per-year fit quality (chi2/ndf). If any year shows
chi2/ndf > 2.0, investigate year-specific angular effects.

### 6.4 QED and QCD Corrections

To extract A_FB^{0,b} from the measured A_FB^b:

  A_FB^{0,b} = A_FB^b / (1 - delta_QCD - delta_QED)

where delta_QCD includes O(alpha_s) and O(alpha_s^2) QCD corrections, and
delta_QED accounts for initial-state radiation and gamma-Z interference.
Note: Section 2.2 defines the full correction as (1 - delta_QCD - delta_QED);
here delta_QCD and delta_QED are listed separately for clarity.
The standard value delta_QCD = 0.0356 +/- 0.0029 at sqrt(s) = M_Z is taken
from hep-ex/0509008, Section 5.5, which cites the primary theoretical
calculations by Altarelli et al. (Nucl. Phys. B356, 1991) and Ravindran
and van Neerven (Phys. Lett. B445, 1998) for the O(alpha_s) and
O(alpha_s^2) terms respectively. The QED correction delta_QED (initial-state
radiation, gamma exchange) is applied via the published correction factors
from the LEP EWWG (hep-ex/0509008, Section 5.4); it is small (~0.001) but
included for completeness.

---

## 7. Systematic Uncertainty Plan

### 7.1 Required Sources from conventions/extraction.md

#### Efficiency Modeling

| Source | Status | Plan |
|--------|--------|------|
| Tag/selection efficiency | Will implement | Vary sigma_d0 parameterization within calibration uncertainties; propagate to R_b via re-extraction |
| Efficiency correlation (C_b, C_c) | Will implement | **C_b determination without MC truth:** since [A1] prevents isolating bb events in MC by flavour, C_b will be estimated using a three-pronged approach: (a) **bFlag=4 proxy:** use bFlag=4 in data as a b-enriched subsample to compute the hemisphere-hemisphere tag correlation in data directly — note bFlag=4 at 94% is not b-enriched (see Section 9.6), so this prong is exploratory and may yield C_b for the full sample rather than b-only; (b) **geometric/kinematic estimation (primary):** compute hemisphere correlations from the full MC (all flavours) and correct for non-b contamination using the fitted f_b; (c) **published value with inflated uncertainty (fallback/validation):** the ALEPH published systematic from hemisphere correlations is delta(R_b) = 0.00050 (hep-ex/9609005, Table 1), corresponding to rho_bQQ with impact coefficient 0.45 on dR_b/R_b. For our simplified single-tag system, adopt a baseline C_b from the published ALEPH Q-tag self-correlation, inflated by a factor of 2x to account for our less constrained tag construction and the absence of per-hemisphere primary vertex reconstruction [D17]. Concretely: assign delta(R_b) from C_b = 0.00100 (2x the published 0.00050). C_b is varied as a single multiplicative factor (not decomposed by source) in the double-tag equations, with sub-components (geometric, kinematic, gluon radiation) checked via data-MC comparison of four correlation-inducing variables: **(1) cos(theta), (2) primary vertex error, (3) jet momentum, (4) y_3** (gluon radiation variable, from ktN2 jet tree — the Durham jet resolution at which 3->2 jets occurs; following hep-ex/9609005 Section "Hemisphere-hemisphere correlation uncertainties" which uses these four variables). The systematic contributions from the four correlation-inducing variables are combined linearly (not in quadrature) to account for correlations between the correlation sources, following hep-ex/9609005. |
| MC efficiency model | Will implement | Compare efficiencies from nominal MC vs reweighted MC (vary fragmentation parameters); limited by single MC sample [L1] |

#### Background Contamination

| Source | Status | Plan |
|--------|--------|------|
| Non-signal contamination (eps_c, eps_uds) | Will implement | Vary charm and light-flavour efficiencies within MC statistical uncertainties; propagate to R_b |
| Background composition | Will implement | Vary R_c within +/- 0.0030 (LEP combined uncertainty); vary gluon splitting rates g_bb and g_cc within published uncertainties |

#### MC Model Dependence

| Source | Status | Plan |
|--------|--------|------|
| Hadronization model | Will implement (limited) | Reweight MC b fragmentation function (Peterson vs Bowler-Lund); cannot compare generators (single MC sample) [L1]. Assign conservative systematic based on published variation from hep-ex/9609005 |
| Physics parameters | Will implement | Vary B hadron lifetimes, decay multiplicities, b fragmentation <x_E> within PDG uncertainties; propagate via MC reweighting |

#### Sample Composition

| Source | Status | Plan |
|--------|--------|------|
| Flavour composition | Will implement | Vary R_c, R_b (iteratively) in the extraction formula |
| Production fractions | Will implement | Vary B+/B0/Bs/Lambda_b production fractions within PDG uncertainties |
| Gluon splitting | Will implement | Vary g_bb = (0.251 +/- 0.063)% (LEP average, inspire_416138) and g_cc = (2.96 +/- 0.38)% (world average, hep-ex/0302003). Note: ALEPH alone measured g_bb = (0.26 +/- 0.04 +/- 0.09)% (hep-ex/9811047); DELPHI measured (0.22 +/- 0.10 +/- 0.08)% (inspire_1661963). Using the LEP average is more conservative. |

#### Additional Sources (from reference analyses)

| Source | Status | Plan |
|--------|--------|------|
| Detector simulation (tracking) | Will implement | d0 smearing study: smear MC d0 by data-MC resolution difference (negative tail comparison), re-extract R_b. Following inspire_433306 Section 7.1 |
| tau contamination | Will implement | Z -> tau+tau- events passing hadronic selection contaminate at ~0.3% level. Correct using published selection efficiency (inspire_367499) |
| Event selection bias | Will implement | Variation of passesAll subcuts; the ratio R_b has reduced sensitivity to selection efficiency if the selection is flavour-independent |
| QCD corrections (A_FB^b) | Will implement | Vary delta_QCD within +/- 0.0029; vary alpha_s within +/- 0.0012 |
| Charge separation model (A_FB^b) | Will implement | Compare kappa values; propagate MC modelling uncertainty on delta_b |
| Charm asymmetry (A_FB^b) | Will implement | Vary A_FB^c within LEP combined uncertainty +/- 0.0035 |

#### Sources Not Applicable

| Source | Reason |
|--------|--------|
| Luminosity | R_b is a ratio measurement; absolute luminosity cancels. A_FB^b is also luminosity-independent |
| Beam energy | All data at Z pole; beam energy uncertainty enters through QED corrections only, which are taken from published values |
| Jet energy scale | Analysis uses tracks, not calorimeter jets |

### 7.2 Calibration Independence

Per conventions/extraction.md, each calibration must come from an observable
independent of the primary result.

- **d0 resolution calibration** (sigma_d0 from negative tail): The negative
  d0 tail shape depends on detector resolution, not on b-hadron content or
  R_b. This is independent of the primary result.
- **Hemisphere correlation C_b** (from MC): C_b depends on detector geometry
  and QCD effects, not on R_b directly. However, it is derived from the same
  MC used for eps_c and eps_uds. The systematic on C_b is evaluated from
  data-MC comparison of correlation-inducing variables (cos theta, primary
  vertex error, jet momenta), providing partial independence.
- **Background efficiencies eps_c, eps_uds** (from MC): Not independently
  calibrated. **Justification for no charm control region:** a charm-enriched
  control region would require either D meson reconstruction (needs PID,
  unavailable [A5]) or a soft lifetime cut (charm hadrons have c*tau ~
  100-300 micron vs ~450 micron for b hadrons), but the soft cut produces a
  sample dominated by b contamination rather than a pure charm sample. The
  multi-working-point scan [D14] provides indirect sensitivity to eps_c:
  at loose working points where charm contamination is higher, the extracted
  R_b is more sensitive to eps_c, and consistency across working points
  constrains the eps_c range. **Concrete uncertainty range:** eps_c is
  assigned +/- 30% relative uncertainty, grounded in the following:
  (i) the published ALEPH Q-tag charm efficiency epsilon_cQ varies by
  a factor ~2-3x across working points (from hep-ex/9609005, where
  epsilon_cQ is one of two efficiencies taken from MC rather than fitted,
  indicating the difficulty of constraining it from data alone);
  (ii) the spread of published charm efficiencies across LEP experiments
  at comparable working points is ~20-40% (inspire_416138, Section 3.5,
  documenting common charm-sector uncertainties from lifetime, decay
  multiplicity, and fragmentation differences);
  (iii) our MC has no truth labels [A1], so the charm efficiency is
  estimated from all-flavour MC with contamination subtraction, adding
  ~10% MC statistical uncertainty on top of ~15-20% modelling uncertainty.
  The 30% covers the envelope of these three sources. Propagated
  as a systematic via re-extraction. This corresponds to an absolute
  uncertainty of ~0.002-0.005 on eps_c depending on working point.

### 7.3 Uncertainty Propagation Method

**[D13] Use toy-based uncertainty propagation (Poisson-fluctuate inputs,
repeat extraction, take RMS) as the primary method.** Analytical propagation
as cross-check. Following conventions/extraction.md recommendation for
extractions with correlated inputs.

### 7.4 A_FB^b-Specific Systematics

| Source | Plan |
|--------|------|
| **Angular dependence of b-tag efficiency** | The b-tag efficiency varies with |cos(theta)| due to reduced VDET hit coverage at forward angles (fewer silicon layers traversed), changing the effective b-purity f_b across the angular range. This is one of the dominant A_FB^b systematics in published analyses. **Mitigation:** parameterize eps_b(cos theta) from data using the double-tag method in angular bins; include the angular dependence in the self-calibrating fit. Systematic: vary the parameterization and propagate to A_FB^b. |
| Hemisphere charge modelling | Compare multiple kappa values; the spread is a measure of model dependence |
| Hemisphere charge correlations | Evaluate from MC; systematic from charge conservation and gluon radiation effects (inspire_1661115, Section on correlations) |
| b fragmentation effect on delta_b | Vary <x_E^b> and fragmentation function; propagate to delta_b |
| Thrust axis misalignment | Propagate angular resolution systematic via MC smearing |
| cos(theta) binning | Vary number of bins; compare fitted A_FB^b |

---

## 8. Precision Estimates

### 8.1 R_b Statistical Precision

From the double-tag method (inspire_416138):

  sigma(R_b)_stat ~ R_b / sqrt(N_tt) * (1 + background correction terms)

With ~2.87M events after passesAll, assuming b-tag efficiency eps_b ~ 30%
(conservative for a probability tag):
- N_t ~ 2 * 2.87M * 0.30 * 0.217 ~ 374k single-tagged hemispheres
- N_tt ~ 2.87M * 0.30^2 * 0.217 * 1.01 ~ 56k double-tagged events
- sigma(R_b)_stat ~ 0.217 / sqrt(56000) ~ 0.00092

This is comparable to the ALEPH published statistical uncertainty of 0.00087
(hep-ex/9609005), which used 4M events with a more sophisticated 5-tag system.
Our slightly larger statistical uncertainty is expected given fewer events
(3.05M vs 4.1M including 1991) and a simpler tagging system.

### 8.2 R_b Systematic Precision

The dominant systematics from hep-ex/9609005 with expected scaling for our
analysis:

| Source (hep-ex/9609005) | Published | Our scaling | Expected |
|-------------------------|-----------|-------------|----------|
| Detector simulation | 0.00050 | x1.5 (no d0 smearing from truth) | ~0.00075 |
| MC statistics | 0.00040 | x1.0 (similar MC size) | ~0.00040 |
| B physics | 0.00030 | x1.5 (fewer constraints on fragmentation) | ~0.00045 |
| Hemisphere correlations | 0.00050 | x2.0 (simpler tag, fewer handles on C_b) | ~0.00100 |
| Charm efficiency | 0.00030 | x1.5 (no charm control region) | ~0.00045 |
| **Total (quadrature)** | **0.0011** | | **~0.0015** |

Our expected systematic is conservatively 1.5-2x larger than the published
value, primarily due to:
- Single MC sample (cannot compare generators) [L1]
- Simplified tagging system (fewer constraints on backgrounds)
- Missing sigma_d0 requiring calibration [A3]
- No per-hemisphere primary vertex (pending [D17])

**Expected total: sigma(R_b) ~ 0.0009 (stat) +/- 0.0015-0.0020 (syst)**

This is ~2-3x the LEP combined uncertainty (0.00066) but comparable to
individual ALEPH results. The larger systematic is driven by our single MC
sample and simplified approach; the methodology differences are documented
and the published method is implemented as a cross-check where feasible.

### 8.3 A_FB^b Precision

From inspire_433746: A_FB^b = 0.0927 +/- 0.0039 (stat) +/- 0.0034 (syst)

**Derivation of statistical precision estimate:**

The statistical uncertainty on A_FB^b from counting is:
  sigma(A_FB^b)_stat ~ 1 / (delta_b * sqrt(N_tagged))

With ~2.87M events, b-tag efficiency eps_b ~ 30%, purity f_b ~ 90%,
acceptance |cos theta| < 0.9 (~90% of solid angle):
- N_tagged ~ 2.87M * 0.30 * 0.217 * 2 * 0.9 ~ 337k tagged hemispheres
- delta_b ~ 0.23 (typical for kappa = 0.5, from inspire_433746)
- sigma(A_FB^b)_stat ~ 1 / (0.23 * sqrt(337000)) ~ 0.0075

This simple counting estimate gives ~0.0075. However, the self-calibrating
fit uses information from the full angular distribution and multiple working
points/kappa values, which improves the precision. Published ALEPH
(inspire_433746) achieved 0.0039 with 4.1M events and kappa = {0.3-inf}.
Scaling by sqrt(4.1M/2.87M) for the reduced event count:
sigma ~ 0.0039 * sqrt(4.1/2.87) ~ 0.0047. Note: we use all five kappa
values [D5] (including kappa = infinity), matching the ALEPH kappa set,
so no additional kappa-count scaling is needed.

**Expected: sigma(A_FB^b)_stat ~ 0.005-0.007** (range from self-calibrating
fit improvement to simple counting). The lower bound (~0.0047) comes from
the direct ALEPH scaling; the upper bound (~0.0075) from simple counting.
The resolving power assessment uses the conservative end of this range.

**Expected total: sigma(A_FB^b) ~ 0.005-0.007 (stat) +/- 0.004-0.005 (syst)**

---

## 9. Mitigation Strategies for Phase 1 Constraints

### 9.1 [A1] No MC Truth Flavour Labels

**Impact:** Cannot calibrate tagging efficiency from MC truth. Cannot perform
traditional MC closure tests.

**Mitigation:**

1. **Double-tag self-calibration.** The double-tag method extracts eps_b
   directly from data (from N_tt / N_t ratio). This is the method's raison
   d'etre and why it was developed at LEP — specifically to avoid dependence
   on MC truth for efficiency calibration (inspire_416138, Section 2.2.1).

2. **Negative d0 tail calibration.** The negative signed impact parameter
   distribution arises purely from tracking resolution. By comparing
   the negative tail in data and MC, we calibrate the resolution function
   without needing truth labels (inspire_433306, Section 7.1). Any data-MC
   difference in the negative tail is used to smear the MC, ensuring the
   tagger response in MC matches data.

3. **bFlag as data-level proxy.** bFlag = 4 in data (94% of events) provides
   a pre-existing b-tag. While we build our own tagger, bFlag serves as an
   independent cross-check: comparing our tag output in bFlag=4 vs bFlag=-1
   subsamples validates tagger behaviour.

4. **Operating point stability as pseudo-closure.** Instead of comparing to
   MC truth, we scan the extracted R_b vs working point. A flat scan
   demonstrates the method is self-consistent. A slope would indicate bias
   from working-point-dependent background contamination.

5. **Meaningful closure tests (replacing tautological MC-split test).**
   A simple MC half-split test is an algebra check, not a closure test:
   both halves share the same generator, fragmentation, and detector model,
   so efficiencies derived from one half perfectly describe the other
   (conventions/extraction.md Pitfalls). Instead, the following closure
   tests are committed:

   (a) **Negative-d0 pseudo-data test:** Construct a pseudo-dataset from
   the negative-d0 tail only (zero-lifetime signal by construction).
   Extraction should return R_b consistent with 0 for the "b" component.
   A nonzero result indicates a bias in the resolution model.

   (b) **bFlag consistency test:** Compare tagger output distributions in
   bFlag=4 vs bFlag=-1 subsamples. The double-tag extraction in the
   bFlag=4 subsample (pre-tagged) should yield R_b consistent with the
   full-sample result if the tagger and bFlag are approximately independent.

   (c) **Artificial contamination injection:** Inject a known fraction of
   "light-flavour-like" events (drawn from the negative-d0 population) into
   the b-tagged sample. The shift in extracted R_b should match the
   analytically predicted shift within uncertainties.

   These are proxy closure tests, not traditional MC-split closure tests
   (which require truth labels). The ultimate validation of the analysis
   is comparison to published ALEPH values [REF1]-[REF3], which were
   obtained with the same data using the full methodology.

### 9.2 [A2] d0 Sentinel Fraction (~36%)

**Impact:** ~36% of tracks have d0 = -999 (no VDET hits), reducing the
effective sample for lifetime tagging.

**Mitigation:**

1. **Quality cut on nvdet > 0** removes sentinel tracks from the b-tag
   computation. These tracks still contribute to jet charge (they have valid
   charge and momentum).

2. **Expected efficiency reduction:** With ~64% of tracks having VDET hits,
   the b-tag efficiency is reduced but not catastrophically — displaced
   B hadron decay products tend to have VDET hits because they traverse
   the vertex detector. The efficiency loss is primarily for soft tracks
   from fragmentation.

3. **Track categories by VDET hits:** Following inspire_433306, treat tracks
   with 1 and 2 VDET hits separately when calibrating sigma_d0. This
   accounts for the different resolution classes. **Phase 3 action:**
   check the d0 sentinel fraction (~36% overall) per year. If the
   sentinel fraction varies significantly across years (e.g., due to
   VDET module damage/repair), this indicates year-dependent VDET
   coverage and must be accounted for in the per-year sigma_d0
   calibration.

### 9.3 [A3] sigma_d0 Not Stored

**Impact:** Cannot compute impact parameter significance directly.

**Mitigation:**

1. **Parameterize sigma_d0** from ALEPH detector performance:
   sigma_d0 = sqrt(A^2 + (B / (p * sin(theta)))^2)
   with A ~ 25 micron, B ~ 70 micron*GeV/c (from 537303 and ALEPH
   detector papers). The sin(theta) dependence is the standard form for
   the Rphi impact parameter d0 (see Section 5.1 and systematic in
   Section 7.1).

2. **Calibrate from negative tail:** The negative d0/sigma_d0 distribution
   should be Gaussian with width 1.0 if sigma_d0 is correctly estimated.
   Fit the width in bins of (nvdet, momentum, cos(theta)) and apply
   correction factors to the parameterization.

3. **Systematic assignment:** The residual uncertainty in sigma_d0 after
   calibration is propagated by varying the parameterization parameters
   (A, B) within the calibration uncertainties and re-extracting R_b.

### 9.4 [A4] MC 1994 Only

**Impact:** Cannot model year-dependent detector effects for 1992, 1993, 1995.

**Mitigation:**

1. **Per-year extraction.** Extract R_b and A_FB^b independently for each
   data-taking year. Consistency (chi2/ndf across years) validates the
   assumption that year-dependent effects are small or cancel in the ratio.

2. **Data-driven resolution calibration per year.** The negative d0 tail
   calibration (Section 9.3) is performed per year, capturing
   year-dependent resolution changes without MC. This implicitly absorbs
   beam spot position variations, which affect the effective d0 resolution
   and are therefore captured in the per-year sigma_d0 calibration.

3. **Conservative systematic.** Assign a systematic uncertainty from the
   spread of per-year results. If chi2/ndf > 2.0 for per-year consistency,
   investigate year-specific effects (VDET alignment, module status).

4. **MC normalization to 1994 data.** All MC comparisons are restricted to
   1994 data where year matching is exact. The full dataset result uses
   corrections derived from 1994 MC, with the per-year variation as a
   cross-check and systematic.

### 9.5 [A5] No Particle Identification (pid = -999)

**Impact:** Cannot identify leptons (no L tag), cannot identify kaons (no X
tag or charm tag). This eliminates 3 of the 5 ALEPH R_b tags from
hep-ex/9609005.

**Mitigation:**

1. **Lifetime-only tagging.** The impact parameter probability tag and mass
   tag do not require PID. These are the two most powerful tags in
   hep-ex/9609005 and form the basis of our approach.

2. **R_c from external input.** Without charm-specific tagging, R_c cannot
   be measured independently. Constrain to SM or LEP combined value [D6].

3. **Jet charge for A_FB^b.** The jet charge method does not require PID —
   it uses all track charges and momenta. This is unaffected by [A5].

### 9.6 [A6] bFlag Absent in MC

**Impact:** Cannot study bFlag behaviour in MC.

**Mitigation:**

1. **Build independent tagger.** Our lifetime-based tagger is built from d0
   and track properties available in both data and MC. bFlag is not used as
   the analysis tagger.

2. **bFlag as data-only cross-check.** Compare our tagger output in
   bFlag=4 vs bFlag=-1 data subsets. If our tagger and bFlag are correlated
   (expected), this validates our tagger against the pre-existing ALEPH
   classification.

   **Note on bFlag=4 interpretation:** bFlag=4 for 94% of events is too
   high a fraction to be a b-tag (R_b ~ 21.6%). It is more likely an event
   quality or selection flag (e.g., "passes hadronic event selection" or
   "good tracking quality") rather than a b-identification flag. Phase 3
   must investigate this by checking the correlation between bFlag and our
   b-tag output: if bFlag=4 events have the same b-tag distribution as the
   full sample, it is not a b-tag. See the bFlag decision tree in
   COMMITMENTS.md (validation tests) for the formal chi2 test and the
   implications for BDT training label selection [D9].

---

## 10. Backgrounds

### 10.1 Classification

| Background | Type | Fraction | Treatment |
|-----------|------|----------|-----------|
| Z -> cc | Irreducible | ~17% of hadronic Z | Charm tagging efficiency eps_c from MC; R_c constrained [D6]; propagate uncertainty |
| Z -> uu, dd, ss | Irreducible | ~61% of hadronic Z | Light-flavour efficiency eps_uds from MC; small after b-tag |
| Z -> tau+tau- | Reducible | ~0.3% of hadronic sample | Estimated from published selection efficiency (inspire_367499: 99.1%); subtract |
| g -> bb (gluon splitting) | Irreducible | ~0.26% of hadronic Z | Creates additional b hemispheres not from Z -> bb vertex; systematic from varying g_bb rate |
| g -> cc (gluon splitting) | Irreducible | ~2.96% of hadronic Z (world average, hep-ex/0302003) | Affects charm efficiency; systematic from varying g_cc rate |
| Non-hadronic (2-photon, etc.) | Instrumental | < 0.1% | Negligible after passesAll preselection |

### 10.2 Background Treatment in Double-Tag

The double-tag formalism explicitly accounts for charm and light-flavour
backgrounds through eps_c, eps_uds terms. Gluon splitting (g -> bb) is the
most subtle background: it creates events with b quarks in both hemispheres
from a non-bb primary vertex, inflating N_tt relative to the Z -> bb
expectation.

**Correct treatment (following hep-ex/0509008 Section 5.4 and
inspire_416138 Section 2.2.1):** Gluon splitting is NOT corrected by
direct subtraction from R_b. Instead, g -> bb enters through the modified
double-tag equations by redefining the effective uds efficiency:

  eps_uds(eff) = eps_uds(direct) + g_bb * eps_g

where eps_g is the tagging efficiency for gluon-splitting b quarks (lower
than direct Z -> bb because of softer kinematics). Similarly for the
double-tag equation:

  eps_uds^2(eff) = eps_uds^2(direct) + g_bb * eps_g^2

The gluon-splitting b quarks are folded into the uds background term
because they originate from light-quark or gluon events, not from Z -> bb.
The charm gluon splitting (g -> cc) is handled analogously:

  eps_uds(eff) += g_cc * eps_gc

The systematic uncertainty from g_bb is evaluated by varying
g_bb = (0.251 +/- 0.063)% (LEP average, inspire_416138 Section on gluon
splitting) in the modified double-tag equations and re-extracting R_b.
The net effect on R_b is ~0.0003 (from published analyses), but it enters
through the modified equations, not as an additive correction.

---

## 11. Reference Analysis Table

### 11.1 ALEPH R_b (hep-ex/9609005) [REF1]

| Property | Value |
|----------|-------|
| Result | R_b = 0.2158 +/- 0.0009 (stat) +/- 0.0011 (syst) |
| Dataset | ALEPH 1992-1995, ~4 million hadronic events |
| Method | Double-tag with 5 mutually exclusive hemisphere tags (Q, S, L, X, uds) |
| Key choices | 3D impact parameter + mass tag for Q tag; hemisphere primary vertex reconstruction |
| MC sample size | Full ALEPH MC production (not quantified in paper) |
| Systematic program | Detector simulation (0.00050), MC stats (0.00040), B physics (0.00030), hemisphere correlations (0.00050), charm efficiency (0.00030) |
| Key difference from us | 5-tag system vs our 1-2 tag system; full PID for L and X tags; full MC truth for efficiency studies |

### 11.2 ALEPH R_b precise (inspire_433306) [REF2]

| Property | Value |
|----------|-------|
| Result | R_b = 0.2159 +/- 0.0009 (stat) +/- 0.0011 (syst) |
| Method | Combined impact parameter + mass tag; negative d0 tail for resolution calibration |
| Key technique | Hemisphere-by-hemisphere primary vertex; d0 smearing to match data-MC |
| MC sample size | Full ALEPH MC production (not quantified in paper; estimated ~10M events from typical LEP MC campaigns) |
| Key difference from us | Access to full MC truth for correlation studies; more sophisticated resolution calibration |

### 11.3 ALEPH A_FB^b (inspire_433746) [REF3]

| Property | Value |
|----------|-------|
| Result | A_FB^b = 0.0927 +/- 0.0039 (stat) +/- 0.0034 (syst) |
| sin^2(theta_eff) | 0.2330 +/- 0.0009 |
| Dataset | ALEPH 1991-1995, ~4.1 million hadronic events |
| Method | Hemisphere charge with lifetime tag; kappa = {0.3, 0.5, 1.0, 2.0, infinity} |
| Key choices | Self-calibrating fit; angular acceptance |cos theta| < 0.9 |
| Key difference from us | Includes 1991 data; full MC for charge separation modelling; five kappa values including infinity |

### 11.4 LEP/SLD Combined (hep-ex/0509008) [REF4]

| Property | Value |
|----------|-------|
| R_b | 0.21629 +/- 0.00066 |
| R_c | 0.1721 +/- 0.0030 |
| A_FB^{0,b} | 0.0992 +/- 0.0016 |
| SM predictions | R_b^SM = 0.21578, R_c^SM = 0.17223, A_FB^{0,b}_SM = 0.1032 |
| Method | Weighted average of ALEPH, DELPHI, L3, OPAL, SLD |
| Key difference | Combination of all experiments; our single-experiment measurement will have larger uncertainties |

### 11.5 DELPHI R_b (inspire_1661836) [REF5]

| Property | Value |
|----------|-------|
| Result | R_b = 0.21625 +/- 0.00067 (stat) +/- 0.00061 (syst) |
| Method | Enhanced impact parameter tag + multivariate analysis |
| Key difference | Different detector; provides independent cross-experiment validation target |

### 11.6 Method Parity Assessment

The ALEPH reference (hep-ex/9609005) used a 5-tag system with 20 measured
quantities fitted simultaneously. Our simplified 1-2 tag approach is less
constraining. **[D14] Implement the multi-working-point version (scan across
3-5 working points, treating each as a quasi-independent tag) to partially
recover the constraining power of the multi-tag approach. This is the
closest feasible approximation to the published method given our constraints
[A5].** The published 5-tag result serves as the primary validation target.

---

## 12. Flagship Figures

**[D15] The following ~6 flagship figures represent the measurement in a
publication:**

1. **R_b operating point stability scan.** Extracted R_b vs b-tag working
   point, showing the flat plateau region. Published ALEPH value overlaid
   as horizontal band. (Tests method robustness.)

2. **A_FB^b angular distribution.** <Q_FB> vs cos(theta_thrust) in the
   b-tagged sample, with fitted linear function. Published ALEPH result
   overlaid. (The money plot for the asymmetry.)

3. **Impact parameter significance distribution.** Signed d0/sigma_d0 for
   data and MC, showing the resolution-dominated negative tail and the
   lifetime-enriched positive tail. Logarithmic y-axis. (Validates the
   core analysis variable.)

4. **Double-tag fraction vs single-tag fraction.** f_d vs f_s at multiple
   working points, with the double-tag prediction curve for different R_b
   values and 1-sigma uncertainty band on the prediction.
   (Visualizes the self-calibrating extraction.)

5. **Systematic uncertainty breakdown.** Horizontal bar chart showing each
   systematic source's contribution to total R_b uncertainty. (Required for
   any precision measurement.)

6. **Per-year stability.** R_b (and A_FB^b) extracted per year, with
   combined result and chi2/ndf. (Demonstrates temporal consistency and
   addresses [A4].)

7. **A_FB^b kappa consistency.** A_FB^b extracted at each kappa value
   {0.3, 0.5, 1.0, 2.0, infinity}, plotted with combined result and
   chi2/ndf. (Tests charge separation model independence — a key cross-
   check since each kappa weights fragmentation differently.)

**Supporting figures (not flagship but required for review):**
- P_hem tagger discriminant: data vs MC, log scale (validates tagger
  output, not just the input d0/sigma_d0)
- delta_b vs kappa (charge separation as function of momentum weighting)

---

## 13. Correction Strategy

### 13.1 R_b Corrections

The double-tag extraction gives R_b at the detector level. Corrections needed:

1. **Event selection bias:** If the hadronic event selection efficiency
   differs between flavours, R_b must be corrected. The selection is
   primarily based on multiplicity and total energy, with weak flavour
   dependence. Correction from MC (~0.1%).

2. **Tau contamination:** Z -> tau+tau- events passing the hadronic
   selection contribute ~0.3%. Correct using published efficiency.

3. **QED corrections:** To obtain R_b^0 from the measured ratio, correct for
   photon exchange and gamma-Z interference using LEP EWWG prescription
   (~0.0003).

4. **Gluon splitting:** Fold g -> bb into the modified double-tag equations
   via effective uds efficiency, as described in Section 10.2.

### 13.2 A_FB^b Corrections

1. **QCD correction:** delta_QCD = 0.0356 +/- 0.0029 (hep-ex/0509008)
2. **QED correction:** ISR, photon exchange from published tables
3. **Angular acceptance:** The |cos theta| < 0.9 cut is corrected analytically

---

## 14. Theory Predictions for Comparison

| Observable | SM Prediction | Source |
|------------|--------------|--------|
| R_b^0 | 0.21578 | hep-ex/0509008 |
| R_c^0 | 0.17223 | hep-ex/0509008 |
| A_FB^{0,b} | 0.1032 | hep-ex/0509008 |
| sin^2(theta_eff) | 0.23149 | hep-ex/0509008 (global fit) |

**[D16] Compare all results to SM predictions AND to published ALEPH and LEP
combined measurements. Report pulls (deviation / uncertainty) for each.**

---

## 15. Constraint, Limitation, and Decision Labels

### Constraints [A] (data/MC properties restricting methodology)

- **[A1]** No MC truth flavour labels
- **[A2]** ~36% d0 sentinel values (tracks without VDET hits)
- **[A3]** sigma_d0 not stored; must be parameterized and calibrated
- **[A4]** MC 1994 only
- **[A5]** No particle identification (pid = -999)
- **[A6]** bFlag absent in MC

### Limitations [L] (features weakening the result)

- **[L1]** Single MC sample (cannot compare generators)
- **[L2]** MVA-induced hemisphere correlations may inflate C_b
- **[L3]** Simplified tag system vs published 5-tag system
- **[L4]** Missing 1991 data (~249k events)

### Decisions [D] (deliberate choices with alternatives)

- **[D1]** Observable definitions follow LEP EWWG standard (hep-ex/0509008)
- **[D2]** Double-tag hemisphere counting for R_b
- **[D3]** Simplified two-tag system rather than full 5-tag
- **[D4]** Hemisphere jet charge for A_FB^b
- **[D5]** kappa = {0.3, 0.5, 1.0, 2.0, infinity} for jet charge
- **[D6]** R_c as constrained parameter, not independently measured
- **[D7]** Calibrate sigma_d0 from negative d0 tail
- **[D8]** Primary: probability tag P_hem; cross-check: N-sigma tag
- **[D9]** BDT training with bFlag proxy labels
- **[D10]** BDT vs cut-based comparison with quantitative metrics
- **[D11]** Include non-VDET tracks in jet charge
- **[D12]** Self-calibrating fit for A_FB^b in cos(theta) bins
- **[D13]** Toy-based uncertainty propagation as primary method
- **[D14]** Multi-working-point extraction for method parity
- **[D15]** Six flagship figures defined (plus F7 kappa comparison)
- **[D16]** Compare all results to SM and published measurements
- **[D17]** Primary vertex definition: investigate d0 reference point at Phase 3
- **[D18]** Approach A includes combined probability-mass tag
- **[D12b]** Four-quantity simultaneous fit for A_FB^b (inspire_433746); DELPHI five-category chi2 as cross-check
- **[D19]** Phase 3 gate: d0 sign convention validation (blocking)

---

## 16. Code Reference

Phase 3 will implement the analysis in the following script structure:
- `phase3_selection/src/build_tagger.py` — b-tag construction
- `phase3_selection/src/compute_sigma_d0.py` — resolution parameterization
- `phase3_selection/src/hemisphere_charge.py` — jet charge computation
- `phase3_selection/src/compare_approaches.py` — Approach A vs B comparison
- `phase4_inference/src/extract_Rb.py` — double-tag extraction
- `phase4_inference/src/extract_AFBb.py` — A_FB^b extraction
- `phase4_inference/src/systematics.py` — systematic evaluation

---

## 17. Strategy Update — REGRESS(4a) Addendum

Date: 2026-04-03 | Trigger: Human gate REGRESS(4a) at Doc 4b

### 17.1 Root Cause

Post-mortem investigations at Doc 4b found superior methods that were
relegated to appendices instead of being the primary analysis:

1. **3-tag system** (tight/loose/anti-b) gives R_b = 0.217-0.222 on 10% data
   vs the 2-tag system which returned R_b = 0.310 (biased by eps_c > eps_b).
2. **Purity-corrected A_FB^b** = 0.074 +/- 0.031 at kappa=2.0 vs the naive
   extraction which gave A_FB^b ~ 0.009 (suppressed by low b-purity).
3. **BDT tagging** achieved AUC = 0.99, characterizing well as an alternative.
4. **eps_uds from anti-tag** provides a direct data constraint that was
   previously unconstrained (100% uncertainty).

### 17.2 Updated Primary Methods

**[D2-REVISED] PRIMARY R_b: 3-tag system (tight/loose/anti-b hemispheres).**

Replaces the 2-tag double-tag method as primary. The 3-tag system defines
three non-overlapping hemisphere categories based on combined tag score:
- Tight: score > thr_tight (b-enriched, eps_b > eps_c > eps_uds)
- Loose: thr_loose < score <= thr_tight (b+c enriched)
- Anti: score <= thr_loose (uds-enriched, eps_uds_anti ~ 0.62)

This provides 3 single-hemisphere + 6 double-tag = 9 observables to
constrain 6 independent efficiency parameters, making the system
overconstrained. Key advantages over 2-tag:
- eps_uds constrained from anti-tag data (not floating with 50-100% unc)
- eps_c constrained from 3-tag fit (10% variation vs old 30%)
- Stability testable across 8+ threshold configurations
- Closure test pulls within +/- 1 sigma

The original 2-tag method is retained as a cross-check.

**[D4-REVISED] PRIMARY A_FB^b: Purity-corrected extraction.**

Replaces the naive slope/sigma(Q_h) extraction. Uses:
- Published ALEPH delta_b values (hep-ex/0509008 Table 12)
- MC-calibrated flavour fractions (f_b, f_c, f_uds) from 3-tag system
- Charm asymmetry subtraction: A_FB^c contribution removed explicitly

The governing formula:
  A_FB^b = (slope - f_c * delta_c * A_FB^c) / (f_b * delta_b)

The self-calibrating fit across WPs remains as cross-check.

**[D10-REVISED] BDT as characterized alternative tagger.**

The BDT (AUC 0.99) is documented as a fully characterized alternative
but not the primary tagger due to label contamination concerns with
bFlag proxy labels. Cut-based remains primary for transparency.

### 17.3 Updated Systematic Treatment

| Source | Old treatment | New treatment |
|--------|--------------|---------------|
| eps_c | 30% relative (arbitrary) | 10% relative (3-tag constraint) |
| eps_uds | 50-100% (unconstrained) | 5% relative (anti-tag data) |
| C_b | WP 5.0 value for all WPs | Per-WP from correlation_results.json |
| Solver failures | "solver fails at +30% eps_c" | No failures (3-tag overconstrained) |

### 17.4 Phase 4a Code Reference (Regression)

- `phase4_inference/4a_expected/src/three_tag_rb_extraction.py` — 3-tag R_b
- `phase4_inference/4a_expected/src/purity_corrected_afb.py` — A_FB^b
- `phase4_inference/4a_expected/src/systematics_v2.py` — updated systematics
- `phase4_inference/4a_expected/src/write_results_json_v2.py` — results
- `phase4_inference/4a_expected/src/plot_phase4a_v2.py` — figures
