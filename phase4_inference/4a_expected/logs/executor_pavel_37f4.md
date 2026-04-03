# Session Log: executor_pavel_37f4

Date: 2026-04-03
Phase: 4a (regression rewrite)
Trigger: REGRESS(4a) from human gate

## Task

Rewrite Phase 4a to use:
1. 3-tag system as PRIMARY R_b method
2. Purity-corrected A_FB^b as PRIMARY
3. eps_uds constrained from anti-tag data
4. Proper systematic treatment (no solver fails)

## Plan

### Scripts to write/update in phase4_inference/4a_expected/src/:
1. `three_tag_rb_extraction.py` - 3-tag R_b with toy uncertainties
2. `purity_corrected_afb.py` - Purity-corrected A_FB^b extraction
3. `systematics_v2.py` - Updated systematics with 3-tag constraints
4. `write_results_json_v2.py` - Updated results aggregation
5. `plot_phase4a_v2.py` - Publication-quality figures

### Key changes from original:
- R_b: move from 2-tag (extract_rb) to 3-tag system
- A_FB^b: use published delta_b values and MC-calibrated purities
- eps_uds: constrain from anti-tag fraction instead of floating with 50-100%
- eps_c: use 3-tag constraint instead of 30% variation
- C_b: per-WP values already available from correlation_results.json

## Progress

- [x] Read existing codebase and understand state
- [x] Update STRATEGY.md (Section 17 addendum)
- [x] Write three_tag_rb_extraction.py — R_b = 0.21578 +/- 0.00026
- [x] Write purity_corrected_afb.py — A_FB^b = -0.078 +/- 0.005
- [x] Write systematics_v2.py — total syst 0.065 (3x improvement)
- [x] Write write_results_json_v2.py — 4 JSON files to analysis_note/results/
- [x] Write plot_phase4a_v2.py — 7 figures produced
- [x] Run full chain — all scripts complete
- [x] Update COMMITMENTS.md — regression addendum added
- [x] Write INFERENCE_EXPECTED.md — complete rewrite
- [x] Update pixi.toml tasks
- [x] Update experiment_log.md
