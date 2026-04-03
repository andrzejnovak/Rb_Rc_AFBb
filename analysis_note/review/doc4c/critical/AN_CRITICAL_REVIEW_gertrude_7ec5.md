# Critical Review — Doc 4c Final Analysis Note
**Session:** gertrude_7ec5  
**Reviewer role:** Critical (two-pass)  
**Input:** `analysis_note/ANALYSIS_NOTE_doc4c_v2.tex/.pdf`, `analysis_note/results/*.json`, `COMMITMENTS.md`, `conventions/extraction.md`, `TOGGLES.md`, `REVIEW_CONCERNS.md`  
**Date:** 2026-04-02

---

## Pass 1: COMMITMENTS.md Completeness Gate

Per Doc 4c protocol: every line in COMMITMENTS.md must be `[x]` or `[D]`. Any `[ ]` is automatic Category A.

### Unchecked items found:

**Validation tests:**
- `[ ]` Data/MC agreement on all MVA inputs (if BDT approach used): chi2/ndf per variable — lines 97-98
- `[ ]` bFlag interpretation validation (chi2/ndf > 2.0 threshold for b-enrichment proxy) — lines 99-104
- `[ ]` d0 sign convention validation [D19]: positive d0 tail enhanced in b-enriched hemispheres — lines 105-106

**Cross-checks:**
- `[ ]` Probability tag vs N-sigma tag comparison — line 132
- `[ ]` Multiple kappa values for A_FB^b (kappa = 0.3, 0.5, 1.0, 2.0, infinity) — line 133
- `[ ]` Per-year extraction (1992, 1993, 1994, 1995) — line 134
- `[ ]` bFlag cross-check (our tagger vs bFlag in data) — line 135
- `[ ]` Constrained R_c vs floated R_c in double-tag fit — line 136
- `[ ]` Multi-working-point extraction vs single working point — line 137
- `[ ]` Analytical vs toy-based uncertainty propagation comparison — lines 138-141
- `[ ]` Simple counting A_FB^b vs self-calibrating fit — lines 142-143

**Comparison targets (all 8 items unchecked):**
- `[ ]` R_b vs ALEPH (hep-ex/9609005): 0.2158 +/- 0.0014 — line 148
- `[ ]` R_b vs LEP combined (hep-ex/0509008): 0.21629 +/- 0.00066 — line 149
- `[ ]` R_b vs SM: 0.21578 — line 150
- `[ ]` A_FB^b vs ALEPH (inspire_433746): 0.0927 +/- 0.0052 — line 151
- `[ ]` A_FB^{0,b} vs LEP combined (hep-ex/0509008): 0.0992 +/- 0.0016 — line 152
- `[ ]` A_FB^{0,b} vs SM: 0.1032 — line 153
- `[ ]` sin^2(theta_eff) vs ALEPH (inspire_433746): 0.2330 +/- 0.0009 — line 154
- `[ ]` R_c fitted vs LEP combined: 0.1721 +/- 0.0030 — line 155

**Count: 19 unchecked `[ ]` items** across three sections (validation tests, cross-checks, comparison targets).

### Assessment of unchecked items:

**Comparison targets (8 items, lines 148-155): CATEGORY A conditional**  
The AN body text (Sections 10 and 10b, Tables 4 and 5) does contain numerical comparisons to ALEPH and LEP combined values for R_b and A_FB^b. The COMMITMENTS.md checkboxes were never ticked, but the content appears in the document. This is a process failure (checkboxes not maintained), not a content gap. Recommend reclassifying these 8 items as `[x]` after verifying that the AN tables match the committed comparison targets. See Pass 2 for the numerical cross-check.

**Cross-checks — partially executed, partially missing:**
- Multiple kappa: DONE in document (Tables 4, 8, App B). Checkbox omission only.
- Per-year extraction: DONE in Table 7 and Section 9.3.4. Checkbox omission only.
- Multi-WP extraction: DONE (15 configurations, App A). Checkbox omission only.
- bFlag cross-check: Section 7.2 documents the chi2 shape comparison (chi2/ndf = 11,447) and confirms bFlag is a quality flag, not a b-enrichment tag. Checkbox omission only.
- Probability tag vs N-sigma tag: NOT found in the document or results JSONs. **True gap.**
- Constrained R_c vs floated R_c: NOT found. R_c is uniformly constrained to SM. **True gap, but [D6] documents the constraint decision — acceptable if formally downscoped.**
- Analytical vs toy propagation comparison: Toys described (Section 8.3), analytical mentioned. The comparison (minimum targets: C_b and R_c propagation must agree within 10%) is NOT explicitly documented. **True gap.**
- Simple counting A_FB^b vs self-calibrating fit: Simple counting is the primary method. Self-calibrating fit was downscoped ([D12b]). The cross-check comparing them is therefore vacuously absent. Acceptable if noted.

**Validation tests — mixed:**
- Data/MC on MVA inputs: BDT is a cross-check only, not primary. Section 7.9 and App C document BDT performance including AUC and stability. The "chi2/ndf per variable" check is not shown. However, the BDT is not the primary tagger — this may be conditionally acceptable if the cut-based tagger inputs (d0, mass) are covered by Figs 7 and the data/MC section.
- bFlag interpretation: Section 7.2 performs a chi2 shape comparison (chi2/ndf = 11,447). The threshold test (chi2/ndf > 2.0 for b-enrichment proxy vs < 2.0 for non-b flag) is NOT explicitly stated as a pass/fail against that gate. The document correctly concludes bFlag is a quality flag, consistent with the < 2 threshold test. Conditionally acceptable.
- d0 sign convention [D19]: The document validates the sign convention in Section 4.2 (positive/negative ratio 3.34 in data, 3.62 in MC at 3-sigma). Fig. 2 shows this. The Phase 3 blocking gate stated "positive d0 tail enhanced in b-enriched hemispheres." This is satisfied. Checkbox omission only.

### Pass 1 Verdict:

**True gaps requiring Category A findings:**
1. Probability tag vs N-sigma tag comparison — genuinely absent
2. Analytical vs toy-based uncertainty propagation comparison — minimum targets not documented
3. Constrained R_c vs floated R_c — [D6] partially covers this but the cross-check was committed separately; needs formal downscoping note if not done

All other unchecked items represent checkbox bookkeeping failures where the content is present in the AN. These are Category B (process) findings.

---

## Pass 2: Physics and Document Integrity Review

### 2.1 Primary results consistency (parameters.json vs AN)

**R_b (full data, combined):**
- `parameters.json`: `R_b_fulldata_corrected_combined.value = 0.21236`, stat = 0.00010, syst = 0.027
- AN abstract and conclusions: "R_b = 0.21236 ± 0.00010 (stat) ± 0.027 (syst)" — **MATCH**
- AN header comment: "R_b = 0.21236 +/- 0.00010 (stat) +/- 0.027 (syst)" — **MATCH**

**A_FB^b (full data, purity-corrected, combined):**
- `parameters.json`: `A_FB_b_fulldata_final.value = 0.0025`, stat = 0.0026, syst = 0.0021
- AN body (Section 9.3.2, eq. 3): "A_FB^b = +0.0025 ± 0.0026 (stat) ± 0.0021 (syst)" — **MATCH**

**A_FB^b at kappa=2.0:**
- `parameters.json`: `A_FB_b_fulldata_final` note points to kappa=2.0 value 0.014
- AN eq. (4): "+0.014 ± 0.005 (stat)" — **MATCH**

**Stability chi2 (full data):**
- `validation.json`: `operating_point_stability_fulldata.chi2_ndf = 779.1` — this is the UNCORRECTED result
- `validation.json`: `operating_point_stability_sf_corrected.chi2_ndf = 0.027 (p=1.0)` — SF-corrected on 10% data
- AN header: "R_b stability: chi2/ndf = 4.4/14 (p=0.99)" — this value appears in the AN body but is NOT in validation.json. The chi2=4.4 appears to be specific to the full-data SF-corrected 15-config run, which is documented in `parameters.json` field `R_b_fulldata_corrected_combined.n_configs = 15` but without the stability chi2 value. **The chi2/ndf = 4.4/14 appears only in the AN; it cannot be verified against any JSON.** This is a **Category B** finding — the headline stability result is not machine-readable.

**MC expected (Phase 4a):**
- `parameters.json`: `stability_chi2_ndf = 1.159e-10` (effectively zero)
- AN Section 9.1: "chi2/ndf = 0.00/7 (p = 1.0)" — **MATCH** (both are effectively zero)

### 2.2 Comparison targets check

**R_b vs ALEPH (0.2158 ± 0.0014):**
- Our result: 0.21236 ± 0.027 (total)
- Difference: |0.21236 - 0.2158| = 0.0034, well within our total uncertainty (0.027)
- Pull = 0.0034 / sqrt(0.027² + 0.0014²) = 0.0034/0.027 = 0.13 — consistent. **PASS**

**R_b vs LEP combined (0.21629 ± 0.00066):**
- Difference: |0.21236 - 0.21629| = 0.0039, within our 0.027 total uncertainty
- Pull = 0.0039/0.027 = 0.14 — consistent. **PASS**
- Precision ratio = 0.027/0.00066 = 41x. The AN quotes ~19x in the precision table (Table 9, using ALEPH as reference). **Inconsistency:** the body (Section 10, Table 9) says "factor of ~19" referencing ALEPH; vs LEP combined the ratio is ~41. Both should be stated. Category C.

**A_FB^b vs LEP combined (0.0992 ± 0.0016):**
- Our combined result: 0.0025 ± 0.0034
- Difference: |0.0025 - 0.0992| = 0.0967
- Pull = 0.0967 / sqrt(0.0034² + 0.0016²) = 0.0967/0.0037 = 26 sigma
- `validation.json` documents this: `A_FB_b_vs_LEP_combined.pull = -193.8` (this appears to be a different calculation with only stat uncertainty). With total uncertainty the pull is ~26 sigma.
- The AN acknowledges this: Section 9.3.2 states the result is "below the LEP combined pole value" with explanation (charm contamination, no subtraction). **However, the validation target rule from `methodology/06-review.md` §6.8 (>3-sigma from reference = Category A unless quantitative explanation) applies.**
- Assessment: The AN does provide a quantitative explanation: (1) b-purity of ~20% dilutes the asymmetry, (2) no charm subtraction is applied, (3) the kappa=2.0 result (0.014) is the closest approximation. However, the explanation is qualitative ("charm contamination dilutes the signal") without a calculation showing what the expected value should be given the known purity and charm asymmetry. **Category B: the explanation is substantive but does not satisfy the three-part requirement of §6.8 (quantitative explanation + demonstrated magnitude match + no simpler explanation).**

**sin^2(theta_eff) vs ALEPH (0.2330 ± 0.0009):**
- Our value: 0.2495 ± 0.0005 (stat, from `parameters.json`)
- Difference: 0.2495 - 0.2330 = 0.0165, pull = 0.0165/0.0010 = 16.5 sigma
- The AN body (Section 9.3.2) states "The sin²θ value is far from the world average (0.23153) because the diluted A_FB^b propagates into an unreliable extraction." This is correct but the Comparison table (tbl:comparison_afb) does not include sin²θ_eff. **The committed comparison target (sin²θ_eff vs ALEPH: 0.2330 ± 0.0009) is absent from the comparison tables.** Category B.

### 2.3 Systematic budget consistency

**Full-data R_b syst:**
- `systematics.json phase_4c_fulldata.rb_total_syst = 0.01812` — this is ~18%
- `parameters.json R_b_fulldata_final.syst = 0.02695`
- AN Table 10 total systematic: 0.027
- The total syst in the final `parameters.json` entry (0.02695) matches the AN (0.027 rounded), but the `phase_4c_fulldata.rb_total_syst = 0.01812` appears discrepant.

  Decomposing in quadrature from `phase_4c_fulldata` systematics: eps_c (0.01486), eps_uds (0.00937), C_b (0.00387), R_c (0.00172), sigma_d0 (0.00075), mc_year (0.0005), hadronization (0.00045), sigma_d0_form (0.0004), mc_stats (0.0004), physics (0.0002), g_cc (0.00014), g_bb (0.00011), selection (0.0001), tau (0.00005) → quadrature sum ≈ sqrt(0.01486² + 0.00937² + 0.00387² + 0.00172² + ...) ≈ sqrt(0.000221 + 0.0000878 + 0.0000150 + ...) ≈ sqrt(0.000335) ≈ 0.0183.

  This matches `phase_4c_fulldata.rb_total_syst = 0.01812` but NOT the AN (0.027) or `R_b_fulldata_final.syst = 0.02695`.

  The AN Table 10 shows C_b variation as 0.00683 (larger than phase_4c 0.00387) and eps_c as 0.01717 vs 0.01486. These appear to use different C_b/eps_c assumptions. **The systematic JSON is internally inconsistent between the `phase_4c_fulldata` section and the final result.** **Category A: the total systematic in the AN (0.027) cannot be reproduced from the phase_4c JSON (0.018). The discrepancy is 49% and affects the headline result.**

**A_FB^b syst (full data):**
- `parameters.json A_FB_b_fulldata_final.syst = 0.0021`
- `systematics.json phase_4c_fulldata.afb_total_syst = 0.0193`
- These differ by ~10x. The `phase_4c_fulldata` afb systematic is far larger. The AN uses 0.0021. This large discrepancy warrants investigation — the AN may be using the minimum systematic (method choice only) while the JSON includes the kappa spread. **Category A: the systematic budget for A_FB^b is inconsistent between JSON files and requires resolution.**

### 2.4 Per-year consistency (Table 7)

The per-year R_b values are:
- 1992: 0.1885, 1993: 0.1876, 1994: 0.1880, 1995: 0.1864
- All values are ~0.187-0.189, significantly below the combined SF result of 0.21226

The AN states chi²/ndf = 3.57/3 (p = 0.31) for R_b — consistent within years. But the per-year values themselves are ~0.013-0.014 below the combined result. The AN states the combined result is 0.21226, while per-year are 0.186-0.189.

This is a systematic discrepancy: the per-year values are extracted using the tight=8, loose=4 working point, while the combined result uses 15 configurations. However, even at tight=8, loose=4, the single-WP result is 0.21226 on full data. The per-year values should be consistent with this if the same SF calibration is applied. **The ~2.5% offset between per-year (~0.187) and the full-data extraction (~0.212) at the same WP is unexplained.** This is **Category A** — the per-year values suggest the per-year SF calibration produces different efficiencies than the full-dataset SF calibration. The chi²/ndf consistency test is valid among years but obscures the absolute discrepancy.

### 2.5 A_FB^b sign and kappa dependence

Per-year A_FB^b values (Table 7):
- 1992: -0.018, 1993: -0.033, 1994: -0.061, 1995: -0.084

All four years give **negative** A_FB^b. The combined full-data result is positive (+0.0025). This cannot be reconciled by statistical fluctuations alone: all four years are negative, and the combined result should be the weighted average of the per-year values, which would also be negative.

The AN does not address this contradiction. The combined result (+0.0025) appears to come from a different calculation (the kappa-combined purity-corrected method across all WPs), while the per-year values may use a different method. **Category A: Table 7 shows all four per-year A_FB^b values are negative while the summary result is positive, with no explanation for the apparent contradiction.**

### 2.6 Validation.json: stability_fulldata failure

`validation.json operating_point_stability_fulldata`:
- chi2 = 5453.73, ndf = 7, chi2/ndf = 779.1, passes = false

The AN change log (v1 → v2) states that v1 had this unstable result and v2 corrected it with SF calibration. The v2 result (15 configs, chi2/ndf = 4.4/14) passes. However, `validation.json` still contains the failing result without a corresponding passing entry for the full-data 15-config SF result. The validation JSON represents the analysis state incompletely. **Category B: validation.json is stale and does not contain the headline full-data SF result.**

### 2.7 The C_b = 1.0 assumption

[D20] documents that C_b = 1.0 is assumed for the SF extraction. The measured C_b on data is 1.365-1.537 (tight WP). The SF method claims to absorb the correlation into per-category scale factors. The AN provides a systematic of ±5% / ±10% C_b variation, producing ΔR_b = 0.00683 (Table 10).

The conventions file (`extraction.md`) warns: "Large C_q corrections amplify the systematic uncertainty on C_q." With C_b ~1.5 on data and C_b = 1.0 assumed, the SF method is claiming to effectively decorrelate the hemispheres. The evidence offered is the closure test (Section 7.8, all pulls < 1σ). This closure test was performed on MC (where the data/MC C_b mismatch is absent), not on data. **The closure test does not validate the C_b = 1.0 assumption on data.** Category B: the decorrelation claim needs a data-level cross-check (e.g., showing C_b on SF-corrected data-equivalent quantities is near unity), or an explicit acknowledgment that the closure test does not cover this.

### 2.8 The kappa-combined A_FB^b: chi2 and method inconsistency

Table 6 (full data): the cross-kappa combination gives chi2/ndf = 10.9/3 (p = 0.012). This fails the consistency criterion (p < 0.05). The AN states: "reflecting the genuine kappa dependence." However, a combination with chi2/ndf = 3.6 and p = 0.012 should not produce a meaningful combined value without addressing the inconsistency. The negative kappa values (kappa=0.3: -0.009, kappa=0.5: -0.005) combined with positive values (kappa=1.0: +0.005, kappa=2.0: +0.014) produce the combined +0.0025, but the cross-kappa chi2 indicates these values are not consistent estimates of the same quantity. **Category B: the combined A_FB^b is computed from inputs with p=0.012 inconsistency without a model explaining the kappa dependence. The stated uncertainty may be underestimated if the spread reflects genuine physics rather than statistical fluctuations.**

### 2.9 Missing items from conventions/extraction.md

The extraction.md file requires:
- Calibration independence: "Each calibration must come from an observable independent of the primary result." The SF calibration uses inclusive tag fractions, which depend on R_b. The AN addresses this (Section 7.7, circularity argument) but the independence argument hinges on the closure test being on MC. **Noted — covered under §2.7.**
- Analytical vs toy propagation verification: "verify against toys for at least the dominant sources." The AN states toys are used. No analytical comparison is shown. This is the open checkbox noted in Pass 1. **Category B.**
- The operating-point stability scan must show "chi2/ndf at each scan point." Appendix A (Table A1) shows chi2/ndf for each WP configuration on 10% data. For full data, Table 2 shows chi2/ndf per WP. **Present.** However, the high chi2/ndf values (chi2/ndf = 443/7 for tight=8) indicate model failure that the AN attributes to residual flavour effects. The conventions file states: "A configuration that produces poor GoF (chi2/ndf > 3) is not a stable operating point." All full-data WPs have chi2/ndf >> 3. The stability of R_b across WPs is used as the relevant metric — the AN makes this argument explicitly. **Conditionally acceptable: the argument is made, but the conventions text suggests the high per-WP chi2 should be investigated more deeply. Category C.**

### 2.10 Cross-phase concerns from REVIEW_CONCERNS.md

**[CP1] Closure test tautology:** Addressed. The 60/40 closure test in Section 7.8 uses independent derivation/validation subsets. Pulls < 1σ. **Resolved.**

**[CP2] A_FB^b extraction formula:** The AN uses purity-corrected method (slope/f_b δ_b) rather than the 5-category chi2 fit. This was formally downscoped [D12b]. The simplified formula is the governing extraction. The downscoping documentation is adequate. **Resolved.**

**[CP3] sigma_d0 angular dependence:** The AN (Section 4.1, eq. 1) uses sin(θ) form; the systematic (Section 6.4) evaluates sin^(3/2)(θ) alternative. The initial concern is addressed. **Resolved.**

**[CP4] PDG inputs not yet fetched:** Table 1 (external inputs) shows B-hadron lifetimes from PDG 2024 (τ_B+ = 1.638 ± 0.004 ps, τ_B0 = 1.517 ± 0.004 ps, M_Z = 91.1880 ± 0.0020 GeV, Γ_Z = 2.4955 ± 0.0023 GeV). **Resolved.**

### 2.11 Page length check

The AN is approximately 3800 lines of LaTeX, including figures and appendices. Estimated rendered length: 50-70 pages. This is within the 50-100 page target. The under-30-page Category A threshold is not triggered.

---

## Summary of Findings

### Category A — Must Resolve (blocks PASS)

| ID | Location | Finding |
|----|----------|---------|
| A1 | COMMITMENTS.md, Pass 1 | 19 unchecked `[ ]` items. Most are bookkeeping gaps where content exists; 3 are genuine gaps: (i) probability tag vs N-sigma comparison absent, (ii) analytical vs toy propagation comparison not documented, (iii) constrained vs floated R_c not done (needs formal [D] entry). |
| A2 | systematics.json vs AN Table 10 | Full-data R_b systematic inconsistency: `phase_4c_fulldata.rb_total_syst` = 0.018 vs AN headline 0.027. A 49% discrepancy in the dominant uncertainty term. The JSON shows different C_b and eps_c values than the AN. The systematic table in the AN is not reproducible from the JSON. |
| A3 | systematics.json vs AN | Full-data A_FB^b systematic inconsistency: `phase_4c_fulldata.afb_total_syst` = 0.019 vs `A_FB_b_fulldata_final.syst` = 0.0021 in parameters.json vs AN value 0.0021. The phase_4c JSON value is an order of magnitude larger than what the AN reports. |
| A4 | Table 7 / Section 9.3.3 | Per-year A_FB^b values are all negative (-0.018, -0.033, -0.061, -0.084 for 1992-1995) while the combined full-data result is positive (+0.0025). The AN does not explain this contradiction. The chi2 consistency test passes within years but the absolute sign conflict between per-year and combined results indicates a methodological discrepancy. |
| A5 | Table 7 vs Section 9.3.1 | Per-year R_b values (~0.186-0.189) are ~1.5% below the full-data combined result (0.21226) at the same working point (tight=8, loose=4). The SF calibration should produce consistent values; the systematic offset between per-year and full-dataset extractions is unexplained. |

### Category B — Must Fix Before PASS

| ID | Location | Finding |
|----|----------|---------|
| B1 | Section 10 | A_FB^b comparison to LEP combined is 26 sigma below reference. The §6.8 validation target rule requires: quantitative explanation + demonstrated magnitude match + no simpler explanation. The AN provides a qualitative explanation (charm dilution) but no calculation showing the expected diluted value given known purity and A_FB^c. Add a calculation: expected_AFB^b = A_FB^b_true × f_b × δ_b / (f_b × δ_b + f_c × δ_c × A_FB^c / A_FB^b_true) to show the dilution factor. |
| B2 | Section 9.3.4 (per-year consistency) | Per-year R_b chi2/ndf = 3.57/3 (p = 0.31) uses values that are ~1.5% below the combined result. The consistency test is internally valid but the absolute calibration differs between per-year and full-dataset extractions. Document why per-year SF calibration produces systematically lower R_b. |
| B3 | validation.json | Stale: does not contain the headline full-data SF-corrected R_b stability result (chi2/ndf = 4.4/14). The headline result in the AN cannot be verified against the machine-readable JSON artifact. Update validation.json. |
| B4 | Section 7.7 / Section 5.2 | C_b = 1.0 decorrelation claim is validated only on MC closure (where data/MC C_b mismatch is absent). No data-level evidence that SF calibration actually decorrelates hemispheres is presented. Either add a data-level test or explicitly limit the claim to "the MC closure test demonstrates unbiasedness under the C_b = 1.0 assumption." |
| B5 | Section 10, Table 9 | sin²θ_eff comparison to ALEPH (0.2330 ± 0.0009) is a committed comparison target (COMMITMENTS.md line 154) but absent from the comparison tables. Add the comparison. |
| B6 | Section 9.3.2 Table 6 | Cross-kappa chi2/ndf = 10.9/3 (p = 0.012) indicates the four kappa values are inconsistent estimates. The combination should either: (a) acknowledge that the combination is invalid under inconsistency and report kappa=2.0 as primary, or (b) identify and model the kappa dependence (charm contamination model) to justify the combination. |
| B7 | COMMITMENTS.md vs AN | Checkbox bookkeeping: 16 items with content present in AN but checkboxes not ticked. Update COMMITMENTS.md to reflect actual status. |

### Category C — Apply Before Commit

| ID | Location | Finding |
|----|----------|---------|
| C1 | Section 10 (precision comparison) | Precision ratio vs LEP combined (41x) is not stated; only the ALEPH ratio (~19x) is mentioned. Add both for completeness. |
| C2 | Section 8.3 / App | Analytical uncertainty propagation: state that the toy method was verified against analytical estimates for the dominant sources (eps_c, C_b), as required by extraction.md. If not done, add a brief comparison or caveat. |
| C3 | Change Log (Section 0) | The "Known Limitations" section (13) still contains item 6 ("Limited 10% subsample statistics") which mentions future full-sample analysis as planned — the full data analysis is complete. Update this item. |
| C4 | App B (afb_details) | Table B3 (afb_all_kappa_thr2) reports A_FB^b at kappa=2.0 as +0.005 (charm-corrected) while the body Table 4 shows +0.014 for the full-data result. These are consistent (10% vs full data), but the table caption in App B does not note it is for the 10% subsample. Clarify. |

---

## Overall Verdict

**CLASSIFICATION: ITERATE (Category A findings block advancement)**

The analysis note v2 is substantially complete — the physics methodology is well-documented, the results are internally consistent at the primary level (R_b value and stat uncertainty match JSON), and most COMMITMENTS.md commitments are substantively fulfilled. The note represents serious, thorough work.

However, five Category A findings must be resolved before the note can advance to final arbiter review:

1. **A2 + A3 (systematic budget inconsistency):** The JSON files contain conflicting systematic totals. The headline R_b uncertainty (0.027) cannot be reproduced from the phase_4c systematics JSON (0.018). This is the most critical finding — the reported precision is not verifiable from the machine-readable artifacts.

2. **A4 (A_FB^b sign conflict per-year vs combined):** All four per-year A_FB^b values are negative; the combined result is positive. This contradiction must be explained or the per-year table must be updated.

3. **A5 (R_b per-year vs combined offset):** The per-year R_b values are systematically ~1.5% below the full-data single-WP result. The source of this offset must be identified.

4. **A1 (COMMITMENTS.md open items):** Three genuine gaps must be resolved (or formally downscoped): probability tag comparison, analytical/toy comparison, constrained/floated R_c cross-check.

The Category B findings (particularly B1 on the A_FB^b vs LEP comparison and B6 on the cross-kappa combination) are important for scientific integrity and must be addressed before the note is finalized.

---
*Review completed: two-pass protocol executed. Session gertrude_7ec5.*
