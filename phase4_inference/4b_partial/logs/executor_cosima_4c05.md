# Session Log: cosima_4c05

## Task
Re-run Phase 4b on 10% data using regression-updated primary methods:
- 3-tag R_b (replaces 2-tag)
- Purity-corrected A_FB^b with afb_c=0.0682 for data
- Updated systematics (eps_c 10%, eps_uds 5%)

## Plan
1. Write `three_tag_rb_10pct.py` -- 3-tag R_b on 10% data
2. Write `purity_afb_10pct.py` -- purity-corrected A_FB^b on 10% data
3. Write `systematics_10pct_v2.py` -- updated systematic treatment
4. Write `plot_phase4b_v2.py` -- publication-quality figures
5. Update `parameters.json` with 10pct entries
6. Write `INFERENCE_PARTIAL.md`

## Data
- 10% data: 288,627 events in data_10pct_tags.npz, data_10pct_jetcharge.npz
- MC: 730,365 events for calibration (phase3 outputs)
- Phase 4a calibration: best config tight=8, loose=4

## Progress
- [x] Checked data arrays and Phase 4a results
- [x] three_tag_rb_10pct.py -- R_b = 0.163 (best), 0.170 (combined)
- [x] purity_afb_10pct.py -- A_FB^b = -0.027 +/- 0.008
- [x] systematics_10pct_v2.py -- syst(R_b)=0.015, syst(AFB)=0.024
- [x] plot_phase4b_v2.py -- 5 figures produced
- [x] parameters.json updated with 10pct entries + systematics
- [x] INFERENCE_PARTIAL.md written

## Key Findings
1. Data/MC tagging efficiency mismatch: R_b from data ~0.17 vs SM 0.216
2. Negative A_FB^b = -0.027 (vs LEP published +0.0995)
3. Both driven by MC calibration not matching data tag distributions
4. Stability test fails for R_b (p=0.0)
5. Systematic uncertainties bring R_b within ~3 sigma of SM

## Completion
All tasks done. Session complete.
