"""Debug: check d0 distribution properties."""
import logging
from pathlib import Path
import numpy as np
from rich.logging import RichHandler

logging.basicConfig(level=logging.INFO, format="%(message)s",
                    handlers=[RichHandler(rich_tracebacks=True)])
log = logging.getLogger(__name__)

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "outputs"

d = np.load(OUT / "preselected_data.npz")
d0 = d["trk_d0"]
log.info("d0 stats:")
log.info("  min=%.6f, max=%.6f", d0.min(), d0.max())
log.info("  mean=%.6f, std=%.6f", d0.mean(), d0.std())
log.info("  n_positive=%d, n_negative=%d", np.sum(d0 > 0), np.sum(d0 < 0))
log.info("  fraction positive=%.4f", np.mean(d0 > 0))

log.info("After sigma_d0 calibration:")
s = np.load(OUT / "d0_significance.npz")
sig = s["data_significance"]
log.info("  sig min=%.3f, max=%.3f", sig.min(), sig.max())
log.info("  n_pos_sig=%d, n_neg_sig=%d", np.sum(sig > 0), np.sum(sig < 0))
log.info("  fraction positive sig=%.4f", np.mean(sig > 0))
log.info("  |sig|>3 positive: %d, negative: %d", np.sum(sig > 3), np.sum(sig < -3))
log.info("  |sig|>5 positive: %d, negative: %d", np.sum(sig > 5), np.sum(sig < -5))
log.info("  |sig|>10 positive: %d, negative: %d", np.sum(sig > 10), np.sum(sig < -10))

# The d0 should be SIGNED: positive = displaced from PV in jet direction
# Check if d0 is correlated with jet activity
# Use the dot_thrust to check which hemisphere has more activity
dot = d["trk_dot_thrust"]
log.info("\nCorrelation d0 with dot_thrust:")
log.info("  mean d0 where dot>0: %.6f", d0[dot > 0].mean())
log.info("  mean d0 where dot<0: %.6f", d0[dot < 0].mean())

# The KEY issue: the d0 might need to be signed w.r.t. the jet axis
# d0 as stored may be unsigned or signed w.r.t. the primary vertex
# Check: is d0 symmetric?
log.info("\nd0 percentiles:")
for p in [1, 5, 10, 25, 50, 75, 90, 95, 99]:
    log.info("  %d%%: %.6f", p, np.percentile(d0, p))
