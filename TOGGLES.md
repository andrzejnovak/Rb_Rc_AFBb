# Analysis Toggles

**Read this file FIRST before any other action.** Every agent — orchestrator,
executor, reviewer, note writer — must read this file at session start and
respect all flags below. Do not assume defaults; read the actual values.

---

## REVIEW_MODEL_DIVERSITY

**Value:** `true`

When `true`, review panels use diverse model assignments (Opus for physics
reasoning and judgment, Sonnet for visual critique and secondary review,
Haiku for mechanical tasks). When `false`, all subagents use `model: "opus"`.

**Spec location:** Per-role assignment table in `methodology/06-review.md` §6.2.
Orchestrator reads the flag in `templates/root_claude.md` → "Subagent model selection."

---

## MAX_REVIEW_ITERATIONS

**Value:** `10`

Hard cap on review iteration cycles. The arbiter should ESCALATE to the
human well before this limit. Warn at 3 (1-bot: 2), strong warn at 5.

**Spec location:** Iteration limits in `methodology/06-review.md` §6.5.
Orchestrator enforces in `templates/root_claude.md` → "Review Protocol."

---

## MCP_ALPHAXIV

**Value:** `false`

Controls access to the alphaxiv MCP server for arXiv literature search
(`embedding_similarity_search`, `full_text_papers_search`,
`get_paper_content`, `answer_pdf_queries`, `read_files_from_github_repository`).
When `false`, agents MUST NOT call these tools — use `WebSearch`/`WebFetch`
with INSPIRE or direct arXiv queries instead.

**Set by:** The orchestrator during startup MCP verification. alphaxiv
requires OAuth 2.0 authentication — if the server is unreachable or
auth has expired, the orchestrator asks the human whether to continue
without it and sets this flag to `false`. Agents must check this toggle
before every alphaxiv call.

**Spec location:** Startup verification in root CLAUDE.md → "MCP verification."
Literature search workflow in `methodology/appendix-integration.md`.

---

## MCP_LEP_CORPUS

**Value:** `true`

Controls access to the LEP experiment corpus MCP server (`search_lep_corpus`,
`compare_measurements`, `get_paper`, `list_corpus_papers`). When `false`,
agents MUST NOT call these tools — use `WebSearch`/`WebFetch` for literature
queries instead. Cross-experiment comparisons via `compare_measurements`
are unavailable when disabled.

**Set by:** The orchestrator during startup MCP verification. If the server
is unreachable, the orchestrator asks the human whether to continue without
it and sets this flag to `false`. Agents must check this toggle before
every MCP call — do not assume the tools exist just because they appear in
the tool list.

**Spec location:** Startup verification in root CLAUDE.md → "MCP verification."
`mcp_manifest.json` lists expected servers, verification methods, and fallbacks.

---

<!-- Add new toggles above this line. Format:
## TOGGLE_NAME
**Value:** `value`
One-paragraph description of what it controls and where it's referenced.
-->
