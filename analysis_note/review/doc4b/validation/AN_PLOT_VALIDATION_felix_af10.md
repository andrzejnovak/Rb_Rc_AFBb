# Plot Validation Report — Doc 4b

**Session:** felix_af10  
**Validator role:** Level 3 (cross-figure consistency, physics narrative, visual review)  
**Scope:** Phase 4b figures in `phase4_inference/4b_partial/`  
**Date:** 2026-04-03  
**Script reviewed:** `phase4_inference/4b_partial/src/plot_phase4b.py`  
**Figures reviewed:** 8 PNGs in `phase4_inference/4b_partial/outputs/figures/`

---

## STEP 1: FIGURE REGISTRY CHECK

### Registry Completeness

- [x] `outputs/FIGURES.json` exists
- [x] FIGURES.json is valid JSON (array of 8 objects, parseable)
- [x] Every PNG in `outputs/figures/` has a corresponding FIGURES.json entry (8/8)
- [x] Every FIGURES.json entry has a corresponding PNG on disk (8/8)
- [x] All required fields present: `filename`, `type`, `script`, `description`, `lower_panel`, `is_2d`, `created`, `script_mtime` — PASS for all 8 entries
- [x] All `type` fields are valid: `result` (×4), `data_mc` (×3), `systematic_impact` (×1) — all in allowed set
- [x] All `lower_panel` fields are valid: `pull` (×1), `none` (×7) — all in allowed set

**[REGISTRY] FINDING R-1 — No orphan or missing figures.** Registry is complete and well-formed. PASS.

### Staleness Check

Script `phase4_inference/4b_partial/src/plot_phase4b.py` mtime: `2026-04-03T10:45:49+00:00`

All 8 figures have creation times ranging from `2026-04-03T10:46:33` to `2026-04-03T10:51:02` — all strictly after script mtime. No stale figures.

**[REGISTRY] Staleness check: PASS — all figures are current.**

---

## STEP 2: CODE LINTER

Script: `phase4_inference/4b_partial/src/plot_phase4b.py`

### Forbidden Patterns

| Pattern | Result |
|---------|--------|
| `set_title` | Not found — PASS |
| `plt.colorbar` / `fig.colorbar(im, ax=` | Not found — PASS |
| `tight_layout` | Not found — PASS |
| `imshow` | Not found — PASS |
| `data=False` with `llabel=` | Not found — PASS |
| `histtype="errorbar"` without `yerr=` | Not found — PASS |
| `\begin{subfigure}` in .tex | Not checked (this is Phase 4b, no AN .tex file) — N/A |
| `bbox_inches` | Handled via `save_and_register` → `plot_utils.py:70` which uses `bbox_inches="tight"` — PASS |

### Absolute Fontsize Violations

**[LINT] FINDING L-1 — Category A: Absolute `fontsize=8` at line 287**

```python
# F5b: plot_systematic_breakdown — line 287
ax.set_yticklabels(display_names, fontsize=8)
```

The CMS stylesheet sets all font sizes correctly for 10×10 figures. Absolute numeric `fontsize=` values are forbidden (Category A per `appendix-plotting.md`). The tick labels on the systematic breakdown horizontal bar chart should use a relative specifier (e.g., `fontsize='x-small'`) or be omitted entirely (letting the theme handle sizing).

**Suggested fix:** Replace `fontsize=8` with `fontsize='x-small'` at line 287.

**[LINT] FINDING L-2 — Category A: Absolute `fontsize=12` at line 456**

```python
# S2b: plot_hemisphere_charge_comparison — line 456
ax.text(0.05, 0.95, f'$\\kappa = {kappa}$',
        transform=ax.transAxes, va='top', fontsize=12)
```

Same rule: absolute numeric fontsize is forbidden. For kappa annotations in subplot panels, use `fontsize='small'` or `fontsize='x-small'`.

**Suggested fix:** Replace `fontsize=12` with `fontsize='small'` at line 456.

### Figsize Check

All single-panel figures use `figsize=(10, 10)` — PASS.

`S2b` uses a 2×2 subplot with `figsize=(10, 10)`. Per `appendix-plotting.md`, for an M×N subplot layout, each panel should remain effectively square, so a 2×2 grid should be `figsize=(20, 20)`.

**[LINT] FINDING L-3 — Category B: `S2b` subplot `figsize=(10, 10)` for a 2×2 grid**

```python
# line 428
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
```

A 2×2 layout at `(10, 10)` produces 5×5-inch panels — compressed and small relative to the expected publication size. The template specifies scaling as `2×2 → (20, 20)`.

**Suggested fix:** Change to `figsize=(20, 20)` at line 428.

### `mpl_magic` Usage

`mpl_magic` is not called in any function. Per `appendix-plotting.md`, `mpl_magic(ax)` is the preferred method for preventing legend-data overlap (by auto-scaling the y-axis). Without it, legends are placed at fixed `loc=` positions that may overlap data. This is not a hard violation in all cases (some plots have genuinely clear regions), but it is a systematic deviation from the recommended pattern.

**[LINT] FINDING L-4 — Category B: `mpl_magic` not used for legend placement**

All plot functions use explicit `loc=` parameters (e.g., `'upper left'`, `'upper right'`, `fontsize='x-small'`) without `mpl_magic`. Where legends are in the upper region of a plot that has data filling the upper range, overlap is possible. The visual review checks each case.

### data_mc Type without Pull Panel

**[LINT] FINDING L-5 — Category A: `S1b` and `S2b` are typed `data_mc` in FIGURES.json but have `lower_panel: none`**

Per `appendix-plotting.md` and `plot_validator.md` §TYPE:data_mc, Phase 4+ data_mc figures require pull panels `(Data − MC) / σ`, not ratio panels. `S1b_tag_fractions_comparison` and `S2b_hemisphere_charge_data_mc` are tagged `data_mc` in FIGURES.json but have no lower panel. This is a Category A violation for Phase 4 figures.

Two possible resolutions:
1. Add pull panels to both S1b and S2b (preferred — provides quantitative agreement assessment).
2. If pull panels are genuinely impractical (e.g., S1b is a line plot, not a histogram), re-tag as `comparison` or `diagnostic` and document the rationale.

**Suggested fix:** Add pull panels to S1b and S2b, or re-classify in FIGURES.json with justification.

### Normalization Labeling

**[LINT] FINDING L-6 — Category B: MC normalized to data integral without legend documentation in `F3b` and `S2b`**

`F3b_d0_sigma_data_mc` (lines 188-189): `scale = h_data.sum() / h_mc.sum()` followed by MC labeled `'MC (normalized)'`. The legend correctly states "normalized" but does not clarify "MC (norm. to data)" — a borderline issue.

`S2b_hemisphere_charge_data_mc` (line 450): `scale = h_data.sum() / h_mc.sum()` with label `'MC (norm.)'`. "MC (norm.)" is ambiguous — does not state normalized to data integral.

Per `normalization.md`, when MC is normalized to the data integral, the legend must contain `"MC (norm. to data)"` or equivalent explicit language. `"MC (norm.)"` alone is insufficient.

**Suggested fix:** Change `'MC (norm.)'` labels to `'MC (norm. to data)'` in `S2b`.

### Cross-Phase Import Check

`plot_phase4b.py` imports `plot_utils` from `phase3_selection/src/` (lines 41-43). This is correct — the Phase 4b script reuses the Phase 3 plotting utilities. PASS.

### Derived-Quantity Error Bar Trap

No `histtype="errorbar"` without `yerr=` found. No `.view()[:] =` assignments in plotting scripts. PASS.

---

## STEP 3: VISUAL REVIEW BY TYPE

### F1b — `F1b_rb_stability_10pct.png` (type: result)

**Description:** This figure shows R_b measurements as a function of the combined tag threshold (working point) at WP=7, 9, and 10. Blue squares show Phase 4a MC results, orange circles show 10% data results, with reference lines for the SM value (R_b = 0.21578, red dashed), ALEPH measurement (green band), and LEP combined (blue band). The figure is square, the experiment label (`ALEPH Open Data`, √s = 91.2 GeV) is correctly placed in the upper portion, and the legend is legible in the upper left.

**Physics assessment:** The Phase 4a MC points at WP=9 and WP=10 lie significantly above the SM band (~0.31, ~0.30), while the 10% data point at WP=7 (0.208) is close to the SM value. Only three working points are populated for MC and two for data (WP=8 and WP=9 return R_b=None for the 10% data — confirmed from the results JSON). The large statistical errors on the 10% data points (~0.07-0.09) are consistent with 10% statistics and the extraction uncertainty.

**Issues:**
- The Phase 4a MC values at WP=9 (~0.315) and WP=10 (~0.305) are well above the SM band. This is noted in the artifact as a "circular calibration diagnostic" — the Phase 4a MC is self-consistent but not a real measurement. However, this presentation may confuse a reader who expects all MC points to cluster near SM. A caption clarification is needed.
- The legend overlaps slightly with the data points in the upper-left region at WP=7 for the 10% data error bar (which extends to ~0.14), but the overlap is not severe.

**[VISUAL] FINDING V-1 — Category B: F1b — Legend upper-left placement partially overlaps with the WP=7 MC error bar.** The blue Phase 4a MC error bar at WP=7 extends upward toward the legend box. Not a severe collision but borderline. `mpl_magic` would have resolved this automatically.

**Verdict:** PASS with minor concern (V-1 tracked separately as Category B).

---

### F2b — `F2b_afb_angular_10pct.png` (type: result)

**Description:** This figure shows the angular distribution `<Q_FB>` vs `cos θ_thrust` for the 10% data at κ=0.3. Data points (black errorbars) scatter between approximately −0.010 and +0.001. The orange fitted line has a small positive slope (slope = 0.00069 ± 0.00145), and the red dashed line shows the expected signal slope of ~0.015. The experiment label, axis labels, and legend are all legible.

**Physics assessment:** The fitted slope (0.00069 ± 0.00145) is significantly below the expected slope of 0.015 from the SM A_FB^b × δ_b. This is a ~10-sigma suppression of the expected signal. The artifact documents this extensively (finding §7.1 in INFERENCE_PARTIAL.md). The figure correctly displays this suppression. However, the mean `<Q_FB>` values are systematically negative (most points below zero), while the expected distribution should be centered near zero with a positive slope. This systematic offset is visible in the figure and is not annotated.

**[VISUAL] FINDING V-2 — Category A: F2b — Systematic negative offset in `<Q_FB>` data points not annotated.** The data points are predominantly negative (approximately −0.005 to −0.007 on the left side, some returning toward zero on the right), while the expected values should be symmetric around zero with a slight positive trend. This is a physics diagnostic pattern (uniform y-offset) that indicates a possible charge-sign calibration issue, a systematic bias in the hemisphere charge computation, or an asymmetry in the kappa=0.3 weight function. The artifact (§7.1) attributes the suppressed asymmetry to jet charge dilution, but does not address the systematic negative offset. This should be flagged: if `<Q_FB>` is systematically negative, the forward-backward asymmetry extraction may carry a bias.

**Suggested annotation:** Add a text box or caption note: "Mean `<Q_FB>` systematically negative — see §7.1 for discussion." At minimum, the pull statistic (the discrepancy between the fitted offset and zero) should be quoted.

**Verdict:** FAIL — V-2 is Category A. The systematic negative offset is a physics diagnostic that appears in the figure without annotation or explanation, violating the "What the disagreement pattern means" requirement.

---

### F3b — `F3b_d0_sigma_data_mc.png` (type: data_mc, lower_panel: pull)

**Description:** This figure shows the signed d₀/σ_d₀ distribution in log scale. The blue filled histogram (MC, normalized to data) peaks sharply near 0, extends to a long tail at positive values (B-hadron decay tracks), while the black error-bar points (Data, full sample) follow closely. The pull panel shows only three populated points (near d₀/σ ~ 2, 4, −0.5) with pulls between −3 and +2. The pull panel has the experiment label bleeding into it — the text `(Data − MC) / σ` appears in the lower panel, which does not carry an exp_label call.

**Physics assessment:** The data/MC agreement in the main panel appears excellent over eight orders of magnitude, consistent with the claim in the artifact. The pull panel is very sparsely populated — only three bins appear in the pull panel despite the axis covering −10 to +30. This is because the pull panel only shows bins where both data AND MC have nonzero counts (`populated = (h_data > 0) & (h_mc_scaled > 0)`), but for a log-scale distribution this should populate most bins. The sparse pull panel suggests the `populated` mask may be filtering out bins where one side is very small but nonzero. This is misleading — a reader might interpret the empty pull panel regions as agreement when they are actually masked out.

**[VISUAL] FINDING V-3 — Category A: F3b — Pull panel almost empty (only ~3 visible points).** With 79 histogram bins and data visible across the full range, the pull panel should show pulls in most bins. The code at lines 207-208 applies `populated = (h_data > 0) & (h_mc_scaled > 0)`, which should be True for most bins given the log-scale distribution shows data in all bins. However, the rendered pull panel shows only 3 points. This suggests a masking or indexing bug. An empty pull panel defeats the purpose of the pull panel for data/MC validation.

**[VISUAL] FINDING V-4 — Category A: F3b — Experiment label appears to bleed into the pull panel region.** Looking at the rendered image, the exp_label region (`ALEPH Open Data` / `√s = 91.2 GeV`) is placed on the main panel axis, which is correct. However, due to `sharex=True` and `hspace=0`, the upper boundary of the pull panel is immediately below the main panel. The exp_label placement looks correct in this figure (it is on the main panel), but the pull panel has a y-axis range of ±4σ with a label `1` visible above the pull panel boundary. This `1` appears to be a rendering artifact at the top of the pull panel from the yticklabel. While not the experiment label itself, the tick `1` in the pull panel is ambiguous and should be removed (set `rax.set_yticks([-2, 0, 2])`).

**Verdict:** FAIL — V-3 is Category A (defective pull panel). V-4 is Category A (ambiguous tick label artifact).

---

### F4b — `F4b_fd_vs_fs_10pct.png` (type: result)

**Description:** This figure shows the double-tag fraction f_d vs single-tag fraction f_s for Phase 4a MC (blue squares) and 10% data (orange circles), overlaid with three R_b theory curves (gray dashed/dotted/dash-dot for R_b = 0.216, 0.230, 0.200). Both MC and data traces run parallel to each other in the middle of the plot, while the theory curves fan out from the origin. The figure is square, the experiment label is correctly placed, and the legend is in the upper right with no visible overlap.

**Physics assessment:** The data and MC points both appear displaced from the theory curves toward higher f_d values for a given f_s. The MC and data are well separated from the theory curves, which could indicate that the theory parameterization (using fixed reference eps_c=0.05, eps_uds=0.01) does not match the actual efficiency values used in the extraction. This is a cross-figure concern: if the theory curves do not pass through the data/MC points, the R_b extraction cannot be directly read off this figure. The figure thus does not serve its stated purpose of illustrating where R_b lies relative to the curves.

**[VISUAL] FINDING V-5 — Category B: F4b — Theory R_b curves do not intersect the data/MC points.** All three theory curves are displaced far to the left of the actual data and MC trajectories. The figure's purpose (showing which R_b theory curve the data follows) is undermined because the curves do not overlap with the data. The reference efficiency parameters (eps_c=0.05, eps_uds=0.01) in the theory curves are likely incompatible with the actual working-point efficiencies at the higher tag thresholds used. Either the theory curves should use the actual efficiency parameters from the MC, or the figure should be annotated to clarify the displacement.

**Verdict:** PASS (Category B finding V-5 documented). The figure communicates that data and MC agree with each other, even if the theory-curve overlay does not serve its intended role.

---

### F5b — `F5b_systematic_breakdown_10pct.png` (type: systematic_impact)

**Description:** This is a horizontal bar chart showing per-source R_b systematic uncertainties on a log-x scale. Fourteen systematic sources are listed on the y-axis (eps_uds, C_b, eps_c, R_c, sigma_d0, hadronization, sigma_d0_form, mc_statistics, g_cc, physics_params, g_bb, selection_bias, tau_contamination). Red dashed line shows stat uncertainty (0.0529), green dash-dot line shows total syst (0.5200). The dominant systematic is eps_uds, followed by C_b and eps_c.

**Physics assessment:** The total systematic (0.5200) is nearly 10× the statistical uncertainty (0.0529) and ~2.5× the central value of R_b (0.208). This is documented in the artifact as expected for 10% data with external C_b assumption. The physics is sound.

**Issues:**
- The y-axis labels use underscored code identifiers: `eps_uds`, `C_b`, `eps_c`, `g_cc`, `g_bb`, `sigma_d0`, `sigma_d0_form`, `mc_statistics`, `physics_params`, `selection_bias`, `tau_contamination`. These are code variable names, not publication-quality labels. Per `appendix-plotting.md`, any raw code identifier visible in a rendered figure is Category A.

**[VISUAL] FINDING V-6 — Category A: F5b — Y-axis labels use code variable names.** Labels like `eps_uds`, `g_cc`, `g_bb`, `sigma_d0_form`, `mc_statistics` are Python identifier-style names. Publication-quality labels would be: `ε_uds (light-quark efficiency)`, `C_b (hemisphere correlation)`, `ε_c (charm efficiency)`, `R_c`, `σ(d₀) calibration`, `Hadronization`, `σ(d₀) form factor`, `MC statistics`, `g(cc̄) rate`, `Physics params`, `g(bb̄) rate`, `Selection bias`, `τ contamination`.

Additionally, the code at line 287 applies `fontsize=8` (already flagged as L-1) — this confirms the absolute fontsize violation is visible in the rendered output.

**[VISUAL] FINDING V-7 — Category A: F5b — Absolute `fontsize=8` renders tick labels visibly smaller than the theme default.** The y-axis tick labels appear smaller than the x-axis label and other text elements, creating an inconsistent visual hierarchy.

**Verdict:** FAIL — V-6 (code variable names, Category A) and V-7 (fontsize inconsistency, confirming L-1, Category A).

---

### F7b — `F7b_kappa_consistency_10pct.png` (type: result)

**Description:** This figure shows A_FB^b measurements as a function of κ for Phase 4a MC (blue squares) and 10% data (orange circles), with an orange band showing the combined 10% data result (0.0085 ± 0.0035) and a green dashed reference line at the ALEPH published value of 0.0927. Phase 4a MC points are near zero or slightly negative; 10% data points show a modest positive signal increasing with κ. The figure is square, experiment label correctly placed.

**Physics assessment:** The combined A_FB^b = 0.0085 ± 0.0035 is ~10σ below the ALEPH published 0.0927. This is a large deviation from a well-measured reference value — per `methodology/06-review.md` §6.8, any result with a pull >3σ from a well-measured reference is Category A unless there is a quantitative explanation. The artifact addresses this (§7.1 on jet charge dilution) but the figure itself has no annotation explaining the ~10σ gap.

**[VISUAL] FINDING V-8 — Category A: F7b — No annotation explaining the ~10σ discrepancy from ALEPH A_FB^b = 0.0927.** The green reference line sits far above all data points at 0.0927, while the combined band is at 0.0085 ± 0.0035. A reader will immediately ask "why is this measurement 10× below the published value?" The figure must either include an in-figure annotation or the caption must quantify the discrepancy and point to the explanation. The validation target rule (§6.8) requires demonstrated magnitude match, not just a narrative.

The artifact documents the cause (jet charge dilution by δ_b factor — the figure shows the raw slope, not the corrected A_FB), but this physics context must appear in the figure or caption.

**[VISUAL] FINDING V-9 — Category B: F7b — The kappa axis extends to 5.5 but the 5th point (kappa=∞ mapped to 5.0) is unlabeled on the x-axis.** The x-axis shows tick marks at 0, 1, 2, 3, 4, 5 but the kappa=∞ point at x=5 is identical to the kappa=5 position. A reader would interpret this as kappa=5.0, not kappa=∞. The tick label at x=5 should be replaced with `∞` or a note in the legend should clarify.

**Verdict:** FAIL — V-8 is Category A per the validation target rule.

---

### S1b — `S1b_tag_fractions_comparison.png` (type: data_mc, lower_panel: none)

**Description:** This figure shows the single-tag fraction f_s as a function of combined tag threshold (1 to 14.5) on a log-y scale. Blue squares (MC full) and orange circles (Data 10%) follow nearly identical log-linear decay curves. Agreement is excellent — the two curves are nearly indistinguishable across the full threshold range. The experiment label is correctly placed, legend in upper right does not overlap.

**Physics assessment:** The excellent data/MC agreement in f_s is an important validation. The agreement appears within 3-5% across all working points (as stated in the artifact). The 3-5% systematic offset (data slightly below MC at higher thresholds) is visible but small. This supports the analysis strategy.

**Issues:**
- Tagged as `data_mc` in FIGURES.json but has no pull panel (already flagged as L-5). For a quantitative assessment of the data/MC agreement level, a pull or ratio panel is required.
- The figure is a data/MC comparison at Phase 4. A pull panel is Category A required.

**[VISUAL] FINDING V-10 — Category A: S1b — `data_mc` figure type with no lower pull panel (Phase 4 requirement).** This re-confirms L-5. The figure shows two lines on a log-y scale — the reader cannot judge the significance of the 3-5% data/MC discrepancy without a ratio or pull panel. Given that f_s is a count-derived quantity (fraction of tagged hemispheres), error bars on both curves are straightforward (binomial errors) and a ratio panel is feasible.

**Verdict:** FAIL — V-10 is Category A (data_mc type without pull panel at Phase 4).

---

### S2b — `S2b_hemisphere_charge_data_mc.png` (type: data_mc, lower_panel: none)

**Description:** This four-panel figure shows the Q_FB distribution for MC (blue filled) and 10% data (black error bars) at four κ values (0.3, 0.5, 1.0, 2.0). In all panels, the data follows the MC very closely. The distributions are bell-shaped, centered near Q_FB = 0, broadening with κ (higher κ → larger hemisphere charge values). The experiment label appears only on the top-left panel.

**Critical issues:**

**[VISUAL] FINDING V-11 — AUTOMATIC Category A RED FLAG: S2b — Experiment label on only one of four panels; text collision in the experiment label region visible.** Looking at the rendered figure carefully: the `ALEPH Open Data` label is placed only on `axes[0,0]` (line 459). The other three panels have no experiment label, which violates the rule that every independent axes must carry the experiment label. Additionally, with `figsize=(10,10)` for a 2×2 subplot, each panel is only 5×5 inches — the text in each panel's upper region (kappa annotation, legend) is rendered at a compressed size relative to what the CMS stylesheet expects for 10×10 figures. **The text collision is severe**: in the rendered image, the experiment label in the top-left panel overlaps with the `κ=0.3` annotation and the legend text. The label text `ALEPH Open Data √s = 91.2 GeV` runs into the `MC (norm.) Data (10%)` legend box.

**[VISUAL] FINDING V-12 — Category A: S2b — Text overlap in all four panels.** The kappa annotations (`κ = 0.3`, etc.) placed at (0.05, 0.95) collide with the legend boxes placed at `loc='upper right'`. In the compressed 10×10 figure, the legends are forced into the upper region where the kappa annotation also lives. At least in the top-left panel, the `ALEPH Open Data` exp_label, the `κ=0.3` annotation, and the `MC (norm.) / Data (10%)` legend are all competing for the same upper-left corner space.

**[VISUAL] FINDING V-13 — Category A: S2b — Missing experiment labels on three of four panels.** Panels at (0,1), (1,0), (1,1) have no `exp_label`. Per the universal checks, a missing experiment label on any figure is an automatic Category A finding that the arbiter may NOT downgrade.

**[VISUAL] FINDING V-14 — Category A: S2b — No pull panels (data_mc type at Phase 4).** Re-confirms L-5 for S2b. All four κ panels show data/MC comparisons without pull panels.

**[VISUAL] FINDING V-15 — Category B: S2b — `figsize=(10, 10)` for a 2×2 subplot.** Confirms L-3. The compressed panel size makes tick labels, legends, and annotations difficult to read at the intended AN inclusion size (~0.45\linewidth).

**Verdict:** FAIL — V-11 through V-14 are Category A findings.

---

## CROSS-FIGURE CONSISTENCY

### Consistency across F1b, F7b, INFERENCE_PARTIAL.md

The key results from the INFERENCE_PARTIAL.md are:
- R_b = 0.208 ± 0.066 (stat) ± 0.520 (syst)
- A_FB^b = 0.0085 ± 0.0035

**F1b** shows R_b at WP=7: ~0.208, WP=10: ~0.268. The primary result (WP=7) matches the artifact claim. PASS.

**F7b** shows combined A_FB^b = 0.0085 ± 0.0035 (the orange band matches the artifact claim). PASS on number consistency.

**F2b** shows slope = 0.00069 ± 0.00145 at κ=0.3. The artifact states this corresponds to A_FB^b after division by δ_b. The chain is: slope = δ_b × A_FB^b → A_FB^b = slope/δ_b. With slope = 0.00069 and δ_b ~ 0.16, this would give A_FB^b ≈ 0.0043 — consistent with the kappa=0.3 individual result (0.0042 from JSON). PASS on number consistency.

**F5b** shows total syst = 0.5200, stat = 0.0529. These match the artifact table. PASS.

### Cross-Figure Physics Narrative ("broken journey, perfect destination")

The progression from F3b (d0/sigma data/MC), S1b (tag fractions), S2b (hemisphere charge) to F1b (R_b), F2b (A_FB slope), F7b (A_FB kappa consistency) has logical coherence. The d0/sigma agreement in F3b supports the tag-fraction agreement in S1b, which supports the R_b extraction in F1b. PASS on narrative structure.

**However:** F2b shows a systematic negative offset in `<Q_FB>` (V-2) that is not diagnosed in either the figure or the artifact's §7.1. If `<Q_FB>` is systematically biased negative, the A_FB^b measurement in F7b may carry a systematic floor. The cross-figure implication: F7b's combined result (0.0085) and F2b's slope (0.00069) both appear suppressed by a similar mechanism (jet charge dilution), but the additional negative offset in F2b is unexplained and could indicate a separate bias. This is a potential "broken journey" finding.

**[VISUAL] FINDING V-16 — Category A: Cross-figure consistency — systematic negative `<Q_FB>` in F2b has no counterpart investigation in the systematic breakdown F5b.** If there is a charge-sign bias in the hemisphere charge reconstruction, it should appear as a systematic in F5b. It does not. Either the effect is captured under another systematic (e.g., `selection_bias`) or it is unaccounted for. The A_FB^b result in F7b should not be trusted until this negative offset is explained and its systematic impact is quantified.

---

## SUMMARY TABLE

| Figure | Type | Visual Verdict | Findings |
|--------|------|---------------|----------|
| F1b_rb_stability_10pct | result | PASS (minor) | V-1 (Cat B: legend near error bar) |
| F2b_afb_angular_10pct | result | **FAIL** | V-2 (Cat A: systematic negative offset unannotated) |
| F3b_d0_sigma_data_mc | data_mc | **FAIL** | V-3 (Cat A: sparse pull panel), V-4 (Cat A: tick artifact) |
| F4b_fd_vs_fs_10pct | result | PASS (minor) | V-5 (Cat B: theory curves displaced) |
| F5b_systematic_breakdown_10pct | systematic_impact | **FAIL** | V-6 (Cat A: code variable names on y-axis), V-7 (Cat A: fontsize) |
| F7b_kappa_consistency_10pct | result | **FAIL** | V-8 (Cat A: 10σ gap unannotated), V-9 (Cat B: kappa=∞ unlabeled) |
| S1b_tag_fractions_comparison | data_mc | **FAIL** | V-10 (Cat A: no pull panel) |
| S2b_hemisphere_charge_data_mc | data_mc | **FAIL** | V-11 (Cat A: text collision), V-12 (Cat A: annotation-legend overlap), V-13 (Cat A: missing exp_label ×3), V-14 (Cat A: no pull panels), V-15 (Cat B: figsize) |

### Code Lint Summary

| Finding | Category | Description |
|---------|----------|-------------|
| L-1 | **A** | Absolute `fontsize=8` at line 287 (F5b y-tick labels) |
| L-2 | **A** | Absolute `fontsize=12` at line 456 (S2b kappa annotation) |
| L-3 | **B** | `figsize=(10,10)` for 2×2 subplot at line 428 (S2b) |
| L-4 | **B** | `mpl_magic` not used — legend overlap risk |
| L-5 | **A** | `S1b` and `S2b` typed `data_mc` but `lower_panel: none` (Phase 4 requires pull) |
| L-6 | **B** | `'MC (norm.)'` label ambiguous — should be `'MC (norm. to data)'` |

### Cross-Figure Finding

| Finding | Category | Description |
|---------|----------|-------------|
| V-16 | **A** | Systematic negative `<Q_FB>` in F2b not diagnosed in F5b systematics |

---

## REQUIRED ACTIONS (Category A — must resolve before PASS)

1. **L-1, V-7:** Remove `fontsize=8` in `plot_systematic_breakdown` (line 287); use `fontsize='x-small'`.
2. **L-2:** Remove `fontsize=12` in `plot_hemisphere_charge_comparison` (line 456); use `fontsize='small'`.
3. **L-5, V-10, V-14:** Add pull panels to `S1b_tag_fractions_comparison` and `S2b_hemisphere_charge_data_mc`, or re-classify as non-`data_mc` type with documented rationale.
4. **V-2:** Annotate `F2b` with the systematic negative offset observation and add a note pointing to the artifact §7.1.
5. **V-3:** Investigate and fix the sparse pull panel in `F3b`. Either the masking logic is dropping valid bins or the histogram alignment has a bug.
6. **V-4:** Fix pull panel y-tick labels in `F3b`; use `rax.set_yticks([-2, 0, 2])` to remove the ambiguous `1` tick.
7. **V-6:** Replace code-identifier y-axis labels in `F5b` with publication-quality names.
8. **V-8:** Annotate `F7b` with the discrepancy from ALEPH A_FB^b = 0.0927 and point to the explanation (jet charge dilution factor δ_b).
9. **V-11, V-12, V-13:** Fix `S2b` text collision and missing exp_labels; increase figure size to `(20, 20)` to give panels room; move or remove kappa annotations to prevent overlap.
10. **V-16:** Investigate systematic negative offset in `<Q_FB>` in F2b; confirm whether this bias propagates to the A_FB^b result and, if so, add a systematic term to F5b.

## RECOMMENDED ACTIONS (Category B — fix before commit)

1. **L-3:** Change `S2b` figsize to `(20, 20)`.
2. **L-4:** Add `mpl_magic(ax)` calls after all plot functions to auto-scale y-axes for legend clearance.
3. **L-6:** Update `'MC (norm.)'` to `'MC (norm. to data)'` in `S2b`.
4. **V-1:** Adjust legend position in `F1b` or use `mpl_magic`.
5. **V-5:** Update theory curves in `F4b` to use actual MC efficiency parameters so the curves pass through the data/MC points.
6. **V-9:** Relabel kappa=∞ point on x-axis of `F7b` as `∞`.

---

*Validation performed by felix_af10 (plot validator, Level 3). Findings prefixed [REGISTRY], [LINT], [VISUAL]. Category A findings are automatic blocks; arbiter may not downgrade.*
