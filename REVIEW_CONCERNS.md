# Review Concerns

Cross-phase review memory. Append findings here after each
review; every reviewer reads this file at session start.

---

## Phase 2 Strategy Review — sigrid_16b8 (2026-04-02)

### Cross-phase concerns to carry forward

**[CP1] Closure test tautology (Category A, Phase 2):**  
The committed closure test (MC split, derivation vs validation halves) will produce pull ≈ 0 by algebraic construction because both halves use the same generator, same efficiency model. Must be redesigned before Phase 3. Future reviewers: verify the Phase 3 closure test uses an operationally independent sample (e.g., negative-d0 tail, bFlag subsets) or artificial contamination injection, NOT a same-MC-half split.

**[CP2] A_FB^b extraction formula (Category A, Phase 2):**  
The simplified formula A_FB^b = (8/3)*<Q_FB>/(R_b*delta_b) in LITERATURE_SURVEY.md is inconsistent with the correct self-calibrating chi2 fit to 5 event categories (N, N_bar, N^D, N^D_bar, N^same) described in inspire_433746 Section 4. Phase 3/4 reviewers: verify that the implemented extraction uses the correct 5-category chi2 fit, not the simplified formula.

**[CP3] sigma_d0 angular dependence (Category A, Phase 2):**  
Strategy parameterizes sigma_d0 with sin^{3/2}(theta) (3D form); the d0 branch appears to be Rφ (2D), for which the correct form is sin(theta). Phase 3 reviewers: verify the resolution parameterization function form against the actual ALEPH detector paper (537303) and check whether the negative d0 tail calibration produces unit-width Gaussians for forward tracks — a failure there is diagnostic of wrong angular dependence.

**[CP4] PDG inputs not yet fetched (Category A, Phase 2):**  
M_Z, Gamma_Z, B hadron lifetimes, and B hadron decay multiplicities are listed as "NEEDS FETCH" in INPUT_INVENTORY.md with no values. Phase 3/4 executors must not use these values without a citable source. Phase 4a reviewers: verify all B physics systematic variations cite specific PDG 2024 values.
