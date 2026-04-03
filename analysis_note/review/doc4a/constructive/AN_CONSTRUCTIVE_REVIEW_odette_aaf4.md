# Constructive Review — Doc 4a Analysis Note
## Reviewer: odette_aaf4 (Constructive)
## Date: 2026-04-02
## Artifact: analysis_note/ANALYSIS_NOTE_doc4a_v1.tex (.pdf)

**MCP_LEP_CORPUS:** true — corpus calls made.

---

## Executive Summary

The Doc 4a analysis note is substantially complete and honest about the limitations
of the Phase 4a MC-only analysis. The authors have been admirably transparent:
the circular calibration is named and documented as such, the dominant systematic
(eps_uds = 0.387) dwarfs the result, and the operating-point-stability failure is
disclosed upfront. The writing is flowing prose, the structure follows the AN
template, and the reproduction contract is exemplary.

However, I identify two Category A items, five Category B items, and a set of
Category C improvements. The Category A items concern (1) a persistent typo in
the observable name that reaches the abstract and conclusions, and (2) an uncited
value (delta_QED) in a published equation. The Category B items cover genuine
methodological gaps: missing intercept-fit chi2 values in the per-kappa table,
unreported C_c / C_uds values used in the formula, the open-question of angular
fit chi2 after the intercept fix, missing parameter sensitivity table (a
COMMITMENTS.md requirement), and an inconsistency in the closure test independence
framing. Category C items address clarity, presentation, and depth improvements.

The analysis is telling the truth about what it measured and how well. The "honest
framing" test is passed — no attempt to hide the circularity or overstate results.
The dominant remaining risk for Phase 4b/4c is the multi-working-point eps_uds
constraint, which is well-motivated but unproven at this stage.

---

## Cross-Phase Concern Review (from REVIEW_CONCERNS.md)

### [CP1] Closure test tautology

**Re-check result: PARTIALLY RESOLVED.**

The AN correctly identifies the independent derivation-validation split (60/40 MC
split, documented seed = 12345) and distinguishes it from a self-consistency check.
Section 6.5.1 ("Mirrored significance") correctly labels the mirrored-significance
test a "code sanity check (the result follows algebraically)." The split closure at
WP 9.0 gives pull = 1.93, which is genuine (efficiencies from derivation set,
extraction from validation set).

However, there is a residual tautology concern: the derivation set still uses
R_b = R_b^SM to calibrate eps_b, eps_c, eps_uds — so the "closure" tests that the
formula is internally consistent under this assumption, not that the method recovers
a general truth. The AN does acknowledge this ("the calibration truth is still
assumed"), but the validation summary table lists this as PASS without flagging
that the independence is only partial. The table caption should add: "independence
is partial — only the MC events used for counting are statistically independent;
the calibration assumptions (R_b = SM input) are shared."

This is **Category B** — the closure test passes, but the PASS claim needs the
partial-independence caveat in the table itself, not just in prose.

### [CP2] A_FB^b extraction formula

**Re-check result: RESOLVED WITH COMMENT.**

The AN explicitly implements a linear fit to <Q_FB> vs cos(theta) with an intercept
(Section 7.2, Eq. 3), and clearly documents that the simplified formula
A_FB^b = (8/3)<Q_FB>/(R_b * delta_b) is NOT used as the extraction formula. The
intercept-inclusive linear regression is correctly identified as the governing
extraction. The downscoping of the full 4-quantity chi2 fit [D12b] is documented
with justification. CP2 is resolved for Phase 4a. Future reviewers at Phase 4b/4c
must verify that the 4-quantity fit is implemented when the real asymmetry is present.

### [CP3] sigma_d0 angular dependence

**Re-check result: RESOLVED.**

Section 4.1 (Eq. 5) explicitly states: "The sin(theta) dependence (not
sin^{3/2}theta) is the correct form for the Rphi-projected impact parameter d0;
the sin^{3/2}theta form applies to 3D impact parameters." This is correct
physics — d0 is a 2D (Rphi) quantity, so the multiple-scattering term scales as
B / (p sin(theta)) not B / (p sin^{3/2}(theta)). The corpus search did not find a
direct counter-example in ALEPH publications; the stated form is consistent with
standard treatment of 2D projected IP. CP3 resolved.

### [CP4] PDG inputs not yet fetched

**Re-check result: RESOLVED.**

Section 5.8 explicitly cites PDG 2024 with B hadron lifetimes to 4 decimal places:
B+ (1.638 ± 0.004) ps, B0 (1.517 ± 0.004) ps, Bs0 (1.516 ± 0.006) ps,
Lambda_b (1.468 ± 0.009) ps, B decay charged multiplicity 5.36 ± 0.01. All cited
as [PDG:2024]. CP4 resolved.

---

## Category A Findings — Must Resolve (Blocks PASS)

### [A1] Persistent typo: A_FM^b for A_FB^b in abstract, conclusions, and appendix

**Location:** Lines 143, 1845, 2215 (abstract, Section 10 opening, Appendix covariance caption).

```
A_\mathrm{FM}^b   <-- three occurrences
```

The correct macro is `A_\mathrm{FB}^b`. This typo appears in the abstract
("the hemisphere jet charge method for A_FM^b"), in the Section 10 opening
("measuring R_b, R_c, and A_FM^b"), and in the Appendix covariance section caption
("R_b--A_FM^b correlation"). The abstract and conclusions are the most-read parts
of any analysis note; this error in the observable name would be caught immediately
by any physicist reviewer.

**Fix:** Replace `\mathrm{FM}` with `\mathrm{FB}` at all three locations (search
for `\\mathrm{FM}` in the .tex file — grep finds exactly 3 matches).

**Category: A** — wrong observable name in abstract and conclusions constitutes a
factual error. Simple one-line fix.

---

### [A2] delta_QED cited but value never given; systematic impact not evaluated

**Location:** Section 4.4 (Eq. 8), p.~20.

Equation 8 reads:
```
A_FB^{0,b} = A_FB^b / (1 - delta_QCD - delta_QED)
```

The text states delta_QCD = 0.0356 ± 0.0029 (cited to [LEP:EWWG:2005]). But
delta_QED appears in the equation without a value, without a citation, and without
a systematic entry in the A_FB^b systematic table (Table 8). The systematic table
lists delta_QCD with impact "≈ 0 on MC" but does not mention delta_QED at all.

The LEP EWWG (hep-ex/0509008 Section 5.5) gives delta_QED ~ 0.002 from ISR
and gamma-Z interference. At A_FB^b ~ 0.09 this contributes ~ 0.0002 to the
pole asymmetry — comparable to the delta_QCD impact at full-data precision.

Two sub-issues:
1. The value of delta_QED is not cited anywhere in the AN.
2. The systematic on delta_QED is absent from Table 8.

Convention `extraction.md` §"Numeric Constants: Never From Memory" and the
project CLAUDE.md rule: "At review, any uncited numeric constant is Category A."
delta_QED appears in a published equation whose numerical application requires its
value to be cited.

**Fix:** Cite the value of delta_QED from hep-ex/0509008 or an equivalent
source, and add it to Table 8 with a note that it is negligible on MC
(same structure as delta_QCD).

**Category: A** — uncited numeric constant in a published equation.

---

## Category B Findings — Must Fix Before PASS

### [B1] Per-kappa AFB table reports origin-only chi2 — intercept-fit chi2 not reported

**Location:** Table 13 (per-kappa A_FB^b results), Section 8.2, p. 30.

The table lists chi2/ndf = 80.5/9, 104.9/9, 114.5/9, 101.5/9 at kappa = 0.3,
0.5, 1.0, 2.0 respectively. The table footnote states: "The chi2/ndf values in
Table 13 are from the origin-only fit (without intercept)."

The governing extraction uses the intercept-inclusive model (Section 7.2, explicitly
called "mandatory"). The Section 7.4 fit validation bullet says "The intercept-inclusive
model eliminates the pathological chi2 from the hemisphere charge bias." But the actual
post-intercept chi2 values are never reported anywhere in the AN.

A reader cannot evaluate fit quality without the chi2 of the model that is actually
used. Reporting only the chi2 of a model that was rejected creates a misleading
impression. The validation summary table (Table 14) says "Angular fit chi2: FAIL
(fixed w/ intercept)" — but without the intercept-model chi2, the FAIL is not
demonstrably fixed.

**Specific question the AN does not answer:** What is chi2/ndf of the linear fit
with intercept at each kappa? Section 7.4 says it is "substantially improved" —
this needs to be quantified.

**Actionable fix:** Add a column "chi2/ndf (intercept)" to Table 13, or add a
dedicated table/sentence: "With the intercept, the chi2/ndf is X.X/8 at kappa=0.3,
Y.Y/8 at kappa=0.5, etc." Update the validation summary table to reflect the
actual post-fix chi2.

**Category: B** — the governing extraction model's fit quality is unquantified.

---

### [B2] C_c and C_uds values used in the formula are not reported

**Location:** Equation (3) (the double-tag formula), and the calibration discussion
in Section 4.5.

The double-tag formula includes C_c and C_uds (hemisphere correlations for charm
and light quarks). Section 4.4 states "Taking eps_c, eps_uds, C_b, C_c, C_uds
from MC." Table 5 reports C_b at multiple working points. But C_c and C_uds are
never reported anywhere in the AN — not in the table, not in the text, not in the
appendix.

The corpus search (hep-ex/9609005, [REF1]) confirms that ALEPH calculated all
three correlation coefficients (rho_{b,IJ}, rho_{c,IJ}, rho_{uds,IJ}) and used
them in the fit. The DELPHI reference (inspire_1661817) gives lambda_b ~ 0.01-0.016,
distinct from the light-quark correlations.

For completeness and reproducibility, C_c and C_uds must be reported. If C_c ~ 1
and C_uds ~ 1 (plausible for lighter flavors with smaller lifetimes), state this
explicitly with the MC-derived values.

**Actionable fix:** Extend Table 5 to include C_c(MC) and C_uds(MC) at each
working point, or add a sentence: "The charm and light-quark correlations are
C_c = X.XX ± 0.00X, C_uds = X.XX ± 0.00X at WP 10.0 (from MC), consistent with
near-unity values expected for shorter-lifetime flavors."

**Category: B** — required inputs to the extraction formula are unreported.

---

### [B3] Parameter sensitivity table missing — COMMITMENTS.md commitment unfulfilled

**Location:** COMMITMENTS.md line 96 ("Parameter sensitivity table: |dR_b/dParam|
* sigma_param for all inputs"); not found in the AN.

The COMMITMENTS.md lists as not-yet-resolved: "Parameter sensitivity table:
|dR_b/dParam| * sigma_param for all inputs." The extraction conventions
(extraction.md §"Required validation checks" item 2) state: "For each MC-derived
input parameter, compute |dResult/dParam| * sigma_param. Flag any parameter
contributing more than 5x the data statistical uncertainty."

The AN has a systematic table (Table 7) with per-source delta_R_b, which partially
serves this purpose. But the parameter sensitivity table specifically requires:
- The derivative |dR_b/dParam| explicitly listed (not just the combined shift)
- The comparison against 5x the statistical uncertainty as a flag criterion

For eps_uds: |dR_b/deps_uds| * sigma(eps_uds) = 0.387 >> 5 * 0.031 = 0.155.
This is the single most important diagnostic — and it is never presented as a
formal table of derivatives.

Note: the Appendix A (Per-bin Systematic Tables) presents shift_up and shift_down,
which are derivatives times the variation. But the formatting as a sensitivity
table (derivatives, sigma_param, and the 5x-stat flag criterion) is not done.

**Actionable fix:** Add a compact 5-row sensitivity table to Section 5 or
Appendix A, showing for each dominant source: param, sigma_param, |dR_b/dParam|,
|dR_b/dParam| * sigma_param, and whether it exceeds 5 * sigma_stat = 0.155.

**Category: B** — COMMITMENTS.md binding commitment unfulfilled.

---

### [B4] Closure test independence language overstates independence

**Location:** Section 6.4 (Independent derivation-validation closure), Table 14
(validation summary), and the Known Limitations section (12.1, point 2).

The AN calls the 60/40 MC split an "independent derivation-validation closure test"
and marks it PASS in Table 14. But Section 12.1 (Known Limitations) itself says:
"the independence is only partial — the calibration truth is still assumed." This
is an internal inconsistency: Table 14 says PASS with no caveat, while Section 12.1
explains the test is not fully independent.

Additionally: the extraction.md conventions warn explicitly: "A self-consistent
extraction (deriving efficiencies and counting yields from the same sample) always
recovers the correct answer by construction — this is an algebra check, not a
closure test." The 60/40 split avoids using the same events twice, but the
calibration assumptions (R_b = SM) are shared. The conventions document is
specifically concerned with this failure mode.

**Actionable fix:** In Table 14, change "PASS" for the closure test to "PASS
(partial independence — calibration truth shared)" and add a footnote. This matches
the language already in Section 12.1 and removes the inconsistency.

**Category: B** — internal inconsistency between the results table and the
limitations section on the same page.

---

### [B5] eps_c systematic: single-sided evaluation presented without adequate motivation

**Location:** Section 5.4 (Charm tagging efficiency), Table 7.

The eps_c systematic uses only the -30% direction (shift_down = -0.078) because
the +30% direction produces a solver failure. The delta_Rb is taken as the
one-sided shift (0.078). This is stated in the text, but the table entry for the
+30% direction shows "null (solver fail)" with no further investigation.

From the standpoint of a journal referee: solver failure at a 1-sigma variation is
a significant methodological signal. It means the extraction is at the physical
boundary for charm contamination. A one-sided treatment of the systematic
underestimates the true uncertainty: if the solver fails at +30%, the uncertainty
in the +eps_c direction is effectively unbounded, not zero.

Two options for proper treatment:
1. Use the larger of the two shifts as a conservative symmetric estimate (currently
   the text implies 0.078, but properly this should note that the +30% direction
   is unphysical, not zero — the upper bound is not 0.078 but unknown).
2. Investigate the boundary: what eps_c value is the last to give a physical
   solution? Use that as the +1sigma endpoint for the asymmetric systematic.

**Actionable fix:** Add to Section 5.4: "The solver failure at +30% eps_c indicates
the extraction is within the physical boundary. The upper systematic is effectively
unbounded — the one-sided value of 0.078 is used conservatively, noting that the
true upper uncertainty may be larger. This will be investigated in Phase 4b when
the multi-working-point fit constrains eps_c from data." Also update Table 7 to
label the eps_c row as "asymmetric (upper unphysical)" rather than leaving
null in the table.

**Category: B** — the one-sided treatment of a solver-failure systematic is not
adequately motivated and may underestimate uncertainty.

---

## Category C Findings — Suggestions

### [C1] Section 7.3 (hemisphere charge bias) lacks the post-intercept chi2

Related to [B1] but specifically for the prose motivation. Section 7.3 says the
fit through the origin produces "catastrophic chi2 (~80-115/9 at all kappa)." It
would strengthen the argument to state the post-intercept chi2 in the same sentence:
"Without intercept: chi2/ndf = 80--115/9; with intercept: chi2/ndf = X.X/8."
This makes the fix demonstrable, not just asserted.

**Category: C**

---

### [C2] Figure captions could quantify data/MC agreement instead of saying "good"

**Affected figures:** Figs 3, 4, 5, 6, 8, 9, 10 — all data/MC comparison plots.

Captions say "Agreement is within 5% across all variables" (caption to Fig. 3)
or "good data/MC agreement" (caption to Fig. 8, 9). These qualitative phrases
are less useful than chi2/ndf for the comparison. Even a single aggregate metric
(chi2/ndf = X over the full range, or Kolmogorov-Smirnov p = 0.XX) would make
the claims verifiable.

Specific suggestion: Section 3.2 says "Agreement is generally good, with no
systematic trends in the pull distributions." Add to this sentence: "Kolmogorov-
Smirnov tests give p = XX across event-level variables and p = XX for d0."

**Category: C**

---

### [C3] Section 5.1 (eps_uds): the 50% variation is not motivated from first principles

The ±50% variation on eps_uds is described as "applied" without a citation for
why 50% is the appropriate scale. ALEPH (hep-ex/9609005 Table 4) uses ±10% for
the light-quark contamination, derived from data/MC comparison of the negative-d0
tail. Our 50% is 5x larger, presumably reflecting the absence of data calibration.

A sentence motivating the choice would help: "In the absence of a data-driven
calibration of eps_uds (which requires MC truth labels, unavailable [A1]), we assign
a conservative ±50% variation covering the plausible range of eps_uds values in the
MC calibration scan (alpha scanned from 0.20 to 0.50 at WP 10.0). The published
ALEPH value uses ±10%, derived from data/MC comparisons of the negative-d0 tail."

**Category: C**

---

### [C4] Figure F4 (f_d vs f_s) — add R_b = 0.280 locus label

**Location:** Caption and description of Fig. F4 (fd_vs_fs.pdf).

The caption describes this as the "double-tag fraction vs single-tag fraction" with
"theoretical prediction curves for different R_b values overlaid." The caption would
be improved by explicitly identifying which R_b curve passes through the data point
at WP 10.0. Adding: "The data at WP 10.0 falls near the R_b = 0.280 curve,
consistent with the extracted value" completes the diagnostic narrative.

**Category: C**

---

### [C5] Future Directions (Section 11) item 4: 3D impact parameter (z0)

Section 11, item 4 ("3D impact parameter") states: "The z0 branch is available
but its sign convention and resolution properties were not fully characterized
in this analysis." This item is labeled as future (infeasible now).

However, the z0 sign convention characterization is a feasible ~1-hour task:
apply the same negative-tail calibration protocol used for d0 to z0, check if
the negative-z0 tail is Gaussian, and verify the positive-z0 excess in b-enriched
hemispheres. This could be done now and would provide a cross-check of the 3D
displacement signature without requiring per-hemisphere vertex fitting.

**Actionable suggestion:** If z0 characterization is feasible within Phase 4b scope,
move it from Future Directions to a Phase 4b diagnostic. If not, state explicitly
why z0 calibration requires more than ~2 hours (e.g., the z0 sign convention in
the ALEPH helix parameterization is not straightforward).

**Category: C** — potentially feasible deferred work.

---

### [C6] Systematic table (Table 7): "Fraction" column is only filled for eps_uds

**Location:** Table 7 (systematic summary for R_b).

The "Fraction" column shows 99.5% for eps_uds and "---" for all other sources.
Computing the fraction for each source would require less than one line of
arithmetic per row. For eps_c: 0.078/0.395 = 19.7%. For C_b: 0.010/0.395 = 2.5%.
The "---" entries look like a formatting gap. Even if the non-dominant fractions
are shown as "<1%", the table reads more professionally.

**Category: C** — minor presentation improvement.

---

### [C7] The "Resolving Power" subsection (Section 10.2) could add a concrete NP benchmark

Section 10.2 says the Phase 4a R_b uncertainty of 0.396 gives "resolving power
Delta_R_b / R_b_SM ~ 180%." This is correct but abstract. A concrete statement
would sharpen it: "This is insufficient to detect even a 10% shift in the Zbb
vertex coupling, which would correspond to Delta_R_b ~ 0.022 — six times smaller
than our Phase 4a statistical uncertainty alone." The published ALEPH analysis
was sensitive to G_F * m_t^2 corrections at the ~0.001 level; our Phase 4a
analysis is not yet in that regime.

**Category: C**

---

### [C8] Appendix (Limitation Index) is missing [A4] — whatever A4 was

**Location:** Table in Appendix G (Limitation Index).

The table jumps from [A3] ("sigma_d0 not stored") to [A5] ("No particle ID"). [A4]
is absent without explanation. If [A4] was formally removed or merged with another
label, add a row: "[A4] — Label retired, merged with [A3]" or similar. A gap in a
sequential index suggests an editing artifact.

**Category: C** — minor audit trail issue.

---

### [C9] The DELPHI total uncertainty in the comparison table is correct but the text is inconsistent

**Location:** Table 15 (R_b comparison) vs. Introduction.

Introduction quotes: "DELPHI measured R_b = 0.21625 ± 0.00067 (stat) ± 0.00061
(syst)." Table 15 quotes the DELPHI value as "0.21625 ± 0.00091," which is the
correct quadrature total (sqrt(0.00067^2 + 0.00061^2) = 0.00091). This is
numerically consistent but a reader skimming might think the two citations
disagree. Add a footnote to Table 15: "Total uncertainty is the quadrature sum
of the stat and syst values quoted in the text."

**Category: C** — minor clarity improvement.

---

### [C10] Missing discussion of why WP 10.0 was chosen over WP 9.0 for the primary result

**Location:** Section 8.1 (R_b self-consistency diagnostic) and Appendix H
(Working Point Selection Details).

The AN states WP 10.0 is "the selected operating point" and "provides the highest
b purity" but does not present a criterion for the selection. WP 9.0 also gives a
valid extraction (used in the closure test, R_b = 0.347, pull = 1.93). Why WP 10.0
and not WP 9.0?

The Appendix H table shows f_d/f_s^2 (proxy for b purity) as 1.50 at WP 10.0 vs
1.37 at WP 8.0, but WP 9.0 is not listed. The working point selection criterion
(highest purity given physical solution) should be stated explicitly.

**Category: C**

---

## Depth Check: Per-Section Assessment

| Section | Depth | One Figure/Discussion That Would Most Improve It |
|---------|-------|--------------------------------------------------|
| 1. Introduction | Good | Add a 1-paragraph "discriminating power" framing: what would a 1-sigma excursion in R_b imply for Zbb vertex? |
| 2. Data Samples | Good | The MC sample description lacks the number of events per period (1994 P1/P2/P3 split in MC). |
| 3. Event Selection | Good | chi2/ndf quantitative data/MC agreement numbers in the cutflow caption. |
| 4. Corrections | Very good — best section | Add C_c, C_uds to the efficiency calibration table (fixes [B2]). |
| 5. Systematics | Good | Add eps_c one-sided motivation (fixes [B5]); parameter sensitivity table (fixes [B3]). |
| 6. Cross-checks | Good | Partial-independence caveat in Table 14 (fixes [B4]). |
| 7. Statistical Method | Good | Post-intercept chi2 (fixes [B1]). |
| 8. Results | Honest and clear | The F1 (stability scan) caption should state which WP is valid and why it was chosen (fixes [C10]). |
| 9. Comparison | Good — appropriately modest | No major additions needed. |
| 10. Conclusions | Good | Concrete NP benchmark in resolving power (fixes [C7]); fix A_FM typo ([A1]). |
| 11. Future Directions | Good | Re-evaluate z0 characterization feasibility (fixes [C5]). |
| 12. Known Limitations | Very good | No major additions needed. |
| Appendices | Very good | Fill Fraction column in Table 7 ([C6]); add [A4] gap explanation ([C8]); cite delta_QED ([A2]). |

---

## Honest Framing Check

**PASSES.** The analysis is telling the truth about what it measured. The abstract
explicitly labels the R_b result as "a self-consistency diagnostic of the circular
calibration procedure" — this is unusually forthright for a physics result. The
operating-point-stability failure is disclosed prominently (validation table, Known
Limitations, Results subsection). The A_FB^b result is correctly described as
"zero by construction on symmetric MC." No physics result is overstated.

The one framing tension is the closure test PASS label (addressed in [B4]) — but
this is an inconsistency in table notation, not an attempt to hide a problem.

---

## Resolving Power Evaluation

**R_b:** No resolving power at Phase 4a. Total uncertainty 0.396 >> R_b^SM = 0.216.
The 283x precision ratio vs ALEPH is quantified and explained. The expected
improvement path (multi-WP eps_uds constraint from data) is documented and
plausible. The analysis does NOT overstate that Phase 4b will achieve 10-20x
improvement — it presents this as an estimate.

**A_FB^b:** Comparable precision to ALEPH in the uncertainty, but the result is
zero by construction. The method has been validated (intercept model, kappa
consistency). The claim that Phase 4b/4c will yield the physical ~0.09 asymmetry
is correct — the signal simply isn't in the MC.

**sin2theta_eff:** The 0.250 value corresponds to A_e = 0 (maximum parity violation
point). This is correctly identified as a formula-validation exercise, not a
measurement.

**Verdict:** The measurement has no resolving power at Phase 4a for R_b, expected
resolving power for A_FB^b at Phase 4b/4c. This is correctly stated.

---

## Corpus Cross-Check Notes

1. The ALEPH hep-ex/9609005 (REF1, corpus hit [1]) confirms that per-hemisphere
   vertex reconstruction was the key to reducing C_b to ~1.01. The AN's explanation
   of the C_b inflation (shared thrust axis, estimated Delta_C_b ~ 0.30) is
   consistent with the corpus evidence. The DELPHI analysis (inspire_1661462,
   corpus hit [2]) also used per-hemisphere vertex reconstruction. The AN
   correctly identifies this as the missing ingredient.

2. The self-calibrating AFB fit (DELPHI inspire_1661115, corpus hit) uses a
   5-category chi2 fit (N, Nbar, N^D, N^D_bar, N^same), which is the methodology
   described in [CP2] and downscoped to Phase 4b/4c [D12b]. The linear regression
   used at Phase 4a is a valid simplified extraction when A_FB ~ 0 (no asymmetry
   to resolve). The corpus supports the downscoping decision.

3. The corpus did not provide direct LEP references for the sin(theta) vs
   sin^{3/2}(theta) question in the ALEPH detector. The claim in Section 4.1 that
   sin(theta) is correct for 2D d0 is standard physics (multiple-scattering in Rphi
   plane scales with the track's path length through material, which is
   proportional to 1/sin(theta) not 1/sin^{3/2}(theta)). No corpus evidence
   contradicts this; the concern [CP3] remains resolved.

---

## Summary Table

| ID | Category | Brief Description | Section |
|----|----------|-------------------|---------|
| A1 | **A** | Typo A_FM^b → A_FB^b (abstract, conclusions, appendix) | 3 locations |
| A2 | **A** | delta_QED value uncited; systematic absent from Table 8 | §4.4, Table 8 |
| B1 | **B** | Post-intercept chi2/ndf not reported; origin-only chi2 in governing-model table | §7.2, Table 13 |
| B2 | **B** | C_c and C_uds values unreported despite appearing in the formula | §4.4, Table 5 |
| B3 | **B** | Parameter sensitivity table missing (COMMITMENTS.md binding) | §5 / App A |
| B4 | **B** | Closure test PASS label inconsistent with partial-independence acknowledged in §12 | Table 14 |
| B5 | **B** | eps_c solver failure at +30% treated as zero, not as unbounded upper uncertainty | §5.4, Table 7 |
| C1 | C | Post-intercept chi2 absent from §7.3 motivation (related to B1) | §7.3 |
| C2 | C | Data/MC captions use qualitative "good" instead of chi2/KS p-values | Multiple figures |
| C3 | C | 50% eps_uds variation not motivated relative to ALEPH's 10% | §5.1 |
| C4 | C | Fig F4 caption doesn't label which R_b curve the data falls on | §8.4, Fig F4 |
| C5 | C | z0 characterization possibly feasible now — reconsider Future Directions placement | §11 |
| C6 | C | Fraction column incomplete (only eps_uds filled) in Table 7 | Table 7 |
| C7 | C | Resolving power needs concrete NP benchmark | §10.2 |
| C8 | C | [A4] gap in Limitation Index without explanation | App G |
| C9 | C | DELPHI total uncertainty inconsistent notation between text and Table 15 | §1, Table 15 |
| C10 | C | WP 10.0 selection criterion not stated | §8.1, App H |

---

## Recommendations for Fixer

Priority order for the fixer:

1. **Fix A1 immediately** — one-line sed/grep fix, eliminates a factual error from
   the abstract.
2. **Fix A2** — add delta_QED value and citation to Eq. 8 and Table 8.
3. **Fix B1** — re-run the intercept-model fits, extract chi2/ndf, add to Table 13
   and update the validation summary table.
4. **Fix B2** — report C_c and C_uds in Table 5 or nearby text.
5. **Fix B3** — add the parameter sensitivity table (5 rows, 5 columns, ~1 hour).
6. **Fix B4** — one-line change to Table 14 caption, add "partial independence" caveat.
7. **Fix B5** — expand §5.4 with the boundary motivation sentence.
8. C1-C10 as time permits.

The A items and B1/B3 are the most important for the scientific record.
B4 and B5 are presentation/framing issues that do not change the physics.

---

*Reviewer: odette_aaf4 (Constructive) | Session date: 2026-04-02*
*MCP_LEP_CORPUS: true | Corpus calls: 4 queries executed*
