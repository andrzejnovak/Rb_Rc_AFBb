# Arbiter Report: Phase 4a Inference -- Expected Results

Session: sven_2b4e | Date: 2026-04-02

Artifact: `phase4_inference/4a_expected/outputs/INFERENCE_EXPECTED.md`
Critical reviewer: ivan_f97c
Plot validator: fiona_7de9

---

## Preamble: Phase 4a Context

This adjudication is performed in the context of Phase 4a -- expected
results on MC pseudo-data with NO MC truth labels. The analysis faces a
fundamental constraint: background efficiencies cannot be calibrated from
truth. Certain findings that would be Category A on data are expected
limitations in this context; others remain blocking regardless. The
adjudication below distinguishes carefully between the two.

---

## Structured Adjudication Table

| # | Finding | Source | Their Cat | Final Cat | Rationale |
|---|---------|--------|-----------|-----------|-----------|
| 1 | Circular calibration: R_b^SM assumed to derive eps_b, then R_b extracted | Critical [A1] | A | **A** | conventions/extraction.md is explicit: "back-substitution is a diagnostic, not a calibration." The artifact presents R_b = 0.280 as a physics result in the summary table rather than as a self-consistency diagnostic. The fix is documentation/relabelling, not a methodological redesign -- the calibration is the only feasible approach without truth labels. But the prose MUST explicitly label this a circular calibration self-consistency check, not a measurement. |
| 2 | Self-calibrating fit chi2/ndf >> 5 (7.7--10.4) at all kappa; simple fit chi2/ndf 8.9--12.7 | Critical [A2] | A | **A** | I verified afb_results.json: self_calibrating_fit chi2/ndf = 298.6/39 = 7.66 (kappa 0.3), up to 404.5/39 = 10.37 (kappa 1.0). All have p = 0.0. The artifact reports only the simple_fit values and dismisses them as "statistical fluctuations." chi2/ndf ~ 10 is not a fluctuation. Per methodology/06-review.md section 6.3.3, p < 0.01 is "Failure -- Category A." This is also linked to cross-phase concern [CP2] about the wrong formula. A Finding + Resolution section with >= 3 remediation attempts is required. |
| 3 | Operating point stability: chi2=0.0, ndf=0, passes=true in validation.json | Critical [A3] | A | **A** | I verified validation.json directly: `"chi2": 0.0, "ndf": 0, "passes": true`. This is a placeholder, not a test result. rb_results.json confirms only WP 10.0 yields a non-null R_b. With one valid point, no stability test is possible. conventions/extraction.md: "Category A if fails." The JSON must be corrected to passes=false. |
| 4 | Independent closure at operative WP (10.0) not demonstrated on validation split | Critical [A4] | A | **A** | validation.json shows per_wp entries only at thresholds 7.0 and 9.0. WP 10.0 closure appears only in rb_results.json on the full MC (pull = 0.97), which is not independent. The validation split at WP 10.0 was either not attempted or produced null. This gap means the method at the operative point is untested on independent data. Must attempt and document result (even if null, with remediation attempts). |
| 5 | Mandatory precision investigation artifact missing (R_b ratio 278x) | Critical [A5] | A | **A** | Phase 4a CLAUDE.md: "If ratio > 5x on same dataset, produce a mandatory investigation artifact." validation.json records ratio = 277.6 with investigation_required = true. No artifact exists. The one-line explanation is not an artifact. Estimated fix: < 1 hour (write a markdown document explaining the ratio). Cannot dismiss as out of scope. |
| 6 | Alpha scan range undocumented; "closest to 0.10" when selected = 0.20 | Critical [A6] | A | **A** | mc_calibration.json WP 10.0 shows all solutions have alpha >= 0.20. The artifact states "closest to 0.10" but the selected value is 0.20. This is a documentation failure on a parameter that directly determines eps_uds, which drives the dominant systematic (0.387). Must document the scan range and correct the prose. |
| 7 | eps_b numerical inconsistency: artifact table 0.238, rb_results.json 0.193 at WP 10.0 | Critical [A7] | A | **A** | I verified: mc_calibration.json full_mc_calibration WP 10.0 eps_b = 0.238; rb_results.json extraction_results WP 10.0 eps_b = 0.193. The 23% discrepancy is confirmed. The artifact Section 2 table cites the full_mc_calibration value. The R_b extraction uses rb_results.json values. Must reconcile -- explain whether different calibration sets are used and why, or fix the inconsistency. |
| 8 | [D12b] four-quantity simultaneous fit not implemented, no formal downscoping | Critical [A8] | A | **B** | The four-quantity fit is a Phase 2 commitment. However, given the MC pseudo-data context (A_FB = 0 by construction), implementing the full four-quantity fit on symmetric MC would be a significant effort with limited diagnostic value -- the fit cannot meaningfully constrain sin^2(theta_eff) when the asymmetry is zero. The correct action is a formal [D] downscoping in COMMITMENTS.md documenting why the four-quantity fit is deferred to Phase 4b/4c where the real asymmetry is present. A silent replacement is wrong, but the fix is documentation (downscoping), not implementation. Downgrade to B. |
| 9 | C_b > 1.3 at WP 10.0 (C_b = 1.537) -- convention-required investigation missing | Critical [A9] | A | **A** | conventions/extraction.md is explicit: "C_b > 1.3 ... Identify which inputs cause the correlation." At WP 10.0, C_b = 1.537 (confirmed from correlation_results.json). The artifact provides qualitative explanation but no quantitative input-by-input decomposition. The convention language is unambiguous. |
| 10 | Committed validation tests missing: negative-d0 closure (a), bFlag consistency (b), production fractions, detector simulation | Critical [A10] | A | **A** | COMMITMENTS.md explicitly lists closure test (a) and (b). Neither is implemented. The artifact claims complete traceability, which is false. Must either implement or formally downscope with documented justification (3+ attempts). |
| 11 | F1: single-point "stability scan" -- not a scan | Plot val [VISUAL-A1] | A | **A** | RED FLAG from plot validator. Cannot downgrade. Additionally corroborated by Critical [A3]: only one valid extraction point exists. A figure labelled "stability scan" with one point is misleading. Fix: rename to "R_b extraction at reference working point" and acknowledge the scan was not achievable, or investigate why other WPs fail. |
| 12 | closure_test_phase4a: eps_c corruption insensitive (near-zero pull) | Plot val [VISUAL-A2] | A | **A** | RED FLAG from plot validator. Cannot downgrade. The Phase 4a CLAUDE.md requires corruption tests to FAIL. The eps_c +20% case produces null extraction (solver failure), which the critical reviewer notes is not the same as genuine sensitivity. The eps_c -20% case produces pull = -2.73 (does fail). So the +20% direction is a solver failure, not a demonstrated sensitivity. The finding stands: eps_c +20% corruption sensitivity is not demonstrated via genuine pull > 2. The overall 4/6 count is met, but this specific tautological case must be documented as a finding. |
| 13 | efficiency_calibration: experiment label text collision | Plot val [VISUAL-A3] | A | **A** | RED FLAG from plot validator. Cannot downgrade. The label collision makes the experiment label partially unreadable. Fix: reposition annotation text. |
| 14 | Multi-panel figsize violations: closure (1x2) and efficiency (1x3) both use (10,10) | Plot val [LINT-B1/VISUAL-A4] | A | **A** | RED FLAG from plot validator (rendering artifact causing content clipping). The template requires scaled dimensions for multi-panel figures. Fix: change to (20,10) and (30,10) respectively. |
| 15 | F2: chi2/ndf = 104.9/9 pathological, not addressed as finding | Plot val [VISUAL-B1] | B | **A** | Upgrading. The chi2/ndf ~ 10 for the A_FB^b angular fit is not merely a plotting concern -- it indicates the fit model does not describe the data. Per methodology/06-review.md section 6.3.3, p < 0.01 is Category A. Both reviewers flagged this. The artifact dismisses it without a formal Finding + Resolution section. The self-calibrating fit is even worse (chi2/ndf = 7.7-10.4, p = 0.0). Combined with [CP2], this is a genuine method validation failure that must be investigated. Merged with finding #2 above for resolution purposes, but the figure-level documentation is independently required. |
| 16 | F4: f_d/f_s trajectory below R_b = 0.200 curves, contradicts R_b = 0.280 | Plot val [VISUAL-B2], cross-figure | A (cross-fig), B (per-fig) | **B** | The plot validator raised this as cross-figure Category A and per-figure Category B. I assess this as Category B. The prediction curves in F4 use fixed efficiencies from a single working point (results[3]). The data trajectory traces a LOCUS of varying efficiencies across working points, not a constant-efficiency trajectory. The two are not directly comparable. However, the inconsistency IS confusing and must be explained in the figure or artifact. The fix is either: (a) add text annotation explaining why the data locus does not follow the constant-efficiency prediction curves, or (b) regenerate curves using WP-specific efficiencies. |
| 17 | F5: log scale or inset needed for subdominant systematics | Plot val [VISUAL-B3] | B | **B** | 12 of 13 bars are invisible at current scale. While the physics state (eps_uds domination) is correct, the figure fails its purpose of showing the breakdown. Add log-scale x-axis or inset. |
| 18 | eps_c +20% corruption: solver failure vs genuine sensitivity | Critical [B1] | B | **B** | The sensitivity claim via null extraction is weaker than via large pull. Document this distinction. The overall 4/6 passes but this case should be flagged as "solver failure" not "sensitivity demonstrated." |
| 19 | [D14] multi-WP extraction not achieved | Critical [B2] | B | **B** | Correctly deferred to Phase 4b where data multi-WP constraint is feasible. Must be explicitly noted as Phase 4b requirement. |
| 20 | Borrowed flat systematics (sigma_d0, hadronization, sigma_d0_form) | Critical [B3] | B | **B** | sigma_d0_form is cited as "scaled from MC statistics" which is the wrong source. Must correct the evaluation method or cite the correct source. sigma_d0 and hadronization scaling by 1.5x needs citation for the scaling factor. These are subdominant (< 0.001 each vs total 0.389) so do not block the physics conclusion, but the documentation must be correct. |
| 21 | F3 and F6 missing from FIGURES.json (committed flagship figures) | Critical [B4] | B | **B** | COMMITMENTS.md lists F3 (impact parameter significance) and F6 (per-year stability) as flagship figures. Neither produced. Must produce or formally remove from commitments with justification. |
| 22 | [D9] BDT cross-check not implemented or downscoped | Critical [B5] | B | **B** | Must formally downscope in COMMITMENTS.md with justification. |
| 23 | A_FB^b precision comparison misleading (0.87x on symmetric MC) | Critical [B6] | B | **B** | The comparison is meaningless when the signal is zero. Must add caveat that the ratio is not meaningful in Phase 4a. |
| 24 | Per-year consistency chi2 = 0.94/3 -- suspiciously low | Critical [B7] | B | **C** | Downgrading. The chi2 = 0.94 with p = 0.82 is within the acceptable range. The spread of R_b values (0.245-0.327) with individual sigmas of 0.06-0.085 is geometrically consistent with chi2 ~ 1. The suspicion of uncertainty overestimate is speculative without evidence. Document the number of valid toys per subset as a transparency measure, but this does not block. |
| 25 | [CP4] PDG-specific values not quoted | Critical [B8] | B | **C** | Downgrading. The physics_params systematic is subdominant (delta_Rb = 0.0002). While best practice requires specific values, the impact on the physics conclusion is negligible. Add specific PDG values to the JSON as a documentation improvement before commit. |
| 26 | A_FB chi2 coherence across F2 and F7 | Plot val (cross-figure) | B | **C** | The chi2 values refer to different quantities (angular bins vs kappa consistency). The apparent tension is resolvable: per-kappa A_FB^b extractions all have chi2/ndf >> 1 individually, but the EXTRACTED SLOPES are all consistent with zero, so the kappa-to-kappa consistency is excellent. This is not a contradiction -- it means the extraction is noisy but unbiased. Demote to documentation improvement. |

---

## Regression Check

Per methodology/06-review.md section 6.7 and the orchestrator regression checklist:

| Trigger | Status | Evidence |
|---------|--------|----------|
| Validation test failure without 3 documented remediation attempts | **YES** | Operating point stability (chi2=0/0, recorded as pass), chi2/ndf >> 5 on A_FB fits (no remediation attempts documented) |
| Single systematic > 80% of total uncertainty | **YES** | eps_uds systematic = 0.387 of total 0.389 = 99.5%. The artifact documents this but does not investigate whether it can be reduced at Phase 4a. |
| GoF toy inconsistency | **NO** | Per-year consistency p = 0.82, kappa consistency p = 0.95 -- both acceptable. |
| > 50% bin exclusion | **NO** | Not applicable (scalar extraction). |
| Tautological comparison presented as validation | **PARTIAL** | Operating point stability passes=true with chi2=0/0 is a tautological pass. eps_c +20% corruption sensitivity via solver failure is arguable. |
| Result > 30% relative deviation from well-measured reference | **YES** | R_b = 0.280 vs SM 0.216 = 30% deviation. On MC pseudo-data generated at SM, this is a method failure (circular calibration bias), not a statistical fluctuation. |
| Any [D] commitment violated without formal downscoping | **YES** | [D12b] four-quantity fit not implemented. [D9] BDT not implemented. [D14] multi-WP not achieved. |

**Multiple regression triggers are met.** However, the regression is to Phase 4a itself (iterate on the executor's work), not to an earlier phase. The calibration approach was set in Phase 2/3 and is the only feasible method without truth labels. The A_FB fit formula concern [CP2] traces to Phase 2 literature survey but the fix is at Phase 4a level (correct the implementation).

---

## Motivated Reasoning Check

The arbiter protocol requires checking whether the executor's narrative is self-serving. Assessment:

1. **"R_b = 0.280 is consistent with SM at ~2 sigma."** The central value is 0.280, the SM is 0.216, and the statistical uncertainty is 0.031. The pull is (0.280 - 0.216)/0.031 = 2.06. But this result is on MC GENERATED AT THE SM VALUE. A 2-sigma deviation from the generation truth is not "consistency" -- it is a bias measurement. The total uncertainty of 0.389 makes the pull trivially small (0.16 sigma), but that is because a single systematic (eps_uds, 99.5% of total) inflates the uncertainty to the point of meaninglessness. This is the textbook case described in the arbiter protocol: "A central value far from the reference that 'passes' a pull test due to inflated uncertainties is not a measurement -- it is a non-result dressed up as agreement."

2. **"The Phase 4a extraction successfully demonstrates the method infrastructure."** This framing shifts the goalposts from "produces expected results" to "demonstrates infrastructure." The phase requirement is to produce expected results, not to demonstrate that code runs. The extracted R_b = 0.280 with 138% relative systematic uncertainty does not constitute an expected result -- it is a diagnostic of method limitations.

3. **"Will be better constrained in Phase 4b/4c."** Multiple issues are deferred to Phase 4b: eps_uds constraint, multi-WP fit, C_b reduction, calibration at loose WPs. While some deferrals are legitimate (data-specific constraints), the aggregate effect is that Phase 4a presents results that are known to be invalid with promises of future improvement. The arbiter protocol warns against "will be addressed later without consequences for the current verdict."

**Conclusion on motivated reasoning:** The executor's narrative is partially self-serving. The framing minimizes the circular calibration problem, the catastrophic chi2 on A_FB fits, and the fact that the measurement has no resolving power. The results must be explicitly relabelled as method diagnostics / self-consistency checks, not physics results.

---

## Arbiter-Identified Issues (Not Raised by Either Reviewer)

**[ARB-1] Covariance matrix physically meaningless (Category B):**
The covariance matrix reports R_b uncertainty = 0.031 (stat) + 0.387 (syst) = 0.389 (total). With the dominant systematic being eps_uds at 99.5% of total, the covariance matrix is driven entirely by one source. The stat-syst decomposition and the off-diagonal correlations are rendered meaningless by this domination. The covariance matrix should carry a note that it reflects the eps_uds sensitivity, not the measurement precision.

**[ARB-2] n_valid_toys reporting gap (Category B):**
validation.json reports n_valid_toys = 25 (out of 1000) at WP 7.0 and n_valid_toys = 305 at WP 9.0. The number of valid toys at the primary extraction point (WP 10.0 on full MC) is not reported anywhere. If the convergence rate at WP 10.0 is also low, the quoted statistical uncertainty may be unreliable. Must report n_valid_toys for all extractions.

---

## Findings Priority List (for fixer agent)

### Category A -- Must Resolve (priority order)

1. **[A2/15] A_FB fit chi2/ndf >> 5 at all kappa.** Investigate the chi2 failure. Check [CP2] formula concern. Provide >= 3 remediation attempts. Present as formal Finding + Resolution in the artifact. If the formula cannot be fixed, document the limitation with evidence. This is the most important physics finding because it may indicate a wrong extraction formula that would bias the real-data result.

2. **[A1] Circular calibration relabelling.** Relabel Section 4 and the summary table. The heading must read "Calibration Self-Consistency Check" or equivalent. The text must explicitly state that R_b = 0.280 is the residual bias of a circular calibration, not a physics measurement. Add a Finding + Resolution section documenting the calibration independence violation per conventions/extraction.md.

3. **[A3] Fix validation.json operating_point_stability.** Set passes = false, add notes field explaining only one valid extraction point. Fix artifact Section 13 to consistently say FAIL (not "Limited").

4. **[A4] Attempt independent closure at WP 10.0 on validation split.** Run the 40% validation split extraction at WP 10.0. If it returns null, document with 3 remediation attempts. If it returns a value, report the pull.

5. **[A7] Reconcile eps_b = 0.238 (mc_calibration) vs 0.193 (rb_results) at WP 10.0.** Explain which value is used where and why they differ. If different calibration procedures produce different eps_b, this must be documented. Fix any inconsistency in the artifact's Section 2 table.

6. **[A6] Document alpha scan range.** Correct "closest to 0.10" to accurately reflect the scan range (starts at 0.20 per mc_calibration.json). Explain why no solutions exist at alpha < 0.20.

7. **[A9] C_b > 1.3 investigation.** Per conventions/extraction.md, identify which tag inputs cause the large hemisphere correlation. Quantify each input's contribution. The investigation need not be exhaustive -- a first-order decomposition (e.g., removing thrust or mass component and measuring C_b change) satisfies the convention.

8. **[A5] Write precision investigation artifact.** Produce `outputs/PRECISION_INVESTIGATION.md` explaining the 278x ratio. Content: (a) methodological differences (simplified tag vs 5-tag), (b) missing calibration sources (no truth labels, no per-hemisphere vertex), (c) MC statistics limitation, (d) comparison without eps_uds systematic = 9x (still large, but tractable).

9. **[A10] Address missing committed validation tests.** For closure tests (a) negative-d0 and (b) bFlag consistency: either implement or formally downscope with documented justification. For missing systematic sources (production fractions, detector simulation): either evaluate or downscope.

10. **[A11/F1] Fix F1 stability scan figure.** Rename to "R_b extraction at reference working point" or investigate why other WPs fail and extend the scan.

11. **[A12] Fix efficiency_calibration figure.** Reposition annotation text to avoid collision with experiment label. Change figsize to (30,10).

12. **[A13] Fix closure_test figure.** Change figsize to (20,10). Document the eps_c +20% null-extraction case as solver failure distinct from sensitivity.

13. **[A14] Multi-panel figsize corrections.** Apply to both closure and efficiency calibration figures.

### Category B -- Must Fix Before PASS

14. **[B-D12b] Formally downscope [D12b] four-quantity fit.** Add [D] entry in COMMITMENTS.md with justification: deferred to Phase 4b/4c where real asymmetry is present.

15. **[B16] F4 f_d/f_s explanation.** Add annotation or artifact text explaining why the data locus does not follow constant-efficiency prediction curves.

16. **[B17] F5 systematic breakdown.** Add log-scale x-axis or inset for subdominant sources.

17. **[B18] eps_c corruption documentation.** Document that eps_c +20% sensitivity is via solver failure, not genuine pull.

18. **[B19] Multi-WP deferral documentation.** Explicitly note in artifact that [D14] multi-WP fit is deferred to Phase 4b.

19. **[B20] Borrowed systematics documentation.** Correct sigma_d0_form evaluation method citation. Cite source for 1.5x scaling factor on sigma_d0 and hadronization.

20. **[B21] Missing flagship figures F3 and F6.** Produce or formally remove from COMMITMENTS.md.

21. **[B22] [D9] BDT downscoping.** Formally downscope in COMMITMENTS.md.

22. **[B23] A_FB precision comparison caveat.** Add note that 0.87x ratio is not meaningful on symmetric MC.

23. **[ARB-1] Covariance matrix note.** Add documentation that the matrix is dominated by eps_uds sensitivity.

24. **[ARB-2] Report n_valid_toys for WP 10.0 primary extraction.**

---

## Reviewer Diagnostic

### Critical Reviewer (ivan_f97c)

**Coverage assessment:** Excellent. The critical reviewer performed a thorough two-pass audit covering: (a) JSON vs artifact consistency, (b) convention coverage, (c) decision traceability, (d) cross-phase concern resolution, (e) external input audit, (f) completeness cross-check vs COMMITMENTS.md.

**Strengths:**
- Caught the operating point stability chi2=0/0 placeholder (Category A) -- this is exactly the kind of mechanical check the critical reviewer should catch.
- Identified the circular calibration as the central methodological issue with precise citation of the applicable convention.
- Traced the eps_b numerical inconsistency across three JSON files (Category A).
- Verified [CP2] cross-phase concern and connected it to the chi2 failure.
- Identified the alpha scan range documentation gap (Category A) -- deep investigation of mc_calibration.json.

**Gaps:**
- Did not catch the multi-panel figsize violations (plot validator's territory, not a gap for the critical reviewer).
- The per-year chi2 suspicion [B7] was speculative -- downgraded to C. The concern about uncertainty overestimate lacked evidence. MINOR COVERAGE CONCERN (not a gap, but the finding was not substantiated).

**Assessment: STRONG REVIEW. No coverage gaps within scope.**

### Plot Validator (fiona_7de9)

**Coverage assessment:** Thorough. All 8 figures reviewed. Registry check complete. Code lint complete. Cross-figure consistency checked.

**Strengths:**
- Caught the single-point stability scan as a Category A physics diagnostic (not just a visual issue).
- Identified the eps_c corruption insensitivity in the closure test figure -- this required reading the visual bar widths and interpreting the physics.
- Caught the experiment label text collision in the efficiency calibration figure.
- Cross-figure consistency check (F4 vs R_b extraction) was insightful.
- Figsize violations caught via both code lint and visual review.

**Gaps:**
- The f_d/f_s cross-figure inconsistency was raised as Category A but is actually explainable (different efficiency loci). The plot validator did not consider the constant-efficiency vs varying-efficiency interpretation before escalating. MINOR -- the finding was correctly flagged even if the severity was slightly high.
- Did not catch the self-calibrating fit chi2/ndf (7.7-10.4) which is much worse than the simple_fit chi2/ndf (8.9-12.7) reported in the figure. The figure shows only the simple_fit results. The plot validator reviewed what was visible in the figures but the underlying JSON had worse numbers. This is at the boundary of plot validator scope (JSON values are critical reviewer territory).

**Assessment: STRONG REVIEW. No significant coverage gaps within scope.**

---

## Verdict: ITERATE

**Rationale:**
- 14 Category A findings remain unresolved (10 from critical reviewer, 4 from plot validator including RED FLAGs).
- 11 Category B findings require fixes.
- Multiple regression triggers are met (chi2/ndf >> 5, single-systematic > 80%, result > 30% deviation from truth, [D] commitments violated).
- The motivated reasoning check reveals the results are framed as physics measurements when they are method diagnostics.

**The regression is within Phase 4a** -- iterate on the executor's work. No regression to Phase 2/3 is warranted because:
- The calibration approach (assuming SM R_b) was the only feasible option without truth labels. The problem is documentation, not methodology.
- The A_FB fit chi2 issue is a Phase 4a implementation question ([CP2] formula), not a Phase 2/3 strategy failure.
- The missing validations and figures are Phase 4a executor deliverables.

**The fixer agent must address ALL Category A findings (items 1-14) and ALL Category B findings (items 14-24) in the priority list above.** Category A items are ordered by physics impact. The most critical fix is investigating the A_FB chi2 failure (#1), as this may indicate a fundamentally wrong extraction formula that would propagate to Phase 4b/4c.

Doc 4a MUST NOT begin until this review passes.
