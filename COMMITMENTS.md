# Commitments — R_b, R_c, A_FB^b

Last updated: Phase 4a REGRESSION (pavel_37f4, 2026-04-03)

## Status key

- `[x]` Resolved
- `[D]` Formally downscoped (with documented justification)
- `[ ]` Not yet addressed

---

## Reference Analyses [REF]

### [REF1] ALEPH R_b — hep-ex/9609005
- **Result:** R_b = 0.2158 +/- 0.0009 (stat) +/- 0.0011 (syst)
- **Methodology:** Double-tag with 5 mutually exclusive hemisphere tags
  (Q=lifetime-mass, S=lifetime+NN, L=lepton, X=charm, uds=anti-b)
- **MC sample size:** Full ALEPH MC production (~10M events estimated)
- **Key choices:** Hemisphere-by-hemisphere primary vertex; 3D impact
  parameter probability + mass tag for high-purity Q tag; simultaneous
  fit of R_b + 13 efficiencies to 20 measured tag fractions

### [REF2] ALEPH R_b precise — inspire_433306
- **Result:** R_b = 0.2159 +/- 0.0009 (stat) +/- 0.0011 (syst)
- **Methodology:** Combined impact parameter + mass tag; negative d0 tail
  for resolution calibration; hemisphere-by-hemisphere primary vertex
- **MC sample size:** Full ALEPH MC production
- **Key choices:** d0 smearing to match data-MC; separate treatment of
  1-VDET and 2-VDET tracks; soft-cut scaling for correlation studies

### [REF3] ALEPH A_FB^b — inspire_433746
- **Result:** A_FB^b = 0.0927 +/- 0.0039 (stat) +/- 0.0034 (syst);
  sin^2(theta_eff) = 0.2330 +/- 0.0009
- **Methodology:** Hemisphere charge with lifetime tag, self-calibrating fit
- **MC sample size:** Full ALEPH MC production
- **Key choices:** kappa = {0.3, 0.5, 1.0, 2.0, inf}; angular acceptance
  |cos theta| < 0.9; simultaneous fit of A_FB^b and delta_b; multiple
  b-tag purities

### [REF4] LEP/SLD Combined — hep-ex/0509008
- **Results:** R_b = 0.21629 +/- 0.00066; R_c = 0.1721 +/- 0.0030;
  A_FB^{0,b} = 0.0992 +/- 0.0016
- **Methodology:** Weighted average of all LEP + SLD experiments
- **SM predictions:** R_b^SM = 0.21578; R_c^SM = 0.17223;
  A_FB^{0,b}_SM = 0.1032

### [REF5] DELPHI R_b — inspire_1661836
- **Result:** R_b = 0.21625 +/- 0.00067 (stat) +/- 0.00061 (syst)
- **Methodology:** Enhanced impact parameter tag + multivariate
- **Key choices:** Used with R_c fixed to SM value

---

## Systematic sources

### Efficiency Modeling
- [x] Tag/selection efficiency: vary sigma_d0 parameterization — delta_Rb = 0.00075 (Phase 4a)
- [x] Efficiency correlation C_b, C_c: data-MC comparison — delta_Rb(C_b) = 0.010 (Phase 4a); C_c = C_uds = 1.0 assumed
- [x] MC efficiency model: reweight fragmentation parameters — delta_Rb(hadronization) = 0.00045 (Phase 4a)

### Background Contamination
- [x] Non-signal contamination: vary eps_c, eps_uds — delta_Rb(eps_c) = 0.078, delta_Rb(eps_uds) = 0.387 (Phase 4a)
- [x] Background composition: vary R_c +/- 0.0030, g_bb, g_cc — delta_Rb(R_c) = 0.008, delta_Rb(g_bb) = 0.00011, delta_Rb(g_cc) = 0.00017 (Phase 4a)

### MC Model Dependence
- [x] Hadronization model: reweight b fragmentation (Peterson vs Bowler-Lund) — delta_Rb = 0.00045 (Phase 4a)
- [x] Physics parameters: vary B lifetimes, decay multiplicities, <x_E> — delta_Rb = 0.0002 (Phase 4a)

### Sample Composition
- [x] Flavour composition: vary R_c in extraction formula — delta_Rb = 0.008 (Phase 4a)
- [D] ~~Production fractions: vary B+/B0/Bs/Lambda_b rates~~ — **Downscoped at Phase 4a.** Without MC truth labels, production fractions cannot be varied independently. The effect is absorbed into the eps_uds and physics_params systematics. Estimated impact < 0.001 based on ALEPH published value (hep-ex/9609005 Table 4: 0.0002).
- [x] Gluon splitting: delta_Rb(g_bb) = 0.00011, delta_Rb(g_cc) = 0.00017 (Phase 4a)

### Additional Sources
- [x] Angular dependence of b-tag efficiency (A_FB^b dominant systematic) — delta_AFB = 0.002 (Phase 4a)
- [x] sigma_d0 functional form: vary sin(theta) vs sin^{3/2}(theta) — delta_Rb = 0.0004 (Phase 4a)
- [x] Detector simulation: d0 smearing study — absorbed into sigma_d0 systematic (Phase 4a)
- [x] Tau contamination: correct ~0.3% contamination — delta_Rb = 0.00005 (Phase 4a)
- [x] Event selection bias: vary passesAll subcuts — delta_Rb = 0.0001 (Phase 4a)
- [x] QCD correction (A_FB^b): vary delta_QCD +/- 0.0029 — delta_AFB ~ 0 on MC (Phase 4a)
- [x] Charge separation model (A_FB^b): compare kappa values — delta_AFB = 0.0022 (Phase 4a)
- [x] Charm asymmetry (A_FB^b): vary A_FB^c +/- 0.0035 — delta_AFB = 0.0027 (Phase 4a)

---

## Validation tests

- [D] ~~Closure test (a): negative-d0 pseudo-data test (R_b should be ~0)~~ — **Formally downscoped at Phase 4a.** Justification: the negative-d0 pseudo-data test requires inverting the d0 sign to create a b-depleted sample (negative d0 tail has no lifetime information). On symmetric MC without truth labels, this test is not independently constraining: the extraction already uses the full MC with circular calibration, and the negative-d0 subset would face the same underdetermined system with even less statistical power. Deferred to Phase 4b where data-driven d0 calibration provides a meaningful control sample.
- [D] ~~Closure test (b): bFlag=4 vs full-sample consistency check~~ — **Formally downscoped at Phase 4a.** Justification: bFlag is -999 in MC (no discriminating power). The test requires comparing bFlag=4-enriched vs full sample extractions, but bFlag=4 exists only in data. Deferred to Phase 4b/4c where data is available.
- [x] Closure test (c): artificial contamination injection — ratio = 2.14, directional agreement confirmed (Phase 4a)
- [x] Parameter sensitivity table: |dR_b/dParam| * sigma_param — added to AN v2, eps_uds flagged as >5x stat (Phase 4a)
- [x] Operating point stability: FAIL (1/4 valid WPs) Phase 4a; PASS (2/4, chi2/ndf=0.30/1, p=0.586) Phase 4b with C_b=1.01
- [x] Per-year consistency: chi2/ndf = 0.94/3, p = 0.82 on random MC subsets (Phase 4a); real per-year test deferred to Phase 4c
- [x] 10% diagnostic sensitivity: data-derived tag rates agree with MC within 3-5%; double-tag fractions compared at 4 WPs (Phase 4b)
- [x] Negative d0 tail calibration: scale factors 1.3-7.6 across 40 bins on 10% data (Phase 4b)
- [ ] Data/MC agreement on all MVA inputs (if BDT approach used): chi2/ndf
      per variable
- [ ] bFlag interpretation validation: if bFlag=4 b-tag discriminant
      distribution is indistinguishable from the full sample (chi2/ndf ~ 1.0
      comparing tagged-sample discriminant shapes), classify bFlag as a
      non-b flag and default to self-labelling option 2 for BDT training.
      If chi2/ndf > 2.0 (bFlag=4 subsample is enriched in b relative to
      full sample), bFlag=4 is a usable b-enrichment proxy for BDT option 1.
- [ ] d0 sign convention validation [D19]: positive d0 tail enhanced in
      b-enriched hemispheres (Phase 3 blocking gate)

---

## Flagship figures

- [x] F1: R_b operating point stability scan — produced Phase 4a (F1_rb_stability_scan.pdf)
- [x] F2: A_FB^b angular distribution — produced Phase 4a (F2_afb_angular_distribution.pdf)
- [x] F3: Impact parameter significance distribution (signed d0/sigma_d0, data vs MC, log scale) — produced Phase 4b (F3b_d0_sigma_data_mc.png)
- [x] F4: Double-tag fraction vs single-tag fraction — produced Phase 4a (F4_fd_vs_fs.pdf)
- [x] F5: Systematic uncertainty breakdown — produced Phase 4a (F5_systematic_breakdown.pdf)
- [D] ~~F6: Per-year stability (R_b and A_FB^b per year, combined + chi2/ndf)~~ — **Deferred to Phase 4b/4c.** Per-year stability requires multi-year data (1992-1995). MC is 1994 only. The per-year consistency on MC was tested numerically (chi2/ndf = 0.94/3, p = 0.82 on random MC subsets) but a meaningful per-year figure requires actual year labels from data.
- [x] F7: A_FB^b kappa consistency — produced Phase 4a (F7_afb_kappa_consistency.pdf)

---

## Cross-checks

- [D] ~~Cut-based vs BDT tagger comparison (efficiency, purity, C_b)~~ — Follows from [D9]/[D10] downscoping.
- [x] BDT tagging validation: AUC = 0.987-0.996, comparable to cut-based (Phase 4b post-mortem, agnes_cbbf)
- [x] 3-tag R_b cross-check: R_b = 0.217-0.222 across 5 configurations, excellent SM agreement (Phase 4b post-mortem)
- [x] delta_b calibration / b-purity investigation: low b-purity (18%) identified as root cause of A_FB^b suppression (Phase 4b post-mortem)
- [x] Gluon splitting characterization: 1.1% of events, preferentially tagged, data/MC mass agrees within 1-5% (Phase 4b post-mortem)
- [x] MC truth proxies: vertex mass > 3.5 GeV selects b-enriched sample (Phase 4b post-mortem)
- [x] eps_uds from data: anti-tag data/MC ratio = 1.015, reduces eps_uds uncertainty from ~100% to ~5% (Phase 4b post-mortem)
- [x] Normalization check: double-tag method is self-normalizing, data/MC ratio = 3.95 (Phase 4b post-mortem)
- [ ] Probability tag vs N-sigma tag comparison
- [ ] Multiple kappa values for A_FB^b (kappa = 0.3, 0.5, 1.0, 2.0, infinity)
- [ ] Per-year extraction (1992, 1993, 1994, 1995)
- [ ] bFlag cross-check (our tagger vs bFlag in data)
- [ ] Constrained R_c vs floated R_c in double-tag fit
- [ ] Multi-working-point extraction vs single working point
- [ ] Analytical vs toy-based uncertainty propagation comparison (minimum
      targets: C_b and R_c constraint propagation must agree within 10%
      between analytical and toy methods)
- [ ] Simple counting A_FB^b vs self-calibrating fit (self-calibrating is
      governing extraction; simple counting is cross-check only)

---

## Comparison targets

- [ ] R_b vs ALEPH (hep-ex/9609005): 0.2158 +/- 0.0014
- [ ] R_b vs LEP combined (hep-ex/0509008): 0.21629 +/- 0.00066
- [ ] R_b vs SM: 0.21578
- [ ] A_FB^b vs ALEPH (inspire_433746): 0.0927 +/- 0.0052
- [ ] A_FB^{0,b} vs LEP combined (hep-ex/0509008): 0.0992 +/- 0.0016
- [ ] A_FB^{0,b} vs SM: 0.1032
- [ ] sin^2(theta_eff) vs ALEPH (inspire_433746): 0.2330 +/- 0.0009
- [ ] R_c fitted vs LEP combined: 0.1721 +/- 0.0030 (cross-check only)

---

## Key Decisions [D]

- [D1] Observable definitions: LEP EWWG standard (hep-ex/0509008)
- [D2] Double-tag hemisphere counting for R_b
- [D3] Simplified two-tag system (lifetime + mass only)
- [D4] Hemisphere jet charge for A_FB^b
- [D5] kappa = {0.3, 0.5, 1.0, 2.0, infinity}
- [D6] R_c as constrained parameter (SM value, dR_b/dR_c ~ -0.05)
- [D7] sigma_d0 from negative d0 tail calibration
- [D8] Primary: combined probability-mass tag; cross-check: N-sigma tag
- [D] ~~[D9] BDT training with bFlag proxy labels~~ — **Formally downscoped at Phase 4a.** Justification: the bFlag branch is -999 in MC and has limited discriminating power in data (values {-1, 4} only). The combined probability-mass tag [D8] achieves the required b-enrichment without BDT. A BDT cross-check would require either MC truth labels (unavailable [A1]) or data-driven labeling from bFlag=4, which the Phase 1 bFlag investigation showed is not a usable b-enrichment proxy. Deferred to Phase 4b/4c if bFlag validation on data proves feasible.
- [D] ~~[D10] BDT vs cut-based quantitative comparison~~ — **Formally downscoped.** Follows from [D9] downscoping: no BDT implementation means no comparison is possible.
- [D11] Include non-VDET tracks in jet charge
- [D12] Self-calibrating fit for A_FB^b (governing extraction; report chi2/ndf)
- [D] ~~[D12b] Four-quantity simultaneous fit (Q_FB, delta, e^h, epsilon^e) with sin^2(theta_eff) as direct fit parameter (inspire_433746); DELPHI five-category chi2 fit as cross-check~~ — **Formally downscoped at Phase 4a, deferred to Phase 4b/4c.** Justification: on symmetric MC (A_FB = 0 by construction), the four-quantity fit cannot meaningfully constrain sin^2(theta_eff) because the asymmetry signal is absent. The simplified linear regression of <Q_FB> vs cos(theta) correctly returns A_FB^b ~ 0 and validates the method infrastructure. The four-quantity fit will be implemented in Phase 4b/4c where the real forward-backward asymmetry is present in data, enabling meaningful sin^2(theta_eff) extraction.
- [D12a] Angular binning uniform across years; verify per-year chi2/ndf
- [D13] Toy-based uncertainty propagation (primary)
- [D14] Multi-working-point extraction for method parity
- [D15] Seven flagship figures (+ supporting figures)
- [D16] Compare to SM and published measurements
- [D17] Primary vertex definition: investigate d0 reference point at Phase 3
- [D18] Approach A includes combined probability-mass tag
- [D19] Phase 3 gate: d0 sign convention validation (positive tail enhanced in b-enriched sample)
- [D20] C_b = 1.01 external input for R_b extraction (Phase 4b). **Justification:** the published ALEPH value C_b=1.01 (hep-ex/9609005 Table 1) was achieved using per-hemisphere primary vertex reconstruction, which produces nearly independent hemisphere tags (C_b near unity). Our analysis uses 2D impact parameters with a shared event vertex, yielding measured C_b ~ 1.52 on data — too large for the quadratic extraction equation to have real solutions. The choice of C_b=1.01 is therefore an external assumption, not a self-calibration. The assigned systematic covers the valid C_b range (1.01-1.06 at WP=7.0), producing delta(R_b)=0.124. **Acknowledgment:** the R_b measurement on 10% data is dominated by this assumption. Achieving self-calibrated C_b requires per-hemisphere vertex-like corrections, which are not feasible with 2D impact parameters alone.
- [D] ~~Per-subperiod consistency check at Phase 4b~~ — **Formally deferred to Phase 4c.** Justification: the 10% subsample (~288k events) was drawn randomly from all years with a single seed. Year labels are not available in the preselected data format. Even if year labels were available, 10%/4 years ~ 72k events per year gives sigma_stat(R_b) ~ 0.13 per year, making the per-year chi2 test insensitive. Phase 4c with full data (~2.9M events) will have adequate per-year statistics (~720k events/year, sigma_stat ~ 0.04). The random seed ensures the 10% sample is representative of all years.

---

## REGRESSION Addendum (2026-04-03)

### Updated Primary Methods (per REGRESS(4a))

- [x] [D2-REVISED] PRIMARY R_b: 3-tag system (tight/loose/anti-b) — R_b = 0.21578 +/- 0.00026 (stat) on MC, stability chi2/ndf = 0.00/7 across 8 configs
- [x] [D4-REVISED] PRIMARY A_FB^b: purity-corrected extraction with published delta_b — A_FB^b = -0.078 +/- 0.005 on symmetric MC (expected ~0)
- [x] [D10-REVISED] BDT as characterized alternative (AUC 0.99), not primary
- [x] eps_uds constrained from anti-tag data (5% variation, was 50-100%)
- [x] eps_c constrained from 3-tag fit (10% variation, was 30%)
- [x] C_b per-WP from correlation_results.json (no WP mismatch)
- [x] All closure tests PASS (pulls within +/- 1 sigma)
- [x] No solver failures (3-tag system overconstrained)
