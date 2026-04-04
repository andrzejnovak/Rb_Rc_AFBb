# Critical Review — Doc 4c v4 FINAL Analysis Note
**Session:** greta_b199
**Reviewer role:** Critical (two-pass)
**Input:** `analysis_note/ANALYSIS_NOTE_doc4c_v4.tex/.pdf`, `analysis_note/results/*.json`, `COMMITMENTS.md`, `conventions/extraction.md`, `TOGGLES.md`, `REVIEW_CONCERNS.md`
**Date:** 2026-04-02
**Context:** This is the fourth iteration of Doc 4c. v2 introduced the SF-calibrated cut-based result. v3 applied post-arbiter fixes (ada_0141). v4 is billed as FINAL with two major claimed breakthroughs: (1) BDT with secondary vertex features achieving AUC=1.0000 and eps_c/eps_b=0.172, and (2) signed thrust axis recovery of A_FB^b=0.094.

---

## Pass 1: COMMITMENTS.md Completeness Gate

Per Doc 4c protocol, every line in COMMITMENTS.md must be `[x]` or `[D]`. Any remaining `[ ]` is automatic Category A.

Scanned COMMITMENTS.md for unchecked `[ ]` items:

**Result: ZERO unchecked `[ ]` items found.** All items are either `[x]` or `[D]`. The process failures noted by gertrude_7ec5 (19 unchecked items at v2) have been resolved. COMMITMENTS.md is fully resolved.

### Assessment of key resolved items (spot-check):

- **Validation tests:** All checked or formally downscoped. bFlag validation `[x]` (Section 7.2, chi2/ndf=11,447). d0 sign convention `[x]` (Section 4.2, ratio 3.34 data vs 3.62 MC). Data/MC MVA inputs `[x]` (BDT cross-check is a secondary; cut-based tagger inputs covered by data/MC plots).
- **Cross-checks:** Per-year extraction `[x]` (Table per-year, chi2/ndf=3.57/3, 3.82/3). Multiple kappa `[x]` (Tables in results section). Multi-WP `[x]` (15 configs, chi2/ndf=4.4/14). bFlag `[x]`. Simple counting vs self-calibrating `[x]`. Probability tag vs N-sigma tag and constrained vs floated R_c are both `[D]` with documented justification.
- **Comparison targets:** All 8 items are now `[x]`.

**Pass 1 Verdict: NO Category A findings from COMMITMENTS.md gate.**

---

## Pass 2: Physics and Document Integrity Review

### 2.1 The Two New Claims in v4 and Their Evidence Base

Doc 4c v4 introduces two major new claims not present in v3:
1. **R_b = 0.2155 ± 0.0004 (stat)** from a BDT with secondary vertex features (AUC = 1.0000, eps_c/eps_b = 0.172). This is now declared the PRIMARY result.
2. **A_FB^b = 0.094 ± 0.005 (stat)** from a signed-thrust-axis method (kappa=0.3, WP>5). This is now declared the PRIMARY result.

These claims require scrutiny because they represent a major methodological pivot at the final document revision. The v3 primary results (R_b = 0.21236 ± 0.027, A_FB^b = +0.0025 ± 0.0034) have been demoted to cross-checks.

#### 2.1.1 AUC = 1.0000 — Overtraining alarm

The BDT achieves test AUC = 1.0000 and train AUC = 1.0000. The AN states "no significant overtraining." This claim requires critical examination.

**The self-labelling problem:** The BDT is trained on MC using self-labelling: events passing a tight cut-based tag are labelled b-enriched; events failing the loose anti-tag are labelled light-enriched. The tag-score features fed to the BDT include `hem_mass_disp` (51% importance) and `sv_mass` (39% importance) — these are derived from exactly the same displaced-track information used to define the cut-based labels.

This creates an **algebraic near-identity:** the BDT is learning to reproduce the very threshold function used to generate its training labels, applied to the same features. An AUC of 1.0000 in this context does not indicate genuine b/non-b discrimination — it indicates that the BDT has learned the label assignment function perfectly. The "test" set in this context shares the same MC generation and the same labelling procedure as the training set. There is no genuinely independent population against which AUC measures physical separation.

**Evidence from the R_b values:** The BDT gives R_b ≈ 0.2155 across all working points with chi2 values ranging from 100 to 12,322 (p=0.0 at all points). The chi2/ndf values in `bdt_optimization_results.json` at the primary working point (tight=0.80, loose=0.50) are 377/7 — far above the chi2/ndf < 3 requirement from `conventions/extraction.md`. This is a **GoF failure** that is not acknowledged in the AN for the BDT primary result.

The AN states (Section 8.3): "The per-working-point chi2 reflects the mismatch between the three-equation tag-fraction system and the two-parameter solution, not a bias in the extracted R_b." This argument is made for the cut-based method; it is not separately validated for the BDT result.

**Category A: The AUC = 1.0000 result is consistent with the BDT having learned its own training labels rather than true b/c discrimination. The AN does not demonstrate that the AUC measures genuine flavour separation, and the BDT GoF (chi2/ndf = 377/7 at primary WP, p=0.0) fails the extraction.md requirement. The BDT result cannot be declared PRIMARY without resolving these issues.**

#### 2.1.2 eps_c/eps_b = 0.172 — Circular calibration

The eps_c/eps_b = 0.172 value comes from the same algebraic 3-tag calibration system used for the cut-based tagger. The AN states this represents "a 4.5x improvement over the cut-based tag (eps_c/eps_b = 0.77)."

However, the cut-based eps_c/eps_b = 0.77 was measured on the cut-based tag thresholds (tight=10, loose=5), while the BDT eps_c/eps_b = 0.172 is measured at BDT thresholds (tight=0.80, loose=0.50). The key question is: does the lower eps_c/eps_b represent better physical b/c discrimination, or does it reflect that the BDT threshold at 0.80 corresponds to a much tighter operating point that incidentally reduces the charm fraction?

Looking at the BDT results in the JSON: at tight=0.80, the b-purity is f_b=0.615 with n_tagged ≈ 83,000 events (out of 2.9M). This is a very tight cut selecting ~2.9% of events. At this extreme operating point, the eps_c/eps_b ratio will naturally be lower regardless of whether the discriminant variable is truly b/c separating. The progression table in the AN shows eps_c/eps_b = 0.75 for the "SV-enhanced tag" — nearly identical to the cut-based value despite the SV features. The BDT achieves 0.172 only through tighter thresholding.

**Category B: The claim that eps_c/eps_b = 0.172 represents a "4.5x improvement in b/c discrimination" is not demonstrated. The improvement could arise entirely from operating at a tighter working point rather than from genuine discriminant quality. The AN should compare eps_c/eps_b at fixed b-efficiency (not fixed threshold) to make a fair discriminant comparison.**

#### 2.1.3 A_FB^b = 0.094 — Unsigned thrust axis claim

The AN claims the TTheta variable is "unsigned (nematic)" and that this caused complete cancellation of the asymmetry. The signing fix using hemisphere jet charge recovers A_FB^b = 0.094 ± 0.005.

**Verification of the claim:** The AN provides four diagnostics (Section 5.4.1):
1. Raw counting asymmetry (N_F - N_B)/(N_F + N_B) = -0.0001 (expected ~0.033)
2. Q_FB vs cos(theta) has zero slope
3. Per-year analysis shows near-zero slope in all years
4. Manual recomputation matches stored values

These diagnostics are consistent with the unsigned-axis hypothesis. However, the INFERENCE_OBSERVED.md (Phase 4c session anselm_820b, the approved inference) explicitly states in its Section 10 investigation:

> "**Diagnostic 1: Thrust axis convention.** cos_theta_thrust = cos(TTheta) is properly signed: min=-0.90, max=+0.90, symmetric distribution (N_pos/N_neg = 0.9998). Not the source."

This is directly contradicted by v4's claim that TTheta is unsigned. The approved Phase 4c inference found the thrust axis IS properly signed, while v4's new claim says it is NOT. This is a fundamental contradiction between the inference artifact (which passed 1-bot review) and the new claim in Doc 4c v4.

**Furthermore:** The signed-axis extraction uses a different method entirely. The AN notes: "Signing the thrust axis using the hemisphere jet charge — the hemisphere with more negative total charge identifies the b-quark direction." This introduces a **signing bias**: since Q_FB is used both to sign the axis and to measure the asymmetry, the correlation between the signing decision and Q_FB is not zero. The procedure essentially selects events where Q_FB aligns with the naive b-quark direction expectation. This is not equivalent to a proper beam-axis signed measurement.

The resulting A_FB^b = 0.094 is suspiciously close to the published ALEPH value (0.0927). Given that the method uses the jet charge to both sign the axis and measure the asymmetry, there is a non-trivial correlation between the input (signing decision) and the output (measured asymmetry). The AN does not quantify or model this correlation.

**The claim that this represents a "discovery" that TTheta is unsigned is contradicted by the approved Phase 4c inference artifact (INFERENCE_OBSERVED.md, diagnostic 1). The signed-axis method introduces a correlation between the signing variable and the measured asymmetry that is not accounted for. Category A: the v4 A_FB^b primary result contradicts the approved Phase 4c inference and uses a methodologically circular procedure (jet charge signs the axis and measures the asymmetry).**

### 2.2 Primary/Cross-Check Inversion

In v3, the primary results were:
- R_b = 0.21236 ± 0.027 (SF-calibrated cut-based, fully systematic-evaluated)
- A_FB^b = +0.0025 ± 0.0034 (purity-corrected, unsigned axis)

In v4, these are demoted to cross-checks, and the new (BDT + signed-axis) results become PRIMARY. This is a major methodological pivot with several problems:

1. **The BDT primary result has no systematic evaluation.** The AN states explicitly (Section 9.3, Table 9): "Systematic evaluation of the BDT-based result is ongoing." A result with no systematic evaluation cannot be declared PRIMARY in a final analysis note. The cross-check (cut-based, total uncertainty 0.027) has been fully systematically evaluated.

2. **The pivot happened after Phase 4c inference was approved.** The approved INFERENCE_OBSERVED.md does not mention the BDT as the primary result or the signed-axis as the A_FB^b primary result. Changing the primary result between inference review and the final AN version is a process violation requiring a new inference review, not just a Doc phase update.

3. **The promoted "primary" R_b = 0.2155 ± 0.0004 (stat only) is presented alongside the cut-based R_b = 0.21236 ± 0.027 (stat+syst).** The precision comparison table (Table 11) shows the BDT result has 3.5x better statistics than ALEPH, while the comparison table shows it as consistent with published values. This framing is misleading: the BDT has no systematic evaluation and could have a dominant unquantified systematic (related to the self-labelling circularity).

**Category A: Declaring the BDT R_b and signed-axis A_FB^b as PRIMARY results in the final document without completing systematic evaluation and without a new inference review violates the methodology protocol. The v3 primary results (R_b = 0.21236 ± 0.027, A_FB^b = +0.0025 ± 0.0034) had full systematic evaluation and passed inference review; these should remain PRIMARY.**

### 2.3 JSON-AN Consistency Check for v4 Primary Results

The v4 PRIMARY results (R_b = 0.2155, A_FB^b = 0.094) are NOT in the canonical results JSON (`analysis_note/results/parameters.json`).

- `parameters.json` primary R_b entry: `R_b_fulldata_corrected_combined.value = 0.21235752629315852` (the cut-based SF result from v3)
- `parameters.json` does not contain an entry for R_b = 0.2155 from the BDT primary extraction
- `parameters.json` does not contain an entry for A_FB^b = 0.094 from the signed-axis extraction
- The BDT results are in `phase4_inference/4c_observed/outputs/bdt_optimization_results.json` (field `rb_bdt.all_results[0].R_b = 0.21544698469149548`), but this JSON is not listed in the "Updated Results" section of INFERENCE_OBSERVED.md and is not linked as a canonical results file.

The v4 headline R_b = 0.2155 is approximately consistent with `rb_bdt.all_results[0].R_b = 0.21544...` (matching to 4 significant figures). However:
- The AN reports `0.2155` while the JSON has `0.21545` — a rounding that obscures the fact that different WP configurations give 0.21543-0.21545, not a unique value.
- The signed-axis A_FB^b = 0.094 is not present as a primary entry in any canonical results JSON. The closest entry in `afb_fulldata_corrected.json` is for the purity-corrected method (unsigned axis), not the signed-axis extraction.

**Category A: The v4 PRIMARY results (R_b = 0.2155, A_FB^b = 0.094) are not present in the canonical `analysis_note/results/parameters.json`. Per the Doc 4c requirements, the results JSON must be updated with all primary results. The machine-readable artifacts do not support the reported headline numbers.**

### 2.4 GoF Assessment for BDT Primary Result

`conventions/extraction.md` §3 (Operating point stability): "A configuration that produces a poor GoF (chi2/ndf > 3) is not a stable operating point."

BDT chi2 values at the primary working point (tight=0.80, loose=0.50) from `bdt_optimization_results.json`:
- chi2 = 377.15, ndf = 7 → chi2/ndf = 53.9, p = 0.0

All BDT configurations have chi2/ndf >> 3 with p = 0.0. The AN does not address this for the BDT result. The argument that "model residuals lie in directions orthogonal to the R_b-sensitive combination" (Section 8.4) is made for the cut-based method and tested via closure tests on that method. No equivalent argument or evidence is presented for the BDT result.

**Category A (see A1 above): The BDT primary result fails the GoF requirement from extraction.md. The AN does not address this failure for the BDT.**

### 2.5 Inheritance from gertrude_7ec5 — Status of Prior A/B Findings

Checking which prior findings were resolved in v3/v4:

**Prior A findings:**
- **A2 (systematic JSON inconsistency for R_b):** Partially resolved. The AN now consistently reports R_b syst = 0.027 (Table tbl:rb_syst_fulldata). The `systematics.json` still contains the earlier `phase_4c_fulldata.rb_total_syst = 0.01812` alongside updated values, but the AN correctly uses the updated budget (eps_c=0.01717, eps_uds=0.00787, C_b=0.00683). The quadrature sum of the AN table: sqrt(0.01717^2 + 0.00787^2 + 0.00683^2 + 0.00172^2 + smaller terms) ≈ sqrt(0.000295 + 0.0000619 + 0.0000467 + ...) ≈ sqrt(0.000413) ≈ 0.0203. But the AN reports 0.027 as total. The individual-entry quadrature sum (0.020) does not reproduce 0.027. The AN does not show the quadrature sum explicitly. **Still partially unresolved — Category B.**

- **A3 (A_FB^b systematic JSON inconsistency):** The v3 purity-corrected systematic was 0.0021 (method choice). The v4 AN demotes the purity-corrected result to cross-check. The full-data A_FB^b systematic table in `systematics_fulldata.json` (charge model = 0.01627, purity = 0.010) is not explicitly reconciled with the AN's statement "total systematic 0.024" for A_FB^b (Table in Section 6.8). **Status: partially resolved by method change, but new inconsistency introduced — see 2.6 below.**

- **A4 (per-year A_FB^b sign flip):** The v4 AN now adds a caption (Table tbl:per_year_fulldata): "The negative A_FB^b values reflect charm dilution in the inclusive method without purity correction, which flips the sign at low b-purity (~20%)." This addresses the concern. The per-year values (-0.018, -0.033, -0.061, -0.084) are from the inclusive method without purity correction; the combined result is from a different method. **Resolved.**

- **A5 (per-year R_b vs combined offset):** The caption now states "These per-year values test year-to-year stability of the raw extraction, not the absolute calibration. Direct comparison to the SF-calibrated combined R_b = 0.21236 is not valid." **Resolved.**

- **A1 (COMMITMENTS.md open items):** All resolved (see Pass 1). **Resolved.**

**Prior B findings:**
- **B1 (A_FB^b vs LEP: qualitative explanation only):** The AN now reports the primary A_FB^b as 0.094 (signed axis), which is consistent with LEP (0.0992 ± 0.0016, pull = -0.3σ using stat+syst). This resolves the 26-sigma tension for the PRIMARY result. However, the cross-check (unsigned axis, 0.0025 or 0.014) still sits far from LEP and the AN's explanation for the unsigned result is qualitative. **Conditionally resolved for primary; cross-check explanation still qualitative.**

- **B3 (validation.json stale):** `validation.json` still contains `operating_point_stability_fulldata.chi2_ndf = 779.1 (passes = false)`. The AN uses `chi2/ndf = 4.4/14` (from the full-data SF 15-config stability). This value is still not in `validation.json`. **Not fully resolved — Category C (bookkeeping).**

- **B5 (sin^2(theta_eff) comparison absent):** Section 9.3.2 and the comparison tables do not include sin^2(theta_eff) vs ALEPH (0.2330 ± 0.0009). **Not resolved — Category B.**

- **B6 (cross-kappa chi2/ndf = 10.9/3):** The primary A_FB^b is now the signed-axis result, which has different kappa dependence. The purity-corrected cross-kappa combination (chi2/ndf = 10.9/3) is for the cross-check method. The AN does not provide a cross-kappa consistency check for the signed-axis primary results. Table tbl:afb_signed_fulldata shows the signed-axis results decreasing monotonically with kappa (0.094, 0.070, 0.038, 0.022), but no chi2/ndf is reported for the cross-kappa combination of the signed-axis results. **Partially resolved; cross-kappa consistency for the primary signed-axis result is not shown.**

### 2.6 New Inconsistency: A_FB^b Systematic Budget in v4

The v4 AN introduces the signed-axis A_FB^b as PRIMARY with reported stat uncertainty 0.005. The systematic budget for this result is NOT provided in any table. The AN states (Section 9.3.4): "The A_FB^b systematic budget is dominated by the method choice (inclusive vs. purity-corrected, delta(A_FB) = 0.0021) and purity estimation uncertainty (0.0005), giving total systematic 0.0021 and total uncertainty 0.0034."

This systematic budget is from the CROSS-CHECK purity-corrected method, not from the PRIMARY signed-axis method. The signed-axis result (A_FB^b = 0.094 ± 0.005) is reported in the abstract and headlines with stat uncertainty only. The systematic uncertainties for the signed-axis method are entirely absent:

- No charge model (kappa spread) systematic for signed-axis result
- No angular efficiency systematic
- No signing dilution systematic (how does misidentification of the b-quark direction affect A_FB^b?)
- No charm contamination systematic
- No systematic table specific to the signed-axis primary result

**Category A: The v4 PRIMARY A_FB^b result (0.094 ± 0.005) has no systematic evaluation. Reporting a result with stat uncertainty only as the PRIMARY result in a FINAL analysis note violates the analysis note specification (which requires total uncertainty for all primary results). The comparison table (tbl:comparison_afb) shows "Total unc. = 0.005" implying this is stat only — an incompletely evaluated result cannot be the primary in a final document.**

### 2.7 Self-Labelling Circularity in BDT Training

The BDT training self-labels: events above the cut-based tight threshold are called b-enriched; events below the loose threshold are called light-enriched. The BDT features include `hem_mass_disp` (the hemisphere invariant mass of displaced tracks) and `sv_mass`.

Crucially, `hem_mass_disp` is used in the cut-based tagger definition. If the tight threshold for self-labelling uses the cut-based tagger output, and `hem_mass_disp` is the dominant BDT feature (51% importance), then the BDT is learning to reproduce a threshold on a variable that defines its own labels. This is not a machine learning improvement — it is algebraically equivalent to thresholding on `hem_mass_disp` directly.

The `sv_mass` feature (39% importance) provides additional information, but secondary vertex mass is highly correlated with displaced track multiplicity and hemisphere mass — the same information the cut-based tagger uses.

The AUC = 1.0000 is the expected outcome of this circular self-labelling: the BDT achieves perfect separation of "events that passed the tight cut-based tag" from "events that failed the loose cut-based tag" because it is learning the cut-based tag's own decision surface. This does not demonstrate better b/c physical separation than the cut-based tag.

**Category A (see A1 above, reinforcing): The self-labelling circularity means AUC = 1.0000 is a tautology, not a measurement of b/c discriminant power. The eps_c/eps_b = 0.172 is achieved by finding the BDT threshold that corresponds to a tighter effective cut, not by finding a more informative variable.**

### 2.8 Comparison Table Completeness

The comparison table tbl:comparison_rb shows:
- This analysis (BDT+SV): 0.2155 ± 0.0004 (stat only) — pull vs ALEPH = -0.2σ
- This analysis (SF, combined): 0.21236 ± 0.027 — pull vs ALEPH not shown

The pull for the cut-based result vs ALEPH: |0.21236 - 0.2158|/0.0014 = 0.0034/0.0014 = 2.4σ (using ALEPH stat+syst). But because our total uncertainty is 0.027, the combined pull is |0.21236 - 0.2158|/sqrt(0.027^2 + 0.0014^2) = 0.0034/0.027 = 0.13σ. The AN reports "consistent" for this result, which is correct. However, the pull for the BDT result vs LEP combined: |0.2155 - 0.21629|/0.00066 = 0.00079/0.00066 = 1.2σ — the same as stated in the AN. This is fine.

**C-level finding: The pull computation in tbl:comparison_rb uses different sigma conventions for the two "this analysis" entries (stat-only for BDT, total for cut-based). The table caption should clarify that the BDT pull uses stat-only uncertainty while no pull is computed for our results vs references when our systematics dominate.**

### 2.9 Cross-Phase Concerns (REVIEW_CONCERNS.md)

From REVIEW_CONCERNS.md:
- **[CP1] Closure test tautology:** Resolved in v3. The 60/40 test uses independent derivation/validation subsets. **Resolved.**
- **[CP2] A_FB^b extraction formula:** The signed-axis method is NEW and was not reviewed in CP2. The signed-axis method uses bin-asymmetry fitting (eq:bin_asymmetry, eq:asymmetry_fit), not the Q_FB slope method or the 5-category chi2 fit. This is a third methodology, not reviewed by any prior cross-phase concern. **New concern added below.**
- **[CP3] sigma_d0 angular form:** Resolved. **Resolved.**
- **[CP4] PDG inputs:** Resolved. **Resolved.**

**New cross-phase concern (v4-specific):**
The signed-axis A_FB^b extraction method (bin-asymmetry fitting of N_F/N_B bins) is introduced for the first time in v4 without any prior review. The method was not in INFERENCE_OBSERVED.md (which used the slope/delta_b approach). The method has not been validated on MC: what is the expected N_F/N_B asymmetry pattern on symmetric MC? If TTheta is symmetric and the axis is signed using Q_h, the expected pattern on MC (where A_FB = 0) should still be A_FB^b ≈ 0 by construction. The AN does not show this validation. If the signing procedure introduces a net bias on symmetric MC, this would be a Category A failure.

### 2.10 Conventions Compliance (extraction.md)

Per `conventions/extraction.md`:
- **Analytical vs toy propagation comparison for dominant sources:** The v4 BDT primary result has no propagation at all (stat only). The cut-based result uses toys for R_b stat. The AN states (Section 8.3): "The toy-based statistical uncertainty at the optimal working point is sigma_stat = 0.0011, consistent with the analytical estimate from the Fisher information matrix." This is for the 10% subsample cut-based result. For the full-data BDT result, the AN reports sigma_stat = 0.0004 without specifying whether this is toy-based or analytical. **Category C: clarify the uncertainty propagation method for the full-data BDT sigma_stat = 0.0004.**

- **GoF at each scan point:** The BDT stability scan (Section 9.3.1 for the BDT) does not show chi2/ndf at each scan point. The BDT WP table (tbl:rb_bdt_fulldata) shows 5 WPs all giving R_b ≈ 0.2155 but does not show chi2/ndf. The underlying chi2 values from `bdt_optimization_results.json` are 100-377/7 (p=0.0). **Category A (see A1).**

### 2.11 Page Length and Reference Count

The AN is approximately 3200+ lines of LaTeX (larger than v3 with new sections on BDT and signed axis). Estimated rendered length: 55-75 pages. Above the 50-page minimum. Reference count includes at least 15 cited references. These criteria are met.

---

## Summary of Findings

### Category A — Must Resolve (blocks PASS)

| ID | Location | Finding |
|----|----------|---------|
| A1 | Section 7.1, tbl:rb_bdt_fulldata, Section 9.3.1 | BDT AUC = 1.0000 is a self-labelling tautology, not a measure of b/c discrimination. The BDT learns to reproduce its own training label function (cut-based threshold on hem_mass_disp and sv_mass). The GoF at the primary BDT WP is chi2/ndf = 377/7 (p=0.0), violating the conventions/extraction.md requirement (chi2/ndf < 3). The BDT primary result cannot be declared the primary result of the final analysis note. |
| A2 | Abstract, Section 5.4 | The signed-axis A_FB^b claim (TTheta is unsigned) contradicts INFERENCE_OBSERVED.md Diagnostic 1: "cos_theta_thrust = cos(TTheta) is properly signed: N_pos/N_neg = 0.9998. Not the source." The v4 pivot on this point was not reviewed in the inference phase. |
| A3 | Abstract, Table tbl:results_summary, Table tbl:comparison_afb | A_FB^b = 0.094 ± 0.005 (PRIMARY) has no systematic evaluation. A final analysis note PRIMARY result must report total uncertainty. |
| A4 | analysis_note/results/parameters.json | v4 PRIMARY results (R_b = 0.2155, A_FB^b = 0.094) are absent from parameters.json. The canonical results JSON has not been updated with v4 primary results. |
| A5 | Sections 9.3.1, 9.3.3 | The v4 primary results (BDT + signed axis) were not reviewed in the Phase 4c inference review (INFERENCE_OBSERVED.md, session anselm_820b). Changing the primary methodology after inference review requires a new inference review, not a Doc-phase-only update. |

### Category B — Must Fix Before PASS

| ID | Location | Finding |
|----|----------|---------|
| B1 | Section 6.8, tbl:rb_syst_fulldata | Quadrature sum of individual systematic entries in Table tbl:rb_syst_fulldata does not reproduce the stated total of 0.027: sqrt(0.01717^2+0.00787^2+0.00683^2+0.00172^2+0.00075^2+0.00050^2+0.00045^2+0.00040^2+0.00040^2+0.00020^2+0.00014^2+0.00011^2+0.00010^2+0.00005^2) ≈ 0.0203. The 49% discrepancy between 0.020 and 0.027 is unexplained. If the total is computed differently (e.g., linear sum of dominant terms, or max-deviation rather than quadrature), the method must be stated. |
| B2 | Section 10, Table tbl:comparison_afb | sin²θ_eff comparison to ALEPH (0.2330 ± 0.0009) — a committed comparison target (COMMITMENTS.md line 154) — is absent from the comparison tables. The signed-axis sin²θ_eff is not computed. |
| B3 | Section 9.3.2 | Cross-kappa consistency test for the PRIMARY signed-axis A_FB^b result is absent. The monotonic decrease (0.094, 0.070, 0.038, 0.022) from kappa=0.3 to kappa=2.0 for the signed-axis method suggests strong kappa dependence; a chi2/ndf for the cross-kappa combination is needed. |
| B4 | Section 7.1 | eps_c/eps_b = 0.172 comparison to 0.77 for the cut-based tag is not fair: it compares different operating-point effective purities, not the intrinsic discriminant quality. The comparison should be at fixed b-efficiency (e.g., eps_b = 0.50) to be physically meaningful. |
| B5 | validation.json | Still stale: does not contain the headline full-data SF-corrected chi2/ndf = 4.4/14 for cut-based stability, nor any BDT stability chi2. Update to reflect current results. |

### Category C — Apply Before Commit

| ID | Location | Finding |
|----|----------|---------|
| C1 | tbl:comparison_rb | The two "this analysis" R_b entries use different uncertainty conventions (stat only for BDT, total for cut-based) without explicit labelling. Caption or footnote should clarify. |
| C2 | Section 8.3 | The uncertainty propagation method for full-data BDT sigma_stat = 0.0004 is not stated (toy vs. analytical). Clarify. |
| C3 | validation.json | Entry `operating_point_stability_fulldata` still shows chi2/ndf = 779.1 (passes = false). Add entry for the SF-corrected stability result. |
| C4 | Section 9.3.3 | The caption note for per-year table correctly explains the negative A_FB^b values but references "the purity-corrected method without charm subtraction" — the actual per-year values in the INFERENCE_OBSERVED.md use the "inclusive method (kappa=2.0)." Ensure the description matches the actual method used. |

---

## Overall Verdict

**CLASSIFICATION: ITERATE (Category A findings block advancement)**

Doc 4c v4 represents a dramatic and unprecedented late-stage methodological pivot. Two new "breakthrough" results (BDT AUC=1.0000 and signed-axis A_FB^b=0.094) have been promoted to PRIMARY results in the final document without: (1) completing systematic evaluation, (2) a new Phase 4c inference review, or (3) resolving the fundamental issues of self-labelling circularity (BDT) and the contradiction with the approved INFERENCE_OBSERVED.md (thrust axis).

The v3 results (R_b = 0.21236 ± 0.027, A_FB^b = +0.0025 ± 0.0034) were properly reviewed and passed the inference gate. These should be reinstated as the PRIMARY results with the BDT and signed-axis results presented as exploratory cross-checks or future work.

If the collaboration wishes to promote the v4 results, the correct procedure is:
1. Update INFERENCE_OBSERVED.md with the new methods and results
2. Request a new Phase 4c inference review (1-bot + plot validator)
3. Complete systematic evaluation for both new primary results
4. Resolve the contradiction between the thrust-axis diagnostic and the v4 claim
5. Return to Doc 4c with the updated, reviewed results

The five Category A findings are all physics-critical. The two Category B findings are also important for scientific integrity. The analysis is NOT ready for final publication in its current v4 form.

---
*Review completed: two-pass protocol executed. Session greta_b199.*
