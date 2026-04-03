# Physics Review: Phase 2 Strategy — R_b, R_c, A_FB^b

Reviewer: andrzej_e80c | Date: 2026-04-02

---

## Overall Assessment

This is a well-constructed strategy that correctly identifies the double-tag
method as the natural approach for R_b given the absence of MC truth labels,
and the hemisphere jet charge method as the standard technique for A_FB^b.
The document demonstrates thorough engagement with the published ALEPH
literature and the LEP EWWG combination. The constraint/limitation/decision
labelling is exemplary. The systematic plan is comprehensive and grounded in
reference analyses.

**Would I approve this strategy for my group?** Yes, with the findings below
addressed. The core physics is sound, the method choices are well justified,
and the mitigation strategies for missing truth labels are credible. The
findings below are refinements, not fundamental objections.

---

## Findings

### (A) Must Resolve

**A1. The gluon splitting correction formula in Section 10.2 is wrong.**

The document writes:

> R_b(corrected) = R_b(measured) - g_bb * (eps_g / eps_b)^2

This is not correct. The gluon splitting g -> bb creates additional
double-tagged events from non-Z->bb events. The correction to R_b is not
simply subtractive with an (eps_g/eps_b)^2 factor. In the double-tag
formalism, gluon splitting modifies both the single-tag and double-tag
fractions because a g->bb event in a light-quark Z decay contributes
b-tagged hemispheres to the "uds" category. The standard treatment
(hep-ex/9609005, Section 7; hep-ex/0509008, Section 5.4) parameterizes
g_bb as a rate and folds it into the efficiency equations:

  eps_uds(effective) = eps_uds(direct) + g_bb * eps_g

and similarly for the double-tag correlation. The correction enters as a
modification to eps_uds and C_uds, not as a simple subtraction from R_b.
Getting this wrong would bias R_b by O(0.001), which is comparable to the
total systematic. Rewrite Section 10.2 to use the correct formalism from
the references.

**A2. The A_FB^b extraction formula (Section 6.3, Eq. for <Q_FB>) is
incomplete and potentially misleading.**

The document writes:

> <Q_FB>(cos theta) = sum_q f_q * delta_q * A_FB^q * cos(theta)

This is the expectation value of Q_FB at a given cos(theta) for a
perfectly efficient and unbiased sample. But the actual observable is the
*distribution* of Q_FB, not its mean, and the extraction must account for:

1. The dilution from charge misassignment (folded into delta_q, OK)
2. The b-tag purity varying with cos(theta) if the tag efficiency has
   angular dependence (through the thrust axis quality)
3. The acceptance function, which is NOT just |cos theta| < 0.9 — the
   effective acceptance depends on the tag efficiency at each angle

The self-calibrating method of inspire_433746 handles these by fitting
in bins and floating the normalization. But the strategy document does not
make clear that the angular dependence of the tag efficiency must be
measured or parameterized. If the tag efficiency drops at high |cos theta|
(which it will, because tracks at high |cos theta| have fewer VDET hits),
the effective f_b varies across the cos(theta) range, and ignoring this
introduces a bias in A_FB^b.

Add an explicit item to the systematic plan for the angular dependence of
the b-tag efficiency and its effect on A_FB^b. This is not optional — it
is one of the dominant systematics in the published analysis.

---

### (B) Should Address

**B1. The R_c "constrained parameter" strategy [D6] needs a clearer
treatment of its impact on R_b.**

The strategy correctly notes that R_c cannot be independently measured
without charm-specific tags, and proposes constraining R_c to the SM value.
But the sensitivity of R_b to R_c is significant: from the double-tag
equations, dR_b/dR_c ~ -(eps_c - eps_uds)/(eps_b - eps_uds). For typical
efficiencies, a shift of 0.003 in R_c (the LEP combined uncertainty)
produces a shift of ~0.0003-0.0005 in R_b. The strategy lists "Vary R_c
within +/- 0.0030" in the systematic plan but does not estimate the
resulting systematic on R_b numerically. This estimate should be included
in Section 8 (Precision Estimates) to verify it is not a dominant
systematic.

The cross-check of floating R_c (strategy item 2 under Section 4.3) is
valuable but the document should state what sensitivity is expected. With
two working points, the system has limited resolving power for both R_b
and R_c simultaneously. Be explicit about expected R_c uncertainty from
the float — if it is O(0.05), the float is not a meaningful cross-check.

**B2. The hemisphere correlation C_b is underemphasized given its
importance.**

The hemisphere correlation was historically one of the largest systematics
on R_b (0.00050 in hep-ex/9609005). The strategy mentions it in the
systematic table and notes the MVA correlation concern [L2], but does
not describe how C_b will actually be *measured* or bounded. "Evaluate
C_b from MC" is stated, but with no MC truth labels, how is C_b
determined from MC? Without truth labels, one cannot isolate bb events in
MC to compute the hemisphere correlation for b quarks specifically.

This is a genuine difficulty. The strategy needs to address it directly:
either (a) use the bFlag=4 subsample in data as a proxy for bb events
and measure the correlation directly, or (b) estimate C_b from the
geometric and kinematic properties that drive it (primary vertex sharing,
hard gluon radiation changing both hemispheres), or (c) adopt the
published value from the reference analysis with an inflated uncertainty.
The current text implies MC truth is available for this calculation when
it is not.

**B3. The precision estimates for A_FB^b (Section 8.3) are too vague.**

The R_b precision estimate (Section 8.1) shows a clear derivation from
event counts and efficiency assumptions. The A_FB^b estimate just says
"sigma ~ 0.004-0.005 (stat)" without showing the calculation. The
statistical uncertainty on A_FB^b from a counting measurement is:

  sigma(A_FB^b) ~ 1 / (delta_b * sqrt(N_b))

where N_b is the number of b-tagged events and delta_b is the charge
separation (~0.2-0.3 depending on kappa). With N_b ~ 374k (from the
single-tag estimate) and delta_b ~ 0.25:

  sigma ~ 1 / (0.25 * sqrt(374000)) ~ 0.0065

This is larger than the quoted 0.004-0.005. The self-calibrating fit
uses multiple purities and kappa values, which improves the precision,
but the strategy should show this calculation explicitly. If our expected
statistical precision is genuinely 0.005-0.007, this is 1.5-2x worse
than the published 0.0039, and the resolving power for sin^2(theta_eff)
should be re-evaluated.

**B4. The d0 resolution parameterization (Section 5.1, item 3) uses
sin^{3/2}(theta), but the standard ALEPH parameterization uses
sin^{5/2}(theta) for the multiple scattering term.**

The standard tracking resolution formula for the transverse impact
parameter in a solenoidal field is:

  sigma_d0 = sqrt(A^2 + (B / (p * sin^{alpha}(theta)))^2)

where alpha depends on the specific detector geometry and the quantity
being measured. For ALEPH specifically, the exponent on sin(theta) in the
multiple scattering term for d0 is closer to 5/2 than 3/2 because d0 is
a transverse quantity and the projected path length in silicon scales
differently from the 3D path length. The negative-tail calibration will
correct for this, but starting with a wrong functional form means the
calibration corrections will be larger and more momentum-dependent than
necessary, potentially introducing systematic biases.

Verify the exponent against the ALEPH detector performance papers
(specifically the ALEPH detector paper, NIM A 294 (1990) 121, and
updates). Use the literature value as the starting point for the
parameterization, then let the negative-tail calibration absorb residual
differences.

**B5. No discussion of the primary vertex reconstruction.**

The signed impact parameter is computed relative to the primary vertex.
The primary vertex position and its uncertainty directly affect d0 and
therefore the tagger performance. The strategy does not mention how the
primary vertex is determined. Key questions:

- Is the primary vertex stored in the ntuple, or must it be reconstructed?
- Is a per-event primary vertex used, or a run-average beam spot?
- Does the primary vertex reconstruction include the tracks being tested
  (creating a bias — the "track-in-vertex" problem)?

The published ALEPH analyses explicitly address the "track-in-vertex"
bias by excluding the track under test from the vertex fit
(inspire_433306). If the stored d0 is computed relative to a vertex that
includes the track, the signed impact parameter significance is biased
toward zero for displaced tracks, reducing tagging power. This needs to
be understood from the Phase 1 data reconnaissance.

**B6. The strategy does not address the thrust axis sign convention for
A_FB^b.**

The thrust axis defines the forward/backward hemispheres but is unsigned
(thrust axis and its negative give the same thrust value). A convention
must be chosen to define "forward" (toward the electron beam) vs
"backward." If the beam direction is not stored in the ntuple, the
strategy must explain how it is recovered. The published ALEPH analysis
(inspire_433746) uses the known beam crossing geometry. This is a
prerequisite for any A_FB^b measurement and should be explicitly addressed.

---

### (C) Suggestions

**C1. Consider a mass tag as a complement to the probability tag.**

The strategy mentions the "Q tag equivalent" but focuses on the impact
parameter probability tag. The hemisphere invariant mass (from track
4-vectors) is a powerful b-tag variable because B hadons produce higher
invariant mass vertices than charm or light flavour. A combined
probability + mass tag was used in the published ALEPH analyses and would
improve purity. This is listed as a BDT input (Section 5.2) but could
also be used in the cut-based approach as a second discriminant for the
multi-working-point strategy [D14].

**C2. For the per-year extraction (Section 9.4, mitigation 1), define
a priori what chi2/ndf threshold triggers investigation.**

"If chi2/ndf >> 1, investigate" is vague. Suggest chi2/ndf > 2.0 (for 4
years, p < 0.1) as the threshold for mandatory investigation and
chi2/ndf > 1.5 as a warning.

**C3. The flagship figures list (Section 12) is good but should include a
charge separation (delta_b) vs kappa plot.**

This is a key validation figure for A_FB^b — it shows the analysis is
measuring a real physical quantity (charge separation tracks the expected
kappa dependence) and provides an internal consistency check. The published
ALEPH analysis prominently features this plot.

**C4. The QCD correction delta_QCD = 0.0356 (Section 6.4) should be
cross-checked against the theoretical calculation.**

The strategy cites hep-ex/0509008 for this value, which is an
experimental combination paper, not a theory calculation. The primary
source is the QCD calculation by Djouadi, Kuhn, and Zerwas (and updates).
Citing the primary theoretical source would strengthen the analysis and
allow a proper uncertainty assessment.

---

## Summary of Findings

| ID | Category | Summary |
|----|----------|---------|
| A1 | A | Gluon splitting correction formula is wrong |
| A2 | A | A_FB^b extraction missing angular dependence of tag efficiency |
| B1 | B | R_c constraint impact on R_b not quantified |
| B2 | B | C_b measurement strategy unclear without MC truth |
| B3 | B | A_FB^b statistical precision estimate not derived |
| B4 | B | d0 resolution sin^{3/2} vs sin^{5/2} exponent |
| B5 | B | Primary vertex reconstruction not discussed |
| B6 | B | Thrust axis sign convention for A_FB^b not addressed |
| C1 | C | Consider mass tag for cut-based approach |
| C2 | C | Define chi2/ndf threshold for per-year consistency |
| C3 | C | Add delta_b vs kappa to flagship figures |
| C4 | C | Cite primary QCD theory source for delta_QCD |

---

## Verdict

**ITERATE.** Two Category A findings must be resolved (the gluon splitting
formula and the missing angular dependence treatment in A_FB^b). The six
Category B findings should also be addressed before this strategy can be
considered a reliable foundation for the measurement.

The strategy is fundamentally sound — the physics choices are correct and
the constraint mitigations are credible. But a strategy document with a
wrong formula and a missing dominant systematic source cannot be approved
as-is. Fix these and the strategy is ready.
