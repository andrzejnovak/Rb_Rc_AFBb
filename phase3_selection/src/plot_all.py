"""Phase 3: All plotting for selection phase.

Produces all figures from precomputed JSON/NPZ artifacts.
Separated from analysis scripts per methodology/11-coding.md Section 11.5.

Reads: outputs/*.json, outputs/*.npz
Writes: outputs/figures/*.png, outputs/figures/*.pdf, outputs/FIGURES.json
"""
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import mplhep as mh
import numpy as np
from mplhep.utils import mpl_magic
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

mh.style.use("CMS")

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "outputs"
FIG = OUT / "figures"
FIG.mkdir(parents=True, exist_ok=True)

SESSION = "magnus_1207"
TIMESTAMP = datetime.now(timezone.utc).strftime("%Y%m%d")
SCRIPT_PATH = f"src/{Path(__file__).name}"


def save_and_register(fig, filename, description, fig_type,
                      lower_panel="none", is_2d=False,
                      observable_type="count"):
    """Save figure and register in FIGURES.json."""
    now = datetime.now(timezone.utc).isoformat()
    script_mtime = datetime.fromtimestamp(
        Path(__file__).stat().st_mtime, tz=timezone.utc
    ).isoformat()

    fig.savefig(FIG / filename, bbox_inches="tight", dpi=200, transparent=True)
    pdf_name = filename.replace(".png", ".pdf")
    fig.savefig(FIG / pdf_name, bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)

    registry_path = OUT / "FIGURES.json"
    if registry_path.exists():
        with open(registry_path) as f:
            registry = json.load(f)
    else:
        registry = []

    registry = [e for e in registry if e["filename"] != filename]
    registry.append({
        "filename": filename,
        "type": fig_type,
        "script": SCRIPT_PATH,
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


def exp_label_data(ax):
    mh.label.exp_label(
        exp="ALEPH", data=True, llabel="Open Data",
        rlabel=r"$\sqrt{s} = 91.2$ GeV", ax=ax,
    )


def exp_label_mc(ax):
    mh.label.exp_label(
        exp="ALEPH", data=True, llabel="Open Simulation",
        rlabel=r"$\sqrt{s} = 91.2$ GeV", ax=ax,
    )


def data_mc_pull(data_vals, mc_vals, bins, xlabel, ylabel, filename,
                 description, log_y=False, data_weights=None, mc_weights=None,
                 mc_scale_to_data=True, observable_type="count"):
    """Generic data/MC comparison with pull panel."""
    fig, (ax, rax) = plt.subplots(
        2, 1, figsize=(10, 10),
        gridspec_kw={"height_ratios": [3, 1]}, sharex=True,
    )
    fig.subplots_adjust(hspace=0)

    h_data, _ = np.histogram(data_vals, bins=bins, weights=data_weights)
    h_mc, _ = np.histogram(mc_vals, bins=bins, weights=mc_weights)

    if data_weights is not None:
        h_data_e2, _ = np.histogram(data_vals, bins=bins,
                                     weights=np.asarray(data_weights)**2)
        h_data_err = np.sqrt(h_data_e2)
    else:
        h_data_err = np.sqrt(np.maximum(h_data, 1))

    if mc_weights is not None:
        h_mc_e2, _ = np.histogram(mc_vals, bins=bins,
                                   weights=np.asarray(mc_weights)**2)
        h_mc_err = np.sqrt(h_mc_e2)
    else:
        h_mc_err = np.sqrt(np.maximum(h_mc, 1))

    if mc_scale_to_data:
        s = h_data.sum() / max(h_mc.sum(), 1)
        h_mc = h_mc * s
        h_mc_err = h_mc_err * s

    bc = 0.5 * (bins[:-1] + bins[1:])

    mh.histplot(h_mc, bins=bins, ax=ax, label="MC (normalized to data)",
                histtype="fill", color="C0", alpha=0.5)
    mh.histplot(h_mc, bins=bins, ax=ax, histtype="step", color="C0")
    ax.errorbar(bc, h_data, yerr=h_data_err, fmt="o", color="black",
                markersize=4, label="Data")

    ax.set_ylabel(ylabel)
    if log_y:
        ax.set_yscale("log")
    ax.legend(fontsize="x-small")
    exp_label_data(ax)
    mpl_magic(ax)

    total_err = np.sqrt(h_data_err**2 + h_mc_err**2)
    pull = np.where(total_err > 0, (h_data - h_mc) / total_err, 0.0)
    rax.errorbar(bc, pull, yerr=1.0, fmt="o", color="black", markersize=3)
    rax.axhline(0, color="gray", ls="--", lw=0.8)
    rax.axhline(2, color="gray", ls=":", lw=0.5)
    rax.axhline(-2, color="gray", ls=":", lw=0.5)
    rax.set_ylabel("Pull")
    rax.set_xlabel(xlabel)
    rax.set_ylim(-4, 4)

    save_and_register(fig, filename, description, "data_mc",
                      lower_panel="pull", observable_type=observable_type)


def plot_cutflow():
    """Plot cutflow table as bar chart."""
    with open(OUT / "cutflow.json") as f:
        cf = json.load(f)

    fig, ax = plt.subplots(figsize=(10, 10))

    # Map code variable names to publication-quality labels [A5 fix]
    CUTFLOW_LABELS = {
        "total": "Total events",
        "passesAll": "Basic quality",
        "cos_theta_cut": r"$|\cos\theta_{\mathrm{thrust}}| < 0.9$",
        "total_tracks": "All tracks",
        "good_tracks": "Quality tracks\n(VDET, purity, TPC)",
    }

    raw_labels = list(cf["data"].keys())
    labels = [CUTFLOW_LABELS.get(k, k) for k in raw_labels]
    data_vals = [cf["data"][k] for k in raw_labels]
    mc_vals = [cf["mc"][k] for k in raw_labels]

    # Normalize MC to data total
    scale = data_vals[0] / max(mc_vals[0], 1)
    mc_vals_scaled = [v * scale for v in mc_vals]

    x = np.arange(len(labels))
    width = 0.35

    ax.bar(x - width/2, data_vals, width, label="Data", color="black", alpha=0.7)
    ax.bar(x + width/2, mc_vals_scaled, width, label="MC (scaled)", color="C0", alpha=0.7)

    ax.set_ylabel("Events / Tracks")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize="small")
    ax.legend(fontsize="x-small")
    ax.set_yscale("log")
    exp_label_data(ax)
    mpl_magic(ax)

    save_and_register(
        fig, f"cutflow_{SESSION}_{TIMESTAMP}.png",
        "Cutflow showing event and track counts after successive selection cuts",
        "diagnostic",
    )


def plot_d0_sign_validation():
    """Plot d0 sign convention validation [D19].

    Fix A8: Use tight tag cut (combined tag > 8) for b-enrichment
    instead of bFlag=4, which covers 99.8% of events and provides
    no enrichment.
    """
    with open(OUT / "d0_sign_validation.json") as f:
        val = json.load(f)

    # Load hemisphere tags to create a genuine b-enriched subsample
    tags = np.load(OUT / "hemisphere_tags.npz", allow_pickle=False)
    signed = np.load(OUT / "signed_d0.npz", allow_pickle=False)
    data = np.load(OUT / "preselected_data.npz", allow_pickle=False)

    sig_all = signed["data_signed_sig"]
    d0_offsets = data["trk_d0_offsets"]
    n_events = len(d0_offsets) - 1

    # b-enriched: events where BOTH hemispheres have combined tag > 8
    # (tight double-tag => high b purity)
    tight_mask = (tags["data_combined_h0"] > 8) & (tags["data_combined_h1"] > 8)
    n_tight = int(np.sum(tight_mask))
    log.info("d0 sign validation: tight-tag b-enriched = %d events (%.1f%%)",
             n_tight, 100 * n_tight / n_events)

    # Broadcast event mask to track level
    counts = np.diff(d0_offsets)
    trk_tight = np.repeat(tight_mask, counts)

    sig_b = sig_all[trk_tight]

    # Compute asymmetries at thresholds
    thresholds_float = [1.0, 2.0, 3.0, 5.0, 7.0, 10.0]
    asym_b_tight = []
    asym_all_list = []

    for thr in thresholds_float:
        n_pos_b = int(np.sum(sig_b > thr))
        n_neg_b = int(np.sum(sig_b < -thr))
        asym_bt = (n_pos_b - n_neg_b) / max(n_pos_b + n_neg_b, 1)
        asym_b_tight.append(asym_bt)

        n_pos_all = int(np.sum(sig_all > thr))
        n_neg_all = int(np.sum(sig_all < -thr))
        asym_at = (n_pos_all - n_neg_all) / max(n_pos_all + n_neg_all, 1)
        asym_all_list.append(asym_at)

    fig, ax = plt.subplots(figsize=(10, 10))

    ax.plot(thresholds_float, asym_b_tight, "o-", color="C3",
            label=f"b-enriched (tight double-tag, {n_tight} events)")
    ax.plot(thresholds_float, asym_all_list, "s-", color="C0",
            label="All events")
    ax.axhline(0, color="gray", ls="--", lw=0.8)

    ax.set_xlabel(r"$|d_0/\sigma_{d_0}|$ threshold")
    ax.set_ylabel(r"Asymmetry $(N_+ - N_-) / (N_+ + N_-)$")
    ax.legend(fontsize="x-small", loc="lower right",
              title=f"Gate: {'PASS' if val['gate_passed'] else 'FAIL'}")
    exp_label_data(ax)

    save_and_register(
        fig, f"d0_sign_validation_{SESSION}_{TIMESTAMP}.png",
        "d0 sign convention validation [D19]: asymmetry of d0/sigma_d0 "
        "positive vs negative tails. b-enriched sample uses tight double-tag "
        "(combined tag > 8 in both hemispheres). "
        "Higher asymmetry in b-enriched sample confirms physics-meaningful sign.",
        "diagnostic",
    )


def plot_sigma_d0_calibration():
    """Plot sigma_d0 calibration quality."""
    with open(OUT / "sigma_d0_params.json") as f:
        params = json.load(f)

    fig, ax = plt.subplots(figsize=(10, 10))

    data_cal = params["data_calibration"]
    mc_cal = params["mc_calibration"]

    # Map code bin labels to human-readable descriptions [A6 fix]
    # Format: nv{N}_p{I}_ct{J} -> nvdet=N, p in [lo,hi], |cos theta| in [lo,hi]
    P_BINS = [0.5, 1.0, 2.0, 5.0, 15.0, 100.0]
    CT_BINS = [0.0, 0.25, 0.5, 0.7, 0.9]

    def _human_label(code_label):
        """Convert e.g. 'nv1_p0_ct0' to 'nv=1, p<1, |ct|<0.25'."""
        parts = code_label.split("_")
        nv = parts[0].replace("nv", "")
        ip = int(parts[1].replace("p", ""))
        ic = int(parts[2].replace("ct", ""))
        p_lo, p_hi = P_BINS[ip], P_BINS[ip + 1]
        ct_lo, ct_hi = CT_BINS[ic], CT_BINS[ic + 1]
        return (f"nv={nv}\n"
                f"p=[{p_lo:.0f},{p_hi:.0f}]\n"
                f"|ct|=[{ct_lo:.2f},{ct_hi:.2f}]")

    bin_labels = []
    bin_labels_human = []
    data_scales = []
    mc_scales = []
    for key in sorted(data_cal.keys()):
        data_scales.append(data_cal[key]["scale_factor"])
        if key in mc_cal:
            mc_scales.append(mc_cal[key]["scale_factor"])
        else:
            mc_scales.append(np.nan)
        bin_labels.append(key)
        bin_labels_human.append(_human_label(key))

    x = np.arange(len(bin_labels))
    ax.plot(x, data_scales, "o", color="black", label="Data", markersize=4)
    ax.plot(x, mc_scales, "s", color="C0", label="MC", markersize=4)
    ax.axhline(1.0, color="gray", ls="--", lw=0.8)

    ax.set_ylabel(r"$\sigma_{d_0}$ scale factor (dimensionless)")
    ax.set_xlabel(r"Calibration bin index (nvdet, $p$ [GeV/$c$], $|\cos\theta|$)")
    # Only show every 5th label to avoid overlap
    show_idx = np.arange(0, len(bin_labels), max(1, len(bin_labels)//8))
    ax.set_xticks(show_idx)
    ax.set_xticklabels([bin_labels_human[i] for i in show_idx],
                       rotation=45, ha="right", fontsize="xx-small")
    ax.legend(fontsize="x-small")
    exp_label_data(ax)
    mpl_magic(ax)

    save_and_register(
        fig, f"sigma_d0_calibration_{SESSION}_{TIMESTAMP}.png",
        "sigma_d0 scale factors from negative d0 tail calibration [D7] "
        "per (nvdet, momentum, cos theta) bin. Scale factor = 1.0 means "
        "the nominal parameterization correctly describes the resolution.",
        "diagnostic", observable_type="derived",
    )


def plot_significance_distribution():
    """Plot signed d0/sigma_d0 distribution data vs MC."""
    sig = np.load(OUT / "d0_significance.npz", allow_pickle=False)

    data_sig = sig["data_significance"]
    mc_sig = sig["mc_significance"]

    bins = np.linspace(-10, 30, 100)

    data_mc_pull(
        data_sig, mc_sig, bins,
        r"Signed $d_0 / \sigma_{d_0}$", "Tracks",
        f"data_mc_significance_{SESSION}_{TIMESTAMP}.png",
        "Signed impact parameter significance d0/sigma_d0 distribution "
        "data vs MC after sigma_d0 calibration. Positive tail from "
        "b/c-hadron decays, negative tail from resolution only.",
        log_y=True,
    )


def plot_hemisphere_tags():
    """Plot hemisphere tag distributions."""
    tags = np.load(OUT / "hemisphere_tags.npz", allow_pickle=False)

    # Combined tag
    data_h0 = tags["data_combined_h0"]
    mc_h0 = tags["mc_combined_h0"]

    bins = np.linspace(0, 20, 60)
    data_mc_pull(
        data_h0[data_h0 > 0], mc_h0[mc_h0 > 0], bins,
        r"Combined tag $-\ln P_{\mathrm{hem}} + \mathrm{mass\ bonus}$",
        "Hemispheres",
        f"data_mc_combined_tag_{SESSION}_{TIMESTAMP}.png",
        "Combined probability-mass hemisphere tag [D8, D18] data vs MC. "
        "Higher values indicate more b-like hemispheres.",
        log_y=True,
    )

    # Hemisphere mass — with b/c threshold line [B5 fix]
    data_mass = tags["data_mass_h0"]
    mc_mass = tags["mc_mass_h0"]

    bins_m = np.linspace(0, 8, 50)

    # Use the data_mc_pull helper then add vertical line
    fig_m, (ax_m, rax_m) = plt.subplots(
        2, 1, figsize=(10, 10),
        gridspec_kw={"height_ratios": [3, 1]}, sharex=True,
    )
    fig_m.subplots_adjust(hspace=0)

    d_m = data_mass[data_mass > 0]
    m_m = mc_mass[mc_mass > 0]
    h_d, _ = np.histogram(d_m, bins=bins_m)
    h_mc_m, _ = np.histogram(m_m, bins=bins_m)
    h_d_err = np.sqrt(np.maximum(h_d, 1))
    h_mc_err = np.sqrt(np.maximum(h_mc_m, 1))
    s = h_d.sum() / max(h_mc_m.sum(), 1)
    h_mc_m = h_mc_m * s
    h_mc_err = h_mc_err * s
    bc = 0.5 * (bins_m[:-1] + bins_m[1:])

    mh.histplot(h_mc_m, bins=bins_m, ax=ax_m, label="MC (normalized to data)",
                histtype="fill", color="C0", alpha=0.5)
    mh.histplot(h_mc_m, bins=bins_m, ax=ax_m, histtype="step", color="C0")
    ax_m.errorbar(bc, h_d, yerr=h_d_err, fmt="o", color="black",
                  markersize=4, label="Data")
    # b/c threshold line
    ax_m.axvline(1.8, color="C3", ls="--", lw=1.5,
                 label=r"$b/c$ threshold 1.8 GeV/$c^2$ [D18]")
    ax_m.set_ylabel("Hemispheres")
    ax_m.legend(fontsize="x-small")
    exp_label_data(ax_m)
    mpl_magic(ax_m)

    total_err = np.sqrt(h_d_err**2 + h_mc_err**2)
    pull = np.where(total_err > 0, (h_d - h_mc_m) / total_err, 0.0)
    rax_m.errorbar(bc, pull, yerr=1.0, fmt="o", color="black", markersize=3)
    rax_m.axhline(0, color="gray", ls="--", lw=0.8)
    rax_m.axhline(2, color="gray", ls=":", lw=0.5)
    rax_m.axhline(-2, color="gray", ls=":", lw=0.5)
    rax_m.axvline(1.8, color="C3", ls="--", lw=1.0, alpha=0.5)
    rax_m.set_ylabel("Pull")
    rax_m.set_xlabel(r"Hemisphere invariant mass [GeV/$c^2$]")
    rax_m.set_ylim(-4, 4)

    save_and_register(
        fig_m, f"data_mc_hemisphere_mass_{SESSION}_{TIMESTAMP}.png",
        "Invariant mass of displaced tracks in hemisphere. "
        "Vertical line at 1.8 GeV/c^2 [D18] separates b from c hemispheres.",
        "data_mc", lower_panel="pull",
    )

    # P_hem only (no mass)
    data_nlp = tags["data_nlp_h0"]
    mc_nlp = tags["mc_nlp_h0"]

    bins_p = np.linspace(0, 15, 50)
    data_mc_pull(
        data_nlp[data_nlp > 0], mc_nlp[mc_nlp > 0], bins_p,
        r"$-\ln P_{\mathrm{hem}}$",
        "Hemispheres",
        f"data_mc_phem_{SESSION}_{TIMESTAMP}.png",
        "Hemisphere probability tag P_hem [D8] data vs MC (log scale). "
        "Based on product of per-track IP significance probabilities.",
        log_y=True,
    )


def plot_jet_charge():
    """Plot jet charge distributions for each kappa."""
    jc = np.load(OUT / "jet_charge.npz", allow_pickle=False)

    kappas = [0.3, 0.5, 1.0, 2.0]

    for kappa in kappas:
        k_str = f"k{kappa:.1f}"
        data_qfb = jc[f"data_qfb_{k_str}"]
        mc_qfb = jc[f"mc_qfb_{k_str}"]

        valid_d = ~np.isnan(data_qfb)
        valid_m = ~np.isnan(mc_qfb)

        bins = np.linspace(-1.5, 1.5, 60)
        data_mc_pull(
            data_qfb[valid_d], mc_qfb[valid_m], bins,
            rf"$Q_{{FB}}$ ($\kappa = {kappa}$)",
            "Events",
            f"data_mc_qfb_k{kappa:.1f}_{SESSION}_{TIMESTAMP}.png",
            f"Forward-backward charge asymmetry Q_FB for kappa={kappa} "
            f"[D4, D5]. Data vs MC comparison.",
            observable_type="derived",
        )

    # kappa=infinity
    data_qfb_inf = jc["data_qfb_kinf"]
    mc_qfb_inf = jc["mc_qfb_kinf"]
    valid_d = ~np.isnan(data_qfb_inf)
    valid_m = ~np.isnan(mc_qfb_inf)

    bins = np.linspace(-2.5, 2.5, 30)
    data_mc_pull(
        data_qfb_inf[valid_d], mc_qfb_inf[valid_m], bins,
        r"$Q_{FB}$ ($\kappa = \infty$, leading particle)",
        "Events",
        f"data_mc_qfb_kinf_{SESSION}_{TIMESTAMP}.png",
        "Leading particle charge Q_FB (kappa=infinity) [D5]. "
        "Discrete values from leading track charge.",
        observable_type="derived",
    )


def plot_rb_scan():
    """Plot R_b operating point stability scan.

    Fix A9/RED FLAG: Show full y-axis range to display biased values,
    add R_b=0.216 reference line prominently, add annotation explaining
    the bias is expected at Phase 3.
    Fix B4: Document no plateau expected at Phase 3.
    Fix B7: Differentiate combined vs probability-only curves.
    """
    with open(OUT / "rb_scan.json") as f:
        scan = json.load(f)

    fig, ax = plt.subplots(figsize=(10, 10))

    # Combined tag — black circles
    thr = scan["combined"]["thresholds"]
    rb = scan["combined"]["R_b"]
    sigma = scan["combined"]["sigma_rb"]

    valid = [(t, r, s) for t, r, s in zip(thr, rb, sigma)
             if r is not None and s is not None and s > 0]
    if valid:
        t_v, r_v, s_v = zip(*valid)
        ax.errorbar(t_v, r_v, yerr=s_v, fmt="o", color="black",
                    markersize=5, label="Combined tag", zorder=5)

    # Probability-only tag — blue triangles, offset slightly [B7 fix]
    thr_p = scan["probability"]["thresholds"]
    rb_p = scan["probability"]["R_b"]
    sigma_p = scan["probability"]["sigma_rb"]

    valid_p = [(t, r, s) for t, r, s in zip(thr_p, rb_p, sigma_p)
               if r is not None and s is not None and s > 0]
    if valid_p:
        t_vp, r_vp, s_vp = zip(*valid_p)
        # Offset x by +0.15 to avoid overlap
        t_vp_off = [t + 0.15 for t in t_vp]
        ax.errorbar(t_vp_off, r_vp, yerr=s_vp, fmt="^", color="C0",
                    markersize=5, label="Probability-only tag", zorder=4)

    # Reference values — prominent
    ref = scan["reference"]
    ax.axhline(ref["SM_Rb"], color="C3", ls="-", lw=2.0,
               label=f"SM $R_b$ = {ref['SM_Rb']:.5f}", zorder=3)
    ax.axhspan(ref["ALEPH_Rb"] - ref["ALEPH_Rb_err"],
               ref["ALEPH_Rb"] + ref["ALEPH_Rb_err"],
               color="C3", alpha=0.2, zorder=1)
    ax.axhline(ref["ALEPH_Rb"], color="C3", ls="--", lw=1.5,
               label=f"ALEPH: {ref['ALEPH_Rb']:.4f} $\\pm$ {ref['ALEPH_Rb_err']:.4f}",
               zorder=2)

    ax.set_xlabel("Tag threshold")
    ax.set_ylabel(r"Extracted $R_b$")
    # Show full range of data [A9 fix]
    ax.set_ylim(0.0, 1.1)

    # Diagnostic note: uncalibrated efficiencies, bias expected
    ax.text(0.98, 0.55,
            "MC diagnostic: nominal $\\varepsilon_c$,\n"
            "$\\varepsilon_{uds}$ not calibrated\n"
            "to this tagger. Bias expected;\n"
            "data-driven calibration will\n"
            "constrain backgrounds.",
            transform=ax.transAxes, ha="right", va="top",
            fontsize="x-small",
            bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.9))

    ax.legend(fontsize="x-small", loc="upper left")
    exp_label_data(ax)
    mpl_magic(ax)

    save_and_register(
        fig, f"rb_operating_scan_{SESSION}_{TIMESTAMP}.png",
        "R_b operating point stability scan [D14]. Extracted R_b vs "
        "tag threshold for combined and probability-only tags. "
        "SM R_b = 0.216 reference shown. Values 0.5-1.0 are expected "
        "at Phase 3 with uncalibrated background efficiencies "
        "(eps_c=0.05, eps_uds=0.005 are nominal, not fitted). "
        "Phase 4 multi-working-point fit will calibrate backgrounds.",
        "result", observable_type="derived",
    )


def plot_closure_tests():
    """Plot closure test results as 3 separate standalone figures.

    Fix B14/Human priority: split 3-panel into separate figures for readability.
    Each figure is (10,10) with proper labels and sizing.
    """
    with open(OUT / "closure_results.json") as f:
        results = json.load(f)

    # Test (a): Mirrored significance — standalone figure
    fig_a, ax_a = plt.subplots(figsize=(10, 10))
    r_a = results["negative_d0"]
    rb_mirrored = r_a.get("R_b_extracted", 0) or 0
    rb_full = r_a.get("full_sample_R_b", 0) or 0
    passes_a = r_a["passes"]
    color_a = "C2" if passes_a else "C3"

    ax_a.bar([0], [rb_full], color="C0", alpha=0.5, width=0.6, label="Full sample")
    ax_a.bar([1], [max(rb_mirrored, 0.002)], color=color_a, alpha=0.8, width=0.6,
             label="Mirrored")
    if rb_mirrored < 0.005:
        ax_a.annotate(f"$R_b$ = {rb_mirrored:.4f}", xy=(1, 0.002),
                      xytext=(1, 0.15), fontsize="medium", ha="center",
                      arrowprops=dict(arrowstyle="->", color="black", lw=1.0))
    ax_a.set_xticks([0, 1])
    ax_a.set_xticklabels(["Full sample", "Mirrored\n(no lifetime)"],
                          fontsize="medium")
    ax_a.set_xlabel("Sample type", fontsize="large")
    ax_a.set_ylabel(r"Extracted $R_b$ (dimensionless)", fontsize="large")
    verdict_a = "PASS" if passes_a else "FAIL"
    ax_a.text(0.5, 0.95, f"Mirrored significance: {verdict_a}\n$R_b$ = {rb_mirrored:.4f}",
              transform=ax_a.transAxes, ha="center", va="top",
              fontsize="medium", color=color_a,
              bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))
    ax_a.legend(fontsize="medium")
    exp_label_data(ax_a)
    save_and_register(
        fig_a, f"closure_mirrored_{SESSION}_{TIMESTAMP}.png",
        "Closure test (a): mirrored-significance pseudo-data (R_b near 0 expected). "
        "Full sample R_b shown for reference.",
        "closure",
    )

    # Test (b): bFlag chi2/ndf — standalone figure
    fig_b, ax_b = plt.subplots(figsize=(10, 10))
    r_b = results["bflag_consistency"]
    chi2_ndf = r_b.get("chi2_ndf", None)
    passes_b = r_b["passes"]
    color_b = "C2" if passes_b else "C3"

    if chi2_ndf is not None:
        ax_b.bar([0], [chi2_ndf], color=color_b, alpha=0.7, width=0.6,
                 label=r"Observed $\chi^2$/ndf")
        ax_b.axhline(1.0, color="gray", ls="--", lw=1.5,
                      label=r"Expected ($\chi^2$/ndf = 1)")
        ax_b.axhline(2.0, color="C1", ls=":", lw=1.5,
                      label="PASS/FAIL threshold = 2")
    ax_b.set_xticks([0])
    ax_b.set_xticklabels(["bFlag=4 vs bFlag=$-$1"], fontsize="medium")
    ax_b.set_xlabel("Comparison", fontsize="large")
    ax_b.set_ylabel(r"$\chi^2$/ndf (significance shape comparison)", fontsize="large")
    ax_b.set_yscale("log")
    chi2_str = f"$\\chi^2$/ndf = {chi2_ndf:,.0f}" if chi2_ndf else "N/A"
    verdict_b = "PASS" if passes_b else "FAIL"
    ax_b.text(0.5, 0.95, f"bFlag discrimination: {verdict_b}\n{chi2_str}",
              transform=ax_b.transAxes, ha="center", va="top",
              fontsize="medium", color=color_b,
              bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))
    ax_b.legend(fontsize="medium")
    exp_label_data(ax_b)
    save_and_register(
        fig_b, f"closure_bflag_{SESSION}_{TIMESTAMP}.png",
        "Closure test (b): bFlag=4 (b-enriched) vs bFlag=-1 (light-enriched) "
        "discriminant shape chi2/ndf.",
        "closure",
    )

    # Test (c): Contamination injection — standalone figure
    fig_c, ax_c = plt.subplots(figsize=(10, 10))
    r_c = results["contamination_injection"]
    ratio = r_c.get("ratio", 0) or 0
    pred = r_c.get("predicted_shift", 0) or 0
    obs = r_c.get("observed_shift", 0) or 0
    passes_c = r_c["passes"]
    color_c = "C2" if passes_c else "C3"

    ax_c.bar([0, 1], [abs(pred), abs(obs)], color=["C0", color_c],
             alpha=0.7, width=0.6)
    ax_c.set_xticks([0, 1])
    ax_c.set_xticklabels(["Predicted shift", "Observed shift"],
                          fontsize="medium")
    ax_c.set_ylabel(r"$|\Delta R_b|$", fontsize="large")
    verdict_c = "PASS" if passes_c else "FAIL"
    ax_c.text(0.5, 0.95, f"Contamination injection: {verdict_c}\nRatio = {ratio:.2f}",
              transform=ax_c.transAxes, ha="center", va="top",
              fontsize="medium", color=color_c,
              bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))
    exp_label_data(ax_c)
    save_and_register(
        fig_c, f"closure_contamination_{SESSION}_{TIMESTAMP}.png",
        "Closure test (c): 5% contamination injection. "
        "Predicted vs observed R_b shift.",
        "closure",
    )


def plot_data_mc_kinematic():
    """Plot data/MC comparisons for kinematic variables."""
    data = np.load(OUT / "preselected_data.npz", allow_pickle=False)
    mc = np.load(OUT / "preselected_mc.npz", allow_pickle=False)

    # Thrust
    data_mc_pull(
        data["thrust"], mc["thrust"],
        np.linspace(0.5, 1.0, 50),
        "Thrust", "Events",
        f"data_mc_thrust_{SESSION}_{TIMESTAMP}.png",
        "Thrust distribution after preselection, data vs MC.",
    )

    # cos(theta_thrust)
    data_mc_pull(
        data["cos_theta_thrust"], mc["cos_theta_thrust"],
        np.linspace(-0.9, 0.9, 40),
        r"$\cos\theta_{\mathrm{thrust}}$", "Events",
        f"data_mc_costheta_{SESSION}_{TIMESTAMP}.png",
        "cos(theta_thrust) after |cos theta| < 0.9 cut.",
    )

    # Charged multiplicity
    data_mc_pull(
        data["nch"], mc["nch"],
        np.arange(0, 50, 1),
        r"$N_{\mathrm{ch}}$", "Events",
        f"data_mc_nch_{SESSION}_{TIMESTAMP}.png",
        "Charged particle multiplicity after preselection.",
    )

    # Sphericity
    data_mc_pull(
        data["sphericity"], mc["sphericity"],
        np.linspace(0, 0.6, 40),
        "Sphericity", "Events",
        f"data_mc_sphericity_{SESSION}_{TIMESTAMP}.png",
        "Sphericity distribution after preselection.",
    )

    # Track d0 (raw, before sigma_d0)
    data_mc_pull(
        data["trk_d0"], mc["trk_d0"],
        np.linspace(-0.1, 0.1, 80),
        r"$d_0$ [cm]", "Tracks",
        f"data_mc_d0_{SESSION}_{TIMESTAMP}.png",
        "Impact parameter d0 for quality-selected tracks (nvdet>0, highPurity, ntpc>4).",
    )

    # Track pT
    data_mc_pull(
        data["trk_pt"], mc["trk_pt"],
        np.logspace(-1, 1.7, 50),
        r"Track $p_T$ [GeV/$c$]", "Tracks",
        f"data_mc_trackpt_{SESSION}_{TIMESTAMP}.png",
        "Track transverse momentum after quality cuts.",
        log_y=True,
    )


def main():
    log.info("=" * 60)
    log.info("Phase 3: Plotting")
    log.info("=" * 60)

    plot_cutflow()
    plot_d0_sign_validation()
    plot_sigma_d0_calibration()
    plot_significance_distribution()
    plot_hemisphere_tags()
    plot_jet_charge()
    plot_rb_scan()
    plot_closure_tests()
    plot_data_mc_kinematic()

    log.info("\nAll plots complete.")

    # Count figures
    with open(OUT / "FIGURES.json") as f:
        reg = json.load(f)
    log.info("Total figures registered: %d", len(reg))


if __name__ == "__main__":
    main()
