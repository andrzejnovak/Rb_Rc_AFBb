"""Phase 4b: Systematic evaluation on 10% data with C_b=1.01."""
import json
import logging
import sys
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
PHASE4B_OUT = HERE.parent / "outputs"
P4A_OUT = HERE.parents[1] / "4a_expected" / "outputs"
RESULTS_DIR = HERE.parents[2] / "analysis_note" / "results"

sys.path.insert(0, str(HERE.parents[1] / "4a_expected" / "src"))
from rb_extraction import extract_rb, count_tags, apply_gluon_correction

R_B_SM = 0.21578
R_C_SM = 0.17223
R_C_ERR = 0.0030
G_BB = 0.00251
G_BB_ERR = 0.00063
G_CC = 0.0296
G_CC_ERR = 0.0038
C_B_PUBLISHED = 1.01
DELTA_QCD_ERR = 0.0029


def main():
    log.info("=" * 60)
    log.info("Phase 4b: Systematic Evaluation (10%% data)")
    log.info("=" * 60)

    # Load results
    with open(PHASE4B_OUT / "rb_results_10pct.json") as f:
        rb = json.load(f)
    with open(PHASE4B_OUT / "afb_results_10pct.json") as f:
        afb = json.load(f)

    best = rb["best_wp"]
    if best is None:
        log.error("No valid R_b extraction")
        return

    data_tags = np.load(PHASE4B_OUT / "data_10pct_tags.npz", allow_pickle=False)
    h0 = data_tags["data_combined_h0"]
    h1 = data_tags["data_combined_h1"]

    REF_WP = best["threshold"]
    R_b_nom = best["R_b"]
    eps_c_nom = best["eps_c"]
    eps_uds_nom = best["eps_uds_eff"]

    N_had, N_t, N_tt, f_s, f_d = count_tags(h0, h1, REF_WP)

    def shift_rb(eps_c, eps_uds, R_c, C_b):
        R_b_var, _ = extract_rb(f_s, f_d, eps_c, eps_uds, R_c, C_b)
        if np.isnan(R_b_var):
            return None
        return float(R_b_var - R_b_nom)

    systematics = {}

    # sigma_d0 (borrowed, scaled)
    systematics["sigma_d0"] = {
        "delta_Rb": 0.00075,
        "method": "Scaled from ALEPH (0.00050) x1.5",
        "source": "hep-ex/9609005",
    }

    # sigma_d0 form
    systematics["sigma_d0_form"] = {
        "delta_Rb": 0.00040,
        "method": "sin(theta) vs sin^{3/2}(theta)",
        "source": "STRATEGY.md 5.1",
    }

    # C_b systematic — from the C_b scan
    # R_b varies from 0.208 (C_b=1.01) to ~0.513 (C_b=1.10)
    # The max valid C_b is ~1.10
    C_b_syst = rb.get("C_b_systematic_range", 0.305)
    systematics["C_b"] = {
        "delta_Rb": C_b_syst,
        "method": "R_b variation over valid C_b range (1.01-1.10)",
        "source": "hep-ex/9609005, Phase 4b C_b scan",
        "notes": "C_b=1.01 is published ALEPH; higher values make discriminant negative",
    }

    # eps_c (+/- 30%)
    eps_c_var = 0.30 * eps_c_nom
    shift_up = shift_rb(eps_c_nom + eps_c_var, eps_uds_nom, R_C_SM, C_B_PUBLISHED)
    shift_down = shift_rb(eps_c_nom - eps_c_var, eps_uds_nom, R_C_SM, C_B_PUBLISHED)
    systematics["eps_c"] = {
        "delta_Rb": max(abs(shift_up or 0), abs(shift_down or 0)),
        "shift_up": shift_up, "shift_down": shift_down,
    }

    # eps_uds (+/- 50%)
    eps_uds_var = 0.50 * eps_uds_nom
    shift_up = shift_rb(eps_c_nom, eps_uds_nom + eps_uds_var, R_C_SM, C_B_PUBLISHED)
    shift_down = shift_rb(eps_c_nom, eps_uds_nom - eps_uds_var, R_C_SM, C_B_PUBLISHED)
    systematics["eps_uds"] = {
        "delta_Rb": max(abs(shift_up or 0), abs(shift_down or 0)),
        "shift_up": shift_up, "shift_down": shift_down,
    }

    # R_c (+/- 0.0030)
    shift_up = shift_rb(eps_c_nom, eps_uds_nom, R_C_SM + R_C_ERR, C_B_PUBLISHED)
    shift_down = shift_rb(eps_c_nom, eps_uds_nom, R_C_SM - R_C_ERR, C_B_PUBLISHED)
    systematics["R_c"] = {
        "delta_Rb": max(abs(shift_up or 0), abs(shift_down or 0)),
        "shift_up": shift_up, "shift_down": shift_down,
    }

    # Borrowed systematics
    systematics["hadronization"] = {"delta_Rb": 0.00045}
    systematics["physics_params"] = {"delta_Rb": 0.00020}
    systematics["g_bb"] = {"delta_Rb": float(G_BB_ERR * 0.5 * 0.217 / 0.612)}
    systematics["g_cc"] = {"delta_Rb": float(G_CC_ERR * 0.3 * eps_c_nom * 0.217 / 0.612)}
    systematics["tau_contamination"] = {"delta_Rb": 0.00005}
    systematics["selection_bias"] = {"delta_Rb": 0.00010}
    systematics["mc_statistics"] = {"delta_Rb": 0.00040}

    total_syst = np.sqrt(sum(s["delta_Rb"]**2 for s in systematics.values()))
    stat_unc = rb["stability"]["sigma_combined"] or best["sigma_stat"]
    total_unc = np.sqrt(stat_unc**2 + total_syst**2)

    # A_FB^b systematics
    afb_nom = afb["combination"]["A_FB_b"]
    afb_systematics = {}
    afb_systematics["delta_QCD"] = {"delta_AFB": DELTA_QCD_ERR * abs(afb_nom or 0.09)}
    # charge_model systematic: spread of A_FB^b across kappa values
    kappa_afb_vals = [
        kr["A_FB_b"] for kr in afb.get("kappa_results", [])
        if "A_FB_b" in kr and kr.get("sigma_A_FB_b", 0) > 0
        and not kr.get("demoted", False)
    ]
    if len(kappa_afb_vals) >= 2:
        charge_model_syst = float(np.std(kappa_afb_vals))
    else:
        charge_model_syst = 0.005  # fallback
    afb_systematics["charge_model"] = {"delta_AFB": charge_model_syst}
    afb_systematics["charm_asymmetry"] = {"delta_AFB": 0.0035 * 0.17 / 0.22}
    afb_systematics["angular_efficiency"] = {"delta_AFB": 0.0020}
    afb_total_syst = np.sqrt(sum(s["delta_AFB"]**2 for s in afb_systematics.values()))
    afb_stat = afb["combination"]["sigma_A_FB_b"] or 0.005

    log.info("\n--- R_b Systematic Summary (10%% data, C_b=1.01) ---")
    for name, s in sorted(systematics.items(), key=lambda x: -x[1]["delta_Rb"]):
        log.info("  %-25s  %.5f", name, s["delta_Rb"])
    log.info("  %-25s  %.5f", "Total systematic", total_syst)
    log.info("  %-25s  %.5f", "Statistical", stat_unc)
    log.info("  %-25s  %.5f", "Total", total_unc)

    log.info("\n--- A_FB^b Systematic Summary (10%% data) ---")
    for name, s in sorted(afb_systematics.items(), key=lambda x: -x[1]["delta_AFB"]):
        log.info("  %-25s  %.5f", name, s["delta_AFB"])
    log.info("  %-25s  %.5f", "Total systematic", afb_total_syst)
    log.info("  %-25s  %.5f", "Statistical", afb_stat)

    output = {
        "rb_systematics": systematics,
        "afb_systematics": afb_systematics,
        "rb_total": {
            "stat": float(stat_unc),
            "syst": float(total_syst),
            "total": float(total_unc),
        },
        "afb_total": {
            "stat": float(afb_stat),
            "syst": float(afb_total_syst),
            "total": float(np.sqrt(afb_stat**2 + afb_total_syst**2)),
        },
    }

    with open(PHASE4B_OUT / "systematics_10pct.json", "w") as f:
        json.dump(output, f, indent=2)
    log.info("\nSaved systematics_10pct.json")

    # Update results JSON
    with open(RESULTS_DIR / "systematics.json") as f:
        syst_global = json.load(f)
    syst_global["phase_4b_10pct"] = output
    with open(RESULTS_DIR / "systematics.json", "w") as f:
        json.dump(syst_global, f, indent=2)
    log.info("Updated analysis_note/results/systematics.json")


if __name__ == "__main__":
    main()
