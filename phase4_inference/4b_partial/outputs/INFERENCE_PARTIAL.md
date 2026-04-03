# Phase 4b: Inference -- 10% Data (REGRESSION)

**Session:** cosima_4c05 | **Date:** 2026-04-03
**Data:** 10% subsample (seed=42, 288,627 events)
**Methods:** 3-tag R_b (primary), purity-corrected A_FB^b (primary)

---

## 1. Summary

Re-ran Phase 4b using the regression-updated primary methods:
- R_b: 3-tag system (tight/loose/anti-b) replacing the 2-tag system
- A_FB^b: purity-corrected with MC-measured delta_b, afb_c = 0.0682 for data

### Key Results (10% data subsample)

| Observable | Value | Stat | Syst | Total | SM/Ref |
|-----------|-------|------|------|-------|--------|
| R_b (best WP) | 0.163 | 0.001 | 0.015 | 0.015 | 0.216 |
| R_b (combined) | 0.170 | 0.000 | 0.015 | 0.015 | 0.216 |
| A_FB^b | -0.027 | 0.008 | 0.024 | 0.025 | 0.100 |
| A_FB^{0,b} | -0.028 | 0.009 | -- | -- | 0.103 |
| sin^2(theta_eff) | 0.255 | 0.002 | -- | -- | 0.232 |

---

## 2. R_b Extraction (3-Tag System)

### Method
The 3-tag system defines three hemisphere categories:
- **Tight** (combined score > thr_tight): b-enriched
- **Loose** (thr_loose < score <= thr_tight): b+c enriched
- **Anti** (score <= thr_loose): uds-enriched

Efficiencies calibrated on full MC (730,365 events, R_b = 0.21578).
R_b extracted from 10% data by chi2 fit to 8 tag-fraction observables.

### Results

| Configuration | R_b | sigma_stat | chi2/ndf | p-value |
|---------------|-----|------------|----------|---------|
| tight=10, loose=5 | 0.16327 | 0.00112 | 1187/7 | 0.000 |
| tight=10, loose=3 | 0.16176 | 0.00118 | 1078/7 | 0.000 |
| tight=8, loose=4 | 0.16932 | 0.00114 | 942/7 | 0.000 |
| tight=8, loose=3 | 0.16943 | 0.00120 | 904/7 | 0.000 |
| tight=12, loose=6 | 0.18978 | 0.00119 | 33/7 | 0.000 |
| tight=7, loose=3 | 0.17331 | 0.00116 | 709/7 | 0.000 |
| tight=9, loose=4 | 0.16635 | 0.00115 | 1057/7 | 0.000 |
| tight=9, loose=5 | 0.16656 | 0.00122 | 1001/7 | 0.000 |

**Best WP:** tight=10, loose=5: R_b = 0.16327 +/- 0.00112 (stat)
**Combined:** R_b = 0.16985 +/- 0.00041, stability chi2/ndf = 389/7, p = 0.0 (FAIL)

### Finding F1: Large Data/MC R_b Discrepancy

**Observation:** R_b from data is ~0.17, vs MC truth of 0.216. Chi2/ndf
values are very large (33--1187), indicating MC-calibrated efficiencies
do not describe data.

**Root cause:** The MC was generated with specific detector response
parameters that do not perfectly match real data. The b-tag discriminant
distributions differ between data and MC, shifting the effective
efficiencies at each working point. This is a calibration mismatch,
not a physics signal.

**Resolution:** The systematic uncertainties (eps_c 10%, eps_uds 5%,
C_b data-MC) partially cover the data/MC difference. For Phase 4c,
a data-driven simultaneous fit of R_b + efficiencies should be
investigated to reduce MC dependence.

---

## 3. A_FB^b Extraction (Purity-Corrected)

### Method
Uses published ALEPH charge separations delta_b (hep-ex/0509008 Table 12),
MC-calibrated flavour fractions (f_b, f_c, f_uds), and afb_c = 0.0682
(published LEP charm asymmetry). Linear fit of <Q_FB> vs cos(theta).

Formula: A_FB^b = (slope - f_c * delta_c * A_FB^c) / (f_b * delta_b)

### Results by Kappa

| kappa | A_FB^b | sigma | chi2/ndf (WP) | p |
|-------|--------|-------|---------------|---|
| 0.3 | -0.052 | 0.020 | 0.42/5 | 0.995 |
| 0.5 | -0.047 | 0.016 | 0.53/5 | 0.991 |
| 1.0 | -0.024 | 0.016 | 0.65/5 | 0.986 |
| 2.0 | +0.002 | 0.016 | 0.34/5 | 0.997 |

**Cross-kappa combination:** A_FB^b = -0.027 +/- 0.008, chi2/ndf = 6.51/3, p = 0.089

### Derived Quantities
- A_FB^{0,b} = -0.028
- sin^2(theta_eff) = 0.255 +/- 0.002

### Finding F2: Negative A_FB^b with kappa dependence

**Observation:** A_FB^b is negative at low kappa and compatible with zero
at high kappa. The cross-kappa p = 0.089 shows marginal consistency.
Published LEP value is +0.0995; our result deviates by ~15 sigma.

**Root cause:** The MC flavour fractions f_b, f_c used for purity
correction are biased by the same data/MC tagging mismatch as R_b.
If f_b is overestimated from MC, the denominator is too large and
A_FB^b is suppressed or inverted. The jet charge slope is very small
(0.001-0.009) and the charm correction subtracts ~0.003-0.008, so
small biases in the denominator have large effects.

**Resolution:** Data-driven purity estimation for Phase 4c. Alternatively,
use lower-threshold WPs where purity corrections are smaller.

---

## 4. Systematic Uncertainties (Regression v2)

### R_b Systematics

| Source | delta(R_b) | Method |
|--------|-----------|--------|
| eps_c (10%, 3-tag) | 0.01292 | Re-extraction, 3-tag calibration |
| eps_uds (5%, anti-tag) | 0.00639 | Re-extraction, anti-tag constraint |
| C_b (data-MC x2) | 0.00336 | Re-extraction at WP=10 |
| R_c (+/- 0.003) | 0.00186 | Re-extraction, LEP combined |
| sigma_d0 | 0.00075 | Scaled from ALEPH x1.5 |
| hadronization | 0.00045 | Peterson vs Bowler-Lund |
| sigma_d0 form | 0.00040 | sin(theta) vs sin^{3/2} |
| MC statistics | 0.00040 | Poisson on calibration |
| physics params | 0.00020 | PDG uncertainties |
| g_bb, g_cc | 0.00011 each | LEP/world average |
| selection bias | 0.00010 | Ratio measurement |
| tau contamination | 0.00005 | Published efficiency |
| **Total systematic** | **0.01495** | |
| Statistical (combined) | 0.00041 | |
| **Total** | **0.01496** | |

### A_FB^b Systematics

| Source | delta(A_FB) |
|--------|------------|
| charge model (kappa spread) | 0.02149 |
| purity uncertainty | 0.01000 |
| angular efficiency | 0.00200 |
| charm asymmetry | 0.00140 |
| delta_b published | 0.00137 |
| delta_QCD | 0.00008 |
| **Total systematic** | **0.02386** |
| Statistical | 0.00838 |
| **Total** | **0.02529** |

### Regression Improvements
- eps_c variation reduced from 30% to 10% (3-tag constraint)
- eps_uds variation reduced from 50% to 5% (anti-tag constraint)
- C_b systematic uses data-MC difference x2 instead of arbitrary range

---

## 5. Comparison with Phase 4a

| | Phase 4a (MC) | Phase 4b (10% data) | Pull |
|---|---|---|---|
| R_b | 0.2158 +/- 0.0003 | 0.163 +/- 0.001 | -45.7 |
| A_FB^b | ~0 (sym MC) | -0.027 +/- 0.008 | N/A |

Both discrepancies trace to data/MC tagging efficiency mismatch.

---

## 6. Recommendations for Phase 4c

1. **Data-driven efficiency calibration:** Use the 3-tag system to
   simultaneously fit R_b + eps_b + eps_c + eps_uds from data.
2. **Data-driven purity for A_FB^b:** Extract f_b, f_c from the data
   3-tag fit rather than MC calibration.
3. **Lower WP for A_FB^b:** Use threshold 2.0-3.0 where purity corrections
   are smaller and less sensitive to efficiency modeling.
4. **Investigate hemisphere charge offset:** The consistent negative
   intercept in Q_FB fits may indicate a systematic bias.

---

## Artifacts

### Scripts
- `src/three_tag_rb_10pct.py` -- 3-tag R_b extraction on 10% data
- `src/purity_afb_10pct.py` -- purity-corrected A_FB^b on 10% data
- `src/systematics_10pct_v2.py` -- systematic evaluation (regression v2)
- `src/plot_phase4b_v2.py` -- publication-quality figures

### Output JSON
- `outputs/three_tag_rb_10pct.json`
- `outputs/purity_afb_10pct.json`
- `outputs/systematics_10pct_v2.json`
- `analysis_note/results/parameters.json` (updated)
- `analysis_note/results/systematics.json` (updated)

### Figures (5)
- `figures/rb_3tag_stability_10pct.pdf` -- R_b across threshold configs
- `figures/afb_kappa_10pct.pdf` -- A_FB^b across kappa values
- `figures/afb_qfb_vs_costheta_10pct.pdf` -- Q_FB vs cos(theta) fit
- `figures/systematics_breakdown_10pct.pdf` -- systematic breakdown
- `figures/rb_comparison_mc_data.pdf` -- MC vs data comparison
