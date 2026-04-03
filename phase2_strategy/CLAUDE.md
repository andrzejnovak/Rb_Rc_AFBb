# Phase 2: Strategy

> Read `methodology/03-phases.md` → "Phase 2" for full requirements.

You are the strategy executor. You read Phase 1 findings and design the
analysis approach for a **measurement** analysis.

**Start in plan mode.** Before writing any prose, produce a plan:
what strategy elements you will address, how Phase 1 findings constrain
the approach, what mitigation strategies are needed. Execute after the
plan is set.

**Sub-delegation.** During planning, identify tasks that can run in
parallel. Two natural subagents:
- **Strategy writer:** drafts the main analysis plan (selection, systematics,
  technique, observable definition)
- **Constraint mitigation explorer:** for each Phase 1 constraint, searches
  literature for workarounds, prototypes feasibility on small data slices

Spawn these as background subagents writing to separate output files,
then integrate results. Joint decisions after both complete. You retain
judgment — subagents handle execution. See
`methodology/03a-orchestration.md` §3a.5.

## MANDATORY input from Phase 1

Before writing ANY strategy content, read and internalize:
- `outputs/DATA_RECONNAISSANCE.md` — what branches exist, MC coverage,
  truth-level info, pre-applied selections
- `outputs/INPUT_INVENTORY.md` — what external inputs are available and
  what is missing
- `outputs/LITERATURE_SURVEY.md` — reference analyses, modern methods,
  published results

Every strategy decision MUST be grounded in these Phase 1 findings. Do
not assume branch availability, MC coverage, or input values — check
Phase 1 deliverables. If Phase 1 did not investigate something you need,
flag it as a gap (but do NOT re-run Phase 1 — work with what is available
and document assumptions).

## Output artifacts

- `outputs/STRATEGY.md` — analysis strategy with physics motivation,
  sample inventory, selection approach, systematic plan, technique
  selection, and mitigation strategies
- `../COMMITMENTS.md` — binding commitments with `[REF]` entries from
  literature

## Methodology references

- Phase requirements: `methodology/03-phases.md` → Phase 2
- Review protocol: `methodology/06-review.md` → §6.2 (4-bot), §6.4
- Artifacts: `methodology/05-artifacts.md`

## RAG queries (mandatory — see executor.md "RAG Access" for toggle check)

Query the experiment corpus for:
1. Prior measurements of the same or similar observables
2. Standard systematic sources for this analysis technique
3. Cross-experiment results if applicable (`compare_measurements`)
4. Drill into each reference analysis identified (`get_paper`)

Cite all retrieved sources in the artifact (paper ID + section).

## Required deliverables

### Physics motivation and observable definition

Define the observable(s) and their physical interpretation precisely.
Verify the definition against Phase 1 literature findings — if the
literature uses a different definition, document the difference and
justify the choice.

### Selection approach enumeration

- **≥2 qualitatively different selection approaches** (not parametric
  variants of the same method). Ground each approach in Phase 1 branch
  availability — do not propose selections on branches that do not exist.
- At least one approach must be MVA-based (BDT on available
  discriminating variables) unless a concrete constraint makes MVA
  infeasible — in which case the constraint must be documented with a
  [D] label and validated at review. Phase 3 treats cut-based selection
  as a downscope from MVA (see `methodology/12-downscoping.md`), so the
  strategy must at minimum identify what MVA inputs are available and why
  an MVA is or isn't planned.

### Systematic uncertainty plan

- Read the applicable `conventions/` files listed below. For every
  required source listed, state "Will implement" or "Not applicable
  because [reason]."
- Ground the plan in Phase 1 MC coverage — do not plan systematics that
  require MC samples Phase 1 showed are unavailable.
- This enumeration is binding — Phase 4a reviews against it. Silent
  omissions are Category A.

### Precision estimates

Using Phase 1 MC statistics and reference analysis values, estimate the
expected statistical and systematic precision. If a reference analysis
achieved better precision with similar resources, document the
methodology differences — this becomes a Phase 4a investigation trigger.

### Technique selection

Determine the analysis technique (unfolding, template fit, etc.) and
justify the choice. This determines which technique-specific requirements
apply in later phases.

### Reference analysis table (B2)

For each reference analysis on the same dataset:
- Extract central value ± total uncertainty
- Methodology and key choices (binning, corrections, fitting approach)
- MC sample size
- Key differences from our planned approach

Record in `../COMMITMENTS.md` as `[REF]` entries. If a reference
achieved better precision with similar resources, document methodology
differences — this becomes a Phase 4a investigation trigger.

### Mitigation strategies (mandatory)

**For EVERY Phase 1 constraint, include a concrete mitigation plan.**
Do not write "X is unavailable, therefore we cannot do Y" — instead,
investigate alternatives. Examples from prior analyses:

- **No truth labels** → derive proxy labels from decay chain (e.g.,
  neutrino content), explore hemisphere tagging from literature, train
  classifier on proxy labels
- **Pre-cut data** → reformulate as ratio measurement where cut channels
  cancel, use published inputs from INPUT_INVENTORY for channels that
  cannot be measured directly
- **Low MC statistics** → investigate detector-level methods to avoid
  MC-noise amplification from correction factors, consider regularized
  unfolding, explore data-driven corrections
- **Missing branches** → identify proxy variables, check if the needed
  quantity can be reconstructed from available information
- **Limited MC coverage** (single energy, year, generator) → assign
  conservative systematic, validate with data-driven cross-checks

The mitigation exploration can run as a parallel subagent: search
literature for proxy methods, prototype feasibility on small data slices
from Phase 1, then integrate findings into the strategy.

### Backgrounds enumeration

Classify each background as irreducible, reducible, or instrumental.
Estimate relative importance (order of magnitude is fine). Ground in
Phase 1 MC sample inventory.

### Flagship figures

Identify ~6 figures that would represent the measurement in a journal
paper. Examples: the final spectrum with uncertainties, the response
matrix, the key data/MC comparison, the systematic breakdown, the theory
comparison overlay. These are defined here and produced at the highest
quality during Doc phases.

**For measurements additionally:**
- Identify the correction/unfolding strategy and its required inputs.
- Survey prior measurements — published data points become the primary
  validation target in Phase 4.
- Identify theory predictions or MC generators for comparison.

## Applicable conventions

- `conventions/unfolding.md` — for unfolded measurements
- `conventions/extraction.md` — for extraction/counting measurements

The technique selected in Phase 2 determines which file applies.
Read the "When this applies" section of each to confirm.

Read these before writing the systematic plan.

## COMMITMENTS.md (mandatory before review)

Before submitting for review, populate `../COMMITMENTS.md` with every
binding commitment from this strategy:
- Every systematic source ("Will implement") → one checkbox line
- Every validation test (closure, stress, cross-check) → one checkbox line
- Every flagship figure (~6 money plots) → one checkbox line
- Every comparison target (published values extracted) → one checkbox line
- Every cross-check committed → one checkbox line
- Every `[REF]` entry: reference analysis central value ± uncertainty,
  methodology, MC sample size (B2)

This file is updated at every phase boundary and reviewed at Doc 4c.
A commitment marked `[ ]` (not addressed) at Doc 4c is Category A.

## Pre-review self-check

Before submitting for review, verify:

- [ ] Phase 1 deliverables read: DATA_RECONNAISSANCE.md, INPUT_INVENTORY.md,
      LITERATURE_SURVEY.md
- [ ] Corpus queries executed — at least 3 searches, all results cited
- [ ] Observable definition verified against Phase 1 literature
- [ ] Backgrounds classified (irreducible, reducible, instrumental)
- [ ] >=2 qualitatively different selection approaches identified (not
      parametric variants of same method), grounded in Phase 1 branch
      availability. At least one MVA-based, or MVA infeasibility
      documented with [D] label
- [ ] Systematic plan enumerates EVERY source in applicable conventions
      files: "Will implement" or "Not applicable because [reason]"
- [ ] Systematic plan grounded in Phase 1 MC coverage
- [ ] Precision estimates grounded in Phase 1 MC statistics + reference values
- [ ] Reference analysis table: for each, central value ± uncertainty,
      methodology, MC sample size, key choices (B2)
- [ ] Method parity: if references used a more sophisticated method,
      committed to matching it or implementing as cross-check
- [ ] Mitigation strategy for EVERY Phase 1 constraint (no truth labels,
      pre-cut data, low MC stats, missing branches, etc.)
- [ ] Constraint [A], limitation [L], and decision [D] labels defined
- [ ] For measurements: flagship figures (~6) identified, correction
      strategy defined, theory comparison independence verified
- [ ] COMMITMENTS.md populated with [REF] entries from reference analyses

**Your reviewer will check** (§6.4): Phase 1 findings used? Backgrounds
complete? Systematic plan covers conventions and respects MC coverage?
Reference analyses tabulated with numerical values? >=2 qualitatively
different selection approaches grounded in available branches? MVA
considered or infeasibility justified? Method parity with published
analyses? Mitigation strategy for every Phase 1 constraint?

## Review

**4-bot review** — see `methodology/06-review.md` for protocol.
Write findings to `review/{role}/` using session-named files
(see `methodology/appendix-sessions.md` for naming conventions).
