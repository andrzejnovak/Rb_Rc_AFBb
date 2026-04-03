# Plot Validation Review — Phase 4c (Full Data)
**Session:** vera_8187
**Date:** 2026-04-02
**Figures dir:** `phase4_inference/4c_observed/outputs/figures/`
**Script:** `phase4_inference/4c_observed/src/plot_phase4c.py`

---

## STEP 1: FIGURE REGISTRY CHECK

### Registry completeness

- [x] `outputs/FIGURES.json` exists
- [x] FIGURES.json is valid JSON (array of 6 objects)
- [x] Every PNG on disk has a corresponding FIGURES.json entry (no orphans)
- [x] Every FIGURES.json entry has a corresponding PNG on disk (no missing)
- [FAIL] **Every entry is MISSING required fields.** All 6 entries lack: `type`, `script`, `lower_panel`, `is_2d`, `created`, `script_mtime`. The registry only stores: `filename`, `pdf`, `png`, `description`, `observable`, `phase`, `figsize`, `style`.

**[REGISTRY] BLOCKING FINDING — FIGURES.json schema is non-compliant.** The `write_figures_json()` function in `plot_phase4c.py` (lines 436–496) does not write the required fields `type`, `script`, `lower_panel`, `is_2d`, `created`, or `script_mtime`. This means: (a) the plot validator cannot determine figure types for type-specific review batching, (b) the smoke test cannot detect stale figures, and (c) no automated review pipeline can run downstream. **This is a Category A blocking finding that must be resolved before review proceeds.** The six missing fields and their expected values are listed in the Fix section below.

### Staleness check

Cannot be performed because `script_mtime` is absent from all registry entries. Independent filesystem check: all six PNGs were created at unix time ~1775239684–1775239688 (2026-04-03 14:08:04–14:08:08); `plot_phase4c.py` was last modified at unix time 1775238599 (2026-04-03 13:49:59). All figures are newer than the script by ~8 minutes. **Not stale** based on direct `stat` comparison.

---

## STEP 2: CODE LINTER

### Forbidden patterns grep — `src/plot_phase4c.py`

| Pattern | Result |
|---------|--------|
| `set_title` | Not found |
| `plt.colorbar` / `fig.colorbar(im, ax=` | Not found |
| `tight_layout` | **Found — line 56** |
| Absolute `fontsize=` numbers | **Found — multiple lines** |
| `hspace=0` | Not found (not needed — no ratio/pull panels) |
| `exp_label` or `atlas.label` | Present on all single-panel figures |
| `bbox_inches="tight"` | Present on all save calls |
| `figsize` non-(10,10) | Not found (all use (10,10)) |
| `imshow` | Not found |
| `histtype="errorbar"` without `yerr=` | Not found |
| `data=False` combined with `llabel=` | Not found |
| Code variable names in labels | Found — see below |

**[LINT] VIOLATION (Category A) — `tight_layout` used (line 56).** The `mpl_magic` function is defined as `fig.tight_layout()`, which is forbidden. The spec requires `bbox_inches="tight"` at save time (which is present), not `tight_layout()` in the figure preparation step. `tight_layout()` can distort subplot spacing and conflicts with the 10x10 square-aspect requirement. All save calls already use `bbox_inches="tight"`, so the `mpl_magic(fig)` call is doubly incorrect — it (a) uses the forbidden pattern and (b) is redundant.

**[LINT] VIOLATION (Category A) — absolute numeric `fontsize=` values used throughout.** The CMS/ATLAS stylesheet locks all font sizes for 10x10 figures. The script overrides them at the global level (lines 45–51: `plt.rcParams.update({"font.size": 16, "axes.labelsize": 18, "xtick.labelsize": 14, "ytick.labelsize": 14, "legend.fontsize": 13})`) and then further overrides per-call: `fontsize=11` (line 103), `fontsize=12` (lines 106, 154, 202, 255, 282, 344, 375, 426), `fontsize=10` (lines 194, 213), `fontsize=11` (lines 202, 220), `fontsize=13` (lines 342, 373). All absolute numeric `fontsize=` arguments to any matplotlib call are Category A. Only relative string sizes (`'small'`, `'x-small'`) are permitted.

**[LINT] VIOLATION (Category B) — `hep.atlas.label` used for an ALEPH analysis.** The script uses `hep.style.use("ATLAS")` and `hep.atlas.label(...)` throughout. This analysis is ALEPH open data. Per the plotting template, ALEPH data should use `mh.label.exp_label(exp="ALEPH", ...)`, not the ATLAS-branded label call. The "ATLAS" branding appears visually on all rendered figures (top-left "ATLAS" logo text). This is incorrect for an ALEPH measurement.

**[LINT] VIOLATION (Category B) — `plot_utils.py` from Phase 3 not imported.** `phase3_selection/src/plot_utils.py` exists but none of the Phase 4c plotting scripts import it. Phase 4+ scripts should import Phase 3 plotting utilities for consistent styling.

**[LINT] NOTE — `systematics_breakdown_fulldata` has no `exp_label` call.** The `plot_systematics_breakdown()` function (lines 164–228) does not call `hep.atlas.label` or any equivalent on either `ax1` or `ax2`. This produces a figure with no experiment label, which is an automatic Category A rendering red flag (per the plot validator spec: "Missing experiment label on any figure" → automatic Category A).

**[LINT] VIOLATION (Category B) — Multi-panel figures with `figsize=(10, 10)` share canvas without scaling.** The `plot_systematics_breakdown()` uses `plt.subplots(1, 2, figsize=(10, 10))`, `plot_per_year()` uses `plt.subplots(2, 1, figsize=(10, 10))`, and `plot_calibration_progression()` uses `plt.subplots(1, 2, figsize=(10, 10))`. For multi-panel figures, the spec notes "2x2 -> (20, 20), 1x3 -> (30, 10)" to keep the per-panel ratio. A 1x2 panel at `(10, 10)` gives each sub-panel 5 units wide by 10 tall — tall and narrow, not square.

---

## STEP 3: VISUAL REVIEW

Figure types inferred from content (registry `type` field is absent):

| Filename | Inferred type |
|----------|--------------|
| `rb_3tag_stability_fulldata` | `result` |
| `afb_kappa_fulldata` | `result` |
| `systematics_breakdown_fulldata` | `systematic_impact` |
| `per_year_consistency` | `diagnostic` |
| `calibration_progression` | `comparison` |
| `bdt_crosscheck_fulldata` | `comparison` |

---

### Figure 1: `rb_3tag_stability_fulldata.png`

**Visual description:** The figure shows R_b measured at 8 working point configurations plotted as orange circles (SF-calibrated) with error bars, and yellow-orange squares (Raw MC calibration) slightly offset horizontally. A dashed-dotted horizontal band shows the combined R_b = 0.1898. The SM value R_b^SM = 0.21578 is shown as a dashed red line. The x-axis carries rotated working-point labels (tight10_loose3, tight6_loose4, etc.). The figure is square and the ATLAS label appears top-left with "ALEPH 1992-1995 fb^-1 (13 TeV)" at top-right — the "(13 TeV)" text is nonsensical for a LEP experiment and luminosity is in "fb^-1" which does not apply to ALEPH.

**Findings:**
- [VISUAL] **VIOLATION (Category A) — Spurious "(13 TeV)" centre-of-mass label on ALEPH figure.** The `hep.atlas.label` call appends the LHC centre-of-mass energy "(13 TeV)" to the right-side label. ALEPH operated at $\sqrt{s} = M_Z \approx 91.2$ GeV, not 13 TeV. This is a fundamental physics labelling error visible on all figures produced by this script that use `hep.atlas.label`. The fix is to use `mh.label.exp_label(exp="ALEPH", ..., rlabel=r"$\sqrt{s}=91.2$ GeV")` with no `com=` argument.
- [VISUAL] **VIOLATION (Category A) — Luminosity unit "fb^-1" is wrong for ALEPH.** ALEPH luminosity is measured in pb^-1 or stated as number of Z events. "fb^-1" is an LHC convention. All rendered figures show "ALEPH 1992-1995 fb^-1 (13 TeV)".
- [VISUAL] **VIOLATION (Category A) — "ATLAS" branding on an ALEPH figure.** The top-left label reads "ATLAS" in bold, which is incorrect. This is a consequence of using `hep.atlas.label` rather than `mh.label.exp_label(exp="ALEPH", ...)`.
- [VISUAL] **PHYSICS WARNING — Combined R_b = 0.1898 is 11% below the SM value of 0.2158.** This is a ~4-sigma deviation from the Standard Model expectation. This is not a visual finding but should be flagged: either the systematic uncertainty is underestimated, the efficiency calibration has a bias, or there is a genuine effect. The figure itself does not display systematic uncertainties — only statistical error bars. This makes the figure incomplete for a final result.
- [VISUAL] PASS — Square aspect ratio, no legend-data overlap, axis labels use LaTeX notation, tick labels readable. The working-point x-axis labels are rotated 45 degrees and readable.

**Verdict: FAIL (Category A — three rendering red flags: ATLAS label on ALEPH figure, "(13 TeV)" CoM, "fb^-1" unit)**

---

### Figure 2: `afb_kappa_fulldata.png`

**Visual description:** The figure shows A_FB^b plotted vs kappa (x-axis range 0.2–2.0) as orange filled circles with error bars. A combined A_FB^b = -0.0755 line is shown as a dashed-dotted orange line. The LEP combined value of 0.0995 is shown as a dashed red line. A horizontal gray dotted line marks zero. The result is consistently negative (approximately -0.07 to -0.10) across all kappa values — meaning the measured A_FB^b is negative while the LEP combined value is positive and the SM expectation is ~+0.10. This sign discrepancy is large. The rightmost kappa=2.0 datapoint appears detached at the far right edge of the plot. The "ATLAS" branding and "(13 TeV) fb^-1" appear again.

**Findings:**
- [VISUAL] **VIOLATION (Category A) — Same ATLAS/13 TeV/fb^-1 labelling errors as Figure 1.** Applies to all figures using `hep.atlas.label`.
- [VISUAL] **PHYSICS RED FLAG — A_FB^b is systematically negative, opposite sign to LEP combined.** The measured combined A_FB^b = -0.0755 is in sign disagreement with the LEP combined value of +0.0995. This is not a small deviation; it is a sign flip. The LEP combined represents the average of all four LEP experiments. A sign-opposite result requires an explanation — either the thrust axis orientation convention is opposite, the jet-charge weighting sign is flipped, or there is a systematic error in the hemisphere assignment. This should be flagged as a Category A physics issue requiring investigation before finalizing results.
- [VISUAL] PASS — Square aspect, no text overlap, LaTeX axis labels, error bars visible and reasonable in magnitude, legend present.

**Verdict: FAIL (Category A — ATLAS label errors; Category A physics — sign-opposite A_FB^b)**

---

### Figure 3: `systematics_breakdown_fulldata.png`

**Visual description:** A 1x2 panel figure showing horizontal bar charts. Left panel: R_b systematic contributions (eps_c dominates, followed by eps_uds, C_b, R_c; smaller contributions from sigma_d0, mc year coverage, hadronization, sigma_d0 form, mc statistics, physics params, g_cc, g_bb, selection bias, tau contamination). Right panel: A_FB^b systematic contributions (charge model dominates, then purity uncertainty, angular efficiency, charm asymmetry, delta_b published, delta QCD). Both panels are tall and narrow due to the 1x2 layout at (10,10) figsize. The x-axis label for R_b is "$\delta R_b$" and for A_FB is "$\delta A_{FB}^b$". No experiment label appears on either panel.

**Findings:**
- [VISUAL] **VIOLATION (Category A — Automatic Red Flag) — Missing experiment label on both panels.** Neither `ax1` nor `ax2` has an `exp_label` or `atlas.label` call. This is an automatic Category A finding that the arbiter may not downgrade.
- [VISUAL] **VIOLATION (Category B) — Panels are tall and narrow, not square.** At `figsize=(10, 10)` with `plt.subplots(1, 2)`, each panel is ~5 units wide by 10 units tall. The bar labels on the y-axis are clipped/compressed vertically. The spec requires scaling 1x2 to (20, 10) for proper per-panel proportions.
- [VISUAL] **VIOLATION (Category B) — Some y-axis tick labels appear to use code-style names.** Items like "eps c", "eps uds", "sigma d0", "mc year coverage", "mc statistics", "sigma d0 form", "g cc", "g bb" are code variable names with underscores replaced by spaces. These are not publication-quality labels. "eps_c" should be "$\varepsilon_c$", "eps_uds" should be "$\varepsilon_{uds}$", "sigma_d0" should be "$\sigma_{d_0}$", etc. Any raw identifier visible on the figure is Category A per the label quality rule.
- [VISUAL] **PHYSICS CHECK — Dominant systematic for R_b is eps_c (charm tagging efficiency), contributing ~1.8 × 10^-2, which is the majority of the total systematic of 0.0181.** This is a single dominant source at ~100% of total syst. The eps_uds contribution is second at ~1.4 × 10^-2. Variation signs are not displayed (only magnitudes), which is acceptable for an impact plot but worth noting. For A_FB^b the charge model dominates at ~1.5 × 10^-2 of a total of 0.0193.
- [VISUAL] PASS — Bar colors are distinguishable between categories (C0 blue, C1 orange, C2 green, C3 red, C4 purple for R_b; C5 cyan for A_FB). No overlap. Bars are not flat (non-trivial per-source variation is visible).

**Verdict: FAIL (Category A — missing experiment label; Category A — code variable names in labels; Category B — panel aspect ratio)**

---

### Figure 4: `per_year_consistency.png`

**Visual description:** A 2x1 panel figure. Top panel: R_b per year (1992, 1993, 1994) plotted as orange circles. Two years (1993, 1994) are visible with R_b ~0.185–0.188; the 1992 point is absent or at the far left edge near 1992.0. A chi2/ndf = 3.6/3, p = 0.312 annotation appears in a wheat-colored box in the upper right. The SM value R_b^SM is shown as a dashed line. Bottom panel: A_FB^b per year (1992, 1993, 1994) shown as blue squares with error bars. Values are negative (approximately -0.03 to -0.08), consistent with the Figure 2 findings. The "ATLAS" + "(13 TeV)" label appears on the top panel only, which is correct (not on the ratio/second panel). The bottom panel has no experiment label, which is correct for a secondary panel sharing context with the top panel.

**Findings:**
- [VISUAL] **VIOLATION (Category A) — Same ATLAS/13 TeV/fb^-1 labelling errors on top panel.**
- [VISUAL] **PHYSICS OBSERVATION — A_FB^b values are negative for all measured years, consistent with the sign discrepancy noted in Figure 2.** The per-year values confirm this is systematic, not a statistical fluctuation.
- [VISUAL] **PHYSICS CONCERN — chi2/ndf = 3.6/3, p = 0.312 for R_b per-year consistency.** This is acceptable (p > 0.05) but a chi2/ndf of 1.2 for only 3 points with large systematic uncertainties is plausible. The ndf=3 suggests 4 data points (one per year 1992-1995) but only 3 are visually apparent in the figure.
- [VISUAL] PASS — Square canvas (10x10), two panels at 2x1. Experiment label on top panel only. Legend present. Chi2 and p-value visible in figure. Error bars reasonable in magnitude. No text collision.

**Verdict: FAIL (Category A — ATLAS label errors; physics sign discrepancy flagged but not a visual finding per se)**

---

### Figure 5: `calibration_progression.png`

**Visual description:** A 1x2 panel figure. Left panel: R_b at three stages (MC (4a), 10% (4b), Full (4c)), plotted as orange filled circles. Values progress from ~0.171 (MC), to ~0.188 (10%), to ~0.188 (Full). The SM R_b^SM is shown as a red dashed line at 0.216. The progression shows R_b rising from the MC expectation toward but not reaching the SM value. Right panel: A_FB^b at the same three stages, as blue squares. MC value is 0.0 (by construction), 10% is approximately -0.023, Full is approximately -0.075. The LEP combined line sits at +0.0995. The "ATLAS" label and "fb^-1 (13 TeV)" appear on the left panel only. Right panel has no experiment label.

**Findings:**
- [VISUAL] **VIOLATION (Category A) — Same ATLAS/13 TeV/fb^-1 labelling errors on left panel.**
- [VISUAL] **NOTE — Right panel has no experiment label, which is acceptable** because this is the secondary panel in a 1x2 layout and the left panel carries the label. However, this convention is more appropriate for 2x1 stacked panels (ratio plots) than for 1x2 side-by-side panels. For 1x2, both panels typically get labels. This is a style concern (Category C).
- [VISUAL] **PHYSICS OBSERVATION — The A_FB^b progression reveals a sign reversal:** MC gives 0.0 (by construction, symmetric), 10% gives ~-0.023, full data gives ~-0.075. This three-point trend shows the measurement converging to a sign-negative value with increasing statistics, which is opposite to the LEP combined value. This is not a visual artifact — it reflects the underlying analysis.
- [VISUAL] **VIOLATION (Category B) — 1x2 layout at (10, 10) gives narrow panels.** Same issue as Figure 3.
- [VISUAL] PASS — No legend-data overlap. Markers are distinguishable. Stage labels (MC, 10%, Full) on x-axis are clear.

**Verdict: FAIL (Category A — ATLAS label errors; Category B — panel aspect ratio)**

---

### Figure 6: `bdt_crosscheck_fulldata.png`

**Visual description:** The figure shows R_b measured using a BDT-based tagger plotted vs BDT score threshold (x-axis 0.30–0.65) as blue squares with error bars. A cut-based R_b = 0.1878 is shown as a dashed-dotted orange line with a light-blue band representing its uncertainty. The SM R_b^SM is shown as a red dashed line at ~0.216. The BDT-based R_b values vary significantly across thresholds: a very low value (~0.10) at threshold=0.30, then ~0.11 at 0.40, ~0.10 at 0.50, and approximately 0.00 at threshold=0.65 (which is below the y-axis lower limit of 0.10, so the point is clipped). The y-axis is fixed to [0.10, 0.35]. The "ATLAS" label and "(13 TeV)" appear at top.

**Findings:**
- [VISUAL] **VIOLATION (Category A) — Same ATLAS/13 TeV/fb^-1 labelling errors.**
- [VISUAL] **VIOLATION (Category A) — Data content clipped.** The BDT threshold=0.65 point appears to be at R_b ≈ 0.00 or below, but the y-axis is hard-coded to [0.10, 0.35] (`ax.set_ylim(0.10, 0.35)`). The rightmost data point appears to be clipped at the lower edge of the plot. This means the figure is hiding data — a serious visual integrity issue.
- [VISUAL] **PHYSICS RED FLAG — BDT cross-check R_b values (0.10–0.12) are significantly lower than the cut-based R_b = 0.1878 and far below the SM value.** The BDT and cut-based methods disagree by 40–80% in absolute terms. If this is a genuine crosscheck, such disagreement requires explanation. The figure as drawn suggests the BDT tagger may have a large efficiency bias or the BDT was trained on features correlated with MC truth in a way that degrades on data.
- [VISUAL] **CONCERN — The BDT cross-check values show no plateau as a function of threshold.** Typically a crosscheck plot should show a stable plateau region where both methods agree. No such plateau is visible here; the BDT R_b decreases monotonically with threshold.
- [VISUAL] PASS — Square aspect ratio, legend present, error bars visible. Axis labels use LaTeX notation ($R_b$, "BDT score threshold").

**Verdict: FAIL (Category A — ATLAS label errors; Category A — data clipped by hard-coded y-axis; Category A — physics red flag: large method disagreement)**

---

## CROSS-FIGURE CONSISTENCY

**[VISUAL] CROSS-FIGURE FINDING (Category A) — Systematic sign error in A_FB^b across all figures.** Figures 2, 4, and 5 all show A_FB^b < 0 while the LEP combined value is +0.0995 and the SM expectation is +0.1031. This is not a statistical fluctuation — it is consistent across all kappa values (Figure 2), all years (Figure 4), and progresses more negative as statistics increase from 10% to full data (Figure 5). A sign error in the jet-charge sum, hemisphere orientation, or the thrust-axis direction convention would produce this signature. This must be investigated before results are finalized.

**[VISUAL] CROSS-FIGURE FINDING (Category A) — ATLAS/13 TeV labelling error is systemic.** All figures that have an experiment label display "ATLAS" and "(13 TeV)" which are incorrect for an ALEPH LEP measurement. This is a single root cause in `hep.atlas.label` usage and affects `rb_3tag_stability_fulldata`, `afb_kappa_fulldata`, `per_year_consistency` (top panel), `calibration_progression` (left panel), and `bdt_crosscheck_fulldata`. The `systematics_breakdown_fulldata` figure has no experiment label at all.

**[VISUAL] CROSS-FIGURE FINDING (Category B) — R_b is consistently 10–12% below SM.** Across Figures 1, 4, 5, and 6, R_b values range from 0.17 to 0.19, consistently below R_b^SM = 0.2158 by 4–6 sigma statistically. This is either a large efficiency calibration bias (the dominant systematic is eps_c, the charm efficiency) or a genuine physics effect. The AN must provide a quantitative explanation.

---

## SUMMARY TABLE

| Figure | Registry | Lint | Visual | Overall |
|--------|----------|------|--------|---------|
| `rb_3tag_stability_fulldata` | FAIL (missing fields) | A+A | A (ATLAS label, 13 TeV, fb^-1) | **FAIL (Cat A)** |
| `afb_kappa_fulldata` | FAIL (missing fields) | A+A | A (label errors) + A (sign flip) | **FAIL (Cat A)** |
| `systematics_breakdown_fulldata` | FAIL (missing fields) | A+A | A (no exp label) + A (code names) + B | **FAIL (Cat A)** |
| `per_year_consistency` | FAIL (missing fields) | A+A | A (label errors) | **FAIL (Cat A)** |
| `calibration_progression` | FAIL (missing fields) | A+A | A (label errors) + B | **FAIL (Cat A)** |
| `bdt_crosscheck_fulldata` | FAIL (missing fields) | A+A | A (label errors) + A (clipped data) + A (method disagreement) | **FAIL (Cat A)** |

**Overall validation verdict: FAIL. All six figures require remediation before review can proceed.**

---

## REQUIRED FIXES (Priority Order)

### P1 — FIGURES.json schema (blocking)
The `write_figures_json()` function must add the following fields to each entry:
- `type`: one of `result`, `systematic_impact`, `diagnostic`, `comparison` (per figure)
- `script`: `"src/plot_phase4c.py"`
- `lower_panel`: `"none"` (no figures have pull/ratio panels)
- `is_2d`: `false` (no 2D figures)
- `created`: ISO 8601 timestamp when the PNG was written
- `script_mtime`: ISO 8601 mtime of `plot_phase4c.py` at generation time
- `observable_type`: `"derived"` for all (measured ratios/asymmetries, not event counts)

Suggested type assignments:
- `rb_3tag_stability_fulldata`: `"result"`
- `afb_kappa_fulldata`: `"result"`
- `systematics_breakdown_fulldata`: `"systematic_impact"`
- `per_year_consistency`: `"diagnostic"`
- `calibration_progression`: `"comparison"`
- `bdt_crosscheck_fulldata`: `"comparison"`

### P2 — Replace ATLAS label with ALEPH label (all figures)
Replace all `hep.atlas.label(ax=ax, data=True, lumi="ALEPH 1992-1995", loc=0)` calls with:
```python
mh.label.exp_label(
    exp="ALEPH",
    data=True,
    llabel="Open Data",
    rlabel=r"$\sqrt{s}=91.2$ GeV",
    ax=ax,
)
```
Also add `import mplhep as mh` and remove `hep.style.use("ATLAS")` in favour of `mh.style.use("CMS")` (or the appropriate LEP-experiment style if one exists in mplhep).

### P3 — Add experiment label to `systematics_breakdown_fulldata`
Add an `exp_label` call on `ax1` (left panel). The right panel (`ax2`) may be left without a label as secondary.

### P4 — Remove `tight_layout` from `mpl_magic` (line 56)
Replace the `mpl_magic` function body with a no-op or remove it and call `mpl_magic` only where needed. All save calls already use `bbox_inches="tight"`.

### P5 — Replace all absolute `fontsize=` values with relative strings
Replace `fontsize=10/11/12/13` with `fontsize='x-small'` or `fontsize='small'` as appropriate. Remove the `plt.rcParams.update({...})` block (lines 45–51) that overrides the stylesheet font sizes.

### P6 — Fix y-axis clipping in `bdt_crosscheck_fulldata`
Remove the hardcoded `ax.set_ylim(0.10, 0.35)` or replace with a range that accommodates all data points including threshold=0.65. Alternatively use `ax.autoscale()` after plotting.

### P7 — Fix multi-panel figsize for side-by-side panels
For `plt.subplots(1, 2, ...)` use `figsize=(20, 10)`. For `plt.subplots(2, 1, ...)` keep `figsize=(10, 10)` or use `(10, 20)` depending on per-panel aspect requirements. Regenerate all affected figures.

### P8 — Fix systematic label names to publication quality
Replace code-style names in `plot_systematics_breakdown()` with LaTeX-formatted labels: `"eps_c"` → `r"$\varepsilon_c$"`, `"eps_uds"` → `r"$\varepsilon_{uds}$"`, `"sigma_d0"` → `r"$\sigma_{d_0}$"`, `"g_cc"` → `r"$g_{c\bar{c}}$"`, `"g_bb"` → `r"$g_{b\bar{b}}$"`, `"mc_model"` → "MC model", `"mc year coverage"` → "MC year coverage", etc.

### P9 — Physics investigation (separate from figure fixes)
The sign of A_FB^b should be investigated immediately. The negative sign across all kappa, all years, and all data fractions suggests a sign error in the jet-charge computation, hemisphere assignment, or thrust-axis orientation convention rather than a physics effect. This is not a figure fix — it is an analysis-level finding that should be escalated to the orchestrator as a potential Phase 3/4 regression trigger.

---

*Review written by vera_8187 (plot validator, Sonnet). Level 3 review only — cross-figure consistency and physics narrative. Mechanical issues at Level 1/2 are flagged as upstream quality gate failures per the plot validator spec.*
