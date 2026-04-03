# Phase 3 Selection — Critical Review (Iteration 2)

**Session:** erik_352e
**Date:** 2026-04-02
**Artifact under review:** `phase3_selection/outputs/SELECTION.md` (magnus_1207, 482 lines)
**Prior review:** boris_44b7 (7A + 5B in iteration 1)
**MCP_LEP_CORPUS:** true (corpus tools available per TOGGLES.md)

---

## Review Context

The fixer (casimir_2c46) addressed all 7A and 5B findings from iteration 1. The claimed fixes are:
- A1: Mirrored-significance closure test (replaces negative-d0 test)
- A2: chi2/ndf shape comparison (replaces counting comparison)
- A3: Track weight investigation documented
- A4: [D17] vertex investigation with 3 approaches
- A5–A7: Figure label and layout fixes
- A8: d0 sign validation uses tight double-tag enrichment
- A9: R_b bias quantitative back-of-envelope documented
- B1–B10: Various documentation and criterion fixes

This review focuses on whether the closure tests are now genuinely meaningful, whether the R_b bias explanation is convincing, whether all strategy commitments are addressed, and whether new issues were introduced.

---

## PASS 1 — Methodology/Validation Audit

### 1.1 Closure Test (a): Mirrored-Significance

**Claimed result (SELECTION.md §8):** f_s(mirrored)=0.000, R_b(mirrored)=0.000.

**JSON verification (closure_results.json):**
```
negative_d0.f_s = 0.0
negative_d0.f_d = 0.0
negative_d0.R_b_extracted = 0.0
negative_d0.passes = true
```

Values match the artifact exactly. The design is: "All positive significances flipped to negative, removing ALL lifetime information. Hemisphere tags recomputed from mirrored significances."

**Assessment of meaningfulness:**

The mirrored-significance test works by construction: the hemisphere probability tag is computed from the positive-significance tail only. After mirroring, every track has negative significance, so N_t = 0 and N_tt = 0 algebraically. The result R_b = 0 is guaranteed by definition — it does not require running any code; it follows from `if no_positive_significance_tracks then P_hem=0 then no_tagged_hemisphere`. This is confirmed by the full-sample f_s = 0.4202 versus mirrored f_s = 0.000: the entire difference arises from the tag definition, not from any physics validation of the sign convention or tagger response.

**Is this a genuine closure test?** Partially. It confirms that the tag is entirely driven by positive-significance tracks (correct behavior — a sanity check). However, it does NOT test:
- Whether the calibrated sigma_d0 is correct (the test would pass even if sigma_d0 were wrong by a factor of 10)
- Whether the sign re-computation is correctly implemented (a bug in the PCA re-signing that flipped the sign back would still give f_s = 0 after mirroring)
- Whether the tag discriminates b from c/uds (a random significance assignment would also give f_s = 0 after mirroring)

The `conventions/extraction.md` independent closure test requirement says: "Apply the full extraction procedure to a statistically independent MC sample... Extract the quantity and compare to MC truth. The pull must be < 2 sigma." The mirrored-significance test does not satisfy this — it is a sanity check that the tag formula is correctly coded, not an independent validation that the method is unbiased.

**Category:** The pass criterion (f_s ratio < 0.5) is trivially satisfied by construction. This is flagged as a **Category B** concern: the test now passes a non-tautological sanity check (unlike the iter 1 version), but the `conventions/extraction.md` independent closure test requirement is not met because there is no independent MC sample and no comparison to MC truth. The artifact should explicitly acknowledge that this test is a code sanity check, not a closure test in the conventions/extraction.md sense.

**Finding B-1 (closure test a): The mirrored-significance test is a guaranteed-pass sanity check, not a statistical closure test. The result f_s=0 and R_b=0 follow algebraically from the tag definition when all significances are negative — no computation is needed. The conventions/extraction.md independent closure test requirement (pull < 2σ vs MC truth) is not satisfied at Phase 3. The artifact should explicitly state this is a code sanity check, not an independent closure test.**

### 1.2 Closure Test (b): bFlag Shape Chi2

**Claimed result (SELECTION.md §8):** chi2/ndf = 11447.

**JSON verification (closure_results.json):**
```
bflag_consistency.chi2 = 80126.9356
bflag_consistency.ndf = 7
bflag_consistency.chi2_ndf = 11446.705
```

Values match: 80127/7 = 11447. Confirmed.

**Assessment of meaningfulness:**

The chi2/ndf = 11447 confirms that bFlag=4 and bFlag=-1 have dramatically different discriminant distributions. This is genuinely informative: bFlag does distinguish some physics.

However, there are three problems:

**Problem 1 — Sample size asymmetry invalidates chi2 interpretation.** The bFlag=-1 sample has only 5,519 events (0.19%). A chi2 test comparing a histogram from 2,881,742 events to one from 5,519 events is statistically ill-posed. The effective degrees of freedom for the small sample are ~70 tracks per histogram bin (5519/7 ≈ 788 events per bin, but the significant tail bins may have far fewer). The chi2 value is dominated by the enormous statistical power of the 2.88M sample, not by the statistical characteristics of the small bFlag=-1 sample. The chi2/ndf = 11447 could mean: (a) the shapes are dramatically different, or (b) the 5,519-event histogram has Poisson fluctuations that create large chi2 values. Without seeing the actual histograms or their bin counts, we cannot distinguish these scenarios. The artifact does not report per-bin counts or examine whether the chi2 is driven by a few bins with tiny bFlag=-1 populations.

**Problem 2 — The committed test from STRATEGY.md §9.6 is ambiguous.** STRATEGY.md states: "if bFlag=4 b-tag discriminant distribution is indistinguishable from the full sample (chi2/ndf ~ 1.0)... classify bFlag as a non-b flag." The chi2/ndf = 11447 is far from 1.0, so the decision tree says bFlag IS a usable b-enrichment proxy. But the fixer correctly notes that the bFlag=-1 sample (0.19%) is too small for BDT training. These two conclusions contradict each other: bFlag has discriminating power (chi2/ndf >> 2) but bFlag=4 is not usable as a b-enrichment label (99.8% coverage). Both are true simultaneously, and the artifact correctly flags this, but the committed decision tree from STRATEGY.md is not cleanly resolved.

**Problem 3 — NDF = 7 suggests only 8 histogram bins.** With 5,519 events in 8 bins, the average bin count is ~690. Some tail bins of the discriminant distribution will have far fewer. If any bins have fewer than ~25 events, the Poisson chi2 approximation breaks down. The artifact does not document the bin contents of the bFlag=-1 histogram.

**Finding B-2 (closure test b): The bFlag chi2/ndf test has a 2.88M-vs-5519 sample size asymmetry that invalidates the chi2 comparison. With 5,519 events spread across 8 bins, the test is dominated by the statistical power of the large sample. The per-bin bFlag=-1 counts must be reported to confirm the chi2 approximation is valid. Category B.**

### 1.3 Closure Test (c): Contamination Injection

**Claimed result (SELECTION.md §8):** baseline R_b = 0.827, contaminated R_b = 0.783, ratio = 2.14.

**JSON verification (closure_results.json):**
```
contamination_injection.baseline_R_b = 0.827431
contamination_injection.contaminated_R_b = 0.783293
contamination_injection.predicted_shift = -0.020577
contamination_injection.observed_shift = -0.044138
contamination_injection.ratio = 2.1450
```

Values confirmed. The artifact now calls this "PASS (open finding)" and frames the 2.14x ratio as an open investigation for Phase 4.

**Assessment:** The framing is improved from iteration 1 (which self-invented a "0.1 to 10" criterion). The current treatment is honest: same-direction shift is confirmed, and the 2.14x discrepancy is documented as an open finding. This is acceptable for Phase 3 given that the background efficiencies are uncalibrated. The Phase 4 plan to re-evaluate after calibration is reasonable.

**No new finding here** — the treatment is appropriate for Phase 3.

### 1.4 R_b Bias Quantitative Analysis

**Claimed analysis (SELECTION.md §7.1):** Back-of-envelope shows eps_c ~ 0.30 needed (vs nominal 0.05) at WP=5.

**Verification:** At WP=5.0, closure_results.json shows full_sample_f_s = 0.4202 and full_sample_R_b = 0.827. From rb_scan.json, the f_s at WP=5 is 0.4202 (confirmed). The SELECTION.md calculation:
- f_s_pred = 0.216 * eps_b + 0.0116
- eps_b = (0.420 - 0.012) / 0.216 = 1.89 — exceeds 1.0

From double_tag_counts.json at threshold=5.0: eps_b (extracted proxy) would be derivable from the R_b formula. The analysis is self-consistent and correctly diagnosed. The eps_b=1.89 result does demonstrate the calibration problem (a physical eps_b cannot exceed 1.0).

**However, there is a missing step.** The analysis shows eps_b > 1 when plugging in SM R_b=0.216. But what does the code actually extract? From rb_scan.json at WP=5.0: R_b = 0.827, eps_b not shown in rb_scan.json (it's in double_tag_counts.json). The artifact's back-of-envelope is correct in direction but the conclusion ("eps_c ~ 0.30 needed") does not explain why eps_b would need to exceed 1.0 to reconcile the formulas — it correctly identifies the problem (background efficiencies far too small) but the quantitative statement that eps_c ~ 0.30 is needed at WP=5 is presented as the fix needed in Phase 4. This is plausible, but the calculation assumes eps_b ~ 0.5 as a "reasonable" value — this is an assumption not derived from data. At WP=5, the data eps_b could be very different.

**Finding C-1 (R_b bias analysis): The back-of-envelope assumption of eps_b ~ 0.5 at WP=5 is not derived from data or MC. The calculated eps_c ~ 0.30 depends on this assumption. A more rigorous estimate would bound eps_b from the f_d/f_s ratio (f_d/f_s ~ eps_b at high purity). At WP=5: f_d/f_s = 0.207/0.420 = 0.493, giving eps_b ~ 0.49, which is close to the assumed 0.5. The artifact should derive eps_b from this data-side bound rather than assuming it. Category C (documentation quality).**

### 1.5 d0 Sign Validation MC Ratio Claim

**SELECTION.MD §3:** "Positive/negative tail ratio at 3-sigma: 1.76 (data), **1.86 (MC)**"

**JSON verification (d0_sign_validation.json):**
The JSON has `tail_ratio_3sigma.ratio_pos_over_neg = 1.7613` for data. There is no MC ratio in this file. The JSON keys are: `n_pos_b`, `n_neg_b`, `n_pos_all`, `n_neg_all`, `asymmetry_b`, `asymmetry_all` for various thresholds. None of these are specifically MC.

**The 1.86 MC ratio is claimed in the artifact but absent from the JSON.** The d0_sign_validation.json appears to be computed entirely from data (2,887,261 events — matching the data cutflow). The JSON lacks a separate MC computation. Either (a) the MC computation was done but not written to this JSON file, or (b) the 1.86 figure is stated from memory or from a different analysis step not saved here.

**Finding A-1 (MC tail ratio not in JSON): SELECTION.MD §3 claims "1.86 (MC)" for the positive/negative tail ratio at 3-sigma, but d0_sign_validation.json contains no MC entry. The JSON contains data tail ratios only. The 1.86 figure is unverifiable from the saved artifacts. Either the MC computation must be added to d0_sign_validation.json, or the claim must be removed. Category A.**

### 1.6 Precision Comparison

The statistical uncertainty on R_b at WP=5 is sigma_rb = 0.00107 (from rb_scan.json). The ALEPH published total uncertainty is 0.0014. Our stat-only at WP=5 is 0.00107 / 0.0014 = 0.76x (smaller stat, consistent given larger dataset). No precision comparison issue.

### 1.7 Data Completeness

SELECTION.MD §2: Total events 3,050,610 (data) and 771,597 (MC). cutflow.json confirms these. All data are processed.

**However:** The MC is only 1994 data (771,597 events). This is documented as [L1] in the strategy and is a known constraint. The artifact correctly notes this in Section 11 (Primary Vertex investigation). No new concern.

### 1.8 Cutflow Monotonic Check

cutflow.json: data: total=3,050,610 → passesAll=2,889,543 → cos_theta_cut=2,887,261. Monotonically non-increasing. Track: total=85,198,110 → good_tracks=46,731,904. Monotonic. **Pass.**

### 1.9 JSON/Artifact Numerical Consistency Spot-Checks

| Claim in SELECTION.md | Source | JSON value | Match? |
|----------------------|--------|-----------|--------|
| f_s=0.000 (mirrored) | §8(a) | closure_results.json | 0.0 | Yes |
| R_b=0.000 (mirrored) | §8(a) | closure_results.json | 0.0 | Yes |
| chi2/ndf=11447 | §8(b) | closure_results.json | 11446.7 | Yes |
| ratio=2.14 (contamination) | §8(c) | closure_results.json | 2.1450 | Yes |
| tail ratio 1.76 (data) | §3 | d0_sign_validation.json | 1.7613 | Yes |
| tail ratio 1.86 (MC) | §3 | d0_sign_validation.json | **ABSENT** | **NO** |
| mean Q_FB=-0.00391, kappa=0.3 | §6 | jet_charge.json | -0.003906 | Yes |
| sigma(Q_h)=0.206, kappa=0.3 | §6 | jet_charge.json | 0.2060 | Yes |
| weight range [0.028, 9.0] | §10 | track_weight_investigation.json | [0.028, 9.0] | Yes |
| vertex spread ~71 micron | §11 | d17_vertex_investigation.json | 70.9 micron | Yes |
| N_t=4,223,810 at WP=2.0 | §5 | double_tag_counts.json | 4,223,810 | Yes |
| N_tt=1,598,458 at WP=2.0 | §5 | double_tag_counts.json | 1,598,458 | Yes |
| scale factors 1.3-7.6 | §4 | sigma_d0_params.json | 2.76-7.6+ | Partial |
| WP scan R_b=0.98-0.48 | §7 | rb_scan.json | 0.980-0.481 | Yes |

**One discrepancy (MC tail ratio, finding A-1). One partial match (scale factor range — see below).**

### 1.10 sigma_d0 Scale Factor Range Check

SELECTION.MD §4 states "Scale factors range from 1.3 to 7.6 across 40 calibration bins." From sigma_d0_params.json: the first three bins shown (nv1_p0_ct0=3.55, nv1_p0_ct1=3.14, nv1_p0_ct2=2.76). The minimum scale factor of 1.3 is claimed for "2+ VDET hits" bins. The file was read with limit=50 lines. The remaining bins with nvdet=2 would show the smaller scale factors. No contradiction identified, but not fully verified due to file length. Plausible given physics (2-VDET tracks have better resolution).

---

## PASS 2 — Standard Critical Review

### 2.1 CP1 Cross-Phase Concern: Closure Test Tautology (REVIEW_CONCERNS.md)

**Status:** The mirrored-significance test (A1 fix) is a genuine improvement over the old negative-d0 test. The result f_s=0, R_b=0 is now driven by a design that removes all lifetime information rather than by a tautological formula. The concern about tautology is **substantially resolved**.

**Remaining gap:** As documented in Finding B-1 above, the test is a guaranteed-pass sanity check (f_s=0 follows from the tag formula algebraically when all significances are negative). The conventions/extraction.md independent closure test requirement is not fully met. This is known and appropriate for Phase 3 given the absence of MC truth labels — the artifact should state this explicitly. The fixer's SELECTION.md does document "mirrored sample has zero b-tagging power, as expected" which is correct framing, but does not acknowledge the algebraic guarantee.

**CP1 status: Substantially resolved. Residual concern documented as Finding B-1.**

### 2.2 CP2 Cross-Phase Concern: A_FB^b Extraction Formula

**Status:** The A_FB^b self-calibrating fit [D12b] was committed in strategy iteration 2. Phase 3 does not implement the A_FB^b extraction — it only computes Q_FB inputs. The formula concern therefore does not apply to Phase 3.

**CP2 status: Not applicable to Phase 3. Will be checked at Phase 4.**

### 2.3 CP3 Cross-Phase Concern: sigma_d0 Angular Dependence

**Status:** SELECTION.md §4 uses sigma_d0 = sqrt(A^2 + (B / (p * sin(theta)))^2) with sin(theta) form. sigma_d0_params.json: `"angular_form": "sin(theta) [Rphi projection]"`. This matches the strategy commitment after the fix (hugo_c460 changed from sin^{3/2} to sin(theta)).

**CP3 status: Resolved.**

### 2.4 CP4 Cross-Phase Concern: PDG Inputs Not Fetched

**Status:** Phase 3 does not use B hadron lifetimes or decay multiplicities — these enter the systematic program in Phase 4. Phase 3 only uses R_c = 0.17223 (cited to hep-ex/0509008) and C_b = 1.01 (cited to hep-ex/9609005). Both citations are present.

**CP4 status: Deferred to Phase 4, as appropriate.**

### 2.5 Decision Label Traceability: All [D] Labels

| Decision | Committed | Implemented? | Evidence |
|----------|-----------|-------------|---------|
| [D1] Observable definitions | LEP EWWG standard | Used in §7 | R_c=0.17223 from hep-ex/0509008 |
| [D2] Double-tag counting | Yes | Yes | §7 formula |
| [D3] Simplified two-tag | Yes | Yes | §5 |
| [D4] Hemisphere jet charge | Yes | Yes | §6 |
| [D5] kappa={0.3,0.5,1.0,2.0,∞} | Yes | Yes | §6 and jet_charge.json |
| [D6] R_c constrained | Yes | Yes | R_c=0.17223 in §7 |
| [D7] sigma_d0 from negative tail | Yes | Yes | §4, sigma_d0_params.json |
| [D8] Combined probability-mass tag | Yes | Yes | §5 |
| [D9] BDT with bFlag labels | Yes | **Deferred** | §12 downscope |
| [D10] BDT vs cut-based comparison | Yes | **Deferred** | §12 downscope |
| [D11] Non-VDET tracks in jet charge | Yes | Yes | §6 |
| [D12] Self-calibrating fit | Phase 4 | Deferred | Correct |
| [D12b] Four-quantity fit | Phase 4 | Deferred | Correct |
| [D13] Toy-based uncertainty propagation | Phase 4 | Deferred | Correct |
| [D14] Multi-working-point extraction | Phase 4 | Plan stated | §7.1 |
| [D17] Primary vertex investigation | Yes (Phase 3) | Yes | §11 |
| [D18] Combined probability-mass | Yes | Yes | §5 |
| [D19] d0 sign gate | Yes (Phase 3) | PASS | §3 |

**Issues with [D9]/[D10] deferral:**

The strategy commits to attempting BDT training with bFlag proxy labels [D9] and a quantitative comparison [D10]. The fixer defers both to Phase 4 with justification: bFlag=4 covers 99.8% of events and is unsuitable as a b-enrichment label. The chi2/ndf = 11447 test shows bFlag DOES discriminate, but the sample size of bFlag=-1 (5,519 events) is too small for BDT training.

**Evaluation:** The downscoping methodology requires (per `methodology/12-downscoping.md`) documenting the constraint and comparison. The artifact has Section 12 (BDT Deferral — Formal Downscoping) which states the bFlag=4 infeasibility and the 5,519-event limitation. However, there is a logical gap: bFlag provides discriminating power (chi2/ndf=11447) but the artifact claims self-labelling from the cut-based tag as the Phase 4 alternative. This is self-referential: using the cut-based tag to label data for BDT training essentially trains a BDT to reproduce the cut-based tag, which cannot outperform it. This may be why BDT should be abandoned entirely rather than deferred, but the artifact doesn't make this argument explicitly.

**Finding B-3 (BDT self-labelling circularity): The Phase 4 plan to use self-labelling from the cut-based tag for BDT training creates a circularity: the BDT learns to reproduce the cut-based discriminant and cannot outperform it. The strategy committed to a quantitative AUC comparison [D10]. Either the BDT deferral should commit to a genuinely independent training approach (e.g., using a different variable subset, or training on phase-space-restricted samples), or [D9]/[D10] should be formally cancelled with justification that no independent training labels exist. Category B.**

### 2.6 Convention Coverage: conventions/extraction.md

Required validation checks vs. SELECTION.md:

| Requirement | Status | Evidence |
|-------------|--------|---------|
| Independent closure test (pull < 2σ vs MC truth) | NOT met | No MC truth; mirrored test is sanity check only |
| Parameter sensitivity table | Deferred to Phase 4 | §14 item 8 |
| Operating point stability scan | Done | §7, rb_scan.json (but no plateau) |
| Per-subperiod consistency | Partially done | Year labels preserved, no per-year R_b yet |
| Data-derived calibration (scale factors) | Done | sigma_d0 negative-tail calibration |

The operating point stability scan is present but shows no plateau — R_b varies monotonically from 0.98 to 0.48 across the threshold scan. `conventions/extraction.md` §validation check 3 states: "The result must be flat within uncertainties — a dramatic variation indicates the measurement is not robust." The artifact explicitly documents this and provides a quantitative explanation (uncalibrated background efficiencies), with Phase 4 plan to calibrate. This is acceptable at Phase 3 given the documented constraint.

**Per-subperiod consistency check** is committed in COMMITMENTS.md ("Per-year extraction, chi2/ndf across years") but Section 13 only notes "Year labels in preselected NPZ." The actual per-year R_b consistency test has not been performed — COMMITMENTS.md marks this as `[ ]` (not resolved).

**Finding B-4 (per-year R_b consistency not done): COMMITMENTS.md §Validation tests: "Per-year consistency: R_b and A_FB^b per year, chi2/ndf across years" is marked `[ ]` (not addressed). The per-year information is preserved in the NPZ files, but the extraction has not been performed. This is a conventions/extraction.md requirement (§4: per-subperiod consistency). At minimum, a per-year cutflow or per-year f_s/f_d should be reported to check for time-dependent effects. Category B.**

### 2.7 Non-Standard Technique Check

**The d0 sign re-computation using PCA-jet angle method is non-standard.** The stored d0 branch has ALEPH helix convention sign; the re-signing uses `signed_d0 = |d0| * sign(PCA_direction dot jet_direction)` with `PCA_direction = (d0*sin(phi), -d0*cos(phi))`.

The strategy §5.1 describes the correct sign: "Positive = track crosses the jet axis downstream of the vertex." The PCA-jet method is a standard approach in lifetime tagging (used in, e.g., ATLAS and CMS b-tagging). However, the specific formula for PCA_direction uses the ALEPH helix convention `(d0*sin(phi), -d0*cos(phi))`, which is documented in the experiment log as requiring "flipped PCA convention compared to the standard textbook formula."

This non-standard convention flip is documented. The validation (tail ratio 1.76) provides evidence that the result is correct. **No new finding — documentation is adequate.**

### 2.8 Quantitative Check: R_b Bias Analysis

SELECTION.MD §7.1 back-of-envelope at WP=5:
- Observed f_s = 0.420 (confirmed: rb_scan.json shows 0.4202)
- Nominal prediction: f_s = eps_b * R_b + eps_c * R_c + eps_uds * (1-R_b-R_c)
- With R_b=0.216, R_c=0.172, eps_c=0.05, eps_uds=0.005:
  f_s_pred = eps_b * 0.216 + 0.05 * 0.172 + 0.005 * 0.612 = eps_b * 0.216 + 0.0116
- Solving: eps_b = (0.420 - 0.012) / 0.216 = 1.89

**Check: Is the formula correct?** From STRATEGY.md §4.1, the single-tag formula is:
```
f_s = eps_b * R_b + eps_c * R_c + eps_uds * (1 - R_b - R_c)
```
The computation in §7.1 uses f_s = 0.420 but the actual f_s at WP=5 is 0.4202 (rb_scan.json). The nominators:
- eps_c * R_c = 0.05 * 0.172 = 0.0086
- eps_uds * (1 - R_b - R_c) = 0.005 * (1 - 0.216 - 0.172) = 0.005 * 0.612 = 0.00306

Total background = 0.0117. eps_b = (0.420 - 0.0117) / 0.216 = 0.4083 / 0.216 = **1.89**. Confirmed.

The artifact rounds 0.0086 + 0.00306 ≈ 0.012 and gets 0.0116, giving eps_b = 1.89. Small rounding difference, result is correct.

**The R_b bias analysis is quantitatively correct and convincingly explains the bias source.** This finding is resolved from iteration 1.

### 2.9 Tag Efficiency Proxy Values

SELECTION.MD §5 reports "f_s | f_d" at various working points. Cross-check at WP=4.0:
- SELECTION.md table: f_s=0.509, f_d=0.290 (columns "N_t=2,940,992, N_tt=836,660")
- rb_scan.json at threshold=4.0: f_s=0.5093, f_d=0.28978, combined
- double_tag_counts.json at threshold=4.0: N_single_tag=2,104,332, N_double_tag=836,660

Wait — there is a discrepancy: SELECTION.md §5 table reports N_t = 2,940,992 at threshold=4.0, but double_tag_counts.json shows N_single_tag=2,104,332. The f_s values match (0.509 and 0.5093), but how?

**Investigation:**
- f_s = N_t / (2 * N_had) = N_t / (2 * 2,887,261) = N_t / 5,774,522
- From SELECTION.md: N_t = 2,940,992 → f_s = 2,940,992 / 5,774,522 = 0.509. Checks out.
- From double_tag_counts.json: N_single_tag = 2,104,332 → f_s = 2,104,332 / 5,774,522 = 0.364. But rb_scan.json shows f_s = 0.5093 at threshold=4.0.

There is a 2,940,992 vs 2,104,332 discrepancy between SELECTION.md table and double_tag_counts.json at WP=4.0. These cannot both correspond to the same quantity with the same f_s.

**Resolution check:** The double_tag_counts.json n_single_tag counts *hemispheres* that are singly tagged (one-hemisphere events). But N_t as used in the f_s formula counts *tagged hemispheres total* (both hemispheres, so 2x for events where both pass). Let me verify:

If N_t = 2 * N_had * f_s = 2 * 2,887,261 * 0.5093 = 2,940,992 — this matches SELECTION.md. But double_tag_counts.json shows "n_single_tag = 2,104,332." This might mean events with exactly one tagged hemisphere (not 2). If double_tag_counts.json uses events with exactly-one-tag (singly tagged events), while N_t in the formula means total tagged hemispheres (= 2 * double_tagged + singly_tagged), then:

N_t (formula) = n_singly_tagged_events + 2 * n_doubly_tagged_events = 2,104,332 + 2*836,660 = 3,777,652. That doesn't match 2,940,992 either.

Alternatively, if n_single_tag in the JSON counts events where AT LEAST one hemisphere passes the cut:
- N_events_tagged = N_t_formula (events with at least one tag)
- But SELECTION.md uses N_t = total tagged hemispheres = 2 * N_had * f_s

**Finding A-2 (N_t/N_tt inconsistency): SELECTION.md §5 table reports N_t=2,940,992 at WP=4.0, but double_tag_counts.json reports n_single_tag=2,104,332 at threshold=4.0. If both represent the same quantity (single-tag counts), they disagree by 40%. The f_s values derived from each (0.509 vs 0.364) differ substantially. The JSON field "n_single_tag" must be clarified: does it count tagged hemispheres or singly-tagged events? Either the JSON or the artifact table uses an inconsistent definition. Category A.**

*Detailed check of WP=4.0 numbers:*
From double_tag_counts.json: n_single_tag=2,104,332, n_double_tag=836,660, f_s=0.5093, N_had=2,887,261.
- If f_s = n_single_tag / (2*N_had): 2,104,332 / 5,774,522 = 0.364 ≠ 0.5093
- If f_s = (n_single_tag + 2*n_double_tag) / (2*N_had): (2,104,332 + 1,673,320) / 5,774,522 = 3,777,652/5,774,522 = 0.654 ≠ 0.5093

Neither definition reconciles. There may be a third definition used. The f_s=0.5093 is confirmed by rb_scan.json, so the issue is what "n_single_tag" means in double_tag_counts.json versus "N_t" in the SELECTION.md table.

**This inconsistency propagates:** SELECTION.md §5 table is the primary documentation of working point properties. If the N_t numbers in that table are not directly derivable from the data artifacts, any downstream Phase 4 calculation that uses those specific counts will need careful reconciliation.

### 2.10 Operating Point Stability — no plateau

The artifact correctly documents "No stability plateau" and explains it through the back-of-envelope in §7.1. The R_b scan shows monotonic decrease from 0.98 to 0.48. The `conventions/extraction.md` requirement that the result be "flat within uncertainties" is clearly NOT met, but the documented explanation (uncalibrated eps_c, eps_uds) is physically reasonable.

**The Phase 4 plan relies on multi-working-point simultaneous fit [D14].** This is well-motivated. However, there is a subtlety: the Phase 3 artifact presents working-point stability as a validation criterion that "will be evaluated after calibration" — but if calibration itself is derived from the working-point scan (by fitting eps_c, eps_uds across working points), the calibration and the stability validation are coupled. The artifact should acknowledge this coupling explicitly.

**Finding C-2 (WP stability and calibration coupling): The Phase 4 multi-working-point fit [D14] simultaneously constrains R_b, eps_b, eps_c, eps_uds from the working-point scan. The operating-point stability check (after calibration) will use the same data that calibrated the background efficiencies. The stability check is therefore partially self-validating. The artifact should acknowledge this and specify what an independent cross-check would look like (e.g., comparing extracted R_b from different kappa values or different sign-cut thresholds). Category C.**

### 2.11 Data/MC Normalization Method

SELECTION.MD §9: "MC is normalized to data integral in all plots." This non-default normalization is stated but not justified. `conventions/extraction.md` does not prohibit it, but the CLAUDE.md notes "L x sigma is the default; data-integral normalization requires explicit justification."

The artifact provides no justification for why MC is normalized to data integral rather than using luminosity × cross-section × efficiency. The only available MC is 1994 (771,597 events), and there is no published luminosity for this specific MC sample. Normalizing to data integral avoids the need for luminosity, which is appropriate given the MC-only coverage limitation, but this should be stated.

**Finding C-3 (MC normalization justification missing): SELECTION.md states MC is normalized to data integral but does not justify this choice. The correct justification (no published luminosity for the 1994 MC sample, consistent with [L1]) should be added. Category C.**

### 2.12 Hemisphere Correlation C_b

SELECTION.md §7 states C_b = 1.01 with source hep-ex/9609005 Table 1, inflated 2x per [D17]. The STRATEGY.md [D17] inflation factor (2x) is correctly applied. C_b = 1.01 in the extraction with eps_c=0.05, eps_uds=0.005 results in R_b > 1 at loose working points — this is the documented bias, not an error.

No new finding.

### 2.13 sigma_d0 Calibration: Post-Calibration Gaussian Width

SELECTION.MD §13 reports "Post-calibration Gaussian validation: calibrated negative-tail MAD*1.48 = 1.10 (data) and 1.10 (MC)." The target is unit width. The reported value is 1.10, meaning the calibration achieves ~10% residual width above unity, not the ideal of exactly 1.0.

The artifact notes this as validation "close to unit width after calibration (by construction within each bin)." The "by construction" qualifier is important: the scale factor is derived from the negative tail and then applied to the same tail, so the result should be exactly 1.0 by construction if the bin statistics are good. A MAD*1.48 = 1.10 suggests that either (a) the calibration bins have limited statistics causing some residual width, or (b) the calibration itself has a systematic offset.

However, examining the per-event median spread from d17_vertex_investigation.json: `calibrated_neg_width_data = 12.83` and `calibrated_neg_width_mc = 12.66`. These are not the same quantity as MAD*1.48 reported in the artifact. The d17 investigation measures the "calibrated_neg_width" in some other unit. The MAD*1.48=1.10 reported in §13 should match what the verification would find if done bin-by-bin, but the d17 JSON shows 12.83 — these appear to measure different things and are not cross-referenced.

**Finding B-5 (post-calibration width verification ambiguous): SELECTION.md §13 reports calibrated negative-tail MAD*1.48 = 1.10. d17_vertex_investigation.json reports calibrated_neg_width_data = 12.83. These should be the same quantity (calibrated d0/sigma_d0 negative tail width) but differ by 11.7x. Either they measure different things (one is overall, one is per-bin) or there is an inconsistency. Clarify what calibrated_neg_width = 12.83 means and reconcile with the 1.10 figure. Category B.**

### 2.14 New Issues Introduced by Fixes

**A8 fix: d0 sign validation uses tight double-tag enrichment (combined tag > 8 in both hemispheres, 8% of events).**

The new b-enriched definition in FIGURES.json: "b-enriched sample uses tight double-tag (combined tag > 8 in both hemispheres)." However, d0_sign_validation.json key `n_b_enriched_events = 2,881,742` — this is 99.81% of events, not 8%. This matches bFlag=4 enrichment, not tight double-tag.

**Finding A-3 (d0 sign validation enrichment mismatch): The FIGURES.json description for d0_sign_validation_magnus_1207 states "b-enriched sample uses tight double-tag (combined tag > 8 in both hemispheres)" but d0_sign_validation.json reports n_b_enriched_events = 2,881,742, which is 2,881,742/2,887,261 = 99.81% of events. A tight double-tag requirement (combined tag > 8) should retain ~8% of events (from §5 table: at threshold 8.0, fraction=0.242 single-tag, much less double-tag). The JSON definition of "b-enriched" in d0_sign_validation.json is actually bFlag=4, not tight double-tag. The FIGURES.json metadata is incorrect. This means the d0 sign validation figure labeled as using "tight double-tag" is actually using bFlag=4 as b-enrichment — which is the tautological comparison that iter-1 finding A-8 was supposed to fix. Category A.**

This is a critical finding: the iter-1 fix A8 (replace bFlag=4 enrichment with tight double-tag) claimed to address the tautological b-enrichment definition, but the JSON shows n_b_enriched_events = 2,881,742 = 99.81% of events = bFlag=4 definition. Either:
1. The JSON was not updated when the figure was recomputed, or
2. The figure description was updated but the actual computation still uses bFlag=4.

The tail ratio 1.76 reported in the JSON and the SELECTION.md matches bFlag=4 enrichment (99.81%). If tight double-tag (8% of events) were used, the tail ratio would be much higher (closer to 2.5-3.0 for a high-purity b sample). A ratio of 1.76 at 3-sigma is consistent with the full sample being slightly b-enriched due to the bFlag=4 definition, not with a tight b-tag requiring double-tagging.

**This means finding A-8 from iteration 1 (replace bFlag=4 with tight double-tag) was NOT actually implemented in the computation — only the figure description was changed. The numerical result (1.76) is from a bFlag=4-enriched sample.**

### 2.15 Tag Working Point Table: f_s Values

SELECTION.MD §5 table at threshold=2.0: "f_s 0.732, f_d 0.554, N_t 4,223,810, N_tt 1,598,458."

rb_scan.json at threshold=2.0: f_s=0.7314562, f_d=0.5536243. Rounded to 3 places: 0.731 and 0.554. The artifact rounds to 0.732 (third decimal rounded up from 0.7314 → 0.731, not 0.732). Minor rounding, acceptable.

double_tag_counts.json at threshold=2.0: N_single_tag=2,625,352, N_double_tag=1,598,458.

The N_tt=1,598,458 matches. The N_t=4,223,810 does not match n_single_tag=2,625,352. This reinforces finding A-2: "N_t" in the SELECTION.md table is NOT "n_single_tag" from double_tag_counts.json.

From f_s: N_t = f_s * 2 * N_had = 0.7314562 * 2 * 2,887,261 = 4,222,945 ≈ 4,223,810. (Small discrepancy due to rounding of f_s.) So N_t = total tagged hemispheres. But double_tag_counts.json n_single_tag = 2,625,352. These are clearly different quantities. The artifact uses N_t = total tagged hemispheres (correct formula definition), while the JSON appears to store something else as "n_single_tag." This needs clarification for Phase 4 reproducibility.

---

## Summary of Findings

### Category A (Must Resolve)

**A-1: MC tail ratio 1.86 absent from JSON.** SELECTION.md §3 claims "1.86 (MC)" for the positive/negative d0/sigma_d0 tail ratio at 3-sigma. d0_sign_validation.json contains no MC entry. The claim is unverifiable. Resolution: add MC computation to the JSON, or remove the claim.

**A-2: N_t/N_tt definition inconsistency.** SELECTION.md §5 working point table reports N_t values derived from total tagged hemispheres (f_s × 2 × N_had), but double_tag_counts.json uses "n_single_tag" for a different quantity (possibly events with exactly one tagged hemisphere). At WP=4.0: table says N_t=2,940,992 but JSON shows n_single_tag=2,104,332. The formula and table use N_t correctly, but the JSON uses an inconsistent label. This must be clarified before Phase 4 code that reads the JSON will use the wrong value in the double-tag formula. Resolution: add explicit documentation in the JSON of what each count represents, or rename JSON fields to match the formula definition.

**A-3: d0 sign validation b-enrichment mismatch.** The FIGURES.json and SELECTION.md describe the b-enriched sample as "tight double-tag (combined tag > 8)" but d0_sign_validation.json has n_b_enriched_events = 2,881,742 = 99.81% of events — identical to the bFlag=4 enrichment that iter-1 finding A-8 was supposed to replace. The tail ratio of 1.76 is consistent with bFlag=4 enrichment, not tight double-tag. Either the computation was not updated and the figure description is false, or the JSON was not updated when the code changed. The d0 sign validation figure is the only artifact supporting the [D19] gate — if the gate was validated with bFlag=4 enrichment (the tautological comparison), the gate result is not meaningful. Resolution: rerun d0_sign_validation.py with the tight double-tag definition and update the JSON. The tail ratio should be significantly higher than 1.76 for a tight b-tag, or document why 1.76 was expected.

### Category B (Should Address)

**B-1: Mirrored-significance closure test is a guaranteed-pass sanity check.** f_s=0 follows algebraically from the tag formula when all significances are negative — no computation needed. The result does not validate the calibration, the sign convention implementation, or the tagger's discriminating power against c/uds. The artifact should explicitly label this as a code sanity check, not an independent closure test per conventions/extraction.md.

**B-2: bFlag chi2 test has 2.88M vs 5519 sample size asymmetry.** With only 8 bins and 5,519 events in the small sample, per-bin counts could be as low as ~50, making the chi2 approximation unreliable in the tails. Per-bin counts for the bFlag=-1 histogram must be reported.

**B-3: BDT self-labelling circularity.** The Phase 4 plan to use the cut-based tag for BDT training labels creates a circularity: the BDT cannot outperform the label source. Either commit to a genuinely independent training approach or formally cancel [D9]/[D10].

**B-4: Per-year R_b consistency not done.** COMMITMENTS.md §Validation tests marks per-year extraction as `[ ]`. Year labels are preserved in NPZ, but no per-year f_s, f_d, or R_b has been computed. This is a conventions/extraction.md requirement.

**B-5: Post-calibration width reconciliation.** MAD*1.48=1.10 in §13 vs calibrated_neg_width=12.83 in d17_vertex_investigation.json — these should be the same quantity but differ by 11.7x. Clarify what each measures and reconcile.

### Category C (Suggestions)

**C-1: eps_b assumption in back-of-envelope.** The assumption eps_b ~ 0.5 in §7.1 should be derived from f_d/f_s ~ 0.49 rather than assumed.

**C-2: WP stability and calibration coupling.** The post-calibration stability check will use the same working-point scan data that calibrated eps_c/eps_uds. This partial self-validation should be acknowledged and an independent cross-check specified.

**C-3: MC normalization justification missing.** Add one sentence: MC is normalized to data integral because no published luminosity exists for the 1994 MC sample [L1].

---

## Verdict

**ITERATE** — 3 Category A, 5 Category B findings require resolution before the Phase 3 artifact can advance.

The most critical finding is **A-3**: the d0 sign validation [D19] gate was supposed to be re-validated with a tight double-tag b-enrichment (the iter-1 fix A-8), but the JSON evidence shows the computation still uses bFlag=4 enrichment (99.81% of events). If the [D19] gate was validated with bFlag=4 — a nearly-inclusive sample — then the gate provides no meaningful confirmation that the physics-signed d0 preferentially tags b quarks versus the general hadronic sample. This is a process failure, not just documentation: the gate's numerical result (1.76) is from an effectively-inclusive sample and may be consistent with simple resolution asymmetry rather than b-quark lifetime enrichment.

**A-1** (MC tail ratio absent from JSON) and **A-2** (N_t definition inconsistency) are documentation-level but must be resolved before Phase 4 code can safely use the JSON outputs.

The closure test fixes are a genuine improvement over iteration 1: the mirrored-significance test is a legitimate sanity check (not tautological in the algebraic sense), and the contamination injection is honestly documented as an open finding. However, the independent closure test requirement from conventions/extraction.md is not satisfied — this gap should be explicitly acknowledged in the artifact rather than left implicit.

---

*Reviewer: erik_352e | 2026-04-02 | Phase 3 Selection, Iteration 2*
