"""Phase 4a REGRESSION: Aggregate results into analysis_note/results/ JSON.

Reads the REGRESSION outputs (3-tag R_b, purity-corrected A_FB^b, v2 systematics)
and writes updated result files.

Reads: outputs/three_tag_rb_results.json
       outputs/purity_corrected_afb_results.json
       outputs/systematics_v2_results.json
       outputs/covariance_v2.json
       outputs/closure_stress_results.json
Writes: analysis_note/results/parameters.json
        analysis_note/results/systematics.json
        analysis_note/results/validation.json
        analysis_note/results/covariance.json
"""
import json
import logging
import shutil
from pathlib import Path

import numpy as np
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "outputs"
AN_RESULTS = HERE.parents[2] / "analysis_note" / "results"
AN_RESULTS.mkdir(parents=True, exist_ok=True)

# Reference uncertainties for precision comparison
REF_RB_ALEPH_ERR = 0.0014   # hep-ex/9609005
REF_RB_LEP_ERR = 0.00066    # hep-ex/0509008
REF_AFB_ALEPH_ERR = 0.0052  # inspire_433746
REF_SIN2_ALEPH_ERR = 0.0009 # inspire_433746


def main():
    log.info("=" * 60)
    log.info("Phase 4a REGRESSION: Writing Results JSON (v2)")
    log.info("=" * 60)

    with open(OUT / "three_tag_rb_results.json") as f:
        rb_res = json.load(f)
    with open(OUT / "purity_corrected_afb_results.json") as f:
        afb_res = json.load(f)
    with open(OUT / "systematics_v2_results.json") as f:
        syst_res = json.load(f)
    with open(OUT / "covariance_v2.json") as f:
        cov = json.load(f)

    # Try to load closure results (may be from original run)
    closure_path = OUT / "closure_stress_results.json"
    if closure_path.exists():
        with open(closure_path) as f:
            closure_res = json.load(f)
    else:
        closure_res = None

    # ================================================================
    # 1. parameters.json
    # ================================================================
    stab = rb_res['stability']
    comb = afb_res['combination']
    s2t = afb_res['sin2theta']

    parameters = {
        'R_b': {
            'value': stab['R_b_combined'],
            'stat': stab['sigma_combined'],
            'syst': syst_res['rb_total']['syst'],
            'total': syst_res['rb_total']['total'],
            'SM': 0.21578,
            'unit': 'dimensionless',
            'method': '3-tag system (tight/loose/anti-b), MC pseudo-data',
            'n_configs': stab.get('n_configs', 0),
            'stability_chi2_ndf': stab.get('chi2_ndf'),
            'stability_p_value': stab.get('p_value'),
        },
        'A_FB_b': {
            'value': comb['A_FB_b'],
            'stat': comb['sigma_A_FB_b'],
            'syst': syst_res['afb_total']['syst'],
            'total': syst_res['afb_total']['total'],
            'SM': 0.1032,
            'unit': 'dimensionless',
            'method': 'Purity-corrected extraction with published delta_b, MC pseudo-data',
            'note': 'On symmetric MC, A_FB^b = 0 by construction. Non-zero values reflect noise.',
        },
        'A_FB_0_b': {
            'value': comb.get('A_FB_0_b'),
            'stat': (comb['sigma_A_FB_b'] / (1.0 - 0.0356 - 0.001)
                     if comb.get('sigma_A_FB_b') else None),
            'syst': syst_res['afb_total']['syst'] / (1.0 - 0.0356 - 0.001),
            'SM': 0.1032,
            'unit': 'dimensionless',
            'method': 'Pole asymmetry from A_FB^b / (1 - delta_QCD - delta_QED)',
        },
        'sin2theta_eff': {
            'value': s2t.get('value'),
            'stat': s2t.get('sigma_stat'),
            'syst': None,
            'SM': s2t.get('SM', 0.23153),
            'unit': 'dimensionless',
            'method': 'Inverted from A_FB^{0,b} via SM formula',
        },
        'R_c': {
            'value': 0.17223,
            'stat': None,
            'syst': 0.0030,
            'total': 0.0030,
            'SM': 0.17223,
            'unit': 'dimensionless',
            'method': 'Constrained to SM value [D6]; uncertainty from LEP combined',
        },
        'phase': '4a_expected_regression',
        'data_type': 'MC pseudo-data only',
        'regression_note': ('Rewritten per REGRESS(4a). Primary methods: '
                            '3-tag R_b, purity-corrected A_FB^b, '
                            'eps_uds from anti-tag, eps_c from 3-tag.'),
    }

    with open(AN_RESULTS / "parameters.json", "w") as f:
        json.dump(parameters, f, indent=2)
    log.info("Saved parameters.json")

    # ================================================================
    # 2. systematics.json
    # ================================================================
    syst_output = {
        'R_b': syst_res['rb_systematics'],
        'A_FB_b': syst_res['afb_systematics'],
        'totals': {
            'R_b': syst_res['rb_total'],
            'A_FB_b': syst_res['afb_total'],
        },
        'method_notes': syst_res.get('method_notes', {}),
    }

    with open(AN_RESULTS / "systematics.json", "w") as f:
        json.dump(syst_output, f, indent=2)
    log.info("Saved systematics.json")

    # ================================================================
    # 3. validation.json
    # ================================================================
    our_rb_total = syst_res['rb_total']['total']
    our_afb_total = syst_res['afb_total']['total']

    precision_rb_aleph = our_rb_total / REF_RB_ALEPH_ERR if our_rb_total else None
    precision_rb_lep = our_rb_total / REF_RB_LEP_ERR if our_rb_total else None
    precision_afb = our_afb_total / REF_AFB_ALEPH_ERR if our_afb_total else None

    # 3-tag stability
    stab_passes = stab.get('passes', False)

    # Closure test from 3-tag results
    closure_3tag = rb_res.get('closure_test', [])
    closure_passes = all(c.get('passes', False) for c in closure_3tag) if closure_3tag else False

    validation = {
        'operating_point_stability': {
            'chi2': stab.get('chi2', 0),
            'ndf': stab.get('ndf', 0),
            'chi2_ndf': stab.get('chi2_ndf'),
            'p_value': stab.get('p_value'),
            'passes': stab_passes,
            'n_configs': stab.get('n_configs', 0),
            'method': '3-tag system across 8 threshold configurations',
        },
        'kappa_consistency': {
            'chi2': comb.get('chi2_kappa', 0),
            'ndf': comb.get('ndf_kappa', 0),
            'p_value': comb.get('p_kappa'),
            'passes': bool(comb.get('p_kappa', 0) > 0.05) if comb.get('p_kappa') else None,
        },
        'independent_closure_3tag': {
            'passes': closure_passes,
            'per_config': closure_3tag,
        },
        'precision_comparison': {
            'R_b_vs_ALEPH': {
                'our_total': our_rb_total,
                'reference_total': REF_RB_ALEPH_ERR,
                'ratio': precision_rb_aleph,
                'source': 'hep-ex/9609005',
                'investigation_required': bool(precision_rb_aleph and precision_rb_aleph > 5.0),
            },
            'R_b_vs_LEP_combined': {
                'our_total': our_rb_total,
                'reference_total': REF_RB_LEP_ERR,
                'ratio': precision_rb_lep,
                'source': 'hep-ex/0509008',
                'investigation_required': bool(precision_rb_lep and precision_rb_lep > 5.0),
            },
            'A_FB_b_vs_ALEPH': {
                'our_total': our_afb_total,
                'reference_total': REF_AFB_ALEPH_ERR,
                'ratio': precision_afb,
                'source': 'inspire_433746',
                'caveat': ('Phase 4a: on symmetric MC. Valid comparison at 4b/4c.'),
            },
        },
    }

    # Add investigation explanation if needed
    for key, val in validation['precision_comparison'].items():
        if val.get('investigation_required'):
            val['explanation'] = (
                'Simplified single-tag system (vs ALEPH 5-tag), '
                'no per-hemisphere vertex reconstruction, '
                'limited MC (1994 only), eps_c > eps_b tag inversion.'
            )

    with open(AN_RESULTS / "validation.json", "w") as f:
        json.dump(validation, f, indent=2)
    log.info("Saved validation.json")

    # ================================================================
    # 4. covariance.json
    # ================================================================
    shutil.copy2(OUT / "covariance_v2.json", AN_RESULTS / "covariance.json")
    log.info("Copied covariance_v2.json to analysis_note/results/")

    # Summary
    log.info("\n--- Phase 4a REGRESSION Results Summary ---")
    log.info("R_b = %.5f +/- %.5f (stat) +/- %.5f (syst)",
             parameters['R_b']['value'] or 0,
             parameters['R_b']['stat'] or 0,
             parameters['R_b']['syst'] or 0)
    log.info("A_FB^b = %.4f +/- %.4f (stat) +/- %.4f (syst)",
             parameters['A_FB_b']['value'] or 0,
             parameters['A_FB_b']['stat'] or 0,
             parameters['A_FB_b']['syst'] or 0)
    if parameters['sin2theta_eff']['value']:
        log.info("sin^2(theta_eff) = %.5f +/- %.5f (stat)",
                 parameters['sin2theta_eff']['value'],
                 parameters['sin2theta_eff']['stat'] or 0)

    if precision_rb_aleph:
        log.info("Precision ratio R_b vs ALEPH: %.2f", precision_rb_aleph)
    if precision_afb:
        log.info("Precision ratio A_FB^b vs ALEPH: %.2f", precision_afb)


if __name__ == "__main__":
    main()
