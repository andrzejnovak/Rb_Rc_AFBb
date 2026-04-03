"""Task 7: Data/MC normalization investigation.

Check what luminosity/cross-section information is available.
Per spec: should use luminosity x cross-section, not normalize to data integral.

Reads: phase3_selection/outputs/cutflow.json
       phase3_selection/outputs/preselected_data.npz
       phase3_selection/outputs/preselected_mc.npz
Writes: outputs/normalization_check.json
"""
import json
import logging
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
P3_OUT = HERE.parents[2] / "phase3_selection" / "outputs"
P4B_OUT = HERE.parent / "outputs"

# Published ALEPH luminosities (hep-ex/0509008, Table 1)
# Year: integrated luminosity (pb^-1)
PUBLISHED_LUMI = {
    1991: 12.2,
    1992: 22.6,
    1993: 22.6,
    1994: 60.6,  # Combined P1+P2+P3
    1995: 32.8,
}

# Z hadronic cross-section (PDG 2024)
SIGMA_HAD_Z = 41.541e3  # fb (41.541 nb = 41541 fb)
# Or equivalently: 30.527 nb at peak (hep-ex/0509008)
SIGMA_HAD_PEAK = 30.527  # nb

# Number of expected hadronic events at peak:
# N = L * sigma_had


def main():
    log.info("=" * 60)
    log.info("Task 7: Data/MC Normalization Check")
    log.info("=" * 60)

    # Load cutflow
    with open(P3_OUT / "cutflow.json") as f:
        cutflow = json.load(f)

    data_total = cutflow["data"]["total"]
    data_presel = cutflow["data"]["cos_theta_cut"]
    mc_total = cutflow["mc"]["total"]
    mc_presel = cutflow["mc"]["cos_theta_cut"]

    log.info("Data: %d total, %d after preselection", data_total, data_presel)
    log.info("MC:   %d total, %d after preselection", mc_total, mc_presel)

    # Load year distributions
    data = np.load(P3_OUT / "preselected_data.npz", allow_pickle=False)
    mc = np.load(P3_OUT / "preselected_mc.npz", allow_pickle=False)

    data_years, data_counts = np.unique(data["year"], return_counts=True)
    mc_years, mc_counts = np.unique(mc["year"], return_counts=True)

    log.info("\nData per year:")
    for y, c in zip(data_years, data_counts):
        log.info("  %d: %d events", y, c)

    log.info("\nMC per year:")
    for y, c in zip(mc_years, mc_counts):
        log.info("  %d: %d events", y, c)

    # Expected events from luminosity
    log.info("\nExpected events from published luminosities:")
    total_expected = 0
    for year, lumi in sorted(PUBLISHED_LUMI.items()):
        if year in data_years:
            expected = lumi * 1000 * SIGMA_HAD_PEAK  # pb^-1 * nb * 1000 fb/nb... wait
            # L in pb^-1, sigma in nb = 1000 fb
            # N = L(pb^-1) * sigma(nb) * 1000 (conversion: 1 pb = 1000 fb, 1 nb = 1000 pb)
            # Wait: 1 nb = 1000 pb, so N = L(pb^-1) * sigma(nb) * 1000
            expected = lumi * SIGMA_HAD_PEAK * 1000
            log.info("  %d: L=%.1f pb^-1, expected N_had = %.0f",
                     year, lumi, expected)
            total_expected += expected

    log.info("  Total expected: %.0f", total_expected)
    log.info("  Total observed (all data): %d", data_total)
    log.info("  Ratio observed/expected: %.3f", data_total / total_expected if total_expected > 0 else 0)

    # Normalization factors
    # Current approach: MC is normalized to data (implicit, by using fractions)
    # The double-tag method uses f_s = N_t / (2*N_had) which is self-normalizing.
    # For data/MC comparison plots, need explicit normalization.
    data_mc_ratio = data_presel / mc_presel
    log.info("\nData/MC ratio after preselection: %.4f", data_mc_ratio)
    log.info("If using L*sigma: need MC normalized to L*sigma*acceptance")

    # 10% subsample
    n_10pct = len(np.load(P4B_OUT / "data_10pct_tags.npz", allow_pickle=False)["data_combined_h0"])
    log.info("\n10%% subsample: %d events", n_10pct)
    log.info("Expected from luminosity (10%%): %.0f", total_expected * 0.1)

    output = {
        'description': (
            'Data/MC normalization investigation. The double-tag method is '
            'self-normalizing (uses fractions f_s, f_d), so absolute normalization '
            'does not affect the R_b extraction. For A_FB^b, the slope of <Q_FB> '
            'vs cos(theta) is also self-normalizing. Data/MC comparison plots '
            'should use luminosity x cross-section normalization where possible.'
        ),
        'data_events': {
            'total': data_total,
            'preselected': data_presel,
            'per_year': dict(zip(data_years.tolist(), data_counts.tolist())),
        },
        'mc_events': {
            'total': mc_total,
            'preselected': mc_presel,
            'per_year': dict(zip(mc_years.tolist(), mc_counts.tolist())),
        },
        'published_luminosities': PUBLISHED_LUMI,
        'luminosity_source': 'ALEPH hep-ex/0509008 Table 1',
        'sigma_had_peak_nb': SIGMA_HAD_PEAK,
        'data_mc_ratio': float(data_mc_ratio),
        'normalization_note': (
            'The double-tag extraction uses event fractions (f_s, f_d), which are '
            'self-normalizing. The A_FB extraction uses mean Q_FB in bins, which is '
            'also self-normalizing. Absolute normalization only matters for data/MC '
            'comparison plots. MC has ~2.5x more events than data after preselection, '
            'consistent with higher MC statistics for the 1994 period.'
        ),
        'subsample_10pct': n_10pct,
    }

    with open(P4B_OUT / "normalization_check.json", "w") as f:
        json.dump(output, f, indent=2, default=str)
    log.info("\nSaved normalization_check.json")


if __name__ == "__main__":
    main()
