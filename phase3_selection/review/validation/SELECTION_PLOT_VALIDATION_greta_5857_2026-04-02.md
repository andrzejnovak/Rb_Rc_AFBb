# Phase 3 Plot Validation Report — Iteration 2

**Session:** greta_5857
**Date:** 2026-04-02
**Validator:** Sonnet plot-validator (Level 3)
**Phase:** phase3_selection
**Iteration:** 2 (follow-up to hana_fccb iteration 1)
**Figures reviewed:** 20 (all entries in FIGURES.json)

Focus: verify resolution of the 5 RED FLAG / Category A issues found in
iteration 1:
1. RED FLAG — R_b scan extracted values 3–5× above SM
2. Category A — cutflow code variable names on x-axis
3. Category A — closure test garbled/overlapping text annotations
4. Category A — sigma_d0 calibration code variable names on x-axis
5. Category A — d0 sign validation curves indistinguishable

---

## STEP 1: FIGURE REGISTRY CHECK

**[REGISTRY] RESULT: PASS**

- FIGURES.json exists in `outputs/` and is valid JSON (array of 20 objects).
- All 20 PNGs in `outputs/figures/` have corresponding FIGURES.json entries. No
  orphan figures, no missing figures.
- All required fields present in every entry: `filename`, `type`, `script`,
  `description`, `lower_panel`, `is_2d`, `created`, `script_mtime`.
- All `type` values are from the allowed set (`diagnostic`, `data_mc`,
  `result`, `closure`).
- All `lower_panel` values are from the allowed set (`pull`, `none`).
- Staleness check: `plot_all.py` mtime = 2026-04-02 14:54:14 UTC. All
  figures created at 15:19–15:31 UTC — figures are newer than the script.
  No stale figures.

**Registry findings: none.**

---

## STEP 2: CODE LINT

All scripts in `phase3_selection/src/` (primarily `plot_all.py` and
`plot_utils.py`) were grepped for forbidden patterns.

| Pattern | File:Line | Result |
|---------|-----------|--------|
| `plt.colorbar` or `fig.colorbar(im, ax=` | — | NONE |
| `tight_layout` | — | NONE |
| `imshow` | — | NONE |
| `histtype="errorbar"` without `yerr=` | — | NONE |
| `figsize=` with non-(10,10) values | — | NONE |
| `data=False` with `llabel=` | — | NONE |
| `np.sqrt(h.values())` or `np.sqrt(counts)` near `yerr=` | — | NONE |
| `.view()[:] =` near errorbar without `yerr=` | — | NONE |
| `\begin{subfigure}` in any .tex | — | NONE |
| bare `print(` | — | NONE |
| Hardcoded hex colors | — | NONE |

**Positive checks verified:**

- `bbox_inches="tight"` at every `savefig` call in both scripts.
- `hspace=0` correctly set in `plot_all.py` line 99 and `plot_utils.py`
  line 119.
- `exp_label_data` called consistently via dedicated helper functions.
- `plot_utils.py` exists and is imported by `plot_all.py`.
- MC legend label reads "MC (normalized to data)" consistently.
- Pull panel ylabel is "Pull" throughout — not "Ratio" or "Data/MC".

**[LINT] VIOLATION (Category A — `set_title`):** `plot_all.py` lines 597,
618, 642 use `ax.set_title(...)` for the three sub-panels of the closure
test figure. The plotting standard forbids `set_title` — titles must go in
AN captions, not on figures. However, this is a multi-panel figure where
sub-panel identifiers "(a)", "(b)", "(c)" serve a specific compositing
purpose. Assess in Step 3 visual review whether the sub-panel titles are
rendering acceptably and whether a legend or annotation alternative exists.
This is a genuine `set_title` violation per the programmatic checks, regardless
of intent.

**[LINT] WARNING (Category B — absolute fontsize):** `plot_all.py` line
321 uses `fontsize=5` (absolute integer) for x-tick labels on the
sigma_d0 calibration plot. Line 625 uses `fontsize=5` for a legend in the
closure test panel. The plotting standard specifies relative fontsize strings
("x-small", "small", etc.), not absolute integers. Absolute fontsizes
produce unpredictable output across different DPI or figure sizes.

**[LINT] WARNING (Category C — mc_scale_to_data for derived quantities,
carried from iteration 1):** `mc_scale_to_data=True` is the default for all
`data_mc_pull` calls including `observable_type="derived"` figures (Q_FB,
P_hem). This absorbs any genuine normalization mismatch. Not a rendering
violation but documented for Phase 4.

**Code lint findings: 1 Category A, 1 Category B, 1 Category C (repeated
from iteration 1).**

---

## STEP 3: VISUAL REVIEW BY TYPE

### Focus: 5 Previously Flagged Figures

---

**Fig 13 (previously RED FLAG): `rb_operating_scan_magnus_1207_20260402.png`**

The R_b operating point stability scan now shows extracted R_b (y-axis
0.0–2.7) versus tag threshold (1–14) for two tagger variants: combined tag
(black circles) and probability-only tag (blue upward triangles). The two
curves are now clearly distinguishable — combined tag is plotted with
error bars at x positions 1, 2, 3, ..., and probability-only is offset
+0.15 in x and uses a different marker (triangle vs circle). The SM R_b
reference (pink/magenta solid line at R_b = 0.21578) and ALEPH reference
band (dashed, same color, with ±0.0014 shading) are now clearly visible
as a horizontal band near R_b ≈ 0.22. The extracted values still range
from ~0.5 to ~1.0 — significantly above the SM prediction — but a yellow
annotation box in the figure explicitly states: "Phase 3: nominal ε_c,
ε_uds / not calibrated to this tagger. / Bias expected; Phase 4 multi-WP
/ fit will constrain backgrounds. / No stability plateau expected / until
calibration [B4]."

The figure is square, the ALEPH experiment label is present, and all text
is legible. The legend is in the upper left and does not overlap with the
data curves.

**Assessment of RED FLAG resolution:** The iteration 1 RED FLAG was
triggered by two compounding problems: (a) extracted values dramatically
above the SM value with no explanation, and (b) the two tagger curves
indistinguishable. Both of these are resolved in iteration 2. The figure
now clearly communicates that the bias is expected at Phase 3 due to
uncalibrated background efficiencies, and the two curves are visually
distinct.

**[VISUAL] RESIDUAL CONCERN (Category B — downgraded from RED FLAG):** The
extracted R_b values remain 2–4× above the SM value with no plateau.
The annotation explains this as expected, but it also makes the figure
scientifically borderline for a Phase 3 deliverable. A reviewer reading this
figure alone could not easily determine whether the analysis is on track.
The statement "Bias expected" should be quantitatively supported: what R_b
value is *expected* given the assumed ε_c = 0.05, ε_uds = 0.005? An
expected-bias curve or shaded band would transform this from a "trust me"
annotation into an independent cross-check. Suggested fix: compute the
predicted R_b_apparent(threshold) from the known formula with the assumed
background efficiencies and overlay it on the scan. If the extracted values
match this curve, the bias is confirmed as formulaic and not a new problem.
This is Category B: the current figure is not wrong, but it is not as
informative as it could be.

**[VISUAL] INFO:** The figure aspect ratio appears slightly non-square in
the rendered PNG (taller than wide), consistent with the `figsize=(10,10)`
setting but with content that produces a portrait-like composition due to
the legend and annotation box. This is marginal — not a Category A
violation since figsize is correct.

**Verdict: CONDITIONAL PASS.** RED FLAG resolved. Residual Category B
concern (quantitative bias prediction not shown). The two-curve
distinguishability problem is fixed.

---

**Fig 1 (previously Category A): `cutflow_magnus_1207_20260402.png`**

The cutflow bar chart shows five paired bars (data black, MC blue) on a
log y-axis for successive selection stages. The x-axis labels now read:
"Total events", "Basic quality", "|cos θ_thrust| < 0.9" (with proper
LaTeX theta symbol), "All tracks", and "Quality tracks (VDET, purity,
TPC)". All labels are in publication-quality language — no code variable
names are visible. The labels are rotated 45°, right-aligned, and at
"small" fontsize, which makes them legible though somewhat compressed.
The ALEPH experiment label and energy label are in the correct positions.
The figure is square.

**[VISUAL] RESIDUAL CONCERN (Category C):** The y-axis label "Events /
Tracks" is still ambiguous — the first three bars count events and the last
two count tracks. This was a Category B finding in iteration 1 and remains
unresolved but is acknowledged here as Category C (the label is technically
not wrong, just imprecise; a two-panel layout would be cleaner but is not
mandated).

**[VISUAL] INFO:** The bar for "All tracks" (both data and MC) reaches
near 10^8, which is ~20× larger than the event counts. This is physically
sensible (approximately 20 tracks per event) and the log scale handles it
appropriately.

**Verdict: PASS.** Category A code-variable-name violation is resolved.
Residual Category C concern noted.

---

**Fig 14 (previously Category A): `closure_tests_magnus_1207_20260402.png`**

The closure test figure has been redesigned as a three-panel layout (1×3
subplots). Panel (a) "Mirrored sig." shows two side-by-side bars: "Full
sample" (tall red bar, R_b ≈ 0.83) and "Mirrored (no lifetime)" (zero
height, near-invisible bar), with a PASS annotation box showing "R_b =
0.0000". Panel (b) "bFlag shape" shows a single bar for chi²/ndf on a log
y-axis, with the value appearing extremely large (chi²/ndf appears to be
~1114, shown as a bar reaching 10^4 on the log scale), alongside reference
lines at chi²/ndf = 1 and threshold = 2, with an annotation "χ²/ndf = 1114"
and a PASS badge. Panel (c) "Contamination 5%" shows two bars for
"Predicted shift" and "Observed shift" in |ΔR_b|, with a PASS annotation
showing "Ratio = 2.14". The ALEPH experiment label is placed on the middle
panel only (ax_b). The overlapping text artifact from iteration 1 is gone —
each annotation is now in its own boxed text in the top-center of each
panel.

**[VISUAL] VIOLATION (Category A — `set_title` in code):** The three
panels carry `set_title` calls: "(a) Mirrored sig.", "(b) bFlag shape",
"(c) Contamination 5%". Per the plotting standard, `ax.set_title()` is
forbidden — panel identification should use annotations or be placed in
the AN caption. The sub-panel titles are visually rendered at the top
of each panel, partially overlapping with the ALEPH experiment label on
the center panel. Specifically, the center panel title "(b) bFlag shape"
sits directly under the "ALEPH Open Data" label text, creating a text
collision that makes both partially unreadable. This is a rendering
consequence of the `set_title` usage. Fix: remove `set_title` calls;
use `ax.text(0.05, 0.95, '(a)', transform=ax.transAxes, ...)` for panel
labels, or label panels solely in the AN caption.

**[VISUAL] VIOLATION (Category A — experiment label placement):** The
ALEPH experiment label (`exp_label_data`) is called on `axes[1]` (the
middle panel) only, rather than on the figure's primary panel. For
multi-panel figures, the experiment label should appear once, typically
on the leftmost or topmost panel, or spanning the figure. Its placement
on the center panel combined with the `set_title` text produces a visible
collision: the "ALEPH Open Data" + "(b) bFlag shape" lines overlap in
the rendered PNG. Per the universal checks, experiment label on every panel
is not required, but the label must appear on the MAIN panel without
collision.

**[VISUAL] PHYSICS CONCERN (Category A — bFlag shape chi²/ndf = 1114):**
Panel (b) shows chi²/ndf ≈ 1114, yet is annotated as PASS. The closure
alarm band specification (phase3 CLAUDE.md) states chi²/ndf > 3 is Category A
(failure). Chi²/ndf = 1114 is catastrophically above the failure threshold
by a factor of ~370. Either the PASS verdict is incorrect (JSON
`closure_results.json` has `passes: true` despite chi²/ndf >> 3), or
the chi²/ndf is not a shape comparison of the expected kind. This cannot
be labeled PASS — it constitutes a closure test FAILURE per the alarm
band rules. This finding was flagged as a concern in iteration 1 (the
bFlag chi²/ndf was already noted as suspicious) and remains unresolved.
This is an automatic Category A: `passes: true` in JSON while the displayed
chi²/ndf = 1114 exceeds the failure threshold = 3 is a Category A
misrepresentation.

**[VISUAL] RESIDUAL CONCERN (Category A — contamination ratio 2.14):** The
contamination injection test shows an observed/predicted ratio of 2.14 and
is labeled PASS. Per the closure alarm band rules, a ratio > 2× (or in
general, a closure test where the formula does not predict the injected
contamination correctly) should fail. The figure labels this PASS, which
the JSON presumably confirms. This represents a misrepresentation of the
closure test result.

**Verdict: FAIL — Multiple Category A violations.** The overlapping
annotation text from iteration 1 has been replaced by a three-panel layout,
but new rendering problems have been introduced (title/experiment label
collision on panel b), and the underlying physics violations persist
(chi²/ndf = 1114 labeled PASS; contamination ratio 2.14 labeled PASS).
The `set_title` usage is now a confirmed [LINT] + [VISUAL] Category A
finding.

---

**Fig 3 (previously Category A): `sigma_d0_calibration_magnus_1207_20260402.png`**

The sigma_d0 calibration figure now shows scale factors per calibration bin
as a scatter plot (data black circles, MC blue squares). The x-axis now
uses human-readable multi-line labels of the form "nv=1\np=[0,1]\n|ct|=[0,0.25]"
for each bin, rotated 45° right-aligned. Not all bins are labeled (every
8th bin is shown per the code's `show_idx` logic). The axis x-label reads
"Calibration bin (nvdet, p [GeV/c], |cos θ|)" which correctly describes
the bin dimensions. The ALEPH experiment label is present. The figure is
square.

**[VISUAL] PARTIAL RESOLUTION of Category A.** The raw code variable names
("nv1_p0_ct0") are no longer visible on the axis. The human-readable labels
"nv=1, p=[0,1], |ct|=[0.00,0.25]" are now shown for the subset of bins
selected by `show_idx`. This satisfies the categorical requirement — a
reader can now determine what each labeled bin represents.

**[VISUAL] NEW CONCERN (Category B — label readability):** The x-axis tick
labels, while human-readable in content, are printed at `fontsize=5` (an
absolute integer — see [LINT] finding above). At fontsize=5 in the rendered
PNG at 200 DPI, the labels are extremely small and require zooming to read.
For an AN figure reproduced at ~0.45 linewidth, these labels will be
illegible. The code only shows every 8th bin label to avoid overlap, but
the result is that most calibration bins have no visible x-axis label,
making the figure's x-axis structure nearly unreadable in context.
Suggested fix: use relative fontsize="xx-small" or "x-small"; consider a
different display approach (bin index on x-axis + bin legend table in caption).

**[VISUAL] PHYSICS CONCERN (persistent from iteration 1):** All scale factors
(both data and MC) range from ~1.5 to ~8.0, well above the reference line
at 1.0. The FIGURES.json description states scale factor = 1.0 means the
nominal parameterization is correct. Values of 2–8 indicate the sigma_d0
parameterization underestimates the resolution by factors of 2–8 everywhere.
This is a substantial physics concern that must be addressed in the
SELECTION.md artifact. It is not a plot quality issue but flags a potential
systematic bias in the d0 significance calculation.

**Verdict: PASS (with Category B concern and physics note).** The Category A
code-variable-name violation is resolved. A new Category B readability
concern exists due to fontsize=5 on very small tick labels.

---

**Fig 2 (previously Category A): `d0_sign_validation_magnus_1207_20260402.png`**

The d0 sign validation figure now shows two clearly distinguishable curves
vs |d0/σ_d0| threshold: a pink/magenta curve labeled "b-enriched (tight
double-tag, 231054 events)" and a blue curve labeled "All events". The
b-enriched curve reaches asymmetry values of 0.41–0.57, while the all-events
curve shows asymmetry of 0.16–0.31. The separation between the two curves
is visually clear and physically meaningful — the b-enriched sample shows
higher positive d0 asymmetry as expected from longer-lived B mesons. The
ALEPH experiment label is present. The figure is square. The legend
annotation "Gate: PASS" is now in the legend frame (not as a floating
annotation), which is cleaner than iteration 1.

**Assessment of Category A resolution:** In iteration 1, the two curves
were nearly indistinguishable because bFlag=4 covered 99.8% of events and
provided no real enrichment. The code was updated (comment: "Fix A8:
Use tight tag cut (combined tag > 8) for b-enrichment instead of bFlag=4")
to use a tight double-tag requirement. The resulting enriched sample has
231,054 events (~18% of total). The two curves are now separated by
approximately 0.2 in asymmetry at each threshold point. The enriched sample
shows a physics-expected higher asymmetry, confirming the d0 sign convention
is meaningful.

**[VISUAL] MINOR CONCERN (Category C — gate criterion not quantified):**
The "Gate: PASS" text in the legend still does not specify the quantitative
criterion being checked (e.g., "PASS: asymmetry_b > asymmetry_all at all
thresholds"). A viewer cannot independently verify the gate logic. This
is presentational and not a rendering violation.

**Verdict: PASS.** The Category A indistinguishability violation is resolved.
The two curves are now clearly distinct and physically motivated.

---

### Review of All Remaining Figures (previously PASS)

---

**Fig 4: `data_mc_significance_magnus_1207_20260402.png`**

The signed d0/σ_d0 distribution on a log scale shows the characteristic
asymmetric shape: symmetric Gaussian core, strong positive tail from b/c
secondary vertices, and near-symmetric negative tail from resolution. Data
(black error bars) and MC (blue filled histogram) agree closely across the
full range from −10 to +30. The pull panel is sparse because only a small
fraction of bins have significant pull deviations. The largest pulls
visible are at the extreme negative tail (~−2.5σ) in low-statistics bins.
The figure is square, the experiment label is present, and the legend does
not overlap content.

**Verdict: PASS.**

---

**Fig 5: `data_mc_combined_tag_magnus_1207_20260402.png`**

The combined hemisphere tag −ln P_hem + mass bonus distribution on a log
scale shows data and MC in good agreement across the bulk (tag 0–15). The
high-tag tail (tag > 15) shows systematic pulls reaching −2.5σ (MC
underestimates the high-b-fraction tail). The distribution falls smoothly
from ~10^5 at tag=0 to ~10^3 at tag=20. No plot quality violations. The
pull panel shows the systematic tail disagreement clearly.

**[VISUAL] CONCERN (persistent from iteration 1):** The systematic negative
pull trend at tag > 15 corresponds to the regime where the b-tagging
efficiency is highest. This may affect the R_b extraction if Phase 4 uses
the high-tag region. The SELECTION.md artifact should document this.

**Verdict: PASS** (concern documented, not a plot quality failure).

---

**Fig 6: `data_mc_hemisphere_mass_magnus_1207_20260402.png`**

The hemisphere invariant mass distribution now shows a prominent pink dashed
vertical line at 1.8 GeV/c² labeled "b/c threshold 1.8 GeV/c² [D18]",
which was missing in iteration 1. Data and MC agree well for mass > 1 GeV/c²,
with systematic disagreement at very low mass (first bin pull ~−2.5σ
visible). The b/c threshold line extends into the pull panel as well
(translucent). This Category B fix from iteration 1 is confirmed resolved.
The figure is square, experiment label present.

**Verdict: PASS.** Category B fix confirmed.

---

**Fig 7: `data_mc_phem_magnus_1207_20260402.png`**

The −ln P_hem distribution shows the same high-tail disagreement as Fig 5
(pulls reaching −3σ for −ln P_hem > 12.5), which is internally consistent.
The distribution body (0–12) shows good agreement. Figure is square,
experiment label present.

**Verdict: PASS.**

---

**Fig 8: `data_mc_qfb_k0.3_magnus_1207_20260402.png`**

The Q_FB (κ=0.3) distribution is approximately Gaussian, centered at zero.
The pull panel shows a clear zigzag pattern across the full range: pulls
oscillate +2/−2σ in an alternating pattern. This is a shape mismatch
indicating the MC Q_FB distribution is slightly narrower or has different
kurtosis than data. The pattern is at the ±2σ level throughout, never
exceeding the plot range. Figure is square, experiment label present.

**[VISUAL] CONCERN (persistent):** The correlated zigzag pull structure
across all Q_FB figures (κ = 0.3, 0.5, 1.0, 2.0) is consistent with a
systematic data/MC width mismatch of ~1–2%. This could affect the AFBb
sensitivity. Documented for Phase 4.

**Verdict: PASS.**

---

**Fig 9: `data_mc_qfb_k0.5_magnus_1207_20260402.png`**

Similar to Fig 8. The distribution is slightly wider (as expected for
higher κ), and the same oscillating pull pattern is visible. Core agreement
is good. Figure quality is acceptable.

**Verdict: PASS.**

---

**Fig 10: `data_mc_qfb_k1.0_magnus_1207_20260402.png`**

Q_FB (κ=1.0) is a smooth Gaussian with no extreme pulls. The distribution
is broader than κ=0.3. The pull panel shows the zigzag at a reduced
amplitude compared to lower κ. Figure is square, experiment label present.

**Verdict: PASS.**

---

**Fig 11: `data_mc_qfb_k2.0_magnus_1207_20260402.png`**

Q_FB (κ=2.0) shows a tent-shaped distribution: flat wings with a central
peak, reflecting the dominance of the leading-particle charge at high κ.
Data and MC agree closely. Pull deviations are scattered at ±2σ with no
systematic trend. Figure is square, experiment label present.

**Verdict: PASS.**

---

**Fig 12: `data_mc_qfb_kinf_magnus_1207_20260402.png`**

The leading-particle charge Q_FB (κ=∞) takes only three discrete values
(−2, 0, +2). The central bin at Q=0 has MC reaching ~1.38×10^6 while data
sits at ~0.77×10^6 (visible from the data error bar landing well below the
MC bar height). Similarly, the outer bins (Q=±2) have MC much taller than
data. The pull panel shows a pull of approximately −2.5σ at Q=+2.

**[VISUAL] CONCERN (persistent):** Data is systematically below MC at all
three bins, but particularly so at Q=0 (approximately −40% in relative
terms from reading the plot). This is a significant data/MC discrepancy
for this discrete variable. It suggests MC overproduces events with a
neutral leading particle, or data has a deficit. Since the charge asymmetry
at Q=±2 is the direct AFBb observable, any data/MC shape disagreement here
is a critical Phase 4 input that needs investigation. This is not a plot
quality failure but a physics flag.

**Verdict: PASS** (concern documented; discrepancy noted for Phase 4).

---

**Fig 15: `data_mc_thrust_magnus_1207_20260402.png`**

The thrust distribution after preselection rises sharply near T→1.0 as
expected for hadronic Z decays. Data and MC agree in shape throughout.
The pull panel shows deviations at the ±2σ level scattered across bins
with no systematic trend. The figure is square, experiment label present.

**Verdict: PASS.**

---

**Fig 16: `data_mc_costheta_magnus_1207_20260402.png`**

The cos θ_thrust distribution after the |cos θ| < 0.9 cut shows the
characteristic dipole-like shape (higher event density near ±0.9, dip in
center). Data and MC agree well. Pull panel shows ±2σ deviations scattered
without systematic trend. Figure is square, experiment label present.

**Verdict: PASS.**

---

**Fig 17: `data_mc_nch_magnus_1207_20260402.png`**

Charged particle multiplicity peaks at Nch ≈ 20 as expected for hadronic
Z decays. Data and MC show excellent agreement across the full distribution
(0–45 tracks). Pull panel shows ±2σ deviations only in the low-multiplicity
tail (Nch < 10) and high tail (Nch > 35) where statistics are limited.
Figure is square, experiment label present.

**Verdict: PASS.**

---

**Fig 18: `data_mc_sphericity_magnus_1207_20260402.png`**

The sphericity distribution falls steeply from a peak at sphericity ≈ 0.0
(jet-like events) to near-zero at sphericity ≈ 0.5+. The first bin
(sphericity ≈ 0.0) shows data visibly above MC with a pull of approximately
+3σ — the data point sits at ~720,000 while the MC bar is at ~630,000.
For sphericity > 0.05 the agreement is good. Figure is square, experiment
label present.

**[VISUAL] CONCERN (persistent):** The first-bin ~3σ pull at sphericity ≈ 0
persists. Very collimated events (low sphericity) are not representative of
typical hadronic Z → bb events but could indicate a fragmentation modeling
issue or a residual two-photon / di-lepton contamination.

**Verdict: PASS** (first-bin concern documented; not an automatic failure
for Phase 3).

---

**Fig 19: `data_mc_d0_magnus_1207_20260402.png`**

The impact parameter d0 distribution for quality tracks shows the
characteristic sharp peak at d0 = 0 with wings extending to ±0.1 cm. The
spike structure near d0 = 0 is visible (multiple adjacent high bins due to
the resolution peak and the discrete structure of vertex detector hits).
Data and MC agree well in the core, with the largest pull deviations (~2.5σ)
visible at d0 ≈ ±0.02 cm in the wings. The figure is square, experiment
label present.

**Verdict: PASS.**

---

**Fig 20: `data_mc_trackpt_magnus_1207_20260402.png`**

The track pT spectrum on a log y-axis falls steeply from a peak at low pT.
Data and MC agree well for pT < 10 GeV/c. At pT > 20 GeV/c, data falls
more steeply than MC — the MC has more events in the high-pT tail. The
pull panel shows pulls of −2.5σ at several points in the 5–30 GeV/c range.
Figure is square, experiment label present.

**[VISUAL] CONCERN (persistent):** The systematic data-below-MC trend at
high pT (> 20 GeV/c) may affect b-tagging efficiency since high-pT tracks
from B decays contribute to the IP significance tagger. This should be
documented in SELECTION.md.

**Verdict: PASS** (concern documented).

---

## CROSS-FIGURE CONSISTENCY CHECKS

**Comparison to iteration 1 cross-figure consistency:**

The primary cross-figure RED FLAG from iteration 1 (R_b scan 3–5× above
SM with no explanation while closure tests claim PASS) is PARTIALLY
resolved. The R_b scan now carries a clear annotation explaining the bias
as expected at Phase 3. However, the closure tests remain problematic:
the bFlag chi²/ndf = 1114 is labeled PASS despite being ~370× above the
closure alarm band failure threshold of chi²/ndf > 3. The "broken journey"
concern therefore persists in a narrower form: the bFlag shape closure
test is physically broken (two distributions from the same event sample
with different bFlag cuts should not have chi²/ndf > 1000 unless the
discriminant is extremely powerful — in which case this is not a closure
test of independent samples but a demonstration of discriminating power,
and the "passes" criterion is wrong).

The remaining figures show internally consistent patterns:
- P_hem tail disagreement (Fig 7) matches combined tag tail (Fig 5) — consistent.
- All Q_FB figures (κ = 0.3, 0.5, 1.0, 2.0) show the same width-mismatch
  pull pattern — consistent.
- sigma_d0 scale factors all above 1.0 (Fig 3) is consistent with the
  calibration procedure's interpretation if the nominal σ_d0 parameterization
  systematically underestimates resolution.

No new broken-journey patterns observed beyond the persistent closure test
concern.

---

## SUMMARY TABLE

| # | Filename | Type | Iteration 1 | Iteration 2 | Category | Finding |
|---|----------|------|-------------|-------------|----------|---------|
| 1 | cutflow_magnus_1207_20260402.png | diagnostic | FAIL (A) | PASS | — | Code variable names fixed |
| 2 | d0_sign_validation_magnus_1207_20260402.png | diagnostic | FAIL (A) | PASS | — | Curves now distinguishable |
| 3 | sigma_d0_calibration_magnus_1207_20260402.png | diagnostic | FAIL (A) | PASS | B | A resolved; fontsize=5 labels are very small |
| 4 | data_mc_significance_magnus_1207_20260402.png | data_mc | PASS | PASS | — | Good data/MC agreement |
| 5 | data_mc_combined_tag_magnus_1207_20260402.png | data_mc | PASS | PASS | — | High-tag tail concern (documented) |
| 6 | data_mc_hemisphere_mass_magnus_1207_20260402.png | data_mc | PASS (B) | PASS | — | B/c threshold line added |
| 7 | data_mc_phem_magnus_1207_20260402.png | data_mc | PASS | PASS | — | Same tail concern as Fig 5 |
| 8 | data_mc_qfb_k0.3_magnus_1207_20260402.png | data_mc | PASS | PASS | — | Width-mismatch pull pattern |
| 9 | data_mc_qfb_k0.5_magnus_1207_20260402.png | data_mc | PASS | PASS | — | Same as Fig 8 |
| 10 | data_mc_qfb_k1.0_magnus_1207_20260402.png | data_mc | PASS | PASS | — | Same as Fig 8 |
| 11 | data_mc_qfb_k2.0_magnus_1207_20260402.png | data_mc | PASS | PASS | — | Tent-shaped, good agreement |
| 12 | data_mc_qfb_kinf_magnus_1207_20260402.png | data_mc | PASS | PASS | — | Data systematically below MC (concern) |
| 13 | rb_operating_scan_magnus_1207_20260402.png | result | FAIL (RED FLAG) | PASS | B | Bias annotation added; curves distinguishable; residual B |
| 14 | closure_tests_magnus_1207_20260402.png | closure | FAIL (A) | FAIL | A | Three new violations: set_title, exp label collision, chi²/ndf=1114 labeled PASS |
| 15 | data_mc_thrust_magnus_1207_20260402.png | data_mc | PASS | PASS | — | Good agreement |
| 16 | data_mc_costheta_magnus_1207_20260402.png | data_mc | PASS | PASS | — | Good agreement |
| 17 | data_mc_nch_magnus_1207_20260402.png | data_mc | PASS | PASS | — | Excellent agreement |
| 18 | data_mc_sphericity_magnus_1207_20260402.png | data_mc | PASS | PASS | — | First-bin pull ~3σ (concern) |
| 19 | data_mc_d0_magnus_1207_20260402.png | data_mc | PASS | PASS | — | Good agreement |
| 20 | data_mc_trackpt_magnus_1207_20260402.png | data_mc | PASS | PASS | — | MC overestimates high-pT tail (concern) |

---

## FINDINGS BY CATEGORY

### RED FLAG (automatic Category A — arbiter may NOT downgrade)

None in iteration 2. The R_b scan RED FLAG from iteration 1 is downgraded
to Category B pending a quantitative bias prediction overlay.

### CATEGORY A VIOLATIONS (new in iteration 2)

1. **[LINT] + [VISUAL] Fig 14 — `closure_tests` / `plot_all.py` lines 597, 618,
   642:** `ax.set_title()` is called on all three closure test sub-panels.
   This is a forbidden pattern per the plotting standard. Additionally, the
   center panel title "(b) bFlag shape" visually collides with the ALEPH
   experiment label, making both partially unreadable in the rendered PNG.
   Fix: remove `set_title` calls; use `ax.text()` annotations at the top of
   each panel for sub-panel labels "(a)", "(b)", "(c)".

2. **[VISUAL] Fig 14 — `closure_tests`:** The ALEPH experiment label is placed
   on the center panel (axes[1]) and collides with the `set_title` text.
   For multi-panel figures, the experiment label must appear once on the
   primary/leftmost panel without collision. Fix: move `exp_label_data` call
   to `axes[0]`, remove `set_title` from all panels.

3. **[VISUAL] Fig 14 — `closure_tests` (physics / misrepresentation):**
   Panel (b) displays chi²/ndf = 1114 for the bFlag shape comparison but
   is annotated "PASS". The closure alarm band threshold is chi²/ndf > 3 →
   FAIL. Chi²/ndf = 1114 is a catastrophic failure (370× the failure
   threshold) and must be labeled FAIL. The `passes: true` flag in
   `closure_results.json` is inconsistent with the displayed value and
   violates the "passes: false while text claims acceptable → Category A
   misrepresentation" rule (and its converse). Fix: correct the PASS/FAIL
   logic in `closure_tests.py`, regenerate the JSON and figure, investigate
   why the bFlag=4 vs bFlag=-1 comparison gives such extreme chi²/ndf.

4. **[VISUAL] Fig 14 — `closure_tests` (contamination ratio):**
   The contamination injection test shows observed/predicted ratio = 2.14
   and is labeled PASS. A ratio of 2.14 indicates the contamination
   propagation formula is off by >2×. Per closure alarm band rules, this
   should fail (ratio > 2 indicates the background model does not accurately
   predict contamination shifts). Fix: correct the PASS threshold or the
   formula, regenerate results.

### CATEGORY B VIOLATIONS (new in iteration 2)

5. **[LINT] `plot_all.py` lines 321, 625:** Absolute `fontsize=5` used
   instead of a relative string (`"x-small"` or `"xx-small"`). The sigma_d0
   calibration tick labels (line 321) and closure test panel legend (line 625)
   use absolute integer fontsize. This produces unpredictable rendering at
   different DPI. Fix: replace `fontsize=5` with `fontsize="xx-small"`.

6. **[VISUAL] Fig 3 — `sigma_d0_calibration`:** Despite the category A
   resolution (labels are now human-readable), the `fontsize=5` labels on the
   x-axis are nearly invisible in the rendered PNG. Even a reader with
   perfect eyesight cannot read the calibration bin labels at the rendered size.
   This makes the figure effectively equivalent to having no x-axis labels for
   the majority of bins. Fix: use larger relative fontsize and consider
   displaying all bins or using a table format.

7. **[VISUAL] Fig 13 — `rb_operating_scan`:** The extracted R_b values are
   explained as "expected bias" in the annotation, but no quantitative
   predicted-bias curve is shown. The figure alone cannot validate that the
   observed values match the expected bias from the assumed background
   efficiencies (ε_c = 0.05, ε_uds = 0.005). A reader cannot tell if the
   bias is "expected" or "larger than expected." Fix: compute and overlay the
   predicted R_b_apparent(threshold) curve derived from the double-tag formula
   with the assumed background efficiencies.

### CATEGORY C WARNINGS (no re-review needed)

8. **[LINT] `plot_all.py`:** `mc_scale_to_data=True` applied to derived-quantity
   figures (Q_FB, P_hem). Carried from iteration 1. Still recommended to
   use luminosity-scaled comparison or add explicit documentation.

9. **[LINT] `plot_all.py`:** Pull denominator is `sqrt(sigma_data² + sigma_MC²)`,
   which double-counts statistical uncertainty. Negligible at current event
   counts. Carried from iteration 1.

10. **[VISUAL] Fig 1 — `cutflow`:** y-axis label "Events / Tracks" is ambiguous
    (some bars count events, some count tracks). A two-panel layout would be
    cleaner. Low priority.

11. **[VISUAL] Fig 2 — `d0_sign_validation`:** "Gate: PASS" text does not
    specify the quantitative gate criterion.

---

## OVERALL VERDICT

**FAIL — 4 Category A violations remain.**

### What was fixed relative to iteration 1

| Finding | Status |
|---------|--------|
| RED FLAG: R_b scan values unexplained | RESOLVED (downgraded to Cat B — annotation added, curves distinguishable) |
| Cat A: cutflow code variable names | FIXED |
| Cat A: d0 sign curves indistinguishable | FIXED (tight double-tag now used) |
| Cat A: sigma_d0 code variable names | FIXED (human-readable labels) |
| Cat B: hemisphere mass threshold line missing | FIXED |
| Cat A: closure test overlapping text | PARTIALLY FIXED (3-panel layout, no text overlap) |

### What remains unresolved (or newly introduced)

| Finding | Category | Source |
|---------|----------|--------|
| `set_title` calls in closure test figure (rendering collision) | A | New in iter 2 |
| Experiment label collision on closure test center panel | A | New in iter 2 |
| bFlag chi²/ndf = 1114 labeled PASS | A | Persists from iter 1 (was "concern", now confirmed Category A) |
| Contamination ratio = 2.14 labeled PASS | A | Persists from iter 1 (was "concern", now confirmed Category A) |
| Absolute fontsize=5 in two places | B | New in iter 2 (sigma_d0, closure legend) |
| sigma_d0 tick labels illegible at fontsize=5 | B | New in iter 2 |
| R_b bias curve not quantitatively predicted | B | New in iter 2 |

### Required before Phase 4 begins

1. **Fix closure test `set_title` calls** — remove `ax.set_title()` on all
   three panels; use `ax.text()` annotations or caption-only panel labels.
   Reposition `exp_label_data` to left panel without collision.

2. **Fix closure test PASS/FAIL logic** — the bFlag chi²/ndf = 1114 must be
   labeled FAIL, not PASS. Investigate what is causing chi²/ndf >> 3 for the
   bFlag=4 vs bFlag=-1 shape comparison. If the shapes genuinely differ this
   much, the closure test is demonstrating discriminating power, not closure,
   and must be redesigned.

3. **Fix contamination injection PASS/FAIL logic** — ratio = 2.14 fails the
   closure test. Investigate the discrepancy between predicted and observed
   contamination shift; fix or document with 3 remediation attempts.

4. **Replace `fontsize=5` with relative fontsize** — two locations in
   `plot_all.py`.

5. **Add predicted bias curve to R_b scan** (Category B) — compute and overlay
   the expected R_b_apparent(threshold) from the double-tag formula with the
   assumed background efficiencies.
