# Phase 1: Exploration + Literature

> Read `methodology/03-phases.md` → "Phase 1" for full requirements.
> Read `methodology/appendix-plotting.md` for figure standards.

You are the exploration executor. Your job is data reconnaissance and
literature survey for a **measurement** analysis.

**Start in plan mode.** Before loading any data or running any searches,
produce a plan: which files to inspect first, what variables to survey,
what literature queries to run. Execute after the plan is set.

**Sub-delegation.** During planning, identify tasks that are large or
independent enough to warrant their own subagent. The two main
workstreams (data reconnaissance and literature search) are independent
and SHOULD run as parallel subagents. Spawn these as background
subagents writing to separate output files, then integrate their results
into your artifacts. You retain judgment — subagents handle execution.
See `methodology/03a-orchestration.md` §3a.5.

## Output artifacts

- `outputs/DATA_RECONNAISSANCE.md` — sample inventory, branch schema,
  MC coverage, truth-level information, pre-applied selections, data
  quality assessment
- `outputs/INPUT_INVENTORY.md` — external inputs needed for the analysis
  (see format below)
- `outputs/LITERATURE_SURVEY.md` — reference analyses, modern methods,
  published measurements, theory predictions
- Exploration figures in `outputs/figures/`

## Methodology references

- Phase requirements: `methodology/03-phases.md` → Phase 1
- Plotting: `methodology/appendix-plotting.md`
- Coding: `methodology/11-coding.md`
- Integration tools: `methodology/appendix-integration.md`

## Workstream 1: Data Reconnaissance

Expect to discover the data format at runtime. See
`methodology/03-phases.md` → Phase 1 "Data discovery" for the protocol
(metadata first → small slice → identify jagged structure → document schema).

### Required investigations

1. **Open ROOT files and list ALL branches with types.** For every tree
   in every file: branch name, data type, number of entries.
2. **Unique-value counts for integer branches.** Print unique values,
   range, and mean for every branch that could be a weight, flag, or
   quality indicator. Non-trivial values (e.g., bFlag=-999, process=-1)
   must be understood and documented.
3. **Check for pre-applied selections.** Compare event counts to
   published cross-section × luminosity. If counts are lower, the data
   has been pre-selected. Determine what was cut and document the impact.
4. **Characterize MC coverage.** Verify generator, tune, beam energy,
   and process match data-taking conditions. Document coverage gaps
   (single energy, single year, limited statistics, missing processes).
5. **Identify truth-level information.** What gen-level quantities are
   available? What truth-matching variables exist? What particle-level
   definition can be supported? If truth labels are absent, document
   this prominently — it is a critical constraint for Phase 2.
6. **Survey key variables.** Produce signal vs. background distributions
   for candidate kinematic variables. Check for pathologies: empty
   branches, outliers, discontinuities, unphysical values.
7. **Validate data quality.** Check for NaN/inf, unphysical values,
   and discontinuities. Document all findings.

Prototype on small subsets (~1000 events). Do not process full data to
"see what's there."

## Workstream 2: Literature Search

### arXiv MCP verification (mandatory — G1)

**Check `TOGGLES.md` → `MCP_ALPHAXIV`.** If `true`, verify by calling
`full_text_papers_search` with a known query. If it succeeds, use
alphaxiv for all subsequent literature queries. If the call fails (auth
expired, server down), log the failure and notify the orchestrator to
set `MCP_ALPHAXIV=false` in TOGGLES.md, then fall back to
WebSearch/WebFetch with INSPIRE queries for all subsequent literature work.

### RAG queries (mandatory — see executor.md "RAG Access" for toggle check)

When MCP_LEP_CORPUS is `true`, query the experiment corpus:
1. `search_lep_corpus`: prior measurements of the same or similar observables
2. `search_lep_corpus`: standard systematic sources for this analysis technique
3. `compare_measurements`: cross-experiment results if applicable
4. `get_paper`: drill into each reference analysis identified

### Modern methodology search (mandatory)

After the corpus search, search the broader literature. If
`MCP_ALPHAXIV=true`, use `embedding_similarity_search` and
`full_text_papers_search`. Otherwise use INSPIRE or web search (see
`methodology/appendix-integration.md`). Search for:
- The most recent published measurement of this observable
- Modern analysis methods (ML unfolding, full-distribution fits,
  resummation-improved theory, etc.)
- Published numerical inputs (luminosities, cross-sections, branching
  ratios) needed for the analysis

Cite all retrieved sources with paper ID + section.

### Reference analysis extraction

For each reference analysis found:
- Extract central value ± uncertainty where available
- Note methodology and technique used
- Note MC sample size if reported
- Note key choices (binning, corrections, systematic treatment)

## INPUT_INVENTORY.md format (G2)

This is a required deliverable. For every external input the analysis
may need (luminosities, cross-sections, branching ratios, reference
values, theory predictions):

```markdown
| Input | Status | Value | Source | Search trail |
|-------|--------|-------|--------|--------------|
| Luminosity | FOUND | 3.14 pb⁻¹ (Table 4) | CERN-EP/99-104 | Corpus: 3 queries, arXiv: 1 |
| R_l^{αs=0} | NOT FOUND | — | — | Corpus: 3q, INSPIRE: 2q, web: 1q |
```

For every NOT FOUND entry: the search trail is mandatory. Phase 2
(strategy) reviewers will check: "Could a different query have found
it?" If the reviewer finds it with an obvious query → Category A.

## Applicable conventions

- `conventions/unfolding.md` — for unfolded measurements
- `conventions/extraction.md` — for extraction/counting measurements

The technique selected in Phase 2 determines which file applies.
Read the "When this applies" section of each to confirm.

Read these to understand standard object definitions for this experiment.

## Rules

- Prototype on small subsets (~1000 events). Do not process full data to
  "see what's there."
- Append findings to experiment_log.md as you go.

## PDF build test (independent — can run in parallel)

Verify the PDF toolchain works by creating a minimal stub `.tex` file at
`analysis_note/test_build.tex` (copy from `conventions/an_template.tex`,
add a test equation and citation) and running `tectonic test_build.tex`.
Delete the stub after confirming. This is independent of exploration and
can be sub-delegated.

## Pre-review self-check

Before submitting for review, verify:

- [ ] DATA_RECONNAISSANCE.md: every file with tree names, branches (with
      types), event counts, cross-sections
- [ ] All integer/flag branches surveyed for unique values
- [ ] Pre-applied selections checked (event count vs. L×σ)
- [ ] MC coverage documented (generator, tune, energy, statistics)
- [ ] Truth-level information catalogued (or absence documented)
- [ ] Data quality validated: no pathologies, outliers, unphysical values
- [ ] INPUT_INVENTORY.md: all needed inputs with Status + Search trail
- [ ] LITERATURE_SURVEY.md: corpus queries + arXiv/web searches executed,
      all sources cited with paper ID + section
- [ ] arXiv MCP availability verified (or failure logged)
- [ ] Variable survey with distributions for key candidates
- [ ] PDF build test passed
- [ ] Experiment log updated with discoveries
- [ ] All figures pass plotting rules (see quick reference below)

### Plotting quick reference

These are the rules most commonly caught at review. Full spec in
`methodology/appendix-plotting.md`.

1. `figsize=(10, 10)` always — never custom sizes
2. `mpl_magic(ax)` after all plotting to prevent legend-data overlap
3. 2D colorbars: `make_square_add_cbar(ax)` or `cbarextend=True` —
   never `fig.colorbar(im)` or `fig.colorbar(im, ax=ax)`
4. `mh.histplot()` for all binned data — never `ax.step()`, `ax.bar()`
5. No absolute `fontsize=N` — use `'x-small'` etc.
6. `exp_label()` on every independent axes, NEVER on ratio panels
7. Separate matplotlib outputs composed in LaTeX — only use multi-panel
   matplotlib for ratio plots with `sharex=True`

## Review

**Self-review + plot validator.** This is a discovery phase, so review
is lightweight. Explicitly check: sample inventory complete? Data quality
checked? Literature searches executed? Input inventory populated?
Experiment log updated? Distributions look physical? The plot validator
runs alongside self-review to validate figures programmatically.
Write findings to `review/{role}/` using session-named files
(see `methodology/appendix-sessions.md` for naming conventions).
