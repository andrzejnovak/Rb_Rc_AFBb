# Combined Validation Report: Doc 4c FINAL
## Plot Validator + Rendering Reviewer + BibTeX Validator

**Session:** helga_6fa6  
**Document:** `analysis_note/ANALYSIS_NOTE_doc4c_v2.pdf/.tex`  
**BibTeX:** `references.bib`  
**Date validated:** 2026-04-03  

---

## CLASSIFICATION: B

The document compiles and renders correctly. All 45 referenced figures exist on disk and are
included without rendering errors. All 11 citation keys used in the text resolve in the BibTeX
file. There are no `\tbd{}` placeholders remaining. However, four Category A/B issues were
identified that must be resolved before final acceptance.

---

## Summary of Findings

### FINDING 1 — Category A: ATLAS experiment label on three figures

**Severity:** A (must resolve — this is a publication-blocking factual error)

**Figures affected:**
- `figures/efficiency_calibration.pdf` (Fig. 5, p. 13) — shows label **"ATLAS"** and luminosity
  string **"ALEPH 10% fb⁻¹ (13 TeV)"**
- `figures/F4b_fd_vs_fs_10pct.pdf` (Fig. 28, p. 38) — shows label **"ATLAS"** and luminosity
  string **"ALEPH 10% fb⁻¹ (13 TeV)"**
- `figures/bdt_calibrated_rb.pdf` (Fig. 16, p. 26) — shows label **"ATLAS"** and luminosity
  string **"ALEPH 10% fb⁻¹ (1.5 TeV)"**

The figures appear to have been produced with an `mplhep` style that defaulted to ATLAS styling.
The correct label is **"ALEPH Open Data"** and the energy string should be **"√s = 91.2 GeV"**
(as used correctly on all other figures in this document). The 13 TeV and 1.5 TeV strings are
also completely wrong for a LEP Z-pole measurement.

A fourth figure, `figures/F5b_systematic_breakdown_10pct.pdf` (Fig. 10, p. 21), shows the
label **"ATLAS"** as well with the luminosity string **"ALEPH 10% fb⁻¹ (13 TeV)"**.

**Required fix:** Regenerate all four figures with the correct experiment label
(`exp_label("ALEPH Open Data")` and `lumi_label("", "√s = 91.2 GeV")`). This is a
cosmetic plotting-script fix; the physics content of the figures is correct.

---

### FINDING 2 — Category A: Broken cross-reference `\cref{sec:extraction:sf}` renders as ??

**Severity:** A (undefined label produces a literal "??" in the PDF)

**Location:** Section 7.8.2 "SF-calibrated BDT 3-tag extraction", line 626 in the PDF (p. 25):
> "The same tag-rate scale factor (SF) approach used for the cut-based tagger (**??**) is
> applied to the BDT."

The label `sec:extraction:sf` does not exist in the document. The SF calibration method is
described in Section 5.2 with label `sec:corrections:smearing`. The correct fix is to change
`\cref{sec:extraction:sf}` to `\cref{sec:corrections:smearing}` in the TeX source (line 1732).

---

### FINDING 3 — Category B: Reproduction Contract cites stale filename

**Severity:** B (incorrect information in the reproduction instructions)

**Location:** Appendix X "Reproduction Contract" (lines 4072–4076 in TeX):

```
tectonic analysis_note/ANALYSIS_NOTE_doc4b_v5.tex
```

This should read `ANALYSIS_NOTE_doc4c_v2.tex` — the current document. The v5 file refers to
a superseded version. A reader following these instructions to reproduce the document would
compile the wrong file.

---

### FINDING 4 — Category B: Multiple BibTeX entries missing journal/volume/pages fields

**Severity:** B (incomplete references; several key papers lack full bibliographic details)

The following used citation keys have incomplete BibTeX entries:

| Key | Missing fields |
|-----|----------------|
| `ALEPH:Rb:1996` | volume, pages |
| `ALEPH:Rb:precise` | volume, pages |
| `ALEPH:AFBb` | journal, volume, pages |
| `LEP:HF:2001` | journal, volume, pages |
| `ALEPH:sigma_had` | journal, volume, pages |
| `DELPHI:Rb` | journal, volume, pages |
| `ALEPH:gbb` | journal, volume, pages |
| `LEP:gcc` | journal, volume, pages |
| `PDG:2024` | volume, pages |

Only `LEP:EWWG:2005` and `ALEPH:opendata` (a misc entry) are fully complete. The `note` fields
contain inspire IDs and arXiv eprints, which is useful, but standard journal fields are expected
for a physics analysis note. The `PDG:2024` entry cites the correct review but lacks the volume
(110) and the article number / pages.

**Required fix:** Add journal, volume, and pages fields to each entry. Minimum acceptable for
journal articles: journal name, year (present), and one of {eprint, doi, pages}. The eprint
fields on `ALEPH:Rb:1996` (`hep-ex/9609005`), `ALEPH:gbb` (`hep-ex/9811047`), and
`LEP:EWWG:2005` are present and sufficient as identifiers; the missing-journal entries
(`ALEPH:AFBb`, `LEP:HF:2001`, `ALEPH:sigma_had`, `DELPHI:Rb`, `LEP:gcc`) should at minimum
have the journal name added.

---

## Checks That PASSED

| Check | Result |
|-------|--------|
| PDF compiles without errors | PASS — document renders fully, 56 pages |
| All 45 referenced figures exist on disk | PASS — all files confirmed present and non-zero |
| No missing figure files | PASS |
| No `\tbd{}` placeholders remaining | PASS — changelog notes all replaced; none found in body |
| No bare Phase 4a/4b/4c references in body text | PASS — only appears in changelog and one figure filename in caption which is acceptable |
| All 11 used citation keys resolve in references.bib | PASS |
| No undefined citation keys (`\cite{?}`) | PASS |
| Experiment label "ALEPH Open Data" on most figures | PASS for 41 of 45 figures; FAIL on 4 figures (Finding 1) |
| Energy label √s = 91.2 GeV on most figures | PASS for 41 of 45 figures; FAIL on 4 figures (Finding 1) |
| Table of contents renders correctly | PASS |
| Mathematics and equations render without errors | PASS |
| Colored provenance markers (blue/red) render | PASS |
| Boxed result equations render | PASS |
| Hyperlinks and cross-references (except Finding 2) | PASS for all except sec:extraction:sf |
| Author field ("JFC Autonomous Analysis Framework") | NOTE — this is a workflow artifact in the author field; acceptable for an internal analysis note but should be noted |
| "Powered by Claude Code" in date field | NOTE — workflow artifact; acceptable for internal note |
| No ATLAS labels in figure captions or body text | PASS (text); FAIL in figure files (Finding 1) |
| Figure axis labels present and readable | PASS on all figures inspected |
| Figure legends present | PASS on all figures inspected |
| No duplicate `\label` in document | PASS |
| BibTeX file parses without structural errors | PASS — all entries syntactically valid |
| References section renders (bibliography present) | PASS |

---

## Detailed Figure Audit (Selected)

Figures inspected directly from the PDF:

- **Fig. 2** (`sigma_d0_calibration`): "ALEPH Open Data", √s = 91.2 GeV. Axis labels correct
  ("Calibration bin index", "σ_d0 scale factor"). Data/MC legend present. PASS.
- **Fig. 3** (`d0_sign_validation`): "ALEPH Open Data", √s = 91.2 GeV. Y-axis correctly labeled
  as asymmetry. Legend shows b-enriched vs. all events. Gate result "PASS" shown in box. PASS.
- **Fig. 4** (`data_mc_combined_tag`): "ALEPH Open Data". Combined tag distribution with pull
  panel. Axis label: "Combined tag -ln P_hem + mass bonus". PASS.
- **Fig. 5** (`efficiency_calibration`): **FAIL — ATLAS label, 13 TeV** (Finding 1).
- **Fig. 6** (`rb_operating_scan`): "ALEPH Open Data", √s = 91.2 GeV. Y-axis "Extracted R_b".
  Reference lines for SM and ALEPH published value shown. PASS.
- **Fig. 10** (`F5b_systematic_breakdown_10pct`): **FAIL — ATLAS label, 13 TeV** (Finding 1).
- **Fig. 11** (`closure_mirrored`): "ALEPH Open Data". Bar chart, correct label and axis. PASS.
- **Fig. 12** (`closure_bflag`): "ALEPH Open Data". χ²/ndf = 11,447 shown in legend. PASS.
- **Fig. 13** (`closure_contamination`): "ALEPH Open Data". Bar chart. PASS.
- **Fig. 14** (`S2b_hemisphere_charge`): "ALEPH Open Data", four-panel Q_FB distributions.
  Four κ values labeled. PASS.
- **Fig. 15** (`F7b_kappa_consistency`): "ALEPH Open Data". AFBb vs κ, reference lines shown.
  PASS.
- **Fig. 16** (`bdt_calibrated_rb`): **FAIL — ATLAS label, 1.5 TeV** (Finding 1).
- **Fig. 22** (`S1b_tag_fractions`): "ALEPH Open Data". Single-tag fraction comparison. PASS.
- **Fig. 23** (`rb_3tag_stability_fulldata`): "ALEPH Open Data". R_b vs working point. PASS.
- **Fig. 24** (`calibration_progression`): "ALEPH Open Data". Two-panel progression plot. PASS.
- **Fig. 25** (`afb_kappa_fulldata`): "ALEPH Open Data", √s = 91.2 GeV. AFBb vs κ. PASS.
- **Fig. 26** (`per_year_consistency`): "ALEPH Open Data". Two-panel per-year R_b and AFBb. PASS.
- **Fig. 27** (`systematics_breakdown_fulldata`): "ALEPH Open Data". Two-panel bar chart. PASS.
- **Fig. 28** (`F4b_fd_vs_fs`): **FAIL — ATLAS label, 13 TeV** (Finding 1).

---

## Numerical Consistency Spot-Checks

Values in abstract, boxed equations, and summary tables are internally consistent:

- Abstract: R_b = 0.21236 ± 0.00010 (stat) ± 0.027 (syst), χ²/ndf = 4.4/14, p = 0.99 —
  matches Table 13 (p. 32) and Eq. 23/25.
- Abstract: A_FB^b = +0.0025 ± 0.0026 (stat) ± 0.0021 (syst) — matches Table 14 (p. 34)
  and Eq. 26.
- Conclusions: all numbers match the Results section.
- Per-year table (Table 15): R_b range 0.186--0.189, χ²/ndf = 3.57/3 — matches text.
- Change log claims "stability χ²/ndf = 4.4/14" — matches body.
- 10% result R_b = 0.212 ± 0.001 ± 0.015 — matches Table 5 and Eq. 18.

No numerical inconsistencies found between abstract, body, tables, and conclusions.

---

## Resolution Required Before PASS

| # | Finding | Severity | Fix |
|---|---------|----------|-----|
| 1 | ATLAS labels on 4 figures (efficiency_calibration, F4b_fd_vs_fs_10pct, bdt_calibrated_rb, F5b_systematic_breakdown_10pct) | A | Regenerate figures with `exp_label("ALEPH Open Data")` and correct energy string |
| 2 | `\cref{sec:extraction:sf}` renders as ?? (Section 7.8.2) | A | Change to `\cref{sec:corrections:smearing}` |
| 3 | Reproduction Contract cites `ANALYSIS_NOTE_doc4b_v5.tex` | B | Update to `ANALYSIS_NOTE_doc4c_v2.tex` |
| 4 | BibTeX entries missing journal/volume/pages for 9 of 11 used keys | B | Add journal names at minimum; add volume/pages where available |
