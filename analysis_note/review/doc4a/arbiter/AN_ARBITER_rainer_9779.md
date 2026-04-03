# Arbiter Adjudication — Doc 4a v5

**Arbiter:** rainer_9779
**Date:** 2026-04-02
**Inputs:** Physics (joe_a13d, 0A/5B), Critical (petra_c30d, 6A/8B), Validation (sally_6783, 0A/8B)

---

## Key Investigation: JSON Tracing

Before adjudicating, I traced the two disputed numbers through the JSON files:

1. **Stability chi2 = 0.38/14.** Found in `phase4_inference/4b_partial/outputs/d0_smearing_results.json`, field `step5_scale_factor_extraction.stability`: chi2 = 0.3787, ndf = 14, p = 1.0. This is the SF-corrected stability across 15 working points. The `parameters.json` field `R_b_10pct_3tag_combined.stability_chi2_ndf = 55.5` is a DIFFERENT quantity: the raw (non-SF-corrected) 3-tag combined stability across 8 configs. Both are real numbers from different methods. The AN correctly quotes 0.38/14 for the SF-corrected result but fails to record it in the canonical `validation.json` or `parameters.json`.

2. **A_FB^b = 0.074.** Found in `phase4_inference/4b_partial/outputs/delta_b_calibration.json`, field `kappa_results.k2.0.extraction_results[0]` (threshold=2.0): `afb_purity_corrected = 0.07366`, `sigma_afb_purity = 0.03088`. This is the purity-corrected (pre-charm-correction) value. The `parameters.json` field `A_FB_b_10pct = -0.027` is the charm-corrected value at the best working point (threshold=10, kappa=2.0). These are different methods AND different working points. Both are real.

**Conclusion:** The critical reviewer's A2 and A3 findings correctly identify that these numbers are not in the canonical JSON files (`parameters.json`, `validation.json`). The numbers are traceable to auxiliary output JSON files, but the AN's Reproduction Contract claims "all numbers sourced from machine-readable JSON results" -- this is technically true but misleading when the canonical results files disagree with what the AN quotes.

---

## Adjudication Table

| ID | Source | Finding | Claimed | Adjudicated | Rationale |
|----|--------|---------|---------|-------------|-----------|
| **A1** | petra | JSON struct ambiguity: top-level R_b is Phase 4a MC, AN quotes 10% | A | **B** | Real issue -- JSON needs restructuring or AN needs explicit field paths. But the 10% numbers ARE in the JSON (`R_b_10pct_3tag_sf`), just not top-level. Downgrade because the numbers are present; the problem is navigation, not absence. |
| **A2** | petra | Stability chi2: AN says 0.38/14, JSON says 55.5/7 | A | **B** | Investigated: 0.38/14 is in `d0_smearing_results.json` (SF-corrected, 15 WPs); 55.5/7 is in `parameters.json` (raw 3-tag, 8 WPs). Both real. The AN correctly uses the SF-corrected value. Fix: propagate 0.38/14 into `validation.json` so the canonical file has it. Not blocking because the number is correct and traceable. |
| **A3** | petra | A_FB^b = 0.074 not in any JSON | A | **B** | Investigated: 0.07366 is in `delta_b_calibration.json` at kappa=2.0, threshold=2.0 (purity-corrected, pre-charm). The `-0.027` in `parameters.json` is charm-corrected at a different WP. Fix: add the primary quoted A_FB^b to `parameters.json` with method annotation. Not blocking because traceable. |
| **A4** | petra | All 15 WPs have chi2/ndf > 2.4; convention requires demo that GoF failure doesn't bias R_b | A | **A** | Upheld. The per-WP chi2/ndf = 17-28/7 is a genuine concern. The AN asserts "model tension cancels" but provides no quantitative support (toy study, published reference, or analytical argument). The convention is explicit. This blocks. |
| **A5** | petra | Phase identification: doc4a filename but doc4b content | A | **C** | This is a known deliberate choice by the orchestrator to combine 4a+4b into a single document after regression. The change log header typo ("Doc 4b v5") is a copy-paste error already caught by validation (sally F11). Add a one-line note in the introduction stating the document covers both expected and 10% validation stages. |
| **A6** | petra | "2sigma below LEP" claim is wrong (actual: 0.8sigma) | A | **A** | Upheld. Pull = (0.0992 - 0.074)/0.031 = 0.81sigma, not ~2sigma. Also, the comparison mixes A_FB^b (measured) with A_FB^{0,b} (pole). Both errors are in the Abstract and Conclusions. Must fix. |
| **B1** | petra | Covariance rho: AN 0.15 vs JSON 0.092 | B | **B** | Confirmed. 60% discrepancy. AN must use the JSON value or explain. |
| **B2** | petra | Chi2=0 on MC is red flag; per-WP closure chi2 not quoted | B | **C** | The AN already explains this (self-consistency on same sample) and has the independent closure test. The physics reviewer found this convincing. Downgrade to suggestion: quote per-WP chi2 from the independent closure test for completeness. |
| **B3** | petra | C_b = 1.0 (AN) vs 1.01 (COMMITMENTS D20) | B | **C** | The 0.01 difference propagates to delta_R_b ~ 0.0001, well below the systematic floor. State the choice explicitly ("C_b = 1.0 for SF extraction, vs ALEPH C_b = 1.01; difference is negligible"). |
| **B4** | petra | SF calibration independence: same tag fractions for calibration and extraction | B | **B** | Legitimate concern. The SF method uses flavour-inclusive tag fractions, which carry R_b information. The independent closure test (pulls < 1sigma on 4 configs) provides indirect evidence of no bias, but the argument should be stated explicitly. |
| **B5** | petra | A_FB^b WP selection: 0.074 (thr=2.0) vs 0.015 (thr=3.0) | B | **B** | The 4x variation across thresholds is real and the AN should quantify the purity correction magnitude at each threshold to support the claim that threshold=2.0 is most reliable. The physics reviewer (B5) also flags this. |
| **B6** | petra | Duplicate \label in appendix | B | **C** | Mechanical LaTeX issue already caught by validation (sally F10). Fix but not blocking. |
| **B7** | petra | sigma_d0 form inconsistency (sin^3/2 vs sin) | B | **B** | Real: two different forms in different sections without explanation. Add the clarifying sentence petra suggests. |
| **B8** | petra | kappa=infinity excluded from A_FB^b, violating D5 | B | **B** | Real commitment violation. Either include kappa=infinity with the published delta_b (if available) or formally revise D5 with justification. |
| **B1-B5** (joe) | physics | 5 findings (SF flavour validation, fit-model syst, rho derivation, contamination ratio, cross-kappa sign flip) | B | **B** | All 5 upheld as B. These are genuine physics improvements, none blocking. |
| **F1-F8** | sally | 8 validation B findings (legend errors, workflow artifacts, caption mismatch, figsize) | B | **B** | All upheld. Mechanical fixes. |
| **F9-F12** | sally | 4 validation C findings | C | **C** | Upheld as suggestions. |
| **C1-C2** | petra | sin2theta citation, MC per-year chi2 absent from AN | C | **C** | Upheld. |
| **C1-C4** | joe | Abstract breakdown, expected slope overlay, repro contract sizes, Section 11 praise | C | **C** | Upheld. |

---

## Summary of Adjudicated Classifications

| Category | Count | IDs |
|----------|-------|-----|
| **A** | 2 | petra-A4 (GoF demo), petra-A6 (2sigma claim) |
| **B** | 18 | petra: A1->B, A2->B, A3->B, B1, B4, B5, B7, B8; joe: B1-B5; sally: F1-F8 |
| **C** | 10 | petra: A5->C, B2->C, B3->C, B6->C, C1, C2; joe: C1-C4 |

---

## Verdict: ITERATE

Two Category A findings block PASS:

1. **A4 (GoF demo):** All 15 SF-corrected working points have chi2/ndf = 2.4-4.0. The AN asserts "model tension cancels in R_b extraction" without supporting evidence. Required: either (a) a toy study injecting artificial tag-fraction residuals of comparable magnitude and showing R_b is unbiased, or (b) citing a published reference that demonstrates this cancellation for overconstrained tag systems, or (c) an analytical argument from the chi2 decomposition showing the R_b-sensitive and R_b-insensitive directions in the fit are orthogonal to the model tension.

2. **A6 (pull claim):** Abstract and Conclusions state "approximately 2sigma below LEP combined." Correct pull is 0.81sigma. Additionally, A_FB^b (measured at sqrt(s)) is compared to A_FB^{0,b} (pole-corrected) without applying delta_QCD corrections. Fix both the number and the comparison type.

The 18 Category B findings should be addressed in the same iteration. Priority order for the fixer:

1. Fix the 2sigma claim (A6) -- trivial text edit
2. Add GoF demonstration (A4) -- requires either a toy study or analytical argument
3. Propagate SF-corrected stability chi2 into `validation.json` (from A2 downgrade)
4. Add primary A_FB^b = 0.074 to `parameters.json` with method annotation (from A3 downgrade)
5. Fix covariance rho to match JSON (B1)
6. Add SF calibration independence argument (B4)
7. Quantify threshold=2.0 purity correction advantage (B5)
8. Resolve sigma_d0 form inconsistency (B7)
9. Address kappa=infinity commitment (B8)
10. Fix all 8 validation findings (sally F1-F8) -- figure regeneration + text edits
11. Address physics reviewer B1-B5 -- text additions

Category C items should be applied before the next review round but do not require re-review.

---

*Signed: rainer_9779 | 2026-04-02*
