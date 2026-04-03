"""Phase 1: Survey key discriminating variables for b-tagging.

Produces data vs MC comparison distributions for variables relevant
to the R_b, R_c, A_FB^b analysis. Writes histogram data to JSON
and figures to outputs/figures/.
"""
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

import awkward as ak
import hist
import matplotlib.pyplot as plt
import mplhep as mh
import numpy as np
import uproot
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

DATA_DIR = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPH/")
MC_DIR = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPHMC/")

NMAX = 5000  # events for survey


def save_and_register(fig, filename, script, description, fig_type,
                      lower_panel="none", is_2d=False, observable_type="count"):
    """Save figure and register in FIGURES.json."""
    now = datetime.now(timezone.utc).isoformat()
    script_mtime = datetime.fromtimestamp(
        Path(__file__).stat().st_mtime, tz=timezone.utc
    ).isoformat()

    fig.savefig(FIG / filename, bbox_inches="tight", dpi=200, transparent=True)
    fig.savefig(FIG / filename.replace(".png", ".pdf"), bbox_inches="tight",
                dpi=200, transparent=True)
    plt.close(fig)

    # Update FIGURES.json
    registry_path = OUT / "FIGURES.json"
    if registry_path.exists():
        with open(registry_path) as f:
            registry = json.load(f)
    else:
        registry = []

    # Remove existing entry for this filename
    registry = [e for e in registry if e["filename"] != filename]
    registry.append({
        "filename": filename,
        "type": fig_type,
        "script": f"src/{Path(__file__).name}",
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


def load_data(nmax=NMAX):
    """Load data from one representative data file."""
    fpath = DATA_DIR / "LEP1Data1994P1_recons_aftercut-MERGED.root"
    branches_evt = ["Thrust", "TTheta", "Sphericity", "nChargedHadrons",
                    "nParticle", "passesAll", "Energy", "bFlag",
                    "nChargedHadronsHP", "missP"]
    branches_trk = ["d0", "z0", "pt", "charge", "weight", "highPurity",
                    "pwflag", "theta", "phi", "pmag"]

    with uproot.open(fpath) as f:
        tree = f["t"]
        evt = tree.arrays(branches_evt, entry_stop=nmax, library="ak")
        trk = tree.arrays(branches_trk, entry_stop=nmax, library="ak")
    return evt, trk


def load_mc(nmax=NMAX):
    """Load MC from first file."""
    fpath = MC_DIR / "LEP1MC1994_recons_aftercut-001.root"
    branches_evt = ["Thrust", "TTheta", "Sphericity", "nChargedHadrons",
                    "nParticle", "passesAll", "Energy", "bFlag",
                    "nChargedHadronsHP", "missP", "particleWeight"]
    branches_trk = ["d0", "z0", "pt", "charge", "weight", "highPurity",
                    "pwflag", "theta", "phi", "pmag"]

    with uproot.open(fpath) as f:
        tree = f["t"]
        evt = tree.arrays(branches_evt, entry_stop=nmax, library="ak")
        trk = tree.arrays(branches_trk, entry_stop=nmax, library="ak")
    return evt, trk


def plot_data_mc_1d(data_vals, mc_vals, bins, xlabel, filename, description,
                    mc_weights=None, log_y=False):
    """Produce a data/MC comparison with pull panel."""
    fig, (ax, rax) = plt.subplots(
        2, 1, figsize=(10, 10),
        gridspec_kw={"height_ratios": [3, 1]},
        sharex=True,
    )
    fig.subplots_adjust(hspace=0)

    # Fill histograms
    h_data = hist.Hist(hist.axis.Variable(bins, label=""))
    h_mc = hist.Hist(hist.axis.Variable(bins, label=""), storage=hist.storage.Weight())

    h_data.fill(data_vals)
    if mc_weights is not None:
        h_mc.fill(mc_vals, weight=mc_weights)
    else:
        h_mc.fill(mc_vals)

    # Normalize MC to data integral
    data_integral = h_data.sum().value if hasattr(h_data.sum(), 'value') else h_data.sum()
    mc_integral = h_mc.sum().value
    if mc_integral > 0:
        scale = data_integral / mc_integral
    else:
        scale = 1.0

    # Plot
    mh.histplot(h_data, ax=ax, histtype="errorbar", color="black",
                label="Data", xerr=True)
    mh.histplot(h_mc, ax=ax, histtype="fill", color="royalblue",
                label="MC (norm. to data)", alpha=0.5,
                flow="none", w2method="sqrt")

    # Scale MC for comparison
    mc_vals_scaled = h_mc.view().value * scale
    mc_err_scaled = np.sqrt(h_mc.view().variance) * scale

    # Replot MC scaled
    ax.clear()
    mh.histplot(h_data, ax=ax, histtype="errorbar", color="black",
                label="Data", xerr=True)

    h_mc_scaled = hist.Hist(hist.axis.Variable(bins, label=""), storage=hist.storage.Weight())
    centers = (np.array(bins[:-1]) + np.array(bins[1:])) / 2
    for i in range(len(centers)):
        h_mc_scaled.view().value[i] = mc_vals_scaled[i]
        h_mc_scaled.view().variance[i] = mc_err_scaled[i]**2

    mh.histplot(h_mc_scaled, ax=ax, histtype="fill", color="royalblue",
                label="MC (norm. to data)", alpha=0.5)

    if log_y:
        ax.set_yscale("log")
    ax.set_ylabel("Events")
    ax.legend(fontsize="x-small")
    # Suppress "Axis 0" label that mh.histplot() sets from hist axis name;
    # x-label belongs on rax (ratio panel) only, not the main panel.
    ax.set_xlabel("")
    ax.tick_params(labelbottom=False)
    mh.label.exp_label(
        exp="ALEPH", data=True, llabel="Open Data",
        rlabel=r"$\sqrt{s} = 91.2$ GeV",
        ax=ax,
    )
    mpl_magic(ax)
    # Remove any residual "Axis" text artifacts from both panels
    for a in [ax, rax]:
        for txt in list(a.texts):
            if "Axis" in txt.get_text():
                txt.remove()

    # Pull panel
    data_content = h_data.values()
    data_err = np.sqrt(data_content)
    pull = np.where(data_err > 0,
                    (data_content - mc_vals_scaled) / data_err,
                    0)
    rax.bar(centers, pull, width=np.diff(bins), color="gray", alpha=0.7)
    rax.axhline(0, color="black", linewidth=0.5)
    rax.axhline(2, color="red", linewidth=0.5, linestyle="--")
    rax.axhline(-2, color="red", linewidth=0.5, linestyle="--")
    rax.set_ylabel(r"$(N_{\mathrm{data}} - N_{\mathrm{MC}}) / \sigma$")
    rax.set_xlabel(xlabel)
    rax.set_ylim(-5, 5)

    save_and_register(fig, filename, __file__, description, "data_mc",
                      lower_panel="pull")


def main():
    log.info("Loading data...")
    data_evt, data_trk = load_data()
    log.info("Loading MC...")
    mc_evt, mc_trk = load_mc()

    # Apply passesAll cut
    data_pass = data_evt[data_evt.passesAll]
    mc_pass = mc_evt[mc_evt.passesAll]
    data_trk_pass = data_trk[data_evt.passesAll]
    mc_trk_pass = mc_trk[mc_evt.passesAll]

    log.info("Data events passing all cuts: %d / %d", len(data_pass), len(data_evt))
    log.info("MC events passing all cuts: %d / %d", len(mc_pass), len(mc_evt))

    # === 1. Track multiplicity ===
    plot_data_mc_1d(
        ak.to_numpy(data_pass.nChargedHadrons),
        ak.to_numpy(mc_pass.nChargedHadrons),
        bins=np.arange(0, 50, 1).tolist(),
        xlabel=r"$N_{\mathrm{ch}}$",
        filename="data_mc_nch_fabiola_b942.png",
        description="Charged hadron multiplicity, data vs MC after hadronic selection",
    )

    # === 2. Thrust ===
    plot_data_mc_1d(
        ak.to_numpy(data_pass.Thrust),
        ak.to_numpy(mc_pass.Thrust),
        bins=np.linspace(0.5, 1.0, 51).tolist(),
        xlabel="Thrust",
        filename="data_mc_thrust_fabiola_b942.png",
        description="Thrust distribution, data vs MC after hadronic selection",
    )

    # === 3. Impact parameter d0 ===
    # Filter out sentinel values (-999)
    data_d0 = ak.flatten(data_trk_pass.d0)
    mc_d0 = ak.flatten(mc_trk_pass.d0)
    data_d0_clean = ak.to_numpy(data_d0[data_d0 > -990])
    mc_d0_clean = ak.to_numpy(mc_d0[mc_d0 > -990])

    plot_data_mc_1d(
        data_d0_clean,
        mc_d0_clean,
        bins=np.linspace(-0.5, 0.5, 101).tolist(),
        xlabel=r"$d_0$ [cm]",
        filename="data_mc_d0_fabiola_b942.png",
        description="Track impact parameter d0, data vs MC (sentinel -999 removed)",
        log_y=True,
    )

    # === 4. Impact parameter significance ===
    # We need to compute d0 significance: d0 / sigma_d0
    # sigma_d0 is not directly available, but we can use |d0| distribution
    # For now, plot |d0| which is the key b-tagging variable
    data_abs_d0 = np.abs(data_d0_clean)
    mc_abs_d0 = np.abs(mc_d0_clean)

    plot_data_mc_1d(
        data_abs_d0,
        mc_abs_d0,
        bins=np.logspace(-4, 0, 51).tolist(),
        xlabel=r"$|d_0|$ [cm]",
        filename="data_mc_absd0_fabiola_b942.png",
        description="|d0| distribution (log scale), data vs MC - key b-tagging variable",
        log_y=True,
    )

    # === 5. Sphericity ===
    plot_data_mc_1d(
        ak.to_numpy(data_pass.Sphericity),
        ak.to_numpy(mc_pass.Sphericity),
        bins=np.linspace(0, 0.6, 31).tolist(),
        xlabel="Sphericity",
        filename="data_mc_sphericity_fabiola_b942.png",
        description="Sphericity distribution, data vs MC after hadronic selection",
    )

    # === 6. cos(theta_thrust) for A_FB^b ===
    data_costheta = np.cos(ak.to_numpy(data_pass.TTheta))
    mc_costheta = np.cos(ak.to_numpy(mc_pass.TTheta))

    plot_data_mc_1d(
        data_costheta,
        mc_costheta,
        bins=np.linspace(-1, 1, 41).tolist(),
        xlabel=r"$\cos\theta_{\mathrm{thrust}}$",
        filename="data_mc_costheta_fabiola_b942.png",
        description="cos(theta_thrust) distribution for A_FB measurement, data vs MC",
    )

    # === 7. Track pt ===
    data_pt = ak.to_numpy(ak.flatten(data_trk_pass.pt))
    mc_pt = ak.to_numpy(ak.flatten(mc_trk_pass.pt))

    plot_data_mc_1d(
        data_pt,
        mc_pt,
        bins=np.logspace(-1, 1.7, 41).tolist(),
        xlabel=r"Track $p_{\mathrm{T}}$ [GeV]",
        filename="data_mc_trackpt_fabiola_b942.png",
        description="Track pT distribution, data vs MC",
        log_y=True,
    )

    # === 8. Per-track weight distribution ===
    data_w = ak.to_numpy(ak.flatten(data_trk_pass.weight))
    mc_w = ak.to_numpy(ak.flatten(mc_trk_pass.weight))

    plot_data_mc_1d(
        data_w,
        mc_w,
        bins=np.linspace(0, 2, 51).tolist(),
        xlabel="Track weight",
        filename="data_mc_trackweight_fabiola_b942.png",
        description="Per-track weight distribution, data vs MC",
    )

    # === 9. bFlag distribution (data only — MC is -999) ===
    data_bflag = ak.to_numpy(data_pass.bFlag)
    bflag_unique, bflag_counts = np.unique(data_bflag, return_counts=True)
    log.info("\nbFlag distribution in data:")
    for v, c in zip(bflag_unique, bflag_counts):
        log.info("  bFlag=%d: %d events (%.2f%%)", v, c, 100 * c / len(data_bflag))

    # === 10. Event yield summary ===
    survey_results = {
        "data_events_total": int(len(data_evt)),
        "data_events_passAll": int(len(data_pass)),
        "mc_events_total": int(len(mc_evt)),
        "mc_events_passAll": int(len(mc_pass)),
        "data_pass_fraction": float(len(data_pass) / len(data_evt)),
        "mc_pass_fraction": float(len(mc_pass) / len(mc_evt)),
        "bFlag_distribution": {str(v): int(c) for v, c in zip(bflag_unique, bflag_counts)},
        "d0_sentinel_fraction_data": float(np.mean(ak.to_numpy(data_d0) <= -990)),
        "d0_sentinel_fraction_mc": float(np.mean(ak.to_numpy(mc_d0) <= -990)),
        "track_weight_mean_data": float(np.mean(data_w)),
        "track_weight_mean_mc": float(np.mean(mc_w)),
        "track_weight_std_data": float(np.std(data_w)),
        "track_weight_std_mc": float(np.std(mc_w)),
    }

    outpath = OUT / "variable_survey_fabiola_b942.json"
    with open(outpath, "w") as f:
        json.dump(survey_results, f, indent=2)
    log.info("Survey results written to %s", outpath)


if __name__ == "__main__":
    main()
