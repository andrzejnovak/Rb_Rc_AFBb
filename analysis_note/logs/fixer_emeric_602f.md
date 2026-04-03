# Fixer Session: emeric_602f

Date: 2026-04-02
Task: Fix AN Doc 4a v1 per arbiter verdict (zelda_65ac)

## Findings Resolution Log

### Category A

| # | Finding | Status | Action |
|---|---------|--------|--------|
| 1 | A_FM^b typo (3 locations) | RESOLVED | Replaced all 3 instances of `\mathrm{FM}` with `\mathrm{FB}` |
| 2 | No closure test at WP 10.0 | RESOLVED (INFEASIBLE) | Documented 3 remediation attempts (standard split, 70/30 split, bootstrap) — all fail due to solver convergence. INFEASIBLE declaration with evidence. |
| 3 | OP stability: no remediation attempts | RESOLVED (INFEASIBLE) | Documented 3 remediation attempts (extended alpha scan, relaxed constraints, iterative R_b input). All structural failures. INFEASIBLE declaration. |
| 4 | Circular calibration bias unexplained | RESOLVED | Added quantitative bias decomposition: eps_uds mis-calibration (~0.06), C_b inflation (~0.005), remainder <0.001. |
| 5 | Per-kappa table reports rejected-model chi2 | RESOLVED | Added intercept-inclusive chi2/ndf column to Table: 25.7/8 to 34.4/8 across kappa. |
| 6 | delta_QED uncited | RESOLVED | Added value (-0.0015) with LEP:EWWG:2005 citation. |
| 7 | kappa=infinity absent from results table | RESOLVED | Added inf row: slope=-0.00191+/-0.00430, delta_b=1.000, A_FB=-0.002. |
| 8 | COMMITMENTS.md not updated | RESOLVED | All systematic checkboxes marked [x] with Phase 4a values. Validation tests, flagship figures updated. |
| 9 | Parameter sensitivity table missing | RESOLVED | Added Table with 5 parameters, derivatives, 5x-stat flags. |
| 10 | Broken \ref{sec:jetcharge} | RESOLVED | Added \label{sec:jetcharge} to hemisphere charge appendix section. |
| 11 | 3 orphaned figures | RESOLVED | Added \ref for fig:datamc_track, fig:p1_d0_trackpt, fig:datamc_tag2. |
| 12 | 7 orphaned tables | RESOLVED | Added \ref for tab:mc_samples, tab:track_cutflow, tab:corrupted_corrections, tab:sin2theta_comparison, tab:weight_impact, tab:hemisphere_charge_properties, tab:nsigma_fractions. |
| 13 | Closure panel (a) rendering bug | RESOLVED | Confirmed rendering bug (zero-height bar invisible). Fixed plot code: different colors for bars, arrow annotation at y=0. Updated caption. Figure regenerating. |
| 14 | Closure panel (b) chi2 annotation truncated | RESOLVED | Fixed plot code: reduced fontsize, added thousands separator. Caption already correct (11,447). |
| 15 | Truncated x-axis label in efficiency_calibration | RESOLVED | Changed inclusion from height=0.45\linewidth to width=\linewidth for better readability of wide 3-panel figure. |
| 16 | Efficiency calibration figure unreadable | RESOLVED | Same fix as #15 — full-width inclusion gives each panel adequate size. |
| 17 | F2 shows only rejected-model fit | PARTIALLY RESOLVED | Added intercept chi2 values to per-kappa table and explanatory note. Full figure regeneration with overlay of both models would require Phase 4a code changes beyond fixer scope. |

### Category B

| # | Finding | Status | Action |
|---|---------|--------|--------|
| 18 | C_c, C_uds values unreported | RESOLVED | Added C_c = C_uds = 1.0 with justification in double-tag formula discussion. |
| 19 | Closure PASS label inconsistent | RESOLVED | Added caveat to Table caption about partial independence. |
| 20 | eps_c solver failure motivation | RESOLVED | Added boundary analysis: +30% causes no real positive solution for eps_b; one-sided systematic acknowledged. |
| 21 | sigma_d0_form no cited measurement | RESOLVED | Added ALEPH:VDET citation for sin(theta) form. |
| 22 | sigma_d0 high-scale-factor tracks | RESOLVED | Added investigation paragraph: 8% of sample, 1-VDET low-p tracks, bin-by-bin calibration handles them. |
| 23 | C_b derivative cross-check | RESOLVED | Added analytical derivative calculation confirming numerical result. |
| 24 | Pull uncertainty at WP 9.0 | RESOLVED | Added +/- 0.08 uncertainty from finite toy statistics (1/sqrt(305)). |
| 25 | r_b, r_c undefined | RESOLVED | Added r_b = r_c = 1 assumption with justification. |
| 26 | f_s/f_d source ambiguity | RESOLVED | Clarified "MC pseudo-data at Phase 4a; real data at Phase 4b/4c" in provenance table and extraction section. |
| 27 | Validation table post-fix chi2 | RESOLVED | Added angular fit (intercept) row: chi2/ndf = 26-34/8, FAIL at chi2/ndf~3-4. |
| 28 | D12b risk note | RESOLVED | Added risk note: Phase 4b carries both implementation and validation risk. |
| 29 | ALEPH:opendata missing fields | RESOLVED | Added author, year, howpublished fields. |
| 30 | LEP:gcc missing author | RESOLVED | Added author field. |
| 31 | BibTeX LaTeX in titles | RESOLVED | Cleaned 8 entries: removed $...$ and \mathrm from titles. |
| 32 | Whitespace gaps | NOT FIXED | Whitespace is LaTeX float placement; at 52 pages, careful adjustment needed. Low priority. |
| 33 | F7 combined band visibility | PARTIALLY RESOLVED | Updated caption to explicitly describe band location and values. Full figure regeneration deferred. |

### Category C (applied)
- Updated captions with quantitative agreement statements
- Added eps_uds 50% variation context
- Clarified MC event counts
- Added kappa=inf in systematic discussion
- Fixed process language in Change Log
- Various prose improvements

## Files Modified
- analysis_note/ANALYSIS_NOTE_doc4a_v2.tex (created from v1, all fixes applied)
- references.bib (BibTeX field additions and title cleanup)
- COMMITMENTS.md (Phase 4a status update)
- phase3_selection/src/plot_all.py (closure test rendering fixes)
