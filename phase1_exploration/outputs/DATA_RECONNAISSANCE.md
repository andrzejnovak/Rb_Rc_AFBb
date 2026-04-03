# Data Reconnaissance — Phase 1

Session: fabiola_b942 | Date: 2026-04-02

## Summary

Explored 6 ALEPH data files (1992-1995) and 41 MC files (1994 only) containing
reconstructed hadronic Z decay events. The data are stored in ROOT TTrees with
151 event/track-level branches plus multiple jet tree variants. Key findings:
(1) no MC truth flavour information is available, (2) track impact parameter d0
is present but ~36% of tracks have sentinel values (-999), (3) per-track weights
exist with mean ~1.02, (4) data has been pre-selected at ntuple production level
(passesNTupleAfterCut = 1 for all events), (5) bFlag exists in data but is -999
in MC, (6) particle ID (pid) is unavailable (all -999).

## File Inventory

### Data Files

| File | Year | Events | Size (MB) |
|------|------|--------|-----------|
| LEP1Data1992_recons_aftercut-MERGED.root | 1992 | 551,474 | 4,060 |
| LEP1Data1993_recons_aftercut-MERGED.root | 1993 | 538,601 | 3,949 |
| LEP1Data1994P1_recons_aftercut-MERGED.root | 1994 P1 | 433,947 | 3,179 |
| LEP1Data1994P2_recons_aftercut-MERGED.root | 1994 P2 | 447,844 | 3,280 |
| LEP1Data1994P3_recons_aftercut-MERGED.root | 1994 P3 | 483,649 | 3,546 |
| LEP1Data1995_recons_aftercut-MERGED.root | 1995 | 595,095 | 4,379 |
| **Total** | | **3,050,610** | **22,393** |

### MC Files

| Files | Year | Total Events | Files |
|-------|------|-------------|-------|
| LEP1MC1994_recons_aftercut-001..041 | 1994 | ~7.8M (est.) | 41 |

MC is 1994 only. Coverage gap: no MC for 1992, 1993, 1995. This must be
addressed in Phase 4 uncertainty treatment.

## Tree Structure

Each ROOT file contains the main tree `t` plus 8 jet trees and 2 boosted-frame
event trees:

### Main tree `t` — 151 branches

**Event-level identification:**
- `EventNo` (int32), `RunNo` (int32), `year` (int32), `subDir` (int32)
- `process` (int32): always -1 (both data and MC)
- `isMC` (bool): 0 for data, 1 for MC
- `uniqueID` (uint64)

**Event-level physics:**
- `Energy` (float): beam energy
- `bFlag` (int32): In data: {-1, 4}; in MC: always -999
- `particleWeight` (float): event weight
- `bx`, `by`, `ebx`, `eby` (float): beam position and errors

**Track-level arrays (per event, variable length):**
- Kinematics: `px[]`, `py[]`, `pz[]`, `pt[]`, `pmag[]`, `mass[]`
- Angular: `eta[]`, `theta[]`, `phi[]`, `rap[]`
- Charge: `charge[]` (int16): values {-1, 0, 1}
- Impact parameters: `d0[]`, `z0[]` (float) — KEY for b-tagging
- Track quality: `highPurity[]` (bool), `ntpc[]`, `nitc[]`, `nvdet[]` (int16)
- PID: `pid[]` (int32): always -999 — NO particle ID
- Particle weight flag: `pwflag[]` (int16): values {0,1,2,3,4,5}
- Per-track weight: `weight[]` (float): mean ~1.02, range [0.074, 1.833]
- Vertex: `vx[]`, `vy[]`, `vz[]` (float)

**Thrust-frame variables (multiple axis definitions):**
- `pt_wrtThr[]`, `eta_wrtThr[]`, etc. — w.r.t. standard thrust axis
- Similar sets for charged thrust, neutral thrust, corrected thrust, missing-p thrust

**Acceptance corrections:**
- `passesArtificAccept[]` (bool), `artificAcceptEffCorrection[]` (float)

**Event selection flags:**
- `passesNTupleAfterCut` (bool): always 1 — pre-selection already applied
- `passesTotalChgEnergyMin` (bool): ~100% pass
- `passesNTrkMin` (bool): ~100% pass
- `passesSTheta` (bool): ~98% pass
- `passesMissP` (bool): ~96% pass
- `passesISR` (bool): ~99% pass
- `passesWW` (bool): ~99% pass
- `passesNeuNch` (bool): ~99.6% pass
- `passesAll` (bool): ~94% pass (intersection of all above)

**Event shape variables:**
- `Thrust`, `TTheta`, `TPhi` — standard thrust axis
- `Sphericity`, `STheta`, `SPhi`, `Aplanarity`
- Linearized versions: `Sphericity_linearized`, `C_linearized`, `D_linearized`
- Multiple thrust variants: charged, neutral, corrected, missing-p

**Multiplicity:**
- `nParticle` (int32): total particles per event
- `nChargedHadrons` (int32): charged hadrons
- `nChargedHadronsHP` (int32): high-purity charged hadrons
- `nChargedHadronsHP_Corrected` (float): corrected multiplicity

**Missing momentum:**
- `missP`, `missPt`, `missTheta`, `missPhi` (float)
- `missChargedP`, `missChargedPt`, `missChargedTheta`, `missChargedPhi` (float)

### Jet Trees (8 variants)

Each with branches: `nref`, `jtpt[]`, `jteta[]`, `jtphi[]`, `jtm[]`, `jtN[]`,
`jtNPW[][6]`, `jtptFracPW[][6]`, plus SoftDrop variables.

| Tree | Algorithm | Entries match `t` |
|------|-----------|-------------------|
| akR4ESchemeJetTree | anti-kT R=0.4, E-scheme | Yes |
| akR4WTAmodpSchemeJetTree | anti-kT R=0.4, WTA | Yes |
| akR8ESchemeJetTree | anti-kT R=0.8, E-scheme | Yes |
| akR8WTAmodpSchemeJetTree | anti-kT R=0.8, WTA | Yes |
| ktN2ESchemeJetTree | kT N=2, E-scheme | Yes |
| ktN2WTAmodpSchemeJetTree | kT N=2, WTA | Yes |
| BoostedWTAR8Evt | Boosted frame R=0.8 | Yes |
| BoostedWTAktN2Evt | Boosted frame kT N=2 | Yes |

## Integer/Flag Branch Survey

### Data (1994 P1 sample, 2000 events)

| Branch | Unique values | Range | Mean | Notes |
|--------|--------------|-------|------|-------|
| year | 1 | [1994, 1994] | 1994 | Single year per file |
| subDir | 1 | [-999, -999] | -999 | Sentinel — not meaningful |
| process | 1 | [-1, -1] | -1 | Not populated |
| isMC | 1 | [0, 0] | 0 | Correctly flagged as data |
| bFlag | 2 | {-1, 4} | 3.23 | **Critical**: -1 = untagged (~6%), 4 = tagged (~94%) |
| passesAll | 2 | {0, 1} | 0.94 | 94% pass all cuts |

### MC (first file, 2000 events)

| Branch | Unique values | Range | Mean | Notes |
|--------|--------------|-------|------|-------|
| isMC | 1 | [1, 1] | 1 | Correctly flagged |
| bFlag | 1 | [-999, -999] | -999 | **NO b-tag info in MC** |
| RunNo | 1 | [10, 10] | 10 | Single run number |
| subDir | 1 | [-1, -1] | -1 | Different sentinel from data |

### Branch Comparison (data vs MC)

- **MC-only branches: NONE** — identical branch structure
- **Data-only branches: NONE**
- **Common branches:** 151

**Critical finding:** There are NO MC-truth branches. No generator-level
flavour labels, no parton-level information, no truth matching variables.
This is the single most important constraint for Phase 2 strategy.

## Truth-Level Information

### Available truth information: NONE

The MC files have the same branch schema as data. There are:
- No generator-level particle arrays
- No truth flavour labels (bFlag is -999 in MC)
- No parton-level quantities
- No truth matching variables
- No generator-level thrust axis

### Implications for the analysis

1. **b-tagging efficiency calibration** cannot use MC truth directly. Must use
   data-driven methods or the self-calibrating property of the double-tag method.
2. **MC closure tests** cannot compare to truth labels. Must use the bFlag from
   data as a proxy or rely on the self-calibrating extraction.
3. **The physics prompt suggests** "If you lack MC truth info, you could derive
   approximate truth from studying the decay chain. Maybe you can find neutrino
   truth flavour." This requires investigating whether the MC stores parton-level
   information accessible through decay chain reconstruction.
4. **Alternative approach:** The `process` branch (always -1) does not distinguish
   Z→bb from Z→cc from Z→light. Without truth labels, the analysis must rely
   entirely on lifetime-based tagging and the double-tag method's self-calibrating
   property.

## Pre-Applied Selections

All events have `passesNTupleAfterCut = True`, meaning the data was pre-selected
at ntuple production level. The selection includes:
- Total charged energy minimum
- Minimum track requirement
- Sphericity theta cut
- Missing momentum cut
- ISR rejection
- WW rejection
- Neutral/charged consistency

The `passesAll` flag (intersection of all individual cuts) is ~94% efficient,
meaning ~6% of events fail at least one additional quality cut beyond the base
ntuple selection.

### Published yield cross-check

From the ALEPH A_FB paper (inspire_433746, Table 1), the total hadronic sample
after selection for 1991-1995 was approximately 4.1 million events. Our total
across 1992-1995 is 3,050,610, which is consistent given:
- We lack 1991 data (the earliest year is 1992)
- The "aftercut" pre-selection further reduces the sample
- The ratio ~3.05M/4.10M ≈ 74% is reasonable for pre-selection efficiency

## Data Quality Assessment

### NaN/Inf check
- No NaN or inf values found in event-level float branches (Energy, Thrust,
  Sphericity, etc.)
- No NaN in track-level kinematic arrays (pt, eta, phi)

### Sentinel values
- `d0`, `z0`: ~36% of tracks have value -999 (sentinel for tracks without
  vertex detector hits). Non-sentinel d0 values range [-0.5, 0.5] cm.
- `pid`: always -999 — particle ID not available
- `ntpc`, `nitc`, `nvdet`: many values at -127 (sentinel for tracks not
  reconstructed in that detector component)

### Per-track weights
- Mean ~1.02 in both data and MC (consistent)
- Range [0.074, 1.833] — non-trivial weights that MUST be applied
- Standard deviation ~0.04 — most weights are near 1.0

### Data/MC agreement (from 5000-event survey)

Variable distributions show reasonable agreement:
- **Thrust:** Good agreement across full range
- **Nch:** Good agreement, slight differences at high multiplicity
- **d0:** Reasonable agreement in core; tails show some discrepancy
- **cos(theta_thrust):** Expected 1+cos²θ shape observed; good agreement
- **Sphericity:** Good agreement
- **Track pT:** Good agreement over 3 orders of magnitude
- **Track weight:** Excellent agreement between data and MC

### bFlag in data
- bFlag = -1: ~6% of events (untagged)
- bFlag = 4: ~94% of events (tagged)
- This appears to be a pre-existing b-tag flag. Its exact definition needs
  investigation from the ALEPH R_b papers.

## Key Variables for the Analysis

### b-tagging variables
1. **d0 (impact parameter):** Available but ~36% sentinel. Core width ~0.02 cm
   with extended tails from heavy-flavour decays. This is the primary
   lifetime tagging variable.
2. **z0 (longitudinal impact parameter):** Similar sentinel fraction.
3. **Track multiplicity (nChargedHadrons):** Mean ~19, useful for mass tag.
4. **Track pT:** Useful for lepton tag (high-pT leptons from b→l).

### A_FB^b variables
1. **TTheta (thrust axis polar angle):** cos(TTheta) gives the production angle.
2. **charge[]:** Per-track charge for jet charge reconstruction.
3. **Thrust:** Event shape variable, also used for hemisphere definition.

### Missing variables
- **Impact parameter significance (d0/sigma_d0):** sigma_d0 is not stored.
  Must be estimated from tracking resolution (ntpc, nitc, nvdet hits) or
  from the negative d0 tail.
- **Secondary vertex reconstruction:** Not pre-computed. Must be built from
  track d0, z0, vx, vy, vz.
- **Particle ID:** Not available (pid = -999 everywhere). Cannot use
  kaon/pion separation for flavour tagging.

## Figures

| Figure | File | Description |
|--------|------|-------------|
| F1 | data_mc_nch_fabiola_b942.png | Charged multiplicity data/MC |
| F2 | data_mc_thrust_fabiola_b942.png | Thrust distribution data/MC |
| F3 | data_mc_d0_fabiola_b942.png | Impact parameter d0 data/MC |
| F4 | data_mc_absd0_fabiola_b942.png | |d0| distribution (log scale) |
| F5 | data_mc_sphericity_fabiola_b942.png | Sphericity data/MC |
| F6 | data_mc_costheta_fabiola_b942.png | cos(theta_thrust) data/MC |
| F7 | data_mc_trackpt_fabiola_b942.png | Track pT data/MC |
| F8 | data_mc_trackweight_fabiola_b942.png | Track weight data/MC |

## Open Issues for Phase 2

1. **No MC truth labels.** This is the critical constraint. Phase 2 must design
   a strategy that works without truth flavour information.
2. **Impact parameter significance** must be computed from available variables
   (d0, tracking detector hits, track momentum).
3. **d0 sentinel fraction (~36%)** — need to understand which tracks lack d0.
   Likely tracks without VDET hits. These tracks cannot be used for lifetime
   tagging but can contribute to jet charge.
4. **bFlag interpretation** — the bFlag=4 in data (absent in MC) suggests
   a pre-existing lifetime tag. Need to verify whether this is a quality
   flag or a physics tag.
5. **MC coverage** — MC is 1994 only. Must handle year-dependent detector
   effects carefully.
6. **Per-track weights** are non-trivial and must be used in all analyses.

## Code Reference

- `pixi run py phase1_exploration/src/explore_files.py` — file structure survey
- `pixi run py phase1_exploration/src/survey_branches.py` — branch and variable survey
- `pixi run py phase1_exploration/src/survey_variables.py` — distribution plots
