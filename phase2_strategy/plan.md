# Phase 2 Strategy Plan — peter_b030

## Strategy Elements to Address

1. **Observable definitions** — R_b, R_c, A_FB^b with exact formulas,
   verified against LEP EWWG combination (hep-ex/0509008) and ALEPH
   papers (hep-ex/9609005, inspire_433746)

2. **Double-tag method formalism** — single-tag and double-tag equations
   from inspire_416138, hemisphere correlation factors, self-calibrating
   property

3. **Selection approaches** (>=2 qualitatively different):
   - Approach A: Signed impact parameter significance (lifetime tag) —
     cut-based, using d0 with estimated sigma_d0
   - Approach B: BDT-based tagger using multiple track/event variables
     (d0, z0, track multiplicity, track pT, nvdet hits)
   - MVA feasibility assessment: available without truth labels using
     bFlag from data as proxy or negative d0 tail calibration

4. **A_FB^b method** — hemisphere jet charge with multiple kappa values,
   thrust axis for quark direction, lifetime tag for b purity

5. **R_c strategy** — constrained by no D meson reconstruction (no PID).
   Must use double-tag method with lifetime information to separate c
   from uds, or adopt published R_c as external input

6. **Systematic uncertainty plan** — enumerate every source from
   conventions/extraction.md:
   - Efficiency modeling (tag efficiency, correlation, MC model)
   - Background contamination (non-signal, composition)
   - MC model dependence (hadronization, physics parameters)
   - Sample composition (flavour fractions, production ratios)

7. **Precision estimates** — grounded in Phase 1 statistics and reference
   analysis values

8. **Reference analysis table** — ALEPH R_b, ALEPH A_FB^b, LEP combined,
   DELPHI R_b with numerical results

9. **Mitigation strategies** for every Phase 1 constraint:
   - [A1] No MC truth labels
   - [A2] d0 sentinel fraction (~36%)
   - [A3] sigma_d0 not stored
   - [A4] MC 1994 only
   - [A5] No PID
   - [A6] bFlag absent in MC

10. **Flagship figures** (~6 money plots)

11. **Backgrounds enumeration** — classified by type

12. **Constraint/limitation/decision labels** throughout

## Phase 1 Constraints and Planned Mitigations

| Constraint | Impact | Mitigation Direction |
|------------|--------|---------------------|
| No MC truth | Cannot calibrate tagger on MC truth | Double-tag self-calibration; data bFlag as proxy; negative d0 tail for resolution |
| 36% d0 sentinel | Reduced tagging statistics | Require VDET hits (nvdet > 0); track quality cuts |
| No sigma_d0 | Cannot compute significance directly | Parameterize from ALEPH publications (~25 micron + 1/p_T term); calibrate on negative d0 tail |
| MC 1994 only | Year-dependent systematics uncovered | Per-year data extraction as cross-check; assign conservative systematic |
| No PID | No kaon/pion separation for charm | Use lifetime-only tagging; R_c from external input or softer lifetime cut |
| bFlag=-999 in MC | Cannot use bFlag for MC studies | Build own tagger from d0; bFlag used only as data cross-check |

## Deliverables

1. `outputs/STRATEGY.md` — complete analysis strategy
2. `../COMMITMENTS.md` — binding commitments with [REF] entries
3. Updated `experiment_log.md`
4. Session log in `logs/`
