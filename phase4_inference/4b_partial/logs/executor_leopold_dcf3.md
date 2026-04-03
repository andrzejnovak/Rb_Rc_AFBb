# Executor Session Log: leopold_dcf3

## Session: Post-mortem investigations for Doc 4b ITERATE gate
Date: 2026-04-03

## Tasks Completed

### Task 1: Delta_b Calibration from Data (CRITICAL)
**Script:** `src/delta_b_calibration.py`
**Output:** `outputs/delta_b_calibration.json`

**Key findings:**
1. sigma(Q_h) was used as delta_b in the old method. For kappa=2.0, sigma(Q_h)=0.59 vs published delta_b=0.579 -- only 2% overestimate. For kappa=0.3, sigma(Q_h)=0.166 vs published=0.162 -- 2.5% overestimate. **delta_b miscalibration is NOT the primary cause of A_FB^b suppression.**

2. **The real issue is b-purity.** At the tightest calibrated WP (10.0):
   - eps_b = 0.15, eps_c = 0.44, eps_uds = 0.11
   - b-purity f_b = 18%, charm purity f_c = 42%, uds f_uds = 39%
   - Our tag tags CHARM more efficiently than b (eps_c >> eps_b)
   
3. The observed Q_FB slope includes large charm contribution:
   - b contribution: ~50% of total slope
   - c contribution: ~45% of total slope
   - The charm contribution is POSITIVE (same sign as b), inflating the raw extraction

4. **Improvement with purity correction:**
   - Old method (slope/sigma_Q_h): A_FB^b ~ 0.009-0.014
   - Purity-corrected (slope/(f_b*delta_b)): A_FB^b ~ 0.05-0.08
   - Charm-corrected: varies, sensitive to delta_c assumption
   - SM value: A_FB_b(obs) = 0.0995

5. The purity-corrected extraction at kappa=2.0 gives A_FB^b ~ 0.08, which is within ~2sigma of the SM value, representing a significant improvement.

### Task 2: MC Truth Proxies
**Script:** `src/mc_truth_proxies.py`
**Output:** `outputs/mc_truth_proxies.json`

**Key findings:**
- pid and process are sentinels (-999, -1) in MC -- no truth labels available
- Vertex mass provides a useful b-enriched proxy:
  - mass > 3.5 GeV: 6% of events, mean hem_tag=12.5 (strongly b-enriched)
  - mass 1.0-3.5 GeV: 31% of events, mean hem_tag=8.9 (c-enriched)
  - mass < 1.0 GeV: 63% of events, mean hem_tag=3.6 (uds-enriched)
- High-pT lepton proxy tags 76% of events (too inclusive)
- Displaced track multiplicity >= 3: 35% of events, strong overlap with existing tag
- Missing momentum provides no discrimination between mass-tagged categories

### Task 3: BDT Tagging
**Script:** `src/bdt_tag.py`
**Output:** `outputs/bdt_tag_results.json`

**Key findings:**
- BDT achieves AUC 0.987-0.996 (no overtraining: train-test AUC diff < 0.001)
- Dominant features: hem_mass (67%), max_sig (20%), n_above2 (7%)
- BDT provides smooth score (better efficiency-purity tradeoff)
- At fixed purity, BDT has ~5-10% higher efficiency than hard cut
- **Limitation:** BDT is self-labeled, trained on same information as cut-based tag. Cannot overcome the fundamental b/c discrimination limit without new variables.

### Task 4: 3-Tag System
**Script:** `src/three_tag_system.py`
**Output:** `outputs/three_tag_results.json`

**Key findings:**
- 3-tag system (tight/loose/anti) provides additional constraints
- Anti-tag (low score) is 62-83% of events depending on thresholds
- Data/MC agreement: tight 96%, loose 99%, anti 102% -- consistent
- R_b extraction from 3-tag: 0.217-0.222 (SM: 0.216) -- good agreement
- The anti-tag directly constrains eps_uds (see Task 6)

### Task 5: Gluon Splitting
**Script:** `src/gluon_splitting.py`
**Output:** `outputs/gluon_splitting_results.json`

**Key findings:**
- Dijet mass mean ~84 GeV (lower than MZ due to charged-only, pion mass)
- Low mass (< 60 GeV) gluon splitting candidates: 1.1% of MC events
- Tag rate in low-mass events (0.38) > high-mass (0.31) -- gluon splitting events are preferentially tagged
- Very low mass (< 30 GeV): only 16 events, too rare to matter
- Data/MC hemisphere mass agreement: within 1-5% across bins

### Task 6: eps_uds Constraints
**Integrated into Task 4 script**

**Key findings:**
- Anti-tag (complement of tight tag) constrains eps_uds_not_tight ~ 0.90
- eps_uds_tight (MC) = 0.114, so eps_uds_loose ~ 0.90 - 0.886 = 0.014
- Anti-tag data/MC ratio: 1.015 (1.5% excess in data), providing direct constraint
- Sensitivity: d(f_anti)/d(R_b) ~ 0.000037 per 0.001 R_b -- modest

### Task 7: Data/MC Normalization
**Script:** `src/normalization_check.py`
**Output:** `outputs/normalization_check.json`

**Key findings:**
- Data: 2,887,261 events (1992-1995), MC: 730,365 events (1994 only)
- Data/MC ratio: 3.95 (expected, since data covers 4 years, MC only 1)
- Observed/expected from L*sigma: 0.72 (reasonable after preselection acceptance)
- The double-tag method uses fractions (self-normalizing), so absolute normalization does not affect R_b or A_FB^b extraction
- Data/MC comparison plots should scale MC by 3.95 or by L*sigma

## Critical Diagnosis: Root Cause of A_FB^b Suppression

The A_FB^b was suppressed 10x because:

1. **The old code used delta_b = sigma(Q_h) to extract A_FB^b via: A_FB^b = slope / delta_b**
2. This is incorrect because it ignores the b-purity of the sample
3. The correct formula is: slope = f_b * delta_b * A_FB_b + f_c * delta_c * A_FB_c
4. With f_b = 0.18, f_c = 0.42 at WP 10, the b contribution is only ~50% of the slope
5. After purity and charm corrections, A_FB^b improves from ~0.01 to ~0.05-0.08

The fundamental limitation is that **eps_c > eps_b** in our tag. A proper b-tag at LEP achieved eps_b >> eps_c (30-40% vs 5-10%), giving f_b > 60%. Our d0-significance tag doesn't discriminate B from D vertices effectively because both produce displaced tracks. The vertex mass provides the best discrimination: B hadrons (mass > 3.5 GeV) have distinctly higher secondary vertex mass than D mesons (mass ~ 2 GeV).

## Files Created
- `src/delta_b_calibration.py`
- `src/mc_truth_proxies.py`
- `src/bdt_tag.py`
- `src/three_tag_system.py`
- `src/gluon_splitting.py`
- `src/normalization_check.py`
- `outputs/delta_b_calibration.json`
- `outputs/mc_truth_proxies.json`
- `outputs/bdt_tag_results.json`
- `outputs/three_tag_results.json`
- `outputs/gluon_splitting_results.json`
- `outputs/normalization_check.json`
