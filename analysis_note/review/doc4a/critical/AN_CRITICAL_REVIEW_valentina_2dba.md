# Critical Review — Analysis Note Doc 4a
## Reviewer: valentina_2dba
## Date: 2026-04-02
## Artifact: `analysis_note/ANALYSIS_NOTE_doc4a_v1.tex` (+ .pdf)
## MCP_LEP_CORPUS: true (available but corpus queries not required for findings below — all based on JSON, AN, and methodology)

---

## PASS 1 — METHODOLOGY / VALIDATION AUDIT (JSON vs AN Claims)

### P1.1 — Chi2/p-value cross-check: JSON vs AN

**Kappa consistency** (validation.json `kappa_consistency`): chi2 = 0.7089, ndf = 4, p = 0.9502. AN §6.2 states "chi2/ndf = 0.71/4 (p = 0.95)." MATCHES.

**Per-year consistency** (validation.json `per_year_consistency`): chi2 = 0.9377, ndf = 3, p = 0.8163. AN §6.3 states "chi2/ndf = 0.94/3 (p = 0.82)." MATCHES.

**Operating point stability** (validation.json `operating_point_stability`): passes = false, n_valid_wp = 1. AN §6 Table 6.1 states "OP stability: N valid WPs = 1/4, FAIL." MATCHES.

**Independent closure** (validation.json `independent_closure`): WP7.0 per_wp[0] passes = false (null R_b). WP9.0 per_wp[1] R_b_extracted = 0.3471, pull = 1.9268, passes = true. AN §6.3 states "WP 9.0: R_b = 0.347, pull = 1.93 (pass, < 2sigma)." MATCHES.

**Corrupted corrections** (validation.json `corrupted_corrections_sensitivity`): n_sensitive = 4, n_total = 6, passes = true. AN Table 6.2 states "Sensitive: 4/6, PASS." MATCHES.

### P1.2 — Primary closure test: ±20% corruption sensitivity test

The ±20% corruption sensitivity test IS present and documented (validation.json + AN Table 6.2). Six perturbations tested. **PASS** for this requirement.

However: see Category A finding [A1] below regarding a critical defect in the corruption test design.

### P1.3 — Zero-impact systematics: nominal-vs-varied overlay figures

Flat/borrowed systematics in systematics.json: `sigma_d0` (scaled, no bin-level re-evaluation), `hadronization` (scaled, no re-evaluation), `sigma_d0_form` (symmetric ±0.0004), `mc_statistics` (Poisson), `physics_params` (PDG propagation), `tau_contamination` (published efficiency), `selection_bias` (ratio reduction).

The protocol requires: for each systematic with zero bin-dependent impact, a nominal-vs-varied overlay figure with max|diff| reported. None of these borrowed systematics have associated overlay figures. The AN does not provide them. **See Category A finding [A2].**

### P1.4 — Precision comparison

`validation.json precision_comparison.R_b_vs_ALEPH.ratio` = 283.18 (>> 5x). `investigation_required` = true. The PRECISION_INVESTIGATION.md is documented in Appendix §A.6 of the AN, decomposing the 283x into four factors. **Investigation artifact EXISTS.** However: see Category A finding [A3] for a problem with this investigation.

### P1.5 — Phase findings with Resolution sections

Reviewing the AN:
- Operating point stability failure: Documented in §12.3 and Table 6.1. Resolution: "expected given circular calibration, will be re-evaluated Phase 4b." A resolution section EXISTS but the rationale is a deferral, not a remediation. See Category A finding [A4].
- Closure test at WP7.0 null: Documented. Resolution: documented gap (no remediation attempts). See Category A finding [A4].
- AFB chi2/ndf >> 5 (origin-only fit): Fixed by adding intercept (§7.2, §7.3). Resolution section EXISTS with 3 remediation attempts documented in the artifact. PASS.
- Circular calibration: Documented and relabeled (§4.4). PASS.

### P1.6 — Phase 3 closure chi2 values vs AN

Phase 3 closure test (b) relabeled "bFlag discrimination power" in Phase 3 fix iteration 2 (cosima_d113). AN §6.4 refers to "bFlag discrimination power (chi2/ndf = 11,447), confirming bFlag separates physics populations." Cross-phase log entry confirms this relabeling. **MATCHES.**

**PASS 1 SUMMARY:** 2 of 6 methodology audit items raise Category A concerns:
- P1.3: Missing nominal-vs-varied overlay figures for borrowed/flat systematics → [A2]
- P1.5 (partial): Documented gaps without 3 remediation attempts → [A4]
Additional Category A finding from the corruption test design → [A1]
Additional Category A finding from precision investigation quality → [A3]

---

## PASS 2 — STANDARD CRITICAL REVIEW

---

### [A1] CATEGORY A — Corruption test is not an independent closure test; WP 10.0 (primary WP) was never tested

**Evidence:** The independent closure test (derivation/validation MC split) was performed at WP 7.0 (null extraction) and WP 9.0 (pull = 1.93), but **NOT at WP 10.0**, which is the actual operating point for the primary R_b result. The AN explicitly states: "WP 10.0 was not tested on the validation split (documented gap)."

This means the primary operating point has NO independent closure validation. The result reported in the abstract, in §8.1, and in all comparison tables uses WP 10.0 — a working point that was never subjected to the mandatory independent closure test required by `conventions/extraction.md` §"Required validation checks" item 1.

The validation.json `independent_closure.per_wp` array has only two entries (threshold 7.0 and 9.0). WP 10.0 is absent.

**Severity:** The operating point stability also fails (only 1/4 WPs valid). The analysis is operating on a single working point that passed neither the stability gate nor the independent closure test. `conventions/extraction.md` §3 (Operating point stability) is explicit: "Category A if fails." The failure is acknowledged but no remediation was attempted.

**Required action:** Either (a) run the independent closure test at WP 10.0 and document the result, or (b) if WP 10.0 also fails with null extraction on the validation split, document this as a fundamental method failure at the primary operating point and flag for Phase 4b investigation with at least 3 remediation attempts.

---

### [A2] CATEGORY A — Flat/borrowed systematics have no propagation evidence (bin-dependent shifts absent)

**Evidence:** Seven systematic sources in systematics.json are evaluated via flat estimates or scaling from published ALEPH values rather than actual propagation through the analysis chain:

| Source | Method | AN claim |
|--------|--------|---------|
| sigma_d0 | "Scaled from ALEPH (0.00050) x1.5" | Not re-propagated |
| hadronization | "Scaled from ALEPH (0.00030) x1.5" | Not re-propagated |
| sigma_d0_form | "Scaled from MC statistics systematic" | Form variation unclear |
| mc_statistics | "Poisson uncertainty on MC counts" | Not re-propagated |
| physics_params | "Propagated from PDG uncertainties via efficiency variation" | Vague |
| tau_contamination | "Corrected using published selection efficiency" | Not re-propagated |
| selection_bias | "Ratio measurement: reduced sensitivity" | Not re-propagated |

The reviewer protocol requires: "For each systematic with zero impact: is the nominal-vs-varied overlay figure present with max|diff| reported?" None of these sources has an associated nominal-vs-varied figure. More critically: the requirement that "for every systematic shift: verify the shift is BIN-DEPENDENT" applies here.

The flat sigma_d0 systematic of delta_Rb = 0.00075 is borrowed from ALEPH's published value, scaled by 1.5x. It is claimed to be subdominant and therefore acceptable by the spec's exception ("subdominant AND magnitude is justified by a cited measurement"). The citation is hep-ex/9609005. This exception is met for sigma_d0 and hadronization specifically.

However, the sigma_d0_form systematic (described as "Scaled from MC statistics systematic" in systematics.json) has NO cited measurement backing the magnitude — the source is listed as "STRATEGY.md Section 5.1," which is an internal document, not a published measurement. This fails the flat-estimate exception requirement ("magnitude is justified by a cited measurement"). **Category A** for sigma_d0_form specifically.

**Required action:** Justify sigma_d0_form magnitude against a published measurement or re-derive it by propagating the functional form change through the full analysis chain.

---

### [A3] CATEGORY A — Circular calibration acknowledged but underinvestigated; "calibration self-consistency" framing inadequate

**Evidence:** The calibration procedure assumes R_b = R_b^SM = 0.21578 to derive eps_b, eps_c, eps_uds, then extracts R_b using those efficiencies. The result R_b = 0.280 deviates from the input by 0.064. The AN relabels the Phase 4a R_b result as a "circular calibration self-consistency check" (§8.1) and notes the bias of 0.064.

The problem: **the magnitude of the circular bias (0.064) is not explained quantitatively.** The AN states "the deviation of 0.064 from the input value quantifies the residual bias of the circular procedure" without any analysis of where this bias comes from. Given that the calibration assumes R_b^SM and the extraction uses the same equations, algebraically one expects R_b_extracted ≈ R_b^SM if the calibration is truly self-consistent. The deviation of 0.064 (30% relative to the SM value of 0.216) indicates the procedure is NOT purely circular — it mixes MC and data tag fractions in a non-trivially consistent way.

The `methodology/06-review.md` §6.8 criterion states: any result with pull > 3 sigma from reference requires "a quantitative explanation for the deviation, a demonstrated magnitude match (calculation/toy/fit variant), and no simpler explanation." The deviation (0.280 vs 0.216, pull = 0.064/0.031_stat = 2.1 in statistical terms) is at the 2-sigma level and the AN provides no explanation for why circular calibration produces this specific 0.064 offset. The Precision Investigation (Appendix §A.6) discusses ONLY the precision ratio, not the central value bias.

**Required action:** Quantitatively explain the 0.064 offset. Is it driven by the eps_c calibration being applied to MC (which has a slightly different true composition than assumed)? Is it a consequence of the alpha=0.20 constraint being the physical boundary? A toy study varying the assumed input R_b from 0.15 to 0.25 and showing the resulting extracted R_b would demonstrate whether the 0.064 offset is consistent with the known MC statistics and constraint choices.

---

### [A4] CATEGORY A — Operating point stability failure lacks the required 3 remediation attempts

**Evidence:** `validation.json operating_point_stability.passes` = false. N_valid_wp = 1 (only WP 10.0 valid). The AN §12.3 documents the failure and §8.1 describes it as "expected given the circular calibration." No remediation attempts are documented.

`conventions/extraction.md` §"Required validation checks" item 3 states: "Category A if fails. Investigate before proceeding." The methodology requirement for failing validation tests is 3 documented remediation attempts.

The AN proposes that on data (Phase 4b), the multi-working-point fit will relax the constraint. But this is a DEFERRAL, not a remediation. The question is: were there attempts to make more working points valid at Phase 4a? The experiment log notes only that WPs 7-9 return null extractions due to the underdetermined calibration — no attempt to modify the alpha scan range, adjust the calibration approach, or use a wider alpha range at tighter WPs.

**Required action:** Document at least 3 remediation attempts (e.g., varying the alpha scan range, using a multi-WP calibration, using a different constraint approach) with their outcomes. If all fail due to the structural limitation of the underdetermined calibration, document this explicitly with "INFEASIBLE after 3 attempts" per the methodology.

---

### [A5] CATEGORY A — A_FB^b per-kappa table omits kappa=infinity; claimed 5-kappa analysis has 4-kappa table

**Evidence:** The AN abstract (line 54) and §6.2 claim "five momentum-weighting parameters kappa = 0.3, 0.5, 1.0, 2.0, infinity." The kappa consistency chi2/ndf = 0.71/4 with ndf=4 (consistent with 5 kappas: 5 measurements, 1 combined = 4 dof). However:

- Table 8.1 (per-kappa AFB results, §8.2) lists ONLY 4 rows: kappa = 0.3, 0.5, 1.0, 2.0. kappa=infinity is ABSENT.
- §5.11 "Charge separation model" systematic states: "Spread across A_FB^b values extracted at kappa = 0.3, 0.5, 1.0, 2.0" — explicitly excluding infinity.

The kappa=infinity working point is described in the abstract and claimed to be included in the analysis infrastructure (§A.8 shows data/MC comparison for kappa=infinity), but no A_FB^b result at kappa=infinity is reported. Given that kappa=infinity uses discrete ±1 charges, its chi2/ndf from the linear fit and its A_FB^b value would behave differently from the continuous-kappa results. Its absence from the summary table and the systematic evaluation is unexplained.

The fact that ndf=4 in the kappa consistency test is CONSISTENT with 5 kappas being tested — if kappa=infinity has much lower sensitivity (the leading-particle charge has highest variance, lowest discriminating power per unit variance), it may simply not appear in the table as a matter of editorial choice. But the reviewer protocol demands traceability: [D5] commits to kappa={0.3, 0.5, 1.0, 2.0, infinity} and the per-kappa table must include all five.

**Required action:** Add kappa=infinity row to Table 8.1 with its A_FB^b, delta_b, slope, and chi2/ndf values, or explicitly document why it was excluded from the results table while remaining in the consistency chi2 computation.

---

### [A6] CATEGORY A — COMMITMENTS.md checkbox status does not match Phase 4a deliverables

**Evidence:** The COMMITMENTS.md file was last updated at Phase 2 fix iteration 2. As of the Doc 4a review, the following commitment checkboxes remain unchecked ([ ]) despite being claimed complete in the AN:

**Systematic sources (all [ ]):**
- Tag/selection efficiency, C_b correlation, MC efficiency model
- eps_c, eps_uds contamination, R_c variation, g_bb, g_cc
- Hadronization, physics parameters, sigma_d0 form, tau contamination, selection bias
- Angular efficiency, QCD correction, charm asymmetry, kappa model

The AN (§5) clearly documents all these systematic evaluations as completed. COMMITMENTS.md shows none of them as [x].

**Validation tests (all [ ] or [D]):**
- Closure test (c) [contamination injection]: [ ] — actually completed and reported in §6.4
- Parameter sensitivity table: [ ] — not completed (no sensitivity table in AN)
- Operating point stability: [ ] — completed (FAILS), result in §8.1 and §12.3
- Per-year consistency: [ ] — completed (PASSES), result in §6.3
- Negative d0 tail unit-width: [ ] — validated in §4.1 caption (unit width by construction)
- d0 sign gate [D19]: [ ] — completed and documented in §4.2

**Flagship figures (all [ ]):**
- F1 (stability scan): present as figures/F1_rb_stability_scan.pdf
- F2 (AFB angular): present as figures/F2_afb_angular_distribution.pdf
- F4 (f_d vs f_s): present as figures/F4_fd_vs_fs.pdf
- F5 (systematic breakdown): present as figures/F5_systematic_breakdown.pdf
- F7 (kappa consistency): present as figures/F7_afb_kappa_consistency.pdf

The COMMITMENTS.md was not updated at the Phase 4a boundary. The orchestrator regression checklist requires verification that all [D] labels from the strategy were implemented — an unchecked COMMITMENTS.md makes this audit impossible.

**Additionally flagged:** The "parameter sensitivity table" commitment ([ ]) is genuinely absent from the AN. No table of |dR_b/dParam| * sigma_param is provided. `conventions/extraction.md` item 2 (Parameter sensitivity table) is mandatory. **This specific gap is its own Category A.**

**Required action:** (1) Update COMMITMENTS.md to reflect the Phase 4a completion status, marking completed items [x], formally downscoped items [D], and genuinely open items [ ]. (2) Add the parameter sensitivity table to the AN.

---

### [A7] CATEGORY A — AFB per-kappa chi2/ndf values in the results table are from the WRONG (rejected) fit model

**Evidence:** Table 8.1 (§8.2) shows chi2/ndf values of 80.5/9, 104.9/9, 114.5/9, 101.5/9 for kappa = 0.3, 0.5, 1.0, 2.0. The table footnote (line 1624) states: "The chi2/ndf values in Table 8.1 are from the origin-only fit (without intercept)."

The AN's own §7.2 and §7.3 establish that the origin-only fit is PATHOLOGICAL (chi2/ndf >> 5) and that the intercept-inclusive model is MANDATORY for the governing extraction. Reporting chi2/ndf from the rejected, pathological model in the primary results table — without the chi2/ndf from the ACCEPTED intercept-inclusive fit — will mislead any reader who does not read the footnote.

A physicist reading Table 8.1 would conclude the fit quality is catastrophically bad. The table does not show the chi2/ndf from the accepted intercept-inclusive fit at any kappa value.

This violates the SHOW YOUR WORK principle: the reported chi2/ndf must correspond to the method that produced the reported results, not to an alternative method that was rejected.

**Required action:** Replace Table 8.1's chi2/ndf column with values from the intercept-inclusive fit, or add a second chi2/ndf column for the intercept-inclusive fit. The origin-only chi2/ndf may be retained in a footnote for context but must not be the primary reported value.

---

### [A8] CATEGORY A — Three typos "A_FM^b" throughout the AN (critical label error)

**Evidence:** The observable is the forward-backward asymmetry A_FB^b. The LaTeX command throughout the AN uses `\mathrm{FB}`. However, three specific instances use `\mathrm{FM}`:

- Line 143 (Introduction): "the hemisphere jet charge method for $A_\mathrm{FM}^b$."
- Line 1845 (Conclusions §1): "The full analysis infrastructure for measuring $R_b$, $R_c$, and $A_\mathrm{FM}^b$..."
- Line 2215 (Appendix §A.2): "a 10\% $R_b$--$A_\mathrm{FM}^b$ correlation"

These are typos in the observable label (FM instead of FB) that would make the AN unpublishable. While this is a typographic error, it appears in the introduction, conclusions, and covariance appendix — the three sections most likely to be read by a referee. Category A because it affects the scientific communication of the observable identity.

**Required action:** Replace all three instances of `A_\mathrm{FM}^b` with `A_\mathrm{FB}^b`.

---

### [B1] CATEGORY B — sigma_d0 calibration yields scale factors of 7.6x: not adequately investigated

**Evidence:** §4.1 states calibrated scale factors range from 1.3 to 7.6. Tracks with 1 VDET hit have scale factors 2.5–7.6, meaning the nominal sigma_d0 parameterization underestimates the actual resolution by factors of 2.5–7.6x for these tracks.

A factor of 7.6 is very large. The AN attributes this to "beam spot, primary vertex, and detector alignment effects not captured by the simple two-parameter model." However:

1. The published ALEPH VDET paper (cited as ALEPH:VDET) presumably has more realistic resolution estimates. The scale factors of 7.6x suggest the parameterization A=25um, B=70um·GeV/c is entirely wrong for 1-VDET tracks at some angles, not just underestimated.
2. Per Appendix §A.5 (Primary Vertex Investigation), data/MC sigma_d0 scale factor ratio is 1.10 (data 10% worse). But if the scale factors are 7.6x on MC tracks, how is the data/MC ratio only 1.10?

The AN does not attempt to cross-check whether the 7.6x scale factor tracks are actually useful for b-tagging (tracks with essentially unknown impact parameter precision) or whether they should be excluded. Including tracks with 7.6x miscalibrated impact parameters inflates the lifetime tag and biases the hemisphere probability.

**Required action:** Investigate whether tracks in bins with scale factors > 4x are making a positive contribution to b-tagging efficiency or introducing bias. If their inclusion worsens the tag quality (lower ROC), exclude them and document.

---

### [B2] CATEGORY B — C_b >> 1 not adequately investigated as a physics red flag

**Evidence:** The analysis measures C_b = 1.54 at WP 10.0, versus the published ALEPH value of C_b ≈ 1.01. The conventions/extraction.md "MVA-induced hemisphere correlations" pitfall states: "Check C_q at the working point: values far from 1.0 (C_b < 0.8 or C_b > 1.3) indicate the classifier introduces correlations beyond the QCD effects." C_b = 1.54 clearly exceeds the 1.3 threshold.

The AN correctly identifies three sources of the inflation (shared thrust axis, gluon radiation, resolution correlation). But it does not investigate whether these sources can be mitigated at Phase 4a:
- The thrust axis is fixed, but using per-hemisphere thrust axes (or the event thrust axis offset by hemisphere) would reduce the shared-axis correlation.
- The resolution correlation source (sigma_d0 calibrated globally) could be tested by varying the calibration binning.

More critically: the self-calibrating advantage of the double-tag method relies on C_b ~ 1. With C_b = 1.54, the f_d/f_s^2 ratio is substantially larger than C_b_true, introducing a systematic in the R_b extraction that is partially — but not entirely — absorbed into the C_b systematic (delta_R_b = 0.010). The 0.010 systematic was derived as "2 × max(sigma_MC, |C_b_data - C_b_MC|)" at WP 10.0, giving delta_C_b ~ 0.010. But the systematic on R_b propagated from this delta_C_b = 0.010 is only 0.010 in R_b — is the propagation formula correct? delta_R_b / delta_C_b should be approximately f_d / (eps_b^2) ~ 0.044 / 0.238^2 ~ 0.78. Thus delta_R_b ~ 0.78 × 0.010 ~ 0.008, which is consistent with the reported 0.010 (using the asymmetric propagation). This cross-check passes, but only barely.

**Required action:** Add a sentence justifying that the C_b systematic (0.010) was verified against the analytical derivative delta_R_b/delta_C_b, and report the derivative value.

---

### [B3] CATEGORY B — eps_c solver failure at +30% not investigated; only one direction propagated

**Evidence:** §5.4 and systematics.json `R_b.eps_c.shift_up` = null (solver failure). The AN states: "delta_R_b uses the shift_down direction only." The systematic (0.078) is therefore a one-sided estimate.

Standard practice for asymmetric systematics is to either (a) use the larger of the two directions symmetrically, or (b) report as an asymmetric uncertainty. The AN uses method (a) implicitly but does not state it. More importantly: the solver failure at +30% eps_c means the analysis operates near the physical boundary of parameter space even at the NOMINAL eps_c. A +30% shift pushes it past the boundary, making the extraction infeasible. This is a significant structural problem that deserves more than a one-sentence note.

**Required action:** Document whether any of the 1000 toys at WP 10.0 that fail (the ~80% with null extractions) correspond to the +eps_c regime, and whether the toy failure rate correlates with the eps_c boundary.

---

### [B4] CATEGORY B — Independent closure at WP9.0 has only 305/1000 valid toys (30.5% convergence)

**Evidence:** validation.json `independent_closure.per_wp[1].n_valid_toys` = 305 (out of 1000, threshold 9.0). AN §6.3 cites this. A 30.5% toy convergence rate means 69.5% of pseudo-experiments produce unphysical solutions at WP 9.0. This is the working point at which the "independent closure" validation was performed.

With 305 valid toys, the RMS-based pull uncertainty has a statistical uncertainty of approximately 1/sqrt(2*305) ~ 4% on the pull value itself. The pull of 1.93 is just below the 2.0 threshold — within ~0.07 of failing. Given the ~4% uncertainty on the pull estimate, this pass is marginal.

The AN does not report confidence intervals on the pull estimate, and does not discuss whether the 69.5% toy failure rate indicates a physically meaningful breakdown at WP 9.0 (not just at WP 10.0).

**Required action:** Report the uncertainty on the pull estimate from finite toy statistics (sqrt(2) * pull / sqrt(n_valid)) and note that the pass is marginal (1.93 ± ~0.08). Discuss whether 305 valid toys is sufficient.

---

### [B5] CATEGORY B — Gluon correction formula (Eq. 4.8): r_b and r_c are undefined

**Evidence:** Equation 4.8 (gluon correction to eps_uds_eff) introduces r_b and r_c as "the tagging efficiency ratios for gluon-produced heavy quarks relative to direct production" but provides no values, citations, or estimates. The systematics.json entry for g_bb lists delta_Rb = 0.00011 "from effective eps_uds variation" but does not document how r_b was determined.

If r_b = r_c = 1 (gluon-splitting b quarks have the same tagging efficiency as direct b quarks), this should be stated explicitly. If different values were used, they must be cited.

**Required action:** State the values of r_b and r_c used in Eq. 4.8 and cite the source (or document that they are assumed to be 1).

---

### [B6] CATEGORY B — The "data" tag fractions f_s and f_d in Table 4.1 are from DATA, not MC — but Phase 4a is supposed to use MC pseudo-data only

**Evidence:** Table 4.1 (§4.4) lists f_s and f_d at working points "measured on data." The AN explicitly states this is Phase 4a. `conventions/extraction.md` §"Standard configuration" states: "The expected result must be computed on MC-generated pseudo-data counts, not on real data."

The calibrated efficiencies in Table 4.3 are from "full MC." The R_b extraction at WP 10.0 uses these MC-calibrated efficiencies but then applies them to extract R_b. The question is: what f_s and f_d are used for the R_b extraction — the data values in Table 4.1, or MC-generated values?

parameters.json shows R_b = 0.2798, while R_b^SM = 0.21578. If the extraction used MC f_s and f_d with SM-derived efficiencies, one expects R_b ≈ 0.216 (up to circular calibration bias). If the extraction uses DATA f_s and f_d (0.172, 0.044) with MC efficiencies, the 0.280 result reflects the real data content — violating the Phase 4a convention.

The AN §8.1 states the result is "a self-consistency diagnostic of the circular calibration procedure." But if data f_s and f_d are being used, this is not purely MC pseudo-data — it is a real data measurement disguised as Phase 4a.

This needs clarification. If the AN is using real data tag fractions for the primary R_b result reported in the abstract and results section, this constitutes premature unblinding.

**Required action:** Explicitly document in §7.1 (R_b extraction) and §8.1 (R_b result) whether the f_s and f_d used in the primary R_b extraction are from (a) MC pseudo-data (generated counts from MC efficiencies times N_had), or (b) data (observed counts in the data sample). If (b), this is a Phase 4c result, not Phase 4a.

---

### [B7] CATEGORY B — Validation table (Table 6.1) lists "Angular fit chi2: FAIL (fixed w/ intercept)" without providing the post-fix chi2

**Evidence:** Table 6.1 reports the AFB angular fit chi2 as "80–115/9, FAIL (fixed w/ intercept)." But: (a) the chi2 from the intercept-inclusive fit is not reported in this table, and (b) the word "FAIL" in the validation summary refers to the rejected model.

The validation table should show the chi2 from the ACCEPTED fit model. The AN elsewhere states the intercept-inclusive fit "substantially improves chi2" but no specific post-fix chi2 values are reported.

**Required action:** Report the chi2/ndf from the intercept-inclusive fit for each kappa value in Table 6.1 (or as a separate entry in the table), and replace "FAIL (fixed w/ intercept)" with "PASS (chi2/ndf = X/Y with intercept)."

---

### [B8] CATEGORY B — The D12b downscoping is structurally problematic: four-quantity fit abandoned on wrong grounds

**Evidence:** COMMITMENTS.md [D12b] is "Formally downscoped at Phase 4a: on symmetric MC (A_FB = 0), the four-quantity fit cannot meaningfully constrain sin^2(theta_eff)." This reasoning is correct as stated — but the strategy commitment (inspire_433746 Section 4) specifies a four-quantity simultaneous fit as the governing extraction method. Downscoping the governing method to a linear regression on MC grounds, then planning to implement it "in Phase 4b/4c," means Phase 4a never validates the four-quantity fit infrastructure.

By Phase 4b, when real asymmetry is present, implementing the four-quantity fit for the first time on blinded data is a riskier approach than having tested it first on MC (even if the sin^2 extraction is uninformative). Phase 4a is precisely the time to debug the four-quantity fit implementation.

The [D12b] downscoping was reviewed and accepted, but from a strict physics standpoint, the linear regression used here is a different extraction method from the one committed to. The robustness cross-check between linear regression and four-quantity fit cannot happen on MC, meaning Phase 4b will have to implement and validate simultaneously under tighter schedule pressure.

This is Category B (not A) because the downscoping was formally reviewed and accepted. However, the risk to Phase 4b should be explicitly noted.

**Required action:** Add a risk note to the Phase 4b outlook section (§10.5 item 4) stating that the four-quantity fit will need both implementation and validation at Phase 4b, without the ability to compare to a Phase 4a baseline.

---

### [C1] CATEGORY C — Abstract cites R_b and A_FB^b precision values that conflate different representations

The abstract reports "R_b = 0.280 ± 0.031 (stat) ± 0.395 (syst)" where the syst is 0.395 while the JSON has syst = 0.3952. The rounding is conservative (0.395 vs 0.3953) but inconsistent with the body text at line 1557 which cites "R_b.syst = 0.3953." Standardize to 3 significant figures throughout (0.395 or 0.3953, not both).

---

### [C2] CATEGORY C — MC event count in data/MC comparison: 730,365 vs 7.8M

Table 3.1 (MC samples) states "~7.8M events estimated." Table 3.2 (cutflow) shows "MC 771,597 total events" before cuts, 730,365 after. The 771K vs 7.8M discrepancy — a factor of ~10 — is not explained. Is the 7.8M an error from the Phase 1 estimate based on file size? The actual MC sample is much smaller. This discrepancy between the text and the table should be resolved.

---

### [C3] CATEGORY C — Missing kappa=infinity in systematic evaluation (charge_model systematic uses only kappa = 0.3, 0.5, 1.0, 2.0)

The charge_model systematic (delta_AFB = 0.0022) is defined as "Spread across A_FB^b values extracted at kappa = 0.3, 0.5, 1.0, 2.0" (§5.11). The kappa=infinity case is excluded. If it is included in the kappa consistency chi2 test (ndf=4 for 5 kappas), it should also be included in the systematic evaluation. The kappa=inf case has highest variance (discrete ±1 charge) and its inclusion could either widen or narrow the spread depending on its A_FB^b value on MC.

---

### [C4] CATEGORY C — Cross-reference inconsistency: Sec. 5.1 C_b inflated by 2x per [D17]; but [D17] is about primary vertex investigation, not C_b

§5.2 states the C_b variation is "inflated 2× per strategy decision [D17]." But [D17] in the limitation index is "Primary vertex definition: investigate d0 reference point at Phase 3." The 2× inflation is a reasonable choice but the [D17] reference is to the investigation that motivated it, not to a specific numeric commitment. The reviewer would expect a [D] label for the 2× inflation factor itself, or an explicit statement that this factor was decided as a result of [D17].

---

### [C5] CATEGORY C — The kappa consistency chi2/ndf = 0.71/4 is suspiciously good (p=0.95)

On MC where A_FB^b = 0 by construction, all kappa values return A_FB^b ≈ 0 trivially. The spread across kappa values reflects only measurement noise. A chi2/ndf of 0.71 with p=0.95 is entirely consistent with this scenario and provides no validation of the charge separation model — it simply confirms that noise fluctuations are consistent with zero. This should be noted explicitly: the kappa consistency test is uninformative at Phase 4a precisely because the MC is symmetric. The diagnostic becomes meaningful on data (Phase 4b).

---

## COMPLETENESS CROSS-CHECK

**Systematic sources:** AN documents 12 sources for R_b and 4 for A_FB^b (16 total). COMMITMENTS.md lists ~15 systematic categories (some overlapping). `conventions/extraction.md` required categories: efficiency modeling (3 sub-items), background contamination (2), MC model (2), sample composition (2) — all 4 categories are covered.

**Missing:** Parameter sensitivity table (|dR_b/dParam| × sigma_param per COMMITMENTS.md and `conventions/extraction.md` item 2) — ABSENT from AN. **Category A flag already in [A6].**

**Validation tests with results:** Independent closure (done at WP 9.0, not WP 10.0), corrupted corrections (done, 4/6), per-year consistency (done on MC subsets), kappa consistency (done), operating point stability (done, FAILS). Missing: independent closure at WP 10.0 [A1].

**Flagship figures:** F1, F2, F4, F5, F7 are all present as PDF files. F3 and F6 formally downscoped with documentation. ✓

**COMMITMENTS.md not updated** — Phase 4a completion status not reflected. **Category A flag in [A6].**

---

## DECISION LABEL TRACEABILITY

| [D] Label | Commitment | Implemented? |
|-----------|-----------|--------------|
| [D1] LEP EWWG observable definitions | Observable definitions verified against hep-ex/0509008 | Yes (§2.1, Strategy §2.2) |
| [D2] Double-tag for R_b | Double-tag method used | Yes |
| [D3] Simplified 2-tag system | Combined prob+mass tag | Yes |
| [D4] Hemisphere jet charge for A_FB^b | Implemented | Yes |
| [D5] kappa = {0.3, 0.5, 1.0, 2.0, inf} | 5 kappas computed | Partial — kappa=inf absent from results table [A5] |
| [D6] R_c constrained to SM | Implemented | Yes |
| [D7] sigma_d0 from negative tail | 40-bin calibration done | Yes |
| [D8] Combined prob+mass tag | Primary tagger | Yes |
| [D12] Self-calibrating fit (governing) | Linear regression with intercept | Yes (note: four-quantity fit downscoped [D12b]) |
| [D12b] Four-quantity fit | Formally downscoped | [D] with documentation |
| [D13] Toy-based uncertainty propagation | Implemented | Yes |
| [D17] Primary vertex investigation | Investigated, infeasible | Yes (Appendix §A.5) |
| [D19] d0 sign convention gate | Passed | Yes (§4.2) |

**Finding:** [D5] is partially violated — kappa=infinity is included in the infrastructure but absent from the results table and systematic evaluation. **Already flagged as [A5].**

---

## ADVERSARIAL PROBING

**"Within 2-sigma" at WP9 closure:** The pull of 1.93 is "within 2-sigma" but: (a) it uses 305 valid toys from a 1000-toy run (69.5% failure rate), (b) it is at WP 9.0, not WP 10.0 (the operating point), and (c) the denominator is the toy RMS from 305 samples. The claim that this validates the method is marginally defensible but weak. The marginal pass (1.93 vs 2.0 threshold) with 30.5% convergence is not confidence-inspiring.

**"Circular calibration self-consistency diagnostic":** This relabeling is honest but masks a deeper problem: the analysis cannot distinguish between circular bias and a real measurement. The R_b = 0.280 could reflect (a) pure circular bias (expected ~0 deviation from SM input), (b) real data content if data f_s/f_d were used, or (c) a mix. The 0.064 unexplained offset [A3] is the concrete symptom.

**"eps_uds will be constrained in Phase 4b":** The plan to constrain eps_uds from a multi-WP fit is described as reducing the systematic from 0.387 to "~0.02." This is a 20x improvement claimed from a technique that has not been tested. The strategy for the multi-WP fit ([D14] in COMMITMENTS.md) is not analyzed or prototyped in the Phase 4a artifact — there is no demonstration that the multi-WP system is over-constrained, or that the functional forms of eps_q(WP) are sufficiently constrained by 4 working points. This claim should be hedged more carefully.

**Competing group question:** "If a competing group published a measurement of R_b next month, what would they have that we don't?"
1. An independent closure test at the primary operating point
2. A parameter sensitivity table per conventional standards
3. Multi-working-point extraction with demonstrated stability
4. Per-hemisphere primary vertex (reducing C_b from 1.54 to ~1.01)
5. Results consistent across at least 2 valid working points

Items 1-3 are addressable at Phase 4a. Items 4-5 require Phase 4b.

---

## CLASSIFICATION SUMMARY

| ID | Category | Description |
|----|----------|-------------|
| [A1] | A | No independent closure test at WP 10.0 (primary operating point) |
| [A2] | A | sigma_d0_form systematic has no published measurement backing the magnitude |
| [A3] | A | 0.064 circular calibration bias unexplained quantitatively |
| [A4] | A | Operating point stability failure: no 3 remediation attempts documented |
| [A5] | A | kappa=infinity absent from per-kappa results table and systematic evaluation |
| [A6] | A | COMMITMENTS.md not updated; parameter sensitivity table absent |
| [A7] | A | Per-kappa A_FB^b table reports chi2/ndf from rejected (origin-only) fit model |
| [A8] | A | Observable label "A_FM^b" typo in 3 locations (Introduction, Conclusions, Appendix) |
| [B1] | B | sigma_d0 scale factors up to 7.6x: high-scale-factor tracks not investigated for bias |
| [B2] | B | C_b propagation from delta_C_b to delta_R_b not cross-checked against analytical derivative |
| [B3] | B | eps_c solver failure at +30%: one-sided systematic not analyzed |
| [B4] | B | Closure at WP9.0: marginal pass (pull=1.93) with only 30.5% toy convergence |
| [B5] | B | r_b, r_c undefined in gluon correction formula (Eq. 4.8) |
| [B6] | B | Ambiguity: are f_s, f_d in R_b extraction from data or MC pseudo-data? |
| [B7] | B | Validation table: "FAIL (fixed w/ intercept)" without post-fix chi2 |
| [B8] | B | D12b downscoping: four-quantity fit never validated on MC, risk to Phase 4b |
| [C1] | C | Rounding inconsistency: syst 0.395 vs 0.3953 across abstract and body |
| [C2] | C | MC event count: 771K vs 7.8M inconsistency between text and table |
| [C3] | C | kappa=infinity excluded from charge_model systematic evaluation |
| [C4] | C | C_b 2x inflation cited as [D17] (vertex investigation), not a dedicated decision label |
| [C5] | C | Kappa consistency chi2 = 0.71/4 uninformative on symmetric MC; should note this explicitly |

**VERDICT: ITERATE**

Eight Category A findings must be resolved before the AN advances to the next review stage. Findings [A1], [A4], [A6], and [A7] are the most structurally significant and should be prioritized. The [A8] typo fix is trivial but must not be overlooked.

---

*Review completed by valentina_2dba, 2026-04-02.*
*Note: MCP_LEP_CORPUS = true; no corpus queries were required — all findings are based on numerical consistency checks against results/*.json, convention coverage against conventions/extraction.md, and AN text analysis.*
