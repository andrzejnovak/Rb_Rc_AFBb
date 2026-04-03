# Fixer Session Log — casimir_2c46

**Date:** 2026-04-02
**Task:** Fix 9 Category A + 10 Category B findings from arbiter verdict

## Progress

### A1: Closure test (a) — RESOLVED
Redesigned from negative-d0 (wrong d0 sign used) to mirrored-significance.
All positive significances flipped to negative. Result: f_s=0, R_b=0.
Complete elimination of lifetime signal confirms tag depends on displaced vertices.

### A2: Closure test (b) — RESOLVED
Replaced tautological R_b comparison with chi2/ndf shape comparison.
Compared bFlag=4 vs bFlag=-1 discriminant distributions.
chi2/ndf = 80127/7 = 11447. Shapes differ dramatically.

### A3: Track weights — RESOLVED
New script: track_weight_investigation.py. Weight mean ~1.02, range [0.03, 9.0].
Impact: <0.5% on Q_FB, ~3% on tag rates. Minor impact documented.
Recommendation: apply in Phase 4 as systematic.

### A4: D17 Primary vertex — RESOLVED
New script: d17_vertex_investigation.py. Three approaches:
1. Per-event median d0 spread = 71 micron (beam spot effects)
2. Data/MC scale factor ratio = 1.10
3. Vertex refit: INFEASIBLE (no vertex code in open data)
Systematic: +/-10% scale factor variation.

### A5: Cutflow labels — RESOLVED
Replaced passesAll, cos_theta_cut etc. with publication-quality text.

### A6: sigma_d0 labels — RESOLVED
Replaced nv1_p0_ct0 codes with human-readable bin descriptions.

### A7: Closure test figure — RESOLVED
Three-panel layout, no overlapping text, each test has own metric.

### A8: d0 sign validation — RESOLVED
Replaced bFlag=4 (99.8% of events) with tight double-tag (8% of events).
Curves now clearly separated: b-enriched ~0.55 vs inclusive ~0.30.

### A9: R_b bias documentation — RESOLVED
Added Section 7.1 with back-of-envelope (eps_c~0.30 needed vs 0.05 nominal).
Added figure annotation. Documented no plateau expected.

### B1: Contamination criterion — RESOLVED
Removed 0.1-10 threshold. Same-direction check only. Ratio 2.14 as open finding.

### B2: BDT deferral — RESOLVED
Added Section 12 formal downscoping document.

### B3: Chi2/ndf — RESOLVED
Added summary table with metrics for all three closure tests.

### B4: Plateau documentation — RESOLVED
Documented in Section 7.1 and figure annotation.

### B5: Hemisphere mass line — RESOLVED
Added 1.8 GeV/c^2 vertical line.

### B6: Closure test layout — RESOLVED
Three-panel layout replaces mixed-metric single axis.

### B7: R_b scan curves — RESOLVED
Black circles vs blue triangles with x-offset.

### B8: Gaussian validation — RESOLVED
MAD*1.48 = 1.10 (data, MC). Close to unit width. Documented.

### B9: Per-year info — RESOLVED
Year labels confirmed in preselected NPZ (1992-1995).

### B10: Parameter sensitivity — RESOLVED
Formally deferred to Phase 4 with documentation.

## Neighborhood Checks

- After fixing closure test (a): verified tests (b) and (c) also updated
- After fixing cutflow labels: checked all figure axis labels in plot_all.py
- After fixing R_b scan: verified both combined and probability scan use same formula
- After fixing closure figure: verified all three panels render correctly
