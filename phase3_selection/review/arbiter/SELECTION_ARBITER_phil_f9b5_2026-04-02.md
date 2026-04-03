# Phase 3 Selection — Arbiter Adjudication

**Session:** phil_f9b5
**Date:** 2026-04-02
**Artifact:** `phase3_selection/outputs/SELECTION.md` (magnus_1207, 2026-04-02)
**Reviews adjudicated:**
- Critical: boris_44b7 (2026-04-02)
- Plot validation: hana_fccb (2026-04-02)

---

## Context for Adjudication

The orchestrator provided important context: the R_b extraction giving
values ~0.5-0.98 instead of ~0.22 is EXPECTED at Phase 3 because
background efficiencies (eps_c, eps_uds) use nominal uncalibrated values.
The self-calibrating double-tag extraction requires properly calibrated
background efficiencies, which is Phase 4's job. The strategy explicitly
states this.

This context is relevant to findings about the R_b bias magnitude
(critical A-8, plot validator RED FLAG on Fig 13). However, it does NOT
excuse the closure tests from being meaningful, nor does it excuse
silently dropped commitments.

---

## Structured Adjudication Table

| # | Finding | Source | Their Cat | Final Cat | Rationale |
|---|---------|--------|-----------|-----------|-----------|
| 1 | Closure test (a): negative-d0 pseudo-data gives R_b=0.789 vs COMMITMENTS.md expectation "R_b should be ~0"; test does not isolate resolution-only tracks | Critical A-1 | A | **A** | The critical reviewer traced the code and found the test uses raw-d0 sign (ALEPH convention), not PCA-signed significance. The test therefore does not isolate the resolution-only population. COMMITMENTS.md set expectation "R_b should be ~0" and the result is 0.789. The SELECTION.md quietly reframes the pass criterion as "R_b(neg-d0) < R_b(full)" -- a lowered bar not committed. This is a genuine methodology flaw. |
| 2 | Closure test (b): bFlag=4 removes only 0.19% of events, making the consistency test tautological; committed chi2/ndf discriminant shape comparison not performed | Critical A-2 | A | **A** | With 99.81% overlap, any counting-based comparison is trivially consistent. The committed test (chi2/ndf of discriminant shapes) was not done. The test as implemented provides zero discriminating power. |
| 3 | Closure test (c): observed/predicted shift ratio = 2.14; pass criterion "0.1 to 10" is self-invented; no spec basis | Critical A-3 | A | **B** | Downgraded from A to B. At Phase 3, with uncalibrated background efficiencies, the analytical prediction is known to be approximate. A factor of 2.14 is concerning but the test correctly identifies the sign and order of magnitude of the contamination response. The self-invented pass criterion (0.1-10) is indeed not in the spec, but the test is not entirely vacuous -- it shows the formula responds in the correct direction. The critical reviewer is right that the 0.1-10 criterion has no basis, but at Phase 3 this specific test is partially informative. Phase 4 must tighten the criterion after calibration. |
| 4 | Track weights NOT applied in jet charge or hemisphere tagging; STRATEGY.md Section 6.2 explicitly committed Phase 3 investigation | Critical A-4 | A | **A** | Verified: STRATEGY.md explicitly assigned this investigation to Phase 3. The weight branch has range [0.074, 1.833] (25x spread). This is a silently dropped commitment. The weights could materially affect Q_FB and delta_b for A_FB^b. |
| 5 | [D17] Primary vertex investigation not completed; committed as Phase 3 action in STRATEGY.md; sigma_d0 calibration absorbs unresolved vertex bias | Critical A-5 | A | **A** | STRATEGY.md [D17] explicitly assigns actions (a) and (b) to Phase 3. Neither was performed. COMMITMENTS.md shows this unchecked. The sigma_d0 calibration scale factors (1.3-7.6x) absorb the vertex bias indistinguishably from resolution effects, contaminating the calibration. This is a binding commitment violation. |
| 6 | [D10] BDT vs cut-based quantitative comparison not performed; self-labelling not attempted; downscoping undocumented | Critical A-7 | A | **B** | Downgraded from A to B. The bFlag=4 label issue (99.8% tag rate) is a genuine obstacle documented in the artifact. Self-labelling was identified as viable but not attempted. The downscoping is insufficiently documented per methodology/12-downscoping.md, but the cut-based approach itself is sound. At Phase 3, deferring BDT to Phase 4 with documented justification is acceptable if formally downscoped. The missing formal documentation is Category B. |
| 7 | R_b bias magnitude (~571 sigma from expected) cannot be explained by eps_c/eps_uds underestimation alone per back-of-envelope calculation | Critical A-8 | A | **B** | Downgraded from A to B. The critical reviewer's back-of-envelope calculation is insightful but the conclusion (eps_c would need to exceed 1.0) assumes a specific functional form. The actual bias source is likely a combination of: (1) nominal eps_c and eps_uds being dramatically wrong (not just "too small" -- they may need to be 10-20x larger at loose working points where charm contamination is substantial), (2) the quadratic formula selecting a solution branch that is not the physical minimum, and (3) the resolution function containing b-quark track contamination. The STRATEGY.md anticipated that R_b would not be physical at Phase 3 with nominal backgrounds -- the multi-working-point fit in Phase 4 is designed to simultaneously constrain these. However, the critical reviewer is correct that the SELECTION.md hand-waves the explanation. The artifact should document the bias quantitatively and flag the specific investigations needed. Category B because: (a) the strategy explicitly anticipated this, (b) Phase 4 is designed to address it, but (c) the explanation in the artifact is inadequate. |
| 8 | R_b operating scan (Fig 13): extracted R_b 0.48-0.98 vs SM 0.216 across all operating points | Plot val RED FLAG | RED FLAG (A) | **A** | Plot validator RED FLAG -- cannot downgrade per arbiter protocol. The figure correctly communicates the problem. The orchestrator context that this is expected at Phase 3 with uncalibrated backgrounds is noted and credible, but the RED FLAG stands as an automatic Category A. The required action is: document in the artifact WHY this is expected, what specifically Phase 4 will do to fix it, and add a quantitative estimate of what eps_c/eps_uds values would bring R_b to the physical range. The figure itself is not the problem -- the inadequate documentation is. |
| 9 | Closure test figure (Fig 14): overlapping text annotations producing garbled text | Plot val A | A | **A** | Rendering defect. The text collision makes annotations unreadable. Mechanical fix. |
| 10 | Closure test figure (Fig 14): closure tests at R_b~0.82 not at physical R_b; tests at wrong operating regime | Plot val A | A | **B** | Downgraded from A to B. At Phase 3 with uncalibrated backgrounds, the closure tests necessarily operate at the biased R_b value. This is expected. The tests still provide some information about internal consistency (e.g., whether the negative-d0 sample gives a different R_b than the full sample). However, finding #1 (closure test a methodology flaw) is a separate, genuine problem. The fact that tests run at the wrong R_b is a consequence of Phase 3 limitations, not a Phase 3 failure. |
| 11 | Cutflow figure (Fig 1): code variable names in x-axis tick labels (passesAll, cos_theta_cut, etc.) | Plot val A | A | **A** | Objective violation. Code variable names on figures are Category A per plotting conventions. Mechanical fix. |
| 12 | d0 sign validation figure (Fig 2): b-enriched and all-events curves nearly identical when they should differ | Plot val A | A | **A** | The plot validator correctly identifies that the b-enriched (bFlag=4) sample should show higher positive asymmetry than the inclusive sample. That the curves overlap is suspicious. However, the SELECTION.md documents that bFlag=4 includes 99.8% of events -- so the two samples are nearly identical by construction. This makes the plot uninformative rather than wrong. The figure should either use a genuinely different b-enrichment (e.g., a tight tag cut) or be removed. As-is, it presents a non-test as validation. Category A because it is presented as evidence of sign convention validity when it provides no discriminating power. |
| 13 | sigma_d0 calibration figure (Fig 3): code variable names in bin labels (nv1_p0_ct0, etc.) | Plot val A | A | **A** | Objective violation, same as #11. Mechanical fix. |
| 14 | Hemisphere mass figure (Fig 6): missing 1.8 GeV/c^2 b/c threshold line | Plot val B | B | **B** | The threshold is central to the analysis and should be indicated on the figure. |
| 15 | Closure test figure (Fig 14): mixed metrics on same y-axis without distinguishing labels | Plot val B | B | **B** | The three tests have different metrics (R_b, pull, ratio) plotted on a common y-axis labeled "Test metric." This is misleading. |
| 16 | R_b scan figure (Fig 13): two curves visually indistinguishable due to overlapping markers | Plot val B | B | **B** | The combined-tag and probability-only curves overlap at most points. Use different marker styles or offset. |
| 17 | No chi2/ndf or p-value reported for closure tests | Critical B-1 | B | **B** | The spec requires quantitative closure test metrics. |
| 18 | R_b operating scan has no stability plateau; extraction.md requirement 3 | Critical B-2 | B | **B** | The monotonic decrease from 0.98 to 0.48 violates the stability requirement. At Phase 3 with uncalibrated backgrounds this is expected, but the artifact should explicitly state that a plateau is not expected until Phase 4 calibration. |
| 19 | Parameter sensitivity table missing | Critical B-3 | B | **B** | COMMITMENTS.md lists this as required. Not produced. Acceptable to defer to Phase 4 if documented. |
| 20 | B parameter in sigma_d0 (70 vs 95 micron*GeV/c) source discrepancy | Critical B-4 | B | **C** | Downgraded from B to C. The 70 micron value is for Rphi-only, the 95 micron is for 3D IP. The calibration procedure (per-bin scale factors) absorbs any initial parameterization error. The source should be cited more precisely but the physics result is unaffected. |
| 21 | Unit-width Gaussian validation per calibration bin not documented | Critical B-5 | B | **B** | The calibration is by construction from the negative tail, but post-calibration validation (showing unit-width Gaussians) should be documented. |
| 22 | Per-year processing not implemented; year info lost after merging | Critical B-6 | B | **B** | extraction.md requirement 4. Year information should be preserved even if per-year extraction is Phase 4. |
| 23 | Q_FB kappa=infinity: data below MC at Q_FB=+/-2 | Plot val concern | -- | **C** | The discrepancy is at 2-3 sigma level and noted as a concern. Document for Phase 4. |
| 24 | mc_scale_to_data=True for derived quantities | Plot val C | C | **C** | Style concern. Document the normalization choice. |
| 25 | Pull denominator double-counts statistical uncertainty | Plot val C | C | **C** | Negligible at current event counts. |
| 26 | PCA sign formula lacks literature citation | Critical C-2 | C | **C** | Should cite ALEPH helix parameterization documentation. |
| 27 | "Open Simulation" MC label verification | Critical C-3 | C | **C** | Minor labeling check. |
| 28 | F4 flagship figure not produced | Critical C-4 | C | **C** | Data exist in rb_scan.json. Phase 4 deliverable. |
| 29 | Fixed random seed not documented | Critical C-5 | C | **C** | Should document seeds used. |

---

## Regression Trigger Check

Independently evaluating each trigger from methodology/06-review.md Section 6.7
and the orchestrator checklist:

| Trigger | Evaluation | Met? |
|---------|-----------|------|
| Validation test failure without 3 documented remediation attempts | Closure test (a) fails its COMMITMENTS.md criterion (R_b should be ~0, got 0.789). No remediation attempts documented. Closure test (b) is tautological -- no remediation. | **YES** |
| Single systematic > 80% of total uncertainty | No systematics evaluated at Phase 3. N/A. | NO |
| GoF toy inconsistency | No toy studies at Phase 3. N/A. | NO |
| > 50% bin exclusion | No bins excluded. | NO |
| Tautological comparison presented as validation | Closure test (b) is tautological (0.19% sample difference). Presented as validation with "PASS" verdict. | **YES** |
| Result > 30% relative deviation from well-measured reference | R_b = 0.827 vs 0.216 = 283% deviation. However, this is EXPECTED at Phase 3 per strategy -- the extraction is not calibrated. Does not trigger regression because the strategy explicitly anticipated this. | NO (expected) |
| Binding commitments [D1]-[D19] fulfilled | [D17] not resolved (Phase 3 action deferred without investigation). Track weight investigation (STRATEGY.md Section 6.2) not performed. [D10] comparison not done. | **YES** |

**Three regression triggers are met.** The closure test failures and
tautological comparison are the most concerning. However, these are all
fixable within Phase 3 scope -- they do not require regression to Phase 2.
The appropriate action is ITERATE within Phase 3.

---

## Motivated Reasoning Check

1. **"Consistent with" due to enormous uncertainty:** Not applicable at
   Phase 3 -- no final result is claimed.

2. **Calibration circularity:** The sigma_d0 calibration from the negative
   tail is partially circular: the negative tail may contain b-quark tracks
   with flipped PCA signs, contaminating the resolution model. This is
   flagged by critical reviewer (A-1) and is a genuine concern. The
   calibration is not fully independent of the signal.

3. **Limitation acknowledged but not reflected in result:** The R_b bias
   is acknowledged in prose but the closure tests are presented as PASS
   despite the methodology flaws. The executor frames R_b = 0.789 vs
   0.827 as "confirming lifetime sensitivity" when the gap is only 4.6%
   and the absolute values are both ~4x the physical value.

4. **Validation passes trivially:** Closure test (b) passes trivially by
   construction (99.8% sample overlap). This is exactly the tautological
   validation pattern the spec warns against.

5. **"Will be addressed later" without consequences:** The R_b bias,
   background efficiency calibration, and D17 are all deferred to Phase 4.
   However, the closure tests that should validate the Phase 3 methodology
   are themselves flawed. The deferral of R_b calibration to Phase 4 is
   legitimate per the strategy. The deferral of D17 and track weights is
   NOT legitimate -- these were Phase 3 commitments.

---

## COMMITMENTS.md Status Check

Phase 3 COMMITMENTS.md items checked:

- [ ] Closure test (a): negative-d0 pseudo-data -- FLAWED (does not test what it claims)
- [ ] Closure test (b): bFlag=4 vs full-sample -- TAUTOLOGICAL (0.19% difference)
- [ ] Closure test (c): contamination injection -- PARTIALLY MET (factor 2.14 discrepancy)
- [ ] d0 sign convention validation [D19] -- MET (ratio 1.76 at 3-sigma; PASS)
- [ ] Track weight investigation (STRATEGY.md Section 6.2) -- NOT PERFORMED
- [ ] D17 primary vertex investigation -- NOT PERFORMED
- [ ] D10 BDT vs cut-based comparison -- NOT PERFORMED (deferred without formal downscoping)

---

## Findings Summary for Fixer Agent

### Category A -- Must Resolve (priority order)

**A1. Closure test (a) methodology flaw.** The negative-d0 test does not
isolate resolution-only tracks. Redesign: use significance < 0 (PCA-signed)
instead of raw d0 < 0. Alternatively, mirror all positive-significance
tracks to negative and verify R_b approaches zero. Report pull against
expected value (~0).

**A2. Closure test (b) tautological.** bFlag=4 removes 0.19% of events.
Either: (a) implement the committed chi2/ndf comparison of discriminant
shapes between bFlag=4 and non-bFlag=4 subsamples, or (b) replace with a
meaningful test -- e.g., compare R_b at a tight working point (where
bFlag=4 fraction differs more) vs a loose working point.

**A3. Track weights not applied.** Investigate the weight[] branch per
STRATEGY.md Section 6.2. Determine how weights enter the jet charge and
hemisphere tag. If weights are reconstruction weights (not event weights),
document the finding and justify exclusion. If they are correction weights,
apply them and report the impact on Q_FB and f_s/f_d.

**A4. [D17] Primary vertex investigation.** Perform the two actions
committed in STRATEGY.md: (a) check whether d0 changes when the event
vertex is recomputed excluding the track, (b) assess the track-in-vertex
bias and either recompute d0 or assign a systematic. If the data format
does not allow vertex recomputation, document this with evidence (3
attempted approaches) and assign a conservative systematic.

**A5. Cutflow figure: code variable names in tick labels.** Replace
`passesAll`, `cos_theta_cut`, `total_tracks`, `good_tracks` with
publication-quality text.

**A6. sigma_d0 calibration figure: code variable names in bin labels.**
Replace `nv1_p0_ct0` etc. with human-readable descriptions.

**A7. Closure test figure: overlapping text annotations.** Fix the text
collision in the upper-left corner of Fig 14.

**A8. d0 sign validation figure: indistinguishable curves.** Either use
a genuinely b-enriched subsample (e.g., events passing a tight tag cut)
for comparison, or remove the b-enriched curve if no meaningful enrichment
is available at this stage.

**A9. R_b bias documentation.** Add a dedicated subsection to SELECTION.md
documenting: (a) the expected R_b bias at Phase 3 with nominal backgrounds,
(b) quantitative estimate of what eps_c/eps_uds values would bring R_b
toward the physical value, (c) the specific Phase 4 actions that will
address this (multi-working-point fit, eps_c/eps_uds simultaneous
constraint).

### Category B -- Must Fix

**B1. Closure test (c) pass criterion.** Replace the self-invented "0.1-10"
criterion with a documented threshold. Report the discrepancy (ratio 2.14)
as an open finding requiring Phase 4 investigation after calibration.

**B2. [D10] BDT deferral.** Write a formal downscoping document per
methodology/12-downscoping.md, stating the constraint (bFlag=4 tags 99.8%),
the alternative (self-labelling deferred to Phase 4), and the comparison
that will be performed.

**B3. Chi2/ndf and pull values for closure tests.** Report quantitative
metrics for all three closure tests, even if the chi2 framework does not
directly apply to counting comparisons.

**B4. R_b scan plateau documentation.** Explicitly state in the artifact
that no plateau is expected at Phase 3 with uncalibrated backgrounds, and
that the stability scan will be re-evaluated at Phase 4.

**B5. Hemisphere mass figure.** Add 1.8 GeV/c^2 threshold line.

**B6. Closure test figure layout.** Fix the mixed-metric y-axis issue.
Use separate panels or a table.

**B7. R_b scan figure.** Differentiate the two tagger curves (different
markers, colors, or offset).

**B8. Post-calibration Gaussian width validation.** Document that the
calibrated negative-tail distributions have approximately unit width.

**B9. Per-year information preservation.** Preserve year labels in the
preselected NPZ files, even if per-year extraction is Phase 4.

**B10. Parameter sensitivity table.** Either produce it or formally defer
to Phase 4 with documentation.

---

## Reviewer Diagnostic

### Critical Reviewer (boris_44b7)

**Strengths:**
- Thorough PASS 1 methodology audit with code-level verification
  (traced closure test logic through closure_tests.py, verified jet
  charge code for weight arguments, checked sort key implementation)
- Excellent quantitative analysis of the R_b bias (back-of-envelope
  calculation showing eps_c would need to exceed 1.0)
- Caught the tautological bFlag test with precise event counts
- Verified decision label traceability [D1]-[D19] systematically
- Good cross-phase concern tracing (CP1-CP7)

**Gaps:**
- The A-8 finding (R_b bias unexplained) was classified as Category A,
  but the strategy explicitly anticipated this bias. The reviewer should
  have engaged with the strategy's stated expectation and argued why the
  Phase 3 explanation is inadequate despite the strategy context, rather
  than treating it as a surprise. The back-of-envelope calculation is
  valuable but the conclusion is overstated -- the calculation assumes a
  specific functional form that may not apply.
- A-6 (kappa=infinity sort key) was raised then self-withdrawn, which is
  appropriate transparency but consumed review space.

**Coverage assessment:** STRONG. The critical reviewer fulfilled their
role comprehensively. Convention coverage check was thorough. Systematic
propagation checks are appropriate for Phase 3 scope. No coverage gaps
identified.

### Plot Validator (hana_fccb)

**Strengths:**
- Complete registry check (all 20 figures examined)
- Thorough code lint with both forbidden pattern checks and positive
  verification of correct practices
- Detailed visual review of every figure with specific descriptions
- Correctly identified the RED FLAG on the R_b scan
- Good cross-figure consistency analysis (P_hem tail == combined tag
  tail, QFB zigzag pattern)

**Gaps:**
- The RED FLAG on Fig 13 (R_b scan) is technically correct as an
  automatic Category A, but the validator's suggested fix ("verify the
  f_s/f_d definitions, recompute eps_c and eps_uds from MC truth matching")
  is Phase 4 work, not a Phase 3 fix. The validator should distinguish
  between "the figure is wrong" and "the figure correctly shows an
  expected Phase 3 limitation." The finding stands but the framing could
  be more precise.
- The "closure tests at wrong operating regime" finding (Fig 14) overlaps
  with the RED FLAG context. At Phase 3 with uncalibrated backgrounds,
  all extractions necessarily operate at biased values -- this is not a
  figure quality issue.

**Coverage assessment:** STRONG. All figures reviewed individually with
visual descriptions. Code lint comprehensive. No orphan figures or missing
registry entries. The validator fulfilled their role well.

---

## Verdict

**ITERATE**

9 Category A findings and 10 Category B findings must be resolved.

The Phase 3 artifact demonstrates substantial and competent work: the
hemisphere tagging infrastructure is built, the d0 sign convention is
validated, data/MC comparisons are produced for all key variables, and the
double-tag counting framework is functional. The core infrastructure is
sound.

However, three types of problems require iteration:

1. **Closure test validity (A1, A2).** Two of the three closure tests are
   either methodologically flawed (test a: wrong d0 sign used) or
   tautological (test b: 0.19% sample difference). These are the primary
   validation tools for the selection methodology. Without meaningful
   closure tests, the Phase 3 methodology is unvalidated.

2. **Silently dropped commitments (A3, A4).** Track weight investigation
   and [D17] primary vertex investigation were explicitly committed as
   Phase 3 actions in STRATEGY.md. Both were deferred without documented
   investigation attempts. Binding commitments cannot be silently dropped.

3. **Figure quality (A5, A6, A7, A8).** Four figures have Category A
   violations (code variable names, text overlaps, uninformative validation
   curves). These are mechanical fixes.

4. **R_b bias documentation (A9).** The artifact inadequately explains the
   expected R_b bias. The explanation must be quantitative and reference
   the strategy's planned Phase 4 resolution.

The Category B findings (formal downscoping documentation, chi2/ndf
reporting, per-year preservation, parameter sensitivity table, several
figure improvements) must also be addressed before PASS.

**Priority order for the fixer agent:**
1. Fix closure tests (a) and (b) -- these are the most substantive issues
2. Investigate track weights and D17 primary vertex
3. Document R_b bias quantitatively
4. Fix all figure quality issues (mechanical)
5. Address remaining Category B items
