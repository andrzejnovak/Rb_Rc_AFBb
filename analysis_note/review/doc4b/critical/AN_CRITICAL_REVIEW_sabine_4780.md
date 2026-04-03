# Critical Review — Doc 4b v1
## Reviewer: sabine_4780
## Date: 2026-04-02
## Artifact: `analysis_note/ANALYSIS_NOTE_doc4b_v1.tex` / `.pdf`

**MCP_LEP_CORPUS status:** `true` (per TOGGLES.md). Corpus queries available but not required for this pass; primary focus is numerical consistency, JSON vs AN cross-check, and convention coverage.

---

## PASS 1 — METHODOLOGY/VALIDATION AUDIT

*Read JSON artifacts + code cross-check before reviewing the AN narrative.*

### P1-A: JSON vs AN numerical consistency

**Finding 1 (Category A): Covariance matrix in Appendix B is stale — 3.6x wrong.**

`analysis_note/results/covariance.json` (the stated single source of truth) gives:

| Entry | JSON value | AN reports (App. B) | Discrepancy |
|-------|-----------|---------------------|-------------|
| V_syst(R_b, R_b) | 0.04311 | 0.156 | 3.6× too large |
| V_syst(R_b, A_FB) | 8.30e-5 | 1.58e-4 | 1.9× too large |
| V_total(R_b, R_b) | 0.04397 | 0.157 | 3.6× too large |
| V_stat(R_b, R_b) | 8.518e-4 | 9.31e-4 | ~9% off |

The systematic covariance value 0.156 = (0.395)², exactly matching the *pre-Doc-4a-v3* R_b systematic uncertainty before the C_b working-point mismatch was corrected. The Doc 4a v3 fix reduced the syst from 0.395 to 0.208 (0.208² = 0.043 ≈ JSON value). The covariance appendix was not updated after that fix. This is the classic post-fix-cycle regression: the summary table was updated but the appendix retains stale pre-fix values. A reader using the covariance matrix for combination purposes would compute errors 1.9–3.6× too large.

Evidence: `covariance.json` field `syst_covariance[0][0]` = 0.04311; AN equation (eq:syst_cov) states 0.156. `systematics.json` totals R_b syst = 0.2076, 0.2076² = 0.0431.

**Finding 2 (Category A): Independent closure WP 9.0 pull in validation table contradicts JSON and figure caption — two of three sources disagree.**

Three locations in the AN report the WP 9.0 closure pull:
- AN Section 6.2 text (line 1634): pull = 1.03
- AN Table 12 (validation summary, line 1756): pull = 1.03 (Indep. closure WP 9.0, PASS)
- AN Figure caption (closure_tests, line 3134): pull = 1.93

`validation.json`, field `phase_4a.independent_closure.per_wp[WP=9.0].pull` = **1.9268**.

The JSON and figure caption agree with pull = 1.93, consistent with near-boundary (< 2σ) PASS. The prose and validation table values of 1.03 are stale from a previous iteration, likely before the C_b correction moved the extraction. This is a direct AN-vs-JSON contradiction on a named validation metric.

Evidence: `validation.json` phase_4a.independent_closure WP=9.0 pull = 1.9268; AN text and Table 12 say 1.03.

**Finding 3 (Category A): AN claims WP 10.0 independent closure (pull = 1.06) but no such entry exists in validation.json.**

AN Section 6.2 (line 1635): "WP 10.0: R_b = 0.387, pull = 1.06 (PASS)."
AN Table 12 (line 1757): "Indep. closure (WP 10.0): pull = 1.06, PASS."

`validation.json` field `phase_4a.independent_closure.per_wp` contains exactly **two entries**: WP=7.0 (null extraction, passes=false) and WP=9.0 (pull=1.927, passes=true). There is no WP=10.0 entry. The JSON is the stated source of truth for validation results. Either the WP 10.0 closure was never run and recorded, or its result was written to a different artifact that does not appear in the JSON. An claimed PASS result with no JSON evidence is Category A: the reader cannot verify the claim.

Evidence: `validation.json` keys in `independent_closure.per_wp` = [{threshold: 7.0, R_b_extracted: null}, {threshold: 9.0, pull: 1.9268}]. No WP=10.0 entry.

**Finding 4 (Category A): Corrupted-corrections sensitivity count inconsistency: AN says 5/6, JSON says 4/6.**

AN Table 8 (corrupted corrections, line 1666): "Sensitive: 4/6 — Criterion (≥ 4/6): PASS". Wait — the table header says 4/6 but then:

AN Table 12 validation summary (line 1758): "Corrupted corrections — N sensitive — 5/6 — ≥ 4/6 — PASS."

`validation.json` `phase_4a.corrupted_corrections_sensitivity.n_sensitive` = **4**, n_total = 6.

So the main corrupted corrections Table 8 correctly states 4/6, but the validation summary Table 12 erroneously states 5/6. The JSON confirms 4/6. The validation table overstates the sensitivity count. Notably, 4/6 still PASSES the ≥ 4/6 criterion, so the verdict is not affected — but the stated metric is wrong in one table.

Evidence: `validation.json` phase_4a.corrupted_corrections_sensitivity.n_sensitive = 4; AN Table 12 says 5/6.

**Finding 5 (Category A): eps_b value for WP 10.0 is inconsistent across three locations in the AN.**

Three places in the AN cite the calibrated b-tagging efficiency at WP 10.0:
- Table 5 (calibrated efficiencies, line 868): ε_b = **0.238**
- Figure caption `efficiency_calibration_eps_b` (line 888): "At WP 10.0: ε_b = **0.151**"
- Section 12.3 (limitations, line 2827): "WP 10.0: R_b = 0.305, ε_b = **0.132**, C_b = 1.537"

Three values (0.238, 0.151, 0.132) for the same physical quantity at the same working point. This cannot all be correct. The Section 12.3 value (0.132) appears in the context of the operating point stability after the C_b correction, which is likely the most recent. The figure caption value (0.151) and Table 5 value (0.238) may be from earlier iterations. Readers relying on the efficiency value for any cross-check will get different answers depending on which section they read.

Evidence: Table 5 line 868, figure caption line 888, Section 12.3 line 2827 — three distinct values.

**Finding 6 (Category A): Stale field citation in AN text for Phase 4a R_b result.**

AN Section 8.1 (result prose, line 1917-1918): "from parameters.json (fields: R_b.value = **0.2798**, R_b.stat = 0.0292, R_b.syst = 0.2076)."

`parameters.json` field `R_b.value` = **0.3099**. The equation immediately above correctly states R_b = 0.310 (matching the JSON 0.310). The field citation 0.2798 is stale — it corresponds to the pre-C_b-correction extraction. The equation text is correct, but the explicit field citation is wrong. Any automated reader parsing the provenance annotation will read the wrong value.

Evidence: `parameters.json` R_b.value = 0.3099478; AN prose cites 0.2798.

**Finding 7 (Category A): eps_uds_nominal cited in AN Section 5.1 (0.0913) contradicts systematics.json (0.1195).**

AN Section 5.1 (line 1028): "The nominal ε_uds = 0.0913 (from systematics.json, field R_b.eps_uds.eps_uds_nominal) is calibrated from MC at WP 10.0."

`systematics.json` field `R_b.eps_uds.eps_uds_nominal` = **0.1195015**.

Discrepancy: 0.0913 vs 0.1195. Additionally, Table 5 (calibrated efficiencies) lists ε_uds = 0.086 at WP 10.0, a third value. The systematic section and the calibrated efficiency table are both nominally reporting WP 10.0 values but differ by ~30%. This suggests the systematics.json reflects a different working point or different analysis pass than the Table 5 calibration.

Evidence: `systematics.json` R_b.eps_uds.eps_uds_nominal = 0.11950; AN text says 0.0913; Table 5 says 0.086.

**Finding 8 (Category B): Precision ratio reported as three different values (150×, 278×, 283×) without explanation.**

Four references to the R_b precision ratio vs ALEPH appear in the AN:
- Section 8.5 (line 2452): "0.210/0.0014 = 150×" (Phase 4a, total/total comparison)
- Section 11.3 (line 2699): "278× precision ratio" 
- Section 12.1 (line 2762): "278× precision ratio versus ALEPH"
- Appendix D header (line 3180): "precision ratio of 283×"

The value 150× is computed from total uncertainties (0.210/0.0014). The 278–283× values differ and appear to come from different reference computations (possibly systematic-only comparison or from a different iteration). The Appendix D text says 283× but breaks it down starting from 283×, then says "Without this source, the total is 0.013, giving a 9× ratio" — this 283× → 9× path is internally consistent if using the stat-dominated ALEPH total of 0.0014 × (150/283 × 283) = complicated. The inconsistency is not explained.

Evidence: four occurrences of different ratio values in lines 2452, 2699, 2762, 3180.

### P1-B: Primary closure test — ±20% corruption sensitivity

The ±20% corruption sensitivity test was run (Table 8 present). The n_sensitive result from the JSON is 4/6, not 5/6 as stated in the validation summary table (Finding 4 above). The test result (4/6, PASS per ≥ 4/6 criterion) is confirmed.

**One of the six corruption scenarios (ε_c +20%) produces solver failure rather than a genuine pull.** The AN Table 8 explicitly notes "Not genuine pull — solver failure." A solver failure is not a sensitivity measurement — it is not clear whether the test is "sensitive" (pull > 2) or just "broken" (no solution). The AN correctly does not count this as a sensitive case, but n_sensitive = 4/6 means only 4 of 6 corruption directions produce meaningful pull measurements. The test criterion (≥ 4/6) is passed, but the ε_c +20% solver failure signals a structural brittleness of the extraction — not a sensitivity pass.

### P1-C: Zero-impact systematic — overlay figure check

ε_uds has delta_R_b = 0.000 in Phase 4a due to solver failure at both varied values. Per the mandatory reviewer protocol, a systematic with zero impact requires a nominal-vs-varied overlay figure with max|diff| reported. The AN provides text explanation (Section 5.1 discusses solver failure) and Table 9 (Appendix A) documents the zero shift. However, no figure shows the nominal R_b extraction vs the ε_uds-varied extraction — there is only the efficiency calibration curve (`efficiency_calibration_eps_uds.pdf`), which shows the efficiency value vs WP, not the R_b shift.

Given that the zero impact arises from solver failure rather than a genuine cancellation, a figure may be impractical. The text explanation is present. Classify as **Category B**: the AN should explicitly state "no figure possible; solver fails at both variations; Category A finding if this systematic later shows non-zero impact on data."

### P1-D: Precision comparison > 5x — investigation artifact

R_b precision ratio = 150× (Phase 4a) and 373× (Phase 4b). Both > 5×. Precision investigation documented in Appendix D (quantitative decomposition into 4 factors). `PRECISION_INVESTIGATION.md` was written at Phase 4a Fix iteration. This satisfies the requirement.

However, Appendix D item 1 (line 3184) cites ε_c as the dominant source giving the factor 283×, but the Phase 4b dominant source shifts to ε_uds (96% of budget). The Appendix D investigation was written for Phase 4a results and not updated with Phase 4b findings. The decomposition is therefore incomplete for the 10% data results.

**Category B**: Appendix D does not include the Phase 4b precision decomposition.

### P1-E: Findings from Phase artifacts — Resolution sections

All findings from Phase 3 and 4a documented in the AN have either Resolution sections (e.g., Section 7.1 for R_b bias, Section 7.8 for δ_b overestimation) or are formally downscoped in COMMITMENTS.md. No finding appears without a resolution or documented infeasibility.

**PASS 1 SUMMARY: 7 Category A findings, 2 Category B. Proceed to Pass 2.**

---

## PASS 2 — STANDARD CRITICAL REVIEW

### §1 Physics correctness and methodology

**Finding 9 (Category A): A_FB^b is reported as a measurement with a central value but the extraction method is known to be wrong by 8–22×.**

The AN reports A_FB^b = 0.0085 ± 0.0035 (stat) ± 0.0044 (syst) with a "2.4σ detection" of the asymmetry. Section 7.8 correctly identifies the δ_b overestimation as the root cause of a 10.9× suppression. The pull from ALEPH is cited as 13.5σ (though the numerical check gives ~11σ when combining uncertainties correctly — see below).

The issue is not that the AN documents the problem (it does, clearly). The issue is that the AN still reports the suppressed value as a physics result in:
- The abstract (lines 66-71)
- Table 4 (Results summary, line 2348)
- The conclusions (item 2, line 2568)
- Section 9.2 comparison table

Reporting a value that is admitted to be wrong by a known factor (8–22×) as a physics result, even with caveats, creates a misleading primary narrative. The abstract says the result is "suppressed 10× relative to the published ALEPH value due to an identified overestimation." A reader who trusts the abstract has a fundamentally wrong value for A_FB^b. The correct framing is: "The slopes are detected at 2.4σ; the A_FB^b value cannot be extracted until δ_b is corrected in Phase 4c."

The sin²θ_eff derived from the suppressed A_FB^b is marked "unreliable" in the abstract but still reported numerically (0.248 ± 0.0007, a 24σ pull from SM if taken at face value). These numbers should not be in Table 4.

**Category A**: A methodology-broken result should not appear in the results tables or abstract as a central value, even with caveats. The correct treatment is: report slopes (detected at 2.4σ), document the δ_b issue, state that A_FB^b and sin²θ_eff cannot be derived until Phase 4c.

**Finding 10 (Category A): 13.5σ pull from ALEPH cited but numerical computation is inconsistent with stated uncertainty.**

AN Section 7.2 and Table 4: "pull of 13.5σ" from ALEPH for A_FB^b.

Numerical check: ALEPH A_FB^b = 0.0927 ± 0.0052; our A_FB^b = 0.0085 ± 0.0056 (total).
Pull = (0.0927 - 0.0085) / √(0.0056² + 0.0052²) = 0.0842 / 0.00764 = **11.0σ**.
Using only our uncertainty: 0.0842 / 0.0056 = **15.0σ**.

The reported 13.5σ matches neither calculation. The AN does not document which uncertainty denominator is used. This is a quantitative claim that cannot be verified from the stated inputs.

Evidence: AN text line 2138; computed values above.

**Finding 11 (Category B): Title and abstract claim measurement of R_c, but R_c is an external input constrained to SM.**

The document title: "Measurement of R_b, R_c, and A_FB^b." The abstract: "R_c = Γ(Z → cc̄)/Γ(Z → had) are measured." But [D6] constrains R_c to the SM value with LEP uncertainty as a systematic. Section 9.4 correctly states R_c is constrained.

The title and abstract create false expectations. The analysis does not measure R_c — it uses R_c as a constrained external input. A referee will correctly flag this. The title should read "Measurement of R_b and A_FB^b in Hadronic Z Decays."

### §2 Validation completeness vs COMMITMENTS.md

**Finding 12 (Category B): Required analytical vs toy uncertainty cross-check not performed — COMMITMENTS.md minimum target violated.**

COMMITMENTS.md (Analytical vs toy-based uncertainty cross-check):
> "minimum targets: C_b and R_c constraint propagation must agree within 10% between analytical and toy methods"

The AN uses toy-based propagation for all uncertainties (D13). No analytical cross-check for C_b or R_c propagation appears in the AN, Appendix, or referenced artifacts. Section 4.2 provides an analytical derivative cross-check for C_b (∂f_d/∂C_b), which is a necessary but not sufficient substitute — it verifies the derivative, not the full propagation through 1000 toy experiments vs the analytical formula.

This minimum target was explicitly listed in COMMITMENTS.md and is not fulfilled.

**Finding 13 (Category B): Per-year extraction not performed on 10% data — validity of deferred rationale.**

COMMITMENTS.md per-year extraction: deferred with stated justification (10%/4 years ~ 72k events/year, σ_stat ~ 0.13, insensitive). This justification is reasonable. But the year labels ARE preserved in the preselected NPZ files (per COMMITMENTS.md item B9 from Phase 3 fix), making it technically feasible. At 72k events/year the stat uncertainty is indeed large, but the test would still provide a qualitative consistency check. The deferral to Phase 4c is acceptable given the statistical argument.

**No Category A** — justification for deferral documented and technically valid.

**Finding 14 (Category B): Simple counting A_FB^b vs self-calibrating cross-check not performed, with no deferral documentation.**

COMMITMENTS.md (cross-checks section): "[ ] Simple counting A_FB^b vs self-calibrating fit (self-calibrating is governing extraction; simple counting is cross-check only)"

This cross-check is listed in COMMITMENTS.md, not yet addressed, and not formally deferred in COMMITMENTS.md or the AN. The AN does not mention this cross-check explicitly. Unlike the per-year consistency, this item has no documented infeasibility or deferral rationale.

### §3 Numerical self-consistency (systematic tables)

**Finding 15 (Category A): 10% data R_b statistical uncertainty is ambiguous — two valid but contradictory values reported.**

The AN reports the 10% data R_b statistical uncertainty as:
- Abstract (line 64) and Section 8.4 eq:rb_10pct (line 2085): σ_stat = **0.066**
- Table 6 (syst_summary_rb_10pct, line 1426): σ_stat = **0.053** ("Combined 2 WPs")
- Table 4 (results_summary, line 2348): σ_stat = 0.066

The values 0.066 and 0.053 refer to different quantities: 0.066 is the statistical uncertainty at WP 7.0 only (`parameters.json` R_b_10pct.stat = 0.0663); 0.053 is the combined uncertainty from the 2-WP operating point stability combination (`systematics.json` phase_4b_10pct.rb_total.stat = 0.0529). Both values are in the JSON and both are valid, but they measure different things. The AN presents both without distinguishing which is the primary result. The combined stat (0.053) should be the primary — the stability combination is the point of the OP stability test. Using 0.066 (WP7 only) elsewhere is inconsistent with the 2-WP combination as the primary result.

Evidence: `parameters.json` R_b_10pct.stat = 0.06629; `systematics.json` phase_4b_10pct.rb_total.stat = 0.05293.

**Finding 16 (Category A): Validation summary table (Table 12) misclassifies the angular fit chi2 FAIL criterion.**

Table 12 lists:
- "Angular fit χ²/ndf (intercept): χ²/ndf = 26–34/8, Criterion < 5, Result: FAIL"

But χ²/ndf = 26/8 = 3.25 to 34/8 = 4.25 — these values do NOT exceed 5.0. The table states both the values AND the criterion, then marks it FAIL when the values satisfy the criterion. The table is internally self-contradictory: if the criterion is < 5 and the values are 3–4, the result should be PASS (or marginally concerning but not FAIL). If the actual rejection criterion is < 2 or < 1.5 (as might be appropriate for a good fit), that criterion is not stated.

This is a systematic-in-table inconsistency between the Criterion column and the Result column for the same row.

Evidence: Table 12 lines 1762-1763; χ²/ndf values 3.21–4.30 < 5.0.

### §4 Circular calibration and independence

**Finding 17 (Category B): Phase 4a R_b is labeled "circular calibration self-consistency diagnostic" but the precision investigation Appendix D does not make clear this is NOT a physics result.**

The AN correctly labels the Phase 4a extraction as a diagnostic throughout the document. However, the abstract reports it as a numerical result with uncertainties (line 59-60), and Table 4 results_summary presents it alongside the 10% data measurement in the same row format. A reader who skims the table without reading the detailed caveats will not immediately identify the Phase 4a column as a self-consistency diagnostic rather than a physics result. The table footnote does not clearly distinguish diagnostic vs measurement.

Per conventions/extraction.md §Standard configuration: "The expected result must be computed on MC-generated pseudo-data counts, not on real data." This is correctly implemented. The issue is presentation clarity in the primary summary table.

**Finding 18 (Category B): The δ_b fix path described in Section 9 (Outlook) is necessary for Phase 4c but lacks a feasibility verification.**

Section 9.1 (Phase 4c outlook item 1): "The self-calibrating fit must be modified to either (1) fit δ_b simultaneously from multiple tag purities (as ALEPH did), or (2) extract δ_b from MC truth (b vs b̄ hemisphere labels)."

Option (2) is infeasible given constraint [A1] (no MC truth labels). Option (1) requires extending the linear regression to multiple purity bins — this approach is described in inspire_433746 and is a substantial code change. The AN does not verify that sufficient statistics exist at multiple purity levels in the 10% subsample to disentangle δ_b from A_FB^b, nor does it confirm the method is being prepared for Phase 4c.

The 13.5σ (or 11σ) deviation from ALEPH for A_FB^b satisfies the regression trigger criterion (>2σ from well-measured reference). The δ_b fix is a binding obligation for Phase 4c, not an optional improvement.

### §5 Cross-phase concern re-checks (REVIEW_CONCERNS.md)

**CP1 (Closure test tautology):** Addressed. The AN correctly redesigned the closure tests (Section 6.3) using mirrored significance (code sanity check), 60/40 MC split (independent closure), and contamination injection. The mirrored-significance test is correctly labeled as a code sanity check, not an independent closure. **RESOLVED**, with the caveat on WP 10.0 closure (Finding 3 above).

**CP2 (A_FB^b extraction formula):** Partially addressed. [D12b] was formally downscoped; the AN uses a simplified linear regression with intercept. The δ_b overestimation (Section 7.8) is the direct consequence. The AN admits the limitation and plans the fix. **KNOWN ISSUE, documented** — the critical finding here is Finding 9 above (reporting the suppressed value as a result).

**CP3 (σ_d0 angular dependence):** Resolved. The AN uses sin(θ) for the 2D Rφ projection and includes sin^{3/2}(θ) as a systematic variation. **RESOLVED**.

**CP4 (PDG inputs):** Resolved. Section 5.8 cites PDG 2024 values for B-hadron lifetimes and decay multiplicities. **RESOLVED**.

### §6 Figure quality checks

The plot watcher protocol was invoked. The AN references Phase 3 figures (magnus_1207_20260402/3 vintage) and Phase 4 figures with consistent naming. No `plt.colorbar` misuse detected for the histograms reviewed (all 1D/2D distributions appear to be 1D in the AN). Figures are referenced in the text. The chi2/ndf values in Figure captions for the AFB fit match Table 3.

**Finding 19 (Category C): Figure caption for F2 angular distribution refers to χ² = 31.9/8 but this is the κ = 0.5 value from Table 3 — the caption should specify which κ.**

Line 2028-2034: "Figure showing multiple κ values with the fitted linear model" — but the caption cites a specific χ²/ndf without specifying the κ that produced it. Since different κ values give different χ²/ndf (25.7/8 at κ=0.3 to 34.4/8 at κ=1.0), the caption should clarify that 31.9/8 is for κ=0.5 only.

### §7 External input audit

The external inputs are documented in Table 1 (input provenance). For C_b: the AN uses C_b = 1.01 (published ALEPH) for the 10% data extraction. Decision [D20] documents the justification. The C_b = 1.01 assumption is an external input that dominates the R_b result on 10% data.

**Finding 20 (Category B): The C_b = 1.01 external assumption drives the entire 10% data R_b result, but no data-driven cross-check of this assumption is presented.**

The AN (line 2100-2105) states: "the R_b central value is not an independent measurement" — correctly. The C_b scan shows R_b varies from 0.196 to 0.332 as C_b varies from 1.01 to 1.06 at WP 7.0. This means the 10% data R_b is almost entirely determined by the choice of C_b. The AN does not attempt any data-driven bound on C_b from the 10% data to constrain this range.

Per conventions/extraction.md: "Each calibration must come from an observable that is independent of the primary result." The C_b = 1.01 assumption is borrowed from a different detector configuration (ALEPH per-hemisphere vertex). No data-driven consistency check is presented.

A cross-check such as: "what C_b value minimizes the residual in the double-tag equations on 10% data?" would constrain the range and bound the dominant uncertainty.

### §8 Adversarial stance checklist

**"Within N-sigma" rationalization check:** The 10% data R_b = 0.208 ± 0.523 is described as "consistent with SM at 0.12σ." The denominator (0.523) is so large that R_b = 0 would also be "within 0.4σ." This is a measurement with zero resolving power on R_b at Phase 4b. The AN acknowledges this in Section 8.4 ("total uncertainty (0.523) is 2.5× the central value"). The caveat is present but the abstract could emphasize more strongly that the R_b number carries no physics information.

**"Methods validation, not a competitive measurement" framing:** The AN uses this framing appropriately for Phase 4a. For Phase 4b, the R_b infrastructure validation claim is legitimate; the A_FB^b "2.4σ detection" claim is not — see Finding 9.

**Tautological validation check:** The Phase 4a calibration derives efficiencies by assuming R_b = R_b^SM, then extracts R_b — circular by construction. The AN is explicit about this (Section 12.1: "circular procedure"). The 60/40 closure split partially breaks this, but still uses the same SM-assumed efficiency derivation. This is a known structural limitation, not a hidden issue. **Documented correctly**.

### §9 Competing measurement comparison

"If a competing group published a measurement of the same quantity next month, what would they have that we don't?"

1. A non-circular δ_b extraction → valid A_FB^b value (we have: suppressed value)
2. Self-calibrated C_b from per-hemisphere vertex → R_b with resolving power (we have: external assumption dominating)
3. Multi-WP simultaneous fit with ε_uds constrained → R_b systematic < 0.1 (we have: 0.5)
4. Per-year consistency check with real year labels → validated temporal stability

All four items are known deficiencies — items 1, 3, 4 are planned for Phase 4c. Item 2 is infeasible with the archived data format.

---

## SUMMARY OF FINDINGS

### Category A (must resolve before Phase 4c advance)

| # | Finding | Location |
|---|---------|----------|
| 1 | Covariance matrix Appendix B is stale (pre-C_b-fix values) | App. B |
| 2 | Closure WP 9.0 pull = 1.03 in prose/table, but JSON and figure = 1.93 | §6.2, Table 12 |
| 3 | WP 10.0 independent closure claimed (pull=1.06, PASS) with no JSON evidence | §6.2, Table 12 |
| 4 | Corrupted corrections: Table 12 says 5/6, JSON and Table 8 say 4/6 | Table 12 |
| 5 | ε_b at WP 10.0 has three different values (0.238, 0.151, 0.132) across the AN | Table 5, Fig. caption, §12.3 |
| 6 | R_b.value field citation in §8.1 says 0.2798 (stale), JSON is 0.3099 | §8.1 |
| 7 | ε_uds_nominal: AN says 0.0913, JSON has 0.1195 | §5.1 |
| 9 | Suppressed A_FB^b (wrong by 8–22×) reported as central value in abstract/Table 4 | Abstract, Table 4 |
| 10 | 13.5σ pull from ALEPH unverifiable; numerical check gives 11σ or 15σ | §7.2 |
| 15 | 10% data R_b stat uncertainty is 0.066 vs 0.053 — two valid values, ambiguous primary | Abstract, Table 4, Table 6 |
| 16 | Table 12 validation marks χ²/ndf = 3–4 as FAIL against stated criterion < 5 | Table 12 |

### Category B (must address before final submission)

| # | Finding | Location |
|---|---------|----------|
| 8 | Precision ratio cited as 150×, 278×, 283× in different sections | §8.5, §11.3, §12.1, App. D |
| 11 | Title/abstract claim R_c "measurement" when it is an external constraint | Title, Abstract |
| 12 | Analytical vs toy uncertainty cross-check (C_b, R_c) not performed — COMMITMENTS minimum target | §7, COMMITMENTS.md |
| 13 | Appendix D precision investigation not updated for Phase 4b dominant systematic | App. D |
| 14 | Simple counting A_FB^b vs self-calibrating cross-check not performed or formally deferred | COMMITMENTS.md |
| 17 | Table 4 does not distinguish Phase 4a diagnostic column from Phase 4b measurement column | Table 4 |
| 18 | δ_b fix plan for Phase 4c lacks feasibility verification on 10% data statistics | §9.1 |
| 19 | Zero-impact systematic (ε_uds in Phase 4a): no overlay figure present | §5.1 |
| 20 | C_b = 1.01 external assumption drives R_b 10% result; no data-driven C_b bound attempted | §8.4 |

### Category C (suggestion)

| # | Finding | Location |
|---|---------|----------|
| 19 | F2 angular distribution figure caption should specify which κ produces the cited χ²/ndf | Fig. caption §7.2 |

---

## CLASSIFICATION: **B**

The AN is a thorough and honest document — it documents its own limitations clearly, labels the circular calibration correctly, and does not hide the δ_b overestimation. The physics content is sound.

However, the document contains **8 Category A numerical self-consistency failures**, most of them stale values from pre-fix iterations that survived the Doc 4a → Doc 4b update cycle. These are the classic pattern: summary tables updated, per-section tables and JSON citations retain stale values. The most serious are: the stale covariance matrix (Appendix B), three values for the same ε_b quantity, and a claimed PASS result (WP 10.0 closure) with no JSON evidence. The A_FB^b reporting issue (Finding 9) is a structural framing problem: a result that is admitted to be wrong by a known factor should not appear in the abstract and summary table as a central value.

**Classification: B** — the analysis note is not ready to advance to human gate. The Category A findings must be resolved, then a verification pass should confirm each fix before the next review. No regression to an earlier inference phase is triggered: all findings are editorial/consistency issues within the Doc phase scope, not physics errors in the underlying analysis chain.

---

*Review compiled by sabine_4780 | Two-pass protocol | Date: 2026-04-02*
