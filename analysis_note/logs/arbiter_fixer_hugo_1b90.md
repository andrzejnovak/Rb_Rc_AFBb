# Arbiter-Fixer Session Log: hugo_1b90
**Date:** 2026-04-04
**Document:** Doc 4c v7 -> v8
**Role:** Adjudicate + Fix

## Inputs
1. AN_PHYSICS_REVIEW_viktor_cc74.md — Classification B (1A, 6B, 5C)
2. AN_CRITICAL_REVIEW_wanda_8260.md — Classification A (6A, 11B, 3C)
3. AN_COMBINED_VALIDATION_zelda_aad2.md — Classification B (2A, 1B)
4. Haiku swarm: 26/31 PASS, 5 FAIL

## Adjudication Table

| ID | Source | Severity | Finding | Verdict | Action |
|----|--------|----------|---------|---------|--------|
| zelda-F1 | zelda | A | Stale Phase 4a MC in F1 (rb_stability) | AGREE | Replace with rb_3tag_stability_fulldata.pdf |
| zelda-F2 | zelda | A | Stale Phase 4a MC in F2 (afb_angular) | AGREE | Generate afb_angular_fulldata.pdf, replace |
| zelda-F7 | zelda | A | Stale Phase 4a MC in F7 (afb_kappa) | AGREE | Replace with afb_kappa_fulldata.pdf |
| zelda-1 | zelda | A | ATLAS label on bdt_crosscheck_rb.pdf | AGREE | Replace with bdt_crosscheck_fulldata.pdf |
| zelda-3 | zelda | B | Garbled label on calibration_progression | AGREE | Regenerate with manual label placement |
| viktor-A1 | viktor | A | Figure 10 labels "MC pseudo-data" | AGREE (=zelda-F2) | Same fix as zelda-F2 |
| wanda-A1 | wanda | A | parameters.json R_b syst=null vs AN 0.027 | AGREE | Updated JSON: syst=0.027, status=evaluated_transfer |
| wanda-A2 | wanda | A | R_b syst total 0.027 != quadrature 0.020 | AGREE | Documented: eps_c added linearly (conservative envelope) |
| wanda-B4 | wanda | A* | BDT AUC=1.000 unexplained | AGREE as B | Added explanation paragraph (self-labelled proxy) |
| wanda-B5 | wanda | A* | chi2/ndf=377/7 inadequately discussed | AGREE as B | Added three-part justification paragraph |
| wanda-B8 | wanda | A* | Thrust signing dilution double-counting | AGREE as B | Added dilution accounting paragraph |
| wanda-B9 | wanda | A* | Per-year R_b~0.188 vs primary 0.2155 | AGREE as B | Added explanation paragraph (charm rejection) |
| viktor-B1 | viktor | B | sigma_d0 SF systematic may be underestimated | NOTE | Documented as known limitation; SF range is conservative |
| viktor-B2 | viktor | B | BDT AUC needs explanation | AGREE (=wanda-B4) | Fixed above |
| viktor-B3 | viktor | B | Fit GoF needs clearer discussion | AGREE (=wanda-B5) | Fixed above |
| viktor-B4 | viktor | B | Diagonal chi2 for correlated fractions | AGREE | Documented in GoF discussion |
| viktor-B5 | viktor | B | BDT training sample systematic | AGREE | Documented in systematic transfer note |
| viktor-B6 | viktor | B | Stub appendices | AGREE | Appendices C-G now populated |
| wanda-B1 | wanda | B | Input provenance table absent | AGREE | Added Table 1 |
| wanda-B2 | wanda | B | Luminosity absent | AGREE | Added luminosity estimate paragraph |
| wanda-B6 | wanda | B | Systematic subsections missing template | PARTIAL | Added error budget narrative; per-source figures remain out of scope |
| wanda-B7 | wanda | B | Error budget narrative absent | AGREE | Added after summary budget |
| wanda-B10 | wanda | B | AFB closure vs reproducibility | AGREE | Added clarification note |
| wanda-B11 | wanda | B | Cut-based vs BDT gap unexplained | AGREE | Added explanation after results table |
| wanda-B12 | wanda | B | AFB observed vs pole mixing | AGREE | Fixed comparison to use pole values |
| wanda-B13 | wanda | B | Conclusions <400 words | AGREE | Expanded to ~450 words |
| wanda-B14 | wanda | B | Stress test absent | NOTE | Closure test documented; formal stress test not performed |
| wanda-D1 | wanda | B | ROC curve absent | NOTE | AUC=1.000 explanation added; ROC not generated |
| wanda-D4 | wanda | B | Notation table absent | AGREE | Added notation table |
| viktor-C1 | viktor | C | Sign validation 8% diff not discussed | AGREE | Added absorption note |
| viktor-C2 | viktor | C | chi2/ndf=0.0/1 suspicious | NOTE | Not fixed (minor) |
| viktor-C3 | viktor | C | Published C_b=1.01 vs measured 1.1-1.5 | NOTE | Not fixed (minor) |
| viktor-C4 | viktor | C | BDT-specific eps_c systematic | NOTE | Documented as future improvement in conclusions |
| viktor-C5 | viktor | C | WP stability p=0.99 discussion | NOTE | Not fixed (minor) |

*wanda promoted B4/B5/B8/B9 to A severity; I adjudicate them as B (fixable, not physics-blocking).

## Figures Regenerated
1. `afb_angular_fulldata.pdf` — NEW, full data kappa=0.3 WP>5
2. `calibration_progression.pdf` — REGENERATED, fixed garbled label

## Figure Path Changes in v8
- F1: `F1_rb_stability_scan.pdf` -> `rb_3tag_stability_fulldata.pdf`
- F2: `F2_afb_angular_distribution.pdf` -> `afb_angular_fulldata.pdf`
- F7: `F7_afb_kappa_consistency.pdf` -> `afb_kappa_fulldata.pdf`
- BDT panel: `bdt_crosscheck_rb.pdf` -> `bdt_crosscheck_fulldata.pdf`

## JSON Updates
- `parameters.json`: R_b_BDT_primary.syst updated from null to 0.027, status from "pending" to "evaluated_transfer"

## Compilation
- tectonic compilation successful
- Output: ANALYSIS_NOTE_doc4c_v8.pdf (713 KB)
- No unresolved references
- Warnings: overfull/underfull hboxes only (cosmetic)

## Not Fixed (out of scope or minor)
- Per-source impact figures for each systematic (B6 partial) — would require new plotting infrastructure
- ROC curve figure (D1) — AUC=1.000 is explained in text
- Formal stress test (B14) — closure test serves this purpose
- C-level suggestions from viktor (C2-C5) — minor improvements for future version
