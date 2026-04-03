# Physics Review: AN Doc 4a v2

**Reviewer:** gunnar_8836 (physics reviewer)
**Document:** ANALYSIS_NOTE_doc4a_v2.pdf (52 pages)
**Date:** 2026-04-02
**Classification:** B

---

## Overall Assessment

This is a well-structured, honest, and impressively thorough analysis note
for an expected-results (MC pseudo-data) phase. The document is transparent
about its limitations, provides quantitative decomposition of precision
gaps relative to published ALEPH, and establishes a credible analysis
infrastructure. The v2 revision addressed many issues from the v1 review
cycle (change log documents ~25 fixes).

However, the document does not yet constitute a publishable measurement.
At Phase 4a this is expected -- the results are self-consistency diagnostics
on MC, not physics. The critical question is whether the infrastructure is
sound enough to produce correct results on data. My assessment is: mostly
yes for A_FB^b, uncertain for R_b due to the circular calibration and the
single-working-point fragility.

**Classification: B** -- the infrastructure is validated for A_FB^b and the
document is editorially strong, but several physics concerns (detailed
below) must be addressed before proceeding to data. None are showstoppers
requiring regression, but they require attention at Phase 4b.

---

## Mandatory Checks

### Figure Inspection

**Figure 1 (cutflow):** Clean. Data/MC agreement confirmed at ~94%
pre-selection efficiency. No issues.

**Figure 2 (event-level data/MC):** All four panels (thrust, cos_theta,
N_ch, sphericity) show agreement within 5%. Pull distributions are
centered on zero with no systematic trends. The cos_theta distribution
correctly shows the 1 + cos^2(theta) shape. PASS.

**Figure 3 (track-level data/MC):** The p_T distribution shows good
agreement over three decades. The d_0 distribution shows known ~10%
resolution difference in the tails (data wider than MC), which is
addressed by the sigma_d0 calibration. The d_0 pull panel has some
>2-sigma pulls at large |d_0| but these are in the tail region where
the calibration corrects. Acceptable -- the disagreement is diagnosed
and corrected downstream.

**Figures 4-6 (Phase 1 data/MC):** These are 5000-event survey plots
with large statistical fluctuations. They serve their purpose as
reconnaissance. No physics concerns.

**Figure 7 (sigma_d0 calibration):** Scale factors range 1.3-7.6.
The high-scale-factor bins (>5) are flagged and investigated (Section
4.1). The investigation is satisfactory -- these are low-momentum
1-VDET tracks that contribute little to the tag. However, I note
the figure x-axis labels are nearly illegible at this resolution.
**(C) Suggestion:** improve x-axis label readability.

**Figure 8 (signed impact parameter validation):** The positive/negative
tail ratio of 3.34 (data) vs 3.62 (MC) demonstrates the sign convention
works. The "Gate: PASS" annotation is clear. PASS.

**Figures 9-10 (tagging variables):** Combined tag and hemisphere
probability show good data/MC agreement. The displaced-track mass
distribution shows the expected b-hadron peak above 1.8 GeV/c^2.
Pull panels are clean. PASS.

**Figure 11 (calibrated efficiencies):** epsilon_b, epsilon_c, epsilon_uds
all decrease monotonically with working point as expected. The large
epsilon_c (0.43-0.62) is physically understood (charm lifetime). No
valid solutions below WP 7 -- this is a structural limitation, not a
bug. PASS.

**Figure 12 (hemisphere correlation C_b):** C_b = 1.2-1.5 vs published
~1.01. The inflation is quantitatively decomposed (shared vertex ~0.30,
gluon radiation ~0.15, resolution ~0.05). Data/MC agree to ~0.01.
The physics explanation is sound -- the open data format stores d_0
relative to a global event vertex, not a per-hemisphere vertex. PASS.

**Figure 13 (systematic breakdown):** The epsilon_uds systematic
dominates at 99.5% of the budget, making all other sources invisible.
The logarithmic scale is appropriate. The annotation correctly identifies
this as a structural issue. PASS.

**Figure 14 (kappa consistency):** chi^2/ndf = 0.71/4 (p = 0.95). All
kappa values consistent with zero asymmetry on symmetric MC. The ALEPH
band is shown for reference. PASS.

**Figure 15 (Phase 3 closure diagnostics):** Three-panel diagnostic
is clear. Mirrored significance correctly gives R_b = 0. bFlag
discrimination is confirmed. Contamination injection shows directional
agreement (ratio 2.14). PASS.

**Figure 16 (R_b stability scan):** Only WP 10.0 yields a valid
extraction. This is a serious diagnostic -- the operating point
stability requirement fails. The document is transparent about this.
See Finding A1.

**Figure 17 (Q_FB vs cos_theta):** The fitted slopes are consistent with
zero on symmetric MC. The intercept is visibly non-zero (~-0.003 to
-0.005), correctly handled by the intercept-inclusive model. chi^2/ndf =
31.9/8 at kappa = 0.5 -- this is still large (p ~ 10^-4). See Finding B1.

**Figure 18 (f_d vs f_s diagnostic):** Creative and physically
informative. The data trajectory in the (f_s, f_d) plane with R_b
prediction curves demonstrates the constraining power of the method.
The caveat note about varying efficiencies is important. PASS.

**Figures 19-20 (Appendix D.1):** |d_0| and track weight data/MC
comparisons. Clean agreement. PASS.

**Figures 21-22 (Appendix D.2):** Q_FB data/MC at all five kappa values.
Good agreement maintained across all kappa. PASS.

**Figure 23 (Phase 3 operating point scan):** Shows the uncalibrated
extraction where R_b is systematically too high (0.5-1.0). The note
correctly explains this is expected before calibration. PASS.

**Figure 24 (Phase 4a closure tests):** Independent closure at WP 9.0
gives pull = 1.93. Corrupted-correction sensitivity shows 4/6 sensitive.
PASS.

### Narrative Consistency Check

The early data/MC comparisons (Figures 2-3) show generally good agreement
with a known ~10% resolution difference in d_0. This resolution difference
is corrected by the sigma_d0 calibration (Figure 7). The flow from raw
d_0 disagreement to calibrated significance distributions to final
extraction is logically consistent. No "broken journey, perfect
destination" problem.

The R_b result (0.280 vs input 0.216) has a 0.064 residual bias from
the circular calibration, which is quantitatively explained and does
not pretend to be a good result. The A_FB^b result (~0 on symmetric MC)
is correctly obtained. The narrative is consistent.

### Suspiciously Good Agreement Check

Not applicable -- the results are not suspiciously good. R_b has a
known 0.064 bias. The chi^2/ndf for the A_FB^b fit is 26-34/8, which
is too high rather than too low. The closure test at WP 10.0 is
INFEASIBLE. This is an honest document.

### Statistical Methodology Check

- **Chi^2 with full covariance:** The statistical covariance is diagonal
  (Eq. 18), which is correct -- the three observables are extracted
  independently (R_b from counting, A_FB^b from linear fit, sin^2_theta
  from the SM formula). The systematic covariance includes the 10%
  R_b-A_FB^b correlation from shared b-tag efficiency.

- **Toy-based uncertainty propagation:** 1000 toys for R_b with only
  ~200/1000 valid extractions (20% convergence rate). This low rate
  reflects the underdetermined system. The statistical uncertainty
  (0.031) is derived from the RMS of valid toys only. This is
  methodologically acceptable but the 80% failure rate is a red flag
  for the stability of the extraction -- see Finding B2.

- **Closure tests:** The independent derivation-validation closure at
  WP 9.0 passes (pull = 1.93 < 2). The primary WP 10.0 closure is
  INFEASIBLE after 3 documented attempts. This is honestly reported.
  The closure shares the SM calibration assumption between derivation
  and validation sets, providing "partial (not full) independence" as
  stated in Table 13. This transparency is appreciated.

- **Systematic evaluation:** The dominant systematic (epsilon_uds at
  +/-50%) is a flat variation without a measurement-based constraint
  at Phase 4a. This is acknowledged and the multi-WP fit at Phase 4b
  is the documented mitigation. The 50% variation itself is the
  physical range (alpha = 0.20 to 0.50 from the scan).

### Input Provenance Check

Table 1 provides a clear provenance table with color coding (blue =
measured, red = external). This is well done. The analysis measures
f_s, f_d, epsilon_b, C_b, and delta_b from data/MC. External inputs
are R_c (constrained to SM), g_bb, g_cc, A_FB^c, delta_QCD, and
delta_QED -- all with citations.

The analysis is NOT a meta-analysis. The core observables (R_b from
double-tag counting, A_FB^b from angular fit) are genuine measurements
from data. The external inputs are standard corrections that every
LEP analysis uses. PASS.

### Commitment Traceability

The abstract commits to measuring R_b, R_c, and A_FB^b. At Phase 4a:
- R_b: self-consistency diagnostic extracted. Committed.
- R_c: constrained to SM. This was a strategy decision [D6], not a
  silent downscope. Committed.
- A_FB^b: method validation on MC. Committed.
- sin^2_theta_eff: correctly derived from A_FB^b. Committed.

No silently dropped commitments detected.

### Future Directions Check

Section 11 lists 6 items, all requiring infrastructure not available in
the archived data format (per-hemisphere vertex fitting, 5-tag system,
MC truth labels, 3D impact parameter, neural network tags, dE/dx). These
are genuinely infeasible. No "why wasn't this done?" red flags. PASS.

---

## Findings

### Category A (Must Resolve)

**A1. Operating point stability failure is inadequately mitigated at
Phase 4a.**

Only 1 of 4 tested working points (WP 10.0) yields a valid R_b
extraction. The stability scan requirement (flat R_b across >=2 WPs)
fails. The document correctly labels this INFEASIBLE and provides 3
remediation attempts. However, the consequences for the R_b measurement
are severe: the entire R_b result rests on a single working point at
the edge of the physical solution space. There is no redundancy.

The multi-WP fit at Phase 4b is the documented path forward, but the AN
does not quantitatively demonstrate that the multi-WP fit will actually
produce solutions at WPs 7-9 on data. The claim that "data-driven
constraints on epsilon_uds enlarge the physical solution space" is
plausible but unproven.

**Required action:** At Phase 4b, the operating point stability must be
re-evaluated with data-constrained efficiencies. If the multi-WP fit
does not produce valid solutions at >=2 working points with consistent
R_b, the R_b measurement should be flagged as unreliable. The Phase 4b
executor must document this as a blocking validation gate.

**A2. The A_FB^b fit chi^2/ndf is still problematic.**

Table 14 shows the intercept-inclusive fit chi^2/ndf ranges from 25.7/8
to 34.4/8 across kappa values. These correspond to p-values of ~10^-3
to 10^-4. While much improved from the origin-only fit (80-115/9), the
residual chi^2 is 3-4 per degree of freedom, indicating the linear model
does not adequately describe the data.

The document attributes this to "bin-level data/MC shape differences in
<Q_FB> not fully absorbed by the linear model." This is a physics issue:
if the cos_theta dependence of the hemisphere charge bias is not linear,
the extracted slope (and hence A_FB^b) could be biased.

**Required action:** At Phase 4b/4c, investigate whether a quadratic or
spline model improves the fit quality. If the chi^2/ndf remains >3
on data, the extracted A_FB^b uncertainty must be inflated to account
for model inadequacy, or the poor fit must be listed as a systematic.

### Category B (Should Address)

**B1. The R_b toy convergence rate (20%) raises questions about the
statistical uncertainty estimate.**

At WP 10.0, only ~200/1000 toys produce valid extractions. The RMS of
these 200 valid toys gives sigma_stat = 0.031. But the 800 failed toys
are not random -- they fail because they produce unphysical solutions.
The valid-only RMS underestimates the true statistical uncertainty
because it conditions on the extraction succeeding.

A proper Feldman-Cousins or likelihood-ratio approach would handle
the physical boundary correctly. The current approach gives a
confidence interval that has undercoverage near the boundary.

**Recommendation:** Document the boundary effect explicitly. At Phase 4b,
if the convergence rate improves (as expected with data constraints),
this becomes less critical. If it remains below ~50%, consider a
profile likelihood approach instead of toy-based RMS.

**B2. The epsilon_c systematic is one-sided.**

Section 5.4 states that the +30% variation produces solver failure (no
physical solution) while the -30% variation gives delta_R_b = 0.078.
The systematic is therefore evaluated from the -30% direction only. This
means the quoted systematic (0.078) represents the downward shift, but
the upward uncertainty from epsilon_c is unbounded within the current
framework.

**Recommendation:** State explicitly in the results table that the
epsilon_c systematic is one-sided (asymmetric). Propagate asymmetric
uncertainties if the multi-WP fit does not resolve this at Phase 4b.

**B3. The C_b systematic prescription is ad hoc.**

The C_b variation is defined as 2 x max(sigma_MC, |C_b^data - C_b^MC|)
= 0.010. This "inflated 2x" prescription is attributed to strategy
decision [D17] but has no statistical motivation. The factor of 2 is
arbitrary. Given that C_b enters multiplicatively in f_d and the
absolute C_b (~1.5) is far from the published value (~1.01), this
deserves more careful treatment.

**Recommendation:** At Phase 4b, derive the C_b systematic from the
data/MC difference directly, or from the spread across working points.
The 2x inflation may be conservative, but "conservative" should be
demonstrated, not assumed.

**B4. No before/after figure for the sigma_d0 calibration.**

Section 4.1 describes calibration scale factors of 1.3-7.6, but no
figure shows the d_0/sigma_d0 distribution before and after calibration.
Figure 7 shows the scale factors themselves, but the reader cannot
verify that the calibration actually produces unit-width negative tails.
The text asserts this ("approximately unit width by construction within
each bin") but the claim is not demonstrated.

**Recommendation:** Add a figure showing the negative d_0/sigma_d0
distribution before and after calibration, at least in a representative
momentum/theta bin. This is the key diagnostic for the impact parameter
resolution model.

**B5. The angular fit chi^2 diagnostic (Table 13) lists three FAIL
entries.**

Table 13 lists "OP stability" as FAIL (1/4 valid WPs) and "Angular fit
chi^2" as FAIL in both origin and intercept forms. While the OP stability
is discussed extensively, the angular fit chi^2 failures are mentioned
only briefly. The intercept model has chi^2/ndf ~ 3-4, which the text
acknowledges but does not fully explain.

**Recommendation:** Add a dedicated subsection discussing the angular fit
chi^2 failure, its potential causes (non-linear charge bias vs cos_theta,
MC shape mismodeling), and the expected behavior on data where the
physical asymmetry is present.

**B6. MC normalization to data integral should be more prominently
flagged.**

Section 3.3 states "The MC is normalized to the data integral in all
plots." This is stated once but easy to miss. For a document where
MC covers only 1994 and data spans 1992-1995, the normalization choice
affects the interpretation of every data/MC comparison.

**Recommendation:** Add a note in the data samples section (Section 2)
explaining why L x sigma normalization is not used and what the
normalization-to-data-integral approach does and does not test.

### Category C (Suggestions)

**C1.** Table 14: add a column for the chi^2/ndf p-value to make the
poor fit quality immediately apparent.

**C2.** Figure 7 x-axis labels: the bin labels (nvdet, p, |cos_theta|)
are too small to read at normal zoom. Consider rotating or simplifying.

**C3.** The Limitation Index (Table 21) is excellent but missing the
angular fit chi^2 issue. Consider adding an [L] entry for the non-linear
hemisphere charge bias.

**C4.** Section 8.1: the bias decomposition (epsilon_uds mis-calibration
dominant at 0.06, C_b inflation contributing ~0.005) is very informative.
Consider promoting this analysis to a dedicated subsection rather than
embedding it in the R_b results text.

**C5.** Appendix M (Systematic Completeness Cross-Reference): Table 26
is valuable. The "Our delta_R_b" column for epsilon_uds shows 0.38700
vs ALEPH's 0.00010 -- this 3870x ratio is the most striking number in
the document and could be highlighted more prominently as the single
metric that defines the analysis precision.

---

## Resolving Power Assessment

- **R_b:** Total uncertainty 0.396 gives 180% resolving power relative
  to SM. This is not a competitive measurement. The document is honest
  about this. After Phase 4b data constraints, the expected precision
  (~0.04) gives ~20% resolving power -- enough to detect large vertex
  corrections but not the sub-percent effects probed by the published
  ALEPH measurement. This is stated correctly in Section 10.2.

- **A_FB^b:** Total uncertainty 0.0045 gives 4.4% resolving power
  relative to SM A_FB^b. This is competitive with the published ALEPH
  precision (0.0052). If the fit quality issue (A2) is resolved, this
  measurement has genuine physics impact.

- **sin^2_theta_eff:** Statistical precision 0.0004 (0.17% relative)
  is competitive with individual LEP measurements. This is the most
  promising observable, contingent on A_FB^b being well-measured on data.

---

## Verdict

**Classification: B.** The analysis note is thorough, transparent, and
demonstrates a working infrastructure. The A_FB^b method is particularly
well-validated (kappa consistency, intercept model, charge separation
properties). The R_b method faces structural challenges from the
underdetermined calibration system that are honestly documented.

The document is ready to proceed to Phase 4b with the following
conditions:
1. The operating point stability (A1) must be re-evaluated on data
   as a blocking gate.
2. The A_FB^b fit quality (A2) must be investigated on data.
3. Category B items should be addressed at the Doc 4b writing stage.

This is not yet a paper -- it is a methods validation document, and it
succeeds as such. The path to a publishable result is clear for A_FB^b
and plausible (but not guaranteed) for R_b.
