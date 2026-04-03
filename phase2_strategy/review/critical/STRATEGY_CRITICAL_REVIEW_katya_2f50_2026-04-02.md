# Critical Review — Phase 2 Strategy (Iteration 2)
**Reviewer session:** katya_2f50
**Date:** 2026-04-02
**Artifact:** `phase2_strategy/outputs/STRATEGY.md` (fixed by felix_d976, 2026-04-02)
**Prior review:** sigrid_16b8 (iteration 1) — ITERATE with 5A, 5B, 4C
**Upstream:** DATA_RECONNAISSANCE.md, INPUT_INVENTORY.md, LITERATURE_SURVEY.md
**Conventions:** `conventions/extraction.md`
**MCP_LEP_CORPUS:** true — corpus queries executed (10 searches)
**Approach:** FRESH full review of the fixed artifact, informed by iteration 1 findings

---

## Summary

This is a fresh review of the post-fix STRATEGY.md. The iteration 1 fixer (felix_d976) resolved
the 7 Category A and 13 Category B items from the arbiter's ITERATE verdict. I evaluate the
full artifact independently, then cross-check iteration 1 concerns for resolution. The strategy is
substantially improved: the gluon-splitting formula, closure test design, sigma_d0 form, and PDG
inputs are now correct. However, five new or residual concerns require resolution before the
strategy can advance.

---

## Prior-Review Concern Disposition

Cross-checking REVIEW_CONCERNS.md items [CP1]–[CP4] and iteration-1 items A1–A5:

| Concern | Status in Fixed Artifact | Evidence |
|---------|--------------------------|----------|
| [CP1] Closure test tautology (A1) | **RESOLVED** | Section 9.1 now commits to three independent closure tests: negative-d0 pseudo-data, bFlag consistency, artificial contamination injection. None rely on same-MC half-split. |
| [CP2] A_FB^b formula inconsistency (A2) | **PARTIALLY RESOLVED — residual issue remains** | Section 4.2 now labels simplified formula as approximation. However, the strategy's governing extraction in Section 6.3 does not match inspire_433746's actual Section 4 fit procedure. See Finding A1 below. |
| [CP3] sigma_d0 sin^{3/2} form (A4) | **RESOLVED** | Section 5.1 and 9.3 now use sin(theta). Systematic for varying between sin(theta) and sin^{3/2}(theta) added. |
| [CP4] PDG inputs not fetched (A5) | **RESOLVED** | INPUT_INVENTORY.md updated: M_Z = 91.1880 +/- 0.0020 GeV, Gamma_Z = 2.4955 +/- 0.0023 GeV, B hadron lifetimes from PDG 2024. |
| A3: Gluon splitting formula | **RESOLVED** | Section 10.2 now uses correct effective eps_uds formulation. COMMITMENTS.md updated. |
| B4: g_bb inconsistency | **PARTIALLY RESOLVED** | Section 7.1 now uses LEP average (0.251 +/- 0.063)%; consistent with COMMITMENTS.md. Notation not in two-component form (not critical — see Finding C1). |
| B5: kappa=infinity exclusion | **RESOLVED** | [D5] now includes kappa=infinity; corrected justification (PID not required for feasibility, reduced delta_b without PID documented). |
| B1: eps_c control region | **PARTIALLY RESOLVED** | Section 7.2 now documents the argument for no charm control region and commits to +/- 30% relative uncertainty. However, the bound is asserted, not derived. See Finding B2. |
| B2: cos theta binning chi2 | **RESOLVED** | [D12] now commits to chi2/ndf at each configuration; bin-count scan (6, 8, 10, 12 bins) added. |
| B3: BDT circularity diagnostic | **RESOLVED** | [D10] now commits to slope diagnostic. |

---

## Checklist of Items Examined

| Item | Status |
|------|--------|
| Phase 1 findings used | PASS — [A1]–[A6] all cited with grounded decisions |
| Observable definitions | PASS (with residual — see A1) |
| Backgrounds classified | PASS — Section 10 with type, fraction, treatment, gluon splitting treatment |
| Systematic plan covers extraction.md row-by-row | PASS — all required sources addressed |
| MC coverage respected | PASS — Section 7 limits model-dependence systematic to 1994 MC, per-year as cross-check |
| Reference analyses tabulated | PASS — 5 references with numerical values |
| >=2 qualitatively different selection approaches | PASS — cut-based (5.1) and BDT (5.2) |
| MVA considered | PASS — BDT with three proxy-label strategies |
| Mitigation for every Phase 1 constraint | PASS (with noting of B1 residual) |
| Precision estimates grounded | PASS — grounded in double-tag formula scaling |
| COMMITMENTS.md populated | PASS — all 18 decisions, systematics, figures, cross-checks |
| Corpus queries executed | PASS — 8 queries in experiment log, results cited |
| Flagship figures defined (6) | PASS — 7 figures plus supporting figures |
| Correction strategy defined | PASS — Section 13 |
| Theory comparison independence | PASS |
| A_FB^b self-calibrating fit correctly specified | PARTIAL — see A1 |
| Closure tests operationally meaningful | PASS |
| Gluon splitting treatment | PASS |
| PDG inputs fetched | PASS |

---

## Findings

### Category A — Must Resolve

---

#### A1. The A_FB^b governing extraction (Section 6.3 / [D12]) mischaracterizes inspire_433746's actual fit

**Finding:** The strategy's Section 6.3 describes the governing extraction as:

> "self-calibrating fit: In b-tagged events, the observed charge asymmetry is:
> `<Q_FB>(cos theta) = sum_q f_q * delta_q * A_FB^q * cos(theta)`
> The fit extracts A_FB^b and delta_b simultaneously by using multiple b-tag purities and multiple kappa values."

This formulation — fitting the mean charge asymmetry as a function of cos(theta) — is not the extraction method used in inspire_433746 Section 4. The corpus retrieval of inspire_433746 Section 4 (Fit Procedure) shows:

> "The four measured quantities (Q_FB, delta, epsilon^h, epsilon^e) are fitted simultaneously in each bin of cos(theta) and hemisphere tag window as a function of three independent variables: (a) delta_b, (b) epsilon^h_b and (c) the weak mixing angle sin^2(theta_eff_w)."

The ALEPH method fits **four** measured quantities simultaneously: the forward-backward charge asymmetry Q_FB, the mean charge separation vector delta, the hemisphere tagging efficiency epsilon^h, and the lepton efficiency epsilon^e. The fit parameter is sin^2(theta_eff) varied through m_top, not A_FB^b directly. A_FB^b is derived from the fitted sin^2(theta_eff). The "Lagrange Multipliers" method is used.

The strategy's formulation `<Q_FB> = sum f_q delta_q A_FB^q cos(theta)` is the formula for the expected mean charge asymmetry in a mixed sample — this is the model being fitted, not a description of the fit procedure. The strategy conflates the expected-value formula with the fit procedure.

**Why this matters:** The Phase 4 executor will implement the A_FB^b extraction based on Section 6.3. If it implements a chi2 fit to the mean Q_FB distribution as a function of cos(theta) — fitting for A_FB^b and delta_b as free parameters — this is a legitimate alternative but differs from the ALEPH reference method which:
1. Uses sin^2(theta_eff) as the fundamental fit parameter (not A_FB^b)
2. Includes epsilon^h and epsilon^e as additional simultaneously fitted quantities
3. Uses Lagrange multipliers, not a standard chi2 minimization

The DELPHI method (inspire_1661252, inspire_1661115) uses the five event-category chi2 fit (N, N_bar, N^D, N^D_bar, N^same) — this is also a valid approach but distinct from ALEPH's. The strategy does not commit to either the ALEPH or DELPHI fit formulation with sufficient specificity. The current description could be interpreted as either.

**Note on CP2 (prior concern):** The iteration 1 fixer correctly designated the simplified formula as an approximation and the self-calibrating fit as governing. However, the fixer's characterization of the "self-calibrating fit" in Section 6.3 remains at the level of the expected-value model, not the operational fit implementation. The prior concern was resolved in principle (the correct method is named) but not in substance (the fit implementation is still ambiguous).

**Verification:** RAG retrieval of inspire_433746 Section 4 confirms the four-quantity simultaneous fit with sin^2(theta_eff) as the fit parameter. The formula `<Q_FB>(cos theta) ~ f_b * delta_b * A_FB^b * cos(theta)` appears in the strategy's Section 6.3 as an intermediate step, but the fit procedure is what determines what Phase 4 executes.

**Required fix:** Section 6.3 / [D12] must commit to a specific fit implementation. Two options:
(a) ALEPH method: fit Q_FB, delta, epsilon^h simultaneously as function of cos(theta) with sin^2(theta_eff) as fit parameter — extract A_FB^b from sin^2(theta_eff) via the EW relation. Requires hardcoding the m_top--sin^2(theta_eff) relation.
(b) Simplified chi2 fit to <Q_FB>(cos theta) treating A_FB^b and delta_b as free parameters per kappa value — simpler to implement, not exactly the ALEPH method but self-consistent. Document as a simplification with respect to inspire_433746.
Either choice is acceptable, but the strategy must commit to one and document the difference from inspire_433746 if option (b) is chosen. The current text is ambiguous between the two.

---

#### A2. Inconsistency between experiment log and STRATEGY.md on kappa values for A_FB^b

**Finding:** The experiment log entry for Phase 2 (peter_b030, 2026-04-02) states under "Key Strategy Decisions":

> "2. A_FB^b via hemisphere jet charge: Standard ALEPH method. kappa = {0.3, 0.5, 1.0, 2.0}."

The STRATEGY.md Section 4.2 and [D5] state: "kappa = {0.3, 0.5, 1.0, 2.0, infinity}" (infinity added in the iteration 1 fix).

The COMMITMENTS.md lists [D5] as "kappa = {0.3, 0.5, 1.0, 2.0, infinity}".

**The experiment log is stale.** It was written before the iteration 1 fix and was not updated by the fixer. The log states kappa = {0.3, 0.5, 1.0, 2.0} (four values, no infinity), but STRATEGY.md and COMMITMENTS.md now commit to five values including infinity.

This is a Category A concern because the experiment log is the primary audit trail and is read by orchestrators on session recovery and by downstream reviewers to understand what was decided. A stale experiment log that conflicts with STRATEGY.md creates ambiguity: a Phase 3 executor reading only the experiment log would implement four kappa values, not five.

**Verification:** experiment_log.md line ~82 states "kappa = {0.3, 0.5, 1.0, 2.0}" (four values). STRATEGY.md [D5] and COMMITMENTS.md [D5] state five values including infinity. The fix log (felix_d976, 2026-04-02) states Category B fix #16: "Corrected [D5] to include kappa=infinity" but did not update the experiment log.

**Required fix:** Append a correction entry to experiment_log.md recording that the kappa set was updated to {0.3, 0.5, 1.0, 2.0, infinity} in the iteration 1 fix, with citation to [D5]. This takes < 5 minutes and is not a strategy decision — it is a documentation correction.

---

### Category B — Should Address

---

#### B1. eps_c uncertainty bound of +/- 30% relative is asserted, not derived

**Finding:** Section 7.2 (Calibration Independence) now documents the argument for not having a charm control region:

> "a charm-enriched control region would require either D meson reconstruction (needs PID) or a soft lifetime cut, but the soft cut produces a sample dominated by b contamination rather than a pure charm sample."

This argument is sound. However, the consequence is then stated as:

> "eps_c is assigned +/- 30% relative uncertainty (covering the MC statistical uncertainty of ~10% and the data-MC modelling difference), propagated as a systematic via re-extraction."

The "+/- 30% relative" is presented without derivation. The "MC statistical uncertainty of ~10%" is asserted without showing the MC event count in the charm-sensitive region at the working point. The "data-MC modelling difference" is not estimated from any comparison — there is no charm-enriched data sample to compare to.

The extraction.md convention states: "If data-derived calibration is not feasible, assign the full data/MC difference as a systematic — but document why calibration was not done." The strategy documents why, but "full data/MC difference" requires an estimate of the data/MC difference, which the strategy does not provide.

**Note:** This was B1 in iteration 1 and was addressed as Category B fix #13 ("Documented why no charm control region; specified +/- 30% relative uncertainty range"). The fix correctly documented the argument, but the specific value 30% remains ungrounded. The fixer cited "MC statistical uncertainty of ~10%" but the 30% total requires the other 20% to come from somewhere quantifiable.

**Required fix:** Either (a) derive the 30% from a comparison of published ALEPH eps_c estimates across different working points (e.g., from hep-ex/9609005's fit results, which provide eps_c at different tag purities), or (b) state that 30% is a conservative bound based on the typical data/MC efficiency ratio for b and c hadrons at LEP (citing a comparable analysis), or (c) use the published eps_c value from hep-ex/9609005 directly, with the full spread between light and heavy tagger working points as the uncertainty range. Any of these is acceptable; an ungrounded percentage is not.

---

#### B2. [D12] kappa=infinity in A_FB^b is committed but its delta_b characteristics are not discussed

**Finding:** [D5] and Section 4.2 commit to including kappa=infinity (leading particle charge). Section 4.2 states:

> "kappa = infinity (leading particle charge — the charge of the highest-momentum track in the hemisphere) does NOT require particle identification; PID improves it but is not required."

However, neither Section 4.2 nor the systematic plan (Section 7.4) discusses the expected charge separation delta_b for kappa=infinity. The published ALEPH analysis (inspire_433746) achieves its precision partly from combining the kappa values, weighted by their information content. kappa=infinity has the lowest charge separation delta_b of all kappa values (it uses only one track's charge, which may not be the b-hadron's primary decay product). If delta_b(kappa=inf) is small — which it will be without PID — the kappa=infinity measurement will have large statistical uncertainty and may degrade the combination.

The strategy commits to reporting delta_b at each kappa value (Section 12, supporting figures: "delta_b vs kappa"), but does not commit to a stability check that verifies kappa=infinity does not dominate the systematic budget or bias the combined result.

**Specific risk:** If kappa=infinity has very small delta_b (e.g., delta_b ~ 0.05 vs delta_b ~ 0.23 for kappa=0.5, from inspire_433746), the extracted A_FB^b will have very large statistical uncertainty for that kappa value, and the combination weight will be negligible. In that case, including kappa=infinity adds no information but adds a cross-check. The strategy should commit to evaluating whether kappa=infinity contributes meaningfully to the combination, and if delta_b is below some threshold (e.g., delta_b < 0.1), document kappa=infinity as a cross-check only rather than an equal partner in the combination.

**Required fix:** Add to Section 4.2 or Section 7.4: "Evaluate delta_b(kappa=infinity). If delta_b < 0.1 (where the information contribution to the combination is < 5% of the kappa=0.5 contribution), document kappa=infinity as a cross-check only and do not include it in the primary combination." This prevents the combination from being over-weighted toward a measurement with negligible information.

---

#### B3. The bFlag=4 interpretation ambiguity is flagged but no Phase 3 investigation action is formalized

**Finding:** Section 9.6 now includes an important note:

> "Note on bFlag=4 interpretation: bFlag=4 for 94% of events is too high a fraction to be a b-tag (R_b ~ 21%). It is more likely an event quality or selection flag... Phase 3 must investigate this by checking the correlation between bFlag and our b-tag output."

This is correct and was added as Category C fix #23. However, COMMITMENTS.md does not include a validation test or cross-check commitment for the bFlag interpretation investigation. The note says "Phase 3 must investigate" but no COMMITMENTS.md entry formalizes this.

**Why this matters:** [D9] commits to "BDT training with bFlag proxy labels (option 1)" — this is a binding decision that depends on bFlag=4 meaning something useful as a signal proxy. If Phase 3's investigation reveals bFlag=4 is a geometric acceptance flag (expected for ~94% of hadronic events passing passesAll), then [D9] is based on a faulty premise. A BDT trained on bFlag=4 as "signal" will learn to separate geometric acceptance from non-acceptance — not b from non-b. The strategy does not have a formal decision tree for what happens if the bFlag interpretation is "quality flag, not b-tag."

**Verification:** DATA_RECONNAISSANCE.md records bFlag={-1, 4} in data (bFlag=-999 in MC). The 94% pass fraction is consistent with a broad quality or selection flag. The experiment log records this as an "open issue" but the strategy does not resolve it with a committed investigation plan.

**Required fix:** Add to COMMITMENTS.md a validation test: "bFlag interpretation check: compute bFlag=4 vs bFlag=-1 b-tag output distributions. If bFlag=4 events have identical b-tag discriminant distribution as the full sample (chi2/ndf consistent with 1.0), classify bFlag as a non-b flag and abandon [D9] BDT training with bFlag labels. In that case, default to self-labelling option 2 as the primary BDT strategy." This gives Phase 3 a concrete decision tree rather than an open investigation.

---

### Category C — Suggestions

---

#### C1. g_bb and g_cc uncertainties in COMMITMENTS.md should cite the specific source used

Section 7.1 now correctly uses the LEP average g_bb = (0.251 +/- 0.063)% with citation (inspire_416138) and g_cc = (2.96 +/- 0.38)% (world average, hep-ex/0302003). COMMITMENTS.md lists the same values. The experiment log notes ALEPH's individual measurement at (0.26 +/- 0.04 +/- 0.09)%.

Suggestion: COMMITMENTS.md should note that the LEP average (not the ALEPH-only value) is being used for g_bb, because this is not self-evident from the values alone. A Phase 4 reviewer who does not read Section 7.1 carefully may assume ALEPH's measurement is used. One sentence in COMMITMENTS.md would suffice: "Using LEP average (0.251 +/- 0.063)% from inspire_416138, not ALEPH-alone (0.26 +/- 0.09)%."

---

#### C2. delta_QCD correction formula in Section 6.4 has a notation inconsistency

Section 6.4 states:
> "A_FB^{0,b} = A_FB^b / (1 - delta_QCD)"

but Section 2.2 gives:
> "A_FB^{0,b} = A_FB^b / (1 - delta_QCD - delta_QED)"

Both appear in the strategy. The difference is whether the QED correction is included in the pole correction formula. This is not a physics error (the QED term delta_QED is small and may be absorbed into the citation of published tables), but the inconsistency will confuse Phase 4 executors implementing the correction. Section 6.4 should either include delta_QED explicitly or state "QED correction from published tables is applied separately; the dominant term is delta_QCD."

---

#### C3. The precision estimate comparison to the competing-group question

From the review methodology (critical_reviewer.md): "Before concluding, answer: if a competing group published a measurement of the same quantity next month, what would they have that we don't?"

Assessment:
- **kappa=infinity delta_b uncertainty:** addressed (kappa=inf now included)
- **eps_c independently calibrated charm control region:** not resolved (B1 above) — published analyses using X tag or D meson reconstruction have a data-derived constraint on eps_c that we don't; our +/- 30% is broader
- **MC truth for hemisphere correlations:** not resolvable without truth labels — legitimate limitation [A1], documented as [L1]
- **Alternative generator comparison:** not resolvable with single MC — legitimate [L1], documented
- **bFlag interpretation resolution:** still open (B3 above) — a competing group would know what their pre-existing tag means

The dominant remaining gap is the eps_c calibration (B1). This is documented as a limitation and the expanded uncertainty (30% relative) compensates for it. No competing group with the same data constraints would do better, so this is not a method gap — it is a data constraint. Acceptable.

---

## Disposition of All Prior Findings

| Prior Item | Resolution | Residual |
|-----------|-----------|----------|
| A1 (closure test tautology) | RESOLVED | None |
| A2 (A_FB^b formula) | PARTIALLY RESOLVED | New A1 (fit implementation ambiguity) |
| A3 (gluon splitting formula) | RESOLVED | None |
| A4 (sigma_d0 sin^{3/2}) | RESOLVED | None |
| A5 (PDG inputs) | RESOLVED | None |
| B1 (eps_c control region) | PARTIALLY RESOLVED | New B1 (30% bound ungrounded) |
| B2 (cos theta binning chi2) | RESOLVED | None |
| B3 (BDT label circularity diagnostic) | RESOLVED | None |
| B4 (g_bb two-component form) | RESOLVED (LEP average used) | C1 (documentation suggestion) |
| B5 (kappa=inf exclusion) | RESOLVED | New B2 (delta_b eval for kappa=inf) |
| C1 (systematic decomposition table) | RESOLVED | Added per-systematic table in Sec 8.2 |
| C2 (bFlag meaning) | PARTIALLY RESOLVED | New B3 (no committed decision tree) |
| C3 (MC sample size REF2) | RESOLVED | Estimate added |
| C4 (competing group gap) | Documented | C3 (summary above) |

---

## Summary

| Category | Count | Items |
|----------|-------|-------|
| A — Must resolve | 2 | A1 (A_FB^b fit implementation ambiguous vs inspire_433746), A2 (experiment log stale on kappa set) |
| B — Should address | 3 | B1 (eps_c 30% ungrounded), B2 (delta_b eval for kappa=inf), B3 (bFlag decision tree not in COMMITMENTS.md) |
| C — Suggestions | 3 | C1 (g_bb source note in COMMITMENTS.md), C2 (delta_QCD notation inconsistency), C3 (competing group summary) |

The strategy is in good shape. The two Category A items are relatively focused:
- A1 requires 1-2 paragraphs clarifying the fit implementation in Section 6.3/[D12]
- A2 requires a 3-line addition to the experiment log

Neither requires structural changes to the strategy. The Category B items require small additions to COMMITMENTS.md and 1-2 sentences in the relevant sections. If the fixer addresses A1 and A2, this strategy should be ready to advance.
