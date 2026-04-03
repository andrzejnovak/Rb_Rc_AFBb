"""Phase 4b REGRESSION: Publication-quality plots for 10% data results.

All figures: figsize=(10,10), mplhep ATLAS style, no titles.

Produces:
- rb_3tag_stability_10pct.pdf — R_b across threshold configs
- afb_kappa_10pct.pdf — A_FB^b across kappa values
- afb_qfb_vs_costheta_10pct.pdf — <Q_FB> vs cos(theta) at best kappa/WP
- systematics_breakdown_10pct.pdf — systematic uncertainty breakdown
- rb_comparison_mc_data.pdf — MC expected vs 10% data R_b

Reads: phase4_inference/4b_partial/outputs/*.json
Writes: phase4_inference/4b_partial/outputs/figures/*.pdf
"""
import json
import logging
from pathlib import Path

import numpy as np
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
PHASE4B_OUT = HERE.parent / "outputs"
FIG_DIR = PHASE4B_OUT / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Style
hep.style.use("ATLAS")
plt.rcParams.update({
    "font.size": 16,
    "axes.labelsize": 18,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "legend.fontsize": 13,
})

R_B_SM = 0.21578
AFB_B_OBS = 0.0995
SIN2_THETA_SM = 0.23153


def save_and_register(fig, name, registry):
    """Save figure and add to registry."""
    path = FIG_DIR / name
    fig.savefig(path, dpi=150, bbox_inches="tight")
    fig.savefig(path.with_suffix(".png"), dpi=150, bbox_inches="tight")
    plt.close(fig)
    registry.append({
        "filename": str(path.relative_to(PHASE4B_OUT)),
        "description": name.replace("_", " ").replace(".pdf", ""),
    })
    log.info("Saved %s", name)


def main():
    log.info("=" * 60)
    log.info("Phase 4b REGRESSION: Plotting (10%% data)")
    log.info("=" * 60)

    with open(PHASE4B_OUT / "three_tag_rb_10pct.json") as f:
        rb_data = json.load(f)
    with open(PHASE4B_OUT / "purity_afb_10pct.json") as f:
        afb_data = json.load(f)
    with open(PHASE4B_OUT / "systematics_10pct_v2.json") as f:
        syst_data = json.load(f)

    registry = []

    # ================================================================
    # 1. R_b stability across threshold configurations
    # ================================================================
    log.info("\n--- Plot: R_b stability ---")
    fig, ax = plt.subplots(figsize=(10, 10))

    valid = [r for r in rb_data["all_results"]
             if r.get("sigma_stat") and r["sigma_stat"] > 0
             and 0.05 < r["R_b"] < 0.50]

    if valid:
        labels = [r["label"] for r in valid]
        rb_vals = [r["R_b"] for r in valid]
        rb_errs = [r["sigma_stat"] for r in valid]
        x = np.arange(len(labels))

        ax.errorbar(x, rb_vals, yerr=rb_errs, fmt="ko", markersize=8,
                     capsize=5, linewidth=2, label="10% data (3-tag)")
        ax.axhline(R_B_SM, color="red", linestyle="--", linewidth=1.5,
                    label="$R_b^{\\mathrm{SM}}$ = %.5f" % R_B_SM)

        # Combined value
        comb = rb_data["stability"]
        if comb.get("R_b_combined") is not None:
            ax.axhline(comb["R_b_combined"], color="blue", linestyle="-.",
                        linewidth=1.5, alpha=0.7,
                        label="Combined = %.5f" % comb["R_b_combined"])
            ax.axhspan(comb["R_b_combined"] - comb["sigma_combined"],
                        comb["R_b_combined"] + comb["sigma_combined"],
                        alpha=0.15, color="blue")

        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=11)
        ax.set_ylabel("$R_b$")
        ax.set_xlabel("Threshold configuration")
        ax.legend(loc="upper right")
        hep.atlas.label(ax=ax, data=True, lumi="ALEPH 10%", loc=0)

    save_and_register(fig, "rb_3tag_stability_10pct.pdf", registry)

    # ================================================================
    # 2. A_FB^b across kappa values
    # ================================================================
    log.info("\n--- Plot: A_FB^b vs kappa ---")
    fig, ax = plt.subplots(figsize=(10, 10))

    kappas = []
    afb_vals = []
    afb_errs = []
    for kr in afb_data["kappa_results"]:
        comb = kr["combination"]
        if comb.get("A_FB_b") is not None and comb.get("sigma_A_FB_b", 0) > 0:
            kappas.append(kr["kappa"])
            afb_vals.append(comb["A_FB_b"])
            afb_errs.append(comb["sigma_A_FB_b"])

    if kappas:
        x = np.arange(len(kappas))
        ax.errorbar(x, afb_vals, yerr=afb_errs, fmt="ko", markersize=8,
                     capsize=5, linewidth=2, label="10% data")
        ax.axhline(AFB_B_OBS, color="red", linestyle="--", linewidth=1.5,
                    label="$A_{\\mathrm{FB}}^{b,\\mathrm{LEP}}$ = %.4f" % AFB_B_OBS)

        comb_afb = afb_data["combination"]
        if comb_afb.get("A_FB_b") is not None:
            ax.axhline(comb_afb["A_FB_b"], color="blue", linestyle="-.",
                        linewidth=1.5, alpha=0.7,
                        label="Combined = %.4f" % comb_afb["A_FB_b"])

        ax.set_xticks(x)
        ax.set_xticklabels(["$\\kappa$ = %.1f" % k for k in kappas], fontsize=14)
        ax.set_ylabel("$A_{\\mathrm{FB}}^b$")
        ax.set_xlabel("Jet charge exponent $\\kappa$")
        ax.legend(loc="best")
        hep.atlas.label(ax=ax, data=True, lumi="ALEPH 10%", loc=0)

    save_and_register(fig, "afb_kappa_10pct.pdf", registry)

    # ================================================================
    # 3. <Q_FB> vs cos(theta) at best kappa/WP
    # ================================================================
    log.info("\n--- Plot: <Q_FB> vs cos(theta) ---")
    fig, ax = plt.subplots(figsize=(10, 10))

    # Use kappa=0.5 as representative
    best_kappa = None
    for kr in afb_data["kappa_results"]:
        if abs(kr["kappa"] - 0.5) < 0.01:
            best_kappa = kr
            break
    if best_kappa is None and afb_data["kappa_results"]:
        best_kappa = afb_data["kappa_results"][0]

    if best_kappa and best_kappa.get("per_wp_results"):
        # Pick lowest sigma WP
        best_wp = min(best_kappa["per_wp_results"],
                      key=lambda r: r["extraction"]["sigma_afb_purity"])
        slope_info = best_wp["slope"]
        centers = np.array(slope_info["bin_centers"])
        means = np.array([v if v is not None else np.nan
                          for v in slope_info["mean_qfb"]])
        sigmas = np.array([v if v is not None else np.nan
                           for v in slope_info["sigma_qfb"]])
        ok = ~np.isnan(means) & ~np.isnan(sigmas) & (sigmas > 0)

        if np.sum(ok) > 0:
            ax.errorbar(centers[ok], means[ok], yerr=sigmas[ok],
                         fmt="ko", markersize=6, capsize=4, linewidth=2,
                         label="10% data")

            # Fit line
            x_fit = np.linspace(-0.9, 0.9, 100)
            y_fit = slope_info["intercept"] + slope_info["slope"] * x_fit
            ax.plot(x_fit, y_fit, "r-", linewidth=2,
                     label="Fit: slope = %.4f $\\pm$ %.4f" % (
                         slope_info["slope"], slope_info["sigma_slope"]))

            ax.axhline(0, color="gray", linestyle=":", linewidth=1)
            ax.set_xlabel("$\\cos\\theta_{\\mathrm{thrust}}$")
            ax.set_ylabel("$\\langle Q_{\\mathrm{FB}} \\rangle$")
            ax.legend(loc="best")
            text = "$\\kappa$ = %.1f, WP = %.1f" % (
                best_kappa["kappa"], best_wp["threshold"])
            ax.text(0.05, 0.95, text, transform=ax.transAxes,
                    fontsize=14, va="top")
            hep.atlas.label(ax=ax, data=True, lumi="ALEPH 10%", loc=0)

    save_and_register(fig, "afb_qfb_vs_costheta_10pct.pdf", registry)

    # ================================================================
    # 4. Systematic breakdown
    # ================================================================
    log.info("\n--- Plot: Systematic breakdown ---")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 10))

    # R_b systematics
    rb_syst = syst_data["rb_systematics"]
    names_rb = sorted(rb_syst.keys(), key=lambda k: -rb_syst[k]["delta_Rb"])
    vals_rb = [rb_syst[k]["delta_Rb"] for k in names_rb]
    y_rb = np.arange(len(names_rb))

    ax1.barh(y_rb, vals_rb, color="steelblue", height=0.6)
    ax1.set_yticks(y_rb)
    ax1.set_yticklabels([n.replace("_", " ") for n in names_rb], fontsize=10)
    ax1.set_xlabel("$\\Delta R_b$")
    ax1.axvline(float(syst_data["rb_total"]["syst"]), color="red",
                 linestyle="--", label="Total syst")
    ax1.axvline(float(syst_data["rb_total"]["stat"]), color="green",
                 linestyle=":", label="Stat")
    ax1.legend(loc="lower right", fontsize=10)
    ax1.invert_yaxis()

    # A_FB systematics
    afb_syst = syst_data["afb_systematics"]
    names_afb = sorted(afb_syst.keys(), key=lambda k: -afb_syst[k]["delta_AFB"])
    vals_afb = [afb_syst[k]["delta_AFB"] for k in names_afb]
    y_afb = np.arange(len(names_afb))

    ax2.barh(y_afb, vals_afb, color="darkorange", height=0.6)
    ax2.set_yticks(y_afb)
    ax2.set_yticklabels([n.replace("_", " ") for n in names_afb], fontsize=10)
    ax2.set_xlabel("$\\Delta A_{\\mathrm{FB}}^b$")
    ax2.axvline(float(syst_data["afb_total"]["syst"]), color="red",
                 linestyle="--", label="Total syst")
    ax2.axvline(float(syst_data["afb_total"]["stat"]), color="green",
                 linestyle=":", label="Stat")
    ax2.legend(loc="lower right", fontsize=10)
    ax2.invert_yaxis()

    fig.subplots_adjust(wspace=0.6)
    save_and_register(fig, "systematics_breakdown_10pct.pdf", registry)

    # ================================================================
    # 5. MC vs Data R_b comparison
    # ================================================================
    log.info("\n--- Plot: MC vs Data R_b ---")
    fig, ax = plt.subplots(figsize=(10, 10))

    comp = rb_data.get("comparison_4a", {})
    items = []
    labels_comp = []

    if comp.get("mc_R_b") is not None:
        items.append((comp["mc_R_b"], comp.get("mc_sigma", 0)))
        labels_comp.append("MC expected (4a)")
    if comp.get("data_R_b") is not None:
        items.append((comp["data_R_b"], comp.get("data_sigma", 0)))
        labels_comp.append("10% data (4b)")

    if items:
        x = np.arange(len(items))
        vals_c = [it[0] for it in items]
        errs_c = [it[1] for it in items]
        ax.errorbar(x, vals_c, yerr=errs_c, fmt="ko", markersize=10,
                     capsize=6, linewidth=2)
        ax.axhline(R_B_SM, color="red", linestyle="--", linewidth=1.5,
                    label="$R_b^{\\mathrm{SM}}$ = %.5f" % R_B_SM)
        ax.set_xticks(x)
        ax.set_xticklabels(labels_comp, fontsize=14)
        ax.set_ylabel("$R_b$")
        ax.legend(loc="best")

        if comp.get("pull") is not None:
            ax.text(0.95, 0.05,
                    "Pull (data $-$ MC) = %.2f$\\sigma$" % comp["pull"],
                    transform=ax.transAxes, ha="right", fontsize=14)
        hep.atlas.label(ax=ax, data=True, lumi="ALEPH 10%", loc=0)

    save_and_register(fig, "rb_comparison_mc_data.pdf", registry)

    # ================================================================
    # Write FIGURES.json
    # ================================================================
    with open(PHASE4B_OUT / "FIGURES.json", "w") as f:
        json.dump(registry, f, indent=2)
    log.info("\nSaved FIGURES.json with %d figures", len(registry))


if __name__ == "__main__":
    main()
