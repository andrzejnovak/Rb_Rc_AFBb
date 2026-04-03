# Verification — Iteration 2 Arbiter Findings

Verifier: vera2_25a0 | Date: 2026-04-02

Source: STRATEGY_ARBITER_oscar_cfd3_2026-04-02.md (1A + 4B)

---

## Finding #1 (Category A): A_FB^b fit formulation ambiguity

**Arbiter requirement:** Section 6.3 must commit to a specific fit
implementation with [D] label. Five-category chi2 or four-quantity fit
must be explicitly specified. sin^2(theta_eff) extraction path must be
clear.

**Evidence:**

- STRATEGY.md line 532: `[D12b]` label present, specifying "four-quantity
  simultaneous fit (following inspire_433746, Section 4)"
- Lines 537-540: Four quantities explicitly defined (Q_FB, delta, e^h,
  epsilon^e)
- Lines 545-547: Three fit parameters defined (delta_b, epsilon^h_b,
  sin^2(theta_eff))
- Lines 557-570: sin^2(theta_eff) extraction path fully specified as a
  direct fit parameter, with A_FB^{0,b} derived via A_e assuming lepton
  universality. Formula given. ALEPH reference cited.
- Lines 572-581: DELPHI five-category chi2 fit documented as cross-check
  alternative
- COMMITMENTS.md line 177: `[D12b]` recorded with four-quantity fit and
  DELPHI cross-check

**Verdict: FIXED.** The fit formulation is unambiguous: four-quantity
simultaneous fit with sin^2(theta_eff) as direct parameter, DELPHI
five-category as cross-check. All arbiter requirements met.

---

## Finding #3 (Category B): d0 sign convention validation gate

**Arbiter requirement:** Explicit [D]-labelled decision committing to d0
sign validation as a Phase 3 blocking gate. Must appear in COMMITMENTS.md.

**Evidence:**

- STRATEGY.md lines 329-338: `[D19]` label present. Text: "Phase 3 gate:
  d0 sign convention validation. Before proceeding with tagger
  construction, verify the d0 sign convention by plotting the d0
  distribution in b-enriched hemispheres." Explicitly states this is a
  "blocking gate — no tagger construction proceeds until the d0 sign is
  validated."
- COMMITMENTS.md line 113: `d0 sign convention validation [D19]: positive
  d0 tail enhanced in b-enriched hemispheres (Phase 3 blocking gate)`
- COMMITMENTS.md line 185: `[D19]` in Key Decisions list

**Verdict: FIXED.** The d0 sign validation is a [D]-labelled blocking
gate with specific pass/fail criteria and remediation path, committed in
both STRATEGY.md and COMMITMENTS.md.

---

## Finding #4 (Category B): C_b published values and inflation factor

**Arbiter requirement:** Section 7.1 C_b row must add: specific published
C_b value from hep-ex/9609005, the inflation factor, and whether C_b is
varied as single number or decomposed.

**Evidence:**

- STRATEGY.md line 621 (C_b row): States "adopt a baseline C_b from the
  published ALEPH Q-tag self-correlation, inflated by a factor of 2x."
  Assigns delta(R_b) from C_b = 0.00100 (2x the published 0.00050).
  States "C_b is varied as a single multiplicative factor (not decomposed
  by source)." Cites hep-ex/9609005. Lists four correlation-inducing
  variables with combination method (linear, not in quadrature).

**Verdict: FIXED.** All three required elements present: published value
(0.00050), inflation factor (2x), and variation method (single
multiplicative factor).

---

## Finding #7 (Category B): eps_c 30% relative uncertainty grounding

**Arbiter requirement:** Ground the 30% figure using concrete evidence
(spread across published working points, LEP data/MC ratios, or published
eps_c spread).

**Evidence:**

- STRATEGY.md lines 687-702: "Concrete uncertainty range: eps_c is
  assigned +/- 30% relative uncertainty, grounded in the following:"
  Three sources cited: (i) ALEPH Q-tag charm efficiency variation of
  ~2-3x across working points (hep-ex/9609005), (ii) spread of published
  charm efficiencies across LEP experiments ~20-40% (inspire_416138,
  Section 3.5), (iii) MC statistical uncertainty ~10% from no-truth-label
  contamination subtraction. "The 30% covers the envelope of these three
  sources."

**Verdict: FIXED.** The 30% is grounded in three concrete, cited sources
rather than asserted. The envelope argument is reasonable.

---

## Finding #8 (Category B): kappa=infinity delta_b threshold

**Arbiter requirement:** Add threshold for demotion to cross-check only
(e.g., delta_b < 0.1).

**Evidence:**

- STRATEGY.md lines 201-209: "If the fitted charge separation
  delta_b(kappa = infinity) < 0.1 (less than half the typical delta_b ~
  0.20-0.25 for lower kappa values), use kappa = infinity as a cross-check
  only, not in the primary combination." Also includes implementation note
  (leading-track definition, not large-kappa limit).

**Verdict: FIXED.** Exact threshold specified (0.1), with physical
motivation and demotion action.

---

## Finding #9 (Category B): bFlag decision tree in COMMITMENTS.md

**Arbiter requirement:** Add validation test entry with chi2 test and
fallback to self-labelling option 2.

**Evidence:**

- COMMITMENTS.md lines 106-111: "bFlag interpretation validation: if
  bFlag=4 b-tag discriminant distribution is indistinguishable from the
  full sample (chi2/ndf ~ 1.0 comparing tagged-sample discriminant
  shapes), classify bFlag as a non-b flag and default to self-labelling
  option 2 for BDT training. If chi2/ndf > 2.0 (bFlag=4 subsample is
  enriched in b relative to full sample), bFlag=4 is a usable
  b-enrichment proxy for BDT option 1."
- STRATEGY.md lines 968-976: Cross-references the COMMITMENTS.md decision
  tree.

**Verdict: FIXED.** Decision tree with specific chi2 thresholds and
both branches (option 1 and option 2) committed.

---

## Summary

| # | Finding | Verdict |
|---|---------|---------|
| 1 | A_FB^b fit formulation (Cat A) | **FIXED** |
| 3 | d0 sign convention gate (Cat B) | **FIXED** |
| 4 | C_b specification (Cat B) | **FIXED** |
| 7 | eps_c 30% grounding (Cat B) | **FIXED** |
| 8 | kappa=inf delta_b threshold (Cat B) | **FIXED** |
| 9 | bFlag decision tree (Cat B) | **FIXED** |

**All 1A + 4B findings from iteration 2 arbiter are FIXED.**

Recommend proceeding to full fresh review panel per protocol.
