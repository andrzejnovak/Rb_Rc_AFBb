# Fixer Session Log — boris_2069

**Date:** 2026-04-03
**Input:** AN_ARBITER_ada_0141.md (5A + 9B + 8C)
**Output:** ANALYSIS_NOTE_doc4c_v3.tex + v3.pdf

## Fixes Applied

### Category A (Must Resolve)

| # | Fix | Evidence |
|---|-----|----------|
| A1 | Regenerated 4 figures (efficiency_calibration.pdf, F4b_fd_vs_fs_10pct.pdf, bdt_calibrated_rb.pdf, F5b_systematic_breakdown_10pct.pdf) with `hep.label.exp_label(exp="ALEPH", ...)` replacing `hep.atlas.label()` | Ran pixi run py on regen_figures_v6.py and bdt_calibrated_extraction.py |
| A2/A3 | Added per-year table caption clarifying: single-config raw MC efficiencies (not SF-calibrated), inclusive slope/delta_b without purity correction; negative AFB reflects charm dilution | Table caption at tbl:per_year_fulldata |
| A4 | Updated systematics.json phase_4c_fulldata: rb_total_syst 0.018 -> 0.027; afb_total_syst 0.019 -> 0.0021; eps_c, eps_uds, C_b delta_Rb values updated to match AN Table 16 | systematics.json |
| A5 | Fixed \cref{sec:extraction:sf} -> \cref{sec:corrections:smearing} (line ~1732) | No ?? in compiled PDF |

### Category B (Must Fix Before PASS)

| # | Fix | Evidence |
|---|-----|----------|
| B1 | Covariance matrix eq. 30: V_11 updated from (0.015)^2 to (0.027)^2, V_22 from (0.025)^2 to (0.0034)^2 | eq:covariance |
| B2 | Added explanation of systematic growth (10% -> full data): C_b range widened, eps_c mismatch amplified by SF calibration | Section 9.2 text |
| B3 | Elevated kappa=2.0 as primary A_FB^b in abstract and conclusions; combined presented as cross-check with chi2/ndf = 10.9/3 caveat | Abstract and Section 11 |
| B4 | Added dilution calculation: A_FB^b_diluted ~ 0.103 * 0.18 * 0.13 ~ 0.002, consistent with +0.0025 | Abstract, results section, conclusions |
| B5 | Added operating_point_stability_sf_fulldata entry to validation.json (chi2=4.4, ndf=14, p=0.99) | validation.json |
| B6 | Fixed reproduction contract: ANALYSIS_NOTE_doc4b_v5.tex -> ANALYSIS_NOTE_doc4c_v3.tex | app:reproduction |
| B7 | Added journal/volume/pages to 5 BibTeX entries: ALEPH:AFBb, LEP:HF:2001, ALEPH:sigma_had, DELPHI:Rb, LEP:gcc | references.bib |
| B8 | Added R_c statement to abstract and introduction: constrained to SM, floating gives sigma > 0.05 | Abstract and Section 1 |
| B9 | Updated COMMITMENTS.md: resolved 3 genuine gaps ([D] for probability tag, constrained/floated R_c, analytical/toy propagation), marked 8 stale checkboxes as [x] | COMMITMENTS.md |

### Category C (Apply Before Commit)

| # | Fix |
|---|-----|
| C1 | Added sentence identifying dominant residual: single-tag/double-tag tension on eps_uds (~3% across configs) |
| C2 | Added sentence: contamination test was pre-calibration; post-SF linearity not separately tested |
| C3 | Added qualifier: "statistically independent (disjoint events, but sharing the same MC model)" |
| C4 | Updated precision ratio: ~19x vs ALEPH, ~41x vs LEP combined |
| C5 | Updated Known Limitations item 6: full dataset processed, stat << syst for R_b |
| C6 | Added "(10% subsample)" clarification to App A systematic shifts table caption |
| C7 | Deferred — minor figure quality, no specific actionable items |
| C8 | No action needed per arbiter |

## Files Modified

- `analysis_note/ANALYSIS_NOTE_doc4c_v3.tex` (new, from v2)
- `analysis_note/ANALYSIS_NOTE_doc4c_v3.pdf` (compiled)
- `phase4_inference/4b_partial/src/regen_figures_v6.py` (ALEPH labels)
- `phase4_inference/4b_partial/src/bdt_calibrated_extraction.py` (ALEPH label)
- `analysis_note/figures/efficiency_calibration.pdf` (regenerated)
- `analysis_note/figures/F4b_fd_vs_fs_10pct.pdf` (regenerated)
- `analysis_note/figures/bdt_calibrated_rb.pdf` (regenerated)
- `analysis_note/figures/F5b_systematic_breakdown_10pct.pdf` (regenerated)
- `analysis_note/results/systematics.json` (A4 fix)
- `analysis_note/results/validation.json` (B5 fix)
- `references.bib` (B7 fix)
- `COMMITMENTS.md` (B9 fix)
