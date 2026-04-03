"""Debug: compute signed d0 w.r.t. jet axis and verify asymmetry.

The stored d0 is the impact parameter signed w.r.t. the primary vertex,
but for b-tagging we need it signed w.r.t. the JET axis:
  sign = +1 if the track crosses the jet axis downstream of PV (displaced vertex)
  sign = -1 if upstream (resolution)

The sign is determined by: sign(d0_signed) = sign(d0) * sign(sin(phi_trk - phi_jet))
Or equivalently: the sign is positive if the track's perigee point lies
in the same half-plane as the jet direction.

For our data: the sign of the impact parameter w.r.t. the thrust axis is:
  signed_d0 = |d0| * sign(r_perp dot j_perp)
where r_perp is the track's point of closest approach direction (perpendicular to beam)
and j_perp is the jet/thrust axis direction projected to transverse plane.
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
theta_trk = data["trk_theta"]
px = data["trk_px"]
py = data["trk_py"]
pz = data["trk_pz"]
ttheta = data["ttheta"]
tphi = data["tphi"]

n_events = len(ttheta)
log.info("Computing signed d0 w.r.t. thrust axis for %d events", n_events)

# Thrust axis transverse components (event-level)
thrust_x = np.sin(ttheta) * np.cos(tphi)
thrust_y = np.sin(ttheta) * np.sin(tphi)

# For each track, the signed IP is:
# signed_d0 = d0 * sign(cross product of track pT direction and thrust pT direction)
# The cross product gives the sign: positive if track curves away from jet axis

signed_d0 = np.empty_like(d0)

for i in range(n_events):
    start, end = offsets[i], offsets[i+1]
    if start == end:
        continue

    # Track transverse momentum direction
    trk_px = px[start:end]
    trk_py = py[start:end]

    # Thrust axis direction in transverse plane
    tx = thrust_x[i]
    ty = thrust_y[i]

    # Cross product (z-component): px*ty - py*tx
    # This gives the sign of the impact parameter w.r.t. the jet axis
    cross = trk_px * ty - trk_py * tx

    # signed d0 = |d0| * sign(cross)
    signed_d0[start:end] = np.abs(d0[start:end]) * np.sign(cross)

log.info("Signed d0 computed")
log.info("  fraction positive: %.4f", np.mean(signed_d0 > 0))
log.info("  fraction negative: %.4f", np.mean(signed_d0 < 0))

# Now check: is the positive tail enhanced?
sig = np.load(OUT / "d0_significance.npz")
sigma_d0 = sig["data_sigma_d0"]

signed_sig = signed_d0 / sigma_d0

log.info("\nSigned significance stats:")
log.info("  |sig|>3 positive: %d, negative: %d",
         np.sum(signed_sig > 3), np.sum(signed_sig < -3))
log.info("  |sig|>5 positive: %d, negative: %d",
         np.sum(signed_sig > 5), np.sum(signed_sig < -5))
log.info("  |sig|>10 positive: %d, negative: %d",
         np.sum(signed_sig > 10), np.sum(signed_sig < -10))

ratio_3 = np.sum(signed_sig > 3) / max(np.sum(signed_sig < -3), 1)
ratio_5 = np.sum(signed_sig > 5) / max(np.sum(signed_sig < -5), 1)
ratio_10 = np.sum(signed_sig > 10) / max(np.sum(signed_sig < -10), 1)
log.info("\nPositive/negative tail ratios:")
log.info("  >3 sigma: %.3f", ratio_3)
log.info("  >5 sigma: %.3f", ratio_5)
log.info("  >10 sigma: %.3f", ratio_10)

if ratio_3 > 1.5:
    log.info("\n*** d0 sign w.r.t. thrust axis VALIDATES the physics sign ***")
else:
    log.info("\n*** d0 sign w.r.t. thrust axis does NOT validate ***")
    log.info("Trying alternative: sign from dot product with hemisphere axis")

    # Alternative: sign from dot product of (track direction at PCA) with thrust
    # The impact parameter is positive if the track's PCA is on the same side
    # as the jet direction
    hem = data["trk_hem"]
    # hem = True means positive dot product with thrust
    # If track is in hemisphere 1 (positive thrust dot), positive d0 should
    # mean displaced from PV toward the jet
    # Try: signed_d0 = d0 * (2*hem - 1)
    signed_d0_v2 = d0 * (2 * hem.astype(float) - 1)
    signed_sig_v2 = signed_d0_v2 / sigma_d0

    log.info("\nV2 (sign from hemisphere assignment):")
    log.info("  |sig|>3 positive: %d, negative: %d",
             np.sum(signed_sig_v2 > 3), np.sum(signed_sig_v2 < -3))
    ratio_3_v2 = np.sum(signed_sig_v2 > 3) / max(np.sum(signed_sig_v2 < -3), 1)
    ratio_5_v2 = np.sum(signed_sig_v2 > 5) / max(np.sum(signed_sig_v2 < -5), 1)
    log.info("  >3 sigma ratio: %.3f", ratio_3_v2)
    log.info("  >5 sigma ratio: %.3f", ratio_5_v2)
