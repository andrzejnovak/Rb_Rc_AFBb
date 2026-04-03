"""Phase 3: sigma_d0 parameterization and calibration [D7].

Computes sigma_d0 = sqrt(A^2 + (B/(p*sin(theta)))^2) with A~25um, B~70um*GeV/c.
Calibrates from negative d0 tail per (nvdet, momentum, cos_theta) bins.

Source: ALEPH detector performance (537303): ~25 micron resolution at 45 GeV/c.
Source: inspire_433306, Section 7.1: negative tail calibration method.

Reads: outputs/preselected_data.npz, outputs/preselected_mc.npz
Writes: outputs/sigma_d0_params.json, outputs/d0_significance.npz
"""
import json
import logging
from pathlib import Path

import numpy as np
from scipy.optimize import minimize
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "outputs"

# Calibration binning [D7]: 5 momentum x 4 |cos theta| x 2 nvdet = 40 bins
P_BINS = [0.5, 1.0, 2.0, 5.0, 15.0, 100.0]  # GeV/c
COSTHETA_BINS = [0.0, 0.25, 0.5, 0.7, 0.9]
NVDET_CLASSES = [1, 2]  # 1 VDET hit, >=2 VDET hits

# Initial parameters from ALEPH detector paper (537303)
# sigma_d0 = sqrt(A^2 + (B/(p*sin(theta)))^2)
# A ~ 25 micron = 0.0025 cm, B ~ 70 micron*GeV/c = 0.0070 cm*GeV/c
A_INIT = 0.0025  # cm (intrinsic resolution)
B_INIT = 0.0070  # cm*GeV/c (multiple scattering)


def load_npz(path):
    """Load NPZ with jagged track reconstruction."""
    data = np.load(path, allow_pickle=False)
    return data


def reconstruct_jagged(flat, offsets):
    """Reconstruct jagged array from flat + offsets."""
    return [flat[offsets[i]:offsets[i+1]] for i in range(len(offsets) - 1)]


def compute_sigma_d0(pmag, theta, A, B):
    """Compute sigma_d0 parametrically.

    sigma_d0 = sqrt(A^2 + (B / (p * sin(theta)))^2)

    Following ALEPH convention for Rphi impact parameter.
    sin(theta) dependence (not sin^{3/2}) for Rphi projection.
    Source: 537303 (ALEPH VDET performance), STRATEGY.md Section 5.1.
    """
    sin_theta = np.sin(theta)
    # Protect against zero/very small values
    sin_theta = np.maximum(sin_theta, 0.01)
    pmag_safe = np.maximum(pmag, 0.1)

    ms_term = B / (pmag_safe * sin_theta)
    return np.sqrt(A**2 + ms_term**2)


def calibrate_bin(d0, sigma_d0_nominal, label=""):
    """Calibrate sigma_d0 scale factor from negative d0 tail.

    The negative tail of d0/sigma_d0 should be a unit Gaussian if sigma_d0
    is correctly estimated. Fit a scale factor to make the negative tail
    have unit width.

    Source: inspire_433306, Section 7.1 — negative tail method.

    Returns scale_factor, negative_tail_sigma, n_tracks.
    """
    # Compute significance with nominal sigma
    sig = d0 / sigma_d0_nominal

    # Select negative tail
    neg_mask = sig < 0
    neg_sig = sig[neg_mask]

    n_neg = len(neg_sig)
    if n_neg < 50:
        log.warning("Bin %s: only %d negative tracks, skipping", label, n_neg)
        return 1.0, np.nan, n_neg

    # Width of negative tail (should be 1.0 for correct sigma_d0)
    # Use robust estimator: MAD * 1.4826
    mad = np.median(np.abs(neg_sig - np.median(neg_sig)))
    neg_width = mad * 1.4826

    if neg_width < 0.01:
        log.warning("Bin %s: negligible negative width %.4f", label, neg_width)
        return 1.0, neg_width, n_neg

    # Scale factor to make unit width
    scale = neg_width
    log.info("  Bin %s: n_neg=%d, neg_width=%.3f, scale=%.3f",
             label, n_neg, neg_width, scale)

    return scale, neg_width, n_neg


def run_calibration(data_dict, prefix=""):
    """Run the full sigma_d0 calibration.

    Returns calibration results per bin.
    """
    d0_flat = data_dict[f"trk_d0"]
    d0_offsets = data_dict[f"trk_d0_offsets"]
    pmag_flat = data_dict[f"trk_pmag"]
    theta_flat = data_dict[f"trk_theta"]
    nvdet_flat = data_dict[f"trk_nvdet"]
    cos_theta_thrust = data_dict["cos_theta_thrust"]

    # Compute track-level |cos theta_thrust| by broadcasting event-level
    # to tracks using offsets
    n_events = len(d0_offsets) - 1
    trk_cos_thrust = np.empty_like(d0_flat)
    for i in range(n_events):
        start, end = d0_offsets[i], d0_offsets[i+1]
        trk_cos_thrust[start:end] = cos_theta_thrust[i]

    # Compute nominal sigma_d0
    sigma_d0_nom = compute_sigma_d0(pmag_flat, theta_flat, A_INIT, B_INIT)

    calibration_results = {}
    scale_factors = np.ones_like(d0_flat)

    for nv in NVDET_CLASSES:
        nv_mask = nvdet_flat >= nv if nv == 2 else nvdet_flat == nv

        for ip, (p_lo, p_hi) in enumerate(zip(P_BINS[:-1], P_BINS[1:])):
            p_mask = (pmag_flat >= p_lo) & (pmag_flat < p_hi)

            for ic, (ct_lo, ct_hi) in enumerate(zip(COSTHETA_BINS[:-1], COSTHETA_BINS[1:])):
                ct_mask = (np.abs(trk_cos_thrust) >= ct_lo) & (np.abs(trk_cos_thrust) < ct_hi)

                bin_mask = nv_mask & p_mask & ct_mask
                n_in_bin = int(np.sum(bin_mask))

                label = f"nv{nv}_p{ip}_ct{ic}"

                if n_in_bin < 100:
                    log.warning("Bin %s: only %d tracks, using default scale=1.0",
                                label, n_in_bin)
                    calibration_results[label] = {
                        "nvdet": nv,
                        "p_range": [p_lo, p_hi],
                        "costheta_range": [ct_lo, ct_hi],
                        "n_tracks": n_in_bin,
                        "scale_factor": 1.0,
                        "neg_width": None,
                    }
                    continue

                scale, neg_width, n_neg = calibrate_bin(
                    d0_flat[bin_mask],
                    sigma_d0_nom[bin_mask],
                    label=label,
                )

                scale_factors[bin_mask] = scale
                calibration_results[label] = {
                    "nvdet": nv,
                    "p_range": [p_lo, p_hi],
                    "costheta_range": [ct_lo, ct_hi],
                    "n_tracks": n_in_bin,
                    "n_neg": int(n_neg),
                    "scale_factor": float(scale),
                    "neg_width": float(neg_width) if not np.isnan(neg_width) else None,
                }

    # Corrected sigma_d0
    sigma_d0_corrected = sigma_d0_nom * scale_factors

    # Final significance
    significance = d0_flat / sigma_d0_corrected

    return calibration_results, sigma_d0_corrected, significance, scale_factors


def main():
    log.info("=" * 60)
    log.info("Phase 3: sigma_d0 Calibration [D7]")
    log.info("=" * 60)

    # Load preselected data
    data = load_npz(OUT / "preselected_data.npz")
    mc = load_npz(OUT / "preselected_mc.npz")

    # Run calibration on data
    log.info("Calibrating on DATA:")
    data_cal, data_sigma, data_sig, data_sf = run_calibration(data, "data")

    log.info("\nCalibrating on MC:")
    mc_cal, mc_sigma, mc_sig, mc_sf = run_calibration(mc, "mc")

    # Save calibration results
    params = {
        "A_init_cm": A_INIT,
        "B_init_cm_GeV": B_INIT,
        "source": "537303 (ALEPH VDET), inspire_433306 (negative tail method)",
        "angular_form": "sin(theta) [Rphi projection]",
        "data_calibration": data_cal,
        "mc_calibration": mc_cal,
    }
    with open(OUT / "sigma_d0_params.json", "w") as f:
        json.dump(params, f, indent=2, default=str)
    log.info("Saved sigma_d0_params.json")

    # Save significance arrays for downstream
    np.savez_compressed(
        OUT / "d0_significance.npz",
        # Data
        data_sigma_d0=data_sigma,
        data_significance=data_sig,
        data_scale_factors=data_sf,
        data_d0=data["trk_d0"],
        data_d0_offsets=data["trk_d0_offsets"],
        # MC
        mc_sigma_d0=mc_sigma,
        mc_significance=mc_sig,
        mc_scale_factors=mc_sf,
        mc_d0=mc["trk_d0"],
        mc_d0_offsets=mc["trk_d0_offsets"],
    )
    log.info("Saved d0_significance.npz")

    # Summary statistics
    log.info("\n--- Summary ---")
    log.info("Data: %d tracks, significance range [%.1f, %.1f]",
             len(data_sig), np.percentile(data_sig, 0.1),
             np.percentile(data_sig, 99.9))
    log.info("MC:   %d tracks, significance range [%.1f, %.1f]",
             len(mc_sig), np.percentile(mc_sig, 0.1),
             np.percentile(mc_sig, 99.9))

    # Check negative tail calibration quality
    neg_data = data_sig[data_sig < 0]
    neg_mc = mc_sig[mc_sig < 0]
    log.info("Data negative tail: sigma=%.3f (target: 1.0)",
             np.std(neg_data))
    log.info("MC negative tail: sigma=%.3f (target: 1.0)",
             np.std(neg_mc))


if __name__ == "__main__":
    main()
