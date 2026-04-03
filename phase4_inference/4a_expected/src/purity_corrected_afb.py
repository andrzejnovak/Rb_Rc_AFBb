"""Phase 4a REGRESSION: Purity-corrected A_FB^b as PRIMARY method.

Implements purity-corrected A_FB^b extraction following the method
developed in phase4b investigation (delta_b_calibration.py).

Key improvements over original afb_extraction.py:
1. Uses PUBLISHED delta_b values (ALEPH hep-ex/0509008 Table 12)
   instead of sigma(Q_h) as delta_b estimate
2. Corrects for finite b-purity using MC-calibrated flavour fractions
3. Subtracts charm asymmetry contribution (DATA ONLY — zero on MC)
4. Per-kappa results with chi2/ndf
5. Toy-based statistical uncertainty

BUG FIX (nikolai_164a): The charm correction previously used the
observed data AFB_C_OBS=0.0682 even when running on symmetric MC
(where A_FB=0 for all flavours by construction). This introduced a
spurious -0.078 asymmetry (15-sigma deviation). Fix: the extraction
function now takes afb_c and afb_uds as explicit parameters. On MC
these are 0; on data they are the observed LEP values.

The governing formula:
  <Q_FB>(cos theta) = sum_q f_q * delta_q * A_FB^q * cos(theta)

  slope = f_b * delta_b * A_FB^b + f_c * delta_c * A_FB^c + f_uds * delta_uds * A_FB^uds

  A_FB^b = (slope - f_c * delta_c * A_FB^c) / (f_b * delta_b)

where f_q are the tagged-sample flavour fractions from MC calibration.
A_FB^c must match the sample: 0 on symmetric MC, AFB_C_OBS on data.

Reads: phase3_selection/outputs/jet_charge.npz
       phase3_selection/outputs/hemisphere_tags.npz
       outputs/mc_calibration.json
Writes: outputs/purity_corrected_afb_results.json
"""
import json
import logging
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
P3_OUT = HERE.parents[2] / "phase3_selection" / "outputs"
OUT = HERE.parent / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

# SM values
# Source: hep-ex/0509008
R_B_SM = 0.21578
R_C_SM = 0.17223
R_UDS_SM = 1.0 - R_B_SM - R_C_SM
AFB_B_SM_POLE = 0.1032   # A_FB^{0,b} SM prediction
AFB_B_OBS = 0.0995        # observed A_FB^b at LEP (before QCD correction)
AFB_C_OBS = 0.0682        # observed A_FB^c at LEP
AFB_UDS = 0.0             # negligible for light quarks
SIN2_THETA_SM = 0.23153   # sin^2(theta_eff) SM

# QCD and QED corrections
# Source: hep-ex/0509008 Section 5.5
DELTA_QCD = 0.0356
DELTA_QCD_ERR = 0.0029
DELTA_QED = 0.001

# Published ALEPH charge separations
# Source: hep-ex/0509008 Table 12
PUBLISHED_DELTA = {
    0.3: {'delta_b': 0.162, 'delta_c': 0.100, 'delta_uds': 0.090},
    0.5: {'delta_b': 0.233, 'delta_c': 0.136, 'delta_uds': 0.115},
    1.0: {'delta_b': 0.374, 'delta_c': 0.198, 'delta_uds': 0.165},
    2.0: {'delta_b': 0.579, 'delta_c': 0.279, 'delta_uds': 0.220},
}

N_COS_BINS = 10
COS_RANGE = (-0.9, 0.9)
N_TOYS = 1000
TOY_SEED = 67890


def estimate_purity_at_wp(mc_cal, f_s_target):
    """Estimate flavour purities from MC calibration.

    From MC-calibrated efficiencies at each WP:
    f_q(WP) = eps_q(WP) * R_q / f_s(WP)
    """
    cal_points = []
    for thr_str, v in mc_cal.items():
        cal_points.append({
            'f_s': v['f_s'],
            'eps_b': v['eps_b'],
            'eps_c': v['eps_c'],
            'eps_uds': v['eps_uds'],
        })

    if not cal_points:
        return None

    # Use closest calibrated point
    closest = min(cal_points, key=lambda p: abs(p['f_s'] - f_s_target))
    denom = (closest['eps_b'] * R_B_SM +
             closest['eps_c'] * R_C_SM +
             closest['eps_uds'] * R_UDS_SM)
    if denom <= 0:
        return None

    f_b = closest['eps_b'] * R_B_SM / denom
    f_c = closest['eps_c'] * R_C_SM / denom
    f_uds = closest['eps_uds'] * R_UDS_SM / denom

    return {'f_b': f_b, 'f_c': f_c, 'f_uds': f_uds}


def measure_qfb_slope(qfb, cos_theta, tag_h0, tag_h1, threshold,
                       n_bins=N_COS_BINS, cos_range=COS_RANGE):
    """Measure <Q_FB> vs cos(theta) slope with intercept."""
    tagged = (tag_h0 > threshold) | (tag_h1 > threshold)
    valid = ~np.isnan(qfb) & tagged
    n_tagged = int(np.sum(valid))

    if n_tagged < 200:
        return None

    cos_sel = cos_theta[valid]
    qfb_sel = qfb[valid]

    bin_edges = np.linspace(cos_range[0], cos_range[1], n_bins + 1)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    mean_qfb = np.zeros(n_bins)
    sigma_qfb = np.zeros(n_bins)
    n_per_bin = np.zeros(n_bins, dtype=int)

    for i in range(n_bins):
        mask = (cos_sel >= bin_edges[i]) & (cos_sel < bin_edges[i + 1])
        n = np.sum(mask)
        n_per_bin[i] = n
        if n > 10:
            mean_qfb[i] = np.mean(qfb_sel[mask])
            sigma_qfb[i] = np.std(qfb_sel[mask]) / np.sqrt(n)
        else:
            mean_qfb[i] = np.nan
            sigma_qfb[i] = np.nan

    valid_bins = ~np.isnan(mean_qfb) & (sigma_qfb > 0)
    if np.sum(valid_bins) < 3:
        return None

    x = bin_centers[valid_bins]
    y = mean_qfb[valid_bins]
    w = 1.0 / sigma_qfb[valid_bins]**2

    # Weighted linear fit with intercept
    S0 = np.sum(w)
    S1 = np.sum(w * x)
    S2 = np.sum(w * x**2)
    Sy = np.sum(w * y)
    Sxy = np.sum(w * x * y)
    det = S0 * S2 - S1**2

    intercept = (S2 * Sy - S1 * Sxy) / det
    slope = (S0 * Sxy - S1 * Sy) / det
    sigma_slope = np.sqrt(S0 / det)

    residuals = y - (intercept + slope * x)
    chi2_val = float(np.sum(w * residuals**2))
    ndf_val = int(np.sum(valid_bins) - 2)
    p_value = 1.0 - chi2_dist.cdf(chi2_val, ndf_val) if ndf_val > 0 else np.nan

    return {
        'slope': float(slope),
        'sigma_slope': float(sigma_slope),
        'intercept': float(intercept),
        'chi2': chi2_val,
        'ndf': ndf_val,
        'p_value': float(p_value),
        'n_tagged': n_tagged,
        'bin_centers': bin_centers.tolist(),
        'mean_qfb': [float(v) if not np.isnan(v) else None for v in mean_qfb],
        'sigma_qfb': [float(v) if not np.isnan(v) else None for v in sigma_qfb],
        'n_per_bin': n_per_bin.tolist(),
    }


def extract_afb_purity_corrected(slope, sigma_slope, purity, kappa,
                                  afb_c=0.0, afb_uds=0.0):
    """Extract A_FB^b with purity and charm corrections.

    A_FB^b = (slope - f_c * delta_c * A_FB^c - f_uds * delta_uds * A_FB^uds)
             / (f_b * delta_b)

    Parameters
    ----------
    afb_c : float
        Forward-backward asymmetry of charm quarks in the SAMPLE being
        analyzed. For symmetric MC this is 0.0 (no EW asymmetry in
        generator). For data use AFB_C_OBS = 0.0682.
    afb_uds : float
        Forward-backward asymmetry of light quarks. Negligible in both
        MC and data (0.0).
    """
    pub = PUBLISHED_DELTA.get(kappa)
    if pub is None or purity is None:
        return None

    f_b = purity['f_b']
    f_c = purity['f_c']
    f_uds = purity['f_uds']
    delta_b = pub['delta_b']
    delta_c = pub['delta_c']
    delta_uds = pub['delta_uds']

    charm_correction = f_c * delta_c * afb_c
    uds_correction = f_uds * delta_uds * afb_uds

    denominator = f_b * delta_b
    if abs(denominator) < 1e-10:
        return None

    afb_b = (slope - charm_correction - uds_correction) / denominator
    sigma_afb = sigma_slope / denominator

    # Also compute naive (no purity correction) for comparison
    afb_naive = slope / delta_b
    sigma_naive = sigma_slope / delta_b

    return {
        'afb_purity_corrected': float(afb_b),
        'sigma_afb_purity': float(sigma_afb),
        'afb_naive': float(afb_naive),
        'sigma_naive': float(sigma_naive),
        'f_b': float(f_b),
        'f_c': float(f_c),
        'charm_correction': float(charm_correction),
        'delta_b_published': float(delta_b),
    }


def sin2theta_to_afb0(sin2theta):
    """Convert sin^2(theta_eff) to A_FB^{0,b}."""
    v_e = -0.5 + 2.0 * sin2theta
    a_e = -0.5
    A_e = 2.0 * v_e * a_e / (v_e**2 + a_e**2)

    v_b = -0.5 + (2.0 / 3.0) * sin2theta
    a_b = -0.5
    A_b = 2.0 * v_b * a_b / (v_b**2 + a_b**2)

    return 0.75 * A_e * A_b


def toy_uncertainty_afb(qfb, cos_theta, tag_h0, tag_h1, threshold,
                         purity, kappa, afb_c=0.0, afb_uds=0.0,
                         n_bins=N_COS_BINS,
                         n_toys=N_TOYS, seed=TOY_SEED):
    """Toy-based uncertainty for purity-corrected A_FB^b.

    Bootstrap the events and re-extract each time.
    """
    tagged = (tag_h0 > threshold) | (tag_h1 > threshold)
    valid = ~np.isnan(qfb) & tagged
    indices = np.where(valid)[0]
    n_total = len(indices)

    if n_total < 200:
        return np.nan, np.nan, [], 0

    rng = np.random.RandomState(seed)
    afb_toys = []

    for _ in range(n_toys):
        # Bootstrap resample
        boot_idx = rng.choice(indices, size=n_total, replace=True)
        cos_boot = cos_theta[boot_idx]
        qfb_boot = qfb[boot_idx]

        # Compute slope
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

        # Purity-corrected extraction
        result = extract_afb_purity_corrected(slope, 0.0, purity, kappa,
                                               afb_c=afb_c, afb_uds=afb_uds)
        if result is not None:
            afb_toys.append(result['afb_purity_corrected'])

    n_valid = len(afb_toys)
    if n_valid < 10:
        return np.nan, np.nan, [], n_valid

    arr = np.array(afb_toys)
    return float(np.mean(arr)), float(np.std(arr)), arr.tolist(), n_valid


def main():
    log.info("=" * 60)
    log.info("Phase 4a REGRESSION: Purity-Corrected A_FB^b (PRIMARY)")
    log.info("=" * 60)

    # Load data
    jc = np.load(P3_OUT / "jet_charge.npz", allow_pickle=False)
    tags = np.load(P3_OUT / "hemisphere_tags.npz", allow_pickle=False)
    mc_tag_h0 = tags["mc_combined_h0"]
    mc_tag_h1 = tags["mc_combined_h1"]
    cos_theta_mc = jc["cos_theta_mc"]
    n_mc = len(mc_tag_h0)
    log.info("MC events: %d", n_mc)

    # Load MC calibration
    with open(OUT / "mc_calibration.json") as f:
        mc_cal_data = json.load(f)
    mc_cal = mc_cal_data["full_mc_calibration"]

    # Load tag efficiencies for f_s
    with open(P3_OUT / "tag_efficiencies.json") as f:
        eff_data = json.load(f)
    mc_fs_by_wp = {}
    for entry in eff_data["combined_mc"]:
        mc_fs_by_wp[entry["threshold"]] = entry["f_s"]

    KAPPA_VALUES = [0.3, 0.5, 1.0, 2.0]
    KAPPA_LABELS = {0.3: 'k0.3', 0.5: 'k0.5', 1.0: 'k1.0', 2.0: 'k2.0'}
    thresholds = [2.0, 3.0, 5.0, 7.0, 9.0, 10.0]

    # CRITICAL: On symmetric MC, there is NO electroweak asymmetry in the
    # generator — A_FB is zero for ALL quark flavours. The charm asymmetry
    # correction must therefore use afb_c=0, NOT the observed data value
    # AFB_C_OBS=0.0682. Using data-derived AFB_C_OBS on MC was the source
    # of the -0.078 spurious asymmetry (15-sigma bug).
    # For data extraction (Phase 4b/4c), pass afb_c=AFB_C_OBS.
    MC_AFB_C = 0.0   # No EW asymmetry in symmetric MC
    MC_AFB_UDS = 0.0

    all_kappa_results = []

    for kappa in KAPPA_VALUES:
        k_str = KAPPA_LABELS[kappa]
        log.info("\n" + "=" * 50)
        log.info("kappa = %.1f", kappa)
        log.info("=" * 50)

        qfb_mc = jc[f"mc_qfb_{k_str}"]

        per_wp_results = []
        for thr in thresholds:
            slope_result = measure_qfb_slope(
                qfb_mc, cos_theta_mc, mc_tag_h0, mc_tag_h1, thr)
            if slope_result is None:
                continue

            f_s = mc_fs_by_wp.get(thr)
            purity = estimate_purity_at_wp(mc_cal, f_s) if f_s else None
            if purity is None:
                continue

            extraction = extract_afb_purity_corrected(
                slope_result['slope'], slope_result['sigma_slope'],
                purity, kappa,
                afb_c=MC_AFB_C, afb_uds=MC_AFB_UDS)
            if extraction is None:
                continue

            log.info("WP %.1f: slope=%.6f, naive_afb=%.4f, purity_afb=%.4f, "
                     "f_b=%.3f, chi2/ndf=%.2f/%d",
                     thr, slope_result['slope'],
                     extraction['afb_naive'],
                     extraction['afb_purity_corrected'],
                     extraction['f_b'],
                     slope_result['chi2'], slope_result['ndf'])

            per_wp_results.append({
                'threshold': float(thr),
                'slope': slope_result,
                'purity': purity,
                'extraction': extraction,
            })

        # Multi-WP combination: weighted average of purity-corrected A_FB^b
        if len(per_wp_results) >= 2:
            afb_vals = np.array([r['extraction']['afb_purity_corrected']
                                 for r in per_wp_results])
            afb_errs = np.array([r['extraction']['sigma_afb_purity']
                                 for r in per_wp_results])
            w = 1.0 / afb_errs**2
            afb_combined = np.sum(w * afb_vals) / np.sum(w)
            sigma_combined = 1.0 / np.sqrt(np.sum(w))

            chi2_wp = np.sum((afb_vals - afb_combined)**2 / afb_errs**2)
            ndf_wp = len(afb_vals) - 1
            p_wp = 1.0 - chi2_dist.cdf(chi2_wp, ndf_wp)

            log.info("Combined A_FB^b = %.4f +/- %.4f, chi2/ndf=%.2f/%d, p=%.3f",
                     afb_combined, sigma_combined, chi2_wp, ndf_wp, p_wp)
        else:
            if per_wp_results:
                afb_combined = per_wp_results[0]['extraction']['afb_purity_corrected']
                sigma_combined = per_wp_results[0]['extraction']['sigma_afb_purity']
            else:
                afb_combined = np.nan
                sigma_combined = np.nan
            chi2_wp, ndf_wp, p_wp = 0.0, 0, 1.0

        # Toy uncertainty at the best WP
        best_wp = min(per_wp_results, key=lambda r: r['extraction']['sigma_afb_purity']) if per_wp_results else None
        if best_wp:
            afb_mean_toy, afb_sigma_toy, _, n_valid_toy = toy_uncertainty_afb(
                qfb_mc, cos_theta_mc, mc_tag_h0, mc_tag_h1,
                best_wp['threshold'], best_wp['purity'], kappa,
                afb_c=MC_AFB_C, afb_uds=MC_AFB_UDS,
                n_toys=N_TOYS, seed=TOY_SEED)
            log.info("Toy uncertainty at WP %.1f: sigma=%.4f (n_valid=%d)",
                     best_wp['threshold'], afb_sigma_toy, n_valid_toy)
        else:
            afb_sigma_toy = np.nan
            n_valid_toy = 0

        kappa_result = {
            'kappa': float(kappa),
            'per_wp_results': per_wp_results,
            'combination': {
                'A_FB_b': float(afb_combined) if not np.isnan(afb_combined) else None,
                'sigma_A_FB_b': float(sigma_combined) if not np.isnan(sigma_combined) else None,
                'sigma_A_FB_b_toy': float(afb_sigma_toy) if not np.isnan(afb_sigma_toy) else None,
                'chi2_wp': float(chi2_wp),
                'ndf_wp': int(ndf_wp),
                'p_wp': float(p_wp),
            },
            'published_delta': PUBLISHED_DELTA.get(kappa),
        }
        all_kappa_results.append(kappa_result)

    # ================================================================
    # Cross-kappa combination
    # ================================================================
    log.info("\n--- Cross-Kappa Combination ---")
    afb_per_kappa = []
    err_per_kappa = []
    kappa_list = []

    for kr in all_kappa_results:
        comb = kr['combination']
        if comb['A_FB_b'] is not None and comb['sigma_A_FB_b'] is not None:
            if comb['sigma_A_FB_b'] > 0:
                afb_per_kappa.append(comb['A_FB_b'])
                err_per_kappa.append(comb['sigma_A_FB_b'])
                kappa_list.append(kr['kappa'])

    if len(afb_per_kappa) >= 2:
        afb_arr = np.array(afb_per_kappa)
        err_arr = np.array(err_per_kappa)
        w = 1.0 / err_arr**2
        afb_final = np.sum(w * afb_arr) / np.sum(w)
        sigma_final = 1.0 / np.sqrt(np.sum(w))
        chi2_kappa = np.sum((afb_arr - afb_final)**2 / err_arr**2)
        ndf_kappa = len(afb_arr) - 1
        p_kappa = 1.0 - chi2_dist.cdf(chi2_kappa, ndf_kappa)

        log.info("Final A_FB^b = %.4f +/- %.4f", afb_final, sigma_final)
        log.info("Kappa chi2/ndf = %.2f/%d, p = %.3f",
                 chi2_kappa, ndf_kappa, p_kappa)
    elif afb_per_kappa:
        afb_final = afb_per_kappa[0]
        sigma_final = err_per_kappa[0]
        chi2_kappa, ndf_kappa, p_kappa = 0.0, 0, 1.0
    else:
        afb_final = np.nan
        sigma_final = np.nan
        chi2_kappa, ndf_kappa, p_kappa = 0.0, 0, 1.0

    # ================================================================
    # Pole asymmetry and sin^2(theta_eff)
    # ================================================================
    if not np.isnan(afb_final):
        afb_0_b = afb_final / (1.0 - DELTA_QCD - DELTA_QED)
        log.info("A_FB^{0,b} = %.4f", afb_0_b)

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
            sin2theta_fit = np.nan
            sigma_sin2theta = np.nan
    else:
        afb_0_b = np.nan
        sin2theta_fit = np.nan
        sigma_sin2theta = np.nan

    # Note: on symmetric MC, A_FB^b should be ~0.
    # The purity-corrected value may differ from 0 due to
    # charm correction and finite statistics.
    log.info("\nNOTE: On symmetric MC, A_FB^b = 0 by construction.")
    log.info("Non-zero values reflect statistical fluctuations and")
    log.info("the charm correction term. Valid comparison to SM")
    log.info("requires Phase 4b/4c with real data.")

    # ================================================================
    # Output
    # ================================================================
    output = {
        'method': 'Purity-corrected A_FB^b with published delta_b',
        'description': (
            'A_FB^b extraction using published ALEPH charge separations '
            'and MC-calibrated flavour fractions to correct for finite '
            'b-purity and charm contamination. This replaces the naive '
            'slope/sigma(Q_h) method which overestimates the physical '
            'delta_b.'
        ),
        'kappa_results': all_kappa_results,
        'combination': {
            'A_FB_b': float(afb_final) if not np.isnan(afb_final) else None,
            'sigma_A_FB_b': float(sigma_final) if not np.isnan(sigma_final) else None,
            'A_FB_0_b': float(afb_0_b) if not np.isnan(afb_0_b) else None,
            'chi2_kappa': float(chi2_kappa),
            'ndf_kappa': int(ndf_kappa),
            'p_kappa': float(p_kappa) if not np.isnan(p_kappa) else None,
            'kappas_used': kappa_list,
        },
        'sin2theta': {
            'value': float(sin2theta_fit) if not np.isnan(sin2theta_fit) else None,
            'sigma_stat': float(sigma_sin2theta) if not np.isnan(sigma_sin2theta) else None,
            'SM': SIN2_THETA_SM,
        },
        'qcd_correction': {
            'delta_QCD': DELTA_QCD,
            'delta_QCD_err': DELTA_QCD_ERR,
            'delta_QED': DELTA_QED,
            'source': 'hep-ex/0509008 Section 5.5',
        },
        'published_delta_source': 'ALEPH hep-ex/0509008 Table 12',
        'mc_note': ('On symmetric MC, A_FB^b = 0 by construction. '
                    'Values here reflect noise + charm correction residuals. '
                    'Valid comparison requires Phase 4b/4c data.'),
    }

    with open(OUT / "purity_corrected_afb_results.json", "w") as f:
        json.dump(output, f, indent=2, default=str)
    log.info("\nSaved purity_corrected_afb_results.json")


if __name__ == "__main__":
    main()
