# AN Plot Validation — Doc 4a, Iteration 2
**Session:** kenji_3c08
**Date:** 2026-04-03
**Validator role:** Level 3 — Fresh review, focused verification of 5 figure-dependent findings from jasper_5871
**Scope:** All figures in ANALYSIS_NOTE_doc4a_v1.tex; targeted re-check of A3/A4 (closure panel rendering), A5 (efficiency_calibration), A2 (F7 band visibility), A1 (F2 chi2 display), and B1 (closure_test_phase4a figsize)

---

## Iteration 1 Context

jasper_5871 identified 5 Category A findings and 10 Category B findings. This iteration performs a **fresh** visual review of all figures, with specific attention to the 5 figure-dependent findings:

| Tag | Figure | Finding Summary |
|-----|--------|-----------------|
| A1 | F2_afb_angular_distribution.png | chi2/ndf = 31.9/8 displayed without intercept-inclusive fit; appears as unresolved bad fit |
| A2 | F7_afb_kappa_consistency.png | Combined result band nearly invisible at AN rendering size |
| A3 | closure_tests_magnus_1207_20260402.png (Phase 3) | Panel (a) shows both bars at equal height; R_b=0.0000 annotation appears inconsistent with bar height |
| A4 | closure_tests_magnus_1207_20260402.png (Phase 3) | Panel (b) annotation shows "1144" vs AN caption "11,447" |
| A5 | efficiency_calibration.png | 3-panel 30×10 composite: text unreadable at AN rendering size |

Additionally, B1 (closure_test_phase4a.png non-square figsize) is tracked.

---

## Step 1: Figure Registry Check

### Phase 3 Registry (`phase3_selection/outputs/FIGURES.json`)

- [x] FIGURES.json exists and is valid JSON
- [x] 36 PNG entries in registry (18 per session: 20260402 + 20260403 re-run)
- [x] All 36 registry entries have corresponding files on disk (0 missing)
- [x] No orphan PNGs: the 36 extra files on disk are PDF companions (not PNGs)
- [x] All entries have required fields: filename, type, script, description, lower_panel, is_2d, created, script_mtime
- [x] All `type` values are from the allowed set (data_mc, diagnostic, result, closure)
- [x] All `lower_panel` values are valid (pull or none)
- [x] Staleness check: 20260403 figures created 09:06–09:16, script_mtime = 09:05 — all fresh. 20260402 figures created April 2, script_mtime April 2 — no violations.

### Phase 4a Registry (`phase4_inference/4a_expected/outputs/FIGURES.json`)

- [x] FIGURES.json exists and is valid JSON
- [x] 8 PNG entries with corresponding files on disk
- [x] No orphan PNGs unregistered in FIGURES.json
- [x] All entries have required fields
- [x] All `type` values valid (result, systematic_impact, closure, diagnostic)
- [x] All `lower_panel` values valid (none throughout — single-panel figures)
- [x] Staleness check: all figures created 07:12–07:17 on 04-03; script_mtime = 04-03 06:20. All fresh.

### AN Figure Reference Check

- [x] AN references: `efficiency_calibration.pdf`, `F7_afb_kappa_consistency.pdf`, `closure_tests_magnus_1207_20260402.pdf`, `F2_afb_angular_distribution.pdf`, `closure_test_phase4a.pdf` — all present in `analysis_note/figures/`
- [x] No `\begin{subfigure}` found in `ANALYSIS_NOTE_doc4a_v1.tex`

**CRITICAL FINDING [REGISTRY-1]:** The AN references `closure_tests_magnus_1207_20260402.pdf` — the filename of the original problematic figure. However, **MD5 verification confirms** the file in `analysis_note/figures/` is byte-for-byte identical to the updated `closure_tests_magnus_1207_20260403.pdf` from Phase 3 outputs. The Phase 3 pipeline regenerated figures with both session timestamps; the updated PDF was staged into the AN figures directory, overwriting or replacing the 20260402 version. The AN is referencing the correct (updated) content under the old filename. This is a provenance inconsistency — the filename suggests the original file but the content is the fixed version. **Not a blocking finding** (content is correct), but the AN tex should be updated to reference `closure_tests_magnus_1207_20260403.pdf` to make provenance auditable.

**[REGISTRY] RESULT: PASS with provenance note (closure figure content is fixed, filename is stale).**

---

## Step 2: Code Lint

Scripts checked:
- `phase3_selection/src/plot_all.py`
- `phase3_selection/src/plot_utils.py`
- `phase4_inference/4a_expected/src/plot_phase4a.py`

### Forbidden Pattern Results

| Pattern | plot_all.py | plot_phase4a.py | Result |
|---------|-------------|-----------------|--------|
| `ax.set_title(` | Not found | Not found | PASS |
| `plt.colorbar` or `fig.colorbar(im, ax=` | Not found | Not found | PASS |
| `tight_layout` | Not found | Not found | PASS |
| `imshow` | Not found | Not found | PASS |
| `histtype="errorbar"` without `yerr=` | Not found | Not found | PASS |
| `\begin{subfigure}` in .tex | Not found | — | PASS |
| `data=False` with `llabel=` | Not found | Not found | PASS |
| `np.sqrt(h.values())` near `yerr=` | Not found | Not found | PASS |
| `.view()[:]` near `histtype="errorbar"` | Not found | Not found | PASS |
| `bbox_inches="tight"` at save | PASS (plot_utils.py line 70) | PASS (via plot_utils) | PASS |

### figsize Violations (Unchanged from Iteration 1)

**[LINT] VIOLATION (Category B) — NOT FIXED:** `plot_phase4a.py` lines 352 and 399:
```python
fig, axes = plt.subplots(1, 2, figsize=(20, 10))   # closure_test_phase4a — line 352
fig, axes = plt.subplots(1, 3, figsize=(30, 10))   # efficiency_calibration — line 399
```
These violations remain in the source code from iteration 1. Both multi-panel Phase 4a figures still use non-square source dimensions. Iteration 1 flagged these as Category B (B1) and Category A (A5) respectively. The source code has not changed (script mtime unchanged at 06:20 on 04-03, predating the re-run). The figures were not regenerated with corrected dimensions.

**[LINT] NOTE (Category B) — UNCHANGED:** `plot_all.py` line 581:
```python
fig, axes = plt.subplots(1, 3, figsize=(10, 10))   # closure_tests
```
The Phase 3 closure test figure uses a square (10,10) source but with 3 panels, producing 3.3:1 per-panel aspect ratio. This is the same lint finding as iteration 1.

**[LINT] RESULT: No new violations. 2 Category B violations persist (same as iteration 1). No Category A code violations.**

---

## Step 3: Visual Review — Targeted 5-Finding Re-Check

### FINDING A3 + A4: closure_tests_magnus_1207_20260402.png (Panel rendering)

**Visual inspection of `closure_tests_magnus_1207_20260403.png` (the content actually in the AN):**

The updated closure figure shows a three-panel layout in a 10×10 square. Panel (a) shows two bars: the left "Full sample" bar fills the y-axis from 0 to ~0.83 in blue, while the right "Mirrored (no lifetime)" bar has been corrected — the bar now shows at negligible height (essentially invisible at the floor), with a black downward-pointing arrow labeled `R_b = 0.0000` annotating the arrow. This is the correct rendering: R_b = 0.0000 is shown by an arrow at the zero level, while the Full sample bar at ~0.83 demonstrates the working tagger. Panel (b) shows `chi2/ndf = 11,44...` in the annotation box — the truncation is now showing "11,44" rather than "1144" from iteration 1, implying the full value (11,447) is partially visible but still truncated by the text box width at rendering. Panel (c) shows the contamination injection result unchanged.

**A3 Status: FIXED.** The "Mirrored" bar is now correctly at y≈0 with an explicit annotation arrow. Both bars are no longer at equal height — the Full sample bar fills the axis while the Mirrored bar is at the floor with the pointer annotation. This directly addresses the Category A rendering bug.

**A4 Status: PARTIALLY FIXED.** The annotation text in panel (b) now begins with "chi2/ndf = 11,44..." — but the value is truncated by the text box boundary. At AN rendering size (~0.225 linewidth per panel given 0.45 linewidth for the composite), the annotation box is very narrow and "11,447" would be rendered as "11,44" or similar, still not fully legible. The full numeric value is correct in the code (`chi2_str = f"$\\chi^2$/ndf = {chi2_ndf:,.0f}"`), and the AN caption states the correct value. This truncation is a presentation issue, not a numerical error. **Category downgraded from A to B**: the underlying number is correct and the caption states the correct value; the figure annotation is merely cosmetically truncated.

**[VISUAL] REMAINING CONCERN (Category B):** Panel (b) annotation text is truncated at "11,44..." due to text box width at compressed panel size. The full chi2/ndf = 11,447 value should be visible. Suggested fix: use scientific notation ("~1.1 × 10^4") to fit the narrow panel.

**[VISUAL] REMAINING CONCERN (Category A):** The closure figure in the AN uses a 10×10 source with 3 panels, yielding extremely compressed ~3.3:1 per-panel aspect. At 0.45 linewidth rendering in the AN (~6 cm total width, ~2 cm per panel), all y-axis tick labels and panel sub-labels are essentially unreadable. The "Full sample" and "Mirrored (no lifetime)" x-tick labels are in "x-small" font and will be invisible in print. This is the same readability failure as iteration 1 for Phase 3 closure figures — it was not fixed by the content correction (which addressed the bar height bug, not the rendering scale issue).

**Verdict for A3: FIXED.** Bar rendering bug resolved — the mirrored bar correctly shows R_b ≈ 0 with annotation arrow.
**Verdict for A4: PARTIALLY FIXED → Category B.** Annotation now shows correct value (partially); discrepancy resolved conceptually but figure annotation remains truncated in narrow panel.

---

### FINDING A5: efficiency_calibration.png (3-panel 30×10 composite)

**Visual inspection:**

The efficiency calibration figure remains a 3-panel composite with `figsize=(30, 10)` in the source code (line 399 — unchanged). The rendered PNG shows three panels side-by-side: left panel shows ε_b (blue line decreasing from ~0.35 at WP 7 to ~0.25 at WP 10), center shows ε_c (orange, ~0.60 to ~0.42), right shows ε_uds (red, ~0.175 to ~0.08). The curves are physically sensible. The y-axis labels ε_b, ε_c, ε_uds are in standard matplotlib tick label size. The "From MC (SM truth)" annotation box appears in the left panel at y≈0.45, positioned below the experiment label.

At the rendered PNG size (inspected directly), the figure is visibly wide and compressed vertically — the per-panel height is roughly 1/3 of the total width, giving a landscape ratio. The axis labels are readable at screen resolution but the panels are narrow (each ~1/3 of total image width). At AN rendering (0.45 linewidth ≈ 6.3 cm × 0.45 = 2.8 cm per panel of effective rendered size), the text will be below threshold for print legibility.

**A5 Status: NOT FIXED.** The source code still uses `figsize=(30, 10)` at line 399 of `plot_phase4a.py`. The figure was not regenerated with corrected dimensions. The rendered output is identical to what was evaluated in iteration 1. The label truncation issue that jasper_5871 identified as Category A remains.

**[VISUAL] VIOLATION (Category A — NOT FIXED):** efficiency_calibration.png remains a 30×10 non-square composite. At AN rendering size (~0.45 linewidth for the entire 3-panel composite, meaning ~0.15 linewidth per panel), all y-axis labels, tick marks, and the "From MC (SM truth)" annotation will be below readable threshold. The fix required — splitting into three separate 10×10 figures or restructuring as a proper 3-panel figure — was not applied. This is a blocking finding.

---

### FINDING A2: F7_afb_kappa_consistency.png (Combined band visibility)

**Visual inspection:**

The figure shows A_FB^b (y-axis) vs kappa (x-axis, labeled 0.3, 0.5, 1.0, 2.0, ∞). The large green horizontal band (ALEPH = 0.0927 ± 0.0052) dominates the upper 15% of the plot, spanning y ≈ 0.087–0.098. The black MC pseudo-data error bars all cluster near y ≈ 0.000–0.008. The blue combined band (Combined = −0.0001 ± 0.0022) is visible as a narrow blue horizontal band near y = 0. At the figure's native resolution, the blue band spans approximately y = −0.0023 to y = +0.0021 — a total width of 4.4 × 10^-3 in y-axis units spanning approximately 0.10 total.

The blue band width on the y-axis is 4.4/100 = 4.4% of the y-range. In the rendered PNG at displayed size, the blue band is approximately 5–7 pixels tall — visible but very thin. At AN rendering scale (0.45 linewidth ≈ 6.3 cm), mapped from a ~600px figure height, each pixel maps to ~10 μm print resolution. The 5-pixel band maps to ~50 μm, which is at the boundary of reliable offset printing resolution (≥ 100 μm typically required for color fills). The band is likely to print as a hairline or disappear entirely on lower-resolution printers.

The code uses `alpha=0.2` for the combined band (`ax.axhspan(..., alpha=0.2, color='blue')`). With alpha=0.2 and a very thin band, the blue fill has low ink density even when visible.

**A2 Status: NOT FIXED.** The source code is unchanged (line 316–319 in `plot_phase4a.py`). The figure was not regenerated. The combined band remains essentially sub-pixel-width at AN rendering size with low alpha. This remains a Category A finding: the primary physics result of the figure (combined A_FB^b) is the feature least visible in the figure.

**[VISUAL] VIOLATION (Category A — NOT FIXED):** The combined A_FB^b band (the primary result shown in this figure) is ~5 pixels tall in the PNG and will render at sub-hairline width in the AN PDF. The ALEPH reference band, which is not the primary result, dominates ~15% of the plot area. The figure communicates the secondary context (ALEPH reference) far more prominently than the primary result (our combined measurement). Suggested fix (as in iteration 1): zoom the y-axis to the data region (y ∈ [−0.015, +0.015]) and show ALEPH as an off-plot arrow or side annotation, OR increase the combined band to linewidth-drawn horizontal lines rather than a filled span.

---

### FINDING A1: F2_afb_angular_distribution.png (chi2/ndf display)

**Visual inspection:**

The figure shows `<Q_FB>` vs cos(θ_thrust) with 10 MC pseudo-data error bars. The red fit line has a gentle positive slope. The chi2/ndf = 31.9/8 annotation box is visible in the upper-left in wheat color. The data points scatter around a mean of approximately −0.004, with a visible offset below zero throughout the cos θ range. The fit line (which passes through the origin-area region) does not capture the systematic negative offset of the data.

The code at line 141 uses `intercept + slope * x_line` for the fit curve, and the `intercept` is fetched via `fit.get('intercept', 0.0)`. If the stored fit includes a non-zero intercept, it is plotted. At line 142, the label says `Fit: slope = 0.00037 ± 0.00107` — only the slope is labeled, not the intercept, suggesting the intercept may be non-zero but unlabeled in the figure. However, the fit line visible in the rendered figure appears to track through approximately y ≈ −0.004 across the full cos θ range, consistent with a negative intercept of about −0.004.

The key issue from iteration 1 was that chi2/ndf = 31.9/8 appears without the better-fitting model shown. Looking at the figure again: the fit line at ~−0.004 level does actually track the data reasonably at most cos θ values — the data points scatter around the line with a few outliers. The chi2/ndf = 31.9/8 is dominated by the two data points that deviate most: the point at cos θ ≈ 0 that sits at approximately +0.0025 (roughly 4σ above the line), and several points that scatter widely. The poor chi2 reflects genuine scatter rather than systematic misfit of the bulk.

The AN caption and methodology note this is an MC-only fit showing zero-consistent slope, and the chi2 is noted as from the origin-only fit formulation. The figure annotation shows `chi2/ndf = 31.9/8` prominently, leaving a reader seeing a high chi2 without immediate context for why this is acceptable.

**A1 Status: NOT FIXED.** The code is unchanged (same script mtime, same figure creation timestamp). The intercept-inclusive fit overlay, alternative chi2 annotation, or explanatory note that jasper_5871 recommended was not added.

**[VISUAL] CONCERN (Category A — NOT FIXED):** The chi2/ndf = 31.9/8 is prominently displayed and corresponds to a p-value < 0.001. The fit line appears to systematically underfit several data points. No second (better) fit curve or explanation of the poor chi2 is shown in the figure itself. A reader of the AN who examines this figure will see what appears to be a demonstrably poor fit with no resolution. The AN text must explicitly address this in the caption or surrounding text, or the figure must be updated to show the better-fitting model.

**[VISUAL] UPDATE FROM ITERATION 1:** On fresh inspection, the chi2/ndf = 31.9/8 situation is nuanced. The data points scatter around y ≈ −0.004 (which appears to be the fit intercept), and the slope is consistent with zero. The high chi2 reflects statistical noise in the MC sample, not a systematic model failure. The AN caption should include the chi2 value and a sentence explaining that the origin-only fit has poor chi2 because a hemisphere-charge bias is absorbed into the intercept. Without this context in the figure, the chi2 display is misleading. Category A is maintained because the figure, as presented, shows an apparently failed fit without resolution.

---

### FINDING B1: closure_test_phase4a.png (Phase 4a, 2-panel 20×10)

**Visual inspection:**

The Phase 4a closure test figure shows a 2-panel layout. The left panel (independent closure) shows a single data point at WP ~9.0 with pull ≈ 2.0, sitting exactly at or just below the 2σ red dotted line. The right panel shows corrupted corrections: large red bars for +20% ε_uds (pull ≈ +6) and −20% ε_uds (pull ≈ −15), confirming sensitivity. The blue bars for +20% C_b and −20% C_b show small pulls (~±1), and the 0-pull point for ε_c corruptions is near zero.

The figure is landscape (20×10 source), confirmed by the visual aspect ratio. The right panel's y-axis labels are in "xx-small" font — at the displayed size they are readable but small. At AN rendering size (0.45 linewidth ≈ 6.3 cm for the full composite, so each panel is ~3.15 cm), labels will be marginal.

**B1 Status: NOT FIXED.** Source code line 352: `figsize=(20, 10)` unchanged.

**[VISUAL] REMAINING CONCERN (Category B — NOT FIXED):** closure_test_phase4a.png remains 20×10 non-square. The right panel y-axis labels ("+ 20% eps_c", "−20% eps_uds", etc.) will be barely readable at AN print scale. However, given that the physics content is clearly communicated (sensitivity demonstrated, closure pull shown), this is Category B and not a blocker.

**[VISUAL] ADDITIONAL OBSERVATION:** The left panel shows the closure pull sitting at pull ≈ 2.0, with the error bar extending both above (reaching ~3.0) and below (~1.0) the 2σ threshold line. The annotation should clarify the pull value numerically. Looking at the figure, the data point appears to sit exactly at y = 2.0, with the lower error bar reaching y ≈ 1.0. Per the AN text ("pull = 1.93"), the point is technically below 2σ. At AN rendering size, the distinction between pull = 1.93 (pass) and pull = 2.0 (borderline) will not be visible; the numerical AN text is necessary to resolve this.

---

## Step 3 (continued): Fresh Visual Review of All Remaining Figures

### TYPE: result (Phase 4a)

#### F1_rb_stability_scan.png

The figure shows a single MC pseudo-data point at WP 10.0 with error bars extending from approximately R_b ≈ 0.25 to R_b ≈ 0.32, centered at R_b ≈ 0.28. The y-axis range is approximately 0.16–0.30. The ALEPH band (blue horizontal fill at R_b ≈ 0.2158 ± 0.0014) and LEP combined band (green, very narrow at R_b ≈ 0.21629 ± 0.00066) both appear as horizontal fills near y ≈ 0.22, clearly below the data point. The SM dashed red line at R_b = 0.21578 overlaps the reference bands. The experiment label (ALEPH Open Simulation) is visible in the upper left. The figure is square (10×10). The legend shows all four elements clearly with no overlap with data.

The x-axis range 9.5–10.5 with only one data point at WP 10.0 still presents a near-empty scan. The y-axis now extends down to ~0.16, which better shows the reference bands relative to the measurement. The data point at R_b ≈ 0.280 ± 0.031 has a large uncertainty that visually extends from 0.25 to 0.31, correctly capturing the Phase 4a expected precision.

**[VISUAL] Category B (unchanged from iteration 1):** The x-axis range 9.5–10.5 with a single point communicates no stability information. The figure label ("stability scan") is still a misnomer. The AN caption addresses this. Not a blocker.

**Verdict:** PASS with Category B note. No new issues identified on fresh inspection.

---

#### F4_fd_vs_fs.png

The figure shows f_d vs f_s for MC pseudo-data (black circles connected by a line) tracing a trajectory from (f_s ≈ 0.14, f_d ≈ 0.05) to (f_s ≈ 0.30, f_d ≈ 0.12). Three R_b prediction curves are shown: R_b = 0.216 (red dashed), 0.200 (blue dotted), 0.250 (green dotted) — all curving upward in the (f_s, f_d) plane. The data trajectory lies below all three prediction curves through most of the f_s range, only approaching them at high f_s. The "Note: Data trace a locus..." annotation box appears in the lower-left at "xx-small" font.

The figure is square (10×10). The experiment label is present. The legend lists all four elements. The axis labels f_s and f_d are publication quality. The three prediction curves are distinguishable (red dashed, blue dotted, green dotted) in color and line style.

**[VISUAL] Category B (unchanged from iteration 1):** The "not directly comparable" annotation is in xx-small font and will be challenging to read at AN scale. The physics communication is adequate given the caption.

**Verdict:** PASS with Category B note. No new issues.

---

#### F5_systematic_breakdown.png

The figure shows a horizontal bar chart of 13 systematic sources on a log x-axis. Light mistag ε_uds is dominant, with its bar extending to the right near the total systematic line (red dashed). Charm efficiency ε_c is the second-largest, followed by hemisphere correlation C_b, R_c constraint, and others. The two vertical reference lines (total syst. = 395.28 × 10^-3 and statistical = 30.52 × 10^-3) are labeled in the legend. A "Note: ε_uds contributes 99.5% of total syst." annotation appears in the lower right. Blue bars (8 sources) and orange bars (5 sources) are shown. The figure is square (10×10). The experiment label is visible in the upper right area.

Fresh visual inspection confirms: the dominant ε_uds bar fills essentially to the total systematic line, which is correct physics (ε_uds dominance documented). All y-axis labels use publication-quality LaTeX notation (ε_uds, σ_d0 parameterization, etc. — no code variable names). The two-color coding (blue = larger, orange = smaller sources) still has no legend explanation for the color boundary.

**[VISUAL] Category B (unchanged):** Color coding threshold unlabeled. The figure is otherwise clean and communicates the systematic hierarchy clearly.

**Verdict:** PASS with Category B note.

---

### TYPE: diagnostic (Phase 4a)

#### hemisphere_correlation.png

The figure shows hemisphere correlation C vs combined tag threshold for MC (blue squares) and data (black circles). Both curves rise steeply from C ≈ 1.03 at WP 2 to C ≈ 1.55 at WP 10. The published ALEPH C_b = 1.01 reference line (red dashed) appears at the bottom, approximately 3–5% below the WP 2 measurements and 50% below the WP 10 measurements. The figure is square (10×10). The legend lists MC, Data, and ALEPH reference.

Fresh inspection confirms: the ALEPH reference line (C_b = 1.01) is well below all measured values, creating the appearance of systematic disagreement. The AN text (Section 7.5) explains this is working-point-dependent — ALEPH's C_b = 1.01 applies at their working point, not at WP 10. The figure provides no annotation linking ALEPH's reference to a specific working point, leaving a reader confused about whether the discrepancy is a systematic problem or an expected working-point effect.

**[VISUAL] Category B (unchanged from iteration 1):** Missing annotation for ALEPH's working point. The current display implies systematic disagreement across all WPs rather than a working-point-specific comparison. The caption must clarify.

**Verdict:** PASS with Category B note.

---

### TYPE: closure (Phase 4a and Phase 3)

#### closure_test_phase4a.png (Phase 4a)

Described in the targeted re-check above (Finding B1). The figure's content is physically sound — sensitivity is demonstrated, the closure pull is borderline-pass (1.93). The non-square dimensions and small labels are Category B concerns that remain unfixed.

**Verdict:** PASS with Category B (non-square dimensions; right panel labels marginally readable at AN scale).

---

#### closure_tests_magnus_1207_20260403.png (Phase 3 — content in AN)

Described in Finding A3/A4 re-check above. Panel (a) is now correctly rendered with the mirrored bar at zero + annotation arrow. Panel (b) shows chi2/ndf annotation that is partially truncated. Panel (c) shows the contamination injection result (Ratio = 2.14, PASS). The figure is readable at screen size; at AN rendering scale, the 3-panel 10×10 composite produces compressed panels with small text.

**[VISUAL] Category A (Readability — carried over from B6/layout concern in iteration 1):** The 3-panel closure figure in a 10×10 source produces ~3.3:1 per-panel aspect ratio. At 0.45 linewidth rendering (~6.3 cm total width), each panel is ~2 cm wide and ~6.3 cm tall — giving a 3.15:1 height-to-width ratio per panel, with extremely narrow widths. The x-tick labels ("Full sample", "Mirrored (no lifetime)") are in "x-small" font. At 2 cm panel width, these multi-word labels will be truncated or illegible. This is an upgrade from the Category B note in iteration 1 based on fresh visual assessment: the extreme panel compression makes this a readability failure (Category A universal check) rather than a quality suggestion.

**Verdict:** FLAG — Category A (panel compression makes x-tick labels illegible at AN rendering size); the underlying rendering bug from A3 is fixed.

---

### TYPE: data_mc (Phase 3) — All figures re-reviewed

Universal checks (applying to all data/MC figures from the 20260403 re-run):
- Experiment label on main panel only: PASS for all
- Data as black errorbar, MC as filled histogram: PASS for all
- Pull panel with "Pull" label (not "Ratio"): PASS for all
- No experiment label on pull panel: PASS for all
- MC normalized to data integral, legend states "MC (normalized to data)": PASS for all
- No gap between main and pull panels: PASS for all

#### data_mc_significance_magnus_1207_20260403.png

Signed d0/σ_d0 on log y-scale. The distribution is steeply peaked at zero with a long positive tail (lifetime signal). Data and MC overlay well across the full range. Pull panel shows mostly ±1–2σ pulls with a few ±3σ excursions at the extreme positive tail (d0/σ > 25) where bin counts are very low. This is the same figure as the 20260402 version — byte-for-byte (same file size: 117,622 bytes for both).

**Verdict:** PASS.

---

#### data_mc_combined_tag_magnus_1207_20260403.png

Combined hemisphere tag on log scale. Good data/MC agreement in the bulk. Pull panel shows random scatter within ±2σ. Identical to 20260402 version (same file size).

**Verdict:** PASS.

---

#### data_mc_hemisphere_mass_magnus_1207_20260403.png

Hemisphere invariant mass with b/c threshold line at 1.8 GeV/c². Good data/MC agreement. Pull panel shows random scatter. Same as 20260402 version.

**Verdict:** PASS.

---

#### data_mc_phem_magnus_1207_20260403.png

–ln P_hem distribution on log scale. Good data/MC agreement. Same as 20260402 version.

**Verdict:** PASS.

---

#### data_mc_qfb_k0.3_magnus_1207_20260403.png

Q_FB at κ=0.3 — Gaussian-shaped, good data/MC agreement. Pull panel shows a mild structured pattern (positive pulls at edges, slightly negative near center) within ±2.5σ. Same as 20260402 version.

**Verdict:** PASS with Category B note (structured pull pattern — same as iteration 1).

---

#### data_mc_qfb_k0.5_magnus_1207_20260403.png

Q_FB at κ=0.5. Good agreement. Similar structured pull pattern as κ=0.3. Same as 20260402 version.

**Verdict:** PASS with Category B note.

---

#### data_mc_qfb_k1.0_magnus_1207_20260403.png

Q_FB at κ=1.0 — broader Gaussian. Excellent data/MC agreement. Pull panel clean. Same as 20260402 version.

**Verdict:** PASS.

---

#### data_mc_qfb_k2.0_magnus_1207_20260403.png

Q_FB at κ=2.0 — flat-topped trapezoidal. Excellent agreement. Same as 20260402 version.

**Verdict:** PASS.

---

#### data_mc_qfb_kinf_magnus_1207_20260403.png

Q_FB at κ=∞ — three sharp spikes at integer Q values. Large pulls in empty bins between spikes are binning artifacts as documented in iteration 1. Same as 20260402 version.

**Verdict:** PASS with Category B note (empty-bin pulls are artifacts, not failures).

---

#### data_mc_thrust_magnus_1207_20260403.png

Thrust distribution. Fresh inspection confirms the structured pull pattern from iteration 1 persists: the pull panel shows negative pulls near thrust 0.85–0.95 and positive pulls at thrust ≥ 0.97, consistent with a slight thrust scale shift between data and MC. Several pulls reach ±2.5–3σ. The pattern is the same as 20260402 (same file size: 112,711 bytes).

**[VISUAL] Category B (unchanged from iteration 1):** Structured 2–3σ pull pattern in thrust indicating shape discrepancy. Should be documented as known in the AN.

**Verdict:** FLAG — Category B.

---

#### data_mc_costheta_magnus_1207_20260403.png

cos θ_thrust distribution — U-shaped. Good data/MC agreement. Pull panel mostly within ±2σ. Same as 20260402 version.

**Verdict:** PASS.

---

### TYPE: diagnostic (Phase 3)

#### cutflow_magnus_1207_20260403.png

Bar chart on log scale for 5 selection stages. Data (black) and MC (blue) visible. Same as 20260402 version (same file size: 143,961 bytes).

**Verdict:** PASS with Category C note (mixed event/track units on single y-axis).

---

#### d0_sign_validation_magnus_1207_20260403.png

b-enriched vs all-events d0 asymmetry curves. b-enriched reaches ~0.57 vs all-events ~0.30 at high thresholds. Clean figure, physics validated. Same as 20260402 version.

**Verdict:** PASS.

---

#### sigma_d0_calibration_magnus_1207_20260403.png

σ_d0 scale factors for 40 calibration bins. All factors in the range 1.5–7.5 (well above 1.0). Data and MC track each other. X-axis labels in very small font with only every 5th label shown. Same as 20260402 version.

**Verdict:** PASS with Category B note (scale factors 1.5–7× without annotated explanation; labels unreadable at AN rendering size).

---

### TYPE: result (Phase 3)

#### rb_operating_scan_magnus_1207_20260403.png

R_b extracted at working points 1–14 for combined (black circles) and probability-only (blue triangles) tags. Both sets decrease from ~0.95–1.0 at low WP to ~0.45–0.5 at WP 14. SM reference line and ALEPH reference line shown. Annotation box explains the Phase 3 bias. The annotation box text is in a moderate font — more readable than the 20260402 version based on visual comparison.

**[VISUAL] Category B (unchanged):** Annotation text readability is marginal at AN rendering size.

**Verdict:** PASS with Category B note.

---

## Cross-Figure Consistency Analysis

**CROSS-FIGURE CHECK 1: Data/MC agreement vs R_b extraction**

Phase 3 data/MC figures show consistently good agreement in event-level variables (thrust, cos θ, N_ch, Q_FB) — the thrust structured pull (B6) is the only notable shape discrepancy. The Phase 3 R_b scan shows biased values (0.5–1.0), documented as expected pre-calibration. The Phase 4a calibration produces R_b = 0.280 ± 0.031. The narrative remains internally consistent. PASS.

**CROSS-FIGURE CHECK 2: F2 (angular fit chi2) vs F7 (kappa consistency)**

F2 shows chi2/ndf = 31.9/8 (poor fit quality) for the A_FB linear model at κ=0.5. F7 shows chi2/ndf = 0.7/4 (excellent kappa consistency). These measure different things. The poor chi2 in F2 should be diagnosed in the AN text — it was flagged in iteration 1 and remains unfixed in the figure (A1 still open). The good kappa consistency in F7 does not resolve the visual impression of a bad fit in F2. Flag maintained.

**CROSS-FIGURE CHECK 3: Phase 4a closure pull vs Phase 3 closure tests**

Phase 4a closure pull at WP 9.0 = 1.93 (borderline pass, visually at 2σ). Phase 3 closure tests (updated 20260403) now show the mirrored closure correctly at R_b = 0.0000. The contamination injection shows ratio 2.14 (pass). The bFlag chi2 = 11,447 >> threshold 2 (pass — large chi2 means strong discrimination, not failure). No cross-figure inconsistency. PASS.

**CROSS-FIGURE CHECK 4: hemisphere_correlation vs C_b used in extraction**

The hemisphere_correlation figure shows C measured at WP 10 ≈ 1.55 (MC) / 1.50 (data), far above the published ALEPH C_b = 1.01. The extraction at WP 10 uses C_b from this figure (~1.55), which is consistent with the physics (C grows with tighter selection). The AN should explicitly state which C_b value was used in the final extraction and why C_b = 1.01 (ALEPH's value at their working point) is not appropriate for WP 10.0. This cross-figure inconsistency (C_b in figure vs C_b implied by ALEPH reference) requires AN text clarification. Category B.

---

## Summary of Findings — Iteration 2

### Status of Iteration 1 Category A Findings

| Iter-1 Tag | Status | Notes |
|------------|--------|-------|
| A1 (F2 chi2 display) | **NOT FIXED** | Code unchanged; chi2/ndf = 31.9/8 shown without better-fitting model or explanation in figure |
| A2 (F7 band visibility) | **NOT FIXED** | Code unchanged; blue combined band remains ~5px at AN rendering size, alpha=0.2 |
| A3 (closure panel rendering) | **FIXED** | Mirrored bar now correctly at y≈0 with annotation arrow; content verified via MD5 |
| A4 (chi2 annotation discrepancy) | **PARTIALLY FIXED → Category B** | Annotation now shows correct value (partially truncated); no numerical discrepancy |
| A5 (efficiency_calibration readability) | **NOT FIXED** | figsize=(30,10) unchanged; figure text unreadable at AN rendering size |

### New Category A Findings (Iteration 2)

| # | Figure | Finding |
|---|--------|---------|
| NA1 | closure_tests_magnus_1207_20260402.pdf (in AN) | 3-panel 10×10 composite produces extreme panel compression at AN rendering: x-tick labels ("Full sample", "Mirrored (no lifetime)") in x-small font will be illegible at ~2 cm panel width. Upgrade from B (iteration 1) to A based on fresh readability assessment. |

### Remaining Category A Violations

| # | Figure | Finding | Suggested Fix |
|---|--------|---------|--------------|
| A1 | F2_afb_angular_distribution.png | chi2/ndf = 31.9/8 displayed without resolution (no intercept-inclusive fit overlay, no explanation in figure) | Add intercept-inclusive fit curve overlay; annotate both chi2 values; or add text annotation explaining the chi2 |
| A2 | F7_afb_kappa_consistency.png | Combined result band (~±0.0022) nearly invisible at AN rendering size; alpha=0.2 compound with sub-pixel height | Zoom y-axis to data region, show ALEPH as off-plot arrow; or replace axhspan with distinct horizontal lines; or increase alpha to 0.5–0.8 |
| A5 | efficiency_calibration.png | figsize=(30,10); at 0.45 linewidth AN rendering each panel is ~0.15 linewidth; text unreadable | Split into three separate 10×10 figures or use properly scaled 3-panel with larger text |
| NA1 | closure_tests (Phase 3 in AN) | 3-panel 10×10 produces ~2 cm panel width at AN scale; x-tick labels illegible | Increase figure width, use abbreviated labels, or split to separate figures |

### Remaining Category B Violations

| # | Figure | Finding |
|---|--------|---------|
| B1 | closure_test_phase4a.png | Non-square figsize (20×10); right panel y-tick labels marginally readable at AN scale |
| B2 | F1_rb_stability_scan.png | Single-point scan; filename "stability_scan" is misleading |
| B3 | F4_fd_vs_fs.png | "Not directly comparable" annotation in xx-small font |
| B4 | F5_systematic_breakdown.png | Color coding threshold unexplained in legend |
| B5 | hemisphere_correlation.png | ALEPH C_b = 1.01 not linked to ALEPH's working point; appears as systematic disagreement |
| B6 | data_mc_thrust.png | Structured 2–3σ pull pattern indicating shape discrepancy |
| B7 | data_mc_qfb_k0.3/k0.5 | Mild structured pull patterns |
| B8 | sigma_d0_calibration.png | Scale factors 1.5–7× without annotated explanation |
| B9 (from A4) | closure_tests (Phase 3, panel b) | "chi2/ndf" annotation truncated at "11,44..." in narrow panel |
| B10 | rb_operating_scan.png | Annotation text readability marginal at AN scale |
| B11 (cross-figure) | hemisphere_correlation vs extraction | C_b at WP 10 ≈ 1.55 not explicitly stated as the value used in extraction; reader may assume ALEPH's 1.01 was used |

### Category C (Suggestions)

| # | Figure | Finding |
|---|--------|---------|
| C1 | cutflow | Mixed event/track units on single y-axis |
| C2 | data_mc_nch | Low N_ch negative pull pattern |
| C3 | data_mc_qfb_kinf | Empty-bin pull artifacts |

---

## Overall Assessment

**3 original Category A violations remain open (A1, A2, A5). 1 new Category A identified (NA1). 1 original A finding was FIXED (A3). 1 original A finding was downgraded to B (A4 → B9).**

The most critical unresolved findings are:

1. **A5** (efficiency_calibration.png non-square) — a core diagnostic figure is unpresentable in the AN. This requires a code change and figure regeneration before review can advance.
2. **A2** (F7 combined band invisible) — the primary physics result of the key result figure is the least visible element. This requires a code change and regeneration.
3. **A1** (F2 chi2 display) — leaves a result figure showing an apparently bad fit with no resolution.
4. **NA1** (Phase 3 closure panels illegible at AN rendering size) — affects the readability of the published closure validation.

**Upstream quality gate assessment:** Findings A1, A2, A5, and NA1 were all present in the iteration 1 review and none were addressed in the code. The executor was given findings from jasper_5871 but did not apply fixes to `plot_phase4a.py` (which remains at the same script mtime 06:20 on 04-03). Only the Phase 3 closure rendering bug (A3) was fixed via a Phase 3 re-run. This suggests the fixer agent applied the rendering fix to Phase 3 but did not address the Phase 4a plotting code issues. **The iteration is not complete** — three Category A issues in the Phase 4a plotting code require code changes before the validation can pass.

**Net iteration 2 result: ITERATE REQUIRED.** 3 Category A findings from iteration 1 remain open plus 1 new Category A. Blocking findings must be resolved before Doc 4a review can advance.
