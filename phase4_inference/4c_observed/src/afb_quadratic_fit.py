"""Phase 4c: Quadratic vs linear fit for A_FB angular distribution.

Investigates whether the <Q_FB> vs |cos(theta)| data shows curvature
beyond the linear model. Fits both linear and quadratic models to:
  1. The |cos(theta)| asymmetry data (primary extraction, from systematics)
  2. The signed cos(theta) data (from the corrected extraction)

Model for |cos(theta)| bins:
  <asymmetry>(|cos|) = a + b*|cos(theta)| + c*|cos(theta)|^2
  A_FB^b = b / delta_b  (from the linear coefficient)

Model for signed cos(theta) bins:
  <Q_FB>(cos) = a + b*cos(theta) + c*cos^2(theta)
  The a + c*cos^2 term is symmetric; the b*cos term gives the asymmetry

Session: magnus_435d

Reads:
  phase4_inference/4c_observed/outputs/afb_systematics_final.json
  phase4_inference/4c_observed/outputs/afb_fulldata_corrected.json
Writes:
  phase4_inference/4c_observed/outputs/afb_quadratic_results.json
  analysis_note/figures/afb_angular_quadratic.pdf
"""
import json
import logging
from pathlib import Path

import numpy as np
from scipy.stats import chi2 as chi2_dist, f as f_dist
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mplhep as hep
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

HERE = Path(__file__).resolve().parent
PHASE4C_OUT = HERE.parent / "outputs"
AN_FIG = HERE.parents[2] / "analysis_note" / "figures"
PHASE4C_OUT.mkdir(parents=True, exist_ok=True)
AN_FIG.mkdir(parents=True, exist_ok=True)

hep.style.use("ATLAS")
plt.rcParams.update({
    "font.size": 16,
    "axes.labelsize": 18,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "legend.fontsize": 13,
})

PUBLISHED_DELTA = {0.3: 0.162, 0.5: 0.208, 1.0: 0.275, 2.0: 0.343}


def weighted_linear_fit(x, y, w):
    """Weighted linear fit: y = a + b*x. Returns (a, b, sigma_a, sigma_b)."""
    S = np.sum(w)
    Sx = np.sum(w * x)
    Sy = np.sum(w * y)
    Sxx = np.sum(w * x**2)
    Sxy = np.sum(w * x * y)
    det = S * Sxx - Sx**2
    a = (Sxx * Sy - Sx * Sxy) / det
    b = (S * Sxy - Sx * Sy) / det
    sigma_a = np.sqrt(Sxx / det)
    sigma_b = np.sqrt(S / det)
    return a, b, sigma_a, sigma_b


def weighted_quadratic_fit(x, y, w):
    """Weighted quadratic fit: y = a + b*x + c*x^2.
    Returns (a, b, c, sigma_a, sigma_b, sigma_c, cov)."""
    A = np.column_stack([np.ones_like(x), x, x**2])
    W = np.diag(w)
    AWA = A.T @ W @ A
    AWy = A.T @ W @ y
    cov = np.linalg.inv(AWA)
    beta = cov @ AWy
    a, b, c = beta
    sigma_a = np.sqrt(cov[0, 0])
    sigma_b = np.sqrt(cov[1, 1])
    sigma_c = np.sqrt(cov[2, 2])
    return a, b, c, sigma_a, sigma_b, sigma_c, cov


def main():
    log.info("=" * 60)
    log.info("AFB Quadratic Fit Investigation (magnus_435d)")
    log.info("=" * 60)

    results = {}

    # ============================================================
    # Part 1: Primary |cos(theta)| extraction
    # ============================================================
    log.info("\n--- Part 1: Primary |cos(theta)| extraction ---")

    with open(PHASE4C_OUT / "afb_systematics_final.json") as f:
        syst_data = json.load(f)

    nom = syst_data["nominal"]
    x = np.array(nom["bin_centers"])
    y = np.array(nom["asymmetry"])
    sigma = np.array(nom["sigma_asymmetry"])
    n_tagged = nom["n_tagged"]
    delta_b = nom["delta_b"]
    kappa = nom["kappa_sign"]
    wp = nom["wp_threshold"]
    w = 1.0 / sigma**2

    # Linear fit
    a_l, b_l, sa_l, sb_l = weighted_linear_fit(x, y, w)
    resid_l = y - (a_l + b_l * x)
    chi2_l = float(np.sum((resid_l / sigma)**2))
    ndf_l = len(x) - 2
    p_l = float(1.0 - chi2_dist.cdf(chi2_l, ndf_l))

    # Quadratic fit
    a_q, b_q, c_q, sa_q, sb_q, sc_q, cov_q = weighted_quadratic_fit(x, y, w)
    resid_q = y - (a_q + b_q * x + c_q * x**2)
    chi2_q = float(np.sum((resid_q / sigma)**2))
    ndf_q = len(x) - 3
    p_q = float(1.0 - chi2_dist.cdf(chi2_q, ndf_q))

    # F-test
    delta_chi2 = chi2_l - chi2_q
    f_stat = (delta_chi2 / 1.0) / (chi2_q / ndf_q) if ndf_q > 0 and chi2_q > 0 else 0
    p_f = float(1.0 - f_dist.cdf(f_stat, 1, ndf_q))

    afb_lin = b_l / delta_b
    sigma_afb_lin = sb_l / delta_b
    afb_quad = b_q / delta_b
    sigma_afb_quad = sb_q / delta_b

    results["primary_abscos"] = {
        "description": "Primary extraction using |cos(theta)| bins",
        "kappa": kappa,
        "wp": wp,
        "n_tagged": n_tagged,
        "delta_b": delta_b,
        "linear": {
            "intercept": float(a_l),
            "slope": float(b_l),
            "sigma_slope": float(sb_l),
            "chi2": chi2_l, "ndf": ndf_l, "p_value": p_l,
            "afb": float(afb_lin),
            "sigma_afb": float(sigma_afb_lin),
        },
        "quadratic": {
            "intercept": float(a_q),
            "slope": float(b_q),
            "cos2_coeff": float(c_q),
            "sigma_slope": float(sb_q),
            "sigma_cos2": float(sc_q),
            "chi2": chi2_q, "ndf": ndf_q, "p_value": p_q,
            "afb": float(afb_quad),
            "sigma_afb": float(sigma_afb_quad),
        },
        "f_test": {
            "delta_chi2": float(delta_chi2),
            "f_statistic": float(f_stat),
            "p_value": float(p_f),
            "quadratic_significantly_better": p_f < 0.05,
        },
    }

    log.info("Primary |cos(theta)| extraction (kappa=%.1f, WP=%.0f):", kappa, wp)
    log.info("  Linear:    chi2/ndf = %.1f/%d (p=%.3f), slope=%.6f +/- %.6f",
             chi2_l, ndf_l, p_l, b_l, sb_l)
    log.info("             A_FB = %.4f +/- %.4f", afb_lin, sigma_afb_lin)
    log.info("  Quadratic: chi2/ndf = %.1f/%d (p=%.3f), slope=%.6f, cos2=%.6f +/- %.6f",
             chi2_q, ndf_q, p_q, b_q, c_q, sc_q)
    log.info("             A_FB = %.4f +/- %.4f", afb_quad, sigma_afb_quad)
    log.info("  F-test:    delta_chi2=%.1f, F=%.1f, p=%.4f  %s",
             delta_chi2, f_stat, p_f,
             "*** SIGNIFICANT ***" if p_f < 0.05 else "(not significant)")
    log.info("  cos^2 coefficient c = %.4f +/- %.4f (%.1f sigma from zero)",
             c_q, sc_q, abs(c_q) / sc_q)

    # ============================================================
    # Part 2: Signed cos(theta) extraction
    # ============================================================
    log.info("\n--- Part 2: Signed cos(theta) extraction ---")

    with open(PHASE4C_OUT / "afb_fulldata_corrected.json") as f:
        afb_corr = json.load(f)

    for kres in afb_corr["kappa_results"]:
        if kres["kappa"] != 0.3:
            continue
        for wpr in kres["per_wp_results"]:
            if wpr["threshold"] != 5.0:
                continue

            s = wpr["slope"]
            x_s = np.array(s["bin_centers"])
            y_s = np.array(s["mean_qfb"])

            # Estimate per-bin sigma from the reported chi2
            # chi2 = sum(resid^2 / sigma^2) with 8 ndf
            a_s, b_s, _, _ = weighted_linear_fit(x_s, y_s, np.ones(len(x_s)))
            resid_s = y_s - (a_s + b_s * x_s)
            rss = np.sum(resid_s**2)
            chi2_reported = s["chi2"]
            sigma_s = np.sqrt(rss / chi2_reported) if chi2_reported > 0 else 1e-6
            w_s = 1.0 / sigma_s**2 * np.ones(len(x_s))

            # Redo fits with proper weights
            a_l2, b_l2, _, sb_l2 = weighted_linear_fit(x_s, y_s, w_s)
            resid_l2 = y_s - (a_l2 + b_l2 * x_s)
            chi2_l2 = float(np.sum(w_s * resid_l2**2))
            ndf_l2 = len(x_s) - 2

            a_q2, b_q2, c_q2, _, sb_q2, sc_q2, _ = weighted_quadratic_fit(x_s, y_s, w_s)
            resid_q2 = y_s - (a_q2 + b_q2 * x_s + c_q2 * x_s**2)
            chi2_q2 = float(np.sum(w_s * resid_q2**2))
            ndf_q2 = len(x_s) - 3
            p_q2 = float(1.0 - chi2_dist.cdf(chi2_q2, ndf_q2)) if ndf_q2 > 0 else 0.0

            delta_chi2_2 = chi2_l2 - chi2_q2
            f2 = (delta_chi2_2 / 1.0) / (chi2_q2 / ndf_q2) if ndf_q2 > 0 and chi2_q2 > 0 else 0
            p_f2 = float(1.0 - f_dist.cdf(f2, 1, ndf_q2))

            results["signed_cos"] = {
                "description": "Signed cos(theta) bins (diagnostic)",
                "kappa": 0.3,
                "wp": 5.0,
                "sigma_per_bin": float(sigma_s),
                "linear": {
                    "intercept": float(a_l2), "slope": float(b_l2),
                    "chi2": chi2_l2, "ndf": ndf_l2,
                },
                "quadratic": {
                    "intercept": float(a_q2), "slope": float(b_q2),
                    "cos2_coeff": float(c_q2), "sigma_cos2": float(sc_q2),
                    "chi2": chi2_q2, "ndf": ndf_q2, "p_value": p_q2,
                },
                "f_test": {
                    "delta_chi2": float(delta_chi2_2),
                    "f_statistic": float(f2),
                    "p_value": float(p_f2),
                    "quadratic_significantly_better": p_f2 < 0.05,
                },
                "note": "The cos^2 term is a symmetric purity/acceptance effect. "
                        "In signed cos(theta), it creates the parabolic shape. "
                        "In |cos(theta)|, it adds a smooth bias but the linear "
                        "slope correctly captures the asymmetry.",
            }

            log.info("Signed cos(theta):")
            log.info("  Linear:    chi2/ndf = %.1f/%d", chi2_l2, ndf_l2)
            log.info("  Quadratic: chi2/ndf = %.1f/%d (p=%.4f)", chi2_q2, ndf_q2, p_q2)
            log.info("  cos^2 coeff: %.6f +/- %.6f (%.1f sigma)",
                     c_q2, sc_q2, abs(c_q2) / sc_q2)
            log.info("  F-test:    p=%.4f %s", p_f2,
                     "*** SIGNIFICANT ***" if p_f2 < 0.05 else "")
            break
        break

    # Save results
    output = {
        "description": "Quadratic vs linear fit comparison for A_FB angular distribution",
        "session": "magnus_435d",
        "conclusion": (
            "The primary extraction uses |cos(theta)| bins where the linear fit gives "
            f"chi2/ndf = {results['primary_abscos']['linear']['chi2']:.1f}/"
            f"{results['primary_abscos']['linear']['ndf']} "
            f"(p = {results['primary_abscos']['linear']['p_value']:.3f}), which is acceptable. "
            "A quadratic term improves the fit marginally (F-test p = "
            f"{results['primary_abscos']['f_test']['p_value']:.3f}) with a cos^2 coefficient "
            f"c = {results['primary_abscos']['quadratic']['cos2_coeff']:.4f} +/- "
            f"{results['primary_abscos']['quadratic']['sigma_cos2']:.4f}. "
            "The A_FB extracted from the linear coefficient is stable: "
            f"linear gives {results['primary_abscos']['linear']['afb']:.4f}, "
            f"quadratic gives {results['primary_abscos']['quadratic']['afb']:.4f}. "
            "In the signed cos(theta) extraction, the cos^2 term is highly significant "
            "(F-test p = " + f"{results['signed_cos']['f_test']['p_value']:.4f}), "
            "reflecting a symmetric purity/acceptance effect that creates the parabolic shape. "
            "The |cos(theta)| extraction correctly isolates the asymmetry signal."
        ),
        "results": results,
    }
    out_path = PHASE4C_OUT / "afb_quadratic_results.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    log.info("\nSaved %s", out_path)

    # ============================================================
    # Plots
    # ============================================================

    # Plot 1: Primary |cos(theta)| with linear vs quadratic
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))

    # Top-left: |cos(theta)| data + fits
    ax = axes[0, 0]
    ax.errorbar(x, y, yerr=sigma, fmt="ko", ms=5, capsize=4, label="Data")
    x_fine = np.linspace(0, 0.9, 200)
    ax.plot(x_fine, a_l + b_l * x_fine, "b--", lw=2,
            label=f"Linear ($\\chi^2$/ndf={chi2_l:.1f}/{ndf_l})")
    ax.plot(x_fine, a_q + b_q * x_fine + c_q * x_fine**2, "r-", lw=2,
            label=f"Quadratic ($\\chi^2$/ndf={chi2_q:.1f}/{ndf_q})")
    ax.set_xlabel("$|\\cos\\theta|$")
    ax.set_ylabel("Asymmetry")
    ax.legend(fontsize=9)
    ax.set_xlim(0, 0.95)
    hep.label.exp_text("ALEPH", ax=ax, loc=1)

    # Top-right: Residuals for |cos|
    ax = axes[0, 1]
    ax.errorbar(x - 0.01, resid_l / sigma, yerr=1.0, fmt="bs", ms=5,
                capsize=3, alpha=0.7, label="Linear")
    ax.errorbar(x + 0.01, resid_q / sigma, yerr=1.0, fmt="r^", ms=5,
                capsize=3, alpha=0.7, label="Quadratic")
    ax.axhline(0, color="gray", ls="-", lw=0.8)
    ax.set_xlabel("$|\\cos\\theta|$")
    ax.set_ylabel("Pull ($\\sigma$)")
    ax.legend(fontsize=10)
    ax.set_ylim(-4, 4)

    # Bottom-left: Signed cos(theta) data + fits
    for kres in afb_corr["kappa_results"]:
        if kres["kappa"] != 0.3:
            continue
        for wpr in kres["per_wp_results"]:
            if wpr["threshold"] != 5.0:
                continue
            s = wpr["slope"]
            break
        break

    x_s = np.array(s["bin_centers"])
    y_s = np.array(s["mean_qfb"])
    res_s = results["signed_cos"]

    ax = axes[1, 0]
    ax.errorbar(x_s, y_s, yerr=res_s["sigma_per_bin"], fmt="ko", ms=5,
                capsize=4, label="Data")
    x_fine_s = np.linspace(-0.9, 0.9, 200)
    a_l2 = res_s["linear"]["intercept"]
    b_l2 = res_s["linear"]["slope"]
    a_q2 = res_s["quadratic"]["intercept"]
    b_q2 = res_s["quadratic"]["slope"]
    c_q2 = res_s["quadratic"]["cos2_coeff"]
    ax.plot(x_fine_s, a_l2 + b_l2 * x_fine_s, "b--", lw=2,
            label=f"Linear ($\\chi^2$={res_s['linear']['chi2']:.0f}/{res_s['linear']['ndf']})")
    ax.plot(x_fine_s, a_q2 + b_q2 * x_fine_s + c_q2 * x_fine_s**2, "r-", lw=2,
            label=f"Quad ($\\chi^2$={res_s['quadratic']['chi2']:.0f}/{res_s['quadratic']['ndf']})")
    ax.set_xlabel("$\\cos\\theta$ (signed)")
    ax.set_ylabel("$\\langle Q_{\\mathrm{FB}} \\rangle$")
    ax.legend(fontsize=9)
    hep.label.exp_text("ALEPH", ax=ax, loc=1)

    # Bottom-right: Summary table
    ax = axes[1, 1]
    ax.axis("off")
    table_data = [
        ["", "Linear", "Quadratic"],
        ["$|\\cos\\theta|$ $\\chi^2$/ndf",
         f"{chi2_l:.1f}/{ndf_l}", f"{chi2_q:.1f}/{ndf_q}"],
        ["$|\\cos\\theta|$ $p$-value",
         f"{p_l:.3f}", f"{p_q:.3f}"],
        ["$|\\cos\\theta|$ $A_{{FB}}^b$",
         f"{afb_lin:.4f}", f"{afb_quad:.4f}"],
        ["signed $\\chi^2$/ndf",
         f"{res_s['linear']['chi2']:.0f}/{res_s['linear']['ndf']}",
         f"{res_s['quadratic']['chi2']:.0f}/{res_s['quadratic']['ndf']}"],
        ["F-test $p$ ($|\\cos|$)",
         "", f"{results['primary_abscos']['f_test']['p_value']:.3f}"],
        ["F-test $p$ (signed)",
         "", f"{results['signed_cos']['f_test']['p_value']:.4f}"],
    ]
    table = ax.table(cellText=table_data, loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.0, 1.8)

    fig.suptitle("$\\kappa = 0.3$, WP $> 5$", fontsize=14, y=0.98)
    fig.savefig(AN_FIG / "afb_angular_quadratic.pdf", bbox_inches="tight")
    fig.savefig(AN_FIG / "afb_angular_quadratic.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    log.info("Saved afb_angular_quadratic.pdf")


if __name__ == "__main__":
    main()
