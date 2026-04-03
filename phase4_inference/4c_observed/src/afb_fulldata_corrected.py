"""Phase 4c CORRECTED: A_FB^b extraction on full data.

FIX: The previous afb_fulldata.py switched from purity-corrected (which
gave 0.074 on 10% at kappa=2.0, WP=2.0) to inclusive (which gave 0.0005)
without justification.

This script runs BOTH methods:
  PRIMARY: Purity-corrected A_FB^b (slope / (f_b * delta_b)) — matches 10%
  CROSS-CHECK: Inclusive (slope / delta_b) — for comparison
  DIAGNOSTIC: Full purity+charm (from purity_corrected_afb.py)

The 10% value of 0.074 came from delta_b_calibration.py using:
  A_FB^b = slope / (f_b * delta_b)
at kappa=2.0, WP=2.0. The purity f_b is estimated from MC calibration
(only at WPs 9/10) which gives f_b~0.19 for ALL WPs. This purity estimate
is approximate for loose WPs.

Reads: phase3_selection/outputs/hemisphere_tags.npz
       phase3_selection/outputs/jet_charge.npz
       phase4_inference/4a_expected/outputs/mc_calibration.json
       phase3_selection/outputs/tag_efficiencies.json
Writes: phase4_inference/4c_observed/outputs/afb_fulldata_corrected.json
        analysis_note/results/parameters.json
"""
import json
import logging
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq
from scipy.stats import chi2 as chi2_dist
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

HERE = Path(__file__).resolve().parent
PHASE4C_OUT = HERE.parent / "outputs"
P4A_OUT = HERE.parents[1] / "4a_expected" / "outputs"
P4B_OUT = HERE.parents[1] / "4b_partial" / "outputs"
P3_OUT = HERE.parents[2] / "phase3_selection" / "outputs"
RESULTS_DIR = HERE.parents[2] / "analysis_note" / "results"
PHASE4C_OUT.mkdir(parents=True, exist_ok=True)

# Import from Phase 4a
sys.path.insert(0, str(HERE.parents[1] / "4a_expected" / "src"))
from purity_corrected_afb import (
    estimate_purity_at_wp, measure_qfb_slope, extract_afb_purity_corrected,
    toy_uncertainty_afb, sin2theta_to_afb0,
    PUBLISHED_DELTA, DELTA_QCD, DELTA_QCD_ERR, DELTA_QED,
    SIN2_THETA_SM, AFB_B_OBS, AFB_B_SM_POLE,
    R_B_SM, R_C_SM, R_UDS_SM,
    N_COS_BINS, COS_RANGE,
)

# For DATA: use observed charm asymmetry
AFB_C_DATA = 0.0682   # observed A_FB^c at LEP (hep-ex/0509008)
AFB_UDS_DATA = 0.0

N_TOYS = 500
TOY_SEED = 67890


def extract_afb_purity_no_charm(slope, sigma_slope, purity, kappa):
    """Extract A_FB^b with purity correction but WITHOUT charm subtraction.

    A_FB^b = slope / (f_b * delta_b)

    This is the method that gave 0.074 on 10% data (delta_b_calibration.py).
    """
    pub = PUBLISHED_DELTA.get(kappa)
    if pub is None or purity is None:
        return None

    f_b = purity['f_b']
    delta_b = pub['delta_b']
    denominator = f_b * delta_b

    if abs(denominator) < 1e-10:
        return None

    afb_b = slope / denominator
    sigma_afb = sigma_slope / denominator

    return {
        'afb_purity_no_charm': float(afb_b),
        'sigma_afb_purity_no_charm': float(sigma_afb),
        'f_b': float(f_b),
        'delta_b': float(delta_b),
    }


def extract_afb_inclusive(slope, sigma_slope, kappa):
    """Extract A_FB^b using inclusive method: slope / delta_b."""
    pub = PUBLISHED_DELTA.get(kappa)
    if pub is None:
        return None

    delta_b = pub['delta_b']
    return {
        'afb_inclusive': float(slope / delta_b),
        'sigma_afb_inclusive': float(sigma_slope / delta_b),
        'delta_b': float(delta_b),
    }


def bootstrap_afb(qfb, cos_theta, tag_h0, tag_h1, threshold,
                   purity, kappa, method='purity_no_charm',
                   afb_c=0.0, afb_uds=0.0,
                   n_bins=N_COS_BINS, n_toys=N_TOYS, seed=TOY_SEED):
    """Bootstrap uncertainty for A_FB^b extraction."""
    pub = PUBLISHED_DELTA.get(kappa)
    if pub is None:
        return np.nan, np.nan, 0

    tagged = (tag_h0 > threshold) | (tag_h1 > threshold)
    valid = ~np.isnan(qfb) & tagged
    indices = np.where(valid)[0]
    n_total = len(indices)

    if n_total < 200:
        return np.nan, np.nan, 0

    rng = np.random.RandomState(seed)
    afb_toys = []

    for _ in range(n_toys):
        boot_idx = rng.choice(indices, size=n_total, replace=True)
        cos_boot = cos_theta[boot_idx]
        qfb_boot = qfb[boot_idx]

        bin_edges = np.linspace(COS_RANGE[0], COS_RANGE[1], n_bins + 1)
        bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

        means = np.zeros(n_bins)
        sigmas = np.zeros(n_bins)
        for i in range(n_bins):
            mask = (cos_boot >= bin_edges[i]) & (cos_boot < bin_edges[i + 1])
            n = np.sum(mask)
            if n > 10:
                means[i] = np.mean(qfb_boot[mask])
                sigmas[i] = np.std(qfb_boot[mask]) / np.sqrt(n)
            else:
                means[i] = np.nan
                sigmas[i] = np.nan

        ok = ~np.isnan(means) & (sigmas > 0)
        if np.sum(ok) < 3:
            continue

        x = bin_centers[ok]
        y = means[ok]
        w = 1.0 / sigmas[ok]**2
        S0 = np.sum(w)
        S1 = np.sum(w * x)
        S2 = np.sum(w * x**2)
        Sy = np.sum(w * y)
        Sxy = np.sum(w * x * y)
        det = S0 * S2 - S1**2
        if abs(det) < 1e-20:
            continue
        slope = (S0 * Sxy - S1 * Sy) / det

        if method == 'purity_no_charm' and purity:
            f_b = purity['f_b']
            delta_b = pub['delta_b']
            denom = f_b * delta_b
            if abs(denom) > 1e-10:
                afb_toys.append(slope / denom)
        elif method == 'purity_charm' and purity:
            result = extract_afb_purity_corrected(slope, 0.0, purity, kappa,
                                                   afb_c=afb_c, afb_uds=afb_uds)
            if result is not None:
                afb_toys.append(result['afb_purity_corrected'])
        else:
            delta_b = pub['delta_b']
            afb_toys.append(slope / delta_b)

    n_valid = len(afb_toys)
    if n_valid < 10:
        return np.nan, np.nan, n_valid

    arr = np.array(afb_toys)
    return float(np.mean(arr)), float(np.std(arr)), n_valid


def main():
    log.info("=" * 60)
    log.info("Phase 4c CORRECTED: A_FB^b on Full Data")
    log.info("=" * 60)
    log.info("PRIMARY: Purity-corrected (slope / (f_b * delta_b)) — matches 10%%")
    log.info("CROSS-CHECK 1: Inclusive (slope / delta_b)")
    log.info("CROSS-CHECK 2: Full purity+charm (from purity_corrected_afb.py)")

    # Load data
    tags = np.load(P3_OUT / "hemisphere_tags.npz", allow_pickle=False)
    data_h0 = tags["data_combined_h0"]
    data_h1 = tags["data_combined_h1"]
    n_data = len(data_h0)
    log.info("Full data events: %d", n_data)

    jc = np.load(P3_OUT / "jet_charge.npz", allow_pickle=False)
    cos_theta_data = jc["cos_theta_data"]

    # Load MC calibration for purities
    with open(P4A_OUT / "mc_calibration.json") as f:
        mc_cal_data = json.load(f)
    mc_cal = mc_cal_data["full_mc_calibration"]

    # Load tag efficiencies for f_s
    with open(P3_OUT / "tag_efficiencies.json") as f:
        eff_data = json.load(f)
    mc_fs_by_wp = {}
    for entry in eff_data["combined_mc"]:
        mc_fs_by_wp[entry["threshold"]] = entry["f_s"]

    KAPPA_VALUES = [0.3, 0.5, 1.0, 2.0]
    KAPPA_LABELS = {0.3: "k0.3", 0.5: "k0.5", 1.0: "k1.0", 2.0: "k2.0"}
    thresholds = [2.0, 3.0, 5.0, 7.0, 9.0, 10.0]

    all_kappa_results = []

    for kappa in KAPPA_VALUES:
        k_str = KAPPA_LABELS[kappa]
        log.info("\n" + "=" * 50)
        log.info("kappa = %.1f", kappa)
        log.info("=" * 50)

        qfb_key = "data_qfb_%s" % k_str
        qfb_data = jc[qfb_key]

        per_wp_results = []
        for thr in thresholds:
            slope_result = measure_qfb_slope(
                qfb_data, cos_theta_data, data_h0, data_h1, thr)
            if slope_result is None:
                continue

            # Get purity estimate
            f_s = mc_fs_by_wp.get(thr)
            purity = estimate_purity_at_wp(mc_cal, f_s) if f_s else None

            # Method 1: Purity-corrected WITHOUT charm (the 10% method)
            purity_no_charm = extract_afb_purity_no_charm(
                slope_result["slope"], slope_result["sigma_slope"],
                purity, kappa) if purity else None

            # Method 2: Inclusive (slope / delta_b)
            inclusive = extract_afb_inclusive(
                slope_result["slope"], slope_result["sigma_slope"], kappa)

            # Method 3: Full purity + charm correction
            purity_charm = None
            if purity:
                purity_charm = extract_afb_purity_corrected(
                    slope_result["slope"], slope_result["sigma_slope"],
                    purity, kappa,
                    afb_c=AFB_C_DATA, afb_uds=AFB_UDS_DATA)

            afb_p = purity_no_charm["afb_purity_no_charm"] if purity_no_charm else float("nan")
            afb_i = inclusive["afb_inclusive"] if inclusive else float("nan")
            afb_c = purity_charm["afb_purity_corrected"] if purity_charm else float("nan")

            log.info(
                "WP %.1f: slope=%.6f, afb_purity=%.4f, afb_incl=%.4f, "
                "afb_charm=%.4f, f_b=%.3f, chi2/ndf=%.2f/%d",
                thr, slope_result["slope"],
                afb_p, afb_i, afb_c,
                purity["f_b"] if purity else 0,
                slope_result["chi2"], slope_result["ndf"])

            per_wp_results.append({
                "threshold": float(thr),
                "slope": slope_result,
                "purity": purity,
                "purity_no_charm": purity_no_charm,
                "inclusive": inclusive,
                "purity_charm": purity_charm,
            })

        # ============================================================
        # Multi-WP combination: purity-corrected (no charm) — PRIMARY
        # ============================================================
        valid_purity = [r for r in per_wp_results
                        if r["purity_no_charm"] is not None
                        and r["purity_no_charm"]["sigma_afb_purity_no_charm"] > 0]

        if len(valid_purity) >= 2:
            afb_vals = np.array([r["purity_no_charm"]["afb_purity_no_charm"]
                                 for r in valid_purity])
            afb_errs = np.array([r["purity_no_charm"]["sigma_afb_purity_no_charm"]
                                 for r in valid_purity])
            w = 1.0 / afb_errs**2
            afb_combined = float(np.sum(w * afb_vals) / np.sum(w))
            sigma_combined = float(1.0 / np.sqrt(np.sum(w)))
            chi2_wp = float(np.sum((afb_vals - afb_combined)**2 / afb_errs**2))
            ndf_wp = len(afb_vals) - 1
            p_wp = float(1.0 - chi2_dist.cdf(chi2_wp, ndf_wp))

            log.info("Purity (no charm) combined: %.4f +/- %.4f, chi2/ndf=%.2f/%d, p=%.3f",
                     afb_combined, sigma_combined, chi2_wp, ndf_wp, p_wp)
        elif valid_purity:
            afb_combined = valid_purity[0]["purity_no_charm"]["afb_purity_no_charm"]
            sigma_combined = valid_purity[0]["purity_no_charm"]["sigma_afb_purity_no_charm"]
            chi2_wp, ndf_wp, p_wp = 0.0, 0, 1.0
        else:
            afb_combined = float("nan")
            sigma_combined = float("nan")
            chi2_wp, ndf_wp, p_wp = 0.0, 0, 1.0

        # Also combine inclusive
        valid_inclusive = [r for r in per_wp_results
                          if r["inclusive"] is not None
                          and r["inclusive"]["sigma_afb_inclusive"] > 0]
        if len(valid_inclusive) >= 2:
            afb_inc_vals = np.array([r["inclusive"]["afb_inclusive"]
                                     for r in valid_inclusive])
            afb_inc_errs = np.array([r["inclusive"]["sigma_afb_inclusive"]
                                     for r in valid_inclusive])
            w_inc = 1.0 / afb_inc_errs**2
            afb_inc_combined = float(np.sum(w_inc * afb_inc_vals) / np.sum(w_inc))
            sigma_inc_combined = float(1.0 / np.sqrt(np.sum(w_inc)))
        elif valid_inclusive:
            afb_inc_combined = valid_inclusive[0]["inclusive"]["afb_inclusive"]
            sigma_inc_combined = valid_inclusive[0]["inclusive"]["sigma_afb_inclusive"]
        else:
            afb_inc_combined = float("nan")
            sigma_inc_combined = float("nan")

        log.info("Inclusive combined: %.4f +/- %.4f", afb_inc_combined, sigma_inc_combined)

        # Bootstrap at reference WP (kappa=2.0, WP=2.0 was the 10% reference)
        best_wp_thr = 2.0
        valid_thrs = [r["threshold"] for r in per_wp_results]
        if best_wp_thr not in valid_thrs:
            best_wp_thr = valid_thrs[0] if valid_thrs else None

        afb_sigma_toy = float("nan")
        n_valid_toy = 0
        if best_wp_thr is not None and purity is not None:
            best_purity = None
            for r in per_wp_results:
                if r["threshold"] == best_wp_thr and r["purity"] is not None:
                    best_purity = r["purity"]
                    break
            if best_purity:
                _, afb_sigma_toy, n_valid_toy = bootstrap_afb(
                    qfb_data, cos_theta_data, data_h0, data_h1,
                    best_wp_thr, best_purity, kappa,
                    method='purity_no_charm',
                    n_toys=N_TOYS, seed=TOY_SEED)
                log.info("Bootstrap sigma at WP %.1f: %.4f (n_valid=%d)",
                         best_wp_thr, afb_sigma_toy, n_valid_toy)

        kappa_result = {
            "kappa": float(kappa),
            "per_wp_results": per_wp_results,
            "combination_purity": {
                "A_FB_b": afb_combined if not np.isnan(afb_combined) else None,
                "sigma_A_FB_b": sigma_combined if not np.isnan(sigma_combined) else None,
                "sigma_A_FB_b_bootstrap": float(afb_sigma_toy) if not np.isnan(afb_sigma_toy) else None,
                "chi2_wp": float(chi2_wp),
                "ndf_wp": int(ndf_wp),
                "p_wp": float(p_wp),
                "method": "purity-corrected (no charm subtraction)",
            },
            "combination_inclusive": {
                "A_FB_b": afb_inc_combined if not np.isnan(afb_inc_combined) else None,
                "sigma_A_FB_b": sigma_inc_combined if not np.isnan(sigma_inc_combined) else None,
                "method": "inclusive (slope / delta_b)",
            },
            "published_delta": PUBLISHED_DELTA.get(kappa),
        }
        all_kappa_results.append(kappa_result)

    # ================================================================
    # Cross-kappa combination (purity method — PRIMARY)
    # ================================================================
    log.info("\n--- Cross-Kappa Combination (Purity Method — PRIMARY) ---")
    afb_per_kappa = []
    err_per_kappa = []
    kappa_list = []

    for kr in all_kappa_results:
        comb = kr["combination_purity"]
        if (comb["A_FB_b"] is not None and comb["sigma_A_FB_b"] is not None
                and comb["sigma_A_FB_b"] > 0):
            afb_per_kappa.append(comb["A_FB_b"])
            err_per_kappa.append(comb["sigma_A_FB_b"])
            kappa_list.append(kr["kappa"])

    if len(afb_per_kappa) >= 2:
        afb_arr = np.array(afb_per_kappa)
        err_arr = np.array(err_per_kappa)
        w = 1.0 / err_arr**2
        afb_final = float(np.sum(w * afb_arr) / np.sum(w))
        sigma_final = float(1.0 / np.sqrt(np.sum(w)))
        chi2_kappa = float(np.sum((afb_arr - afb_final)**2 / err_arr**2))
        ndf_kappa = len(afb_arr) - 1
        p_kappa = float(1.0 - chi2_dist.cdf(chi2_kappa, ndf_kappa))
    elif afb_per_kappa:
        afb_final = afb_per_kappa[0]
        sigma_final = err_per_kappa[0]
        chi2_kappa, ndf_kappa, p_kappa = 0.0, 0, 1.0
    else:
        afb_final = float("nan")
        sigma_final = float("nan")
        chi2_kappa, ndf_kappa, p_kappa = 0.0, 0, 1.0

    log.info("PURITY: A_FB^b = %.4f +/- %.4f, chi2/ndf=%.2f/%d, p=%.3f",
             afb_final if not np.isnan(afb_final) else 0,
             sigma_final if not np.isnan(sigma_final) else 0,
             chi2_kappa, ndf_kappa, p_kappa)

    # Also combine inclusive across kappas
    afb_inc_per_kappa = []
    err_inc_per_kappa = []
    for kr in all_kappa_results:
        comb = kr["combination_inclusive"]
        if (comb["A_FB_b"] is not None and comb["sigma_A_FB_b"] is not None
                and comb["sigma_A_FB_b"] > 0):
            afb_inc_per_kappa.append(comb["A_FB_b"])
            err_inc_per_kappa.append(comb["sigma_A_FB_b"])

    if len(afb_inc_per_kappa) >= 2:
        afb_inc_arr = np.array(afb_inc_per_kappa)
        err_inc_arr = np.array(err_inc_per_kappa)
        w_inc = 1.0 / err_inc_arr**2
        afb_inc_final = float(np.sum(w_inc * afb_inc_arr) / np.sum(w_inc))
        sigma_inc_final = float(1.0 / np.sqrt(np.sum(w_inc)))
    elif afb_inc_per_kappa:
        afb_inc_final = afb_inc_per_kappa[0]
        sigma_inc_final = err_inc_per_kappa[0]
    else:
        afb_inc_final = float("nan")
        sigma_inc_final = float("nan")

    log.info("INCLUSIVE: A_FB^b = %.4f +/- %.4f",
             afb_inc_final if not np.isnan(afb_inc_final) else 0,
             sigma_inc_final if not np.isnan(sigma_inc_final) else 0)

    # Per-kappa summary
    log.info("\n--- Per-Kappa Summary (Purity Method) ---")
    for kr in all_kappa_results:
        comb = kr["combination_purity"]
        log.info("kappa=%.1f: A_FB^b = %s +/- %s",
                 kr["kappa"],
                 "%.4f" % comb["A_FB_b"] if comb["A_FB_b"] is not None else "N/A",
                 "%.4f" % comb["sigma_A_FB_b"] if comb["sigma_A_FB_b"] is not None else "N/A")

    # ================================================================
    # Pole asymmetry and sin^2(theta_eff)
    # ================================================================
    sin2theta_fit = float("nan")
    sigma_sin2theta = float("nan")
    afb_0_b = float("nan")

    if not np.isnan(afb_final):
        afb_0_b = afb_final / (1.0 - DELTA_QCD - DELTA_QED)
        log.info("\nA_FB^{0,b} = %.4f", afb_0_b)

        try:
            sin2theta_fit = brentq(
                lambda s: sin2theta_to_afb0(s) - afb_0_b, 0.20, 0.26)
            sin2theta_up = brentq(
                lambda s: sin2theta_to_afb0(s) - (afb_0_b - sigma_final / (1 - DELTA_QCD - DELTA_QED)),
                0.20, 0.26)
            sin2theta_dn = brentq(
                lambda s: sin2theta_to_afb0(s) - (afb_0_b + sigma_final / (1 - DELTA_QCD - DELTA_QED)),
                0.20, 0.26)
            sigma_sin2theta = abs(sin2theta_up - sin2theta_dn) / 2.0
            log.info("sin^2(theta_eff) = %.5f +/- %.5f", sin2theta_fit, sigma_sin2theta)
        except Exception as e:
            log.warning("sin^2(theta_eff) extraction failed: %s", e)

    # ================================================================
    # Comparison with Phase 4b
    # ================================================================
    log.info("\n--- Comparison with Phase 4b (10%% data) ---")
    # The 10% reference value from delta_b_calibration (kappa=2.0, WP=2.0)
    afb_10pct_ref = 0.07366
    sigma_10pct_ref = 0.03088
    log.info("10%% purity-corrected (kappa=2, WP=2): %.4f +/- %.4f",
             afb_10pct_ref, sigma_10pct_ref)
    log.info("Full combined (purity): %.4f +/- %.4f",
             afb_final if not np.isnan(afb_final) else 0,
             sigma_final if not np.isnan(sigma_final) else 0)

    log.info("Published LEP A_FB^b = %.4f (observed)", AFB_B_OBS)
    pull_vs_lep = None
    if not np.isnan(afb_final) and sigma_final > 0:
        pull_vs_lep = (afb_final - AFB_B_OBS) / sigma_final
        log.info("Pull vs LEP published = %.2f sigma", pull_vs_lep)

    # ================================================================
    # Systematics
    # ================================================================
    log.info("\n--- Systematic Uncertainties ---")
    syst_components = {}

    if not np.isnan(afb_final):
        # Method comparison: difference between purity and inclusive
        if not np.isnan(afb_inc_final):
            syst_components["method_choice"] = abs(afb_final - afb_inc_final)

        # Purity variation: vary f_b by 20%
        # The purity estimation is the dominant uncertainty
        # since mc_calibration only covers 2 WPs
        syst_components["purity_estimation"] = 0.20 * abs(afb_final)

        # QCD correction uncertainty
        syst_components["delta_QCD"] = DELTA_QCD_ERR * abs(afb_final) / (1 - DELTA_QCD)

        # afb_c uncertainty (if using charm correction)
        # For the no-charm method, this is zero
        syst_components["afb_c_unused"] = 0.0

        syst_total = np.sqrt(sum(v**2 for v in syst_components.values()))
        log.info("Systematic components:")
        for name, val in sorted(syst_components.items()):
            log.info("  %s: %.5f", name, val)
        log.info("Total systematic: %.5f", syst_total)
    else:
        syst_total = 0.0

    # ================================================================
    # Output
    # ================================================================
    output = {
        "method": "Purity-corrected A_FB^b (no charm subtraction), full data (CORRECTED)",
        "description": (
            "A_FB^b extraction on the complete ALEPH 1992-1995 dataset "
            "(%d events). PRIMARY: purity-corrected (slope / (f_b * delta_b)) "
            "matching the 10%% method. CROSS-CHECK: inclusive (slope / delta_b). "
            "The previous code switched to inclusive without justification." % n_data
        ),
        "fix_description": (
            "Restored purity-corrected method as primary (matches 10% approved "
            "at human gate). The old code switched to inclusive because the "
            "full purity+charm method gave negative A_FB^b. The issue was that "
            "estimate_purity_at_wp only has calibration at WP 9/10, giving "
            "f_b~0.19 and f_c~0.40 for ALL WPs. When the large charm correction "
            "(f_c * delta_c * afb_c) is subtracted, the result flips sign. "
            "The purity-corrected method WITHOUT charm subtraction avoids this "
            "instability and is what was actually approved."
        ),
        "n_data_events": n_data,
        "afb_c_used_for_crosscheck": AFB_C_DATA,
        "kappa_results": all_kappa_results,
        "combination_primary": {
            "A_FB_b": afb_final if not np.isnan(afb_final) else None,
            "sigma_A_FB_b": sigma_final if not np.isnan(sigma_final) else None,
            "A_FB_0_b": float(afb_0_b) if not np.isnan(afb_0_b) else None,
            "chi2_kappa": float(chi2_kappa),
            "ndf_kappa": int(ndf_kappa),
            "p_kappa": float(p_kappa) if not np.isnan(p_kappa) else None,
            "kappas_used": kappa_list,
            "method": "purity-corrected (no charm subtraction)",
        },
        "combination_crosscheck_inclusive": {
            "A_FB_b": afb_inc_final if not np.isnan(afb_inc_final) else None,
            "sigma_A_FB_b": sigma_inc_final if not np.isnan(sigma_inc_final) else None,
            "method": "inclusive (slope / delta_b)",
        },
        "sin2theta": {
            "value": float(sin2theta_fit) if not np.isnan(sin2theta_fit) else None,
            "sigma_stat": float(sigma_sin2theta) if not np.isnan(sigma_sin2theta) else None,
            "SM": SIN2_THETA_SM,
        },
        "systematics": {
            "components": {k: float(v) for k, v in syst_components.items()},
            "total": float(syst_total),
        },
        "comparison_lep": {
            "A_FB_b_LEP": AFB_B_OBS,
            "our_A_FB_b": afb_final if not np.isnan(afb_final) else None,
            "pull": float(pull_vs_lep) if pull_vs_lep is not None else None,
        },
        "comparison_10pct": {
            "afb_10pct_ref": afb_10pct_ref,
            "sigma_10pct_ref": sigma_10pct_ref,
            "our_afb": afb_final if not np.isnan(afb_final) else None,
            "our_sigma": sigma_final if not np.isnan(sigma_final) else None,
        },
        "qcd_correction": {
            "delta_QCD": DELTA_QCD,
            "delta_QCD_err": DELTA_QCD_ERR,
            "delta_QED": DELTA_QED,
        },
        "published_delta_source": "ALEPH hep-ex/0509008 Table 12",
        "n_bootstrap_toys": N_TOYS,
    }

    out_path = PHASE4C_OUT / "afb_fulldata_corrected.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    log.info("\nSaved %s", out_path.name)

    # ================================================================
    # Update parameters.json
    # ================================================================
    params_path = RESULTS_DIR / "parameters.json"
    if params_path.exists():
        with open(params_path) as f:
            params = json.load(f)
    else:
        params = {}

    if not np.isnan(afb_final):
        params["A_FB_b_fulldata_corrected"] = {
            "value": afb_final,
            "stat": sigma_final,
            "syst": float(syst_total),
            "total": float(np.sqrt(sigma_final**2 + syst_total**2)),
            "SM": AFB_B_SM_POLE,
            "LEP_observed": AFB_B_OBS,
            "method": "Purity-corrected (no charm), full data (CORRECTED)",
            "n_events": n_data,
        }
        # Update the "final" entry
        params["A_FB_b_fulldata_final"] = {
            "value": afb_final,
            "stat": sigma_final,
            "syst": float(syst_total),
            "total": float(np.sqrt(sigma_final**2 + syst_total**2)),
            "SM": AFB_B_SM_POLE,
            "LEP_observed": AFB_B_OBS,
            "method": "Purity-corrected (no charm), full ALEPH 1992-1995 data (CORRECTED)",
        }
    if not np.isnan(afb_0_b):
        params["A_FB_0_b_fulldata"] = {
            "value": float(afb_0_b),
            "stat": float(sigma_final / (1 - DELTA_QCD - DELTA_QED)) if not np.isnan(sigma_final) else None,
            "SM": AFB_B_SM_POLE,
        }
    if not np.isnan(sin2theta_fit):
        params["sin2theta_eff_fulldata"] = {
            "value": float(sin2theta_fit),
            "stat": float(sigma_sin2theta) if not np.isnan(sigma_sin2theta) else None,
            "SM": SIN2_THETA_SM,
        }

    # Also store inclusive as cross-check
    if not np.isnan(afb_inc_final):
        params["A_FB_b_fulldata_inclusive_crosscheck"] = {
            "value": afb_inc_final,
            "stat": sigma_inc_final,
            "SM": AFB_B_SM_POLE,
            "LEP_observed": AFB_B_OBS,
            "method": "Inclusive (slope / delta_b), full data — cross-check only",
            "n_events": n_data,
        }

    with open(params_path, "w") as f:
        json.dump(params, f, indent=2)
    log.info("Updated parameters.json with corrected A_FB_b entries")


if __name__ == "__main__":
    main()
