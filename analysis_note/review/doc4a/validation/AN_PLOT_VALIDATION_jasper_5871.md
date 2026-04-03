# AN Plot Validation — Doc 4a
**Session:** jasper_5871  
**Date:** 2026-04-03  
**Validator role:** Level 3 (cross-figure consistency, physics narrative, composition quality)  
**Scope:** All figures appearing in ANALYSIS_NOTE_doc4a_v1.tex

---

## Step 1: Figure Registry Check

### Phase 3 Registry (`phase3_selection/outputs/FIGURES.json`)

- [x] FIGURES.json exists and is valid JSON
- [x] All 20 PNG entries have corresponding files on disk (no missing figures)
- [x] No orphan PNGs in `outputs/figures/` unregistered in FIGURES.json
- [x] All entries have all required fields: filename, type, script, description, lower_panel, is_2d, created, script_mtime
- [x] All `type` values are from the allowed set (data_mc, diagnostic, result, closure)
- [x] All `lower_panel` values are from the allowed set (pull, none)
- [x] No stale figures detected (all figures newer than registered script_mtime)

### Phase 4a Registry (`phase4_inference/4a_expected/outputs/FIGURES.json`)

- [x] FIGURES.json exists and is valid JSON
- [x] All 8 PNG entries have corresponding files on disk (no missing figures)
- [x] No orphan PNGs unregistered in FIGURES.json
- [x] All entries have all required fields
- [x] All `type` values are from the allowed set (result, systematic_impact, closure, diagnostic)
- [x] All `lower_panel` values are valid
- [x] No stale figures detected

### AN Figure Reference Check

- [x] All 36 PDF figures referenced in ANALYSIS_NOTE_doc4a_v1.tex exist in `analysis_note/figures/`
- [x] No orphan PDFs in `analysis_note/figures/` not referenced in the AN
- [x] No duplicate figure filenames

**[REGISTRY] RESULT: PASS — both registries are complete and consistent.**

---

## Step 2: Code Lint

Grepped all plotting scripts in `phase3_selection/src/` and `phase4_inference/4a_expected/src/`.

### Scripts checked
- `phase3_selection/src/plot_all.py`
- `phase3_selection/src/plot_utils.py`
- `phase4_inference/4a_expected/src/plot_phase4a.py`

### Forbidden pattern results

| Pattern | Result |
|---------|--------|
| `ax.set_title(` | Not found — PASS |
| `plt.colorbar` or `fig.colorbar(im, ax=` | Not found — PASS |
| `tight_layout` | Not found — PASS |
| `imshow` | Not found — PASS |
| `histtype="errorbar"` without `yerr=` | Not found — PASS |
| `\begin{subfigure}` in .tex | Not found — PASS |
| `data=False` with `llabel=` | Not found — PASS |
| `np.sqrt(h.values())` near `yerr=` | Not found — PASS |
| `.view()[:]` near `histtype="errorbar"` | Not found — PASS |

### figsize violations

**[LINT] VIOLATION (Category B):** `plot_phase4a.py` lines 352 and 399:
```python
fig, axes = plt.subplots(1, 2, figsize=(20, 10))   # closure_test_phase4a
fig, axes = plt.subplots(1, 3, figsize=(30, 10))   # efficiency_calibration
```
Multi-panel figures use non-square dimensions. Spec requires `(10, 10)` for all figures. Multi-panel composites should either use `(10, 10)` with appropriate height ratios, or be split into separate square figures. These figures appear in the AN as side-by-side panels which helps, but the source dimensions are still non-square.

**[LINT] NOTE (Category B — borderline):** `plot_all.py` line 581:
```python
fig, axes = plt.subplots(1, 3, figsize=(10, 10))   # closure_tests
```
Three panels in a square figure produces a 3.33:1 width-to-height aspect ratio per panel. The rendered output confirms this results in severely compressed panels (see visual review below).

### Normalization documentation

MC is normalized to data integral throughout (mc_scale_to_data=True by default in `data_mc_pull()`). The legend correctly states "MC (normalized to data)" in all data/MC plots. This is consistent and documented.

**[LINT] NOTE (Category C):** `plot_utils.py` also normalizes MC to data integral in `data_mc_comparison()` but uses "MC" (without "normalized to data") as the default `mc_label`. However, in practice `plot_all.py` passes "MC (normalized to data)" explicitly. No actual violation in rendered output.

### Phase 4+ pull label check

`plot_phase4a.py` does not produce data/MC comparison plots — only result, systematic_impact, diagnostic, and closure figures. No ratio-vs-pull issue applies.

### Cross-phase import

`plot_phase4a.py` imports `plot_utils` from Phase 3 (lines 27–29). This satisfies the cross-phase import requirement.

**[LINT] RESULT: 1 Category B violation (non-square figsize in phase4a), 1 Category B note (3-panel closure in square figure). No Category A violations.**

---

## Step 3: Visual Review by Type

All figures are reviewed individually. For each, a minimum 3-sentence description is provided before the verdict.

---

### TYPE: result

#### F1_rb_stability_scan.png

The figure shows a single MC pseudo-data point at combined tag threshold WP 10.0, with a measurement of R_b = 0.280 ± 0.031 (error bar visible). The ALEPH published band (blue, R_b = 0.2158 ± 0.0014) and LEP combined band (green, very narrow) appear as horizontal spans; the SM value (red dashed) appears as a horizontal line around y = 0.28 — very close to where the data point lies. The x-axis spans WP 9.5–10.5, which is an extremely narrow range containing only a single measurement point; the figure is titled "stability scan" but contains no scan — this mismatch between figure description and content is documented in the code comment ("only WP 10.0 yields a valid extraction") and the AN caption acknowledges it explicitly.

**Specific checks:**
- Square aspect ratio (10x10): PASS
- Experiment label present (ALEPH Open Simulation): PASS
- No axis title: PASS
- Legend does not overlap data: The legend box sits in the upper region and the data point is near the bottom-center. PASS
- The y-axis label "R_b" is present but appears as a small subscript-b label at top-left — it is technically there.
- Caption-figure coherence: The caption says "Only WP 10.0 yields a valid extraction (R_b = 0.280 ± 0.031); all other working points return null." The figure shows exactly one point. PASS.
- The ALEPH band appears as a thick blue horizontal band. The SM value (red dotted line) is barely distinguishable from the ALEPH band; both sit very close to y~0.28, and the annotation describing R_b = 0.21578 for SM is at the top of the plot near 0.28 — the SM line and ALEPH band overlap visually near y=0.216–0.222 while the data point is at y~0.28, above them. The distinction between SM (0.216) and the data point (0.280) is clear.

**[VISUAL] WARNING (Category B):** The x-axis range (9.5 to 10.5) contains only a single data point; axes range is narrow and provides no "stability" information. This is documented in the code and caption, but the x-axis could usefully show a wider range to visually reinforce the documented limitation. Not a publication blocker but a presentation weakness.

**[VISUAL] WARNING (Category B):** The figure is labeled "F1_rb_stability_scan" and the AN figure caption begins "$R_b$ operating point stability scan" — but the figure contains only one point. The caption does acknowledge this limitation, but the figure title in the filename/description creates a potential reader confusion. Both the code comment and the FIGURES.json description note this explicitly. Acceptable as documented, but could be renamed "F1_rb_extraction" for clarity.

**Verdict:** PASS with Category B notes on naming and x-axis range. No blocking issue.

---

#### F2_afb_angular_distribution.png

The figure shows mean Q_FB (y-axis, labeled ⟨Q_FB⟩) vs cos(θ_thrust) (x-axis), with 10 MC pseudo-data points shown as black error bars. The red fit line has a gentle positive slope (slope = 0.00037 ± 0.00107). The data points are scattered around a constant negative offset of approximately −0.004 with large statistical error bars; several points at cos θ ≈ 0 to 0.5 are notably high relative to the fit line. The chi2/ndf = 31.9/8 annotation appears in a yellow box in the upper-left corner, and N_tagged = 467,279 is also annotated.

**Specific checks:**
- Square aspect ratio: PASS
- Experiment label (ALEPH Open Simulation): PASS
- Legend present (fit slope + data): PASS
- Legend does not overlap data: The legend sits lower-center, where some data points also reside. At the rendered figure size (~0.45 linewidth in the AN), the legend box may be tight but is readable.
- Caption-figure coherence: Caption states "slopes are consistent with zero, as expected for symmetric MC." The figure shows slope = 0.00037, consistent with zero. PASS.
- y-axis label uses proper LaTeX (⟨Q_FB⟩): PASS
- Units present where needed: Q_FB is dimensionless, no unit required. PASS.

**[VISUAL] CONCERN (Category A — PHYSICS DIAGNOSTIC):** The chi2/ndf = 31.9/8 (p < 0.001) corresponds to a very poor fit. The residuals show systematic structure: the data points at intermediate cos θ values sit above the linear fit while the extreme values are below, suggesting a non-linear relationship or unmodeled offset that the linear fit cannot capture. The caption says "slopes are consistent with zero" and the AN text notes the intercept-inclusive fit "substantially improves chi2" — but the figure (using the origin-only fit) shows a demonstrably poor chi2/ndf. The AN table lists chi2/ndf = 31.9/8 for kappa=0.5 but marks this as from the origin-only fit. This is an UNDIAGNOSED PATTERN in the figure: a chi2 of 31.9/8 is not "fits poorly due to zero slope" — it indicates the data does not follow the fitted line. The caption attributes the offset to "hemisphere charge bias absorbed by the intercept term" but the figure does not show the intercept-inclusive fit that actually fits well. A reviewer reading the figure as presented sees a manifestly poor fit. This is a Level 3 upstream quality gate issue: the figure should either show the better-fitting model (with intercept) or explicitly annotate the chi2 improvement from the intercept-inclusive version.

**Verdict:** FLAG — Category A (poor chi2/ndf shown without the better-fitting model; reader sees a bad fit without resolution shown in the figure itself). Suggested fix: show the intercept-inclusive fit curve overlaid, annotate both chi2 values, or replace the origin-only curve with the full-model curve.

---

#### F4_fd_vs_fs.png

The figure shows the double-tag fraction f_d (y-axis) vs the single-tag fraction f_s (x-axis), with MC pseudo-data points shown as a connected black line with markers tracing a curve in the (f_s, f_d) plane. Three overlaid prediction curves for R_b = 0.216 (red dashed), 0.200 (blue dotted), and 0.250 (green dotted) are drawn using fixed WP 10 efficiencies. A yellow annotation box in the lower-left documents the interpretation limitation: "Data trace a locus of varying efficiencies; prediction curves use fixed WP 10 efficiencies. The two are not directly comparable."

**Specific checks:**
- Square aspect ratio: PASS
- Experiment label (ALEPH Open Simulation): PASS
- No gap between caption description and figure content: Caption correctly describes the trajectory interpretation. PASS.
- Legend present: PASS (legend in upper-left lists all three R_b curves and "MC pseudo-data").
- Axis labels include descriptive names and not code variable names: PASS (f_s and f_d labeled clearly).

**[VISUAL] CONCERN (Category B):** The data trajectory (black solid line) lies well below all three R_b prediction curves across most of the f_s range, only joining them near the high-f_s end. This visual gap could mislead a reader into thinking the extraction fails or is inconsistent. The annotation box addresses this but is very small (xx-small font) at AN rendering size (~0.45 linewidth). The caption explains the non-comparability but the visual discrepancy between data trajectory and all prediction curves is stark. Consider enlarging the annotation or moving the "not directly comparable" note to the caption body more prominently.

**Verdict:** PASS with Category B warning on annotation legibility at AN rendering size.

---

#### F7_afb_kappa_consistency.png

The figure shows A_FB^b (y-axis) extracted at five kappa values (x-axis, using custom ticks 0.3, 0.5, 1.0, 2.0, ∞) as black error bars. The blue band (Combined = −0.0001 ± 0.0022) is barely visible near y=0 as a very thin blue horizontal band. The green band (ALEPH = 0.0927 ± 0.0052) appears as a thick green horizontal span at the top of the plot, far above the data points. The chi2/ndf = 0.7/4, p = 0.950 annotation appears in a wheat-colored box at lower right. The data points all cluster tightly near y = 0, except for the kappa=0.3 point which appears slightly above (y ~ +0.006).

**Specific checks:**
- Square aspect ratio: PASS
- Experiment label: PASS
- Custom x-tick labels (0.3, 0.5, 1.0, 2.0, ∞): PASS
- Legend present: PASS
- y-axis range: spans roughly −0.01 to +0.10, capturing both the near-zero data region and the ALEPH reference band. PASS.

**[VISUAL] CONCERN (Category A — PHYSICS DIAGNOSTIC):** The figure shows our MC result (consistent with zero) and the ALEPH published value (0.0927) separated by approximately 40 mm of whitespace on the plot, with no connecting diagnostic shown. The green ALEPH band occupies the top 10% of the plot; the blue combined band is almost invisible (~0.5 mm thick) near y=0. At AN rendering size (~0.45 linewidth), the blue combined band will be sub-pixel and may not render visibly at all. This is a presentation failure: the primary result (combined A_FB^b) is the thinnest feature in the figure. Suggested fix: either zoom the y-axis to focus on the data region (showing ALEPH as an off-plot arrow), or make the combined band visually prominent with a wider band width and/or shading.

**[VISUAL] NOTE:** The figure correctly represents the physics (MC has no asymmetry; the comparison to ALEPH is not meaningful at 4a). The caption in the AN explains this correctly. No physics error.

**Verdict:** FLAG — Category A (primary result band nearly invisible at AN rendering size). Category B on overall visual hierarchy.

---

### TYPE: systematic_impact

#### F5_systematic_breakdown.png

The figure is a horizontal bar chart showing R_b systematic uncertainty contributions from 13 sources, ranked by magnitude on a log-scale x-axis. The bars are split into two colors: blue (C0) for sources > 0.3e-3 and orange (C1) for smaller sources. The dominant source "Light mistag ε_uds" bar extends to the right edge of the plot, truncated by the axis. Two vertical dashed lines mark the total systematic (red dashed, labeled 395.28 × 10^-3) and statistical (blue dotted, labeled 30.52 × 10^-3). An annotation note in the lower-right reads "Note: ε_uds contributes 99.5% of total syst."

**Specific checks:**
- Square aspect ratio: PASS
- Experiment label (ALEPH Open Simulation): PASS
- y-axis labels use publication-quality names (not code names): PASS — all labels use LaTeX notation (ε_uds, ε_c, σ_d0 parameterization, etc.)
- Legend present: PASS (total syst. and statistical lines labeled)
- Log x-scale: PASS (appropriate for spanning 3 orders of magnitude)

**[VISUAL] CONCERN (Category A):** The "Light mistag ε_uds" bar is so dominant that it appears to extend beyond the right axis boundary — the bar is truncated at the axis edge (x ~ 10^3 × 10^-3 = 1, but the total syst. is 395.28 × 10^-3 = 0.395, so the uds bar should extend to ~395 × 10^-3). The total systematic line (red dashed) and the uds bar must be at approximately the same x value. Looking at the figure: the uds bar appears to end near the total syst. vertical line, which is correct. The issue is readability — with the bar touching the vertical "total syst." line, it appears truncated. This is an artifact of the bar chart combined with vertical reference lines at the same value.

**[VISUAL] CONCERN (Category B):** The two-color coding (blue for large impacts > 0.3e-3, orange for small) is applied to only 4 sources in orange (Physics parameters, Gluon splitting g_cc, Gluon splitting g_bb, tau contamination, Selection bias). The distinction between "large" and "small" at the 0.3e-3 threshold is somewhat arbitrary and is not labeled in the legend. A reader might wonder what the color distinction means. Consider adding a legend entry or annotation explaining the threshold.

**[VISUAL] NOTE:** The per-source systematic contributions are distinguishable, the bars have realistic variation (spanning ~3 orders of magnitude), and the color coding is functionally adequate. The figure communicates the ε_uds dominance clearly.

**Verdict:** PASS with Category B note on color coding documentation. The figure is functional despite the crowding at the dominant source bar.

---

### TYPE: closure

#### closure_test_phase4a.png

The figure is a two-panel composite (1x2 layout, figsize=(20,10) — non-square source, Category B lint finding). The left panel shows the independent closure test with a single data point at WP 9.0, pull ≈ 2.0, with 2σ reference lines (red dotted). The right panel shows a horizontal bar chart of corrupted-correction sensitivity tests: red bars for failed cases (|pull| > 2σ) and one or two blue bars for the C_b corruptions that passed. The label "Corrupted corrections (should FAIL)" appears as text in the upper-right panel. The experiment label appears on the left panel only.

**Specific checks:**
- Experiment label on left panel only: PASS (experiment label should appear on the main panel only; for a composite, left panel is appropriate)
- Square aspect ratio at source level: FAIL (20x10 — Category B lint finding confirmed visually; the rendered composite is landscape, not square)
- Pull panel range: The left panel shows y-axis −4 to +4. PASS.
- Closure test sensitivity: The right panel shows that +20% ε_uds and −20% ε_uds corruptions produce very large pulls (bars extend past 5 or −15), confirming sensitivity. PASS.

**[VISUAL] CONCERN (Category A):** The single closure test point at WP 9.0 shows pull ≈ 2.0 — exactly at the 2σ threshold. This is a borderline pass. The AN text states "pull = 1.93 (pass, < 2σ)" which is technically true, but visually the point appears to sit at or above the 2σ red line. At AN rendering size, this borderline pass could be misread as a failure. The figure caption in the AN correctly states the pull value numerically, which resolves the ambiguity for careful readers.

**[VISUAL] CONCERN (Category B):** The right panel horizontal bar chart has y-axis labels ("+ 20% eps_c", "−20% eps_c", etc.) in very small font (xx-small in code). At AN rendering size (~0.45 linewidth for the full composite, so each panel is ~0.225 linewidth), these labels will be extremely difficult to read.

**[VISUAL] NOTE (Category B):** Non-square source dimensions (20x10) confirmed — flagged in lint. At the rendered size in the AN, the figure appears compressed horizontally and text in the right panel is cramped.

**Verdict:** FLAG — Category B (non-square dimensions, small labels in right panel). Category A note on borderline closure pull visual appearance. Not a blocking finding given numerical AN documentation, but the label readability is a genuine concern.

---

#### closure_tests_magnus_1207_20260402.png (Phase 3)

The figure is a three-panel composite in a square (10x10) frame, giving each panel a 3.3:1 width-to-height ratio. The left panel (a) shows two red bars for "Full sample" (R_b ~ 0.83) and "Mirrored (no lifetime)" (R_b ~ 0.83); a "PASS" verdict in red text with "R_b = 0.0000" is annotated. The center panel (b) shows a single tall red bar for chi2/ndf shape (value ~ 1.1×10^4); the panel label is partially obscured by a small text box at the top reading "chi2/ndf 1144". The right panel (c) shows two bars — a short blue "Predicted shift" and a taller red "Observed shift" — with a "PASS, Ratio = 2.14" annotation.

**Specific checks:**
- Square aspect ratio: The source is (10,10) but the 1x3 layout makes each panel ~3.3:1 landscape. The visual rendering is extremely wide relative to height per panel.
- Experiment label: Appears in the left panel. PASS (experiment label on first panel of composite).
- y-axis labels: "R_b" on left, "chi2/ndf (shape)" on center (log scale), "|ΔR_b|" on right. PASS for publication quality.

**[VISUAL] CONCERN (Category A):** The left panel shows two bars that appear essentially identical in height (both at R_b ~ 0.83), but the PASS annotation says "R_b = 0.0000" for the mirrored closure. The description is that R_b = 0 should be obtained on mirrored pseudo-data (no lifetime signal), which would correspond to a bar at y=0. However, the left panel bars clearly both show R_b ~ 0.83. This is inconsistent with the annotation and the closure test interpretation. After careful re-reading of the code: the left panel plots both "Full sample" R_b and "Mirrored (no lifetime)" R_b from the closure result JSON. If R_b = 0.0000 as annotated, then the "Mirrored" bar should be at y=0, not at y~0.83. This is a potential **misrendering** — either the bar values are wrong, or the annotation is wrong, or the vertical axis does not start at zero and both bars are actually close to the floor. Looking at the figure: both bars appear to fill most of the y-axis height, with the axis running from 0.0 to about 0.85. If the PASS annotation says R_b = 0.0000, but the bar height shows R_b = 0.83... the bar must correspond to the "Full sample" and the "Mirrored" bar must be either at y=0 (invisible) or the labels/bars are swapped.

**[VISUAL] SEVERE CONCERN (Category A — RED FLAG):** The closure test in panel (a) shows both bars at equal height (~0.83), but the test is supposed to show that mirrored significance gives R_b = 0. If the mirrored bar is at 0.83 instead of 0, the test is either mislabeled or the closure genuinely failed for this test (R_b != 0 on mirrored data). Either interpretation is Category A: it is either a mislabeled/misrendered figure, or the closure test for the "mirrored significance" case shows R_b = 0.83, which does not validate zero lifetime sensitivity.

On careful inspection, the bars in panel (a) are both at y~0.83 (identical height). The PASS annotation "R_b = 0.0000" and the yellow box with "PASS" are overlaid. The AN caption says "mirrored-significance code sanity check (f_s = 0 as expected)". The FIGURES.json description says "mirrored-significance pseudo-data (R_b=0 expected, no lifetime signal)." If R_b = 0 is expected and obtained, the bar should be at y=0. This is a clear rendering bug: both bars appear at the same nonzero height. The R_b = 0.0000 result is stated in text but not visible in the bar height.

**[VISUAL] ADDITIONAL CONCERN (Category A):** The center panel (b) is the bFlag chi2/ndf test showing chi2 ~ 1.1×10^4. The panel label text "chi2/ndf 1144" appears in a small box near the top of the bar, partially overlapping the bar. At AN rendering size, the text "chi2/ndf 1144" overwrites the bar annotation. The referenced AN caption says "chi2/ndf = 11,447" — the figure shows "1144" (abbreviated). This numerical discrepancy between the figure annotation and the caption text should be clarified.

**[VISUAL] CONCERN (Category B):** The 1×3 panel in a 10×10 figure produces extremely compressed panels with poor aspect ratio. As noted in code lint, this is a presentation issue that makes all labels very small.

**Verdict:** FLAG — Category A (RED FLAG): panel (a) shows both bars at equal height while annotation says R_b = 0.0000; this is either a rendering bug or the closure test did not actually return R_b = 0 for mirrored data. Requires investigation and figure regeneration with bars correctly positioned. Category A: chi2/ndf annotation in panel (b) shows "1144" while AN caption states "11,447" — numerical discrepancy. Category B: compressed panel layout.

---

### TYPE: diagnostic

#### efficiency_calibration.png (Phase 4a)

The figure is a three-panel composite (1x3 layout, figsize=(30,10) — severely non-square). The panels show ε_b (blue), ε_c (orange), and ε_uds (red) efficiency curves vs working point (7.0 to 10.0). All three panels show smooth monotonic curves. The y-axis labels (ε_b, ε_c, ε_uds) appear as single-character subscripts in very small text at the top of each panel. The experiment label appears only on the leftmost panel.

**Specific checks:**
- Square aspect ratio: FAIL — figsize=(30,10) is 3:1 landscape. Category B lint finding confirmed.
- Experiment label on left panel only: PASS
- y-axis labels: ε_b, ε_c, ε_uds are proper publication-quality labels. PASS.
- x-axis label: "Working point" on all three panels. PASS.
- Curves show realistic physics: ε_b decreases from ~0.35 to ~0.25 as WP increases (tighter tag), ε_c from ~0.6 to ~0.43, ε_uds from ~0.175 to ~0.08. These trends are physically sensible — higher working points exclude more events, reducing all efficiencies.

**[VISUAL] CONCERN (Category A):** At AN rendering size (~0.45 linewidth for the full composite, meaning each panel is ~0.15 linewidth), the y-axis tick labels and axis labels will be extremely small. The ε_b, ε_c, ε_uds labels in the figure appear at "x-small" fontsize — at 0.15 linewidth rendering, these will be nearly unreadable. This is a readability failure.

**[VISUAL] CONCERN (Category B):** The figsize=(30,10) source produces three square-ish panels (10×10 each), but since they are composited into a 30×10 figure and saved at dpi=200, the resulting PNG at 6000×2000 pixels is fine for screen viewing but when rendered in the AN at ~0.45 linewidth (~6 cm), the entire three-panel composite is only about 2 cm tall — making text illegible at print resolution.

**[VISUAL] NOTE:** The "From MC (SM truth)" annotation appears in a wheat box in the left panel. This annotation is helpful and at this location does not overlap data. PASS.

**Verdict:** FLAG — Category A (readability failure at AN rendering size for 3-panel 30×10 composite). The three panels should either be presented as three separate square figures (each at 0.45 linewidth) or as a 3-panel figure with appropriate scaling per the appendix-plotting.md compositing rules.

---

#### hemisphere_correlation.png (Phase 4a)

The figure shows hemisphere correlation C vs combined tag threshold for MC (blue squares) and data (black circles), with the published ALEPH C_b = 1.01 reference line (red dashed). Both MC and data show a strongly increasing C from ~1.03 at WP 2 to ~1.55 at WP 10, far above the ALEPH published value of 1.01.

**Specific checks:**
- Square aspect ratio (10x10): PASS
- Experiment label (ALEPH Open Simulation): PASS
- Legend: MC, Data, and ALEPH reference all labeled. PASS.
- y-axis label: "Hemisphere correlation C" — clear and readable. PASS.
- x-axis label: "Combined tag threshold" — clear. PASS.

**[VISUAL] CONCERN (Category A — PHYSICS DIAGNOSTIC):** The measured correlation C grows from ~1.03 at low working points to ~1.55 at WP 10.0, while the published ALEPH C_b value is 1.01. The discrepancy at WP 10.0 (C ~ 1.55 vs 1.01) is ~50% relative and represents 3–4 orders of magnitude difference in the hemisphere correlation factor's significance for R_b extraction. This large discrepancy is not diagnosed in the figure or the AN text near this figure. The AN text (Section 7.5) mentions "C_b measured from MC and data at each working point" but does not explain why the measured C is 1.01–1.55 across WPs when the ALEPH published value is 1.01 (appropriate at their working point). This may be physically correct (ALEPH's working point had a lower tag threshold than WP 10.0, so C_b = 1.01 at their operating point while C_b = 1.55 at WP 10.0 is plausible from the measured trend). However, the figure does not annotate which working point ALEPH used for their C_b measurement, making the comparison misleading — the ALEPH C_b = 1.01 reference line appears as a flat horizontal that is systematically well below all measured values, which could confuse a reader into thinking there is a fundamental disagreement.

**Verdict:** FLAG — Category B (missing annotation linking ALEPH's C_b = 1.01 to their specific working point; current display implies systematic disagreement rather than working-point-dependent comparison). The caption in the AN should clarify this comparison.

---

#### sigma_d0_calibration_magnus_1207_20260402.png (Phase 3)

The figure shows σ_d0 scale factors for 40 calibration bins (x-axis, labeled "Calibration bin (nvdet, p [GeV/c], |cos θ|)") with data (black circles) and MC (blue squares). Scale factors range from approximately 1.5 to 7.5 (well above the horizontal reference line at 1.0). The x-axis shows compact bin labels in very small font (xx-small), with only every 5th label shown (roughly 8 visible labels out of 40).

**Specific checks:**
- Square aspect ratio (10x10): PASS
- Experiment label (ALEPH Open Data): PASS
- y-axis label: "σ_d0 scale factor" — clear. PASS.
- Axis labels not code variables: The x-tick labels use abbreviated human-readable format (nv=1, p=[0,1], |ct|=[0.00,0.25]). PASS for publication quality.

**[VISUAL] CONCERN (Category B):** All scale factors are in the range 1.5–7.5, well above 1.0. This means the nominal σ_d0 parameterization consistently underestimates the actual impact parameter resolution by factors of 1.5 to 7.5 across all bins. The figure shows no annotated explanation for why scale factors this large (up to 7×) are expected or acceptable. At AN rendering size, the calibration scatter is visible but the individual bin labels are unreadable.

**[VISUAL] NOTE:** The data and MC scale factors track each other reasonably well across most bins, with some divergence in specific momentum ranges. This is physically consistent (both need large corrections to describe data) and the agreement between Data and MC scale factors suggests consistent correction requirements.

**Verdict:** PASS with Category B note (large scale factors without annotated physics explanation; all labels unreadable at AN rendering size). The figure communicates the key finding (systematic correction needed) adequately.

---

#### cutflow_magnus_1207_20260402.png (Phase 3)

The figure is a bar chart on a log scale showing event/track counts for Data (black) and MC (blue, labeled "MC (scaled)") at five selection stages. The x-axis labels are: "Total events," "Basic quality," "|cos θ_thrust| < 0.9," "All tracks," "Quality tracks (VDET, purity, TPC)." The bars show a jump of ~3 orders of magnitude between the event-level cuts (~3–5 million) and the track-level counts (~100 million), which is physically expected (many tracks per event).

**Specific checks:**
- Square aspect ratio: PASS (10x10)
- Experiment label (ALEPH Open Data): PASS
- y-axis label: "Events / Tracks" — adequate for a mixed-unit plot. PASS.
- x-axis labels rotated 45°, readable. PASS.
- Data/MC agreement visible at all stages. PASS.

**[VISUAL] CONCERN (Category B):** Mixing event-level counts ("Total events," "Basic quality," "|cos θ_thrust| < 0.9") with track-level counts ("All tracks," "Quality tracks") on the same y-axis is dimensionally inconsistent — these quantities have different physical meanings and units. The y-axis label "Events / Tracks" acknowledges this, and the log scale makes the transitions visible, but a reader may find it confusing to see "All tracks" (10^8) compared to "Total events" (10^6) on the same axis without explanation of the ~100× jump.

**[VISUAL] NOTE:** The cutflow is monotonically non-increasing within the event stage and within the track stage, which is correct. The bar chart does not show the |cos θ| cut having significant impact (Basic quality and the angular cut bars appear similar height), consistent with the ~90% angular acceptance.

**Verdict:** PASS with Category B note (mixed event/track units on single axis; could benefit from splitting into two panels or annotating the event-to-track transition).

---

#### d0_sign_validation_magnus_1207_20260402.png (Phase 3)

The figure shows two asymmetry curves (b-enriched in purple/magenta with filled circles, all events in blue with squares) as functions of |d0/σ_d0| threshold from 1 to 10. Both curves rise sharply from the threshold 1 to 3, then plateau. The b-enriched curve reaches ~0.57 and the all-events curve reaches ~0.30. A "Gate: PASS" annotation appears in the lower-right legend area.

**Specific checks:**
- Square aspect ratio (10x10): PASS
- Experiment label (ALEPH Open Data): PASS
- y-axis label: "Asymmetry (N+ − N−)/(N+ + N−)" — publication quality. PASS.
- x-axis label: "|d0/σ_d0| threshold" — clear. PASS.
- Legend includes event counts (231,054 events for b-enriched): PASS.

**[VISUAL] NOTE:** The b-enriched asymmetry (~0.57) being higher than the all-events asymmetry (~0.30) at all thresholds demonstrates the expected physics: b-enriched samples have more lifetime signal and thus more large-|d0| tracks, giving higher positive asymmetry. This confirms the d0 sign convention is physically meaningful. PASS on physics diagnostic.

**Verdict:** PASS — figure cleanly communicates the d0 sign convention validation.

---

### TYPE: data_mc

All data/MC figures follow the same template from `plot_utils.py` / `data_mc_pull()`: MC as blue filled histogram (step+fill), data as black errorbar points, pull panel with pulls labeled from −4 to +4, MC normalized to data integral with legend label "MC (normalized to data)." This template is consistently applied.

Universal checks (applying to all 12 data/MC figures):
- Experiment label on main panel only: PASS for all
- Data as black errorbar: PASS for all
- MC as filled histogram: PASS for all
- Pull panel: PASS for all (uses pulls, not ratio)
- Lower panel label: "Pull" on all figures — PASS (pull label, not "Ratio" or "Data/MC")
- No experiment label on pull panel: PASS for all
- No gap between main and pull panels (hspace=0): PASS visually for all

#### data_mc_significance_magnus_1207_20260402.png

Shows signed d0/σ_d0 on log y-scale. The distribution is heavily peaked near 0 with an exponential positive tail (b-hadron lifetime signal). The MC follows data very well visually. The pull panel shows pulls mostly within ±2σ with a few excursions near the tails.

The figure shows a long positive tail extending to ~30σ, which is the b-lifetime signature. The pull panel shows a few pulls at ±3σ at the extreme tail (bins with few counts). This is statistically expected in low-count tail regions.

**[VISUAL] CONCERN (Category B):** Pull panel bins at extreme values (d0/σ > 20) appear to have very large pulls (visually up to ±3σ). These could be statistically driven by low bin counts in the tail. The AN should note the expected pull distribution (with ~5% of bins above 2σ for 100 bins, ~5 bins above 2σ expected). No investigation required if the count is consistent with statistical expectation.

**Verdict:** PASS with Category B note on tail pull statistics.

---

#### data_mc_combined_tag_magnus_1207_20260402.png

Shows the combined hemisphere tag (−ln P_hem + mass bonus) on log scale. The distribution falls from peak near 0 to very small values near 20. Pulls are mostly within ±2σ with scatter; several bins at high tag values (> 15) show pulls of ±2–3σ.

The combined tag shows excellent data/MC agreement in the bulk (tag 0–12), with expected statistical fluctuations at the tail where b-tagged hemispheres concentrate. The pull panel scatter is consistent with random fluctuations; no systematic offset or shape trend is visible.

**Verdict:** PASS.

---

#### data_mc_hemisphere_mass_magnus_1207_20260402.png

Shows hemisphere invariant mass on linear scale. The distribution peaks sharply at low mass and falls smoothly. A purple dashed vertical line marks the b/c threshold at 1.8 GeV/c². Data and MC agree well visually. The pull panel shows random scatter within ±3σ with no systematic trend.

**[VISUAL] CONCERN (Category B):** The b/c threshold line at 1.8 GeV/c² also appears in the pull panel (as a faint purple dashed line). Per the universal checks, additional vertical lines in the pull panel can create visual clutter. However, this is a minor annotation for orientation, not an experiment label. Acceptable.

**Verdict:** PASS.

---

#### data_mc_phem_magnus_1207_20260402.png

Shows −ln P_hem on log scale. Shape falls from peak at ~0 to tail at ~15. Good visual data/MC agreement. Pull panel shows several bins with pulls ≥ 2σ at the high-tag tail.

**Verdict:** PASS.

---

#### data_mc_qfb_k0.3_magnus_1207_20260402.png

Shows Q_FB at κ=0.3 — a Gaussian-shaped distribution centered at zero. Excellent data/MC agreement visible. The pull panel shows a systematic pattern: pulls at the edges (large |Q_FB|) are slightly positive while pulls near the center are slightly negative, suggesting a very mild shape discrepancy. The pattern appears within ±2.5σ.

**[VISUAL] CONCERN (Category B):** There is a visible alternating pattern in the pull panel that follows a positive-then-negative-then-positive sequence. This suggests a mild shape discrepancy rather than random fluctuations. The AN caption (Appendix section) states "good agreement across all three values." The pattern is within 2.5σ but is structured rather than random.

**Verdict:** PASS with Category B warning (structured pull pattern in Q_FB at κ=0.3; check if chi2/ndf is elevated).

---

#### data_mc_qfb_k0.5_magnus_1207_20260402.png

Shows Q_FB at κ=0.5 with good visual data/MC agreement. The pull panel shows a similar mild structured pattern as κ=0.3. Overall within ±2.5σ.

**Verdict:** PASS (same Category B note as κ=0.3).

---

#### data_mc_qfb_k1.0_magnus_1207_20260402.png

Shows Q_FB at κ=1.0 — broader Gaussian. Data/MC agreement is excellent. Pull panel shows random scatter within ±1.5σ, the cleanest of the Q_FB series.

**Verdict:** PASS.

---

#### data_mc_qfb_k2.0_magnus_1207_20260402.png

Shows Q_FB at κ=2.0 — flat-topped trapezoidal distribution (kinematic endpoint effects). Data/MC agreement is excellent across the plateau and edges. Pull panel is clean.

**Verdict:** PASS.

---

#### data_mc_qfb_kinf_magnus_1207_20260402.png

Shows Q_FB at κ=∞ (leading particle charge) — three sharp spikes at Q_FB = −2, 0, +2 (integer values from leading track charge). The MC fills these three bins with large counts; data points appear as black dots on the MC histogram for the three filled bins, with many empty bins between. The pull panel shows very large pulls (±3σ) in the empty bins between the three signal bins — these are bins with MC=0 and Data≈0, where statistical fluctuations give undefined or large pulls.

**[VISUAL] CONCERN (Category B):** The pull panel for the κ=∞ figure shows large pull excursions (visually ≥3σ in multiple bins) in the empty regions between the Q_FB = {−2, 0, +2} spikes. These are not genuine physics failures — they arise because empty bins produce undefined or singular pulls when both MC and data are zero (division by zero → pull=0) or when one is nonzero by a fluctuation. The 1-error-bar pull formula assigns pull=1 per the code, but bins where MC=0 should be masked. This is a cosmetic issue that could mislead a reviewer.

**Verdict:** PASS with Category B note (empty-bin pulls in pull panel for discrete Q_FB distribution look alarming but are an artifact of the binning choice).

---

#### data_mc_thrust_magnus_1207_20260402.png

Shows thrust distribution from 0.5 to 1.0. The distribution is sharply peaked near thrust=1 (jet-like events) with a long tail at lower thrust. Data/MC agreement is visually good in the bulk but the pull panel shows a structured pattern: negative pulls around thrust 0.85–0.95 and positive pulls at thrust ≥ 0.95. Several pulls reach ±2.5–3σ. This indicates a shape discrepancy in the thrust distribution.

**[VISUAL] CONCERN (Category A — PHYSICS DIAGNOSTIC):** The thrust pull pattern shows a systematic x-offset structure (data peaks slightly earlier than MC at thrust ~ 0.97, then data falls below MC at thrust ~ 0.99, then data is above at thrust = 1.0). This is consistent with a slight thrust scale calibration issue: the simulation places events at slightly higher thrust values than observed in data. A systematic shape mismodelling in thrust at the level of 2–3σ in multiple consecutive bins represents a shape disagreement that could affect the event selection if the thrust axis cut (|cos θ_thrust| selection is correlated with thrust shape). The AN should document this known shape discrepancy.

**Verdict:** FLAG — Category B (structured 2–3σ pull pattern in thrust; needs documentation as known shape discrepancy even if not a blocking issue for this analysis).

---

#### data_mc_costheta_magnus_1207_20260402.png

Shows cos θ_thrust distribution — a U-shaped curve (cos θ acceptance with endpoint enhancement). Data/MC agreement is very good visually. The pull panel shows random scatter mostly within ±2σ with no systematic trend. A few pulls at ±2σ at the boundaries.

**Verdict:** PASS.

---

#### data_mc_nch_magnus_1207_20260402.png

Shows charged multiplicity (N_ch) distribution — a nearly Gaussian distribution centered near N_ch ~ 21. Data/MC agreement is good. The pull panel shows a few structured deviations near N_ch = 10–13 (pulls reaching −2.5σ) suggesting a mild multiplicity shape discrepancy at low multiplicities.

**[VISUAL] NOTE (Category C):** The low-multiplicity region (N_ch < 12) shows a consistent negative-pull pattern (data below MC). This could indicate tau contamination or diffractive events being slightly mismodelled, but the effect is small (< 2.5σ).

**Verdict:** PASS with Category C note.

---

#### data_mc_trackpt_magnus_1207_20260402.png

Shows track p_T on log scale. The distribution falls steeply from a peak near p_T = 0. Data/MC agreement is good in the bulk. The pull panel shows very large data/MC discrepancies at high p_T (above ~30 GeV/c): visible discrete data points (2–3 events) appear isolated above the MC histogram bins which have gone to zero.

**[VISUAL] CONCERN (Category B):** The track p_T figure extends to ~50 GeV/c, but the MC appears to have effectively zero events above ~40 GeV/c (the bin content vanishes). Data shows a few isolated events in these extreme bins, giving large positive pulls. These are likely statistical fluctuations in near-zero MC bins. The plot range could be truncated at ~20 GeV/c where meaningful statistics end. The current range creates misleading pulls in empty bins.

**Verdict:** PASS with Category B note (plot range extends into statistically empty region, creating misleading pulls at high p_T).

---

#### data_mc_d0_magnus_1207_20260402.png

Shows track impact parameter d0 in cm. The distribution is sharply peaked at d0=0 with a fine-structure comb pattern visible (spikes at d0 ~ ±0.01, ±0.02 cm — discrete d0 measurement lattice). Data/MC both show this structure. The pull panel shows structured deviations at the d0 = ±0.01–0.02 cm positions where the comb peaks appear.

**[VISUAL] CONCERN (Category B):** The "comb" structure in the d0 distribution (discrete measurement grid visible at ≤ 5σ separation) creates structured pulls that are not a data/MC physics disagreement but a binning artifact — the histogram bins align differently with the measurement grid for data vs MC. This is a known feature of silicon vertex detector measurements. The pulls at the comb positions reach ±2–3σ. The AN should note this as an instrumental binning effect rather than a physics discrepancy.

**Verdict:** PASS with Category B note (d0 comb structure creates binning-artifact pulls).

---

### TYPE: result (Phase 3)

#### rb_operating_scan_magnus_1207_20260402.png (Phase 3)

The figure shows R_b extracted at each working point threshold from 1 to 14, for two taggers: combined (black circles) and probability-only (blue triangles). Both sets of values start near R_b ~ 0.95–1.0 at low thresholds and decrease toward ~0.45–0.5 at high thresholds (WP 14). A prominent horizontal line at R_b = 0.216 (SM) and a dotted dashed line at R_b = 0.216 (ALEPH) are shown. An annotation box explains the Phase 3 calibration bias.

**Specific checks:**
- Square aspect ratio (10x10): PASS
- Experiment label (ALEPH Open Data): PASS
- y-axis range: 0.0 to 1.1 (full range showing all extracted values). PASS (AN-noted fix A9 implemented correctly).
- The phase 3 annotation text is readable at this size.

**[VISUAL] CONCERN (Category B):** At AN rendering size (~0.45 linewidth), the annotation box text (6 lines in "x-small" font) will be difficult to read. The box contains key explanatory text ("Phase 3: nominal ε_c, ε_uds not calibrated..."). This text is important context for the figure.

**Verdict:** PASS with Category B note on annotation text readability at AN rendering size.

---

## Cross-Figure Consistency Analysis

**CROSS-FIGURE CHECK 1: Data/MC agreement vs R_b extraction result**

The Phase 3 data/MC figures show generally good agreement (most pulls within ±2σ, no systematic offset) for event-level variables (thrust, cos θ, N_ch, sphericity). The Q_FB distributions also show good agreement. However, the Phase 3 R_b operating scan shows values 2–5× above the SM expectation (0.5–1.0 vs 0.216). This is documented as "expected at Phase 3" due to uncalibrated background efficiencies. The Phase 4a calibration brings the extraction to R_b = 0.280 ± 0.396. The narrative is internally consistent: good kinematics, good tag variable modelling, but the efficiency calibration is the source of the extraction bias. This is a correct "broken foundations → calibration → repaired extraction" story. PASS on cross-figure consistency.

**CROSS-FIGURE CHECK 2: F2 (angular fit) vs F7 (kappa consistency)**

The angular fit in F2 shows chi2/ndf = 31.9/8 (p < 0.001) for κ=0.5. The kappa consistency figure (F7) shows chi2/ndf = 0.71/4 (p = 0.95) for the kappa-to-kappa consistency. These are measuring different things: the chi2 in F2 is the fit quality of the linear Q_FB vs cos θ model, while F7's chi2 is the consistency of A_FB^b across kappa values. Both being near-zero A_FB^b is consistent. But the poor chi2/ndf in F2 is not resolved by the good consistency in F7. This is an unresolved inconsistency that should be documented. [Flagged already in F2 visual review.]

**CROSS-FIGURE CHECK 3: Closure test pulls vs claimed validation**

The Phase 4a independent closure test at WP 9.0 has pull = 1.93 (near 2σ threshold). The corrupted-correction sensitivity shows 4/6 cases FAILing. The AN claims the validation passes. The closure pull of 1.93 is a borderline pass — the figure visually shows the pull point at or just below the 2σ red line. The AN documents this carefully. No cross-figure inconsistency, but the borderline nature should be noted.

**CROSS-FIGURE CHECK 4: Phase 3 closure tests (panel a) vs Phase 4a discussion**

As flagged in the visual review, Phase 3 closure panel (a) shows both R_b bars at equal height (~0.83) while the annotation says "R_b = 0.0000." If this is a rendering bug (the mirrored bar is at y=0 but the y-axis starts above zero), the figure is misleading. If the bar is genuinely at 0.83, the closure test failed. The Phase 4a closure section doesn't reference the Phase 3 panel (a) result as problematic, suggesting it may be a rendering issue. This must be investigated.

**CROSS-FIGURE CHECK 5: hemisphere_correlation C_b vs R_b extraction**

The hemisphere correlation figure shows C_b ranging from 1.03 to 1.55 across working points, while the AN text uses C_b = 1.01 (from the Phase 3 ALEPH calibration). If the extraction at WP 10.0 uses C_b read from this figure (~1.55) rather than the published 1.01, the extraction result changes substantially. This inconsistency between the C_b figure and the claimed C_b in the extraction deserves explicit documentation in the AN.

---

## Summary of Findings

### Category A (Must Resolve — Blocking)

| # | Figure | Finding | Suggested Fix |
|---|--------|---------|--------------|
| A1 | F2_afb_angular_distribution.png | chi2/ndf = 31.9/8 (p < 0.001) shown without better-fitting model; appears as unresolved bad fit | Show intercept-inclusive fit overlay, annotate both chi2 values, or explain the intercept in the figure itself |
| A2 | F7_afb_kappa_consistency.png | Combined result band (width = ±0.0022) is nearly invisible (sub-pixel) at AN rendering size | Increase band width/opacity, or zoom y-axis and show ALEPH as off-plot arrow/annotation |
| A3 | closure_tests_magnus_1207_20260402.png panel (a) | Both R_b bars appear at y~0.83 while annotation says "R_b = 0.0000"; either the closure test did not return R_b=0, or the figure has a rendering bug | Investigate bar values: if mirrored R_b=0, the bar should be invisible (at y=0) or the y-axis starts at 0.82 (then the bar is visually wrong); regenerate with correct bar heights and y-axis range |
| A4 | closure_tests_magnus_1207_20260402.png panel (b) | "chi2/ndf 1144" annotated in figure, but AN caption states "chi2/ndf = 11,447" — 10× discrepancy | Verify the correct value and update the figure annotation or caption |
| A5 | efficiency_calibration.png | 3-panel 30×10 composite: all text unreadable at AN rendering size (~0.15 linewidth per panel) | Split into three separate square figures at 0.45 linewidth each, or use a proper 3-panel figure with appropriate scaling |

### Category B (Must Fix — Quality Issues)

| # | Figure | Finding | Suggested Fix |
|---|--------|---------|--------------|
| B1 | closure_test_phase4a.png | Non-square figsize (20×10); right panel labels (xx-small font) unreadable at AN rendering size | Restructure as two separate square figures or use figsize=(10,10) with adjusted layout |
| B2 | F1_rb_stability_scan.png | x-axis range 9.5–10.5 with single data point; labeled "stability scan" but contains no scan | Annotate the reason for single-point extraction, or rename figure to "rb_extraction" |
| B3 | F4_fd_vs_fs.png | "Not directly comparable" annotation in xx-small font, may be unreadable at AN rendering size | Enlarge annotation font or move key text to the caption body |
| B4 | F5_systematic_breakdown.png | Color coding (blue vs orange) threshold not explained in legend | Add legend entry or annotation explaining the color split criterion |
| B5 | hemisphere_correlation.png | ALEPH C_b = 1.01 reference corresponds to ALEPH's operating point, not WP 10.0; comparison is misleading without annotation | Add annotation noting ALEPH's working point, or label the x-axis position where C_b = 1.01 was measured |
| B6 | data_mc_thrust_magnus_1207_20260402.png | Structured 2–3σ pull pattern (data peaks at slightly lower thrust than MC) | Document as known shape discrepancy in the AN section on data/MC; assess impact on event selection |
| B7 | data_mc_qfb_k0.3/k0.5 | Structured pull patterns (not random scatter) | Note in AN text or investigate if shape discrepancy is significant |
| B8 | data_mc_trackpt_magnus_1207_20260402.png | Plot range extends to 50 GeV/c with empty MC bins; misleading high-pT pulls | Truncate at ~20 GeV/c or mask empty-bin pulls |
| B9 | data_mc_d0_magnus_1207_20260402.png | d0 comb-structure binning creates artificial ±2–3σ pulls | Note as instrumental effect in AN, or rebin to avoid alignment with measurement grid |
| B10 | rb_operating_scan_magnus_1207_20260402.png | Annotation text (6 lines x-small) may be unreadable at AN rendering size | Increase font size or move text to caption |

### Category C (Suggestions)

| # | Figure | Finding |
|---|--------|---------|
| C1 | cutflow_magnus_1207_20260402.png | Mixed event/track units on single y-axis; consider separating or annotating the transition |
| C2 | data_mc_nch_magnus_1207_20260402.png | Mild negative-pull pattern at low N_ch; consistent with tau contamination but sub-2.5σ |
| C3 | data_mc_qfb_kinf | Empty-bin pulls in pull panel appear alarming but are binning artifacts; annotate if possible |

---

## Overall Assessment

**Blocking findings:** 5 Category A violations require resolution before AN review can proceed.

The most critical findings are:
1. **A3** (Phase 3 closure panel (a) rendering bug or genuine test failure) — this could indicate the basic closure test did not actually validate d0 lifetime behavior
2. **A1** (F2 poor chi2/ndf without resolution) — leaves a key result figure showing an apparently bad fit
3. **A5** (efficiency calibration unreadable at AN rendering size) — a diagnostic figure core to the analysis narrative is unpresentable

The physics narrative is internally consistent (good kinematics → good tagging → expected calibration bias → explained extraction uncertainty), but several presentation failures prevent the AN from communicating this narrative clearly at print scale.

**Upstream quality gate flag:** Findings A3, A4, B1, and B2 suggest that the Level 1 (watcher) and Level 2 (Haiku swarm) quality gates did not catch: (1) the rendering bug in the Phase 3 closure panel, (2) the non-square multi-panel figures, and (3) the text legibility issues at AN rendering scale. These are Level 1/2 process failures per `agents/plot_validator.md` §2.
