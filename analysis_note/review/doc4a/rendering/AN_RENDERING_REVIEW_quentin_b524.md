# Rendering Review — Doc 4a v1
**Reviewer:** quentin_b524
**Document:** `analysis_note/ANALYSIS_NOTE_doc4a_v1.pdf` / `.tex`
**Date:** 2026-04-03
**Classification:** **B** (one A-borderline item, multiple B items; no hard compilation failures)

---

## 1. Compilation Status

The PDF exists and is 50 pages, meeting the 50-100 page target (lower bound exactly). No compilation errors are in evidence: tectonic produced a complete document. All 36 referenced figure PDF files are present on disk and accounted for.

---

## 2. Findings

### Finding R1 — Unresolved cross-reference `\ref{sec:jetcharge}` renders as `??`
**Classification: A**

**Symptom (PDF page 9, body prose in Sec. 3.2):**
> "However, they ARE included in the jet charge computation (Section **??**), which uses all charged tracks…"

**Root cause:** `.tex` line 383 references `\ref{sec:jetcharge}`. No `\label{sec:jetcharge}` exists anywhere in the document. The jet-charge section is labeled `sec:doubletag` (Sec. 4.4) and `sec:stat_afb` (Sec. 7.2); neither has the key `sec:jetcharge`.

**Fix:** Either add `\label{sec:jetcharge}` to the jet-charge computation subsection (Appendix J, which begins at `.tex` line ~2560 and covers hemisphere charge properties), or change the `\ref` to the correct existing label — most likely `\ref{sec:stat_afb}` or `\ref{sec:afb_bias}`, or to the Appendix J label. The quickest correct fix is to label Appendix J with `\label{sec:jetcharge}` since that is the section that defines $Q_h(\kappa)$ (Eq. 22). Alternatively point to `sec:doubletag` since the context is the double-tag counting method and hemisphere splitting.

---

### Finding R2 — Three orphaned figures (label only, no `\ref` from body prose)
**Classification: A**

The reviewer spec states: "A figure with no incoming reference is an orphan — the reader encounters it with no context." The following figures have `\label` but zero `\ref{}` from any prose:

| Figure | `.tex` label line | Content | Appears on PDF page |
|---|---|---|---|
| Fig. 3 | 435 (`fig:datamc_track`) | Data/MC track $p_T$ and $d_0$ | 11 |
| Fig. 6 | 482 (`fig:p1_d0_trackpt`) | Phase 1 $d_0$ and track $p_T$ | 12 |
| Fig. 10 | 661 (`fig:datamc_tag2`) | Hemisphere invariant mass and signed $d_0/\sigma_{d_0}$ | 15 |

**Root cause:** These are composite figures with a second panel that was split from a referenced figure (Figs. 2, 5, 9 respectively). The splitting created new `\label` entries but the prose `\ref{}` calls were not added.

**Fix:** Add a sentence in the surrounding prose referencing each figure number. For example, after the paragraph ending "…the pull distributions" in Sec. 3.3, add "Figure~\ref{fig:datamc_track} shows the corresponding comparisons for track-level variables." Similarly for Figs. 6 and 10.

---

### Finding R3 — Seven orphaned tables (label only, no `\ref` from body prose)
**Classification: A**

The following tables appear in the document with `\label` but are never referenced by a `\ref{}` from body text (the caption is their only mention):

| Table | `.tex` label line | Content |
|---|---|---|
| Tab. 3 | 291 (`tab:mc_samples`) | Monte Carlo samples |
| Tab. 5 | 391 (`tab:track_cutflow`) | Track selection cutflow |
| Tab. 11 | 1348 (`tab:corrupted_corrections`) | Corrupted-correction sensitivity |
| Tab. 17 | 1820 (`tab:sin2theta_comparison`) | $\sin^2\theta_\mathrm{eff}^\mathrm{lept}$ comparison |
| Tab. 21 | 2515 (`tab:weight_impact`) | Track weight impact on $Q_\mathrm{FB}$ |
| Tab. 22 | 2573 (`tab:hemisphere_charge_properties`) | Hemisphere charge properties |
| Tab. 24 | 2654 (`tab:nsigma_fractions`) | N-sigma tag fractions |

**Root cause:** Tables were introduced during drafting but the `\ref{}` calls in surrounding prose were omitted.

**Fix:** Add `Table~\ref{tab:...}` calls in the relevant prose for each table. Several of these already have prose that describes the content; the fix is inserting the reference sentence. For example, Sec. 6.6.3 (corrupted corrections) describes the results but directs the reader to "Figure~\ref{fig:p3_closure}" without referencing Tab. 11. Similarly, Sec. 9.6 on $\sin^2\theta_\mathrm{eff}^\mathrm{lept}$ comparison lacks a `\ref` to Tab. 17.

---

### Finding R4 — Typo `A_\mathrm{FM}^b` instead of `A_\mathrm{FB}^b` (3 occurrences)
**Classification: A**

**Symptom (PDF):** On PDF pages 6 (Intro para. 4), 32 (Conclusions), and 38 (Appendix B.2), the notation $A_\mathrm{FM}^b$ appears where $A_\mathrm{FB}^b$ is clearly intended. The subscript "FM" is not physics notation; "FB" (forward-backward) is correct.

**Root cause:** `.tex` lines 143, 1845, and 2215 contain `$A_\mathrm{FM}^b$`. This is a transcription error; no other instance of "FM" asymmetry notation exists in the document.

**Fix:** Replace all three occurrences of `\mathrm{FM}` with `\mathrm{FB}` in these lines.

---

### Finding R5 — Large whitespace gaps on multiple pages
**Classification: B**

The following pages show blank space exceeding 1/3 of the page, which a journal referee would notice:

- **PDF page 4 (TOC continuation):** Table of contents ends at approximately 60% of the page. The remaining ~40% is blank. This arises because `\clearpage` is issued after the TOC and the TOC itself is short. Acceptable for a working document but visually poor.
- **PDF page 5 (Change Log):** The Change Log section occupies ~1/4 of the page with ~3/4 blank. The `\clearpage` before Sec. 1 leaves a near-empty page.
- **PDF page 12 (Sec. 3.4–3.5):** A large vertical gap (~1/3 page) appears between Figs. 4 and 5 (Phase 1 composite figures). This arises from float placement with `height=0.38\linewidth` panels that do not fill the page efficiently.
- **PDF page 14 (Sec. 4.2):** A large gap appears below Fig. 8 before Sec. 4.3 begins. Float placement leaves ~40% of page blank.
- **PDF page 36 (Sec. 12.6):** Section body occupies ~1/4 of the page with the rest blank before the References section on page 37.

**Root cause:** Aggressive `\FloatBarrier` and `\clearpage` usage combined with `height=0.45\linewidth` figures forces floats to consume full pages even when content is sparse. The `\needspace{4\baselineskip}` calls before each section heading prevent sections from starting near the bottom but can push content too aggressively.

**Fix:** Consolidate the Change Log onto the TOC page (remove the `\clearpage` between TOC and Change Log, or move Change Log before TOC). For the large gaps within sections, consider using `\begin{figure}[h]` instead of `[htbp]` where flow is important, or use `\vspace{}` to reduce the gap attractively rather than having it uncontrolled.

---

### Finding R6 — Inconsistent figure sizing in composite panels
**Classification: B**

The document mixes two sizing conventions for composite (multi-panel) figures:
- Most composites use `height=0.38\linewidth` (`.tex` lines 411–413, 427–428, 450–476, 641–655)
- The triple-panel Fig. 21 (QFB survey, Appendix D.2) uses `width=0.32\linewidth` (`.tex` lines 2329–2331), inconsistent with the height-based convention specified in the preamble

Additionally, the preamble sets a global default of `height=0.45\linewidth` via `\setkeys{Gin}{}`, but composite panels override to `height=0.38\linewidth` — this is correct for side-by-side layout but should be documented.

**Root cause:** The triple-panel uses `width=` instead of `height=`, likely because the author wanted equal-width columns for a 3-panel row. At `width=0.32\linewidth`, panels that are taller than wide appear squished vertically.

**Fix (recommendation):** Change the triple-panel to `height=0.30\linewidth` with `keepaspectratio` to match the height-based convention. The three panels will naturally fit side-by-side.

---

### Finding R7 — `\tbd{}` markers present and visible (expected, Phase 4a)
**Classification: C (informational)**

Five `\tbd{}` placeholders appear in Table 14 (Results summary, PDF page 29) for 10% data and full data columns. These render correctly as gray italic text (e.g., "*Doc 4b*", "*Doc 4c*") and are appropriate for Phase 4a. No action required. They are clearly distinguishable from surrounding content.

---

## 3. Cross-Reference Completeness Check

All `\ref{sec:...}` calls were checked against defined `\label{sec:...}` entries:
- **Resolved:** All `\ref{sec:...}` calls except `sec:jetcharge` resolve (see Finding R1)
- **`\ref{sec:precision_investigation}`** resolves to Appendix F (line 2426) — correct
- **`\ref{sec:afb_bias}`** resolves to Sec. 7.3 (line 1459) — correct

All `\ref{eq:...}` calls observed in the PDF text (Eqs. 7–8, 11, 13) are defined. All `\cite{...}` keys in the `.tex` match entries in `../references.bib`. No unresolved citations (`[?]`) are visible in the rendered bibliography.

---

## 4. Figure Rendering Assessment

All 36 figure PDF files are present on disk. Reading the rendered figures from the PDF:

- **Experiment label:** All figures carry "ALEPH Open Data" or "ALEPH Open Simulation" labels — consistent and correct
- **Axis legibility:** At the rendered sizes (~0.45 linewidth for standalone, ~0.38 for composites), axis labels and tick marks are legible. The calibration bin labels on the x-axis of Fig. 7 (sigma_d0 calibration, PDF page 14) are dense (40 bins compressed to ~0.45 linewidth) but still readable.
- **Legend placement:** Legends do not overlap data points in any inspected figure
- **Error bars:** Error bars are of reasonable magnitude; the systematic breakdown (Fig. 13) correctly uses a log-x axis to display the range
- **Physics content (rendering flag only):** The closure test Fig. 15 (PDF page 25) correctly labels panels (a), (b), (c) but the panel separation is visually tight — readable but borderline. No figures show obviously wrong physics content from a rendering perspective.
- **Fig. 11 (efficiency calibration, PDF page 17):** The third panel ($\varepsilon_\mathrm{uds}$ vs working point) has its x-axis label cut off at "W" — the full label "Working point" does not appear. This is a figure-file rendering issue.

### Finding R8 — Truncated x-axis label in Fig. 11 right panel
**Classification: A**

**Symptom (PDF page 17, Fig. 11 rightmost panel):** The x-axis label shows only "W" rather than "Working point". The other two panels show the complete "Working point" label.

**Root cause:** The figure source file `efficiency_calibration.pdf` was generated with the third panel's x-axis label clipped, likely due to the subplot layout leaving insufficient space for the full label. Since the figure is an external PDF embedded via `\includegraphics`, the fix must be in the figure generation script, not the `.tex`.

**Fix:** Regenerate `efficiency_calibration.pdf` with sufficient bottom margin or use `tight_layout()` / `bbox_inches="tight"` in the figure generation script to ensure all axis labels are fully visible.

---

## 5. Page Count

50 pages — exactly at the lower bound of the 50-100 page target. Acceptable for Phase 4a (an intermediate deliverable). The appendices are substantive and contribute positively. The large whitespace gaps noted in Finding R5 artificially inflate the page count; compressing them would reduce to ~46 pages and push below the threshold. The note writer should verify that compressing whitespace does not drop below 50 pages.

---

## 6. Summary of Findings

| ID | Classification | Description |
|---|---|---|
| R1 | **A** | Unresolved `\ref{sec:jetcharge}` renders as `??` on PDF p. 9 |
| R2 | **A** | 3 orphaned figures (Figs. 3, 6, 10) — no `\ref` from prose |
| R3 | **A** | 7 orphaned tables (Tabs. 3, 5, 11, 17, 21, 22, 24) — no `\ref` from prose |
| R4 | **A** | Typo `A_\mathrm{FM}^b` appears 3 times (lines 143, 1845, 2215) |
| R8 | **A** | Truncated x-axis label ("W" only) in Fig. 11 right panel |
| R5 | **B** | Large whitespace gaps on pages 4, 5, 12, 14, 36 |
| R6 | **B** | Inconsistent figure sizing convention (width= vs height=) in Fig. 21 |
| R7 | **C** | `\tbd{}` markers present (expected and correct for Phase 4a) |

**Total A items: 5. Total B items: 2. Total C items: 1.**

---

## 7. Overall Classification

**Category B.**

The document compiles successfully, all figure files are present, the bibliography is complete, and the physics content is rendered clearly. However, five Category A rendering defects are present: one unresolved cross-reference (`??` visible to a reader), four orphaned items (3 figures + 7 tables not referenced from prose), three instances of a typo in a key observable name, and one truncated axis label. These must be resolved before the document proceeds to final review. None require rerunning analysis code; all are text or figure-regeneration fixes.

The PDF meets the minimum page count (50 pages exactly) and the `\tbd{}` placeholders are correctly rendered for Phase 4a.
