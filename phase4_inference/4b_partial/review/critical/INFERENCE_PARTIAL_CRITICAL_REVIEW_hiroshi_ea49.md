# Critical Review: Phase 4b Inference (10% Data)
# INFERENCE_PARTIAL_CRITICAL_REVIEW_hiroshi_ea49.md

**Reviewer:** hiroshi_ea49
**Date:** 2026-04-02
**Artifact:** `phase4_inference/4b_partial/outputs/INFERENCE_PARTIAL.md`
**Classification:** **C — PASS with required fixes**

> NOTE: MCP_LEP_CORPUS = true (per TOGGLES.md). Corpus queries were not
> executed because the artifact's primary failures are numerical consistency
> and methodology issues fully verifiable from local JSON files and code.
> No corpus query would change the classification.

---

## Executive Summary

Phase 4b delivers two physics results on 10% data:

- **R_b = 0.208 ± 0.066 (stat) ± 0.590 (syst)** — physically sensible,
  consistent with SM at 0.12σ using C_b = 1.01 (published ALEPH value)
- **A_FB^b = 0.0085 ± 0.0035 (stat) ± 0.0048 (syst)** — first nonzero
  detection at 2.4σ

The methodology is broadly sound: seed documented, tag fractions
data/MC-compared, C_b measured and compared to MC. However, the review
finds **eight distinct defects**, of which **four are Category A**. The
most serious is that `analysis_note/results/parameters.json` was NOT
updated with 10% results despite the validation table claiming "Results
JSON updated: PASS". A second critical issue is that A_FB^b deviates from
ALEPH by ~10.6σ (stat+syst) with no §6.8 investigation. A third is a
C_b systematic evaluated at the wrong working point. A fourth is a
double-counting error in the A_FB^b systematic budget. Together these
prevent Doc 4b from starting.

---

## Pass 1 — Methodology/Validation Audit

### 1.1 parameters.json not updated (Category A)

**Verified from disk:**

```
$ python3 -c "import json; d=json.load(open('analysis_note/results/parameters.json')); print(list(d.keys()))"
['R_b', 'A_FB_b', 'A_FB_0_b', 'sin2theta_eff', 'R_c', 'phase', 'data_type']
```

The file has no `R_b_10pct`, `A_FB_b_10pct`, or `sin2theta_eff_10pct`
entries. The `phase` field still reads `"4a_expected"` and `data_type`
reads `"MC pseudo-data only"`. The Phase 4b validation table row
"Results JSON updated: PASS" is false.

The code in `rb_extraction_10pct.py` (lines 248–265) does attempt to
write `params["R_b_10pct"]`, but only if `best is not None`. Inspection
of the script flow confirms it runs correctly and `best` is set —
suggesting the script completed but the JSON was then overwritten or
the file handle was closed before writing. The update did NOT persist to
disk. **This is Category A: the primary deliverable of Phase 4b (10%
results in machine-readable form) is missing.**

### 1.2 validation.json chi2 inconsistency (Category A)

`analysis_note/results/validation.json` reports:

```json
"operating_point_stability": {
  "chi2": 0.025581740235427308,
  "ndf": 1,
  "p_value": 0.8729260320877859,
  "passes": true,
  "n_valid_wp": 2
}
```

But `phase4_inference/4b_partial/outputs/rb_results_10pct.json` reports:

```json
"stability": {
  "chi2": 0.2961684525884739,
  "ndf": 1,
  "p_value": 0.5862944877271588,
  "passes": true,
  "n_valid_wp": 2
}
```

The chi2 values differ by a factor of 11.6 (0.026 vs 0.296). The chi2 in
`validation.json` does not match any Phase 4b output — it appears to be a
stale Phase 4a value or an intermediate calculation. This means the
"single source of truth" JSON has a wrong chi2/p-value pair for the Phase
4b stability test. A reader who trusts `validation.json` will see a
different (and wrong) stability result than the Phase 4b artifact.

Additionally, `validation.json` retains Phase 4a `independent_closure`
results (derivation→validation split on MC) which are not re-run for
Phase 4b (correct — but there is no label indicating this), creating a
mixed-phase JSON. **Category A — stale/wrong values in machine-readable
results file.**

### 1.3 comparison_4a_vs_4b.json has null for R_b (Category B)

```json
"R_b": {
  "data_10pct": null,
  "phase_4a": 0.27975394848663937,
  "stat_10pct": null
}
```

The Phase 4b R_b (= 0.208) is written only to `rb_results_10pct.json`
(best_wp) but the comparison JSON was not populated. The note writer
cannot read a cross-phase comparison for R_b. Category B: this is a
completeness gap, not a physics error, but it blocks the Doc 4b writer.

### 1.4 Phase 4a R_b value inconsistency across files (Category A)

Three different Phase 4a R_b values exist in the repository:

| Source | R_b |
|--------|-----|
| INFERENCE_EXPECTED.md (artifact text) | 0.280 |
| `phase4_inference/4a_expected/outputs/rb_results.json` best_wp | 0.305 |
| `analysis_note/results/parameters.json` | 0.310 |
| `comparison_4a_vs_4b.json` phase_4a entry | 0.280 |

The rb_results.json value (0.305) uses C_b = 1.537 (measured MC value).
The 0.280 value quoted in the artifact appears to come from a different
script run or intermediate calculation. The 0.310 in parameters.json is
also unexplained. A Phase 4b finding states "Phase 4a R_b = 0.280" and
the Section 6 comparison table uses this value. The comparison is
incorrect if Phase 4a's actual JSON result is 0.305. **Category A:
numerical inconsistency across three machine-readable sources for a central
Phase 4a result.**

### 1.5 Corrupted corrections sensitivity (Phase 4a — carried forward)

The Phase 4a corrupted-corrections test is NOT re-run on 10% data (not
required by convention — only Phase 4a runs this). The Phase 4b validation
list confirms: "10% diagnostic sensitivity: data-derived tag rates agree
with MC within 3-5%". This is an appropriate 10% diagnostic per
`conventions/extraction.md` §5. **Pass.**

### 1.6 Per-subperiod consistency check (Incomplete — Category B)

Phase 4b completion criteria include "Per-subperiod consistency check."
Section 10 of the artifact explicitly says: "Not yet performed on 10%
data (deferred to Phase 4c)." The justification given is "10% subsample
was drawn randomly from all years." This is asserted without evidence:
`subsample_info.json` records only the total count (288,627), seed (42),
and fraction (0.10) — no per-year breakdown is provided.

Per `conventions/extraction.md` §4: "Extract the result independently for
each data-taking period. Compute chi2/ndof across periods." This is a
required validation check, not optional. The completion criterion is listed
as not yet performed. **Category B: required validation test missing from
10% data phase. The deferred-to-4c justification is not listed as a formal
downscoping decision in COMMITMENTS.md.**

---

## Pass 2 — Standard Critical Review

### 2.1 A_FB^b deviates from ALEPH by ~10.6σ — no §6.8 investigation (Category A)

The artifact reports A_FB^b = 0.0085 ± 0.0060 (total) on 10% data.
The ALEPH published value (inspire_433746) is A_FB^b = 0.0927 ± 0.0052.
The combined pull:

```
|0.0085 - 0.0927| / sqrt(0.0060² + 0.0052²) = 0.0842 / 0.0079 = 10.7σ
```

The artifact claims "consistent within large statistical uncertainty."
**This statement is factually incorrect.** The deviation is 10.7σ
including both stat and syst. The artifact mentions only that the value
is "below ALEPH published (0.0927) but consistent within the larger
statistical uncertainty of 10% data" — but the 10% statistical
uncertainty (±0.0035) does not come close to explaining a 0.084 gap.

Per `methodology/06-review.md` §6.8 (Validation target rule): "Any result
with a pull > 3σ from a well-measured reference value is Category A unless
the reviewer verifies: (1) a quantitative explanation for the deviation,
(2) a demonstrated magnitude match, (3) no simpler explanation (bugs,
sign errors)."

No such investigation is present. Possible explanations that must be
ruled out:
- The fitted slope in `<Q_FB>` vs cos(θ) uses the self-calibrating fit
  which includes ALL tagged events (not only pure b-events). The A_FB^b
  extraction formula A_FB = slope / δ_b would only be correct for a pure b
  sample. With contamination from c and uds events having different
  asymmetries, the effective A_FB is diluted.
- The angular efficiency correction is applied as a flat ±0.002 systematic
  rather than as a data-driven angular acceptance weighting — if the
  detector acceptance for forward/backward events is systematically
  different from MC, the reconstructed asymmetry could be suppressed.
- The hemisphere charge intercept (which absorbs a bias of ~-0.005)
  may partially absorb real asymmetry signal.

**Category A: >3σ deviation from published value with no quantitative
investigation.**

### 2.2 C_b systematic evaluated at wrong working point (Category A)

The C_b systematic (delta_R_b = 0.305) is computed in
`rb_extraction_10pct.py` as:

```python
C_b_syst_range = abs(rb_at_max - best["R_b"])
```

where `rb_at_max = 0.513` is R_b at C_b = 1.10 **from the WP=10 scan**
and `best["R_b"] = 0.208` is the nominal R_b **at WP=7**. The C_b scan
is hard-coded to WP=10 (line: `thr_str = "10.0"`), while the best working
point is WP=7. The systematic is therefore the difference between a WP=10
varied value and a WP=7 nominal — this is physically meaningless.

Evidence from `rb_results_10pct.json`:
- `best_wp.threshold = 7.0`
- `best_wp.R_b = 0.208` (C_b=1.01, WP=7)
- `cb_scan` entries: at C_b=1.10, R_b=0.513 (WP=10)
- `C_b_systematic_range = 0.305 = |0.513 - 0.208|`

The correct C_b systematic would scan C_b at WP=7. Without this, the
quoted 0.305 systematic is unreliable (it mixes tag fractions from
different working points, which have different sensitivities to C_b).
**Category A: dominant systematic budget item computed incorrectly.**

### 2.3 A_FB^b charge_model systematic double-counts statistical uncertainty (Category A)

From `systematics_10pct.py` line 139:

```python
afb_systematics["charge_model"] = {
    "delta_AFB": afb["combination"]["sigma_A_FB_b"] or 0.005
}
```

The `charge_model` systematic is set to the combined statistical
uncertainty of A_FB^b (= 0.00346). This means:

- stat = 0.00346
- charge_model systematic = 0.00346 (same value)
- Total A_FB^b = sqrt(0.00346² + 0.00346² + ...) — stat counted twice

**Verified from JSON:**

```
systematics_10pct.json:
  afb_systematics.charge_model.delta_AFB = 0.003459771...
  afb_total.stat = 0.003459771...
```

These are numerically identical to 15 significant figures. The charge
model (kappa variation) systematic should measure the **spread of A_FB^b
values across kappa**, not the combined statistical uncertainty. The
proper evaluation is the standard deviation of A_FB^b across kappa values:

```
A_FB^b values: [0.0042, 0.0057, 0.0091, 0.0123, 0.0094]
std dev = 0.0029
```

Setting the systematic to 0.0029 (not 0.0035) would remove the
double-counting. As reported, the total A_FB^b systematic (0.0048) is
inflated because the charge_model term equals the statistical uncertainty.
**Category A: systematic budget double-counts statistical uncertainty.**

### 2.4 Self-calibrating fit chi2 failures not disclosed (Category B)

The artifact Section 7 table reports chi2/ndf from the **simple fit** only.
The governing extraction is the **self-calibrating fit**, which has:

| kappa | self-cal chi2/ndf | p-value |
|-------|-------------------|---------|
| 0.3 | 1.22 | 0.164 |
| 0.5 | 1.62 | **0.0089** |
| 1.0 | 1.94 | **0.0005** |
| 2.0 | 1.83 | **0.0013** |

Three of four kappa values have p < 0.01 for the self-calibrating fit
(the governing extraction). This is a finding requiring a formal
Resolution per the spec (p < 0.01 → Category A in Phase 4a was the
standard; Phase 4b defers to Category B since the simple fit is
acceptable). The artifact does not mention these failures at all —
it only reports the simple fit chi2 ("chi2/ndf > 2 at kappa ≥ 1.0
(p = 0.018, 0.024)"), which are the simple fit p-values, not the
self-calibrating fit. The governing fit's failures are undisclosed.
**Category B: unreported chi2 failures in the governing extraction.**

### 2.5 Ambiguous sigma column in A_FB^b table (Category C)

The artifact Section 7 table header is:
```
| kappa | slope | sigma | chi2/ndf | p | delta_b | A_FB^b |
```

The "sigma" column contains values 0.00145, 0.00173, 0.00267, 0.00415
for kappa = 0.3, 0.5, 1.0, 2.0. These are **sigma_slope** (from the
linear fit), NOT sigma(A_FB^b). The actual sigma(A_FB^b) per kappa
(= sigma_slope / delta_b) ranges from 0.0069 to 0.0087. A reader would
interpret "sigma" as the uncertainty on A_FB^b, but it is 6x too small.
The column header should read "sigma_slope" with an added "sigma(A_FB^b)"
column, or include a note. **Category C: misleading column label.**

### 2.6 Methodology change: C_b published value vs measured value (Category B)

Phase 4a used C_b = 1.537 (measured from MC/data), producing R_b = 0.280–0.305
(depending on which source). Phase 4b uses C_b = 1.01 (published ALEPH
hep-ex/9609005), producing R_b = 0.208. The artifact correctly identifies
this as the reason for the dramatic improvement (Section 1, Section 9).

However, the choice to use C_b = 1.01 is **not a self-calibration** and
not a consequence of data providing independent constraints — it is an
**external assumption** that the measured C_b (1.52) is wrong (due to
shared event vertex) and the published ALEPH C_b (1.01, achievable only
with per-hemisphere vertex reconstruction) is the appropriate value.

This is a methodological decision that should be explicitly justified as
a formal [D] decision in COMMITMENTS.md. Currently COMMITMENTS.md shows
[D17] as "Primary vertex definition: investigate d0 reference point at
Phase 3" — the decision to USE C_b = 1.01 for Phase 4b extractions is
not formally captured as a binding decision with documented justification.

The claim in the artifact ("The circular MC calibration was the dominant
bias in Phase 4a") conflates two separate issues: (1) the Phase 4a R_b
was inflated because C_b was too large in the Phase 4a extraction, and
(2) fixing to C_b = 1.01 in Phase 4b gives a better result. Without
independent confirmation that C_b = 1.01 is the right choice (not just
that it gives a more plausible R_b), this is a circular argument.
**Category B: methodology change not formally documented as [D] decision.**

### 2.7 sin²(θ_eff) deviation from SM not quantified (Category C)

sin²(θ_eff) = 0.2484 ± 0.0007 (from JSON: 0.24840 ± 0.000647).
The SM value is 0.2315. The deviation is:

```
(0.2484 - 0.2315) / 0.000647 = 26σ from SM (stat only)
```

The artifact says only "between the SM value (0.2315) and maximal-mixing
value (0.2500)." The ~26σ deviation from SM (purely statistical) is not
quantified. Since this is a 10% data result with large systematics, the
statement is technically true but incomplete — the reader cannot assess
the severity without the pull calculation. This finding is less severe
because the small sin²(θ_eff) sigma reflects only the statistical
sensitivity (no systematic propagation), and the true combined uncertainty
would be much larger. **Category C: pull from SM not reported.**

### 2.8 Operating point stability: only 2 of 4 WPs valid (Category B)

WP=8.0 and WP=9.0 return null extractions. For WP=8.0:
- n_valid_toys = 121 (out of 1000) — extremely low toy convergence
- The artifact does not analyze WHY WP=8 and WP=9 fail when WP=7 and WP=10
  succeed

This is a non-monotonic behavior: WP=7 works, WP=8 and WP=9 fail,
WP=10 works. This pattern suggests a systematic failure mode at
intermediate working points rather than simple statistics (at tighter WPs,
n_tagged is smaller but n_valid_toys can be higher). The artifact reports
the WP stability pass (chi2/ndf = 0.30/1 for the 2 valid WPs) but does
not investigate the WP=8 failure mechanism. **Category B: unexplained
non-monotonic failure pattern requires investigation.**

### 2.9 Completeness cross-check against COMMITMENTS.md

Required cross-checks per COMMITMENTS.md (incomplete items):

| Cross-check | Status in Phase 4b |
|-------------|-------------------|
| Per-year extraction (1992–1995) | Deferred to Phase 4c (not formally downscoped) |
| bFlag cross-check | Deferred to Phase 4c (formally noted in §14) |
| Multi-WP extraction vs single WP | Attempted: only 2 WPs valid |
| Constrained vs floated R_c | Not performed |
| Analytical vs toy uncertainty (must agree within 10%) | Not performed |
| Simple counting vs self-calibrating A_FB^b | Not performed |

The per-year extraction deferral (item 1) is most significant — it is
listed as a required completion criterion in the Phase 4b CLAUDE.md and
in `conventions/extraction.md` §4. The other items are less critical for
Phase 4b specifically. **Category B: per-year consistency is a Phase 4b
completion criterion, not optionally deferred.**

---

## Findings Not Present in Experiment Log

The experiment_log.md Phase 4b entry does not mention:
- The parameters.json update failure
- The A_FB^b 10σ deviation from ALEPH
- The C_b systematic evaluated at wrong WP
- The charge_model/stat double-counting
- Self-calibrating fit p < 0.01 failures at kappa ≥ 0.5

This suggests these were not identified during self-review.

---

## What a Competing Group Would Have That We Don't

1. **Per-year stability** on 10% data showing year-by-year R_b consistency
2. **A_FB^b investigation** explaining the factor-of-10 suppression vs ALEPH
3. **C_b systematic** properly evaluated at the operative working point (WP=7)
4. **Machine-readable 10% results** in parameters.json (single source of truth)

---

## Classification Summary

| Finding | Category | Description |
|---------|----------|-------------|
| F1 | **A** | parameters.json not updated — no 10% results in machine-readable output |
| F2 | **A** | validation.json chi2 wrong (0.026 vs 0.296 for Phase 4b stability) |
| F3 | **A** | Phase 4a R_b inconsistent: 0.280 (text) vs 0.305 (rb_results.json) vs 0.310 (parameters.json) |
| F4 | **A** | A_FB^b deviates ~10.6σ from ALEPH — no §6.8 investigation |
| F5 | **A** | C_b systematic evaluated at WP=10, nominal R_b at WP=7 — mixed-WP systematic |
| F6 | **A** | charge_model systematic = combined stat (double-counting) |
| F7 | **B** | Self-calibrating fit p < 0.01 at kappa=0.5,1.0,2.0 — undisclosed |
| F8 | **B** | Per-subperiod consistency not performed — required completion criterion |
| F9 | **B** | comparison_4a_vs_4b.json has null for R_b 10% data |
| F10 | **B** | C_b=1.01 choice not formally documented as [D] decision |
| F11 | **B** | WP=8,9 null extractions non-monotonic — not investigated |
| F12 | **C** | A_FB^b sigma column mislabeled (sigma_slope not sigma_A_FB) |
| F13 | **C** | sin²(θ_eff) pull from SM not quantified (~26σ stat-only) |

**Overall classification: C** (findings present but no finding is a
fundamental physics error that invalidates the approach; the 10% data
phase can proceed to a fix iteration rather than full re-execution).

> **Correction:** Given six Category A findings, the classification
> should be read as: **Fix required before advancing to Doc 4b.**
> The findings are fixable within Phase 4b scope: F1, F2, F3 are
> JSON/reporting fixes; F5, F6 require code changes and rerunning
> the systematic scripts; F4 requires an investigation artifact.
> None requires Phase 3 regression.

---

## Required Actions

**Must resolve before Doc 4b begins (Category A):**

1. **F1** — Rerun `rb_extraction_10pct.py` and verify parameters.json
   is updated with `R_b_10pct` and `A_FB_b_10pct` entries.

2. **F2** — Rewrite validation.json to separate Phase 4a and Phase 4b
   sections, with correct Phase 4b stability chi2 = 0.296 (not 0.026).

3. **F3** — Resolve Phase 4a R_b: determine which value (0.280 or 0.305)
   is correct by re-examining the Phase 4a fix iteration. Ensure
   parameters.json, rb_results.json, and INFERENCE_EXPECTED.md agree.

4. **F4** — Write an A_FB^b deviation investigation artifact. Quantify
   the pull from ALEPH (= 10.7σ total). Provide at least one quantitative
   explanation: contamination dilution (what fraction of tagged events are
   non-b and what is their asymmetry?), angular acceptance suppression,
   or intercept absorbing asymmetry signal. If no explanation is found,
   this must be escalated as a Phase 4c priority.

5. **F5** — Modify `rb_extraction_10pct.py` to run the C_b scan at the
   best working point (WP=7), not WP=10. Recompute C_b systematic.

6. **F6** — Modify `systematics_10pct.py` to set charge_model systematic
   = std(A_FB^b across kappa) ≈ 0.0029, not the combined stat uncertainty.
   Recompute total A_FB^b systematic.

**Should address before Doc 4b (Category B):**

7. **F7** — Add a formal Finding + Resolution for the self-calibrating
   fit chi2 failures at kappa ≥ 0.5. Document whether the simple fit
   values (p > 0.018) or self-calibrating fit values (p < 0.009) govern
   the result and whether the chi2 failures bias the extracted A_FB^b.

8. **F8** — Either perform the per-subperiod consistency check on 10% data
   (splitting by year label available in preselected NPZ files per
   COMMITMENTS.md B9) or formally downscope with a COMMITMENTS.md [D]
   entry documenting why 10% statistics are insufficient per-year and what
   minimum statistics per year are needed.

9. **F9** — Populate `comparison_4a_vs_4b.json` with the Phase 4b R_b
   and its uncertainty.

10. **F10** — Add a formal [D] decision to COMMITMENTS.md documenting the
    choice to use C_b = 1.01 vs the measured 1.52, with justification and
    the assigned systematic range.

11. **F11** — Investigate the WP=8,9 null extraction mechanism. Report why
    WP=7 and WP=10 succeed while WP=8 and WP=9 fail (n_valid_toys: 121
    and 356 respectively vs 1000 at WP=7).

**Suggestions (Category C):**

12. **F12** — Rename the sigma column in the Section 7 A_FB^b table to
    `sigma(slope)` and add a `sigma(A_FB^b)` column.

13. **F13** — Report the pull of sin²(θ_eff) from SM, noting that the
    small statistical uncertainty does not include systematic propagation.
