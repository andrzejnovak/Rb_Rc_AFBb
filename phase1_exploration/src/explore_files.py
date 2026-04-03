"""Phase 1 data reconnaissance: explore ROOT file structure.

Opens all data and MC ROOT files, lists trees, branches with types,
and event counts. Writes results to JSON for downstream scripts.
"""
import json
import logging
from pathlib import Path

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
OUT.mkdir(parents=True, exist_ok=True)

DATA_DIR = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPH/")
MC_DIR = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPHMC/")

DATA_FILES = sorted(DATA_DIR.glob("LEP1Data*_recons_aftercut-MERGED.root"))
MC_FILES = sorted(MC_DIR.glob("LEP1MC1994_recons_aftercut-*.root"))


def explore_file(fpath: Path, max_events: int = 1000) -> dict:
    """Explore a single ROOT file: trees, branches, types, counts."""
    info = {"file": fpath.name, "size_MB": fpath.stat().st_size / 1e6, "trees": {}}
    with uproot.open(fpath) as f:
        for key in f.keys():
            name = key.rstrip(";1").rstrip(";2")
            obj = f[key]
            if hasattr(obj, "num_entries"):
                tree_info = {
                    "num_entries": obj.num_entries,
                    "branches": {},
                }
                for bname in obj.keys():
                    branch = obj[bname]
                    btype = str(branch.typename)
                    tree_info["branches"][bname] = btype
                info["trees"][name] = tree_info
    return info


def main():
    results = {"data_files": [], "mc_files": []}

    log.info("=== Exploring %d data files ===", len(DATA_FILES))
    for fpath in DATA_FILES:
        log.info("  %s", fpath.name)
        info = explore_file(fpath)
        results["data_files"].append(info)
        for tname, tinfo in info["trees"].items():
            log.info(
                "    Tree %s: %d entries, %d branches",
                tname,
                tinfo["num_entries"],
                len(tinfo["branches"]),
            )

    log.info("=== Exploring MC files (first 3 of %d) ===", len(MC_FILES))
    for fpath in MC_FILES[:3]:
        log.info("  %s", fpath.name)
        info = explore_file(fpath)
        results["mc_files"].append(info)
        for tname, tinfo in info["trees"].items():
            log.info(
                "    Tree %s: %d entries, %d branches",
                tname,
                tinfo["num_entries"],
                len(tinfo["branches"]),
            )

    # Also count entries in all MC files without full branch scan
    log.info("=== Counting entries in all %d MC files ===", len(MC_FILES))
    mc_total = 0
    mc_counts = []
    for fpath in MC_FILES:
        with uproot.open(fpath) as f:
            for key in f.keys():
                obj = f[key]
                if hasattr(obj, "num_entries"):
                    mc_total += obj.num_entries
                    mc_counts.append({"file": fpath.name, "entries": obj.num_entries})
                    break  # Only count first tree
    results["mc_total_entries"] = mc_total
    results["mc_file_counts"] = mc_counts
    log.info("Total MC entries: %d across %d files", mc_total, len(MC_FILES))

    outpath = OUT / "file_exploration_fabiola_b942.json"
    with open(outpath, "w") as f:
        json.dump(results, f, indent=2)
    log.info("Written to %s", outpath)


if __name__ == "__main__":
    main()
