"""Debug: vectorized signed d0 computation."""
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
log.info("Events: %d, Tracks: %d", n_events, len(d0))

# Broadcast event-level quantities to track level
# Using np.repeat with counts
counts = np.diff(offsets)
ttheta_trk = np.repeat(ttheta, counts)
tphi_trk = np.repeat(tphi, counts)

# Thrust axis components
thrust_x = np.sin(ttheta_trk) * np.cos(tphi_trk)
thrust_y = np.sin(ttheta_trk) * np.sin(tphi_trk)
thrust_z = np.cos(ttheta_trk)

# Determine hemisphere for each track
dot_thrust = px_trk * thrust_x + py_trk * thrust_y + pz_trk * thrust_z
hem_sign = np.sign(dot_thrust)

# Jet direction for each track (thrust axis in its hemisphere)
jet_x = hem_sign * thrust_x
jet_y = hem_sign * thrust_y

# PCA direction: (-d0*sin(phi), d0*cos(phi))
pca_x = -d0 * np.sin(phi_trk)
pca_y = d0 * np.cos(phi_trk)

# Signed IP = |d0| * sign(PCA dot jet_transverse)
dot_pca_jet = pca_x * jet_x + pca_y * jet_y
signed_d0 = np.abs(d0) * np.sign(dot_pca_jet)

log.info("Signed d0 (vectorized PCA method) computed")
log.info("  fraction positive: %.4f", np.mean(signed_d0 > 0))

sig_data = np.load(OUT / "d0_significance.npz")
sigma_d0 = sig_data["data_sigma_d0"]
signed_sig = signed_d0 / sigma_d0

for thr in [3, 5, 7, 10]:
    npos = int(np.sum(signed_sig > thr))
    nneg = int(np.sum(signed_sig < -thr))
    ratio = npos / max(nneg, 1)
    log.info("  |sig|>%d: pos=%d, neg=%d, ratio=%.3f", thr, npos, nneg, ratio)

# Also try: the raw d0 sign directly (maybe it IS already physics-signed
# but with the wrong convention)
raw_sig = d0 / sigma_d0
log.info("\nRaw d0/sigma (no re-signing):")
for thr in [3, 5, 7, 10]:
    npos = int(np.sum(raw_sig > thr))
    nneg = int(np.sum(raw_sig < -thr))
    ratio = npos / max(nneg, 1)
    log.info("  >%d: pos=%d, neg=%d, ratio=%.3f", thr, npos, nneg, ratio)

# Try flipped raw sign
log.info("\nFlipped raw d0/sigma:")
for thr in [3, 5, 7, 10]:
    npos = int(np.sum(-raw_sig > thr))
    nneg = int(np.sum(-raw_sig < -thr))
    ratio = npos / max(nneg, 1)
    log.info("  >%d: pos=%d, neg=%d, ratio=%.3f", thr, npos, nneg, ratio)

# Key insight: maybe the UNSIGNED |d0|/sigma is the correct variable
# and the "sign" should come from the PCA-jet calculation
log.info("\nFinal check: is there ANY asymmetry in any definition?")
log.info("  raw d0>0: %d (%.4f)", int(np.sum(d0 > 0)), np.mean(d0 > 0))
log.info("  signed_d0>0: %d (%.4f)", int(np.sum(signed_d0 > 0)), np.mean(signed_d0 > 0))
log.info("  signed_d0>0 in high-|d0| (|d0|>0.02cm): %.4f",
         np.mean(signed_d0[np.abs(d0) > 0.02] > 0))
log.info("  signed_d0>0 in high-|d0| (|d0|>0.05cm): %.4f",
         np.mean(signed_d0[np.abs(d0) > 0.05] > 0))
log.info("  signed_d0>0 in high-|d0| (|d0|>0.1cm): %.4f",
         np.mean(signed_d0[np.abs(d0) > 0.1] > 0))
