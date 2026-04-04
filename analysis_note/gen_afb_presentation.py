"""Generate improved A_FB^b presentation figures for Doc 4c v10.

Creates two figures:
  F_afb_extraction: <Q_FB> vs |cos(theta)| with fit line + annotation
  F_afb_signed_diagnostic: <Q_FB> vs signed cos(theta) showing parabolic shape

Session: sal_f027
"""
import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mplhep as mh
from scipy.stats import chi2 as chi2_dist

HERE = Path(__file__).resolve().parent
FIG_DIR = HERE / "figures"
P4C_OUT = HERE.parent / "phase4_inference" / "4c_observed" / "outputs"

sys.path.insert(0, str(HERE.parent / "phase3_selection" / "src"))
from plot_utils import exp_label_data

mh.style.use("CMS")


def plot_afb_extraction():
    """Primary figure: <Q_FB> vs |cos(theta)| with fit and derivation annotation."""

    with open(P4C_OUT / "afb_systematics_final.json") as f:
        d = json.load(f)

    nom = d["nominal"]
    x = np.array(nom["bin_centers"])
    y = np.array(nom["asymmetry"])
    sigma = np.array(nom["sigma_asymmetry"])
    product = nom["product"]           # fitted delta_b * AFB
    sigma_product = nom["sigma_product"]
    delta_b = nom["delta_b"]
    afb_b = nom["afb_b"]
    sigma_afb = nom["sigma_afb"]
    chi2_val = nom["chi2"]
    ndf = nom["ndf"]
    p_val = nom["p_value"]
    n_tagged = nom["n_tagged"]

    # Fit curve: a(|cos|) = (8/3) * |cos| / (1 + cos^2) * product
    x_fine = np.linspace(0, 0.9, 200)
    model_fine = (8.0 / 3.0) * x_fine / (1.0 + x_fine**2) * product

    fig, ax = plt.subplots(figsize=(10, 10))

    ax.errorbar(x, y, yerr=sigma, fmt="o", color="black",
                markersize=8, capsize=5, linewidth=2, zorder=5,
                label="ALEPH data 1992--1995")

    ax.plot(x_fine, model_fine, "r-", linewidth=2.5, zorder=4,
            label=r"Fit: $\frac{8}{3}\,\frac{|\cos\theta|}{1+\cos^2\!\theta}"
                  r"\;\delta_b\,A_{\mathrm{FB}}^b$")

    ax.axhline(0, color="gray", linestyle=":", linewidth=1)

    # Fit result annotation box
    lines = [
        r"$\kappa = 0.3$,  WP $> 5$",
        r"$N_{\mathrm{tagged}}$ = %s" % f"{n_tagged:,}",
        "",
        r"Fit: $\delta_b \cdot A_{\mathrm{FB}}^b = %.5f \pm %.5f$"
            % (product, sigma_product),
        r"$\chi^2/\mathrm{ndf} = %.1f\,/\,%d$  ($p = %.2f$)"
            % (chi2_val, ndf, p_val),
        "",
        r"$\delta_b(\kappa\!=\!0.3) = %.3f$  [ALEPH published]" % delta_b,
        r"$\Rightarrow\; A_{\mathrm{FB}}^b = %.4f \pm %.4f\;\mathrm{(stat)}$"
            % (afb_b, sigma_afb),
    ]
    ax.text(0.04, 0.96, "\n".join(lines), transform=ax.transAxes,
            ha="left", va="top", fontsize=14,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="wheat", alpha=0.7),
            linespacing=1.4)

    ax.set_xlabel(r"$|\cos\theta_{\mathrm{thrust}}|$")
    ax.set_ylabel(r"$\langle Q_{\mathrm{FB}} \rangle$")
    ax.set_xlim(-0.02, 0.95)
    ax.legend(loc="lower right", fontsize=13)
    exp_label_data(ax)

    fig.savefig(FIG_DIR / "F_afb_extraction.pdf", bbox_inches="tight")
    fig.savefig(FIG_DIR / "F_afb_extraction.png", bbox_inches="tight", dpi=150)
    plt.close(fig)
    print("Saved F_afb_extraction.pdf")


def plot_afb_signed_diagnostic():
    """Diagnostic figure: <Q_FB> vs signed cos(theta) showing parabolic shape."""

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
    chi2_lin = s["chi2"]
    ndf_lin = s["ndf"]
    slope = s["slope"]
    intercept = s["intercept"]
    n_tagged = s["n_tagged"]

    # Quadratic fit for the diagnostic
    # Load from quadratic results
    with open(P4C_OUT / "afb_quadratic_results.json") as f:
        qr = json.load(f)
    sc = qr["results"]["signed_cos"]
    a_q = sc["quadratic"]["intercept"]
    b_q = sc["quadratic"]["slope"]
    c_q = sc["quadratic"]["cos2_coeff"]
    chi2_quad = sc["quadratic"]["chi2"]
    ndf_quad = sc["quadratic"]["ndf"]

    fig, ax = plt.subplots(figsize=(10, 10))

    ax.errorbar(bin_centers, mean_qfb, yerr=sigma_qfb, fmt="o", color="black",
                markersize=8, capsize=5, linewidth=2, zorder=5,
                label="ALEPH data 1992--1995")

    x_fine = np.linspace(-0.9, 0.9, 200)

    # Linear fit
    y_lin = slope * x_fine + intercept
    ax.plot(x_fine, y_lin, "b--", linewidth=2, zorder=4,
            label=r"Linear ($\chi^2/\mathrm{ndf} = %.0f/%d$)" % (chi2_lin, ndf_lin))

    # Quadratic fit
    y_quad = a_q + b_q * x_fine + c_q * x_fine**2
    ax.plot(x_fine, y_quad, "r-", linewidth=2, zorder=4,
            label=r"Quadratic ($\chi^2/\mathrm{ndf} = %.0f/%d$)" % (chi2_quad, ndf_quad))

    ax.axhline(0, color="gray", linestyle=":", linewidth=1)

    lines = [
        r"$\kappa = 0.3$,  WP $> 5$",
        r"$N_{\mathrm{tagged}}$ = %s" % f"{n_tagged:,}",
        "",
        "Parabolic shape from",
        r"$|\cos\theta|$-dependent $b$-tag purity",
        "(symmetric — cancels in folded extraction)",
    ]
    ax.text(0.04, 0.96, "\n".join(lines), transform=ax.transAxes,
            ha="left", va="top", fontsize=14,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="wheat", alpha=0.7),
            linespacing=1.4)

    ax.set_xlabel(r"$\cos\theta_{\mathrm{thrust}}$")
    ax.set_ylabel(r"$\langle Q_{\mathrm{FB}} \rangle$")
    ax.legend(loc="lower left", fontsize=13)
    exp_label_data(ax)

    fig.savefig(FIG_DIR / "F_afb_signed_diagnostic.pdf", bbox_inches="tight")
    fig.savefig(FIG_DIR / "F_afb_signed_diagnostic.png", bbox_inches="tight", dpi=150)
    plt.close(fig)
    print("Saved F_afb_signed_diagnostic.pdf")


if __name__ == "__main__":
    plot_afb_extraction()
    plot_afb_signed_diagnostic()
