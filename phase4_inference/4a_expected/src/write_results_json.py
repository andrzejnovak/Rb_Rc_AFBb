"""Phase 4a: Aggregate results into analysis_note/results/ JSON files.

Reads all Phase 4a output JSONs and writes the four mandatory files:
- parameters.json: R_b, R_c, A_FB^b, sin^2(theta_eff) with stat+syst
- systematics.json: per-source shifts
- validation.json: chi2/ndf, p-values, precision comparison
- covariance.json: stat, syst, total matrices

Reads: outputs/*.json
Writes: analysis_note/results/*.json
"""
import json
import logging
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
    log.info("Phase 4a: Writing Results JSON")
    log.info("=" * 60)

    with open(OUT / "rb_results.json") as f:
        rb_res = json.load(f)
    with open(OUT / "afb_results.json") as f:
        afb_res = json.load(f)
    with open(OUT / "systematics_results.json") as f:
        syst_res = json.load(f)
    with open(OUT / "covariance.json") as f:
        cov = json.load(f)
    with open(OUT / "closure_stress_results.json") as f:
        closure_res = json.load(f)

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
            'method': 'Double-tag hemisphere counting, MC pseudo-data',
            'working_point': rb_res.get('best_wp', {}).get('threshold'),
        },
        'A_FB_b': {
            'value': comb['A_FB_b'],
            'stat': comb['sigma_A_FB_b'],
            'syst': syst_res['afb_total']['syst'],
            'total': syst_res['afb_total']['total'],
            'SM': 0.1032,
            'unit': 'dimensionless',
            'method': 'Self-calibrating hemisphere jet charge fit, MC pseudo-data',
        },
        'A_FB_0_b': {
            'value': comb['A_FB_0_b'],
            'stat': comb['sigma_A_FB_b'] / (1.0 - 0.0356 - 0.001) if comb['sigma_A_FB_b'] else None,
            'syst': syst_res['afb_total']['syst'] / (1.0 - 0.0356 - 0.001),
            'SM': 0.1032,
            'unit': 'dimensionless',
            'method': 'Pole asymmetry from A_FB^b / (1 - delta_QCD - delta_QED)',
        },
        'sin2theta_eff': {
            'value': s2t['value'],
            'stat': s2t['sigma_stat'],
            'syst': None,  # Propagated from A_FB^b systematics
            'SM': s2t['SM'],
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
        'phase': '4a_expected',
        'data_type': 'MC pseudo-data only',
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
    }

    with open(AN_RESULTS / "systematics.json", "w") as f:
        json.dump(syst_output, f, indent=2)
    log.info("Saved systematics.json")

    # ================================================================
    # 3. validation.json
    # ================================================================
    # Precision comparison
    our_rb_total = syst_res['rb_total']['total']
    our_afb_total = syst_res['afb_total']['total']

    precision_ratio_rb_aleph = our_rb_total / REF_RB_ALEPH_ERR if our_rb_total and REF_RB_ALEPH_ERR else None
    precision_ratio_rb_lep = our_rb_total / REF_RB_LEP_ERR if our_rb_total and REF_RB_LEP_ERR else None
    precision_ratio_afb = our_afb_total / REF_AFB_ALEPH_ERR if our_afb_total and REF_AFB_ALEPH_ERR else None

    # Operating point stability: only 1 of 4 WPs has valid extraction.
    # A stability scan requires >= 2 points. Mark as FAIL (finding [A3]).
    n_valid_wp = sum(1 for r in rb_res['extraction_results'] if r['R_b'] is not None)
    op_stability_passes = n_valid_wp >= 2

    validation = {
        'operating_point_stability': {
            'chi2': stab['chi2'],
            'ndf': stab['ndf'],
            'chi2_ndf': stab['chi2_ndf'],
            'p_value': stab['p_value'] if op_stability_passes else None,
            'passes': op_stability_passes,
            'n_valid_wp': n_valid_wp,
            'notes': ('Only WP 10.0 yields a valid R_b extraction; '
                      '3 of 4 WPs return null. Stability scan not computable.')
                     if not op_stability_passes else None,
        },
        'kappa_consistency': {
            'chi2': comb['chi2_kappa'],
            'ndf': comb['ndf_kappa'],
            'p_value': comb['p_kappa'],
            'passes': bool(comb['p_kappa'] > 0.05) if comb['p_kappa'] else None,
        },
        'independent_closure': {
            'passes': closure_res['independent_closure']['overall_passes'],
            'per_wp': closure_res['independent_closure']['per_wp'],
        },
        'corrupted_corrections_sensitivity': {
            'n_sensitive': closure_res['corrupted_corrections']['n_sensitive'],
            'n_total': closure_res['corrupted_corrections']['n_total'],
            'passes': closure_res['corrupted_corrections']['overall_passes'],
        },
        'per_year_consistency': {
            'chi2': closure_res['per_year_consistency']['chi2'],
            'ndf': closure_res['per_year_consistency']['ndf'],
            'p_value': closure_res['per_year_consistency']['p_value'],
            'passes': closure_res['per_year_consistency']['passes'],
        },
        'precision_comparison': {
            'R_b_vs_ALEPH': {
                'our_total': our_rb_total,
                'reference_total': REF_RB_ALEPH_ERR,
                'ratio': precision_ratio_rb_aleph,
                'source': 'hep-ex/9609005',
            },
            'R_b_vs_LEP_combined': {
                'our_total': our_rb_total,
                'reference_total': REF_RB_LEP_ERR,
                'ratio': precision_ratio_rb_lep,
                'source': 'hep-ex/0509008',
            },
            'A_FB_b_vs_ALEPH': {
                'our_total': our_afb_total,
                'reference_total': REF_AFB_ALEPH_ERR,
                'ratio': precision_ratio_afb,
                'source': 'inspire_433746',
            },
        },
    }

    # Flag if ratio > 5x
    for key, val in validation['precision_comparison'].items():
        if val['ratio'] and val['ratio'] > 5.0:
            val['investigation_required'] = True
            val['explanation'] = ('Ratio > 5x: simplified single-tag system, '
                                  'no per-hemisphere vertex, limited MC (1994 only)')
        else:
            val['investigation_required'] = False

    # A_FB precision caveat (finding [B23]): comparison not meaningful on symmetric MC
    afb_entry = validation['precision_comparison'].get('A_FB_b_vs_ALEPH')
    if afb_entry:
        afb_entry['caveat'] = (
            'Phase 4a comparison not meaningful: our result is on symmetric MC '
            '(A_FB^b = 0 by construction) while ALEPH measured real asymmetry (~0.09). '
            'The 0.87x ratio reflects noise precision on zero signal vs real measurement. '
            'Valid comparison requires Phase 4b/4c data.'
        )

    with open(AN_RESULTS / "validation.json", "w") as f:
        json.dump(validation, f, indent=2)
    log.info("Saved validation.json")

    # ================================================================
    # 4. covariance.json (already written by systematics.py, copy here)
    # ================================================================
    import shutil
    shutil.copy2(OUT / "covariance.json", AN_RESULTS / "covariance.json")
    log.info("Copied covariance.json to analysis_note/results/")

    # Summary
    log.info("\n--- Phase 4a Results Summary ---")
    log.info("R_b = %.5f +/- %.5f (stat) +/- %.5f (syst)",
             parameters['R_b']['value'] or 0,
             parameters['R_b']['stat'] or 0,
             parameters['R_b']['syst'] or 0)
    log.info("A_FB^b = %.4f +/- %.4f (stat) +/- %.4f (syst)",
             parameters['A_FB_b']['value'] or 0,
             parameters['A_FB_b']['stat'] or 0,
             parameters['A_FB_b']['syst'] or 0)
    log.info("sin^2(theta_eff) = %.5f +/- %.5f (stat)",
             parameters['sin2theta_eff']['value'] or 0,
             parameters['sin2theta_eff']['stat'] or 0)

    if precision_ratio_rb_aleph:
        log.info("Precision ratio R_b vs ALEPH: %.2f", precision_ratio_rb_aleph)
    if precision_ratio_afb:
        log.info("Precision ratio A_FB^b vs ALEPH: %.2f", precision_ratio_afb)


if __name__ == "__main__":
    main()
