"""Generate corrected figures for Doc 4c v8.

Fixes:
1. AFB angular distribution: full data at kappa=0.3, WP>5 (replaces stale Phase 4a MC)
2. Calibration progression: fix garbled label
3. BDT crosscheck: already correct in bdt_crosscheck_fulldata.pdf

Note: F1 (rb_stability) and F7 (afb_kappa) are replaced in the tex by
pointing to the already-correct full-data figures.
"""
import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mplhep as mh

HERE = Path(__file__).resolve().parent
FIG_DIR = HERE / "figures"
P4C_OUT = HERE.parent / "phase4_inference" / "4c_observed" / "outputs"
P4B_OUT = HERE.parent / "phase4_inference" / "4b_partial" / "outputs"

sys.path.insert(0, str(HERE.parent / "phase3_selection" / "src"))
from plot_utils import exp_label_data

mh.style.use("CMS")


def plot_afb_angular_fulldata():
    """Plot mean Q_FB vs cos_theta for full data at kappa=0.3, WP>5.

    This replaces the stale Phase 4a MC pseudo-data figure.
    Uses the corrected AFB extraction data.
    """
    with open(P4C_OUT / "afb_fulldata_corrected.json") as f:
        d = json.load(f)

    # Find kappa=0.3, WP=5 result
    for kr in d["kappa_results"]:
        if kr["kappa"] == 0.3:
            for wpr in kr["per_wp_results"]:
                if wpr["threshold"] == 5.0:
                    s = wpr["slope"]
                    break
            break

    bin_centers = np.array(s["bin_centers"])
    mean_qfb = np.array(s["mean_qfb"])
    sigma_qfb = np.array(s["sigma_qfb"])
    chi2_val = s["chi2"]
    ndf = s["ndf"]
    slope = s["slope"]
    sigma_slope = s["sigma_slope"]
    intercept = s["intercept"]
    n_tagged = s["n_tagged"]

    fig, ax = plt.subplots(figsize=(10, 10))

    ax.errorbar(bin_centers, mean_qfb, yerr=sigma_qfb, fmt="o", color="C0",
                markersize=8, capsize=5, linewidth=2,
                label="ALEPH data 1992--1995")

    # Fit line
    x_fit = np.linspace(-0.9, 0.9, 200)
    y_fit = slope * x_fit + intercept
    ax.plot(x_fit, y_fit, "r-", linewidth=2,
            label=("Fit: slope = %.5f $\\pm$ %.5f" % (slope, sigma_slope)))

    ax.axhline(0, color="gray", linestyle=":", linewidth=1)

    # Annotation box
    txt = "\n".join([
        r"$\kappa = 0.3$, WP $> 5$",
        r"$\chi^2$/ndf = %.1f/%d" % (chi2_val, ndf),
        r"$N_{\rm tagged}$ = %s" % f"{n_tagged:,}",
    ])
    ax.text(0.05, 0.95, txt, transform=ax.transAxes, ha="left", va="top",
            fontsize="x-small",
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

    ax.set_xlabel(r"$\cos\theta$")
    ax.set_ylabel(r"$\langle Q_{\rm FB} \rangle$")
    ax.legend(loc="lower left", fontsize="x-small")
    exp_label_data(ax)

    fig.savefig(FIG_DIR / "afb_angular_fulldata.pdf",
                bbox_inches="tight", dpi=200)
    fig.savefig(FIG_DIR / "afb_angular_fulldata.png",
                bbox_inches="tight", dpi=200)
    plt.close(fig)
    print("Saved afb_angular_fulldata.pdf")


def plot_calibration_progression_fixed():
    """Regenerate calibration progression with correct label placement."""
    R_B_SM = 0.21578
    AFB_B_OBS = 0.0995

    with open(P4C_OUT / "three_tag_rb_fulldata.json") as f:
        full_rb = json.load(f)
    with open(P4C_OUT / "afb_fulldata.json") as f:
        full_afb = json.load(f)

    p4b_rb_path = P4B_OUT / "three_tag_rb_10pct.json"
    p4b_afb_path = P4B_OUT / "purity_afb_10pct.json"

    stages = ["MC (4a)", "10% (4b)", "Full (4c)"]
    rb_vals = []
    rb_errs = []

    mc_rb = full_rb["comparison_4a"]["mc_R_b"]
    mc_sig = full_rb["comparison_4a"]["mc_sigma"]
    rb_vals.append(mc_rb)
    rb_errs.append(mc_sig or 0)

    if p4b_rb_path.exists():
        with open(p4b_rb_path) as f:
            p4b = json.load(f)
        rb_10 = p4b["stability"]["R_b_combined"]
        sig_10 = p4b["stability"]["sigma_combined"]
        rb_vals.append(rb_10)
        rb_errs.append(sig_10 or 0)
    else:
        partial_rb = full_rb["comparison_4b"]["partial_R_b"]
        partial_sig = full_rb["comparison_4b"]["partial_sigma"]
        rb_vals.append(partial_rb or 0)
        rb_errs.append(partial_sig or 0)

    full_rb_val = full_rb["stability"]["R_b_combined"]
    full_rb_sig = full_rb["stability"]["sigma_combined"]
    rb_vals.append(full_rb_val or 0)
    rb_errs.append(full_rb_sig or 0)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 10))

    x = np.arange(len(stages))
    ax1.errorbar(x, rb_vals, yerr=rb_errs, fmt="o", color="C0",
                 markersize=12, capsize=6, linewidth=2)
    ax1.axhline(R_B_SM, color="red", linestyle="--", linewidth=1.5,
                label=r"$R_b^{\rm SM}$")
    ax1.set_xticks(x)
    ax1.set_xticklabels(stages)
    ax1.set_ylabel(r"$R_b$")
    ax1.legend(fontsize="small")
    # Manual label to avoid garbled overlap in two-panel layout
    ax1.text(0.05, 1.02, "ALEPH Open Data",
             fontsize=14, fontweight="bold",
             transform=ax1.transAxes, ha="left", va="bottom")
    ax1.text(0.95, 1.02, r"$\sqrt{s} = 91.2$ GeV",
             fontsize=12,
             transform=ax1.transAxes, ha="right", va="bottom")

    # A_FB comparison
    afb_vals = [0.0]
    afb_errs = [0.0]

    if p4b_afb_path.exists():
        with open(p4b_afb_path) as f:
            p4b_a = json.load(f)
        afb_10 = p4b_a["combination"]["A_FB_b"]
        sig_10_a = p4b_a["combination"]["sigma_A_FB_b"]
        afb_vals.append(afb_10 or 0)
        afb_errs.append(sig_10_a or 0)
    else:
        afb_vals.append(0)
        afb_errs.append(0)

    afb_full = full_afb["combination"]["A_FB_b"]
    sig_full_a = full_afb["combination"]["sigma_A_FB_b"]
    afb_vals.append(afb_full or 0)
    afb_errs.append(sig_full_a or 0)

    ax2.errorbar(x, afb_vals, yerr=afb_errs, fmt="s", color="C1",
                 markersize=12, capsize=6, linewidth=2)
    ax2.axhline(AFB_B_OBS, color="red", linestyle="--", linewidth=1.5,
                label=r"LEP combined")
    ax2.axhline(0, color="gray", linestyle=":", linewidth=1)
    ax2.set_xticks(x)
    ax2.set_xticklabels(stages)
    ax2.set_ylabel(r"$A_{\rm FB}^b$")
    ax2.legend(fontsize="small")

    # Wider spacing to prevent label overlap
    fig.subplots_adjust(wspace=0.40)

    fig.savefig(FIG_DIR / "calibration_progression.pdf",
                bbox_inches="tight", dpi=200)
    fig.savefig(FIG_DIR / "calibration_progression.png",
                bbox_inches="tight", dpi=200)
    plt.close(fig)
    print("Saved calibration_progression.pdf (fixed)")


if __name__ == "__main__":
    plot_afb_angular_fulldata()
    plot_calibration_progression_fixed()
    print("Done generating v8 figures.")
