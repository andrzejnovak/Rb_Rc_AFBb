"""Phase 4c: Per-year R_b and A_FB^b extraction using BDT tagger.

Re-runs the per-year consistency check with the BDT tagger instead of
the cut-based combined tag. The BDT is trained on the full MC (same as
the primary result) and applied to each year's data independently.

Session: magnus_435d

Reads:
  phase3_selection/outputs/preselected_mc.npz
  phase3_selection/outputs/preselected_data.npz
  phase3_selection/outputs/hemisphere_tags.npz
  phase3_selection/outputs/signed_d0.npz
  phase3_selection/outputs/d0_significance.npz
  phase3_selection/outputs/jet_charge.npz
  phase4_inference/4c_observed/outputs/sv_tags.npz
  phase4_inference/4a_expected/outputs/mc_calibration.json
Writes:
  phase4_inference/4c_observed/outputs/per_year_bdt_results.json
  analysis_note/figures/per_year_bdt_consistency.pdf
"""
import json
import logging
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.stats import chi2 as chi2_dist
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mplhep as hep
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

HERE = Path(__file__).resolve().parent
P3_OUT = HERE.parents[2] / "phase3_selection" / "outputs"
P4A_OUT = HERE.parents[1] / "4a_expected" / "outputs"
PHASE4C_OUT = HERE.parent / "outputs"
AN_FIG = HERE.parents[2] / "analysis_note" / "figures"
PHASE4C_OUT.mkdir(parents=True, exist_ok=True)
AN_FIG.mkdir(parents=True, exist_ok=True)

# Import 3-tag functions
sys.path.insert(0, str(HERE.parents[1] / "4a_expected" / "src"))
from three_tag_rb_extraction import (
    count_three_tag, calibrate_three_tag_efficiencies,
    extract_rb_three_tag, toy_uncertainty_three_tag,
    R_B_SM, R_C_SM,
)
from purity_corrected_afb import (
    measure_qfb_slope, PUBLISHED_DELTA,
)

# Also import the BDT feature builder
sys.path.insert(0, str(HERE))
from bdt_sv_optimization import build_all_features, make_proxy_labels

hep.style.use("ATLAS")
plt.rcParams.update({
    "font.size": 16,
    "axes.labelsize": 18,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "legend.fontsize": 13,
})

N_TOYS = 500
TOY_SEED = 99999

# Published delta_b values
DELTA_B = {0.3: 0.162}


def train_bdt_on_mc(mc, signed_d0, hem_tags, sv_tags, jet_charge, d0_sig):
    """Train the BDT on the full MC sample. Returns model and feature names."""
    import xgboost as xgb

    n_mc = len(hem_tags["mc_nlp_h0"])
    log.info("Training BDT on %d MC events...", n_mc)

    mc_h0, mc_h1, feat_names = build_all_features(
        mc, signed_d0["mc_signed_sig"], hem_tags, sv_tags,
        jet_charge, d0_sig, "mc", n_mc)

    label_h0, label_h1 = make_proxy_labels(hem_tags, "mc", n_mc)

    X_all = np.vstack([mc_h0, mc_h1])
    y_all = np.concatenate([label_h0, label_h1])
    X_all = np.nan_to_num(X_all, nan=0.0, posinf=100.0, neginf=-100.0)

    rng = np.random.RandomState(42)
    idx = rng.permutation(len(y_all))
    n_train = len(y_all) // 2
    X_train, y_train = X_all[idx[:n_train]], y_all[idx[:n_train]]

    dtrain = xgb.DMatrix(X_train, label=y_train, feature_names=feat_names)
    params = {
        "objective": "binary:logistic",
        "eval_metric": "auc",
        "max_depth": 4,
        "learning_rate": 0.05,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "min_child_weight": 100,
        "seed": 42,
        "verbosity": 0,
    }
    bdt = xgb.train(params, dtrain, num_boost_round=300, verbose_eval=False)
    log.info("BDT training complete.")
    return bdt, feat_names


def score_data_hemispheres(bdt, feat_names, data, signed_d0, hem_tags,
                           sv_tags, jet_charge, d0_sig):
    """Score data hemispheres with the BDT. Returns (score_h0, score_h1)."""
    import xgboost as xgb

    n_data = len(hem_tags["data_nlp_h0"])
    data_h0, data_h1, _ = build_all_features(
        data, signed_d0["data_signed_sig"], hem_tags, sv_tags,
        jet_charge, d0_sig, "data", n_data)

    data_h0 = np.nan_to_num(data_h0, nan=0.0, posinf=100.0, neginf=-100.0)
    data_h1 = np.nan_to_num(data_h1, nan=0.0, posinf=100.0, neginf=-100.0)

    d_h0 = xgb.DMatrix(data_h0, feature_names=feat_names)
    d_h1 = xgb.DMatrix(data_h1, feature_names=feat_names)

    return bdt.predict(d_h0), bdt.predict(d_h1)


def score_mc_hemispheres(bdt, feat_names, mc, signed_d0, hem_tags,
                         sv_tags, jet_charge, d0_sig):
    """Score MC hemispheres with the BDT. Returns (score_h0, score_h1)."""
    import xgboost as xgb

    n_mc = len(hem_tags["mc_nlp_h0"])
    mc_h0, mc_h1, _ = build_all_features(
        mc, signed_d0["mc_signed_sig"], hem_tags, sv_tags,
        jet_charge, d0_sig, "mc", n_mc)

    mc_h0 = np.nan_to_num(mc_h0, nan=0.0, posinf=100.0, neginf=-100.0)
    mc_h1 = np.nan_to_num(mc_h1, nan=0.0, posinf=100.0, neginf=-100.0)

    d_h0 = xgb.DMatrix(mc_h0, feature_names=feat_names)
    d_h1 = xgb.DMatrix(mc_h1, feature_names=feat_names)

    return bdt.predict(d_h0), bdt.predict(d_h1)


def extract_rb_bdt_3tag(data_h0, data_h1, mc_h0, mc_h1,
                        thr_tight, thr_loose, C_b=1.0):
    """Extract R_b using BDT scores with the 3-tag SF method."""
    counts_data = count_three_tag(data_h0, data_h1, thr_tight, thr_loose)
    counts_mc = count_three_tag(mc_h0, mc_h1, thr_tight, thr_loose)
    cal_mc = calibrate_three_tag_efficiencies(counts_mc, R_B_SM, R_C_SM)

    sf_tight = counts_data["f_s_tight"] / max(counts_mc["f_s_tight"], 1e-10)
    sf_loose = counts_data["f_s_loose"] / max(counts_mc["f_s_loose"], 1e-10)

    cal_sf = dict(cal_mc)
    cal_sf["eps_b_tight"] = min(cal_mc["eps_b_tight"] * sf_tight, 0.999)
    cal_sf["eps_b_loose"] = min(cal_mc["eps_b_loose"] * sf_loose, 0.999)
    cal_sf["eps_b_anti"] = max(1.0 - cal_sf["eps_b_tight"] - cal_sf["eps_b_loose"], 0.001)
    cal_sf["eps_c_tight"] = min(cal_mc["eps_c_tight"] * sf_tight, 0.999)
    cal_sf["eps_c_loose"] = min(cal_mc["eps_c_loose"] * sf_loose, 0.999)
    cal_sf["eps_c_anti"] = max(1.0 - cal_sf["eps_c_tight"] - cal_sf["eps_c_loose"], 0.001)
    cal_sf["eps_uds_tight"] = min(cal_mc["eps_uds_tight"] * sf_tight, 0.999)
    cal_sf["eps_uds_loose"] = min(cal_mc["eps_uds_loose"] * sf_loose, 0.999)
    cal_sf["eps_uds_anti"] = max(1.0 - cal_sf["eps_uds_tight"] - cal_sf["eps_uds_loose"], 0.001)

    ext = extract_rb_three_tag(counts_data, cal_sf, R_C_SM, C_b_tight=C_b)
    return ext, cal_sf, sf_tight, sf_loose


def extract_afb_signed_thrust(qfb_data, cos_theta, score_h0, score_h1,
                              thr_tag, kappa=0.3):
    """Extract A_FB^b using signed thrust axis method on BDT-tagged events.

    Uses the |cos(theta)| method (same as primary extraction):
    the mean signed Q_FB in bins of |cos(theta)| gives the asymmetry slope.

    Tags events where max(score_h0, score_h1) > thr_tag.
    Uses kappa=0.3 by default.
    """
    max_score = np.maximum(score_h0, score_h1)
    tagged = max_score > thr_tag
    n_tagged = int(np.sum(tagged))

    if n_tagged < 100:
        log.warning("Too few tagged events (%d) at threshold %.2f", n_tagged, thr_tag)
        return None

    cos_tagged = cos_theta[tagged]
    qfb_tagged = qfb_data[tagged]
    abs_cos = np.abs(cos_tagged)

    n_bins = 10
    cos_edges = np.linspace(0, 0.9, n_bins + 1)
    centers = 0.5 * (cos_edges[:-1] + cos_edges[1:])

    # Compute per-bin asymmetry: <Q_FB> / delta_b
    # Using the signed Q_FB in |cos| bins
    mean_qfb = np.zeros(n_bins)
    sigma_qfb = np.zeros(n_bins)
    n_per_bin = np.zeros(n_bins)

    for i in range(n_bins):
        mask = (abs_cos >= cos_edges[i]) & (abs_cos < cos_edges[i + 1])
        n_per_bin[i] = np.sum(mask)
        if n_per_bin[i] > 10:
            bin_qfb = qfb_tagged[mask]
            finite = np.isfinite(bin_qfb)
            n_finite = np.sum(finite)
            if n_finite > 10:
                mean_qfb[i] = np.nanmean(bin_qfb)
                sigma_qfb[i] = np.nanstd(bin_qfb) / np.sqrt(n_finite)

    valid = sigma_qfb > 0
    if np.sum(valid) < 3:
        log.warning("AFB: only %d valid bins, returning None", int(np.sum(valid)))
        return None

    # Linear fit: mean_qfb = a + b * |cos_theta|
    x = centers[valid]
    y = mean_qfb[valid]
    w = 1.0 / sigma_qfb[valid]**2

    S = np.sum(w)
    Sx = np.sum(w * x)
    Sy = np.sum(w * y)
    Sxx = np.sum(w * x**2)
    Sxy = np.sum(w * x * y)

    det = S * Sxx - Sx**2
    intercept = (Sxx * Sy - Sx * Sxy) / det
    slope = (S * Sxy - Sx * Sy) / det
    sigma_slope = np.sqrt(S / det)

    residuals = y - (intercept + slope * x)
    chi2_val = float(np.sum((residuals / sigma_qfb[valid])**2))
    ndf = len(x) - 2
    p_val = float(1.0 - chi2_dist.cdf(chi2_val, ndf)) if ndf > 0 else 0.0

    delta_b = DELTA_B.get(kappa, 0.162)
    afb = slope / delta_b
    sigma_afb = sigma_slope / delta_b

    return {
        "slope": float(slope),
        "sigma_slope": float(sigma_slope),
        "intercept": float(intercept),
        "chi2": chi2_val,
        "ndf": ndf,
        "p_value": p_val,
        "n_tagged": n_tagged,
        "afb": float(afb),
        "sigma_afb": float(sigma_afb),
    }


def main():
    log.info("=" * 60)
    log.info("Per-Year BDT Extraction (magnus_435d)")
    log.info("=" * 60)

    # Load all data
    log.info("Loading data...")
    data_npz = np.load(P3_OUT / "preselected_data.npz", allow_pickle=False)
    mc_npz = np.load(P3_OUT / "preselected_mc.npz", allow_pickle=False)
    year = data_npz["year"]

    hem_tags = np.load(P3_OUT / "hemisphere_tags.npz", allow_pickle=False)
    sv_tags = np.load(PHASE4C_OUT / "sv_tags.npz", allow_pickle=False)
    jet_charge = np.load(P3_OUT / "jet_charge.npz", allow_pickle=False)
    signed_d0 = np.load(P3_OUT / "signed_d0.npz", allow_pickle=False)
    d0_sig = np.load(P3_OUT / "d0_significance.npz", allow_pickle=False)

    cos_theta_data = jet_charge["cos_theta_data"]
    qfb_k03 = jet_charge["data_qfb_k0.3"]

    # Train BDT on full MC
    bdt, feat_names = train_bdt_on_mc(
        mc_npz, signed_d0, hem_tags, sv_tags, jet_charge, d0_sig)

    # Score all data
    log.info("Scoring data hemispheres...")
    score_data_h0, score_data_h1 = score_data_hemispheres(
        bdt, feat_names, data_npz, signed_d0, hem_tags,
        sv_tags, jet_charge, d0_sig)

    # Score MC
    log.info("Scoring MC hemispheres...")
    score_mc_h0, score_mc_h1 = score_mc_hemispheres(
        bdt, feat_names, mc_npz, signed_d0, hem_tags,
        sv_tags, jet_charge, d0_sig)

    # BDT working point
    thr_tight = 0.80
    thr_loose = 0.50

    # Full-data BDT R_b for reference
    ext_full, _, _, _ = extract_rb_bdt_3tag(
        score_data_h0, score_data_h1, score_mc_h0, score_mc_h1,
        thr_tight, thr_loose, C_b=1.0)
    log.info("Full-data BDT R_b = %.4f", ext_full["R_b"])

    # Per-year extraction
    years = sorted(set(year))
    per_year_results = []

    for yr in years:
        yr_mask = year == yr
        n_yr = int(np.sum(yr_mask))
        log.info("\n--- Year %d: %d events ---", yr, n_yr)

        h0_yr = score_data_h0[yr_mask]
        h1_yr = score_data_h1[yr_mask]

        # R_b
        ext_yr, cal_yr, sf_t, sf_l = extract_rb_bdt_3tag(
            h0_yr, h1_yr, score_mc_h0, score_mc_h1,
            thr_tight, thr_loose, C_b=1.0)

        # Toy uncertainty
        rb_mean, rb_sigma, _, n_valid = toy_uncertainty_three_tag(
            h0_yr, h1_yr, thr_tight, thr_loose,
            cal_yr, R_C_SM, n_toys=N_TOYS, seed=TOY_SEED + yr)

        log.info("R_b(BDT SF) = %.5f +/- %.5f", ext_yr["R_b"],
                 rb_sigma if not np.isnan(rb_sigma) else 0)

        # A_FB^b using signed thrust axis (use loose threshold for larger sample)
        cos_yr = cos_theta_data[yr_mask]
        qfb_yr = qfb_k03[yr_mask]
        afb_result = extract_afb_signed_thrust(
            qfb_yr, cos_yr, h0_yr, h1_yr, thr_tag=thr_loose, kappa=0.3)

        if afb_result is not None:
            log.info("A_FB^b(k=0.3) = %.4f +/- %.4f",
                     afb_result["afb"], afb_result["sigma_afb"])

        per_year_results.append({
            "year": int(yr),
            "n_events": n_yr,
            "R_b_bdt_sf": ext_yr["R_b"],
            "sigma_stat_rb": float(rb_sigma) if not np.isnan(rb_sigma) else None,
            "chi2_rb": ext_yr["chi2"],
            "ndf_rb": ext_yr["ndf"],
            "sf_tight": float(sf_t),
            "sf_loose": float(sf_l),
            "A_FB_b": float(afb_result["afb"]) if afb_result else None,
            "sigma_stat_afb": float(afb_result["sigma_afb"]) if afb_result else None,
            "afb_chi2_ndf": f"{afb_result['chi2']:.1f}/{afb_result['ndf']}" if afb_result else None,
        })

    # Consistency chi2
    valid_rb = [r for r in per_year_results
                if r["sigma_stat_rb"] is not None and r["sigma_stat_rb"] > 0
                and 0.05 < r["R_b_bdt_sf"] < 0.50]

    if len(valid_rb) >= 2:
        rb_vals = np.array([r["R_b_bdt_sf"] for r in valid_rb])
        rb_errs = np.array([r["sigma_stat_rb"] for r in valid_rb])
        w = 1.0 / rb_errs**2
        rb_avg = np.sum(w * rb_vals) / np.sum(w)
        chi2_yr = float(np.sum((rb_vals - rb_avg)**2 / rb_errs**2))
        ndf_yr = len(valid_rb) - 1
        p_yr = float(1.0 - chi2_dist.cdf(chi2_yr, ndf_yr))
        log.info("\nR_b per-year chi2/ndf = %.2f/%d, p = %.4f",
                 chi2_yr, ndf_yr, p_yr)
    else:
        chi2_yr, ndf_yr, p_yr = 0.0, 0, 1.0

    valid_afb = [r for r in per_year_results
                 if r["A_FB_b"] is not None and r["sigma_stat_afb"] is not None
                 and r["sigma_stat_afb"] > 0]

    if len(valid_afb) >= 2:
        afb_vals = np.array([r["A_FB_b"] for r in valid_afb])
        afb_errs = np.array([r["sigma_stat_afb"] for r in valid_afb])
        w = 1.0 / afb_errs**2
        afb_avg = np.sum(w * afb_vals) / np.sum(w)
        chi2_afb = float(np.sum((afb_vals - afb_avg)**2 / afb_errs**2))
        ndf_afb = len(valid_afb) - 1
        p_afb = float(1.0 - chi2_dist.cdf(chi2_afb, ndf_afb))
        log.info("AFB per-year chi2/ndf = %.2f/%d, p = %.4f",
                 chi2_afb, ndf_afb, p_afb)
    else:
        chi2_afb, ndf_afb, p_afb = 0.0, 0, 1.0

    output = {
        "description": "Per-year R_b and A_FB^b extraction using BDT tagger (magnus_435d)",
        "bdt_working_point": {"thr_tight": thr_tight, "thr_loose": thr_loose},
        "full_data_rb": ext_full["R_b"],
        "per_year": per_year_results,
        "consistency_rb": {
            "chi2": chi2_yr, "ndf": ndf_yr, "p_value": p_yr,
            "passes": p_yr > 0.01,
        },
        "consistency_afb": {
            "chi2": chi2_afb, "ndf": ndf_afb, "p_value": p_afb,
            "passes": p_afb > 0.01,
        },
    }

    out_path = PHASE4C_OUT / "per_year_bdt_results.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    log.info("Saved %s", out_path)

    # --- Plot ---
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10),
                                    gridspec_kw={"hspace": 0.3})

    years_plot = [r["year"] for r in per_year_results]
    rb_vals_plot = [r["R_b_bdt_sf"] for r in per_year_results]
    rb_errs_plot = [r["sigma_stat_rb"] if r["sigma_stat_rb"] else 0
                    for r in per_year_results]

    ax1.errorbar(years_plot, rb_vals_plot, yerr=rb_errs_plot,
                 fmt="ko", ms=8, capsize=5, label="Per-year (BDT)")
    # Combined band
    if len(valid_rb) >= 2:
        ax1.axhline(rb_avg, color="blue", ls="-", lw=1.5, label=f"Combined: {rb_avg:.4f}")
        sigma_avg = 1.0 / np.sqrt(np.sum(1.0 / np.array(rb_errs_plot)**2))
        ax1.axhspan(rb_avg - sigma_avg, rb_avg + sigma_avg,
                     alpha=0.2, color="blue")
    ax1.axhline(0.21578, color="red", ls="--", lw=1, label="SM $R_b^{\\mathrm{SM}}$")
    ax1.set_ylabel("$R_b$")
    ax1.set_xlabel("Year")
    ax1.legend(fontsize=11)
    ax1.text(0.05, 0.95,
             f"$\\chi^2$/ndf = {chi2_yr:.1f}/{ndf_yr} ($p$ = {p_yr:.2f})",
             transform=ax1.transAxes, va="top", fontsize=12)
    hep.label.exp_text("ALEPH", ax=ax1, loc=1)

    afb_vals_plot = [r["A_FB_b"] if r["A_FB_b"] else 0
                     for r in per_year_results]
    afb_errs_plot = [r["sigma_stat_afb"] if r["sigma_stat_afb"] else 0
                     for r in per_year_results]

    ax2.errorbar(years_plot, afb_vals_plot, yerr=afb_errs_plot,
                 fmt="ko", ms=8, capsize=5, label="Per-year (BDT, $\\kappa=0.3$)")
    if len(valid_afb) >= 2:
        ax2.axhline(afb_avg, color="blue", ls="-", lw=1.5,
                     label=f"Combined: {afb_avg:.3f}")
        sigma_afb_avg = 1.0 / np.sqrt(np.sum(1.0 / np.array(
            [r["sigma_stat_afb"] for r in valid_afb])**2))
        ax2.axhspan(afb_avg - sigma_afb_avg, afb_avg + sigma_afb_avg,
                     alpha=0.2, color="blue")
    ax2.axhline(0.0927, color="red", ls="--", lw=1, label="ALEPH published")
    ax2.set_ylabel("$A_{\\mathrm{FB}}^b$")
    ax2.set_xlabel("Year")
    ax2.legend(fontsize=11)
    ax2.text(0.05, 0.95,
             f"$\\chi^2$/ndf = {chi2_afb:.1f}/{ndf_afb} ($p$ = {p_afb:.2f})",
             transform=ax2.transAxes, va="top", fontsize=12)
    hep.label.exp_text("ALEPH", ax=ax2, loc=1)

    fig.savefig(AN_FIG / "per_year_bdt_consistency.pdf",
                bbox_inches="tight")
    fig.savefig(AN_FIG / "per_year_bdt_consistency.png",
                dpi=150, bbox_inches="tight")
    plt.close(fig)
    log.info("Saved per_year_bdt_consistency.pdf")


if __name__ == "__main__":
    main()
