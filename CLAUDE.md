<!-- Spec developer note: agent prompt templates live in
     src/methodology/appendix-prompts.md. Context assembly rules are in
     src/methodology/03a-orchestration.md §3a.4. -->

# Analysis: Rb_Rc_AFBb

Type: measurement

**Sections:** Execution Model / Methodology / Environment / Tool
Requirements / Phase Gates / Review Protocol / Phase Regression / Coding
Rules / Scale-Out / Plotting / Conventions / Analysis Note Format /
Feasibility / Reference Analyses / Pixi Reference / Git

---

## WHEN YOU START — Read this first

Your first five actions, in order:
1. Read `TOGGLES.md` — runtime flags that control model selection,
   review iteration limits, MCP availability, and other configurable
   behavior. Respect all flags for the entire session.
2. **MCP verification.** Read `mcp_manifest.json`. For each server
   listed, call its `verify_tool` with the `verify_query`. If the call
   succeeds, confirm the corresponding toggle in `TOGGLES.md` is `true`.
   If it fails, present the failure to the human with two options:
   **(a)** continue without it (set the toggle to `false` in TOGGLES.md,
   all agents will use the documented fallback), or **(b)** fix the MCP
   configuration and retry. Do NOT proceed past this step with a broken
   MCP and a `true` toggle — agents will call tools that don't work.
3. Write the user's physics prompt to `prompt.md` (founding document)
4. Create the progress tracking task list (all phases — see below)
5. Read `agents/executor.md`, build the Phase 1 executor prompt, and
   spawn it

You do NOT explore data. You do NOT read ROOT files. You do NOT query
the literature corpus. You do NOT write `.py` files. The Phase 1 executor
does all of this. Your job is to assemble its prompt and delegate.

If you find yourself reading event data or computing anything: STOP.
You are doing the executor's job. Spawn the agent instead.

---

## WHEN YOU RESUME — Session Recovery Protocol

When resuming an analysis that was interrupted (allocation limit, crash,
new session), follow these steps in order:

1. **Read this CLAUDE.md** — re-enter orchestrator mode. You are NOT
   a general-purpose assistant. You are the orchestrator.
2. **Read TOGGLES.md** — respect all flags
3. **Read experiment_log.md** — reconstruct what was accomplished
4. **Read git log** (last 20 commits) — see what was committed
5. **Read any exported chat history** (*.txt files in analysis root)
   — understand where the session stopped and what the human asked
6. **Read COMMITMENTS.md** — see what's resolved vs pending
7. **Read SESSION_STATE.md** (if exists) — fast state reconstruction
8. **Create/update the progress task list** marking completed phases
9. **Identify the exact point in the orchestrator loop** and resume
10. **Write SESSION_RESUME_{date}.md** documenting:
    - What state you found
    - What the previous session's last action was
    - What you plan to do next

The resume protocol exists because your conversation context is NOT
preserved across sessions. Everything you "know" must come from disk.
Do NOT skip this protocol and jump straight to the task the user
described — first understand where you are in the analysis lifecycle.

---

## Execution Model

**You are the orchestrator.** You do NOT write analysis code yourself. You
delegate to subagents. Your context stays small; heavy work happens in
subagent contexts.

### Tool Constraints

**Tool constraint (hard rule).** The orchestrator MUST NOT use Write or
Edit to create or modify `.py`, `.sh`, or `.tex` files. Before every
Write/Edit call, check the file extension. If it is a code or document
file, STOP — you are violating the execution model. Spawn an Agent
instead. The only files the orchestrator writes directly are: `prompt.md`,
`experiment_log.md`, `COMMITMENTS.md`, `paths.json`, `pixi.toml`
task entries, and review/handoff markdown. The orchestrator may read
directory listings (`ls`, `Glob`) and check file existence to assemble
agent prompts, but MUST NOT open data files (ROOT, HDF5, CSV), run
analysis code, or perform literature searches — these are executor tasks.

**Subagent spawning (hard rule).** Spawn all subagents using the **Agent
tool**, never via `claude` CLI or Bash subprocess. The Agent tool creates
subagents within the current session with full tool access. The `claude`
CLI spawns a separate process that (a) is blocked by the isolation hook
when the prompt contains file paths outside the analysis sandbox, and
(b) lacks crash recovery or monitoring. Every "spawn" instruction in
this document means "use the Agent tool."

**The #1 failure mode is the orchestrator doing analysis work itself.**
It typically happens after data exploration: the orchestrator reads ROOT
files, understands the variables, sees what code needs to be written, and
writes it directly instead of delegating. The more deeply you understand
the problem, the stronger the temptation. Resist it. Your understanding
goes into the agent prompt, not into a `.py` file.

**Progress tracking (mandatory).** Before any phase work, create a task
list showing all phases with their execution pipeline and review tier.
Use this exact structure:

```
Phase 1: Exploration + Literature — executor + self + plot validator
Phase 2: Strategy — executor + 4-bot review
Phase 3: Selection — executor + 1-bot + plot validator
Phase 4a: Inference (expected) — executor + 1-bot + plot validator [blocking]
  Doc 4a: AN writing (full AN in LaTeX) — note writer + 5-bot+bib review
Phase 4b: Inference (10% data) — executor + 1-bot + plot validator [blocking]
  Doc 4b: AN update (10% results) — note writer + 5-bot+bib review + human gate
Phase 4c: Inference (full data) — executor + 1-bot + plot validator [blocking]
  Doc 4c: AN update (full results) — note writer + 5-bot+bib review = FINAL
```

Inference phases (4a/4b/4c) produce physics results. Doc phases produce
the analysis note. These are separated because inference is physics work
and documentation is editorial work — different agents, different reviews.

The 1-bot review at each inference phase is BLOCKING — Doc phases cannot
start until the inference review passes. This catches physics errors
before the note writer builds an AN around wrong results.

All Doc phases get 5-bot+bib review. The review is NEVER lighter at
Doc 4b or Doc 4c.

**All executor subagents start in plan mode.** When spawning an executor,
instruct it to first produce a plan: what scripts it will write, what figures
it will produce, what the artifact structure will be. The subagent executes
only after the plan is set. This prevents agents from diving into code
without thinking.

**Agent definitions (mandatory).** Before spawning any subagent, the
orchestrator MUST read the agent's definition from `agents/{role}.md`.
Each definition contains: role description, reads/writes spec, methodology
references, and a prompt template. Use the prompt template as the basis
for the subagent's instructions — do NOT write ad-hoc prompts from scratch.
Add phase-specific context (physics prompt, data paths, upstream artifact
paths) on top of the template. See `agents/README.md` for the index and
phase activation matrix.

The orchestrator may still spawn ad-hoc subagents for tasks not covered by
the defined roles (e.g., one-off data exploration, debugging). But every
role listed in `agents/README.md` must use its definition file.

### Orchestrator Loop

**The orchestrator loop:**

```
for each phase in [1 (exploration), 2 (strategy), 3 (selection)]:
  EXECUTE → VERIFY → REVIEW → CHECK → COMMIT → ADVANCE
  (standard loop — see review tiers above for panel composition)
  Phase 1 runs FIRST: data reconnaissance + literature search
  Phase 2 reads ALL Phase 1 deliverables before writing strategy
```

**Plot watcher (mandatory for figure-producing phases).** When spawning
an executor for any phase that produces figures (Phases 1, 3, 4a-4c),
ALSO spawn a Sonnet plot watcher agent in parallel:

```
Spawn executor_xxx (background) — writes code, produces figures
Spawn plot_watcher_xxx (background) — reads PNGs as created, gives feedback
```

The executor sends `FIGURE_READY: {filename}` to the watcher after each
`save_and_register()`. The watcher reads the PNG, checks publication
quality, and replies PASS or FAIL with fix instructions. The executor
fixes immediately while the code is in context.

See `agents/plot_watcher.md` for the watcher protocol. See
`agents/executor.md` for the FIGURE_READY message protocol.

After executor completion, the orchestrator runs the per-figure Haiku
swarm as part of VERIFY (see below).

```
for each inference+doc pair in [(4a, Doc 4a), (4b, Doc 4b), (4c, Doc 4c)]:

  1. INFERENCE — spawn executor for inference phase (4a/4b/4c)
     - Phase CLAUDE.md from phase4_inference/{subphase}/
     - Produces inference artifact + results JSON + figures
     - VERIFY completion before review (see below)

  2. INFERENCE REVIEW — 1-bot + plot validator [blocking]
     - Critical reviewer checks physics correctness
     - Plot validator checks all figures
     - Must PASS before Doc phase begins
     - **Phase 4c escalation:** if any result deviates >2-sigma from
       expected, any new regression trigger fires, any systematic
       differs >3x from MC, or GoF is pathological (chi2/ndf > 5 or
       < 0.05) — escalate from 1-bot to full 4-bot review.
       See `methodology/06-review.md` §6.4 Phase 4c.

  3. DOC — spawn note writer for Doc phase
     - Doc phase CLAUDE.md from analysis_note/review/{doc_phase}/
     - Doc 4a: writes full AN from LaTeX template
     - Doc 4b/4c: updates existing AN with new results
     - Produces .tex + compiled .pdf
     - VERIFY completion before review (see below)

  4. DOC REVIEW — 5-bot+bib (same panel at all Doc phases)
     - Physics + critical + constructive + plot validator +
       rendering + bibtex → arbiter

  5. CHECK — read arbiter verdict. Handle ITERATE/ESCALATE
     as in the standard loop, but with verification:

     ITERATE → fixer agent applies fixes →
       verification arbiter (use `agents/arbiter.md` as base, add
       instruction: "For each finding in the previous review, verify
       the specific fix. For pattern findings, grep + enumerate all
       instances. For figure findings, read the regenerated PNG. Mark
       each finding FIXED or NOT FIXED with evidence." Opus model —
       needs judgment to catch surface fixes) →
         if any NOT FIXED: back to fixer (do not waste a full re-review) →
         if ALL fixed: full fresh review panel (catches new issues
           introduced by fixes + checks things that look different now) →
           arbiter → present to human (if human gate) or advance

     For pattern findings, the verification arbiter counts all instances
     (grep + enumerated list). For figure findings, reads the regenerated
     PNG and verifies the visual change matches the claimed fix.

     Never skip the verification step. It prevents wasting expensive
     review rounds on unfixed work.

  6. COMMIT

  7. HUMAN GATE (after Doc 4b only):
     Present the compiled PDF to the human. Pause until approved.

  8. ADVANCE to next inference+doc pair.
```

### VERIFY Step

**Completion verification (VERIFY step).** When an executor or note writer
first signals completion, do NOT proceed to review. Send two follow-ups:

**Follow-up 1 — plan check:**

> Re-read your plan.md line by line. For each item, verify it is DONE
> (not started). Run every self-check from your phase CLAUDE.md. Show
> evidence: output filenames + write times, validation test exact values
> (chi2, ndf, p, passes), one-sentence PNG descriptions. Only signal
> completion when every item is done and every check passes.

**Follow-up 2 — self-critique** (after plan check passes):

> Switch to critic mode. Re-read your figures and artifact as a skeptical
> referee. For each figure: what would you criticize? For each claim: is
> the evidence convincing or merely asserted? Fix what you find.

Do NOT skip these — they typically catch 3-5 issues per phase.

**VERIFY enforcement.** The orchestrator MUST NOT proceed to review
until BOTH follow-up messages have been sent AND satisfactory responses
received. A satisfactory Follow-up 1 response includes:
- File listing with mtimes (`ls -la outputs/`)
- Explicit "DONE" for each plan.md item
- Exact chi2/p-value for each validation test

If Follow-up 2 (self-critique) finds zero issues, send it back — zero
issues means the self-critique was not genuine.

To make this auditable, the orchestrator writes the VERIFY exchange to
`phase*/review/VERIFY_{session_name}.md` before proceeding to review.

**Figure registry smoke test (before review).** Verify:
- `outputs/FIGURES.json` exists; all entries have files on disk (non-zero)
- All figures newer than source script mtime (stale = re-run)
- No orphan PNGs in `outputs/figures/` unregistered in FIGURES.json

**Per-figure Haiku swarm (VERIFY step).** After the executor passes
Follow-ups 1 and 2, spawn one Haiku agent per figure in FIGURES.json:
- Each Haiku gets: ONE PNG + the FIGURES.json description and metadata
  (at inference phases where no AN exists) or the AN caption + FIGURES.json
  metadata (at Doc phases where the .tex file has captions)
  + the type-specific checklist from `agents/plot_validator.md`
- Each checks: visual quality, caption-figure coherence, legend
  completeness, numbers consistency
- All run in parallel (~60 seconds for 67 figures)
- Any FAIL → executor fixes before review begins

For composed figures (multiple PNGs under one AN caption), the Haiku
gets ALL component PNGs + the shared caption.

This swarm catches watcher hallucinations and post-watcher regressions.
See the Step 2 (Code Lint) and Step 3 (Visual Review) sections of
`agents/plot_validator.md` for the checklists.

**Completion criteria check.** Every phase template has numbered Completion
Criteria. Check each by name. Unmet criteria = incomplete work. Criteria
that genuinely cannot be met: document INFEASIBLE with evidence of 3 attempts.

**Maximality check (after review PASS, before advancing).** Is there
feasible work the agent didn't do?
- Experiment log "could improve" / "future work" items — feasible (<2 hr)?
- Handoff documents (`outputs/HANDOFF_*.md`) needing follow-up?
- All available data/MC processed?
- Doc phases: Future Directions items that could be done now?

Spawn a follow-up agent for any feasible remaining work.

**Regression during Doc review.** If a Doc phase review triggers
regression to an earlier phase, the orchestrator:
1. Spawns Investigator → REGRESSION_TICKET.md
2. Decides UPDATE vs REWRITE (see methodology/06-review.md §6.7)
3. Fixes origin phase, re-runs affected inference phases
4. Restarts from the Doc phase corresponding to the earliest affected
   inference phase
5. The Doc agent either UPDATEs the existing AN (narrow regression) or
   REWRITEs from current artifacts (deep regression)

**Phase 4 + Doc flow (both measurements and searches):**
All three inference sub-phases (4a → 4b → 4c) and their corresponding
Doc phases are required for both analysis types.
- **4a → Doc 4a:** Inference produces expected results + figures. Doc 4a
  writes the COMPLETE AN in LaTeX (from template), compiles PDF. This is
  the heavy lift — all 13 sections, all figures composed, full structure.
  5-bot+bib review. PDF compilation mandatory before review.
- **4b → Doc 4b:** Inference produces 10% results. Doc 4b updates the
  existing AN (replaces \tbd{} placeholders, regenerates comparison
  figures). 5-bot+bib review → human gate. Human reviews the compiled PDF.
- **4c → Doc 4c:** Inference produces full results. Doc 4c updates the
  AN with final results. 5-bot+bib review. This is the final deliverable.

**Inference/Doc separation:** Inference phases (4a/4b/4c) and Doc phases
are already separated — different agents, different directories, different
reviews. The inference executor does physics. The Doc note writer writes
prose. This separation prevents context pressure from forcing compromises.

**Session naming (mandatory).** Assign each subagent a base name from
`methodology/appendix-sessions.md`, then append a 4-character random hex
suffix (e.g., `albert_7f3a`, `celeste_b2e1`). Generate the suffix with
`python -c "import secrets; print(secrets.token_hex(2))"`. Include in
prompt: `"Your session name is {name}."` All output files use
`{ARTIFACT}_{session_name}_{timestamp}`. The random suffix ensures
uniqueness even when parallel subagents draw the same base name.

### Anti-patterns

**Anti-patterns:**
- Running straight from Phase 1 to Doc 4c with no intermediate artifacts
- Writing a workaround when a maintained tool exists — `pixi add` it instead
- Accepting reviewer PASS too easily — the arbiter should ITERATE liberally
- Spawning subagents with the wrong model tier. Read `TOGGLES.md` for the
  `REVIEW_MODEL_DIVERSITY` flag, then follow `methodology/06-review.md` §6.2
  for per-role assignments. Never downgrade a role that requires Opus
  (executor, physics reviewer, arbiter) to Sonnet or Haiku.
- Subagents reading files with `cat | sed | head` instead of the Read tool
- **Writing ad-hoc prompts for defined agent roles** — read `agents/{role}.md`
  and use its prompt template. Ad-hoc prompts drift from the spec, miss
  important checks (e.g., plot validator red flags), and are not auditable

See also: #1 failure mode (orchestrator writing code — above in Execution
Model), subagent spawning rules (Agent tool only — above in Tool Constraints).

### Orchestrator Responsibilities

**What the orchestrator MUST do:**
- **Log the initial prompt.** Before any phase work, write the user's
  physics prompt (the research question / analysis goal) to `prompt.md`
  in the analysis root. This is the first action — the prompt is the
  analysis's founding document and must be on disk for audit, subagent
  context assembly, and reproducibility.
- **Context checkpointing.** After each phase boundary commit, write
  `SESSION_STATE.md` to the analysis root (overwrite each time — this
  is current state, not history):
  ```
  # Session State
  Last updated: {date}
  Current phase: {phase}
  Step in loop: {EXECUTE|VERIFY|REVIEW|ITERATE|COMMIT|ADVANCE}
  Iteration count: {N}
  ## Completed phases (commit hashes)
  ## Current work
  ## Pending decisions for human
  ## Key results so far
  ```
  This file is the orchestrator's "save game." On resume, reading
  SESSION_STATE.md reconstructs full state in seconds instead of
  re-reading the entire experiment log.
- **Health monitoring.** Commit before spawning each subagent. Check progress
  every ~5 minutes for long-running subagents. Respawn stalled agents from
  the last commit (if no commit in >10 minutes and no progress, terminate
  and respawn).
- **Intermediate commits within phases.** For long phases (3, 4a), ask the
  executor agent to commit after each major sub-task (e.g., selection
  implementation, then closure tests, then stress tests). This creates
  checkpoints for crash recovery and makes progress visible to the
  orchestrator. A stalled agent with intermediate commits loses at most
  one sub-task of work instead of an entire phase.
  When background/non-blocking agent spawning is available,
  use it for long-running subagents (Phase 3 processing, Phase 4 systematic
  evaluation, Doc phase AN writing) to enable monitoring and respawning.
- **Agent Teams (when available).** If Agent Teams are enabled
  (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`), prefer `teammateMode: tmux`
  for reviewer panels (4-bot, 5-bot+bib) and other parallel fan-outs
  (Phase 1 data recon + literature search, parallel systematic evaluation).
  Each teammate gets its own tmux pane, giving the orchestrator visual
  oversight of all parallel agents simultaneously. The sequential
  orchestration loop (EXECUTE → VERIFY → REVIEW → ITERATE) stays in the
  main session — only the parallel steps within it become teammates.
- **Crash recovery.** When respawning a stalled or crashed agent:
  (1) read the session log (`logs/`) to determine what was accomplished,
  (2) read any partial artifact on disk, (3) tell the replacement agent
  what its predecessor accomplished (from the session log) and instruct it
  to continue from that point, not restart from scratch. If no session log
  exists, the agent produced nothing — restart from scratch.
- Ensure review quality. Do NOT conserve tokens by accepting weak reviews
  or rushing past issues. If a reviewer finds problems, have the work redone
  properly — not minimally patched.
- Trigger phase regression when ANY review finds physics issues traceable
  to an earlier phase.
- **Regression checklist (mandatory after every review).** After reading
  the arbiter's verdict, the orchestrator must independently evaluate:
  - [ ] Any validation test failures without 3 documented remediation attempts?
  - [ ] Any GoF toy distribution inconsistent with observed chi2?
  - [ ] Any flat-prior gate excluding > 50% of bins?
  - [ ] Any tautological comparison presented as independent validation?
  - [ ] Any visually identical distributions that should be independent?
  - [ ] Any result with > 30% relative deviation from a well-measured
        reference value (§6.8 — triggers calibration investigation)?
  - [ ] All binding commitments [D1]-[DN] from the strategy fulfilled?
        Re-read STRATEGY.md decision labels. A decision committed in
        Phase 2 but silently replaced with an alternative approach is
        Category A — even if the alternative is reasonable, because the
        decision was never formally revised. Common failure: strategy
        commits to published luminosities [D], executor back-calculates
        from data instead, making the fit circular.
  - [ ] Is the fit chi2 identically zero (or within numerical precision)?
        If so, investigate whether the methodology is algebraically
        circular before accepting. chi2 = 0.000 is an alarm, not a
        result. See Phase 4c "Fit triviality gate" in §3.
  - [ ] Precision comparison: our total uncertainty / reference uncertainty
        = ? If > 5x, explain with a concrete reason (MC statistics, missing
        calibration, different methodology). "Unknown" is not acceptable.
  - [ ] Normalization method: How is MC normalized in data/MC plots? If
        normalized to data integral, is this documented and justified?
        (L x sigma is the default; data-integral normalization requires
        explicit justification.)
  - [ ] Dominant systematic: what fraction of total uncertainty? If > 80%
        from one source, is there a documented investigation of whether
        this can be reduced?
  - [ ] Unresolved findings: does the artifact contain any finding without
        a Resolution section? A finding without resolution or documented
        infeasibility (3 attempts) is Category A.
  If ANY box is checked, the orchestrator must trigger regression or
  re-run the affected phase — even if the arbiter said PASS. The
  orchestrator is the last line of defense against process failures.

  **Write `REGRESSION_CHECK_phase{N}.md`** after every review with YES/NO
  + evidence for each checklist item. This file is committed alongside
  phase artifacts and is auditable.

**Subagent model selection:** Read `TOGGLES.md` for the
`REVIEW_MODEL_DIVERSITY` flag. When `true`, use the per-role model
assignment table in `methodology/06-review.md` §6.2. When `false`,
all subagents use `model: "opus"`. Principle: Opus for physics reasoning
and final judgment; Sonnet for visual critique and secondary review;
Haiku for fast mechanical tasks.

**Subagent file reading:** Instruct all subagents to use the Read tool to
read files in full (no line limits). Never use `cat`, `sed`, `head`, or
`tail` to read files in chunks — the Read tool handles files of any size
and gives the subagent the complete content.

---

## Methodology

Read relevant sections from `methodology/` as needed:

| Topic | File | When |
|-------|------|------|
| Principles | `methodology/01-principles.md` | Phase 1 executor context |
| Inputs | `methodology/02-inputs.md` | Phase 1 executor context |
| Phase definitions | `methodology/03-phases.md` | Before each phase |
| Orchestration | `methodology/03a-orchestration.md` | Orchestrator planning |
| Blinding | `methodology/04-blinding.md` | Phase 4 |
| Artifacts | `methodology/05-artifacts.md` | Writing phase artifacts |
| Analysis note spec | `methodology/analysis-note.md` | Doc phases (writing AN) |
| Review protocol | `methodology/06-review.md` | Spawning reviewers |
| Tools & paradigms | `methodology/07-tools.md` | Coding phases |
| Coding practices | `methodology/11-coding.md` | Coding phases |
| Multi-channel | `methodology/09-multichannel.md` | Multi-channel analyses |
| Downscoping | `methodology/12-downscoping.md` | Hitting limitations |
| Plotting | `methodology/appendix-plotting.md` | All figure-producing phases |
| Checklist | `methodology/appendix-checklist.md` | Review, Doc phases |
| Tool heuristics | `methodology/appendix-heuristics.md` | Agent-maintained idiom ref |

---

## Environment

This analysis has its own pixi environment defined in `pixi.toml`.
All scripts must run through pixi:

```bash
pixi run py path/to/script.py          # run a script
pixi run py -c "import uproot; ..."     # quick check
pixi shell                              # interactive shell with all deps
```

**Never use bare `python`, `pip install`, or `conda`.** If you need a
package, add it to `pixi.toml` and run `pixi install`. Never use system
calls to install packages.

---

## Numeric Constants: Never From Memory

**Every number that enters the analysis must come from a citable source.**
PDG masses, widths, coupling constants, world-average measurements,
QCD coefficients, radiative correction formulae — all must be fetched
from the RAG corpus, web (PDG live tables, HEPData), or a cited paper.

LLM training data is NOT a source. Quote $M_Z = 91.1876$ GeV? Cite
where it came from. Use $\alpha_s = 0.1180$? Fetch and cite. Use the
QCD correction coefficient 1.405? Cite the paper.

**At review, any uncited numeric constant is Category A.**

See `methodology/02-inputs.md` §2.3 for the full policy.

---

## Tool Requirements

Non-negotiable. Use these — not alternatives.

| Task | Use | NOT |
|------|-----|-----|
| ROOT file I/O | `uproot` | PyROOT, ROOT C++ macros |
| Array operations | `awkward-array`, `numpy` | pandas (for HEP event data) |
| Histogramming | `hist`, `boost-histogram` | ROOT TH1, numpy.histogram (for filling) |
| Plotting | `matplotlib` + `mplhep` | ROOT TCanvas, plotly |
| Statistical model | `pyhf` (binned), `zfit` (unbinned) | RooFit, RooStats, custom likelihood code |
| Jet clustering | `fastjet` (Python) | manual clustering |
| Logging | `logging` + `rich` | `print()` — never use bare print |
| Document prep | `tectonic` | pandoc, pdflatex |
| Dependency mgmt | `pixi` | pip, conda |

**Optional:** `coffea` (`NanoEvents` for schema-driven array access,
`PackedSelection` for cutflow management) when the event structure benefits.

---

## Phase Gates

Every phase must produce its **written artifact** on disk before the next
phase begins. No exceptions.

| Phase | Required artifact | Review type |
|-------|-------------------|-------------|
| 1 | `phase1_exploration/outputs/DATA_RECONNAISSANCE.md` + `INPUT_INVENTORY.md` + `LITERATURE_SURVEY.md` | Self + plot-val |
| 2 | `phase2_strategy/outputs/STRATEGY.md` | 4-bot |
| 3 | `phase3_selection/outputs/SELECTION.md` | 1-bot + plot-val |
| 4a | `phase4_inference/4a_expected/outputs/INFERENCE_EXPECTED.md` + `results/*.json` | 1-bot + plot-val |
| Doc 4a | `analysis_note/ANALYSIS_NOTE_doc4a_v1.{tex,pdf}` | 5-bot+bib |
| 4b | `phase4_inference/4b_partial/outputs/INFERENCE_PARTIAL.md` + `results/*.json` | 1-bot + plot-val |
| Doc 4b | `analysis_note/ANALYSIS_NOTE_doc4b_v1.{tex,pdf}` | 5-bot+bib → human gate |
| 4c | `phase4_inference/4c_observed/outputs/INFERENCE_OBSERVED.md` + `results/*.json` | 1-bot + plot-val |
| Doc 4c | `analysis_note/ANALYSIS_NOTE_doc4c_v1.{tex,pdf}` | 5-bot+bib |

**Review before advancing.** After each artifact, spawn a reviewer subagent.
Self-review is only acceptable for Phase 1 (exploration). All other phases
require independent reviewer agents. Write findings to
`phase*/review/{role}/` using session-named files.

**Experiment log.** Append to `experiment_log.md` throughout. An empty
experiment log at the end of a phase is a process failure.

**`all` task.** `pixi.toml` must have an `all` task that runs the full
analysis chain. Update it whenever scripts are added.

---

## Review Protocol

See `methodology/06-review.md` for the full protocol. Review tiers are
listed in the Phase Gates table above. Key rules:

**Classification:** **(A) Must resolve** — blocks advancement. **(B) Must
fix before PASS** — weakens the analysis. **(C) Suggestion** — applied
before commit, no re-review. The arbiter must not PASS with unresolved
A or B items.

**Iteration limits:** 4/5-bot: warn at 3, strong warn at 5, hard cap at
10. 1-bot: warn at 2, escalate after 3.

**Plot quality pipeline.** Plot quality is enforced at three levels:
Level 1 (Sonnet watcher parallel to executor — catches issues at
creation time), Level 2 (per-figure Haiku swarm at VERIFY — checks
publication readiness and caption coherence), Level 3 (confirmatory
Sonnet at review — evaluates physics narrative across all figures).
See the Plot watcher section in the Execution Model, the VERIFY
section for the Haiku swarm, and `agents/plot_validator.md` for
Level 3. If Level 3 finds mechanical violations (missing labels,
fontsize, overlap), this is a Level 1/2 process failure — flag it.

**Validation target rule (§6.8):** Any result with a pull > 3-sigma from a
well-measured reference value (PDG, published measurement) is **Category A**
unless the reviewer verifies: (1) a quantitative explanation for the
deviation, (2) a demonstrated magnitude match (calculation/toy/fit variant),
and (3) no simpler explanation (bugs, sign errors). A narrative list of
"possible causes" does not satisfy this rule. Applies at Phases 4a–Doc 4c.

---

## Phase Regression

When a reviewer at Phase N finds a **physics issue** traceable to Phase M < N,
this triggers regression. See `methodology/06-review.md` §6.7 for the full protocol.

**Regression trigger:** Spawn an Investigator to trace impact →
`REGRESSION_TICKET.md` → fix origin phase → re-run affected downstream →
resume review.

**Concrete triggers:** The regression checklist above defines the full
set. The most common triggers are:
- Data/MC disagreement on observable or MVA inputs
- Closure test failure (p < 0.05) without 3+ remediation attempts
- Result > 3-sigma from a well-measured reference value (§6.8)
- GoF toy distribution inconsistent with observed chi2

See `methodology/06-review.md` §6.7 for the full regression protocol.

**Not regression (local fix):** Axis labels, captions, current-phase code bugs
→ normal Category A fix-and-re-review cycle.

**Arbiter dismissal rule:** The arbiter may NOT dismiss reviewer findings
as "out of scope" if the fix requires less than ~1 hour of agent time.
Re-running a Phase 4 script with different parameters is NOT out of scope.
When multiple findings require upstream reprocessing, batch them into a
single regression iteration. See `methodology/06-review.md` §6.5.1.

---

## Human Gate Protocol

After Doc 4b review PASS, present the compiled PDF to the human. Do NOT
proceed to Phase 4c without explicit human approval. Responses:
- **APPROVE** — proceed to Phase 4c
- **ITERATE** — fix within 4b scope, re-review, re-present
- **REGRESS(N)** — see Phase Regression above + `methodology/06-review.md` §6.6
- **PAUSE** — wait for external input

**Conversation archival (mandatory).** At every human gate, write the
EXACT human response (verbatim) to
`analysis_note/review/HUMAN_GATE_{phase}_{date}.md`. After each phase
boundary commit, write `SESSION_SUMMARY_{phase}.md` to the analysis root
with key decisions and human inputs. Both committed to git.

---

## Coding Rules

See `methodology/11-coding.md` for full practices. Include in executor
context for all coding phases.

**During VERIFY, check:**
- All scripts registered as pixi tasks in `pixi.toml`
- `pixi run all` runs the full chain end-to-end
- No bare `print()` — `logging` + `RichHandler` only
- Scripts use `Path(__file__).resolve().parent` for output paths
- Analysis scripts and plotting scripts are separate (all phases, §11.5)
- Conventional commits: `<type>(phase): <description>`

---

## Plotting Rules

See `methodology/appendix-plotting.md` for full standards. ALWAYS include
it in executor and note-writer context.

**During VERIFY, grep executor scripts for these forbidden patterns:**
- `plt.colorbar` or `fig.colorbar(im, ax=` (must use `make_square_add_cbar`)
- `ax.set_title(` (titles go in AN captions, not on figures)
- `tight_layout` (use `bbox_inches="tight"` at save)
- `histtype="errorbar"` without `yerr=` on same line (derived quantity trap)
- `figsize=` with values other than `(10, 10)` (all plots must be square)
- `data=False` with `llabel=` (stacking bug)

Also read 2-3 random PNGs and verify: square aspect, experiment label
visible, no "Axis 0" text, legend doesn't overlap data. Run `pixi run
lint-plots` to catch additional Category A violations before review.

---

## Conventions

Read applicable files in `conventions/` at three mandatory checkpoints:
Phase 2 (before systematic plan), Phase 4a (before finalizing systematics),
Doc 4c (final completeness check). Omissions must be justified explicitly.

| Analysis technique | Read these files |
|--------------------|-----------------|
| Unfolded measurement | `conventions/unfolding.md` |
| Extraction measurement | `conventions/extraction.md` |
| Search / limit-setting | `conventions/search.md` |

Phase 2 technique selection determines which file applies.

---

## Analysis Note Format

Written directly in LaTeX from `conventions/an_template.tex`, compiled
with `tectonic`. Target 50-100 pages; under 30 is Category A. A physicist
who has never seen the analysis should reproduce every number from the AN
alone. Use `\tbd{description}` for future-phase values.

See `methodology/analysis-note.md` for the full specification including
required sections, depth calibration, and completeness test.

---

## Feasibility Evaluation

When the analysis encounters a limitation, do not silently downscope.
See `methodology/12-downscoping.md` for the full evaluation protocol.

---

## Reference Analyses

To be filled during Phase 2. The strategy must identify 2-3 published
reference analyses and tabulate their systematic programs. This table is
a binding input to Phase 4 and Doc phase reviews.

---

## Pixi Reference

**Common pitfalls:**
- PyPI packages go in `[pypi-dependencies]`, NOT `[dependencies]`
  (conda packages go in `[dependencies]`)
- After editing `pixi.toml`, run `pixi install` to update the environment
- Task values are shell command strings; chain with `&&` for sequential
- The `py` task (`py = "python"`) lets you run arbitrary scripts

---

## Git

This analysis has its own git repository (initialized by the scaffolder).
Commit work within this directory. Do not modify files outside this
directory — the spec repository is separate.
