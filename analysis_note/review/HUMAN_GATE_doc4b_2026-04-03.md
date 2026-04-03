# Human Gate Response — Doc 4b

Date: 2026-04-03
Response: **ITERATE**

## Verbatim human response

ITERATE. R_b looks reasonable-ish but it's confusing that in the chat you report "R_b works beautifully: 0.208 ± 0.066 on 10% data, only 0.12σ from SM. The method is validated.", while the doc show ~0.3. The syst still feels too high. 2) A_fb is 10x of expected result - this should have been immediately flagged for iteration. Overall this is not nearly exhaustive enough. You also never tried the alternative mc truth defining approaches - these could be tested and compared to existing, didnt even try to run the BDT/NN for tagging. R_c taken from SM is ok. You have deferred fixes sent for 4c, that should never happen really. Some Figures like 27 are way too small in tex. There is no way that each of the 4 plots is sized to .45 of linewidth. Fig 28 has a random caption in the plot that should have been in caption. Fig 30 pulls look sus, only 3 points show up? "δb overestimation identified as critical issue: The charge separation δb = σ(Qh) overestimates the physical value by 8–22× across κ, fully explaining the AFBb suppression. This must be corrected in Phase 4c via multi-purity fitting or MC-truth calibration" this is a typical issue that should be resolved before 4c - data can be used for calibrations before unblinding, just not for the target measurement. In future dirs 11: 2 - you say cant do 5 tag, but can you do 3 tag then? In fact you should have explored all the future directions here as well. Fig 25 again label on plot issue. Fig 36 violates our plotting spec - should be 2 separate figures. There's also a number of workflow artifacts in the AN phase 1/2/3 etc mentions, this should have been cleaned up. A_e and A_b are undefined. Provenance is only in the initial paragraph still, coloring not propagated through the AN. Fig 3 sizing is reasonably good, but could still be larger - fig 2 should have the same size of the individual plots, currently much smaller. Data/MC norms are not using luminosity/xs for scaling per spec, should be corrected and calibrated. Data in data/mc figures not indicated if 1994 only to match MC or all years... Gluon splitting maybe could be filtered out by trying to reconstruct the invariant mass right? Z will give ~90, gluons ~0, careful treatment is needed for gamma* DY process component tho. Links to files like "from systematics.json, field R_b.R_c.delta_Rb" are internal info that shouldnt be leaking into the AN. Physics wise basically you should have looked at the eta_light and eta_b, seen they are 100% unc and investigate further to constrain them better. Fig 15 overlap of legend and plot artists. Fig 17 not showing the aleph value - the yscale constrain on data is reasonable, but puts one of the values completely out - should have used split axes. Fig 18/19 not obviously readable, should be improved. Fig 20 again text overlap to artists. Fig 21 yscale issue again. Fig 24 shows weird inconsistencies between expected and measured. Fig 28 text issue. Fig 30 is definitely something you should have been able to do in phase3/4a it's data/MC of an input variable, not a measured result. 

## Categorized issues

### Physics/methodology (must do before Phase 4c)
1. Delta_b calibration from data NOW — not defer to Phase 4c. Data can be used for calibrations.
2. Try alternative MC truth approaches (decay chain, neutrino content) — never attempted
3. Try BDT/NN for tagging — was downscoped without trying
4. Explore 3-tag system if 5-tag infeasible
5. Constrain eps_uds and eps_b better (currently ~100% uncertainty)
6. Gluon splitting investigation via invariant mass reconstruction
7. Explore ALL future directions items now
8. Data/MC normalization should use luminosity/cross-section per spec

### AN content
9. R_b 0.208 vs 0.3 confusion — clarify Phase 4a vs 4b clearly
10. A_e and A_b undefined
11. Remove workflow artifacts (Phase 1/2/3 mentions)
12. Remove internal file references (systematics.json field names)
13. Provenance coloring propagated through full AN
14. Data in figures: clarify if 1994 only or all years

### Figures (15+ issues)
15-30: Fig 2/3 sizing, Fig 15 overlap, Fig 17 split axes, Fig 18/19 readability, Fig 20 overlap, Fig 21 yscale, Fig 24 inconsistencies, Fig 25 label, Fig 27 sizing, Fig 28 caption in plot, Fig 30 pulls, Fig 36 split into 2
