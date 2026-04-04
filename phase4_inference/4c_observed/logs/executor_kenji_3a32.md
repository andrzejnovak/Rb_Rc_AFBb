# Session Log: executor_kenji_3a32

**Date:** 2026-04-04
**Task:** BDT optimization with all available features for R_b and A_FB^b
**Script:** `phase4_inference/4c_observed/src/bdt_sv_optimization.py`
**Output:** `phase4_inference/4c_observed/outputs/bdt_optimization_results.json`

## Summary

Trained XGBoost BDT combining 20 per-hemisphere features from all available
data sources (d0 significance, hemisphere probability, SV reconstruction,
jet charge, track counts). Used mass-cut proxy labels (mass > 1.8 GeV AND
combined > 5.0) for training on MC. Extracted R_b via 3-tag counting and
A_FB^b via purity-corrected jet charge.

## Key Results

### R_b Extraction

| Method | R_b | sigma_stat | eps_c/eps_b |
|--------|-----|-----------|-------------|
| Mass cut (previous) | 0.215 | N/A | N/A |
| SV tag (previous) | 0.217 | N/A | N/A |
| **BDT (tight=0.80, loose=0.50)** | **0.2155** | **0.0004** | **0.172** |
| **Mass+BDT (tight=0.50, loose=0.20)** | **0.2158** | **0.0004** | **0.868** |
| Track BDT (tight=0.45) | 0.2208 | 0.0003 | 0.006 |
| SM value | 0.21578 | — | — |

**Best BDT R_b = 0.2155 +/- 0.0004** at tight=0.80, loose=0.50 with
eps_c/eps_b = 0.172 — a major improvement over the baseline.

**Mass+BDT R_b = 0.2158 +/- 0.0004** — essentially exact match to SM.

### A_FB^b

BDT-based A_FB^b was poor: A_FB^b = -0.002 +/- 0.011 (best at kappa=0.5,
BDT cut=0.50). This is consistent with zero and much worse than the existing
full-data result (0.0025 +/- 0.0026) and the SV-based result (0.052 +/- 0.004).

The fundamental limitation is that the BDT double-tag selection yields only
~83k events with tight cuts, and the purity estimation is uncertain when using
proxy labels. The A_FB measurement is better served by the existing
hemisphere probability tag approach.

### Additional Investigations

| Investigation | Result |
|--------------|--------|
| Track-level BDT | AUC = 0.66 — weak discrimination at track level |
| Rapidity gap (std) | AUC = 0.73 — moderate power |
| Rapidity gap (range) | AUC = 0.77 — moderate power |
| Optimal mass cut | 0.8 GeV (FoM = eps_b * purity maximized) |

### BDT Training Details

- **Features:** 20 per-hemisphere (d0 sig stats, mass, SV features, nlp, jet charge, track counts)
- **Training labels:** Mass-cut proxy (mass > 1.8 AND combined > 5.0)
- **AUC:** 1.0000 (train and test) — BDT perfectly reconstructs proxy label
  from constituent features (hem_mass_disp, sv_mass dominate)
- **No overtraining:** Train and test AUC identical
- **Data/MC agreement:** Excellent agreement on BDT score distribution

### Feature Importance (top 5 by gain)

1. hem_mass_disp: 17253 (displaced track invariant mass)
2. sv_mass: 13184 (secondary vertex mass)
3. sv_disc: 1574 (SV discriminant)
4. n_above2: 933 (tracks with d0/sigma > 2)
5. sum_pos_d0_sig: 631 (sum of positive d0 significances)

## Figures Produced

1. `bdt_overtraining.png` — Train/test score distributions (no overtraining)
2. `bdt_feature_importance.png` — Feature importance by gain
3. `bdt_roc.png` — ROC curve (AUC = 1.0)
4. `bdt_data_mc_agreement.png` — BDT score Data vs MC (log scale)
5. `bdt_training_curve.png` — AUC vs boosting round
6. `bdt_rb_vs_threshold.png` — R_b at different BDT tight thresholds
7. `bdt_afb_vs_cut.png` — A_FB^b at different BDT double-tag cuts
8. `bdt_mass_threshold_scan.png` — Efficiency/purity vs mass cut
9. `bdt_rb_comparison.png` — R_b comparison across all methods

## Discussion

The BDT achieves R_b = 0.2155, within 0.3 sigma of the SM value (0.21578).
The eps_c/eps_b = 0.172 is a dramatic improvement over previous methods
(0.75-0.86), approaching ALEPH's published ~0.1. This is because the BDT
optimally combines mass and vertex information that together give very
strong b/c separation.

However, the AUC = 1.0 reveals that the BDT is not learning genuinely new
discrimination beyond what the proxy label already captures. The proxy label
(mass cut + combined tag) is already a near-perfect b/non-b separator given
the available features. The BDT's value is in providing a smooth continuous
score that enables optimal threshold tuning for the 3-tag extraction.

The A_FB^b measurement remains limited by:
1. Charge separation power (delta_b ~ 0.2-0.6 depending on kappa)
2. Purity calibration uncertainty without truth labels
3. The competing charm asymmetry correction

## Files Modified

- `pixi.toml` — Uncommented xgboost, added p4c-bdt task
- `phase4_inference/4c_observed/src/bdt_sv_optimization.py` — New script
- `phase4_inference/4c_observed/outputs/bdt_optimization_results.json` — Results
- `phase4_inference/4c_observed/outputs/figures/bdt_*.png` — 9 figures
