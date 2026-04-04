"""Phase 4c: Publication-quality figures for full-data results.

Produces:
1. R_b stability across working points
2. A_FB^b vs kappa (inclusive method)
3. Systematic breakdown (R_b and A_FB)
4. Per-year consistency
5. Calibration progression (10% vs full)
6. BDT cross-check comparison

All figures: figsize=(10,10), mplhep CMS style with ALEPH label, no set_title.

FIX (kenji_2b8e): Replaced ATLAS labels with ALEPH, removed absolute
fontsizes, replaced tight_layout with bbox_inches="tight", uses
save_and_register from plot_utils, publication-style systematic names.
"""
import json
import logging
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mplhep as mh
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

HERE = Path(__file__).resolve().parent
PHASE4C_OUT = HERE.parent / "outputs"
FIG_DIR = PHASE4C_OUT / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

P4B_OUT = HERE.parents[1] / "4b_partial" / "outputs"

# Import plot_utils from phase3 for exp_label and mpl_magic
sys.path.insert(0, str(HERE.parents[2] / "phase3_selection" / "src"))
from plot_utils import exp_label_data

SCRIPT_PATH = Path(__file__).resolve()


def save_and_register(fig, filename, script_path, description,
                      fig_type, lower_panel="none", is_2d=False,
                      observable_type="count"):
    """Save figure to Phase 4c outputs and register in FIGURES.json.

    Local wrapper that writes to phase4c outputs instead of phase3.
    """
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc).isoformat()
    script_file = Path(script_path)
    if script_file.exists():
        script_mtime = datetime.fromtimestamp(
            script_file.stat().st_mtime, tz=timezone.utc
        ).isoformat()
    else:
        script_mtime = now

    fig.savefig(FIG_DIR / filename, bbox_inches="tight", dpi=200,
                transparent=True)
    pdf_name = filename.replace(".png", ".pdf")
    fig.savefig(FIG_DIR / pdf_name, bbox_inches="tight", dpi=200,
                transparent=True)
    plt.close(fig)

    registry_path = PHASE4C_OUT / "FIGURES.json"
    if registry_path.exists():
        with open(registry_path) as f:
            registry = json.load(f)
    else:
        registry = []

    registry = [e for e in registry if e["filename"] != filename]
    registry.append({
        "filename": filename,
        "type": fig_type,
        "script": str(script_path),
        "description": description,
        "lower_panel": lower_panel,
        "is_2d": is_2d,
        "created": now,
        "script_mtime": script_mtime,
        "observable_type": observable_type,
    })
    with open(registry_path, "w") as f:
        json.dump(registry, f, indent=2)

    log.info("Saved %s", filename)

R_B_SM = 0.21578
R_C_SM = 0.17223
AFB_B_SM = 0.1031
AFB_B_OBS = 0.0995

mh.style.use("CMS")

# Publication-style systematic name mapping
SYST_LABELS = {
    "tag_efficiency": r"Tag efficiency",
    "charm_contamination": r"Charm contamination",
    "light_contamination": r"Light quark contamination",
    "gluon_splitting_bb": r"$g \to b\bar{b}$",
    "gluon_splitting_cc": r"$g \to c\bar{c}$",
    "mc_statistics": "MC statistics",
    "hemisphere_correlation": "Hemisphere correlation",
    "mc_modelling": "MC modelling",
    "qcd_correction": "QCD correction",
    "delta_b_published": r"$\delta_b$ (published)",
    "delta_c_published": r"$\delta_c$ (published)",
    "sf_calibration": "Scale factor calibration",
    "afb_c_input": r"$A_{FB}^c$ input",
}


def _label(name):
    """Convert code-style systematic name to publication label."""
    return SYST_LABELS.get(name, name.replace("_", " "))


def plot_rb_stability():
    """Plot R_b across working point configurations."""
    with open(PHASE4C_OUT / "three_tag_rb_fulldata.json") as f:
        data = json.load(f)

    results = data["all_results"]
    valid = [r for r in results
             if r.get("sigma_stat") and r["sigma_stat"] > 0
             and 0.05 < r["R_b_sf"] < 0.50]

    if not valid:
        log.warning("No valid R_b results for stability plot")
        return

    fig, ax = plt.subplots(figsize=(10, 10))

    labels = [r["label"] for r in valid]
    rbs = [r["R_b_sf"] for r in valid]
    errs = [r["sigma_stat"] for r in valid]
    x = np.arange(len(valid))

    ax.errorbar(x, rbs, yerr=errs, fmt="o", color="C0", markersize=8,
                capsize=5, linewidth=2, label="SF-calibrated")

    rbs_raw = [r["R_b_raw"] for r in valid]
    ax.scatter(x + 0.15, rbs_raw, marker="s", color="C3", s=50,
               zorder=5, label="Raw MC calibration")

    stab = data["stability"]
    if stab["R_b_combined"] is not None:
        ax.axhline(stab["R_b_combined"], color="C0", linestyle="-.",
                    linewidth=1.5, alpha=0.7,
                    label=r"Combined $R_b$ = %.4f" % stab["R_b_combined"])
        if stab["sigma_combined"]:
            ax.axhspan(stab["R_b_combined"] - stab["sigma_combined"],
                       stab["R_b_combined"] + stab["sigma_combined"],
                       color="C0", alpha=0.10)

    ax.axhline(R_B_SM, color="red", linestyle="--", linewidth=1.5,
                label=r"$R_b^{\rm SM}$ = %.5f" % R_B_SM)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_ylabel(r"$R_b$")
    ax.set_xlabel("Working point")
    ax.legend(loc="upper left", fontsize="x-small")
    exp_label_data(ax)

    save_and_register(
        fig, "rb_3tag_stability_fulldata.png", str(SCRIPT_PATH),
        "R_b across 8 working point configurations (SF-calibrated, full data)",
        "result", lower_panel="none", observable_type="derived",
    )
    log.info("Saved rb_3tag_stability_fulldata")


def plot_afb_kappa():
    """Plot A_FB^b across kappa values (inclusive method)."""
    with open(PHASE4C_OUT / "afb_fulldata.json") as f:
        data = json.load(f)

    kappas = []
    afbs = []
    errs = []

    for kr in data["kappa_results"]:
        comb = kr["combination_inclusive"]
        if comb["A_FB_b"] is not None and comb["sigma_A_FB_b"] is not None:
            kappas.append(kr["kappa"])
            afbs.append(comb["A_FB_b"])
            errs.append(comb["sigma_A_FB_b"])

    if not kappas:
        log.warning("No valid AFB results for kappa plot")
        return

    fig, ax = plt.subplots(figsize=(10, 10))

    ax.errorbar(kappas, afbs, yerr=errs, fmt="o", color="C0", markersize=10,
                capsize=6, linewidth=2, label="Full data (inclusive)")

    comb = data["combination"]
    if comb["A_FB_b"] is not None:
        ax.axhline(comb["A_FB_b"], color="C0", linestyle="-.",
                    linewidth=1.5, alpha=0.7,
                    label=r"Combined $A_{FB}^b$ = %.4f" % comb["A_FB_b"])

    ax.axhline(AFB_B_OBS, color="red", linestyle="--", linewidth=1.5,
                label=r"LEP combined = %.4f" % AFB_B_OBS)
    ax.axhline(0, color="gray", linestyle=":", linewidth=1)

    ax.set_xlabel(r"$\kappa$")
    ax.set_ylabel(r"$A_{FB}^b$")
    ax.legend(fontsize="x-small")
    exp_label_data(ax)

    save_and_register(
        fig, "afb_kappa_fulldata.png", str(SCRIPT_PATH),
        "A_FB^b across kappa values, inclusive method (full data)",
        "result", lower_panel="none", observable_type="derived",
    )
    log.info("Saved afb_kappa_fulldata")


def plot_systematics_breakdown():
    """Plot systematic breakdown for R_b and A_FB."""
    with open(PHASE4C_OUT / "systematics_fulldata.json") as f:
        data = json.load(f)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 10))

    # R_b systematics
    rb_syst = data["rb_systematics"]
    rb_items = sorted(rb_syst.items(), key=lambda x: -x[1]["delta_Rb"])
    names_rb = [_label(item[0]) for item in rb_items]
    vals_rb = [item[1]["delta_Rb"] for item in rb_items]

    colors_rb = []
    for item in rb_items:
        cat = item[1].get("category", "other")
        if "efficiency" in cat:
            colors_rb.append("C0")
        elif "background" in cat or "contamination" in cat:
            colors_rb.append("C1")
        elif "composition" in cat:
            colors_rb.append("C2")
        elif "mc_model" in cat:
            colors_rb.append("C3")
        else:
            colors_rb.append("C4")

    y = np.arange(len(names_rb))
    ax1.barh(y, vals_rb, color=colors_rb, height=0.6)
    ax1.set_yticks(y)
    ax1.set_yticklabels(names_rb, fontsize="x-small")
    ax1.set_xlabel(r"$\delta R_b$")
    ax1.invert_yaxis()

    total_syst = data["rb_summary"]["syst"]
    ax1.axvline(total_syst, color="red", linestyle="--",
                 label=r"Total syst = %.4f" % total_syst)
    ax1.legend(fontsize="x-small")

    # A_FB systematics
    afb_syst = data["afb_systematics"]
    afb_items = sorted(afb_syst.items(), key=lambda x: -x[1]["delta_AFB"])
    names_afb = [_label(item[0]) for item in afb_items]
    vals_afb = [item[1]["delta_AFB"] for item in afb_items]

    y2 = np.arange(len(names_afb))
    ax2.barh(y2, vals_afb, color="C5", height=0.6)
    ax2.set_yticks(y2)
    ax2.set_yticklabels(names_afb, fontsize="x-small")
    ax2.set_xlabel(r"$\delta A_{FB}^b$")
    ax2.invert_yaxis()

    total_syst_afb = data["afb_summary"]["syst"]
    ax2.axvline(total_syst_afb, color="red", linestyle="--",
                 label=r"Total syst = %.4f" % total_syst_afb)
    ax2.legend(fontsize="x-small")

    exp_label_data(ax1)

    save_and_register(
        fig, "systematics_breakdown_fulldata.png", str(SCRIPT_PATH),
        "Systematic uncertainty breakdown for R_b and A_FB^b (full data)",
        "systematic_impact", lower_panel="none", observable_type="derived",
    )
    log.info("Saved systematics_breakdown_fulldata")


def plot_per_year():
    """Plot per-year R_b and A_FB consistency."""
    path = PHASE4C_OUT / "per_year_results.json"
    if not path.exists():
        log.warning("per_year_results.json not found")
        return

    with open(path) as f:
        data = json.load(f)

    per_year = data["per_year"]
    years = [r["year"] for r in per_year]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

    # R_b per year
    rb_vals = [r["R_b_sf"] for r in per_year]
    rb_errs = [r.get("sigma_stat_rb") or 0 for r in per_year]
    ax1.errorbar(years, rb_vals, yerr=rb_errs, fmt="o", color="C0",
                  markersize=10, capsize=6, linewidth=2)
    ax1.axhline(R_B_SM, color="red", linestyle="--", linewidth=1.5,
                 label=r"$R_b^{\rm SM}$")
    ax1.set_ylabel(r"$R_b$")
    ax1.set_xlabel("Year")
    ax1.legend(fontsize="small")

    cons_rb = data["consistency_rb"]
    ax1.text(0.95, 0.95,
             r"$\chi^2$/ndf = %.1f/%d" % (cons_rb["chi2"], cons_rb["ndf"]) +
             "\np = %.3f" % cons_rb["p_value"],
             transform=ax1.transAxes, ha="right", va="top",
             fontsize="x-small",
             bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

    exp_label_data(ax1)

    # A_FB per year
    afb_vals = [r.get("A_FB_b") for r in per_year]
    afb_errs = [r.get("sigma_stat_afb") or 0 for r in per_year]
    valid_afb = [(y, a, e) for y, a, e in zip(years, afb_vals, afb_errs)
                 if a is not None]

    if valid_afb:
        yrs, avals, aerrs = zip(*valid_afb)
        ax2.errorbar(yrs, avals, yerr=aerrs, fmt="s", color="C1",
                      markersize=10, capsize=6, linewidth=2)

    ax2.axhline(AFB_B_OBS, color="red", linestyle="--", linewidth=1.5,
                 label=r"LEP combined")
    ax2.axhline(0, color="gray", linestyle=":", linewidth=1)
    ax2.set_ylabel(r"$A_{FB}^b$")
    ax2.set_xlabel("Year")
    ax2.legend(fontsize="small")

    save_and_register(
        fig, "per_year_consistency.png", str(SCRIPT_PATH),
        "Per-year R_b and A_FB^b consistency (1992-1995, full data)",
        "result", lower_panel="none", observable_type="derived",
    )
    log.info("Saved per_year_consistency")


def plot_calibration_progression():
    """Compare 10% vs full data results."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 10))

    with open(PHASE4C_OUT / "three_tag_rb_fulldata.json") as f:
        full_rb = json.load(f)
    with open(PHASE4C_OUT / "afb_fulldata.json") as f:
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

    x = np.arange(len(stages))
    ax1.errorbar(x, rb_vals, yerr=rb_errs, fmt="o", color="C0",
                  markersize=12, capsize=6, linewidth=2)
    ax1.axhline(R_B_SM, color="red", linestyle="--", linewidth=1.5,
                 label=r"$R_b^{\rm SM}$")
    ax1.set_xticks(x)
    ax1.set_xticklabels(stages)
    ax1.set_ylabel(r"$R_b$")
    ax1.legend(fontsize="small")
    exp_label_data(ax1)

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
    ax2.set_ylabel(r"$A_{FB}^b$")
    ax2.legend(fontsize="small")

    # Adjust spacing to prevent header overlap in two-panel layout
    fig.subplots_adjust(wspace=0.35)

    save_and_register(
        fig, "calibration_progression.png", str(SCRIPT_PATH),
        "R_b and A_FB^b progression from MC to 10% to full data",
        "comparison", lower_panel="none", observable_type="derived",
    )
    log.info("Saved calibration_progression")


def plot_bdt_crosscheck():
    """Plot BDT cross-check results."""
    path = PHASE4C_OUT / "bdt_crosscheck_fulldata.json"
    if not path.exists():
        log.warning("bdt_crosscheck_fulldata.json not found")
        return

    with open(path) as f:
        data = json.load(f)

    results = data["results_by_threshold"]
    valid = [r for r in results if r["R_b"] is not None and 0.05 < r["R_b"] < 0.5]

    if not valid:
        log.warning("No valid BDT results")
        return

    fig, ax = plt.subplots(figsize=(10, 10))

    thrs = [r["bdt_threshold"] for r in valid]
    rbs = [r["R_b"] for r in valid]
    errs = [r["sigma_Rb"] or 0.01 for r in valid]

    ax.errorbar(thrs, rbs, yerr=errs, fmt="s", color="C1", markersize=10,
                 capsize=6, linewidth=2, label="BDT-based")

    cut_rb = data["cut_based_comparison"]["R_b_cut_based"]
    cut_sig = data["cut_based_comparison"]["sigma_cut_based"]
    if cut_rb is not None:
        ax.axhline(cut_rb, color="C0", linestyle="-.", linewidth=1.5,
                    label=r"Cut-based $R_b$ = %.4f" % cut_rb)
        if cut_sig:
            ax.axhspan(cut_rb - cut_sig, cut_rb + cut_sig,
                       color="C0", alpha=0.15)

    ax.axhline(R_B_SM, color="red", linestyle="--", linewidth=1.5,
                label=r"$R_b^{\rm SM}$")

    ax.set_xlabel("BDT score threshold")
    ax.set_ylabel(r"$R_b$")
    ax.set_ylim(0.10, 0.35)
    ax.legend(fontsize="small")
    exp_label_data(ax)

    save_and_register(
        fig, "bdt_crosscheck_fulldata.png", str(SCRIPT_PATH),
        "BDT cross-check R_b vs cut-based (full data)",
        "comparison", lower_panel="none", observable_type="derived",
    )
    log.info("Saved bdt_crosscheck_fulldata")


def main():
    log.info("=" * 60)
    log.info("Phase 4c: Publication-Quality Figures (Fixed)")
    log.info("=" * 60)

    plot_rb_stability()
    plot_afb_kappa()
    plot_systematics_breakdown()
    plot_per_year()
    plot_calibration_progression()
    plot_bdt_crosscheck()


if __name__ == "__main__":
    main()
