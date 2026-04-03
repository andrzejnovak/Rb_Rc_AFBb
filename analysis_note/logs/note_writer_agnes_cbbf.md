# Session Log: note_writer_agnes_cbbf

Date: 2026-04-02
Task: Integrate 7 post-mortem investigation results into AN v4

## Actions taken

1. Copied ANALYSIS_NOTE_doc4b_v3.tex to v4.tex
2. Read all 6 investigation JSON files (delta_b_calibration, three_tag_results, bdt_tag_results, mc_truth_proxies, gluon_splitting_results, normalization_check)
3. Added v4 change log entry documenting all changes
4. **CRITICAL: Updated A_FB^b narrative** — replaced "delta_b overestimation" root cause with "low b-purity" (f_b ~ 18%, eps_c > eps_b). Added purity-corrected A_FB^b values (0.05-0.08 depending on kappa; 0.074 +/- 0.031 at kappa=2.0, within 2sigma of SM).
5. Added new Section "Post-mortem investigations" with 7 subsections documenting all investigations with key numbers from JSON files
6. Updated results summary table with 3-tag R_b (0.217-0.222) and purity-corrected A_FB^b (0.074 +/- 0.031)
7. Updated abstract with corrected narrative and new results
8. Updated conclusions with 8 findings (was 6)
9. Updated outlook section to focus on b-purity improvement rather than delta_b fix
10. Updated comparison section with 3-tag cross-check and purity-corrected A_FB^b
11. Updated parameters.json with R_b_3tag and A_FB_b_purity_corrected entries
12. Updated COMMITMENTS.md marking 7 investigations as completed

## Key numbers integrated
- delta_b overestimation factor: ~1.0-1.2x (NOT 8-22x as previously stated)
- b-purity: f_b ~ 18-19% at WP 10.0
- eps_c = 0.44 > eps_b = 0.15 (root cause)
- Purity-corrected A_FB^b: 0.074 +/- 0.031 (kappa=2.0, threshold=2)
- 3-tag R_b: 0.217-0.222 (5 configurations, all near SM 0.216)
- BDT AUC: 0.987-0.996
- Gluon splitting: 1.1% of events
- eps_uds data/MC ratio: 1.015 (anti-tag constraint)
- Data/MC normalization ratio: 3.95 (self-normalizing methods)
