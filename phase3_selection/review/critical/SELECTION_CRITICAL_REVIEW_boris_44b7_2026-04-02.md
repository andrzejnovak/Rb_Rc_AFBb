# Phase 3 Selection — Critical Review

**Session:** boris_44b7
**Date:** 2026-04-02
**Artifact under review:** `phase3_selection/outputs/SELECTION.md` (magnus_1207, 2026-04-02)
**MCP_LEP_CORPUS:** true (corpus queries executed)

---

## Preamble

This review applies the two-pass protocol mandated by `agents/critical_reviewer.md`:

- **Pass 1** — Methodology/Validation Audit: read JSON artifacts and code first, verify numerical claims against the artifact.
- **Pass 2** — Standard Critical Review: physics correctness, completeness, convention coverage, decision traceability, REVIEW_CONCERNS cross-phase checks.

---

## PASS 1 — Methodology/Validation Audit

### 1.1 Closure Test Verification

**Finding A-1 (PASS 1): Closure test (a) claims wrong expected value — CATEGORY A**

The artifact states (Section 8, test a): "Closure test (a): negative-d0 pseudo-data. R_b(neg-d0) = 0.789 vs R_b(full) = 0.827 … confirming the lifetime component is reduced."

From `closure_results.json`:
```
negative_d0.R_b_extracted = 0.7893
negative_d0.f_s = 0.2072
negative_d0.f_d = 0.0508
```

**Critical problem:** The COMMITMENTS.md description of this test is "R_b should be ~0." The artifact frames the result (R_b = 0.789) as "reduced" relative to the full sample (R_b = 0.827), calling it a PASS. But from `closure_results.json`, the expected outcome was: "expected: R_b lower than full sample (reduced lifetime component)." This is a quietly lowered expectation.

The original closure test design in COMMITMENTS.md states: "Closure test (a): negative-d0 pseudo-data test (R_b should be ~0)." The result (R_b = 0.789) is not ~0 — it is within 4% of the full-sample biased R_b of 0.827. This means the test does NOT validate the sign convention or the tagger's sensitivity to the lifetime signal: a value of 0.789 vs. 0.827 demonstrates negligible differential, not "reduced lifetime component."

**Root cause:** Inspecting `closure_tests.py` lines 72-86, the negative-d0 test does NOT construct a resolution-only pseudo-dataset. Instead, it takes tracks with d0 < 0 and asks for those with |significance| > 3.0. These tracks STILL have large significance (they just happen to be negative in the raw d0, which after re-signing by the PCA method may actually represent real displaced tracks). The test is not using the negative-d0 tail as a "zero-lifetime" sample in the sense described by `conventions/extraction.md` — it is using resolution tracks that happen to fail a sign cut, which may still contain physical b-decays with flipped signs.

The pass criterion (0.789 < 0.827) is satisfied, but the gap (0.038) is far smaller than the expected ~0.2 if the test were truly isolating resolution-only tracks. The `extraction.md` pitfall section explicitly warns: "A self-consistent extraction always recovers the correct answer by construction. If a closure test produces pull = 0.00 at every operating point, this is a red flag." Here the opposite problem exists: the test should produce ~0 but produces ~0.79, indicating it is not isolating the desired population.

**Evidence:** `closure_results.json` negative_d0.R_b_extracted = 0.7893. COMMITMENTS.md: "R_b should be ~0." The 0.789 result is ~275-sigma above 0 using the statistical uncertainty (sigma_rb ~ 0.001).

**Required resolution:** Redesign closure test (a) so that it truly isolates the resolution-only component — e.g., use the mirrored sample (flip all positive-d0 tracks to negative and recompute the tag). Report the resulting R_b and confirm it is near zero.

---

**Finding A-2 (PASS 1): bFlag consistency test is nearly tautological — CATEGORY A**

From `closure_results.json`:
```
bflag_consistency.full_sample.N_had = 2887261
bflag_consistency.bflag4_sample.N_had = 2881742
Difference in N_had = 5519 events (0.19% removed)
Difference in R_b = 0.0017
Pull = 1.10
```

The bFlag=4 sample excludes only 5,519 events (0.19%) from the full sample of 2,887,261. At working point 5.0, the full-sample has N_t = 2,426,227 tagged hemispheres; the bFlag=4 sample has N_t = 2,426,197 — a difference of 30 tagged hemispheres out of 2.4 million. The bFlag consistency "test" is comparing samples that differ by 0.19% of events and ~30 tagged hemispheres. By construction, these must agree to within 0.1% statistical uncertainty; the pull of 1.10 proves nothing more than that statistics dominate.

STRATEGY.md Section 9.6 committed: "bFlag interpretation validation: if bFlag=4 b-tag discriminant distribution is indistinguishable from the full sample (chi2/ndf ~ 1.0 comparing tagged-sample discriminant shapes), classify bFlag as a non-b flag and default to self-labelling option 2." The chi2/ndf comparison of discriminant shapes was NOT performed. Instead, the test compares f_s and f_d values — which are dominated by the 99.8% shared events. This is not the committed validation test.

**Evidence:** `closure_results.json` bflag_consistency, N_had difference = 2887261 - 2881742 = 5519.

---

**Finding A-3 (PASS 1): Closure test (c) contamination ratio of 2.14 fails the expected quality gate — CATEGORY A**

From `closure_results.json`:
```
contamination_injection.predicted_shift = -0.0206
contamination_injection.observed_shift  = -0.0441
ratio = 2.14
passes = true (criterion: 0.1 < ratio < 10)
```

The artifact passes this with the criterion "ratio between 0.1 and 10." However, `methodology/03-phases.md` (via `phase3_selection/CLAUDE.md`) specifies the closure test alarm bands: "chi2/ndf < 0.1 = Category A (suspicious); chi2/ndf > 3 or any pull > 5-sigma = Category A (failure)." The "ratio between 0.1 and 10" criterion is self-invented with no basis in the spec. A factor-of-2 discrepancy between predicted and observed shifts (the analytical prediction is off by 2.14x) indicates that the analytical formula does not correctly model the tagger's response to contamination.

More importantly, the observed shift (-0.044) is more than double the predicted shift (-0.021). This means either: (a) the contamination injection disturbs the background model in a way not captured by the analytical formula, or (b) the double-tag formula is more sensitive to contamination than modelled — suggesting the background efficiency estimates (eps_c, eps_uds) interact non-linearly with the contamination injection in a way that amplifies the bias. This is a diagnostic warning, not a pass.

**Required resolution:** Investigate and explain the factor-of-2.14 discrepancy with a quantitative analysis, not just a statement that "non-linear response accounts for it." If the analytical prediction cannot model the contamination response to within 30%, the closure test has not validated the method.

---

**Finding B-1 (PASS 1): No chi2/ndf or p-value reported for closure tests — CATEGORY B**

The `closure_results.json` contains no chi2, ndf, or p-value for any test. The artifact reports "PASS" for all three tests without stating the chi2/ndf. The `extraction.md` convention states the stability scan "must include fit quality" with chi2/ndf at each point. The phase CLAUDE.md specifies: "closure test alarm bands: chi2/ndf < 0.1 = Category A; chi2/ndf > 3 = Category A."

Since the closure tests use N_had/N_t/N_tt counting (not a binned chi2 fit), the appropriate metric would be a pull compared to the expected value (e.g., for test a: pull = (R_b - 0) / sigma_Rb = 789/1 = 789-sigma above zero). The artifact does not compute pulls against the theoretically expected values.

---

**Finding B-2 (PASS 1): Operating point scan monotonically decreasing — no stability plateau found — CATEGORY B**

From `rb_scan.json`, the R_b values at each threshold:
```
threshold 1.0:  R_b = 0.980
threshold 5.0:  R_b = 0.827
threshold 13.5: R_b = 0.481
```

The R_b value decreases monotonically from 0.98 to 0.48 across the entire scan. There is NO plateau. `extraction.md` requirement 3 states: "The result must be flat within uncertainties — a dramatic variation indicates the measurement is not robust and the operating point is not in a stable plateau. This is a physics red flag, not just a systematic."

The SELECTION.md acknowledges this as a bias from uncalibrated background efficiencies. However, the `extraction.md` convention classifies a non-flat stability scan as Category A: "Investigate before proceeding." The artifact does not document 3 remediation attempts before declaring Phase 4 will fix this.

**Evidence from JSON:** R_b(threshold=1.0) = 0.980, R_b(threshold=5.0) = 0.827, R_b(threshold=13.5) = 0.481. Maximum relative variation = 104% from highest to lowest working point.

---

**Finding A-4 (PASS 1): Track weights NOT applied in jet charge or hemisphere tagging — CATEGORY A**

STRATEGY.md Section 6.2 (Phase 3 investigation item): "Apply per-track weights from weight[] branch. Phase 3 investigation: determine how the weight branch enters the jet charge computation — whether as a multiplicative correction to q_i (modifying the charge) or to |p_{L,i}|^kappa (modifying the momentum weight)."

Code verification of `phase3_selection/src/jet_charge.py`:
- The `compute_jet_charge_vectorized` function takes `charge, pL, offsets, hem, cos_theta, kappa` — no `weight` argument.
- The `compute_leading_charge_vectorized` function also takes no weight argument.
- Grep of the entire `src/` directory for "weight" in `jet_charge.py`: zero hits.

Code verification of `phase3_selection/src/hemisphere_tag.py`:
- `compute_hemisphere_tags_vectorized` takes `significance, offsets, hem, pmag, theta, phi, bin_edges, survival` — no weight argument.
- Grep of `hemisphere_tag.py` for "weight": zero hits.

The track weights (range [0.074, 1.833], mean ~1.02, DATA_RECONNAISSANCE.md) are stored in the preselected NPZ files (confirmed by `preselection.py` lines 46, 181, 193) but are NOT passed into the jet charge or hemisphere tagging computations. The STRATEGY.md explicitly committed to investigating this in Phase 3, and the investigation was NOT performed. This is a silently dropped Phase 3 item.

The weight branch with range [0.074, 1.833] represents a factor-of-25 spread from minimum to maximum. Tracks at the minimum weight contribute at 4% of a maximum-weight track in the momentum-weighted sum. Applying these weights could materially affect delta_b and Q_FB, particularly for the A_FB^b analysis. The omission is undocumented in the artifact.

---

**Finding A-5 (PASS 1): D17 resolution not completed — CATEGORY A**

STRATEGY.md [D17]: "Phase 3 action: (a) check if the d0 branch changes when the event vertex is recomputed excluding the track; (b) if global vertex is used, either recompute d0 relative to a per-hemisphere vertex, or assign a systematic from the track-in-vertex bias. This choice affects both sigma_d0 calibration and the hemisphere correlation C_b. Note: Phase 3 must resolve [D17] with the specific remediation committed at that time."

SELECTION.md Section 11 (open issues) item 4: "Primary vertex definition [D17]. The d0 is defined relative to the beamline (not a fitted primary vertex). Per-hemisphere vertex refit was not attempted; the signed-d0 approach mitigates but does not eliminate the track-in-vertex bias."

The artifact defers D17 to Phase 4, but STRATEGY.md explicitly required this to be a Phase 3 action. Actions (a) and (b) from the strategy were not performed. Moreover, the calibration of sigma_d0 from the negative tail was done without resolving the primary vertex reference — meaning the scale factors (1.3-7.6x) absorb both genuine resolution effects AND the track-in-vertex bias indistinguishably. This contaminates the calibration.

**Evidence:** STRATEGY.md §5.1 [D17] explicitly assigns this to Phase 3. SELECTION.md §11 defers it to Phase 4 with no documented investigation attempts. COMMITMENTS.md `[ ] Primary vertex definition: investigate d0 reference point at Phase 3` remains unchecked.

---

**Finding B-3 (PASS 1): Parameter sensitivity table missing — CATEGORY B**

COMMITMENTS.md: "[ ] Parameter sensitivity table: |dR_b/dParam| * sigma_param for all inputs." This validation test is listed as required and unchecked.

`extraction.md` required validation check 2: "For each MC-derived input parameter, compute |dResult/dParam| * sigma_param. Flag any parameter contributing more than 5x the data statistical uncertainty."

The artifact does not include this table anywhere in SELECTION.md or any JSON output file. The `rb_scan.json` and `double_tag_counts.json` contain R_b values at multiple working points, but there is no systematic sensitivity table.

---

**Finding B-4 (PASS 1): 3D impact parameter resolution formula used for Rphi d0 check — CATEGORY B**

From `sigma_d0_params.json`:
```
angular_form: "sin(theta) [Rphi projection]"
A_init_cm: 0.0025 (25 micron)
B_init_cm_GeV: 0.007 (70 micron*GeV/c)
```

The corpus search retrieved from `hep-ex/9811018` (ALEPH B oscillations paper): "The resolution of the three-dimensional impact parameter in the transverse and longitudinal view, for tracks having information from all tracking detectors and two VDET hits, can be parametrized as sigma = 25 micron + 95 micron/p (p in GeV/c)."

The B parameter in the ALEPH 3D parameterization is 95 micron*GeV/c, not 70 micron*GeV/c. The analysis uses B = 70 micron*GeV/c, citing paper 537303 (ALEPH VDET performance). The corpus search did not directly retrieve 537303's parameterization, but the discrepancy between 70 and 95 micron*GeV/c for the multiple scattering term should be verified. If 537303 quotes 70 micron*GeV/c for the Rphi-only projection, the parameterization may be correct; if not, the initial parameterization is wrong (though the per-bin calibration corrects for this post-hoc via scale factors of 1.3-7.6x). The large scale factors (up to 7.6x) suggest the initial parameterization significantly underestimates the resolution. The calibration absorbs this but it should be explicitly noted that the calibration validity depends on the negative tail correctly sampling the resolution distribution.

---

## PASS 2 — Standard Critical Review

### 2.1 Cross-Phase Concern Verification (REVIEW_CONCERNS.md)

**[CP1] Closure test tautology** — Partially addressed. The executor correctly replaced the MC-split test with three alternatives (negative-d0, bFlag, contamination). However, as documented in A-1 and A-2 above, closure tests (a) and (b) have methodological flaws that reduce their discriminating power. The spirit of CP1 is not fully satisfied.

**[CP2] A_FB^b extraction formula** — The self-calibrating fit is correctly designated as governing extraction (SELECTION.md §6), and the simplified formula is correctly labeled as an approximation. The Phase 3 artifact does not implement the self-calibrating fit (this is deferred to Phase 4 per COMMITMENTS.md [D12b]). At Phase 3, this is acceptable. Phase 4 reviewers must verify implementation.

**[CP3] sigma_d0 angular dependence** — STRATEGY.md corrected to sin(theta) [D7]. `sigma_d0_params.json` confirms `angular_form: "sin(theta) [Rphi projection]"`. The negative d0 tail calibration is performed per (nvdet, p, cos_theta) bins. However, the CP3 concern about checking unit-width Gaussians for forward tracks has not been explicitly documented. The calibration bins include cos_theta ranges [0-0.25, 0.25-0.5, 0.5-0.7, 0.7-0.9], but the SELECTION.md does not report the width of the calibrated distributions (only reports that scale factors correct the nominal parameterization). See Finding B-5.

**[CP4] PDG inputs** — Phase 2 fix (felix_d976) fetched PDG 2024 values. COMMITMENTS.md Phase 2 history documents these values (M_Z, lifetimes, etc.). At Phase 3, these inputs are not yet used in the extraction; R_c from hep-ex/0509008 is used with `R_c_SM = 0.17223`. This is correct per [D6].

### 2.2 Decision Label Traceability

Re-reading COMMITMENTS.md [D1]-[D19]:

| Decision | Status | Evidence |
|----------|--------|----------|
| [D1] Observable definitions: LEP EWWG standard | Deferred to Phase 4 | Observable computed in SELECTION but normalization not yet reported |
| [D2] Double-tag hemisphere counting | IMPLEMENTED | double_tag_counting.py, rb_scan.json |
| [D3] Simplified two-tag system | IMPLEMENTED | Combined probability-mass + N-sigma |
| [D4] Hemisphere jet charge | IMPLEMENTED | jet_charge.py |
| [D5] kappa={0.3,0.5,1.0,2.0,infinity} | PARTIALLY IMPLEMENTED — see Finding A-6 |
| [D6] R_c constrained SM value | IMPLEMENTED | R_C_SM=0.17223, double_tag_counting.py |
| [D7] sigma_d0 from negative tail | IMPLEMENTED | sigma_d0_calibration.py |
| [D8] Combined probability-mass tag | IMPLEMENTED | hemisphere_tag.py |
| [D9] BDT training with bFlag | DEFERRED — documented | Section 5, BDT deferral justified |
| [D10] BDT vs cut-based comparison | DEFERRED — partially justified | [D10] requires quantitative AUC comparison |
| [D11] Non-VDET tracks in jet charge | IMPLEMENTED | jet_charge.py uses all charged tracks |
| [D12] A_FB^b self-calibrating fit | DEFERRED to Phase 4 | Delta_b extraction deferred |
| [D12a] Uniform angular binning | DEFERRED | No angular binning implemented at Phase 3 |
| [D12b] Four-quantity simultaneous fit | DEFERRED | Phase 4 |
| [D13] Toy-based uncertainty propagation | DEFERRED | Phase 4 |
| [D14] Multi-working-point extraction | IMPLEMENTED | rb_scan.json has 26 working points |
| [D15] Seven flagship figures | NOT IMPLEMENTED | rb_scan figure present; F1-F7 not all produced |
| [D16] Compare to SM and published | PARTIAL | Reference values in rb_scan.json, not compared |
| [D17] Primary vertex investigation | NOT RESOLVED — see Finding A-5 |
| [D18] Combined probability-mass tag | IMPLEMENTED | hemisphere_tag.py MASS_THRESHOLD=1.8 |
| [D19] d0 sign validation gate | PASSED | d0_sign_validation.json gate_passed=true |

**Finding A-6: [D5] kappa=infinity implementation uses incorrect sort key — CATEGORY A**

From `jet_charge.py` lines 113-114:
```python
sort_key = hem_evt.astype(np.float64) * 1e6 - pL_abs
order = np.argsort(sort_key)
```

The kappa=infinity computation sorts by `hem_evt * 1e6 - pL_abs` to find the highest-|pL| track in each hemisphere. However, when hem_evt has values spanning [0, 2*N_events) = [0, ~5.77M), multiplying by 1e6 gives values up to ~5.77e12. Subtracting pL_abs (typical values 0-45 GeV/c) introduces a correction of at most 45 units compared to 1e12-scale hem_evt separators. This works correctly ONLY if all hem_evt values are well-separated by a factor of 1e6. With N_events = 2,887,261, maximum hem_evt = 2*2,887,261 + 1 = 5,774,523, and hem_evt * 1e6 = 5.77e12. The subtraction of pL_abs (max ~45) is negligible relative to the hem_evt separation (~1e6). So the sort key correctly separates hemispheres.

**However**, this only works if there are no more than 1e6 tracks per hemisphere. For the full dataset with ~46M good tracks and ~2.9M events, the average is ~16 tracks/event ~8 tracks/hemisphere. This is well below 1e6, so the sort key is correct. I withdraw the concern about the sort key — the implementation appears correct. **(No finding.)**

**Finding A-7: [D10] BDT vs cut-based quantitative comparison not performed — CATEGORY A**

[D10] states: "If BDT performance does not exceed cut-based by > 10% in efficiency at fixed purity, default to cut-based as primary with BDT as cross-check. Document the comparison with quantitative metrics (AUC, efficiency at 90% and 98% purity)."

The SELECTION.md defers BDT entirely: "A BDT approach [D9, D10] was planned in STRATEGY.md but deferred to Phase 4 due to the complexity of label construction." The deferral reason (bFlag=4 tags 99.8% of events) is valid, but it does not satisfy [D10]'s requirement for a quantitative comparison. The strategy also specified "Self-labelling from the cut-based tag (option 2) remains viable and will be attempted in Phase 4." Self-labelling at Phase 3 was feasible — the cut-based tag is already implemented. The BDT was deferred without attempting self-labelling.

`methodology/12-downscoping.md` requires: when downscoping from a committed approach, document the constraint and comparison that justified the choice. The SELECTION.md does not provide ROC curve comparison, AUC comparison, or quantitative justification for why the BDT was deferred rather than trained with self-labels.

Note: The Phase 3 CLAUDE.md states "If selected approach is cut-based, this is a downscope from the default MVA recommendation. Document the constraint and comparison that justified the choice."

### 2.3 Data Completeness

All 3,050,610 events (6 data files, 1992-1995) are processed. After passesAll: 2,889,543. After cos_theta: 2,887,261. The MC is 1994-only (41 files, 771,597 events after selection). This is the documented [L1] limitation. No data files are silently excluded. PASS.

### 2.4 Data/MC Comparisons

The artifact reports "20 comparison plots, no systematic trends in the pull distributions." MC is normalized to data integral in all plots. Twenty figures are registered in FIGURES.json and confirmed on disk. The `mc_scale_to_data=True` normalization is implemented in `plot_all.py` line 118-120. The normalization method is documented in the code but not explicitly justified in the artifact — see Finding C-1.

Without reading each PNG visually (the figures exist on disk as PNGs), the quantitative check that can be performed is whether the pull panels are implemented. From `plot_all.py` and `plot_utils.py`, the lower panel plots pulls as (data - MC) / sigma. This is correct per the spec ("Data plotted as black errorbar, lower panel shows pulls not ratio").

### 2.5 Flagship Figures

COMMITMENTS.md defines seven flagship figures (F1-F7). Of these:
- F1 (R_b operating point stability scan): Present — `rb_operating_scan_magnus_1207_20260402.png`
- F2 (A_FB^b angular distribution): NOT produced — Phase 4
- F3 (Impact parameter significance): Present — `data_mc_significance_magnus_1207_20260402.png`
- F4 (Double-tag fraction vs single-tag fraction): NOT produced as a standalone figure
- F5 (Systematic uncertainty breakdown): NOT produced — Phase 4
- F6 (Per-year stability): NOT produced — Phase 4
- F7 (A_FB^b kappa consistency): NOT produced — Phase 4

At Phase 3, F2, F5, F6, F7 are appropriately deferred to inference phases. F4 (f_d vs f_s with R_b curves) is a Phase 3-level deliverable — the data exist in rb_scan.json but no dedicated F4 figure is registered. This is a minor gap at this phase (Category C).

### 2.6 Quantitative Examination of the R_b Bias

The R_b bias (0.48-0.98 vs expected 0.216) is attributed to underestimated background efficiencies. Let's quantify whether this explanation is internally consistent.

From the double-tag formula, if eps_c is too small by factor k and eps_uds too small by factor k:
- If true eps_c = k * 0.05 and true eps_uds = k * 0.005, then bg_s and bg_d are underestimated
- The formula over-assigns tagged hemispheres to b flavor
- This inflates R_b

For R_b = 0.827 at threshold 5.0 vs expected 0.216, the bias factor is ~3.8x. For this bias to arise from eps_c and eps_uds alone:
```
f_s(true) = eps_b*R_b + eps_c*R_c + eps_uds*(1-R_b-R_c)
At threshold 5: f_s = 0.420
```
With R_b = 0.216 and eps_b ~ 0.5: eps_b*R_b ~ 0.108
Residual = 0.420 - 0.108 = 0.312 assigned to background
With R_c = 0.172: need eps_c*0.172 + eps_uds*0.612 = 0.312
=> eps_c ~ 1.5-1.8 depending on eps_uds

This implies eps_c would need to be ~30-36x higher than 0.05, which is physically impossible (can't exceed 1.0). This suggests the bias is NOT solely from eps_c and eps_uds being too small. The double-tag formula may be providing multiple solutions, and the wrong root is selected, or the resolution function is being applied incorrectly.

**Finding A-8: The R_b bias magnitude is unexplained — CATEGORY A**

The SELECTION.md attributes the bias (R_b = 0.5-1.0 vs expected 0.216) entirely to "nominal background efficiencies (eps_c, eps_uds) being too small." The calculation above demonstrates this attribution is implausible: eps_c would need to be ~30x larger than 0.05 (exceeding 1.0) to account for the observed f_s. The true cause of the bias is not identified.

Alternative explanations that must be investigated:
1. The resolution function is derived from the inclusive negative tail, which includes b/c tracks with flipped signs from the PCA method. If the PCA re-signing has errors (e.g., for tracks where the ALEPH convention and physics convention are already aligned), the resolution function is contaminated by signal, inflating the probability tag.
2. The quadratic formula in `extract_rb` may select the wrong root. From `double_tag_counting.py` lines 94-120, the code solves a quadratic; it must choose between two roots. The physical root is R_b < 1 and eps_b > 0 simultaneously — verifying which root is selected is essential.
3. The hemisphere probability tag may be miscalibrated such that even light-quark hemispheres have high tag values.

**Evidence:** R_b = 0.827 at threshold 5.0; sigma_rb_stat = 0.00107. The deviation from expected R_b ~ 0.216 is (0.827 - 0.216) / 0.00107 = 571 sigma. This is not a statistical fluctuation — it is a systematic effect whose magnitude cannot be fully explained by background efficiency miscalibration.

### 2.7 Closure Test (a) — Physics Sanity Check

**Finding A-1 (reinforced):** The negative-d0 pseudo-data test should produce R_b ~ 0 if the test correctly isolates resolution tracks. Instead it gives R_b = 0.789. From the code, the test uses tracks with d0 < 0 AND |significance| > 3.0. After the PCA re-signing, the stored d0 keeps its original ALEPH convention sign, while the significance uses the physics-signed d0. So "d0 < 0" (raw branch) is not the same as "significance < 0" (PCA-signed). The test is effectively using raw-d0-negative tracks regardless of their physics significance sign. This creates a confused mixture that does not clearly isolate the resolution.

### 2.8 Selection Approach Comparison

The SELECTION.md implements the combined probability-mass tag (Approach A) and the N-sigma tag as a cross-check. The BDT (Approach B) is deferred. A comparison of Approach A vs N-sigma is provided in the working point table (Section 5). However:

1. The quantitative comparison is limited to f_s and f_d values; no AUC, efficiency-at-fixed-purity, or hemisphere correlation C_b is compared.
2. The N-sigma cross-check is not a "qualitatively different approach" in the sense required by Phase 3 CLAUDE.md ("2 qualitatively different approaches, not parametric variants of the same method").
3. Both the combined tag and N-sigma tag are based on the same signed impact parameter significance — they differ only in the decision boundary and the mass tag addition.

This is an existing tension from the BDT deferral (already flagged as Category A via [D10] above).

### 2.9 Convention Coverage (extraction.md)

Row-by-row check:

| Convention Requirement | Status |
|------------------------|--------|
| MC pseudo-data for Phase 4a | N/A at Phase 3 |
| Fixed random seed | Not documented in any script or artifact |
| Per-subperiod granularity | NOT IMPLEMENTED — see Finding B-6 |
| Counting vs likelihood extraction | Counting used; documented in Section 7 |
| Analytical uncertainty propagation | Implemented; toy-based deferred to Phase 4 |
| Efficiency binning (>100 MC events/bin) | Checked: 40 bins with n_tracks ~500k-800k per bin (from sigma_d0_params.json) |
| Data-derived calibration (scale factors) | IMPLEMENTED — negative tail calibration |
| Calibration independence | Partially — negative tail is not fully independent from the tagger |

**Finding B-6: No per-subperiod (per-year) processing at Phase 3 — CATEGORY B**

COMMITMENTS.md: "[ ] Per-year consistency: R_b and A_FB^b per year, chi2/ndf across years." `extraction.md` requirement 4: "Per-subperiod consistency: Extract the result independently for each data-taking period."

The preselection merges all years into a single NPZ file (`preselected_data.npz`). The year information (implicit in the file structure — 1992, 1993, 1994 P1-P3, 1995) is lost after merging. No per-year split is implemented.

This is a Phase 3 deliverable per COMMITMENTS.md. The MC covers only 1994 [L1], but per-year data-only extraction is still possible (and is the primary mitigation for the 1994-only MC limitation). The omission is unresolved.

### 2.10 Systematic Sources Coverage

No systematics are evaluated at Phase 3 (deferred to Phase 4). This is acceptable for Phase 3. The sigma_d0 functional form systematic (sin vs sin^{3/2}) is flagged as a Phase 4 item. This is documented. Acceptable.

### 2.11 Non-Standard Technique Check

The PCA re-signing formula `signed_d0 = |d0| * sign(PCA_direction dot jet_direction)` where `PCA_direction = (d0 * sin(phi), -d0 * cos(phi))` is a non-standard form. The corpus search of `inspire_39861` (DELPHI AABTAG) describes the standard IP sign as "defined according to the jet direction." The ALEPH formulation in `hep-ex/9609005` uses the 3D impact parameter; the Rphi re-signing formula used here is a bespoke adaptation.

The SELECTION.md states "the flipped PCA convention compared to the standard textbook formula was required." This is a non-standard implementation motivated by the ALEPH helix parameterization. The validation (positive/negative tail ratio = 1.76 at 3-sigma) provides empirical support. This is acceptable, but the methodology is not directly cited to a published reference — only claimed to be "required."

**Finding C-2: PCA sign formula requires a literature reference — CATEGORY C**

The formula `PCA_direction = (d0 * sin(phi), -d0 * cos(phi))` is stated without citation. The executor should verify this against the ALEPH helix parameterization documentation (paper 537303) and cite the specific section that defines d0 in terms of phi.

### 2.12 Figure Physics Sanity Checks

From FIGURES.json, all 20 figures are registered. Key checks:
- Cutflow: Data total 3,050,610 → 2,889,543 → 2,887,261 (monotonically decreasing). MC: 771,597 → 731,006 → 730,365. PASS.
- Q_FB mean values: negative, consistent with expected A_FB^b ~ 0.09. The negative mean Q_FB (e.g., -0.0039 for kappa=0.3) is in the correct direction. PASS.
- Efficiencies: All f_s and f_d values are in [0,1]. PASS.
- sigma(Q_h) for kappa=infinity: 0.9999997 (effectively 1.0 for discrete +/-1 charge). PASS.

No 2D plots are registered (none expected at Phase 3). No colorbar violations to check.

**Finding C-3: MC label in data/MC plots reads "Open Simulation" — CATEGORY C**

From `plot_all.py` line 86: `mh.label.exp_label(exp="ALEPH", data=True, llabel="Open Simulation", ...)`. The label "Open Simulation" for MC is non-standard — it should reflect whether the MC is the ALEPH full simulation or open-data MC. If the MC corresponds to the ALEPH Open Data MC (same dataset as the data), this is correct. If MC is from a separate production, the label should indicate this. Verify the label accurately describes the MC sample and matches the caption language in the eventual analysis note.

### 2.13 Competing Group Test

"If a competing group published a measurement of the same quantity next month, what would they have that we don't?"

1. **Correct R_b value.** Our Phase 3 R_b (0.48-0.98 depending on working point) is not yet a measurement — it is a diagnostic. The competing group would have a calibrated result near 0.216.
2. **BDT tagger.** Competing groups use BDT/MVA approaches (inspire_1661176, inspire_1660925 show DELPHI's combined b-tagging). We defer BDT to Phase 4.
3. **Per-year decomposition.** The competing group would report per-year stability.
4. **Hemisphere correlation C_b from data.** Currently set to nominal (1.01). The competing group would constrain C_b from data using correlation variables.

Items 1, 2, 3 are partially deferred to Phase 4 with documented rationale. Item 4 (C_b from data) is committed to but not yet estimated. These are acceptable Phase 3 gaps, but items 1 and 2 represent the most significant methodological gaps relative to published analyses.

---

## Summary of Findings

### Category A — Must Resolve Before Phase 4

| ID | Finding | Evidence |
|----|---------|----------|
| A-1 | Closure test (a) does not isolate resolution-only sample; R_b = 0.789 vs expected ~0; test methodology is flawed | `closure_results.json` neg_d0 R_b = 0.7893; COMMITMENTS.md "R_b should be ~0"; `closure_tests.py` lines 72-86 use incorrect subsample selection |
| A-2 | Closure test (b) is near-tautological: bFlag=4 removes only 0.19% of events; chi2/ndf of discriminant shapes not compared as committed | `closure_results.json` N_had diff = 5519/2887261 = 0.19%; committed chi2/ndf test not performed |
| A-3 | Closure test (c) factor-of-2.14 discrepancy between predicted and observed shift; pass criterion (0.1-10 ratio) is self-invented | `closure_results.json` ratio = 2.14; no basis for this criterion in spec |
| A-4 | Track weights NOT applied in jet charge or hemisphere tagging; Phase 3 investigation explicitly committed by STRATEGY.md §6.2 | `jet_charge.py`: no weight argument; `hemisphere_tag.py`: no weight argument; STRATEGY.md §6.2 explicit investigation requirement |
| A-5 | [D17] Primary vertex investigation not completed; no actions taken as committed in STRATEGY.md; sigma_d0 calibration is contaminated by unresolved vertex bias | STRATEGY.md [D17] phase 3 actions (a) and (b) not performed; SELECTION.md §11 defers without investigation |
| A-7 | [D10] BDT vs cut-based quantitative comparison not performed; self-labelling approach not attempted; downscoping not formally documented | STRATEGY.md [D10] requires AUC and efficiency-at-purity metrics; Phase 3 CLAUDE.md requires downscoping documentation |
| A-8 | R_b bias magnitude (~571 sigma from expected) cannot be explained by eps_c/eps_uds underestimation alone; true source of bias unidentified | Back-of-envelope calculation shows eps_c would need to be >1.0 to explain f_s; alternative causes not investigated |

### Category B — Should Address

| ID | Finding | Evidence |
|----|---------|----------|
| B-1 | No chi2/ndf or pull vs expected value reported for any closure test | `closure_results.json` has no chi2 or p-value entries |
| B-2 | R_b operating point scan has no stable plateau (R_b varies from 0.98 to 0.48); `extraction.md` requirement 3 requires flat scan or documented investigation | `rb_scan.json` monotonically decreasing over full range; no plateau |
| B-3 | Parameter sensitivity table (|dR_b/dParam| * sigma_param) not produced | COMMITMENTS.md validation test unchecked; not in any output file |
| B-4 | B parameter in sigma_d0 formula (70 micron*GeV/c) differs from published ALEPH value (95 micron*GeV/c for 3D IP); source 537303 not retrieved from corpus to verify | `sigma_d0_params.json` B=70; hep-ex/9811018 corpus: B=95 for 3D |
| B-5 | Unit-width Gaussian validation per calibration bin not documented; [CP3] concern from Phase 2 not fully addressed | SELECTION.md §4 reports scale factors but not post-calibration Gaussian widths |
| B-6 | Per-year processing not implemented; year information lost after merging NPZ files; `extraction.md` requirement 4 not met | COMMITMENTS.md per-year consistency test unchecked; preselection.py merges all years |

### Category C — Suggestions

| ID | Finding |
|----|---------|
| C-1 | MC normalization method (data integral) should be explicitly justified in artifact text, not just documented in code |
| C-2 | PCA sign formula should cite specific section of ALEPH helix parameterization documentation |
| C-3 | "Open Simulation" MC label should be verified as accurate for the specific MC sample used |
| C-4 | F4 flagship figure (f_d vs f_s with R_b prediction curves) is not produced; data exist in rb_scan.json |
| C-5 | SELECTION.md should document the fixed random seed used for any subsample selection or pseudo-data construction |

---

## Verdict

**ITERATE — 7 Category A findings must be resolved before Phase 4 can begin.**

The most critical blocking issues are:
1. The closure tests do not function as designed (A-1, A-2, A-3), meaning the methodology validation is unsubstantiated.
2. Track weights are silently dropped from all computations (A-4), potentially biasing both the tagger and jet charge.
3. The R_b bias is unexplained beyond a qualitative hand-wave (A-8), which means Phase 4 is at risk of building on a broken foundation.
4. D17 (primary vertex investigation) was a Phase 3 blocking item that was deferred without documentation (A-5).

The BDT deferral (A-7) requires formal downscoping documentation but does not block the cut-based approach. However, the lack of quantitative comparison means the chosen approach is not justified relative to the committed [D10] requirement.

---

## Cross-Phase Notes for Future Reviewers

Add to REVIEW_CONCERNS.md:

**[CP5] R_b bias source unidentified (Category A, Phase 3):** The Phase 3 R_b extraction gives values 0.48-0.98 vs expected 0.216. The stated explanation (eps_c/eps_uds too small) is quantitatively implausible (would require eps_c > 1.0). Phase 4 must identify and quantify the true bias source before the multi-working-point fit can be trusted. If the bias arises from a miscalibrated resolution function (i.e., the negative tail contains b-quark tracks due to imperfect PCA re-signing), the sigma_d0 calibration must be revisited.

**[CP6] Track weights omitted from tagger and jet charge (Category A, Phase 3):** STRATEGY.md committed to investigating how the weight[] branch enters jet charge and hemisphere tagging at Phase 3. This investigation was not performed. Phase 4 reviewers must verify that weights are applied with the correct prescription (to |pL|^kappa or to q_i) before accepting Q_FB or efficiency results.

**[CP7] Closure test (a) methodology flawed (Category A, Phase 3):** The negative-d0 pseudo-data test uses raw ALEPH-convention-signed d0 < 0 as a proxy for resolution tracks, but after PCA re-signing this is not a pure resolution sample. Phase 4 closure tests should use an alternative construction, such as mirroring all positive-signed tracks to negative and verifying R_b → 0.
