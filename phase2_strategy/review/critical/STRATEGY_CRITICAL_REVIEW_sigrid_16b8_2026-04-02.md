# Critical Review — Phase 2 Strategy
**Reviewer session:** sigrid_16b8  
**Date:** 2026-04-02  
**Artifact:** `phase2_strategy/outputs/STRATEGY.md` (peter_b030, 2026-04-02)  
**Upstream:** DATA_RECONNAISSANCE.md, INPUT_INVENTORY.md, LITERATURE_SURVEY.md  
**Conventions:** `conventions/extraction.md`  
**Review focus:** §6.4 Phase 2  
**MCP_LEP_CORPUS:** true — corpus queries executed

---

## Checklist of Items Examined

| Item | Status | Evidence |
|------|--------|----------|
| Phase 1 findings used | PASS (with gaps, see A1) | Constraint labels [A1-A6] cited; branch availability grounded in recon |
| Observable definitions verified | PARTIAL (see A2, A3) | R_b and R_c verified; A_FB^b formula has issues |
| Backgrounds classified | PASS | Section 10 with type, fraction, treatment |
| Systematic plan covers extraction.md row-by-row | PARTIAL (see B1, B2) | Most covered; two gaps identified |
| MC coverage respected | PASS | Section 7 explicitly limits systematics to 1994; [L1] propagated |
| Reference analyses tabulated | PASS | 5 references with numerical values in Sec. 11 |
| ≥2 qualitatively different selection approaches | PASS | Cut-based (5.1) and BDT (5.2) — qualitatively different |
| MVA considered | PASS | BDT Approach B with three proxy-label strategies |
| Method parity with published | PARTIAL (see B3) | 5-tag acknowledged; multi-WP mitigation proposed; one gap |
| Mitigation for every Phase 1 constraint | PARTIAL (see A4) | [A1–A6] covered; [A3] mitigation internally inconsistent |
| Precision estimates grounded | PASS | Computed from double-tag formula with refs |
| COMMITMENTS.md populated | PASS | All 16 decisions + systematics + figures + cross-checks |
| Corpus queries executed | PASS | 8 queries documented in experiment_log; results cited |
| Flagship figures defined | PASS | 6 figures in Section 12 |
| Correction strategy defined | PASS | Section 13 |
| Theory comparison independence | PASS | SM predictions from hep-ex/0509008 cited; no circularity visible |

---

## Findings

### Category A — Must Resolve

---

#### A1. Closure test is structurally tautological given the single MC sample

**Finding:** COMMITMENTS.md (validation tests) commits to: "Independent closure test: extract R_b from independent MC split (derivation vs validation halves, fixed seed). Pull < 2 sigma."

The strategy also commits to deriving eps_c, eps_uds, C_b, C_c, C_uds from MC (Section 4.1, Section 7.1). If the same MC sample is split in half, and one half is used to derive efficiencies while the other supplies the yield counts N_t and N_tt, the closure test recovers the correct answer **by construction** for the following reason: in a double-tag extraction, R_b is the only unknown that is genuinely extracted from data; the efficiencies eps_c and eps_uds are taken from MC and substituted directly into the formula. When the "validation" half is also MC — with the same generator, same fragmentation parameters, same detector model — the "independent" test has no resolving power. Any bias in the efficiency model (e.g., wrong eps_c) cancels identically in both halves.

`conventions/extraction.md` (Pitfalls section) states explicitly: "A self-consistent extraction (deriving efficiencies and counting yields from the same sample) always recovers the correct answer by construction — this is an algebra check, not a closure test. If a closure test produces pull = 0.00 at every operating point, this is a red flag that it is self-consistent rather than independent."

**The strategy does not identify this risk or propose any mitigation.** Phase 3 will implement this test and will almost certainly observe pull ≈ 0 across all working points, which the executor may interpret as "excellent closure." That is the opposite of what it means.

**Required fix:** The strategy must define what a meaningful closure test looks like given the single MC sample. Options: (a) use the negative-d0 tail data to define a "resolution-only" pseudo-sample and test that the extraction gives R_b = 0 (expected for zero lifetime signal); (b) use the bFlag=4 vs bFlag=-1 split as a proxy signal/background split and verify the tagger does not artificially inflate or deflate double-tag rates; (c) inject a known artificial contamination into the MC-derived efficiency parameters and verify the resulting R_b shift matches analytical expectation. The COMMITMENTS.md closure test description must be rewritten to be operationally meaningful.

---

#### A2. A_FB^b observable formula does not follow cited source — normalization inconsistency

**Finding:** STRATEGY.md Section 2.2 gives the A_FB^b extraction formula (Section 6.3) as:

```
<Q_FB>(cos theta) = sum_q f_q * delta_q * A_FB^q * cos(theta)
```

and also states (Section 4.2, literature survey):

```
A_FB^b = (8/3) * <Q_FB> / (R_b * delta_b)
```

These two forms are inconsistent as written. The second formula (from LITERATURE_SURVEY.md, cited as from inspire_433746 and inspire_342763) gives A_FB^b as proportional to the inclusive <Q_FB>, normalized by R_b * delta_b. The first formula (Section 6.3) gives <Q_FB> as a sum over flavour fractions f_q, making it the observed charge asymmetry in the tagged sample — not the inclusive hadronic sample.

The corpus confirms that inspire_433746 (Section 3, Principles of the Method) uses the self-calibrating fit to the five event categories (N, N_bar, N^D, N^D_bar, N^same) in bins of polar angle. The formula A_FB^b = (8/3) * <Q_FB> / (R_b * delta_b) is a **simplified approximation** valid only for a 100% pure b sample. In reality, the correct extraction accounts for the b purity f_b in the tagged sample, which varies with the b-tag working point.

**Specific issue:** The simplified formula in the LITERATURE_SURVEY.md is:

```
A_FB^b = (8/3) * <Q_FB> / (R_b * delta_b)
```

This formula has normalization R_b in the denominator, but <Q_FB> in the numerator is for the **inclusive hadronic sample**. If <Q_FB> is measured in the **b-tagged sample** (as it must be in practice), the denominator should be f_b * R_b * delta_b, where f_b is the b purity. As the DELPHI papers (inspire_1661115, inspire_1661252) make clear, the correct extraction uses the full self-calibrating fit to the polar-angle-binned event rates, not this simplified formula.

**Required fix:** Section 4.2 and Section 6.3 must state clearly which formula governs the primary extraction (the self-calibrating fit to polar-angle-binned event categories, following inspire_433746 Section 4) and which formula is the approximation used for illustration. The simplified formula must be explicitly labeled as approximate and should not appear in COMMITMENTS.md as if it is the extraction formula. Failing to resolve this ambiguity will cause the Phase 4 executor to implement the wrong formula.

---

#### A3. Gluon splitting correction formula for R_b is wrong as written

**Finding:** Section 10.2 states the gluon splitting correction as:

```
R_b(corrected) = R_b(measured) - g_bb * (eps_g / eps_b)^2
```

This formula is not dimensionally or physically correct as a stand-alone expression. The gluon splitting correction to the double-tag extraction is a correction to the double-tag **fraction** f_d, not directly to R_b. The full correction is:

```
f_d(corrected) = f_d(observed) - g_bb * eps_g^2
```

and then R_b is re-extracted from the corrected f_d. Alternatively, the correction enters through the modified extraction formula where the gluon-splitting contribution is subtracted from N_tt before computing f_d. The factor (eps_g / eps_b)^2 does not directly appear in R_b without the full derivation connecting it to N_tt / N_had.

The LEP EWWG prescription (hep-ex/0509008, Section 5.4) and the DELPHI analysis (inspire_1660341, Section 4.4) define the correction through the modified double-tag formula, not through a simple subtraction from R_b. The corpus corpus search on "R_b extraction gluon splitting correction formula" confirms the corrections enter through the double-tag formula, not through direct R_b subtraction.

**Required fix:** Replace the ad hoc formula with the correct correction through the double-tag formula. Cite hep-ex/0509008 Section 5.4 for the exact prescription. The COMMITMENTS.md "Gluon splitting: vary g_bb" systematic should specify that g_bb enters through the corrected double-tag formula, not through a direct subtraction.

---

#### A4. sigma_d0 parameterization: sin^{3/2}(theta) vs sin^{3/2}(theta) — momentum dependence is inconsistent with ALEPH source

**Finding:** Section 5.1 (and 9.3) gives the sigma_d0 parameterization as:

```
sigma_d0 = sqrt(A^2 + (B / (p * sin^{3/2}(theta)))^2)
```

The citation for A ~ 25 micron, B ~ 70 micron*GeV/c is given as "537303, Section: Preamble." However, the ALEPH VDET performance paper and the ALEPH b-tagging methodology (as found in the corpus under hep-ex/9609005 and inspire_433306) parameterize the transverse impact parameter resolution in the Rφ plane as:

```
sigma(d0) = A ⊕ B/p
```

where the angular dependence is **sin(theta)**, not sin^{3/2}(theta). The sin^{3/2}(theta) dependence is the correct form for the **3D** impact parameter (the distance of closest approach in 3D space), which includes projection effects. However, the d0 branch in the data (as confirmed by DATA_RECONNAISSANCE.md) is the **2D** Rφ impact parameter, for which the angular dependence of the multiple-scattering term is B/(p sin(theta)), not B/(p sin^{3/2}(theta)).

The DELPHI papers on resolution tuning (inspire_1661709, inspire_1660379) confirm the standard parameterization for the Rφ projection is B/p with angular factors through cot(theta), not sin^{3/2}(theta). The sin^{3/2}(theta) form arises when projecting a 3D resolution into the Rφ plane for tracks measured in the forward region — it is not the standard d0 parameterization.

**This is consequential:** if sigma_d0 is overestimated for forward tracks (small sin(theta), where sin^{3/2}(theta) << sin(theta)), the impact parameter significance S = d0/sigma_d0 will be underestimated for those tracks, reducing b-tag efficiency for forward b-hadrons and biasing the angular distribution of the tagged sample — directly affecting A_FB^b.

**Required fix:** Verify the functional form against the actual ALEPH tracking paper (537303). If the d0 branch is Rφ only, use B/(p sin(theta)). If it is a 3D quantity, justify sin^{3/2}(theta) with an explicit derivation. Add this as a systematic source: "sigma_d0 parameterization functional form" — vary between sin(theta) and sin^{3/2}(theta) and propagate to R_b and A_FB^b.

---

#### A5. No PDG inputs fetched for mandatory numerical inputs — COMMITMENTS.md lists "NEEDS FETCH" items with no resolution

**Finding:** INPUT_INVENTORY.md lists M_Z, Gamma_Z, B hadron lifetimes, and B hadron decay multiplicities as "NEEDS FETCH" from PDG live tables. STRATEGY.md uses these quantities implicitly (e.g., B physics systematic in Section 7.1 commits to "Vary B hadron lifetimes, decay multiplicities, b fragmentation <x_E> within PDG uncertainties"), but no actual PDG values are cited with URLs or paper references.

CLAUDE.md (Numeric Constants) states explicitly: "Every number that enters the analysis must come from a citable source. PDG masses, widths, coupling constants, world-average measurements, QCD coefficients, radiative correction formulae — all must be fetched from the RAG corpus, web, or a cited paper. LLM training data is NOT a source. At review, any uncited numeric constant is Category A."

The strategy commits to using these quantities in Phase 4 systematic evaluation (B hadron lifetimes, decay multiplicities) but does not provide the values. This means Phase 3/4 executors will either re-derive them (violating the numeric constants policy) or invent them from training knowledge.

**Required fix:** Before review can pass, the strategy must include a resolved input table entry for M_Z, Gamma_Z, B hadron lifetime averages, and B meson decay multiplicities. These should be fetched from the PDG 2024 Review of Particle Physics (doi:10.1093/ptep/ptac097 or equivalent). The fetch does not need to happen in the strategy document itself, but the COMMITMENTS.md "NEEDS FETCH" entries must be resolved with actual values and citations before the strategy is considered complete.

---

### Category B — Should Address

---

#### B1. Missing systematic source from extraction.md: data-derived calibration scale factors

**Finding:** `conventions/extraction.md` Standard Configuration (6th bullet) states: "When the extraction depends on MC-derived efficiencies (e.g., tagging efficiency), derive data/MC scale factors from a control sample using tag-and-probe or similar methods. Apply these scale factors to the MC before extraction. If data-derived calibration is not feasible, assign the full data/MC difference as a systematic — but document why calibration was not done. Relying on uncalibrated MC efficiencies without justification is Category A."

The systematic plan in Section 7.1 treats eps_c and eps_uds as MC-derived parameters with "inflated systematic covering the data-implied range." It does not specify what "data-implied range" means or how it is derived without truth labels. Without a data-driven calibration or a documented control sample that constrains eps_c and eps_uds independently, the uncertainty assignment is unconstrained.

**Issue:** The strategy does not propose a control region for eps_c. The ALEPH reference analysis (hep-ex/9609005) uses the X tag (charm tag) and the charm-enriched tag regions to constrain eps_c from data. We lack these. But there is no documented analysis of whether a loose lifetime tag (c hadrons have lifetimes ~0.5 ps vs b hadrons ~1.5 ps — a factor of 3, leading to smaller but nonzero d0 displacement) could be used as a charm-enriched control region to constrain eps_c empirically. The strategy mentions "Float R_c in extended fit" as a cross-check [D6] but does not use this to bound eps_c.

**Required fix:** Document explicitly why a charm-enriched control region is not feasible (or demonstrate it is feasible and plan to implement it). If not feasible, document the specific argument and state that the eps_c uncertainty will be inflated conservatively by X%, citing a comparison to what hep-ex/9609005 achieved. The phrase "inflated systematic covering the data-implied range" is operationally empty without specifying the range.

---

#### B2. Missing sensitivity analysis for the number of cos(theta) bins in A_FB^b

**Finding:** Section 6.3 / [D12] states "Fit A_FB^b in bins of |cos(theta_thrust)| using the self-calibrating method. Use 8-10 uniform bins in |cos(theta)|." No justification is given for uniform binning or for 8-10 bins specifically.

The review checklist (critical_reviewer.md, BINNING CHECK) requires: "Is the binning physics-motivated or just uniform? For observables with regions of varying physical interest (endpoints, peaks, tails), uniform binning wastes resolution where it matters and oversamples where it doesn't."

For the A_FB^b measurement, the statistical sensitivity to the cos(theta)-linear term scales as the variance of cos(theta) in each bin, which is uniform across bins for uniform binning in cos(theta). However, near |cos(theta)| = 1 (forward/backward), the signal fraction changes rapidly and the b-tag efficiency drops (as confirmed by DELPHI papers: inspire_1661252 Figure 10 shows b efficiency falling sharply at large |cos(theta)|). Published analyses address this by checking the chi2/ndf of the linear fit.

The strategy commits to "Compare to a simple counting method (N_F - N_B) / (N_F + N_B) as cross-check" but does not commit to scanning the number of bins or verifying chi2/ndf of the angular fit. The extraction.md pitfall on operating point stability requires: "Report chi2/ndf at each scan point alongside the extracted value."

**Required fix:** Add a commitment to report chi2/ndf of the cos(theta) linear fit. Justify the choice of 8-10 uniform bins or add a scan of N_bins as part of the stability check. Given that the angular efficiency is not uniform (LITERATURE_SURVEY.md: angular acceptance |cos theta| < 0.9), consider efficiency-corrected binning or at minimum verify the angular efficiency correction does not bias the fit in the extreme bins.

---

#### B3. BDT training with bFlag proxy labels: the circularity risk is underspecified

**Finding:** Decision [D9] / [D10] proposes training a BDT with bFlag = 4 as signal and bFlag = -1 as background. The strategy acknowledges "contamination of non-b events in bFlag = 4 biases the training labels, but the double-tag method's self-calibrating property absorbs this bias into the measured efficiency."

This argument is incomplete. The double-tag method's self-calibrating property **does** absorb the overall efficiency bias — but it does not absorb **shape** biases in the BDT discriminant. If the BDT is trained with bFlag as labels and bFlag carries non-b contamination distributed differently across the discriminant (e.g., high-multiplicity uds events passing bFlag = 4), the discriminant shape in data will differ from a truth-label-trained discriminant. When the operating point is scanned, the eps_b vs purity curve will reflect this contamination, and the extracted R_b vs working point will show a slope rather than a flat plateau.

The strategy (correctly) plans the operating point stability scan as a cross-check. But it does not explicitly commit to investigating this slope as evidence of BDT training label contamination, rather than simply discarding the BDT in favor of the cut-based approach. The distinction matters: a sloping R_b vs working point scan when using the BDT (but not the cut-based approach) is diagnostic of bFlag label contamination, and should be documented as such rather than treated as a reason to prefer the cut-based approach without discussion.

**Required fix:** Add to [D10] a specific diagnostic: if the BDT working point scan shows a slope > (1 sigma / scan range) while the cut-based scan is flat, document this as evidence of bFlag label contamination and record the magnitude of the slope as a systematic bound. This turns a failure mode into a measurement of the bFlag contamination.

---

#### B4. The g_bb uncertainty quoted is internally inconsistent between COMMITMENTS.md and STRATEGY.md

**Finding:** STRATEGY.md Section 7.1 (Gluon splitting) states:
"Vary g_bb = (0.26 +/- 0.10)% and g_cc = (3.26 +/- 0.48)%"

COMMITMENTS.md lists the same:
"Gluon splitting: vary g_bb = (0.26 +/- 0.10)%, g_cc = (3.26 +/- 0.48)%"

The g_bb uncertainty here is **+/- 0.10%**, but the strategy Section 7.1 body text in the sample composition table lists g_bb = "(0.26 +/- 0.10)%." However, the corpus search on "g_bb measurement gluon splitting" found: hep-ex/9811047 (ALEPH) gives g_bb = "(0.26 +/- 0.04 +/- 0.09)%," and DELPHI (inspire_1661963) gives g_bb = "(0.22 +/- 0.10 +/- 0.08)%." The LEP combined value from hep-ex/0509008 is g_bb = "(0.29 +/- 0.06)%."

The strategy is using the ALEPH measurement value 0.26 with total uncertainty +/- 0.10% (combining statistical and systematic in quadrature: sqrt(0.04^2 + 0.09^2) ≈ 0.098). This is acceptable. However, the INPUT_INVENTORY.md lists g_bb from hep-ex/9811047 as "(0.26 +/- 0.04 +/- 0.09)%" — the two-component uncertainty form — which when combined gives ≈ +/-0.10% total. The COMMITMENTS.md compact form "+/- 0.10%" is consistent with this, but it should be written as "+/- 0.04 (stat) +/- 0.09 (syst)" to be traceable. The single-number form loses the decomposition needed when combining experiments.

**Required fix:** Write the g_bb and g_cc uncertainties in the two-component form in both STRATEGY.md and COMMITMENTS.md, with citations to the specific measurement used. Use the LEP combined value (hep-ex/0509008: g_bb = 0.29 +/- 0.06%) as the primary input rather than the single-experiment ALEPH value, to ensure consistency with the reference analyses.

---

#### B5. kappa = infinity (leading particle charge) exclusion is under-justified

**Finding:** Section 4.2 [D5] states: "kappa = infinity (leading particle charge) is not used because it requires particle identification for optimal performance."

The corpus confirms (hep-ex/9609005 Section: Five Hemisphere Tags) that the ALEPH reference analysis (inspire_433746) uses kappa = {0.3, 0.5, 1.0, 2.0, infinity}. The LITERATURE_SURVEY.md confirms: "Multiple kappa values provide redundancy: kappa = infinity (leading particle charge) is not used because it requires particle identification."

However, kappa = infinity in the jet charge formula gives weight only to the highest-momentum track. This does **not** require particle identification — it requires identifying which track has the highest longitudinal momentum, which is available from the px/py/pz branches. The leading track's charge (which is the integer {-1, 0, +1} from the charge[] branch) is available without PID.

The actual reason kappa = infinity may not be optimal without PID is that the leading particle in a b-hadron hemisphere is sometimes a neutral particle (B meson → pi0, etc.) or a misidentified track, and PID helps identify the true charge carrier. But this is a systematic issue, not a feasibility issue. The strategy frames it as "requires PID" but should frame it as "reduced performance without PID."

**Required fix:** Correct the justification in [D5]. kappa = infinity is feasible without PID; it may have reduced charge separation power (delta_b for kappa=inf will be smaller without PID to veto neutral-dominated events). Include kappa = infinity as an additional working point and measure its delta_b — the comparison with the PID-assisted value from inspire_433746 is itself a systematic cross-check on charge separation performance.

---

### Category C — Suggestions

---

#### C1. Precision estimate (Section 8.2) borrows ALEPH's systematic program without adjustment

The systematic precision estimate of sigma(R_b)_syst ~ 0.0015-0.0020 is described as "1.5-2x larger than published." This is stated without a systematic-by-systematic decomposition. A table showing which systematics are expected to be larger (e.g., MC model dependence due to single sample), which are smaller (e.g., no lepton/kaon tag backgrounds), and which are unchanged would improve transparency and give Phase 4a reviewers a concrete benchmark.

#### C2. The "bFlag = 4 ~ 94% of events" observation needs a decision

The strategy notes bFlag = 4 as a pre-existing b-tag for 94% of events and proposes it as a training label proxy and as a cross-check. However, it does not commit to investigating what bFlag = 4 actually means — is it a geometric acceptance flag, a b-tag from the ALEPH software, or something else? Since 94% is too high to be a b-tag (R_b ~ 21%), bFlag = 4 almost certainly means something other than "b-tagged event." It likely represents a quality or hadronic-event flag. The strategy should commit to resolving this interpretation in Phase 3 before using bFlag as a training label.

#### C3. Reference REF2 (inspire_433306) is missing the dataset size

COMMITMENTS.md REF2 states "MC sample size: Full ALEPH MC production" — the same for REF1. The phase 2 CLAUDE.md requires "MC sample size" for each reference. The convention is to provide a number or acknowledge it was not reported in the paper. "Full ALEPH MC production" is not a number. An estimate ("~10M events based on LEP luminosity × factor of 3-4 MC oversampling typical of ALEPH, consistent with REF1 estimate") would be more useful.

#### C4. The "competing group next month" test

Answering §6.3 question 3: What would a competing group publishing next month have that we don't?
- kappa = infinity (leading particle charge) for A_FB^b — see B5 above
- Properly calibrated eps_c control region — see B1 above  
- Alternative fragmentation model (HERWIG vs PYTHIA) — acknowledged as [L1] but no attempt to even obtain HERWIG predictions from published papers as cross-check inputs
- bFlag interpretation — unknown

The dominant gap is the eps_c constraint, which published analyses (hep-ex/9609005) addressed through the X tag. Our mitigation (constrain R_c to SM) handles the R_c uncertainty but not the eps_c uncertainty independently. This is documented as a limitation, which is appropriate, but it should appear explicitly in the precision comparison in Section 8.

---

## Summary of Findings

| Category | Count | Items |
|----------|-------|-------|
| A — Must resolve | 5 | A1 (closure test tautology), A2 (A_FB formula inconsistency), A3 (g_bb correction formula), A4 (sigma_d0 sin^{3/2} form), A5 (PDG inputs not fetched) |
| B — Should address | 5 | B1 (eps_c control region), B2 (cos theta binning chi2), B3 (BDT label circularity diagnostic), B4 (g_bb two-component uncertainty form), B5 (kappa=inf exclusion misstated) |
| C — Suggestions | 4 | C1 (systematic decomposition), C2 (bFlag meaning), C3 (MC sample size REF2), C4 (competing group gap) |

**Assessment:** The strategy is substantially complete and represents serious engagement with the constraints. The reference analysis table is well-populated, the systematic plan is comprehensive, the mitigation strategies are thoughtful, and the observable definitions are mostly correct. However, five issues require resolution before Phase 3 can begin with confidence:

1. The closure test as described will produce a trivially passing result (pull ≈ 0) by algebraic construction — this must be redesigned.
2. The A_FB^b extraction formula is stated in two inconsistent forms; the correct self-calibrating fit framework must be unambiguously committed.
3. The gluon splitting correction formula is not physically correct as written.
4. The sigma_d0 angular dependence may be wrong (sin^{3/2} vs sin) with direct impact on A_FB^b.
5. Several mandatory numerical inputs remain in "NEEDS FETCH" status with no resolution.

Items B1–B5 represent methodological gaps that will become Category A at Phase 3 or Phase 4a review if not addressed in the strategy revision.

---

## RAG Evidence Summary

The following corpus queries were used to verify claims in STRATEGY.md:

| Query | Key Finding |
|-------|-------------|
| Double tag method formalism, epsilon_b, C_b | Confirmed formula in hep-ex/9609005 Section "The Method" — consistent with STRATEGY.md Section 4.1 |
| Hemisphere jet charge kappa, delta_b | Confirmed kappa formulation; DELPHI papers confirm self-calibrating fit to 5 event categories, NOT simple Q_FB formula |
| QCD correction A_FB delta_QCD | Confirmed delta_QCD ~ +3-4% for jet charge analysis (inspire_1631399); STRATEGY.md value 0.0356 is consistent |
| Impact parameter significance negative tail resolution | DELPHI tuning papers confirm parameterization sigma = A ⊕ B/p with angular dependence in Rz but standard form in Rphi — inconsistency with sin^{3/2} noted |
| Gluon splitting rates | Confirmed g_cc = (3.26 +/- 0.48)% from hep-ex/0302003; g_bb from hep-ex/9811047; values in strategy consistent |
| A_FB extraction formula Q_FB | DELPHI papers confirm self-calibrating chi2 fit to N, N_bar, N^D, N^D_bar, N^same — NOT the simplified formula A_FB = (8/3)<Q_FB>/(R_b*delta_b) which appears in LITERATURE_SURVEY.md |
| ALEPH R_b B hadron fragmentation systematic | Confirmed reweighting approach for fragmentation, consistent with strategy plan |
