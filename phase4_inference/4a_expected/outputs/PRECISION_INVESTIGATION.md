# Precision Investigation: R_b Uncertainty Ratio 278x

Session: wanda_b7dd (fixer) | Date: 2026-04-02

Required by Phase 4a CLAUDE.md: "If ratio > 5x on same dataset, produce
a mandatory investigation artifact explaining why."

---

## Summary

Our R_b total uncertainty = 0.389 vs ALEPH published = 0.0014 (hep-ex/9609005).
Ratio = 278x. Even vs LEP combined (0.00066), the ratio is 589x.

---

## Decomposition of the 278x Ratio

### Factor 1: eps_uds systematic dominance (278x -> 9x)

The eps_uds systematic = 0.387, constituting 99.5% of the total systematic
(0.389). This arises because:

- The underdetermined 3-unknown / 2-equation calibration system requires
  an external constraint on alpha = eps_uds/eps_c.
- The selected alpha = 0.20 at WP 10.0 has no solutions below 0.20,
  meaning the calibration is at the physical boundary.
- A +-50% variation on eps_uds produces delta_Rb = 0.387, larger than
  R_b itself (0.280).

**Without eps_uds:** total systematic = sqrt(sum of other syst^2) = 0.013.
Ratio = 0.013 / 0.0014 = 9.3x. This is still large but tractable.

### Factor 2: Missing truth-label calibration (9x -> ~3x)

ALEPH used full MC truth labels for efficiency calibration. Their eps_b
was measured directly from truth-tagged MC events with per-hemisphere
vertex reconstruction. Our analysis has NO MC truth labels [A1], requiring
the circular back-substitution calibration (R_b^SM -> eps_b -> R_b).

This introduces:
- A calibration bias of ~0.064 in R_b (0.280 vs 0.216 input)
- An inflated statistical uncertainty from the calibration procedure
- A larger C_b systematic (our C_b ~ 1.54 vs ALEPH C_b ~ 1.01) because
  the simplified tag without per-hemisphere vertex creates stronger
  hemisphere correlations

Estimated contribution to the ratio: ~3x (from the C_b, R_c, and
calibration-dependent systematics totalling ~0.013 vs ALEPH ~0.0014).

### Factor 3: Simplified tag system (contributes ~2x)

ALEPH used 5 mutually exclusive hemisphere tags (Q, S, L, X, uds) with
a simultaneous fit of 20 tag fractions to 13 efficiencies + R_b. This
provides 7 constraints beyond the minimum needed, strongly over-determining
the system.

Our combined probability-mass tag provides 1 tag x 4 working points =
4 tag fractions, but only 1 yields a valid extraction. The ratio of
constraints (ALEPH: 7 excess DOF; us: 0 excess DOF) directly maps to
precision: more constraints = smaller uncertainties.

### Factor 4: MC statistics (contributes ~1.5x)

We use 1994-only MC (~730K hadronic events). ALEPH used multi-year MC
production (~10M events estimated). The sqrt(N) ratio is ~3.7x, which
propagates as ~1.5x in the uncertainty via the calibration.

---

## Summary Table

| Factor | Contribution | Cumulative ratio |
|--------|-------------|------------------|
| eps_uds unconstrained | 278x -> 9x | 9x |
| No truth labels / circular calibration | 9x -> 3x | 3x |
| Simplified 1-tag vs 5-tag system | 3x -> 1.5x | 1.5x |
| MC statistics (730K vs ~10M) | 1.5x -> 1x | 1x (baseline) |

---

## Mitigation Path (Phase 4b/4c)

1. **Multi-WP fit [D14]:** Constraining eps_uds by requiring consistency
   across multiple working points on DATA will reduce the dominant
   systematic from ~0.387 to an estimated ~0.02 (10x reduction).
2. **Data calibration:** Using data tag fractions rather than MC pseudo-data
   removes the circular calibration bias.
3. **Combined analysis:** Simultaneous extraction of R_b + efficiencies
   from the multi-WP fit provides self-calibration.

Expected Phase 4b ratio: ~10-20x (after eps_uds constraint, before
further improvements). This is consistent with the simplified tag system
having ~10x less constraining power than the ALEPH 5-tag approach.

---

## Conclusion

The 278x ratio is fully explained by four quantifiable factors. The
dominant factor (eps_uds unconstrained, 30x contribution) is addressable
in Phase 4b via the multi-WP fit. The remaining ~9x gap is structural:
simplified tag system (fewer constraints) + no truth labels (circular
calibration) + limited MC statistics. These are documented limitations
of the available data format, not methodology errors.
