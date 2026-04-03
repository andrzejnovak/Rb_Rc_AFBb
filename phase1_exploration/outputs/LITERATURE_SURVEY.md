# Literature Survey — Phase 1

Session: fabiola_b942 | Date: 2026-04-02

## Summary

Comprehensive literature search performed using LEP corpus (MCP_LEP_CORPUS=true)
and arXiv. Identified key reference analyses for R_b, R_c, and A_FB^b from ALEPH
and the LEP/SLD combination. The definitive reference is the LEP EWWG Z-pole
combination (hep-ex/0509008, Phys. Rept. 427, 257, 2006). The ALEPH-specific
references are hep-ex/9609005 (R_b with multiple tags) and inspire_433746
(A_FB^b with lifetime tag and hemisphere charge).

## Reference Analyses

### 1. ALEPH R_b — hep-ex/9609005

**Title:** "A Measurement of R(b) using multiple tags"
**Experiment:** ALEPH
**Dataset:** 1992-1995 data (~4 million hadronic events)
**Method:** Five mutually exclusive hemisphere tags (Q, S, L, X, and uds tags).
The Q tag is a high-purity b-tag combining 3D impact parameter probability
and a mass tag exploiting the b/c hadron mass difference. Double-tag method
with 5 single-tag fractions and 15 double-tag fractions fitted simultaneously.
**Result:** R_b = 0.2158 +/- 0.0009 (stat.) +/- 0.0011 (syst.) (preliminary)
**Key features:**
- Hemisphere-by-hemisphere primary vertex reconstruction
- Hemisphere correlation factors computed from MC
- Background efficiencies (charm, uds) fitted from data using multiple tags
- Systematic dominated by detector simulation uncertainty

**Systematic program (from corpus):**
- Detector simulation (tracking resolution, d0 smearing)
- b/c physics uncertainties (fragmentation, lifetimes, branching ratios)
- Hemisphere-hemisphere correlation uncertainties
- Background efficiency uncertainties

### 2. ALEPH A_FB^b — inspire_433746

**Title:** "An upgraded measurement of A(b)(FB) from the charge asymmetry
in lifetime tagged Z decays"
**Experiment:** ALEPH
**Dataset:** 1991-1995 data (~4.0 million hadronic events after selection)
**Method:** Hemisphere charge method with lifetime tagging. Jet charge with
momentum weighting parameter kappa = {0.3, 0.5, 1.0, 2.0, infinity}.
Simultaneous fit to angular distribution and purity dependence.
**Result:**
- sin^2(theta_w^eff) = 0.2330 +/- 0.0009
- A_FB^b = 0.0927 +/- 0.0039 (stat.) +/- 0.0034 (syst.)
**Key features:**
- Fitted b-tag efficiency and charge separation simultaneously
- Angular acceptance |cos(theta)| < 0.9
- Multiple kappa values provide redundancy
- Systematic dominated by b hemisphere charge and lifetime tag efficiency

**Event counts per year (Table 1 from paper):**

| Year | Hadronic sel. | After all cuts |
|------|--------------|----------------|
| 1991 | 249,000 | 241,000 |
| 1992 | 681,000 | 668,000 |
| 1993 | 678,000 | 668,000 |
| 1994 | 1,749,000 | 1,716,000 |
| 1995 | 749,000 | 732,000 |
| Total | 4,104,000 | 4,025,000 |

### 3. ALEPH R_b (precise measurement) — inspire_433306

**Title:** "A Precise Measurement of Gamma(Z -> bb) / Gamma(Z -> hadrons)"
**Method:** Combined impact parameter and mass tag for b-hemispheres.
Uses negative impact parameter significance to calibrate tracking resolution.
**Key technique:** The negative d0 tail is used to characterize the resolution
function, since truly negative impact parameters arise only from resolution
effects, not from displaced vertices.

### 4. ALEPH R_c — inspire_483143

**Title:** "Production of c and b flavored mesons and their decays at LEP"
**Method:** R_c from charm counting — summing over exclusive production rates
of D0, D+, Ds+, Lambda_c with corrections for other charmed baryons.
**Result (ALEPH):** R_c = 0.166 +0.012 -0.011 (stat.) +/- 0.009 (syst.)
**LEP combined (from charm counting):** R_c = (17.31 +/- 0.44)%

### 5. LEP/SLD EWWG Z-pole Combination — hep-ex/0509008

**Title:** "Precision Electroweak Measurements on the Z Resonance"
**Publication:** Phys. Rept. 427, 257 (2006)
**Key combined results (from hep-ex/0509008):**

| Observable | Combined Value | SM Prediction |
|------------|---------------|---------------|
| R_b^0 | 0.21629 +/- 0.00066 | 0.21578 |
| R_c^0 | 0.1721 +/- 0.0030 | 0.17223 |
| A_FB^{0,b} | 0.0992 +/- 0.0016 | 0.1032 |
| A_FB^{0,c} | 0.0707 +/- 0.0035 | 0.0738 |
| sin^2(theta_eff) | 0.23153 +/- 0.00016 | — |

Note: A_FB^b shows the largest deviation from SM (2.8 sigma), driven by
the tension between A_FB^b and A_l(SLD) determinations of sin^2(theta_eff).

### 6. DELPHI R_b — inspire_1661836

**Title:** "A precise measurement of the partial decay width ratio R_b^0"
**Result:** R_b = 0.21625 +/- 0.00067 (stat.) +/- 0.00061 (syst.)
(with R_c fixed to SM value)
**Method:** Enhanced impact parameter tag + multivariate analysis.
Useful as cross-experiment comparison and methodological reference.

### 7. DELPHI R_b (earlier) — inspire_1661831

**Results from three methods:**
- Double lifetime tag: R_b = 0.2216 +/- 0.0017 (stat.) +/- 0.0027 (syst.)
- Mixed tag: R_b = 0.2231 +/- 0.0029 +/- 0.0035
- Multivariate: R_b = 0.2186 +/- 0.0032 +/- 0.0022
- Combined: R_b = 0.2210 +/- 0.0016 (stat.) +/- 0.0020 (syst.)

## Double-Tag Method Formalism

From the LEP EWWG combination (inspire_416138, hep-ex/0112021):

The double-tag method divides events into hemispheres. For N_had hadronic Z
decays, with N_t single-tagged hemispheres and N_tt double-tagged events:

```
N_t / (2 N_had) = eps_b * R_b + eps_c * R_c + eps_uds * (1 - R_b - R_c)
N_tt / N_had = C_b * eps_b^2 * R_b + C_c * eps_c^2 * R_c + ...
```

where eps_q are hemisphere tagging efficiencies and C_q are hemisphere
correlation factors. The key advantage: eps_b is measured from data
(from the ratio N_tt/N_t), making the result largely insensitive to MC
modelling of b-hadron properties.

## A_FB^b Method — Hemisphere Charge

From inspire_433746 and inspire_342763:

The quark direction is estimated using the thrust axis. The quark vs
antiquark is distinguished using hemisphere charge:

```
Q_h = sum_i q_i * |p_L,i|^kappa / sum_i |p_L,i|^kappa
```

where the sum runs over tracks in a hemisphere, q_i is the track charge,
and p_L,i is the longitudinal momentum w.r.t. the thrust axis. The
parameter kappa controls the weighting: kappa=0 gives unit weights
(track counting), larger kappa emphasizes high-momentum tracks.

The mean charge separation delta_b = <Q_b> - <Q_bbar> is measured from
data using the lifetime tag and is a key input.

The forward-backward asymmetry is:

```
A_FB^b = (8/3) * <Q_FB> / (R_b * delta_b)
```

where <Q_FB> is the mean forward-backward charge asymmetry.

## ALEPH Hadronic Cross Section

From inspire_367499:
- sigma_0^had = 41.56 +/- 0.09 (stat.) +/- 0.15 (syst.) nb
- Hadronic event selection efficiency: 99.1 +/- 0.09% (calorimetric),
  97.4 +/- 0.24% (track-based)
- Background: ~0.7-1.0%

## Standard Model Predictions

From the LEP EWWG combination and cited references:
- R_b^SM = 0.21578 (sensitive to m_top via vertex corrections)
- R_c^SM = 0.17223
- A_FB^{0,b} (SM) = 0.1032
- sin^2(theta_eff) = 0.23149 (from global SM fit)

## Modern Methodology

The LEP measurements of R_b, R_c, and A_FB^b are definitive — no modern
experiments have remeasured these at the Z pole. The methodology (double-tag
counting, hemisphere charge) is well-established and specific to e+e- at
the Z pole. No "modern" ML-based alternatives have been applied to these
specific observables, as the measurements are statistics-limited and the
classical methods are optimal.

The state of the art remains the LEP/SLD EWWG combination from 2005
(hep-ex/0509008). Future improvements would come from FCC-ee or CEPC.

## Search Trail

| Query Tool | Query | Results | Key Findings |
|-----------|-------|---------|-------------|
| LEP corpus | R_b measurement lifetime tag double tag hemisphere | 8 | hep-ex/9609005, inspire_416138 |
| LEP corpus | R_c charm measurement hadronic Z decay | 5 | inspire_483143 |
| LEP corpus | A_FB b quark sin2 theta effective | 5 | inspire_433746, inspire_1631399 |
| LEP corpus | compare_measurements R_b | 6 | ALEPH + DELPHI R_b papers |
| LEP corpus | ALEPH luminosity per year | 5 | inspire_309800, inspire_367499 |
| LEP corpus | hadronic cross section sigma_had | 5 | inspire_367499 |
| LEP corpus | signed impact parameter significance b-tagging | 5 | inspire_433306 |
| LEP corpus | LEP combined R_b R_c A_FB world average | 5 | hep-ex/0112021, hep-ex/0509008 |
| arXiv | precision electroweak measurements Z resonance | 5 | hep-ex/0509008v3 |
| arXiv | LEP R_b A_FB electroweak | 5 | hep-ex/0306005 |

## Key Numerical Inputs Found

(Full inventory in INPUT_INVENTORY.md)

| Quantity | Value | Source |
|----------|-------|--------|
| R_b (ALEPH, multiple tags) | 0.2158 +/- 0.0009 +/- 0.0011 | hep-ex/9609005 |
| R_b (LEP/SLD combined) | 0.21629 +/- 0.00066 | hep-ex/0509008 |
| R_c (LEP combined) | 0.1721 +/- 0.0030 | hep-ex/0509008 |
| A_FB^b (ALEPH, hemisphere charge) | 0.0927 +/- 0.0039 +/- 0.0034 | inspire_433746 |
| A_FB^{0,b} (LEP combined) | 0.0992 +/- 0.0016 | hep-ex/0509008 |
| sin^2(theta_eff) (ALEPH, from A_FB^b) | 0.2330 +/- 0.0009 | inspire_433746 |
| sigma_0^had (ALEPH) | 41.56 +/- 0.18 nb | inspire_367499 |
| ALEPH total hadronic events (1991-95) | ~4.1 million | inspire_433746 |
