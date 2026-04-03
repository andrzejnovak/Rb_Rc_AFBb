# Regression Ticket

Date: 2026-04-03
Trigger: Human gate REGRESS(4a) at Doc 4b
Origin: Phase 2 (Strategy) + Phase 4a (Inference)

## Root cause

The post-mortem investigations at Doc 4b discovered that:
1. The **3-tag system** (tight/loose/anti-b) gives R_b = 0.217-0.222, better than the 2-tag system
2. **Purity-corrected A_FB^b** = 0.074 ± 0.031 is much closer to SM than the raw value
3. **BDT tagging** (AUC 0.99) provides a better discriminant than cut-based
4. **eps_uds can be constrained from data** via the anti-tag

These methods should be the PRIMARY analysis, not post-mortem appendices. The AN reads as patched rather than coherent.

## Scope

### Phase 2 Strategy Update
- Primary R_b method: 3-tag system (tight/loose/anti-b)
- Primary A_FB^b: purity-corrected extraction with multi-purity calibration
- BDT as primary tagger (or at minimum a fully characterized alternative)
- eps_uds constrained from anti-tag data
- Proper uncertainty treatment (no "solver fails" placeholders)

### Phase 4a Re-execution
- Implement 3-tag extraction as primary
- Compute proper uncertainties on 3-tag R_b (toy-based)
- Implement purity-corrected A_FB^b with uncertainties
- Fix eps_c/eps_uds systematic treatment
- All results with complete uncertainty breakdown

### Doc 4a Rewrite
- One coherent story built around the best methods
- Not patched from previous versions
- All figure quality issues addressed from the start

### Phase 4b Re-execution
- Run 3-tag + purity-corrected on 10% data
- Update all JSON results

### Doc 4b Update + Human Gate
- Coherent AN with full results

## Impact
- Phase 3 selection infrastructure: UNCHANGED (tagging code works)
- Phase 4a: REWRITE (new primary methods)
- Doc 4a: REWRITE from scratch
- Phase 4b: REWRITE
- Doc 4b: REWRITE from updated Doc 4a
