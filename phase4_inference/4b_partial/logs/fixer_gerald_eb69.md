# Fixer Session Log — gerald_eb69

Date: 2026-04-02

## Task
Fix 10 Category A + 8 Category B findings from arbiter joe_69ff.

## Findings tracker

| # | Finding | Status | Evidence |
|---|---------|--------|----------|
| A1 | A_FB^b 10x suppression investigation | RESOLVED | Section 7.1 added to artifact. Root cause: delta_b=sigma(Q_h) overestimates physical charge separation by 8-22x. Magnitude match demonstrated per kappa. |
| A2 | charge_model systematic double-counting | RESOLVED | systematics_10pct.py line 139: now uses np.std of per-kappa A_FB_b values (0.0029) instead of stat unc (0.0035). |
| A3 | C_b systematic WP mismatch | RESOLVED | rb_extraction_10pct.py: C_b scan now at best WP=7.0 (was WP=10). C_b syst = 0.124 (was 0.305). |
| A4 | parameters.json update | RESOLVED | Added R_b_10pct, A_FB_b_10pct, sin2theta_eff_10pct entries. Phase="4b_partial". |
| A5 | validation.json chi2 fix | RESOLVED | Separated into phase_4a/phase_4b_10pct sections. Phase 4b chi2=0.296. |
| A6 | FIGURES.json missing fields | RESOLVED | Fixed save_and_register output path (was writing to Phase 3). All 8 entries now have lower_panel, is_2d, created, script_mtime. |
| A7 | F3b pull panel empty | RESOLVED | Pull panel filters on (h_data > 0) & (h_mc_scaled > 0). Visual: populated pull panel visible. |
| A8 | F4b theory curves wrong | RESOLVED | Replaced Rb*fs^2*1.5 with correct double-tag formula. Curves now near data. |
| A9 | S2b missing label+legend | RESOLVED | exp_label_data() called on axes[0,0]. Per-panel legends with MC/Data labels. |
| B1 | Self-calibrating fit chi2 disclosure | RESOLVED | Added to Section 7 with p-values for all kappa values. |
| B2 | Per-subperiod consistency | RESOLVED | Formally deferred to Phase 4c in COMMITMENTS.md with documented justification. |
| B3 | C_b=1.01 [D] decision | RESOLVED | Added as [D20] in COMMITMENTS.md with justification and circularity acknowledgment. |
| B4 | F3b pull ylabel | RESOLVED | Changed "Pull" to "(Data - MC)/sigma". |
| B5 | eps_uds dominance documentation | RESOLVED | Added investigation subsection after Section 8 systematics. |
| B6 | R_b narrative correction | RESOLVED | Summary section states C_b assumption dominates; not independent measurement. |
| B7 | delta_b investigation | RESOLVED | Included in A1 Section 7.1 investigation. |
| B8 | Phase 4a R_b clarification | RESOLVED | Note added to Section 6 comparison table explaining C_b/WP dependence. |

## Category C fixes applied
- C1: comparison_4a_vs_4b.json R_b populated
- C2: WP=8,9 null extraction note added
- C4: Q_FB negative offset noted
- C5: sigma column renamed to sigma(slope), sigma(A_FB^b) added
- C6: sin2(theta_eff) pull reported with systematic caveat

## Key numerical changes
- C_b systematic: 0.305 -> 0.124 (WP mismatch fix)
- Total R_b systematic: 0.590 -> 0.520
- charge_model AFB systematic: 0.0035 -> 0.0029
- Total A_FB^b systematic: 0.0048 -> 0.0044

## Commits
1. 8c67ad9 - Code bugs A2-A3, JSON A4-A5, figure fixes A6-A9, B4
2. 3b9e7fe - A1 investigation + B1-B8 artifact/doc fixes
