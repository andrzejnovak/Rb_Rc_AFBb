"""Debug: try flipped PCA sign convention."""
import logging
from pathlib import Path
import numpy as np
from rich.logging import RichHandler

logging.basicConfig(level=logging.INFO, format="%(message)s",
                    handlers=[RichHandler(rich_tracebacks=True)])
log = logging.getLogger(__name__)

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "outputs"

data = np.load(OUT / "preselected_data.npz")

d0 = data["trk_d0"]
offsets = data["trk_d0_offsets"]
phi_trk = data["trk_phi"]
px_trk = data["trk_px"]
py_trk = data["trk_py"]
pz_trk = data["trk_pz"]
ttheta = data["ttheta"]
tphi = data["tphi"]

n_events = len(ttheta)
counts = np.diff(offsets)
ttheta_trk = np.repeat(ttheta, counts)
tphi_trk = np.repeat(tphi, counts)

thrust_x = np.sin(ttheta_trk) * np.cos(tphi_trk)
thrust_y = np.sin(ttheta_trk) * np.sin(tphi_trk)
thrust_z = np.cos(ttheta_trk)

dot_thrust = px_trk * thrust_x + py_trk * thrust_y + pz_trk * thrust_z
hem_sign = np.sign(dot_thrust)

jet_x = hem_sign * thrust_x
jet_y = hem_sign * thrust_y

# FLIPPED PCA direction: (d0*sin(phi), -d0*cos(phi))
pca_x = d0 * np.sin(phi_trk)
pca_y = -d0 * np.cos(phi_trk)

dot_pca_jet = pca_x * jet_x + pca_y * jet_y
signed_d0 = np.abs(d0) * np.sign(dot_pca_jet)

log.info("FLIPPED PCA sign convention:")
log.info("  fraction positive: %.4f", np.mean(signed_d0 > 0))

sig_data = np.load(OUT / "d0_significance.npz")
sigma_d0 = sig_data["data_sigma_d0"]
signed_sig = signed_d0 / sigma_d0

for thr in [3, 5, 7, 10, 15, 20]:
    npos = int(np.sum(signed_sig > thr))
    nneg = int(np.sum(signed_sig < -thr))
    ratio = npos / max(nneg, 1)
    asym = (npos - nneg) / max(npos + nneg, 1)
    log.info("  |sig|>%d: pos=%d, neg=%d, ratio=%.3f, asym=%.4f",
             thr, npos, nneg, ratio, asym)

# Save the signed d0 for downstream use if it validates
if np.sum(signed_sig > 3) / max(np.sum(signed_sig < -3), 1) > 1.5:
    log.info("\n*** VALIDATED: Flipped PCA sign gives physics-meaningful d0 ***")

    np.savez_compressed(
        OUT / "signed_d0.npz",
        data_signed_d0=signed_d0,
        data_signed_sig=signed_sig,
    )
    log.info("Saved signed_d0.npz")

    # Also compute for MC
    mc = np.load(OUT / "preselected_mc.npz")
    mc_d0 = mc["trk_d0"]
    mc_offsets = mc["trk_d0_offsets"]
    mc_phi = mc["trk_phi"]
    mc_px = mc["trk_px"]
    mc_py = mc["trk_py"]
    mc_pz = mc["trk_pz"]
    mc_ttheta = mc["ttheta"]
    mc_tphi = mc["tphi"]

    mc_counts = np.diff(mc_offsets)
    mc_ttheta_trk = np.repeat(mc_ttheta, mc_counts)
    mc_tphi_trk = np.repeat(mc_tphi, mc_counts)

    mc_tx = np.sin(mc_ttheta_trk) * np.cos(mc_tphi_trk)
    mc_ty = np.sin(mc_ttheta_trk) * np.sin(mc_tphi_trk)
    mc_tz = np.cos(mc_ttheta_trk)

    mc_dot = mc_px * mc_tx + mc_py * mc_ty + mc_pz * mc_tz
    mc_hem = np.sign(mc_dot)

    mc_jx = mc_hem * mc_tx
    mc_jy = mc_hem * mc_ty

    mc_pca_x = mc_d0 * np.sin(mc_phi)
    mc_pca_y = -mc_d0 * np.cos(mc_phi)

    mc_dot_pj = mc_pca_x * mc_jx + mc_pca_y * mc_jy
    mc_signed_d0 = np.abs(mc_d0) * np.sign(mc_dot_pj)
    mc_sigma_d0 = sig_data["mc_sigma_d0"]
    mc_signed_sig = mc_signed_d0 / mc_sigma_d0

    np.savez_compressed(
        OUT / "signed_d0.npz",
        data_signed_d0=signed_d0,
        data_signed_sig=signed_sig,
        mc_signed_d0=mc_signed_d0,
        mc_signed_sig=mc_signed_sig,
    )
    log.info("Saved signed_d0.npz (data + MC)")

    log.info("\nMC signed significance ratios:")
    for thr in [3, 5, 7, 10]:
        npos = int(np.sum(mc_signed_sig > thr))
        nneg = int(np.sum(mc_signed_sig < -thr))
        ratio = npos / max(nneg, 1)
        log.info("  |sig|>%d: pos=%d, neg=%d, ratio=%.3f", thr, npos, nneg, ratio)
else:
    log.info("\n*** NOT validated ***")
