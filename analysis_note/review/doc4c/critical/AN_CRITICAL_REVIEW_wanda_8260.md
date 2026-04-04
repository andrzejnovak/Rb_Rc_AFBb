# Critical Review — Doc 4c v7 (DEFINITIVE REWRITE)
**Session:** wanda_8260
**Date:** 2026-04-02
**Document:** analysis_note/ANALYSIS_NOTE_doc4c_v7.tex
**Protocol:** Two-pass (COMMITMENTS check + full physics/completeness review)

---

## PASS 1 — COMMITMENTS.md Verification

Reviewed all entries in COMMITMENTS.md. Every line is either `[x]` (resolved) or `[D]` (formally downscoped with documented justification). No open `[ ]` items remain.

**Result: PASS — all commitments resolved.**

Downscoped items carry adequate justification in each case. The most consequential downscopes — the BDT training with bFlag labels [D9/D10], the negative-d0 closure test, the four-quantity simultaneous AFB fit [D12b], and the floating R_c [D] — each have explicit feasibility statements. The Phase 4c items added in the REGRESSION Addendum are marked [x] and appear to be completed. No concerns at this level.

---

## PASS 2 — Full Physics and Completeness Review

### A. JSON–AN Consistency: Primary Results

**R_b primary result:**
- AN abstract and §10: `R_b = 0.2155 ± 0.0004 (stat) ± 0.027 (syst)`, method = BDT 3-tag SF-calibrated.
- `parameters.json`, field `R_b_BDT_primary`: value = 0.2155, stat = 0.0004, **syst = null**, systematic_status = "pending", note = "Stat-only. Systematic evaluation of BDT-based extraction is ongoing."

**Finding A1 [CATEGORY A]:** The primary R_b result is presented in the AN with a full systematic uncertainty of 0.027, but the authoritative JSON record (`parameters.json`) explicitly marks this as `syst = null` and `systematic_status = "pending"`. The note says the 0.027 figure is from the "cut-based cross-check." This is a direct contradiction between the AN and its source-of-truth JSON. A document claiming a final definitive result cannot have the underlying data record say "ongoing." The systematic was evaluated for the cut-based cross-check method, not for the BDT primary, and has been relabelled without proper re-evaluation.

**A_FB^b primary result:**
- AN abstract and §10: `A_FB^b = 0.094 ± 0.005 (stat) ± 0.027 (syst)`, method = signed-thrust-axis, kappa=0.3.
- `parameters.json`, field `A_FB_b_signed_primary`: value = 0.094, stat = 0.005, syst = 0.02713, total = 0.02756, systematic_status = "evaluated".

Signed primary AFB is internally consistent. The AN rounds 0.02713 to 0.027, which is acceptable.

**R_b systematic total inconsistency:**
- AN Table 7 (`tbl:syst-rb`) lists sources and values summing in quadrature to 0.020, not 0.027. The individual entries (eps_c = 0.017, eps_uds = 0.008, C_b = 0.007, R_c = 0.002, sigma_d0 = 0.001, mc_year = 0.001, hadronization = 0.0005, sigma_d0_form = 0.0004, mc_statistics = 0.0004, physics_params = 0.0002, g_cc = 0.0001, g_bb = 0.0001, selection_bias = 0.0001, tau = 0.00005) sum in quadrature to 0.0202, while the table's "Total systematic" row claims 0.027. The total is inconsistent with the listed entries by approximately 34%. `systematics.json` (field `phase_4c_fulldata.rb_total_syst`) confirms the correct quadrature sum is 0.02695, matching the systematics.json. The discrepancy arises because the top-level `systematics.json` section (`R_b`) carries an older, unconstrained evaluation (eps_c = 0.044, eps_uds = 0.038) yielding 0.065. The phase_4c_fulldata block has the correct constrained values (eps_c = 0.017, eps_uds = 0.008) summing to 0.020.

**Finding A2 [CATEGORY A]:** The R_b systematic total (0.027) stated in the AN abstract, §10, Table 7, and conclusions does not equal the quadrature sum of the entries in Table 7 (= 0.020). Either: (a) additional sources contribute to the 0.027 that are not listed in Table 7, or (b) the 0.027 figure was copied from an earlier, unconstrained version and was not updated when the constrained systematics were adopted. The reader cannot reproduce the stated total from the table. This is a Category A arithmetic inconsistency.

---

### B. Section-by-Section Review

**§1 Introduction — PASS with minor gaps**
Physics motivation is clear. Observable definitions are correct and cited. Prior measurements from ALEPH, DELPHI, and LEP/SLD are properly introduced with citations and numbers. Color coding (\measured, \external) is defined and used consistently.

**Finding B1 [CATEGORY B]:** The mandatory input provenance table (required by methodology/analysis-note.md §1) is absent. The spec requires a structured table listing each key input with columns for Input, Source, and Provenance category (Measured/Published/Derived/Theory). The color coding commands are defined but a formal table is not present. This is Category B per the spec: "Category B if absent at Doc 4c review."

**§2 Data Samples — FAIL on luminosity**
Event count tables are present and correct. MC sample table is correct.

**Finding B2 [CATEGORY B]:** The data table (`tbl:data`) contains only event counts, no luminosity column. The spec (required section §2) states "Integrated luminosity is mandatory. Every data-taking period must have a luminosity column." The spec further says "An analysis note without luminosity figures is Category B." The text does not estimate luminosity via `L = N_had / sigma_had` either. The MC table is also missing the Generator and cross-section columns required by the spec's MC sample table template.

**§3 Event Selection — PASS with one gap**
Cutflow table is present with data and MC. Track quality cuts are listed. N-1 distributions are not individually shown (one compound cutflow figure is shown). The AN text adequately motivates each cut.

**Finding B3 [CATEGORY C]:** The spec requires "N-1 preferred" distribution plots for each cut. The current figure (fig:cutflow) shows an aggregate efficiency bar chart rather than per-cut distributions. This is a suggestion for improvement, not a hard failure given the cutflow table provides the numbers.

**§4 Flavour Tagging and §5 Corrections — mixed**

The tagging section is well-written. The d0 sign convention is explained with an equation. The hemisphere probability formula and combined tag formula are both displayed. The three-tag framework equations (eqs. fs, fd, chi2) are complete and reproducible.

**Finding B4 [CATEGORY A]:** The BDT is described as achieving `AUC = 1.000` on the test sample (§4.3). An AUC of exactly 1.000 — perfect discrimination — is a red flag that the BDT training is overfit or the self-labelled "b-enriched" / "light-enriched" samples are not statistically independent of the test set, or the feature distributions are trivially separable at the labelling threshold. The AN does not discuss or explain this figure. An AUC of 1.000 means the BDT learns to identify the selection cut applied to create training labels, not the underlying b-quark physics. The ROC curve figure is absent from the AN. If the BDT discriminates perfectly, it is learning the tagging threshold rather than b-quark properties — which calls into question the independence assumption of the three-tag system.

**Finding B5 [CATEGORY A]:** The BDT-based extraction fit GoF is reported as `chi2/ndf = 377/7` (§9.1). This p-value is essentially zero. The AN explains this as the "linear SF correction not fully capturing data/MC differences at the per-mille level" and relies on the WP stability test (chi2/ndf = 1.1/12, p = 1.0) to argue the extracted value is robust. However, per the spec (methodology/analysis-note.md §4, Statistical methodology standards): "The primary extraction must have chi2/ndf < 3 (p > 0.01). A primary result with p < 0.01 is Category A unless: (a) the source of poor GoF is identified, (b) it is demonstrated not to bias the extracted parameter, and (c) a configuration with acceptable GoF is shown as a cross-check." Condition (a) is partially met (stated but not demonstrated); condition (b) is asserted but not demonstrated quantitatively (no bias study); condition (c) is partially met by the cross-check table. This does not satisfy the spec's three-part requirement.

**Finding B6 [CATEGORY B]:** The systematic subsections in §7 do not follow the mandatory four-part template (physical origin → evaluation method with propagation chain → numerical impact with per-source impact figure → interpretation). The eps_c subsection begins with the impact on the constraint precision, not with the physical origin of the uncertainty. None of the systematic subsections include individual per-source impact figures (shifts as a function of the varied parameter). The summary budget tables exist but per-source shift figures are absent. The spec states "flat shifts on shape measurements are Category A" and requires "impact figure showing how the result shifts."

**Finding B7 [CATEGORY B]:** The error budget narrative paragraph required by the spec (§5: "Error budget narrative (required)") is absent after the systematic budget tables. The spec requires discussion of: (a) which sources dominate and why, (b) statistical vs systematic limitation, (c) concrete improvements, (d) resolving power. The conclusions section touches on some of these points but not in the dedicated location required after the per-source tables.

**§6 A_FB^b Extraction — mostly sound**

The jet charge definition, thrust axis signing procedure, and extraction formula are clearly presented with equations. The signing ambiguity discovery and resolution are documented.

**Finding B8 [CATEGORY A]:** The thrust axis signing procedure uses the hemisphere jet charge itself to determine the forward direction. This is circular: the hemisphere with more negative charge is assigned as the b-quark direction because b-quarks have Q = -1/3. But the charge separation delta_b used in the extraction formula (eq. afb-extraction) is taken from published ALEPH values calibrated under the assumption of a correct quark-direction assignment. If the self-signing procedure has a wrong-sign fraction of 43% (= 1 - 0.57), then the extracted A_FB^b is diluted by approximately (2*0.57 - 1)^2 = 0.020, not just by the hemisphere charge separation. The AN does not quantitatively account for the wrong-sign fraction in the dilution correction, nor does it verify that the published delta_b values from the ALEPH method (which used a different quark-direction assignment method) are valid inputs to a jet-charge-signed analysis. This is a potential double-counting of the dilution factor.

**§7 Systematic Uncertainties**

See B6 and A2 above. The dominant systematic for A_FB^b (kappa dependence, delta_AFB = 0.024) is evaluated from the spread across kappa values — using the deviation at kappa=0.5 from the primary kappa=0.3. The physical explanation of why the 0.3→0.5 deviation defines the systematic is not provided. The AN notes that kappa=1.0 and 2.0 deviations "are not included" due to "multi-flavour dilution bias" — this is reasonable but requires justification as to why kappa=0.5 is included but kappa=1.0 is not.

**§8 Cross-Checks**

**Finding B9 [CATEGORY A]:** The per-year consistency cross-check (Table 5, tbl:per-year) uses the cut-based SF-corrected method at WP (tight=8, loose=4), which gives R_b ~ 0.188 per year. The primary result is the BDT-based extraction giving R_b = 0.2155. These differ by ~0.027, which is exactly equal to the quoted systematic uncertainty. The table caption calls WP (tight=8, loose=4) "the primary working point" — but the primary result uses the BDT. The AN does not explain why the per-year cross-check uses a different, non-primary method, or why the per-year values (0.186–0.189) are 1.3 sigma below the primary result (0.2155). A reader who sees per-year values of 0.188 and a primary result of 0.2155 from the "same" analysis will question whether the methods are consistent. This discrepancy must be explicitly addressed.

**Finding B10 [CATEGORY B]:** The A_FB^b closure test description in §8.3 states "0/12 pulls above 3-sigma (across 4 kappa x 3 WP configurations), with a maximum |pull| = 2.8." A maximum pull of 2.8 at 12 trials has p ~ 0.25 of occurring by chance (expected ~0.3% per pull, 12 independent tests), so this is not alarming. However, the closure test is performed on a 60/40 data split, not on MC pseudo-data — for A_FB^b. The spec requires the independent closure test to compare to "MC truth" for extraction measurements. On data, there is no truth value to compare to. The closure test for A_FB^b is described as testing "independent 60/40 split of the full data" — this tests reproducibility, not closure. This distinction should be stated.

**§9 Statistical Method**

The chi2 formulation is clear. The discussion of the GoF failure at chi2/ndf = 377/7 is present but (as noted in B5) does not satisfy the spec's three-part requirement.

**§10 Results**

Results table (tbl:all-results) is present and complete. The summary table includes R_b, A_FB^b, A_FB^{0,b}, and R_c. Values are consistent with parameters.json for A_FB^b. The R_b systematic inconsistency (A2) propagates to this table.

**Finding B11 [CATEGORY B]:** Table 6 (`tbl:rb-results`) shows a summary of R_b results from different methods. The cut-based SF result at tight=8 is listed as R_b = 0.1878 — more than 1 sigma below the primary BDT result (0.2155). The table does not explain this ~0.027 discrepancy between two supposedly calibrated methods measuring the same quantity. A footnote or paragraph explaining why the BDT is preferred and why the cut-based method at this working point differs so significantly would be required for a reader to trust the primary result.

**§11 Comparison to Prior Results**

Comparison is present and quantitative for all listed references. Pulls are computed. The precision ratio table (tbl:precision) honestly documents the 19x–41x larger R_b uncertainty compared to published ALEPH and LEP/SLD results.

**Finding B12 [CATEGORY B]:** The comparison of A_FB^b to the LEP combined result (A_FB^{0,b} = 0.0992 ± 0.0016) uses the primary result of 0.094 (which is the observed-frame A_FB^b, not the pole asymmetry A_FB^{0,b} = 0.097). The pull quoted in §11.2 is computed with A_FB^{0,b} values (0.094 vs 0.0992) mixing the un-corrected measurement with the pole quantity. The text notes this but the pull calculation mixes quantities.

**§12 Conclusions**

The conclusions section is approximately 280 words — below the 400-word minimum required by the spec ("Conclusions must be at least 400 words (~1 page)"). Key forward-looking elements are present but compressed.

**Finding B13 [CATEGORY B]:** Conclusions section word count (approximately 280 words) is below the 400-word minimum specified in methodology/analysis-note.md. The spec states this must be at least one page, standing alone for a reader who reads only abstract + conclusions.

**§13 Future Directions and §14 Known Limitations**

Both sections are present and substantive. The limitation index in the appendix is provided. The reproduction contract is present. The per-systematic detail appendix is complete.

---

### C. Methodology/Analysis-Note.md — 13 Required Sections Check

| # | Required Section | Status |
|---|-----------------|--------|
| 1 | Introduction with input provenance table | Present but provenance TABLE absent [B1] |
| 2 | Data Samples with luminosity column | Events present, luminosity absent [B2] |
| 3 | Event Selection | Present, N-1 plots absent but acceptable [B3] |
| 4 | Corrections/Unfolding | Present, stress test absent [B14] |
| 5 | Systematic Uncertainties | Present, total inconsistency [A2], format issues [B6] |
| 6 | Cross-Checks | Present, per-year method inconsistency [B9], AFB closure scope [B10] |
| 7 | Statistical Method | Present, GoF failure inadequately addressed [B5] |
| 8 | Results | Present, total inconsistency [A2] |
| 9 | Comparison to Prior Results | Present, minor mixing [B12] |
| 10 | Conclusions | Present but short [B13] |
| 11 | Future Directions | Present |
| 12 | Known Limitations | Present |
| 13 | Appendices (limitation index, reproduction contract) | Present |

**Finding B14 [CATEGORY B]:** The spec requires (§4): "The AN must state the stress test reweighting formula, the variable used, the magnitudes tested (5%, 10%, 20%), and the recovery accuracy at each level." No stress test is documented in §5 (Corrections and Calibration). The contamination injection closure test (COMMITMENTS [x]) is referenced in the text but the reweighting formula, magnitudes, and per-magnitude recovery accuracy are not stated in the AN body.

---

### D. Additional Findings

**Finding D1 [CATEGORY B]:** The BDT section states AUC = 1.000 without a ROC curve figure. The spec (from analysis-note.md) states that "MVA diagnostics when a classifier is used (ROC, score distributions, feature importance)" must appear. Feature importance is shown (Appendix B). Score distributions are not shown as separate data/MC comparison plots. The ROC curve is absent.

**Finding D2 [CATEGORY C]:** The change log (§ Change Log, before Introduction) describes the v7 changes correctly but is written in terms of phase labels ("BDT-based R_b promoted to primary result"). The spec says change log entries should not reference internal process labels. The phase progression language ("Phase 4c" in the reproduction contract appendix) appears only in verbatim code blocks, which is acceptable.

**Finding D3 [CATEGORY C]:** In §9.1, the extraction is stated to use a chi2 minimization over "8 observables" from the three-tag system, with 1 free parameter giving "7 degrees of freedom." However, since the efficiencies are fixed from MC (not floated), the chi2 with 7 dof tests the model adequacy, not the fit residuals. The AN correctly notes this but does not clarify how the statistical uncertainty on R_b is propagated (from the chi2 minimum's curvature vs. analytical error propagation from the counting formula). The spec requires documentation of the uncertainty propagation method.

**Finding D4 [CATEGORY B]:** The notation table required by analysis-note.md ("Every physical quantity must use a single, consistent symbol throughout the AN. The same variable appearing under different names in different sections is Category A. Define symbols at first use and maintain a consistent convention.") — no dedicated notation/symbol table is present. Symbols are defined at first use and appear consistent, but the formal table is absent. This is Category B per spec, which requires it explicitly.

---

## Summary of Findings

### Category A (Must Resolve — blocks advancement)

| ID | Section | Finding |
|----|---------|---------|
| A1 | §10, Abstract, JSON | R_b primary syst in AN (0.027) contradicted by parameters.json (`syst=null`, status="pending") |
| A2 | §7, Table 7, Abstract | R_b systematic total (0.027) does not equal quadrature sum of listed entries (0.020); arithmetic inconsistency |
| B4 | §4.3 BDT | AUC = 1.000 unexplained, no ROC figure, overfit risk not addressed |
| B5 | §9.1 | Primary extraction chi2/ndf = 377/7 not adequately addressed per three-part spec requirement |
| B8 | §6 | Thrust-axis signing uses charge for direction; double-counting of dilution in delta_b not addressed |
| B9 | §8.1 | Per-year table uses cut-based SF (R_b ~ 0.188) inconsistent with BDT primary (0.2155); not explained |

### Category B (Must Fix Before PASS)

| ID | Section | Finding |
|----|---------|---------|
| B1 | §1 | Input provenance table absent |
| B2 | §2 | Luminosity column absent from data table; MC table missing Generator/sigma columns |
| B6 | §7 | Systematic subsections missing four-part template; no per-source impact figures |
| B7 | §7 | Error budget narrative paragraph absent after budget tables |
| B10 | §8.3 | AFB closure test on data split (not MC truth); closure vs reproducibility distinction not stated |
| B11 | §10 | 0.027 gap between cut-based (0.188) and BDT (0.2155) in results table unexplained |
| B12 | §11 | AFB comparison mixes observed and pole asymmetry quantities |
| B13 | §12 | Conclusions ~280 words, below 400-word minimum |
| B14 | §5 | Stress test formula, variables, magnitudes, and recovery accuracy absent |
| D1 | §4.3 | ROC curve and BDT score distributions absent |
| D4 | General | Formal notation/symbol table absent |

### Category C (Suggestions)

| ID | Section | Finding |
|----|---------|---------|
| B3 | §3 | N-1 per-cut distributions preferred over aggregate bar chart |
| D2 | Change Log | Phase labels in change log entries (minor) |
| D3 | §9.1 | Statistical uncertainty propagation method not explicitly stated |

---

## Classification: **(A) — Must Resolve**

Six Category A findings are present. The most critical are:

1. **A1/A2 together**: The stated systematic uncertainty on R_b (0.027) is simultaneously (a) marked "pending" in the authoritative JSON, and (b) arithmetically inconsistent with the table entries in the AN. These two findings combined mean the R_b result as stated is not reproducible from its source data or from the AN itself.

2. **B5**: chi2/ndf = 377/7 for the primary extraction is a GoF failure that is not resolved per the spec's three-part requirement. A primary result with essentially zero p-value requires a demonstrated bias study, not just an assertion of robustness.

3. **B4**: AUC = 1.000 is a physics alarm. If the BDT learns the tagging threshold perfectly, the self-calibration logic of the three-tag system is compromised.

4. **B8**: The self-signed thrust axis introduces a dilution that may be double-counted with the published delta_b. The AN does not address this.

5. **B9**: The 0.027 discrepancy between the per-year cross-check method (cut-based, R_b ~ 0.188) and the primary method (BDT, R_b = 0.2155) is not explained. A reader will interpret this as a systematic bias that is not captured.

The document is well-structured and represents a genuine improvement over earlier versions. The narrative is coherent and the physics motivations are sound. The completeness (13 sections, appendices, figures all on disk) is good. However, the internal arithmetic inconsistency in the dominant result (R_b systematic total), the JSON–AN mismatch, and the unexplained per-year/primary method discrepancy are fundamental errors that cannot be accepted at final review.

**Recommend: ITERATE with fixer agent addressing A1, A2, B9, B5, B4, B8 as mandatory before re-review. B-level findings to be addressed in the same iteration.**
