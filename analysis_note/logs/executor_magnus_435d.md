# Session Log: magnus_435d

## Session: executor + note writer
## Date: 2026-04-04

## Tasks Completed

### Issue 1: Per-year cross-check with BDT tagger
- Created `phase4_inference/4c_observed/src/per_year_bdt_extraction.py`
- Trains BDT on full MC, scores data per-year, extracts R_b and A_FB^b
- Results (per_year_bdt_results.json):
  - 1992: R_b = 0.2157 +/- 0.0009
  - 1993: R_b = 0.2156 +/- 0.0008
  - 1994: R_b = 0.2158 +/- 0.0006
  - 1995: R_b = 0.2156 +/- 0.0007
  - chi2/ndf = 0.04/3 (p = 0.998) -- essentially perfect consistency
- Per-year A_FB^b with signed-thrust method also extracted, chi2/ndf = 1.06/3 (p = 0.79)
- Generated: per_year_bdt_consistency.pdf

### Issue 2: A_FB angular distribution fit model
- Created `phase4_inference/4c_observed/src/afb_quadratic_fit.py`
- Results (afb_quadratic_results.json):
  - |cos(theta)| bins (primary): linear chi2/ndf = 10.9/8 (p=0.208), acceptable
  - |cos(theta)| bins: quadratic chi2/ndf = 6.9/7 (p=0.44), F-test p=0.084 (not significant)
  - Signed cos(theta) bins: cos^2 term is 6.5 sigma significant
  - The cos^2 component is a symmetric purity/acceptance effect
  - The |cos(theta)| extraction correctly isolates the asymmetry
  - Linear model is the correct choice for the primary extraction
- Generated: afb_angular_quadratic.pdf

### Issue 3: AN expansion to v9 (50 pages)
- Copied v8 to v9, expanded from 1999 to 3100+ lines (34 to 50 pages)
- **New SV reconstruction section** (sec 4.5):
  - Displaced track selection criteria
  - Vertex finding algorithm
  - SV property distributions with data/MC figures (mass, ntrk, flight, flight_sig)
  - SV discriminant
  - Role of SV features
- **New detailed BDT training section** (sec 4.6):
  - XGBoost hyperparameters
  - Proxy label construction
  - 50/50 train/test split
  - Full 10-feature list with importances
  - Overtraining check with figures
  - AUC=1.0 explanation with 3-point validation
  - Data/MC agreement figure
  - ROC curve
- **Expanded systematic sections**:
  - eps_c: linear envelope treatment explained in detail
  - eps_uds: anti-tag constraint derivation
  - C_b: sources of correlation, evaluation method, BDT vs cut-based
  - sigma_d0: scale factor and angular form variations
  - R_c: sum rule relationship
  - Gluon splitting: mechanism explained
  - All other sources: method descriptions added
- **Expanded AFB systematics**: per-source detailed method descriptions
- **AFB angular fit model study**: new section (sec 6.4)
- **Per-year BDT cross-check**: new subsection with table and figure
- **Cross-check comparison tables**: cut-based vs BDT, multiple AFB methods
- **New appendices**:
  - BDT optimization scans (figures)
  - BDT vs cut-based comparison table
  - Angular fit model details with tables
  - Per-year BDT extraction details with SF table
  - Data/MC agreement summary (8 additional figures)
  - SV-enhanced cross-checks
  - Closure test details
  - BDT R_b comparison
  - Detailed extraction algebra
- Added xgboost reference to references.bib

## Figures Staged
- analysis_note/figures/per_year_bdt_consistency.pdf
- analysis_note/figures/afb_angular_quadratic.pdf
- analysis_note/figures/sv_sv_mass_dist.png
- analysis_note/figures/sv_sv_ntrk_dist.png
- analysis_note/figures/sv_sv_flight_dist.png
- analysis_note/figures/sv_sv_flight_sig_dist.png
- analysis_note/figures/sv_discriminant_dist.png
- analysis_note/figures/sv_efficiency_scan.png
- analysis_note/figures/sv_rb_comparison.png
- analysis_note/figures/bdt_overtraining.png
- analysis_note/figures/bdt_feature_importance.png
- analysis_note/figures/bdt_roc.png
- analysis_note/figures/bdt_data_mc_agreement.png
- analysis_note/figures/bdt_training_curve.png
- analysis_note/figures/bdt_rb_comparison.png
- analysis_note/figures/bdt_rb_vs_threshold.png
- analysis_note/figures/bdt_mass_threshold_scan.png
- analysis_note/figures/bdt_afb_vs_cut.png
- analysis_note/figures/sv_afb_fit_kappa2.0_svtight.png

## Key Findings
1. The per-year R_b discrepancy (0.188 vs 0.2155) was entirely due to charm contamination in the cut-based tag. The BDT tagger gives consistent per-year R_b ~ 0.2157.
2. The "peaked/gaussian" Q_FB vs cos(theta) pattern was a symmetric cos^2 purity/acceptance effect visible in signed cos(theta) bins. The |cos(theta)| extraction (primary method) correctly handles this.
3. The AN expanded from 34 to 50 pages with substantial physics content.
