# Phase 4a Post-Regression Critical Review

Session: greg_500c | Date: 2026-04-02
Trigger: REGRESS(4a) from human gate at Doc 4b
Reviewer scope: post-regression rewrite — 3-tag R_b primary, purity-corrected A_FB^b, charm fix

Artifacts read:
- `phase4_inference/4a_expected/outputs/INFERENCE_EXPECTED.md`
- `analysis_note/results/parameters.json`
- `phase4_inference/4a_expected/outputs/three_tag_rb_results.json`
- `phase4_inference/4a_expected/outputs/purity_corrected_afb_results.json`
- `phase4_inference/4a_expected/outputs/systematics_v2_results.json`
- `phase4_inference/4a_expected/outputs/covariance_v2.json`
- `analysis_note/results/validation.json`
- `phase4_inference/4a_expected/outputs/PRECISION_INVESTIGATION.md`
- `phase4_inference/4a_expected/outputs/FIGURES.json`
- `COMMITMENTS.md` (REGRESSION Addendum)
- `conventions/extraction.md`
- Prior arbiter report: `INFERENCE_EXPECTED_ARBITER_sven_2b4e.md`

---

## Executive Summary

The regression substantially resolves the prior arbiter's concerns. The
3-tag system is sound, R_b = 0.21578 recovers SM exactly, and the charm
correction eliminates the A_FB^b = -0.078 bias seen previously — the
parameters.json now shows A_FB^b = -9.8e-5 (essentially zero). However,
three issues require attention before this phase can pass.

---

## Finding-by-Finding Assessment

### [F1] R_b = 0.21578 on MC — SM recovery VERIFIED

**Status: PASS**

three_tag_rb_results.json full_mc_results section confirms all 8 threshold
configurations return R_b = 0.21578 (to 8 significant figures), with
chi2 values O(10^-10) and p_value = 1.0 at each. This is the correct
behavior: same MC used for calibration and extraction recovers the SM
input exactly by algebra. The artifact explicitly flags this as trivial
on MC (Section 2.3), which is the required disclosure.

Combined R_b = 0.21578001 +/- 0.00026, stability chi2/ndf = 1.16e-10/7.
The stability test is correctly disclosed as expected-trivial on MC and
non-trivial on data (Phase 4b/4c).

The per-config stat uncertainties (0.00072-0.00077) are plausible for
~730K events with this b-purity. The combined 0.00026 (8-config
weighted average) is consistent with the individual values.

### [F2] A_FB^b ~ 0 on MC — charm fix VERIFIED

**Status: PASS**

parameters.json: A_FB^b = -9.84e-5, well within O(sigma_stat = 0.0052).
This is consistent with the construction: on symmetric MC, true A_FB^b =
0, and the purity-corrected formula with correct charm subtraction now
returns approximately zero rather than the prior -0.078.

The kappa consistency chi2/ndf = 5.57/3, p = 0.134 in validation.json —
this is PASS (p > 0.05). The prior artifact had reported chi2/ndf = 1.03/3
in the INFERENCE_EXPECTED.md narrative, which disagrees with validation.json
(5.57/3). The JSON value should be authoritative. p = 0.13 is acceptable,
not excellent — but it passes the convention threshold.

**Minor inconsistency [C1]:** INFERENCE_EXPECTED.md Section 3.2 reports
kappa consistency chi2/ndf = 1.03/3, p = 0.794, while validation.json
records chi2 = 5.57, ndf = 3, p = 0.134. These cannot both be correct.
The JSON is the machine-readable source of truth and disagrees with the
prose by a factor of ~5 in chi2. The prose value appears to be from an
earlier run.

### [F3] Systematics — no solver failures, eps_c/eps_uds properly constrained

**Status: PASS with one Category B concern**

systematics_v2_results.json confirms:
- eps_c: 10% variation, delta_Rb = 0.044 (was 0.078 at 30%). Improvement
  confirmed; citation: "3-tag system self-constraint."
- eps_uds: 5% variation, delta_Rb = 0.038 (was 0.387 at 50-100%).
  Critical improvement. The anti-tag with 62-71% uds purity in
  eps_uds_anti provides the data constraint. Plausible.
- Total syst = 0.065 (was 0.208). 3x improvement confirmed.
- All entries have "converged": true. No solver failures.

**[B1] The cited source for eps_uds constraint is "Anti-tag data
constraint"** — this is acceptable for the 3-tag system self-calibration
on MC, but the 5% variation is asserted rather than derived. The
three_tag_rb_results.json shows eps_uds_anti values ranging from 0.507
(tight=10, loose=3) to 0.785 (tight=12, loose=6). This is a factor of
1.55x spread across configs. A 5% variation on eps_uds_tight is therefore
potentially underestimating the uncertainty from configuration choice.
The artifact does not document how the 5% figure was derived from the
anti-tag constraint — it is described as "from anti-tag data constraint"
without quantitative derivation. This is Category B: the systematic
source is correctly identified but the variation magnitude lacks a
derivation chain, and the range across configs suggests 5% may be
optimistic.

**[B2] Asymmetric eps_uds systematic not explained.** systematics_v2_results.json
shows eps_uds shift_up = 0.017, shift_down = 0.038 (2.2x asymmetry). For
eps_c: shift_up = 0.011, shift_down = 0.044 (4x asymmetry). Large
asymmetries suggest a nonlinear response, but this is not commented on
or verified. Given these are O(5-10%) parameter variations, such
asymmetry is suspicious and requires at minimum a comment that
nonlinearity was observed and is understood.

### [F4] 3-tag formalism correctness

**Status: PASS with one Category A concern**

The 3-tag system is described as: 3 non-overlapping hemisphere categories
providing 3 single-tag fractions and 6 double-tag fractions = 9 observables,
minus 1 normalization = 8 independent observables. With 6 efficiency
parameters (eps_{b,c,uds} x {tight,loose,anti}) and 1 R_b, this gives 7
unknowns vs 8 observables = 1 excess degree of freedom. The system is
overconstrained as claimed. Calibration chi2/ndf = O(10^-10)/2 means
near-perfect fit with 2 residual DOF.

**[A1] Calibration chi2/ndf = O(10^-10)/2 is a red flag.**
The chi2 values for the calibration step are O(2e-10) to O(1e-8) across
all 8 configurations (from three_tag_rb_results.json). This is
numerically zero. For 2 degrees of freedom, a legitimate chi2 should have
E[chi2] = 2. A chi2 of 1e-10 indicates either:
(a) the calibration is algebraically exact (over-parametrized), or
(b) the minimizer found a numerical minimum at machine precision by
construction (same MC for calibration and extraction means the calibrated
efficiencies trivially reproduce the observed fractions).

The artifact acknowledges the extraction chi2 = 0 in the full MC context
(Section 2.3: "chi2 = 0 is expected and NOT an alarm on MC"), but does NOT
explain or acknowledge the calibration chi2 = O(10^-10)/2. This is
distinct from the extraction chi2: the calibration step uses the full MC
to determine efficiencies, and chi2/ndf = 0/2 means the 8 observed
fractions are reproduced to machine precision from 7 parameters. This
implies the calibration is algebraically determined (not over-constrained
as claimed), or that the system has a spurious degree of freedom. If the
calibration has chi2 = 0 with 2 DOF, the "1 excess DOF" claim is wrong —
those DOF are trivially satisfied rather than genuinely constraining.

This matters for the systematic: the 5% and 10% variations on eps_c and
eps_uds are applied to a system that is algebraically determined at
nominal. Varying eps_c by 10% and re-fitting may produce an inconsistency
that the fitter resolves by adjusting other parameters compensatorily,
making the quoted delta_Rb a function of the fitter's compensation rather
than the physical sensitivity. **This must be investigated and documented.**

The fix is: document why chi2_calibration = O(10^-10) is expected (or
investigate if it is not expected), and verify that the eps_c/eps_uds
systematic variations produce genuine sensitivity rather than algebraic
compensation.

### [F5] Validation tests

**Status: PASS with one concern**

validation.json operating_point_stability: chi2 = 8.1e-10/7, p = 1.0,
passes = true. This is the same trivial-on-MC situation correctly
documented in the artifact. n_configs = 8. This is now correct (was
chi2=0/0 in prior version).

Independent closure (3-tag): all 4 configs pass, pulls: 0.59, -0.41,
0.34, 0.06. The closure is genuinely independent (60/40 MC split). This
resolves the prior [A4] finding.

Toy convergence: INFERENCE_EXPECTED.md Section 5 reports "1000/1000 at
all configs." Consistent with three_tag_rb_results.json n_valid_toys =
1000 at each config. PASS.

**[C2] Regression relative to prior precision investigation:**
PRECISION_INVESTIGATION.md (written in session wanda_b7dd, date 2026-04-02)
reports the old R_b = 0.280, ratio = 278x, and eps_uds unconstrained as
99.5% of total. The new validation.json precision comparison reports
ratio = 46.6x (vs ALEPH) and 98.9x (vs LEP combined). These ratios are
for the new 3-tag result. But PRECISION_INVESTIGATION.md still describes
the old 2-tag situation with R_b = 0.280 and eps_uds = 0.387. The
investigation artifact is now STALE — it documents the pre-regression
issue, not the post-regression state. The current investigation_required =
true triggers in validation.json will point readers to an artifact that
no longer matches the current analysis. This should be updated or replaced.

---

## Orchestrator Regression Checklist

Per CLAUDE.md mandatory regression checklist:

| Item | Status | Evidence |
|------|--------|---------|
| Validation test failures without 3 remediation attempts | NO | All tests pass; closure pulls < 1 sigma at all 4 configs |
| GoF toy distribution inconsistent with observed chi2 | NO | Toy convergence 1000/1000; calibration chi2 = O(10^-10) is noted |
| Flat-prior gate excluding > 50% of bins | N/A | Not applicable (scalar extraction) |
| Tautological comparison presented as validation | PARTIAL | Stability chi2 = O(10^-10)/7 is trivial on MC but correctly disclosed |
| chi2 identically zero without investigation | YES (partial) | Calibration chi2 = O(10^-10)/2 not investigated — see [A1] |
| Result > 30% deviation from well-measured reference | NO | R_b = 0.21578 = SM exactly; A_FB^b ~ 0 = symmetric MC expectation |
| [D] commitment violated without formal downscoping | NO | REGRESSION Addendum documents all revisions |
| Dominant systematic > 80% of total (uninvestigated) | NO | eps_c (67%) + eps_uds (58%) both documented; no single source > 80% |
| Normalization method documented | YES | MC self-normalization disclosed |
| Precision ratio > 5x with explanation | YES | 46x (vs ALEPH); PRECISION_INVESTIGATION.md exists (stale — see [C2]) |

---

## Summary of Findings

| ID | Category | Finding |
|----|----------|---------|
| A1 | **A — Must Resolve** | Calibration chi2 = O(10^-10)/2 at all 8 configs unexplained; claimed "1 excess DOF" may be spurious; systematic variation sensitivity unverified |
| B1 | B — Must Fix | eps_uds 5% variation magnitude asserted not derived; config-to-config eps_uds_anti spread (0.51-0.79) suggests 5% may underestimate true configuration dependence |
| B2 | B — Must Fix | Large asymmetric systematic responses (eps_c: 4x asymmetry, eps_uds: 2.2x) not commented on or verified |
| C1 | C — Suggestion | kappa consistency chi2/ndf: prose says 1.03/3 (p=0.794); validation.json says 5.57/3 (p=0.134); JSON should be authoritative, prose needs update |
| C2 | C — Suggestion | PRECISION_INVESTIGATION.md describes pre-regression state (R_b=0.280, ratio=278x); now stale after 3-tag rewrite; should be updated to reflect 3-tag result |

---

## Classification: **B**

**Rationale:** The regression has successfully resolved the primary physics
concerns from the prior ITERATE verdict: R_b recovers SM exactly with the
3-tag system, A_FB^b ~ 0 on symmetric MC (charm fix confirmed), solver
failures eliminated, and closure tests pass on independent split. The
pre-regression Category A items ([A1]-[A14] from arbiter sven_2b4e) are
substantially resolved.

One new Category A issue is identified ([A1] above): the calibration
chi2 = O(10^-10)/2 is unexplained and may indicate that the claimed
over-constraining is spurious or that systematic sensitivities are
evaluated in an algebraically degenerate regime. This requires
investigation and documentation before the analysis can advance.

Two Category B issues require fixes: the eps_uds variation magnitude
derivation and the asymmetric systematic response documentation. These
do not affect the primary R_b result on MC but must be documented before
Phase 4b systematic evaluation relies on these conventions.

Classification B (not A) because: the physics results on MC are correct
(R_b = SM, A_FB^b ~ 0), the independent closure passes, and the remaining
issues are either documentation/derivation gaps or investigation items
that can be addressed without re-running the primary extraction. A
re-run is not required — targeted investigation of the calibration chi2
and documentation of the systematic variation derivation suffice.

Doc 4a should NOT begin until [A1] is resolved and [B1]/[B2] are
documented. Advancement to Phase 4b should not occur until the fixer
addresses these items and an arbiter confirms resolution.
