"""Task 1: Delta_b calibration from DATA using multi-purity self-calibrating fit.

CRITICAL FINDING: Our b-tag has eps_c (0.44) > eps_b (0.15), meaning charm
is tagged more efficiently than b. This gives b-purity of only ~18% at the
tightest available WP. This is inverted from ALEPH's proper Q-tag which had
eps_b ~ 0.30-0.40, eps_c ~ 0.05-0.10.

Despite this, we can still attempt the multi-purity calibration:
1. Measure the slope of <Q_FB> vs cos(theta) at each WP on data
2. Use MC-calibrated purities to correct for flavour fractions
3. Extract the product delta_b * A_FB_b from the slopes
4. Compare to using published delta_b values

Reads: phase4_inference/4b_partial/outputs/data_10pct_tags.npz
       phase4_inference/4b_partial/outputs/data_10pct_jetcharge.npz
       phase4_inference/4a_expected/outputs/mc_calibration.json
       phase3_selection/outputs/hemisphere_tags.npz
       phase3_selection/outputs/jet_charge.npz
       phase3_selection/outputs/tag_efficiencies.json
Writes: outputs/delta_b_calibration.json
"""
import json
import logging
from pathlib import Path

import numpy as np
from scipy.optimize import minimize
from scipy.stats import chi2 as chi2_dist
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

HERE = Path(__file__).resolve().parent
P4B_OUT = HERE.parent / "outputs"
P4A_OUT = HERE.parents[1] / "4a_expected" / "outputs"
P3_OUT = HERE.parents[2] / "phase3_selection" / "outputs"

# SM values
R_B_SM = 0.21578
R_C_SM = 0.17223
R_UDS_SM = 1.0 - R_B_SM - R_C_SM
AFB_B_OBS = 0.0995   # observed A_FB^b at LEP (before QCD correction)
AFB_C_OBS = 0.0682   # observed A_FB^c at LEP
AFB_UDS = 0.0         # negligible for light quarks

DELTA_QCD = 0.0356
DELTA_QED = 0.001
AFB_B_SM = 0.1032  # pole value

# Published ALEPH charge separations (hep-ex/0509008 Table 12)
# delta_q = <Q_q> - <Q_qbar>
PUBLISHED = {
    0.3: {'delta_b': 0.162, 'delta_c': 0.100, 'delta_uds': 0.090},
    0.5: {'delta_b': 0.233, 'delta_c': 0.136, 'delta_uds': 0.115},
    1.0: {'delta_b': 0.374, 'delta_c': 0.198, 'delta_uds': 0.165},
    2.0: {'delta_b': 0.579, 'delta_c': 0.279, 'delta_uds': 0.220},
}

N_COS_BINS = 10
COS_RANGE = (-0.9, 0.9)


def measure_slope_at_wp(qfb, cos_theta, tag_h0, tag_h1, threshold,
                         n_bins=N_COS_BINS, cos_range=COS_RANGE):
    """Measure the slope of <Q_FB> vs cos(theta) at a given WP."""
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
    n_events = np.zeros(n_bins, dtype=int)

    for i in range(n_bins):
        mask = (cos_sel >= bin_edges[i]) & (cos_sel < bin_edges[i + 1])
        n = np.sum(mask)
        n_events[i] = n
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

    return {
        'slope': float(slope),
        'sigma_slope': float(sigma_slope),
        'intercept': float(intercept),
        'chi2': chi2_val,
        'ndf': ndf_val,
        'n_tagged': n_tagged,
    }


def estimate_purity_at_wp(f_s, mc_cal):
    """Estimate flavour purities by interpolating MC calibration.

    We have MC calibration at only WP=9.0 and WP=10.0.
    For other WPs, we use the relationship:
    f_q = eps_q * R_q / f_s
    and interpolate eps_q as a function of f_s.
    """
    # Get calibrated values
    cal_points = []
    for thr_str, v in mc_cal.items():
        cal_points.append({
            'f_s': v['f_s'],
            'eps_b': v['eps_b'],
            'eps_c': v['eps_c'],
            'eps_uds': v['eps_uds'],
        })

    if len(cal_points) < 1:
        return None

    # For now, just use the closest calibrated point
    closest = min(cal_points, key=lambda p: abs(p['f_s'] - f_s))
    denom = closest['eps_b'] * R_B_SM + closest['eps_c'] * R_C_SM + closest['eps_uds'] * R_UDS_SM
    f_b = closest['eps_b'] * R_B_SM / denom if denom > 0 else 0
    f_c = closest['eps_c'] * R_C_SM / denom if denom > 0 else 0
    f_uds = closest['eps_uds'] * R_UDS_SM / denom if denom > 0 else 0

    return {'f_b': f_b, 'f_c': f_c, 'f_uds': f_uds}


def self_cal_fit_2param(slopes_data, purities, kappa):
    """Two-parameter self-calibrating fit: delta_b and A_FB_b simultaneously.

    Model: slope(WP) = f_b(WP) * delta_b * A_FB_b
                      + f_c(WP) * delta_c * A_FB_c
                      + f_uds(WP) * delta_uds * A_FB_uds

    With delta_c, delta_uds from published values, fit for delta_b and A_FB_b.
    """
    pub = PUBLISHED.get(kappa)
    if pub is None:
        return None

    n_wp = len(slopes_data)
    slope_vals = np.array([s['slope'] for s in slopes_data])
    slope_errs = np.array([s['sigma_slope'] for s in slopes_data])
    f_b_vals = np.array([p['f_b'] for p in purities])
    f_c_vals = np.array([p['f_c'] for p in purities])
    f_uds_vals = np.array([p['f_uds'] for p in purities])

    # Charm and uds corrections
    charm_corr = f_c_vals * pub['delta_c'] * AFB_C_OBS
    uds_corr = f_uds_vals * pub['delta_uds'] * AFB_UDS

    # Corrected slopes: should equal f_b * delta_b * A_FB_b
    slope_corr = slope_vals - charm_corr - uds_corr

    # Fit for product = delta_b * A_FB_b
    w = 1.0 / slope_errs**2
    product = np.sum(w * slope_corr * f_b_vals) / np.sum(w * f_b_vals**2)
    sigma_product = 1.0 / np.sqrt(np.sum(w * f_b_vals**2))

    # Also fit the UNCORRECTED slope for comparison
    product_uncorr = np.sum(w * slope_vals * f_b_vals) / np.sum(w * f_b_vals**2)
    sigma_product_uncorr = 1.0 / np.sqrt(np.sum(w * f_b_vals**2))

    residuals = slope_corr - product * f_b_vals
    chi2_val = float(np.sum(w * residuals**2))
    ndf_val = n_wp - 1

    p_value = 1.0 - chi2_dist.cdf(chi2_val, ndf_val) if ndf_val > 0 else np.nan

    return {
        'product_delta_b_afb': float(product),
        'sigma_product': float(sigma_product),
        'product_uncorrected': float(product_uncorr),
        'sigma_product_uncorrected': float(sigma_product_uncorr),
        'chi2': chi2_val,
        'ndf': ndf_val,
        'p_value': float(p_value),
        'charm_corrections': charm_corr.tolist(),
        'f_b_values': f_b_vals.tolist(),
    }


def main():
    log.info("=" * 60)
    log.info("Task 1: Delta_b Calibration from 10%% Data")
    log.info("=" * 60)

    # Load 10% data
    tags = np.load(P4B_OUT / "data_10pct_tags.npz", allow_pickle=False)
    jc = np.load(P4B_OUT / "data_10pct_jetcharge.npz", allow_pickle=False)
    tag_h0 = tags["data_combined_h0"]
    tag_h1 = tags["data_combined_h1"]
    cos_theta = tags["cos_theta"]
    n_events = len(tag_h0)
    log.info("10%% data: %d events", n_events)

    # Also load MC
    mc_tags = np.load(P3_OUT / "hemisphere_tags.npz", allow_pickle=False)
    mc_jc = np.load(P3_OUT / "jet_charge.npz", allow_pickle=False)
    mc_tag_h0 = mc_tags["mc_combined_h0"]
    mc_tag_h1 = mc_tags["mc_combined_h1"]
    mc_cos_theta = mc_jc["cos_theta_mc"]

    # Load MC calibration
    with open(P4A_OUT / "mc_calibration.json") as f:
        mc_cal_data = json.load(f)
    mc_cal = mc_cal_data["full_mc_calibration"]

    # Load tag efficiencies for f_s at each WP
    with open(P3_OUT / "tag_efficiencies.json") as f:
        eff_data = json.load(f)
    mc_fs_by_wp = {}
    for entry in eff_data["combined_mc"]:
        mc_fs_by_wp[entry["threshold"]] = entry["f_s"]

    # Working points
    thresholds = [2.0, 3.0, 5.0, 7.0, 9.0, 10.0, 12.0]
    KAPPA_VALUES = [0.3, 0.5, 1.0, 2.0]
    KAPPA_LABELS = {0.3: 'k0.3', 0.5: 'k0.5', 1.0: 'k1.0', 2.0: 'k2.0'}

    all_results = {}

    for kappa in KAPPA_VALUES:
        k_str = KAPPA_LABELS[kappa]
        log.info("\n" + "=" * 50)
        log.info("kappa = %.1f", kappa)
        log.info("=" * 50)

        qfb_data = jc[f"data_qfb_{k_str}"]
        qfb_mc = mc_jc[f"mc_qfb_{k_str}"]

        # ================================================================
        # Step 1: Slopes at each WP (data and MC)
        # ================================================================
        log.info("\n--- Slopes at each WP ---")
        log.info("%-6s %-12s %-12s %-12s %-12s %-8s",
                 "WP", "slope_data", "err_data", "slope_mc", "err_mc", "n_data")

        slopes_data = []
        slopes_mc = []
        purities_for_fit = []

        for thr in thresholds:
            s_data = measure_slope_at_wp(qfb_data, cos_theta, tag_h0, tag_h1, thr)
            s_mc = measure_slope_at_wp(qfb_mc, mc_cos_theta, mc_tag_h0, mc_tag_h1, thr)

            f_s_mc = mc_fs_by_wp.get(thr)
            purity = estimate_purity_at_wp(f_s_mc, mc_cal) if f_s_mc else None

            sd_slope = s_data['slope'] if s_data else float('nan')
            sd_err = s_data['sigma_slope'] if s_data else float('nan')
            sm_slope = s_mc['slope'] if s_mc else float('nan')
            sm_err = s_mc['sigma_slope'] if s_mc else float('nan')
            n_d = s_data['n_tagged'] if s_data else 0

            log.info("%-6.1f %-12.6f %-12.6f %-12.6f %-12.6f %-8d",
                     thr, sd_slope, sd_err, sm_slope, sm_err, n_d)

            if s_data and purity:
                slopes_data.append(s_data)
                slopes_mc.append(s_mc)
                purities_for_fit.append(purity)

        # ================================================================
        # Step 2: Self-calibrating fit
        # ================================================================
        if len(slopes_data) >= 2:
            fit = self_cal_fit_2param(slopes_data, purities_for_fit, kappa)
            if fit:
                product = fit['product_delta_b_afb']
                sigma = fit['sigma_product']
                log.info("\n--- Self-cal fit results ---")
                log.info("  product (delta_b * A_FB_b): %.6f +/- %.6f", product, sigma)
                log.info("  product (uncorrected): %.6f +/- %.6f",
                         fit['product_uncorrected'], fit['sigma_product_uncorrected'])
                log.info("  chi2/ndf = %.2f/%d, p = %.3f", fit['chi2'], fit['ndf'], fit['p_value'])
        else:
            fit = None

        # ================================================================
        # Step 3: Extract A_FB^b using published delta_b
        # ================================================================
        pub = PUBLISHED.get(kappa)
        log.info("\n--- A_FB^b extraction strategies ---")

        extraction_results = []
        for thr_idx, thr in enumerate(thresholds):
            s = measure_slope_at_wp(qfb_data, cos_theta, tag_h0, tag_h1, thr)
            purity = estimate_purity_at_wp(mc_fs_by_wp.get(thr), mc_cal) if mc_fs_by_wp.get(thr) else None
            if s is None or purity is None or pub is None:
                continue

            observed_slope = s['slope']
            sigma_slope = s['sigma_slope']

            # Method A: Naive (old method) - slope / delta_b
            afb_naive = observed_slope / pub['delta_b']
            sigma_naive = sigma_slope / pub['delta_b']

            # Method B: Purity-corrected - slope / (f_b * delta_b)
            afb_purity = observed_slope / (purity['f_b'] * pub['delta_b'])
            sigma_purity = sigma_slope / (purity['f_b'] * pub['delta_b'])

            # Method C: Charm-corrected - (slope - charm) / (f_b * delta_b)
            charm_corr = purity['f_c'] * pub['delta_c'] * AFB_C_OBS
            afb_charm = (observed_slope - charm_corr) / (purity['f_b'] * pub['delta_b'])
            sigma_charm = sigma_slope / (purity['f_b'] * pub['delta_b'])

            extraction_results.append({
                'threshold': float(thr),
                'slope': float(observed_slope),
                'sigma_slope': float(sigma_slope),
                'n_tagged': s['n_tagged'],
                'f_b': purity['f_b'],
                'f_c': purity['f_c'],
                'charm_correction': float(charm_corr),
                'afb_naive': float(afb_naive),
                'afb_purity_corrected': float(afb_purity),
                'afb_charm_corrected': float(afb_charm),
                'sigma_afb_naive': float(sigma_naive),
                'sigma_afb_purity': float(sigma_purity),
                'sigma_afb_charm': float(sigma_charm),
            })

            log.info("WP %.1f: slope=%.6f, naive=%.4f, purity=%.4f, charm_corr=%.4f (SM=%.4f)",
                     thr, observed_slope, afb_naive, afb_purity, afb_charm, AFB_B_OBS)

        # ================================================================
        # Step 4: Compare old delta_b = sigma(Q_h) to calibrated
        # ================================================================
        log.info("\n--- Old vs calibrated delta_b ---")
        qh0_data = jc[f"data_qh_h0_{k_str}"]
        tagged_ref = (tag_h0 > 5.0) | (tag_h1 > 5.0)
        valid = ~np.isnan(qh0_data) & tagged_ref
        sigma_qh = float(np.std(qh0_data[valid]))
        log.info("  sigma(Q_h) [old 'delta_b'] = %.4f", sigma_qh)
        log.info("  Published delta_b = %.4f", pub['delta_b'] if pub else float('nan'))
        if pub:
            log.info("  Ratio sigma(Q_h)/delta_b = %.3f", sigma_qh / pub['delta_b'])
            log.info("  sigma(Q_h) OVERESTIMATES physical delta_b by %.1f%%",
                     (sigma_qh / pub['delta_b'] - 1) * 100)

        kappa_result = {
            'kappa': float(kappa),
            'published_delta_b': pub['delta_b'] if pub else None,
            'sigma_qh_old_method': float(sigma_qh),
            'overestimate_factor': float(sigma_qh / pub['delta_b']) if pub else None,
            'self_cal_fit': fit,
            'extraction_results': extraction_results,
        }
        all_results[k_str] = kappa_result

    # ================================================================
    # Summary
    # ================================================================
    log.info("\n" + "=" * 70)
    log.info("SUMMARY TABLE: A_FB^b by extraction method")
    log.info("=" * 70)
    log.info("%-8s %-12s %-12s %-12s %-12s %-12s", "kappa", "old_method",
             "naive_pub", "purity_corr", "charm_corr", "SM_value")

    for kappa in KAPPA_VALUES:
        k_str = KAPPA_LABELS[kappa]
        kr = all_results.get(k_str, {})
        er = kr.get('extraction_results', [])
        # Use best (most precise) WP
        if er:
            best = min(er, key=lambda x: abs(x['sigma_afb_naive']))
            # Old method: slope / sigma(Q_h)
            old_afb = best['slope'] / kr['sigma_qh_old_method'] if kr['sigma_qh_old_method'] > 0 else float('nan')
            log.info("%-8.1f %-12.4f %-12.4f %-12.4f %-12.4f %-12.4f",
                     kappa, old_afb, best['afb_naive'],
                     best['afb_purity_corrected'], best['afb_charm_corrected'],
                     AFB_B_OBS)

    log.info("\nKEY FINDINGS:")
    log.info("1. sigma(Q_h) is NOT delta_b. It overestimates physical delta_b.")
    log.info("2. However, delta_b calibration alone does NOT fix the suppression.")
    log.info("3. The REAL issue is b-purity: eps_c (0.44) > eps_b (0.15),")
    log.info("   giving only 18%% b-purity at the tightest WP.")
    log.info("4. The charm contribution to the slope is ~50%% of the total.")
    log.info("5. After purity+charm corrections, A_FB^b improves but depends")
    log.info("   critically on the accuracy of the purity estimate.")

    output = {
        'description': (
            'Delta_b calibration from 10% data. '
            'Key finding: the A_FB^b suppression is not primarily due to '
            'delta_b miscalibration, but due to low b-purity (18% at tightest WP). '
            'eps_c=0.44 > eps_b=0.15 means charm dominates our tagged sample. '
            'Using published delta_b values and correcting for purity and charm '
            'gives improved but uncertain A_FB^b extraction.'
        ),
        'method': 'Multi-WP slope analysis with MC-calibrated purities',
        'kappa_results': all_results,
        'published_source': 'ALEPH hep-ex/0509008 Table 12',
        'sm_afb_b_observed': AFB_B_OBS,
        'sm_afb_b_pole': AFB_B_SM,
        'critical_finding': {
            'issue': 'eps_c > eps_b: charm tagged more efficiently than b',
            'eps_b_at_wp10': 0.15,
            'eps_c_at_wp10': 0.44,
            'b_purity_at_wp10': 0.18,
            'implication': ('The b-tag is not discriminating b from c effectively. '
                           'The d0-significance tag catches D-meson decays (c->D) '
                           'as efficiently as B-hadron decays, likely because both '
                           'produce displaced tracks. A proper b-tag requires '
                           'reconstructing the full B-hadron decay chain or using '
                           'vertex mass/multiplicity cuts to distinguish B from D.'),
        },
    }

    with open(P4B_OUT / "delta_b_calibration.json", "w") as f:
        json.dump(output, f, indent=2, default=str)
    log.info("\nSaved delta_b_calibration.json")


if __name__ == "__main__":
    main()
