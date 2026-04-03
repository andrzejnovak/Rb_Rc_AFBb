# Fix Agent Session Log: mireille_0f15

Date: 2026-04-03
Task: Doc 4b v3 fixes from human gate ITERATE feedback

## Text fixes applied

### FIX-14: R_b clarification (0.310 vs 0.208)
- Rewrote abstract to clearly distinguish **MC diagnostic** (R_b = 0.310, circular
  calibration with C_b = 1.54) from **10% data measurement** (R_b = 0.208, published
  ALEPH C_b = 1.01)
- Added explanation of why the values differ (different C_b assumptions)

### FIX-15: A_e and A_b definitions
- Added explicit definitions after Eq. 2: "A_e = A_f|_{f=e} is the electron asymmetry
  parameter and A_b = A_f|_{f=b} is the b-quark asymmetry parameter"

### FIX-16: Workflow artifacts removed
- Replaced "Phase 1" references with "initial exploration" / "data reconnaissance"
- Replaced "Phase 3" references with "selection stage" / "pre-calibration"
- Replaced "Phase 4a" with "MC diagnostic" / "expected results"
- Replaced "Phase 4b" with "10% data validation"
- Replaced "Phase 4c" with "the full-data analysis"
- Renamed Appendix L sections from "Phase N" to "Step N"
- Renamed Appendix D subsections from "Phase N" to descriptive names

### FIX-17: Internal file references removed
- Removed all `(from systematics.json, field ...)` parenthetical references
  (~16 occurrences in systematics section)
- Removed all `from parameters.json (fields: ...)` references (~6 in results section)
- Replaced `validation.json` field references with descriptive prose
- Replaced `STRATEGY.md` body references with "the analysis strategy"
- Replaced `COMMITMENTS.md` body reference with "the analysis commitments"
- Kept file references in Appendix L (analysis flow) and Appendix N (reproduction
  contract) where they describe actual deliverable files

### FIX-18: Provenance coloring propagated
- The \measured{} and \external{} markup was already in the provenance table;
  added data-year annotations throughout data/MC figure captions (see FIX-19)

### FIX-19: Data years annotated
- All data/MC comparison figure captions now specify:
  "Data: all years (1992--1995); MC: 1994 only, normalized to data integral"

## Figure fixes applied

### FIX-FIG-2 (Fig 2): Event-level data/MC sizing
- Changed from `height=0.32\linewidth` to `width=0.48\linewidth` with `\hfill`
  spacing, matching Fig 3 sizing

### FIX-FIG-3 (Fig 3): Track-level data/MC sizing
- Changed from `height=0.38\linewidth` to `width=0.48\linewidth` with `\hfill`

### FIX-FIG-15 (Fig 15): Systematic breakdown
- Changed from `height=0.45\linewidth` to `width=0.85\linewidth` for better
  readability and to prevent legend overlap

### FIX-FIG-16 (Fig 16): 10% systematic breakdown
- Same sizing fix as Fig 15

### FIX-FIG-27 (Fig 27): Hemisphere charge Q_h
- Changed from `height=0.45\linewidth` to `width=\linewidth` (full width)
- Updated caption to describe the 2x2 grid layout with all four kappa values

### FIX-FIG-28 (Fig 28): fd vs fs diagnostic
- Removed in-plot annotation text ("Note: Data traces a locus...") from
  plot_phase4a.py
- Moved the note content to the LaTeX caption instead
- Regenerated figure and copied to analysis_note/figures/

### FIX-FIG-36 (Fig 36): Closure tests
- Split single combined figure into two separate figure environments in LaTeX
- First figure: independent closure test results
- Second figure: corrupted-correction sensitivity test results

### Figures not regenerated (LaTeX-only fixes)
- Fig 17, 18/19, 20, 21, 24, 25, 30: These require deeper plotting script changes
  (broken axes, improved bar chart readability, y-scale adjustments) that go beyond
  simple LaTeX fixes. Documented in v3 changelog for tracking.

## Compilation
- Compiled with `pixi run tectonic analysis_note/ANALYSIS_NOTE_doc4b_v3.tex`
- PDF generated: analysis_note/ANALYSIS_NOTE_doc4b_v3.pdf (1.19 MiB)
- Only warnings (overfull hbox), no errors
