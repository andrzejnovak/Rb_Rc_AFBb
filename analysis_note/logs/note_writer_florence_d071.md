# Session Log: note_writer_florence_d071

**Date:** 2026-04-03
**Task:** Complete rewrite of Analysis Note (Doc 4b v5)

## What was done

Wrote the complete Analysis Note from scratch (not from any previous version),
starting from `conventions/an_template.tex` as the template.

### Key decisions

1. **One coherent story:** The note tells a linear narrative from ALEPH Open Data
   through self-calibrating methods to R_b and A_FB^b results. No workflow
   artifacts, no "Phase 1/2/3/4" language, no internal file references.

2. **Primary methods:**
   - R_b: 3-tag hemisphere counting with SF-corrected efficiencies
   - A_FB^b: Purity-corrected jet charge extraction at kappa=2.0

3. **All numbers from JSON:** Every numerical result comes from
   `analysis_note/results/parameters.json`, `systematics.json`, `validation.json`,
   and the Phase 4b output JSON files.

4. **Provenance markers:** Blue for measured quantities, red for external inputs,
   throughout all equations and tables.

5. **Data years annotated:** Every figure caption specifies the data years
   (1992-1995) and MC year (1994).

### Structure (50 pages)

Main body (13 numbered sections):
- Introduction (with A_e, A_b, sin2theta definitions)
- Data Samples (detector description, data, MC, quality)
- Event Selection (event-level, track-level, primary vertex)
- Tagging Infrastructure (sigma_d0, d0 sign, probability, mass, 3-tag, BDT, jet charge)
- Corrections and Calibration (double-tag, d0 smearing, SF, A_FB^b extraction)
- Systematic Uncertainties (12 sources for R_b, 6 for A_FB^b, with tables)
- Cross-Checks (7 subsections)
- Statistical Method (chi2, toys, GoF)
- Results (expected + 10% data, boxed equations)
- Comparison to Prior Results (tables, precision decomposition)
- Methodology Comparison (tagging, A_FB^b, calibration)
- Conclusions
- Future Directions (6 items)
- Known Limitations (7 items)

Appendices (15 sections):
- Systematic shifts, efficiency tables, cutflow, BDT details, weights,
  auxiliary plots, limitation index, R_b all WPs, d0 smearing details,
  covariance, gluon splitting, exploration figures, hemisphere mass,
  WP optimisation, A_FB^b interpretation, calibration comparison,
  sensitivity, d0 sign validation detail, efficiency algebra,
  figure summary, notation, numerical constants, reproduction contract

### Figures included

29 figures referenced, all from `analysis_note/figures/` directory.
All are PDF format. Includes flagship figures (F1b-F7b series),
supplementary figures (S1b, S2b), data/MC comparisons, closure tests,
and exploration-phase distributions.

### Compilation

Compiled with tectonic. Final PDF: 50 pages, 990 KB.
Minor warnings (overfull hbox, annotation out of page boundary) but no errors.

## Files written

- `analysis_note/ANALYSIS_NOTE_doc4a_v5.tex` (fresh LaTeX source)
- `analysis_note/ANALYSIS_NOTE_doc4a_v5.pdf` (compiled PDF, 50 pages)
- `analysis_note/logs/note_writer_florence_d071.md` (this file)
