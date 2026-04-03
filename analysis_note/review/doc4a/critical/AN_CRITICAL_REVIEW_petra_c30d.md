# Critical Review — Analysis Note Doc 4a v5 (Complete Rewrite)
## Reviewer: petra_c30d
## Date: 2026-04-02
## Artifact: `analysis_note/ANALYSIS_NOTE_doc4a_v5.tex` + compiled PDF
## Session type: Two-pass (Pass 1: JSON–AN consistency, Pass 2: Convention/traceability/completeness)
## MCP_LEP_CORPUS: true

---

## Prefatory Note

This is a fresh review of the complete v5 rewrite. The document has been rebuilt from scratch following the human gate. I do not carry forward the verdict of prior reviewers. All findings below are my own assessments against the JSON results, COMMITMENTS.md, conventions/extraction.md, and the analysis-note specification.

---

## PASS 1 — JSON–AN CONSISTENCY AND METHODOLOGY AUDIT

### P1.1 — Primary R_b result: JSON vs AN

**JSON source:** `results/parameters.json`, field `R_b`
- value: 0.21578001028371308
- stat: 0.0002649384172009339
- syst: 0.06529879851715782
- total: 0.06529933598551582

**AN states (Abstract):** "R_b = 0.212 ± 0.001 (stat) ± 0.015 (syst)" on 10% data.
**AN states (§9.2, eq. rb_result):** "R_b = 0.212 ± 0.001 (stat) ± 0.015 (syst)"
**AN states (§9.2):** "The combined result across 15 configurations is R_b = 0.2121 ± 0.0003 (stat)"

**JSON source (10% data):** `results/parameters.json`, field `R_b_10pct_3tag_sf`
- value: 0.21215693120884146
- stat: 0.0011362194648926766

**Consistency assessment:** The AN abstract and results section quote R_b = 0.212 ± 0.001 (stat), sourced from `R_b_10pct_3tag_sf` (value 0.2122, stat 0.0011). The figure 0.212 is a rounded version of 0.2122 — acceptable rounding at 3 significant figures. The stat uncertainty 0.001 rounds 0.0011 — acceptable.

However, the **syst = 0.015** in the AN is sourced from `systematics.json` (phase_4b_10pct_v2 totals, syst = 0.014950692183304174 ≈ 0.015). This is internally consistent.

**BUT there is a significant inconsistency:** The top-level `R_b` entry in `parameters.json` carries syst = 0.06529879851715782 and total = 0.06529933598551582 — the Phase 4a MC systematic, which is 4× larger than the 10% data systematic. The AN uses the 10% data systematic throughout (0.015) but never explicitly declares that the top-level parameters.json R_b entry is the Phase 4a MC result, not the 10% result.

**FINDING [A1] — JSON struct ambiguity creates reproducibility risk (Category A):**
The top-level `R_b` in `parameters.json` (stat=0.00026, syst=0.065) is from Phase 4a MC pseudo-data (as annotated by `"phase": "4a_expected_regression"`), while the primary result of the AN is from the `R_b_10pct_3tag_sf` entry (stat=0.0011, syst=0.015). The AN §9.2 cites "R_b = 0.212 ± 0.001 (stat) ± 0.015 (syst)" without specifying which JSON field these numbers come from. The Reproduction Contract appendix (§app:reproduction) says "all numbers sourced from machine-readable JSON results" but does not trace which field. A physicist reproducing the analysis from the AN alone would likely use the top-level `R_b` entry first and obtain contradictory uncertainty figures (syst=0.065 vs 0.015). The JSON must either (a) be restructured so the primary result is unambiguous, or (b) the AN must explicitly state field paths for all key results. **Failure to resolve this makes the Reproduction Contract (§app:reproduction) misleading.**

### P1.2 — Operating point stability chi2: JSON vs AN

**JSON source:** `results/validation.json`, field `operating_point_stability`
- chi2: 8.115400772537508e-10
- ndf: 7
- chi2_ndf: 1.1593429675053582e-10
- p_value: 1.0
- n_configs: 8
- method: "3-tag system across 8 threshold configurations"

**AN states (§9.2):** "stability chi2/ndf = 0.38/14 (p = 1.0)"
**AN states (§7.4):** "stability chi2/ndf = 0.38/14 across configurations"
**AN states (Table tbl:rb_calibration):** "chi2_stab/ndf = 0.38/14"

**FINDING [A2] — Stability chi2/ndf discrepancy between JSON and AN (Category A):**
The `validation.json` records the Phase 4a MC operating point stability as chi2 = 8.1e-10 over ndf = 7 (i.e., essentially zero, 8 configurations). The AN consistently quotes chi2/ndf = 0.38/14 (15 configurations) for the 10% data SF-corrected stability. These are different tests:
- `validation.json` `operating_point_stability` = Phase 4a MC, 8 configs, chi2 ≈ 0
- AN chi2/ndf = 0.38/14 = Phase 4b 10% data, 15 configs

The problem is that `validation.json` does NOT contain an entry for the 10% data stability chi2 = 0.38/14. This number appears in `parameters.json` under `R_b_10pct_3tag_combined.stability_chi2_ndf = 55.54941080985365` and `stability_p = 0.0` — which is NOT 0.38/14 and does NOT pass. The stability test for the 10% 3-tag combined gives chi2/ndf = 55.5/7, p = 0. The AN reports 0.38/14, p = 1.0 which is a qualitatively different result.

This is a critical number inconsistency: the JSON says the 10% combined 3-tag stability chi2/ndf = 55.5/7 (FAIL), but the AN says 0.38/14 (excellent PASS). Either the JSON is stale (from before the SF-corrected method) or the AN is using a different test that is not recorded in the JSON. Either way, there is no `validation.json` entry for "SF-corrected 10% data stability chi2 = 0.38/14 across 15 WPs." **This is the most important number in the analysis and it cannot be traced to any JSON field.**

### P1.3 — A_FB^b result: JSON vs AN

**JSON source:** `parameters.json`, field `A_FB_b` (Phase 4a MC):
- value: -9.842212181052319e-05 (≈ -0.000098)
- stat: 0.0051890120160684675
- syst: 0.012174092114641622

**JSON source:** `parameters.json`, field `A_FB_b_10pct`:
- value: -0.027338898448293465
- stat: 0.008383539716223472
- syst: 0.02386394081861357
- total: 0.02529370296274919

**AN Abstract states:** "A_FB^b = 0.074 ± 0.031 (stat+syst)" at kappa=2.0

**FINDING [A3] — Primary A_FB^b result not present in any JSON field (Category A):**
The AN's primary result for A_FB^b is 0.074 at the loosest working point (threshold=2.0, kappa=2.0) with total uncertainty 0.031. This value does not appear in `parameters.json`, `systematics.json`, `validation.json`, or `covariance.json`. The `A_FB_b_10pct` entry gives -0.027 (not 0.074) with total = 0.025 (not 0.031). The AN §9.2 and appendix `tbl:afb_full_kappa` show A_FB^b at threshold=2.0 as 0.074 with sigma=0.031, but there is no JSON entry recording this value. The Reproduction Contract states "all numbers sourced from machine-readable JSON results" — this fails for the primary A_FB^b result. 

Furthermore, the mismatch between `A_FB_b_10pct` = -0.027 and the AN's 0.074 is large enough that it likely reflects different working points or methods. The JSON appears to store the best-WP result (threshold=10, consistent with `A_FB_b_10pct.subsample_fraction=0.1, n_events=288627`) while the AN quotes the loosest WP. But this distinction is nowhere explained in the JSON.

### P1.4 — Systematic totals: JSON vs AN

**JSON source:** `systematics.json`, top-level `totals.R_b`:
- stat: 0.0002649384172009339
- syst: 0.06529879851715782
- total: 0.06529933598551582

These are Phase 4a MC numbers. The corresponding 10% data totals appear under `phase_4b_10pct_v2`:
- `rb_total`: value=0.1698, stat=0.0004, syst=0.01495, total=0.01496

**AN (Table tbl:syst_rb):** Total systematic = 0.015, statistical = 0.001.

The AN systematic total of 0.015 matches `phase_4b_10pct_v2.rb_total.syst = 0.01495`. This is consistent. However the individual line items are inconsistent:

- AN: eps_c: ΔR_b = 0.013 — JSON `phase_4b_10pct_v2.rb_systematics.eps_c.delta_Rb = 0.012916` — MATCH (rounded).
- AN: eps_uds: ΔR_b = 0.006 — JSON `phase_4b_10pct_v2.rb_systematics.eps_uds.delta_Rb = 0.006388` — MATCH.
- AN: C_b: ΔR_b = 0.003 — JSON `phase_4b_10pct_v2.rb_systematics.C_b.delta_Rb = 0.003355` — MATCH.
- AN: R_c: ΔR_b = 0.002 — JSON `phase_4b_10pct_v2.rb_systematics.R_c.delta_Rb = 0.001864` — MILD MISMATCH (0.002 vs 0.00186, but rounding is acceptable).
- AN: g_cc: ΔR_b = 0.0002 — JSON `phase_4b_10pct_v2.rb_systematics.g_cc.delta_Rb = 0.00011452` — **INCONSISTENCY**: AN rounds up to 0.0002 but JSON gives 0.000115. These are combined (g_bb + g_cc in the AN as a single 0.0002 line). g_bb = 0.000111 + g_cc = 0.000115 = 0.000226; rounding to 0.0002 is acceptable.

The A_FB^b systematics in the AN (Table tbl:syst_afb) cite charge model = 0.021. The JSON `phase_4b_10pct_v2.afb_systematics.charge_model.delta_AFB = 0.02148631620532875`. MATCH.

**Overall P1.4:** Systematic budget numbers are consistent between the AN and the 10% phase_4b JSON data, but use of Phase 4a top-level systematics entries in the JSON for cross-checking is impossible because they reflect different (MC-only) systematics. The dual structure of the JSON file creates confusion.

### P1.5 — Covariance matrix: JSON vs AN

**JSON source:** `covariance.json`
- correlation_matrix[0][1] = 0.09199142014252694 (R_b–A_FB^b correlation)

**AN (Appendix app:covariance, eq:covariance):** ρ ≈ 0.15

**FINDING [B1] — Covariance matrix correlation value inconsistent (Category B):**
The `covariance.json` records the R_b–A_FB^b correlation as ρ = 0.092, but the AN equation states ρ ≈ 0.15 in the covariance matrix. The AN text says "ρ ≈ 0.15 is the correlation coefficient arising from the shared eps_c systematic." The discrepancy (0.092 vs 0.15) is ~60% and cannot be attributed to rounding. Either the JSON is computed from Phase 4a MC efficiencies (where eps_c is different) or the AN value was estimated rather than computed. Given that covariance.json also mixes Phase 4a and 10% data in a single file with no version tag, this is plausible — but the AN must use the JSON value (0.092) or the JSON must be updated.

### P1.6 — Closure test: JSON vs AN

**JSON source:** `validation.json`, field `independent_closure_3tag`
- Four configurations, all passes=true
- Pulls: +0.59, -0.41, +0.34, +0.06

**AN (Table tbl:closure, §7.5):** Reports same four configs with pulls +0.59, -0.41, +0.34, +0.06.

MATCH. The independent closure test data traces perfectly from JSON to AN.

### P1.7 — Phase 4a MC R_b: JSON vs AN

**JSON source:** `parameters.json`, field `R_b`
- value: 0.21578001028371308
- stat: 0.0002649384172009339
- stability_chi2_ndf: 1.1593429675053582e-10 (≈ 0)

**AN (§9.1):** "R_b = 0.21578 ± 0.00026 (stat) with operating point stability chi2/ndf = 0.00/7 (p = 1.0)"

MATCH (chi2/ndf ≈ 1.16e-10 rounds to 0.00/7; p_value = 1.0). The identically-zero chi2 is explained in the AN as expected on MC. However:

**FINDING [B2] — Chi2 = 0 on MC is a protocol red flag (Category B):**
Per the orchestrator regression checklist (CLAUDE.md), "Is the fit chi2 identically zero? If so, investigate whether the methodology is algebraically circular before accepting. chi2 = 0.000 is an alarm, not a result." The AN §9.1 addresses this explicitly ("The identically zero chi2 is expected on MC: when the same sample is used for both calibration and extraction, the calibrated efficiencies exactly reproduce the observed fractions at the SM R_b") and points to the independent closure test. The explanation is present and the independent closure test is documented. The convention file `extraction.md` warns: "A self-consistent extraction (deriving efficiencies and counting yields from the same sample) always recovers the correct answer by construction — this is an algebra check, not a closure test." The AN correctly identifies this. **This finding is partially mitigated** — the acknowledgment and the independent closure test exist. However, the AN should quote the chi2 of the Phase 4a extraction on the **independent validation half** (not just the combined chi2 of the 4 configs in Table tbl:closure) to make the distinction between self-consistency and closure explicit. Currently §9.1 says "The independent closure test validates the method's unbiasedness with non-trivial chi2 values" without quoting those chi2 values. The individual per-WP extraction chi2 from the 40% validation subset is not reported.

---

## PASS 2 — CONVENTION COVERAGE, SYSTEMATIC COMPLETENESS, DECISION TRACEABILITY

### P2.1 — extraction.md: Required systematic sources coverage

Checking against `conventions/extraction.md` "Required systematic sources":

**Efficiency modeling:**
- [x] Tag/selection efficiency (sigma_d0 ±10%, sigma_d0 form) — PRESENT
- [x] Efficiency correlation (C_b) — PRESENT  
- [x] MC efficiency model (hadronization) — PRESENT

**Background contamination:**
- [x] Non-signal contamination (eps_c, eps_uds) — PRESENT
- [x] Background composition (R_c, g_bb, g_cc, tau) — PRESENT

**MC model dependence:**
- [x] Hadronization model (Peterson vs Bowler-Lund) — PRESENT
- [x] Physics parameters (B lifetimes, decay multiplicities) — PRESENT

**Sample composition:**
- [x] Flavour composition (R_c variation) — PRESENT
- [D] Production fractions — Formally downscoped per COMMITMENTS.md [D] entry with justification.

**Convention coverage: COMPLETE.** All required systematic categories from `extraction.md` are covered or formally downscoped with documented justification.

### P2.2 — extraction.md: Required validation checks

1. **Independent closure test (Category A if fails):** PRESENT — §7.5, Table tbl:closure. Four MC configurations, all pulls < 1 sigma. PASS.

2. **Parameter sensitivity table:** PRESENT — Appendix app:sensitivity, Table tbl:sensitivity. eps_c contributes 13× stat. PASS.

3. **Operating point stability:** PRESENT — §7.4. SF-corrected: 0.38/14 (as reported in AN; JSON discrepancy flagged in [A2]). NOTE: The convention requires reporting chi2/ndf at EACH scan point alongside the extracted value. The AN table `tbl:rb_all_wp` in the appendix reports individual chi2/ndf values (17–28/7) at each configuration alongside R_b. PASS for the 10% data SF result. However the convention warns: "A configuration that produces a small statistical uncertainty but poor GoF (chi2/ndf > 3) is not a stable operating point." ALL 15 configurations have chi2/ndf > 2 (range 17–28 for ndf=7). The AN §8.3 acknowledges this: "the individual chi2/ndf values range from 17/7 to 28/7 (p = 0.001–0.016)" and explains the cancellation in R_b extraction. But no working point has acceptable GoF. **This should be flagged per convention requirements.** See [A4].

4. **Per-subperiod consistency:** The AN §7.4 reports "chi2/ndf = 0.94/3, p = 0.82 on random MC subsets." Per-year analysis on data deferred to Phase 4c with justification. The convention says "Extract the result independently for each data-taking period." Deferral is documented in COMMITMENTS.md [D]. **DEFERRED but documented — acceptable at Phase 4b.**

5. **10% diagnostic sensitivity:** PRESENT — §7.6 tag fraction comparison, Table tbl:working_points. Data/MC differences of 1–5% documented. PASS.

**FINDING [A4] — No working point has acceptable GoF; convention violation not addressed (Category A):**
`extraction.md` §3 ("Operating point stability") states: "A configuration that produces a small statistical uncertainty but poor GoF (chi2/ndf > 3) is not a stable operating point — it indicates the model does not describe the data at that configuration." Every one of the 15 SF-corrected working points has chi2/ndf = 17/7 to 28/7 (all > 3 when computed as chi2/(7 ndf) = 2.4 to 4.0). The AN §8.3 explains that "the model tension cancels in the R_b extraction" but this explanation does not satisfy the convention requirement. The convention says the GoF failure must be "understood and demonstrated not to bias the result." "Model tension cancels in R_b extraction" is an assertion, not a demonstration. Required: either (a) a toy study showing that artificial tag-fraction residuals of similar chi2 magnitude do not bias R_b, or (b) citing a published reference that demonstrates this cancellation property of the three-tag overconstrained system. Neither is present.

### P2.3 — COMMITMENTS.md key decisions: traceability

Checking that all [D] decisions are traceable in the AN:

- **[D1] Observable definitions LEP EWWG standard:** AN §1 cites hep-ex/0509008 for all observable definitions. PASS.
- **[D2/D2-REVISED] PRIMARY R_b: 3-tag system:** AN §4.4 and §5.1 describe the three-tag system. PASS.
- **[D3] Simplified two-tag system (now superseded by D2-REVISED):** AN correctly presents 3-tag as primary with 2-tag as background. PASS.
- **[D4/D4-REVISED] PRIMARY A_FB^b: purity-corrected extraction:** AN §5.3 and §5.4. PASS.
- **[D5] kappa = {0.3, 0.5, 1.0, 2.0, infinity}:** AN §4.5, Table tbl:qfb shows all five. PASS (note: kappa=infinity is characterized but not used in the purity-corrected extraction because no published delta_b for kappa=infinity is cited — this is not explained).
- **[D6] R_c constrained:** AN §5.1 and Table tbl:external_inputs. PASS.
- **[D7] sigma_d0 from negative d0 tail calibration:** AN §4.1. PASS.
- **[D12a] Angular binning uniform across years:** AN §5.3 uses 8 cos(theta) bins. PASS.
- **[D13] Toy-based uncertainty propagation:** AN §8.3. PASS.
- **[D14] Multi-working-point extraction:** AN Table tbl:rb_all_wp. PASS.
- **[D20] C_b = 1.01 external input (Phase 4b):** AN §5.2 and §6.3 explain C_b = 1.0 for SF extraction. **FINDING [B3]** (see below).
- **[D19] d0 sign convention validation:** AN Appendix app:d0_sign_detail. PASS.

**FINDING [B3] — D20 commitment partially misstated in AN (Category B):**
COMMITMENTS.md [D20] specifies C_b = 1.01 as the external input for Phase 4b R_b extraction, citing published ALEPH value. The AN §5.2 (Corrections) and the Limitation Index appendix say "C_b = 1.0 for SF extraction." The external inputs table (Table tbl:external_inputs) lists "C_b: 1.0 (SF method)." The discrepancy between 1.0 (AN) and 1.01 (COMMITMENTS) is small but COMMITMENTS.md explicitly says "C_b = 1.01 external input" with the ALEPH citation. If the SF method assumes C_b = 1.0 exactly (decorrelated limit), this must be stated as a distinct choice from the ALEPH C_b = 1.01. The current text conflates them.

### P2.4 — Convention: Calibration independence

`extraction.md` states: "Calibration independence is mandatory. Each calibration must come from an observable that is independent of the primary result."

The tag-rate scale factors are defined as SF_cat = f_cat^data / f_cat^smeared_MC. These scale factors are applied to the efficiency calibration, and then the same tagged fractions are used to extract R_b. This creates a potential circularity: if SF_cat already encodes information about R_b through the tag fraction ratios, then the extraction is not independent.

**FINDING [B4] — SF calibration independence not demonstrated (Category B):**
The SF calibration uses the same observed tag fractions (f_tight, f_loose, f_anti) from data that are subsequently used in the chi2 minimization to extract R_b. The SF effectively normalizes the MC efficiencies to match the data tag rates before extraction. This is not strictly independent: the data tag rates carry information about R_b. The convention file flags this as: "Deriving the correction by assuming the primary result equals a reference value (back-substitution) is a diagnostic, not a calibration." The SF method is not quite back-substitution (it doesn't assume a specific R_b), but it uses the same observables for calibration and extraction. The AN does not address this potential circularity. A brief argument is needed: either (a) the SF calibration is insensitive to R_b (because it operates on flavour-inclusive fractions), or (b) the bias from this circularity is bounded and shown to be small.

### P2.5 — Convention: GoF and the self-calibrating chi2

`extraction.md` §3 states: "The stability scan must include fit quality. Report chi2/ndf... at each scan point."

The AN Table tbl:rb_all_wp does include chi2/ndf at each working point. However, these chi2 values are for the 3-tag fraction chi2 (the model fit to 8 observables), not the stability chi2. The stability chi2 (whether R_b varies across configurations) is separate and reported only as a combined value (0.38/14). The convention's intent is that each extraction point be evaluated for GoF.

**Status: PARTIALLY MET.** The AN reports individual chi2/ndf at each WP (Appendix Table tbl:rb_all_wp) which satisfies the letter of the requirement, but the interpretation in §8.3 needs to be strengthened (see [A4]).

### P2.6 — Convention: "Running on real data in Phase 4a" pitfall

The convention warns against computing the extraction on real data in Phase 4a. The document header states "Doc 4b v5" (a typo; the AN is labelled as doc4a in the filename) and refers to "10% data validation results." The AN presents 10% data results extensively throughout, including as the primary quoted result in the Abstract.

**FINDING [A5] — Phase identification conflict (Category A):**
The document filename is `ANALYSIS_NOTE_doc4a_v5.tex`, but the change log header reads "Doc 4b v5: Full rewrite from scratch..." and the AN contains extensive 10% data results as the primary result (Abstract, §9.2, all comparison tables). Phase 4a should produce results on MC pseudo-data only, per `extraction.md`: "The expected result must be computed on MC-generated pseudo-data counts, not on real data." The 10% data results belong in Doc 4b. The document appears to be a combined Doc 4a + 4b note — which is not the protocol. The protocol stages these separately: Doc 4a documents MC expected results, Doc 4b introduces 10% data results.

This has a cascading effect: the 10% data primary result (R_b = 0.212 ± 0.015) is the central AN result, but per protocol it belongs in Doc 4b. Doc 4a should present R_b = 0.21578 ± 0.00026 (stat) on MC pseudo-data as the "expected" result, with the full systematic budget evaluated on that MC extraction. The document is conflating two phases.

**Note:** I recognize this may reflect a deliberate choice by the orchestrator (combining 4a+4b into a single document given the regression history), but it is a protocol deviation that must be documented explicitly in the AN if intentional, with a note that the "Doc 4a" label covers both expected and 10%-data-validated stages.

### P2.7 — A_FB^b result: working-point dependence disclosure

The AN §9.2 quotes A_FB^b = 0.074 at kappa=2.0 as the primary result, but Appendix Table tbl:afb_full_kappa shows the result ranges from -0.032 (kappa=0.3) to +0.074 (kappa=2.0) and threshold-dependent values at kappa=2.0 range from -0.014 (threshold=9.0) to +0.052 (threshold=12.0). The stated primary result is at the extreme positive end of the distribution.

**FINDING [B5] — Primary A_FB^b result selection not adequately justified (Category B):**
The AN selects threshold=2.0, kappa=2.0 as the primary result (A_FB^b = 0.074) on the grounds that this working point gives the largest sample and smallest purity corrections. However:
1. At threshold=3.0, kappa=2.0, the result is +0.015 — qualitatively different from 0.074.
2. At threshold=5.0, kappa=2.0, the result is -0.006 — sign-flipped.
3. The cross-kappa chi2/ndf = 6.51/3 (p = 0.089) indicates marginal consistency, meaning the four kappa values are not statistically consistent with each other.

The AN §app:afb_interpretation acknowledges the working-point dependence but does not explain why 0.074 (threshold=2.0) is quoted as the "primary" when 0.015 (threshold=3.0) differs by 4×. If the loosest working point is claimed to be most reliable because purity corrections are smallest, the AN must quantify the purity correction magnitude at threshold=2.0 vs threshold=3.0 and show it is indeed smaller. Currently this is asserted without the quantitative support.

Furthermore, the Abstract says A_FB^b is "approximately 2sigma below the LEP combined value" — but 0.074 vs 0.0992 is (0.0992 - 0.074) / 0.031 = 0.82 sigma, not 2 sigma. The conclusions §11 repeat "approximately 2sigma below" — same inconsistency.

**FINDING [A6] — Abstract pull claim for A_FB^b is wrong (Category A):**
Abstract: "approximately 2sigma below the LEP combined value of A_FB^{0,b} = 0.0992 ± 0.0016."
Computed pull: (0.0992 - 0.074) / 0.031 = 0.81 sigma.
Conclusions §11: "approximately 2sigma below the LEP combined pole value."
This is incorrect by a factor of ~2.5. The correct statement is "approximately 0.8 sigma below." Note that the LEP value is A_FB^{0,b} (pole asymmetry, corrected) while the AN's 0.074 is A_FB^b (measured, not pole-corrected). The comparison is therefore also potentially incorrect in type — A_FB^b (measured at sqrt(s)) vs A_FB^{0,b} (pole extrapolated) differ by QCD and ISR corrections (delta_QCD = 0.0356). The Abstract should clarify whether the comparison is to A_FB^b or A_FB^{0,b} and apply the appropriate correction before computing the pull.

### P2.8 — Duplicate figure label in LaTeX

**FINDING [B6] — Duplicate \label in appendix (Category B):**
At line 2570–2571 of the .tex file, a single figure environment has two \label commands:
```latex
\label{fig:datamc_sphericity}
\label{fig:datamc_d0}
```
Both labels appear on the same figure environment. Cross-referencing either label will point to the same figure, which is correct for a composite, but the Auxiliary Plots section header says "\cref{fig:datamc_sphericity}" and "\cref{fig:datamc_d0}" as if they are different figures. Additionally, the figure summary table (app:figure_summary) lists them separately: `\ref{fig:datamc_sphericity}` for "Sphericity + d0" and does not separately list fig:datamc_d0. This will produce a duplicate cross-reference in the TOC/figure list and is a LaTeX rendering issue.

### P2.9 — sin2theta_eff extraction formula

The AN equation (eq:sin2theta) gives:
```
sin2theta_eff = (1/4)(1 - sqrt(1 - sqrt(16/3 * A_FB^{0,b} / A_b)))
```
This is a non-standard form. The standard extraction is via A_FB^{0,b} = (3/4) A_e A_b with A_e ≈ A_b ≈ 2v_f a_f / (v_f^2 + a_f^2) in the limit of equal lepton/b couplings.

**FINDING [C1] — sin2theta_eff formula in Introduction should cite its derivation (Category C):**
Equation (eq:sin2theta) in §1 is presented without derivation or citation. In practice sin2theta_eff is extracted by numerically inverting A_e(s2t) × A_b(s2t) = (4/3) A_FB^{0,b}, using parameterized formulae for A_e(s2t) and A_b(s2t) that include radiative corrections. The closed-form in the AN assumes A_b = 0.935 (SM value) independently of sin2theta_eff, which may not be stated. Cite the specific inversion procedure used (LEP EWWG 2005 §6.3 or equivalent).

### P2.10 — sigma_d0 angular dependence resolution

REVIEW_CONCERNS.md cross-phase concern [CP3] raised: "Strategy parameterizes sigma_d0 with sin^{3/2}(theta) (3D form); the d0 branch appears to be R-phi (2D), for which the correct form is sin(theta)."

**AN (eq:sigma_d0):** Uses sin(theta) form: sigma_d0 = sqrt(A^2 + (B / (p sin theta))^2)

This is the 2D (R-phi) form, consistent with [CP3]'s recommendation. The prior cross-phase concern is now resolved in the AN. PASS.

However, the detector description §2.1 states: "the transverse impact parameter resolution is approximately sigma_d0 ≈ 25 + 70/(p sin^{3/2} theta) μm ... citing ALEPH:Rb:precise." Then §4.1 gives the calibration formula using sin(theta). These two forms (sin^{3/2} in detector description, sin in calibration) are inconsistent within the same document.

**FINDING [B7] — Inconsistent sigma_d0 angular dependence within the AN (Category B):**
§2.1 quotes sin^{3/2}(theta) from the ALEPH VDET reference, while §4.1 (eq:sigma_d0) uses sin(theta). The systematic for the form difference (delta_Rb = 0.0004) is evaluated and documented. But the document says different things in two sections without explaining that the 3/2 form is the published formula while the sin form is the analysis choice (from the CP3 investigation that found d0 is 2D). The text in §4.1 and the systematic §6.5 should explicitly resolve this: "The ALEPH published resolution parameterization uses sin^{3/2}(theta) appropriate for the 3D impact parameter; our analysis uses sin(theta) because the stored d0 is the 2D R-phi impact parameter. The systematic variation between the two forms contributes delta_Rb = 0.0004."

### P2.11 — ITC described as not used but nvdet/ntpc cuts described

The track selection §3.2 says "its hit count (nitc) contributes to the overall track quality but is not used as an independent selection variable." Then the selection uses nvdet > 0, highPurity = 1, ntpc > 4. The ITC is thus not used in any explicit selection cut. This is internally consistent and clearly stated. No issue.

### P2.12 — Charm efficiency: eps_c > eps_b in tight tag

The AN §5.2 (introduction to purity) states: "the b-purity is only f_b ≈ 0.18, with charm dominating at f_c ≈ 0.42." The efficiency table (tbl:efficiencies) shows eps_c^tight = 0.360 and eps_b^tight = 0.497 — so eps_c < eps_b in the tight category, which is correct. But the purity f_c > f_b because R_c / R_b is nearly 1:1.25, and eps_c / eps_b = 0.72, so the charm purity is boosted. The AN §2.3 states eps_c > eps_b — this appears in §6.1: "eps_c = 0.285" vs "eps_b = 0.371" on 10% data SF-corrected (Table tbl:efficiencies_sf). The SF-corrected eps_c (0.276) < eps_b (0.371) — so still eps_c < eps_b. The phrase "charm efficiency exceeds eps_c/eps_b ≈ 0.77" in §6.1 is a ratio, not saying eps_c > eps_b. No factual inconsistency here, but the language could mislead. PASS (minor clarity issue, not a finding).

### P2.13 — Per-kappa A_FB^b: kappa=infinity not in purity extraction

The jet charge table (tbl:qfb) presents <Q_FB> for kappa = {0.3, 0.5, 1.0, 2.0, infinity}. But the purity-corrected A_FB^b extraction (§5.3, Table tbl:afb_per_kappa, Table tbl:afb_all_kappa_thr2) includes only kappa = {0.3, 0.5, 1.0, 2.0}. The kappa=infinity case is excluded. The COMMITMENTS.md [D5] commits to kappa = {0.3, 0.5, 1.0, 2.0, infinity}.

**FINDING [B8] — kappa=infinity excluded from A_FB^b extraction without documented justification (Category B):**
[D5] commits to five kappa values. The AN evaluates only four for A_FB^b. No published delta_b for kappa=infinity is cited in any table (Table tbl:external_inputs, app:constants). The absence of the kappa=infinity result in the purity-corrected extraction is never explained. If delta_b(kappa=infinity) is unavailable from hep-ex/0509008, this must be stated. If it is available, the result must be included. This is a binding commitment.

### P2.14 — Per-year consistency on real data

COMMITMENTS.md lists "Per-year consistency: chi2/ndf = 0.94/3, p = 0.82 on random MC subsets" as resolved [x]. The real per-year test is deferred to Phase 4c. The AN §7.3 (implicit in §12.6 Future Directions) mentions this deferral. No specific section in the AN discusses the MC-subset per-year test result (chi2/ndf = 0.94/3, p = 0.82). This is documented in COMMITMENTS but absent from the AN.

**FINDING [C2] — MC per-year consistency result (chi2/ndf=0.94/3, p=0.82) not quoted in AN (Category C):**
The COMMITMENTS.md records this validation result as [x] resolved. The AN omits it. It should appear in §7 (Cross-Checks) or the Statistical Method section, with a note that this was done on random MC subsets as a proxy for per-year stability until full data is available.

### P2.15 — Reproduction contract vs JSON field ambiguity

See [A1]. The reproduction contract claims "all numbers sourced from machine-readable JSON results" but the primary results (R_b stability chi2, A_FB^b = 0.074) cannot be traced to any JSON field. This makes the contract false.

---

## OVERALL ASSESSMENT

### Category A findings (must resolve before PASS):

- **[A1]** JSON struct ambiguity: top-level parameters.json carries Phase 4a MC numbers (syst=0.065) while AN primary result uses 10% numbers (syst=0.015) from different JSON fields. Reproduction Contract is misleading.
- **[A2]** Stability chi2/ndf = 0.38/14 (AN) vs chi2/ndf = 55.5/7 (JSON `R_b_10pct_3tag_combined`) — major numerical inconsistency for the most critical validation number in the analysis.
- **[A3]** Primary A_FB^b = 0.074 ± 0.031 not present in any JSON results file. JSON records -0.027 at the best WP. Reproduction Contract fails for the primary A_FB^b result.
- **[A4]** All 15 working points have chi2/ndf > 2.4 (range 2.4–4.0). Convention requires showing GoF failure does not bias R_b — the assertion "model tension cancels" is unsupported. A toy study or published reference required.
- **[A5]** Phase identification conflict: filename says doc4a, change log says "Doc 4b v5", and the primary results are 10% data (belonging in Doc 4b). This must be explicitly resolved.
- **[A6]** Abstract and Conclusions state A_FB^b is "approximately 2sigma below" LEP combined — computed pull is 0.81 sigma. Also, A_FB^b (measured) is compared directly to A_FB^{0,b} (pole-corrected) without applying the QCD/QED corrections (delta_QCD = 0.0356) — not an apples-to-apples comparison.

### Category B findings (fix before PASS):

- **[B1]** Covariance matrix: AN states ρ ≈ 0.15, covariance.json records ρ = 0.092.
- **[B2]** Chi2=0 on MC Phase 4a is acknowledged as expected but the independent closure test chi2 per WP is not quoted, weakening the distinction between self-consistency and true closure.
- **[B3]** D20 specifies C_b = 1.01 (ALEPH value); AN uses C_b = 1.0 (exact), without acknowledging the 0.01 difference.
- **[B4]** SF calibration independence not demonstrated — same tag fractions used for SF calibration and R_b extraction may introduce circularity.
- **[B5]** A_FB^b = 0.074 (threshold=2.0) vs 0.015 (threshold=3.0) differ by 4× with no quantitative justification for preferring threshold=2.0.
- **[B6]** Duplicate \label in appendix figure environment.
- **[B7]** sigma_d0 form inconsistency within AN (sin^{3/2} in §2.1, sin in §4.1) not resolved with an explanation.
- **[B8]** kappa=infinity excluded from A_FB^b extraction, violating [D5] commitment, without documented justification.

### Category C findings (suggestions):

- **[C1]** sin2theta_eff inversion formula in Introduction missing citation for specific parameterization used.
- **[C2]** MC per-year consistency chi2/ndf = 0.94/3, p = 0.82 documented in COMMITMENTS.md but absent from the AN.

---

## VERDICT

**Classification: B (Cannot PASS with unresolved A or B findings)**

The v5 rewrite represents a substantial improvement over prior versions. The document structure is clean, the systematic budget is well-organized, external inputs are cited, and the limitation index is thorough. The independent closure test passes with well-documented pulls, and the data-driven calibration story (raw → smeared → SF-corrected) is clearly narrated.

However, six Category A findings block a PASS verdict:

The most serious are [A2] (stability chi2/ndf discrepancy between JSON and AN for the primary validation number), [A3] (primary A_FB^b result untraced to any JSON), and [A6] (2sigma claim for A_FB^b is wrong by a factor of ~2.5). These are not editorial issues — they are failures of the primary results section to match the documented evidence. They must be resolved before any re-review.

[A5] (phase identification) requires a clear statement of whether this is a combined Doc 4a+4b document (permissible but must be declared) or a mislabelled Doc 4b. [A1] (JSON ambiguity) must be resolved for the Reproduction Contract to be honest. [A4] (GoF failure across all working points) requires either a toy study or a published reference.

The eight Category B findings are individually tractable and can be resolved in a single iteration.

**Recommended next action:** Fixer agent addresses all A and B findings, pays particular attention to reconciling the stability chi2/ndf and A_FB^b values with their JSON sources, and then the arbiter verifies before re-review.

---

*Signed: petra_c30d | 2026-04-02 | Two-pass review complete*
