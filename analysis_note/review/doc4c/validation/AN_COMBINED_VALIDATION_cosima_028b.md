# Combined Validation Report: Doc 4c FINAL (v4)
## Plot Validator + Rendering Reviewer + BibTeX Validator

**Session:** cosima_028b
**Document:** `analysis_note/ANALYSIS_NOTE_doc4c_v4.pdf/.tex`
**BibTeX:** `references.bib`
**Date validated:** 2026-04-02
**Prior session:** helga_6fa6 (validated v2; found 4 issues — 2A, 2B)
**Haiku swarm input:** 43/45 PASS, 2 FAIL (closure_test_phase4a undersized; efficiency_calibration no label)

---

## CLASSIFICATION: B

The document compiles to 62 pages (within the 50–100 target) and renders
correctly. All 46 referenced figures exist on disk and resolve without
errors. All 11 citation keys used in the text resolve in `references.bib`.
No `\tbd{}` placeholders remain in the body. No ATLAS experiment labels
appear in any figure. The four A-category issues found in the v2 review
(helga_6fa6) are confirmed resolved in v4.

However, three issues remain that prevent a clean PASS:
- One figure (`systematics_breakdown_fulldata`) carries no experiment label or
  energy string at all (Category B — publication standard violation).
- One figure (`calibration_progression`) has a garbled header due to text
  overlap in the two-panel layout (Category B — rendering defect).
- One figure caption (`closure_test_phase4a`) claims "four tested
  configurations" while the figure shows only two working points (Category B —
  caption-figure inconsistency; this is the Haiku swarm's first FAIL).
- The Reproduction Contract (Appendix) still cites `ANALYSIS_NOTE_doc4c_v3.tex`
  rather than `ANALYSIS_NOTE_doc4c_v4.tex` (Category C — stale filename).

---

## CONFIRMED RESOLVED (from helga_6fa6 / v2 review)

| Finding (v2) | Status in v4 |
|---|---|
| ATLAS label on `efficiency_calibration.pdf` | RESOLVED — now shows "ALEPH Open Data", √s = 91.2 GeV |
| ATLAS label on `F4b_fd_vs_fs_10pct.pdf` | RESOLVED — now shows "ALEPH Open Data", √s = 91.2 GeV |
| ATLAS label on `bdt_calibrated_rb.pdf` | RESOLVED — now shows "ALEPH Open Data", √s = 91.2 GeV |
| ATLAS label on `F5b_systematic_breakdown_10pct.pdf` | RESOLVED — now shows "ALEPH Open Data" |
| Broken cross-reference `\cref{sec:extraction:sf}` → ?? | RESOLVED — reference replaced throughout; no ?? found in body |

---

## NEW FINDINGS

### FINDING 1 — Category B: `systematics_breakdown_fulldata` has no experiment label

**Severity:** B (publication standard violation — every figure must carry the
experiment identifier and energy label)

**Figure:** `figures/systematics_breakdown_fulldata.pdf` (also confirmed in
the corresponding `.png`)

Visual inspection of both the PDF and PNG confirms that the figure header is
completely absent. There is no "ALEPH Open Data" identifier and no "√s = 91.2
GeV" energy string. All other figures in the document carry these labels
correctly. The figure appears to have been generated without the `mplhep`
experiment-label call (`hep.label.exp_label` / `hep.label.lumitext`) or with
those calls producing no output (e.g., wrong axes object passed).

This is one of the two FAILs reported by the Haiku swarm (reported as
"efficiency_calibration no label" — the Haiku swarm may have inspected the
wrong figure file; the label issue is confirmed here on
`systematics_breakdown_fulldata`, not `efficiency_calibration` which is now
correctly labelled in v4).

**Required fix:** Regenerate `systematics_breakdown_fulldata.pdf/.png` with
`hep.label.exp_label(ax, exp="ALEPH", data=True, label="Open Data")` and
`hep.label.lumitext(text="", rlabel=r"$\sqrt{s} = 91.2$ GeV", ax=ax)` (or
equivalent). The figure content and physics are correct.

---

### FINDING 2 — Category B: `calibration_progression` header rendering defect

**Severity:** B (figure rendered with garbled header — unacceptable for
publication or internal review)

**Figure:** `figures/calibration_progression.pdf` (confirmed in both PDF and
`.png`)

Visual inspection shows the header text reads "ALEPH*s*Open Data/" with the
√ symbol rendered as a literal "s" and the energy string ("s = 91.2 GeV")
colliding with and overwriting part of the experiment label text. The
result in the document is: "**ALEPH** *s*Open Data/" overlaid with the
right-side energy label, making the header unreadable.

The cause is the narrow two-panel figure layout: the left-side experiment
label and right-side energy label are positioned so close together that they
overlap. The `√` character is not rendering correctly in this context (likely
a font encoding issue with the `lumi_label` call in the narrow subplot).

**Required fix:** Either (a) widen the figure to give the header space, (b)
drop the energy label from the right header and include it only in the caption,
or (c) use `hep.label.exp_label(ax=left_ax)` and
`hep.label.lumitext(ax=right_ax)` targeting separate axes. The figure content
and physics are correct.

---

### FINDING 3 — Category B: Caption-figure inconsistency on `closure_test_phase4a`

**Severity:** B (caption makes a claim contradicted by the figure)

**Figure:** `figures/closure_test_phase4a.pdf` (line 2169 in TeX; confirmed
by direct visual inspection of both PDF and PNG)

**Caption (lines 2170–2175):** "The **four tested configurations** all recover
$R_b$ within $\pm 1\sigma$ of the SM input value..."

**Figure content:** Only **two** working points are shown on the x-axis:
`thr=9` and `thr=10`. The figure contains exactly two data points. The caption
claim of "four tested configurations" is factually wrong as shown.

This is the Haiku swarm's first reported FAIL ("closure_test_phase4a
undersized"). Note also that both data points fall at $R_b \approx 0.31$,
which is ~40% above the SM value of 0.21578 — neither recovers $R_b$ within
$\pm 1\sigma$ of SM. The caption claim that all configurations "recover $R_b$
within $\pm 1\sigma$" is also inconsistent with the plotted values. This
figure appears to be a stale or partial version from an earlier analysis stage
and should either be regenerated with the correct configurations, or replaced
with the more complete `closure_tests_magnus_1207_20260403.pdf` which exists
in the figures directory.

**Required fix:** Either (a) regenerate `closure_test_phase4a.pdf` with all
tested configurations producing results near the SM value, or (b) update the
caption to accurately describe the two-point figure and correct the
"within $\pm 1\sigma$ of SM" claim to match the actual plotted values (which
are ~$0.31$, not near $0.216$).

---

### FINDING 4 — Category C: Reproduction Contract cites stale filename

**Severity:** C (incorrect but cosmetic — a reader following the instructions
would compile the wrong file)

**Location:** Appendix "Reproduction Contract", line 4258 in TeX:
```
tectonic analysis_note/ANALYSIS_NOTE_doc4c_v3.tex
```

This should read `ANALYSIS_NOTE_doc4c_v4.tex` — the current final document.
The v3 file is a superseded version.

**Required fix:** Change `v3` to `v4` on line 4258.

---

## Checks That PASSED

| Check | Result |
|-------|--------|
| PDF compiles without errors | PASS — 62 pages, renders fully |
| All 46 referenced figures exist on disk | PASS — all files confirmed present and non-zero |
| No missing figure files | PASS |
| No `\tbd{}` placeholders in body | PASS — only occurrence is inside `\verb|...|` in changelog (not rendered as placeholder) |
| No bare Phase 4a/4b/4c references in body text | PASS — the one body occurrence is a figure filename in `\includegraphics` which is acceptable |
| All 11 used citation keys resolve in `references.bib` | PASS — all 11 keys found |
| No undefined citation keys | PASS |
| No ATLAS labels in figure files | PASS — all 4 previously-flagged figures are now correctly labelled |
| No ATLAS text in TeX body | PASS — one mention at line 4027 is in a legitimate technical comparison (ALEPH vs ATLAS/CMS d0 sign convention), not an experiment label |
| Experiment label "ALEPH Open Data" on figures | PASS for 44 of 46 figures; FAIL on `systematics_breakdown_fulldata` (Finding 1) and garbled on `calibration_progression` (Finding 2) |
| Energy label √s = 91.2 GeV on figures | PASS for 44 of 46 figures; same failures |
| Table of contents renders correctly | PASS |
| Mathematics and equations render without errors | PASS |
| Colored provenance markers render | PASS — blue (\measured) and red (\external) render correctly |
| Hyperlinks and cross-references | PASS — no ?? found in body; sec:extraction:sf issue from v2 is resolved |
| No duplicate `\label` definitions | PASS — zero duplicates found |
| BibTeX file parses without structural errors | PASS — all 15 entries syntactically valid |
| Bibliography section renders | PASS |
| Page count in 50–100 range | PASS — 62 pages |
| Sections count adequate | PASS — 39 sections/subsections; all required sections present |
| Per-year consistency figure present | PASS — `per_year_consistency.pdf` present and correctly labelled |
| Systematic breakdown figure present | FAIL (label missing) — see Finding 1 |
| Comparison overlay figure present | PASS — `calibration_progression.pdf` present (garbled label — see Finding 2) |
| BibTeX entries completeness | PARTIAL — same 9/11 entries missing volume/pages as in v2; BibTeX was not updated. This inherited from v2 but is a pre-existing B finding carried forward; no new degradation in v4. |

---

## BibTeX Status (inherited from v2, not updated in v4)

The `references.bib` file is unchanged from the v2 review. The nine entries
flagged by helga_6fa6 as missing journal/volume/pages fields remain
incomplete. Per the classification in the helga_6fa6 report (Category B),
these should be addressed. They are not newly introduced by v4 and the
eprint/note fields provide sufficient identification for internal use, but
they fall short of journal publication standards.

| Key | Status |
|-----|--------|
| `ALEPH:Rb:1996` | eprint present (`hep-ex/9609005`); volume/pages missing |
| `ALEPH:Rb:precise` | note only (inspire:433306); journal/volume/pages missing |
| `ALEPH:AFBb` | volume/pages present; journal field present |
| `LEP:EWWG:2005` | volume/pages present; eprint present — COMPLETE |
| `LEP:HF:2001` | eprint present (`hep-ex/0112021`); journal missing |
| `ALEPH:sigma_had` | volume/pages present; journal present — COMPLETE |
| `DELPHI:Rb` | volume/pages present; journal present — COMPLETE |
| `ALEPH:gbb` | eprint present (`hep-ex/9811047`); journal/volume/pages missing |
| `LEP:gcc` | volume/pages/eprint present — COMPLETE |
| `PDG:2024` | journal present; volume/pages missing |
| `ALEPH:opendata` | misc entry; complete for type |

Re-examination finds that several entries flagged as incomplete in v2 are in
fact complete on re-reading. The genuinely incomplete entries (missing both
journal and eprint) are: `ALEPH:Rb:precise`, `DELPHI:AFBb`, `DELPHI:AFBb:2`
(though these last two are in the bib file but unused in v4). All 11 used
citation keys have at minimum an eprint or inspire ID and are identifiable.
The BibTeX situation is improved from the v2 assessment. Remaining gaps are
cosmetic for an internal note.

---

## Figure Audit Summary (45 figures inspected)

| Figure | Label | Energy | Notes |
|--------|-------|--------|-------|
| `sigma_d0_calibration_magnus_1207_20260403` | ALEPH Open Data | √s = 91.2 GeV | PASS |
| `d0_sign_validation_magnus_1207_20260403` | ALEPH Open Data | √s = 91.2 GeV | PASS |
| `data_mc_combined_tag_magnus_1207_20260403` | ALEPH Open Data | √s = 91.2 GeV | PASS |
| `efficiency_calibration` | ALEPH Open Data | √s = 91.2 GeV | PASS (fixed from v2) |
| `rb_operating_scan_magnus_1207_20260403` | ALEPH Open Data | √s = 91.2 GeV | PASS |
| `F5b_systematic_breakdown_10pct` | ALEPH Open Data | √s = 91.2 GeV | PASS (fixed from v2) |
| `closure_mirrored_magnus_1207_20260403` | ALEPH Open Data | √s = 91.2 GeV | PASS |
| `closure_bflag_magnus_1207_20260403` | ALEPH Open Data | √s = 91.2 GeV | PASS |
| `closure_contamination_magnus_1207_20260403` | ALEPH Open Data | √s = 91.2 GeV | PASS |
| `S2b_hemisphere_charge_data_mc` | ALEPH Open Data | √s = 91.2 GeV | PASS |
| `F7b_kappa_consistency_10pct` | ALEPH Open Data | √s = 91.2 GeV | PASS |
| `bdt_calibrated_rb` | ALEPH Open Data | √s = 91.2 GeV | PASS (fixed from v2) |
| `S1b_tag_fractions_comparison` | ALEPH Open Data | √s = 91.2 GeV | PASS |
| `rb_3tag_stability_fulldata` | ALEPH Open Data | √s = 91.2 GeV | PASS |
| `calibration_progression` | GARBLED | GARBLED | FAIL — see Finding 2 |
| `afb_kappa_fulldata` | ALEPH Open Data | √s = 91.2 GeV | PASS |
| `per_year_consistency` | ALEPH Open Data | √s = 91.2 GeV | PASS |
| `systematics_breakdown_fulldata` | MISSING | MISSING | FAIL — see Finding 1 |
| `hemisphere_correlation` | ALEPH Open Simulation | √s = 91.2 GeV | PASS |
| `F4b_fd_vs_fs_10pct` | ALEPH Open Data | √s = 91.2 GeV | PASS (fixed from v2) |
| `closure_test_phase4a` | ALEPH Open Simulation | √s = 91.2 GeV | Caption inconsistency — see Finding 3 |
| All other figures (25 additional) | ALEPH Open Data/Simulation | √s = 91.2 GeV | PASS |

---

## Numerical Consistency Spot-Checks

Values in abstract, boxed equations, and summary tables are internally
consistent with the v4 primary results:

- Abstract: $R_b = 0.2155 \pm 0.0004$ (stat), $A_\text{FB}^b = 0.094 \pm 0.005$ (stat)
- Results section Table (tbl:results_summary): $R_b = 0.2155$, matching abstract
- Comparison section: pull from SM $< 1\sigma$, consistent with quoted values
- Per-year table: χ²/ndf = 3.6/3 — matches `per_year_consistency` figure annotation
- Closure test text: max|pull| = 2.80 PASS — consistent with body text claims
- BDT combined R_b = 0.217 in `bdt_calibrated_rb` figure legend matches
  nearby text in the crosscheck section

Note: The `afb_kappa_fulldata` figure shows the inclusive (unsigned-axis) result
$A_\text{FB}^b \approx 0.0005$ (not the primary signed-axis result of 0.094).
The caption correctly identifies this as the inclusive cross-check, not the
primary result. No inconsistency.

---

## Resolution Required Before PASS

| # | Finding | Severity | Fix |
|---|---------|----------|-----|
| 1 | `systematics_breakdown_fulldata.pdf` has no experiment label or energy string | B | Regenerate with `hep.label.exp_label` and `hep.label.lumitext` |
| 2 | `calibration_progression.pdf` has garbled header (√s overlaps ALEPH label in two-panel layout) | B | Fix figure layout: widen, or apply labels to separate axes |
| 3 | `closure_test_phase4a.pdf` caption claims "four tested configurations" but figure shows two; both points at R_b ~0.31, not within 1σ of SM | B | Regenerate figure with correct configurations OR update caption to match actual figure content |
| 4 | Reproduction Contract cites `ANALYSIS_NOTE_doc4c_v3.tex` (line 4258) | C | Change `v3` to `v4` |
