# Phase 4b Arbiter Adjudication

**Arbiter:** joe_69ff
**Date:** 2026-04-02
**Artifact:** `phase4_inference/4b_partial/outputs/INFERENCE_PARTIAL.md`
**Reviews adjudicated:**
- Critical: hiroshi_ea49 (6A, 5B, 2C)
- Plot validation: yuki_519e (9A, 2B)

---

## Structured Adjudication Table

| # | Finding | Source(s) | Their Cat | Final Cat | Rationale |
|---|---------|-----------|-----------|-----------|-----------|
| 1 | parameters.json not updated with 10% results; `phase` still reads `4a_expected` | Critical F1 | A | **A** | Independently verified: `parameters.json` contains only Phase 4a values (`R_b.value = 0.310`, `phase` absent or stale). No `R_b_10pct` or `A_FB_b_10pct` entries. The artifact's validation table claiming "Results JSON updated: PASS" is false. This is the primary machine-readable deliverable of Phase 4b. |
| 2 | validation.json chi2 wrong (0.026 vs 0.296) | Critical F2 | A | **A** | Independently verified: `validation.json` reports `operating_point_stability.chi2 = 0.02558`, while `rb_results_10pct.json` reports `stability.chi2 = 0.296`. The validation.json value is stale (Phase 4a). Mixed-phase JSON without labels is an integrity failure. |
| 3 | Phase 4a R_b inconsistent across files (0.280 text vs 0.305 JSON vs 0.310 parameters.json) | Critical F3 | A | **B** | The inconsistency is real (verified three distinct values). However, Phase 4a has already passed review and been committed. The 0.280 vs 0.305 discrepancy arises from different C_b values used (1.01 vs 1.537). The parameters.json value (0.310) is from a different WP. This is a documentation/traceability issue that should be resolved, but it does not affect the Phase 4b physics result. Downgraded from A to B because: (1) Phase 4a is frozen, (2) the Phase 4b extraction uses its own independent C_b=1.01 assumption, (3) the comparison to Phase 4a is diagnostic, not a physics input. The fixer should add a clarifying note to the artifact specifying which C_b assumption yields each Phase 4a value. |
| 4 | A_FB^b = 0.0085 deviates ~10.7-sigma from ALEPH 0.0927 -- no section 6.8 investigation | Critical F4 + Plot VISUAL-9 + Plot CROSS-1 | A (both) | **A** | This is the most serious physics finding. Both reviewers independently flagged it. The artifact claims the result is "consistent within the larger statistical uncertainty of the 10% sample" -- this is factually incorrect (pull = 10.7-sigma total). The self-calibrating fit extracts A_FB^b = slope / delta_b; if delta_b is overestimated (the fit returns delta_b = 0.166-0.566 depending on kappa, vs a physically expected ~0.1-0.15 for kappa=0.3), the A_FB^b is suppressed. A section 6.8 investigation is mandatory: quantitative diagnosis of the suppression mechanism, demonstrated magnitude match, and exclusion of simpler explanations (sign error, contamination dilution, intercept absorbing signal). This investigation BLOCKS advancement to Doc 4b. |
| 5 | C_b systematic evaluated at WP=10 while nominal R_b is at WP=7 | Critical F5 | A | **A** | Independently verified from code: `rb_extraction_10pct.py` line 132 hard-codes `thr_str = "10.0"` for the C_b scan, but `best_wp.threshold = 7.0`. The systematic `C_b_systematic_range = |0.513 - 0.208| = 0.305` mixes efficiencies from two different operating points. This is the dominant R_b systematic (0.305) and it is computed incorrectly. Must recompute at WP=7. |
| 6 | charge_model systematic = combined stat uncertainty (double-counting) | Critical F6 | A | **A** | Independently verified from code: `systematics_10pct.py` line 139 sets `charge_model.delta_AFB = afb["combination"]["sigma_A_FB_b"]` which is the statistical uncertainty (0.00346). The charge_model systematic should be the spread of A_FB^b across kappa values (~0.0029 from std dev of [0.004, 0.006, 0.009, 0.012]). As coded, stat is counted twice in quadrature. |
| 7 | Self-calibrating fit p < 0.01 at kappa = 0.5, 1.0, 2.0 -- undisclosed | Critical F7 | B | **B** | The artifact reports only simple fit chi2 values. The self-calibrating fit (the governing extraction per D12) has p < 0.01 at 3/4 kappa values. This must be disclosed with a formal Finding + Resolution. The simple fit being acceptable at kappa=0.3 provides a fallback, but the reader must know the governing fit has GoF problems at higher kappa. |
| 8 | Per-subperiod consistency not performed (required completion criterion) | Critical F8 | B | **B** | The Phase 4b CLAUDE.md completion criteria explicitly list "Per-subperiod consistency check". Section 10 says "Not yet performed -- deferred to Phase 4c." This is a required check per conventions/extraction.md section 4. Either perform it (even if low-statistics -- report the chi2) or formally downscope with a COMMITMENTS.md [D] entry documenting minimum-statistics requirements per year. |
| 9 | comparison_4a_vs_4b.json has null for R_b | Critical F9 | B | **C** | This JSON is an internal convenience file, not a primary deliverable. The R_b values exist in rb_results_10pct.json. Populating it is a cleanup task that does not affect physics. Downgraded to C. |
| 10 | C_b = 1.01 choice not formally documented as [D] decision | Critical F10 | B | **B** | The choice to use C_b = 1.01 (published ALEPH, per-hemisphere vertex) instead of the measured ~1.52 (shared event vertex) is a major methodological decision. It is discussed in the artifact but not captured as a formal [D] entry in COMMITMENTS.md. This is required for traceability. The critical reviewer's point about the argument being partially circular (C_b = 1.01 chosen because it gives plausible R_b) is valid and should be acknowledged in the [D] justification. |
| 11 | WP=8,9 null extractions -- non-monotonic, not investigated | Critical F11 | B | **C** | On 10% data with limited statistics, null extractions at intermediate WPs are plausible: the quadratic extraction equation has no real solution when the tag fractions are too close to the C_b boundary. The non-monotonic pattern (7 works, 8/9 fail, 10 works) could reflect different sensitivity regions of the extraction formula. This is worth noting but not blocking -- 2 valid WPs is acceptable per the spec. Downgraded to C with requirement to add a brief note in the artifact. |
| 12 | FIGURES.json missing 4 required fields for all 8 entries | Plot REGISTRY-1 | A (BLOCKING) | **A** | Plot validator RED FLAG -- cannot downgrade. The registry was populated manually, missing `lower_panel`, `is_2d`, `created`, `script_mtime`. Fix by patching `save_and_register` or populating manually. |
| 13 | F3b pull panel nearly empty (3/80 bins visible) | Plot VISUAL-3 | A | **A** | Plot validator RED FLAG. The pull panel provides no diagnostic information. Must exclude zero-count bins or restrict the pull range to populated bins. |
| 14 | F3b pull ylabel = "Pull" not "(Data - MC)/sigma" | Plot VISUAL-4 | A | **B** | The label "Pull" is technically correct shorthand. The spec requires formula notation at Phase 4+. This is a labeling fix, not a physics error. Downgraded to B -- still must fix but lower priority than physics items. |
| 15 | F4b theory curves use incorrect formula (fd = Rb * fs^2 * 1.5) | Plot VISUAL-6 | A | **A** | The theory overlay uses an undocumented scaling factor 1.5. The curves are visually far from the data points, making the figure misleading. Must replace with the correct double-tag formula or label prominently as "Approximate (illustrative only)". |
| 16 | F5b eps_uds dominates >80% of total systematic -- no investigation | Plot VISUAL-7 | A | **B** | The eps_uds dominance (0.499/0.590 = 85%) is a real concern and triggers the regression checklist item "any single systematic > 80% of total uncertainty." However, eps_uds at 50% variation is an intentionally conservative estimate on 10% data. The artifact acknowledges this is large but defers reduction to Phase 4c multi-WP fit. The investigation of reducibility should be documented (even briefly: "ALEPH constrained eps_uds using uds control regions; our single-tag method cannot do this; multi-WP fit [D14] is the planned mitigation"). Downgraded to B because the 10% phase is not expected to resolve this -- but documentation is required. |
| 17 | F7b A_FB^b 24-sigma from ALEPH reference | Plot VISUAL-9 | A | **A** | Subsumed by Finding #4. Same physics issue. |
| 18 | S2b missing experiment label | Plot VISUAL-13 | A (auto) | **A** | Plot validator RED FLAG (automatic Category A per spec). Missing experiment label on a data/MC comparison figure. |
| 19 | S2b missing legend | Plot VISUAL-14 | A (auto) | **A** | Plot validator RED FLAG (automatic Category A per spec). No legend means a reader cannot distinguish data from MC. |
| 20 | R_b ~ SM but A_FB^b ~10x suppressed -- undiagnosed cross-figure inconsistency | Plot CROSS-1 | A | **A** | Subsumed by Finding #4. The internal inconsistency (R_b consistent with SM while A_FB^b is 10x suppressed) strengthens the case that the A_FB^b extraction has a specific methodological problem. |
| 21 | S1b missing pull panel for data_mc type | Plot VISUAL-11 | B | **C** | S1b is a supplementary figure showing tag fraction agreement. The visual agreement is excellent. A pull panel would be informative but is not blocking. Downgraded to C. |
| 22 | S2b MC series has no label in histplot | Plot LINT-2 | B | **A** | Subsumed by Finding #19. The missing legend IS the missing label. Already Category A via RED FLAG. |
| 23 | F4b theory curve coefficient 1.5 uncited | Plot LINT-3 | B | **A** | Subsumed by Finding #15. The uncited coefficient is the root cause of the incorrect theory curves. |
| 24 | F2b negative Q_FB bias across cos(theta) bins | Plot VISUAL-2 | Observation | **C** | A systematic offset in Q_FB is expected if the detector has a charge asymmetry or if the jet charge calibration has a non-zero intercept (which the artifact documents: intercept ~ -0.004). This should be noted in the artifact text but is not a physics error. |
| 25 | sigma column mislabeled in Section 7 table | Critical F12 | C | **C** | Agreed. Rename to sigma(slope) and add sigma(A_FB^b) column. |
| 26 | sin2(theta_eff) pull from SM not quantified | Critical F13 | C | **C** | Agreed. The 26-sigma stat-only pull should be reported with an explicit caveat that no systematic propagation is included. |

---

## Findings Raised by Arbiter (Missed by Reviewers)

### ARB-1: Motivated reasoning in R_b narrative (Category B)

The artifact frames R_b = 0.208 +/- 0.066 as a dramatic improvement over Phase 4a. The critical reviewer noted the C_b = 1.01 choice is an external assumption, not a self-calibration. I want to strengthen this: the fact that C_b = 1.01 gives R_b ~ 0.21 (near SM) while C_b = 1.10 gives R_b ~ 0.51 (unphysical) means the R_b "measurement" on 10% data is not a measurement at all -- it is almost entirely determined by the C_b assumption. The total uncertainty is 0.592, which is 2.7x the central value. A result of 0.208 +/- 0.592 is consistent with anything from -0.38 to +0.80. The narrative that "real data provides independent constraints breaking the circularity" is misleading when the dominant source of improvement is the choice to input C_b = 1.01 rather than measure it. The artifact should state clearly: "R_b on 10% data is dominated by the C_b assumption. The 10% validation demonstrates that the extraction infrastructure works and that tag fractions agree with MC, but the R_b central value and precision are not competitive."

### ARB-2: delta_b values in self-calibrating fit are suspiciously large (Category B)

The self-calibrating fit returns delta_b = 0.166 (kappa=0.3) to 0.566 (kappa=2.0). For comparison, the ALEPH published analysis (REF3) extracted delta_b values that, combined with A_FB^b = 0.0927, imply A_FB = slope / delta_b gives the correct A_FB. If our delta_b is overestimated, A_FB^b is directly suppressed. The investigation for Finding #4 should specifically examine: (a) what delta_b values ALEPH obtained, (b) whether our fitted delta_b is consistent with expectations for each kappa, and (c) whether the contamination from non-b hemispheres in the tagged sample inflates delta_b.

---

## Regression Check

Per methodology/06-review.md section 6.7 and the orchestrator regression checklist:

| Trigger | Status | Evidence |
|---------|--------|----------|
| Validation test failure without 3 remediation attempts | **YES** | A_FB^b deviates >3-sigma from ALEPH with no investigation (section 6.8). Self-calibrating fit p < 0.01 at 3/4 kappa values with no remediation. |
| Single systematic > 80% of total uncertainty | **YES** | eps_uds = 0.499/0.590 = 85% of R_b total systematic. Documented but investigation of reducibility missing. |
| GoF toy inconsistency | No | Toy distributions not checked at Phase 4b (appropriate -- this is a 10% validation). |
| > 50% bin exclusion | No | No bin exclusion applied. |
| Tautological comparison presented as validation | **BORDERLINE** | The R_b "improvement" narrative partially conflates choosing C_b = 1.01 with data providing independent constraints. Not fully tautological but the narrative overstates what the data contributed. |
| Precision > 5x reference without explanation | **YES** | R_b total 0.592 / ALEPH 0.0014 = 423x. Partially explained (C_b + eps_uds dominance), but the explanation is not concrete enough: ALEPH achieved C_b = 1.01 via per-hemisphere vertex (feasibility of vertex-like corrections not explored); eps_uds was constrained by data control regions (not attempted). |
| Result > 30% relative deviation from reference | **YES** | A_FB^b = 0.0085 vs ALEPH 0.0927 = 91% relative deviation. Investigation mandatory per section 6.8. |

**Regression triggers met: YES (multiple).** However, these do NOT require regression to Phase 3 -- they are Phase 4b-local issues (code bugs, missing investigation, documentation gaps). The infrastructure works; the problems are in systematic evaluation, the A_FB^b extraction chain, and reporting.

---

## Verdict: **ITERATE**

Phase 4b cannot pass with 10 unresolved Category A findings and 6 Category B findings. The physics core (tag fractions, d0 calibration, hemisphere correlations) is sound. The extraction infrastructure works. But the results layer has code bugs (C_b systematic at wrong WP, charge_model double-counting), a major unexplained deviation (A_FB^b 10x suppressed), and several figure/reporting deficiencies.

---

## Fix List (Priority Order)

### Category A -- Must resolve before Doc 4b

**A1. [Finding #4, #17, #20] A_FB^b section 6.8 investigation (BLOCKING)**
Write an investigation artifact diagnosing the A_FB^b = 0.0085 vs ALEPH 0.0927 suppression. Required content:
- Quantify the pull: 10.7-sigma total
- Examine fitted delta_b values vs expectation from ALEPH (REF3). If delta_b is too large, A_FB^b is mechanically suppressed
- Check contamination dilution: what fraction of tagged hemispheres are non-b? What is the effective dilution of the asymmetry signal?
- Check whether the fit intercept absorbs real asymmetry signal
- Check for sign errors in the cos(theta) assignment
- Demonstrate whether the suppression magnitude can be explained quantitatively
- If no explanation is found after 3 attempts: document as open issue with clear impact statement for Phase 4c

**A2. [Finding #6] Fix charge_model systematic double-counting**
In `systematics_10pct.py` line 139, replace `afb["combination"]["sigma_A_FB_b"]` with the standard deviation of A_FB^b across kappa values. Recompute total A_FB^b systematic.

**A3. [Finding #5] Fix C_b systematic to use best WP**
In `rb_extraction_10pct.py`, change C_b scan from WP=10 (`thr_str = "10.0"`) to the best working point (WP=7, `thr_str = "7.0"`). Recompute C_b systematic.

**A4. [Finding #1] Update parameters.json with 10% results**
Add `R_b_10pct`, `A_FB_b_10pct`, `sin2theta_eff_10pct` entries. Update `phase` and `data_type` fields. Ensure the write persists to disk (verify with read-back).

**A5. [Finding #2] Fix validation.json**
Separate Phase 4a and Phase 4b sections. Update Phase 4b stability chi2 to 0.296 (from rb_results_10pct.json). Label Phase 4a entries clearly.

**A6. [Finding #12] Fix FIGURES.json registry**
Populate missing fields (`lower_panel`, `is_2d`, `created`, `script_mtime`) for all 8 entries.

**A7. [Finding #13] Fix F3b pull panel**
Exclude zero-count bins from pull panel. Only show pulls where both data and MC have nonzero counts.

**A8. [Finding #15] Fix F4b theory curves**
Replace `fd_theory = Rb * fs^2 * 1.5` with the correct double-tag formula, or label curves "Approximate (illustrative only)" with visible annotation.

**A9. [Finding #18, #19] Fix S2b: add experiment label + legend**
Add `exp_label_data(ax)` call and `label=` arguments + `ax.legend()` to `plot_hemisphere_charge_comparison`.

### Category B -- Must fix before PASS

**B1. [Finding #7] Disclose self-calibrating fit chi2 failures**
Add a Finding + Resolution to the artifact documenting p < 0.01 at kappa >= 0.5 for the self-calibrating fit. State whether simple fit or self-calibrating fit governs the result and whether the chi2 failures bias A_FB^b.

**B2. [Finding #8] Per-subperiod consistency**
Either perform the per-year check on 10% data (even with large uncertainties) or add a formal [D] entry to COMMITMENTS.md with documented justification for deferral.

**B3. [Finding #10] Document C_b = 1.01 as [D] decision**
Add a [D] entry to COMMITMENTS.md capturing: the choice, the justification (published ALEPH value from per-hemisphere vertex reconstruction, not achievable with 2D impact parameters), the assigned systematic range (1.01--1.10), and acknowledgment that this is an external input, not a self-calibration.

**B4. [Finding #14] Fix F3b pull ylabel**
Change "Pull" to "(Data - MC)/sigma" per Phase 4+ requirements.

**B5. [Finding #16] Document eps_uds dominance investigation**
Add a brief investigation to the artifact: why eps_uds is so large, what ALEPH did to constrain it (data control regions), why our method cannot replicate that, and what Phase 4c mitigation is planned (multi-WP fit D14).

**B6. [ARB-1] Correct R_b narrative**
The artifact should state explicitly that R_b on 10% data is dominated by the C_b assumption. The 10% validation demonstrates working infrastructure and data/MC consistency in tag fractions, but the R_b central value is not an independent measurement.

**B7. [ARB-2] Investigate delta_b in A_FB^b fit**
Include delta_b examination as part of the A_FB^b investigation (A1). Compare fitted delta_b to ALEPH published values. Check for contamination-driven inflation.

**B8. [Finding #3] Clarify Phase 4a R_b values**
Add a note to the artifact specifying which C_b assumption produces each quoted Phase 4a R_b value (0.280 at C_b ~ 1.01, 0.305 at C_b = 1.537, 0.310 at different WP/C_b).

### Category C -- Apply before commit (no re-review)

- C1. [Finding #9] Populate comparison_4a_vs_4b.json R_b entry
- C2. [Finding #11] Add brief note on WP=8,9 null extraction mechanism
- C3. [Finding #21] Optionally add pull panel to S1b
- C4. [Finding #24] Note Q_FB negative offset in artifact text
- C5. [Finding #25] Rename sigma column to sigma(slope) in Section 7 table
- C6. [Finding #26] Report sin2(theta_eff) pull from SM with systematic caveat

---

## Reviewer Diagnostic

### Critical Reviewer (hiroshi_ea49)
- **Role coverage:** Thorough. Checked convention coverage (extraction.md section 4 per-subperiod requirement), systematic propagation (C_b systematic at wrong WP, charge_model double-counting), JSON consistency (parameters.json, validation.json, comparison JSON), and section 6.8 compliance. Produced evidence-based findings with specific file paths and numerical values.
- **Coverage gaps:** None significant. The critical reviewer identified 6 Category A findings, all verified as valid. The only finding I downgraded (F3: Phase 4a R_b inconsistency) was appropriately raised -- the downgrade reflects scope boundaries, not a reviewer error.
- **Assessment:** Strong performance. The double-counting bug (F6) and wrong-WP systematic (F5) are exactly the kind of code-level findings the critical reviewer should catch.

### Plot Validator (yuki_519e)
- **Role coverage:** Comprehensive Level 3 validation. Checked registry completeness, code lint (forbidden patterns, derived-quantity sqrt(N)), and visual review of all 8 figures. Cross-figure consistency analysis identified the R_b/A_FB^b tension (CROSS-1).
- **Coverage gaps:** The VISUAL-7 finding (eps_uds > 80% dominance) was flagged as Category A, but it is more appropriately B at the 10% validation stage (the dominance is expected and documented, though investigation is missing). Minor overcall. The VISUAL-4 finding (pull ylabel) was appropriately flagged but is B-level, not A-level.
- **Assessment:** Strong performance. The cross-figure consistency analysis (CROSS-1) added genuine value beyond what the critical reviewer caught. The registry check (REGISTRY-1) caught a real process failure. Two minor severity overcalls (VISUAL-4, VISUAL-7) do not diminish the quality.

---

**VERDICT: ITERATE**

10 Category A findings (A1--A9, with some merged) and 8 Category B findings must be resolved. The A_FB^b investigation (A1) is the highest-priority item and should be attempted first, as its outcome may affect the systematic budget and narrative. Code fixes (A2, A3) and JSON/figure fixes (A4--A9) can proceed in parallel.

No Phase 3 regression is required. All issues are Phase 4b-local.
