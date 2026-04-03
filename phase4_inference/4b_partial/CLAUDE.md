# Phase 4b: Inference — 10% Data Validation

> Read `methodology/03-phases.md` → "Phase 4b" for full requirements.

You are validating the analysis with **10% of the data** for a
**measurement** analysis.
Data access: **10% data subsample (fixed random seed) + MC normalized to 10% luminosity.**

## Output artifacts

- `outputs/INFERENCE_PARTIAL.md` — inference artifact with 10% results
- `analysis_note/results/*.json` — updated with 10% results
- `outputs/figures/*.pdf` — regenerated result figures with 10% data

## What this phase does

- Run full analysis chain on 10% data subsample
- Compare to Phase 4a expected (overlay, chi2)
- Evaluate GoF, NP pulls, impact ranking on 10% data
- Flag discrepancies with expected results
- Regenerate result figures with 10% data
- For extraction: include diagnostics sensitive to data/MC differences
  (not just the final quantity)

## Figure registry (mandatory)

Register all figures in `outputs/FIGURES.json` per
`methodology/appendix-plotting.md` (full schema and fields defined there).

## Key requirements

- 10% data selected with fixed documented random seed
- MC normalized to 10% luminosity
- Compare to Phase 4a expected — should be compatible within
  large uncertainties
- Fix problems BEFORE seeing more data
- Update `analysis_note/results/` JSON with 10% results
- Update `COMMITMENTS.md`

## Applicable conventions

- `conventions/unfolding.md` — for unfolded measurements
- `conventions/extraction.md` — for extraction/counting measurements

The technique selected in Phase 2 determines which file applies.
Read the "When this applies" section of each to confirm.

## Review

**1-bot + plot validator** [blocking] — critical reviewer checks 10%
results for consistency with expected. Plot validator checks all figures.
Must PASS before Doc 4b begins.

## Completion Criteria (ALL must be true)
- [ ] 10% subsample processed (fixed seed)
- [ ] Comparison to Phase 4a expected results with figures
- [ ] GoF/NP diagnostics
- [ ] Per-subperiod consistency check
- [ ] All figures saved AND registered in FIGURES.json
- [ ] Results JSON updated in analysis_note/results/
- [ ] COMMITMENTS.md updated
- [ ] Every finding has a Resolution + Evidence section
