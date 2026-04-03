# Session Log — plot_validator hana_fccb

**Date:** 2026-04-02  
**Role:** Plot validator (Level 3)  
**Phase:** phase3_selection  
**Model:** claude-sonnet-4-6

---

## Session Timeline

### 09:00 — Session start

Read `agents/plot_validator.md` to confirm role definition and checklist requirements. Confirmed the three-step pipeline: registry check, code lint, visual review.

### 09:05 — Step 1: Figure Registry Check

Ran Python script to validate FIGURES.json:
- 20 entries, 20 PNGs on disk — exact match, no orphans or missing files.
- All required fields present in all entries.
- All `type` values valid (`diagnostic`, `data_mc`, `result`, `closure`).
- All `lower_panel` values valid (`pull`, `none`).
- Staleness check: all figures are current — script mtime in registry matches filesystem mtime within 2 s, and all figures were created after the registered script mtime.

**Result: PASS — no registry findings.**

### 09:10 — Step 2: Code Lint

Grepped all 13 Python scripts in `phase3_selection/src/` for all forbidden patterns. All eight primary checks returned NONE. Additional verification:
- `bbox_inches="tight"` present at every `savefig`.
- `hspace=0` correctly set in both plot modules.
- Experiment label applied consistently via `exp_label_data` helper.
- MC normalization label correct: "MC (normalized to data)".
- Lower panel uses "Pull" label, not "Ratio" or "Data/MC".
- `plot_utils.py` exists and is imported.

Two Category C warnings noted: `mc_scale_to_data=True` applied to derived quantities, and pull denominator double-counts statistical uncertainty. Both non-blocking.

**Result: PASS with 2 Category C warnings — no Category A or B violations.**

### 09:20 — Step 3: Visual Review

Read all 20 PNGs. Key findings during visual inspection:

**Critical discovery — rb_operating_scan:** The R_b operating scan showed extracted values between 0.48 and 0.98 across tag thresholds 1–14. The SM and ALEPH reference values (~0.216) appear as faint lines at the bottom of the figure. This is a 3–5× discrepancy. Investigated by reading `src/double_tag_counting.py` and `outputs/rb_scan.json`:
- At threshold 5 (chosen working point), f_s = 0.420 and f_d = 0.207.
- The extract_rb function uses eps_c=0.05 and eps_uds=0.005 as nominal constants.
- These background efficiency assumptions are not calibrated to the actual tagger performance. Given f_s=42% at threshold 5, this is clearly not a b-pure tagger — the background terms are underestimated, causing eps_b and R_b to be overestimated.
- Confirmed: background efficiency nominal values (5% charm tag rate, 0.5% light-flavor mistag) are standard industry estimates that may not reflect this tagger's actual performance on ALEPH open data.

**Second critical finding — closure test figure text artifact:** The closure test figure has overlapping annotation text in the upper-left corner. The two text strings ("Pull=..." and "Ratio=...") are rendered at the same position, producing garbled output.

**Three label violations (Category A):** Figures 1 (cutflow), 2 (d0 sign validation), and 3 (sigma_d0 calibration) all have code-style variable names in axis labels.

**d0 sign validation concern:** The b-enriched (bFlag=4) and all-events curves are nearly indistinguishable, when physically they should differ (b-enriched should show higher positive asymmetry). This may indicate bFlag=4 is not isolating a substantially different sample composition.

**Closure test physics concern:** The contamination injection test shows a 2.15 ratio (observed/predicted), which is labeled PASS. At R_b~0.82 (not physical), the closure is internally self-consistent but does not validate the physics formula.

### 09:50 — Report writing

Wrote validation report to `phase3_selection/review/validation/SELECTION_PLOT_VALIDATION_hana_fccb_2026-04-02.md`.

---

## Key Findings Summary

| Severity | Count | Description |
|----------|-------|-------------|
| RED FLAG | 1 | R_b scan shows 3–5× discrepancy from SM at all operating points |
| Category A | 5 | Label violations (3) + closure text artifact (1) + closure physics (1) |
| Category B | 3 | Missing threshold line, mixed closure metrics, indistinguishable scan curves |
| Category C | 2 | MC normalization for derived quantities, pull denominator double-counting |
| PASS | 12 | 12 of 20 figures pass all checks |

---

## Files Read

- `agents/plot_validator.md`
- `phase3_selection/outputs/FIGURES.json`
- `phase3_selection/src/plot_all.py` (lint + context)
- `phase3_selection/src/double_tag_counting.py` (R_b formula investigation)
- `phase3_selection/outputs/closure_results.json` (closure test values)
- `phase3_selection/outputs/rb_scan.json` (R_b scan values)
- `phase3_selection/outputs/tag_efficiencies.json` (efficiency values)
- All 20 PNGs in `phase3_selection/outputs/figures/`

## Files Written

- `phase3_selection/review/validation/SELECTION_PLOT_VALIDATION_hana_fccb_2026-04-02.md`
- `phase3_selection/logs/plot_validator_hana_fccb_2026-04-02.md` (this file)
