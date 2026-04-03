"""Debug: compute signed d0 using PCA position and jet direction.

The signed impact parameter for b-tagging requires:
1. The PCA (point of closest approach) of the track to the primary vertex
2. The jet direction

sign(IP) = sign( (PCA - PV) dot jet_direction )

For a track with impact parameter d0 and azimuthal angle phi at the PCA:
PCA_x = -d0 * sin(phi)   [standard helix convention]
PCA_y = +d0 * cos(phi)

Then signed_IP = |d0| * sign( PCA_direction dot jet_direction )
"""
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
px = data["trk_px"]
py = data["trk_py"]
ttheta = data["ttheta"]
tphi = data["tphi"]

n_events = len(ttheta)
log.info("Events: %d, Tracks: %d", n_events, len(d0))

# Jet direction in transverse plane (thrust axis)
thrust_x = np.sin(ttheta) * np.cos(tphi)
thrust_y = np.sin(ttheta) * np.sin(tphi)

# PCA direction (perpendicular to track at point of closest approach)
# In standard ALEPH convention:
# d0 is signed such that d0 = -PCA_x*sin(phi0) + PCA_y*cos(phi0)
# where phi0 is the track azimuth at the PCA.
# So PCA direction is (-sin(phi0), cos(phi0)) * d0

# The PCA position relative to origin is approximately:
# PCA_x ~ -d0 * sin(phi_trk)
# PCA_y ~ +d0 * cos(phi_trk)

signed_d0 = np.empty_like(d0)

for i in range(n_events):
    start, end = offsets[i], offsets[i+1]
    if start == end:
        continue

    d = d0[start:end]
    phi = phi_trk[start:end]

    # PCA direction
    pca_x = -d * np.sin(phi)
    pca_y = d * np.cos(phi)

    # Jet direction (thrust axis projected to transverse plane)
    jx = thrust_x[i]
    jy = thrust_y[i]

    # For each track, the jet is the thrust axis direction in the
    # HEMISPHERE the track belongs to. If the track is in hemisphere 1
    # (positive thrust dot), the jet direction is +thrust. If hemisphere 0,
    # the jet direction is -thrust.
    trk_px_i = px[start:end]
    trk_py_i = py[start:end]
    trk_pz = data["trk_pz"][start:end]

    # Dot product with thrust axis (3D) to determine hemisphere
    thrust_z = np.cos(ttheta[i])
    dot_thrust = trk_px_i * thrust_x[i] + trk_py_i * thrust_y[i] + trk_pz * thrust_z
    hem_sign = np.sign(dot_thrust)

    # Jet direction for each track (±thrust, depending on hemisphere)
    jet_x = hem_sign * jx
    jet_y = hem_sign * jy

    # Signed IP: positive if PCA is "in front of" PV along jet direction
    dot = pca_x * jet_x + pca_y * jet_y
    signed_d0[start:end] = np.abs(d) * np.sign(dot)

log.info("Signed d0 (PCA method) computed")
log.info("  fraction positive: %.4f", np.mean(signed_d0 > 0))
log.info("  fraction negative: %.4f", np.mean(signed_d0 < 0))

# Check tail asymmetry
sig_data = np.load(OUT / "d0_significance.npz")
sigma_d0 = sig_data["data_sigma_d0"]
signed_sig = signed_d0 / sigma_d0

for thr in [3, 5, 7, 10]:
    npos = np.sum(signed_sig > thr)
    nneg = np.sum(signed_sig < -thr)
    ratio = npos / max(nneg, 1)
    log.info("  |sig|>%d: pos=%d, neg=%d, ratio=%.3f", thr, npos, nneg, ratio)

# Also try: just use the ABSOLUTE d0 (unsigned) as the b-tagging variable
# This is the "track probability" approach where P(track) = P(|d0/sigma| > observed)
# No sign needed — the probability approach uses the survival function
log.info("\nUsing |d0|/sigma_d0 (unsigned) for tagging:")
abs_sig = np.abs(d0) / sigma_d0
for thr in [3, 5, 7, 10]:
    n_above = np.sum(abs_sig > thr)
    log.info("  |d0/sigma|>%d: %d tracks (%.2f%%)",
             thr, n_above, 100.0 * n_above / len(abs_sig))
