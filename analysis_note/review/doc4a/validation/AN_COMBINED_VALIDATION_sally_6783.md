# AN Combined Validation — Doc 4a v5
**Session:** sally_6783  
**Date:** 2026-04-03  
**Document:** `analysis_note/ANALYSIS_NOTE_doc4a_v5.{tex,pdf}`  
**Scope:** Plot validator + rendering reviewer (combined)

---

## Overall Classification: **B**

The document compiles cleanly, all cross-references resolve, and the physics
content is coherent. However, several Category B defects are present across
three areas: workflow artifact leakage into figures and body text, a
caption/figure content mismatch on Figure 14, and a misleading legend entry
in Figure 5. No Category A defects are identified. All issues are fixable
without re-running the analysis.

---

## 1. Cross-Reference and Compilation Check

**Result: PASS**

- No `??` tokens appear in the compiled PDF for any `\ref`, `\cref`,
  `\label`, or `\cite` command. All 29 figures, all tables, and all
  equations resolve correctly.
- Bibliography compiles to 11 entries; all are cited. No orphaned entries.
- The `\tbd{}` placeholders in the Results summary table (Table 11, rows
  "Rb full data" and "AFBb full data") and in the Conclusions paragraph are
  rendered in grey italic — this is the correct placeholder mechanism for a
  Doc 4a note where full-data results are not yet available. These are not
  defects.
- `\cref` and `\ref` are both in use; no mixing causes malformed output.

**Minor note (Category C):** Line 4 of the TeX file and the Change Log
section (page 4 of the PDF) both read "Doc **4b** v5" rather than "Doc 4a
v5". The filename is `ANALYSIS_NOTE_doc4a_v5.tex` but the internal label
says Doc 4b. This is a copy-paste artefact from the Doc 4b rewrite. Fix the
header comment (line 4) and the Change Log heading to read "Doc 4a v5".

---

## 2. Figure Rendering Check

All 29 numbered figures are present on disk in both PDF and PNG form under
`analysis_note/figures/` and cross-checked against `phase*/outputs/figures/`.
All `\includegraphics` paths resolve. No figure produces a bounding-box
error or blank box in the compiled PDF.

---

## 3. Figure Quality — Per-Figure Findings

### 3.1 Figure 5 — Efficiency calibration (1×3 panel): Category B

**File:** `figures/efficiency_calibration.pdf`  
**Problem:** The legend in the left panel (eps_b) reads **"From MC (SM
truth)"**. This label is factually incorrect and contradicts a core analysis
constraint stated explicitly in Section 2.3: "The MC contains no truth
flavour labels … the bFlag branch is −999 for all MC events." The efficiencies
are calibrated by chi^2 minimisation assuming R_b = R_b^SM, not from MC
truth labels. The legend text will mislead any reader who notices it.  
**Severity:** Category B — incorrect factual claim in a figure legend.  
**Fix:** Change legend text to "From MC (assuming R_b^SM)" or "MC
self-calibrated (R_b = R_b^SM)".

**Secondary problem (Category C):** The 1×3 subplot uses `figsize=(10,10)`,
producing three very narrow non-square panels (~3.3 in wide each). The
y-axis label on the right panel (eps_uds) renders close to the panel edge.
The standard for multi-panel figures is to scale width proportionally
(e.g., `figsize=(30,10)` for a 1×3). Figures are still legible at current
size but do not meet the square-panel standard.

### 3.2 Figure 6 — R_b operating point scan on MC: Category B (workflow artifact)

**File:** `figures/rb_operating_scan_magnus_1207_20260403.pdf`  
**Problem:** The figure contains an embedded annotation text box reading:

> "Phase 3: nominal eps_c, eps_uds not calibrated to this tagger.  
> Bias expected, Phase 4 multi-WP fit will constrain backgrounds.  
> No stability plateau expected until calibration [B4]"

This is an internal workflow note baked into the figure at production time
and never removed. It exposes the internal phase structure of the analysis
to any reader of the document and reads as unprofessional in a physics note.  
**Severity:** Category B — workflow artifact visible in a numbered figure.  
**Fix:** Regenerate the figure without the annotation box.

### 3.3 Figure 14 — Hemisphere charge distribution: Category B (caption/figure mismatch)

**File:** `figures/S2b_hemisphere_charge_data_mc.pdf`  
**TeX caption (line 1431–1435):**
> "Hemisphere charge Q_h distribution **at kappa = 2.0** in data (1992–1995,
> 10%) and MC (1994, normalised to data integral). The distribution is
> symmetric about zero …"

**Actual figure content (verified from PNG):** The figure is a **2×2 panel**
showing Q_FB distributions for **kappa = 0.3, 0.5, 1.0, and 2.0** — all four
kappa values simultaneously, not just kappa = 2.0. The caption describes only
one panel of a four-panel figure.

This is a substantive mismatch: a reader following the caption will conclude
the figure shows a single distribution, but the figure actually shows the
kappa evolution across four values.  
**Severity:** Category B — caption does not describe what the figure shows.  
**Fix:** Update the caption to read: "Hemisphere charge difference Q_FB
distributions for four momentum-weighting exponents (kappa = 0.3, 0.5, 1.0,
2.0) in data (1992–1995, 10%) and MC (1994, normalised to data integral). The
distributions broaden with increasing kappa. The slight asymmetry in data
reflects the physical forward-backward asymmetry."

### 3.4 Figure 15 — Kappa consistency for A_FB^b: Category B (workflow artifact)

**File:** `figures/F7b_kappa_consistency_10pct.pdf`  
**Problem:** The figure legend contains the entry **"Phase 4a (MC)"** (blue
squares). This is an internal workflow label naming an analysis phase, which
should never appear in a physics note figure. The PDF rendering on page 23
confirms this legend entry is visible.  
**Severity:** Category B — workflow artifact in figure legend.  
**Fix:** Rename the legend entry to "Expected (MC pseudo-data)" or simply
"MC" to match the language used elsewhere in the note.

### 3.5 Figure 7 — R_b stability on 10% data: Category B (workflow artifact in legend)

**File:** `figures/F1b_rb_stability_10pct.pdf`  
**Problem:** The figure legend (confirmed from PNG) contains **"Phase 4a
(MC)"** as a legend entry for the blue data points, alongside "10% data".
This is the same workflow-artifact legend-label class as Figure 15.  
**Severity:** Category B.  
**Fix:** Rename "Phase 4a (MC)" to "MC pseudo-data" or "MC (SF-corrected)".

### 3.6 Figure 20 — Independent closure test (1×2 panel): Category C

**File:** `figures/closure_test_phase4a.pdf`  
**Problem:** The figure title region shows partially overprinted text:
"**ALEPH** Open Simulation" is overlaid by what appears to be garbled font
rendering. Additionally, the 1×2 panel uses `figsize=(10,10)`, squashing the
two subplots into narrow non-square panels. The left-panel y-axis label
("Pull (R_b^extracted - R_b^SM)/sigma") is cut on the left edge in the
rendered PDF. The right panel label for corruption scenarios is also
compressed.  
**Severity:** Category C (rendering is degraded but content is readable).  
**Fix:** Regenerate with `figsize=(20,10)` to give each panel a square
aspect. Verify the experiment-label rendering does not overprint.

### 3.7 Figures 3, 8, 11–13 — Pass

All single-panel figures (d0_sign validation, AFB angular distribution,
mirrored-significance sanity check, bFlag discrimination, contamination
injection) render correctly: square aspect, experiment label visible, axis
labels readable, no overlap, no title on panel. Pass.

### 3.8 Figures 16–19, 23–29 — Data/MC comparison figures: Pass

All multi-panel data/MC comparisons (thrust, costheta, multiplicity, track
pT, QFB at multiple kappas, hemisphere mass, sphericity, d0, track weight)
render correctly. Each panel shows the "ALEPH Open Data" experiment label
and sqrt(s)=91.2 GeV energy label. Pull panels are present and correctly
labelled. MC normalisation to data integral is stated in each caption.
Year annotations (data: 1992–1995; MC: 1994) are present in all captions.
Pass.

### 3.9 Duplicate \label on Figure 23 (Appendix F): Category C

**TeX lines 2569–2570:**
```latex
\label{fig:datamc_sphericity}
\label{fig:datamc_d0}
```
Two `\label` commands are placed inside the same `\figure` environment. LaTeX
will silently use the last label and the first label will be multiply defined.
Any `\cref{fig:datamc_sphericity}` will resolve to the correct figure (LaTeX
does not crash), but the behaviour is undefined if both labels are ever
referenced independently. The appendix text at line 2551–2553 references both
labels.  
**Severity:** Category C.  
**Fix:** Split into two separate figure environments (one for sphericity, one
for d0), or reference only one label in the appendix text.

---

## 4. Workflow Artifact Check (Body Text)

### 4.1 "Phase 4c" in body text: Category B

**TeX line 2228–2232 (Conclusions section):**
```latex
\tbd{The full data results (Phase 4c, $\sim$2.9 million events)
will reduce the statistical uncertainties by a factor of
$\sim$3, and the data-driven calibration can be refined with the
larger sample. The dominant charm efficiency systematic will
remain the precision bottleneck.}
```
This sentence is wrapped in `\tbd{}` (grey italic), so it renders visibly in
the PDF as a placeholder paragraph in the Conclusions section. While `\tbd`
is an appropriate mechanism for Doc 4a, the phrase "Phase 4c" inside the
grey-italic placeholder is an internal workflow term that would be confusing
to any external reader. The Known Limitations section (item 6, line 2394)
also contains "planned for Phase~4c" in unformatted body text (not inside
`\tbd{}`).  
**Severity:** Category B — unformatted "Phase 4c" reference at line 2394 is
a workflow artifact in plain body text.  
**Fix:** At line 2394, replace "planned for Phase~4c" with "planned for the
full-data analysis". The `\tbd`-wrapped occurrence in Conclusions is
acceptable as a placeholder (grey italic signals draft status) but should
also be rephrased to remove the internal phase name.

Similarly, appendix R (Interpretation of the A_FB^b Result), page 45, line
997 reads "The full data sample (*Phase 4c*) will improve the statistical
precision …" with "Phase 4c" in italics inside a sentence that is NOT wrapped
in `\tbd{}`. This is a plain-text workflow artifact.  
**Fix:** Rephrase to "The full data sample (~2.9M events) will improve …"

### 4.2 "Doc 4c" placeholders in Results table: Pass (acceptable)

Table 11 rows for "Rb (full data)" and "AFBb (full data)" contain `\tbd{Doc
4c}` entries in all cells. These render in grey italic and clearly signal
placeholder status. This is the correct Doc 4a treatment.

### 4.3 Change Log says "Doc 4b v5": Category C

The file is `ANALYSIS_NOTE_doc4a_v5.tex` and the document version should be
Doc 4a v5. The Change Log heading and the TeX header comment both say "Doc 4b
v5", which is a copy-paste error from the prior rewrite. Fix in both
locations.

---

## 5. Internal File Reference Check

**Result: PASS with one minor finding.**

No bare filesystem paths to analysis scripts, data files, or phase
directories appear in the document body. The Reproduction Contract appendix
(X) correctly references the analysis via `pixi run` commands and relative
paths from the analysis root — this is appropriate for a reproducibility
section. The `\includegraphics` path `figures/closure_test_phase4a.pdf`
contains "phase4a" in the filename, which is an internal naming convention
but is encapsulated within the figures directory and not exposed to readers
as a workflow path.

---

## 6. Provenance Markers Check

**Result: PASS**

The `\measured{}` (blue) and `\external{}` (red) commands are defined in the
preamble and used consistently throughout:
- `\measured{}` usage: 33 occurrences. Applied to all analysis results (R_b,
  A_FB^b, calibration ratios, efficiency values measured from data or
  smeared-MC).
- `\external{}` usage: 86 occurrences. Applied to all published/theory values
  (SM predictions, LEP combinations, PDG constants, published delta_b, R_c).
- The abstract, introduction, results tables, systematics tables, and
  comparison tables all apply markers correctly.
- The provenance legend is explained in the Change Log and in the preamble
  comments.

No instances found where a measured quantity is marked as external or vice
versa.

---

## 7. Orphaned Figures/Tables Check

**Result: PASS**

All 29 numbered figures are referenced from the text at least once via
`\cref{}` or `\ref{}`. All 27 tables are similarly referenced. No figure or
table floats without an in-text reference.

---

## 8. Forbidden Plotting Pattern Scan (phase*/src/)

Checked `phase3_selection/src/` and `phase4_inference/4a_expected/src/` and
`phase4_inference/4b_partial/src/` for the six forbidden patterns:

| Pattern | phase3/src | phase4a/src | phase4b/src | Status |
|---|---|---|---|---|
| `plt.colorbar` / `fig.colorbar(im, ax=` | NOT FOUND | NOT FOUND | NOT FOUND | PASS |
| `ax.set_title(` | NOT FOUND | NOT FOUND | NOT FOUND | PASS |
| `tight_layout` | NOT FOUND | NOT FOUND | NOT FOUND | PASS |
| `histtype="errorbar"` without `yerr=` | NOT FOUND | NOT FOUND | NOT FOUND | PASS |
| `data=False` with `llabel=` | NOT FOUND | NOT FOUND | NOT FOUND | PASS |
| `figsize=` with non-(10,10) values | **FOUND** (phase4a, line 360: `(1,2,figsize=(10,10))`; line 376 approx: `(1,3,figsize=(10,10))`; phase4b line 444: `figsize=(20,20)`) | see note | see note | **Category B** |

**figsize violation detail:** The forbidden pattern rule states "figsize=
with values other than (10,10)". The violations here are the inverse:
multi-panel figures that *keep* (10,10) when they should scale proportionally.
This produces the compressed-panel rendering seen in Figures 5 (1×3) and 20
(1×2). The phase4b script also contains one `figsize=(20,20)` for a 2×2
panel (correct). The prior plot-validation report
(`phase4_inference/4a_expected/review/validation/INFERENCE_EXPECTED_PLOT_VALIDATION_fiona_7de9.md`)
already identified and classified these as Category B; they were not fixed
before the AN was compiled.

---

## 9. Summary of Findings

| # | Location | Finding | Category |
|---|---|---|---|
| F1 | Fig. 5 legend | "From MC (SM truth)" — factually wrong; no MC truth labels exist | B |
| F2 | Fig. 6 embedded annotation | "Phase 3: nominal eps_c…" workflow note baked into figure | B |
| F3 | Fig. 14 caption | Caption says "at kappa=2.0" but figure is 2×2 panel for kappa=0.3,0.5,1.0,2.0 | B |
| F4 | Fig. 15 legend | "Phase 4a (MC)" — workflow artifact in legend | B |
| F5 | Fig. 7 legend | "Phase 4a (MC)" — workflow artifact in legend | B |
| F6 | Body text §14 item 6 | "planned for Phase~4c" — unformatted workflow term in body | B |
| F7 | Appendix R body text | "Phase 4c" in italic but not tbd-wrapped | B |
| F8 | Source scripts | 1×2 and 1×3 panels using figsize=(10,10) instead of scaled dimensions | B |
| F9 | Fig. 20 rendering | 1×2 panel compressed; y-axis label clipped; experiment label overprint | C |
| F10 | TeX line 2569–2570 | Duplicate \label{} in same figure environment | C |
| F11 | Change Log + TeX header | "Doc 4b v5" should read "Doc 4a v5" | C |
| F12 | Fig. 5 layout | 1×3 panel not square at figsize=(10,10) | C |

**Category A findings: 0**  
**Category B findings: 8**  
**Category C findings: 4**

---

## 10. Required Actions Before Advancing

The following must be resolved before this document is submitted as a final
Doc 4a:

1. **F1** — Fix Fig. 5 legend: remove "From MC (SM truth)", replace with
   "MC self-calibrated (R_b = R_b^SM)".
2. **F2** — Regenerate Fig. 6 (`rb_operating_scan_magnus_1207_20260403`)
   without the embedded "Phase 3" annotation box.
3. **F3** — Rewrite Fig. 14 caption to describe the actual 2×2 four-kappa
   panel content.
4. **F4, F5** — Regenerate Figs. 7 and 15 with legend entry "Phase 4a (MC)"
   replaced by "MC pseudo-data" or "MC".
5. **F6, F7** — Replace all bare "Phase 4c" references in body text (not
   inside `\tbd{}`) with "full-data analysis" or equivalent.
6. **F8** — Fix `plot_phase4a.py` lines ~360 and ~376 to use `figsize=(20,10)`
   and `figsize=(30,10)` respectively, then regenerate Figs. 5 and 20.

Category C items (F9–F12) should be fixed before final submission but do not
block advancement to Doc 4b preparation.
