# Plot Watcher Session Log
# Session: celeste_06a6
# Started: 2026-04-02

## Role
Plot watcher running in parallel with executor fabiola_b942 for Phase 1 exploration.
Evaluates each figure for publication quality as it is created.

## Standards Reference
- methodology/appendix-plotting.md — full plotting standards
- agents/plot_watcher.md — role definition

## Publication-Quality Gate Checklist
- [ ] Not blank/empty (has visible content in all panels)
- [ ] Experiment label visible and correctly positioned
- [ ] No "Axis 0" text artifacts
- [ ] Legend does not overlap data, curves, or error bars
- [ ] Every plotted element has a legend entry
- [ ] All text readable (not clipped, overlapping, or too small)
- [ ] Axis labels present with units, publication-quality names
- [ ] Error bars present and distinguishable (stat vs syst if both)
- [ ] Square aspect ratio (or justified non-square)
- [ ] No code variable names anywhere
- [ ] Font sizes visually match body text at rendered AN size
- [ ] Reference lines/bands clearly identified

## Key Rules (from appendix-plotting.md)
- figsize must be (10, 10) — non-negotiable
- mh.style.use("CMS") required
- exp_label with exp="ALEPH", data=True, llabel="Open Data" or "Open Simulation"
- No ax.set_title() — titles go in AN captions
- No tight_layout() — use bbox_inches="tight" at save
- Legend must not overlap data (use mpl_magic or manual placement)
- No code variable names in any visible text
- fontsize= numeric arguments forbidden (use relative strings like "x-small")
- Colorbar: must use make_square_add_cbar or cbarextend=True
- No "Axis 0" text artifacts

## Figure Reviews

Waiting for FIGURE_READY messages from executor fabiola_b942...

