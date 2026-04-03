"""Phase 4a REGRESSION: Publication-quality figures for expected results.

Produces figures for the 3-tag R_b and purity-corrected A_FB^b analysis.

Reads: outputs/*.json
Writes: outputs/figures/*.png, outputs/FIGURES.json
"""
import json
import logging
from pathlib import Path

import matplotlib.pyplot as plt
import mplhep as mh
import numpy as np
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

# Import Phase 3 plot utilities
import sys
HERE = Path(__file__).resolve().parent
P3_SRC = HERE.parents[2] / "phase3_selection" / "src"
sys.path.insert(0, str(P3_SRC))
import plot_utils as pu
from plot_utils import setup_figure, exp_label_mc

# Override output directories for Phase 4a
OUT = HERE.parent / "outputs"
FIG = OUT / "figures"
FIG.mkdir(parents=True, exist_ok=True)

pu.OUT = OUT
pu.FIG = FIG
save_and_register = pu.save_and_register

mh.style.use("CMS")
SCRIPT = "phase4_inference/4a_expected/src/plot_phase4a_v2.py"

# Reference values
# Source: hep-ex/0509008, hep-ex/9609005, inspire_433746
R_B_SM = 0.21578
R_B_ALEPH = 0.2158
R_B_ALEPH_ERR = 0.0014
R_B_LEP = 0.21629
R_B_LEP_ERR = 0.00066
AFB_B_ALEPH = 0.0927
AFB_B_ALEPH_ERR = 0.0052


def plot_three_tag_stability(rb_res):
    """R_b operating point stability across 3-tag threshold configurations."""
    fig, ax = setup_figure()

    results = rb_res['full_mc_results']
    valid = [r for r in results
             if r['R_b'] is not None and r['sigma_stat'] is not None
             and 0.1 < r['R_b'] < 0.4 and r['sigma_stat'] > 0]

    if not valid:
        log.warning("No valid extractions for stability plot")
        plt.close(fig)
        return

    labels = [r['label'] for r in valid]
    rb_vals = [r['R_b'] for r in valid]
    rb_errs = [r['sigma_stat'] for r in valid]
    x = np.arange(len(valid))

    ax.errorbar(x, rb_vals, yerr=rb_errs, fmt='ko', markersize=6, capsize=3,
                label='3-tag extraction (MC)')

    ax.axhspan(R_B_ALEPH - R_B_ALEPH_ERR, R_B_ALEPH + R_B_ALEPH_ERR,
               alpha=0.2, color='blue',
               label=f'ALEPH $R_b$ = {R_B_ALEPH} $\\pm$ {R_B_ALEPH_ERR}')
    ax.axhline(R_B_SM, color='red', linestyle='--', linewidth=1,
               label=f'SM $R_b$ = {R_B_SM}')
    ax.axhspan(R_B_LEP - R_B_LEP_ERR, R_B_LEP + R_B_LEP_ERR,
               alpha=0.1, color='green',
               label=f'LEP combined = {R_B_LEP} $\\pm$ {R_B_LEP_ERR}')

    # Combined value
    stab = rb_res['stability']
    if stab['R_b_combined'] is not None:
        ax.axhline(stab['R_b_combined'], color='black', linestyle='-',
                   linewidth=1.5, alpha=0.5)
        ax.axhspan(stab['R_b_combined'] - (stab['sigma_combined'] or 0),
                   stab['R_b_combined'] + (stab['sigma_combined'] or 0),
                   alpha=0.1, color='gray',
                   label=f'Combined = {stab["R_b_combined"]:.4f}')

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=9)
    ax.set_ylabel('$R_b$')
    ax.set_xlabel('Threshold configuration')
    ax.legend(loc='upper right', fontsize=10)
    exp_label_mc(ax)

    save_and_register(fig, "three_tag_rb_stability.png", SCRIPT,
                      "R_b operating point stability across 3-tag threshold configurations",
                      "validation")
    plt.close(fig)


def plot_three_tag_closure(rb_res):
    """Independent closure test results for 3-tag system."""
    fig, ax = setup_figure()

    closure = rb_res.get('closure_test', [])
    if not closure:
        log.warning("No closure test results")
        plt.close(fig)
        return

    labels = [c['label'] for c in closure]
    pulls = [c['pull'] if c['pull'] is not None else 0 for c in closure]
    passes = [c.get('passes', False) for c in closure]
    x = np.arange(len(closure))

    colors = ['green' if p else 'red' for p in passes]
    ax.bar(x, pulls, color=colors, alpha=0.7, edgecolor='black')
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axhline(2, color='red', linestyle='--', linewidth=1, alpha=0.5)
    ax.axhline(-2, color='red', linestyle='--', linewidth=1, alpha=0.5)
    ax.axhspan(-2, 2, alpha=0.05, color='green')

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=10)
    ax.set_ylabel('Pull: $(R_b^{\\mathrm{extracted}} - R_b^{\\mathrm{SM}}) / \\sigma$')
    ax.set_xlabel('Threshold configuration')
    exp_label_mc(ax)

    save_and_register(fig, "three_tag_closure.png", SCRIPT,
                      "Independent closure test pulls for 3-tag R_b extraction",
                      "validation")
    plt.close(fig)


def plot_systematic_breakdown(syst_res):
    """Systematic uncertainty breakdown for R_b."""
    fig, ax = setup_figure()

    syst = syst_res['rb_systematics']
    names = list(syst.keys())
    shifts = [syst[n]['delta_Rb'] for n in names]

    # Sort by magnitude
    order = np.argsort(shifts)[::-1]
    names_sorted = [names[i] for i in order]
    shifts_sorted = [shifts[i] for i in order]

    y = np.arange(len(names_sorted))
    ax.barh(y, shifts_sorted, color='steelblue', alpha=0.8, edgecolor='black')

    # Add total systematic
    total_syst = syst_res['rb_total']['syst']
    stat = syst_res['rb_total']['stat']
    ax.axvline(total_syst, color='red', linestyle='--', linewidth=2,
               label=f'Total syst = {total_syst:.5f}')
    ax.axvline(stat, color='blue', linestyle=':', linewidth=2,
               label=f'Statistical = {stat:.5f}')

    ax.set_yticks(y)
    ax.set_yticklabels(names_sorted, fontsize=9)
    ax.set_xlabel('$\\Delta R_b$')
    ax.legend(loc='lower right', fontsize=10)
    exp_label_mc(ax)

    save_and_register(fig, "rb_systematic_breakdown.png", SCRIPT,
                      "Systematic uncertainty breakdown for R_b",
                      "result")
    plt.close(fig)


def plot_afb_kappa_results(afb_res):
    """A_FB^b per kappa value with combined result."""
    fig, ax = setup_figure()

    kappa_results = afb_res['kappa_results']
    kappas = []
    afb_vals = []
    afb_errs = []

    for kr in kappa_results:
        comb = kr['combination']
        if comb.get('A_FB_b') is not None and comb.get('sigma_A_FB_b') is not None:
            if comb['sigma_A_FB_b'] > 0:
                kappas.append(kr['kappa'])
                afb_vals.append(comb['A_FB_b'])
                afb_errs.append(comb['sigma_A_FB_b'])

    if not kappas:
        log.warning("No A_FB^b results to plot")
        plt.close(fig)
        return

    x = np.arange(len(kappas))
    ax.errorbar(x, afb_vals, yerr=afb_errs, fmt='ko', markersize=6, capsize=3,
                label='Purity-corrected (MC)')

    # Combined
    final = afb_res['combination']
    if final.get('A_FB_b') is not None:
        ax.axhline(final['A_FB_b'], color='black', linestyle='-',
                   linewidth=1.5, alpha=0.5,
                   label=f'Combined = {final["A_FB_b"]:.4f}')

    ax.axhline(0, color='gray', linestyle=':', linewidth=1,
               label='Expected (symmetric MC)')

    ax.set_xticks(x)
    ax.set_xticklabels([f'$\\kappa$ = {k}' for k in kappas], fontsize=11)
    ax.set_ylabel('$A_{\\mathrm{FB}}^b$')
    ax.set_xlabel('$\\kappa$')
    ax.legend(loc='upper right', fontsize=10)
    exp_label_mc(ax)

    save_and_register(fig, "afb_kappa_results.png", SCRIPT,
                      "Purity-corrected A_FB^b per kappa on MC pseudo-data",
                      "result")
    plt.close(fig)


def plot_afb_angular_distribution(afb_res):
    """Angular distribution of <Q_FB> vs cos(theta) at reference WP."""
    fig, ax = setup_figure()

    # Use kappa=2.0 as reference (highest delta_b)
    kappa_2 = None
    for kr in afb_res['kappa_results']:
        if kr['kappa'] == 2.0:
            kappa_2 = kr
            break

    if kappa_2 is None or not kappa_2.get('per_wp_results'):
        log.warning("No kappa=2.0 results for angular plot")
        plt.close(fig)
        return

    # Use the WP with most events
    best_wp = max(kappa_2['per_wp_results'],
                  key=lambda r: r['slope']['n_tagged'])
    slope_data = best_wp['slope']

    bin_centers = np.array(slope_data['bin_centers'])
    mean_qfb = np.array([v if v is not None else np.nan
                          for v in slope_data['mean_qfb']])
    sigma_qfb = np.array([v if v is not None else np.nan
                           for v in slope_data['sigma_qfb']])

    valid = ~np.isnan(mean_qfb) & ~np.isnan(sigma_qfb) & (sigma_qfb > 0)
    if np.sum(valid) < 3:
        log.warning("Too few valid bins for angular plot")
        plt.close(fig)
        return

    ax.errorbar(bin_centers[valid], mean_qfb[valid], yerr=sigma_qfb[valid],
                fmt='ko', markersize=5, capsize=3, label='MC pseudo-data')

    # Fit line
    slope = slope_data['slope']
    intercept = slope_data['intercept']
    x_fit = np.linspace(-0.9, 0.9, 100)
    ax.plot(x_fit, intercept + slope * x_fit, 'r-', linewidth=1.5,
            label=f'Fit: slope = {slope:.5f} $\\pm$ {slope_data["sigma_slope"]:.5f}')

    ax.axhline(0, color='gray', linestyle=':', linewidth=0.5)
    ax.set_xlabel('$\\cos\\theta$')
    ax.set_ylabel('$\\langle Q_{\\mathrm{FB}} \\rangle$')
    ax.legend(loc='upper left', fontsize=10)
    exp_label_mc(ax)

    save_and_register(fig, "afb_angular_distribution.png", SCRIPT,
                      "Angular distribution of Q_FB vs cos(theta) at kappa=2.0",
                      "result")
    plt.close(fig)


def plot_efficiency_pattern(rb_res):
    """3-tag efficiency pattern: eps_b, eps_c, eps_uds per tag category."""
    fig, ax = setup_figure()

    best = rb_res.get('best_config')
    if best is None:
        log.warning("No best config for efficiency plot")
        plt.close(fig)
        return

    cal = best['calibration']
    categories = ['tight', 'loose', 'anti']
    flavours = ['b', 'c', 'uds']
    colors = {'b': 'tab:blue', 'c': 'tab:orange', 'uds': 'tab:green'}

    x = np.arange(len(categories))
    width = 0.25

    for i, flav in enumerate(flavours):
        vals = [cal[f'eps_{flav}_{cat}'] for cat in categories]
        ax.bar(x + i * width, vals, width, label=f'$\\epsilon_{{{flav}}}$',
               color=colors[flav], alpha=0.8, edgecolor='black')

    ax.set_xticks(x + width)
    ax.set_xticklabels(['Tight\n(b-enriched)', 'Loose\n(b+c)', 'Anti\n(uds-enriched)'],
                       fontsize=11)
    ax.set_ylabel('Efficiency')
    ax.legend(fontsize=12)
    exp_label_mc(ax)

    save_and_register(fig, "three_tag_efficiency_pattern.png", SCRIPT,
                      "Per-flavour efficiencies in the 3-tag system",
                      "supporting")
    plt.close(fig)


def plot_afb_systematic_breakdown(syst_res):
    """Systematic uncertainty breakdown for A_FB^b."""
    fig, ax = setup_figure()

    syst = syst_res['afb_systematics']
    names = list(syst.keys())
    shifts = [syst[n]['delta_AFB'] for n in names]

    order = np.argsort(shifts)[::-1]
    names_sorted = [names[i] for i in order]
    shifts_sorted = [shifts[i] for i in order]

    y = np.arange(len(names_sorted))
    ax.barh(y, shifts_sorted, color='darkorange', alpha=0.8, edgecolor='black')

    total_syst = syst_res['afb_total']['syst']
    stat = syst_res['afb_total']['stat']
    ax.axvline(total_syst, color='red', linestyle='--', linewidth=2,
               label=f'Total syst = {total_syst:.4f}')
    ax.axvline(stat, color='blue', linestyle=':', linewidth=2,
               label=f'Statistical = {stat:.4f}')

    ax.set_yticks(y)
    ax.set_yticklabels(names_sorted, fontsize=9)
    ax.set_xlabel('$\\Delta A_{\\mathrm{FB}}^b$')
    ax.legend(loc='lower right', fontsize=10)
    exp_label_mc(ax)

    save_and_register(fig, "afb_systematic_breakdown.png", SCRIPT,
                      "Systematic uncertainty breakdown for A_FB^b",
                      "result")
    plt.close(fig)


def main():
    log.info("=" * 60)
    log.info("Phase 4a REGRESSION: Plotting")
    log.info("=" * 60)

    with open(OUT / "three_tag_rb_results.json") as f:
        rb_res = json.load(f)
    with open(OUT / "purity_corrected_afb_results.json") as f:
        afb_res = json.load(f)
    with open(OUT / "systematics_v2_results.json") as f:
        syst_res = json.load(f)

    log.info("Plotting 3-tag R_b stability...")
    plot_three_tag_stability(rb_res)

    log.info("Plotting 3-tag closure test...")
    plot_three_tag_closure(rb_res)

    log.info("Plotting R_b systematic breakdown...")
    plot_systematic_breakdown(syst_res)

    log.info("Plotting A_FB^b kappa results...")
    plot_afb_kappa_results(afb_res)

    log.info("Plotting A_FB^b angular distribution...")
    plot_afb_angular_distribution(afb_res)

    log.info("Plotting efficiency pattern...")
    plot_efficiency_pattern(rb_res)

    log.info("Plotting A_FB^b systematic breakdown...")
    plot_afb_systematic_breakdown(syst_res)

    log.info("\nAll plots saved to %s", FIG)


if __name__ == "__main__":
    main()
