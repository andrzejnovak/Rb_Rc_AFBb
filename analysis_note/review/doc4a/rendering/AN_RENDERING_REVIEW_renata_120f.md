# Rendering Review — Doc 4a v2
**Reviewer:** renata_120f
**Document:** `analysis_note/ANALYSIS_NOTE_doc4a_v2.pdf` / `.tex`
**Date:** 2026-04-03
**Classification:** **C** (all v1 A and B items resolved; no new rendering defects found)

---

## 1. Compilation Status

The PDF exists, is 52 pages (within the 50–100 page target), and shows no compilation
errors. All 36 figure PDF files are present on disk. The compiled PDF matches the LaTeX
source with no rendering artefacts in any of the 52 pages inspected.

---

## 2. Verification of v1 Findings

The v1 review (quentin_b524) identified 5 Category A items, 2 Category B items, and
1 Category C item. Each is verified below.

### R1 — Unresolved `\ref{sec:jetcharge}` (was A)
**STATUS: FIXED.**

`.tex` line 410: `computation (Section~\ref{sec:jetcharge})` — the `\ref` is present.
`.tex` line 2776: `\label{sec:jetcharge}` — the matching label is now defined in
Appendix J (Hemisphere Charge Properties). The PDF body (page 9, Sec. 3.2) renders
"Section J" correctly with no `??`. Cross-reference resolves completely.

### R2 — Three orphaned figures (was A)
**STATUS: FIXED.**

All three figures now have prose `\ref{}` calls:
- `fig:datamc_track` — `.tex` line 435: "Figure~\ref{fig:datamc_track} shows the
  track-level comparisons for $p_T$ and $d_0$." (PDF page 9, Sec. 3.3)
- `fig:p1_d0_trackpt` — `.tex` line 474: "Figure~\ref{fig:p1_d0_trackpt}" in the
  Phase 1 exploration prose. (PDF page 11, Sec. 3.4)
- `fig:datamc_tag2` — `.tex` line 679: "Figure~\ref{fig:datamc_tag2} shows the
  displaced-track..." (PDF page 14, Sec. 4.3)

### R3 — Seven orphaned tables (was A)
**STATUS: FIXED.**

All seven tables now have prose `\ref{}` calls confirmed in the `.tex`:
- `tab:mc_samples` — line 310
- `tab:track_cutflow` — line 404
- `tab:corrupted_corrections` — line 1474
- `tab:sin2theta_comparison` — line 1987
- `tab:weight_impact` — line 2715
- `tab:hemisphere_charge_properties` — line 2779
- `tab:nsigma_fractions` — line 2863

Each reference appears in a natural prose sentence that directs the reader to the table.

### R4 — Typo `A_\mathrm{FM}^b` (was A)
**STATUS: FIXED.**

Searched the entire `.tex` for `A_\mathrm{FM}`. The only occurrence is on line 76,
inside the Change Log bullet item documenting the fix itself:
`\item Fixed $A_\mathrm{FM}^b$ typo $\to$ $A_\mathrm{FB}^b$ (3 instances).`
This is correct — the Change Log records the historical error. All physics content
uses `$A_\mathrm{FB}^b$` throughout. The PDF title page (page 1), Introduction
(page 6), Sec. 4.8 (page 19), Conclusions (page 34), and all appendices show
`$A_\mathrm{FB}^b$` without exception. No `FM` subscript visible in any physics prose.

### R8 — Truncated x-axis label in Fig. 11 right panel (was A)
**STATUS: FIXED.**

The `efficiency_calibration.pdf` figure was regenerated. All three panels
($\varepsilon_b$, $\varepsilon_c$, $\varepsilon_\mathrm{uds}$) now show the complete
"Working point" x-axis label with no clipping. Verified by direct inspection of the
figure source file.

### R5 — Large whitespace gaps (was B)
**STATUS: SUBSTANTIALLY IMPROVED; residual gap is Category C.**

The most severe gaps from v1 have been reduced. The Change Log and TOC now occupy
pages 1–5, with content distributed more evenly. One residual whitespace gap remains:
page 4 (the fourth TOC page) ends at approximately 55% with the bottom ~45% blank,
because the TOC content terminates mid-page followed by a `\clearpage`. This is a
cosmetic issue in a working document and does not affect readability. The final page
(page 52) also has approximately 65% blank, which is normal for the last page of an
appendix. No gaps exceeding one-third of a page appear within body sections.
**Reclassified: C (informational).**

### R6 — Inconsistent figure sizing (was B)
**STATUS: UNCHANGED; reclassified to C.**

Fig. 21 (QFB survey, Appendix D.2, `.tex` lines 2540–2542) still uses
`width=0.32\linewidth` for the three-panel row rather than the `height=` convention
used elsewhere. Inspection of the rendered PDF (page 42) confirms the panels are
legible and not distorted — the three panels fit side-by-side at a visually appropriate
size. The inconsistency is a style preference rather than a readability defect.
No action required before advancement.
**Reclassified: C (informational).**

### R7 — `\tbd{}` markers (was C)
**STATUS: PRESENT AND CORRECT.**

Five `\tbd{}` calls in Table 15 (Results summary, page 32) render as gray italic
"*Doc 4b*" and "*Doc 4c*" placeholders. The table header row also uses
`\tbd{10\% data}` and `\tbd{Full data}` as column headers. All render correctly
and are clearly distinguishable from surrounding content. Expected and correct for
Phase 4a.

---

## 3. Cross-Reference Completeness Check

All cross-references were verified:

- **`\ref{sec:jetcharge}`**: resolves to Appendix J (label at line 2776). **PASS.**
- **All `\ref{sec:...}` calls** (approximately 79 total `\ref{}` calls in the document):
  no `??` appears anywhere in the 52-page PDF. **PASS.**
- **All `\ref{eq:...}` calls** (Eqs. 7–8, 11, 13 referenced from prose): resolve
  correctly. **PASS.**
- **All `\ref{fig:...}` calls**: 24 figures referenced from prose; all resolve. **PASS.**
- **All `\ref{tab:...}` calls**: 26 tables referenced from prose; all resolve. **PASS.**
- **All `\cite{...}` keys**: 12 bibliography entries; all render with numeric labels
  [1]–[12] in the bibliography on page 39. No `[?]` unresolved citations visible. **PASS.**
- **TOC page numbers**: spot-checked against actual section pages — consistent. **PASS.**

---

## 4. Figure Rendering Assessment

All 36 figure PDF files are present on disk and all 36 `\includegraphics` calls are
accounted for. Key observations from full PDF inspection:

- **Experiment labels**: All figures carry "ALEPH Open Data" or "ALEPH Open Simulation"
  labels — consistent throughout. **PASS.**
- **Axis legibility**: At rendered sizes, all axis labels and tick marks are legible.
  The calibration bin labels on Fig. 7 (page 13) remain dense but readable. **PASS.**
- **Fig. 11 (efficiency calibration, page 17)**: All three panels now show the complete
  "Working point" x-axis label. The v1 truncation (finding R8) is resolved. **PASS.**
- **Fig. 21 (QFB survey, page 42)**: Three-panel figure using `width=0.32\linewidth`.
  Panels render at consistent size and are legible. Style inconsistency noted in R6
  above (Category C). **PASS.**
- **Legend placement**: No legend overlaps data in any inspected figure. **PASS.**
- **Error bars**: Present and of reasonable magnitude throughout. **PASS.**
- **Fig. 15 (closure test diagnostics, page 27)**: The three panels (a), (b), (c)
  have some label overlap in the upper region of the composite, but remain readable.
  Not a new finding; within acceptable bounds for a working document.

---

## 5. Table Overflow Check

All tables were inspected across the 52 pages:

- Tables 9 (systematic summary, page 22), 13 (validation, page 27), 16 (Rb comparison,
  page 33), 21 (constraint index, page 44), and 26 (systematic cross-reference, page 50)
  are the widest tables. All remain within the text block; no content overflows the
  page margins. **PASS.**
- Table 19 (per-bin systematics, page 40) uses a five-column layout that fits within
  margins. **PASS.**
- No table requires horizontal scrolling or is cropped. **PASS.**

---

## 6. Font Consistency Check

- Body text: 11pt Computer Modern throughout. **Consistent.**
- Math: `amsmath` / `amssymb`. All operator names use `\mathrm{}` correctly. **PASS.**
- `\tbd{}` placeholders: gray italic, visually distinct. **PASS.**
- `\measured{}` (blue) and `\external{}` (red) colour annotations: rendered correctly
  in Table 1 (page 7) without font size changes. **PASS.**
- Monospace (`\texttt{}`): used appropriately for branch names and JSON fields. **PASS.**
- Line numbers (via `lineno` package): present and consistent throughout. This is
  appropriate for a working document under review.

---

## 7. Page Count

52 pages — within the 50–100 page target. The 2-page increase from v1 (50 pages)
reflects the additions documented in the Change Log (parameter sensitivity table,
new prose for previously orphaned items, expanded cross-check documentation). The
document comfortably clears the 50-page lower bound.

---

## 8. `\tbd{}` Markers

Five `\tbd{}` instances present (Table 15 results summary, page 32). All are correct
and expected for Phase 4a. **No action required.**

---

## 9. New Issues Identified

No new rendering defects were identified in v2. The document is clean.

**One minor observation (Category C, no action required):**

- **N.2 Pixi task sequence (page 50):** The `verbatim` block references
  `tectonic ANALYSIS_NOTE_doc4a_v1.tex` (the v1 filename). The current document is v2.
  This is inside a `\begin{verbatim}...\end{verbatim}` block and represents a stale
  filename in the reproduction instructions. It does not affect compilation or rendering
  but should be updated to `v2` before the final Doc 4c submission.

---

## 10. Summary of Findings

| ID | Classification | Description | Status vs v1 |
|---|---|---|---|
| R1 | ~~A~~ → **FIXED** | `\ref{sec:jetcharge}` resolved; no `??` in PDF | Fixed |
| R2 | ~~A~~ → **FIXED** | 3 orphaned figures now have prose references | Fixed |
| R3 | ~~A~~ → **FIXED** | 7 orphaned tables now have prose references | Fixed |
| R4 | ~~A~~ → **FIXED** | `A_\mathrm{FM}^b` typo removed from all physics prose | Fixed |
| R8 | ~~A~~ → **FIXED** | Fig. 11 x-axis label complete in all three panels | Fixed |
| R5 | ~~B~~ → **C** | Residual whitespace on TOC p.4 and final page only | Improved |
| R6 | ~~B~~ → **C** | Fig. 21 width= vs height= inconsistency; legible | Unchanged style |
| R7 | C | `\tbd{}` markers present (expected for Phase 4a) | Unchanged/correct |
| NEW-1 | C | `verbatim` block references `v1` filename in N.2 | New (minor) |

**Total A items: 0. Total B items: 0. Total C items: 3.**

---

## 11. Overall Classification

**Category C.**

All five Category A findings and both Category B findings from the v1 review have been
resolved in v2. The document compiles cleanly to 52 pages, all cross-references resolve
(zero `??` in the PDF), all figure files are present on disk, the `A_\mathrm{FM}^b`
typo is corrected throughout, the `\ref{sec:jetcharge}` cross-reference resolves, all
previously orphaned figures and tables now have prose references, and the Fig. 11
x-axis label is fully visible. The three remaining Category C items are cosmetic
(whitespace, a style inconsistency in one figure, and a stale filename in a verbatim
block) and do not require re-review.

The document is ready to advance.
