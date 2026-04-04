"""Phase 4c: Full BDT optimization with all available features.

Session: kenji_3a32

Trains XGBoost BDT combining d0 significance, hemisphere probability,
hemisphere mass, SV features, track multiplicity, jet charge — everything
available per-hemisphere. Uses mass-cut proxy labels for training on MC.

Tasks:
  1. BDT on ALL available features (train on MC, apply to data)
  2. BDT-based R_b extraction via 3-tag counting
  3. BDT-based A_FB^b via purity-corrected jet charge
  4. Combined mass+BDT tag, mass threshold scan, other improvements
  5. Summary of best achievable results

Reads:
  phase3_selection/outputs/preselected_mc.npz
  phase3_selection/outputs/preselected_data.npz
  phase3_selection/outputs/hemisphere_tags.npz
  phase3_selection/outputs/signed_d0.npz
  phase3_selection/outputs/d0_significance.npz
  phase3_selection/outputs/jet_charge.npz
  phase4_inference/4c_observed/outputs/sv_tags.npz
Writes:
  phase4_inference/4c_observed/outputs/bdt_optimization_results.json
  phase4_inference/4c_observed/outputs/figures/bdt_*.png
"""
import json
import logging
import sys
import time
from pathlib import Path

import numpy as np
from scipy.optimize import minimize
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
FIG_DIR = PHASE4C_OUT / "figures"
PHASE4C_OUT.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Import 3-tag functions
sys.path.insert(0, str(HERE.parents[1] / "4a_expected" / "src"))
from three_tag_rb_extraction import (
    count_three_tag, calibrate_three_tag_efficiencies,
    extract_rb_three_tag, toy_uncertainty_three_tag,
    R_B_SM, R_C_SM, R_UDS_SM,
)
from purity_corrected_afb import (
    estimate_purity_at_wp, measure_qfb_slope,
    PUBLISHED_DELTA, SIN2_THETA_SM, AFB_B_OBS, AFB_B_SM_POLE,
    DELTA_QCD, DELTA_QCD_ERR, DELTA_QED,
    N_COS_BINS, COS_RANGE,
)

hep.style.use("ATLAS")
plt.rcParams.update({
    "font.size": 16,
    "axes.labelsize": 18,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "legend.fontsize": 13,
})

N_TOYS = 500
TOY_SEED = 42424


# ============================================================
# FEATURE BUILDING
# ============================================================
def build_all_features(npz_data, signed_d0_arr, hem_tags, sv_tags,
                       jet_charge, d0_sig, prefix, n_events):
    """Build comprehensive per-hemisphere feature matrix.

    Returns (features_h0, features_h1, feature_names).
    """
    offsets = npz_data["trk_d0_offsets"]
    hem = npz_data["trk_hem"]
    pmag = npz_data["trk_pmag"]
    theta = npz_data["trk_theta"]
    phi = npz_data["trk_phi"]
    charge = npz_data["trk_charge"]
    nvdet = npz_data["trk_nvdet"]
    pt = npz_data["trk_pt"]

    sig = signed_d0_arr
    PION_MASS = 0.13957

    event_idx = np.repeat(np.arange(n_events), np.diff(offsets))
    hem_evt = 2 * event_idx + hem.astype(np.int64)

    # --- d0 significance features ---
    max_sig = np.full(2 * n_events, -999.0)
    np.maximum.at(max_sig, hem_evt, sig)
    max_sig[max_sig < -900] = 0

    pos_mask = sig > 0
    sum_pos_sig = np.zeros(2 * n_events)
    n_pos = np.zeros(2 * n_events, dtype=np.int64)
    np.add.at(sum_pos_sig, hem_evt[pos_mask], sig[pos_mask])
    np.add.at(n_pos, hem_evt[pos_mask], 1)
    mean_pos_sig = np.where(n_pos > 0, sum_pos_sig / n_pos, 0)

    # Counts of displaced tracks
    above2 = sig > 2.0
    above3 = sig > 3.0
    above5 = sig > 5.0
    n_above2 = np.zeros(2 * n_events, dtype=np.int64)
    n_above3 = np.zeros(2 * n_events, dtype=np.int64)
    n_above5 = np.zeros(2 * n_events, dtype=np.int64)
    np.add.at(n_above2, hem_evt[above2], 1)
    np.add.at(n_above3, hem_evt[above3], 1)
    np.add.at(n_above5, hem_evt[above5], 1)

    # Sum of positive d0 significances
    sum_pos = np.zeros(2 * n_events)
    np.add.at(sum_pos, hem_evt[pos_mask], sig[pos_mask])

    # --- Hemisphere mass (displaced tracks) ---
    E = np.sqrt(pmag**2 + PION_MASS**2)
    px_trk = pmag * np.sin(theta) * np.cos(phi)
    py_trk = pmag * np.sin(theta) * np.sin(phi)
    pz_trk = pmag * np.cos(theta)

    disp_mask = sig > 2.0
    sum_E = np.zeros(2 * n_events)
    sum_px = np.zeros(2 * n_events)
    sum_py = np.zeros(2 * n_events)
    sum_pz = np.zeros(2 * n_events)
    n_disp = np.zeros(2 * n_events, dtype=np.int64)
    disp_idx = hem_evt[disp_mask]
    np.add.at(sum_E, disp_idx, E[disp_mask])
    np.add.at(sum_px, disp_idx, px_trk[disp_mask])
    np.add.at(sum_py, disp_idx, py_trk[disp_mask])
    np.add.at(sum_pz, disp_idx, pz_trk[disp_mask])
    np.add.at(n_disp, disp_idx, 1)

    m2 = sum_E**2 - sum_px**2 - sum_py**2 - sum_pz**2
    hem_mass = np.sqrt(np.maximum(m2, 0))
    hem_mass[n_disp < 2] = 0.0

    # --- Total hemisphere momentum ---
    p_hem = np.zeros(2 * n_events)
    np.add.at(p_hem, hem_evt, pmag)

    # --- Track multiplicity ---
    ntrk = np.zeros(2 * n_events, dtype=np.int64)
    np.add.at(ntrk, hem_evt, 1)

    # --- Hemisphere probability (-ln P) ---
    nlp_h0 = hem_tags[f"{prefix}_nlp_h0"]
    nlp_h1 = hem_tags[f"{prefix}_nlp_h1"]

    # --- Combined tag ---
    combined_h0 = hem_tags[f"{prefix}_combined_h0"]
    combined_h1 = hem_tags[f"{prefix}_combined_h1"]

    # --- SV features ---
    sv_mass_h0 = sv_tags[f"{prefix}_sv_mass_h0"]
    sv_mass_h1 = sv_tags[f"{prefix}_sv_mass_h1"]
    sv_ntrk_h0 = sv_tags[f"{prefix}_sv_ntrk_h0"]
    sv_ntrk_h1 = sv_tags[f"{prefix}_sv_ntrk_h1"]
    sv_flight_h0 = sv_tags[f"{prefix}_sv_flight_h0"]
    sv_flight_h1 = sv_tags[f"{prefix}_sv_flight_h1"]
    sv_flight_sig_h0 = sv_tags[f"{prefix}_sv_flight_sig_h0"]
    sv_flight_sig_h1 = sv_tags[f"{prefix}_sv_flight_sig_h1"]
    sv_pt_h0 = sv_tags[f"{prefix}_sv_pt_h0"]
    sv_pt_h1 = sv_tags[f"{prefix}_sv_pt_h1"]
    sv_disc_h0 = sv_tags[f"{prefix}_sv_disc_h0"]
    sv_disc_h1 = sv_tags[f"{prefix}_sv_disc_h1"]

    # --- Jet charge (kappa=2.0) ---
    jc_h0 = jet_charge[f"{prefix}_qh_h0_k2.0"]
    jc_h1 = jet_charge[f"{prefix}_qh_h1_k2.0"]

    # --- Hemisphere mass from hem_tags (all tracks, broader) ---
    mass_h0 = hem_tags[f"{prefix}_mass_h0"]
    mass_h1 = hem_tags[f"{prefix}_mass_h1"]

    # --- nsig3 from tags ---
    nsig3_h0 = hem_tags[f"{prefix}_nsig3_h0"]
    nsig3_h1 = hem_tags[f"{prefix}_nsig3_h1"]

    # Assemble features for h0 and h1
    # NOTE: Exclude combined_tag and hem_mass_all from BDT features because
    # they directly encode the proxy label (mass > 1.8 AND combined > 5).
    # Including them gives AUC=1.0 trivially. We want the BDT to learn
    # from the underlying track/vertex observables.
    # We DO include nlp (-ln P) since it's a non-trivial probability tag
    # that is only partially correlated with the label.
    feature_names = [
        "max_d0_sig",           # 0
        "mean_pos_d0_sig",      # 1
        "sum_pos_d0_sig",       # 2
        "n_above2",             # 3
        "n_above3",             # 4
        "n_above5",             # 5
        "hem_mass_disp",        # 6 (mass of displaced tracks)
        "nlp",                  # 7 (-ln P hemisphere probability)
        "sv_mass",              # 8
        "sv_ntrk",              # 9
        "sv_flight",            # 10
        "sv_flight_sig",        # 11
        "sv_pt",                # 12
        "sv_disc",              # 13 (SV discriminant)
        "jet_charge_k2",        # 14
        "total_p",              # 15
        "ntrk",                 # 16
        "n_disp_trk",           # 17
        "n_pos_sig",            # 18
        "nsig3",                # 19
    ]

    features_h0 = np.column_stack([
        max_sig[0::2], mean_pos_sig[0::2], sum_pos[0::2],
        n_above2[0::2], n_above3[0::2], n_above5[0::2],
        hem_mass[0::2],
        nlp_h0,
        sv_mass_h0, sv_ntrk_h0, sv_flight_h0, sv_flight_sig_h0, sv_pt_h0, sv_disc_h0,
        np.abs(jc_h0),  # |Q_jet| — absolute value since sign has no b/non-b info
        p_hem[0::2], ntrk[0::2], n_disp[0::2], n_pos[0::2],
        nsig3_h0,
    ])

    features_h1 = np.column_stack([
        max_sig[1::2], mean_pos_sig[1::2], sum_pos[1::2],
        n_above2[1::2], n_above3[1::2], n_above5[1::2],
        hem_mass[1::2],
        nlp_h1,
        sv_mass_h1, sv_ntrk_h1, sv_flight_h1, sv_flight_sig_h1, sv_pt_h1, sv_disc_h1,
        np.abs(jc_h1),
        p_hem[1::2], ntrk[1::2], n_disp[1::2], n_pos[1::2],
        nsig3_h1,
    ])

    return features_h0, features_h1, feature_names


def make_proxy_labels(hem_tags, prefix, n_events):
    """Mass-cut proxy label: hemisphere mass > 1.8 GeV AND max d0 sig > 5.

    This is our best b-enrichment tag. Use combined_h for d0 info.
    """
    mass_h0 = hem_tags[f"{prefix}_mass_h0"]
    mass_h1 = hem_tags[f"{prefix}_mass_h1"]
    combined_h0 = hem_tags[f"{prefix}_combined_h0"]
    combined_h1 = hem_tags[f"{prefix}_combined_h1"]

    # Mass > 1.8 AND combined > 5 (conservative b-enrichment)
    label_h0 = ((mass_h0 > 1.8) & (combined_h0 > 5.0)).astype(np.float32)
    label_h1 = ((mass_h1 > 1.8) & (combined_h1 > 5.0)).astype(np.float32)
    return label_h0, label_h1


# ============================================================
# TASK 1: TRAIN BDT ON ALL FEATURES
# ============================================================
def task1_train_bdt(mc, data, signed_d0, hem_tags, sv_tags, jet_charge, d0_sig):
    """Train XGBoost BDT on MC with all features."""
    log.info("=" * 70)
    log.info("TASK 1: Train XGBoost BDT on ALL available features")
    log.info("=" * 70)

    import xgboost as xgb
    from sklearn.metrics import roc_auc_score, roc_curve

    n_mc = len(hem_tags["mc_nlp_h0"])
    n_data = len(hem_tags["data_nlp_h0"])

    log.info("Building MC features (%d events)...", n_mc)
    mc_h0, mc_h1, feat_names = build_all_features(
        mc, signed_d0["mc_signed_sig"], hem_tags, sv_tags,
        jet_charge, d0_sig, "mc", n_mc)

    log.info("Building Data features (%d events)...", n_data)
    data_h0, data_h1, _ = build_all_features(
        data, signed_d0["data_signed_sig"], hem_tags, sv_tags,
        jet_charge, d0_sig, "data", n_data)

    # Proxy labels on MC
    label_h0, label_h1 = make_proxy_labels(hem_tags, "mc", n_mc)

    # Stack both hemispheres for training
    X_all = np.vstack([mc_h0, mc_h1])
    y_all = np.concatenate([label_h0, label_h1])

    log.info("Total training samples: %d (signal frac: %.3f)",
             len(y_all), np.mean(y_all))

    # Replace NaN/inf
    X_all = np.nan_to_num(X_all, nan=0.0, posinf=100.0, neginf=-100.0)

    # 50/50 train/test split
    rng = np.random.RandomState(42)
    idx = rng.permutation(len(y_all))
    n_train = len(y_all) // 2
    train_idx = idx[:n_train]
    test_idx = idx[n_train:]

    X_train, y_train = X_all[train_idx], y_all[train_idx]
    X_test, y_test = X_all[test_idx], y_all[test_idx]

    log.info("Train: %d samples (sig frac %.3f)", len(X_train), np.mean(y_train))
    log.info("Test:  %d samples (sig frac %.3f)", len(X_test), np.mean(y_test))

    # Train XGBoost
    dtrain = xgb.DMatrix(X_train, label=y_train, feature_names=feat_names)
    dtest = xgb.DMatrix(X_test, label=y_test, feature_names=feat_names)

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

    evals_result = {}
    bdt = xgb.train(
        params, dtrain,
        num_boost_round=300,
        evals=[(dtrain, "train"), (dtest, "test")],
        evals_result=evals_result,
        verbose_eval=50,
    )

    # Scores
    score_train = bdt.predict(dtrain)
    score_test = bdt.predict(dtest)

    auc_train = roc_auc_score(y_train, score_train)
    auc_test = roc_auc_score(y_test, score_test)
    log.info("AUC train: %.4f, AUC test: %.4f", auc_train, auc_test)

    # Feature importance
    importance = bdt.get_score(importance_type="gain")
    log.info("Feature importance (gain):")
    sorted_imp = sorted(importance.items(), key=lambda x: x[1], reverse=True)
    for name, gain in sorted_imp:
        log.info("  %s: %.1f", name, gain)

    # Score MC hemispheres separately for R_b extraction
    mc_h0_clean = np.nan_to_num(mc_h0, nan=0.0, posinf=100.0, neginf=-100.0)
    mc_h1_clean = np.nan_to_num(mc_h1, nan=0.0, posinf=100.0, neginf=-100.0)
    data_h0_clean = np.nan_to_num(data_h0, nan=0.0, posinf=100.0, neginf=-100.0)
    data_h1_clean = np.nan_to_num(data_h1, nan=0.0, posinf=100.0, neginf=-100.0)

    d_mc_h0 = xgb.DMatrix(mc_h0_clean, feature_names=feat_names)
    d_mc_h1 = xgb.DMatrix(mc_h1_clean, feature_names=feat_names)
    d_data_h0 = xgb.DMatrix(data_h0_clean, feature_names=feat_names)
    d_data_h1 = xgb.DMatrix(data_h1_clean, feature_names=feat_names)

    score_mc_h0 = bdt.predict(d_mc_h0)
    score_mc_h1 = bdt.predict(d_mc_h1)
    score_data_h0 = bdt.predict(d_data_h0)
    score_data_h1 = bdt.predict(d_data_h1)

    # --- PLOTS ---

    # 1. Overtraining check
    fig, ax = plt.subplots(figsize=(10, 10))
    bins = np.linspace(0, 1, 51)
    ax.hist(score_train[y_train == 0], bins=bins, density=True,
            histtype="stepfilled", alpha=0.3, color="blue", label="Train bkg")
    ax.hist(score_train[y_train == 1], bins=bins, density=True,
            histtype="stepfilled", alpha=0.3, color="red", label="Train sig")
    h_test_bkg, _, _ = ax.hist(score_test[y_test == 0], bins=bins, density=True,
                                histtype="step", lw=2, color="blue", linestyle="--",
                                label="Test bkg")
    h_test_sig, _, _ = ax.hist(score_test[y_test == 1], bins=bins, density=True,
                                histtype="step", lw=2, color="red", linestyle="--",
                                label="Test sig")
    ax.set_xlabel("BDT score")
    ax.set_ylabel("Normalized density")
    ax.legend()
    hep.label.exp_text("ALEPH", ax=ax, loc=1)
    fig.savefig(FIG_DIR / "bdt_overtraining.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    log.info("Saved bdt_overtraining.png")

    # 2. Feature importance
    fig, ax = plt.subplots(figsize=(10, 10))
    names_sorted = [x[0] for x in sorted_imp]
    gains_sorted = [x[1] for x in sorted_imp]
    ax.barh(range(len(names_sorted)), gains_sorted, color="steelblue")
    ax.set_yticks(range(len(names_sorted)))
    ax.set_yticklabels(names_sorted)
    ax.set_xlabel("Gain")
    ax.invert_yaxis()
    hep.label.exp_text("ALEPH", ax=ax, loc=1)
    fig.savefig(FIG_DIR / "bdt_feature_importance.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    log.info("Saved bdt_feature_importance.png")

    # 3. ROC curve
    fpr_train, tpr_train, _ = roc_curve(y_train, score_train)
    fpr_test, tpr_test, _ = roc_curve(y_test, score_test)
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.plot(fpr_train, tpr_train, label=f"Train (AUC={auc_train:.4f})", lw=2)
    ax.plot(fpr_test, tpr_test, label=f"Test (AUC={auc_test:.4f})", lw=2, ls="--")
    ax.plot([0, 1], [0, 1], "k--", lw=1)
    ax.set_xlabel("False positive rate")
    ax.set_ylabel("True positive rate")
    ax.legend()
    hep.label.exp_text("ALEPH", ax=ax, loc=4)
    fig.savefig(FIG_DIR / "bdt_roc.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    log.info("Saved bdt_roc.png")

    # 4. Data/MC agreement on BDT score
    fig, ax = plt.subplots(figsize=(10, 10))
    bins = np.linspace(0, 1, 51)
    mc_all = np.concatenate([score_mc_h0, score_mc_h1])
    data_all = np.concatenate([score_data_h0, score_data_h1])
    # Normalize MC to data integral
    mc_counts, _ = np.histogram(mc_all, bins=bins)
    data_counts, _ = np.histogram(data_all, bins=bins)
    mc_scale = np.sum(data_counts) / max(np.sum(mc_counts), 1)
    centers = 0.5 * (bins[:-1] + bins[1:])
    ax.step(centers, data_counts, where="mid", color="black", lw=2, label="Data")
    ax.step(centers, mc_counts * mc_scale, where="mid", color="red", lw=2, label="MC (scaled)")
    ax.set_xlabel("BDT score")
    ax.set_ylabel("Hemispheres")
    ax.legend()
    ax.set_yscale("log")
    hep.label.exp_text("ALEPH", ax=ax, loc=1)
    fig.savefig(FIG_DIR / "bdt_data_mc_agreement.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    log.info("Saved bdt_data_mc_agreement.png")

    # 5. Training curve
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.plot(evals_result["train"]["auc"], label="Train AUC", lw=2)
    ax.plot(evals_result["test"]["auc"], label="Test AUC", lw=2, ls="--")
    ax.set_xlabel("Boosting round")
    ax.set_ylabel("AUC")
    ax.legend()
    hep.label.exp_text("ALEPH", ax=ax, loc=4)
    fig.savefig(FIG_DIR / "bdt_training_curve.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    log.info("Saved bdt_training_curve.png")

    return {
        "bdt": bdt,
        "feat_names": feat_names,
        "score_mc_h0": score_mc_h0,
        "score_mc_h1": score_mc_h1,
        "score_data_h0": score_data_h0,
        "score_data_h1": score_data_h1,
        "auc_train": auc_train,
        "auc_test": auc_test,
        "importance": sorted_imp,
        "n_mc": n_mc,
        "n_data": n_data,
    }


# ============================================================
# TASK 2: BDT-BASED R_b EXTRACTION
# ============================================================
def task2_bdt_rb(bdt_results, hem_tags):
    """Extract R_b using BDT score as the tagging discriminant."""
    log.info("\n" + "=" * 70)
    log.info("TASK 2: BDT-based R_b extraction via 3-tag counting")
    log.info("=" * 70)

    score_mc_h0 = bdt_results["score_mc_h0"]
    score_mc_h1 = bdt_results["score_mc_h1"]
    score_data_h0 = bdt_results["score_data_h0"]
    score_data_h1 = bdt_results["score_data_h1"]

    # Use the existing 3-tag machinery with BDT scores
    # Scale BDT scores [0,1] to match the tag score range used by count_three_tag
    # count_three_tag expects scores and thresholds; we'll use BDT scores directly
    # with quantile-based thresholds

    # Determine thresholds from MC BDT score distribution
    all_mc_scores = np.concatenate([score_mc_h0, score_mc_h1])
    log.info("MC BDT score quantiles: 50%%=%.3f, 70%%=%.3f, 80%%=%.3f, "
             "90%%=%.3f, 95%%=%.3f",
             np.quantile(all_mc_scores, 0.5),
             np.quantile(all_mc_scores, 0.7),
             np.quantile(all_mc_scores, 0.8),
             np.quantile(all_mc_scores, 0.9),
             np.quantile(all_mc_scores, 0.95))

    # Scan threshold configurations
    threshold_configs = [
        # (tight_threshold, loose_threshold)
        (0.8, 0.3),
        (0.8, 0.4),
        (0.8, 0.5),
        (0.7, 0.3),
        (0.7, 0.4),
        (0.6, 0.3),
        (0.6, 0.4),
        (0.5, 0.2),
        (0.5, 0.3),
        (0.9, 0.4),
        (0.9, 0.5),
        (0.9, 0.6),
        (0.85, 0.4),
        (0.85, 0.5),
    ]

    results = []
    for thr_tight, thr_loose in threshold_configs:
        label = f"BDT tight={thr_tight:.2f}, loose={thr_loose:.2f}"

        # MC calibration
        counts_mc = count_three_tag(score_mc_h0, score_mc_h1, thr_tight, thr_loose)
        cal_mc = calibrate_three_tag_efficiencies(counts_mc, R_B_SM, R_C_SM)

        # Data counts
        counts_data = count_three_tag(score_data_h0, score_data_h1, thr_tight, thr_loose)

        # Scale factors
        sf_tight = counts_data["f_s_tight"] / max(counts_mc["f_s_tight"], 1e-10)
        sf_loose = counts_data["f_s_loose"] / max(counts_mc["f_s_loose"], 1e-10)
        sf_anti = counts_data["f_s_anti"] / max(counts_mc["f_s_anti"], 1e-10)

        # Apply SFs with renormalization
        cal_sf = {}
        for q in ["b", "c", "uds"]:
            et = cal_mc[f"eps_{q}_tight"] * sf_tight
            el = cal_mc[f"eps_{q}_loose"] * sf_loose
            ea = cal_mc[f"eps_{q}_anti"] * sf_anti
            tot = et + el + ea
            if tot > 0:
                cal_sf[f"eps_{q}_tight"] = float(et / tot)
                cal_sf[f"eps_{q}_loose"] = float(el / tot)
                cal_sf[f"eps_{q}_anti"] = float(ea / tot)
            else:
                cal_sf[f"eps_{q}_tight"] = cal_mc[f"eps_{q}_tight"]
                cal_sf[f"eps_{q}_loose"] = cal_mc[f"eps_{q}_loose"]
                cal_sf[f"eps_{q}_anti"] = cal_mc[f"eps_{q}_anti"]

        # Extract R_b
        extraction = extract_rb_three_tag(counts_data, cal_sf, R_C_SM, C_b_tight=1.0)

        # Toy uncertainty
        rb_mean, rb_sigma, _, n_valid = toy_uncertainty_three_tag(
            score_data_h0, score_data_h1, thr_tight, thr_loose,
            cal_sf, R_C_SM, n_toys=N_TOYS, seed=TOY_SEED)

        # b-purity in tight tag
        f_b_tight = cal_mc["eps_b_tight"] * R_B_SM / max(counts_mc["f_s_tight"], 1e-10)
        eps_c_over_eps_b = cal_mc["eps_c_tight"] / max(cal_mc["eps_b_tight"], 1e-10)

        log.info("%s: R_b=%.4f +/- %.4f, eps_c/eps_b=%.3f, f_b=%.3f, chi2/ndf=%.1f/%d",
                 label, extraction["R_b"],
                 rb_sigma if not np.isnan(rb_sigma) else 0.0,
                 eps_c_over_eps_b, f_b_tight,
                 extraction["chi2"], extraction["ndf"])

        results.append({
            "label": label,
            "thr_tight": float(thr_tight),
            "thr_loose": float(thr_loose),
            "R_b": extraction["R_b"],
            "sigma_stat": float(rb_sigma) if not np.isnan(rb_sigma) else None,
            "chi2": extraction["chi2"],
            "ndf": extraction["ndf"],
            "p_value": extraction["p_value"],
            "eps_b_tight": cal_mc["eps_b_tight"],
            "eps_c_tight": cal_mc["eps_c_tight"],
            "eps_uds_tight": cal_mc["eps_uds_tight"],
            "eps_c_over_eps_b": float(eps_c_over_eps_b),
            "f_b_tight": float(f_b_tight),
            "sf_tight": float(sf_tight),
            "sf_loose": float(sf_loose),
            "sf_anti": float(sf_anti),
            "n_valid_toys": n_valid,
        })

    # Best result: valid R_b, smallest uncertainty
    valid = [r for r in results if r["sigma_stat"] is not None
             and r["sigma_stat"] > 0 and 0.10 < r["R_b"] < 0.35]
    if valid:
        best = min(valid, key=lambda x: x["sigma_stat"])
        log.info("\nBest BDT R_b: %s", best["label"])
        log.info("  R_b = %.5f +/- %.5f (eps_c/eps_b = %.3f)",
                 best["R_b"], best["sigma_stat"], best["eps_c_over_eps_b"])
    else:
        best = None
        log.warning("No valid BDT R_b result!")

    # Plot: R_b vs threshold
    fig, ax = plt.subplots(figsize=(10, 10))
    valid_r = [r for r in results if r["sigma_stat"] is not None and r["sigma_stat"] > 0]
    if valid_r:
        thrights = [r["thr_tight"] for r in valid_r]
        rbs = [r["R_b"] for r in valid_r]
        sigmas = [r["sigma_stat"] for r in valid_r]
        ax.errorbar(thrights, rbs, yerr=sigmas, fmt="o", color="blue", markersize=6)
        ax.axhline(R_B_SM, color="red", ls="--", lw=2, label=f"SM $R_b$ = {R_B_SM:.5f}")
        ax.set_xlabel("BDT tight threshold")
        ax.set_ylabel("$R_b$")
        ax.legend()
        hep.label.exp_text("ALEPH", ax=ax, loc=1)
    fig.savefig(FIG_DIR / "bdt_rb_vs_threshold.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    log.info("Saved bdt_rb_vs_threshold.png")

    return {"results": results, "best": best}


# ============================================================
# TASK 3: BDT-BASED A_FB^b
# ============================================================
def task3_bdt_afb(bdt_results, jet_charge, data):
    """Extract A_FB^b using BDT-tagged events."""
    log.info("\n" + "=" * 70)
    log.info("TASK 3: BDT-based A_FB^b extraction")
    log.info("=" * 70)

    score_data_h0 = bdt_results["score_data_h0"]
    score_data_h1 = bdt_results["score_data_h1"]
    score_mc_h0 = bdt_results["score_mc_h0"]
    score_mc_h1 = bdt_results["score_mc_h1"]
    n_data = bdt_results["n_data"]
    n_mc = bdt_results["n_mc"]

    cos_theta_data = jet_charge["cos_theta_data"]
    cos_theta_mc = jet_charge["cos_theta_mc"]

    # A_FB^c values — zero on MC, observed on data
    AFB_C_OBS = 0.0682
    AFB_UDS = 0.0

    hem_tags_for_afb = np.load(P3_OUT / "hemisphere_tags.npz", allow_pickle=False)

    results_afb = []

    for bdt_cut in [0.5, 0.6, 0.7, 0.8, 0.9]:
        # Select events with BOTH hemispheres passing BDT cut (b-enriched)
        data_both_tag = (score_data_h0 > bdt_cut) & (score_data_h1 > bdt_cut)
        mc_both_tag = (score_mc_h0 > bdt_cut) & (score_mc_h1 > bdt_cut)

        n_tagged_data = np.sum(data_both_tag)
        n_tagged_mc = np.sum(mc_both_tag)

        if n_tagged_data < 1000 or n_tagged_mc < 100:
            log.info("BDT cut %.2f: too few events (data=%d, mc=%d), skipping",
                     bdt_cut, n_tagged_data, n_tagged_mc)
            continue

        log.info("BDT cut %.2f: %d data events, %d MC events",
                 bdt_cut, n_tagged_data, n_tagged_mc)

        # Estimate b-purity from MC tag counts
        mc_comb_h0_raw = hem_tags_for_afb["mc_combined_h0"]
        mc_comb_h1_raw = hem_tags_for_afb["mc_combined_h1"]

        # For events where both hemispheres pass BDT:
        # estimate purity from fraction of events where combined score is high
        high_combined = (mc_comb_h0_raw[mc_both_tag] > 8.0) & (mc_comb_h1_raw[mc_both_tag] > 8.0)
        f_b_est = np.mean(high_combined) if np.sum(mc_both_tag) > 0 else 0.5

        for kappa in [0.3, 0.5, 1.0, 2.0]:
            k_str = f"k{kappa}"
            qf_data = jet_charge[f"data_qf_{k_str}"]
            qb_data = jet_charge[f"data_qb_{k_str}"]
            qfb_data = jet_charge[f"data_qfb_{k_str}"]

            # Q_FB for tagged events
            qfb_tagged = qfb_data[data_both_tag]
            cos_tagged = cos_theta_data[data_both_tag]

            # Measure slope: <Q_FB> vs cos(theta)
            n_bins = 10
            cos_edges = np.linspace(COS_RANGE[0], COS_RANGE[1], n_bins + 1)
            cos_centers = 0.5 * (cos_edges[:-1] + cos_edges[1:])
            qfb_means = np.zeros(n_bins)
            qfb_errs = np.zeros(n_bins)
            for i in range(n_bins):
                mask = (cos_tagged >= cos_edges[i]) & (cos_tagged < cos_edges[i+1])
                if np.sum(mask) > 10:
                    qfb_means[i] = np.mean(qfb_tagged[mask])
                    qfb_errs[i] = np.std(qfb_tagged[mask]) / np.sqrt(np.sum(mask))

            # Fit slope: <Q_FB> = slope * cos(theta)
            valid_bins = qfb_errs > 0
            if np.sum(valid_bins) < 3:
                continue

            w = 1.0 / qfb_errs[valid_bins]**2
            slope = np.sum(w * qfb_means[valid_bins] * cos_centers[valid_bins]) / \
                    np.sum(w * cos_centers[valid_bins]**2)
            slope_err = 1.0 / np.sqrt(np.sum(w * cos_centers[valid_bins]**2))

            # Get published delta values
            if kappa in PUBLISHED_DELTA:
                delta_b = PUBLISHED_DELTA[kappa]["delta_b"]
                delta_c = PUBLISHED_DELTA[kappa]["delta_c"]
            else:
                continue

            # Estimate flavour fractions from MC calibration
            # For the double-tagged sample: use MC truth proxy
            # f_b, f_c, f_uds in the tagged sample
            f_b = min(max(f_b_est, 0.3), 0.95)  # reasonable bounds
            f_c = (1.0 - f_b) * R_C_SM / (R_C_SM + R_UDS_SM)
            f_uds = 1.0 - f_b - f_c

            # A_FB^b = (slope - f_c * delta_c * A_FB^c) / (f_b * delta_b)
            charm_correction = f_c * delta_c * AFB_C_OBS
            afb_b = (slope - charm_correction) / (f_b * delta_b)
            afb_b_err = slope_err / (f_b * delta_b)

            # QCD correction: A_FB^{0,b} = A_FB^b / (1 - DELTA_QCD)
            afb_b_pole = afb_b / (1.0 - DELTA_QCD - DELTA_QED)
            afb_b_pole_err = afb_b_err / (1.0 - DELTA_QCD - DELTA_QED)

            log.info("  kappa=%.1f: slope=%.5f +/- %.5f, f_b=%.3f, "
                     "A_FB^b=%.4f +/- %.4f, A_FB^{0,b}=%.4f +/- %.4f",
                     kappa, slope, slope_err, f_b,
                     afb_b, afb_b_err, afb_b_pole, afb_b_pole_err)

            results_afb.append({
                "bdt_cut": float(bdt_cut),
                "kappa": float(kappa),
                "n_tagged": int(n_tagged_data),
                "f_b_est": float(f_b),
                "slope": float(slope),
                "slope_err": float(slope_err),
                "afb_b": float(afb_b),
                "afb_b_err": float(afb_b_err),
                "afb_b_pole": float(afb_b_pole),
                "afb_b_pole_err": float(afb_b_pole_err),
            })

    # Best AFB result
    valid_afb = [r for r in results_afb
                 if r["afb_b_err"] > 0 and abs(r["afb_b"]) < 0.5]
    if valid_afb:
        # Pick kappa=0.5 results (best compromise), or smallest error
        k05 = [r for r in valid_afb if r["kappa"] == 0.5]
        best_afb = min(k05 if k05 else valid_afb, key=lambda x: x["afb_b_err"])
        log.info("\nBest BDT A_FB^b: cut=%.2f, kappa=%.1f",
                 best_afb["bdt_cut"], best_afb["kappa"])
        log.info("  A_FB^b = %.4f +/- %.4f", best_afb["afb_b"], best_afb["afb_b_err"])
        log.info("  A_FB^{0,b} = %.4f +/- %.4f", best_afb["afb_b_pole"],
                 best_afb["afb_b_pole_err"])
    else:
        best_afb = None

    # Plot: A_FB^b vs BDT cut for kappa=0.5
    fig, ax = plt.subplots(figsize=(10, 10))
    for kappa in [0.5, 1.0, 2.0]:
        k_results = [r for r in results_afb if r["kappa"] == kappa]
        if k_results:
            cuts = [r["bdt_cut"] for r in k_results]
            afbs = [r["afb_b"] for r in k_results]
            errs = [r["afb_b_err"] for r in k_results]
            ax.errorbar(cuts, afbs, yerr=errs, fmt="o-", label=f"$\\kappa={kappa}$",
                       markersize=6)
    ax.axhline(AFB_B_OBS, color="red", ls="--", lw=2,
               label=f"LEP $A_{{FB}}^b$ = {AFB_B_OBS:.4f}")
    ax.set_xlabel("BDT double-tag cut")
    ax.set_ylabel("$A_{FB}^b$")
    ax.legend()
    hep.label.exp_text("ALEPH", ax=ax, loc=1)
    fig.savefig(FIG_DIR / "bdt_afb_vs_cut.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    log.info("Saved bdt_afb_vs_cut.png")

    return {"results": results_afb, "best": best_afb}


# ============================================================
# TASK 4a: COMBINED MASS + BDT TAG
# ============================================================
def task4a_mass_bdt_combined(bdt_results, hem_tags):
    """Mass precut + BDT score as combined discriminant."""
    log.info("\n" + "=" * 70)
    log.info("TASK 4a: Combined mass > 1.8 GeV precut + BDT tag")
    log.info("=" * 70)

    score_mc_h0 = bdt_results["score_mc_h0"]
    score_mc_h1 = bdt_results["score_mc_h1"]
    score_data_h0 = bdt_results["score_data_h0"]
    score_data_h1 = bdt_results["score_data_h1"]

    mc_mass_h0 = hem_tags["mc_mass_h0"]
    mc_mass_h1 = hem_tags["mc_mass_h1"]
    data_mass_h0 = hem_tags["data_mass_h0"]
    data_mass_h1 = hem_tags["data_mass_h1"]

    # Apply mass precut: zero out BDT score if mass < 1.8
    mc_massbdt_h0 = score_mc_h0 * (mc_mass_h0 > 1.8).astype(float)
    mc_massbdt_h1 = score_mc_h1 * (mc_mass_h1 > 1.8).astype(float)
    data_massbdt_h0 = score_data_h0 * (data_mass_h0 > 1.8).astype(float)
    data_massbdt_h1 = score_data_h1 * (data_mass_h1 > 1.8).astype(float)

    results = []
    for thr_tight, thr_loose in [(0.7, 0.3), (0.7, 0.4), (0.6, 0.3),
                                  (0.6, 0.2), (0.5, 0.2), (0.8, 0.3),
                                  (0.8, 0.4), (0.8, 0.5), (0.5, 0.3)]:
        label = f"mass+BDT tight={thr_tight:.2f}, loose={thr_loose:.2f}"

        counts_mc = count_three_tag(mc_massbdt_h0, mc_massbdt_h1, thr_tight, thr_loose)
        cal_mc = calibrate_three_tag_efficiencies(counts_mc, R_B_SM, R_C_SM)
        counts_data = count_three_tag(data_massbdt_h0, data_massbdt_h1, thr_tight, thr_loose)

        sf_tight = counts_data["f_s_tight"] / max(counts_mc["f_s_tight"], 1e-10)
        sf_loose = counts_data["f_s_loose"] / max(counts_mc["f_s_loose"], 1e-10)
        sf_anti = counts_data["f_s_anti"] / max(counts_mc["f_s_anti"], 1e-10)

        cal_sf = {}
        for q in ["b", "c", "uds"]:
            et = cal_mc[f"eps_{q}_tight"] * sf_tight
            el = cal_mc[f"eps_{q}_loose"] * sf_loose
            ea = cal_mc[f"eps_{q}_anti"] * sf_anti
            tot = et + el + ea
            if tot > 0:
                cal_sf[f"eps_{q}_tight"] = float(et / tot)
                cal_sf[f"eps_{q}_loose"] = float(el / tot)
                cal_sf[f"eps_{q}_anti"] = float(ea / tot)
            else:
                cal_sf[f"eps_{q}_tight"] = cal_mc[f"eps_{q}_tight"]
                cal_sf[f"eps_{q}_loose"] = cal_mc[f"eps_{q}_loose"]
                cal_sf[f"eps_{q}_anti"] = cal_mc[f"eps_{q}_anti"]

        extraction = extract_rb_three_tag(counts_data, cal_sf, R_C_SM, C_b_tight=1.0)

        rb_mean, rb_sigma, _, n_valid = toy_uncertainty_three_tag(
            data_massbdt_h0, data_massbdt_h1, thr_tight, thr_loose,
            cal_sf, R_C_SM, n_toys=N_TOYS, seed=TOY_SEED)

        eps_c_over_eps_b = cal_mc["eps_c_tight"] / max(cal_mc["eps_b_tight"], 1e-10)
        f_b_tight = cal_mc["eps_b_tight"] * R_B_SM / max(counts_mc["f_s_tight"], 1e-10)

        log.info("%s: R_b=%.4f +/- %.4f, eps_c/eps_b=%.3f, f_b=%.3f",
                 label, extraction["R_b"],
                 rb_sigma if not np.isnan(rb_sigma) else 0.0,
                 eps_c_over_eps_b, f_b_tight)

        results.append({
            "label": label,
            "thr_tight": float(thr_tight),
            "thr_loose": float(thr_loose),
            "R_b": extraction["R_b"],
            "sigma_stat": float(rb_sigma) if not np.isnan(rb_sigma) else None,
            "chi2": extraction["chi2"],
            "ndf": extraction["ndf"],
            "p_value": extraction["p_value"],
            "eps_c_over_eps_b": float(eps_c_over_eps_b),
            "f_b_tight": float(f_b_tight),
            "sf_tight": float(sf_tight),
            "sf_loose": float(sf_loose),
            "sf_anti": float(sf_anti),
        })

    valid = [r for r in results if r["sigma_stat"] is not None
             and r["sigma_stat"] > 0 and 0.10 < r["R_b"] < 0.35]
    best = min(valid, key=lambda x: x["sigma_stat"]) if valid else None

    if best:
        log.info("\nBest mass+BDT R_b: %s", best["label"])
        log.info("  R_b = %.5f +/- %.5f", best["R_b"], best["sigma_stat"])

    return {"results": results, "best": best}


# ============================================================
# TASK 4b: MASS THRESHOLD OPTIMIZATION
# ============================================================
def task4b_mass_threshold_scan(hem_tags):
    """Scan mass cut from 1.0 to 3.0 GeV for optimal b-purity/efficiency."""
    log.info("\n" + "=" * 70)
    log.info("TASK 4b: Mass threshold optimization scan")
    log.info("=" * 70)

    mc_mass_h0 = hem_tags["mc_mass_h0"]
    mc_mass_h1 = hem_tags["mc_mass_h1"]
    mc_combined_h0 = hem_tags["mc_combined_h0"]
    mc_combined_h1 = hem_tags["mc_combined_h1"]
    data_mass_h0 = hem_tags["data_mass_h0"]
    data_mass_h1 = hem_tags["data_mass_h1"]
    data_combined_h0 = hem_tags["data_combined_h0"]
    data_combined_h1 = hem_tags["data_combined_h1"]

    # Use combined > 8 as b-truth proxy
    b_proxy_h0 = mc_combined_h0 > 8.0
    b_proxy_h1 = mc_combined_h1 > 8.0

    mass_cuts = np.arange(0.5, 4.1, 0.1)
    results = []

    for mcut in mass_cuts:
        # Fraction of b-proxy hemispheres passing mass cut
        n_b = np.sum(b_proxy_h0) + np.sum(b_proxy_h1)
        n_b_pass = np.sum(b_proxy_h0 & (mc_mass_h0 > mcut)) + \
                   np.sum(b_proxy_h1 & (mc_mass_h1 > mcut))
        eps_b = n_b_pass / max(n_b, 1)

        n_nonb = np.sum(~b_proxy_h0) + np.sum(~b_proxy_h1)
        n_nonb_pass = np.sum(~b_proxy_h0 & (mc_mass_h0 > mcut)) + \
                      np.sum(~b_proxy_h1 & (mc_mass_h1 > mcut))
        eps_nonb = n_nonb_pass / max(n_nonb, 1)

        # Purity = eps_b * R_b / (eps_b * R_b + eps_nonb * (1 - R_b))
        purity = eps_b * R_B_SM / max(eps_b * R_B_SM + eps_nonb * (1 - R_B_SM), 1e-10)

        # Figure of merit: eps_b * purity (want both high)
        fom = eps_b * purity

        results.append({
            "mass_cut": float(mcut),
            "eps_b": float(eps_b),
            "eps_nonb": float(eps_nonb),
            "purity": float(purity),
            "fom": float(fom),
        })

    # Find optimal
    best_idx = np.argmax([r["fom"] for r in results])
    best_mcut = results[best_idx]["mass_cut"]
    log.info("Optimal mass cut: %.1f GeV (eps_b=%.3f, purity=%.3f, FoM=%.4f)",
             best_mcut, results[best_idx]["eps_b"],
             results[best_idx]["purity"], results[best_idx]["fom"])

    # Plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
    mcuts = [r["mass_cut"] for r in results]
    ax1.plot(mcuts, [r["eps_b"] for r in results], "b-", lw=2, label="$\\epsilon_b$")
    ax1.plot(mcuts, [r["eps_nonb"] for r in results], "r-", lw=2, label="$\\epsilon_{non-b}$")
    ax1.set_ylabel("Efficiency")
    ax1.legend()
    ax1.axvline(best_mcut, color="gray", ls=":", lw=1)
    hep.label.exp_text("ALEPH", ax=ax1, loc=1)

    ax2.plot(mcuts, [r["purity"] for r in results], "g-", lw=2, label="b-purity")
    ax2.plot(mcuts, [r["fom"] for r in results], "k-", lw=2, label="FoM = $\\epsilon_b \\times$ purity")
    ax2.set_xlabel("Hemisphere mass cut [GeV/$c^2$]")
    ax2.set_ylabel("Purity / FoM")
    ax2.legend()
    ax2.axvline(best_mcut, color="gray", ls=":", lw=1)

    fig.savefig(FIG_DIR / "bdt_mass_threshold_scan.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    log.info("Saved bdt_mass_threshold_scan.png")

    return {"results": results, "optimal_mass_cut": best_mcut}


# ============================================================
# TASK 4d: TRACK-LEVEL BDT (lightweight)
# ============================================================
def task4d_track_level_bdt(mc, signed_d0, hem_tags, data):
    """Train a track-level BDT and aggregate to hemisphere scores."""
    log.info("\n" + "=" * 70)
    log.info("TASK 4d: Track-level BDT")
    log.info("=" * 70)

    import xgboost as xgb

    offsets = mc["trk_d0_offsets"]
    n_mc = len(offsets) - 1
    sig = signed_d0["mc_signed_sig"]
    hem = mc["trk_hem"]
    pmag = mc["trk_pmag"]
    pt = mc["trk_pt"]
    theta = mc["trk_theta"]
    nvdet = mc["trk_nvdet"]
    charge = mc["trk_charge"]
    d0 = mc["trk_d0"]

    event_idx = np.repeat(np.arange(n_mc), np.diff(offsets))
    hem_evt = 2 * event_idx + hem.astype(np.int64)

    # Track-level features
    X_trk = np.column_stack([
        np.abs(sig),
        np.abs(d0),
        pt,
        pmag,
        theta,
        nvdet.astype(np.float32),
        np.abs(charge).astype(np.float32),
    ])
    trk_feat_names = ["abs_d0_sig", "abs_d0", "pt", "pmag", "theta", "nvdet", "abs_charge"]

    # Label: track belongs to a "b-enriched" hemisphere
    mc_combined_h0 = hem_tags["mc_combined_h0"]
    mc_combined_h1 = hem_tags["mc_combined_h1"]
    combined_scores = np.zeros(2 * n_mc)
    combined_scores[0::2] = mc_combined_h0
    combined_scores[1::2] = mc_combined_h1
    trk_labels = (combined_scores[hem_evt] > 8.0).astype(np.float32)

    # Subsample for speed (use 20% of tracks)
    rng = np.random.RandomState(123)
    n_trk = len(X_trk)
    sub_mask = rng.random(n_trk) < 0.2
    X_sub = X_trk[sub_mask]
    y_sub = trk_labels[sub_mask]

    X_sub = np.nan_to_num(X_sub, nan=0.0, posinf=100.0, neginf=-100.0)

    # Train/test split
    idx = rng.permutation(len(X_sub))
    n_train = len(X_sub) // 2
    X_train = X_sub[idx[:n_train]]
    y_train = y_sub[idx[:n_train]]
    X_test = X_sub[idx[n_train:]]
    y_test = y_sub[idx[n_train:]]

    log.info("Track BDT: %d train, %d test (sig frac: %.3f)",
             len(X_train), len(X_test), np.mean(y_train))

    dtrain = xgb.DMatrix(X_train, label=y_train, feature_names=trk_feat_names)
    dtest = xgb.DMatrix(X_test, label=y_test, feature_names=trk_feat_names)

    params = {
        "objective": "binary:logistic",
        "eval_metric": "auc",
        "max_depth": 3,
        "learning_rate": 0.1,
        "subsample": 0.8,
        "min_child_weight": 200,
        "seed": 42,
        "verbosity": 0,
    }

    bdt_trk = xgb.train(params, dtrain, num_boost_round=100,
                         evals=[(dtest, "test")], verbose_eval=50)

    from sklearn.metrics import roc_auc_score
    score_test = bdt_trk.predict(dtest)
    auc = roc_auc_score(y_test, score_test)
    log.info("Track-level BDT AUC: %.4f", auc)

    # Score ALL MC tracks and aggregate to hemisphere
    X_trk_clean = np.nan_to_num(X_trk, nan=0.0, posinf=100.0, neginf=-100.0)
    d_all = xgb.DMatrix(X_trk_clean, feature_names=trk_feat_names)
    trk_scores = bdt_trk.predict(d_all)

    # Aggregate: mean track score per hemisphere
    hem_score_sum = np.zeros(2 * n_mc)
    hem_score_n = np.zeros(2 * n_mc, dtype=np.int64)
    np.add.at(hem_score_sum, hem_evt, trk_scores)
    np.add.at(hem_score_n, hem_evt, 1)
    hem_score_mean = np.where(hem_score_n > 0, hem_score_sum / hem_score_n, 0)

    # Also max track score per hemisphere
    hem_score_max = np.zeros(2 * n_mc)
    np.maximum.at(hem_score_max, hem_evt, trk_scores)

    trk_mc_h0_mean = hem_score_mean[0::2]
    trk_mc_h1_mean = hem_score_mean[1::2]
    trk_mc_h0_max = hem_score_max[0::2]
    trk_mc_h1_max = hem_score_max[1::2]

    # Do the same for data
    data_offsets = data["trk_d0_offsets"]
    n_data = len(data_offsets) - 1
    data_sig = signed_d0["data_signed_sig"]
    data_hem = data["trk_hem"]

    X_data_trk = np.column_stack([
        np.abs(data_sig),
        np.abs(data["trk_d0"]),
        data["trk_pt"],
        data["trk_pmag"],
        data["trk_theta"],
        data["trk_nvdet"].astype(np.float32),
        np.abs(data["trk_charge"]).astype(np.float32),
    ])
    X_data_trk = np.nan_to_num(X_data_trk, nan=0.0, posinf=100.0, neginf=-100.0)
    d_data_all = xgb.DMatrix(X_data_trk, feature_names=trk_feat_names)
    data_trk_scores = bdt_trk.predict(d_data_all)

    data_event_idx = np.repeat(np.arange(n_data), np.diff(data_offsets))
    data_hem_evt = 2 * data_event_idx + data_hem.astype(np.int64)

    data_hem_sum = np.zeros(2 * n_data)
    data_hem_n = np.zeros(2 * n_data, dtype=np.int64)
    np.add.at(data_hem_sum, data_hem_evt, data_trk_scores)
    np.add.at(data_hem_n, data_hem_evt, 1)
    data_hem_mean = np.where(data_hem_n > 0, data_hem_sum / data_hem_n, 0)

    trk_data_h0_mean = data_hem_mean[0::2]
    trk_data_h1_mean = data_hem_mean[1::2]

    # R_b extraction with track-level BDT
    results = []
    for thr_tight, thr_loose in [(0.5, 0.3), (0.5, 0.35), (0.45, 0.3),
                                  (0.55, 0.35), (0.6, 0.35)]:
        counts_mc = count_three_tag(trk_mc_h0_mean, trk_mc_h1_mean, thr_tight, thr_loose)
        cal_mc = calibrate_three_tag_efficiencies(counts_mc, R_B_SM, R_C_SM)
        counts_data = count_three_tag(trk_data_h0_mean, trk_data_h1_mean, thr_tight, thr_loose)

        sf_tight = counts_data["f_s_tight"] / max(counts_mc["f_s_tight"], 1e-10)
        sf_loose = counts_data["f_s_loose"] / max(counts_mc["f_s_loose"], 1e-10)
        sf_anti = counts_data["f_s_anti"] / max(counts_mc["f_s_anti"], 1e-10)

        cal_sf = {}
        for q in ["b", "c", "uds"]:
            et = cal_mc[f"eps_{q}_tight"] * sf_tight
            el = cal_mc[f"eps_{q}_loose"] * sf_loose
            ea = cal_mc[f"eps_{q}_anti"] * sf_anti
            tot = et + el + ea
            if tot > 0:
                cal_sf[f"eps_{q}_tight"] = float(et / tot)
                cal_sf[f"eps_{q}_loose"] = float(el / tot)
                cal_sf[f"eps_{q}_anti"] = float(ea / tot)
            else:
                for tag in ["tight", "loose", "anti"]:
                    cal_sf[f"eps_{q}_{tag}"] = cal_mc[f"eps_{q}_{tag}"]

        extraction = extract_rb_three_tag(counts_data, cal_sf, R_C_SM, C_b_tight=1.0)

        rb_mean, rb_sigma, _, n_valid = toy_uncertainty_three_tag(
            trk_data_h0_mean, trk_data_h1_mean, thr_tight, thr_loose,
            cal_sf, R_C_SM, n_toys=N_TOYS, seed=TOY_SEED)

        eps_c_over_eps_b = cal_mc["eps_c_tight"] / max(cal_mc["eps_b_tight"], 1e-10)

        log.info("Track BDT tight=%.2f, loose=%.2f: R_b=%.4f +/- %.4f, eps_c/eps_b=%.3f",
                 thr_tight, thr_loose, extraction["R_b"],
                 rb_sigma if not np.isnan(rb_sigma) else 0.0, eps_c_over_eps_b)

        results.append({
            "thr_tight": float(thr_tight),
            "thr_loose": float(thr_loose),
            "R_b": extraction["R_b"],
            "sigma_stat": float(rb_sigma) if not np.isnan(rb_sigma) else None,
            "eps_c_over_eps_b": float(eps_c_over_eps_b),
        })

    valid = [r for r in results if r["sigma_stat"] is not None
             and r["sigma_stat"] > 0 and 0.10 < r["R_b"] < 0.35]
    best = min(valid, key=lambda x: x["sigma_stat"]) if valid else None

    return {
        "track_bdt_auc": float(auc),
        "results": results,
        "best": best,
    }


# ============================================================
# TASK 4e: RAPIDITY GAP
# ============================================================
def task4e_rapidity_gap(mc, signed_d0, hem_tags):
    """Check if rapidity distribution of displaced tracks has discrimination power."""
    log.info("\n" + "=" * 70)
    log.info("TASK 4e: Rapidity gap investigation")
    log.info("=" * 70)

    offsets = mc["trk_d0_offsets"]
    n_mc = len(offsets) - 1
    sig = signed_d0["mc_signed_sig"]
    hem = mc["trk_hem"]
    pmag = mc["trk_pmag"]
    theta = mc["trk_theta"]
    PION_MASS = 0.13957

    E = np.sqrt(pmag**2 + PION_MASS**2)
    pz = pmag * np.cos(theta)
    # Rapidity
    rapidity = 0.5 * np.log((E + pz) / np.maximum(E - pz, 1e-10))

    event_idx = np.repeat(np.arange(n_mc), np.diff(offsets))
    hem_evt = 2 * event_idx + hem.astype(np.int64)

    # For displaced tracks (sig > 2), compute rapidity spread per hemisphere
    disp = sig > 2.0
    # Mean rapidity of displaced tracks per hemisphere
    rap_sum = np.zeros(2 * n_mc)
    rap_sumsq = np.zeros(2 * n_mc)
    n_disp = np.zeros(2 * n_mc, dtype=np.int64)
    np.add.at(rap_sum, hem_evt[disp], rapidity[disp])
    np.add.at(rap_sumsq, hem_evt[disp], rapidity[disp]**2)
    np.add.at(n_disp, hem_evt[disp], 1)

    rap_mean = np.where(n_disp > 0, rap_sum / n_disp, 0)
    rap_var = np.where(n_disp > 1,
                       (rap_sumsq / n_disp - rap_mean**2), 0)
    rap_std = np.sqrt(np.maximum(rap_var, 0))

    # Max-min rapidity range for displaced tracks
    rap_max = np.full(2 * n_mc, -999.0)
    rap_min = np.full(2 * n_mc, 999.0)
    np.maximum.at(rap_max, hem_evt[disp], rapidity[disp])
    np.minimum.at(rap_min, hem_evt[disp], rapidity[disp])
    rap_range = np.where(n_disp > 1, rap_max - rap_min, 0)

    # Compare b-enriched vs non-b
    mc_combined_h0 = hem_tags["mc_combined_h0"]
    mc_combined_h1 = hem_tags["mc_combined_h1"]
    b_mask_h0 = mc_combined_h0 > 8.0
    nonb_mask_h0 = mc_combined_h0 < 3.0

    rap_std_h0 = rap_std[0::2]
    rap_range_h0 = rap_range[0::2]

    log.info("Rapidity spread (displaced tracks):")
    log.info("  b-enriched: mean std=%.3f, mean range=%.3f",
             np.mean(rap_std_h0[b_mask_h0]),
             np.mean(rap_range_h0[b_mask_h0]))
    log.info("  non-b:      mean std=%.3f, mean range=%.3f",
             np.mean(rap_std_h0[nonb_mask_h0]),
             np.mean(rap_range_h0[nonb_mask_h0]))

    # Separation power
    from sklearn.metrics import roc_auc_score
    labels = np.concatenate([np.ones(np.sum(b_mask_h0)), np.zeros(np.sum(nonb_mask_h0))])
    scores = np.concatenate([rap_std_h0[b_mask_h0], rap_std_h0[nonb_mask_h0]])
    valid = np.isfinite(scores) & (scores > 0)
    if np.sum(valid) > 100 and np.sum(labels[valid] == 1) > 10:
        auc = roc_auc_score(labels[valid], scores[valid])
        log.info("  Rapidity std AUC: %.4f", auc)
    else:
        auc = 0.5
        log.info("  Insufficient valid samples for AUC")

    scores_range = np.concatenate([rap_range_h0[b_mask_h0], rap_range_h0[nonb_mask_h0]])
    valid_r = np.isfinite(scores_range) & (scores_range > 0)
    if np.sum(valid_r) > 100:
        auc_range = roc_auc_score(labels[valid_r], scores_range[valid_r])
        log.info("  Rapidity range AUC: %.4f", auc_range)
    else:
        auc_range = 0.5

    return {
        "rapidity_std_auc": float(auc),
        "rapidity_range_auc": float(auc_range),
        "b_enriched_mean_std": float(np.mean(rap_std_h0[b_mask_h0])),
        "nonb_mean_std": float(np.mean(rap_std_h0[nonb_mask_h0])),
    }


# ============================================================
# MAIN
# ============================================================
def main():
    t0 = time.time()
    log.info("=" * 70)
    log.info("BDT OPTIMIZATION WITH ALL FEATURES — Session kenji_3a32")
    log.info("=" * 70)

    # Load all data
    log.info("Loading data files...")
    mc = np.load(P3_OUT / "preselected_mc.npz", allow_pickle=False)
    data = np.load(P3_OUT / "preselected_data.npz", allow_pickle=False)
    signed_d0 = np.load(P3_OUT / "signed_d0.npz", allow_pickle=False)
    hem_tags = np.load(P3_OUT / "hemisphere_tags.npz", allow_pickle=False)
    sv_tags = np.load(PHASE4C_OUT / "sv_tags.npz", allow_pickle=False)
    jet_charge = np.load(P3_OUT / "jet_charge.npz", allow_pickle=False)
    d0_sig = np.load(P3_OUT / "d0_significance.npz", allow_pickle=False)

    log.info("MC events: %d, Data events: %d",
             len(hem_tags["mc_nlp_h0"]), len(hem_tags["data_nlp_h0"]))

    # === TASK 1: Train BDT ===
    bdt_results = task1_train_bdt(mc, data, signed_d0, hem_tags, sv_tags,
                                   jet_charge, d0_sig)

    # === TASK 2: BDT-based R_b ===
    rb_results = task2_bdt_rb(bdt_results, hem_tags)

    # === TASK 3: BDT-based A_FB^b ===
    afb_results = task3_bdt_afb(bdt_results, jet_charge, data)

    # === TASK 4a: Combined mass + BDT ===
    mass_bdt_results = task4a_mass_bdt_combined(bdt_results, hem_tags)

    # === TASK 4b: Mass threshold scan ===
    mass_scan_results = task4b_mass_threshold_scan(hem_tags)

    # === TASK 4d: Track-level BDT ===
    track_bdt_results = task4d_track_level_bdt(mc, signed_d0, hem_tags, data)

    # === TASK 4e: Rapidity gap ===
    rapidity_results = task4e_rapidity_gap(mc, signed_d0, hem_tags)

    # ============================================================
    # TASK 5: SUMMARY OF BEST RESULTS
    # ============================================================
    log.info("\n" + "=" * 70)
    log.info("TASK 5: SUMMARY OF BEST ACHIEVABLE RESULTS")
    log.info("=" * 70)

    summary = {
        "description": "BDT optimization — best achievable R_b and A_FB^b",
        "session": "kenji_3a32",
        "n_data_events": int(len(hem_tags["data_nlp_h0"])),
        "n_mc_events": int(len(hem_tags["mc_nlp_h0"])),
    }

    # Collect all R_b results
    all_rb_results = []

    # Previous baselines
    all_rb_results.append({
        "method": "Mass cut (previous best)",
        "R_b": 0.215, "sigma_stat": None, "eps_c_over_eps_b": None,
    })
    all_rb_results.append({
        "method": "SV tag (previous best)",
        "R_b": 0.217, "sigma_stat": None, "eps_c_over_eps_b": None,
    })

    if rb_results["best"]:
        b = rb_results["best"]
        all_rb_results.append({
            "method": f"BDT ({b['label']})",
            "R_b": b["R_b"], "sigma_stat": b["sigma_stat"],
            "eps_c_over_eps_b": b["eps_c_over_eps_b"],
        })

    if mass_bdt_results["best"]:
        b = mass_bdt_results["best"]
        all_rb_results.append({
            "method": f"Mass+BDT ({b['label']})",
            "R_b": b["R_b"], "sigma_stat": b["sigma_stat"],
            "eps_c_over_eps_b": b["eps_c_over_eps_b"],
        })

    if track_bdt_results["best"]:
        b = track_bdt_results["best"]
        all_rb_results.append({
            "method": f"Track BDT (tight={b['thr_tight']:.2f})",
            "R_b": b["R_b"], "sigma_stat": b["sigma_stat"],
            "eps_c_over_eps_b": b["eps_c_over_eps_b"],
        })

    log.info("\n--- R_b Results Summary ---")
    log.info("%-40s  %8s  %8s  %8s", "Method", "R_b", "sigma", "eps_c/eps_b")
    log.info("-" * 70)
    for r in all_rb_results:
        log.info("%-40s  %8.5f  %8s  %8s",
                 r["method"],
                 r["R_b"],
                 f"{r['sigma_stat']:.5f}" if r["sigma_stat"] else "   N/A",
                 f"{r['eps_c_over_eps_b']:.3f}" if r["eps_c_over_eps_b"] else "  N/A")
    log.info("SM value: R_b = %.5f", R_B_SM)

    # A_FB^b
    log.info("\n--- A_FB^b Results Summary ---")
    if afb_results["best"]:
        b = afb_results["best"]
        log.info("Best BDT A_FB^b: %.4f +/- %.4f (kappa=%.1f, cut=%.2f)",
                 b["afb_b"], b["afb_b_err"], b["kappa"], b["bdt_cut"])
        log.info("  A_FB^{0,b} = %.4f +/- %.4f", b["afb_b_pole"], b["afb_b_pole_err"])
    log.info("Previous SV A_FB^b: 0.052 +/- 0.004")
    log.info("ALEPH published A_FB^b: 0.093 +/- 0.005")

    # Additional investigations
    log.info("\n--- Additional Investigations ---")
    log.info("Rapidity gap: std AUC=%.4f, range AUC=%.4f",
             rapidity_results["rapidity_std_auc"],
             rapidity_results["rapidity_range_auc"])
    log.info("Track-level BDT AUC: %.4f", track_bdt_results["track_bdt_auc"])
    log.info("Optimal mass cut: %.1f GeV", mass_scan_results["optimal_mass_cut"])

    summary["bdt_training"] = {
        "auc_train": bdt_results["auc_train"],
        "auc_test": bdt_results["auc_test"],
        "feature_importance": bdt_results["importance"][:10],
    }
    summary["rb_bdt"] = {
        "all_results": rb_results["results"],
        "best": rb_results["best"],
    }
    summary["rb_mass_bdt"] = {
        "all_results": mass_bdt_results["results"],
        "best": mass_bdt_results["best"],
    }
    summary["afb_bdt"] = {
        "all_results": afb_results["results"],
        "best": afb_results["best"],
    }
    summary["mass_threshold_scan"] = mass_scan_results,
    summary["track_bdt"] = track_bdt_results,
    summary["rapidity_gap"] = rapidity_results,
    summary["all_rb_results"] = all_rb_results

    # --- COMPARISON PLOT ---
    fig, ax = plt.subplots(figsize=(10, 10))
    methods = []
    rbs = []
    sigmas = []
    for i, r in enumerate(all_rb_results):
        if r["R_b"] is not None:
            methods.append(r["method"][:30])
            rbs.append(r["R_b"])
            sigmas.append(r["sigma_stat"] if r["sigma_stat"] else 0)

    y_pos = range(len(methods))
    ax.errorbar(rbs, y_pos, xerr=sigmas, fmt="o", color="blue", markersize=8, capsize=5)
    ax.axvline(R_B_SM, color="red", ls="--", lw=2, label=f"SM $R_b$ = {R_B_SM:.5f}")
    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(methods)
    ax.set_xlabel("$R_b$")
    ax.legend()
    ax.invert_yaxis()
    hep.label.exp_text("ALEPH", ax=ax, loc=1)
    fig.savefig(FIG_DIR / "bdt_rb_comparison.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    log.info("Saved bdt_rb_comparison.png")

    # Save results
    with open(PHASE4C_OUT / "bdt_optimization_results.json", "w") as f:
        json.dump(summary, f, indent=2, default=str)
    log.info("\nSaved bdt_optimization_results.json")

    elapsed = time.time() - t0
    log.info("\nTotal time: %.1f minutes", elapsed / 60)


if __name__ == "__main__":
    main()
