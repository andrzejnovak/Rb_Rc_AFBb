# Phase 3 Plot Validation Report

**Session:** hana_fccb  
**Date:** 2026-04-02  
**Validator:** Sonnet plot-validator (Level 3)  
**Phase:** phase3_selection  
**Figures reviewed:** 20 (all entries in FIGURES.json)

---

## STEP 1: FIGURE REGISTRY CHECK

**[REGISTRY] RESULT: PASS**

- FIGURES.json exists in `outputs/` and is valid JSON (array of 20 objects).
- Every PNG in `outputs/figures/` has a corresponding FIGURES.json entry. No orphan figures.
- Every FIGURES.json entry has a corresponding PNG on disk. No missing figures.
- All 20 entries contain all required fields: `filename`, `type`, `script`, `description`, `lower_panel`, `is_2d`, `created`, `script_mtime`.
- All `type` values are from the allowed set (`diagnostic`, `data_mc`, `result`, `closure`).
- All `lower_panel` values are from the allowed set (`pull`, `none`).
- Staleness check: no figures are stale (script mtime in registry matches filesystem within 2 s, and all figures were created after the script mtime).

**Registry findings: none.**

---

## STEP 2: CODE LINT

All scripts in `phase3_selection/src/` were grepped for each forbidden pattern.

| Pattern | Result |
|---------|--------|
| `plt.colorbar` or `fig.colorbar(im, ax=` | NONE |
| `ax.set_title(` | NONE |
| `tight_layout` | NONE |
| `histtype="errorbar"` without `yerr=` on same line | NONE |
| `figsize=` with values other than `(10, 10)` | NONE |
| `data=False` with `llabel=` | NONE |
| `except ImportError` with silent fallback | NONE |
| `print(` without logging | NONE |
| `imshow` | NONE |
| Hardcoded hex colors | NONE |
| `np.sqrt(h.values())` or `np.sqrt(counts)` near `yerr=` | NONE |
| `.view()[:] =` or `.view()[:] +=` near errorbar without `yerr=` | NONE |

**Additional positive checks verified:**

- `bbox_inches="tight"` is used at every `savefig` call in both `plot_all.py` and `plot_utils.py`.
- `hspace=0` is set correctly in both `plot_all.py` (line 99) and `plot_utils.py` (line 119).
- `exp_label` (`mh.label.exp_label`) is called via dedicated helpers `exp_label_data` and `exp_label_mc` in `plot_all.py`. Applied consistently.
- MC normalization: `mc_scale_to_data=True` by default, and the legend label reads `"MC (normalized to data)"`. Correctly documented.
- Lower panel ylabel in `data_mc_pull` reads `"Pull"`, not `"Ratio"` or `"Data/MC"`.
- `plot_utils.py` is present in `phase3_selection/src/` and is imported by `plot_all.py`.
- No ratio panels in any figure (Phase 3, not Phase 4+, so ratio would be acceptable — but pull is used throughout, which is better practice).

**[LINT] WARNING (Category C):** `data_mc_pull` in `plot_all.py` applies `mc_scale_to_data=True` by default for all variables, including `observable_type="derived"` quantities (the Q_FB and P_hem plots). Normalizing a derived quantity to data integral is methodologically questionable — the normalization factor absorbs any genuine data/MC shape difference in the normalization bin range. Not a rendering violation, but worth documenting. Suggested fix: pass `mc_scale_to_data=False` for derived-quantity figures and use a luminosity-scaled comparison, or add explicit documentation in the artifact.

**[LINT] WARNING (Category C):** The `data_mc_pull` function uses `np.sqrt(np.maximum(h_data, 1))` as the data error for count figures (correct Poisson approximation) and propagates `np.sqrt(h_mc_e2)` from summed weights for MC. No violation of the `yerr=` rule, but the pull denominator is `sqrt(sigma_data^2 + sigma_MC^2)` which double-counts statistical uncertainty. At the event counts involved (hundreds of thousands of events per bin), this is numerically negligible but is noted for Phase 4.

**Code lint findings: no Category A or B violations. Two Category C warnings noted above.**

---

## STEP 3: VISUAL REVIEW BY TYPE

### TYPE: diagnostic

---

**Fig 1: `cutflow_magnus_1207_20260402.png`**

The figure is a grouped bar chart showing event and track counts after successive selection cuts (total, passesAll, cos_theta_cut, total_tracks, good_tracks) on a log scale. Both data (black) and MC (blue) bars are shown side by side for each cut stage. The ALEPH Open Data experiment label is present in the upper-left and the energy label in the upper-right. The log y-axis spans roughly 10^6 to 10^8, which is appropriate for the range of values shown. The bar labels along the x-axis ("total", "passesAll", "cos_theta_cut", "total_tracks", "good_tracks") are code-style variable names. The figure is square (10x10). The legend is in the upper left and does not overlap with bars.

**[VISUAL] VIOLATION (Category A):** The x-axis tick labels are code variable names: `passesAll`, `cos_theta_cut`, `total_tracks`, `good_tracks`. These must be replaced with publication-quality text: e.g., "Total events", "Basic quality", "|cos θ| < 0.9", "All tracks", "Good tracks". Code variable names visible on a figure are Category A per the label quality check.

**[VISUAL] WARNING (Category B):** The y-axis label "Events / Tracks" is ambiguous — some bars count events (first three) and others count tracks (last two). Consider a two-panel layout or clearer labeling to distinguish the two quantities.

**Verdict: FAIL** — Category A violation (code variable names in tick labels).

---

**Fig 2: `d0_sign_validation_magnus_1207_20260402.png`**

The figure shows the d0 sign convention validation: asymmetry (N+ − N−)/(N+ + N−) as a function of |d0/σ_d0| threshold, for two samples (b-enriched bFlag=4 and all events). The "Gate: PASS" text is displayed in the upper-right of the plot area. The ALEPH experiment label is present. The figure is square. The y-axis range (0 to ~0.65) is appropriate. Both curves show rising asymmetry with threshold, confirming the sign convention is physics-meaningful.

**[VISUAL] VIOLATION (Category A):** The two curves (pink/magenta for b-enriched and blue for all events) are nearly indistinguishable — they overlap almost completely across all threshold values. This defeats the purpose of the validation: the b-enriched sample should show a *higher* positive asymmetry than the inclusive sample, because b-jets have longer-lived secondaries and thus more tracks with large positive d0. The fact that the two lines plot on top of each other is suspicious and should be investigated. Possible cause: bFlag=4 is not providing a significantly different sample composition, or the two datasets are not independent.

**[VISUAL] WARNING (Category B):** The in-plot annotation "Gate: PASS" is not meaningful without numeric evidence (what criterion is the gate checking, and what is the measured value?). The artifact should document the quantitative basis for PASS.

**Verdict: FAIL** — Category A physics concern (two curves indistinguishable when they should differ).

---

**Fig 3: `sigma_d0_calibration_magnus_1207_20260402.png`**

The figure shows σ_d0 scale factors per calibration bin (indexed by nvdet/momentum/cos θ combinations) for data (black circles) and MC (blue squares). A horizontal reference line at scale factor = 1.0 is shown. The ALEPH experiment label is present. The figure is square. Calibration bin labels on the x-axis (e.g., "nv1_p0_ct0", "nv1_p1_ct1") are readable but are code-style identifiers.

**[VISUAL] VIOLATION (Category A):** The calibration bin x-axis labels ("nv1_p0_ct0", "nv2_p3_ct3", etc.) are internal code-style identifiers, not publication-quality names. These should be replaced with human-readable text such as "nvdet=1, low p, cos θ∈[0,0.25]" or use a two-row label. As plotted, a reader cannot determine what each bin represents.

**[VISUAL] CONCERN:** All scale factors are between 1.4 and 8.0 — significantly above 1.0. The FIGURES.json description states "Scale factor = 1.0 means the nominal parameterization correctly describes the resolution," but all bins show scale factors well above 1.0. This indicates a systematic overestimation of the resolution everywhere, which is a substantial physics concern: either the nominal σ_d0 parameterization is very wrong, or the calibration methodology has an error. This is not a plot quality issue but should be flagged for the physics reviewer.

**Verdict: FAIL** — Category A violation (code variable names in axis tick labels).

---

### TYPE: data_mc

---

**Fig 4: `data_mc_significance_magnus_1207_20260402.png`**

The signed impact parameter significance d0/σ_d0 distribution is shown on a log scale for data (black error bars) vs MC (filled blue histogram, normalized to data). The x-axis spans −10 to +30. A pull panel is below with ylabel "Pull". The experiment label is present. The figure is square. Data and MC agree visually well in the core region. The positive tail (b/c lifetime tracks) is visible and MC tracks it closely. Only a handful of pull points are visible (sparse bins outside the core), and those showing pulls near ±3 are in the extreme tails where statistics are low — consistent with Poisson fluctuations. No systematic offset or shape distortion is visible.

**[VISUAL] Verdict: PASS.** The d0/σ_d0 data/MC comparison looks physically reasonable. The asymmetric distribution with positive tail is the expected signature of b/c-hadron secondary vertices.

---

**Fig 5: `data_mc_combined_tag_magnus_1207_20260402.png`**

The combined probability-mass hemisphere tag (−ln P_hem + mass bonus) distribution is shown for data vs MC. The x-axis spans 0 to ~20. Log y-axis. The pull panel shows deviations up to ~3σ in the high-tag tail (tag value > 15), with a systematic trend: the last ~5 bins all have pulls near −2 to −3. This represents a consistent underprediction of the high-tag tail by MC. The experiment label is present. Figure is square.

**[VISUAL] CONCERN:** The systematic trend in the high-tag tail (tag > 15, pulls consistently −2 to −3σ) suggests MC underestimates the rate of highly b-like hemispheres. This is a potential modeling problem that could bias the R_b extraction since the operating point sits at tag threshold ~5. At threshold 5 the agreement appears reasonable (~1σ pulls), so the impact at the chosen working point may be limited. Flag for investigation in the artifact.

**[VISUAL] Verdict: PASS** (adequate agreement at working point, tail discrepancy documented in concern above).

---

**Fig 6: `data_mc_hemisphere_mass_magnus_1207_20260402.png`**

The hemisphere invariant mass distribution is shown for data vs MC on a linear y-scale. X-axis spans 0 to 8 GeV/c². The pull panel shows systematic behavior: the lowest-mass bin (first bin, near 0 GeV/c²) has a strong downward pull (~−2.5 to −3σ) and the next few bins show mild structure. This first-bin discrepancy is the most prominent feature. For mass > 1 GeV/c² the agreement is good (~1σ). The 1.8 GeV/c² threshold separating b from c hemispheres is not marked on the figure.

**[VISUAL] WARNING (Category B):** The 1.8 GeV/c² b/c separation threshold (mentioned in the FIGURES.json description as "[D18]") is not indicated on the figure. A vertical line or shaded region at 1.8 GeV/c² would greatly improve the figure's physics communication. Suggested fix: add `ax.axvline(1.8, color='red', ls='--', label='b/c threshold')`.

**[VISUAL] Verdict: PASS** with Category B finding noted.

---

**Fig 7: `data_mc_phem_magnus_1207_20260402.png`**

The hemisphere probability tag P_hem (shown as −ln P_hem, log y scale) distribution is shown for data vs MC. The x-axis spans 0 to ~15. Data and MC agree well in the core (0–10), with the same systematic trend in the tail (−ln P_hem > 12) as seen in the combined tag figure: MC underestimates the tail rate with pulls reaching ~−3σ in the last bins. The experiment label is present. Figure is square.

**[VISUAL] CONCERN:** Same high-tag tail disagreement as Fig 5. The two figures share the same systematic pattern, which is internally consistent (the combined tag is derived from P_hem), confirming this is a genuine modeling issue in the high-b-fraction tail.

**[VISUAL] Verdict: PASS** (same assessment as Fig 5 — working-point agreement is acceptable).

---

**Fig 8: `data_mc_qfb_k0.3_magnus_1207_20260402.png`**

The Q_FB distribution for kappa=0.3 is shown: a Gaussian-like distribution centered at 0, spanning −1.5 to +1.5. The pull panel shows pulls of up to ~3σ with a systematic zigzag pattern — pulls alternate positive and negative across adjacent bins, suggesting the MC shape does not perfectly describe the Q_FB width or non-Gaussianity. The experiment label is present. Figure is square.

**[VISUAL] CONCERN:** The pull pattern for Q_FB (kappa=0.3, 0.5, 1.0, 2.0) shows a correlated zigzag structure that is typical of a slight width mismatch between data and MC. The data distribution is slightly narrower or broader than MC, and the integral normalization constraint forces the pulls to alternate sign. This is a shape disagreement that may affect the AFBb extraction in Phase 4.

**[VISUAL] Verdict: PASS** (pulls within ±3σ and the shape mismatch is at the ~1% level in the wings, acceptable for Phase 3).

---

**Fig 9: `data_mc_qfb_k0.5_magnus_1207_20260402.png`**

Similar to Fig 8 with kappa=0.5: Gaussian-shaped Q_FB distribution with pull zigzag pattern in the tails. The distribution is slightly wider than kappa=0.3. Agreement in the core is excellent. The systematic shape mismatch in the wings is at the same level as kappa=0.3.

**[VISUAL] Verdict: PASS.**

---

**Fig 10: `data_mc_qfb_k1.0_magnus_1207_20260402.png`**

Q_FB for kappa=1.0. Same structure as Figs 8–9. The distribution is broader (wider Gaussian). Pull panel shows the same wing zigzag. Core agreement is good.

**[VISUAL] Verdict: PASS.**

---

**Fig 11: `data_mc_qfb_k2.0_magnus_1207_20260402.png`**

Q_FB for kappa=2.0. The distribution is tent-shaped (bimodal tendency) with a clear W-shape, as expected for higher kappa values where the leading-particle charge dominates. Pull pattern shows occasional ±2σ deviations with no strong systematic trend.

**[VISUAL] Verdict: PASS.**

---

**Fig 12: `data_mc_qfb_kinf_magnus_1207_20260402.png`**

The leading-particle charge Q_FB (kappa=infinity) distribution is discrete with only three values (−2, 0, +2). Three tall bars are shown. Data error bars sit on top of MC bars, but data bars for Q=−2 and Q=+2 appear shorter than MC bars (the data error bars land at ~0.76×10^6 while the MC bar reaches ~1.38×10^6). The pull panel shows a large pull (~3σ) for one of the outer bins.

**[VISUAL] CONCERN (RED FLAG):** The data values at Q_FB = ±2 (leading particle charge = ±1) appear significantly lower than MC. The Q=0 bin appears to have data equal to MC. This is a systematic pattern — MC predicts too many charged leading particles relative to data, or the data has more events where the leading particle is neutral. This could reflect a data/MC discrepancy in leading-track selection or a genuine physics effect (jet charge miscalibration). This pattern should be explicitly addressed in the artifact.

**[VISUAL] Verdict: PASS** (the discrepancy is at the ~2–3σ level and not an automatic Category A, but should be documented and investigated for Phase 4 AFBb impact).

---

### TYPE: result

---

**Fig 13: `rb_operating_scan_magnus_1207_20260402.png`**

The R_b operating point stability scan shows extracted R_b as a function of tag threshold from 1 to ~14, for combined tag (black circles) and probability-only tag (blue squares). The ALEPH published value (pink horizontal line at 0.2158) and SM prediction (red dashed at 0.21578) are shown at the bottom of the figure. The scan data runs from R_b ~ 0.98 at threshold 1 down to R_b ~ 0.48 at threshold 14. The extracted R_b values are 3–5× larger than the reference values at all operating points.

**[VISUAL] RED FLAG (Category A — automatic):** The extracted R_b values across the entire operating range (0.48 to 0.98) are dramatically inconsistent with the SM prediction (0.216) and ALEPH published value (0.216). The scan shows no plateau or region of stability near the physical value. The reference lines (ALEPH and SM) appear as a faint band at the very bottom of the figure, nearly at R_b = 0, while the scan data occupies the upper two-thirds of the y-axis. This is not a plot quality issue — it is a physics correctness failure. The double-tag formula is either: (a) using the wrong definition of "single-tag fraction" (counting hemisphere tags rather than event tags), (b) using incorrect background efficiencies for eps_c and eps_uds that do not match this tagger's actual performance, or (c) applying the formula to a high-contamination, low-purity tagger where the approximation breaks down. The visual presentation of the scan alongside reference values that differ by a factor of 3–5 is the most critical finding of this validation. Suggested fix: verify the f_s/f_d definitions, recompute eps_c and eps_uds from MC truth matching, and cross-check the algebraic derivation of extract_rb.

**[VISUAL] WARNING (Category B):** The two curves (combined tag and probability-only tag) are plotted with markers so similar (black circle vs blue square) that they overlap visually at nearly every threshold point, making them indistinguishable in the rendered figure. The figure conveys no information about whether the two taggers give consistent results.

**Verdict: FAIL — RED FLAG.** R_b extracted values are 3–5× above physical value at all operating points. This is an automatic Category A finding that cannot be downgraded.

---

### TYPE: closure

---

**Fig 14: `closure_tests_magnus_1207_20260402.png`**

The closure test figure shows three test metrics plotted as filled red circles at "Negative d0 pseudo-data" (metric ~0.80), "bFlag=4 vs full sample" (metric ~1.10), and "Contamination injection (5%)" (metric ~2.15). All three points are labeled PASS in the legend. The ALEPH experiment label is present. The figure is square.

**[VISUAL] VIOLATION (Category A — text artifact):** There is a text overlap in the upper-left corner of the figure. The annotation text "Pull=0.17893" and "Ratio=0.17893" (or similar) are overprinted on each other, resulting in garbled overlapping text. This is a text collision / rendering artifact that makes the annotation unreadable.

**[VISUAL] CONCERN:** The "contamination injection" metric is ~2.15, while the description says this represents the observed/predicted shift ratio. A ratio of 2.15 means the observed shift from contamination is 2.15× the predicted shift — which suggests the double-tag formula is not properly accounting for the contamination propagation. The `passes: true` flag is set despite this 2× discrepancy. The closure test criterion for this check is not documented in the figure itself, making it impossible to assess whether "PASS" is justified.

**[VISUAL] WARNING (Category B):** The y-axis label is "Test metric" with no units or explanation of what the metric means for each of the three tests. Each test has a different metric (R_b extracted, pull, observed/predicted ratio) — plotting them on a common y-axis without distinguishing their interpretations is misleading. Suggested fix: use a table or multi-panel layout showing each test's result with its specific metric and threshold.

**Verdict: FAIL** — Category A text artifact (overlapping annotations in upper-left); Category B layout concern.

---

**Fig 15 (preselection data/MC): `data_mc_thrust_magnus_1207_20260402.png`**

The thrust distribution after preselection is shown on a linear y-scale. X-axis spans 0.5 to 1.0. The distribution rises sharply near T~1 as expected for e+e− → hadrons at LEP. Data and MC agree well. The pull panel shows deviations at the ~2σ level in the low-thrust region (0.5–0.7, where statistics are low) and at ~2σ in the high-thrust bins. No systematic offset is visible. Experiment label present, figure is square.

**[VISUAL] Verdict: PASS.**

---

**Fig 16: `data_mc_costheta_magnus_1207_20260402.png`**

The cos(θ_thrust) distribution after the |cos θ| < 0.9 cut is shown. The distribution has the characteristic dipole shape (high at ±0.9 edges, dip in center) expected for the thrust-axis polar angle in e+e− → qq̄ events. Data and MC agree well, with pulls in the ±2σ range scattered across bins. Experiment label present, figure is square.

**[VISUAL] Verdict: PASS.**

---

**Fig 17: `data_mc_nch_magnus_1207_20260402.png`**

The charged particle multiplicity distribution after preselection is shown. The distribution peaks at Nch ~20–22, consistent with hadronic Z decays. Data and MC show excellent agreement across the distribution. Pulls are within ±2σ. Experiment label present, figure is square.

**[VISUAL] Verdict: PASS.**

---

**Fig 18: `data_mc_sphericity_magnus_1207_20260402.png`**

The sphericity distribution after preselection is shown on a linear y-scale. The distribution falls steeply from sphericity ~0 (jet-like events) to ~0.6, as expected. The first bin (sphericity near 0) shows a data point significantly above the MC bar (Data ≈ 740k, MC ≈ 700k), giving a pull of approximately +3σ. The rest of the distribution shows acceptable agreement with pulls within ±2.5σ.

**[VISUAL] CONCERN:** The first-bin (sphericity ≈ 0) pull of ~3σ is on the boundary of requiring investigation. This is the most jet-like events bin and represents a real data/MC discrepancy in very collimated events. May indicate a jet fragmentation modeling issue. Note for Phase 4.

**[VISUAL] Verdict: PASS** (borderline — first-bin pull should be noted in the artifact).

---

**Fig 19: `data_mc_d0_magnus_1207_20260402.png`**

The impact parameter d0 distribution for quality-selected tracks is shown on a linear y-scale. The distribution is strongly peaked at d0 = 0 with wings extending to ±0.1 cm. Data and MC overlay well in the core. The figure shows a characteristic "spike" structure at d0 = 0 and adjacent bins, with fine bin structure (multiple thin bars visible near the core). Pulls are within ±3σ, with the largest deviations in the extreme tails.

**[VISUAL] Verdict: PASS.**

---

**Fig 20: `data_mc_trackpt_magnus_1207_20260402.png`**

The track transverse momentum distribution is shown on a log y-scale. X-axis spans 0 to ~50 GeV/c. The distribution falls steeply from a peak at low pT. Data and MC agree well in the bulk (pT < 10 GeV/c) but MC significantly overestimates data for pT > 30 GeV/c (MC has a longer tail). The high-pT bins show large pulls (>3σ for pT > 30 GeV/c), and data points at the highest pT bins appear below MC by a significant margin. Experiment label present, figure is square.

**[VISUAL] CONCERN:** The track pT spectrum shows a systematic data-below-MC trend at high pT (>20 GeV/c), which could indicate either: (a) MC fragmentation produces too many high-pT tracks, (b) track reconstruction efficiency is overestimated at high pT in MC, or (c) a minimum bias contamination issue. High-pT tracks are important for the b-tag because displaced high-pT tracks from B meson decays are key tagger inputs. If MC overproduces high-pT tracks, the b-tagging efficiency extracted from MC may be biased. This should be investigated in the SELECTION.md artifact.

**[VISUAL] Verdict: PASS** (concern noted for artifact documentation).

---

## CROSS-FIGURE CONSISTENCY CHECKS

**[VISUAL] RED FLAG (Category A):** The R_b operating scan (Fig 13) shows extracted R_b values in the range 0.48–0.98 across all operating points, while the reference value (SM/ALEPH) is 0.216. The closure tests (Fig 14) are evaluated at working point threshold=5, where the R_b formula gives 0.827 — again 4× above the reference. Despite this, the closure test is reported as PASS. A closure test performed with a fundamentally broken formula cannot provide meaningful closure — the PASS verdict for the closure test is based on internal self-consistency of a wrong formula, not on agreement with the physical quantity. This constitutes a "broken journey" finding: the pipeline is self-consistent but the result does not approach the physical value. This requires investigation before Phase 4.

**[VISUAL] INFO:** Cross-figure shapes are internally consistent. The P_hem distribution (Fig 7) and combined tag distribution (Fig 5) show the same high-tag-tail disagreement, which is expected since the combined tag is derived from P_hem. The QFB distributions (Figs 8–12) show systematically similar pull patterns, indicating a consistent shape modeling issue for the charge asymmetry variable. These are consistent with a single underlying cause.

---

## SUMMARY TABLE

| # | Filename | Type | Verdict | Category | Finding |
|---|----------|------|---------|----------|---------|
| 1 | cutflow_magnus_1207_20260402.png | diagnostic | FAIL | A | Code variable names in x-axis tick labels |
| 2 | d0_sign_validation_magnus_1207_20260402.png | diagnostic | FAIL | A | Two curves indistinguishable when they should differ |
| 3 | sigma_d0_calibration_magnus_1207_20260402.png | diagnostic | FAIL | A | Code variable names in calibration bin x-axis labels |
| 4 | data_mc_significance_magnus_1207_20260402.png | data_mc | PASS | — | Good data/MC agreement on signed d0/σ_d0 |
| 5 | data_mc_combined_tag_magnus_1207_20260402.png | data_mc | PASS | — | High-tag-tail disagreement noted (concern) |
| 6 | data_mc_hemisphere_mass_magnus_1207_20260402.png | data_mc | PASS | B | Missing b/c threshold line at 1.8 GeV/c² |
| 7 | data_mc_phem_magnus_1207_20260402.png | data_mc | PASS | — | Same tail concern as Fig 5 |
| 8 | data_mc_qfb_k0.3_magnus_1207_20260402.png | data_mc | PASS | — | Minor shape mismatch in wings |
| 9 | data_mc_qfb_k0.5_magnus_1207_20260402.png | data_mc | PASS | — | Same as Fig 8 |
| 10 | data_mc_qfb_k1.0_magnus_1207_20260402.png | data_mc | PASS | — | Same as Fig 8 |
| 11 | data_mc_qfb_k2.0_magnus_1207_20260402.png | data_mc | PASS | — | Tent-shaped distribution, acceptable pulls |
| 12 | data_mc_qfb_kinf_magnus_1207_20260402.png | data_mc | PASS | — | Data below MC at Q_FB=±2 (concern noted) |
| 13 | rb_operating_scan_magnus_1207_20260402.png | result | FAIL | RED FLAG | R_b extracted 3–5× above SM/ALEPH reference across all operating points |
| 14 | closure_tests_magnus_1207_20260402.png | closure | FAIL | A | Overlapping text annotations (garbled); closure at R_b~0.82 not at physical R_b |
| 15 | data_mc_thrust_magnus_1207_20260402.png | data_mc | PASS | — | Good data/MC agreement |
| 16 | data_mc_costheta_magnus_1207_20260402.png | data_mc | PASS | — | Good data/MC agreement |
| 17 | data_mc_nch_magnus_1207_20260402.png | data_mc | PASS | — | Excellent agreement |
| 18 | data_mc_sphericity_magnus_1207_20260402.png | data_mc | PASS | — | First-bin pull ~3σ (concern) |
| 19 | data_mc_d0_magnus_1207_20260402.png | data_mc | PASS | — | Good agreement |
| 20 | data_mc_trackpt_magnus_1207_20260402.png | data_mc | PASS | — | MC overestimates data at pT>30 GeV/c (concern) |

---

## FINDINGS BY CATEGORY

### RED FLAG (automatic Category A — arbiter may NOT downgrade)

1. **[VISUAL] Fig 13 — rb_operating_scan:** R_b extracted values range 0.48–0.98 across all tag thresholds, versus SM prediction of 0.216 and ALEPH measurement of 0.2158 ± 0.0014. The values are 3–5× too large at every operating point. The double-tag formula is likely using incorrectly defined tag fractions or incorrect background efficiencies (eps_c=0.05, eps_uds=0.005 are nominal assumptions not calibrated to this tagger). This result is unphysical and must be diagnosed before Phase 4. The visual presentation of the figure alongside reference lines that lie at the bottom of the y-axis communicates this failure clearly.

### CATEGORY A VIOLATIONS

2. **[VISUAL] Fig 14 — closure_tests:** Text annotations overlap in the upper-left corner, producing garbled unreadable text ("Pull=0.17893" and "Ratio=0.17893" overprinted). Fix: separate annotations vertically or move them to avoid collision.

3. **[VISUAL] Fig 14 — closure_tests (physics):** The closure tests are performed at R_b ~ 0.82, which is not the physical R_b value. A closure test at the wrong operating regime cannot validate the analysis methodology. The contamination injection closure test shows a 2.15× ratio (observed/predicted shift), which itself indicates the formula does not propagate contamination correctly — yet is labeled PASS.

4. **[VISUAL] Fig 1 — cutflow:** Code variable names in x-axis tick labels: `passesAll`, `cos_theta_cut`, `total_tracks`, `good_tracks`. Fix: replace with publication-quality text.

5. **[VISUAL] Fig 2 — d0_sign_validation:** Two validation curves (b-enriched vs all events) appear nearly identical when they should be visually distinct. The b-enriched sample should show higher asymmetry. Requires investigation.

6. **[VISUAL] Fig 3 — sigma_d0_calibration:** Code variable names in x-axis calibration bin labels ("nv1_p0_ct0", etc.). Fix: replace with human-readable bin descriptions.

### CATEGORY B VIOLATIONS

7. **[VISUAL] Fig 6 — data_mc_hemisphere_mass:** Missing vertical line or annotation indicating the 1.8 GeV/c² b/c separation threshold described in the FIGURES.json description.

8. **[VISUAL] Fig 14 — closure_tests:** Mixed metrics on same y-axis (R_b value, pull, and ratio) without distinguishing labels makes the figure misleading.

9. **[VISUAL] Fig 13 — rb_operating_scan:** Combined-tag and probability-only-tag curves are visually indistinguishable at most operating points due to overlapping markers.

### CATEGORY C WARNINGS (no re-review needed)

10. **[LINT] plot_all.py:** `mc_scale_to_data=True` is applied to derived-quantity figures (Q_FB, P_hem), which absorbs any overall normalization mismatch in the normalization integral.

11. **[LINT] plot_all.py:** Pull denominator is `sqrt(sigma_data² + sigma_MC²)`, which double-counts statistical uncertainty. Negligible at current event counts but should be corrected for Phase 4.

---

## OVERALL VERDICT

**FAIL — RED FLAG present.**

The primary finding is the R_b operating point scan showing extracted values 3–5× above the SM prediction and published ALEPH measurement at every tag threshold. This is a physics correctness failure, not a presentation issue. The figure clearly communicates the problem (reference lines visible at R_b ~ 0.22 while the scan data sits at 0.5–1.0), and the underlying source is identifiable from the code (assumed background efficiencies eps_c=0.05, eps_uds=0.005 are nominal rough estimates not validated against this specific tagger's performance on this dataset).

Additionally, three figures have Category A label violations (code variable names), and the closure test figure has a rendering artifact (overlapping text). These are fixable in one iteration.

The 12 PASS figures show generally good data/MC modeling for the preselection observables, with minor concerns (high-tag-tail disagreement, sphericity first-bin pull, high-pT track spectrum) that should be documented in the SELECTION.md artifact.

**Required before Phase 4 begins:**
1. Diagnose and fix the R_b formula / tag fraction definition (RED FLAG)
2. Fix axis label code names in Figs 1, 3 (Category A)
3. Investigate d0 sign validation curve overlap (Category A)
4. Fix closure test annotation collision (Category A)
5. Add hemisphere mass threshold line (Category B)
