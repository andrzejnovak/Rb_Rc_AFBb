# Critical Review — Phase 4c Full Data

**Reviewer:** sven_2437 | **Date:** 2026-04-03
**Artifact under review:** `phase4_inference/4c_observed/outputs/INFERENCE_OBSERVED.md`
**Supporting JSONs:** `three_tag_rb_fulldata.json`, `afb_fulldata.json`,
  `systematics_fulldata.json`, `per_year_results.json`, `bdt_crosscheck_fulldata.json`
**Upstream:** `analysis_note/results/parameters.json`, `systematics.json`, `validation.json`
**Comparison:** `phase4_inference/4b_partial/outputs/INFERENCE_PARTIAL.md`
**Toggles checked:** `MCP_LEP_CORPUS = true`. Corpus calls available.

---

## PASS 1 — METHODOLOGY/VALIDATION AUDIT

### 1.1 Validation.json vs AN claims

The `validation.json` file contains **Phase 4a MC results only** — it was
not updated for Phase 4c full data. Evidence:

- `validation.json` → `"operating_point_stability"` → `chi2/ndf = 1.16e-10`,
  which is the Phase 4a MC trivial-zero result (Section 1.2 below).
- `validation.json` → `"operating_point_stability_sf_corrected"` →
  `chi2 = 0.3787, ndf = 14` — labelled as "10% data" from `4b_partial/outputs`.
- `validation.json` → `"independent_closure_3tag"` → four MC configs with
  pulls 0.06–0.59. These are the Phase 4a closure results.

**There is no Phase 4c entry in `validation.json`.** The INFERENCE_OBSERVED.md
reports WP stability chi2/ndf = 5454/7 (p = 0.0, FAIL) but this number
does not appear anywhere in `validation.json`. The AN-facing results JSON
(`analysis_note/results/parameters.json`) records
`"stability_chi2_ndf": 779.1040059253958` at `R_b_fulldata_3tag_combined`
— a completely different number from both the artifact (5454/7) and the
raw three_tag JSON (chi2 = 5453.7/7). The chi2 in the AN JSON matches
the raw JSON. The AN artifact reports 5454/7. These are the same to
rounding — but the AN JSON source field is not cited from a
Phase 4c `validation.json` entry.

**Finding [V1]:** `validation.json` was never updated for Phase 4c.
The Phase 4c WP stability FAIL, GoF at each WP, and per-year consistency
tests are not registered there. A reader cross-checking `validation.json`
would see Phase 4a/4b results only. Category A — the spec requires
`results/*.json` to be updated with Phase 4c results.

### 1.2 Fit triviality gate — closure chi2 = 0

The `validation.json` → `"operating_point_stability"` reports
`chi2 = 8.115e-10` (numerically zero). The CLAUDE.md Phase 4c spec
states: "Fit triviality gate (chi2 = 0 → investigate circularity)." This
was not investigated in the artifact. The Phase 4a closure chi2 = 0 was
noted in COMMITMENTS.md (`[x] ... stability chi2/ndf = 0.00/7 across 8 configs`)
but the triviality investigation is absent.

**Finding [V2]:** The triviality gate was not formally cleared. The MC
closure chi2 ~ 0 means the MC calibration is algebraically self-consistent
(efficiencies extracted from MC and counts evaluated on same MC →
trivially closed). This is the classic pitfall listed in
`conventions/extraction.md`: "A self-consistent extraction always recovers
the correct answer by construction." The Phase 4a MC closure result is
not an independent validation. Category A — per CLAUDE.md Phase 4c:
"Fit triviality gate (chi2 = 0 is an alarm, not a result)."

### 1.3 Primary closure test: ±20% corruption sensitivity

The CLAUDE.md Phase 4c prompt specifies (via `agents/critical_reviewer.md`
Pass 1): "Primary closure test: was the ±20% corruption sensitivity test
run and documented?" COMMITMENTS.md lists:
- [x] Closure test (c): artificial contamination injection — "ratio = 2.14,
  directional agreement confirmed (Phase 4a)"

This was run on MC pseudo-data in Phase 4a. No Phase 4c re-run on
full data appears in the artifact. There is no stress test on the full
data — no parameter injection, no artificial contamination test using the
Phase 4c pipeline.

**Finding [V3]:** No Phase 4c closure/stress test on full data. The
COMMITMENTS.md closure entries are Phase 4a artifacts. The Phase 4c
artifact proceeds directly from calibration to extraction to
systematics without any independent validation of the full-data pipeline.
Category A — per `conventions/extraction.md` §1: "Independent closure
test (Category A if fails) — apply the full extraction procedure to a
statistically independent MC sample." At Phase 4c the relevant check
is: does the full-data pipeline recover the expected result when the
analysis chain is end-to-end? A bootstrapped subset, a jackknife split,
or a re-run on the calibration MC with the full-data workflow would satisfy
this gate. None is present.

### 1.4 Systematic zero-impact overlay figures

The spec requires: "For each systematic with zero impact: is the
nominal-vs-varied overlay figure present?" The systematics breakdown
figure is registered in FIGURES.json but described only as "Systematic
uncertainty breakdown for R_b and A_FB^b" — this is a bar chart of
magnitudes, not a bin-by-bin overlay. No bin-by-bin overlays exist for
any systematic in the output artifacts.

Additionally, the sigma_d0 systematic delta(R_b) = 0.00075 and
sigma_d0_form delta(R_b) = 0.00040 are both listed as "Scaled from
ALEPH published x1.5" or "Scaled from MC statistics systematic" —
flat estimates, not propagated through the analysis chain.

**Finding [V4]:** Flat systematic estimates for sigma_d0 (0.00075) and
sigma_d0_form (0.00040) are not propagated through the analysis chain.
Per `agents/critical_reviewer.md`: "For EVERY systematic shift: verify
the shift is BIN-DEPENDENT. A perfectly flat relative shift ... means
the systematic was not actually propagated." These two are pure number
assignments. Category A — systematic not propagated.

### 1.5 Precision comparison

From `validation.json`:
- `R_b_vs_ALEPH`: our_total = 0.06530, reference = 0.0014, ratio = 46.6x
- `R_b_vs_LEP_combined`: our_total = 0.06530, reference = 0.00066, ratio = 98.9x

These are Phase 4a numbers. The Phase 4c systematic total is 0.01812
(from INFERENCE_OBSERVED.md). Let us compute:
- vs ALEPH (0.0014): 0.01812 / 0.0014 = 12.9x (still massive)
- vs LEP combined (0.00066): 0.01812 / 0.00066 = 27.5x

The explanation in `validation.json` cites four causes but does not
quantify their relative contribution. The dominant systematic is eps_c
at 0.01486 (82% of total systematic), a 10% variation of the charm
efficiency. ALEPH's eps_c systematic was evaluated at the per-cent level
with a data-driven charm control region. Without a charm control region
we are 10x larger on this source alone.

**Finding [V5]:** The precision comparison artifact was not updated for
Phase 4c. The "investigation_required: true" field was set at Phase 4a
and the investigation was never completed. The new Phase 4c numbers
(12.9x vs ALEPH) require a documented explanation identifying which
specific limitation is responsible for the factor-of-12 precision gap
and why it could not be recovered. Category B.

### 1.6 Findings without resolution sections

The INFERENCE_OBSERVED.md has three numbered findings (F1–F4). All four
have interpretation sections. F3 (A_FB^b negative) states: "The root cause
is the MC purity correction" — but offers no Resolution with evidence of
3 remediation attempts. F4b (4c escalation concern) is not listed. The
spec requires: "Every finding has a Resolution + Evidence section"
(Phase 4c CLAUDE.md completion criteria). F3 has an interpretation but
no Resolution header and no documented attempts.

**Finding [V6]:** F3 (wrong-sign A_FB^b) lacks a formal Resolution
section with documented remediation attempts. This finding is
physics-critical: A_FB^b = -0.076 vs SM +0.100 is a >8-sigma deviation.
The artifact explains the bias but does not document what was tried to
correct it (data-driven purity, alternative kappa, hemisphere charge
offset investigation). Category A.

### Pass 1 Summary

| ID | Issue | Severity |
|----|-------|----------|
| V1 | validation.json not updated for Phase 4c | A |
| V2 | Fit triviality gate not cleared (MC chi2 = 0 is algebraic) | A |
| V3 | No Phase 4c independent closure/stress test | A |
| V4 | sigma_d0 and sigma_d0_form systematics are flat estimates | A |
| V5 | Precision comparison not updated; investigation incomplete | B |
| V6 | F3 (wrong-sign A_FB^b) lacks Resolution + remediation record | A |

---

## PASS 2 — STANDARD CRITICAL REVIEW

### 2.1 Physics Sanity — A_FB^b Wrong Sign (Category A mandatory per spec)

**Result:** A_FB^b = -0.076 +/- 0.019 (total). SM value = +0.100.
Deviation from SM = (-0.076 - 0.100) / 0.019 = -9.3 sigma.
Deviation from published ALEPH value (+0.0927) = (-0.076 - 0.0927) / 0.019
= -8.9 sigma.

Per `CLAUDE.md` §"Review Protocol" §6.8 and `agents/critical_reviewer.md`:
"Any result with a pull > 3-sigma from a well-measured reference value is
Category A unless the reviewer verifies: (1) a quantitative explanation,
(2) a demonstrated magnitude match (calculation/toy/fit variant), and
(3) no simpler explanation (bugs, sign errors)."

**Checking the three conditions:**

(1) Quantitative explanation: The artifact states the bias comes from MC
purity correction — f_b from MC is overestimated because MC b-tag
efficiency is higher than data b-tag efficiency. The jet charge slope is
small (~0.001-0.009 for kappa=0.3) and charm correction subtracts a
comparable amount. This is qualitative, not quantitative. What is the
actual f_b bias magnitude? The full-data eps_b_tight (SF) = 0.485 vs
MC eps_b_tight = 0.499 — a 2.8% difference. A 2.8% overestimate of f_b
in the denominator of A_FB^b = (slope - f_c*delta_c*A_FB^c) / (f_b*delta_b)
cannot produce an 18-unit shift from +0.100 to -0.076. The bias would
be of order 2.8% * 0.100 = 0.003, not 0.176. **Condition (1) not
quantitatively satisfied** — the proposed mechanism does not explain the
magnitude of the wrong sign.

(2) Demonstrated magnitude match: No calculation or toy is presented
showing that the known data/MC efficiency mismatch produces the observed
A_FB^b value of -0.076. Condition (2) not satisfied.

(3) Simpler explanation not excluded: The slope of <Q_FB> vs cos(theta)
is negative across all kappas (from afb_fulldata.json: mean_qfb at
cos(theta) = 0.81 is -0.006175, more negative than at cos(theta) = -0.81
which is -0.005740, for kappa=0.3). This is qualitatively wrong: <Q_FB>
should be positive in the forward hemisphere for b quarks (b quark jet
tends to go forward; b-bar jet backward, and their jet charges have
opposite sign). The slope being negative and nearly flat suggests either
(a) a sign convention error in the jet charge or thrust axis definition,
(b) charge conjugation confusion between b and b-bar, or (c) the wrong
cos(theta) sign convention. These are all simpler explanations than a
large purity bias. Condition (3) not excluded.

**Finding [P1]:** A_FB^b = -0.076 is -9.3 sigma from SM (+0.100). The
proposed explanation (purity bias) is not quantitatively demonstrated
to explain the magnitude or the sign reversal. Simpler explanations
(jet charge sign convention, thrust axis sign, b vs b-bar hemisphere
assignment) have not been systematically excluded. The artifact notes
"the slope of Q_FB vs cos(theta) is very small" but does not check
whether the slope sign is correct. Category A — this is the most
critical finding in the review.

Per COMMITMENTS.md [D4]: "Hemisphere jet charge for A_FB^b." The
convention was specified but the sign of A_FB^b tracks the sign of the
jet charge. If the thrust axis direction convention is wrong (b jet
defined as going in the minus-z direction when it should be plus-z),
the entire asymmetry inverts. The per-year A_FB^b values in
per_year_results.json are all negative: 1992 = -0.018, 1993 = -0.033,
1994 = -0.061, 1995 = -0.084. The 1994 MC (which is the calibration
year) gives the largest negative value. This is consistent with a
systematic sign error rather than a statistical fluctuation.

### 2.2 R_b GoF Failure — All WPs Fail

From three_tag_rb_fulldata.json, all 8 working points have chi2/ndf >> 1:

| WP | chi2_sf | ndf | chi2/ndf |
|----|---------|-----|----------|
| tight=8, loose=4 | 10915 | 7 | 1559 |
| tight=10, loose=5 | 12965 | 7 | 1852 |
| tight=9, loose=4 | 12075 | 7 | 1725 |
| tight=8, loose=3 | 10332 | 7 | 1476 |
| tight=10, loose=3 | 12038 | 7 | 1720 |
| tight=9, loose=5 | 11389 | 7 | 1627 |
| tight=7, loose=3 | 8567 | 7 | 1224 |
| tight=12, loose=6 | 137 | 7 | 19.6 |

The Phase 4c CLAUDE.md requires: "GoF of primary configuration:
chi2/ndf < 3 (p > 0.01)." The primary configuration (tight=8, loose=4,
chosen as "best WP") has chi2/ndf = 1559. The only WP approaching
acceptable GoF is tight=12, loose=6 at chi2/ndf = 19.6 — still failing
the < 3 criterion by a factor of 6.5.

The artifact acknowledges this but frames it as expected. Per
`conventions/extraction.md`: "A configuration that produces a small
statistical uncertainty but poor GoF (chi2/ndf > 3) is not a stable
operating point — it indicates the model does not describe the data at
that configuration. When selecting among multiple configurations, the
selection criterion must balance precision and GoF. If the minimum-variance
configuration has poor GoF while other configurations have acceptable GoF,
the latter should be preferred unless the GoF failure is understood and
demonstrated not to bias the result."

**Finding [P2]:** The primary R_b configuration (tight=8, loose=4) has
chi2/ndf = 1559/7, failing the Phase 4c GoF gate by three orders of
magnitude. The tight=12, loose=6 WP is the only one with quasi-acceptable
chi2/ndf = 19.6/7, and gives R_b = 0.2159 consistent with SM. The artifact
does not explain why the WP with the best GoF (and best result) was not
chosen as primary. Instead, "best WP" is defined as "lowest statistical
uncertainty" — a criterion that actively selects the configuration with
the worst GoF. This reverses the GoF-informed selection rule from
the conventions. Category A — the selected primary WP is not the
GoF-optimal WP and the artifact does not demonstrate that the poor GoF
does not bias the result.

### 2.3 WP Stability Failure — Combined Result is Unreliable

From three_tag_rb_fulldata.json:
`"stability": {"chi2": 5453.7, "ndf": 7, "p_value": 0.0, "passes": false}`

The artifact combines R_b = 0.1898 from 8 WPs with chi2/ndf = 5454/7 as
if this is a valid combination. A combination with chi2/ndf = 779 per
degree of freedom is not a weighted average — the weights are statistically
meaningless when the measurements are inconsistent at this level. The
combined uncertainty (stat = 0.00013) is artificially small because
it does not account for the inconsistency.

The INFERENCE_OBSERVED.md Summary Table lists "R_b (combined, SF) = 0.1898
+/- 0.0001 (stat) +/- 0.018 (syst)" — but the stat uncertainty 0.0001
comes from the combination chi2 fit across 8 inconsistent WPs. The
true statistical uncertainty, using any single WP, is ~0.0004. The
factor-of-4 reduction from combination across inconsistent WPs is
statistically invalid.

**Finding [P3]:** The "combined" R_b stat uncertainty (0.0001) is
unreliable because it is derived from a combination across 8 WPs that
are mutually inconsistent by chi2/ndf = 779. The true R_b should be
reported from a single well-understood WP with its own statistical
uncertainty, not a combination inflated by systematics and averaged
across inconsistent configurations. Category A.

### 2.4 SF Calibration Circularity Concern

The SF calibration applies: SF_i = f_s_i(data) / f_s_i(MC) (single-tag
fractions data/MC). This SF is then applied to the MC efficiencies before
R_b extraction from the same data. There is a circularity question: the
SF is derived from the same data events that are then used in the
chi2 fit for R_b extraction. The SF is a linear correction to the
single-tag fractions, but the chi2 fit minimizes discrepancy in all 8
single + double tag fractions. If the SF correction absorbs part of the
R_b information from the single-tag fractions, the subsequent chi2 fit is
not fully independent of the calibration step.

The artifact does not address this. The conventions file states:
"Calibration independence is mandatory. Each calibration must come from
an observable that is independent of the primary result ... Deriving the
correction by assuming the primary result equals a reference value is
a diagnostic, not a calibration."

**Finding [P4]:** The SF calibration uses the same data events as the
R_b extraction. The single-tag fractions f_s_i(data) that define the
SF are part of the 8 observables used in the chi2 fit. This is a
partially circular calibration: SF forces f_s_i(SF-calibrated MC)
to equal f_s_i(data), which trivially reduces chi2 contribution from the
single-tag terms. The residual GoF failure (chi2/ndf = 1559) comes only
from the double-tag fractions. This makes the extraction not independent
of the calibration. The calibration independence requirement in
`conventions/extraction.md` is not satisfied. Category B — the circularity
is partial and the double-tag fractions remain as independent constraints,
but it inflates the apparent performance of SF calibration.

### 2.5 A_FB^b Cross-Kappa Combination Invalid

From the artifact:
"Cross-kappa combination: A_FB^b = -0.076 +/- 0.003, chi2/ndf = 36.15/3, p = 0.000"

A cross-kappa chi2/ndf = 36.15/3 = 12.05 (p ~ 0) means the four kappa
values give mutually inconsistent results. The kappa dependence spans
-0.097 (kappa=0.3) to -0.055 (kappa=2.0) — a factor of 1.8 difference.
This is not statistical variation; this is evidence of a systematic model
failure. Combining inconsistent measurements with a weighted average
when chi2/ndf >> 1 produces a meaningless central value with artificially
small uncertainty (0.003 stat from combination vs 0.005-0.006 per
individual kappa).

**Finding [P5]:** The A_FB^b cross-kappa combination is invalid. The four
kappa values are mutually inconsistent (chi2/ndf = 12). The combined
uncertainty (0.003) is smaller than any individual kappa uncertainty (0.005)
— a physical impossibility when the measurements are inconsistent. The
artifact should report the kappa=2.0 value (best GoF, lowest kappa
dependence sensitivity) as primary, and treat the kappa spread as a
systematic. The cross-kappa combination overestimates the precision by
at least a factor of 2. Category A.

### 2.6 Per-Year A_FB^b Shows Monotonic Trend — Not Examined

Per_year_results.json shows A_FB^b:
- 1992: -0.018
- 1993: -0.033
- 1994: -0.061
- 1995: -0.084

This is a monotonically increasing negative trend over the four years, not
consistent with random fluctuations around a fixed value. The
per-year chi2 = 3.82/3 (p = 0.28) passes, but this tests only whether
the year-to-year scatter is consistent with statistical uncertainties —
it does not test for a trend. A monotonic trend over 4 years with
sigma_stat ~ 0.025-0.028 per year represents a linear slope of
approximately -0.022 per year.

**Finding [P6]:** The per-year A_FB^b shows a monotonic decreasing trend
(1992 to 1995: -0.018, -0.033, -0.061, -0.084). This is not examined in
the artifact. A year-dependent systematic (e.g., changing detector
conditions, center-of-mass energy shift across years, evolving MC
year-coverage bias) could produce this trend. The chi2/ndf consistency
test passes because the absolute scatter is within sigma_stat, but the
trend itself is physically anomalous. Category B.

### 2.7 BDT Cross-Check is Not a Cross-Check

The BDT cross-check gives R_b values of 0.094–0.123 across thresholds
0.7–0.3. These are 40–57% below the SM value of 0.216, worse than the
cut-based result. The artifact explains: "BDT efficiencies are calibrated
using the cut-based truth proxy (threshold=10), which itself has the
data/MC mismatch."

This means the BDT cross-check is not independent: it uses the cut-based
result as its calibration input. A cross-check that depends on the primary
method is not a cross-check — it is a propagation of the primary result's
systematic.

**Finding [P7]:** The BDT cross-check is not independent of the cut-based
result (it is calibrated on it). This renders it useless as a validation.
The artifact should state explicitly that the BDT does not provide
independent cross-check capability given the calibration chain. Category B.

### 2.8 Phase 4c Escalation Check

Per CLAUDE.md Phase 4c: "Phase 4c escalation check: any result >2sigma
from expected triggers 4-bot." 

- R_b (combined full) = 0.1898 vs R_b (MC expected) = 0.2158:
  deviation = (0.1898 - 0.2158) / sqrt(0.018^2 + 0.065^2) = -0.026 / 0.068
  = -0.38 sigma in total uncertainty. But total uncertainty dominated by
  systematic — in stat uncertainty: (0.1898 - 0.2158) / 0.00013 = -200 sigma.

The escalation check should use the relevant uncertainty. If we compare
4c full data vs 4b 10% data at the same WP, the comparison chi2 is
reported in the JSON: `"pull": 32.56` (using stat only). This is vastly
>2 sigma.

If we compare to the MC expected (Phase 4a): pull = -62.1 (from JSON).

**Finding [P8]:** The Phase 4c escalation trigger has fired (R_b deviates
>2 sigma from Phase 4a expected when measured in stat uncertainty). The
artifact does not acknowledge the escalation trigger. Per CLAUDE.md, this
requires escalation from 1-bot to full 4-bot review. The orchestrator
must be informed. This review is written as the escalation response.
Category A — the escalation check was not formally evaluated in the
artifact.

### 2.9 Numerical Self-Consistency Checks

Spot-checking key values across sources:

**R_b (combined) — three sources:**
- INFERENCE_OBSERVED.md Table: R_b (combined, SF) = 0.1898
- parameters.json → R_b_fulldata_3tag_combined → value: 0.18982
- three_tag_rb_fulldata.json → stability → R_b_combined: 0.18982

These are consistent (0.1898 vs 0.18982, rounding). OK.

**R_b best WP stat uncertainty — two sources:**
- INFERENCE_OBSERVED.md: R_b (best WP) sigma_stat = 0.0004
- parameters.json → R_b_fulldata_3tag → stat: 0.00036
- three_tag_rb_fulldata.json → best_config → sigma_stat: 0.000365

The INFERENCE_OBSERVED.md rounds to 0.0004 but the true value is 0.00036.
Rounding error of 10% in stat uncertainty quoted in the summary table.

**eps_c systematic — two sources:**
- INFERENCE_OBSERVED.md Table: eps_c delta(R_b) = 0.01486
- systematics_fulldata.json → eps_c → delta_Rb: 0.014863
- parameters.json phase_4c section → eps_c → delta_Rb: 0.014863

Consistent. OK.

**A_FB^b combined systematic — two sources:**
- INFERENCE_OBSERVED.md Total systematic = 0.019
- parameters.json → A_FB_b_fulldata_final → syst: 0.01930
- systematics_fulldata.json → afb_total_syst: 0.01930

Consistent. OK.

**R_b total systematic — two sources:**
- INFERENCE_OBSERVED.md: Total systematic = 0.018
- parameters.json → R_b_fulldata_final → syst: 0.018115

Consistent. OK.

**A_FB^b combined stat — artifact vs JSON:**
- INFERENCE_OBSERVED.md: stat = 0.0026
- parameters.json → A_FB_b_fulldata_final → stat: 0.002641
- afb_fulldata.json reports per-kappa sigma values (0.005-0.006); the
  cross-kappa combination stat = 0.0026 would be sqrt(chi2/3 weighted
  inverse variance) — but chi2/ndf = 12 means this is not a valid
  combination stat.

The 0.0026 stat is from a chi2-minimization across 4 mutually inconsistent
kappa values and is physically unreliable (see Finding P5).

**R_b stat (combined) — artifact vs physical:**
- INFERENCE_OBSERVED.md: stat = 0.0001
- parameters.json: stat = 0.000134

As noted in Finding P3, this comes from combining across 8 inconsistent
WPs and is not physically meaningful.

**Finding [P9]:** The stat uncertainties for both "combined" quantities
(R_b = 0.0001, A_FB^b = 0.003 from cross-kappa) are derived from
inconsistent combinations and are not physically valid. The AN summary
table will misrepresent the precision of these measurements. Category A.

### 2.10 COMMITMENTS.md — Open Items Not Resolved

Reading COMMITMENTS.md, the following items remain open (not marked [x]
or [D]):

Cross-checks:
- [ ] Probability tag vs N-sigma tag comparison
- [ ] bFlag cross-check (our tagger vs bFlag in data)
- [ ] Constrained R_c vs floated R_c in double-tag fit
- [ ] Analytical vs toy-based uncertainty propagation comparison
- [ ] Simple counting A_FB^b vs self-calibrating fit

Validation:
- [ ] Data/MC agreement on all MVA inputs (BDT approach)
- [ ] bFlag interpretation validation
- [ ] d0 sign convention validation [D19]

Comparison targets:
- [ ] R_b vs ALEPH (hep-ex/9609005)
- [ ] R_b vs LEP combined (hep-ex/0509008)
- [ ] R_b vs SM
- [ ] A_FB^b vs ALEPH (inspire_433746)
- [ ] A_FB^{0,b} vs LEP combined
- [ ] sin^2(theta_eff) vs ALEPH

The Phase 4c CLAUDE.md completion criteria requires: "Update
COMMITMENTS.md — all lines should be [x] or [D]." This criterion is not
met. There are 13 open items.

**Finding [P10]:** COMMITMENTS.md has 13 unresolved items at the end of
Phase 4c. The completion criterion "all lines [x] or [D]" is violated.
In particular, the comparison targets (R_b vs ALEPH, R_b vs SM, etc.)
are listed as commitments but never formally evaluated in the artifact.
The artifact's Summary Table shows R_b = 0.190 vs SM 0.2158 but there
is no chi2/sigma evaluation. Category A.

### 2.11 D19 Validation Gate Not Cleared

COMMITMENTS.md [D19]: "Phase 3 gate: d0 sign convention validation
(positive d0 tail enhanced in b-enriched hemispheres)." This is listed
as `[ ]` — never completed. It was supposed to be a Phase 3 blocking gate.

**Finding [P11]:** The d0 sign convention was never validated at Phase 3
and remains unverified at Phase 4c. Given that A_FB^b has the wrong sign
(Finding P1), the d0 sign convention validation is now urgently relevant.
If the d0 sign convention is inverted, b-tagged events would preferentially
fall in the wrong hemisphere, inverting the observed asymmetry. Category A.

### 2.12 MC Year Coverage Systematic Underestimated

The MC covers only 1994 while data spans 1992-1995. The Phase 4c artifact
adds `mc_year_coverage` systematic: delta(R_b) = 0.0005, "Estimated from
per-year SF variation."

From per_year_results.json, the per-year scale factors (sf_tight) are:
- 1992: 0.932
- 1993: 1.006
- 1994: 0.959
- 1995: 1.014

The 1992 scale factor (0.932) is notably lower than the others, suggesting
a genuine year-dependent efficiency difference. The spread is 0.932–1.014,
a range of 0.082. Yet the mc_year_coverage systematic is 0.0005 on R_b —
far smaller than would be implied by a 8% SF range. The per-year R_b
values are 0.185–0.189 (range 0.004), all relative to MC-calibrated
efficiencies that are valid for 1994 only.

**Finding [P12]:** The mc_year_coverage systematic (0.0005) appears
underestimated given the per-year SF spread (0.932–1.014 in sf_tight).
A 2.7% SF difference between years (worst case 1992 vs 1995) at
epsilon_b_tight ~ 0.485 translates to a non-trivial R_b shift, likely
~0.002-0.005 rather than 0.0005. No calculation is shown. Category B.

### 2.13 chi2_calibration Numerically Zero in MC Extraction

From three_tag_rb_fulldata.json, every working point shows:
`"chi2_calibration": ~4e-10, "ndf_calibration": 2`

This is the MC internal calibration chi2 (deriving MC efficiencies from
MC counts). chi2 ~ 0 is the triviality alarm from Finding V2. The
calibration chi2 is zero because the MC efficiency is derived by inverting
the same system that generates the calibration counts. This is the
self-consistent extraction pitfall documented in `conventions/extraction.md`.

However, this is expected for the MC calibration step (not the data
extraction step). The data extraction chi2 is 10000+, which captures the
data/MC mismatch. The concern is that the MC "closure" was used to validate
the method (Phase 4a), and that closure is tautological.

### 2.14 Completeness Cross-Check vs Phase Requirements

Required deliverables vs produced:

| Requirement | Status |
|-------------|--------|
| Full dataset processed (2887261 events) | Done |
| Systematics re-evaluated on full data | Partial — sigma_d0 and sigma_d0_form remain scaled estimates |
| GoF check with p-value | Done (chi2/ndf documented, all failing) |
| Comparison to Phase 4b and 4a with figures | calibration_progression.pdf exists |
| Viability check (total unc documented) | Done (R_b: 9.6%, A_FB: 25.8%) |
| All figures saved AND registered in FIGURES.json | Done (6 figures, all on disk) |
| Results JSON updated | Partial (validation.json not updated — V1) |
| COMMITMENTS.md fully resolved | NOT done (13 open items — P10) |
| Every finding has Resolution + Evidence section | NOT done (F3 missing — V6) |

3 of 9 completion criteria are not met. Category A.

### 2.15 Validation.json — Phase 4a Values Stale at Phase 4c

Specific stale values in `validation.json`:
- `precision_comparison.R_b_vs_ALEPH.our_total = 0.065` (Phase 4a)
  vs Phase 4c value 0.018 — factor 3.6 stale
- `operating_point_stability.chi2 = 8e-10` (Phase 4a MC)
  vs Phase 4c chi2 = 5454 — stale by 13 orders of magnitude
- The `independent_closure_3tag` section contains only Phase 4a MC
  configs, not Phase 4c results

A reviewer reading `validation.json` would conclude the analysis has:
- chi2/ndf ~ 0 (perfect stability)
- Precision within 47x of ALEPH

Neither reflects the Phase 4c reality (chi2/ndf = 779, precision 13x).

### 2.16 Adversarial Check — Rationalizations

The artifact contains several rationalization patterns to flag:

**"This validates the SF calibration approach" (F1):** The tight=12 WP
giving R_b = 0.2159 is presented as validation. But this WP has
chi2/ndf = 19.6 — still failing the Phase 4c GoF requirement. The
assertion that one WP (out of 8) happening to agree with SM "validates"
the approach is not rigorous. It could equally be argued that this WP
accidentally agrees due to a balance of biases at that threshold.

**"SF calibration systematically improves R_b" (Section 2):** The SF
improves R_b from raw (0.17) to SF-calibrated (0.19) but the improvement
is insufficient (SM = 0.216). Framing partial correction as "systematic
improvement" is technically accurate but obscures that the method is
still substantially biased.

**"Expected given data/MC mismatch" (Section 8):** The GoF failures are
rationalized as expected. But chi2/ndf = 1559 is not expected from
moderate data/MC differences — it indicates either (a) the model is
completely wrong for these data, (b) the uncertainty on the observables
is badly underestimated, or (c) there is a structural problem in the
chi2 formulation. The artifact does not investigate these alternatives.

---

## 3. Summary of All Findings

### Category A — Must Resolve

| ID | Finding | Location |
|----|---------|---------|
| V1 | validation.json not updated for Phase 4c; stale Phase 4a values | validation.json |
| V2 | Fit triviality gate not cleared; MC chi2 = 0 is algebraic artifact | validation.json, INFERENCE |
| V3 | No Phase 4c independent closure/stress test on full data | INFERENCE Section 5+ |
| V4 | sigma_d0 and sigma_d0_form are flat estimates, not propagated | systematics_fulldata.json |
| V6 | F3 (wrong-sign A_FB^b) lacks Resolution + 3 remediation attempts | INFERENCE Section 3 |
| P1 | A_FB^b = -0.076 is -9.3σ from SM; sign error not excluded | INFERENCE Section 3 |
| P2 | Primary WP (tight=8,4) chi2/ndf = 1559; GoF gate violated | INFERENCE Section 2 |
| P3 | Combined R_b stat = 0.0001 invalid (combination of inconsistent WPs) | INFERENCE Table |
| P5 | Cross-kappa A_FB^b combination invalid; chi2/ndf = 12 | INFERENCE Section 3 |
| P8 | Escalation trigger fired; 4-bot review required (>200σ from 4a) | COMMITMENTS, CLAUDE.md |
| P9 | Physically invalid "combined" stat uncertainties in summary table | INFERENCE Summary |
| P10 | COMMITMENTS.md: 13 open items; completion criterion violated | COMMITMENTS.md |
| P11 | D19 (d0 sign convention) never validated; critical given wrong-sign AFB | COMMITMENTS.md |

### Category B — Should Address

| ID | Finding | Location |
|----|---------|---------|
| V5 | Precision comparison not updated; 12.9x gap vs ALEPH unexplained | validation.json |
| P4 | SF calibration partially circular (same data for calibration and fit) | INFERENCE Section 2 |
| P6 | Per-year A_FB^b shows monotonic trend not examined | per_year_results.json |
| P7 | BDT cross-check not independent; cannot serve as cross-check | INFERENCE Section 6 |
| P12 | MC year coverage systematic (0.0005) likely underestimated given SF spread | systematics.json |

### Category C — Suggestion

| ID | Finding |
|----|---------|
| C1 | INFERENCE Summary Table should note that "best WP" criterion (lowest stat) conflicts with GoF criterion |
| C2 | BDT cross-check should be relabelled as "BDT diagnostic" since it is calibrated on the cut-based result |
| C3 | FIGURES.json descriptions should note which figure supports each completion criterion |

---

## 4. Escalation Assessment

Per CLAUDE.md Phase 4c: "any result >2-sigma from expected triggers 4-bot."

From three_tag_rb_fulldata.json `comparison_4a.pull = -62.1` (stat).
From three_tag_rb_fulldata.json `comparison_4b.pull = +32.6` (stat).

**Both escalation triggers have fired.** The escalation from 1-bot to full
4-bot review is mandatory. The most critical issue requiring 4-bot
attention is Finding P1: the wrong sign of A_FB^b, with Findings P2/P3/P5
as immediate follow-on. The orchestrator must be notified.

Additionally, D19 (sign convention validation — Finding P11) was a Phase 3
blocking gate that was never executed. This is a process violation that
predates Phase 4c and should trigger a regression investigation.

---

## 5. Verdict

**Classification: A (Must Resolve — 13 Category A findings)**

The Phase 4c artifact cannot advance to Doc 4c in its current state.
The most urgent issues are:

1. **Wrong sign of A_FB^b** — quantitative explanation required or sign
   error must be excluded by tracing the hemisphere charge sign convention
   end-to-end through the code.
2. **D19 (d0 sign validation) gap** — this Phase 3 blocking gate was never
   executed; escalation to regression investigation required.
3. **GoF failure at all WPs** — the primary WP has chi2/ndf = 1559; the
   GoF-optimal WP (tight=12,6) should be investigated as a possible
   primary.
4. **Invalid combinations** — both combined R_b (chi2/ndf = 779) and
   combined A_FB^b (chi2/ndf = 12) produce meaningless central values
   and misleadingly small stat uncertainties.
5. **Validation infrastructure** — validation.json was never updated for
   Phase 4c; COMMITMENTS.md has 13 open items.

MCP_LEP_CORPUS = true. Corpus calls were not needed for this review —
the issues are internal consistency failures that do not require reference
comparison to diagnose.
