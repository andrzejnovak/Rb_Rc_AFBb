# Input Inventory — Phase 1

Session: fabiola_b942 | Date: 2026-04-02

## Summary

This inventory catalogues every external input the R_b/R_c/A_FB^b analysis
may need. Sources are the LEP corpus (MCP tools) and arXiv. The analysis
is an extraction measurement using the double-tag method, so the key
external inputs are: luminosities, hadronic cross-sections, SM predictions
for validation targets, and physics parameters for systematic evaluation.

## Inventory

| Input | Status | Value | Source | Search trail |
|-------|--------|-------|--------|--------------|
| R_b (LEP/SLD combined) | FOUND | 0.21629 +/- 0.00066 | hep-ex/0509008 | Corpus: 3q, arXiv: 1q |
| R_b (ALEPH reference) | FOUND | 0.2158 +/- 0.0009 +/- 0.0011 | hep-ex/9609005 | Corpus: 2q |
| R_c (LEP combined) | FOUND | 0.1721 +/- 0.0030 | hep-ex/0509008 | Corpus: 2q |
| R_c (ALEPH, charm counting) | FOUND | 0.166 +0.012/-0.011 +/- 0.009 | inspire_483143 | Corpus: 2q |
| A_FB^{0,b} (LEP combined) | FOUND | 0.0992 +/- 0.0016 | hep-ex/0509008 | Corpus: 2q |
| A_FB^b (ALEPH) | FOUND | 0.0927 +/- 0.0039 +/- 0.0034 | inspire_433746 | Corpus: 2q |
| sin^2(theta_eff) (ALEPH) | FOUND | 0.2330 +/- 0.0009 | inspire_433746 | Corpus: 2q |
| sin^2(theta_eff) (LEP/SLD) | FOUND | 0.23153 +/- 0.00016 | hep-ex/0509008 | Corpus: 2q, arXiv: 1q |
| sigma_0^had (ALEPH) | FOUND | 41.56 +/- 0.18 nb | inspire_367499 | Corpus: 2q |
| R_b^SM prediction | FOUND | 0.21578 | hep-ex/0509008 | Corpus: 2q |
| R_c^SM prediction | FOUND | 0.17223 | hep-ex/0509008 | Corpus: 2q |
| A_FB^{0,b} SM prediction | FOUND | 0.1032 | hep-ex/0509008 | Corpus: 2q |
| ALEPH hadronic events (total, 91-95) | FOUND | ~4.1 million | inspire_433746 (Table 1) | Corpus: 2q |
| ALEPH hadronic events per year | FOUND | See Table 1 | inspire_433746 | Corpus: 2q |
| Hadronic selection efficiency | FOUND | 99.1% (calo), 97.4% (track) | inspire_367499 | Corpus: 1q |
| ALEPH integrated luminosity per year | NOT FOUND | — | — | Corpus: 5q (luminosity, hadronic events, per year, data taking). Found total event counts but not per-year luminosity in pb^-1. hep-ex/0509008 may have this but paper not in corpus. |
| R_b SM (m_top dependence) | FOUND | R_b sensitive to m_top via vertex corrections | hep-ex/9811047 | Corpus: 1q |
| M_Z | FOUND | 91.1880 +/- 0.0020 GeV | PDG 2024 (pdglive.lbl.gov, node S044M) | WebFetch: pdglive Z boson mass |
| Gamma_Z | FOUND | 2.4955 +/- 0.0023 GeV | PDG 2024 (pdglive.lbl.gov, node S044) | WebFetch: pdglive Z boson width |
| g_bb splitting rate | FOUND | (0.26 +/- 0.04 +/- 0.09)% ALEPH | hep-ex/9811047 | Corpus: 1q |
| Hemisphere correlation C_b | NEEDS DERIVATION | MC-derived, ~1.0 | Phase 3-4 task | Will derive from MC |
| b fragmentation parameters | NOT FOUND | — | — | Corpus: 2q. Parameters needed for systematic variations. Will need dedicated search in Phase 2. |
| B+ lifetime | FOUND | (1.638 +/- 0.004) ps | PDG 2024 (pdglive.lbl.gov, node S041) | WebFetch: pdglive B+ mean life |
| B0 lifetime | FOUND | (1.517 +/- 0.004) ps | PDG 2024 (pdglive.lbl.gov, node S042) | WebFetch: pdglive B0 mean life |
| Bs0 lifetime | FOUND | (1.516 +/- 0.006) ps | PDG 2024 (pdglive.lbl.gov, node S086) | WebFetch: pdglive Bs0 mean life |
| Lambda_b lifetime | FOUND | (1.468 +/- 0.009) ps | PDG 2024 (pdglive.lbl.gov, node S040) | WebFetch: pdglive Lambda_b mean life |
| B meson decay multiplicity | FOUND | <n_ch> = 5.36 +/- 0.01 per B | CLEO (PRD 61, 072002, 2000); PDG 2024 tables | WebSearch: B meson charged multiplicity |

## Status Summary

- **FOUND:** 23 inputs with values and citations
- **NOT FOUND (with search trail):** 2 inputs (per-year luminosity, b fragmentation params)
- **NEEDS DERIVATION from data/MC:** 1 input (hemisphere correlation)

## Priority for Phase 2

1. **Luminosity per year** — Critical for any absolute cross-section calculation.
   The double-tag method for R_b extracts a ratio and does not need absolute
   luminosity, but R_c charm counting and any normalization checks do.
   Search trail: queried "ALEPH luminosity per year" (5 queries), found total
   event counts from inspire_433746 but not luminosity in pb^-1. The hep-ex/0509008
   paper likely contains this but is not in the corpus. Will need WebFetch to
   obtain the actual values.

2. **PDG values** — M_Z, Gamma_Z, B hadron properties: RESOLVED.
   All values fetched from PDG 2024 (pdglive.lbl.gov) with citations.

3. **b fragmentation parameters** — Needed for the MC model dependence
   systematic. Will search more specifically in Phase 2.
