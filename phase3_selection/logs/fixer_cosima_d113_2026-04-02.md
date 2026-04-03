# Fixer Session Log: cosima_d113

**Date:** 2026-04-02
**Task:** Fix 1 Category A + 5 Category B from arbiter phil2_94f9

## Resolution Status

| # | Category | Finding | Status | Evidence |
|---|----------|---------|--------|----------|
| 1 | A | MC tail ratio not in JSON | RESOLVED | d0_sign_validation.json now has mc.tail_ratio_3sigma.ratio_pos_over_neg = 3.62 |
| 2 | B | d0 sign validation JSON stale | RESOLVED | JSON uses tight double-tag (231,054 data, 62,952 MC events) not bFlag=4 |
| 3 | B | set_title calls in plot_all.py | RESOLVED | 3 set_title -> ax.text(), exp_label moved to axes[0], fontsize=5 -> "xx-small" |
| 4 | B | bFlag chi2 mislabeled | RESOLVED | Section 8 renamed "Validation Tests", test (b) = "bFlag discrimination power" |
| 5 | B | Contamination ratio labeling | RESOLVED | Labeled as "directional agreement", alarm band inapplicability explained |
| 6 | B | Mirrored-significance relabeling | RESOLVED | Labeled as "code sanity check", MC truth absence documented |

## Changes made

### d0_sign_validation.py
- Rewrote to use tight double-tag (combined > 8 both hemispheres) for b-enrichment
- Added MC computation alongside data
- Extracted common logic into _compute_tail_stats() helper
- Results: data ratio = 3.34, MC ratio = 3.62 (previously 1.76 data-only with bFlag=4)

### plot_all.py
- Lines 597, 618, 642: ax.set_title() -> ax.text() with bottom positioning
- Line 649: exp_label_data(axes[1]) -> exp_label_data(axes[0])
- Line 625: fontsize=5 -> fontsize="xx-small" (closure legend)
- Line 321: fontsize=5 -> fontsize="xx-small" (sigma_d0 tick labels)

### SELECTION.md
- Section 1: Updated key finding with new ratios (3.34 data, 3.62 MC)
- Section 3: Updated validation block with tight-tag method and both ratios
- Section 8: Renamed to "Validation Tests", relabeled all three tests
- Section 13: Updated validation table with new labels and ratios

### closure_results.json
- bflag_consistency.test: "bflag_shape_chi2" -> "bflag_discrimination_power"

### Verification
- d0_sign_validation.py: exit code 0, JSON verified with correct values
- plot_all.py: exit code 0, 20 figures regenerated
- Closure test figure: visually verified no set_title, no text collision
- Sigma_d0 figure: visually verified relative fontsize on tick labels

## Neighborhood checks
- Checked all fontsize values in plot_all.py: only the two fixed instances used absolute 5
- Checked all set_title calls: only the three fixed instances existed
- Checked all tail ratio references in SELECTION.md: Sections 1, 3, 13 all updated consistently
