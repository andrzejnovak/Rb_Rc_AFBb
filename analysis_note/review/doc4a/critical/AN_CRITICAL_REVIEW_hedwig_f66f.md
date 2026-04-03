# Critical Review — Analysis Note Doc 4a v2 (FRESH)
## Reviewer: hedwig_f66f
## Date: 2026-04-02
## Artifact: `analysis_note/ANALYSIS_NOTE_doc4a_v2.tex` + compiled PDF
## Prior review: valentina_2dba (v1), arbiter zelda_65ac, fixer emeric_602f, verifier vera3_fbef
## MCP_LEP_CORPUS: true

---

## PASS 1 — METHODOLOGY / VALIDATION AUDIT (JSON vs AN Claims)

### P1.1 — Chi2/p-value cross-check: JSON vs AN

**Kappa consistency** (`analysis_note/results/validation.json`, field `kappa_consistency`): chi2 = 0.7089, ndf = 4, p = 0.9502. AN §6.2 states "chi2/ndf = 0.71/4 (p = 0.95)." MATCHES.

**Per-year consistency** (`validation.json`, field `per_year_consistency`): chi2 = 0.9377, ndf = 3, p = 0.8163. AN §6.3 states "chi2/ndf = 0.94/3 (p = 0.82)." MATCHES.

**Operating point stability** (`validation.json`, field `operating_point_stability`): passes = false, n_valid_wp = 1. AN §12.3 states "WP stability: FAIL, 1/4 valid WPs." MATCHES.

**Independent closure WP 9.0** (`validation.json`, field `independent_closure.per_wp[1]`): R_b_extracted = 0.3471, pull = 1.9268, passes = true. AN §6.3 states "WP 9.0: R_b = 0.347, pull = 1.93 (pass)." MATCHES.

**Corrupted corrections** (`validation.json`, field `corrupted_corrections_sensitivity`): n_sensitive = 4, n_total = 6, passes = true. AN Table 6 states "4/6, PASS." MATCHES.

**Per-kappa chi2 (origin fit)** (`phase4_inference/4a_expected/outputs/afb_results.json`): kappa=0.3: chi2 = 80.54/9 = 8.95. AN Table `tab:afb_perkappa` reports 80.5/9. MATCHES (rounded).

**Per-kappa chi2 (intercept)** (`afb_results.json`): kappa=0.3: intercept chi2 = 25.685/8 = 3.211. AN Table `tab:afb_perkappa` reports 25.7/8. MATCHES.

### P1.2 — Primary closure test: ±20% corruption sensitivity

The test is present in `closure_stress_results.json` and documented in AN Table `tab:corrupted_corrections`. 6 perturbations tested; 4/6 show sensitivity (pull > 2). **PASS.**

### P1.3 — Zero-impact systematics: nominal-vs-varied overlay figures absent

The AN retains 7 flat/borrowed systematicss (sigma_d0, hadronization, sigma_d0_form, mc_statistics, physics_params, tau_contamination, selection_bias) without bin-dependent propagation figures. The previous review (valentina_2dba [A2]) flagged this. The fixer (emeric_602f) resolved the sigma_d0_form finding by citing ALEPH:VDET for the functional form. However, the underlying issue — that NO bin-dependent propagation was performed — was NOT resolved. The fix only added a citation for the functional form choice, not a demonstration that the shift is non-zero and bin-dependent.

**Status: PARTIALLY ADDRESSED.** The sigma_d0_form citation was added (finding [A2] declared FIXED by vera3_fbef for the citation sub-issue). But the core methodology requirement — "for every systematic shift: verify the shift is BIN-DEPENDENT" — remains unmet for all 7 flat systematics. The exception clause ("subdominant AND magnitude justified by cited measurement") applies only to sigma_d0 and hadronization explicitly. For sigma_d0_form, the cited source (ALEPH:VDET) provides the functional form, not the magnitude delta_Rb = 0.0004.

**New finding: see [A1] below.**

### P1.4 — Precision comparison

`validation.json precision_comparison.R_b_vs_ALEPH.ratio` = 283.18, investigation_required = true. AN Appendix §A.5 (Precision Investigation) decomposes 283x into four factors. Investigation artifact EXISTS and is detailed. **PASS on presence.** The narrative is internally consistent.

### P1.5 — Phase findings with Resolution sections

- Operating point stability failure: Section 12.3 documents 3 remediation attempts, all INFEASIBLE. **Resolution section EXISTS with 3 attempts.**
- Closure WP 10.0 INFEASIBLE: Documented in Section 6.4 with 3 attempt descriptions. However: see **[A2]** below — `rb_results.json` shows WP 10.0 closure PASSES, directly contradicting the AN.
- AFB chi2 >> 5: Resolved by intercept (Section 7.2/7.3). PASS.
- Circular calibration bias: Quantitative decomposition added (Section 8.1). PASS.

### P1.6 — C_b working-point consistency

**CRITICAL FAILURE.** The AN uses C_b = 1.179 as the nominal value in the systematic evaluation (`systematics.json`, field `R_b.C_b.C_b_nominal` = 1.1786). But the analysis runs at WP 10.0, where `correlation_results.json` (field `mc_vs_wp[threshold=10.0].C`) gives C_b = 1.5372. The value 1.1786 is the C_b at WP 5.0 (`correlation_results.json`, field `mc_vs_wp[threshold=5.0].C` = 1.1786). **The C_b systematic is evaluated at the wrong working point.** The AN's Table `tab:cb_values` correctly shows C_b(MC) = 1.537 at WP 10.0, but the systematic evaluation uses WP 5.0's C_b. **See [A3].**

### P1.7 — Operating point stability JSON vs AN

`rb_results.json` field `stability.passes` = true and `stability.chi2_ndf` = null; but `validation.json` `operating_point_stability.passes` = false. The rb_results.json shows only 1 valid extraction, chi2 = 0.0/0 (not computable). The validation.json correctly reports passes=false. The two JSONs are consistent. **No issue.**

**PASS 1 SUMMARY:** 3 significant issues found:
- P1.3: Flat systematics still lack bin-dependent propagation → [A1] (narrower scope than v1 [A2])
- P1.5 (partial): WP 10.0 closure claim contradicted by rb_results.json → [A2]
- P1.6: C_b evaluated at wrong working point → [A3]

---

## PASS 2 — STANDARD CRITICAL REVIEW

---

### [A1] CATEGORY A — sigma_d0_form systematic magnitude unsupported; the cited paper (ALEPH:VDET) establishes the functional form, not the numerical delta_Rb

**Evidence:** `systematics.json`, field `R_b.sigma_d0_form`:
```json
"method": "Scaled from MC statistics systematic (STRATEGY.md 8.2)",
"source": "STRATEGY.md Section 5.1"
```
The fixer replaced "STRATEGY.md Section 5.1" with a reference to `ALEPH:VDET` in the AN text (line 1058). But `ALEPH:VDET` is the ALEPH detector paper (inspect parameter paper 537303), which describes the VDET geometry and impact parameter resolution — it specifies the functional form sin(theta), NOT a published numerical delta_Rb value. The claimed `delta_Rb(sigma_d0_form) = 0.0004` remains without an independent measurement to back it.

The reviewer protocol states: "flat estimates are acceptable only when (a) the source is subdominant AND (b) the magnitude is justified by a cited measurement." Condition (b) is not met — ALEPH:VDET provides a detector description, not a measurement of how sin(theta) vs sin^{3/2}(theta) changes R_b by 0.0004.

The AN's text (line 1063): "The impact on R_b is evaluated by re-running the calibration with each form." If this were true, the method should be "Re-extraction with varied form" — but the JSON method field says "Scaled from MC statistics systematic." These are contradictory. Either the propagation was actually run (in which case the JSON method field is wrong) or the propagation was NOT run (in which case the AN text is wrong).

**Required action:** Clarify whether the delta_Rb = 0.0004 comes from (a) actual re-propagation through the analysis chain (if so, update JSON method field and report the shifted eps_b values), or (b) a borrowed/scaled value (if so, provide a published measurement for the magnitude). The current state contradicts itself.

---

### [A2] CATEGORY A — rb_results.json shows WP 10.0 closure PASSES (pull = 0.97) but AN declares "INFEASIBLE"

**Evidence from `phase4_inference/4a_expected/outputs/rb_results.json`:**
```json
"closure_test": [
  ...
  {
    "threshold": 10.0,
    "R_b_extracted": 0.2459177303197952,
    "R_b_truth": 0.21578,
    "sigma_stat": 0.031015158289246787,
    "pull": 0.9717097052586765,
    "passes": true,
    "N_tt": 14332
  }
]
```

The AN (Section 6.4, lines 1448–1468) declares three remediation attempts, all INFEASIBLE, concluding: "The WP 10.0 closure gap remains an acknowledged limitation."

The `rb_results.json` `closure_test[3]` at WP 10.0 shows a VALID extraction with pull = 0.97 (PASSES, < 2 sigma). The `closure_stress_results.json` (which populates `validation.json`) was written on 2026-04-02 16:34 before the re-run on 2026-04-03 03:06 that produced the current `rb_results.json`. The AN was updated after 05:28 (validation.json timestamp) but reports INFEASIBLE at WP 10.0 — inconsistent with the current rb_results.json.

Three possibilities:
1. The `rb_results.json` `closure_test` at WP 10.0 is the BOOTSTRAP closure (not independent), which would explain the contradiction. The AN's bootstrap attempt (attempt 3) says it recovers pull = 0.94. But `rb_results.json` shows pull = 0.972, which is close to 0.94 — this IS likely the bootstrap.
2. The re-run on Apr 3 03:06 changed the closure implementation and WP 10.0 now has a genuine independent closure that passes.
3. The `rb_results.json` contains a mislabeled bootstrap as "closure_test."

The AN's text for bootstrap: "Using 80% derivation and the full MC as 'validation' (deliberately circular as a diagnostic) recovers the full-MC result (R_b = 0.280, pull = 0.94 vs input 0.216)." But `rb_results.json` shows R_b_extracted = 0.246 (not 0.280) and pull = 0.972 — these are not the same. The extracted R_b of 0.246 is close to the WP 10.0 full-MC result, not 0.280. This suggests the `rb_results.json` `closure_test` at WP 10.0 may be using a different split (40% validation) than the bootstrap attempt described in the AN.

**This requires resolution.** If WP 10.0 closure genuinely passes on the standard 60/40 split, the AN's declaration of INFEASIBLE is false and the primary operating point has a valid closure test — which changes the conclusions. If it is the bootstrap (circular), the rb_results.json labeling is misleading and must be corrected.

**Required action:** Identify whether `rb_results.json` `closure_test[threshold=10.0]` corresponds to: (a) the 60/40 independent split — in which case INFEASIBLE is wrong and must be corrected with the actual closure result; (b) the bootstrap — in which case the JSON entry must be clearly labeled as "bootstrap (not independent)" and the parameters must match the AN's description (pull = 0.94, R_b = 0.280, not pull = 0.97, R_b = 0.246).

---

### [A3] CATEGORY A — C_b systematic uses WP 5.0 value (1.179) at an analysis running at WP 10.0 (where C_b = 1.537)

**Evidence:**
- `correlation_results.json` `mc_vs_wp[threshold=5.0].C` = 1.1786 — this is C_b at WP 5.0.
- `correlation_results.json` `mc_vs_wp[threshold=10.0].C` = 1.5372 — this is C_b at WP 10.0.
- `systematics.json` `R_b.C_b.C_b_nominal` = 1.1786305990748411 — this matches WP 5.0, NOT WP 10.0.
- `rb_results.json` `extraction_results[threshold=10.0].C_b` = 1.1786305990748411 — the extraction also uses the WP 5.0 C_b value at WP 10.0.
- AN Table `tab:cb_values` (line 840): "WP 10.0: C_b(MC) = 1.537" — correctly identified in the table.

The C_b at WP 10.0 should be 1.537, but the systematic evaluation uses C_b = 1.179 (WP 5.0 value). This means:

1. **The primary extraction uses wrong C_b.** The rb_results.json applies C_b = 1.179 at WP 10.0 — but the MC-measured value at WP 10.0 is 1.537. The extraction of R_b = 0.280 is computed with a C_b that is 0.358 too low. Since C_b enters the double-tag formula as a multiplicative factor on f_d, using C_b = 1.179 instead of 1.537 at WP 10.0 inflates f_d's contribution attributed to non-b backgrounds, biasing R_b.

2. **The systematic on C_b (delta_Rb = 0.010) is evaluated around the wrong nominal.** The variation 2x max(sigma_MC, |C_b_data - C_b_MC|) = 0.010 is computed at WP 5.0, not WP 10.0. At WP 10.0, the MC statistical uncertainty is sigma_C = 0.0098 and data-MC difference is |1.5065 - 1.5372| = 0.031. The correct variation would be 2 x max(0.010, 0.031) = 0.062, which is 6x larger than the reported 0.010.

The `correlation_results.json` `summary.reference_wp` = 5.0 and `C_b_nominal` = 1.1786 explicitly document that the "nominal" C_b was set to WP 5.0's value — a deliberate choice by the executor that was not documented in the AN as a limitation or justified by any physics argument.

**Quantitative impact estimate:** With |dR_b/dC_b| ~ 1.0 (from the AN's own analytical cross-check at line 982), the C_b error of 0.358 would produce Delta_R_b ~ 0.358. This is comparable to the dominant eps_uds systematic (0.387). The "biased" C_b therefore likely accounts for a significant portion of the 0.064 residual that the AN attributes to eps_uds mis-calibration.

**Required action:** (1) Correct the C_b nominal to 1.537 (the WP 10.0 measured value) in the extraction. (2) Recompute the C_b systematic variation using the WP 10.0 data-MC difference (0.031), giving delta_Rb(C_b) ~ 0.062. (3) Recompute the R_b extraction with correct C_b. (4) Update the bias decomposition in Section 8.1 to reflect the corrected C_b contribution. This may change R_b significantly and will affect all downstream systematic calculations.

---

### [A4] CATEGORY A — Intercept chi2/ndf still FAILS (3–4 across all kappa); the AN does not document what the intercept chi2 failure means for the extraction validity

**Evidence from `afb_results.json`:**
- kappa=0.3: intercept chi2/ndf = 25.685/8 = 3.21
- kappa=0.5: intercept chi2/ndf = 31.876/8 = 3.98
- kappa=1.0: (from AN Table line 1785): 34.4/8 = 4.30
- kappa=2.0: 31.5/8 = 3.94
- kappa=∞: 17.0/8 = 2.13

All kappa values except kappa=∞ have chi2/ndf > 3.0. The conventions criterion (extraction.md §3, "The stability scan must include fit quality... chi2/ndf > 3 is not a stable operating point") identifies chi2/ndf > 3 as indicating model failure.

The AN (line 1795): "The residual chi2/ndf ~ 3–4 in the intercept model likely reflects bin-level data/MC shape differences in <Q_FB> not fully absorbed by the linear model." This is an acknowledgment of model inadequacy, not a demonstration that the extracted A_FB^b is unbiased.

The reviewer protocol requires: "When selecting among multiple configurations, the selection criterion must balance precision and GoF. If the minimum-variance configuration has poor GoF while other configurations have acceptable GoF, the latter should be preferred unless the GoF failure is understood and demonstrated not to bias the result."

The AN has NOT demonstrated that chi2/ndf ~ 3–4 does not bias A_FB^b. The claim "likely reflects bin-level data/MC shape differences" is speculative. There are at least three alternative explanations: (a) the linear model is wrong (the true relationship is non-linear in cos_theta), (b) there are additional physics contributions (e.g., energy-dependent efficiency variation), (c) the weight normalization creates non-uniform bin errors.

At chi2/ndf = 4.3 for kappa=1.0, the probability is p = 0.0003 — decisively below any reasonable GoF threshold. The kappa=∞ value (chi2/ndf = 2.13, p = 0.03) is marginally acceptable but still below p > 0.05.

**Required action:** Demonstrate quantitatively that the chi2/ndf excess does not bias A_FB^b. Minimum required: (1) a goodness-of-fit study varying the angular binning (already noted "6, 8, 10, 12 bins tested" — report the chi2 at each), (2) a residual plot verifying no systematic cos_theta trend, (3) a statement of whether any kappa value achieves acceptable chi2/ndf. If no kappa value has acceptable chi2, this is a Category A method failure that must be declared, not rationalized as "bin-level shape differences."

---

### [B1] CATEGORY B — Kappa systematic (delta_AFB = 0.0022) uses spread across kappa = 0.3, 0.5, 1.0, 2.0 only — kappa=∞ excluded from systematic evaluation

**Evidence:** `systematics.json` `A_FB_b.charge_model.delta_AFB` = 0.002158690494398422, described as "Spread across A_FB^b values extracted at kappa = 0.3, 0.5, 1.0, 2.0." The AN text (line 1181): "Spread across A_FB^b values extracted at kappa = 0.3, 0.5, 1.0, 2.0" — explicitly excludes kappa=∞.

But the kappa consistency chi2 (ndf=4) is consistent with 5 kappa values (5 measurements minus 1 = 4 dof), and kappa=∞ IS included in the consistency test. If kappa=∞ is included in the test but excluded from the systematic evaluation, the spread (and hence systematic) is understated.

From AN Table `tab:afb_perkappa`: kappa=∞ gives A_FB^b = -0.002, kappa=0.3 gives 0.003. The range across all 5 kappa values is 0.003 - (-0.002) = 0.005, compared to 0.003 - (-0.002) = 0.005 for kappa 0.3–2.0 (the AN's reported delta_AFB = 0.0022 is the RMS, not the range). Including kappa=∞ (-0.002, which is slightly below the kappa=2.0 value of -0.002) may not change the RMS significantly, but this must be explicitly verified and documented.

**Required action:** Include kappa=∞ in the systematic calculation and report the revised delta_AFB(kappa) with all five values. Document whether the change is negligible.

---

### [B2] CATEGORY B — AN Table `tab:syst_summary_rb`: eps_c row claims delta_Rb = 0.078 but `systematics.json` records this as one-sided (downward only); the "fraction" column is "---" for eps_c but this source is 19% of the total systematic — omitting its fraction is misleading

**Evidence:** `systematics.json` `R_b.eps_c.delta_Rb` = 0.07816724158538715 (downward only; shift_up is null due to solver failure). The total systematic = 0.395.

The fraction column in Table `tab:syst_summary_rb` shows "---" for all sources except eps_uds (99.5%). But eps_c contributes 0.078/0.395 = 19.7% in quadrature. The AN notes eps_c is one-sided and uses the downward direction only; the upper uncertainty on R_b from eps_c is "unbounded" (line 1027–1028). This means the total systematic is ALSO one-sided — the "+1 sigma" bound on R_b from the total systematic is not properly defined.

The quadrature sum formula requires symmetric uncertainties. Using the one-sided eps_c value in a quadrature sum and presenting the result as a symmetric systematic (±0.395) is technically incorrect. The AN should present the eps_c systematic as one-sided and state that the total systematic has an asymmetric component.

**Required action:** (1) Report the eps_c contribution as one-sided in the budget table, with a note that the upper uncertainty from eps_c is unbounded. (2) State that the total systematic uncertainty is effectively one-sided: delta_R_b^{syst,down} = 0.395, delta_R_b^{syst,up} < 0.395 (dominated by the bounded sources only). The abstract and result table report "±0.395 (syst)" which is misleading when the dominant contribution has no meaningful upward bound.

---

### [B3] CATEGORY B — The AN's C_b analytical derivative cross-check (line 982) is internally inconsistent

**Evidence (line 979–983):**
```
From Equation eq:fd, partial f_d / partial C_b = eps_b^2 * R_b.
Using eps_b = 0.193 and R_b = 0.280:
partial f_d / partial C_b = 0.193^2 * 0.280 = 0.0104.
The propagation through to R_b gives
|dR_b/dC_b| ≈ delta_R_b / sigma_{C_b} = 0.010 / 0.010 = 1.0.
```

This cross-check uses eps_b = 0.193 from WP 10.0 (`rb_results.json` field `extraction_results[threshold=10.0].eps_b` = 0.193). But (as shown in finding [A3]) the systematic uses C_b = 1.179 (WP 5.0) as nominal. The cross-check is self-consistent in isolation (it recovers 1.0 as expected) but uses different working points for different quantities — it's mixing WP 10.0 eps_b with WP 5.0 C_b, confirming the mismatch is pervasive.

Furthermore, the analytical expression `|dR_b/dC_b|` is derived from `delta_R_b / sigma_{C_b}` = 0.010 / 0.010 = 1.0. If C_b were correct (1.537, sigma = 0.062 per [A3]), then `|dR_b/dC_b|` = delta_R_b(corrected) / sigma_{C_b}(corrected). With the corrected sigma ~0.062 and the same sensitivity, delta_R_b(C_b) ~0.062 — which is 6x larger than the reported 0.010 and would push C_b from subdominant to the second-largest systematic.

**Required action:** Redo the C_b derivative cross-check using the correct WP 10.0 values (C_b = 1.537, sigma_C_b = 0.062 from data-MC difference at WP 10.0). This is consequential, not decorative.

---

### [B4] CATEGORY B — The AN does not document why C_b was evaluated at WP 5.0 (the "reference WP") instead of WP 10.0 (the operating WP)

**Evidence:** `correlation_results.json` `summary.reference_wp` = 5.0, with comment `C_b_nominal` = 1.1786. No comment explains why WP 5.0 was chosen as the reference. The AN never mentions that C_b is evaluated at WP 5.0 — Table `tab:cb_values` shows C_b at WP 5.0 = 1.179 and WP 10.0 = 1.537 but doesn't explain which is used in the extraction. A reader would assume the operating WP (10.0) is used.

If there is a documented rationale for using WP 5.0 C_b in a WP 10.0 extraction (e.g., WP 5.0 has higher statistical precision and the correction is WP-independent by design), this must be explained explicitly in Section 4.4 (hemisphere correlation subsection). Currently absent.

---

### [B5] CATEGORY B — Stress test results in `closure_stress_results.json` show two tests with |pull| > 2 (FAIL); the AN does not report these as FAIL

**Evidence from `closure_stress_results.json` `stress_tests`:**
- R_c = 0.14 (extreme variation): pull = 2.46 — fails the < 2 criterion
- R_c = 0.20 (extreme variation): pull = 1.42 — passes
- C_b = 1.05 (alternative C_b): pull = -2.09 — fails the < 2 criterion

Two stress tests produce |pull| > 2. The AN does not document these results explicitly. The stress tests appear in `closure_stress_results.json` but are not referenced in the AN's Table `tab:validation_summary` (which lists only the contamination injection, closure, per-year, kappa, OP stability, d0 sign, angular fit, and mirrored significance tests — no stress tests).

The stress test at C_b = 1.05 (pull = -2.09) is particularly interesting in the context of finding [A3]: the extraction fails when C_b is reduced to the "correct" ALEPH value (~1.01), suggesting the current extraction is calibrated to the inflated C_b.

**Required action:** Report the stress test results in the AN (either in the validation table or as a dedicated subsection), document the criterion used, and explain why the R_c = 0.14 and C_b = 1.05 failures are acceptable (or investigate further).

---

### [C1] CATEGORY C — Abstract reports A_FB^b with 3-decimal precision ("−0.0001 ± 0.002 ± 0.004") but the v2 change log header says "A_FB^{0,b}" — verify observable label consistency

The abstract consistently uses A_FB^b (measured asymmetry) which is correct for Phase 4a. This is not the pole asymmetry A_FB^{0,b}. Consistent throughout the abstract and summary table. No issue in the current text. Noted for completeness.

---

### [C2] CATEGORY C — Systematic summary table `tab:syst_summary_rb` last row before Total: C_b, R_c, sigma_d0 etc. have "---" in the Fraction column, but their fractions sum to ~0.5% (non-negligible when combined). Consider reporting "< 0.1%" for each subdominant source for completeness.

---

### [C3] CATEGORY C — Validation table `tab:validation_summary` row "Angular fit chi2 (intercept)": reports chi2/ndf = 26–34/8 with result "FAIL (chi2/ndf ~ 3–4)." The criterion column says "< 5." Since the values (3.2–4.3) are below 5, this should be labeled FAIL or BORDERLINE — not FAIL for all. At kappa=∞, chi2/ndf = 2.13 which passes the < 5 criterion. The table lumps all kappa values together in one row. Consider reporting per-kappa or noting that kappa=∞ passes while others fail.

---

### [C4] CATEGORY C — `covariance.json` `stat_covariance` diagonal: sqrt(9.31e-4) = 0.0305, which matches `parameters.json` `R_b.stat` = 0.0305. Check confirmed. The covariance matrix is consistent with the reported uncertainties.

---

## Numerical Self-Consistency Spot-Checks

**Check 1:** `parameters.json` `R_b.syst` = 0.3952801661342814. From `systematics.json`: quadrature sum of all sources: sqrt(0.387^2 + 0.078^2 + 0.010^2 + 0.008^2 + 0.00075^2 + 0.00045^2 + 0.0004^2 + 0.0004^2 + 0.0002^2 + 0.00017^2 + 0.00011^2 + 0.0001^2 + 0.00005^2) = sqrt(0.14977 + 0.00608 + 0.0001 + 0.000064 + ~0) = sqrt(0.15601) = 0.3950. Reported: 0.3953. Difference < 0.1%. **CONSISTENT.**

**Check 2:** AN abstract: "R_b = 0.280 ± 0.031 (stat) ± 0.395 (syst)." `parameters.json`: value = 0.27975, stat = 0.030516, syst = 0.39528. Rounded correctly to 3 significant figures. **CONSISTENT.**

**Check 3:** AN line 1362–1364: "combined A_FB^b = −0.0002 ± 0.0022 with chi2/ndf = 0.71/4 (p = 0.95)." `parameters.json` `A_FB_b.stat` = 0.002158690494398422 ≈ 0.0022. `validation.json` `kappa_consistency.chi2` = 0.7089, p = 0.9502. The AN states "0.0022" but the stat = 0.002159 is correct. The value is from the combined kappa fit, not the individual. **CONSISTENT** (within rounding).

**Check 4:** `systematics.json` `R_b.C_b.C_b_nominal` = 1.1786305990748411 vs `correlation_results.json` `mc_vs_wp[threshold=5.0].C` = 1.1786305990748411. **Exact match.** This confirms C_b nominal is the WP 5.0 value — the WP mismatch in [A3] is confirmed.

**Check 5:** AN line 1287: "delta_Rb(eps_uds) = 0.387 [99.5% of budget]." From systematics.json, delta_Rb(eps_uds) = 0.387. 0.387^2 / 0.395^2 = 0.1498/0.1560 = 96.1%. The AN claims "99.5%." But 0.387^2/total_syst^2 = 0.1498/0.1564 = 95.8%. **DISCREPANCY:** The AN claims 99.5% but the correct fraction is 95.8% (the eps_c contribution of 0.078^2 = 0.0061 contributes 3.9% of the systematic variance). The "99.5%" claim is wrong; the correct value is ~96%.

This discrepancy propagates to the abstract (which doesn't mention this figure) and the interpretation. While the dominant-systematic characterization is qualitatively correct, the reported 99.5% figure is quantitatively false. **See [B6].**

---

### [B6] CATEGORY B — eps_uds fraction of total systematic reported as 99.5% is incorrect; correct value is ~95.8%

**Evidence:** From `systematics.json`: eps_uds delta_Rb = 0.387; eps_c delta_Rb = 0.078. Quadrature: 0.387^2 = 0.14977; 0.078^2 = 0.00608; total syst^2 = 0.15594 (ignoring subdominant sources). eps_uds fraction = 0.14977 / 0.15594 = 96.0%. The AN (lines 944, 1293) claims "constituting 99.5% of the total systematic budget."

The error: if eps_c is included (which it is — it's in the quadrature sum), the eps_uds fraction is 95.8%, not 99.5%. The 99.5% would only be correct if eps_c were excluded from the budget. The AN includes eps_c in the quadrature total (0.395) but then computes eps_uds/total as 0.387/0.395 = 98.0% — which would be the ratio of magnitudes, not variance fractions. Neither 98.0% nor 99.5% is the correct "fraction of variance."

**Required action:** Report the correct variance fraction: eps_uds contributes ~96.0% of the total systematic variance, with eps_c contributing ~3.9%. Alternatively, report eps_uds as the dominant source at 98% of the linear total (0.387/0.395 = 98.0%). Chose one convention and apply it consistently.

---

## Decision Label Traceability [D] Audit

The COMMITMENTS.md is now updated (per emeric_602f, verified by vera3_fbef). Spot-checking key decisions:

- **[D1] LEP EWWG observable definitions:** Implemented. Equations 1–3 use standard definitions. PASS.
- **[D2] Double-tag hemisphere counting:** Implemented (Equations 4–5). PASS.
- **[D4] Hemisphere jet charge for A_FB^b:** Implemented (Section 4). PASS.
- **[D5] kappa = {0.3, 0.5, 1.0, 2.0, ∞}:** Table `tab:afb_perkappa` now includes kappa=∞. PASS.
- **[D7] sigma_d0 from negative tail calibration:** Implemented. PASS.
- **[D12] Self-calibrating fit for A_FB^b with chi2/ndf:** Implemented (intercept model). BUT: chi2/ndf fails (see [A4]). CONCERN.
- **[D13] Toy-based uncertainty propagation:** Implemented. PASS.
- **[D14] Multi-working-point extraction:** Promised as Phase 4b deliverable. Acceptable deferral.
- **[D17] Primary vertex investigation:** Documented. Scope documented as infeasible for Phase 4a. PASS.
- **[D19] d0 sign convention validation:** Gate PASSED (ratio = 3.34 > 1). PASS.
- **[D12b] Four-quantity simultaneous fit:** Downscoped; risk note added to Section 10. PASS on process.

**New concern on [D8] Combined probability-mass tag:** The AN uses this tag but Table `tab:working_points` shows f_s at WP 10.0 = 0.172, f_d = 0.044 on DATA. The AN abstract and Section 4 state "MC pseudo-data" for Phase 4a — but the working points table uses 991,373 N_t and 128,206 N_tt which are large (Phase 4a should use MC counts, not full data counts). From Section 4.3.1 lines 729–730: "Measuring f_s and f_d at the chosen working point (from MC pseudo-data at Phase 4a; from real data at Phase 4b/4c)." Table `tab:working_points` has N_t = 991,373 — the MC has 730,365 events after selection (Table `tab:cutflow`). N_t = 991,373 > 730,365 MC events. **This means Table `tab:working_points` uses DATA counts.** See [A5].

---

### [A5] CATEGORY A — Table `tab:working_points` uses DATA counts for f_s, f_d, violating Phase 4a constraint (MC pseudo-data only)

**Evidence:**
- `phase4_inference/4a_expected/outputs/rb_results.json` `extraction_results[threshold=10.0].N_had` = 730365 (MC event count).
- AN Table `tab:working_points` WP 10.0: $N_t = 991{,}373$, $N_{tt} = 128{,}206$. 
- From `correlation_results.json` `data_vs_wp[threshold=10.0].N_tt` = 128206.
- From `correlation_results.json` `mc_vs_wp[threshold=10.0].N_tt` = 35715.

The MC double-tag count at WP 10.0 is 35,715. The data double-tag count is 128,206. The AN table's N_{tt} = 128,206 is the DATA value. The rb_results.json uses N_had = 730,365 (MC) for the extraction — these are consistent with MC. But Table `tab:working_points` reports DATA counts (N_t = 991,373, N_{tt} = 128,206) alongside f_s = 0.172, f_d = 0.044 — which are the DATA fractions (N_t / (2 * N_had_data) = 991,373 / (2 * 2,887,261) = 0.172).

The f_s and f_d used in the actual extraction (`rb_results.json`, WP 10.0) are: f_s = 0.17836, f_d = 0.04890. These match the DATA fractions (not the MC fractions). The MC fractions would be: f_s(MC) = 260,533 / (2 * 730,365) = 0.178, f_d(MC) = 35,715 / 730,365 = 0.0489. The values are numerically close (0.178 data vs 0.178 MC) because the MC replicates the data kinematics at WP 10.0.

But the N_t and N_tt in Table `tab:working_points` are clearly data counts — 991,373 tagged events cannot come from 730,365 total MC events (since each event contributes at most 2 hemisphere tags, the maximum MC N_t = 2 * 730,365 = 1,460,730; however at WP 10.0 only ~18% are tagged, giving N_t(MC) = 0.18 * 2 * 730,365 = 263,000 — far less than 991,373). Therefore the working points table reports DATA N_t and N_tt.

`conventions/extraction.md` §"Standard configuration": "The expected result must be computed on MC-generated pseudo-data counts, not on real data." `phase4_inference/4a_expected/CLAUDE.md`: "Data access: MC/Asimov pseudo-data only. No real data."

If the actual extraction uses data f_s and f_d (even if the values happen to be numerically similar), Phase 4a has violated the blinding protocol and is NOT computing expected results on MC pseudo-data.

**Investigation needed:** Determine whether the extraction used MC f_s/f_d (730,365 event denominator) or DATA f_s/f_d (2,887,261 event denominator). The f_s and f_d values are numerically similar, making this hard to distinguish from values alone. But the table's N_t = 991,373 > 730,365 total MC events is unambiguous: the table describes DATA counts.

**Required action:** (1) Confirm whether the WP 10.0 extraction in rb_results.json used MC or data N_had. The rb_results.json shows N_had = 730,365 which is the MC count — if this is correct, the extraction IS on MC pseudo-data, but the table's displayed N_t = 991,373 is mislabeled (it shows data-derived counts as a reference while the extraction used MC). (2) If the extraction used DATA, this is a blinding violation and requires full investigation and regression to Phase 4a with MC-only extraction. (3) Clarify in Section 4.3 whether f_s and f_d in the table are data-derived or MC-derived, and which was used for the actual R_b extraction.

---

## Completeness Cross-Check vs COMMITMENTS.md

**Systematic sources:** COMMITMENTS.md now has all systematic checkboxes marked [x] with Phase 4a values. Counting: 12 R_b sources + 4 A_FB^b sources = 16 total. AN Section 5 documents 12 R_b sources and 4 A_FB^b sources. Counts match conventions/extraction.md required categories. **PASS.**

**Validation tests:** COMMITMENTS.md:
- [x] Closure (c) contamination injection — documented
- [x] Parameter sensitivity table — Table `tab:sensitivity` present
- [x] Operating point stability — FAIL documented with 3 remediation attempts
- [x] Per-year consistency — PASS (p = 0.82)
- [ ] 10% diagnostic sensitivity — deferred to Phase 4b (acceptable)
- [ ] Negative d0 tail calibration — the unit-width validation (MAD*1.48 ~ 1.10) is documented in SELECTION.md but not in the AN
- [ ] Probability tag vs N-sigma tag comparison — COMMITMENTS.md shows [ ] for this cross-check; the AN Section 6.1 documents it briefly but it's not in the validation table

**Flagship figures:** COMMITMENTS.md: F1–F5, F7 all [x] with file names. F3 (impact parameter significance) and F6 (per-year stability) formally deferred [D]. Files exist on disk. **PASS.**

**Cross-checks (open items from COMMITMENTS.md):**
- [ ] Multiple kappa values — DONE (Section 6.2)
- [ ] Per-year extraction — deferred (Phase 4b)
- [ ] bFlag cross-check — deferred (Phase 4b)
- [ ] Constrained vs floated R_c — not done; listed as open [ ] in COMMITMENTS.md
- [ ] Multi-working-point extraction — deferred [D14]
- [ ] Analytical vs toy uncertainty comparison — minimum targets (C_b and R_c) must agree within 10%: the AN provides the analytical derivative for C_b (Section 5.2) but NOT for R_c. The R_c analytical check is absent. **See [B7].**

---

### [B7] CATEGORY B — Analytical vs toy uncertainty comparison for R_c is absent; COMMITMENTS.md minimum target not met

**Evidence:** COMMITMENTS.md: "Analytical vs toy-based uncertainty propagation comparison (minimum targets: C_b and R_c constraint propagation must agree within 10% between analytical and toy methods)." The AN provides the C_b analytical cross-check (Section 5.2, lines 977–984). The R_c analytical cross-check is absent — the AN only reports "delta_Rb(R_c) = 0.008 from re-extraction with varied R_c" (Section 5.3, a toy method). There is no analytical computation of dR_b/dR_c from the double-tag formula derivatives to verify this.

**Required action:** Provide the analytical derivative dR_b/dR_c from Equations eq:fs–eq:fd. The strategy commits to this minimum (COMMITMENTS.md, cross-check item on analytical comparison). The expected dR_b/dR_c is approximately -0.05 (from STRATEGY.md Section 4.3); with sigma_Rc = 0.003, the analytical delta_Rb = 0.05 * 0.003 = 0.00015. This does NOT agree within 10% with the toy result (0.008). The discrepancy must be investigated.

(Note: The AN reports dR_b/dR_c ~ -0.05 as the "sensitivity" in Section 5.3 line 999, but then reports delta_Rb(R_c) = 0.008. At sigma_Rc = 0.003, this requires |dR_b/dR_c| = 2.53 — inconsistent with the claimed ~0.05. The parameter sensitivity Table `tab:sensitivity` shows |dR_b/dR_c| = 2.53 from the systematics.json, while the strategy claimed ~-0.05. This 50x discrepancy must be explained.)

---

## Adversarial Stance Checks

**"This is a self-consistency diagnostic, not a measurement":** The AN repeatedly uses this framing to excuse the large R_b uncertainty and circular calibration. The framing is appropriate at Phase 4a. No concern.

**"Within N-sigma":** The R_b pull of 0.16 vs ALEPH is "within 0.16 sigma" — trivially within range due to enormous uncertainty. Correctly characterized as "uninformative" in the AN. **No concern.**

**"Expected on symmetric MC":** A_FB^b ~ 0 is claimed to validate the extraction because MC is symmetric. This is a legitimate Phase 4a validation. **No concern.**

**"Methods validation, not a competitive measurement":** The AN correctly states Phase 4a produces expected results only. **No concern.**

**"Will be addressed in Phase 4b":** Used for per-year consistency, bFlag cross-check, D12b fit, and negative-d0 calibration. These are legitimate deferrals with concrete deliverables identified. **No concern.**

**Circular calibration:** Correctly identified and labeled throughout. The "self-consistency diagnostic" framing is appropriate and well-supported by the bias decomposition. **No concern.**

**dR_b/dR_c inconsistency (50x discrepancy noted above in [B7]):** The strategy said ~-0.05 but systematics give 2.53. If |dR_b/dR_c| = 2.53 (from actual extraction), the strategy estimate of -0.05 was wrong by 50x. This discrepancy should be explained — the double-tag formula structure makes |dR_b/dR_c| substantially larger than -0.05 once one accounts for the fact that R_c appears in both f_s and f_d and the extraction amplifies small shifts through the underdetermined system.

---

## What a competing group would have that we don't

1. MC truth labels → direct efficiency calibration, independent closure test at the primary WP
2. Per-hemisphere primary vertex → C_b ~ 1.01 instead of 1.5, order-of-magnitude smaller C_b systematic
3. 5-tag system → over-determined system, simultaneous constraint on all efficiencies
4. Particle identification → L and X tags, direct R_c measurement
5. Valid closure test at the operating point (WP 10.0) — currently unresolved (finding [A2])
6. Correct C_b at operating point (finding [A3])
7. GoF-acceptable angular fit (chi2/ndf < 2) at all kappa values (finding [A4])

Items 1–4 are fundamental limitations documented in Section 11–12. Items 5–7 are resolvable within the current framework.

---

## CLASSIFICATION

**Category A (must resolve, blocks advancement):**
- [A1] sigma_d0_form method/magnitude contradicts itself
- [A2] WP 10.0 closure status contradicted by rb_results.json (requires clarification of bootstrap vs independent)
- [A3] C_b systematic evaluated at wrong working point (WP 5.0 vs operating WP 10.0); extraction may use wrong C_b
- [A4] Intercept chi2/ndf = 3–4 not demonstrated to be unbiased; GoF failure unaddressed
- [A5] Table `tab:working_points` displays DATA counts (N_t = 991,373 > 730,365 MC events); must clarify whether extraction used MC or data f_s/f_d

**Category B (should address):**
- [B1] kappa=∞ excluded from kappa systematic evaluation
- [B2] eps_c one-sided systematic not propagated to total uncertainty asymmetry
- [B3] C_b analytical cross-check uses WP-mismatched values
- [B4] Rationale for C_b reference WP 5.0 undocumented
- [B5] Stress test results not reported in validation table; C_b = 1.05 and R_c = 0.14 stress tests fail
- [B6] eps_uds fraction of total systematic budget incorrectly reported as 99.5% (correct: ~96%)
- [B7] R_c analytical vs toy cross-check absent; 50x discrepancy in dR_b/dR_c not explained

**Category C (suggestion):**
- [C1] Observable label consistency — no action needed (already correct)
- [C2] Fraction column for subdominant systematics — fill in or note "< 0.1%"
- [C3] Validation table angular chi2 row conflates all kappa values — separate or note kappa=∞ passes
- [C4] Covariance consistency — PASS, no action

---

## OVERALL CLASSIFICATION

**(B) — ITERATE required.** The [A3] finding (C_b at wrong working point, affecting the primary extraction) and [A5] (data vs MC counts ambiguity) are the most serious: [A3] could invalidate the R_b extraction result and its bias decomposition, and [A5] could indicate a blinding violation. These must be resolved before the AN can pass review. The [A4] finding (chi2/ndf failure unaddressed) is a persistent issue from the v1 review that was partially fixed but not fully resolved. The total of 5 Category A and 7 Category B findings indicates a document that needs a focused fix cycle before passing.

---

*Reviewer: hedwig_f66f | Date: 2026-04-02 | Session: Fresh review of AN v2*
