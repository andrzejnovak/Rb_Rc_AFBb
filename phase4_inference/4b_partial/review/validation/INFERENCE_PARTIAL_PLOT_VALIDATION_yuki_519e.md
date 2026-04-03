# Phase 4b Inference Plot Validation
**Session:** yuki_519e  
**Date:** 2026-04-02  
**Validator role:** Plot Validator (Level 3 — cross-figure + code lint + visual)  
**Phase:** 4b_partial (10% data inference)  
**Figures directory:** `phase4_inference/4b_partial/outputs/figures/`  
**Source directory:** `phase4_inference/4b_partial/src/`

---

## Step 1: Figure Registry Check

### Registry completeness

- [x] `FIGURES.json` exists in `outputs/`
- [x] `FIGURES.json` is valid JSON (parseable array of 8 objects)
- [x] Every PNG in `outputs/figures/` has a corresponding registry entry (no orphan figures)
- [x] Every registry entry has a corresponding PNG on disk (no missing figures)
- [ ] **FAIL: Every entry has ALL required fields** — see finding [REGISTRY-1] below
- [x] Every "type" field is one of the allowed values
- [ ] **FAIL: Every "lower_panel" field is present** — all entries missing this field (see [REGISTRY-1])

**[REGISTRY-1] BLOCKING — VIOLATION (Category A)**  
All 8 registry entries are missing four required fields: `lower_panel`, `is_2d`, `created`, `script_mtime`. The FIGURES.json appears to have been written manually rather than by `save_and_register`. The `save_and_register` function in `phase3_selection/src/plot_utils.py` writes to `phase3_selection/outputs/FIGURES.json` (its `OUT` is hardcoded to the Phase 3 directory), so Phase 4b's registry was never populated by the function. The file on disk is a stub with only four fields per entry.

*Required fields missing from all 8 entries:* `lower_panel`, `is_2d`, `created`, `script_mtime`

**Fix:** Either (a) update `SCRIPT_PATH` handling in `plot_phase4b.py` so `save_and_register` resolves the registry path relative to `PHASE4B_OUT` rather than `phase3_selection/outputs/`, or (b) re-run `plot_phase4b.py` after patching `save_and_register` to accept an explicit registry path, or (c) populate the missing fields manually in FIGURES.json. The most robust fix is (a).

### Staleness check

- script `plot_phase4b.py` mtime: 1775208449 (Unix)
- all figure PNGs mtime: 1775209120 (Unix)
- Figures are 671 seconds **newer** than the script — not stale. PASS.

Other source scripts (`rb_extraction_10pct.py` mtime 1775208643, `systematics_10pct.py` mtime 1775208691) are not plotting scripts and therefore not subject to figure staleness.

---

## Step 2: Code Lint

Checked: `plot_phase4b.py`, `rb_extraction_10pct.py`, `systematics_10pct.py`, `run_phase4b.py`, `debug_rb.py`.

### Forbidden pattern grep

- `ax.set_title(` — **NOT FOUND.** PASS.
- `plt.colorbar` / `fig.colorbar` — **NOT FOUND.** PASS.
- `tight_layout` — **NOT FOUND.** PASS.
- `imshow` — **NOT FOUND.** PASS.
- `\begin{subfigure}` — **NOT FOUND.** PASS.
- `figsize=` with non-`(10, 10)` dimensions — **NOT FOUND.** All figures use `(10, 10)` or the 2×2 subplot which also uses `figsize=(10, 10)`. PASS.
- `histtype="errorbar"` without explicit `yerr=` — `histtype='fill'` and `histtype='step'` are used; no `histtype="errorbar"` present. PASS.
- `data=False` combined with `llabel=` — **NOT FOUND.** PASS.
- `bbox_inches="tight"` — present inside `save_and_register` (line 70 of `plot_utils.py`). PASS.
- `exp_label` — `exp_label_data(ax)` called at every main panel. PASS (see visual check for S2b caveat).

### Ratio-panel ylabel check (Phase 4+ rule)

**[LINT-1] WARNING (Category A)**  
`plot_d0_sigma_data_mc()` labels the lower panel `ylabel='Pull'` (line 205). This is correct for Phase 4 — pull panel required, ratio panel forbidden. PASS.

No ratio-panel ylabel found anywhere. PASS.

### Derived-quantity sqrt(N) check

`np.sqrt(np.maximum(h_data, 1))` used in `plot_d0_sigma_data_mc` (line 188) and `plot_hemisphere_charge_comparison` (line 431) as `yerr` for data points. These are count quantities (event counts from histogram), so `sqrt(N)` is correct. PASS.

`np.sqrt(h_data + h_mc_scaled)` used for pull denominator (line 198). This is the combined Poisson uncertainty for the pull, appropriate for count histograms. PASS.

### Cross-phase import check

Phase 4b `plot_phase4b.py` imports `from plot_utils import save_and_register, exp_label_data, exp_label_mc` (line 42), correctly reusing Phase 3 plotting utilities. PASS.

### Normalization labeling

`plot_d0_sigma_data_mc` normalizes MC to data integral (line 182: `scale = h_data.sum() / h_mc.sum()`). The legend label reads `'MC (normalized)'` (line 185). This is acceptable as a short label; a more explicit `'MC (norm. to data)'` would be preferred per conventions but is not a blocking violation.

`plot_hemisphere_charge_comparison` also normalizes MC to data integral (line 425) but the MC is labeled only by its blue fill with no legend entry visible (no `label=` kwarg on the `mh.histplot` call at line 429-430). **[LINT-2] VIOLATION (Category B):** S2b MC series has no legend label in the subplot panels, making the color coding ambiguous without a legend.

### F4b theoretical curves — comment flags approximate physics

Line 234 in `plot_phase4b.py` contains `# Rough scaling` adjacent to `fd_theory = Rb_val * fs_theory**2 * 1.5`. The coefficient 1.5 is not cited from any source and is flagged as a rough approximation. This affects the theory curve overlays in F4b. **[LINT-3] WARNING (Category B):** The R_b theory curves in F4b use an undocumented scaling factor (`1.5`) with no citation. Per the analysis numeric-constants policy, every number must come from a citable source. The curves may be directionally illustrative but should be labeled "Approximate" or replaced with the correct analytic formula from the double-tag counting methodology.

---

## Step 3: Visual Review

### F1b — `F1b_rb_stability_10pct.png` (type: result)

**Description:** Forest plot showing R_b values at two operating points (WP=7, WP=10) for Phase 4a MC (blue squares) and 10% data (orange circles), with SM, ALEPH, and LEP combined reference bands. The plot is square with a clear experiment label ("ALEPH Open Data", sqrt(s)=91.2 GeV). Both data series lie near the reference bands within large uncertainties at WP=7, while at WP=10 both sit ~0.06 above the SM/reference values — the 10% data point at WP=10 is approximately 0.26 vs. SM 0.216, a deviation of roughly 0.8–1.0 sigma given the large statistical uncertainties.

The legend is well-placed in the upper-left and does not overlap data. Axis labels and tick labels are readable. The y-axis range (0.10–0.45) is appropriate given the large error bars. No pull panel (not required for this figure type). The figure communicates a stability check clearly.

**Physics note:** WP=10 shows both Phase 4a MC and 10% data sitting above SM by ~0.04–0.06. Given the 10% statistical error (~0.05), this is within 1–2 sigma, which is expected for a partial-data result.

**VERDICT: PASS** with minor observation — only two operating points are shown (WP=7 and WP=10). The script processes four thresholds (7, 8, 9, 10), but only two appear on the plot. This suggests the extraction returned null for WP=8 and WP=9, which should be documented or the figure should include null-result markers.

---

### F2b — `F2b_afb_angular_10pct.png` (type: result)

**Description:** Mean forward-backward charge Q_FB plotted vs cos(theta_thrust) at kappa=0.3 using 10% data, with a linear fit (orange) and the SM expected slope (red dashed). The data points (black error bars) show large scatter with no clear angular trend — the fitted slope (0.00069 ± 0.00145) is consistent with zero and roughly 10x smaller than the SM expectation (~0.015). The figure is square with experiment label, readable axis labels, and a clean legend. The data clearly cannot resolve A_FB at 10% statistics, which is expected and physically motivated.

**[VISUAL-1] WARNING (Category B):** The SM expectation curve (`Expected delta_b x A_FB^b ~ 0.015`) is plotted starting from x=-0.9 but the `x_fit` variable is defined inside the `for kr in afb['kappa_results']:` loop (line 141) and then referenced outside that loop at line 149. If the loop finds no kappa=0.3 result, `x_fit` would be undefined — a latent code bug. This is a code correctness warning, not a visual problem in this render.

**[VISUAL-2] OBSERVATION:** The data points show a systematic offset toward negative Q_FB values across nearly all cos(theta) bins (most points below zero). This is a consistent negative bias in the mean hemisphere charge. The fitted intercept is non-zero (~-0.004). If this is a physical asymmetry in the detector or a systematic, it should be noted in the artifact. This may indicate a charge asymmetry in the jet charge reconstruction.

**VERDICT: PASS** (the content is physically reasonable for 10% statistics). Flag [VISUAL-2] for artifact documentation.

---

### F3b — `F3b_d0_sigma_data_mc.png` (type: data_mc)

**Description:** Signed d0/sigma_d0 distribution comparing 10% data (black error bars) and normalized MC (blue filled histogram) on a log y-scale, with a pull panel below. The distribution is correct in shape — a narrow peak near 0 (prompt tracks) with an asymmetric tail extending to large positive values (displaced b/c tracks). The overall normalization agreement is good by construction (MC normalized to data), and the shapes agree in the core and tails.

**[VISUAL-3] VIOLATION (Category A):** The pull panel is nearly empty — only 3–4 pull markers are visible across the full range of 80 bins, concentrated near x=2–4. Almost all bins show no pull marker at all. This strongly suggests most bins have zero data counts (the log scale tail at large signed d0 is below ~100 counts/bin). The errorbar call plots `yerr=1.0` uniformly for every pull bin, which is correct in form but produces invisible markers in bins with zero data. However, the missing pull points may alternatively indicate a rendering issue with zero-value pulls not being plotted by the errorbar call when `pull=0.0` for bins with `h_data=h_mc_scaled=0`. The pull panel gives essentially no diagnostic information for this distribution. The panel should either (a) exclude bins with zero counts from both numerator and denominator, or (b) show a count of bins with non-trivial pull statistics explicitly.

**[VISUAL-4] VIOLATION (Category A):** The pull panel y-label reads `'Pull'`. Per Phase 4+ rules, the y-label for pull panels must use the formula notation `(Data - MC)/sigma`, not the bare word "Pull". This is a Category A violation at Phase 4.

**[VISUAL-5] OBSERVATION — upstream quality gate failure:** The experiment label appears on the main panel correctly. The pull panel has no experiment label (correct — label belongs on main panel only). However, the ratio/pull panel x-axis label `Signed d0/sigma_d0` uses a plain-text subscript rather than LaTeX (`\sigma_{d_0}`). Minor rendering concern.

**VERDICT: FAIL** — [VISUAL-3] (uninformative pull panel) and [VISUAL-4] (pull ylabel) are both Category A.

---

### F4b — `F4b_fd_vs_fs_10pct.png` (type: result)

**Description:** Scatter plot of double-tag fraction f_d vs single-tag fraction f_s for Phase 4a MC (blue squares connected by line) and 10% data (orange circles connected by line), with three R_b theory curves. The Phase 4a and 10% data trajectories are nearly identical, lying close together across the operating-point scan (threshold 7–10). The theory curves appear in the lower-right quadrant, far below where the data and MC points lie (upper portion of the plot, f_d in the range 0.045–0.115, f_s in 0.17–0.30).

**[VISUAL-6] VIOLATION (Category A) — Physics diagnostic:** The R_b theory curves (dashed/dotted/dash-dot gray lines) are clearly separated from the data and MC points by a large gap. The curves show f_d values of 0–0.05 for f_s in 0.0–0.4, while the actual measured points sit at f_d = 0.04–0.115. The theory curves use the approximate formula `fd_theory = Rb * fs^2 * 1.5` (flagged in [LINT-3]) which does not match the actual tag-counting relationship. This means the figure communicates a false comparison — the reader cannot extract R_b by reading off which curve the data falls on, because the curves do not reflect the actual extraction equation. A figure whose stated purpose is to show R_b sensitivity via f_d vs f_s plane, but where the theory curves are physically incorrect, is actively misleading.

**Fix:** Replace the approximate formula with the correct double-tag counting relationship: `f_d = eps_b^2 * R_b * C_b + cross-terms`, using the actual MC-calibrated eps_c and eps_uds values. Alternatively, label the curves "Approximate (illustrative only)" with a conspicuous note.

**VERDICT: FAIL** — [VISUAL-6] is Category A.

---

### F5b — `F5b_systematic_breakdown_10pct.png` (type: systematic_impact)

**Description:** Horizontal bar chart on a log x-axis showing R_b systematic uncertainty contributions from 13 sources, ranked by magnitude. Two vertical lines mark the statistical uncertainty (dashed red, ~0.053) and total systematic uncertainty (dash-dot green, ~0.59). The dominant contribution is `eps_uds` followed by `C_b` and `eps_c`, consistent with expectations for this analysis where the light-quark mis-tag rate is poorly constrained. The bars span roughly 4 orders of magnitude from `tau_contamination` (~0.00005) to `eps_uds` (~0.5).

**[VISUAL-7] VIOLATION (Category A) — Dominant systematic flag:** The total systematic (0.5898) is approximately 11x the statistical uncertainty (0.0529). A single source (`eps_uds` at ~0.5+ delta_R_b) accounts for >80% of the total uncertainty. Per the regression checklist, when one source dominates >80% of total uncertainty, there must be a documented investigation of whether it can be reduced. The eps_uds contribution at 50% variation is very large; the ALEPH published analysis achieved much smaller eps_uds systematics by constraining uds-tag rates from data control regions. This should be flagged in the artifact.

**[VISUAL-8] OBSERVATION:** The label `eps uds` in the y-axis uses a plain space, not an underscore or proper subscript. While minor, it is inconsistent with publication typography. Similarly `sigma d0` and `sigma d0 form` should be rendered with proper subscripts in LaTeX.

**Physics note on C_b:** The C_b systematic bar (~0.3 delta_R_b) is the second-largest contribution and reflects the range of R_b values for C_b in [1.01, 1.10]. This is a very large systematic — nearly 6x the stat uncertainty — and arises directly from the absence of per-hemisphere vertex reconstruction [D17]. The figure is honest about this but the implied total uncertainty (quadrature sum ~0.59 systematic + 0.053 stat) means the 10% R_b extraction has ~0.59 total uncertainty, making the result R_b = 0.26 ± 0.05(stat) ± 0.59(syst) — entirely dominated by one systematic and not competitive with any reference value. This is expected at 10% stage but should be clearly stated in the artifact.

**VERDICT: PASS** with flags [VISUAL-7] and [VISUAL-8] for artifact documentation. The figure itself is honest and clear, though the physics situation it reveals (C_b and eps_uds domination) warrants investigation documentation.

---

### F7b — `F7b_kappa_consistency_10pct.png` (type: result)

**Description:** Forest plot of A_FB^b vs kappa (0.3, 0.5, 1, 2, 5) for Phase 4a MC (blue squares) and 10% data (orange circles, offset by +0.05 in kappa for visibility), with the ALEPH reference A_FB^b=0.0927 (green dashed) and a combined value band (orange shaded, 0.0085 ± 0.0035). The plot is square, well-labeled, and the legend is clear.

**[VISUAL-9] VIOLATION (Category A) — Physics diagnostic:** The extracted A_FB^b values at all kappa values (both Phase 4a MC and 10% data) cluster near zero (range approximately -0.003 to +0.013), while the ALEPH reference is 0.0927. The combined value is 0.0085 ± 0.0035 — the reference lies ~24 sigma above the measurement. This is a large and unexplained deviation from a well-measured published value. Per §6.8 (validation target rule), a pull >3-sigma from a reference requires: (1) quantitative explanation, (2) demonstrated magnitude match, (3) no simpler explanation such as a bug.

The figure shows the ALEPH reference but does not visually indicate the tension magnitude (the reference line is far above all plotted points, at the very top edge of the plot). This deviation is not simply a 10% statistics effect — A_FB^b measured this way should converge to the SM value given enough events, but 10% data should still be unbiased. The ~10x suppression relative to ALEPH is physically suspicious and requires investigation in the artifact.

**[VISUAL-10] OBSERVATION:** The kappa=inf point is plotted at kappa=5 with no axis annotation distinguishing it from kappa=5. If kappa=5 and kappa=inf are both present and plotted at x=5, they would overlap. The code offset of +0.05 helps distinguish Phase 4a vs 10% data, but the kappa=inf label is lost.

**VERDICT: FAIL** — [VISUAL-9] is Category A (>3-sigma deviation from published reference without documented quantitative explanation).

---

### S1b — `S1b_tag_fractions_comparison.png` (type: data_mc)

**Description:** Line plot on a log y-axis showing single-tag fraction f_s vs combined tag threshold (1–15) for full MC (blue squares) and 10% data (orange circles). Both series follow an identical exponential decrease from ~0.5 at threshold=1 to ~0.08 at threshold=15. The agreement between data and MC is very good across the full range, with a slight separation at threshold >12 where 10% data lies marginally above MC. No pull panel is present.

**[VISUAL-11] VIOLATION (Category B) — Missing lower panel:** S1b is registered as type `data_mc` but has no pull or ratio panel. For a data/MC comparison figure, a lower panel showing agreement quantitatively is expected. The visual agreement looks excellent, but the absence of a pull panel means no quantitative chi2 or pull statistics are shown. This is a Category B issue at Phase 4 (visual agreement is apparent but not quantified).

**[VISUAL-12] OBSERVATION:** No experiment label issue detected — "ALEPH Open Data" and sqrt(s)=91.2 GeV are visible. Legend labels "MC (full)" and "Data (10%)" are clear. The asymmetry between "full MC" and "10% data" means this is not a fair like-for-like comparison (full MC statistics vs. 10% data). This is acceptable for Phase 4b but should be noted: statistical fluctuations in data will be larger than in MC, but the excellent agreement suggests the tag fractions are well-modeled.

**VERDICT: PASS** with flag [VISUAL-11] for missing pull panel (Category B).

---

### S2b — `S2b_hemisphere_charge_data_mc.png` (type: data_mc)

**Description:** 2×2 subplot grid showing Q_FB distributions at kappa=0.3, 0.5, 1.0, 2.0 for full MC (blue filled histogram) and 10% data (black error bars). Each panel shows a bell-shaped distribution centered near zero, with increasingly flat shape as kappa increases (more discriminating power at intermediate kappa, as expected). Data and MC agree well at all four kappa values, with no visible systematic offsets.

**[VISUAL-13] VIOLATION (Category A) — Missing experiment label:** The 2×2 subplot figure has no experiment label ("ALEPH Open Data" / sqrt(s) annotation). The `plot_hemisphere_charge_comparison` function does not call `exp_label_data` or any equivalent. The function uses `fig.suptitle('')` to suppress the title but never adds the experiment label. Per the rendering red flags list, a missing experiment label is automatic Category A.

**[VISUAL-14] VIOLATION (Category A) — Missing legend:** The MC histogram (blue fill) and data points (black error bars) have no legend in any of the four panels. The `mh.histplot` call at line 429 has no `label=` argument, and the `ax.errorbar` at line 431 also has no `label=`. There is no `ax.legend()` call in `plot_hemisphere_charge_comparison`. Without a legend, the figure is ambiguous — a reader cannot determine which series is data and which is MC without external knowledge.

**[VISUAL-15] OBSERVATION — Upstream quality gate:** S2b is a 2×2 subplot. Per the plotting rules, subplot compositions should use a single experiment label on the overall figure. The function omits this entirely.

**VERDICT: FAIL** — [VISUAL-13] (missing experiment label) and [VISUAL-14] (missing legend) are both automatic Category A.

---

## Cross-Figure Consistency

### Physics narrative

The Phase 4b figures tell a coherent (if sobering) story: the tag fractions (S1b) are well-modeled in MC, the d0 distribution (F3b) is well-described, and the f_d vs f_s plane (F4b) shows 10% data matching MC expectations. However, the extracted physics results (F1b: R_b above SM; F7b: A_FB^b ~10x below ALEPH) both deviate from expectations in ways that are not clearly documented or diagnosed in the figures themselves. The systematic breakdown (F5b) explains why R_b has large uncertainty, but the A_FB^b suppression is not explained anywhere in the figure set.

**[CROSS-1] VIOLATION (Category A):** F1b shows R_b(10% data, WP=10) ~ 0.26, consistent with SM within 1 sigma. F7b shows A_FB^b(combined) ~ 0.0085, inconsistent with ALEPH 0.0927 at ~24 sigma. These two measurements come from different techniques applied to the same dataset. If R_b is consistent with SM, the same b-quark events should also produce an A_FB^b consistent with SM. The A_FB^b suppression (~10x) while R_b is approximately correct suggests a specific analysis failure in the A_FB^b extraction chain, not a statistical fluctuation. This broken-input scenario must be diagnosed before these results are presented together. See §6.8 validation target rule.

### Suspiciously extreme metrics

- A_FB^b combined = 0.0085 vs reference 0.0927: pull ~24 sigma. **Category A** — see [VISUAL-9] and [CROSS-1].
- R_b at WP=10 ~ 0.26 vs SM 0.216: ~0.8 sigma given statistical uncertainty. Acceptable.
- Total syst / stat ratio = 0.5898 / 0.0529 ≈ 11:1. Extreme but documented as driven by C_b and eps_uds. Noted in [VISUAL-7].

---

## Summary Table

| Figure | Type | Verdict | Category A Issues | Category B Issues |
|--------|------|---------|-------------------|-------------------|
| F1b_rb_stability_10pct | result | PASS | — | Two of four WPs missing (null extractions) |
| F2b_afb_angular_10pct | result | PASS | — | Negative Q_FB bias [VISUAL-2] |
| F3b_d0_sigma_data_mc | data_mc | **FAIL** | Uninformative pull panel [VISUAL-3]; Pull ylabel [VISUAL-4] | — |
| F4b_fd_vs_fs_10pct | result | **FAIL** | Theory curves not physically correct [VISUAL-6] | — |
| F5b_systematic_breakdown_10pct | systematic_impact | PASS | — | Dominant systematic investigation needed [VISUAL-7] |
| F7b_kappa_consistency_10pct | result | **FAIL** | A_FB^b 24-sigma from reference [VISUAL-9] | — |
| S1b_tag_fractions_comparison | data_mc | PASS | — | Missing pull panel [VISUAL-11] |
| S2b_hemisphere_charge_data_mc | data_mc | **FAIL** | Missing experiment label [VISUAL-13]; Missing legend [VISUAL-14] | — |

### Registry

| Finding | Step | Category | Description |
|---------|------|----------|-------------|
| REGISTRY-1 | Step 1 | **A (BLOCKING)** | All 8 entries missing `lower_panel`, `is_2d`, `created`, `script_mtime` |

### Code Lint

| Finding | Step | Category | Description |
|---------|------|----------|-------------|
| LINT-2 | Step 2 | B | S2b MC series has no `label=` in `mh.histplot` |
| LINT-3 | Step 2 | B | F4b theory curve coefficient 1.5 uncited |

### Visual

| Finding | Step | Category | Description |
|---------|------|----------|-------------|
| VISUAL-3 | Step 3 | A | F3b pull panel nearly empty (80 bins, 3 visible markers) |
| VISUAL-4 | Step 3 | A | F3b pull ylabel = "Pull" not "(Data - MC)/sigma" |
| VISUAL-6 | Step 3 | A | F4b R_b theory curves use incorrect formula, misleading comparison |
| VISUAL-7 | Step 3 | A | F5b: eps_uds dominates >80% of systematic — investigation undocumented |
| VISUAL-9 | Step 3 | A | F7b: A_FB^b 24-sigma from ALEPH reference — unexplained |
| VISUAL-11 | Step 3 | B | S1b: no pull panel for data_mc type |
| VISUAL-13 | Step 3 | A (auto) | S2b: missing experiment label |
| VISUAL-14 | Step 3 | A (auto) | S2b: missing legend |
| CROSS-1 | Cross-fig | A | R_b~SM but A_FB^b ~10x suppressed — undiagnosed |

---

## Overall Verdict: **FAIL**

**9 Category A findings.** The Phase 4b plot set cannot pass review in its current state.

**Blocking issues requiring resolution before re-review:**

1. **[REGISTRY-1]** FIGURES.json missing four required fields for all 8 entries. Fix `save_and_register` routing or populate manually.
2. **[VISUAL-9] + [CROSS-1]** A_FB^b extracted from 10% data is ~10x suppressed relative to ALEPH reference. This is a Category A physics finding that requires (a) quantitative diagnosis of the suppression mechanism, (b) a demonstrated fix or documented infeasibility (3 attempts), and (c) update of artifact text and figures. A 24-sigma deviation from a well-measured reference is not a statistical fluctuation at 10% data.
3. **[VISUAL-13] + [VISUAL-14]** S2b missing experiment label and legend. Fix in `plot_hemisphere_charge_comparison` by adding `exp_label_data` and `ax.legend()` calls.
4. **[VISUAL-3] + [VISUAL-4]** F3b pull panel is uninformative and uses wrong ylabel. Fix pull panel to exclude zero-count bins and use LaTeX formula for ylabel.
5. **[VISUAL-6]** F4b theory curves use an approximate formula not matching the extraction equation. Replace or clearly label as illustrative.
6. **[VISUAL-7]** eps_uds dominates >80% of total systematic — investigation of reducibility must be documented in artifact.
