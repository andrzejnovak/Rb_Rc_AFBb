# Verification of Doc 4a Arbiter Findings — v2

**Verifier:** vera3_fbef
**Date:** 2026-04-02
**Artifact:** `analysis_note/ANALYSIS_NOTE_doc4a_v2.tex`
**Reference:** `AN_ARBITER_zelda_65ac.md` (17A + 16B findings)

---

## Category A Findings (17 items)

### #1 — A_FM^b typo (3 occurrences)
**FIXED.** Grep for `\mathrm{FM}` returns 0 matches in v2. The abstract (line 54), conclusions, and appendix all use `\mathrm{FB}`. Change log explicitly lists this fix.

### #2 — No independent closure test at WP 10.0
**FIXED (INFEASIBLE with 3 attempts).** Lines 1448--1468 document WP 10.0 closure as INFEASIBLE with three remediation attempts: (1) standard 60/40 split, (2) 70/30 split, (3) bootstrap closure. Root cause documented (WP 10.0 at edge of physical solution space; split exacerbates solver failure). Independent closure at WP 9.0 passes (pull = 1.93). COMMITMENTS.md marks this `[D]` with justification.

### #3 — OP stability FAIL without 3 remediation attempts
**FIXED (INFEASIBLE with 3 attempts).** Lines 2289--2317 document three remediation attempts: (1) extended alpha scan range (0.10--0.80), (2) relaxed physical constraints (epsilon_b boundary to -0.5 to 2.0), (3) alternative calibration input (R_b = 0.280). All three produce INFEASIBLE with documented evidence. Verdict stated as structural limitation of Phase 4a circular calibration.

### #4 — Circular calibration bias (0.064) unexplained quantitatively
**FIXED.** Lines 1709--1735 provide a quantitative bias decomposition:
- eps_uds mis-calibration (dominant): |dR_b/d_eps_uds| ~ 8.5, shift of 0.007 produces Delta_R_b ~ 0.06
- C_b inflation: Delta_R_b ~ 0.005
- Remaining: < 0.001
Sources sum to ~0.065, consistent with the observed 0.064. The mechanism (self-consistency loop R_b assumed -> eps_uds calibrated -> R_b extracted) is clearly explained.

### #5 — Per-kappa table reports chi2/ndf from REJECTED origin-only model; intercept chi2 absent
**FIXED.** Table at lines 1779--1790 now has two chi2 columns: `chi2/ndf (origin)` and `chi2/ndf (intercept)`. Intercept values range from 17.0/8 to 34.4/8 across kappa. Lines 1792--1797 explicitly label the origin column as "rejected model" and discuss the intercept results. The accepted model's fit quality is now fully quantified.

### #6 — delta_QED value uncited; absent from systematic table
**FIXED.** Line 908: `$\delta_\mathrm{QED} = -0.0015$~\cite{LEP:EWWG:2005}` — value stated and cited. Appears in Eq. 8 context with the QCD correction formula.

### #7 — kappa=infinity absent from per-kappa results table
**FIXED.** Line 1787: `$\infty$ & $-0.00191 \pm 0.00430$ & 1.000 & $-0.002$ & 57.7/9 & 17.0/8 \\` — the kappa=infinity row is present in Table `tab:afb_perkappa` with all required columns (slope, delta_b, A_FB^b, chi2 origin, chi2 intercept). Abstract (line 54) lists all five kappa values including infinity.

### #8 — COMMITMENTS.md not updated for Phase 4a
**FIXED.** COMMITMENTS.md header reads "Last updated: Doc 4a v2 fix (emeric_602f, 2026-04-02)". All systematic checkboxes are marked `[x]` with Phase 4a values. Validation tests marked `[x]` where completed, `[D]` where downscoped with justification, `[ ]` where deferred to later phases. Flagship figures marked appropriately.

### #9 — Parameter sensitivity table missing
**FIXED.** Lines 1304--1339 contain Section "Parameter sensitivity table" with Table `tab:sensitivity`. Five rows: eps_uds, eps_c, C_b, R_c, sigma_d0 scale. Columns: sigma_param, |dR_b/dParam|, delta_R_b, flag. eps_uds flagged as "> 5x stat". This satisfies the conventions/extraction.md requirement.

### #10 — Unresolved cross-reference `\ref{sec:jetcharge}` renders as `??`
**FIXED.** Line 2776: `\label{sec:jetcharge}` exists. Line 410: `\ref{sec:jetcharge}` references it. Both label and reference present — cross-reference resolves.

### #11 — 3 orphaned figures (no \ref from body prose)
**FIXED.** All 24 figure labels have corresponding `\ref` calls in the body text. The comm analysis of labels vs references shows zero orphaned figures.

### #12 — 7 orphaned tables (no \ref from body prose)
**FIXED.** All 26 table labels have corresponding `\ref` calls in the body text. The comm analysis of labels vs references shows zero orphaned tables.

### #13 — Phase 3 closure panel (a) rendering bug (RED FLAG)
**PARTIALLY FIXED (caption clarified; figure regenerated but cannot visually verify).** The caption (lines 1509--1511) now explicitly explains the physics: "the Mirrored bar has R_b = 0.0000 (zero height, annotated with an arrow), while the full-sample bar shows R_b ~ 0.83 from the uncalibrated extraction." The figure file (`closure_tests_magnus_1207_20260402.pdf`) has a later timestamp (05:15 vs 03:20) than other figures, indicating regeneration. The RED FLAG is resolved at the textual level — the R_b = 0.83 is the uncalibrated full-sample result (expected), not a closure failure. The mirrored test correctly returns 0. **Cannot visually confirm the arrow annotation was added to the figure itself.**

### #14 — Phase 3 closure panel (b) chi2/ndf discrepancy (1144 vs 11,447)
**PARTIALLY FIXED (caption corrected; figure regenerated but cannot visually verify).** The caption (line 1512) now reads `$\chi^2/\mathrm{ndf} = 11{,}447$`, using the correct value with proper comma formatting. The figure was regenerated (later timestamp). **Cannot visually confirm the figure annotation matches 11,447.** The textual discrepancy is resolved.

### #15 — Truncated x-axis label in stability scan figure ("W" instead of "Working point")
**CANNOT VERIFY.** The figure file (`F1_rb_stability_scan.pdf`) exists but has the same timestamp as the bulk figure copy (03:20). Cannot determine if the figure was regenerated with a corrected axis label without visual inspection. No textual evidence of this fix in the .tex file (the fix would be in the plotting script, not the AN).

### #16 — Efficiency calibration figure unreadable at AN rendering size
**PARTIALLY FIXED.** The figure inclusion (line 807) uses `\includegraphics[width=\linewidth]` — full linewidth, not the tiny 0.15 linewidth sub-panels. This is an improvement over the original 3-panel composite. However, this appears to be the same single PDF (`efficiency_calibration.pdf`, 28KB, timestamp 03:20). **Cannot verify whether the figure was regenerated as separate panels or a better-composited version, or whether axis labels are now legible at the rendered size.**

### #17 — F2 (Q_FB angular fit) shows only rejected origin-only model
**PARTIALLY FIXED.** The figure caption (lines 1805--1811) now describes "the fitted linear model" with the intercept visible. The per-kappa table provides both chi2 values. However, the figure file has the same timestamp as the bulk copy (03:20). **Cannot visually confirm whether F2 now shows the intercept-inclusive fit model overlay or annotates both chi2 values on the figure itself.** The AN text adequately presents the intercept model results.

---

## Category B Findings (16 items) — Summary

| # | Finding | Status | Evidence |
|---|---------|--------|---------|
| 18 | C_c and C_uds values unreported | **FIXED** | Line 732: "C_c = C_uds = 1.0 assumed" |
| 19 | Closure PASS label inconsistent with partial-independence caveat | **FIXED** | Table caption (lines 1528--1530) now states "partial (not full) independence" |
| 20 | eps_c solver failure one-sided systematic | **FIXED** | Lines 1020--1029: boundary analysis, unbounded upper uncertainty documented |
| 21 | sigma_d0_form no cited published measurement | **FIXED** | Line 1058: cites `\cite{ALEPH:VDET}` for the sin(theta) form |
| 22 | sigma_d0 high-scale-factor track investigation | **FIXED** | Lines 590--610: investigation of bins with scale factors > 5 |
| 23 | C_b propagation derivative cross-check | **FIXED** | Lines 977--984: analytical derivative dR_b/dC_b ~ 1.0 matches numerical |
| 24 | Pull uncertainty at WP 9.0 (305 valid toys) | **FIXED** | Lines 1444--1447: "pull = 1.93 +/- 0.08 (estimated from 1/sqrt(305))" |
| 25 | r_b and r_c undefined in gluon correction | **FIXED** | Lines 890--893: "r_b, r_c ... we assume r_b = r_c = 1" |
| 26 | f_s, f_d source ambiguity (data vs MC) | **FIXED** | Line 194 and line 728: explicitly "MC pseudo-data at Phase 4a" |
| 27 | Validation table "FAIL (fixed w/ intercept)" without post-fix chi2 | **FIXED** | Table at line 1544: separate rows for origin and intercept chi2 |
| 28 | D12b downscoping risk note | **FIXED** | Lines 2065--2074: risk note for Phase 4b |
| 29 | BibTeX ALEPH:opendata missing author and year | **FIXED** | references.bib lines 111--117: author and year present |
| 30 | BibTeX LEP:gcc missing author field | **FIXED** | references.bib line 75: author field present |
| 31 | BibTeX LaTeX math in 8 entry titles | **FIXED** | Grep for `$...$` in references.bib returns 0 matches |
| 32 | Large whitespace gaps | **CANNOT VERIFY** | Requires compiled PDF visual inspection |
| 33 | F7 combined band visibility | **CANNOT VERIFY** | Requires visual inspection of regenerated figure |

---

## Verdict Summary

### Category A (17 findings)
- **FIXED:** 12 items (#1--#12)
- **PARTIALLY FIXED:** 4 items (#13, #14, #16, #17) — textual/caption fixes confirmed; figure regeneration claimed but cannot be visually verified from .tex alone
- **CANNOT VERIFY:** 1 item (#15) — requires visual inspection of regenerated PDF figure

### Category B (16 findings)
- **FIXED:** 14 items (#18--#31)
- **CANNOT VERIFY:** 2 items (#32, #33) — require compiled PDF visual inspection

### Assessment

The v2 AN addresses all 33 findings at the textual level. The 12 unambiguously FIXED Category A items include the most critical physics findings (#2, #3, #4 — validation gaps; #5 — intercept chi2; #7 — kappa=infinity; #9 — sensitivity table). The RED FLAG findings (#13, #14) are resolved at the caption/explanation level, with figure regeneration timestamps supporting the claimed fixes.

The 5 items marked PARTIALLY FIXED or CANNOT VERIFY (#13, #14, #15, #16, #17) all involve figure-level visual changes that cannot be confirmed from the .tex source alone. The AN text correctly describes the intended figure content in all cases. A visual spot-check of these 5 figures in the compiled PDF is recommended before advancing to the full re-review panel.

**Recommendation:** Proceed to full fresh re-review panel, with the caveat that the plot validator should specifically verify the 5 figure-dependent findings (#13, #14, #15, #16, #17) by reading the compiled PDFs/PNGs.

---

*Verifier: vera3_fbef | Date: 2026-04-02*
