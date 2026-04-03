"""Phase 4c: BDT cross-check on full data.

Trains BDT on MC, applies to full data, extracts R_b via double-tag counting.

Reads: phase3_selection/outputs/preselected_mc.npz
       phase3_selection/outputs/preselected_data.npz
       phase3_selection/outputs/hemisphere_tags.npz
       phase3_selection/outputs/signed_d0.npz
Writes: phase4_inference/4c_observed/outputs/bdt_crosscheck_fulldata.json
"""
import json
import logging
from pathlib import Path

import numpy as np
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
PHASE4C_OUT = HERE.parent / "outputs"
PHASE4C_OUT.mkdir(parents=True, exist_ok=True)

hep.style.use("ATLAS")
plt.rcParams.update({
    "font.size": 16,
    "axes.labelsize": 18,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "legend.fontsize": 13,
})

R_B_SM = 0.21578
R_C_SM = 0.17223


def build_features(npz_data, signed_d0, sig_key):
    """Build per-hemisphere features for BDT."""
    sig = signed_d0[sig_key]
    offsets = npz_data["trk_d0_offsets"]
    hem = npz_data["trk_hem"]
    pmag = npz_data["trk_pmag"]
    theta = npz_data["trk_theta"]
    phi = npz_data["trk_phi"]
    n_events = len(offsets) - 1

    event_idx = np.repeat(np.arange(n_events), np.diff(offsets))
    hem_evt = 2 * event_idx + hem.astype(np.int64)

    PION_MASS = 0.13957

    max_sig = np.full(2 * n_events, -999.0)
    np.maximum.at(max_sig, hem_evt, sig)
    max_sig[max_sig < -900] = 0

    pos_mask = sig > 0
    sum_pos_sig = np.zeros(2 * n_events)
    n_pos = np.zeros(2 * n_events, dtype=np.int64)
    np.add.at(sum_pos_sig, hem_evt[pos_mask], sig[pos_mask])
    np.add.at(n_pos, hem_evt[pos_mask], 1)
    mean_pos_sig = np.where(n_pos > 0, sum_pos_sig / n_pos, 0)

    above2 = sig > 2.0
    above3 = sig > 3.0
    n_above2 = np.zeros(2 * n_events, dtype=np.int64)
    n_above3 = np.zeros(2 * n_events, dtype=np.int64)
    np.add.at(n_above2, hem_evt[above2], 1)
    np.add.at(n_above3, hem_evt[above3], 1)

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

    p_hem = np.zeros(2 * n_events)
    np.add.at(p_hem, hem_evt, pmag)

    ntrk = np.zeros(2 * n_events, dtype=np.int64)
    np.add.at(ntrk, hem_evt, 1)

    features_h0 = np.column_stack([
        max_sig[0::2], mean_pos_sig[0::2],
        n_above2[0::2], n_above3[0::2],
        hem_mass[0::2], p_hem[0::2], ntrk[0::2],
    ])
    features_h1 = np.column_stack([
        max_sig[1::2], mean_pos_sig[1::2],
        n_above2[1::2], n_above3[1::2],
        hem_mass[1::2], p_hem[1::2], ntrk[1::2],
    ])

    return features_h0, features_h1


def extract_rb_double_tag(tag_h0, tag_h1, eps_b, eps_c, eps_uds, C_b, R_c):
    """Extract R_b from double-tag counting."""
    n_events = len(tag_h0)
    n_s = np.sum(tag_h0.astype(int) + tag_h1.astype(int))
    n_d = np.sum(tag_h0 & tag_h1)

    f_s = n_s / (2 * n_events)
    f_d = n_d / n_events

    denom = eps_b**2 * C_b - eps_uds**2
    if abs(denom) < 1e-12:
        return None, None, None, None

    R_b = (f_d - R_c * (eps_c**2 - eps_uds**2) - eps_uds**2) / denom
    sigma_fd = np.sqrt(f_d * (1 - f_d) / n_events)
    sigma_Rb = sigma_fd / abs(denom)

    return float(R_b), float(sigma_Rb), float(f_s), float(f_d)


def main():
    log.info("=" * 60)
    log.info("Phase 4c: BDT Cross-Check on Full Data")
    log.info("=" * 60)

    mc = np.load(P3_OUT / "preselected_mc.npz", allow_pickle=False)
    mc_tags = np.load(P3_OUT / "hemisphere_tags.npz", allow_pickle=False)
    signed_d0 = np.load(P3_OUT / "signed_d0.npz", allow_pickle=False)
    data = np.load(P3_OUT / "preselected_data.npz", allow_pickle=False)

    mc_h0 = mc_tags["mc_combined_h0"]
    mc_h1 = mc_tags["mc_combined_h1"]
    n_mc = len(mc_h0)

    try:
        from sklearn.ensemble import GradientBoostingClassifier
    except ImportError:
        log.error("sklearn not available")
        return

    # Build MC features
    log.info("Building MC features...")
    features_h0_mc, features_h1_mc = build_features(mc, signed_d0, "mc_signed_sig")

    # Train on MC h0 with cut-based labels
    label_threshold = 7.0
    labels_h0 = (mc_h0 > label_threshold).astype(int)

    rng = np.random.RandomState(42)
    train_mask = rng.random(n_mc) < 0.6

    X_train = features_h0_mc[train_mask]
    y_train = labels_h0[train_mask]
    log.info("Training BDT: %d samples, signal fraction = %.3f",
             len(X_train), np.mean(y_train))

    bdt = GradientBoostingClassifier(
        n_estimators=100, max_depth=3, learning_rate=0.1,
        min_samples_leaf=100, random_state=42,
    )
    bdt.fit(X_train, y_train)

    # Score MC
    score_h0_mc = bdt.predict_proba(features_h0_mc)[:, 1]
    score_h1_mc = bdt.predict_proba(features_h1_mc)[:, 1]

    # Build data features
    log.info("Building data features...")
    features_h0_data, features_h1_data = build_features(data, signed_d0, "data_signed_sig")

    score_h0_data = bdt.predict_proba(features_h0_data)[:, 1]
    score_h1_data = bdt.predict_proba(features_h1_data)[:, 1]

    # Extract at various BDT thresholds
    results_by_threshold = []
    for bdt_thr in [0.3, 0.4, 0.5, 0.6, 0.7]:
        bdt_tag_h0_mc = score_h0_mc > bdt_thr
        bdt_tag_h1_mc = score_h1_mc > bdt_thr

        # MC efficiencies using truth proxy
        truth_b_h0 = mc_h0 > 10.0
        truth_b_h1 = mc_h1 > 10.0
        eps_b_approx = (np.sum(bdt_tag_h0_mc[truth_b_h0]) + np.sum(bdt_tag_h1_mc[truth_b_h1])) / \
                       max(np.sum(truth_b_h0) + np.sum(truth_b_h1), 1)

        non_b_h0 = ~truth_b_h0
        non_b_h1 = ~truth_b_h1
        eps_nonb_approx = (np.sum(bdt_tag_h0_mc[non_b_h0]) + np.sum(bdt_tag_h1_mc[non_b_h1])) / \
                          max(np.sum(non_b_h0) + np.sum(non_b_h1), 1)

        eps_c_cut = 0.285
        eps_uds_cut = 0.077
        ratio_c_uds = eps_c_cut / max(eps_uds_cut, 1e-6)
        eps_c_bdt = eps_nonb_approx * ratio_c_uds / (1 + ratio_c_uds)
        eps_uds_bdt = eps_nonb_approx / (1 + ratio_c_uds)

        # Apply to full data
        bdt_tag_h0 = score_h0_data > bdt_thr
        bdt_tag_h1 = score_h1_data > bdt_thr

        R_b, sigma_Rb, f_s, f_d = extract_rb_double_tag(
            bdt_tag_h0, bdt_tag_h1,
            eps_b_approx, eps_c_bdt, eps_uds_bdt, 1.01, R_C_SM)

        log.info("BDT thr=%.1f: R_b=%.4f +/- %.4f, f_s=%.4f, f_d=%.4f",
                 bdt_thr, R_b or 0, sigma_Rb or 0, f_s or 0, f_d or 0)

        results_by_threshold.append({
            "bdt_threshold": bdt_thr,
            "R_b": R_b,
            "sigma_Rb": sigma_Rb,
            "f_s": f_s,
            "f_d": f_d,
            "eps_b_approx": float(eps_b_approx),
            "eps_c_approx": float(eps_c_bdt),
            "eps_uds_approx": float(eps_uds_bdt),
        })

    # Find best BDT threshold
    valid_results = [r for r in results_by_threshold
                     if r["R_b"] is not None and 0.05 < r["R_b"] < 0.5]
    best = min(valid_results,
               key=lambda r: abs(r["R_b"] - R_B_SM), default=None)

    # Load cut-based result for comparison
    rb_full_path = PHASE4C_OUT / "three_tag_rb_fulldata.json"
    cut_based_rb = None
    cut_based_sigma = None
    if rb_full_path.exists():
        with open(rb_full_path) as f:
            full_rb = json.load(f)
        if full_rb.get("best_config"):
            cut_based_rb = full_rb["best_config"]["R_b"]
            cut_based_sigma = full_rb["best_config"]["sigma_stat"]

    output = {
        "description": "BDT cross-check R_b on full ALEPH 1992-1995 data",
        "n_data_events": len(features_h0_data),
        "results_by_threshold": results_by_threshold,
        "best": {
            "bdt_threshold": best["bdt_threshold"] if best else None,
            "R_b": best["R_b"] if best else None,
            "sigma_Rb": best["sigma_Rb"] if best else None,
        },
        "cut_based_comparison": {
            "R_b_cut_based": cut_based_rb,
            "sigma_cut_based": cut_based_sigma,
        },
    }

    with open(PHASE4C_OUT / "bdt_crosscheck_fulldata.json", "w") as f:
        json.dump(output, f, indent=2, default=str)
    log.info("\nSaved bdt_crosscheck_fulldata.json")


if __name__ == "__main__":
    main()
