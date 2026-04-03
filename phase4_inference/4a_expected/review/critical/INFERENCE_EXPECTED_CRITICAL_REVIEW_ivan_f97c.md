# Critical Review: Phase 4a Inference — Expected Results

**Reviewer:** ivan_f97c (critical reviewer)
**Date:** 2026-04-02
**Artifact:** `phase4_inference/4a_expected/outputs/INFERENCE_EXPECTED.md`
**MCP_LEP_CORPUS:** true (available but not invoked — corpus calls would confirm published methodology details, but all critical findings below are grounded in the JSON artifacts, STRATEGY.md, conventions, and REVIEW_CONCERNS.md)

---

## Two-Pass Protocol

### PASS 1 — METHODOLOGY/VALIDATION AUDIT

#### 1.1 Validation JSON vs Artifact Claims

**Operating point stability — CRITICAL DISCREPANCY (Category A):**
`validation.json` records:
```json
"operating_point_stability": {"chi2": 0.0, "ndf": 0, "chi2_ndf": null, "p_value": 1.0, "passes": true}
```
`rb_results.json` records:
```json
"stability": {"chi2": 0.0, "ndf": 0, "chi2_ndf": null}
```
The artifact (Section 4, Section 13) claims "Operating point stability: Limited — Only WP 10.0 valid." Yet `passes: true` is asserted with chi2 = 0.0, ndf = 0, chi2_ndf = null. A chi2 of exactly 0.0 with ndf = 0 is not a fit result — it is a placeholder that was never computed. The stability scan uses only WP = 10.0 as "best" because 3 of 4 working points return R_b = null (no valid extraction). This is not a stable plateau — it is a single operating point. The validation JSON falsely records `passes: true` for a test that was never executed. The artifact text is more honest than the JSON; the JSON is wrong.

**Independent closure — JSON inconsistency (Category A):**
`validation.json` → `independent_closure.passes = true` based on `per_wp` entries for thresholds 7.0 and 9.0.
- WP 7.0: `R_b_extracted = null`, `pull = null`, `passes: false`
- WP 9.0: `R_b_extracted = 0.347`, `pull = 1.93`, `passes: true`

The closure JSON in `closure_stress_results.json` corroborates: WP 7 fails, WP 9 passes with pull = 1.93. The overall `passes: true` verdict requires 1/2 WPs to pass, which is met — but the JSON field `n_valid_toys: 25` for WP 7.0 in `validation.json` raises a flag: only 25 of 1000 toys converged. The artifact does not report this (the 25 valid toys vs 1000 attempted). If 97.5% of toys fail at WP 7, that is a method failure, not a closure pass boundary. The artifact cites the pull for WP 9 as 0.97 (from closure_stress_results.json line matching) but the independent validation JSON shows pull = 1.93 at WP 9.0 and no extraction at WP 10.0 in the validation set. The rb_results.json closure_test shows WP 10 extraction from the full MC (not the validation split) gives pull = 0.97. The artifact conflates the full-MC extraction (pull 0.97, WP 10) with the independent closure on the validation split (pull 1.93, WP 9). The independent closure at the operative working point (WP 10) does NOT appear in the independent closure results — it was never run on the validation half at WP 10, possibly because the validation half returns null.

**Self-calibrating fit chi2/ndf — severe failure not reported (Category A):**
The A_FB^b `self_calibrating_fit` chi2/ndf values in `afb_results.json`:
- kappa 0.3: chi2/ndf = 298.6 / 39 = **7.66** (p = 0.0)
- kappa 0.5: chi2/ndf = 378.7 / 39 = **9.71** (p = 0.0)
- kappa 1.0: chi2/ndf = 404.5 / 39 = **10.37** (p = 0.0)
- kappa 2.0: chi2/ndf = 359.3 / 39 = **9.21** (p = 0.0)

All self-calibrating fits have chi2/ndf >> 1 with p-value = 0.0 (i.e., the model is catastrophically rejected). The artifact (Section 5) reports the `simple_fit` chi2/ndf values (80.5/9 = 8.95, etc.) and labels these "non-zero chi2 reflects statistical fluctuations." But the self_calibrating_fit chi2 values are much worse. The `conventions/extraction.md` (Section 3, stability scan) requires: "The stability scan must include fit quality. A configuration that produces a small statistical uncertainty but poor GoF (chi2/ndf > 3) is not a stable operating point." The self-calibrating fit has chi2/ndf > 7 at every kappa — yet the artifact presents these as valid extractions with no investigation.

Furthermore, the `simple_fit` chi2/ndf values are themselves alarming:
- kappa 0.3: 80.5/9 = 8.9
- kappa 0.5: 104.9/9 = 11.7
- kappa 1.0: 114.5/9 = 12.7
- kappa 2.0: 101.5/9 = 11.3

These are all far above chi2/ndf > 5, which the physics sanity checklist defines as a Category A red flag. The artifact dismisses this as "statistical fluctuations in the binned <Q_FB> distribution, not a model failure." This rationalization is unsupported — chi2/ndf ~ 10 across ten bins is not a fluctuation; it indicates either mis-modelling of the distribution or systematic bias in the mean Q_FB values. The reviewer's note from REVIEW_CONCERNS.md [CP2] already flagged concerns about the A_FB^b extraction formula; this evidence suggests the implemented formula does not correctly model the <Q_FB> vs cos(theta) relationship.

**Corrupted corrections sensitivity — tautological case not addressed (Category B):**
`closure_stress_results.json` shows C_b corruptions (+/-20% of C_b-1) produce pulls 1.57 and 0.34 — both passing closure. The artifact labels these "tautological." However, the eps_c +20% corruption ALSO produces `R_b_extracted = null, pull = null` with `sensitivity_validated: true`. A null extraction is not a demonstrated sensitivity — it is a solver failure. The artifact conflates "solver fails" with "closure test fails," which are not the same thing. If the solver fails due to the corruption, it may be that the corruption produces unphysical inputs rather than genuinely testing the test's sensitivity. The 4/6 criterion appears to be met, but 2 of the 4 "sensitive" tests involve either null extractions (eps_c +20%) or numerical runaway pulls (eps_uds +20%: pull = -14.6).

**Precision comparison — incomplete investigation artifact (Category A):**
`validation.json` records R_b ratio = 277.6x with `investigation_required: true` and explanation "simplified single-tag system, no per-hemisphere vertex, limited MC (1994 only)." The Phase 4a CLAUDE.md requires: "If ratio > 5x on same dataset, produce a mandatory investigation artifact explaining why." No such investigation artifact exists. The explanation in `validation.json` is a one-line string, not an investigation artifact. The CLAUDE.md states clearly this is mandatory.

#### 1.2 Closure Test Sensitivity — ±20% Corruption Test

The corrupted corrections test was run (closure_stress_results.json). The test demonstrates 4/6 sensitivity, meeting the >=4 criterion. However, as noted above, the eps_c +20% case produces null extraction (solver failure rather than genuine sensitivity) and the self-calibrating-fit chi2 issue means the method's nominal validity is already questionable. The sensitivity test's premise — that the nominal closure PASSES and corruptions FAIL — is partially violated: the nominal closure at WP 7 also produces null extraction.

#### 1.3 Systematic Bin-Dependence Check

The artifact provides R_b systematics as single delta values (systematics.json), not as bin-dependent shifts. For the eps_c and eps_uds systematics (which are "re-extraction" with a varied parameter), there is no shape measurement at stake (R_b is a scalar), so a single delta value is appropriate. However:
- `sigma_d0` systematic: delta = 0.00075, labeled "Scaled from ALEPH published (0.00050) x1.5." This is a flat borrowed systematic without demonstrated propagation.
- `hadronization` systematic: delta = 0.00045, "Scaled from published ALEPH systematic (0.00030) x1.5." Same issue.
- `sigma_d0_form` systematic: delta = 0.0004, "Scaled from MC statistics systematic." This is the wrong source — the sigma_d0 form systematic should come from actually varying the parameterization, not scaling from MC statistics.

For the eps_uds systematic: shift_up = -0.256 (R_b decreases when eps_uds increases by 50%), shift_down = +0.387 (R_b increases when eps_uds decreases by 50%). The asymmetry (0.256 vs 0.387) is correctly captured, and the quoted delta_Rb = 0.387 uses the larger. This asymmetry is expected and the approach is correct.

#### 1.4 Per-Finding Resolution Check

INFERENCE_EXPECTED.md has the following findings:
- Finding: eps_c is large (0.43-0.62) → Resolution given
- Finding: No solutions at WP < 7 → Resolution given
- Finding: C_b significantly exceeds published ALEPH value → Resolution given
- Finding: All slopes consistent with zero (A_FB^b) → Resolution given
- Finding: eps_uds systematic dominates → Resolution given

All findings in the artifact have Resolution sections. However, the chi2/ndf >> 1 in the simple_fit and self_calibrating_fit results are NOT presented as findings with resolutions — they are rationalized in-text. Given the magnitude (chi2/ndf > 8), this should be a formal finding with a Resolution section, not a parenthetical dismissal.

#### 1.5 Phase 3 Closure Chi2 Consistency

The per-year consistency test uses 4 random MC subsets (not actual years). The chi2 across subsets is 0.94/3 = 0.31, p = 0.82. The subsets show R_b values: 0.327, 0.308, 0.245, 0.253. The spread is 0.082 across four equal MC quarters. This is large relative to the nominal uncertainty of 0.031 at WP 10, suggesting the extraction is sensitive to MC sub-sample variation in a way that the quoted statistical uncertainty does not capture. A proper chi2 consistency test across subsets with individual uncertainties (each has sigma ~ 0.06-0.085 from the JSON) gives chi2 = 0.94, which is suspiciously low — a chi2/ndf of 0.31 when results span 0.245 to 0.327 with sigma ~ 0.07 suggests the individual uncertainties may be overestimated, inflating the chi2 denominator. This needs investigation.

---

**PASS 1 SUMMARY:**
- **Category A:** Operating point stability chi2 = 0/null recorded as PASS; self-calibrating fit chi2/ndf >> 5 at all kappa; mandatory precision comparison investigation artifact absent; independent closure at operative WP (10.0) not demonstrated on validation half
- **Category B:** eps_c +20% corruption registers as sensitivity via solver failure; sigma_d0 and hadronization systematics are borrowed flat values

---

### PASS 2 — STANDARD CRITICAL REVIEW

#### 2.1 Circular Calibration (Category A)

The calibration of (eps_b, eps_c, eps_uds) is performed by assuming R_b = R_b^SM = 0.21578 (from hep-ex/0509008) and R_c = R_c^SM = 0.17223 as "MC generation truth," then inverting the double-tag equations. R_b is then extracted using these calibrated efficiencies — and the result (R_b = 0.280) differs from the input SM value (0.216).

This is a textbook example of back-substitution calibration. The conventions/extraction.md states explicitly: "Deriving the correction by assuming the primary result equals a reference value (back-substitution) is a diagnostic, not a calibration." The calibration uses R_b^SM to derive eps_b, and then R_b is extracted using eps_b — this is not independent. The artifact acknowledges the extraction is biased (~2 sigma high) but frames it as expected from the underdetermined system, not as a calibration independence failure.

The calibration independence failure is a fundamental methodological problem, not a "Phase 4a limitation." The conventions file (extraction.md) is unambiguous: "Calibration independence is mandatory." Using SM R_b to derive the efficiency correction and then measuring R_b with that correction violates this requirement. A calibration so dependent on the SM assumption that it cannot even produce a neutral result (recovery of SM from MC pseudo-data) is categorically invalid.

The extracted R_b = 0.280 vs. SM = 0.216 on MC pseudo-data (which was generated at the SM value) is NOT a ~2 sigma deviation from SM — it is a measure of how badly the circular calibration is biased. The artifact partially acknowledges this ("bias from underdetermined calibration") but never explicitly states: "this is a circular calibration, not an independent measurement." The distinction matters because the result is presented in a result table alongside SM values as if it were a real measurement.

**This is the most important finding in the review. The result R_b = 0.280 ± 0.031 (stat) on MC pseudo-data is not a measurement of R_b — it is a measure of the residual bias in a circular calibration procedure. Presenting it as a physics result in a table is misleading, even in Phase 4a.**

#### 2.2 Decision Traceability [D] Labels

**[D12b] — Not implemented (Category A):**
STRATEGY.md [D12b] commits to: "Four-quantity simultaneous fit (Q_FB, delta, e^h, epsilon^e) with sin^2(theta_eff) as direct fit parameter (inspire_433746); DELPHI five-category chi2 fit as cross-check."
The Phase 4a extraction implements a `simple_fit` (linear regression of <Q_FB> vs cos(theta)) and a `self_calibrating_fit` (multi-threshold regression). Neither implements the four-quantity simultaneous fit for sin^2(theta_eff) as a direct fit parameter. sin^2(theta_eff) = 0.2500 is computed by inverting the SM formula for A_FB^{0,b}, not by fitting it directly.

The artifact says (Section 5): "Self-Calibrating Fit: Extracted from <Q_FB> vs cos(theta) in b-tagged MC events at multiple kappa values." This is the linear regression approach [D12], not the four-quantity fit [D12b]. The [D12b] commitment is silently replaced — this is Category A per the CLAUDE.md review rules ("A [D] label that was committed in Phase 1 but violated without a formal downscoping decision is Category A").

**[D5] kappa = {0.3, 0.5, 1.0, 2.0, infinity} — implemented:**
afb_results.json confirms kappa infinity is included. [D5] implemented. PASS.

**[D14] Multi-working-point extraction — partially implemented (Category B):**
[D14] commits to "multi-working-point simultaneous fit for method parity." The implemented extraction uses a single working point (WP = 10.0) for R_b because only WP 10.0 yields a valid extraction. The multi-WP framework is present in the code (rb_results.json has entries for WP 7-10) but produces null at 3/4 working points. The artifact defers the actual multi-WP simultaneous fit to Phase 4b. This is a partial implementation, and Phase 4a notes it as an open issue. Since the stated rationale (WP < 10 has no valid solution) is documented, this is Category B rather than A — but it is a significant gap: the multi-WP fit is the key technique for constraining eps_uds, and its absence is exactly why the eps_uds systematic dominates at 0.387.

**[D13] Toy-based uncertainty propagation — partially implemented (Category B):**
`rb_results.json` shows `n_toys = 1000` for the full MC extraction, but `n_valid_toys: 25` for WP 7.0 in the validation set. With only 25 convergent toys out of 1000, the toy-based uncertainty at WP 7.0 is unreliable. The artifact's statistical uncertainty of 0.031 at WP 10 comes from the 1000-toy extraction — how many valid toys at WP 10? The JSON does not report this number for the primary extraction, only for the closure test validation set. This is a reporting gap.

**[D9] BDT training with bFlag proxy labels — not implemented (Category B):**
STRATEGY.md [D9] commits to a BDT approach with bFlag proxy labels or self-labelling as one of the two selection approaches. Phase 4a uses the combined probability-mass tag from Phase 3 selection. There is no mention of BDT results, comparison to BDT, or documentation that the BDT approach was abandoned with a formal downscoping. COMMITMENTS.md has "Cut-based vs BDT tagger comparison" as an unchecked cross-check item. The artifact does not address this.

#### 2.3 [CP2] A_FB^b Formula — Prior Review Concern Not Resolved

REVIEW_CONCERNS.md [CP2] (from Phase 2 review, sigrid_16b8):
> "The simplified formula A_FB^b = (8/3)*<Q_FB>/(R_b*delta_b) in LITERATURE_SURVEY.md is inconsistent with the correct self-calibrating chi2 fit to 5 event categories (N, N_bar, N^D, N^D_bar, N^same) described in inspire_433746 Section 4. Phase 3/4 reviewers: verify that the implemented extraction uses the correct 5-category chi2 fit."

The implemented extraction (`afb_results.json`) uses:
1. A `simple_fit`: linear regression of mean <Q_FB> vs cos(theta) (NOT the 5-category chi2 fit)
2. A `self_calibrating_fit`: multi-threshold slope regression across b-tag working points

Neither is the 5-event-category chi2 fit to (N, N_bar, N^D, N^D_bar, N^same) described in inspire_433746. The prior concern [CP2] is NOT resolved. The catastrophic chi2/ndf > 7 in the self_calibrating_fit is consistent with using the wrong fit formula — the model does not describe the data at any kappa. This is not a minor formatting issue; it means the A_FB^b extraction method may be systematically wrong.

**The combination A_FB^b = -0.0002 ± 0.0022 has chi2/kappa = 0.70/4 (p=0.95), which looks good in isolation — but only because the underlying per-kappa A_FB^b values are all consistent with zero. Consistency with zero does not validate the method; it means the signal is not present (as expected on symmetric MC). The method's failure to model the <Q_FB> distribution (chi2/ndf >> 1) would cause a systematic bias in the slope extraction when the real asymmetry is present.**

#### 2.4 C_b Discrepancy — Convention Violation (Category A)

`conventions/extraction.md` states: "Values far from 1.0 (C_b < 0.8 or C_b > 1.3) indicate the classifier introduces correlations beyond the QCD effects. Identify which inputs cause the correlation and consider removing them — the loss in AUC may be small while the gain in C_b stability is large."

At WP = 10.0 (the operative point), C_b = 1.537 (MC) and C_b = 1.507 (data) per correlation_results.json. Both are well above 1.3. The convention requires an investigation: which inputs cause the correlation, and can they be removed? The artifact provides a qualitative explanation (no per-hemisphere vertex, event-level thrust) but does NOT perform the required investigation (quantifying each input's contribution to C_b inflation). The data-MC consistency for C_b (delta ~ 0.005-0.030 across WPs) is good, which validates the MC estimation of C_b — but it does not justify the magnitude of C_b.

Furthermore, the `mc_calibration.json` records `correlation_inputs: C_b = 1.01` (from hep-ex/9609005 Table 1, inflated 2x per [D17]). This is inconsistent with the measured C_b = 1.179 from correlation_results.json (which is also used in the extraction per rb_results.json). The mc_calibration.json `correlation_inputs` appear to be the published ALEPH value used for reference, not the value used in the extraction. But this is confusing and creates a documentation inconsistency: a reader of mc_calibration.json would incorrectly infer C_b = 1.01 was used in the derivation-set calibration.

#### 2.5 eps_b Values — Inconsistency Between Calibration Sets (Category A)

`mc_calibration.json` derivation_calibration WP 10.0: eps_b = 0.248
`mc_calibration.json` full_mc_calibration WP 10.0: eps_b = 0.238
`rb_results.json` best_wp WP 10.0: eps_b = 0.193

Three different eps_b values at WP 10.0:
- derivation-set calibration: 0.248
- full-MC calibration: 0.238
- extraction best_wp: 0.193

The artifact (Section 2) reports eps_b = 0.363, 0.278, 0.243, 0.238 for WPs 7-10 (matching full_mc_calibration). But rb_results.json reports eps_b = 0.193 at WP 10. The difference (0.238 vs 0.193) is 23%, which is large and unexplained. The NUMERICAL SELF-CONSISTENCY CHECK (mandatory at Phase 4a) requires: "For each systematic source, verify that the per-section subsection table, the summary table, and any discussion prose all quote the SAME numerical value." The eps_b discrepancy between the artifact table and the rb_results.json fails this check.

The artifact Table in Section 2 gives eps_b = 0.238 for WP 10.0. The rb_results.json best_wp gives eps_b = 0.193. The R_b extraction uses the best_wp values. These must be consistent.

#### 2.6 Figure F3 — Missing (Category B)

COMMITMENTS.md Flagship figures requires:
- F1: R_b operating point stability scan ✓ (present)
- F2: A_FB^b angular distribution ✓ (present)
- F3: Impact parameter significance distribution (signed d0/sigma_d0, data vs MC, log scale) — **MISSING from FIGURES.json**
- F4: Double-tag fraction vs single-tag fraction ✓ (present)
- F5: Systematic uncertainty breakdown ✓ (present)
- F6: Per-year stability — **MISSING from FIGURES.json**
- F7: A_FB^b kappa consistency ✓ (present)

F3 and F6 are committed flagship figures that do not appear in FIGURES.json or the figures directory. The artifact lists 8 figures (F1, F2, F4, F5, F7, S1-S3) but F3 (impact parameter significance) and F6 (per-year stability) are absent. The "per-year consistency" validation is reported numerically (chi2 = 0.94, p = 0.82) but no figure is produced. F3 is particularly important as it is the primary data/MC comparison of the b-tagging variable. Its absence means there is no visual validation of the core tagger input.

#### 2.7 Precision Comparison — A_FB^b Ratio Misleading (Category B)

The artifact claims A_FB^b precision ratio = 0.87x (better than ALEPH). This is correct numerically (our 0.0046 total vs ALEPH 0.0052), but the comparison is misleading. The ALEPH result measures the real A_FB^b = 0.09 on data. Our result measures A_FB^b = 0 on symmetric MC. The "uncertainty" we report is dominated by the charge model systematic (0.0022 from kappa spread) — which is MC-evaluated on symmetric data. When the real asymmetry is present, the extraction is harder (the slope is meaningful, the fit model must correctly describe the angular distribution). Claiming 0.87x precision parity with ALEPH based on MC pseudo-data where the signal is absent is not a meaningful comparison.

#### 2.8 [CP4] PDG Inputs Traceability (Category B)

REVIEW_CONCERNS.md [CP4]: "M_Z, Gamma_Z, B hadron lifetimes, and B hadron decay multiplicities are listed as 'NEEDS FETCH' in INPUT_INVENTORY.md. Phase 4a reviewers: verify all B physics systematic variations cite specific PDG 2024 values."

The physics_params systematic in systematics.json cites "PDG 2024, STRATEGY.md Section 7.1" with delta_Rb = 0.0002 via "Propagated from PDG uncertainties via efficiency variation." No specific B hadron lifetime values or decay multiplicities are quoted. While this systematic is subdominant (0.0002), the [CP4] concern about fetchable inputs is partially addressed but not fully — the specific PDG 2024 values for B lifetimes and decay multiplicities are not quoted in any JSON output.

#### 2.9 External Input Audit (Category A)

`conventions/extraction.md` (External Input Audit, mandatory at Phase 4a): For each quantity NOT measured from data, verify: (1) the artifact documents WHY it cannot be measured from this data, (2) a data-driven cross-check was attempted, (3) the published uncertainty is propagated as a systematic.

Key external inputs:
- **R_c = 0.17223 (SM value):** Documented why (no PID, [A5]) ✓. Data-driven cross-check: COMMITMENTS.md lists "Constrained R_c vs floated R_c in double-tag fit" — not implemented in Phase 4a, deferred. [D6] constrains R_c; the floated cross-check is a COMMITMENTS.md item still unchecked. The uncertainty propagation (delta_Rb = 0.008 from R_c variation) ✓.
- **alpha = eps_uds/eps_c "typical LEP value" ~ 0.10:** The chosen alpha is NOT the "typical LEP value of 0.10" — the actual alpha selected is 0.20 at WP 10.0 (2x the stated prior). The artifact states "The physical solution with alpha closest to 0.10 is selected" but mc_calibration.json shows the selected alpha = 0.20 at WP 10.0. The discrepancy between the stated prior (0.10) and the selected value (0.20) is 100%, and this selection is made without any justification for why 0.20 is the "physical" solution among 22 solutions in mc_calibration.json. The criterion "closest to 0.10" with the selected value being 0.20 requires explanation — at WP 10 with 22 solutions, was there no solution with alpha closer to 0.10?

Looking at mc_calibration.json WP 10.0 all_solutions: the listed solutions show alpha values at 0.20, 0.20, 0.21, 0.21, 0.22... The 22 solutions are all at alpha ≥ 0.20. If the solver scans from 0.20 upward, and the stated prior is 0.10, then either (a) there are no solutions at alpha ≤ 0.19, or (b) the alpha scan range does not extend below 0.20. The artifact does not document the alpha scan range. If the scan starts at 0.20, the "closest to 0.10" criterion is vacuous.

**This is a significant undocumented choice that directly affects the extracted eps_uds and thus the dominant systematic.**

#### 2.10 Operating Point Stability — Physical Failure Not Properly Characterized (Category A)

`conventions/extraction.md` (Operating point stability, Category A if fails): "The result must be flat within uncertainties — a dramatic variation indicates the measurement is not robust and the operating point is not in a stable plateau."

The stability scan result is:
- WP 7.0: R_b = null (no valid extraction)
- WP 8.0: R_b = null
- WP 9.0: R_b = null (in full MC extraction from rb_results.json)
- WP 10.0: R_b = 0.280

With only one valid extraction point, there is no "flat plateau" to demonstrate. The conventions file requires the result to be "flat within uncertainties over a range spanning at least 2x the optimized region." A single point trivially passes any consistency test but demonstrates nothing. The convention requires explicitly that an instability (dramatic variation) must be investigated — here we have a more extreme case: no variation is possible because only one point converges. This must be classified as a stability failure, not a pass.

The `validation.json` recording `chi2 = 0.0, ndf = 0, passes: true` for this test is therefore incorrect. The correct classification under conventions/extraction.md is: operating point stability test was not achievable (fewer than 2 valid extraction points), NOT "passes: true."

#### 2.11 Completeness Cross-Check vs COMMITMENTS.md

Counting systematic sources documented vs committed:
- COMMITMENTS.md systematic sources: sigma_d0, C_b/C_c/C_uds, eps_c/eps_uds, R_c, hadronization, physics params, angular efficiency, sigma_d0 form, detector simulation, tau contamination, selection bias, QCD correction, charge separation model, charm asymmetry.
- **Missing:** "MC efficiency model: reweight fragmentation parameters" — committed but not evaluated. This is separate from the hadronization systematic (which is scaled from published values, not evaluated by reweighting).
- **Missing:** "Production fractions: vary B+/B0/Bs/Lambda_b rates" — committed under Sample Composition but not in systematics.json.
- **Missing:** Detector simulation (d0 smearing study) — committed as systematic source but not implemented; only the sigma_d0 form variation is present.

Validation tests committed vs implemented:
- Closure test (a): negative-d0 pseudo-data test — NOT implemented. The implemented closure is the 60/40 split. The negative-d0 test was committed as closure test (a) in COMMITMENTS.md but is not present in the Phase 4a outputs.
- Closure test (b): bFlag=4 vs full-sample consistency — NOT implemented.
- Closure test (c): artificial contamination injection with known shift — implemented as "corrupted corrections sensitivity." ✓
- Parameter sensitivity table — NOT implemented. COMMITMENTS.md requires "|dR_b/dParam| * sigma_param for all inputs." systematics.json provides delta_Rb values (which is effectively this table), but it is not presented as a formal parameter sensitivity table per the extraction.md convention.
- 10% diagnostic sensitivity — explicitly Phase 4b, acceptable.

The declared completeness ("All required components from STRATEGY.md [D1]-[D19] are implemented") is inaccurate. At minimum 3-4 committed validation tests are absent.

#### 2.12 Cross-Phase Concern [CP1] — Closure Test Tautology Partially Addressed

REVIEW_CONCERNS.md [CP1] flagged that a same-MC-half split would produce pull ≈ 0 by construction. The implemented independent closure (60% derivation, 40% validation) is NOT the same MC half — it uses different event indices for derivation and validation. This is better than pure algebraic self-consistency.

However, the closure at WP 9.0 gives pull = 1.93 (near the 2-sigma threshold). The `conventions/extraction.md` notes: "If a closure test produces pull = 0.00 at every operating point, this is a red flag." The Phase 4a closure avoids the tautological case. [CP1] is adequately addressed at WP 9.0.

The remaining issue: the closure at the primary operating point (WP 10.0) is not demonstrated on the validation half. WP 10.0 closure result appears only in rb_results.json (full MC) with pull = 0.97. The validation-split closure at WP 10.0 returns null in closure_stress_results.json. This gap means the method's bias at the operative point is untested on independent data.

---

## Summary of Findings

### Category A — Must Resolve

**[A1] Circular Calibration — Fundamental Methodological Failure:**
The efficiency calibration assumes R_b^SM to derive eps_b and then extracts R_b using those eps_b values. This is back-substitution, not calibration. conventions/extraction.md (Calibration independence is mandatory) and methodology/06-review.md §6.8 Tier 2 classify this explicitly as "a diagnostic, not a calibration." The extracted R_b = 0.280 on MC pseudo-data (generated at SM R_b = 0.216) is entirely explained by the circular calibration — it cannot be interpreted as a physics result. The artifact must explicitly label Section 4 results as "Calibration Self-Consistency Check" rather than as a physics extraction.

**[A2] Self-Calibrating Fit Chi2/ndf >> 5 — Unreported Critical Failure:**
The A_FB^b self-calibrating fit produces chi2/ndf values of 7.7–10.4 at all kappa values (p=0.0). The simple_fit chi2/ndf = 8.9–12.7 (also all p≈0). Per the physics sanity checklist, chi2/ndf > 5 is a Category A red flag. The artifact dismisses these as "statistical fluctuations" without investigation. Cross-phase concern [CP2] (wrong formula) may explain this. Resolution requires: (1) checking whether the correct formula is implemented, (2) investigating the chi2/ndf failure mode, (3) presenting this as a formal finding with evidence and remediation attempts.

**[A3] Operating Point Stability — Falsely Recorded as PASS:**
`validation.json` records chi2=0.0, ndf=0, passes=true for the stability test. With only 1 valid extraction point, the stability test was not performed. conventions/extraction.md explicitly categorizes operating point stability failure as Category A. The correct JSON entry is passes=false with notes=insufficient_valid_wps. The artifact text (Section 13: "Limited — Only WP 10.0 valid") is inconsistent with the JSON verdict.

**[A4] Independent Closure at Operative WP (10.0) — Not Demonstrated:**
The independent closure on the 40% validation split produces null at WP 10.0. The only closure result at WP 10.0 is from the full MC (pull = 0.97), which is not independent of the derivation. The conventions require an independent closure test. The method's bias at WP 10.0 on an independent sample is unknown.

**[A5] Mandatory Precision Investigation Artifact — Missing:**
Phase 4a CLAUDE.md: "If ratio > 5x on same dataset, produce a mandatory investigation artifact." The ratio is 278x. No investigation artifact exists. The one-line explanation in validation.json is not an artifact.

**[A6] Alpha Selection Undocumented — Critical for eps_uds:**
The alpha scan range that determines eps_uds calibration starts at 0.20 (not 0.10 as stated). With the dominant systematic (eps_uds, delta_Rb = 0.387) determined by the calibrated eps_uds value, and the alpha selection being opaque, the entire systematic budget is built on an undocumented parameter choice. The scan range must be documented and the statement "closest to 0.10" must be corrected (actual selected value is 0.20).

**[A7] eps_b Numerical Inconsistency (0.238 vs 0.193 at WP 10.0):**
Section 2 table reports eps_b = 0.238 at WP 10.0 (matching full_mc_calibration). rb_results.json reports eps_b = 0.193. These are used in different parts of the extraction and must be reconciled. The mandatory self-consistency check fails on this value.

**[A8] [D12b] Four-Quantity Simultaneous Fit — Not Implemented:**
STRATEGY.md [D12b] commits to the four-quantity simultaneous fit (Q_FB, delta, e^h, epsilon^e) with sin^2(theta_eff) as a direct fit parameter. The implemented extraction is a linear regression of <Q_FB> vs cos(theta), not the committed four-quantity fit. sin^2(theta_eff) = 0.2500 is derived from A_FB^b via formula inversion, not fitted directly. This is a binding decision label violated without a formal downscoping.

**[A9] C_b > 1.3 — Convention-Required Investigation Missing:**
conventions/extraction.md: "C_b > 1.3 indicates the classifier introduces correlations beyond QCD effects. Identify which inputs cause the correlation." At WP 10.0, C_b = 1.537 (MC). No investigation of which inputs cause this is present. This is explicitly required by the applicable conventions.

**[A10] Committed Validation Tests Missing:**
COMMITMENTS.md validation tests (a) negative-d0 pseudo-data closure and (b) bFlag=4 vs full-sample consistency are not implemented. The artifact claims "All required components from STRATEGY.md [D1]-[D19] are implemented," which is false given these missing validation tests. Two additional missing committed systematic sources: production fraction variation and detector simulation d0 smearing study.

### Category B — Should Address

**[B1] eps_c +20% Corruption — Solver Failure vs Sensitivity:**
The corrupted_corrections sensitivity test records eps_c +20% as `sensitivity_validated: true` based on `closure_passes: false` — but this closure failure is due to solver breakdown (R_b_extracted = null), not a genuine chi2 failure. Sensitivity via solver failure is weaker evidence than sensitivity via pull > 2.

**[B2] [D14] Multi-WP Extraction Not Achieved:**
The multi-working-point simultaneous fit (binding commitment [D14]) is not implemented in Phase 4a. The eps_uds systematic dominates (0.387) precisely because the multi-WP constraint is absent. Must be implemented in Phase 4b or formally downscoped with a [D] revision.

**[B3] Borrowed Flat Systematics Without Propagation:**
sigma_d0 (delta = 0.00075, scaled from ALEPH x1.5), sigma_d0_form (delta = 0.0004, wrongly scaled from MC statistics), and hadronization (delta = 0.00045, scaled from ALEPH x1.5) are flat borrowed estimates. While subdominant to eps_uds, the sigma_d0_form systematic uses the wrong source (should be actual parameterization variation, not a multiple of the MC statistics systematic). The sigma_d0 and hadronization scaled estimates are potentially acceptable if documented as subdominant + infeasible to propagate, but the missing citation evidence for the 1.5x scaling factor is concerning.

**[B4] Figures F3 and F6 Missing from FIGURES.json:**
F3 (impact parameter significance, data vs MC) and F6 (per-year stability) are committed flagship figures per COMMITMENTS.md. Neither appears in FIGURES.json or the figures directory.

**[B5] [D9] BDT Cross-Check — Not Implemented or Downscoped:**
STRATEGY.md [D9] commits to BDT training. No BDT results or formal downscoping documentation exists in Phase 4a outputs.

**[B6] A_FB^b Precision Comparison Misleading:**
Claiming 0.87x precision relative to ALEPH is misleading on symmetric MC where the signal is zero. The statement should clarify that this comparison is not meaningful because the ALEPH statistical uncertainty was dominated by the finite asymmetry, not statistical noise.

**[B7] Chi2 = 0.94/3 Per-Year Consistency — Uncertainty Overestimate Warning:**
The per-year consistency chi2 = 0.94 with R_b values spanning 0.245-0.327 and individual sigmas of 0.06-0.085 is suspicious. If the individual toy-based uncertainties are overestimated (e.g., because many toys fail to converge), the chi2 would be artificially low. The number of valid toys per subset is not reported.

**[B8] [CP4] PDG-Specific Values Not Quoted:**
The physics_params systematic (delta_Rb = 0.0002) cites "PDG 2024" without quoting specific B hadron lifetime and decay multiplicity values. These values must be recorded in the JSON for reproducibility.

### Category C — Suggestions

**[C1]** The eps_c efficiency at WP 10.0 (0.431) is dramatically larger than typical LEP charm tagging efficiencies (~5% as mentioned in SELECTION.md Section 7.1). The artifact acknowledges this but should quantify the pull: if eps_c ~ 0.43 and R_c ~ 0.17, charm hemispheres contribute 0.43 * 0.17 = 0.073 to f_s — roughly 40% of the b contribution (0.193 * 0.216 = 0.042). This large charm contamination substantially increases the sensitivity to eps_c and the associated systematic.

**[C2]** The self-calibrating_fit results for kappa=infinity have `self_calibrating_fit: null`. The artifact claims five kappa values are used in the combination, but the self-calibrating fit at kappa=infinity is not performed. Only the simple_fit result enters for kappa=infinity. This should be explicit.

**[C3]** The covariance matrix records zero correlation between R_b and sin^2(theta_eff) in both stat and syst covariance. The prose says "10% R_b - A_FB^b correlation through shared b-tag efficiency dependence." This 10% off-diagonal element is present in the syst_covariance (rho = 0.088). The zero R_b/sin^2 correlation is physically expected (they are extracted from independent fits) — this is fine but should be stated.

**[C4]** The A_FB^b angular distribution figure (F2) is described but the chi2/ndf in the figure would show the catastrophically bad fit. A reader should understand immediately from F2 why the fit is not a good model of the distribution.

---

## Classification

**Overall: CATEGORY A — Must Resolve**

The Phase 4a extraction contains multiple Category A issues that collectively undermine the validity of the presented results. The two most fundamental are:

1. **Circular calibration (A1):** The extraction procedure is not an independent measurement. The results cannot be interpreted as physics results without explicit re-labelling as self-consistency diagnostics.

2. **Unreported self-calibrating fit failure (A2):** The A_FB^b extraction method produces chi2/ndf > 7 at every kappa, consistent with the prior review concern [CP2] that the wrong formula may be implemented. The method has not been validated to correctly model the <Q_FB> distribution.

Issues A3–A10 are individually Category A and must be resolved before Doc 4a begins. The doc phase would be built on wrong or missing results.

**Required actions before Doc 4a:**
1. Resolve A1: Relabel calibration results correctly. Document the circular calibration explicitly. Propose alternative calibration approach or formally document why no independent calibration is feasible.
2. Resolve A2: Investigate chi2/ndf failure in A_FB^b fits. Check [CP2] formula concern. Provide remediation attempts (at least 3 per spec).
3. Resolve A3: Correct validation.json operating point stability entry to passes=false.
4. Resolve A4: Demonstrate independent closure at WP 10.0 on the validation split, or document why it produces null and attempt remediation.
5. Resolve A5: Write mandatory precision investigation artifact.
6. Resolve A6: Document alpha scan range; correct "closest to 0.10" claim when selected value is 0.20.
7. Resolve A7: Reconcile eps_b = 0.238 vs 0.193 at WP 10.0.
8. Resolve A8: Implement [D12b] four-quantity fit or formally downscope with documented justification.
9. Resolve A9: Investigate and document C_b > 1.3 source.
10. Resolve A10: Implement committed validation tests (a) and (b), or formally downscope with 3+ documented remediation attempts each.
