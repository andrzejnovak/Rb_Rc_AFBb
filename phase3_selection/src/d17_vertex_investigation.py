"""Phase 3: Primary vertex investigation [D17].

STRATEGY.md [D17] committed Phase 3 actions:
(a) Check if d0 changes when the event vertex is recomputed excluding the track
(b) If global vertex is used, either recompute d0 or assign a systematic

Since we cannot refit the primary vertex (no vertex reconstruction code
in the open data), we investigate:
1. Whether d0 is measured relative to (0,0) or a fitted primary vertex
2. The spread of d0 in the resolution-dominated regime
3. The track-in-vertex bias magnitude from MC comparison
4. Whether sigma_d0 calibration absorbs vertex bias

Reads: outputs/preselected_data.npz, outputs/preselected_mc.npz,
       outputs/d0_significance.npz
Writes: outputs/d17_vertex_investigation.json
"""
import json
import logging
from pathlib import Path

import numpy as np
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "outputs"


def investigate_d0_reference(data, mc):
    """Investigate what d0 is measured relative to.

    If d0 is measured relative to (0,0), the resolution core should be
    offset by the beam position. If measured relative to a fitted primary
    vertex, the core should be centered at 0.

    Also check if d0 varies event-to-event in a way consistent with
    per-event vertex fitting.
    """
    log.info("--- D17 Investigation: d0 Reference Point ---")

    results = {}

    for prefix, sample in [("data", data), ("mc", mc)]:
        d0 = sample["trk_d0"]
        offsets = sample["trk_d0_offsets"]
        n_events = len(offsets) - 1

        # Overall d0 statistics
        median_d0 = float(np.median(d0))
        mean_d0 = float(np.mean(d0))
        std_d0 = float(np.std(d0))

        log.info("%s d0: mean=%.6f cm, median=%.6f cm, std=%.4f cm",
                 prefix, mean_d0, median_d0, std_d0)

        # Per-event median d0 (if vertex is per-event, this varies)
        n_check = min(n_events, 50000)
        evt_medians = []
        for i in range(n_check):
            start, end = offsets[i], offsets[i+1]
            if end - start < 5:
                continue
            evt_medians.append(float(np.median(d0[start:end])))

        evt_medians = np.array(evt_medians)
        spread_evt = float(np.std(evt_medians))
        mean_evt_median = float(np.mean(evt_medians))

        log.info("%s per-event median d0: mean=%.6f, spread=%.6f cm",
                 prefix, mean_evt_median, spread_evt)

        # If d0 is relative to beamline (0,0), per-event medians should
        # cluster tightly near 0. If relative to a per-event vertex that
        # moves, the spread of per-event medians would be ~0.
        # A non-zero spread indicates beam spot convolution.

        # Check d0 width in low-momentum bin (dominated by resolution+beam)
        pmag = sample["trk_pmag"]
        low_p_mask = pmag < 1.0
        if np.any(low_p_mask):
            d0_low_p = d0[low_p_mask]
            width_low_p = float(np.std(d0_low_p))
            # MAD-based robust width
            mad_low_p = float(np.median(np.abs(d0_low_p - np.median(d0_low_p))) * 1.4826)
        else:
            width_low_p = np.nan
            mad_low_p = np.nan

        log.info("%s d0 width (p < 1 GeV): std=%.4f cm, MAD*1.48=%.4f cm",
                 prefix, width_low_p, mad_low_p)

        results[prefix] = {
            "mean_d0_cm": mean_d0,
            "median_d0_cm": median_d0,
            "std_d0_cm": std_d0,
            "per_event_median_mean": mean_evt_median,
            "per_event_median_spread": spread_evt,
            "n_events_checked": n_check,
            "d0_width_low_p_std": width_low_p,
            "d0_width_low_p_mad": mad_low_p,
        }

    return results


def investigate_vertex_bias(data, mc, sig_data):
    """Estimate the track-in-vertex bias magnitude.

    The track-in-vertex bias occurs when the primary vertex includes
    the track being measured, pulling d0 toward zero. This biases
    d0 toward smaller values and inflates the resolution.

    We estimate the bias by comparing:
    1. d0 width in data vs MC (MC vertex is known, data vertex may be biased)
    2. Scale factors in the sigma_d0 calibration (absorb vertex bias)
    """
    log.info("\n--- D17 Investigation: Track-in-Vertex Bias ---")

    # Compare resolution widths
    data_sig = sig_data["data_significance"]
    mc_sig = sig_data["mc_significance"]

    # Negative tail width (should be unit Gaussian after calibration)
    data_neg = data_sig[data_sig < 0]
    mc_neg = mc_sig[mc_sig < 0]

    data_neg_width = float(np.std(data_neg))
    mc_neg_width = float(np.std(mc_neg))

    log.info("Calibrated negative tail width: data=%.4f, MC=%.4f",
             data_neg_width, mc_neg_width)

    # Load calibration scale factors
    with open(OUT / "sigma_d0_params.json") as f:
        params = json.load(f)

    data_scales = [v["scale_factor"] for v in params["data_calibration"].values()
                   if v["scale_factor"] is not None]
    mc_scales = [v["scale_factor"] for v in params["mc_calibration"].values()
                 if v["scale_factor"] is not None]

    mean_data_sf = float(np.mean(data_scales))
    mean_mc_sf = float(np.mean(mc_scales))
    ratio_sf = mean_data_sf / max(mean_mc_sf, 0.01)

    log.info("Mean scale factor: data=%.3f, MC=%.3f, ratio=%.3f",
             mean_data_sf, mean_mc_sf, ratio_sf)
    log.info("If ratio > 1, data has worse resolution than MC -> "
             "vertex bias or alignment effects")

    # The excess scale factor in data vs MC can be attributed to:
    # 1. Beam spot size (data has finite beam spot, MC may not)
    # 2. Vertex reconstruction bias (track-in-vertex)
    # 3. Detector alignment differences

    vertex_bias_estimate = float(abs(mean_data_sf - mean_mc_sf) / mean_data_sf)

    return {
        "calibrated_neg_width_data": data_neg_width,
        "calibrated_neg_width_mc": mc_neg_width,
        "mean_scale_factor_data": mean_data_sf,
        "mean_scale_factor_mc": mean_mc_sf,
        "data_mc_scale_ratio": ratio_sf,
        "vertex_bias_fraction_estimate": vertex_bias_estimate,
    }


def main():
    log.info("=" * 60)
    log.info("Phase 3: Primary Vertex Investigation [D17]")
    log.info("=" * 60)

    data = np.load(OUT / "preselected_data.npz", allow_pickle=False)
    mc = np.load(OUT / "preselected_mc.npz", allow_pickle=False)
    sig_data = np.load(OUT / "d0_significance.npz", allow_pickle=False)

    results = {}

    # Investigation (a): What is d0 measured relative to?
    results["d0_reference"] = investigate_d0_reference(data, mc)

    # Investigation (b): Track-in-vertex bias
    results["vertex_bias"] = investigate_vertex_bias(data, mc, sig_data)

    # Conclusion
    # Three approaches attempted:
    # 1. Per-event median d0 spread analysis (above)
    # 2. Data/MC scale factor comparison (above)
    # 3. Vertex refit (INFEASIBLE: no vertex reconstruction in open data)

    data_spread = results["d0_reference"]["data"]["per_event_median_spread"]
    mc_spread = results["d0_reference"]["mc"]["per_event_median_spread"]
    sf_ratio = results["vertex_bias"]["data_mc_scale_ratio"]

    # Assess
    if data_spread > 0.001:  # > 10 micron event-to-event variation
        vertex_type = "Per-event vertex or beam spot convolution"
        vertex_note = (f"Per-event median d0 spread = {data_spread*10000:.1f} micron "
                       "suggests d0 includes beam spot / vertex effects.")
    else:
        vertex_type = "d0 appears relative to origin or stable reference"
        vertex_note = (f"Per-event median d0 spread = {data_spread*10000:.1f} micron "
                       "is small, suggesting d0 is relative to a stable reference.")

    results["conclusion"] = {
        "vertex_type": vertex_type,
        "vertex_note": vertex_note,
        "infeasible_approaches": [
            "Vertex refit excluding track: no vertex reconstruction code available "
            "in open data format. The d0 branch is pre-computed and cannot be "
            "recomputed from (vx, vy) since no per-event vertex position is stored."
        ],
        "systematic_recommendation": (
            f"The data/MC scale factor ratio is {sf_ratio:.2f}. "
            "The sigma_d0 calibration absorbs beam spot and vertex effects "
            "into the per-bin scale factors. A systematic uncertainty should be "
            "assigned by varying scale factors by +/- 10% to cover residual "
            "vertex-related biases. This systematic enters through the "
            "hemisphere tag efficiency and the correlation C_b."
        ),
        "approaches_attempted": 3,
        "approaches_feasible": 2,
        "approaches_infeasible": 1,
    }

    log.info("\n--- Conclusion ---")
    log.info(results["conclusion"]["vertex_type"])
    log.info(results["conclusion"]["vertex_note"])
    log.info(results["conclusion"]["systematic_recommendation"])

    with open(OUT / "d17_vertex_investigation.json", "w") as f:
        json.dump(results, f, indent=2)
    log.info("Saved d17_vertex_investigation.json")


if __name__ == "__main__":
    main()
