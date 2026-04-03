# Phase 1 Execution Plan — fabiola_b942

Session: fabiola_b942
Date: 2026-04-02

## Objective

Data reconnaissance and literature survey for the measurement of R_b, R_c,
and A_FB^b in hadronic Z decays using archived ALEPH data at sqrt(s) = 91.2 GeV.

## Workstream 1: Data Reconnaissance

### 1.1 File inventory (script: `explore_files.py`)
- Open each ROOT data file (6 data files: 1992, 1993, 1994P1-P3, 1995)
- Open MC files (up to 30 files: LEP1MC1994_recons_aftercut-001..030)
- List all trees, branches with types and event counts
- Output: branch schema table in DATA_RECONNAISSANCE.md

### 1.2 Branch survey (script: `survey_branches.py`)
- For every integer/flag branch: unique values, range, mean
- Check for weight branches, quality flags
- Check for truth-level information (MC truth flavour, generator-level quantities)
- Identify track-level vs event-level structure (jagged arrays)

### 1.3 Pre-selection check
- Compare event counts to published L x sigma
- Estimate pre-selection efficiency f_presel per year
- Document what cuts were applied at ntuple level

### 1.4 Variable survey (script: `survey_variables.py`)
- Prototype on ~1000 events
- Key variables for b-tagging: signed impact parameter significance, secondary
  vertex properties, jet charge, track multiplicity
- Key event variables: thrust, sphericity, n_tracks, n_jets
- Data vs MC comparison for candidate discriminating variables
- Output: distribution plots in outputs/figures/

### 1.5 Data quality checks (script: `check_quality.py`)
- Check for NaN/inf values
- Check for unphysical values (negative energies, tracks with impossible kinematics)
- Check for discontinuities

## Workstream 2: Literature Search

### 2.1 LEP corpus queries
- Query: R_b measurement ALEPH lifetime tag
- Query: R_c measurement ALEPH
- Query: A_FB^b forward-backward asymmetry b-quark ALEPH
- Query: double-tag method hemisphere R_b
- Query: systematic uncertainties R_b R_c

### 2.2 arXiv/INSPIRE searches
- Search for modern R_b, R_c measurements or combinations
- Search for LEP electroweak precision measurements
- Search for sin^2(theta_eff) from A_FB^b

### 2.3 Reference analysis extraction
- Extract published values, uncertainties, methodology
- Identify luminosities, cross-sections, branching ratios needed
- Build INPUT_INVENTORY.md

### 2.4 Cross-experiment comparison
- Use compare_measurements for R_b, R_c, A_FB^b across LEP experiments

## Workstream 3: PDF Build Test

- Copy conventions/an_template.tex to analysis_note/test_build.tex
- Add test equation and citation
- Run tectonic
- Verify compilation, then delete stub

## Deliverables

1. `outputs/DATA_RECONNAISSANCE.md`
2. `outputs/INPUT_INVENTORY.md`
3. `outputs/LITERATURE_SURVEY.md`
4. `outputs/FIGURES.json` (figure registry)
5. Exploration figures in `outputs/figures/`
6. Updated `experiment_log.md`
7. Session log: `logs/executor_fabiola_b942_20260402.md`

## Figures planned

- F1: Track multiplicity distribution (data vs MC)
- F2: Impact parameter significance distribution (data vs MC)
- F3: Thrust distribution (data vs MC)
- F4: Jet charge distribution (data vs MC)
- F5: Branch type summary (diagnostic)
- F6: Event yield per data period (diagnostic)
