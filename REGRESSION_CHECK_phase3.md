# Regression Check — Phase 3

Date: 2026-04-02

| Check | Result | Evidence |
|-------|--------|----------|
| Validation test failures without 3 remediation attempts? | NO | Closure tests redesigned: (a) mirrored-significance=code sanity check (f_s=0 confirmed), (b) bFlag discrimination (chi2/ndf>>2 expected), (c) contamination injection (directional agreement documented) |
| GoF toy distribution inconsistent with observed chi2? | NO | N/A at Phase 3 |
| Flat-prior gate excluding >50% of bins? | NO | N/A at Phase 3 |
| Tautological comparison presented as validation? | NO | All closure tests properly labeled (sanity check vs discrimination vs directional) |
| Visually identical distributions that should be independent? | NO | d0 sign validation now uses tight double-tag enrichment (8% of events), clearly separated from inclusive |
| Result >30% deviation from reference? | YES — DOCUMENTED | R_b=0.83 vs expected 0.22. Quantitatively explained: uncalibrated eps_c/eps_uds at Phase 3. Phase 4 calibration will resolve. |
| All binding commitments fulfilled? | PARTIAL | [D19] PASS, [D7] done, [D8,D18] done, [D4,D5] done, [D17] investigated. [D9,D10] BDT formally downscoped. Per-year extraction deferred to Phase 4. |
| Fit chi2 identically zero? | NO | N/A at Phase 3 |
| Precision comparison >5x reference? | N/A | No final result at Phase 3 |
| Normalization method documented? | YES | MC normalized to data integral, documented |
| Dominant systematic >80% from one source? | N/A | Phase 4 task |
| Unresolved findings? | NO | All 9A+10B (iter 1) + 1A+5B (iter 2) resolved |

**Verdict: No blocking regression triggers. R_b bias is documented and expected — Phase 4 calibration required. Clear to advance.**
