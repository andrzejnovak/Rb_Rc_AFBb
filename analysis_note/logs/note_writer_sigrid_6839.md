# Session Log: note_writer_sigrid_6839

## Task
Update the rewritten AN (v6) with 10% data results.
Create doc4b_v5.tex from doc4a_v6.tex.

## Date
2026-04-03

## Key Finding
The Doc 4a v6 document already contained all 10% data validation results
integrated throughout its body text, tables, and figures. The v6 rewrite
(from the REGRESS(4a) cycle) incorporated the 10% data results directly
rather than using \tbd{} placeholders for them. This means the Doc 4b
promotion required only metadata and provenance updates, not content changes.

## What Was Done
1. Copied `ANALYSIS_NOTE_doc4a_v6.tex` to `ANALYSIS_NOTE_doc4b_v5.tex`
2. Updated the file header comment to identify as Doc 4b v5 with JSON source provenance
3. Added a Doc 4b v5 change log entry documenting:
   - Promotion from Doc 4a v6
   - All numerical values sourced from parameters.json and Phase 4b JSONs
   - Figures F1b-F7b, S1b, S2b included
   - Calibration progression documented
   - \tbd{} placeholders retained only for Doc 4c (full data)
4. Updated the reproduction contract to reference the correct filename
5. Compiled successfully with tectonic (1.33 MiB PDF, 6 passes)

## Verified Content Already Present in v6
- Abstract: R_b = 0.212 +/- 0.001 +/- 0.015, A_FB^b = 0.074 +/- 0.031
- Calibration progression: 0.163 -> 0.199 -> 0.212 (Sec 5.2, App H)
- 10% data tables: Tbl 4 (tag fractions), Tbl 5 (R_b calibration), Tbl 6 (AFB per kappa)
- 10% data figures: F1b, F2b, F3b, F4b, F5b, F7b, S1b, S2b
- Systematic budgets: Tbl 3 (AFB syst), Tbl 4 (R_b syst)
- All 15 WP stability results in App F
- Per-kappa AFB results in App I
- Comparison tables with published values

## Remaining \tbd{} Placeholders (for Doc 4c)
- Results summary table: full-data R_b and A_FB^b rows
- Conclusions: paragraph about full data expectations

## Output Files
- `analysis_note/ANALYSIS_NOTE_doc4b_v5.tex` (source)
- `analysis_note/ANALYSIS_NOTE_doc4b_v5.pdf` (compiled, 1.33 MiB)
