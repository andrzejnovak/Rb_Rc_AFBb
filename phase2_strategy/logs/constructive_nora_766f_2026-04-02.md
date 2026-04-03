# Session Log — Constructive Reviewer
# Session: nora_766f | Date: 2026-04-02

## Role
Constructive reviewer for Phase 2 (Strategy). Strengthening the analysis
and flagging genuine errors as Category A.

## Inputs read

1. `agents/constructive_reviewer.md` — role definition and prompt template
2. `TOGGLES.md` — MCP_LEP_CORPUS=true, MCP_ALPHAXIV=false
3. `phase2_strategy/outputs/STRATEGY.md` — primary artifact (read in three
   chunks due to size: lines 1-300, 300-600, 600-900+)
4. `phase1_exploration/outputs/DATA_RECONNAISSANCE.md` — upstream artifact
5. `phase1_exploration/outputs/INPUT_INVENTORY.md` — upstream artifact
6. `phase1_exploration/outputs/LITERATURE_SURVEY.md` — upstream artifact
7. `experiment_log.md` — session history (2 entries: Phase 1, Phase 2)
8. `COMMITMENTS.md` — binding commitments as of Phase 2
9. `conventions/extraction.md` — applicable technique conventions
10. `REVIEW_CONCERNS.md` — empty at session start

## MCP corpus searches performed (MCP_LEP_CORPUS=true)

1. "hemisphere correlation factor double tag R_b systematic"
   → hep-ex/9609005: four-variable protocol (cos(theta), PV error, jet momenta, y_3)
   → inspire_1660341 (DELPHI): C_b matrix definition and asymptotic estimation

2. "A_FB b quark charge separation delta_b calibration systematic"
   → inspire_1661252 (DELPHI): neural network charge tag, A_FB^b = 0.0931±0.0034±0.0017
   → inspire_1661397, inspire_1660891, inspire_1661115 (DELPHI): differential
     asymmetry binning; signed cos(theta) bins; hemisphere correlation corrections

3. "R_c double tag charm efficiency extraction method"
   → inspire_416138: double-tag method formalism including charm efficiency
   → inspire_1661805 (DELPHI): R_b and R_c category descriptions

4. "primary vertex reconstruction hemisphere b-tag ALEPH VDET impact parameter"
   → hep-ex/9609005: per-hemisphere primary vertex reconstruction confirmed
   → inspire_433306: d0 smearing relative to primary vertex errors
   → inspire_1661462 (DELPHI): beam-spot-constrained iterative vertex fit

5. "b fragmentation function Peterson Bowler systematic reweighting LEP"
   → inspire_1660220 (DELPHI), inspire_669505 (DELPHI): reweighting procedure
     for Peterson/Bowler/Lund fragmentation functions confirmed

6. "hemisphere mass tag b quark secondary vertex invariant mass"
   → hep-ex/9609005: confirms mass tag is a DISTINCT algorithm from P_hem,
     combined for Q tag. Tracks combined until invariant mass > 1.8 GeV/c^2.

## Key findings

### Category A (2)
- A1: Primary vertex reconstruction strategy is unspecified. The d0 significance
  depends critically on what vertex d0 is measured relative to (beam spot only
  vs. fitted event vertex). This affects the tagging discriminant and C_b.
  Resolution: investigate stored d0 definition; add [D] label for vertex choice.

- A2: The hemisphere invariant mass tag (second component of ALEPH Q tag) is not
  committed to in Approach A, creating scope ambiguity. The mass tag is implementable
  from available 4-vector branches and provides significant purity improvement.
  Resolution: commit explicitly to combined probability+mass tag in [D8].

### Category B (4)
- B1: R_c cross-check sensitivity unestimated; operating point undefined.
- B2: Angular binning not year-dependent despite known VDET change in 1994.
- B3: y_3 omitted from hemisphere correlation check variables (ALEPH-prescribed).
- B4: A_FB^b flagship figure missing background-subtracted version and kappa comparison.

### Category C (6)
- C1: Stability scan conflates robustness with bias bound.
- C2: sigma_d0 calibration binning not specified.
- C3: |cos(theta)| vs signed cos(theta) ambiguity in [D12].
- C4: SM vs LEP-measured R_c constraint value undocumented.
- C5: Per-year chi2/ndf threshold not specified.
- C6: Tagging discriminant (P_hem output) missing from flagship figures.

## Output written

- `phase2_strategy/review/constructive/STRATEGY_CONSTRUCTIVE_REVIEW_nora_766f_2026-04-02.md`
  Full review with 2 Category A, 4 Category B, 6 Category C findings.

## Assessment

Strategy is fundamentally sound. The double-tag self-calibration approach
is optimal given the no-MC-truth constraint. The systematic plan covers all
required sources from conventions/extraction.md. The A findings are fixable
within Phase 2/3 without changing the core approach. The most impactful
resolution is A1 (primary vertex definition) which requires a quick data check,
and A2 (mass tag commitment) which requires a one-line change to [D8].
