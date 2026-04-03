"""Phase 3 reusable plotting utilities.

Provides:
- data_mc_comparison: data vs MC with pull panel
- save_and_register: saves PNG+PDF, writes FIGURES.json entry
- standard figure setup (figsize, style, experiment label)

All figures use mplhep CMS style with ALEPH Open Data branding.
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


def save_and_register(
    fig,
    filename,
    script_path,
    description,
    fig_type,
    lower_panel="none",
    is_2d=False,
    observable_type="count",
):
    """Save figure as PNG+PDF and register in FIGURES.json.

    Parameters
    ----------
    fig : matplotlib Figure
    filename : str — filename in outputs/figures/ (e.g., 'foo.png')
    script_path : str or Path — path to the plotting script (relative to phase dir)
    description : str — one-line description
    fig_type : str — one of: data_mc, 2d_heatmap, diagnostic, result,
        systematic_impact, closure, comparison, roc
    lower_panel : str — 'pull', 'ratio', or 'none'
    is_2d : bool
    observable_type : str — 'count' or 'derived'
    """
    now = datetime.now(timezone.utc).isoformat()
    # Use the calling script's mtime if available
    script_file = Path(script_path)
    if script_file.exists():
        script_mtime = datetime.fromtimestamp(
            script_file.stat().st_mtime, tz=timezone.utc
        ).isoformat()
    else:
        script_mtime = now

    fig.savefig(FIG / filename, bbox_inches="tight", dpi=200, transparent=True)
    pdf_name = filename.replace(".png", ".pdf")
    fig.savefig(FIG / pdf_name, bbox_inches="tight", dpi=200, transparent=True)
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
    registry.append(
        {
            "filename": filename,
            "type": fig_type,
            "script": str(script_path),
            "description": description,
            "lower_panel": lower_panel,
            "is_2d": is_2d,
            "created": now,
            "script_mtime": script_mtime,
            "observable_type": observable_type,
        }
    )
    with open(registry_path, "w") as f:
        json.dump(registry, f, indent=2)

    log.info("Saved %s", filename)


def setup_figure():
    """Create a standard 10x10 figure."""
    fig, ax = plt.subplots(figsize=(10, 10))
    return fig, ax


def setup_ratio_figure():
    """Create a standard figure with main + pull/ratio panel."""
    fig, (ax, rax) = plt.subplots(
        2,
        1,
        figsize=(10, 10),
        gridspec_kw={"height_ratios": [3, 1]},
        sharex=True,
    )
    fig.subplots_adjust(hspace=0)
    return fig, ax, rax


def exp_label_data(ax, rlabel=r"$\sqrt{s} = 91.2$ GeV"):
    """Add ALEPH Open Data experiment label."""
    mh.label.exp_label(
        exp="ALEPH",
        data=True,
        llabel="Open Data",
        rlabel=rlabel,
        ax=ax,
    )


def exp_label_mc(ax, rlabel=r"$\sqrt{s} = 91.2$ GeV"):
    """Add ALEPH Open Simulation experiment label."""
    mh.label.exp_label(
        exp="ALEPH",
        data=True,
        llabel="Open Simulation",
        rlabel=rlabel,
        ax=ax,
    )


def data_mc_comparison(
    data_values,
    mc_values,
    bins,
    xlabel,
    ylabel="Events",
    data_label="Data",
    mc_label="MC",
    mc_weights=None,
    data_weights=None,
    log_y=False,
    density=False,
    filename=None,
    script_path=None,
    description=None,
    observable_type="count",
):
    """Produce a data vs MC comparison plot with pull panel.

    Parameters
    ----------
    data_values : array-like — data values to histogram
    mc_values : array-like — MC values to histogram
    bins : array-like — bin edges
    xlabel : str — x-axis label
    ylabel : str — y-axis label for main panel
    data_label, mc_label : str — legend labels
    mc_weights, data_weights : array-like or None — per-event weights
    log_y : bool — log scale on y axis
    density : bool — normalize to unit area
    filename : str or None — if provided, save and register
    script_path : str or None — path to calling script
    description : str or None — figure description for registry
    observable_type : str — 'count' or 'derived'

    Returns
    -------
    fig, ax, rax
    """
    fig, ax, rax = setup_ratio_figure()

    # Histogram data
    h_data, _ = np.histogram(data_values, bins=bins, weights=data_weights)
    h_mc, _ = np.histogram(mc_values, bins=bins, weights=mc_weights)

    # Errors
    if data_weights is not None:
        h_data_err2, _ = np.histogram(
            data_values, bins=bins, weights=np.asarray(data_weights) ** 2
        )
        h_data_err = np.sqrt(h_data_err2)
    else:
        h_data_err = np.sqrt(np.maximum(h_data, 1))

    if mc_weights is not None:
        h_mc_err2, _ = np.histogram(
            mc_values, bins=bins, weights=np.asarray(mc_weights) ** 2
        )
        h_mc_err = np.sqrt(h_mc_err2)
    else:
        h_mc_err = np.sqrt(np.maximum(h_mc, 1))

    # Normalize MC to data integral
    if not density:
        data_integral = h_data.sum()
        mc_integral = h_mc.sum()
        if mc_integral > 0:
            scale = data_integral / mc_integral
            h_mc = h_mc * scale
            h_mc_err = h_mc_err * scale
    else:
        bin_widths = np.diff(bins)
        data_integral = (h_data * bin_widths).sum()
        mc_integral = (h_mc * bin_widths).sum()
        if data_integral > 0:
            h_data = h_data / data_integral
            h_data_err = h_data_err / data_integral
        if mc_integral > 0:
            h_mc = h_mc / mc_integral
            h_mc_err = h_mc_err / mc_integral

    bin_centers = 0.5 * (bins[:-1] + bins[1:])

    # Main panel: MC as filled histogram, data as points
    mh.histplot(
        h_mc,
        bins=bins,
        ax=ax,
        label=mc_label,
        histtype="fill",
        color="C0",
        alpha=0.5,
    )
    mh.histplot(
        h_mc,
        bins=bins,
        ax=ax,
        label=None,
        histtype="step",
        color="C0",
    )
    ax.errorbar(
        bin_centers,
        h_data,
        yerr=h_data_err,
        fmt="o",
        color="black",
        markersize=4,
        label=data_label,
    )

    ax.set_ylabel(ylabel)
    if log_y:
        ax.set_yscale("log")
    ax.legend(fontsize="x-small")
    exp_label_data(ax)
    mpl_magic(ax)

    # Pull panel: (data - MC) / sqrt(sigma_data^2 + sigma_mc^2)
    total_err = np.sqrt(h_data_err**2 + h_mc_err**2)
    pull = np.where(total_err > 0, (h_data - h_mc) / total_err, 0.0)

    rax.errorbar(bin_centers, pull, yerr=1.0, fmt="o", color="black", markersize=3)
    rax.axhline(0, color="gray", linestyle="--", linewidth=0.8)
    rax.axhline(2, color="gray", linestyle=":", linewidth=0.5)
    rax.axhline(-2, color="gray", linestyle=":", linewidth=0.5)
    rax.set_ylabel("Pull")
    rax.set_xlabel(xlabel)
    rax.set_ylim(-4, 4)

    if filename is not None and script_path is not None:
        save_and_register(
            fig,
            filename,
            script_path,
            description or f"Data/MC comparison: {xlabel}",
            "data_mc",
            lower_panel="pull",
            observable_type=observable_type,
        )

    return fig, ax, rax
