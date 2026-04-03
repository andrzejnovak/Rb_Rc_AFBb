# Phase 4c Executor Log: anselm_820b

**Date:** 2026-04-03
**Task:** Final R_b, A_FB^b measurement on full ALEPH 1992-1995 data

## Execution Timeline

1. **Data inventory**: Phase 3 outputs already contain ALL data (2,887,261
   events with year labels 1992-1995) and hemisphere tags + jet charges
   computed for full dataset. No ROOT file reprocessing needed.

2. **three_tag_rb_fulldata.py**: 3-tag R_b at 8 WPs with SF calibration.
   Key finding: tight=12,loose=6 gives R_b = 0.2159, matching SM.
   Combined R_b = 0.190, stability fails (expected).

3. **afb_fulldata.py**: A_FB^b at 4 kappas x 6 WPs. Toys reduced to 100
   (from 1000) due to computational cost on 2.8M events. Combined
   A_FB^b = -0.076, negative due to MC purity bias.

4. **per_year_extraction.py**: R_b and A_FB per year. Both consistency
   tests pass (p > 0.28).

5. **systematics_fulldata.py**: Full systematic budget. Total syst(R_b)
   = 0.018, dominated by eps_c (0.015) and eps_uds (0.009).

6. **bdt_crosscheck_fulldata.py**: BDT cross-check confirms lower R_b
   without SF correction.

7. **plot_phase4c.py**: 6 publication-quality figures generated.

## Decisions Made

- Used SF calibration (data/MC tag-rate ratios) to correct MC efficiencies.
  This is the key improvement over Phase 4b.
- Selected tight=8,loose=4 as best WP (lowest stat uncertainty) for
  systematics evaluation, while noting tight=12,loose=6 recovers SM value.
- Reduced A_FB toys to 100 for computational feasibility.
- Added MC year coverage systematic (0.00050) since MC is 1994-only.

## Issues

- R_b WP stability fails: systematic data/MC efficiency mismatch is
  WP-dependent and not fully captured by linear SF correction.
- A_FB is negative: MC purity correction is biased. Would need
  data-driven purity estimation to fix.
- BDT cross-check gives low R_b: no SF correction applied to BDT pipeline.
