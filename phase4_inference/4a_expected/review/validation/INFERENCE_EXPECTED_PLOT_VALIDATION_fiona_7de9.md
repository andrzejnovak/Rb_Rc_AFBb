# Plot Validation: Phase 4a Inference — Expected
## Session: fiona_7de9 | Date: 2026-04-02

---

## STEP 1: FIGURE REGISTRY CHECK

### Registry Completeness

- [x] `outputs/FIGURES.json` exists and is parseable JSON (array of 8 objects)
- [x] Every PNG in `outputs/figures/` has a corresponding entry in FIGURES.json
- [x] Every entry in FIGURES.json has a corresponding PNG on disk

**PNG inventory (8 files):**
```
F1_rb_stability_scan.png        -> entry present
F2_afb_angular_distribution.png -> entry present
F4_fd_vs_fs.png                 -> entry present
F5_systematic_breakdown.png     -> entry present
F7_afb_kappa_consistency.png    -> entry present
closure_test_phase4a.png        -> entry present
efficiency_calibration.png      -> entry present
hemisphere_correlation.png      -> entry present
```

- [x] All required fields present (`filename`, `type`, `script`, `description`, `lower_panel`, `is_2d`, `created`, `script_mtime`)
- [x] All `type` values are from the allowed set: `result` (5 entries), `systematic_impact` (1), `closure` (1), `diagnostic` (2)
- [x] All `lower_panel` values are `none` — consistent with no ratio/pull panels present

**Missing field:** The `observable_type` field is present in all 8 entries (value `"count"` throughout) — this is not a required field in the schema but is present; no issue.

### Staleness Check

All 8 FIGURES.json entries report:
- `script_mtime`: `"2026-04-02T20:34:32+00:00"`
- `created`: ranging from `"2026-04-02T20:35:17..."` to `"2026-04-02T20:39:38..."`

The figures were all created after the script's modification time. No stale figures detected.

**[REGISTRY] RESULT: PASS — Registry complete, no orphans, no missing files, no stale figures.**

---

## STEP 2: CODE LINT

All linting was performed on `phase4_inference/4a_expected/src/plot_phase4a.py`.

### Forbidden Pattern Checks

- [LINT] `ax.set_title(` — NOT FOUND. PASS.
- [LINT] `plt.colorbar` / `fig.colorbar(im, ax=` — NOT FOUND. PASS.
- [LINT] `tight_layout` — NOT FOUND. PASS.
- [LINT] `imshow` — NOT FOUND. PASS.
- [LINT] `\begin{subfigure}` in .tex files — NOT FOUND. PASS.
- [LINT] `data=False` combined with `llabel=` — NOT FOUND. PASS.
- [LINT] `histtype="errorbar"` without `yerr=` — NOT FOUND. PASS (no histtype="errorbar" at all).
- [LINT] `np.sqrt(h.values())` / `np.sqrt(counts)` near yerr — NOT FOUND. PASS.
- [LINT] `.view()[:]` near `histtype="errorbar"` — NOT FOUND. PASS.
- [LINT] Hardcoded hex colors — NOT FOUND. Colors use `'C0'`, `'C1'`, `'C2'` (theme cycle), `'black'`, `'blue'`, `'red'`, `'gray'` (semantically motivated). PASS.
- [LINT] Absolute numeric `fontsize=` values — NOT FOUND. All fontsize uses are relative strings (`'x-small'`, `'xx-small'`). PASS.
- [LINT] Ratio panel ylabel containing `ratio`/`Ratio`/`Data/MC` — NOT APPLICABLE (no ratio panels exist). PASS.
- [LINT] `bbox_inches="tight"` at save — confirmed via `save_and_register` in Phase 3 plot_utils (inherited). PASS.
- [LINT] `exp_label` / `exp_label_mc` present on all figures — CONFIRMED. All 8 figure functions call `exp_label_mc(ax)` (or `exp_label_mc(axes[0])` for multi-panel). PASS.
- [LINT] Phase 3 `plot_utils` imported — CONFIRMED. `import plot_utils as pu` + `from plot_utils import setup_figure, setup_ratio_figure, exp_label_mc` at lines 29-30. PASS.
- [LINT] Normalization: no `normalize` or `scale_to` calls found — MC is not normalized to data integral. PASS.

### figsize for Multi-Panel Figures

**[LINT] VIOLATION (Category B):** Two multi-panel figures use `figsize=(10, 10)` instead of the scaled dimensions required by the template:

1. `plot_closure_test` (line 329): `plt.subplots(1, 2, figsize=(10, 10))` — per template, 1x2 should be `(20, 10)`.
2. `plot_efficiency_calibration` (line 376): `plt.subplots(1, 3, figsize=(10, 10))` — per template, 1x3 should be `(30, 10)`.

These figures are rendered with panels compressed horizontally into a square canvas, which visually squashes the subpanels. The template states "For MxN subplots, scale to keep ratio: 2x2 -> (20, 20), 1x3 -> (30, 10)."

**Suggested fix:** Change line 329 to `figsize=(20, 10)` and line 376 to `figsize=(30, 10)`.

### Cross-Phase Import

- [LINT] Phase 3 `plot_utils.py` is present at `phase3_selection/src/plot_utils.py` and is correctly imported by the Phase 4a plotting script. PASS.

### Consistency Checks

- [LINT] All 8 figures referenced in FIGURES.json exist on disk. PASS.
- [LINT] No duplicate figure filenames found. PASS.

---

## STEP 3: VISUAL REVIEW BY TYPE

### F1: R_b Stability Scan (type: result)

**Description:** The figure shows R_b values (y-axis, range 0.15-0.30) versus combined tag threshold (x-axis). Only a single data point appears near threshold ~10 with a large error bar extending roughly from 0.24 to 0.31. The ALEPH reference band (blue, narrow, near R_b = 0.216) and LEP combined band (green, very narrow) are barely visible as thin slivers near the bottom of the plot, well separated from the data point at ~0.28. A red dashed SM reference line at R_b = 0.2158 is invisible at this scale. The chi2/ndf annotation appears in the lower-left corner.

The figure does show the expected bias (MC pseudo-data at ~0.28 vs SM at ~0.216), and the reference lines are present. However, there is a major axis range problem: the y-axis spans 0.15 to 0.30 which is correct but the data point and reference bands are in very different regions (0.28 vs 0.216), making the comparison hard to read. More critically, only ONE data point appears visible for what should be a stability scan over multiple thresholds — the scan spans multiple working points but all except one appear to have produced a null extraction. The stability scan is supposed to show consistency of R_b across thresholds; a single point provides no stability information.

**[VISUAL] FINDING (Category A — physics diagnostic):** The R_b stability scan shows only a single valid extraction point at threshold ~10, but the scan should cover multiple working points (the code iterates over a range of thresholds). Either nearly all extractions failed (returned `None`) or only one threshold yielded a valid R_b. This is a physics diagnostic failure — a "stability scan" with one point cannot demonstrate stability. The FIGURES.json description says "R_b operating point stability scan with ALEPH and LEP bands" but the rendered figure does not deliver a scan. This should trigger an investigation into why extractions fail at other working points.

**[VISUAL] ADDITIONAL OBSERVATION:** The red dashed SM line and the ALEPH/LEP bands are present but completely dominated by the single data point with its very large error bars (~0.06 statistical), making it impossible to visually compare to references. This is not a code violation but reflects the physics state.

Universal checks:
- Square aspect ratio: PASS (10x10 single panel)
- Experiment label ("ALEPH Open Simulation" + sqrt(s)): PASS
- Readability: PASS (text legible)
- Legend overlap: PASS (legend upper-right, no overlap with data)
- Axis labels ("Combined tag threshold", "R_b"): PASS
- Rendering red flags: none

**VERDICT: FAIL (Category A) — single-point stability scan is not a scan.**

---

### F2: A_FB^b Angular Distribution (type: result)

**Description:** The figure shows mean charge asymmetry <Q_FB> (y-axis) vs cos(theta_thrust) (x-axis, range -1 to 1) at kappa=0.5. Black error bar points are shown for 10 angular bins; a red fit line with near-zero slope is overlaid. The fit slope is 0.00036 +/- 0.00107 — consistent with zero within one sigma. A chi2 annotation in the upper-left box shows chi2/ndf = 104.9/9 with N_tagged = 467,279.

The near-zero A_FB is physically correct for MC pseudo-data: the ALEPH simulation does not embed the EW forward-backward asymmetry at generator level, so zero is expected. The fit line is essentially flat and the data scatter around zero with no clear trend, confirming correct behavior. However, the chi2/ndf = 104.9/9 is extremely high (~11.7 per degree of freedom), indicating that either the scatter of the data points around zero is much larger than the estimated statistical uncertainties, or the fit is wrong. The data points show a non-trivial pattern: negative values at forward and backward angles, a positive outlier near cos(theta) ~ 0, which looks like an odd physical shape rather than pure noise.

**[VISUAL] FINDING (Category B — physics diagnostic):** The chi2/ndf = 104.9/9 is pathological for a fit to a flat line. This either means the statistical error bars are underestimated (which would be a bug) or the angular distribution has genuine non-trivial structure unrelated to the forward-backward asymmetry. The annotation is visible and the value matches the plot (one can see the points are not consistent with the fit line at all). This should be flagged for investigation in the artifact — it was acknowledged in INFERENCE_EXPECTED.md but without quantitative diagnosis.

**[VISUAL] OBSERVATION:** The chi2 value should appear in the artifact's validation test list. Per the INFERENCE_EXPECTED.md, A_FB ~ 0 is expected and the extraction is described as working correctly, but a chi2/ndf of ~12 on the angular bins is not consistent with a well-behaved measurement.

Universal checks:
- Square aspect ratio: PASS
- Experiment label: PASS
- Legend does not overlap data: PASS (legend lower-right, clear space)
- Axis labels with appropriate notation: PASS
- Readability: PASS

**VERDICT: CONDITIONAL PASS with Category B finding on chi2/ndf pathology.**

---

### F4: f_d vs f_s (type: result)

**Description:** The figure shows double-tag fraction f_d (y-axis) vs single-tag fraction f_s (x-axis). Black data points trace an upward-curving trajectory from roughly (0.15, 0.04) to (0.30, 0.12), representing the MC pseudo-data at different working points. Three prediction curves are overlaid: red dashed (R_b = 0.216 = SM), blue dotted (R_b = 0.200), green dotted (R_b = 0.250). The data points fall below all three prediction curves by a visible offset — the data curve lies below the R_b = 0.216 SM curve, suggesting the data's effective R_b is lower than SM in this space, which is inconsistent with the R_b ~ 0.28 extracted value from F1.

The figure communicates the double-tag counting method's geometric structure well. The prediction curves are smooth and well-separated. However, the data systematically falls below even the R_b = 0.200 curve for most of the scan range, which should manifest as an extracted R_b below 0.20 — contradicting the INFERENCE_EXPECTED.md result of R_b = 0.280.

**[VISUAL] FINDING (Category B — physics diagnostic):** The f_d vs f_s data trajectory lies below the R_b = 0.200 prediction curve, which should imply an extracted R_b < 0.20. This is inconsistent with the reported R_b = 0.280 in the artifact. Either the prediction curves are generated with incorrect eps_c/eps_uds values (the code uses `results[3]` for fixed efficiencies, which may correspond to a single working point rather than the locus), or there is a systematic inconsistency in the extraction. This cross-check should be explicitly addressed in the artifact.

**[VISUAL] NOTE:** The legend correctly labels the three R_b curves. The axis labels are informative. The figure itself is well-styled and readable.

Universal checks:
- Square aspect ratio: PASS
- Experiment label: PASS
- Legend does not overlap data: PASS
- Axis labels with units: PASS (dimensionless fractions, no units needed)
- Readability: PASS

**VERDICT: CONDITIONAL PASS with Category B finding on f_d/f_s vs extracted R_b inconsistency.**

---

### F5: Systematic Uncertainty Breakdown (type: systematic_impact)

**Description:** Horizontal bar chart showing systematic contributions to delta_R_b (in units of 10^-3, x-axis). Thirteen systematic sources are listed on the y-axis in descending order of magnitude. The dominant source is "Light mistag eps_uds" with a bar extending to ~387 x 10^-3 — nearly off the right side of the plot given the axis range. The remaining 12 systematics all have bars that are barely visible (sub-10 x 10^-3) relative to the eps_uds bar. A red dashed vertical line marks the total systematic = 387.47 x 10^-3, and a blue dotted line marks the statistical = 30.52 x 10^-3.

The figure confirms that eps_uds utterly dominates the systematic budget (>99% of total syst), as expected from the analysis: with no MC truth labels and the simplified combined tag, the light-flavor mistag rate uncertainty propagates with enormous leverage. The figure is correctly ordered and the color coding (blue bars for dominant, orange for subdominant) helps distinguish magnitudes, though for most bars the color difference is moot since they are invisible at this scale.

**[VISUAL] FINDING (Category B — layout):** The eps_uds bar dominates so completely that all other 12 systematics are invisible at this scale — each is less than 3% of the eps_uds contribution. The figure technically shows the breakdown but is informationally useless for the subdominant sources. A log-scale x-axis or a secondary inset zooming into the subdominant sources would be needed for publication. As currently rendered, 12 of 13 bars appear as essentially zero width.

**[VISUAL] FINDING (Category B — physics):** The total systematic delta_R_b = 387 x 10^-3 = 0.387 on R_b ~ 0.280 represents a 138% relative systematic uncertainty. This is far larger than the statistical uncertainty and completely dominates the result. While correctly reported in the artifact, this systematic magnitude is physically extreme — the eps_uds +50% variation produces a delta_R_b of 0.387 which exceeds R_b itself (0.280). This signals that the measurement is not useful with the current methodology, which is correctly diagnosed in the artifact but should be more prominently flagged in the figure (e.g., a text annotation noting this is a pathological case due to data limitations).

Type-specific checks (systematic_impact):
- [x] Per-source impact visible and distinguishable: PARTIAL (only eps_uds is visible; others are effectively zero-width)
- [x] Variations are not flat: PASS (eps_uds shows clear non-zero impact)
- [x] Sign of variation physically motivated: The sign is unsigned (delta_R_b magnitudes shown, positive only) — no up/down distinction. This is ACCEPTABLE for this style of breakdown plot.
- [x] Colors distinguishable: PASS (blue for large, orange for small — though all small bars look identical)

Universal checks:
- Square aspect ratio: PASS
- Experiment label: PASS
- Readability: PASS (y-axis labels use publication-quality LaTeX names, not code variable names)
- Legend does not overlap data: PASS (legend in lower-right, below the bars)
- Axis label: PASS (delta_R_b x 10^-3)

**VERDICT: CONDITIONAL PASS with Category B findings (log scale needed; eps_uds dominance annotation needed).**

---

### F7: A_FB^b Kappa Consistency (type: result)

**Description:** The figure shows A_FB^b (y-axis) vs kappa (x-axis, from 0.3 to infinity with custom tick labels). Black data points with error bars are plotted at five kappa values; all cluster tightly around A_FB^b = 0. The combined result band (blue, narrow, centered on ~0) and ALEPH reference band (green, near 0.09) are both shown. The chi2/ndf = 0.7/4, p = 0.951 annotation appears in the lower-right corner.

The figure correctly shows that A_FB^b ~ 0 at all kappa values in MC pseudo-data, consistent with the known absence of forward-backward asymmetry in the ALEPH simulation. The consistency across kappa values is excellent (chi2/ndf = 0.7/4, p = 0.95), which is the expected result. The ALEPH reference band (green, around 0.09) is well-separated from the data points around 0, making the comparison visually clear. However, the y-axis range extends to 0.10 (top) showing the green ALEPH band at the top edge with the blue combined band squeezed at the bottom near zero — the axis range is appropriate for the physics.

**[VISUAL] OBSERVATION:** The near-perfect chi2/ndf = 0.7/4 and extremely high p-value (0.951) for the kappa consistency test could be a flag of over-coverage (inflated uncertainties), but given the MC-only context where A_FB is genuinely zero by construction, this is expected behavior. Marking as observation only, not a violation.

**[VISUAL] MINOR ISSUE:** At kappa = 0.3 and 0.5, the x-tick labels overlap slightly ("0.3 0.5" appear to collide at this rendering size). Upon careful inspection the ticks are at 0.3, 0.5, 1.0, 2.0, infinity — the 0.3 and 0.5 marks are close together. This is marginal but worth noting.

Type-specific checks (result):
- [x] Comparison to published values included (ALEPH band): PASS
- [x] Uncertainty bands clearly distinguished (blue = combined, green = ALEPH): PASS
- [x] Legend complete: PASS
- [ ] Forest plots have numerical value labels: NOT APPLICABLE (this is a kappa scan, not a forest plot)

Universal checks:
- Square aspect ratio: PASS
- Experiment label ("ALEPH Open Simulation"): PASS
- Readability: PASS
- Legend overlap: PASS (legend centered in open space)

**VERDICT: PASS.**

---

### closure_test_phase4a: Closure Tests (type: closure)

**Description:** Two-panel figure (1x2 layout). LEFT panel: Independent closure — a single data point at working point ~9 with pull value ~2.0 and large error bars (~1.5 sigma) spanning roughly 0.5 to 3.5. The 2-sigma reference lines (red dotted) are shown at +/-2. The single point sits exactly at the 2-sigma line. RIGHT panel: Corrupted corrections — horizontal bars for six corruption scenarios (+/-20% eps_c, +/-20% eps_uds, +/-20% C_b-1). The eps_uds corruptions show large red bars extending to ~+10 and ~-10 pull (well outside the +/-2 reference lines). The C_b corruptions show smaller blue bars around -1 to -3 (partially inside 2 sigma). The eps_c corruptions show small bars near zero (within 2 sigma).

The figure correctly uses a 1x2 layout. The corrupted corrections panel demonstrates sensitivity for eps_uds (large pulls, clearly outside 2 sigma) but shows INSENSITIVITY for eps_c corruptions (pulls near zero, inside 2 sigma). The eps_c corruptions appear to produce nearly zero pull, which means the closure test does NOT detect +/-20% corruption of the charm efficiency. This is a physics problem: a closure test that cannot detect 20% corruptions in a key systematic is tautological for that systematic.

**[VISUAL] FINDING (Category A — closure test tautology):** The corrupted eps_c corrections show near-zero pull in the right panel (blue or very small bars, both inside the 2-sigma lines). This means the closure test is insensitive to 20% variations in eps_c — the systematic that contributes to the extraction but whose corruption is not detected. Per the phase CLAUDE.md requirement: "run with intentionally corrupted corrections (±20%) and verify the test FAILS. If it still passes, the test is tautological — redesign it." The eps_c corrupted tests appear to PASS (pull inside 2 sigma), meaning the closure test is tautological with respect to charm efficiency.

**[VISUAL] FINDING (Category A — experiment label on right panel):** The experiment label ("ALEPH Open Simulation") appears ONLY on the left panel (as expected via `exp_label_mc(axes[0])`), which is correct per the template. PASS.

**[VISUAL] FINDING (Category B — layout, multi-panel figsize):** The 1x2 panel is rendered at figsize=(10,10) when it should be (20,10). The panels appear compressed horizontally — the left panel's y-axis label ("Pull (R_b^extracted - R_b^SM)/sigma") is cut off on the left edge. The right panel's y-axis labels for corruption scenarios are also potentially clipped. This is a consequence of the figsize violation identified in Step 2.

**[VISUAL] LAYOUT ISSUE (Category A):** In the rendered image, the right panel labels (corruption scenario names like "+20% eps_c", "-20% eps_c" etc.) appear on the right side of the horizontal bars rather than as y-tick labels — they overlap with the bar endpoints and the +/-2 sigma reference lines in some cases. The left panel's experiment label text ("Open Simulation") partially overlaps with a panel-internal label "Independent closure" in the upper-left corner.

**[VISUAL] OBSERVATION:** The independent closure test shows a single point at the 2-sigma boundary. Per the closure type check: "Pull statistics: count bins above 2sigma and 3sigma. Expected ~5% above 2sigma." With one working point, one point at exactly 2 sigma is not statistically meaningful as a closure check. The independent closure has only one operating point, which makes the pull statistics meaningless.

Type-specific checks (closure):
- [ ] Pull statistics: only one working point — cannot apply the 5%/0.3% rule. INCOMPLETE.
- [x] Closure on independent sample: confirmed in INFERENCE_EXPECTED.md (MC split). PASS.

**VERDICT: FAIL (Category A) — eps_c corruption insensitivity indicates tautological closure for charm efficiency; single working point makes pull statistics meaningless.**

---

### efficiency_calibration: MC Efficiency Calibration (type: diagnostic)

**Description:** Three-panel figure (1x3 layout) showing eps_b (left, blue), eps_c (middle, orange), eps_uds (right, red) vs working point. Each panel shows a smoothly decreasing efficiency curve from lower to higher working points. The experiment label appears only on the left panel. The three curves show physically sensible behavior: eps_b decreases from ~0.37 to ~0.24, eps_c from ~0.62 to ~0.43, eps_uds from ~0.18 to ~0.09.

The figure is functional and shows the calibrated efficiency curves from MC. The notable physics point visible in the figure is that eps_c (~0.43-0.62) is much larger than eps_b (~0.24-0.37), which is physically unusual (charm efficiency higher than b efficiency for a b-tagging algorithm) and is correctly flagged in the INFERENCE_EXPECTED.md as a finding. The curves are smooth with only 4 data points each.

**[VISUAL] FINDING (Category A — severe rendering artifact: experiment label text collision):** In the rendered figure, the experiment label "ALEPH" overlaps with "Open Simulation" text and the "From MC (SM truth)" annotation in the upper-left region of the left panel. The letter "P" from "ALEPH" and the "H" are visibly colliding with the annotation text box, producing an illegible region. This is a rendering red flag — text-text collision making the experiment label partially unreadable.

**[VISUAL] FINDING (Category B — multi-panel figsize):** 1x3 subplots at figsize=(10,10) produces very narrow panels. The y-axis labels (eps_b, eps_c, eps_uds) are partially clipped on the left edge of each panel. The x-axis labels appear adequate but the panels are cramped.

**[VISUAL] FINDING (Category B — no experiment label on center and right panels):** Only `axes[0]` gets `exp_label_mc`, which is correct per conventions (experiment label on main panel only). However, the center and right panels have no y-axis label visible at all in the rendered figure due to the narrow panel width. While the axis label (eps_c, eps_uds) is set in the code, it is effectively invisible at this figsize.

Type-specific checks (diagnostic):
- [x] Chi2/p-values visible: NOT APPLICABLE (calibration curves, no fit chi2 shown)
- [x] Curves show non-trivial shape: PASS (smoothly decreasing, physically motivated)

**VERDICT: FAIL (Category A) — experiment label text collision in left panel is a rendering red flag.**

---

### hemisphere_correlation: C vs Working Point (type: diagnostic)

**Description:** Single-panel figure showing hemisphere correlation C (y-axis, range ~1.0 to 1.55) vs combined tag threshold (x-axis, range 2 to 10). Blue squares (MC, with small error bars) and black circles (Data, with small error bars) are plotted at each threshold from 2 to 10. Both MC and Data track each other closely and show a monotonically increasing trend from C ~ 1.03 at WP=2 to C ~ 1.52-1.55 at WP=10. A red dashed reference line at C = 1.01 (published ALEPH C_b) is shown, well below the data at all but the lowest working point.

This is a well-rendered figure. The MC and Data points are visually distinguishable (blue vs black, square vs circle markers). The rising trend in C with working point is physically plausible — at stricter thresholds, the two hemispheres are more constrained, increasing the correlation. The red reference line at 1.01 clearly shows that the measured C_b substantially exceeds the published ALEPH value at all but the very lowest working points, consistent with the documented finding that the combined tag produces stronger hemisphere correlations than the ALEPH Q-tag.

**[VISUAL] OBSERVATION:** The figure correctly shows that C_b = 1.01 (ALEPH) is only matched at approximately WP~2, while the nominal working point is much higher. This is a physically important diagnostic correctly visualized.

**[VISUAL] MINOR CONCERN:** The legend says "Published ALEPH C_b = 1.01" for the reference line, which is informative and correctly labeled. The rlabel shows "sqrt(s) = 91.2 GeV" which is appropriate.

Type-specific checks (diagnostic):
- [x] Non-trivial values: PASS (C ranges 1.03 to 1.55 — clearly non-trivial)
- [x] No spurious chi2 = 0.000: NOT APPLICABLE

Universal checks:
- Square aspect ratio: PASS
- Experiment label: PASS ("ALEPH Open Simulation" + sqrt(s) label)
- Readability: PASS
- Legend does not overlap data: PASS (legend upper-left, data rises from lower-left to upper-right, no collision)
- Axis labels and units: PASS ("Combined tag threshold", "Hemisphere correlation C")

**VERDICT: PASS.**

---

## CROSS-FIGURE CONSISTENCY

**[VISUAL] FINDING (Category A — f_d/f_s inconsistency with extracted R_b):**
F4 (f_d vs f_s) shows the data trajectory falling systematically BELOW the R_b = 0.200 prediction curve, while INFERENCE_EXPECTED.md reports R_b = 0.280. If the data points in F4 lie below R_b = 0.200 curves, the geometric double-tag method should extract R_b < 0.200, not 0.280. This inconsistency between F4 and the reported result requires explanation. It may be that the prediction curves in F4 use fixed efficiencies from a single working point (results[3]) and the locus of data points is not a constant-efficiency trajectory, but this should be explicitly noted.

**[VISUAL] FINDING (Category B — A_FB physics coherence):**
F2 shows chi2/ndf = 104.9/9 for the angular fit at kappa=0.5, but F7 shows chi2/ndf = 0.7/4 for kappa consistency. These chi2 values refer to different quantities (angular fit vs kappa-to-kappa consistency), so they are not inherently contradictory, but the large chi2 in F2 means the individual kappa extraction at kappa=0.5 is poorly described by a linear fit — which should be visible as large scatter in F7 as well. The F7 kappa scan shows very small error bars and tight consistency, which appears at odds with the poor angular fit chi2 in F2. This tension is not explained in the artifact.

**[VISUAL] FINDING (Category B — hemisphere correlation context):**
F_hemisphere shows C_b ~ 1.18-1.55 at the working points used for extraction, while F1's R_b extraction uses the C_b directly. The large C_b (up to 1.55) is used in the extraction without explicit correction, contributing to the R_b bias. The artifact notes this finding, but the cross-figure narrative — F_hemisphere -> F1 (why R_b is biased) -> F5 (why C_b is a large systematic) — is not laid out sequentially in a way a reviewer can follow without reading the artifact prose.

---

## SUMMARY TABLE

| Figure | Type | Category | Issues |
|--------|------|----------|--------|
| F1_rb_stability_scan | result | **A** | Single-point "scan" — not a stability scan |
| F2_afb_angular_distribution | result | B | chi2/ndf = 104.9/9 pathological |
| F4_fd_vs_fs | result | B | f_d/f_s data below R_b=0.200 curve contradicts R_b=0.280 |
| F5_systematic_breakdown | systematic_impact | B | Log scale needed; eps_uds dominance should be annotated |
| F7_afb_kappa_consistency | result | PASS | Minor tick crowding at 0.3/0.5 |
| closure_test_phase4a | closure | **A** | eps_c corruption insensitive; single closure point |
| efficiency_calibration | diagnostic | **A** | Experiment label text collision; cramped panels |
| hemisphere_correlation | diagnostic | PASS | Well-rendered; physics coherent |

**Cross-figure findings:**
- Category A: f_d/f_s vs extracted R_b inconsistency
- Category B: A_FB chi2 coherence across F2 and F7; narrative flow missing

---

## FINDINGS REQUIRING RESOLUTION BEFORE REVIEW PASS

### Category A (blocking)

**[VISUAL-A1] F1: Single-point stability scan**
The R_b stability scan has only one valid extraction point. A scan with one point cannot demonstrate stability. Investigate why extractions fail at other working points. Either fix the extractions or rename the figure to "R_b extraction at reference working point" and acknowledge the limited scan coverage.

**[VISUAL-A2] closure_test_phase4a: eps_c corruption insensitive**
The +/-20% eps_c corruption produces near-zero pull in the corrupted corrections panel. The phase CLAUDE.md explicitly requires that corruption tests FAIL. The eps_c closure is tautological. Redesign: either use a different observable sensitive to eps_c corruption, or acknowledge this as a documented limitation with a finding + resolution section.

**[VISUAL-A3] efficiency_calibration: Experiment label collision**
The "ALEPH" experiment label overlaps with the "From MC (SM truth)" annotation text in the left panel. This is a rendering red flag. Fix by repositioning the annotation (e.g., lower y-position) or using a different ax.transAxes location that does not conflict with the mplhep exp_label placement.

**[LINT-B1 / VISUAL-A4] Multi-panel figsize violations**
Both `closure_test_phase4a` (1x2) and `efficiency_calibration` (1x3) use `figsize=(10,10)` instead of the scaled dimensions required by the template. The compressed panels cause content clipping and the text collision in efficiency_calibration. Fix: `figsize=(20,10)` for closure test, `figsize=(30,10)` for efficiency calibration.

### Category B (must fix before PASS)

**[VISUAL-B1] F2: chi2/ndf = 104.9/9 not addressed**
The pathological chi2/ndf for the angular fit should have a documented finding + resolution in the artifact. The INFERENCE_EXPECTED.md mentions A_FB ~ 0 is correct but does not explicitly address why the fit chi2 is so large. Add a Finding section in the artifact.

**[VISUAL-B2] F4: f_d/f_s trajectory below R_b = 0.200 curves**
The cross-figure inconsistency between F4 and the reported R_b = 0.280 needs explicit explanation in the artifact (or the prediction curves in F4 need to be regenerated with the same efficiencies used in the extraction, showing where the data actually lies relative to the theoretical locus).

**[VISUAL-B3] F5: Log-scale or inset for subdominant systematics**
The systematic breakdown is visually useless for 12 of 13 sources. Add a log-scale x-axis or a secondary inset zoomed to the sub-10 x 10^-3 range.

---

## UPSTREAM QUALITY GATE NOTE

No mechanical violations (missing labels, fontsize, legend overlap) that should have been caught at Level 1/2 were found — except for the text collision in efficiency_calibration (Level 2 Haiku swarm should have caught this) and the figsize violations for multi-panel figures (Level 1 watcher should have caught this). These constitute a **Level 1/2 upstream quality gate failure** for those two specific issues.

---

*Validation performed by: fiona_7de9 (plot_validator, Sonnet)*
*Phase: 4a Inference Expected*
*Figures reviewed: 8/8*
*Registry check: PASS*
*Code lint: 1 Category B finding (multi-panel figsize)*
*Visual review: 3 Category A findings, 3 Category B findings, 2 cross-figure findings*
*Overall verdict: FAIL — Category A findings must be resolved before advancing to Doc 4a*
