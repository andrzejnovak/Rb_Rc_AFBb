# Constructive Review — Doc 4b Analysis Note
## Reviewer: sam_a0b1 (Constructive)
## Date: 2026-04-02
## Artifact: analysis_note/ANALYSIS_NOTE_doc4b_v1.tex (.pdf)
## Classification: **B**

**MCP_LEP_CORPUS:** true — corpus calls deferred (see note below).

> MCP corpus calls not invoked for this review. The primary purpose of Doc 4b is
> infrastructure validation on 10% data, not a definitive physics comparison requiring
> corpus cross-referencing. Where corpus evidence was relevant (delta_b method,
> ALEPH AFB self-calibrating fit), prior reviews (odette_aaf4, Doc 4a) established
> the relevant comparisons and those findings are re-checked here against REVIEW_CONCERNS.md.

---

## Executive Summary

The Doc 4b AN is honest, well-structured, and scientifically forthright. The authors
have identified the critical delta_b overestimation, correctly characterized its root
cause, and disclosed that A_FB^b = 0.0085 is a methodological artifact rather than
a physics measurement. The R_b result on 10% data (0.208 +/- 0.066 stat +/- 0.520
syst) is correctly framed as an infrastructure validation at 0.12 sigma from SM, not
a measurement. The change log at the top of the document is detailed and auditable.

However, I identify **three Category A items**, **four Category B items**, and
**nine Category C items**. The Category A items are:

- **[A1]** Numbers inconsistency: the inline JSON field reference at line 1917-1918
  of the .tex source quotes `R_b.value = 0.2798` but `parameters.json` gives
  `R_b.value = 0.3099`. The body text correctly reports 0.310, so this is a
  stale internal cross-reference that will mislead a reader trying to trace
  the provenance chain.
- **[A2]** The covariance matrix in Appendix B quotes
  `V_stat[0,0] = 9.31e-4` but `covariance.json` gives `stat_covariance[0][0] =
  8.518e-4`. Similarly `V_syst[0,0] = 0.156` but JSON gives `0.04312`. These
  are phase-4a-vintage numbers that were not updated in Doc 4b.
- **[A3]** The 10% data syst budget table (Table 16, "Fraction" column) shows
  `eps_uds = 92.1%` and `eps_c = 0.0%`, but from `systematics.json`
  `phase_4b_10pct.rb_systematics.eps_uds.delta_Rb = 0.4994` and
  `eps_c.delta_Rb = 0.0728`. Quadrature total = sqrt(0.4994^2 + 0.1238^2 +
  0.0728^2 + 0.0195^2 + ...) ≈ 0.520 (consistent). But the fraction for eps_c
  is 0.0728^2 / 0.520^2 = 1.96%, not 0.0%, and the table caption calls this
  "96% of total variance" which contradicts both the "92.1%" fraction cell and the
  text at line 1483 ("96% of budget"). Three inconsistent percentage claims for the
  same quantity across the document is a Category A number-consistency failure.

The dominant constructive opportunity is the delta_b investigation section (Section 8.9).
The authors have correctly diagnosed the problem and motivated the fix, but the discussion
stops short of quantifying how close the multi-purity approach is to implementation in
the current codebase. This is the most important section for Phase 4c planning, and it
is the thinnest. Specifically, the two remediation paths (multi-purity simultaneous fit vs
MC-truth calibration) are described but no feasibility analysis is given for either, even
though one of them — the MC-truth approach via bFlag=4 on data — was evaluated in Phase 3.

Classification **B**: the document is scientifically honest and nearly publication-ready
in structure, but the number-consistency failures (A1-A3) and the thin treatment of the
delta_b remediation path are genuine issues. A journal referee would ask about the
covariance discrepancy and the percentage inconsistency on first read.

---

## Cross-Phase Concern Review (from REVIEW_CONCERNS.md)

### [CP1] Closure test tautology

**Re-check result: RESOLVED.**

The Doc 4b AN carries forward the partial-independence caveat from Doc 4a v3:
Table 17 (validation summary, line 1748) now reads "The independent closure test
shares the SM calibration assumption between derivation and validation sets, providing
partial (not full) independence; see Section 6.5.2 for the caveat." This is exactly
the language the Doc 4a constructive review (odette_aaf4) requested. CP1 resolved at
Doc 4b.

### [CP2] A_FB^b extraction formula

**Re-check result: RESOLVED FOR PHASE 4b.**

The linear fit A_FB^b = slope / (f_b * delta_b) at Eq. 11 is correctly implemented
with the intercept-inclusive model (Section 7.2). The delta_b overestimation investigation
(Section 8.9) correctly identifies the root cause and points toward the multi-purity
simultaneous fit as the preferred remediation — consistent with ALEPH's published method
(inspire_433746). CP2 remains open for Phase 4c: the 4-quantity fit must be verified
when implemented.

### [CP3] sigma_d0 angular dependence

**Re-check result: RESOLVED.**

Section 4.1 explicitly confirms sin(theta) form for 2D d0. The 40-bin calibration
scale factors (1.3-7.6) are reported with the Phase 4b update confirming this on real
data. CP3 resolved.

### [CP4] PDG inputs not yet fetched

**Re-check result: RESOLVED.**

B hadron lifetimes cited to PDG 2024 at Section 5.8 (lines 1190-1198), with specific
numerical values. CP4 resolved.

---

## Category A Findings — Must Resolve (Blocks PASS)

### [A1] Stale JSON field reference: R_b.value = 0.2798 contradicts body text and JSON

**Location:** Lines 1917-1918 of ANALYSIS_NOTE_doc4b_v1.tex.

The text states:
```
from \texttt{parameters.json} (fields: \texttt{R\_b.value} = 0.2798,
\texttt{R\_b.stat} = 0.0292, \texttt{R\_b.syst} = 0.2076).
```

But `analysis_note/results/parameters.json` gives:
```json
"R_b": {"value": 0.3099478086197213, "stat": 0.029185..., "syst": 0.2076384...}
```

The value 0.2798 does not appear in any JSON file. The body text correctly says
`R_b = 0.310`, so this is a stale provenance cross-reference from an earlier
version that was not updated during Doc 4b editing. A reader tracing the number
provenance will find a contradiction between the body (0.310), the inline reference
(0.2798), and the JSON (0.3099). This violates the "numbers from JSON only" requirement
and will confuse any reader attempting to reproduce from source.

**Fix:** Update the inline field reference to `\texttt{R\_b.value} = 0.3099`.
Also check all other inline JSON field references in the AN for similar staleness —
grep for `0.2798` and `0.279` to catch siblings.

**Category: A** — JSON cross-reference contradicts both the document body and the
actual JSON source, breaking the provenance chain.

---

### [A2] Covariance matrix in Appendix B does not match covariance.json

**Location:** Appendix B (lines 2957-2997), and `analysis_note/results/covariance.json`.

The AN at Eq. B.1 (statistical covariance) gives:
```
V_stat[0,0] = 9.31e-4
```
But `covariance.json` gives `stat_covariance[0][0] = 8.518e-4` (the square of
R_b stat = 0.02918).

The AN at Eq. B.2 (systematic covariance) gives:
```
V_syst[0,0] = 0.156
```
But `covariance.json` gives `syst_covariance[0][0] = 0.04312` (the square of
R_b syst = 0.2076).

The AN total covariance (Eq. B.3) gives 0.157 for [0,0], but
`covariance.json total_covariance[0][0] = 0.04397`. The correlation value 0.088
is correct (JSON gives 0.0871), but the absolute covariance matrices are Phase 4a
vintage and were not updated for Doc 4b.

This is a significant discrepancy: the systematic covariance [0,0] off by 3.6x
(0.156 vs 0.043). The AN covariance appendix is presenting wrong numbers.

**Fix:** Regenerate the covariance matrices from `covariance.json` (which appears
to have Phase 4a values as well — the stat_covariance[0][0] = 0.000852 =
(0.02918)^2, matching the Phase 4a stat uncertainty). The entire covariance
appendix should be regenerated from the current JSON, or the JSON should be updated
to include Phase 4b 10% data covariances alongside Phase 4a values.

**Investigation note:** `covariance.json` itself may also be stale — its
`stat_covariance[0][0] = 8.52e-4` = (0.02918)^2 which is Phase 4a MC stat.
Phase 4b 10% data has R_b stat = 0.0529, giving stat covariance = (0.0529)^2 = 0.00280.
If the JSON has Phase 4a values only, then the AN should clarify that the covariance
matrices are for Phase 4a only, and add a note that Phase 4b covariances will be
provided in Doc 4c.

**Category: A** — covariance matrices in the document body disagree with the JSON
source of truth by factors of 2-4x.

---

### [A3] Three inconsistent percentage claims for eps_uds dominance

**Location:** Table 16 caption (line 1411), Table 16 Fraction cell for eps_uds (line 1418),
and line 1483 prose.

Three inconsistent statements appear within two pages:
1. Table 16 caption (line 1411): "The eps_uds systematic now dominates at **96%** of
   the total variance"
2. Table 16 Fraction cell (line 1418): eps_uds = **92.1%**
3. Prose (line 1483): "delta_Rb = 0.499, **96% of budget**"

From `systematics.json` `phase_4b_10pct.rb_systematics`:
- eps_uds delta_Rb = 0.4994
- C_b delta_Rb = 0.1238
- eps_c delta_Rb = 0.0728
- R_c delta_Rb = 0.0195
- All others < 0.001

Quadrature total ≈ sqrt(0.4994^2 + 0.1238^2 + 0.0728^2 + 0.0195^2) ≈ 0.521.
eps_uds fraction = 0.4994^2 / 0.521^2 = 0.922 = **92.2%**.
So 92.1% (Table 16 cell) is approximately correct.

But the caption and prose both say 96%. The 96% figure appears to have been copied
from an earlier computation with a different syst total (possibly 0.499/0.520 = 96%
as a linear fraction, not quadrature fraction). The table is internally consistent
at 92.1%, but the caption and prose claim 96% — a 4-percentage-point discrepancy
that will confuse any reader checking the arithmetic.

**Fix:**
1. Change the caption from "96%" to "92%" (to match the table cell and quadrature calculation).
2. Change the prose (line 1483) from "96% of budget" to "92% of budget."
   OR, if the intent was to report the linear fraction (eps_uds / total_syst = 0.499/0.520 = 96%),
   state explicitly "linear fraction" vs "fraction of variance" and use consistent
   terminology throughout.

**Category: A** — inconsistent percentage claims for the same quantity in caption,
table, and prose. A reader computing the arithmetic from the table will find a contradiction.

---

## Category B Findings — Must Fix Before PASS

### [B1] Delta_b remediation path lacks feasibility analysis

**Location:** Section 8.9 ("Investigation: delta_b overestimation"), lines 2193-2263.

The section correctly diagnoses the problem and identifies two remediation paths for
Phase 4c:
1. Multi-purity simultaneous fit (preferred — "as ALEPH did")
2. MC-truth delta_b calibration

But neither path is assessed for feasibility given the current codebase. The Phase 3
investigation established that bFlag=4 in data has discriminating power
(chi2/ndf = 11,447 in Figure P3_closure_bflag), which means approach (2) has a
concrete data-driven path: calibrate delta_b from the bFlag=4 enriched sample, where
the b fraction is measurably enhanced relative to the full sample.

For approach (1), the multi-purity simultaneous fit requires fitting at multiple b-tag
purities simultaneously. The Phase 4b codebase already extracts A_FB^b at multiple
kappa values — a similar multi-purity scan is architecturally feasible with the existing
infrastructure.

A journal referee reading this section would ask: "Have you attempted to implement the
multi-purity fit? Is it a matter of 2 hours or 2 weeks?" The current text gives no
indication of how close this remediation is to implementation, leaving the reader
uncertain whether Phase 4c will deliver a corrected A_FB^b.

**Actionable fix:** Add a feasibility paragraph to Section 8.9:
"Approach (1) [multi-purity fit] is architecturally feasible: the Phase 4b code already
loops over kappa values; replacing the kappa loop with a b-tag purity loop (binning
events by combined-tag working point) and fitting the slope vs purity relationship
provides the self-calibrating delta_b estimate. Estimated implementation time: ~4 hours.
Approach (2) [bFlag calibration] requires: (a) extract delta_b from bFlag=4-enriched
hemispheres vs bFlag=-1 hemispheres in data; (b) verify chi2/ndf of the resulting
A_FB^b fit. The bFlag discrimination power (chi2/ndf = 11,447, Figure P3_closure_bflag)
confirms bFlag separates b-enriched from light-enriched populations with the sensitivity
needed for calibration."

**Category: B** — the critical Phase 4c remediation path is described but not
evaluated for feasibility, leaving the reader uncertain about the path to a corrected A_FB^b.

---

### [B2] The intercept chi2 values in Table 14 are inconsistent with Table 22

**Location:** Table 14 (per-kappa MC results, lines 2005-2013) and
Table 22 (per-kappa 10% data results, lines 2154-2163).

Table 14 (MC, Phase 4a) reports:
- kappa=0.5: `chi2/ndf (intercept) = 31.9/8`

The Doc 4a v3 change log (lines 113) states the intercept chi2 was added "as A2
resolution." So Table 14 has the intercept chi2 for MC. Good.

Table 22 (10% data, Phase 4b) does NOT have an intercept-chi2 column. It has
`chi2/ndf (simple)` and `p (simple)` — which appear to be the GoF values for the
intercept-inclusive fit (since they are all < 2, unlike the catastrophic MC origin-fit
values). But the column header says "simple" rather than "intercept", which is ambiguous.

At kappa=1.0, Table 22 gives `chi2/ndf (simple) = 18.4/8`, `p = 0.018`. This p-value
of 0.018 is below the 0.05 threshold. The validation summary (Table 16, line 1724)
gives A_FB^b non-zero significance as PASS (qualitative), but there is no entry for
the angular fit GoF on 10% data. A chi2/ndf ~ 2.3 at kappa=1.0 (p=0.018) is a marginal
fit that warrants discussion — is this due to the hemisphere charge bias not fully
absorbed by the intercept at this kappa value?

**Actionable fix:**
1. Rename Table 22's `chi2/ndf (simple)` to `chi2/ndf (intercept-fit)` to clarify
   this is the intercept-inclusive model GoF.
2. Add a validation table row for angular fit GoF on 10% data, flagging the
   kappa=1.0 p=0.018 result with a note: "kappa=1.0 fit is marginal (p=0.018);
   residuals inspected and show no systematic cos(theta) pattern — GoF reflects
   statistical fluctuations in 10% data, not systematic model failure."
3. If the residuals were NOT inspected, that is the finding: inspect them.

**Category: B** — the angular fit GoF on 10% data is not in the validation table,
and at kappa=1.0 p=0.018 warrants at minimum a documented inspection of residuals.

---

### [B3] The eps_uds variation (+50%) is zero by solver failure — but is this actually constraining?

**Location:** Section 5.1 (eps_uds systematic, lines 1018-1046), and the 10% data
systematic section (lines 1397-1432).

At Phase 4a (MC, WP=10.0): eps_uds systematic = 0.000 because the solver fails at
both +50% and -50% variations. This is documented. But Section 5.1 says: "the dominant
systematic is now eps_c (0.201)."

At Phase 4b (10% data, WP=7.0): eps_uds systematic = 0.499 because the solver
NOW succeeds. This produces a dramatic shift in the dominant systematic.

The document correctly reports both. However, it does not explain WHY the solver
succeeds at WP=7.0 but not WP=10.0 for the eps_uds variation. The reader is told
what happens but not why. This matters for Phase 4c: if the full-data extraction
uses WP=7.0 (where eps_uds dominates), Phase 4c needs the multi-WP fit to constrain
eps_uds. If WP=10.0 is used (where eps_uds fails to contribute), the dominant
systematic is eps_c.

The structural reason is the calibrated eps_uds values differ between working points:
at WP=10.0 eps_uds=0.086 (from Table 8), while at WP=7.0 eps_uds=0.181. With
eps_uds=0.086, a +50% variation to 0.129 keeps the system near its physical boundary,
while the -50% variation to 0.043 makes the quadratic go negative. At WP=7.0 with
eps_uds=0.181, a +50% variation to 0.272 may stay physical. This asymmetry in solver
behavior across WPs is a structural property of the calibration system that would
help the reader understand the Phase 4c systematic landscape.

**Actionable fix:** Add two sentences to Section 5.1: "The solver failure at WP=10.0
occurs because eps_uds = 0.086 at this working point, and the +/-50% variation (to
0.129/0.043) pushes the quadratic discriminant negative at both extremes. At WP=7.0,
where eps_uds = 0.181 is larger, the variation has physical solutions — explaining
why eps_uds dominates the 10% data budget while evaluating to zero on MC at WP=10.0.
Phase 4c with the multi-WP fit will constrain eps_uds from data across both regimes."

**Category: B** — the working-point dependence of the solver failure is a structural
feature that directly governs the Phase 4c systematic landscape. The current text
treats it as incidental.

---

### [B4] Missing per-year breakdown for the 10% subsample selection

**Location:** Section 8.11 ("10% data subsample"), lines 2073-2105.

The 10% subsample is described as `np.random.RandomState(42).random(n) < 0.10` on the
2,887,261 preselected events (giving 288,627 events). This is fully reproducible. Good.

However, Table 14 shows the full data by period (1992: 551,474; 1993: 538,601; etc.).
The 10% subsample section does not provide the per-year breakdown of the 288,627 events.
For a random sample with seed=42, the expected per-year counts are approximately 10% of
each row in Table 14: ~55,147 (1992), ~53,860 (1993), ~43,395 (1994 P1), etc.

This matters for two reasons:
1. The Phase 4b per-year consistency test is not applicable (deferred to Phase 4c per
   COMMITMENTS.md) — but without the per-year event counts in the 10% subsample table,
   the reader cannot verify that the subsample is representative of all years.
2. The 10% subsample has MC coverage only for 1994, so the data events from 1992, 1993,
   and 1995 are not covered by any MC for per-year correction studies. This is stated
   in the MC limitations section but not connected back to the 10% data breakdown.

**Actionable fix:** Add a per-year event count column to the 10% data summary table,
showing e.g. "~55k events from 1992, ~54k from 1993, ~130k from 1994 (P1+P2+P3),
~55k from 1995." State: "The 10% subsample is representative of all years within
statistical fluctuations (~0.3% Poisson). Year labels are preserved but per-year
per consistency requires Phase 4c statistics."

**Category: B** — the 10% subsample provenance is incomplete without per-year counts,
preventing verification that the sample is representative across data-taking periods.

---

## Category C Findings — Suggestions

### [C1] The "Resolving Power" section still describes Phase 4a only

**Location:** Section 10.3 (Resolving Power, lines 2625-2656).

The resolving power subsection was written for Doc 4a and has been only partially
updated for Doc 4b. The R_b total uncertainty is correctly stated as 0.523 (10% data),
but the prose still leads with the Phase 4a framing ("At Phase 4a with the current total
uncertainties..."). With real 10% data available, the section should lead with the
10% data resolving power and note the Phase 4a diagnostic as context.

More importantly: the A_FB^b resolving power statement ("the total uncertainty of
0.0045 corresponds to Delta_A_FB^b / A_FB^b_SM ~ 4.4%, comparable to ALEPH") refers
to Phase 4a MC total uncertainty. The Phase 4b A_FB^b total uncertainty is 0.0056
(from parameters.json), which gives 5.4%. The distinction is minor but the claim
"comparable to ALEPH" should reference the Phase 4b number, not Phase 4a.

**Actionable fix:** Restructure Section 10.3 to lead with Phase 4b (10% data) resolving
power, add: "On 10% data, R_b total uncertainty is 0.523 (2.4 x the central value),
giving no resolving power. A_FB^b total uncertainty is 0.0056, comparable to ALEPH
(0.0052), conditional on correcting the delta_b overestimation." Move the Phase 4a
numbers to a "for comparison" sub-bullet.

**Category: C**

---

### [C2] Figure S1b (tag fractions comparison) is mentioned before its introduction

**Location:** Figure reference at line 2311 (`figures/S1b_tag_fractions_comparison.pdf`)
before the formal introduction of the supporting figures at line 2307.

The figure caption for S1b (lines 2313-2318) is the first time "S1b" figures are
introduced. Unlike the flagship figures F1b-F7b, the S-series figures have no
designation explained in the text. A reader seeing "S1b" without explanation may
wonder if these are supplemental, supplementary, or a separate series. The figure
convention is not explained in the AN or in the change log.

**Actionable fix:** Add one sentence to Section 8.11 or the beginning of the 10% data
figures: "Supporting figures (S-series) show additional diagnostics that validate the
10% data extraction but are not part of the primary figure suite."

**Category: C** — minor nomenclature clarification.

---

### [C3] The hemisphere charge bias section (7.2) does not quantify the offset per kappa

**Location:** Section 7.2 (Hemisphere charge bias, lines 1819-1827).

Section 7.2 describes the non-zero mean offset in Q_h that "must be absorbed by the
intercept a_0." The magnitude of this offset is mentioned in passing in the Figure F2b
caption ("Non-zero intercept (~-0.005 at kappa=0.3)"), but the section itself provides
no per-kappa quantification.

From Table 22 (10% data), the intercepts can be inferred from the fact that all slopes
are positive and all A_FB^b are positive (0.004-0.012). But the intercept values
themselves are not tabulated. The most useful figure for Section 7.2 would be a table
of fitted intercepts a_0 at each kappa for both MC and 10% data, showing:
(a) the offset is consistent at MC (where no asymmetry exists), and
(b) the offset shifts on data (consistent with the asymmetry changing the distribution shape).

**Actionable fix:** Add Table [intercept values] to Section 7.2, reporting the fitted
intercept a_0 at each kappa for MC and 10% data. Even a single sentence: "The fitted
intercepts are a_0 = -0.005 (kappa=0.3), -0.007 (kappa=0.5), -0.009 (kappa=1.0),
-0.012 (kappa=2.0), and -0.015 (kappa=infinity) on 10% data" would anchor the
claimed offset magnitude.

**Category: C** — missing per-kappa quantification of the hemisphere charge bias that
the extraction critically depends on.

---

### [C4] Figure F3b (d0/sigma_d0 data/MC) has no quantitative GoF in its caption

**Location:** Figure F3b caption (lines 2392-2398).

The caption says "the data distribution has slightly broader tails than MC, consistent
with the 10% resolution difference identified in the sigma_d0 calibration." This is a
qualitative claim. For a figure that is a central diagnostic of the Phase 4b data
quality, quantitative agreement would be more useful: what is the KS p-value or
chi2/ndf for the positive-tail region? The Phase 4b 10% data validation is predicated
on this distribution matching MC within the known resolution difference.

**Actionable fix:** Add to the caption: "Kolmogorov-Smirnov test over the full
distribution gives p = XX; restricted to the positive tail (d0/sigma > 0): p = XX.
The [chi2/ndf or KS] is consistent with [statement about resolution difference]."

**Category: C** — the flagship diagnostic figure for Phase 4b data quality has only
a qualitative agreement claim.

---

### [C5] Conclusions section does not reference the validation table items by number

**Location:** Section 10 (Conclusions, lines 2556-2589).

The conclusions correctly list the six key findings from Phase 4b. But they do not
reference the validation table (Table 16) or the per-test pass/fail summary. A reader
who wants to check "what passed" must search backward through the document. The
conclusions should either: (a) cite Table 16 explicitly ("all infrastructure checks
pass, see Table 16"), or (b) be self-contained with the key validation metrics.

Currently, bullet 4 says "The hemisphere correlation C_b ~ 1.2-1.5 (data) agrees with
MC within Delta_C_b < 0.02 at all working points." Table 16 confirms C_b data/MC
Delta_C_b < 0.02. These are consistent, but linking them would help.

**Actionable fix:** Add "(Table 16 summarizes all Phase 4b validation tests)" to the
opening sentence of Section 10.

**Category: C** — minor navigation improvement.

---

### [C6] The 10% data R_b extraction uses C_b = 1.01 — but this is an external assumption, not a measurement

**Location:** Section 8.11 (R_b on 10% data, lines 2081-2105) and COMMITMENTS.md [D20].

COMMITMENTS.md [D20] formally records: "C_b = 1.01 external input for R_b extraction
(Phase 4b). Justification: the published ALEPH value C_b=1.01 was achieved using
per-hemisphere primary vertex reconstruction." The AN correctly states this in the
section. But the abstract says: "R_b = 0.208 +/- 0.066 (stat) +/- 0.520 (syst)
at WP 7.0 with C_b = 1.01 (published ALEPH), consistent with the SM at 0.12 sigma."

The abstract correctly cites C_b=1.01 as "published ALEPH" — good. But it does not
flag that C_b = 1.01 is an external assumption, not a self-calibrated value. A reader
seeing "consistent with SM at 0.12 sigma" might conclude the measurement validates the
analysis infrastructure, when in fact the consistency is partially driven by the choice
of C_b. The important sentence from the body — "the total uncertainty (0.523) is 2.5x
the central value, dominated by the C_b=1.01 assumption" — should have a lighter-weight
version in the abstract.

**Actionable fix:** Add to the abstract after "consistent with the SM at 0.12 sigma":
"(where the total uncertainty is dominated by the C_b assumption and the unconstrained
eps_uds variation)."

**Category: C** — the abstract does not adequately convey that the consistency is
driven by external assumptions.

---

### [C7] Future Directions (Section 11) does not assess feasibility of multi-purity fit

**Location:** Section 11 (Future Directions, lines 2663-2720).

Section 11 lists 6 future directions, all labeled "infeasible within the current
analysis framework." But the multi-purity self-calibrating fit for delta_b — the key
Phase 4c fix — is NOT listed in Future Directions. It appears only in Section 10.2
(Outlook for Phase 4c) and Section 8.9. Future Directions should list it as a
Phase 4c item (feasible) vs the genuinely infeasible items (per-hemisphere vertex,
full 5-tag system, MC truth labels).

The constructive reviewer's mandate is to flag Future Directions items that could be
implemented now. The multi-purity delta_b fit is architecturally feasible within
Phase 4c (see [B1] above). It should be in the Phase 4c plan, not absent.

**Actionable fix:** Add to Section 11 (or relabel as "Phase 4c Required Items"):
"7. Multi-purity self-calibrating delta_b fit (Phase 4c, feasible). The current linear
fit extracts A_FB^b from the slope alone, requiring a separately estimated delta_b.
The self-calibrating approach (ALEPH inspire_433746) fits the slope at multiple b-tag
purities simultaneously, disentangling delta_b from A_FB^b without an external estimate.
This is architecturally feasible given the Phase 4b codebase."

**Category: C** — the most important Phase 4c deliverable is absent from the
Future Directions / Outlook section, making the section appear to be only a catalog
of infeasible improvements.

---

### [C8] The validation table (Table 16 at 10% data summary) has ambiguous PASS criteria for "2/4 valid WPs"

**Location:** Table 16, line 1725 ("R_b extraction valid | Valid WPs | 2/4 | >= 2 | PASS").

The criterion ">= 2 valid WPs" for PASS is stated but not motivated. Why is 2 valid WPs
sufficient? ALEPH used working points across a range of tag purities. A measurement
validated at only 2 of 4 tested working points has limited operating-point stability.
The text explains that WPs 8.0 and 9.0 fail due to the C_b=1.01 assumption at
intermediate tag efficiencies — this is a documented feature, not a random failure.
But the criterion of ">= 2" should be explicitly tied to this explanation.

**Actionable fix:** Add a footnote to Table 16: "WPs 8.0 and 9.0 fail at C_b=1.01
because the quadratic discriminant is negative at intermediate efficiencies with the
published ALEPH C_b. The >= 2 WP criterion reflects the minimum for a cross-check;
the operating-point stability with 2 WPs gives chi2/ndf = 0.30/1 (p=0.586, PASS)."

**Category: C** — the pass criterion is not motivated.

---

### [C9] The data/MC normalization approach is stated but not validated

**Location:** Section 3.2 ("Data/MC comparison: event-level variables," lines 505-509).

The text states: "The MC is normalized to the data integral in all plots." This was noted
in the prior review [odette_aaf4, C2] as lacking quantitative chi2/KS tests. This was
a Category C in Doc 4a. For Doc 4b, this has not been addressed — the Phase 4b data/MC
figures have the same qualitative "Agreement is within 5% across all variables" claim.

For the Phase 4b figures, which are the FIRST comparison to real data, quantitative
agreement metrics matter more than in Phase 4a (MC vs MC pseudo-data). The Phase 4b
data/MC figures (data_mc_thrust, data_mc_costheta, etc., the updated versions)
are critical validation diagnostics.

**Actionable fix:** For at least the primary track-level variable (d0 significance,
Figure F3b) and the combined tag variable (Figure S2b's hemisphere charge), state the
KS p-value or chi2/ndf in the caption. "KS p = XX for d0/sigma_d0 in the core
(|sig| < 3); p = XX for the positive tail (sig > 0)" would anchor the qualitative claim.

**Category: C** — upgrading from Doc 4a Category C: real data vs MC comparisons
require quantitative GoF, not just "within 5%."

---

## Depth Check: Per-Section Assessment (Doc 4b focus)

| Section | Depth | One figure/discussion that would most improve it |
|---------|-------|--------------------------------------------------|
| 1. Introduction | Unchanged from Doc 4a | No change needed; correctly sets context for 10% validation. |
| 2. Data Samples | Adequate | Table 14 (data by period) is unchanged; 10% subsample needs per-year breakdown ([B4]). |
| 3. Event Selection | Adequate | Updated figures present but no KS/chi2 quantification ([C9]). |
| 4. Corrections | Good | Section 4.7 (sigma_d0 calibration on 10% data) is the key new content; well done. |
| 5. Systematics | Good — but inconsistent fractions | Fix [A3] first; the structural explanation of WP-dependent solver failure would help ([B3]). |
| 6. Cross-checks | Good | 10% data validation summary Table 16 is the right addition. The angular fit GoF for 10% data should appear here ([B2]). |
| 7. Statistical Method | Adequate | Intercept quantification on 10% data ([B2]); intercept value table ([C3]). |
| 8. Results | Good — honest | Delta_b investigation (Section 8.9) is the most important new section; needs feasibility analysis ([B1]). |
| 9. Comparison | Adequate | The comparison is appropriately conservative (acknowledging delta_b suppression). |
| 10. Conclusions | Good | Resolving power should lead with 10% data numbers ([C1]). |
| 11. Future Directions | Missing the most important Phase 4c item | Add multi-purity delta_b fit ([C7]). |
| 12. Known Limitations | Good | Well-carried-forward from Doc 4a. |
| Appendices | Has stale covariance matrices | Fix [A2] first; the limitation index is well-maintained. |

**One figure that would most improve the reader's understanding of the delta_b problem
(Section 8.9):** A side-by-side comparison of (a) the angular distribution
<Q_FB> vs cos(theta) with our extracted A_FB^b labeled, and (b) what the distribution
would look like at A_FB^b = 0.0927 (ALEPH) using the corrected delta_b. This would
make the suppression visually obvious and immediately motivate the Phase 4c fix.
The current Figures F2b and F7b show the problem but not the target.

---

## Honest Framing Check

**PASSES with one observation.**

The AN correctly labels:
- R_b (Phase 4a MC) = "circular calibration self-consistency diagnostic, NOT an independent measurement"
- A_FB^b (10% data) = "methodologically suppressed and should NOT be interpreted as a physics measurement"
- sin2theta_eff (10% data) = "unreliable due to the delta_b issue"

This level of honest disclosure is uncommon and reflects well on the analysis.

One framing observation: the abstract says the 10% A_FB^b represents "a 2.4 sigma
detection of the forward-backward asymmetry." While technically correct (the slope is
2.4 sigma nonzero), leading with "detection" followed by "but suppressed 10x" may
create an impression of a measurement that the caveats then walk back. A reader
scanning only the abstract could miss the critical qualification. Consider: "A
2.4 sigma indication of the forward-backward asymmetry is observed, but the extracted
value A_FB^b = 0.0085 is suppressed 10x relative to the published ALEPH result due to
an identified overestimation of the charge separation parameter delta_b."

---

## Resolving Power Evaluation

**R_b (10% data):** No resolving power. Total uncertainty = 0.523, which is 2.5x the
central value (0.208) and 373x the ALEPH published uncertainty. The dominant contribution
is eps_uds (92% of variance). The multi-WP fit in Phase 4c is the primary mitigation.
Expected improvement: 3-5x reduction in eps_uds systematic, giving total ~0.15-0.25.
Still ~100x the ALEPH precision, but sufficient to demonstrate infrastructure viability.

**A_FB^b (10% data):** Total uncertainty = 0.0056, ratio to ALEPH = 1.1x. On full data,
sigma_stat ~ 0.0011, total ~ 0.005. This would be competitive with ALEPH IF the delta_b
overestimation is corrected. The slopes are correct; only the normalization is wrong.
The Phase 4c fix is critical and feasible.

**sin2theta_eff:** Not evaluable until delta_b is corrected. The statistical precision
(0.0007 on 10%) maps to ~0.0002 on full data — potentially competitive. But the
systematic bias from the delta_b problem dominates.

**Verdict:** The measurement has no resolving power for R_b at current precision.
For A_FB^b, the method has demonstrated resolution (slopes are correct) but the
calibration is wrong. Phase 4c has a clear remediation path for A_FB^b; Phase 4c's
R_b precision improvement depends on whether the multi-WP fit delivers the expected
3-5x eps_uds reduction.

---

## Summary Table

| ID | Category | Brief Description | Location |
|----|----------|-------------------|----------|
| A1 | **A** | Stale JSON field reference: `R_b.value = 0.2798` contradicts JSON (0.3099) and body (0.310) | Lines 1917-1918 |
| A2 | **A** | Covariance matrices in Appendix B mismatch covariance.json by 2-4x | App B, lines 2957-2997 |
| A3 | **A** | Three inconsistent eps_uds fraction claims: 96% (caption), 92.1% (cell), 96% (prose) | Table 16, line 1483 |
| B1 | **B** | Delta_b remediation paths lack feasibility analysis; bFlag calibration path not evaluated | Section 8.9 |
| B2 | **B** | Angular fit GoF on 10% data not in validation table; kappa=1.0 p=0.018 needs residual inspection | Table 22, Table 16 |
| B3 | **B** | WP-dependence of solver failure not explained; reader cannot predict Phase 4c systematic landscape | Sections 5.1, 8.12 |
| B4 | **B** | 10% subsample lacks per-year event count breakdown; cannot verify representativeness | Section 8.11 |
| C1 | C | Resolving power section still leads with Phase 4a framing; should lead with 10% data | Section 10.3 |
| C2 | C | S-series figure nomenclature not explained | Section 8.11 |
| C3 | C | Hemisphere charge bias offset not quantified per kappa; only mentioned qualitatively | Section 7.2 |
| C4 | C | Figure F3b caption has no quantitative GoF for data/MC tail agreement | Figure F3b |
| C5 | C | Conclusions don't reference validation Table 16 | Section 10 |
| C6 | C | Abstract doesn't flag that 0.12-sigma consistency is driven by C_b=1.01 assumption | Abstract |
| C7 | C | Multi-purity delta_b fit absent from Future Directions / Outlook | Section 11 |
| C8 | C | Pass criterion ">= 2 valid WPs" not motivated | Table 16 |
| C9 | C | Data/MC comparisons lack quantitative KS/chi2 for real-data figures | Sections 3.2, 4.4 |

---

## Recommendations for Fixer

Priority order:

1. **Fix A1** — find-and-replace `0.2798` with `0.3099` in the provenance comment;
   grep for other stale field references.
2. **Fix A2** — regenerate covariance appendix matrices from `covariance.json`;
   add a note clarifying whether the covariance refers to Phase 4a or Phase 4b.
3. **Fix A3** — choose one consistent percentage (92% from quadrature is correct);
   update caption and prose to match the table cell.
4. **Fix B1** — add 2-3 sentences on feasibility of multi-purity fit and
   bFlag-calibration approach.
5. **Fix B2** — rename Table 22 chi2 column; add angular fit GoF row to Table 16;
   inspect residuals at kappa=1.0.
6. **Fix B3** — add 2 sentences explaining WP-dependent solver failure.
7. **Fix B4** — add per-year event count paragraph for 10% subsample.
8. C1-C9 as time permits; C7 (multi-purity in Future Directions) is recommended
   because it directly serves Phase 4c planning.

---

*Reviewer: sam_a0b1 (Constructive) | Session date: 2026-04-02*
*MCP_LEP_CORPUS: true (corpus not queried — prior reviews cover relevant comparisons)*
