"""Phase 3: Event preselection + track quality cuts + cutflow.

Implements:
- Event preselection: passesAll=1, |cos(theta_thrust)|<0.9
- Track quality: nvdet>0, highPurity=1, ntpc>4
- Cutflow table with data AND MC counts
- Saves intermediate arrays to NPZ for downstream scripts.

Outputs: outputs/cutflow.json, outputs/preselected_data.npz,
         outputs/preselected_mc.npz
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
OUT.mkdir(parents=True, exist_ok=True)

DATA_DIR = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPH/")
MC_DIR = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPHMC/")

# Branches to load
EVENT_BRANCHES = [
    "passesAll", "Thrust", "TTheta", "TPhi",
    "Sphericity", "nParticle", "nChargedHadrons",
    "bFlag", "isMC", "year", "particleWeight",
    "Energy",
]
TRACK_BRANCHES = [
    "px", "py", "pz", "pt", "pmag", "mass",
    "theta", "phi", "eta", "charge",
    "d0", "z0", "highPurity", "ntpc", "nitc", "nvdet",
    "weight",
]
ALL_BRANCHES = EVENT_BRANCHES + TRACK_BRANCHES


def load_files(directory, max_files=None, max_events=None):
    """Load data from ROOT files in a directory."""
    files = sorted(directory.glob("*.root"))
    if max_files:
        files = files[:max_files]
    log.info("Loading %d files from %s", len(files), directory)

    arrays_list = []
    for f in files:
        try:
            tree = uproot.open(f)["t"]
            arr = tree.arrays(ALL_BRANCHES, library="ak",
                              entry_stop=max_events)
            arrays_list.append(arr)
            log.info("  %s: %d events", f.name, len(arr))
        except Exception as e:
            log.warning("Failed to load %s: %s", f.name, e)

    if not arrays_list:
        raise RuntimeError(f"No files loaded from {directory}")

    combined = ak.concatenate(arrays_list)
    log.info("Total: %d events", len(combined))
    return combined


def apply_preselection(events):
    """Apply event preselection and return mask + cutflow dict."""
    n_total = len(events)
    cutflow = {"total": int(n_total)}

    # passesAll = 1
    mask_passes = events["passesAll"] == 1
    cutflow["passesAll"] = int(ak.sum(mask_passes))

    # |cos(theta_thrust)| < 0.9
    cos_ttheta = np.cos(events["TTheta"])
    mask_costheta = np.abs(cos_ttheta) < 0.9
    mask_combined = mask_passes & mask_costheta
    cutflow["cos_theta_cut"] = int(ak.sum(mask_combined))

    return mask_combined, cutflow


def apply_track_quality(events):
    """Apply track quality cuts and return good-track mask (per track).

    Returns a boolean array with shape matching the jagged track arrays.
    """
    nvdet = events["nvdet"]
    hp = events["highPurity"]
    ntpc = events["ntpc"]
    d0 = events["d0"]

    # nvdet > 0 (has VDET hits, d0 is meaningful)
    mask_nvdet = nvdet > 0
    # highPurity = 1
    mask_hp = hp == 1
    # ntpc > 4
    mask_ntpc = ntpc > 4
    # d0 is not sentinel
    mask_d0 = d0 > -998  # sentinel is -999

    mask = mask_nvdet & mask_hp & mask_ntpc & mask_d0

    return mask


def compute_cos_theta_thrust(events):
    """Compute cos(theta_thrust) from TTheta."""
    return np.cos(events["TTheta"])


def extract_hemisphere_data(events, track_mask):
    """Extract track-level data for good tracks, split into hemispheres.

    Hemispheres defined by thrust axis: positive/negative cos(angle to thrust).
    Returns dict with keys for downstream processing.
    """
    # Thrust axis direction from TTheta, TPhi
    ttheta = events["TTheta"]
    tphi = events["TPhi"]

    # Thrust axis unit vector (event-level)
    tx = np.sin(ttheta) * np.cos(tphi)
    ty = np.sin(ttheta) * np.sin(tphi)
    tz = np.cos(ttheta)

    # Track momenta
    px = events["px"]
    py = events["py"]
    pz = events["pz"]

    # Dot product of track momentum with thrust axis (per track, jagged)
    # Need to broadcast event-level thrust to track level
    dot = px * tx + py * ty + pz * tz

    # Hemisphere assignment: positive dot = hemisphere 1, negative = hemisphere 0
    hem_assign = (dot > 0)

    return {
        "hem_assign": hem_assign,
        "track_mask": track_mask,
        "dot_thrust": dot,
    }


def save_preselected(events, event_mask, track_mask, hem_data, prefix, out_dir):
    """Save preselected data to NPZ format for downstream use."""
    sel = events[event_mask]
    tm = track_mask[event_mask]

    # Event-level quantities
    result = {
        "passesAll": ak.to_numpy(sel["passesAll"]),
        "thrust": ak.to_numpy(sel["Thrust"]),
        "ttheta": ak.to_numpy(sel["TTheta"]),
        "tphi": ak.to_numpy(sel["TPhi"]),
        "sphericity": ak.to_numpy(sel["Sphericity"]),
        "nch": ak.to_numpy(sel["nChargedHadrons"]),
        "bflag": ak.to_numpy(sel["bFlag"]),
        "is_mc": ak.to_numpy(sel["isMC"]),
        "year": ak.to_numpy(sel["year"]),
        "cos_theta_thrust": np.cos(ak.to_numpy(sel["TTheta"])),
        "energy": ak.to_numpy(sel["Energy"]),
    }

    # Track-level: save as flattened arrays + offsets for jaggedness
    # Use ak.num to reconstruct offsets from counts (avoids layout issues)
    for br in ["d0", "z0", "pmag", "pt", "theta", "phi", "charge",
               "nvdet", "ntpc", "weight", "px", "py", "pz", "mass"]:
        arr = sel[br]
        # Apply track mask
        good = arr[tm]
        counts = ak.to_numpy(ak.num(good))
        offsets = np.zeros(len(counts) + 1, dtype=np.int64)
        np.cumsum(counts, out=offsets[1:])
        flat = ak.to_numpy(ak.flatten(good))
        result[f"trk_{br}"] = flat
        result[f"trk_{br}_offsets"] = offsets

    # Also save all-track arrays (without quality cut) for jet charge
    for br in ["charge", "pmag", "theta", "phi", "px", "py", "pz", "weight"]:
        arr = sel[br]
        counts = ak.to_numpy(ak.num(arr))
        offsets = np.zeros(len(counts) + 1, dtype=np.int64)
        np.cumsum(counts, out=offsets[1:])
        flat = ak.to_numpy(ak.flatten(arr))
        result[f"alltrk_{br}"] = flat
        result[f"alltrk_{br}_offsets"] = offsets

    # Hemisphere assignment for good tracks
    hem = hem_data["hem_assign"][event_mask]
    good_hem = hem[tm]
    counts_gh = ak.to_numpy(ak.num(good_hem))
    offsets_gh = np.zeros(len(counts_gh) + 1, dtype=np.int64)
    np.cumsum(counts_gh, out=offsets_gh[1:])
    result["trk_hem"] = ak.to_numpy(ak.flatten(good_hem))
    result["trk_hem_offsets"] = offsets_gh

    # Hemisphere assignment for all tracks
    hem_all = hem_data["hem_assign"][event_mask]
    counts_ha = ak.to_numpy(ak.num(hem_all))
    offsets_ha = np.zeros(len(counts_ha) + 1, dtype=np.int64)
    np.cumsum(counts_ha, out=offsets_ha[1:])
    result["alltrk_hem"] = ak.to_numpy(ak.flatten(hem_all))
    result["alltrk_hem_offsets"] = offsets_ha

    # Thrust axis dot product for good tracks (for signed d0)
    dot = hem_data["dot_thrust"][event_mask]
    good_dot = dot[tm]
    counts_gd = ak.to_numpy(ak.num(good_dot))
    offsets_gd = np.zeros(len(counts_gd) + 1, dtype=np.int64)
    np.cumsum(counts_gd, out=offsets_gd[1:])
    result["trk_dot_thrust"] = ak.to_numpy(ak.flatten(good_dot))
    result["trk_dot_thrust_offsets"] = offsets_gd

    # All-track dot product for jet charge
    counts_dt = ak.to_numpy(ak.num(dot))
    offsets_dt = np.zeros(len(counts_dt) + 1, dtype=np.int64)
    np.cumsum(counts_dt, out=offsets_dt[1:])
    result["alltrk_dot_thrust"] = ak.to_numpy(ak.flatten(dot))
    result["alltrk_dot_thrust_offsets"] = offsets_dt

    np.savez_compressed(out_dir / f"{prefix}.npz", **result)
    log.info("Saved %s.npz (%d events)", prefix, int(ak.sum(event_mask)))


def main():
    log.info("=" * 60)
    log.info("Phase 3: Preselection")
    log.info("=" * 60)

    # Load data
    data = load_files(DATA_DIR)
    mc = load_files(MC_DIR)

    # Event preselection
    data_emask, data_cutflow = apply_preselection(data)
    mc_emask, mc_cutflow = apply_preselection(mc)

    log.info("Data cutflow: %s", data_cutflow)
    log.info("MC cutflow: %s", mc_cutflow)

    # Track quality
    data_tmask = apply_track_quality(data)
    mc_tmask = apply_track_quality(mc)

    # Count good tracks before/after
    data_sel = data[data_emask]
    mc_sel = mc[mc_emask]
    data_tm_sel = data_tmask[data_emask]
    mc_tm_sel = mc_tmask[mc_emask]

    data_total_tracks = int(ak.sum(ak.num(data_sel["d0"])))
    data_good_tracks = int(ak.sum(ak.sum(data_tm_sel, axis=1)))
    mc_total_tracks = int(ak.sum(ak.num(mc_sel["d0"])))
    mc_good_tracks = int(ak.sum(ak.sum(mc_tm_sel, axis=1)))

    data_cutflow["total_tracks"] = data_total_tracks
    data_cutflow["good_tracks"] = data_good_tracks
    mc_cutflow["total_tracks"] = mc_total_tracks
    mc_cutflow["good_tracks"] = mc_good_tracks

    log.info("Data tracks: %d total, %d good (%.1f%%)",
             data_total_tracks, data_good_tracks,
             100 * data_good_tracks / max(data_total_tracks, 1))
    log.info("MC tracks: %d total, %d good (%.1f%%)",
             mc_total_tracks, mc_good_tracks,
             100 * mc_good_tracks / max(mc_total_tracks, 1))

    # Hemisphere data
    data_hem = extract_hemisphere_data(data, data_tmask)
    mc_hem = extract_hemisphere_data(mc, mc_tmask)

    # Save
    save_preselected(data, data_emask, data_tmask, data_hem,
                     "preselected_data", OUT)
    save_preselected(mc, mc_emask, mc_tmask, mc_hem,
                     "preselected_mc", OUT)

    # Save cutflow
    cutflow = {"data": data_cutflow, "mc": mc_cutflow}
    with open(OUT / "cutflow.json", "w") as f:
        json.dump(cutflow, f, indent=2)
    log.info("Cutflow saved to cutflow.json")

    log.info("Preselection complete.")


if __name__ == "__main__":
    main()
