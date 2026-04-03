"""Phase 4a: All figures for expected results.

Produces flagship and supporting figures. Imports plot_utils from Phase 3.

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
from plot_utils import setup_figure, setup_ratio_figure, exp_label_mc

# Override output directories for Phase 4a
OUT = HERE.parent / "outputs"
FIG = OUT / "figures"
FIG.mkdir(parents=True, exist_ok=True)

# Monkey-patch plot_utils to use Phase 4a directories
pu.OUT = OUT
pu.FIG = FIG
save_and_register = pu.save_and_register

mh.style.use("CMS")
SCRIPT = "phase4_inference/4a_expected/src/plot_phase4a.py"

# Reference values
R_B_SM = 0.21578
R_B_ALEPH = 0.2158
R_B_ALEPH_ERR = 0.0014
R_B_LEP = 0.21629
R_B_LEP_ERR = 0.00066
AFB_B_ALEPH = 0.0927
AFB_B_ALEPH_ERR = 0.0052


def plot_rb_stability(rb_res):
    """F1: R_b operating point stability scan with ALEPH band."""
    fig, ax = plt.subplots(figsize=(10, 10))

    results = rb_res['extraction_results']
    thresholds = [r['threshold'] for r in results if r['R_b'] is not None]
    rb_vals = [r['R_b'] for r in results if r['R_b'] is not None]
    rb_errs = [r['sigma_stat'] for r in results if r['R_b'] is not None]

    if not thresholds:
        log.warning("No valid R_b extractions for stability plot")
        plt.close(fig)
        return

    ax.errorbar(thresholds, rb_vals, yerr=rb_errs, fmt='o', color='black',
                markersize=6, capsize=3, label='MC pseudo-data')

    # ALEPH band
    ax.axhspan(R_B_ALEPH - R_B_ALEPH_ERR, R_B_ALEPH + R_B_ALEPH_ERR,
               alpha=0.2, color='blue', label=f'ALEPH $R_b$ = {R_B_ALEPH} $\\pm$ {R_B_ALEPH_ERR}')
    ax.axhline(R_B_SM, color='red', linestyle='--', linewidth=1,
               label=f'SM $R_b$ = {R_B_SM}')

    # LEP combined
    ax.axhspan(R_B_LEP - R_B_LEP_ERR, R_B_LEP + R_B_LEP_ERR,
               alpha=0.1, color='green', label=f'LEP combined = {R_B_LEP} $\\pm$ {R_B_LEP_ERR}')

    # Combined result
    stab = rb_res['stability']
    if stab['R_b_combined']:
        ax.axhline(stab['R_b_combined'], color='black', linestyle=':',
                   linewidth=0.8)

    ax.set_xlabel('Combined tag threshold')
    ax.set_ylabel('$R_b$')
    ax.legend(fontsize='x-small', loc='upper right')
    ax.set_ylim(0.15, 0.30)

    # Annotate chi2/ndf
    if stab['chi2_ndf'] is not None:
        ax.text(0.05, 0.05,
                f'$\\chi^2$/ndf = {stab["chi2"]:.1f}/{stab["ndf"]} = {stab["chi2_ndf"]:.2f}\n'
                f'p = {stab["p_value"]:.3f}',
                transform=ax.transAxes, fontsize='x-small',
                verticalalignment='bottom',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    exp_label_mc(ax)

    # Note: only WP 10.0 yields a valid extraction; this is not a stability
    # scan but a single-point extraction. Renamed per finding [A11/F1].
    desc = ("R_b extraction at reference working point (WP 10.0). "
            "Other WPs yield null extraction due to underdetermined calibration. "
            "ALEPH and LEP combined bands shown for reference.")
    save_and_register(fig, "F1_rb_stability_scan.png", SCRIPT, desc,
                      "result", lower_panel="none")


def plot_afb_angular(afb_res):
    """F2: A_FB^b angular distribution at reference kappa."""
    fig, ax = plt.subplots(figsize=(10, 10))

    # Use kappa=0.5 as reference (good balance of sensitivity and resolution)
    ref_kappa_idx = 1  # kappa=0.5
    kappa_data = afb_res['kappa_results'][ref_kappa_idx]
    kappa = kappa_data['kappa']

    if kappa_data['simple_fit'] is None:
        log.warning("No simple fit for kappa=%.1f", kappa)
        plt.close(fig)
        return

    fit = kappa_data['simple_fit']
    bin_centers = np.array(fit['bin_centers'])
    mean_qfb = np.array([x if x is not None else np.nan for x in fit['mean_qfb']])
    sigma_qfb = np.array([x if x is not None else np.nan for x in fit['sigma_qfb']])
    valid = ~np.isnan(mean_qfb)

    ax.errorbar(bin_centers[valid], mean_qfb[valid], yerr=sigma_qfb[valid],
                fmt='o', color='black', markersize=5, capsize=3,
                label=f'MC pseudo-data ($\\kappa$ = {kappa})')

    # Fit line (intercept + slope * cos theta)
    x_line = np.linspace(-0.9, 0.9, 100)
    slope = fit['slope']
    intercept = fit.get('intercept', 0.0)
    ax.plot(x_line, intercept + slope * x_line, 'r-', linewidth=2,
            label=f'Fit: slope = {slope:.5f} $\\pm$ {fit["sigma_slope"]:.5f}')

    ax.axhline(0, color='gray', linestyle='--', linewidth=0.5)
    ax.set_xlabel('$\\cos\\theta_{\\mathrm{thrust}}$')
    ax.set_ylabel('$\\langle Q_{FB} \\rangle$')
    ax.legend(fontsize='x-small')

    # Annotate
    ax.text(0.05, 0.95,
            f'$\\chi^2$/ndf = {fit["chi2"]:.1f}/{fit["ndf"]}\n'
            f'$N_{{tagged}}$ = {fit["n_tagged"]:,}',
            transform=ax.transAxes, fontsize='x-small',
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    exp_label_mc(ax)

    save_and_register(fig, "F2_afb_angular_distribution.png", SCRIPT,
                      "A_FB^b angular distribution: <Q_FB> vs cos(theta)",
                      "result", lower_panel="none")


def plot_fd_vs_fs(rb_res):
    """F4: Double-tag fraction vs single-tag fraction with R_b curves."""
    fig, ax = plt.subplots(figsize=(10, 10))

    results = rb_res['extraction_results']
    f_s_vals = [r['f_s'] for r in results]
    f_d_vals = [r['f_d'] for r in results]

    ax.plot(f_s_vals, f_d_vals, 'ko-', markersize=6, label='MC pseudo-data')

    # Draw R_b prediction curves
    eps_b_range = np.linspace(0.05, 0.80, 200)
    for R_b_curve, color, ls in [
        (R_B_SM, 'red', '--'),
        (0.20, 'blue', ':'),
        (0.25, 'green', ':'),
    ]:
        last = results[-1]  # Use last (highest WP) extraction result
        eps_c_nom = last['eps_c'] if last['eps_c'] else 0.1
        eps_uds_nom = last['eps_uds_eff'] if last['eps_uds_eff'] else 0.01
        C_b = last['C_b'] if last['C_b'] else 1.01

        f_s_curve = []
        f_d_curve = []
        for eb in eps_b_range:
            fs = eb * R_b_curve + eps_c_nom * R_C_SM + eps_uds_nom * (1 - R_b_curve - R_C_SM)
            fd = (C_b * eb**2 * R_b_curve + eps_c_nom**2 * R_C_SM
                  + eps_uds_nom**2 * (1 - R_b_curve - R_C_SM))
            f_s_curve.append(fs)
            f_d_curve.append(fd)
        ax.plot(f_s_curve, f_d_curve, color=color, linestyle=ls, linewidth=1,
                label=f'$R_b$ = {R_b_curve:.3f}')

    ax.set_xlabel('$f_s$ (single-tag fraction)')
    ax.set_ylabel('$f_d$ (double-tag fraction)')
    ax.legend(fontsize='x-small')

    # Note moved to LaTeX caption per Doc 4b v3 review

    exp_label_mc(ax)

    save_and_register(fig, "F4_fd_vs_fs.png", SCRIPT,
                      "Double-tag vs single-tag fraction with R_b prediction curves. "
                      "Data points trace varying-efficiency locus; curves use fixed WP 10 efficiencies.",
                      "result", lower_panel="none")


def plot_systematic_breakdown(syst_res):
    """F5: Systematic uncertainty breakdown (horizontal bar chart)."""
    fig, ax = plt.subplots(figsize=(10, 10))

    rb_systs = syst_res['rb_systematics']
    names = list(rb_systs.keys())
    shifts = [rb_systs[n]['delta_Rb'] for n in names]

    # Sort by magnitude
    order = np.argsort(shifts)[::-1]
    names = [names[i] for i in order]
    shifts = [shifts[i] for i in order]

    # Clean names for display
    display_names = {
        'sigma_d0': '$\\sigma_{d_0}$ parameterization',
        'sigma_d0_form': '$\\sigma_{d_0}$ angular form',
        'C_b': 'Hemisphere correlation $C_b$',
        'eps_c': 'Charm efficiency $\\epsilon_c$',
        'eps_uds': 'Light mistag $\\epsilon_{uds}$',
        'R_c': '$R_c$ constraint',
        'g_bb': 'Gluon splitting $g_{b\\bar{b}}$',
        'g_cc': 'Gluon splitting $g_{c\\bar{c}}$',
        'hadronization': 'Hadronization model',
        'physics_params': 'Physics parameters',
        'tau_contamination': '$\\tau$ contamination',
        'selection_bias': 'Selection bias',
        'mc_statistics': 'MC statistics',
    }

    labels = [display_names.get(n, n) for n in names]

    y_pos = np.arange(len(names))
    colors = ['C0' if s > 0.0003 else 'C1' for s in shifts]

    shifts_1e3 = [max(s * 1000, 1e-3) for s in shifts]  # floor for log scale
    ax.barh(y_pos, shifts_1e3, color=colors, alpha=0.7)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize='x-small')
    ax.set_xlabel('$\\delta R_b$ ($\\times 10^{-3}$)')
    ax.set_xscale('log')
    ax.invert_yaxis()

    # Add total
    total = syst_res['rb_total']['syst']
    ax.axvline(total * 1000, color='red', linestyle='--', linewidth=1.5,
               label=f'Total syst. = {total*1000:.2f} $\\times 10^{{-3}}$')
    stat = syst_res['rb_total']['stat']
    ax.axvline(stat * 1000, color='blue', linestyle=':', linewidth=1.5,
               label=f'Statistical = {stat*1000:.2f} $\\times 10^{{-3}}$')

    # Annotate: eps_uds dominates 99.5% of total systematic
    ax.text(0.5, 0.02,
            'Note: $\\epsilon_{uds}$ contributes 99.5% of total syst.',
            transform=ax.transAxes, fontsize='xx-small',
            ha='center', style='italic')

    ax.legend(fontsize='x-small')
    exp_label_mc(ax)

    save_and_register(fig, "F5_systematic_breakdown.png", SCRIPT,
                      "R_b systematic uncertainty breakdown",
                      "systematic_impact", lower_panel="none")


def plot_kappa_consistency(afb_res):
    """F7: A_FB^b kappa consistency."""
    fig, ax = plt.subplots(figsize=(10, 10))

    kappas = []
    afb_vals = []
    afb_errs = []
    for kr in afb_res['kappa_results']:
        if 'A_FB_b' not in kr:
            continue
        if kr.get('demoted', False):
            k = kr['kappa']
            if np.isfinite(k):
                kappas.append(k)
            else:
                kappas.append(5.0)  # Plot infinity at x=5
            afb_vals.append(kr['A_FB_b'])
            afb_errs.append(kr.get('sigma_A_FB_b', 0.01))
            ax.errorbar(kappas[-1], afb_vals[-1], yerr=afb_errs[-1],
                        fmt='x', color='gray', markersize=8, capsize=3)
            continue
        k = kr['kappa']
        if np.isfinite(k):
            kappas.append(k)
        else:
            kappas.append(5.0)
        afb_vals.append(kr['A_FB_b'])
        afb_errs.append(kr.get('sigma_A_FB_b', 0.01))

    ax.errorbar(kappas, afb_vals, yerr=afb_errs, fmt='o', color='black',
                markersize=6, capsize=3, label='MC pseudo-data')

    # Combined result — fix A6: increase visibility with hatching + thicker edges
    comb = afb_res['combination']
    if comb['A_FB_b'] is not None:
        ax.axhspan(comb['A_FB_b'] - comb['sigma_A_FB_b'],
                   comb['A_FB_b'] + comb['sigma_A_FB_b'],
                   alpha=0.35, color='blue', hatch='///', edgecolor='blue', linewidth=1.5,
                   label=f'Combined = {comb["A_FB_b"]:.4f} $\\pm$ {comb["sigma_A_FB_b"]:.4f}')
        # Also draw solid lines at band edges for visibility at small scales
        ax.axhline(comb['A_FB_b'] - comb['sigma_A_FB_b'], color='blue',
                   linewidth=1.0, linestyle='-')
        ax.axhline(comb['A_FB_b'] + comb['sigma_A_FB_b'], color='blue',
                   linewidth=1.0, linestyle='-')

    # ALEPH reference — shown as annotation since scale differs greatly
    ax.axhline(AFB_B_ALEPH, color='green', linewidth=1.5, linestyle='--',
               label=f'ALEPH = {AFB_B_ALEPH} $\\pm$ {AFB_B_ALEPH_ERR}')

    # Zoom y-axis to data region for visibility (fix A6)
    all_y = afb_vals + [comb['A_FB_b']] if comb['A_FB_b'] is not None else afb_vals
    all_yerr = afb_errs + [comb['sigma_A_FB_b']] if comb['A_FB_b'] is not None else afb_errs
    if all_y:
        y_min = min(y - e for y, e in zip(all_y, all_yerr))
        y_max = max(y + e for y, e in zip(all_y, all_yerr))
        margin = 0.3 * (y_max - y_min)
        ax.set_ylim(y_min - margin, y_max + margin)

    ax.set_xlabel('$\\kappa$')
    ax.set_ylabel('$A_{FB}^b$')
    ax.legend(fontsize='x-small')

    # Custom x-ticks
    ax.set_xticks([0.3, 0.5, 1.0, 2.0, 5.0])
    ax.set_xticklabels(['0.3', '0.5', '1.0', '2.0', '$\\infty$'])

    # Annotate chi2
    if comb['p_kappa'] is not None:
        ax.text(0.95, 0.05,
                f'$\\chi^2$/ndf = {comb["chi2_kappa"]:.1f}/{comb["ndf_kappa"]}\n'
                f'p = {comb["p_kappa"]:.3f}',
                transform=ax.transAxes, fontsize='x-small',
                verticalalignment='bottom', horizontalalignment='right',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    exp_label_mc(ax)

    save_and_register(fig, "F7_afb_kappa_consistency.png", SCRIPT,
                      "A_FB^b kappa consistency across five kappa values",
                      "result", lower_panel="none")


def plot_closure_test(closure_res):
    """Closure test results."""
    fig, axes = plt.subplots(1, 2, figsize=(20, 10))

    # Left: Independent closure test pulls
    ax = axes[0]
    closure = closure_res['independent_closure']['per_wp']
    thresholds = [r['threshold'] for r in closure if r['pull'] is not None]
    pulls = [r['pull'] for r in closure if r['pull'] is not None]

    ax.errorbar(thresholds, pulls, yerr=1.0, fmt='o', color='black',
                markersize=6, capsize=3)
    ax.axhline(0, color='gray', linestyle='--')
    ax.axhline(2, color='red', linestyle=':', label='2$\\sigma$')
    ax.axhline(-2, color='red', linestyle=':')
    ax.set_xlabel('Working point (tag threshold)')
    ax.set_ylabel(r'Pull $(R_b^{\mathrm{extracted}} - R_b^{\mathrm{SM}}) / \sigma$')
    ax.set_ylim(-4, 4)
    ax.legend(fontsize='xx-small')
    ax.set_title('Independent closure', fontsize='small', loc='left')

    # Right: Corrupted corrections
    ax = axes[1]
    corrupted = closure_res['corrupted_corrections']['results']
    labels = [r['corruption'] for r in corrupted]
    pulls = [r['pull'] if r['pull'] is not None else 0 for r in corrupted]
    colors = ['red' if abs(p) > 2 else 'blue' for p in pulls]

    y_pos = np.arange(len(labels))
    ax.barh(y_pos, pulls, color=colors, alpha=0.7)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize='xx-small')
    ax.axvline(2, color='red', linestyle=':', linewidth=1)
    ax.axvline(-2, color='red', linestyle=':', linewidth=1)
    ax.set_xlabel(r'Pull $(R_b^{\mathrm{corrupted}} - R_b^{\mathrm{SM}}) / \sigma$')
    ax.set_ylabel('Corruption type')
    ax.invert_yaxis()
    ax.set_title('Corrupted corrections (should FAIL)', fontsize='small', loc='left')

    exp_label_mc(axes[0])

    save_and_register(fig, "closure_test_phase4a.png", SCRIPT,
                      "Phase 4a closure tests: independent closure and sensitivity validation",
                      "closure", lower_panel="none")


def plot_efficiency_calibration(cal):
    """MC efficiency calibration curves — 3 separate figures (fix A5)."""
    full = cal['full_mc_calibration']
    thresholds = []
    eps_b_vals = []
    eps_c_vals = []
    eps_uds_vals = []

    for thr_str, data in sorted(full.items(), key=lambda x: float(x[0])):
        thresholds.append(float(thr_str))
        eps_b_vals.append(data['eps_b'])
        eps_c_vals.append(data['eps_c'])
        eps_uds_vals.append(data['eps_uds'])

    for vals, label, color, fname, desc in [
        (eps_b_vals, '$\\epsilon_b$', 'C0',
         'efficiency_calibration_eps_b.png', 'MC-derived b-tagging efficiency vs working point'),
        (eps_c_vals, '$\\epsilon_c$', 'C1',
         'efficiency_calibration_eps_c.png', 'MC-derived charm tagging efficiency vs working point'),
        (eps_uds_vals, '$\\epsilon_{uds}$', 'C2',
         'efficiency_calibration_eps_uds.png', 'MC-derived light-flavour mistag rate vs working point'),
    ]:
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.plot(thresholds, vals, 'o-', color=color, markersize=8, linewidth=2)
        ax.set_xlabel('Working point')
        ax.set_ylabel(label)
        ax.set_ylim(bottom=0)
        ax.text(0.05, 0.45, 'MC calibration (assuming $R_b^{\\rm SM}$)',
                transform=ax.transAxes, fontsize='small', va='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        exp_label_mc(ax)
        save_and_register(fig, fname, SCRIPT, desc,
                          "diagnostic", lower_panel="none")


def plot_correlation(corr):
    """C_b vs working point."""
    fig, ax = plt.subplots(figsize=(10, 10))

    mc_wp = corr['mc_vs_wp']
    data_wp = corr['data_vs_wp']

    thr_mc = [r['threshold'] for r in mc_wp]
    C_mc = [r['C'] for r in mc_wp]
    sig_mc = [r['sigma_C'] for r in mc_wp]

    thr_data = [r['threshold'] for r in data_wp]
    C_data = [r['C'] for r in data_wp]
    sig_data = [r['sigma_C'] for r in data_wp]

    ax.errorbar(thr_mc, C_mc, yerr=sig_mc, fmt='s', color='C0',
                markersize=5, capsize=3, label='MC')
    ax.errorbar([t + 0.1 for t in thr_data], C_data, yerr=sig_data,
                fmt='o', color='black', markersize=5, capsize=3, label='Data')

    ax.axhline(1.01, color='red', linestyle='--', linewidth=1,
               label='Published ALEPH $C_b$ = 1.01')
    ax.axhline(1.0, color='gray', linestyle=':', linewidth=0.5)

    ax.set_xlabel('Combined tag threshold')
    ax.set_ylabel('Hemisphere correlation $C$')
    ax.legend(fontsize='x-small')
    exp_label_mc(ax)

    save_and_register(fig, "hemisphere_correlation.png", SCRIPT,
                      "Hemisphere correlation C vs working point (MC and data)",
                      "diagnostic", lower_panel="none")


R_C_SM = 0.17223


def main():
    log.info("=" * 60)
    log.info("Phase 4a: Plotting")
    log.info("=" * 60)

    # Load results
    with open(OUT / "rb_results.json") as f:
        rb_res = json.load(f)
    with open(OUT / "afb_results.json") as f:
        afb_res = json.load(f)
    with open(OUT / "systematics_results.json") as f:
        syst_res = json.load(f)
    with open(OUT / "closure_stress_results.json") as f:
        closure_res = json.load(f)
    with open(OUT / "mc_calibration.json") as f:
        cal = json.load(f)
    with open(OUT / "correlation_results.json") as f:
        corr = json.load(f)

    # Flagship figures
    log.info("Plotting F1: R_b stability scan")
    plot_rb_stability(rb_res)

    log.info("Plotting F2: A_FB^b angular distribution")
    plot_afb_angular(afb_res)

    log.info("Plotting F4: f_d vs f_s")
    plot_fd_vs_fs(rb_res)

    log.info("Plotting F5: Systematic breakdown")
    plot_systematic_breakdown(syst_res)

    log.info("Plotting F7: Kappa consistency")
    plot_kappa_consistency(afb_res)

    # Supporting figures
    log.info("Plotting closure tests")
    plot_closure_test(closure_res)

    log.info("Plotting efficiency calibration")
    plot_efficiency_calibration(cal)

    log.info("Plotting hemisphere correlation")
    plot_correlation(corr)

    log.info("\nAll figures saved to %s", FIG)


if __name__ == "__main__":
    main()
