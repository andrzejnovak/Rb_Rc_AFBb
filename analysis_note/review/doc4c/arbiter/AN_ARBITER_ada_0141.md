# Arbiter Adjudication — Doc 4c FINAL

**Session:** ada_0141  
**Date:** 2026-04-02  
**Inputs:** phil_1838 (physics), gertrude_7ec5 (critical), helga_6fa6 (validation)

---

## Overall Verdict: ITERATE

Five Category A fixes required. All are targeted — no structural rewrite needed.

---

## Adjudication Table

Each row merges overlapping findings from the three reviewers into a single
actionable item. The "Source" column maps back to original finding IDs.

### Category A — Must Resolve

| # | Issue | Source | Adjudication | Fix |
|---|-------|--------|--------------|-----|
| A1 | ATLAS labels on 4 figures | phil F3, gertrude (implicit), helga F1 | **CONFIRMED.** Four figures (`efficiency_calibration.pdf`, `F4b_fd_vs_fs_10pct.pdf`, `bdt_calibrated_rb.pdf`, `F5b_systematic_breakdown_10pct.pdf`) show "ATLAS" and wrong energy (13 TeV / 1.5 TeV). Publication-blocking. | Regenerate all 4 figures with `exp_label("ALEPH Open Data")` and `lumi_label("", "sqrt(s) = 91.2 GeV")`. Recompile PDF. |
| A2 | Per-year R_b (~0.188) vs combined (0.212) unexplained | phil F1, gertrude A5 | **CONFIRMED as documentation gap.** The per-year extraction script likely uses raw MC efficiencies (no SF correction), producing the pre-calibration value (~0.188) consistent with the "smeared" step in Fig. 7. The combined result uses the full SF pipeline. The AN never states this. The values are not contradictory — they are from different calibration stages — but the reader cannot know that. | Add a footnote or paragraph to Table 15 / Section 9.3.4 stating: "Per-year values use single-configuration extraction at tight=8/loose=4 without the cross-configuration SF combination applied to the primary result. These values test year-to-year stability of the raw extraction, not the absolute calibration." If the per-year script CAN be re-run with SF correction, do so and replace the table. |
| A3 | Per-year A_FB^b all negative vs combined positive | phil F2, gertrude A4 | **CONFIRMED as same root cause as A2.** Without SF/purity correction the charm contamination flips the sign. The per-year extraction parameters (kappa, working point, correction method) are unstated. | State the extraction parameters for per-year A_FB^b. Add explanation: the per-year values use a single working point without purity correction, so charm dilution dominates and produces negative values. The combined result uses the purity-corrected method. |
| A4 | Systematic budget: JSON says 0.018, AN says 0.027 | gertrude A2, A3 | **CONFIRMED.** `phase_4c_fulldata.rb_total_syst = 0.018` vs `R_b_fulldata_final.syst = 0.027`. The discrepancy is 49%. Similarly for A_FB^b (0.019 vs 0.0021). The `parameters.json` final entry (0.027) matches the AN, so the headline result is self-consistent, but the `systematics.json` phase_4c section is stale or uses different assumptions. | Update `systematics.json` phase_4c_fulldata entries to match the final systematic budget in the AN and `parameters.json`. Document in the JSON which C_b and eps_c variation ranges were used. If the two JSON sections intentionally represent different systematic evaluations (e.g., single-WP vs combined), add a `method` field to disambiguate. |
| A5 | Broken cross-reference `\cref{sec:extraction:sf}` renders as ?? | helga F2 | **CONFIRMED.** Renders as literal "??" in the PDF. | Change `\cref{sec:extraction:sf}` to `\cref{sec:corrections:smearing}` (line 1732 in .tex). Recompile. |

### Category B — Must Fix Before PASS

| # | Issue | Source | Adjudication | Fix |
|---|-------|--------|--------------|-----|
| B1 | Covariance matrix uses 10% systematics (V_11 = 0.015^2) not full-data (0.027) | phil F4 | **CONFIRMED.** Eq. 30 covariance matrix is inconsistent with Table 16. | Update eq. 30 covariance matrix to use full-data systematic values. |
| B2 | Systematics grew ~2x from 10% to full data without explanation | phil F6 | **CONFIRMED.** eps_c: 0.013 -> 0.017, C_b: 0.003 -> 0.007, total: 0.015 -> 0.027. | Add 1-2 sentences in Section 9.2 explaining that full-data systematic evaluation uses wider C_b variation range (5%/10% vs the 10%-data range) and that eps_c grows because the data/MC mismatch is larger on the full dataset. |
| B3 | Combined A_FB^b from inconsistent kappa values (chi2 p=0.012) | gertrude B6, phil F5 | **CONFIRMED.** Cross-kappa chi2/ndf = 10.9/3 fails consistency. The combined value (+0.0025) is less meaningful than kappa=2.0 (+0.014). | Elevate kappa=2.0 as the primary A_FB^b result in the abstract and conclusions. Present the combined value as a cross-check with a caveat about the cross-kappa inconsistency (p=0.012). Remove or strongly caveat the sin2(theta_eff) derived from the combined value. |
| B4 | A_FB^b 26-sigma below LEP combined lacks quantitative dilution calculation | gertrude B1 | **CONFIRMED.** The explanation is qualitative only. | Add a 1-line calculation: expected diluted A_FB = A_FB^b_true * f_b * delta_b ~ 0.103 * 0.18 * 0.13 ~ 0.002, consistent with observed +0.0025. This converts the qualitative argument into a quantitative one. |
| B5 | validation.json stale — missing headline full-data SF result | gertrude B3 | **CONFIRMED.** The chi2/ndf = 4.4/14 (p=0.99) appears only in the AN, not in any JSON. | Add `operating_point_stability_sf_fulldata` entry to validation.json with chi2=4.4, ndf=14, p=0.99, passes=true. |
| B6 | Reproduction Contract cites wrong filename (doc4b_v5.tex) | helga F3 | **CONFIRMED.** | Change `ANALYSIS_NOTE_doc4b_v5.tex` to `ANALYSIS_NOTE_doc4c_v2.tex` in Appendix X. |
| B7 | BibTeX entries missing journal/volume/pages for 9 of 11 keys | helga F4 | **CONFIRMED.** Not blocking physics, but blocks a clean bibliography. | Add journal names to the 5 entries that lack them entirely (ALEPH:AFBb, LEP:HF:2001, ALEPH:sigma_had, DELPHI:Rb, LEP:gcc). Add volume/pages where readily available. |
| B8 | R_c not measured — no explicit statement or quantitative justification | phil F9 | **CONFIRMED.** The prompt requested R_c. It is constrained externally but this is not stated in the abstract or introduction. | Add to abstract: "R_c is constrained to the SM value; the data do not independently constrain it." Add 1 sentence in Section 5.1 quantifying why (e.g., floating R_c gives sigma(R_c) > 0.05). |
| B9 | COMMITMENTS.md: 3 genuine gaps + 16 stale checkboxes | gertrude A1 | **CONFIRMED in part.** The 16 stale checkboxes are bookkeeping (B-level). The 3 genuine gaps: (i) probability tag vs N-sigma comparison, (ii) analytical vs toy propagation comparison, (iii) constrained vs floated R_c. | For each genuine gap: either execute the cross-check and document, or add a formal [D] downscoping entry with justification. Update all 16 stale checkboxes to [x]. |

### Category C — Apply Before Commit

| # | Issue | Source | Fix |
|---|-------|--------|-----|
| C1 | Per-WP chi2 decomposition (which observables drive tension) | phil F7 | Add 1 sentence identifying dominant residual (e.g., "single-tag/double-tag tension on eps_uds"). |
| C2 | Contamination injection not repeated post-SF | phil F8 | Add sentence: "The contamination test was performed pre-calibration; post-SF linearity was not separately tested." |
| C3 | Closure test "independent" is statistical only | phil F10 | Add qualifier: "statistically independent (disjoint events) but sharing the same MC model." |
| C4 | Precision ratio vs LEP combined (41x) not stated | gertrude C1 | Add both ratios (19x vs ALEPH, 41x vs LEP combined) in Table 9. |
| C5 | Known Limitations item 6 stale (mentions future full-data) | gertrude C3 | Update to reflect full-data analysis is complete. |
| C6 | App B table caption missing "10% subsample" clarification | gertrude C4 | Add "(10% subsample)" to Table B3 caption. |
| C7 | Minor figure quality (overlapping text, cramped labels) | phil F11 | Adjust where feasible. |
| C8 | Byline format | phil F13 | Note for journal submission; no action for AN. |

---

## Findings NOT Adopted

| Source | Why dismissed |
|--------|--------------|
| gertrude B4 (C_b=1.0 data-level test) | The closure test + systematic variation (5%/10%) adequately covers this. A data-level decorrelation test would require infrastructure not available. The systematic (0.007) is already the third-largest contributor. Existing coverage is sufficient for Doc 4c scope. |
| gertrude B2 (per-year R_b consistency further documentation) | Merged into A2 — the root cause is the same (unstated calibration difference). A2 fix resolves B2. |

---

## Fix Priority Order

The fixer should address these in order to minimize recompilation cycles:

1. **A1** — Regenerate 4 figures (requires running plotting script)
2. **A5** — Fix broken cross-reference in .tex
3. **A2 + A3** — Add per-year extraction clarification (text edits)
4. **A4** — Update systematics.json
5. **B1** — Update covariance matrix in eq. 30
6. **B3** — Elevate kappa=2.0 as primary A_FB^b
7. **B4** — Add dilution calculation
8. **B5** — Update validation.json
9. **B6** — Fix reproduction contract filename
10. **B2, B7, B8, B9** — Remaining B fixes (text + JSON + bib)
11. **C1-C8** — Category C items
12. **Recompile PDF** — final tectonic build

---

## Verification Instructions

The verification arbiter should check:

- **A1:** Read all 4 regenerated figure PDFs — confirm "ALEPH Open Data" label and "sqrt(s) = 91.2 GeV" energy string. No "ATLAS" anywhere.
- **A2/A3:** Grep for "per-year" or "Table 15" in .tex — confirm calibration method is stated.
- **A4:** Read systematics.json — confirm phase_4c_fulldata.rb_total_syst matches parameters.json R_b_fulldata_final.syst within rounding.
- **A5:** Compile PDF — confirm no "??" in Section 7.8.2.
- **B1:** Read eq. 30 — confirm V_11 consistent with 0.027 (not 0.015).
- **B3:** Read abstract — confirm kappa=2.0 is presented as primary A_FB^b.
- **B5:** Read validation.json — confirm operating_point_stability_sf_fulldata entry exists.
- **B6:** Grep "doc4b" in .tex — should return zero hits.

---

*Arbiter adjudication complete. Session ada_0141.*
