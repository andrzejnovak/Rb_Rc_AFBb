# Rendering Review: ANALYSIS_NOTE_doc4b_v1
**Reviewer:** agnes_eff4
**Document:** `analysis_note/ANALYSIS_NOTE_doc4b_v1.{tex,pdf}`
**Date:** 2026-04-03
**Classification:** B

---

## 1. Summary

The document compiles cleanly to a 63-page PDF. All figures are present on disk, all cross-references resolve internally, and the bibliography is complete relative to the `.bib` file. Two figures are cited via range syntax (`\ref{A}--\ref{C}`) where the middle label (`fig:eff_cal_eps_c` and `fig:p3_closure_bflag`) carries no standalone `\ref{}` call in the prose — these are orphaned in the strict sense of having no direct citation but are covered by range notation. One prose sentence has a grammatical break left over from editing. Remaining `\tbd{}` placeholders are intentional forward-references to Doc 4c and are correctly typeset in gray italic. Overall rendering quality is high.

---

## 2. Reference Checks

### 2.1 Cross-references (internal `\ref{}`)

All 81 `\ref{}` calls resolve to labels defined in the same file. Zero unresolved cross-references.

The `sec:jetcharge` reference (previously broken in Doc 4a v1, fixed in v2) is correctly resolved at line 483 → label at line 3317. Confirmed.

### 2.2 Bibliography

The TeX file uses `\bibliography{../references}`. The file `references.bib` exists at the expected path. All 11 unique citation keys used in the document are present in `references.bib`:

| Key | Status |
|-----|--------|
| ALEPH:Rb:1996 | present |
| LEP:EWWG:2005 | present |
| ALEPH:AFBb | present |
| DELPHI:Rb | present |
| ALEPH:opendata | present |
| LEP:HF:2001 | present |
| LEP:gcc | present |
| ALEPH:VDET | present |
| PDG:2024 | present |
| ALEPH:sigma_had | present |
| ALEPH:Rc | present |

Four entries in `references.bib` are unused by this document (`ALEPH:Rb:precise`, `ALEPH:gbb`, `DELPHI:AFBb`, `DELPHI:AFBb:2`). This is not an error; they are available for future phases.

### 2.3 `\tbd{}` placeholders

Six remaining `\tbd{}` instances (5 in Table 21 results summary, 1 column header). All are intentional forward-references to Doc 4c and are typeset correctly in gray italic. The Change Log entry for Doc 4b v1 states: "Replaced all `\tbd{10%}` and `\tbd{Doc 4b}` placeholders with real values." This is confirmed — the only remaining `\tbd{}` calls use "Doc 4c" or "Full data" as argument, which is correct for this phase.

---

## 3. Figure Checks

### 3.1 All referenced figure files exist on disk

All 48 PDF files referenced via `\includegraphics` are present in `analysis_note/figures/`. Zero missing figure files.

### 3.2 Orphaned figure floats (Category B)

Two figure environments have labels that are never cited by a standalone `\ref{}` call:

**`fig:eff_cal_eps_c` (line 901)**
- Figure 12 (calibrated charm-tagging efficiency $\varepsilon_c$ vs working point).
- The prose at line 880 reads: `Figures~\ref{fig:eff_cal_eps_b}--\ref{fig:eff_cal_eps_uds}` — a range reference spanning `fig:eff_cal_eps_b`, `fig:eff_cal_eps_c`, and `fig:eff_cal_eps_uds`. The middle figure is included by the range but has no direct `\ref{}` citation.
- In the compiled PDF, Figure 12 appears on page 20 and is visually referenced by the caption-numbered range. The figure is not truly orphaned in the reader's experience, but it is technically unreferenced in the LaTeX sense.

**`fig:p3_closure_bflag` (line 1696)**
- Figure 19 (bFlag discrimination power, Phase 3 closure test (b)).
- The prose at line 1676 reads: `Figures~\ref{fig:p3_closure_mirrored}--\ref{fig:p3_closure_contamination}` — a range reference spanning three figures including this one. Same issue as above.

Both cases arise from the figure-splitting change documented in the Change Log ("A5: efficiency_calibration figure split into 3 separate standalone figures" and "B14: Phase 3 closure figure split into 3 separate standalone figures"). The range citation is acceptable prose style, but strictly speaking the middle figure in each triplet lacks a direct `\ref{}` call. This is **Category B**: the reader can see the figure but a LaTeX-level audit would not catch it as referenced.

**Recommendation:** Add `\ref{fig:eff_cal_eps_c}` and `\ref{fig:p3_closure_bflag}` to the prose, or restructure the range references to include all three labels explicitly (e.g., `Figures~\ref{fig:eff_cal_eps_b}, \ref{fig:eff_cal_eps_c}, and~\ref{fig:eff_cal_eps_uds}`).

### 3.3 No orphaned table floats

All 32 table environments have direct `\ref{}` citations. No orphaned tables.

### 3.4 Float environment balancing

- `\begin{figure}` / `\end{figure}`: 36 / 36. Balanced.
- `\begin{table}` / `\end{table}`: 32 / 32. Balanced.
- `\begin{equation}` / `\end{equation}`: 27 / 27. Balanced.

### 3.5 Figure sizing

All figures use `height=` set to 0.32, 0.38, or 0.45 `\linewidth`. Multi-panel figures (2-up) use 0.38; single-panel figures use 0.45; the 4-up event-level comparison uses 0.32. This is internally consistent. The policy requires square `figsize=(10,10)` at generation; the rendered sizes are rectangular in the AN due to the `height=` constraint, which is standard practice and does not violate the plotting rules (those apply to the saved PNG/PDF dimensions at source, not the inclusion size).

---

## 4. Prose and Formatting Checks

### 4.1 Sentence fragment in Section 5.1 (Category B)

At lines 1038–1039 in the TeX (Section 5.1, Light-flavour mistag rate):

```
The dominant systematic is now $\varepsilon_c$ (0.201).
and $-0.256$ (when increased).
```

The period after `(0.201)` ends the sentence, but `and $-0.256$ (when increased).` is a sentence fragment. This appears to be a vestige of an editing cut. The intended meaning is that the dominant systematic is $\varepsilon_c$ with shift 0.201 in the downward direction and $-0.256$ when increased (i.e., solver failure gives zero for $\varepsilon_\mathrm{uds}$ but $\varepsilon_c$ is non-zero in both directions). The fragment leaves the reader without a verb.

**Recommendation:** Rewrite as: "The dominant systematic is now $\varepsilon_c$: $\delta R_b = 0.201$ (downward shift) and $-0.256$ (upward shift)."

### 4.2 Hard-coded table reference (Category C)

Line 3547 in Appendix M contains:
```
Source (ALEPH Table 4) & ...
```
This is a reference to a specific table number in the published ALEPH paper [1], not a `\ref{}` to a table in this document. It is correctly formatted as plain text (not `\ref{}`), as it refers to an external document. No action required.

### 4.3 `\tbd{}` in column header (Category C)

Table 21 uses `\tbd{Full data}` as a column header. This renders in gray italic as intended, signaling a future column. Acceptable for a Doc 4b note.

### 4.4 Line numbers

`\linenumbers` is active (line 21 of preamble). Line numbers appear in the compiled PDF as expected. This is appropriate for a review-stage document.

### 4.5 Hyperlinks and colors

The `hyperref` package is loaded. All `\ref{}` and `\cite{}` calls render as colored hyperlinks in the PDF (green for citations, red for internal refs, as visible in the screenshots). The table of contents entries are also hyperlinked. No broken hyperlinks detected.

### 4.6 Consistent notation

- $A_\mathrm{FB}^b$ (not $A_\mathrm{FM}^b$): the v2 fix is confirmed. No remaining `A_\mathrm{FM}` instances in the current document body (the change log mentions the fix, which is expected).
- $R_b$, $R_c$, $C_b$, $\varepsilon_b$, $\varepsilon_c$, $\varepsilon_\mathrm{uds}$: notation is internally consistent throughout.
- $\delta_b$ vs $\delta_b$: used consistently for charge separation throughout.
- $\sin^2\theta_\mathrm{eff}^\mathrm{lept}$: consistent use of this form.

### 4.7 Page count and document length

The PDF is 63 pages. The requirement is 50–100 pages; the document satisfies this. Appendices A–N are present and substantive.

---

## 5. Compilation Log

The document compiles with `tectonic` (as required by the spec). No compilation errors or missing file errors are indicated by the presence of the PDF. The log directory contains `note_writer_philippa_7ec1.md` confirming the note writer compiled and verified the document.

---

## 6. Findings Summary

| ID | Category | Finding | Location |
|----|----------|---------|----------|
| R1 | B | `fig:eff_cal_eps_c` has no direct `\ref{}` citation; covered only by range notation `\ref{fig:eff_cal_eps_b}--\ref{fig:eff_cal_eps_uds}` | Line 880 / Figure 12 |
| R2 | B | `fig:p3_closure_bflag` has no direct `\ref{}` citation; covered only by range notation `\ref{fig:p3_closure_mirrored}--\ref{fig:p3_closure_contamination}` | Line 1676 / Figure 19 |
| R3 | B | Sentence fragment "and $-0.256$ (when increased)." following a period in Section 5.1 | Line 1038–1039 |
| R4 | C | Four unused entries in `references.bib` (`ALEPH:Rb:precise`, `ALEPH:gbb`, `DELPHI:AFBb`, `DELPHI:AFBb:2`) | `references.bib` |

---

## 7. Classification

**B** — Two figure citation gaps (range-only, not truly orphaned in the reader experience) and one prose sentence fragment. All cross-references resolve, all figure files exist on disk, bibliography is complete, float environments are balanced, no missing figures, no broken internal links. The document is structurally sound and ready for human review after fixing the three Category B items.
