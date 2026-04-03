# Session Log: note_writer_nora_56c2

Date: 2026-04-03

## Task
Update Doc 4c v1 -> v2 with CORRECTED full-data results from the SF-calibrated re-run.
Fix 6 figures that failed the Haiku swarm.

## Actions

### 1. Copied v1 to v2
- `cp ANALYSIS_NOTE_doc4c_v1.tex -> ANALYSIS_NOTE_doc4c_v2.tex`

### 2. Updated all numerical results (CORRECTED values)

**R_b** (was: 0.190 +/- 0.0001 stat +/- 0.018 syst, 8-config combined, stability FAIL):
- Now: 0.21236 +/- 0.00010 stat +/- 0.027 syst, 15-config combined, C_b=1.0
- Stability: chi2/ndf = 4.4/14 (p=0.99) -- PASS
- Best single WP (tight=8, loose=4): 0.21226 +/- 0.00036
- Source: `rb_fulldata_corrected.json` -> stability section

**A_FB^b** (was: +0.0005 +/- 0.0005, inclusive method):
- Now: +0.0025 +/- 0.0026 stat +/- 0.0021 syst, purity-corrected (no charm)
- At kappa=2.0: +0.014 +/- 0.005
- Per-kappa: 0.3->-0.009, 0.5->-0.005, 1.0->+0.005, 2.0->+0.014
- Source: `afb_fulldata_corrected.json` -> combination_primary

**Derived quantities:**
- A_FB^{0,b} = +0.0026 +/- 0.0027
- sin2theta_eff = 0.2495 +/- 0.0005

**Systematics (Rb, corrected):**
- eps_c: 0.01717 (was 0.01486)
- eps_uds: 0.00787 (was 0.00937)
- C_b variation: 0.00683 (was 0.00387)
- Total: 0.027 (was 0.01812)

### 3. Sections updated
- Header comment
- Abstract (full rewrite of results paragraph)
- Change log (new v2 entry + archived v1)
- Section 9: R_b results (combined, best WP, final boxed equation)
- Section 9: A_FB^b results (method text, kappa table, combined, kappa=2 boxed)
- Section 9: Derived pole asymmetry and sin2theta
- Section 9: Systematic budget table (Rb total, dominant terms)
- Section 9: AFB systematic discussion
- Section 9: Summary table
- Section 10: Comparison tables (R_b and A_FB)
- Section 10: Precision comparison table
- Section 10: Discussion text
- Section 11: Conclusions (all final numbers)
- WP stability table (corrected to 15-config with C_b=1.0)
- All figure captions referencing the old results

### 4. Fixed 6 figures (axis labels)

1. **sigma_d0_calibration** (plot_all.py): Added "dimensionless" to y-axis, "index" to x-axis
2. **closure_mirrored** (plot_all.py): Added x-axis label "Sample type", y-axis "Extracted R_b (dimensionless)"
3. **closure_bflag** (plot_all.py): Added x-axis label, expanded y-axis label, improved legend entries
4. **S2b hemisphere charge** (plot_phase4b.py): Clarified y-axis "Events / bin", x-axis "(momentum-weighted charge)"
5. **F7b kappa consistency** (plot_phase4b.py): Clarified y-axis "(purity-corrected, no charm subtraction)"
6. **closure_test_phase4a** (plot_phase4a.py): Added labels on both panels, proper ylabel on right panel

### 5. Regenerated figures
- `pixi run py phase3_selection/src/plot_all.py` -- 51 figures
- `pixi run py phase4_inference/4b_partial/src/plot_phase4b.py` -- 7 figures
- `pixi run py phase4_inference/4a_expected/src/plot_phase4a.py` -- all figures
- `pixi run py phase4_inference/4c_observed/src/plot_phase4c.py` -- 6 figures
- All regenerated figures copied to `analysis_note/figures/`

### 6. Compiled PDF
- `tectonic ANALYSIS_NOTE_doc4c_v2.tex` -- success
- Output: `ANALYSIS_NOTE_doc4c_v2.pdf` (1.10 MiB)
- Warnings: overfull/underfull hbox (cosmetic), bbl rerun convergence (harmless)

## Verification
- No remaining \tbd{} placeholders
- No remaining uncorrected values (0.190, +0.0005, +0.0027 all replaced or in changelog/appendix context)
- All 6 figure scripts regenerated and staged
- PDF compiles cleanly
