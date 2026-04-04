# Session log: fixer_sal_f027

**Date:** 2026-04-04
**Task:** Improve A_FB^b presentation in the analysis note

## What was done

### 1. Generated two new figures

- `F_afb_extraction.pdf`: Primary extraction figure showing <Q_FB> vs |cos(theta)| with the theory-shape fit overlaid. Annotation box on the figure shows the complete derivation chain: fitted product, chi2/ndf, published delta_b, and the resulting A_FB^b. The reader can verify the division on sight.

- `F_afb_signed_diagnostic.pdf`: Diagnostic figure showing <Q_FB> vs signed cos(theta) with linear and quadratic fits. Demonstrates the parabolic shape from |cos(theta)|-dependent b-tag purity, and explains why the folded extraction is used.

Script: `analysis_note/gen_afb_presentation.py`

### 2. Updated the analysis note (v9 -> v10)

Key changes in `ANALYSIS_NOTE_doc4c_v10.tex`:

- **Section 6.3 (Extraction formula):** Rewrote to show the actual fit model (theory shape `(8/3) cos/(1+cos^2) * delta_b * AFB`) instead of describing it as a simple linear fit. Added explicit 3-step derivation with numbered equations: (1) fit result with chi2, (2) published delta_b input, (3) division giving the result. Referenced the new extraction figure.

- **Section 9.2 (AFB extraction in Results):** Replaced the enumerated procedure to use the theory-shape model. Added explicit Step 1/2/3 derivation matching the extraction section, with cross-references to the new figures.

- **Section 6.4 (Angular fit model investigation):** Replaced the old 4-panel quadratic figure with the new signed diagnostic figure as the primary diagnostic, kept the old quadratic figure as supplementary. Updated text to reference both new figures.

### 3. Compiled with tectonic

PDF produced: `ANALYSIS_NOTE_doc4c_v10.pdf` (2.3 MiB). Only standard overfull/underfull hbox warnings.

## Key numbers (from afb_systematics_final.json)

- Fitted product: delta_b * AFB = 0.01517 +/- 0.00078
- chi2/ndf = 7.1/9 (p = 0.63)
- delta_b(kappa=0.3) = 0.162 (published ALEPH)
- AFB = 0.01517/0.162 = 0.0937 +/- 0.0048 (stat)

## Files created/modified

- NEW: `analysis_note/gen_afb_presentation.py`
- NEW: `analysis_note/figures/F_afb_extraction.{pdf,png}`
- NEW: `analysis_note/figures/F_afb_signed_diagnostic.{pdf,png}`
- NEW: `analysis_note/ANALYSIS_NOTE_doc4c_v10.tex`
- NEW: `analysis_note/ANALYSIS_NOTE_doc4c_v10.pdf`
- NEW: `analysis_note/logs/fixer_sal_f027.md` (this file)
