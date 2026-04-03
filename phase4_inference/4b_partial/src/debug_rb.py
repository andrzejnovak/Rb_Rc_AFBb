"""Debug R_b extraction on 10% data."""
import numpy as np
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
P4A_OUT = HERE.parents[1] / "4a_expected" / "outputs"

with open(P4A_OUT / "mc_calibration.json") as f:
    cal = json.load(f)

with open(P4A_OUT / "correlation_results.json") as f:
    corr = json.load(f)

wp = cal["full_mc_calibration"]["10.0"]
eps_c = wp["eps_c"]
eps_uds = wp["eps_uds"]

G_BB, G_CC = 0.00251, 0.0296
eps_uds_eff = eps_uds + G_BB * 0.5 + G_CC * 0.3 * eps_c
print(f"eps_c={eps_c:.4f}, eps_uds_eff={eps_uds_eff:.5f}")

for item in corr["mc_vs_wp"]:
    if item["threshold"] in [5.0, 7.0, 8.0, 10.0]:
        print(f"C_b(MC,WP={item['threshold']}) = {item['C']:.4f}")

for item in corr["data_vs_wp"]:
    if item["threshold"] in [5.0, 7.0, 8.0, 10.0]:
        print(f"C_b(Data,WP={item['threshold']}) = {item['C']:.4f}")

# Data vs MC f_s, f_d
print("\nData 10%: f_s=0.17150, f_d=0.04471")
print("MC full:  f_s=", wp["f_s"], "f_d=", wp["f_d"])

# Try extraction with different C_b
R_C_SM = 0.17223
R_B_SM = 0.21578

f_s_data = 0.17150
f_d_data = 0.04471

print("\n--- R_b extraction attempts ---")
for C_b in [1.01, 1.10, 1.179, 1.30, 1.40, 1.52]:
    a = f_s_data - eps_c * R_C_SM - eps_uds_eff * (1.0 - R_C_SM)
    bg_d = 1.0 * eps_c**2 * R_C_SM + 1.0 * eps_uds_eff**2 * (1.0 - R_C_SM)
    rhs_coeff = f_d_data - bg_d - 2 * C_b * a * eps_uds_eff
    quad_a = (C_b - 1.0) * eps_uds_eff**2
    quad_b_val = -rhs_coeff
    quad_c = C_b * a**2
    disc = quad_b_val**2 - 4 * quad_a * quad_c
    print(f"C_b={C_b:.3f}: a={a:.5f}, quad_a={quad_a:.8f}, quad_b={quad_b_val:.8f}, quad_c={quad_c:.8f}, disc={disc:.8f}")
    if disc >= 0:
        sqrt_disc = np.sqrt(disc)
        r1 = (-quad_b_val + sqrt_disc) / (2 * quad_a)
        r2 = (-quad_b_val - sqrt_disc) / (2 * quad_a)
        candidates = [r for r in [r1, r2] if 0 < r < 1]
        best = min(candidates, key=lambda x: abs(x - R_B_SM)) if candidates else None
        eps_b = a / best + eps_uds_eff if best else None
        print(f"  r1={r1:.4f}, r2={r2:.4f}, R_b={best}, eps_b={eps_b}")
    else:
        print(f"  NEGATIVE discriminant")

# The issue: use per-WP C_b, not the WP=5.0 reference
print("\n--- Using per-WP C_b ---")
for item in corr["mc_vs_wp"]:
    thr = item["threshold"]
    C_b = item["C"]
    thr_str = str(float(thr))
    if thr_str not in cal["full_mc_calibration"]:
        continue
    cal_wp = cal["full_mc_calibration"][thr_str]
    e_c = cal_wp["eps_c"]
    e_u = cal_wp["eps_uds"]
    e_u_eff = e_u + G_BB * 0.5 + G_CC * 0.3 * e_c

    # Use MC f_s, f_d (to verify Phase 4a result)
    a = cal_wp["f_s"] - e_c * R_C_SM - e_u_eff * (1.0 - R_C_SM)
    bg_d = 1.0 * e_c**2 * R_C_SM + 1.0 * e_u_eff**2 * (1.0 - R_C_SM)
    rhs_coeff = cal_wp["f_d"] - bg_d - 2 * C_b * a * e_u_eff
    qa = (C_b - 1.0) * e_u_eff**2
    qb = -rhs_coeff
    qc = C_b * a**2
    disc = qb**2 - 4 * qa * qc
    result = "neg disc" if disc < 0 else f"disc={disc:.8f}"
    if disc >= 0:
        sqrt_d = np.sqrt(disc)
        r1 = (-qb + sqrt_d) / (2 * qa)
        r2 = (-qb - sqrt_d) / (2 * qa)
        cands = [r for r in [r1, r2] if 0 < r < 1]
        best = min(cands, key=lambda x: abs(x - R_B_SM)) if cands else None
        result += f", R_b={best}"
    print(f"WP={thr}: C_b={C_b:.4f}, {result}")
