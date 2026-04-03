"""Phase 1: Survey integer/flag branches, truth-level info, and key variables.

Reads ~1000 events from data and MC, surveys integer branches for unique values,
checks for truth information in MC, and computes basic statistics.
"""
import json
import logging
from pathlib import Path

import awkward as ak
import numpy as np
import uproot
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "outputs"

DATA_DIR = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPH/")
MC_DIR = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPHMC/")

NMAX = 2000  # prototype on small subset


def survey_integer_branches(tree, branches, nmax=NMAX):
    """Survey integer/bool branches for unique values."""
    results = {}
    # Identify integer/bool branches (event-level only, not jagged)
    int_branches = []
    for bname, btype in branches.items():
        if "[]" not in btype and ("int" in btype or "bool" in btype):
            int_branches.append(bname)

    if not int_branches:
        return results

    arrays = tree.arrays(int_branches, entry_stop=nmax, library="np")
    for bname in int_branches:
        arr = arrays[bname]
        unique = np.unique(arr)
        results[bname] = {
            "dtype": str(arr.dtype),
            "n_unique": int(len(unique)),
            "unique_values": unique.tolist() if len(unique) <= 30 else f"[{unique.min()}..{unique.max()}]",
            "min": int(unique.min()) if len(unique) > 0 else None,
            "max": int(unique.max()) if len(unique) > 0 else None,
            "mean": float(np.mean(arr)),
        }
    return results


def survey_float_branches(tree, branches, nmax=NMAX):
    """Survey event-level float branches for basic stats."""
    results = {}
    float_branches = []
    for bname, btype in branches.items():
        if "[]" not in btype and "float" in btype:
            float_branches.append(bname)

    if not float_branches:
        return results

    arrays = tree.arrays(float_branches, entry_stop=nmax, library="np")
    for bname in float_branches:
        arr = arrays[bname]
        results[bname] = {
            "mean": float(np.mean(arr)),
            "std": float(np.std(arr)),
            "min": float(np.min(arr)),
            "max": float(np.max(arr)),
            "n_nan": int(np.sum(np.isnan(arr))),
            "n_inf": int(np.sum(np.isinf(arr))),
        }
    return results


def survey_track_variables(tree, nmax=NMAX):
    """Survey track-level variables relevant for b-tagging."""
    results = {}
    track_branches = ["d0", "z0", "pt", "charge", "weight", "highPurity",
                       "pid", "pwflag", "ntpc", "nitc", "nvdet"]
    # Only read branches that exist
    available = [b for b in track_branches if b in tree.keys()]
    if not available:
        return results

    arrays = tree.arrays(available, entry_stop=nmax, library="ak")
    for bname in available:
        arr = ak.flatten(arrays[bname])
        np_arr = ak.to_numpy(arr)
        results[bname] = {
            "n_total": int(len(np_arr)),
            "mean": float(np.mean(np_arr)),
            "std": float(np.std(np_arr)),
            "min": float(np.min(np_arr)),
            "max": float(np.max(np_arr)),
            "n_nan": int(np.sum(np.isnan(np_arr.astype(float)))),
        }
        if bname in ("pid", "pwflag", "charge", "highPurity", "ntpc", "nitc", "nvdet"):
            unique = np.unique(np_arr)
            if len(unique) <= 50:
                results[bname]["unique_values"] = unique.tolist()
            else:
                results[bname]["n_unique"] = int(len(unique))
    return results


def check_mc_vs_data_branches(data_branches, mc_branches):
    """Find branches present in MC but not data (potential truth info)."""
    data_set = set(data_branches.keys())
    mc_set = set(mc_branches.keys())
    mc_only = mc_set - data_set
    data_only = data_set - mc_set
    return {
        "mc_only_branches": sorted(mc_only),
        "data_only_branches": sorted(data_only),
        "common_branches": len(data_set & mc_set),
    }


def main():
    results = {}

    # === DATA ===
    data_file = DATA_DIR / "LEP1Data1994P1_recons_aftercut-MERGED.root"
    log.info("Surveying data: %s", data_file.name)
    with uproot.open(data_file) as f:
        tree = f["t"]
        branches = {b: str(tree[b].typename) for b in tree.keys()}

        results["data_integer_survey"] = survey_integer_branches(tree, branches)
        results["data_float_survey"] = survey_float_branches(tree, branches)
        results["data_track_survey"] = survey_track_variables(tree)
        results["data_branches"] = branches
        results["data_n_entries"] = tree.num_entries

    # === MC ===
    mc_file = MC_DIR / "LEP1MC1994_recons_aftercut-001.root"
    log.info("Surveying MC: %s", mc_file.name)
    with uproot.open(mc_file) as f:
        tree = f["t"]
        mc_branches = {b: str(tree[b].typename) for b in tree.keys()}

        results["mc_integer_survey"] = survey_integer_branches(tree, mc_branches)
        results["mc_float_survey"] = survey_float_branches(tree, mc_branches)
        results["mc_track_survey"] = survey_track_variables(tree)
        results["mc_branches"] = mc_branches
        results["mc_n_entries"] = tree.num_entries

    # === Branch comparison ===
    results["branch_comparison"] = check_mc_vs_data_branches(
        results["data_branches"], results["mc_branches"]
    )

    # === Event counts across all data files ===
    log.info("Counting events across all data files...")
    data_counts = {}
    for fpath in sorted(DATA_DIR.glob("LEP1Data*_recons_aftercut-MERGED.root")):
        with uproot.open(fpath) as f:
            tree = f["t"]
            data_counts[fpath.name] = tree.num_entries
    results["data_event_counts"] = data_counts
    results["data_total_events"] = sum(data_counts.values())

    outpath = OUT / "branch_survey_fabiola_b942.json"
    with open(outpath, "w") as fp:
        json.dump(results, fp, indent=2, default=str)
    log.info("Written to %s", outpath)

    # Print key findings
    log.info("\n=== KEY FINDINGS ===")
    log.info("Data total events: %d", results["data_total_events"])
    for fname, count in data_counts.items():
        log.info("  %s: %d", fname, count)

    comp = results["branch_comparison"]
    log.info("\nMC-only branches (potential truth info): %s", comp["mc_only_branches"])
    log.info("Data-only branches: %s", comp["data_only_branches"])

    log.info("\n=== Integer branch survey (data) ===")
    for bname, info in results["data_integer_survey"].items():
        log.info("  %s: unique=%s, range=[%s, %s], mean=%.3f",
                 bname, info["n_unique"], info["min"], info["max"], info["mean"])

    log.info("\n=== Integer branch survey (MC) ===")
    for bname, info in results["mc_integer_survey"].items():
        log.info("  %s: unique=%s, range=[%s, %s], mean=%.3f",
                 bname, info["n_unique"], info["min"], info["max"], info["mean"])

    log.info("\n=== Track-level survey (data, first %d events) ===", NMAX)
    for bname, info in results["data_track_survey"].items():
        log.info("  %s: mean=%.4f, std=%.4f, range=[%.4f, %.4f], n_nan=%d",
                 bname, info["mean"], info["std"], info["min"], info["max"], info["n_nan"])


if __name__ == "__main__":
    main()
