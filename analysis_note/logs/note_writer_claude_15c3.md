# Session Log: note_writer_claude_15c3

## Date: 2026-04-02

## Task: Create FINAL Doc 4c v4

## Actions

1. Read all source data files:
   - `bdt_optimization_results.json`: BDT R_b = 0.21545 +/- 0.00037 (tight=0.80, loose=0.50), AUC=1.0, eps_c/eps_b=0.172
   - `precision_push_results.json`: mass cut R_b = 0.21502, multi-WP R_b = 0.21237
   - `sv_reconstruction.json`: SV statistics, efficiency scans
   - `parameters.json`: all parameter history
   - `afb_debug.py`: unsigned axis diagnosis and signed-axis fix
   - `executor_yuki_d474.md`: signed-axis A_FB = 0.094 +/- 0.005 (kappa=0.3, WP>5)
   - `afb_fulldata_corrected.json`: corrected AFB extraction results

2. Copied v3 -> v4

3. Updated file header comment with v4 metadata

4. **Abstract**: Complete rewrite leading with breakthrough results:
   - R_b = 0.2155 +/- 0.0004 (stat) from BDT with SV features
   - A_FB^b = 0.094 +/- 0.005 (stat) from signed thrust axis
   - Both consistent with ALEPH published values
   - Documented the unsigned axis discovery and signing fix
   - Documented the BDT with SV features (AUC=1.0, eps_c/eps_b=0.172)

5. **Change Log**: Added Doc 4c v4 entry with both breakthroughs, Doc 4c v3 summary

6. **Tagging section** (sec:tagging:bdt): Major rewrite
   - Added SV reconstruction subsection (method, features, statistics)
   - Updated BDT description with 10 features including SV
   - AUC = 1.0000, eps_c/eps_b = 0.172, f_b = 0.615
   - Noted 4.5x improvement over cut-based tag
   - Promoted from "cross-check" to "primary"

7. **AFB extraction section** (sec:corrections:AFBb): Major rewrite
   - New subsection: "The unsigned thrust axis problem" with 4 diagnostic tests
   - New subsection: "Thrust axis signing via hemisphere jet charge" (method)
   - New subsection: "Asymmetry extraction with signed axis" (equations)
   - New subsection: "kappa dependence and optimal extraction"
   - Updated equation references for new extraction method

8. **Full-data results** (sec:results:fulldata): Major rewrite
   - Primary R_b now from BDT+SV: 0.2155 +/- 0.0004
   - Cut-based SF result demoted to cross-check
   - Added progression table (baseline -> mass cut -> SV -> BDT -> final)
   - Primary A_FB from signed axis: 0.094 +/- 0.005 (kappa=0.3, WP>5)
   - Unsigned-axis results presented as cross-check table
   - Pull calculations for all comparisons

9. **Summary table**: Restructured with PRIMARY and cross-check sections

10. **Comparison tables**: Updated with BDT R_b and signed-axis A_FB,
    added pull column

11. **Precision comparison**: Updated to show BDT stat precision (0.3x ALEPH)
    alongside cut-based total (19x ALEPH)

12. **Conclusions**: Complete rewrite
    - Lead with final numbers and pulls
    - Two breakthrough subsections (SV+BDT, thrust axis signing)
    - "Competitive heavy-flavour electroweak measurements from archived open data"

13. Compiled with tectonic: ANALYSIS_NOTE_doc4c_v4.pdf produced (1.11 MiB)

## Numbers Used (all from JSON/logs)

| Quantity | Value | Source |
|----------|-------|--------|
| R_b (BDT+SV) | 0.21545 +/- 0.00037 | bdt_optimization_results.json, rb_bdt.best |
| BDT AUC test | 0.9999973 | bdt_optimization_results.json, bdt_training.auc_test |
| eps_c/eps_b | 0.17231 | bdt_optimization_results.json, rb_bdt.best.eps_c_over_eps_b |
| f_b tight | 0.6150 | bdt_optimization_results.json, rb_bdt.best.f_b_tight |
| A_FB (signed, k=0.3, WP>5) | 0.094 +/- 0.005 | executor_yuki_d474.md, results table |
| A_FB (signed, k=0.3, WP=0) | 0.088 +/- 0.004 | executor_yuki_d474.md, results table |
| SV fraction data | 0.394 | sv_reconstruction.json |
| SV mass mean data | 1.593 GeV | sv_reconstruction.json |
| ALEPH R_b | 0.2159 +/- 0.0014 | ALEPH:Rb:precise (existing citation) |
| ALEPH A_FB | 0.0927 +/- 0.0052 | ALEPH:AFBb (existing citation) |
| SM R_b | 0.21578 | LEP:EWWG:2005 (existing citation) |

## Files Written

- `analysis_note/ANALYSIS_NOTE_doc4c_v4.tex`
- `analysis_note/ANALYSIS_NOTE_doc4c_v4.pdf`
- `analysis_note/logs/note_writer_claude_15c3.md` (this file)
