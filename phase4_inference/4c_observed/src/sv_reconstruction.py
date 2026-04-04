"""Phase 4c: Secondary vertex reconstruction for enhanced b/c separation.

Implements SV reconstruction from displaced tracks to improve b-tagging
beyond the current d0-significance + mass tag. The SV properties (vertex
mass, track multiplicity, flight distance) provide powerful b/c
discrimination because b hadrons are heavier, longer-lived, and produce
higher-multiplicity vertices than c hadrons.

Current best: R_b = 0.2150 (mass cut), eps_c/eps_b ~ 0.5-0.7.
Target: eps_c/eps_b ~ 0.1 using SV properties (ALEPH achieved this).

Algorithm:
  Step 1: Select displaced tracks (signed significance > 2) per hemisphere
  Step 2: For hemispheres with >= 2 displaced tracks, compute SV properties
  Step 3: SV properties: vertex mass, multiplicity, flight distance proxy
  Step 4: Build combined SV discriminant for b/c separation
  Step 5: Extract R_b with SV-enhanced tag using 3-tag calibration
  Step 6: Extract A_FB^b in SV-tagged events

Note: MC truth flavor (bFlag) is not available in this dataset (bFlag=-999
for MC). Therefore b/c separation power is evaluated indirectly through
the algebraic 3-tag calibration (which solves for eps_b, eps_c, eps_uds
from tag fractions + known R_b, R_c).

Reads: phase3_selection/outputs/preselected_data.npz
       phase3_selection/outputs/preselected_mc.npz
       phase3_selection/outputs/signed_d0.npz
       phase3_selection/outputs/d0_significance.npz
       phase3_selection/outputs/hemisphere_tags.npz
       phase3_selection/outputs/jet_charge.npz
Writes: phase4_inference/4c_observed/outputs/sv_tags.npz
        phase4_inference/4c_observed/outputs/sv_reconstruction.json
        phase4_inference/4c_observed/outputs/figures/sv_*.png
        analysis_note/results/parameters.json

Session: felix_91e9
"""
import json
import logging
import sys
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mplhep as mh
import numpy as np
from scipy.stats import chi2 as chi2_dist
from rich.logging import RichHandler

mh.style.use("CMS")

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

HERE = Path(__file__).resolve().parent
PHASE4C_OUT = HERE.parent / "outputs"
P4A_OUT = HERE.parents[1] / "4a_expected" / "outputs"
P3_OUT = HERE.parents[2] / "phase3_selection" / "outputs"
RESULTS_DIR = HERE.parents[2] / "analysis_note" / "results"
FIG_DIR = PHASE4C_OUT / "figures"
PHASE4C_OUT.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Import 3-tag functions from Phase 4a
sys.path.insert(0, str(HERE.parents[1] / "4a_expected" / "src"))
from three_tag_rb_extraction import (
    count_three_tag, calibrate_three_tag_efficiencies,
    extract_rb_three_tag, toy_uncertainty_three_tag,
    R_B_SM, R_C_SM, R_UDS_SM,
)

PION_MASS = 0.13957  # GeV/c^2


def exp_label_data(ax):
    """Add ALEPH Open Data experiment label."""
    mh.label.exp_label(
        exp="ALEPH", data=True, llabel="Open Data",
        rlabel=r"$\sqrt{s} = 91.2$ GeV", ax=ax,
    )


def exp_label_mc(ax):
    """Add ALEPH Open Simulation experiment label."""
    mh.label.exp_label(
        exp="ALEPH", data=True, llabel="Open Simulation",
        rlabel=r"$\sqrt{s} = 91.2$ GeV", ax=ax,
    )


# ============================================================================
# Step 1 + 2 + 3: SV reconstruction per hemisphere
# ============================================================================


def compute_sv_properties(
    signed_sig, d0, px, py, pz, pmag, theta, phi,
    offsets, hem, sigma_d0,
    sig_threshold=2.0,
):
    """Compute secondary vertex properties per hemisphere.

    For each hemisphere with >= 2 displaced tracks (signed_sig > threshold):
    - Vertex mass: invariant mass of displaced tracks (pion hypothesis)
    - Track multiplicity: number of displaced tracks
    - Flight distance proxy: weighted mean |d0| of displaced tracks
    - Flight significance: flight distance / uncertainty
    - Vertex pT: transverse momentum of vertex

    Returns dict with arrays of shape (n_events,) for h0 and h1.
    """
    n_events = len(offsets) - 1
    n_hems = 2 * n_events

    # Event index for each track
    event_idx = np.repeat(np.arange(n_events), np.diff(offsets))
    hem_evt_idx = 2 * event_idx + hem.astype(np.int64)

    # Displaced track mask
    disp_mask = signed_sig > sig_threshold

    # 4-vectors for displaced tracks (pion mass hypothesis)
    E = np.sqrt(pmag**2 + PION_MASS**2)
    px_trk = pmag * np.sin(theta) * np.cos(phi)
    py_trk = pmag * np.sin(theta) * np.sin(phi)
    pz_trk = pmag * np.cos(theta)

    # --- Vertex mass (invariant mass of displaced tracks) ---
    sum_E = np.zeros(n_hems)
    sum_px = np.zeros(n_hems)
    sum_py = np.zeros(n_hems)
    sum_pz = np.zeros(n_hems)

    disp_idx = hem_evt_idx[disp_mask]
    np.add.at(sum_E, disp_idx, E[disp_mask])
    np.add.at(sum_px, disp_idx, px_trk[disp_mask])
    np.add.at(sum_py, disp_idx, py_trk[disp_mask])
    np.add.at(sum_pz, disp_idx, pz_trk[disp_mask])

    m2 = sum_E**2 - sum_px**2 - sum_py**2 - sum_pz**2
    sv_mass = np.sqrt(np.maximum(m2, 0.0))

    # --- Track multiplicity ---
    sv_ntrk = np.zeros(n_hems, dtype=np.int32)
    np.add.at(sv_ntrk, disp_idx, 1)

    # --- Flight distance estimate ---
    # Use weighted average of |d0| as proxy for flight distance.
    # For tracks from a common SV, d0 ~ L * sin(angle).
    sum_d0_w = np.zeros(n_hems)
    sum_w = np.zeros(n_hems)

    abs_d0_disp = np.abs(d0[disp_mask])
    w_disp = 1.0 / np.maximum(sigma_d0[disp_mask], 1e-6)**2

    np.add.at(sum_d0_w, disp_idx, abs_d0_disp * w_disp)
    np.add.at(sum_w, disp_idx, w_disp)

    safe_w = np.maximum(sum_w, 1e-30)
    sv_flight = sum_d0_w / safe_w  # cm
    sigma_flight = 1.0 / np.sqrt(safe_w)
    sv_flight_sig = sv_flight / np.maximum(sigma_flight, 1e-10)

    # --- Vertex pT ---
    sv_pt = np.sqrt(sum_px**2 + sum_py**2)

    # --- Only keep hemispheres with >= 2 displaced tracks ---
    no_sv = sv_ntrk < 2
    sv_mass[no_sv] = 0.0
    sv_flight[no_sv] = 0.0
    sv_flight_sig[no_sv] = 0.0
    sv_pt[no_sv] = 0.0

    return {
        "sv_mass_h0": sv_mass[0::2],
        "sv_mass_h1": sv_mass[1::2],
        "sv_ntrk_h0": sv_ntrk[0::2],
        "sv_ntrk_h1": sv_ntrk[1::2],
        "sv_flight_h0": sv_flight[0::2],
        "sv_flight_h1": sv_flight[1::2],
        "sv_flight_sig_h0": sv_flight_sig[0::2],
        "sv_flight_sig_h1": sv_flight_sig[1::2],
        "sv_pt_h0": sv_pt[0::2],
        "sv_pt_h1": sv_pt[1::2],
    }


def build_sv_discriminant(sv_props):
    """Build a combined SV discriminant from vertex properties.

    The discriminant combines:
    - Vertex mass: b hadrons ~ 3-5 GeV, c hadrons ~ 1-2 GeV
    - Track multiplicity: b ~ 4-5, c ~ 2-3
    - Flight significance: b ~ 10+, c ~ 5

    Combined as a simple linear combination:
      D = w_mass * mass_score + w_ntrk * ntrk_score + w_flight * flight_score

    Scaled to [0, ~10] for compatibility with existing threshold system.
    """
    mass_h0 = sv_props["sv_mass_h0"]
    mass_h1 = sv_props["sv_mass_h1"]
    ntrk_h0 = sv_props["sv_ntrk_h0"]
    ntrk_h1 = sv_props["sv_ntrk_h1"]
    flight_h0 = sv_props["sv_flight_sig_h0"]
    flight_h1 = sv_props["sv_flight_sig_h1"]

    # Mass score: higher mass -> more b-like, saturate at 8 GeV
    mass_score_h0 = np.minimum(mass_h0, 8.0) / 8.0
    mass_score_h1 = np.minimum(mass_h1, 8.0) / 8.0

    # Multiplicity score: more tracks -> more b-like, saturate at 8
    ntrk_score_h0 = np.minimum(ntrk_h0.astype(float), 8.0) / 8.0
    ntrk_score_h1 = np.minimum(ntrk_h1.astype(float), 8.0) / 8.0

    # Flight significance score: log scale, saturate at 30
    flight_score_h0 = np.log1p(np.minimum(flight_h0, 30.0)) / np.log1p(30.0)
    flight_score_h1 = np.log1p(np.minimum(flight_h1, 30.0)) / np.log1p(30.0)

    # Weights: mass most discriminating, then multiplicity, then flight
    w_mass = 3.0
    w_ntrk = 2.0
    w_flight = 1.0
    w_total = w_mass + w_ntrk + w_flight

    disc_h0 = (w_mass * mass_score_h0 + w_ntrk * ntrk_score_h0 +
               w_flight * flight_score_h0) / w_total * 10.0
    disc_h1 = (w_mass * mass_score_h1 + w_ntrk * ntrk_score_h1 +
               w_flight * flight_score_h1) / w_total * 10.0

    return disc_h0, disc_h1


def build_combined_tag(sv_disc_h0, sv_disc_h1, old_h0, old_h1,
                       w_sv=0.5, w_old=0.5):
    """Combine SV discriminant with existing d0-significance tag.

    Normalizes old tag to same scale as SV tag (~0-10), then weighted sum.
    """
    old_p99 = max(np.percentile(old_h0[old_h0 > 0], 99),
                  np.percentile(old_h1[old_h1 > 0], 99), 1.0)
    old_norm_h0 = old_h0 / old_p99 * 10.0
    old_norm_h1 = old_h1 / old_p99 * 10.0

    combined_h0 = w_sv * sv_disc_h0 + w_old * old_norm_h0
    combined_h1 = w_sv * sv_disc_h1 + w_old * old_norm_h1
    return combined_h0, combined_h1


# ============================================================================
# Efficiency scan using algebraic calibration
# ============================================================================


def scan_calibrated_efficiencies(h0, h1, thresholds_tight, thr_loose_offset=3.0):
    """Scan working points and compute algebraic eps_b, eps_c, eps_uds.

    Since we lack MC truth, we use the 3-tag algebraic calibration to
    infer per-flavor efficiencies from the observed tag fractions and
    known SM R_b, R_c values.

    Returns list of dicts with eps_b, eps_c, eps_uds at each WP.
    """
    results = []
    for thr_t in thresholds_tight:
        thr_l = thr_t - thr_loose_offset
        if thr_l <= 0:
            continue
        counts = count_three_tag(h0, h1, thr_t, thr_l)
        cal = calibrate_three_tag_efficiencies(counts, R_B_SM, R_C_SM)

        eps_b = cal.get("eps_b_tight", 0.0)
        eps_c = cal.get("eps_c_tight", 0.0)
        eps_uds = cal.get("eps_uds_tight", 0.0)
        ratio = eps_c / max(eps_b, 1e-10) if eps_b > 0.001 else float('nan')

        results.append({
            "thr_tight": float(thr_t),
            "thr_loose": float(thr_l),
            "f_s_tight": counts["f_s_tight"],
            "eps_b_tight": eps_b,
            "eps_c_tight": eps_c,
            "eps_uds_tight": eps_uds,
            "eps_c_over_eps_b": ratio,
        })

    return results


# ============================================================================
# A_FB^b extraction
# ============================================================================

PUBLISHED_DELTA = {2.0: 0.2397, 3.0: 0.2478, 4.0: 0.2553}


def compute_afb_sv_tagged(cos_theta, jet_charge_h0, jet_charge_h1,
                           sv_tag_h0, sv_tag_h1, thr_sv,
                           n_bins=10, cos_range=0.9):
    """Compute A_FB^b in SV-tagged events.

    Selects events where both hemispheres pass SV tag threshold.
    Fits <Q_FB> vs cos_theta to extract slope = 8/3 * A_FB^b * delta_b.
    """
    double_tagged = (sv_tag_h0 > thr_sv) & (sv_tag_h1 > thr_sv)
    n_dt = int(np.sum(double_tagged))

    if n_dt < 100:
        log.warning("Only %d double-tagged events for AFB, skipping", n_dt)
        return None

    cos = cos_theta[double_tagged]
    qh0 = jet_charge_h0[double_tagged]
    qh1 = jet_charge_h1[double_tagged]

    # Q_FB = Q_F - Q_B (forward hemisphere defined by cos > 0)
    q_fb = np.where(cos > 0, qh0 - qh1, qh1 - qh0)

    abs_cos = np.abs(cos)
    bin_edges = np.linspace(0, cos_range, n_bins + 1)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    mean_qfb = np.zeros(n_bins)
    err_qfb = np.zeros(n_bins)
    n_per_bin = np.zeros(n_bins, dtype=int)

    for i in range(n_bins):
        mask = (abs_cos >= bin_edges[i]) & (abs_cos < bin_edges[i + 1])
        n_in = int(np.sum(mask))
        n_per_bin[i] = n_in
        if n_in > 1:
            mean_qfb[i] = np.mean(q_fb[mask])
            err_qfb[i] = np.std(q_fb[mask]) / np.sqrt(n_in)

    valid = n_per_bin > 10
    if np.sum(valid) < 3:
        return None

    x = bin_centers[valid]
    y = mean_qfb[valid]
    w = 1.0 / np.maximum(err_qfb[valid], 1e-10)**2

    # Weighted linear fit through origin: y = slope * x
    slope = np.sum(w * x * y) / np.sum(w * x**2)
    slope_err = 1.0 / np.sqrt(np.sum(w * x**2))

    return {
        "n_double_tagged": n_dt,
        "slope": float(slope),
        "slope_err": float(slope_err),
        "bin_centers": bin_centers.tolist(),
        "mean_qfb": mean_qfb.tolist(),
        "err_qfb": err_qfb.tolist(),
        "n_per_bin": n_per_bin.tolist(),
    }


# ============================================================================
# Plotting
# ============================================================================


def plot_sv_distributions(data_sv, mc_sv, figdir):
    """Plot SV property distributions for data vs MC."""
    properties = [
        ("sv_mass_h0", "SV Mass [GeV]", np.linspace(0, 10, 51)),
        ("sv_ntrk_h0", "SV Track Multiplicity", np.arange(-0.5, 12.5, 1.0)),
        ("sv_flight_h0", "Flight Distance Proxy [cm]", np.linspace(0, 0.5, 51)),
        ("sv_flight_sig_h0", "Flight Significance", np.linspace(0, 30, 51)),
    ]

    for varname, xlabel, bins in properties:
        fig, (ax_main, ax_ratio) = plt.subplots(
            2, 1, figsize=(10, 10), height_ratios=[3, 1],
            sharex=True, gridspec_kw={"hspace": 0.05},
        )

        mc_vals = mc_sv[varname]
        data_vals = data_sv[varname]

        has_sv_mc = mc_vals > 0
        has_sv_data = data_vals > 0

        n_data_sv = int(np.sum(has_sv_data))
        n_mc_sv = int(np.sum(has_sv_mc))
        mc_scale = n_data_sv / max(n_mc_sv, 1)

        # MC histogram (scaled to data)
        h_mc, _ = np.histogram(mc_vals[has_sv_mc], bins=bins)
        h_mc_scaled = h_mc * mc_scale

        # Data as points
        h_data, _ = np.histogram(data_vals[has_sv_data], bins=bins)
        bin_centers = 0.5 * (bins[:-1] + bins[1:])
        bin_widths = np.diff(bins)

        ax_main.bar(bin_centers, h_mc_scaled, width=bin_widths,
                     alpha=0.6, color="#1f77b4", label="MC (scaled)")
        ax_main.errorbar(bin_centers, h_data,
                         yerr=np.sqrt(np.maximum(h_data, 1)),
                         fmt="ko", markersize=4, label="Data")

        ax_main.set_ylabel("Hemispheres")
        ax_main.legend(loc="upper right", fontsize=12)
        exp_label_data(ax_main)

        # Ratio
        ratio = np.where(h_mc_scaled > 0, h_data / h_mc_scaled, 1.0)
        ratio_err = np.where(h_mc_scaled > 0,
                             np.sqrt(np.maximum(h_data, 1)) / h_mc_scaled, 0.0)
        ax_ratio.errorbar(bin_centers, ratio, yerr=ratio_err,
                          fmt="ko", markersize=4)
        ax_ratio.axhline(1.0, color="gray", linestyle="--", linewidth=0.8)
        ax_ratio.set_xlabel(xlabel)
        ax_ratio.set_ylabel("Data / MC")
        ax_ratio.set_ylim(0.5, 1.5)

        safe_varname = varname.replace("_h0", "")
        fig.savefig(figdir / f"sv_{safe_varname}_dist.png",
                    dpi=150, bbox_inches="tight")
        plt.close(fig)
        log.info("  Saved sv_%s_dist.png", safe_varname)


def plot_sv_discriminant(data_disc_h0, mc_disc_h0, figdir):
    """Plot SV discriminant distribution."""
    fig, ax = plt.subplots(figsize=(10, 10))

    bins = np.linspace(0, 10, 51)
    has_sv_data = data_disc_h0 > 0
    has_sv_mc = mc_disc_h0 > 0

    n_data_sv = int(np.sum(has_sv_data))
    n_mc_sv = int(np.sum(has_sv_mc))
    mc_scale = n_data_sv / max(n_mc_sv, 1)

    h_mc, _ = np.histogram(mc_disc_h0[has_sv_mc], bins=bins)
    h_data, _ = np.histogram(data_disc_h0[has_sv_data], bins=bins)
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    bin_widths = np.diff(bins)

    ax.bar(bin_centers, h_mc * mc_scale, width=bin_widths,
           alpha=0.6, color="#1f77b4", label="MC (scaled)")
    ax.errorbar(bin_centers, h_data,
                yerr=np.sqrt(np.maximum(h_data, 1)),
                fmt="ko", markersize=4, label="Data")

    ax.set_xlabel("SV Discriminant")
    ax.set_ylabel("Hemispheres")
    ax.legend(fontsize=12)
    ax.set_yscale("log")
    exp_label_data(ax)

    fig.savefig(figdir / "sv_discriminant_dist.png",
                dpi=150, bbox_inches="tight")
    plt.close(fig)
    log.info("  Saved sv_discriminant_dist.png")


def plot_efficiency_scan(scan_old, scan_sv, scan_combined, figdir):
    """Plot eps_c/eps_b vs eps_b for different tags."""
    fig, ax = plt.subplots(figsize=(10, 10))

    for label, scan, color, marker in [
        ("Current (d0 sig + mass)", scan_old, "#1f77b4", "o"),
        ("SV discriminant", scan_sv, "#d62728", "s"),
        ("SV + current combined", scan_combined, "#2ca02c", "^"),
    ]:
        eps_b = [r["eps_b_tight"] for r in scan if not np.isnan(r["eps_c_over_eps_b"])]
        ratio = [r["eps_c_over_eps_b"] for r in scan if not np.isnan(r["eps_c_over_eps_b"])]
        if eps_b:
            ax.plot(eps_b, ratio, f"-{marker}", color=color, markersize=5, label=label)

    ax.set_xlabel(r"$\varepsilon_b^{\mathrm{tight}}$ (from calibration)")
    ax.set_ylabel(r"$\varepsilon_c^{\mathrm{tight}} / \varepsilon_b^{\mathrm{tight}}$")
    ax.set_yscale("log")
    ax.set_ylim(0.01, 2.0)
    ax.set_xlim(0, 0.8)
    ax.axhline(0.1, color="gray", linestyle=":", linewidth=0.8,
               label=r"ALEPH target $\varepsilon_c/\varepsilon_b = 0.1$")
    ax.legend(fontsize=11)
    exp_label_mc(ax)

    fig.savefig(figdir / "sv_efficiency_scan.png",
                dpi=150, bbox_inches="tight")
    plt.close(fig)
    log.info("  Saved sv_efficiency_scan.png")


def plot_afb_fit(afb_result, figdir, label="sv"):
    """Plot A_FB fit: <Q_FB> vs cos_theta."""
    if afb_result is None:
        return

    fig, ax = plt.subplots(figsize=(10, 10))

    x = np.array(afb_result["bin_centers"])
    y = np.array(afb_result["mean_qfb"])
    yerr = np.array(afb_result["err_qfb"])
    valid = np.array(afb_result["n_per_bin"]) > 10

    ax.errorbar(x[valid], y[valid], yerr=yerr[valid],
                fmt="ko", markersize=5, label="Data")

    slope = afb_result["slope"]
    x_fit = np.linspace(0, 0.9, 100)
    ax.plot(x_fit, slope * x_fit, "r-", linewidth=2,
            label=rf"Fit: slope = {slope:.4f} $\pm$ {afb_result['slope_err']:.4f}")

    ax.set_xlabel(r"$|\cos\theta_{\mathrm{thrust}}|$")
    ax.set_ylabel(r"$\langle Q_{\mathrm{FB}} \rangle$")
    ax.legend(fontsize=12)
    ax.axhline(0, color="gray", linestyle="--", linewidth=0.8)
    exp_label_data(ax)

    fig.savefig(figdir / f"sv_afb_fit_{label}.png",
                dpi=150, bbox_inches="tight")
    plt.close(fig)
    log.info("  Saved sv_afb_fit_%s.png", label)


def plot_rb_comparison(sv_results, old_rb, old_sigma, figdir):
    """Plot R_b from SV tag vs current method."""
    valid = [r for r in sv_results
             if r["sigma_stat"] is not None and r["sigma_stat"] > 0
             and 0.05 < r["R_b"] < 0.50]
    if not valid:
        return

    fig, ax = plt.subplots(figsize=(10, 10))

    labels = [r["label"].replace("SV ", "") for r in valid]
    rb_vals = [r["R_b"] for r in valid]
    rb_errs = [r["sigma_stat"] for r in valid]

    y_pos = np.arange(len(valid))
    ax.errorbar(rb_vals, y_pos, xerr=rb_errs, fmt="ro", markersize=6,
                label="SV-enhanced tag")
    ax.axvline(R_B_SM, color="gray", linestyle="--", linewidth=1.0,
               label=f"SM $R_b$ = {R_B_SM:.5f}")
    ax.axvline(old_rb, color="blue", linestyle="-.", linewidth=1.0,
               label=f"Current $R_b$ = {old_rb:.4f}")
    ax.axvspan(old_rb - old_sigma, old_rb + old_sigma,
               alpha=0.15, color="blue")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel(r"$R_b$")
    ax.legend(fontsize=11, loc="upper right")
    exp_label_data(ax)

    fig.savefig(figdir / "sv_rb_comparison.png",
                dpi=150, bbox_inches="tight")
    plt.close(fig)
    log.info("  Saved sv_rb_comparison.png")


# ============================================================================
# Main
# ============================================================================


def main():
    t0 = time.time()
    log.info("=" * 60)
    log.info("Phase 4c: Secondary Vertex Reconstruction")
    log.info("Session: felix_91e9")
    log.info("=" * 60)

    # ================================================================
    # Load data
    # ================================================================
    log.info("\n--- Loading data ---")
    data = np.load(P3_OUT / "preselected_data.npz", allow_pickle=False)
    mc = np.load(P3_OUT / "preselected_mc.npz", allow_pickle=False)
    signed = np.load(P3_OUT / "signed_d0.npz", allow_pickle=False)
    d0sig = np.load(P3_OUT / "d0_significance.npz", allow_pickle=False)
    tags = np.load(P3_OUT / "hemisphere_tags.npz", allow_pickle=False)

    n_data = len(data["bflag"])
    n_mc = len(mc["bflag"])
    log.info("Data events: %d", n_data)
    log.info("MC events: %d", n_mc)
    log.info("Data tracks (selected): %d", len(data["trk_d0"]))
    log.info("MC tracks (selected): %d", len(mc["trk_d0"]))

    # ================================================================
    # Step 1-3: Compute SV properties for data and MC
    # ================================================================
    log.info("\n--- Step 1-3: Computing SV properties ---")

    sv_results = {}
    for prefix, sample, sig_key, d0_key, sigma_key in [
        ("data", data, "data_signed_sig", "data_d0", "data_sigma_d0"),
        ("mc", mc, "mc_signed_sig", "mc_d0", "mc_sigma_d0"),
    ]:
        log.info("Processing %s...", prefix)
        sv = compute_sv_properties(
            signed_sig=signed[sig_key],
            d0=d0sig[d0_key],
            px=sample["trk_px"],
            py=sample["trk_py"],
            pz=sample["trk_pz"],
            pmag=sample["trk_pmag"],
            theta=sample["trk_theta"],
            phi=sample["trk_phi"],
            offsets=sample["trk_d0_offsets"],
            hem=sample["trk_hem"],
            sigma_d0=d0sig[sigma_key],
            sig_threshold=2.0,
        )

        for k, v in sv.items():
            sv_results[f"{prefix}_{k}"] = v

        n_hems_with_sv = int(np.sum(sv["sv_ntrk_h0"] >= 2) +
                             np.sum(sv["sv_ntrk_h1"] >= 2))
        n_hems_total = 2 * len(sv["sv_ntrk_h0"])
        log.info("  SV found in %d / %d hemispheres (%.1f%%)",
                 n_hems_with_sv, n_hems_total,
                 100.0 * n_hems_with_sv / n_hems_total)

        has_sv = sv["sv_ntrk_h0"] >= 2
        if np.sum(has_sv) > 0:
            log.info("  SV mass (h0, has SV): mean=%.3f, median=%.3f GeV",
                     np.mean(sv["sv_mass_h0"][has_sv]),
                     np.median(sv["sv_mass_h0"][has_sv]))
            log.info("  SV ntrk (h0, has SV): mean=%.1f",
                     np.mean(sv["sv_ntrk_h0"][has_sv]))
            log.info("  SV flight proxy (h0, has SV): mean=%.4f cm",
                     np.mean(sv["sv_flight_h0"][has_sv]))

    # ================================================================
    # Build SV discriminant
    # ================================================================
    log.info("\n--- Step 4: Building SV discriminant ---")

    data_sv = {k.replace("data_", ""): v
               for k, v in sv_results.items() if k.startswith("data_")}
    mc_sv = {k.replace("mc_", ""): v
             for k, v in sv_results.items() if k.startswith("mc_")}

    data_disc_h0, data_disc_h1 = build_sv_discriminant(data_sv)
    mc_disc_h0, mc_disc_h1 = build_sv_discriminant(mc_sv)

    has_sv_data = data_disc_h0 > 0
    has_sv_mc = mc_disc_h0 > 0
    log.info("SV discriminant: data h0 mean=%.3f (N=%d), mc h0 mean=%.3f (N=%d)",
             np.mean(data_disc_h0[has_sv_data]), int(np.sum(has_sv_data)),
             np.mean(mc_disc_h0[has_sv_mc]), int(np.sum(has_sv_mc)))

    # ================================================================
    # Efficiency scan using algebraic calibration (no truth needed)
    # ================================================================
    log.info("\n--- Efficiency scan (algebraic calibration) ---")

    # Scan on MC: old tag
    thresholds_tight = np.arange(2.0, 14.0, 0.5).tolist()
    scan_old_mc = scan_calibrated_efficiencies(
        tags["mc_combined_h0"], tags["mc_combined_h1"],
        thresholds_tight, thr_loose_offset=3.0)

    # Scan on MC: SV tag
    sv_thresholds = np.arange(1.0, 9.0, 0.25).tolist()
    scan_sv_mc = scan_calibrated_efficiencies(
        mc_disc_h0, mc_disc_h1,
        sv_thresholds, thr_loose_offset=1.5)

    # Combined tag
    mc_comb_h0, mc_comb_h1 = build_combined_tag(
        mc_disc_h0, mc_disc_h1,
        tags["mc_combined_h0"], tags["mc_combined_h1"])
    comb_thresholds = np.arange(1.0, 10.0, 0.25).tolist()
    scan_comb_mc = scan_calibrated_efficiencies(
        mc_comb_h0, mc_comb_h1,
        comb_thresholds, thr_loose_offset=2.0)

    # Report key working points
    log.info("\n--- eps_c/eps_b at key working points (MC calibration) ---")
    for label, scan in [("Old tag", scan_old_mc), ("SV tag", scan_sv_mc),
                        ("Combined", scan_comb_mc)]:
        valid_scan = [r for r in scan
                      if 0.001 < r["eps_b_tight"] < 0.8
                      and not np.isnan(r["eps_c_over_eps_b"])]
        if valid_scan:
            # Find WP closest to eps_b = 0.3
            best_030 = min(valid_scan,
                           key=lambda r: abs(r["eps_b_tight"] - 0.30))
            log.info("  %s @ eps_b~0.30: eps_b=%.3f, eps_c=%.4f, "
                     "eps_c/eps_b=%.4f (thr=%.1f/%.1f)",
                     label, best_030["eps_b_tight"], best_030["eps_c_tight"],
                     best_030["eps_c_over_eps_b"],
                     best_030["thr_tight"], best_030["thr_loose"])
            # Also at eps_b ~ 0.5
            best_050 = min(valid_scan,
                           key=lambda r: abs(r["eps_b_tight"] - 0.50))
            log.info("  %s @ eps_b~0.50: eps_b=%.3f, eps_c=%.4f, "
                     "eps_c/eps_b=%.4f (thr=%.1f/%.1f)",
                     label, best_050["eps_b_tight"], best_050["eps_c_tight"],
                     best_050["eps_c_over_eps_b"],
                     best_050["thr_tight"], best_050["thr_loose"])

    # ================================================================
    # Plots
    # ================================================================
    log.info("\n--- Generating plots ---")
    plot_sv_distributions(data_sv, mc_sv, FIG_DIR)
    plot_sv_discriminant(data_disc_h0, mc_disc_h0, FIG_DIR)
    plot_efficiency_scan(scan_old_mc, scan_sv_mc, scan_comb_mc, FIG_DIR)

    # ================================================================
    # Step 5: R_b extraction with SV-enhanced tag
    # ================================================================
    log.info("\n--- Step 5: R_b extraction with SV-enhanced tag ---")

    # Build combined tag for data
    data_comb_h0, data_comb_h1 = build_combined_tag(
        data_disc_h0, data_disc_h1,
        tags["data_combined_h0"], tags["data_combined_h1"])

    # Threshold configurations for the combined SV tag
    sv_tag_configs = [
        (3.0, 1.5), (4.0, 2.0), (5.0, 2.5), (5.0, 3.0),
        (6.0, 3.0), (6.0, 4.0), (7.0, 3.5), (7.0, 4.0),
        (8.0, 4.0), (8.0, 5.0),
    ]

    C_B_SF = 1.0
    N_TOYS = 500
    TOY_SEED = 99999

    sv_rb_results = []
    for thr_tight, thr_loose in sv_tag_configs:
        label = "SV tight=%.1f, loose=%.1f" % (thr_tight, thr_loose)

        # MC calibration
        counts_mc = count_three_tag(mc_comb_h0, mc_comb_h1,
                                     thr_tight, thr_loose)
        cal_mc = calibrate_three_tag_efficiencies(counts_mc, R_B_SM, R_C_SM)

        # Data counts
        counts_data = count_three_tag(data_comb_h0, data_comb_h1,
                                       thr_tight, thr_loose)

        # Scale factors
        sf_tight = counts_data["f_s_tight"] / max(counts_mc["f_s_tight"], 1e-10)
        sf_loose = counts_data["f_s_loose"] / max(counts_mc["f_s_loose"], 1e-10)
        sf_anti = counts_data["f_s_anti"] / max(counts_mc["f_s_anti"], 1e-10)

        # SF-corrected calibration with renormalization
        cal_sf = {}
        for q in ["b", "c", "uds"]:
            et = cal_mc.get(f"eps_{q}_tight", 0) * sf_tight
            el = cal_mc.get(f"eps_{q}_loose", 0) * sf_loose
            ea = cal_mc.get(f"eps_{q}_anti", 0) * sf_anti
            tot = et + el + ea
            if tot > 0:
                cal_sf[f"eps_{q}_tight"] = float(et / tot)
                cal_sf[f"eps_{q}_loose"] = float(el / tot)
                cal_sf[f"eps_{q}_anti"] = float(ea / tot)
            else:
                cal_sf[f"eps_{q}_tight"] = cal_mc.get(f"eps_{q}_tight", 0)
                cal_sf[f"eps_{q}_loose"] = cal_mc.get(f"eps_{q}_loose", 0)
                cal_sf[f"eps_{q}_anti"] = cal_mc.get(f"eps_{q}_anti", 0)

        # Extract R_b
        extraction = extract_rb_three_tag(
            counts_data, cal_sf, R_C_SM, C_b_tight=C_B_SF)

        # Toy uncertainty
        rb_mean, rb_sigma, _, n_valid = toy_uncertainty_three_tag(
            data_comb_h0, data_comb_h1, thr_tight, thr_loose,
            cal_sf, R_C_SM, n_toys=N_TOYS, seed=TOY_SEED)

        eps_c_over_b = cal_mc.get("eps_c_tight", 0) / max(
            cal_mc.get("eps_b_tight", 1e-10), 1e-10)

        log.info(
            "%s: R_b=%.5f +/- %.5f, eps_c/eps_b=%.4f, "
            "SF_t=%.3f, SF_l=%.3f",
            label, extraction["R_b"],
            rb_sigma if not np.isnan(rb_sigma) else 0.0,
            eps_c_over_b, sf_tight, sf_loose,
        )

        sv_rb_results.append({
            "thr_tight": float(thr_tight),
            "thr_loose": float(thr_loose),
            "label": label,
            "R_b": extraction["R_b"],
            "sigma_stat": float(rb_sigma) if not np.isnan(rb_sigma) else None,
            "chi2": extraction["chi2"],
            "ndf": extraction["ndf"],
            "p_value": extraction["p_value"],
            "eps_b_tight": cal_mc.get("eps_b_tight"),
            "eps_c_tight": cal_mc.get("eps_c_tight"),
            "eps_c_over_eps_b": eps_c_over_b,
            "scale_factors": {
                "sf_tight": float(sf_tight),
                "sf_loose": float(sf_loose),
                "sf_anti": float(sf_anti),
            },
        })

    # Best result
    valid_sv = [r for r in sv_rb_results
                if r["sigma_stat"] is not None and r["sigma_stat"] > 0
                and 0.05 < r["R_b"] < 0.50]

    if valid_sv:
        best_sv = min(valid_sv, key=lambda x: x["sigma_stat"])
        log.info("\n--- Best SV Configuration ---")
        log.info("Config: %s", best_sv["label"])
        log.info("R_b = %.5f +/- %.5f", best_sv["R_b"], best_sv["sigma_stat"])
        log.info("eps_c/eps_b = %.4f", best_sv["eps_c_over_eps_b"])
        log.info("SM R_b = %.5f", R_B_SM)

        # Stability
        rb_vals = np.array([r["R_b"] for r in valid_sv])
        rb_errs = np.array([r["sigma_stat"] for r in valid_sv])
        w = 1.0 / rb_errs**2
        rb_sv_combined = float(np.sum(w * rb_vals) / np.sum(w))
        sigma_sv_combined = float(1.0 / np.sqrt(np.sum(w)))
        chi2_stab = float(np.sum((rb_vals - rb_sv_combined)**2 / rb_errs**2))
        ndf_stab = len(valid_sv) - 1
        p_stab = float(1.0 - chi2_dist.cdf(chi2_stab, ndf_stab)) if ndf_stab > 0 else 1.0

        log.info("\n--- SV Tag Stability ---")
        log.info("Combined R_b = %.5f +/- %.5f", rb_sv_combined, sigma_sv_combined)
        log.info("chi2/ndf = %.2f/%d, p = %.4f", chi2_stab, ndf_stab, p_stab)
    else:
        best_sv = None
        rb_sv_combined = None
        sigma_sv_combined = None
        chi2_stab, ndf_stab, p_stab = 0.0, 0, 1.0
        log.warning("No valid SV-based R_b extraction!")

    # Comparison with current mass-cut result
    log.info("\n--- Comparison with current result ---")
    rb_current = 0.2150
    sigma_current = 0.0004
    if best_sv:
        pull = abs(best_sv["R_b"] - rb_current) / np.sqrt(
            best_sv["sigma_stat"]**2 + sigma_current**2)
        log.info("Current R_b = %.5f +/- %.5f", rb_current, sigma_current)
        log.info("SV R_b = %.5f +/- %.5f", best_sv["R_b"], best_sv["sigma_stat"])
        log.info("Pull = %.2f", pull)

    # Plot R_b comparison
    plot_rb_comparison(sv_rb_results, rb_current, sigma_current, FIG_DIR)

    # ================================================================
    # Step 6: A_FB^b with SV tag
    # ================================================================
    log.info("\n--- Step 6: A_FB^b with SV tag ---")

    try:
        jc = np.load(P3_OUT / "jet_charge.npz", allow_pickle=False)
        has_jc = True
        log.info("Loaded jet charge data")
    except FileNotFoundError:
        has_jc = False
        log.warning("jet_charge.npz not found, skipping AFB")

    afb_results = {}
    if has_jc:
        cos_theta = data["cos_theta_thrust"]

        # Jet charge keys: data_qh_h0_k{kappa}, data_qh_h1_k{kappa}
        for kappa_str in ["2.0"]:
            h0_key = f"data_qh_h0_k{kappa_str}"
            h1_key = f"data_qh_h1_k{kappa_str}"

            if h0_key not in jc.files:
                log.warning("  jet charge key %s not found", h0_key)
                continue

            jc_h0 = jc[h0_key]
            jc_h1 = jc[h1_key]

            # SV discriminant double-tag
            for sv_thr_label, sv_thr in [("loose", 1.5), ("medium", 3.0),
                                          ("tight", 5.0)]:
                afb = compute_afb_sv_tagged(
                    cos_theta, jc_h0, jc_h1,
                    data_disc_h0, data_disc_h1, sv_thr,
                )
                if afb is not None:
                    kappa = float(kappa_str)
                    delta_b = PUBLISHED_DELTA.get(kappa, 0.24)
                    afb_b = afb["slope"] / (8.0 / 3.0 * delta_b)
                    afb_b_err = afb["slope_err"] / (8.0 / 3.0 * delta_b)

                    log.info("  kappa=%.1f, SV>%.1f: slope=%.4f+/-%.4f, "
                             "A_FB^b=%.4f+/-%.4f (n_dt=%d)",
                             kappa, sv_thr, afb["slope"], afb["slope_err"],
                             afb_b, afb_b_err, afb["n_double_tagged"])

                    key = f"kappa{kappa_str}_sv{sv_thr_label}"
                    afb_results[key] = {
                        **afb,
                        "kappa": kappa,
                        "sv_threshold": sv_thr,
                        "delta_b": delta_b,
                        "A_FB_b": float(afb_b),
                        "A_FB_b_err": float(afb_b_err),
                        "tag_type": "sv_only",
                    }
                    plot_afb_fit(afb, FIG_DIR,
                                 label=f"kappa{kappa_str}_sv{sv_thr_label}")

            # Combined SV+old tag double-tag
            for sv_thr_label, sv_thr in [("medium", 3.0), ("tight", 5.0)]:
                afb = compute_afb_sv_tagged(
                    cos_theta, jc_h0, jc_h1,
                    data_comb_h0, data_comb_h1, sv_thr,
                )
                if afb is not None:
                    kappa = float(kappa_str)
                    delta_b = PUBLISHED_DELTA.get(kappa, 0.24)
                    afb_b = afb["slope"] / (8.0 / 3.0 * delta_b)
                    afb_b_err = afb["slope_err"] / (8.0 / 3.0 * delta_b)

                    log.info("  kappa=%.1f, Comb>%.1f: slope=%.4f+/-%.4f, "
                             "A_FB^b=%.4f+/-%.4f (n_dt=%d)",
                             kappa, sv_thr, afb["slope"], afb["slope_err"],
                             afb_b, afb_b_err, afb["n_double_tagged"])

                    key = f"kappa{kappa_str}_comb{sv_thr_label}"
                    afb_results[key] = {
                        **afb,
                        "kappa": kappa,
                        "sv_threshold": sv_thr,
                        "delta_b": delta_b,
                        "A_FB_b": float(afb_b),
                        "A_FB_b_err": float(afb_b_err),
                        "tag_type": "combined",
                    }
                    plot_afb_fit(afb, FIG_DIR,
                                 label=f"kappa{kappa_str}_comb{sv_thr_label}")

    # ================================================================
    # Save results
    # ================================================================
    log.info("\n--- Saving results ---")

    # Save SV tags
    sv_tag_arrays = {
        "data_sv_disc_h0": data_disc_h0,
        "data_sv_disc_h1": data_disc_h1,
        "mc_sv_disc_h0": mc_disc_h0,
        "mc_sv_disc_h1": mc_disc_h1,
        "data_sv_combined_h0": data_comb_h0,
        "data_sv_combined_h1": data_comb_h1,
        "mc_sv_combined_h0": mc_comb_h0,
        "mc_sv_combined_h1": mc_comb_h1,
    }
    for k, v in sv_results.items():
        sv_tag_arrays[k] = v

    np.savez_compressed(PHASE4C_OUT / "sv_tags.npz", **sv_tag_arrays)
    log.info("Saved sv_tags.npz")

    # JSON results
    output = {
        "method": "Secondary vertex reconstruction for b/c separation",
        "description": (
            "SV reconstruction from displaced tracks (signed d0 significance > 2) "
            "per hemisphere. SV properties (vertex mass, track multiplicity, "
            "flight distance proxy) combined into a discriminant. "
            "R_b extracted using 3-tag system with SV-enhanced combined tag. "
            "eps_c/eps_b evaluated via algebraic calibration (no MC truth flavor available)."
        ),
        "n_data_events": n_data,
        "n_mc_events": n_mc,
        "sv_statistics": {
            "data_sv_fraction_h0": float(np.mean(data_sv["sv_ntrk_h0"] >= 2)),
            "data_sv_fraction_h1": float(np.mean(data_sv["sv_ntrk_h1"] >= 2)),
            "mc_sv_fraction_h0": float(np.mean(mc_sv["sv_ntrk_h0"] >= 2)),
            "mc_sv_fraction_h1": float(np.mean(mc_sv["sv_ntrk_h1"] >= 2)),
            "data_sv_mass_mean": float(np.mean(data_sv["sv_mass_h0"][data_sv["sv_ntrk_h0"] >= 2])),
            "mc_sv_mass_mean": float(np.mean(mc_sv["sv_mass_h0"][mc_sv["sv_ntrk_h0"] >= 2])),
        },
        "efficiency_scans": {
            "old_tag_mc": scan_old_mc,
            "sv_tag_mc": scan_sv_mc,
            "combined_tag_mc": scan_comb_mc,
        },
        "rb_extraction": {
            "all_configs": sv_rb_results,
            "best": {
                "label": best_sv["label"],
                "R_b": best_sv["R_b"],
                "sigma_stat": best_sv["sigma_stat"],
                "eps_c_over_eps_b": best_sv["eps_c_over_eps_b"],
            } if best_sv else None,
            "stability": {
                "R_b_combined": rb_sv_combined,
                "sigma_combined": sigma_sv_combined,
                "chi2": chi2_stab,
                "ndf": ndf_stab,
                "p_value": p_stab,
            },
            "comparison_current": {
                "current_R_b": rb_current,
                "current_sigma": sigma_current,
                "sv_R_b": best_sv["R_b"] if best_sv else None,
                "sv_sigma": best_sv["sigma_stat"] if best_sv else None,
            },
        },
        "afb_results": afb_results,
        "sm_values": {"R_b": R_B_SM, "R_c": R_C_SM},
    }

    out_path = PHASE4C_OUT / "sv_reconstruction.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    log.info("Saved sv_reconstruction.json")

    # Update parameters.json
    params_path = RESULTS_DIR / "parameters.json"
    if params_path.exists():
        with open(params_path) as f:
            params = json.load(f)
    else:
        params = {}

    if best_sv:
        params["R_b_sv_tag"] = {
            "value": best_sv["R_b"],
            "stat": best_sv["sigma_stat"],
            "SM": R_B_SM,
            "method": "3-tag with SV-enhanced combined tag",
            "eps_c_over_eps_b": best_sv["eps_c_over_eps_b"],
            "working_point": best_sv["label"],
        }

    if rb_sv_combined is not None:
        params["R_b_sv_tag_combined"] = {
            "value": rb_sv_combined,
            "stat": sigma_sv_combined,
            "SM": R_B_SM,
            "method": "3-tag with SV-enhanced tag, combined WPs",
        }

    if afb_results:
        best_afb_key = min(afb_results.keys(),
                           key=lambda k: afb_results[k].get("A_FB_b_err", 999))
        best_afb = afb_results[best_afb_key]
        params["A_FB_b_sv_tag"] = {
            "value": best_afb["A_FB_b"],
            "stat": best_afb["A_FB_b_err"],
            "method": f"SV-tagged double-tag, {best_afb_key}",
            "n_double_tagged": best_afb["n_double_tagged"],
        }

    with open(params_path, "w") as f:
        json.dump(params, f, indent=2)
    log.info("Updated parameters.json")

    elapsed = time.time() - t0
    log.info("\n--- Done (%.1f s) ---", elapsed)
    log.info("Summary:")
    if best_sv:
        log.info("  R_b (SV tag) = %.5f +/- %.5f", best_sv["R_b"],
                 best_sv["sigma_stat"])
        log.info("  eps_c/eps_b = %.4f (from calibration)",
                 best_sv["eps_c_over_eps_b"])
        log.info("  Current R_b = %.5f +/- %.5f", rb_current, sigma_current)
    if afb_results:
        best_afb = afb_results[best_afb_key]
        log.info("  A_FB^b (SV tag) = %.4f +/- %.4f",
                 best_afb["A_FB_b"], best_afb["A_FB_b_err"])


if __name__ == "__main__":
    main()
