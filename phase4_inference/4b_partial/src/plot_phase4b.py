"""Phase 4b: Comparison plots — 10% data vs MC/expected.

Produces:
- F1b: R_b stability scan with 10% data overlay
- F2b: A_FB^b angular distribution from 10% data
- F3b: d0/sigma_d0 data vs MC comparison (deferred from 4a)
- F4b: Double-tag fraction vs single-tag fraction (data overlay)
- F5b: Systematic breakdown (10% data)
- F7b: Kappa consistency (10% data)
- S1b: Tag fractions data vs MC comparison
- S2b: Hemisphere charge data vs MC
"""
import json
import logging
import sys
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

mh.style.use("CMS")

HERE = Path(__file__).resolve().parent
PHASE4B_OUT = HERE.parent / "outputs"
FIG = PHASE4B_OUT / "figures"
FIG.mkdir(parents=True, exist_ok=True)

P3_OUT = HERE.parents[2] / "phase3_selection" / "outputs"
P4A_OUT = HERE.parents[1] / "4a_expected" / "outputs"
RESULTS_DIR = HERE.parents[2] / "analysis_note" / "results"

sys.path.insert(0, str(HERE.parents[2] / "phase3_selection" / "src"))
import plot_utils
from plot_utils import exp_label_data, exp_label_mc

# Override plot_utils module-level FIG and OUT so save_and_register
# writes to Phase 4b outputs, not Phase 3 outputs.
plot_utils.FIG = FIG
plot_utils.OUT = PHASE4B_OUT
from plot_utils import save_and_register

SCRIPT_PATH = str(Path(__file__).relative_to(HERE.parents[2]))


def load_results():
    """Load all Phase 4b results."""
    with open(PHASE4B_OUT / "rb_results_10pct.json") as f:
        rb = json.load(f)
    with open(PHASE4B_OUT / "afb_results_10pct.json") as f:
        afb = json.load(f)
    with open(PHASE4B_OUT / "comparison_4a_vs_4b.json") as f:
        comp = json.load(f)
    with open(P4A_OUT / "rb_results.json") as f:
        rb_4a = json.load(f)
    with open(P4A_OUT / "afb_results.json") as f:
        afb_4a = json.load(f)

    syst = None
    syst_path = PHASE4B_OUT / "systematics_10pct.json"
    if syst_path.exists():
        with open(syst_path) as f:
            syst = json.load(f)

    return rb, afb, comp, rb_4a, afb_4a, syst


def plot_rb_stability(rb, rb_4a):
    """F1b: R_b stability scan with 10% data overlay."""
    fig, ax = plt.subplots(figsize=(10, 10))

    # Phase 4a MC results
    wps_4a = []
    rbs_4a = []
    errs_4a = []
    for r in rb_4a['extraction_results']:
        if r['R_b'] is not None:
            wps_4a.append(r['threshold'])
            rbs_4a.append(r['R_b'])
            errs_4a.append(r['sigma_stat'] or 0.05)

    if wps_4a:
        ax.errorbar(wps_4a, rbs_4a, yerr=errs_4a, fmt='s', color='C0',
                     label='MC pseudo-data', markersize=8, capsize=4)

    # Phase 4b 10% data results
    wps_4b = []
    rbs_4b = []
    errs_4b = []
    for r in rb['extraction_results']:
        if r['R_b'] is not None:
            wps_4b.append(r['threshold'])
            rbs_4b.append(r['R_b'])
            errs_4b.append(r['sigma_stat'] or 0.05)

    if wps_4b:
        ax.errorbar(wps_4b, rbs_4b, yerr=errs_4b, fmt='o', color='C1',
                     label='10% data', markersize=8, capsize=4)

    # SM and ALEPH bands
    ax.axhline(0.21578, color='red', linestyle='--', linewidth=1.5,
               label=r'$R_b^{\rm SM} = 0.21578$')
    ax.axhspan(0.2158 - 0.0014, 0.2158 + 0.0014, color='green', alpha=0.15,
               label=r'ALEPH $0.2158 \pm 0.0014$')
    ax.axhspan(0.21629 - 0.00066, 0.21629 + 0.00066, color='blue', alpha=0.1,
               label=r'LEP combined $0.21629 \pm 0.00066$')

    ax.set_xlabel('Working Point (combined tag threshold)')
    ax.set_ylabel(r'$R_b$')
    ax.set_ylim(0.10, 0.45)
    ax.legend(loc='upper left', fontsize='x-small')
    exp_label_data(ax)

    save_and_register(fig, "F1b_rb_stability_10pct.png", SCRIPT_PATH,
                      "R_b operating point stability: MC pseudo-data vs 10% data",
                      "result")


def plot_afb_angular(afb):
    """F2b: A_FB^b angular distribution from 10% data."""
    fig, ax = plt.subplots(figsize=(10, 10))

    # Find kappa=0.3 simple fit for display (best sensitivity)
    for kr in afb['kappa_results']:
        if kr['kappa'] == 0.3 and kr.get('simple_fit'):
            sf = kr['simple_fit']
            bin_centers = np.array(sf['bin_centers'])
            mean_qfb = np.array([x if x is not None else np.nan for x in sf['mean_qfb']])
            sigma_qfb = np.array([x if x is not None else np.nan for x in sf['sigma_qfb']])

            valid = ~np.isnan(mean_qfb)
            ax.errorbar(bin_centers[valid], mean_qfb[valid],
                        yerr=sigma_qfb[valid], fmt='o', color='black',
                        label=r'10% data ($\kappa=0.3$)', markersize=6, capsize=3)

            # Fit line
            slope = sf['slope']
            intercept = sf.get('intercept', 0.0)
            x_fit = np.linspace(-0.9, 0.9, 100)
            ax.plot(x_fit, intercept + slope * x_fit, 'C1-',
                    label=f'Fit: slope = {slope:.5f} $\\pm$ {sf["sigma_slope"]:.5f}')
            break

    # SM expectation (for comparison)
    # A_FB^b ~ 0.0927 (ALEPH published)
    # <Q_FB> ~ delta_b * A_FB^b * cos(theta)
    # With delta_b ~ 0.16 and A_FB ~ 0.09 => slope ~ 0.015
    ax.plot(x_fit, 0.015 * x_fit, 'r--', alpha=0.5,
            label=r'Expected $\delta_b \times A_{\rm FB}^b \approx 0.015$')

    ax.axhline(0, color='gray', linestyle=':', linewidth=0.5)
    ax.set_xlabel(r'$\cos\theta_{\rm thrust}$')
    ax.set_ylabel(r'$\langle Q_{\rm FB} \rangle$')
    ax.legend(fontsize='x-small')
    exp_label_data(ax)

    save_and_register(fig, "F2b_afb_angular_10pct.png", SCRIPT_PATH,
                      "A_FB^b angular distribution from 10% data (kappa=0.3)",
                      "result")


def plot_d0_sigma_data_mc():
    """F3b: d0/sigma_d0 data vs MC (deferred from Phase 4a)."""
    # Load Phase 3 data for full sample and MC
    data_sig = np.load(P3_OUT / "signed_d0.npz", allow_pickle=False)
    data_signed = data_sig["data_signed_sig"]
    mc_signed = data_sig["mc_signed_sig"]

    fig, (ax, rax) = plt.subplots(2, 1, figsize=(10, 10),
                                   gridspec_kw={"height_ratios": [3, 1]},
                                   sharex=True)
    fig.subplots_adjust(hspace=0)

    bins = np.linspace(-10, 30, 80)
    bin_centers = 0.5 * (bins[:-1] + bins[1:])

    h_data, _ = np.histogram(data_signed, bins=bins)
    h_mc, _ = np.histogram(mc_signed, bins=bins)

    # Normalize MC to data
    scale = h_data.sum() / h_mc.sum() if h_mc.sum() > 0 else 1.0
    h_mc_scaled = h_mc * scale

    mh.histplot(h_mc_scaled, bins=bins, ax=ax, label='MC (normalized)',
                histtype='fill', color='C0', alpha=0.5)
    mh.histplot(h_mc_scaled, bins=bins, ax=ax, histtype='step', color='C0')
    ax.errorbar(bin_centers, h_data, yerr=np.sqrt(np.maximum(h_data, 1)),
                fmt='o', color='black', markersize=3, label='Data (full)')

    ax.set_ylabel('Events')
    ax.set_yscale('log')
    ax.set_ylim(1, ax.get_ylim()[1] * 2)
    ax.legend(fontsize='x-small')
    exp_label_data(ax)

    # Pull panel — show bins where at least one of data or MC is nonzero
    total_err = np.sqrt(np.maximum(h_data, 1) + np.maximum(h_mc_scaled, 1))
    pull = (h_data - h_mc_scaled) / total_err
    populated = (h_data > 0) | (h_mc_scaled > 0)
    rax.errorbar(bin_centers[populated], pull[populated], yerr=1.0,
                 fmt='o', color='black', markersize=2)
    rax.axhline(0, color='gray', linestyle='--', linewidth=0.8)
    rax.axhline(2, color='gray', linestyle=':', linewidth=0.5)
    rax.axhline(-2, color='gray', linestyle=':', linewidth=0.5)
    rax.set_ylabel(r'(Data $-$ MC) / $\sigma$')
    rax.set_xlabel(r'Signed $d_0 / \sigma_{d_0}$')
    rax.set_ylim(-4, 4)
    rax.set_yticks([-2, 0, 2])

    save_and_register(fig, "F3b_d0_sigma_data_mc.png", SCRIPT_PATH,
                      "Signed d0/sigma_d0 data vs MC comparison (log scale)",
                      "data_mc", lower_panel="pull")


def plot_fd_vs_fs(rb, rb_4a):
    """F4b: Double-tag fraction vs single-tag fraction with R_b curves."""
    fig, ax = plt.subplots(figsize=(10, 10))

    # Phase 4a MC
    fs_4a = [r['f_s'] for r in rb_4a['extraction_results'] if r['f_s'] > 0]
    fd_4a = [r['f_d'] for r in rb_4a['extraction_results'] if r['f_s'] > 0]
    ax.plot(fs_4a, fd_4a, 's-', color='C0', label='MC pseudo-data', markersize=6)

    # Phase 4b 10% data
    fs_4b = [r['f_s'] for r in rb['extraction_results'] if r['f_s'] > 0]
    fd_4b = [r['f_d'] for r in rb['extraction_results'] if r['f_s'] > 0]
    ax.plot(fs_4b, fd_4b, 'o-', color='C1', label='10% data', markersize=6)

    # R_b theory curves using double-tag formula:
    # f_s = R_b*eps_b + R_c*eps_c + (1-R_b-R_c)*eps_uds
    # f_d = R_b*eps_b^2*C_b + R_c*eps_c^2 + (1-R_b-R_c)*eps_uds^2
    # For a fixed R_b, eps_b varies with WP; we parameterize
    # eps_b = (f_s - R_c*eps_c - (1-R_b-R_c)*eps_uds) / R_b
    # f_d = R_b * eps_b^2 * C_b + R_c*eps_c^2 + (1-R_b-R_c)*eps_uds^2
    # Use representative eps_c=0.05, eps_uds=0.01, C_b=1.01, R_c=0.172
    eps_c_ref, eps_uds_ref, Cb_ref, Rc_ref = 0.05, 0.01, 1.01, 0.172
    fs_theory = np.linspace(0.05, 0.4, 100)
    for Rb_val, ls, lbl in [(0.216, '--', r'$R_b = 0.216$ (SM)'),
                              (0.230, ':', r'$R_b = 0.230$'),
                              (0.200, '-.', r'$R_b = 0.200$')]:
        eps_b_th = (fs_theory - Rc_ref * eps_c_ref
                    - (1 - Rb_val - Rc_ref) * eps_uds_ref) / Rb_val
        fd_theory = (Rb_val * eps_b_th**2 * Cb_ref
                     + Rc_ref * eps_c_ref**2
                     + (1 - Rb_val - Rc_ref) * eps_uds_ref**2)
        valid_th = eps_b_th > 0
        ax.plot(fs_theory[valid_th], fd_theory[valid_th], ls, color='gray',
                alpha=0.5, label=lbl)

    ax.set_xlabel(r'$f_s$ (single-tag fraction)')
    ax.set_ylabel(r'$f_d$ (double-tag fraction)')
    ax.set_xlim(0, 0.4)
    ax.set_ylim(0, 0.15)
    ax.legend(fontsize='x-small')
    exp_label_data(ax)

    save_and_register(fig, "F4b_fd_vs_fs_10pct.png", SCRIPT_PATH,
                      "Double-tag vs single-tag fraction: MC and 10% data",
                      "result")


def plot_systematic_breakdown(syst):
    """F5b: Systematic breakdown for 10% data."""
    if syst is None:
        log.warning("No systematics results available; skipping F5b")
        return

    fig, ax = plt.subplots(figsize=(10, 10))

    rb_systs = syst['rb_systematics']
    names = sorted(rb_systs.keys(), key=lambda k: -rb_systs[k]['delta_Rb'])
    values = [rb_systs[n]['delta_Rb'] for n in names]

    # Publication-quality labels
    label_map = {
        'eps_uds': r'Light-quark mistag ($\varepsilon_{\rm uds}$)',
        'C_b': r'Hemisphere correlation ($C_b$)',
        'eps_c': r'Charm efficiency ($\varepsilon_c$)',
        'R_c': r'$R_c$ constraint',
        'sigma_d0': r'$\sigma_{d_0}$ scale ($\pm 10\%$)',
        'sigma_d0_form': r'$\sigma_{d_0}$ angular form',
        'hadronization': 'Hadronization model',
        'physics_params': 'Physics parameters',
        'g_bb': r'Gluon splitting $g_{b\bar{b}}$',
        'g_cc': r'Gluon splitting $g_{c\bar{c}}$',
        'tau_contamination': r'$\tau$ contamination',
        'selection_bias': 'Selection bias',
        'mc_statistics': 'MC statistics',
    }
    display_names = [label_map.get(n, n.replace('_', ' ')) for n in names]

    y_pos = np.arange(len(names))
    bars = ax.barh(y_pos, values, color='C0', alpha=0.7)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(display_names, fontsize='x-small')
    ax.set_xlabel(r'$\delta R_b$')
    ax.set_xscale('log')

    # Add stat uncertainty line
    stat = syst['rb_total']['stat']
    ax.axvline(stat, color='red', linestyle='--', label=f'Stat. unc. = {stat:.4f}')

    # Total systematic line
    total_syst = syst['rb_total']['syst']
    ax.axvline(total_syst, color='green', linestyle='-.',
               label=f'Total syst. = {total_syst:.4f}')

    ax.legend(fontsize='x-small')
    ax.invert_yaxis()
    exp_label_data(ax)

    save_and_register(fig, "F5b_systematic_breakdown_10pct.png", SCRIPT_PATH,
                      "R_b systematic uncertainty breakdown (10% data)",
                      "systematic_impact")


def plot_kappa_consistency(afb, afb_4a):
    """F7b: Kappa consistency for 10% data."""
    fig, ax = plt.subplots(figsize=(10, 10))

    # Phase 4a MC
    kappas_4a = []
    afbs_4a = []
    errs_4a = []
    for kr in afb_4a['kappa_results']:
        if 'A_FB_b' in kr and kr.get('sigma_A_FB_b', 0) > 0:
            k = kr['kappa']
            if k == float('inf'):
                k = 5.0  # Plot position for inf
            kappas_4a.append(k)
            afbs_4a.append(kr['A_FB_b'])
            errs_4a.append(kr['sigma_A_FB_b'])

    if kappas_4a:
        ax.errorbar(kappas_4a, afbs_4a, yerr=errs_4a, fmt='s', color='C0',
                     label='MC pseudo-data', markersize=8, capsize=4)

    # Phase 4b 10% data
    kappas_4b = []
    afbs_4b = []
    errs_4b = []
    for kr in afb['kappa_results']:
        if 'A_FB_b' in kr and kr.get('sigma_A_FB_b', 0) > 0:
            k = kr['kappa']
            if k == float('inf') or str(k) == 'inf' or str(k) == 'Infinity':
                k = 5.0
            kappas_4b.append(k)
            afbs_4b.append(kr['A_FB_b'])
            errs_4b.append(kr['sigma_A_FB_b'])

    if kappas_4b:
        ax.errorbar([k + 0.05 for k in kappas_4b], afbs_4b, yerr=errs_4b,
                     fmt='o', color='C1', label='10% data', markersize=8, capsize=4)

    # Reference values
    ax.axhline(0.0927, color='green', linestyle='--', linewidth=1.5,
               label=r'ALEPH $A_{\rm FB}^b = 0.0927$')
    ax.axhline(0.0, color='gray', linestyle=':', linewidth=0.5)

    # Combined value
    comb = afb['combination']
    if comb['A_FB_b'] is not None:
        ax.axhspan(comb['A_FB_b'] - (comb['sigma_A_FB_b'] or 0),
                   comb['A_FB_b'] + (comb['sigma_A_FB_b'] or 0),
                   color='C1', alpha=0.15,
                   label=f'Combined: {comb["A_FB_b"]:.4f} $\\pm$ {comb["sigma_A_FB_b"]:.4f}')

    ax.set_xlabel(r'$\kappa$ (momentum-weighting exponent)')
    ax.set_ylabel(r'$A_{\rm FB}^b$ (purity-corrected, no charm subtraction)')
    ax.set_xlim(0, 5.5)
    ax.legend(fontsize='x-small')
    exp_label_data(ax)

    save_and_register(fig, "F7b_kappa_consistency_10pct.png", SCRIPT_PATH,
                      "A_FB^b kappa consistency: MC pseudo-data vs 10% data",
                      "result")


def plot_tag_fractions_comparison():
    """S1b: Tag fractions data vs MC comparison."""
    # Load full MC and 10% data tags
    mc_tags = np.load(P3_OUT / "hemisphere_tags.npz", allow_pickle=False)
    data_10pct_path = PHASE4B_OUT / "data_10pct_tags.npz"
    if not data_10pct_path.exists():
        log.warning("data_10pct_tags.npz not found; skipping S1b")
        return

    data_tags = np.load(data_10pct_path, allow_pickle=False)

    fig, ax = plt.subplots(figsize=(10, 10))

    thresholds = np.arange(1, 15, 0.5)

    mc_h0 = mc_tags["mc_combined_h0"]
    mc_h1 = mc_tags["mc_combined_h1"]
    n_mc = len(mc_h0)

    data_h0 = data_tags["data_combined_h0"]
    data_h1 = data_tags["data_combined_h1"]
    n_data = len(data_h0)

    fs_mc = []
    fs_data = []
    for thr in thresholds:
        t0_mc = mc_h0 > thr
        t1_mc = mc_h1 > thr
        fs_mc.append((np.sum(t0_mc) + np.sum(t1_mc)) / (2 * n_mc))

        t0_d = data_h0 > thr
        t1_d = data_h1 > thr
        fs_data.append((np.sum(t0_d) + np.sum(t1_d)) / (2 * n_data))

    ax.plot(thresholds, fs_mc, 's-', color='C0', label='MC (full)', markersize=4)
    ax.plot(thresholds, fs_data, 'o-', color='C1', label='Data (10%)', markersize=4)
    ax.set_xlabel('Combined tag threshold')
    ax.set_ylabel(r'$f_s$ (single-tag fraction)')
    ax.set_yscale('log')
    ax.legend(fontsize='x-small')
    exp_label_data(ax)

    save_and_register(fig, "S1b_tag_fractions_comparison.png", SCRIPT_PATH,
                      "Single-tag fraction vs threshold: MC and 10% data",
                      "diagnostic")  # Line plot — pull panels impractical


def plot_hemisphere_charge_comparison():
    """S2b: Hemisphere charge distributions data vs MC."""
    data_jc_path = PHASE4B_OUT / "data_10pct_jetcharge.npz"
    if not data_jc_path.exists():
        log.warning("data_10pct_jetcharge.npz not found; skipping S2b")
        return

    data_jc = np.load(data_jc_path, allow_pickle=False)
    mc_jc = np.load(P3_OUT / "jet_charge.npz", allow_pickle=False)

    fig, axes = plt.subplots(2, 2, figsize=(20, 20))

    for idx, kappa in enumerate([0.3, 0.5, 1.0, 2.0]):
        ax = axes[idx // 2, idx % 2]
        k_str = f"k{kappa:.1f}"

        qfb_data = data_jc[f"data_qfb_{k_str}"]
        qfb_mc = mc_jc[f"mc_qfb_{k_str}"]

        valid_data = ~np.isnan(qfb_data)
        valid_mc = ~np.isnan(qfb_mc)

        bins = np.linspace(-0.5, 0.5, 50)
        h_data, _ = np.histogram(qfb_data[valid_data], bins=bins)
        h_mc, _ = np.histogram(qfb_mc[valid_mc], bins=bins)

        # Normalize
        scale = h_data.sum() / h_mc.sum() if h_mc.sum() > 0 else 1.0
        h_mc_scaled = h_mc * scale

        bin_centers = 0.5 * (bins[:-1] + bins[1:])
        mh.histplot(h_mc_scaled, bins=bins, ax=ax, histtype='fill',
                     color='C0', alpha=0.4, label='MC (norm. to data)')
        ax.errorbar(bin_centers, h_data, yerr=np.sqrt(np.maximum(h_data, 1)),
                     fmt='o', color='black', markersize=2, label='Data (10%)')
        ax.set_xlabel(r'$Q_{\rm FB}$ (momentum-weighted charge)')
        ax.set_ylabel('Events / bin')
        ax.text(0.05, 0.85, f'$\\kappa = {kappa}$',
                transform=ax.transAxes, va='top', fontsize='small')
        ax.legend(fontsize='x-small', loc='upper right')
        exp_label_data(ax)
    save_and_register(fig, "S2b_hemisphere_charge_data_mc.png", SCRIPT_PATH,
                      "Q_FB distribution: MC (full) vs 10% data at four kappa values",
                      "diagnostic")  # 2x2 subplot comparison — pull panels in subplots impractical


def main():
    log.info("=" * 60)
    log.info("Phase 4b: Plotting")
    log.info("=" * 60)

    rb, afb, comp, rb_4a, afb_4a, syst = load_results()

    plot_rb_stability(rb, rb_4a)
    plot_afb_angular(afb)
    plot_d0_sigma_data_mc()
    plot_fd_vs_fs(rb, rb_4a)
    plot_systematic_breakdown(syst)
    plot_kappa_consistency(afb, afb_4a)
    plot_tag_fractions_comparison()
    plot_hemisphere_charge_comparison()

    log.info("All Phase 4b plots saved to %s", FIG)


if __name__ == "__main__":
    main()
