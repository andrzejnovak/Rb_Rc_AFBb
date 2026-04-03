# Regression Check — Phase 4a

Date: 2026-04-03

| Check | Result | Evidence |
|-------|--------|----------|
| Validation test failures without 3 remediation attempts? | NO | A_FB chi2 investigated with 3 approaches (coarse bins, intercept fit, reweighting). Operating point stability honestly recorded as non-passing (single valid WP). |
| GoF toy distribution inconsistent with observed chi2? | N/A | No GoF toys at Phase 4a |
| Flat-prior gate excluding >50% of bins? | NO | N/A |
| Tautological comparison presented as validation? | NO | R_b extraction relabeled as self-consistency diagnostic. Closure tests properly labeled. |
| Visually identical distributions that should be independent? | NO | N/A |
| Result >30% deviation from reference? | YES — DOCUMENTED | R_b=0.280 vs SM=0.216 (30% deviation). Documented as expected: circular calibration on MC pseudo-data. Precision investigation artifact written. |
| All binding commitments fulfilled? | PARTIAL | [D9,D10] BDT formally downscoped. [D12b] four-quantity fit downscoped on symmetric MC. F3,F6 deferred. All downscopes documented. |
| Fit chi2 identically zero? | NO | R_b chi2 is null (single WP). A_FB chi2/ndf investigated and documented. |
| Precision comparison >5x reference? | YES — INVESTIGATED | R_b ratio=283x. Investigation artifact produced (PRECISION_INVESTIGATION.md): circular calibration, simplified tag, no per-hemisphere vertex. A_FB ratio=0.87x (competitive). |
| Normalization method documented? | YES | MC pseudo-data, no normalization needed |
| Dominant systematic >80% from one source? | YES — DOCUMENTED | eps_uds dominates R_b (>80%). Documented: will be constrained by multi-WP data fit at Phase 4b/4c. |
| Unresolved findings? | 2 PARTIAL | Independent closure at WP 10.0 and n_valid_toys need code rerun. Non-blocking for Doc 4a. |

**Verdict: Advance to Doc 4a.** The R_b extraction is a self-consistency diagnostic (circular calibration). The real measurement happens at Phase 4b/4c with data. The A_FB^b extraction correctly gives zero on symmetric MC (competitive precision 0.87x ALEPH). All critical findings addressed.
