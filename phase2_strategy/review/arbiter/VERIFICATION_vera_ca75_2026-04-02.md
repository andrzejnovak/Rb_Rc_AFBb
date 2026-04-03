# Verification of Fixer Fixes — Phase 2 Strategy

**Verification arbiter:** vera_ca75
**Date:** 2026-04-02
**Fixer session:** felix_d976
**Original arbiter verdict:** STRATEGY_ARBITER_albert_1036_2026-04-02.md
**Artifacts verified:** STRATEGY.md, COMMITMENTS.md, INPUT_INVENTORY.md

---

## Methodology

For each of the 20 findings (7A + 13B), I verified:
- The specific text change in STRATEGY.md
- Consistency across all locations (STRATEGY.md, COMMITMENTS.md, decision labels)
- Correctness of new formulas against cited references
- Completeness of pattern fixes (all instances, not just one)

---

## Category A Findings (7)

### Fix 1: Gluon splitting formula (Finding #1) — **FIXED**

**Evidence:** The incorrect formula `R_b(corrected) = R_b(measured) - g_bb * (eps_g/eps_b)^2` has been removed. Section 10.2 (lines 882-906) now gives the correct treatment: gluon splitting enters through modified double-tag equations via effective uds efficiency:

```
eps_uds(eff) = eps_uds(direct) + g_bb * eps_g
eps_uds^2(eff) = eps_uds^2(direct) + g_bb * eps_g^2
```

This matches the LEP EWWG prescription (hep-ex/0509008 Section 5.4) and inspire_416138 Section 2.2.1, both cited. The g_bb value uses the LEP average 0.251 +/- 0.063% (inspire_416138) rather than the ALEPH-only value. COMMITMENTS.md line 73-75 confirms: "g_bb enters through modified double-tag equations (effective eps_uds), not direct R_b subtraction." Charm gluon splitting (g_cc) is also handled analogously (line 898-900). The formula is physically correct.

### Fix 2: A_FB^b angular-dependent tag efficiency (Finding #2) — **FIXED**

**Evidence:** Section 7.4 (line 614) now includes "Angular dependence of b-tag efficiency" as an explicit systematic source, with description: efficiency varies with |cos(theta)| due to reduced VDET hit coverage at forward angles, changing effective b-purity across the angular range. Mitigation: parameterize eps_b(cos theta) from data using double-tag in angular bins; include in self-calibrating fit. COMMITMENTS.md line 78 includes: "Angular dependence of b-tag efficiency (A_FB^b dominant systematic)." This is present in both the systematic table and the commitments file.

### Fix 3: Closure test redesign (Finding #3) — **FIXED**

**Evidence:** Section 9.1 (lines 731-751) now explicitly states: "A simple MC half-split test is an algebra check, not a closure test" with direct citation to conventions/extraction.md Pitfalls. The tautological test has been replaced with three meaningful alternatives:

(a) Negative-d0 pseudo-data test (R_b should be ~0)
(b) bFlag consistency test (bFlag=4 vs full-sample)
(c) Artificial contamination injection with known shift

COMMITMENTS.md lines 91-93 list all three closure tests as separate commitments. The conventions file's exact language about self-consistent extraction is quoted. The regression trigger identified by the original arbiter (tautological test committed) is resolved.

### Fix 4: A_FB^b formula normalization (Finding #4) — **FIXED**

**Evidence:** Section 4.2 (lines 207-224) now clearly labels the simplified formula as "approximation, valid only for 100% pure b sample" and states "It is NOT the governing extraction method." The governing extraction is designated as the self-calibrating fit (inspire_433746, Section 4), with the full tagged-sample formula given in Section 6.3. COMMITMENTS.md line 164 reads: "[D12] Self-calibrating fit for A_FB^b (governing extraction; report chi2/ndf)." Line 133-134 explicitly states the simple counting method is a "cross-check only." The inconsistency is resolved by clearly separating the two formulas and designating their roles.

### Fix 5: sigma_d0 angular dependence (Finding #5) — **FIXED**

**Evidence:** Section 5.1 (lines 285-298) now uses the correct formula:

```
sigma_d0 = sqrt(A^2 + (B / (p * sin(theta)))^2)
```

with explicit justification: "The sin(theta) dependence (not sin^{3/2}) is the standard form for the Rphi-projected impact parameter d0" (line 288-289). The distinction is documented: sin^{3/2}(theta) applies to 3D impact parameters; since the stored d0 is the Rphi projection, sin(theta) is correct. A systematic "sigma_d0 functional form: vary between sin(theta) and sin^{3/2}(theta)" is committed (lines 296-298, COMMITMENTS.md line 79). The formula also appears correctly in the mitigation section (line 781). Both R_b and A_FB^b propagation are committed.

### Fix 6: PDG inputs (Finding #6) — **FIXED**

**Evidence:** INPUT_INVENTORY.md now shows all previously "NEEDS FETCH" entries as FOUND with values and PDG 2024 citations:

- M_Z = 91.1880 +/- 0.0020 GeV (PDG 2024, node S044M)
- Gamma_Z = 2.4955 +/- 0.0023 GeV (PDG 2024, node S044)
- B+ lifetime = (1.638 +/- 0.004) ps (PDG 2024, node S041)
- B0 lifetime = (1.517 +/- 0.004) ps (PDG 2024, node S042)
- Bs0 lifetime = (1.516 +/- 0.006) ps (PDG 2024, node S086)
- Lambda_b lifetime = (1.468 +/- 0.009) ps (PDG 2024, node S040)
- B meson decay multiplicity = 5.36 +/- 0.01 (CLEO PRD 61 + PDG 2024)

Zero "NEEDS FETCH" entries remain. The Priority for Phase 2 section confirms "PDG values — RESOLVED."

### Fix 7: Primary vertex definition (Finding #7) — **FIXED**

**Evidence:** Decision [D17] added in Section 5.1 (lines 317-331) with detailed treatment. The strategy identifies the ALEPH reference uses per-hemisphere primary vertex (quoting hep-ex/9609005). It documents the "track-in-vertex" problem explicitly. Phase 3 action items are specific: (a) check if d0 changes when event vertex is recomputed excluding the track, (b) if global vertex, either recompute or assign systematic. Implications for both sigma_d0 and C_b are noted. COMMITMENTS.md line 170 lists [D17]. The decision label section (line 1097) includes it. This is not a deferral to Phase 3 without specification — the investigation plan is concrete.

---

## Category B Findings (13)

### Fix 8: Mass tag commitment (Finding #8) — **FIXED**

**Evidence:** [D8] in Section 5.1 (lines 341-347) now reads: "Primary: combined probability-mass tag (P_hem + hemisphere invariant mass cut at 1.8 GeV/c^2, following the ALEPH Q tag in hep-ex/9609005). [D18]." The mass component is explicitly included in Approach A, not just in the BDT. COMMITMENTS.md lines 156 and 171 list [D8] and [D18] accordingly. The ambiguity identified by the arbiter is resolved.

### Fix 9: C_b measurement strategy (Finding #10) — **FIXED**

**Evidence:** Section 7.1 (line 531) now describes a three-pronged C_b determination approach: (a) bFlag=4 proxy as primary — use bFlag=4 in data for hemisphere correlation measurement; (b) geometric/kinematic estimation from full MC corrected for non-b contamination; (c) published value from hep-ex/9609005 Section 7 as validation target with inflated uncertainty. All three options from the reviewer are committed, not just one. The correlation-inducing variables now include y_3 (see Fix 19 below).

### Fix 10: A_FB^b precision estimate derivation (Finding #11) — **FIXED**

**Evidence:** Section 8.3 (lines 677-696) now shows the full derivation. The simple counting estimate gives sigma ~ 0.0075 (consistent with the reviewer's ~0.0065 order-of-magnitude). The self-calibrating fit improvement is estimated by scaling the published ALEPH result. The final range is updated to 0.005-0.007 (stat), wider than the original 0.004-0.005. The resolving power text uses "the conservative end of this range."

### Fix 11: Thrust axis sign convention (Finding #12) — **FIXED**

**Evidence:** Section 6.1 (lines 442-450) now includes an explicit paragraph: "Forward" is defined as the hemisphere with cos(theta_thrust) > 0, i.e., the positive z-axis = electron beam direction at LEP. The strategy commits to verifying the coordinate convention at Phase 3 by checking the 1 + cos^2(theta) shape symmetry. The fallback ("If the beam direction is not recoverable, A_FB^b cannot be measured") is stated.

### Fix 12: R_c impact on R_b quantified (Finding #9) — **FIXED**

**Evidence:** Section 4.3 (lines 256-261) now includes the sensitivity calculation: dR_b/dR_c ~ -eps_c/eps_b ~ -0.05, giving delta(R_b) = 0.05 * 0.0030 ~ 0.00015, confirmed small compared to total ~0.0015-0.0020. The cite is inspire_416138 Eq. 1-2. COMMITMENTS.md [D6] includes the sensitivity estimate.

### Fix 13: eps_c control region justification (Finding #13) — **FIXED**

**Evidence:** Section 7.2 (lines 589-601) now provides a concrete justification: charm control region would require D meson reconstruction (needs PID, unavailable [A5]) or a soft lifetime cut that produces b-dominated rather than charm-pure samples. The multi-working-point scan provides indirect constraint. The uncertainty range is specified concretely: eps_c assigned +/- 30% relative uncertainty (covering ~10% MC statistical and data-MC modelling difference), corresponding to absolute ~0.002-0.005 on eps_c.

### Fix 14: cos(theta) binning chi2/ndf (Finding #14) — **FIXED**

**Evidence:** [D12] in Section 6.3 (lines 491-497) now commits to: "Report chi2/ndf of the angular fit at each configuration (bin count, kappa value, working point). Perform a bin-count scan (6, 8, 10, 12 bins) to verify stability." COMMITMENTS.md line 164 includes "report chi2/ndf." This satisfies conventions/extraction.md validation check 3.

### Fix 15: BDT label contamination diagnostic (Finding #15) — **FIXED**

**Evidence:** Section 5.2 (lines 391-395) now includes the specific diagnostic: "If the BDT working point scan shows a slope > 1-sigma/range while the cut-based scan is flat, this is evidence of label contamination." The action on detection is specified: "Document slope magnitude and significance. If slope is detected, revert to cut-based as primary."

### Fix 16: kappa = infinity (Finding #17) — **FIXED**

**Evidence:** [D5] in Section 4.2 (lines 192-199) now reads: "kappa = {0.3, 0.5, 1.0, 2.0, infinity}" with the correction: "kappa = infinity (leading particle charge — the charge of the highest-momentum track in the hemisphere) does NOT require particle identification; PID improves it but is not required." The incorrect justification for excluding it has been removed. All downstream references (REF3, decision labels) include infinity.

### Fix 17: R_c cross-check sensitivity (Finding #18) — **FIXED**

**Evidence:** Section 4.3 (lines 248-253) now includes: "Estimated R_c sensitivity from cross-check: with ~56k double-tagged events and eps_c/eps_b ~ 0.05, the statistical precision on a floated R_c is ~0.004-0.007 (from inspire_416138 scaling). This is comparable to the LEP combined uncertainty and sufficient to detect a large deviation from SM." This prevents the cross-check from being silently dropped.

### Fix 18: Year-dependent angular binning (Finding #19) — **FIXED**

**Evidence:** [D12a] added in Section 6.3 (lines 499-503): "Angular binning uniformity across years. Given the VDET change between 1993 and 1994, per-year angular acceptance may differ. Use the same binning for all years but verify per-year fit quality (chi2/ndf). If any year shows chi2/ndf > 2.0, investigate year-specific angular effects." COMMITMENTS.md line 165 lists [D12a].

### Fix 19: y_3 in hemisphere correlation check (Finding #20) — **FIXED**

**Evidence:** Section 7.1 (line 531) now lists four correlation-inducing variables: "(1) cos(theta), (2) primary vertex error, (3) jet momentum, (4) y_3" with the description: "gluon radiation variable, from ktN2 jet tree — the Durham jet resolution at which 3->2 jets occurs; following hep-ex/9609005 Section 7 which uses four variables including y_3." This matches the ALEPH reference.

### Fix 20: A_FB^b kappa comparison figure (Finding #21) — **FIXED**

**Evidence:** Section 12 (lines 1006-1009) now includes flagship figure F7: "A_FB^b kappa consistency. A_FB^b extracted at each kappa value {0.3, 0.5, 1.0, 2.0, infinity}, plotted with combined result and chi2/ndf." COMMITMENTS.md line 119 lists F7. [D15] references "plus F7 kappa comparison."

---

## Summary

| # | Finding | Category | Verdict |
|---|---------|----------|---------|
| 1 | Gluon splitting formula | A | **FIXED** |
| 2 | Angular-dependent tag efficiency | A | **FIXED** |
| 3 | Closure test redesign | A | **FIXED** |
| 4 | A_FB^b formula normalization | A | **FIXED** |
| 5 | sigma_d0 angular dependence | A | **FIXED** |
| 6 | PDG inputs | A | **FIXED** |
| 7 | Primary vertex definition | A | **FIXED** |
| 8 | Mass tag commitment | B | **FIXED** |
| 9 | C_b measurement strategy | B | **FIXED** |
| 10 | A_FB^b precision estimate | B | **FIXED** |
| 11 | Thrust axis sign convention | B | **FIXED** |
| 12 | R_c impact on R_b | B | **FIXED** |
| 13 | eps_c control region | B | **FIXED** |
| 14 | cos(theta) chi2/ndf | B | **FIXED** |
| 15 | BDT label diagnostic | B | **FIXED** |
| 16 | kappa = infinity | B | **FIXED** |
| 17 | R_c cross-check sensitivity | B | **FIXED** |
| 18 | Year-dependent binning | B | **FIXED** |
| 19 | y_3 correlation variable | B | **FIXED** |
| 20 | Kappa comparison figure | B | **FIXED** |

**Result: 20/20 FIXED.**

---

## Verification Verdict: ALL FIXED

All 7 Category A and 13 Category B findings have been genuinely resolved. The fixes are substantive, not surface-level:

- Formulas are physically correct (gluon splitting through modified double-tag equations, sigma_d0 with sin(theta) for Rphi d0, A_FB normalization hierarchy)
- Pattern fixes appear in all required locations (STRATEGY.md systematic tables, COMMITMENTS.md, decision labels)
- PDG values have actual numbers with PDG 2024 citations
- New commitments (closure tests, diagnostics, figures) are specific and actionable

**The strategy is ready for a fresh full review.**

One observation for the fresh review panel: the fixer also applied several Category C improvements (bFlag=4 interpretation note in Section 9.6, stability scan vs bias distinction in Section 5.1, supporting figures in Section 12). These should be checked for correctness during the full review but do not require re-verification here.
