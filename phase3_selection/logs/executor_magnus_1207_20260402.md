# Phase 3 Executor Log — magnus_1207

Session: magnus_1207 | Date: 2026-04-02
Phase: 3 — Selection / Processing

## Plan

### Scripts to write (analysis — src/)

1. **preselection.py** — Event preselection (passesAll=1, |cos(theta_thrust)|<0.9), track quality cuts (nvdet>0, highPurity=1, ntpc>4), cutflow table, save intermediate arrays to NPZ
2. **d0_sign_validation.py** — [D19] BLOCKING gate: validate d0 sign convention by checking asymmetry of d0/sigma_d0 in b-enriched hemispheres
3. **sigma_d0_calibration.py** — [D7] Parameterize sigma_d0, calibrate from negative d0 tail per (nvdet, momentum, cos theta) bins
4. **hemisphere_tag.py** — Build hemisphere probability tag P_hem [D8], mass tag [D18], combined tag; scan working points
5. **jet_charge.py** — Hemisphere jet charge Q_h for kappa={0.3, 0.5, 1.0, 2.0, infinity} [D4,D5]
6. **double_tag_counting.py** — Count N_t, N_tt at multiple working points; operating point scan
7. **closure_tests.py** — Three closure tests from COMMITMENTS.md: negative-d0 pseudo-data, bFlag consistency, artificial contamination injection
8. **plot_utils.py** — Reusable plotting utilities (data_mc_comparison, save_and_register, standard figure setup)

### Scripts to write (plotting)

9. **plot_preselection.py** — Cutflow visualization, cos(theta) distribution
10. **plot_d0_validation.py** — d0 sign convention validation figure
11. **plot_sigma_d0.py** — sigma_d0 calibration results
12. **plot_tagging.py** — P_hem distributions, mass tag, efficiency vs purity
13. **plot_jet_charge.py** — Q_h distributions for each kappa
14. **plot_double_tag.py** — R_b operating point scan, N_t/N_tt distributions
15. **plot_closure.py** — Closure test results
16. **plot_data_mc.py** — Data/MC comparisons for ALL variables entering observable

### Figures to produce

- F_presel: Cutflow table/bar chart
- F_d0sign: d0/sigma_d0 distribution in b-enriched vs inclusive hemispheres [D19]
- F_sigma_d0: sigma_d0 calibration quality per bin
- F_phem: P_hem distribution data vs MC
- F_mass: Hemisphere mass distribution
- F_tag_eff: Tagging efficiency vs purity (cut-based vs BDT if applicable)
- F_qh: Hemisphere charge distributions per kappa
- F_rb_scan: R_b vs working point stability scan (flagship F1 preview)
- F_closure_neg: Negative-d0 closure test
- F_closure_bflag: bFlag consistency test
- F_closure_inject: Contamination injection test
- F_data_mc_*: Data/MC for d0/sigma_d0, hemisphere mass, P_hem, jet charge, thrust, cos(theta)

### Artifact structure

- outputs/SELECTION.md — primary artifact
- outputs/FIGURES.json — figure registry
- outputs/figures/*.png, *.pdf — all figures
- outputs/cutflow.json — cutflow numbers
- outputs/sigma_d0_params.json — calibration parameters
- outputs/tag_efficiencies.json — efficiencies at working points
- outputs/double_tag_counts.json — N_t, N_tt per working point
- outputs/closure_results.json — closure test results
- outputs/jet_charge.json — jet charge distributions and delta_b

## Execution Log

### Step 1: Plot utilities module
Starting with plot_utils.py as foundation for all subsequent plotting.

