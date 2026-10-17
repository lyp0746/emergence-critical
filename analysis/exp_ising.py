# -*- coding: utf-8 -*-
"""exp_ising.py —— 二维方晶格 Ising 的 Metropolis 模拟（本书新增数值实验，可复算）。

设计原则（写进正文的纪律）：
  1) 所有参数、种子、迭代数写在这里，并被写入 data/exp_ising.json；
  2) 只在“已知精确解”的地方作比较，不把模拟值当成理论；
  3) 估计临界指数时只在 T_c 与 χ 峰附近取值，并报告有限尺度偏差。

对照基准（Onsager 1944；精确指数）：
  T_c = 2/ln(1+√2) ≈ 2.26919；β = 1/8；γ = 7/4；ν = 1。
平均场（Landau）：T_c 由方程给出、β = 1/2、γ = 1、ν = 1/2。
"""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "assets", "svg")
os.makedirs(DATA, exist_ok=True)

SEED = 20261016
TC = 2.0 / math.log(1.0 + math.sqrt(2.0))          # 2.26919
COARSE_T = [1.6 + 0.1 * i for i in range(17)]       # 1.6 ~ 3.2（画相图用）
FINE_T = [round(2.20 + 0.02 * i, 3) for i in range(9)]  # 2.20 ~ 2.36（估计指数用）
COARSE_L = [16, 24, 32]
FINE_L = [24, 32, 48]
THERM_C, MEAS_C = 1500, 4000
THERM_F, MEAS_F = 3000, 10000


def sweep(s, T, rng):
    L = s.shape[0]
    idx = np.arange(L)
    for color in (0, 1):
        mask = ((idx[:, None] + idx[None, :]) % 2) == color
        nb = (np.roll(s, 1, 0) + np.roll(s, -1, 0) +
              np.roll(s, 1, 1) + np.roll(s, -1, 1))
        dE = 2.0 * s * nb
        acc = (dE <= 0) | (rng.random(s.shape) < np.exp(-np.maximum(dE, 0) / T))
        s[mask & acc] *= -1


def run(L, T, therm, meas, seed):
    rng = np.random.default_rng(seed)
    s = rng.choice([-1, 1], size=(L, L)).astype(np.int8)
    for _ in range(therm):
        sweep(s, T, rng)
    m1 = m2 = m4 = 0.0
    for _ in range(meas):
        sweep(s, T, rng)
        m = abs(float(s.mean()))
        m1 += m
        m2 += m * m
        m4 += m ** 4
    m1, m2, m4 = m1 / meas, m2 / meas, m4 / meas
    N = L * L
    return dict(T=T, L=L, m=m1, m2=m2,
                chi=N / T * (m2 - m1 * m1),
                U=1.0 - m4 / (3.0 * m2 * m2))


print("== coarse scan ==")
coarse = []
for L in COARSE_L:
    for i, T in enumerate(COARSE_T):
        r = run(L, T, THERM_C, MEAS_C, SEED + 1000 * L + i)
        coarse.append(r)
        print("  L=%2d T=%.2f |m|=%.4f chi=%7.2f U=%.4f" % (L, T, r["m"], r["chi"], r["U"]))

print("== fine scan near Tc ==")
fine = []
for L in FINE_L:
    for i, T in enumerate(FINE_T):
        r = run(L, T, THERM_F, MEAS_F, SEED + 7000 + 1000 * L + i)
        fine.append(r)
        print("  L=%2d T=%.3f |m|=%.4f chi=%7.2f U=%.4f" % (L, T, r["m"], r["chi"], r["U"]))
json.dump(dict(seed=SEED, tc_exact=round(TC, 5), coarse=coarse, fine=fine),
          open(os.path.join(DATA, "exp_ising.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

# ---------------- 估计量 ----------------
def binder_cross(rows, L1, L2):
    a = [r for r in rows if r["L"] == L1]
    b = [r for r in rows if r["L"] == L2]
    for i in range(len(a) - 1):
        d1, d2 = a[i]["U"] - b[i]["U"], a[i + 1]["U"] - b[i + 1]["U"]
        if d1 == 0:
            return a[i]["T"]
        if d1 * d2 < 0:
            return round(a[i]["T"] + (a[i + 1]["T"] - a[i]["T"]) * abs(d1) / (abs(d1) + abs(d2)), 4)
    return None

tc_fine_24_32 = binder_cross(fine, 24, 32)
tc_fine_32_48 = binder_cross(fine, 32, 48)
tc_coarse_16_24 = binder_cross(coarse, 16, 24)


def m_at(rows, L, T):
    """在 T 处对 log|m| 做线性插值（T 落在细扫网格内）。"""
    pts = sorted([r for r in rows if r["L"] == L], key=lambda r: r["T"])
    for i in range(len(pts) - 1):
        if pts[i]["T"] <= T <= pts[i + 1]["T"]:
            t0, t1 = pts[i]["T"], pts[i + 1]["T"]
            y0, y1 = math.log(pts[i]["m"]), math.log(pts[i + 1]["m"])
            return math.exp(y0 + (y1 - y0) * (T - t0) / (t1 - t0))
    return None


def slope(xs, ys):
    return float(np.polyfit(np.log(xs), np.log(ys), 1)[0])


m_tc_vals = {L: m_at(fine, L, TC) for L in FINE_L}
m_tc = [dict(L=L, m=m_tc_vals[L]) for L in FINE_L if m_tc_vals[L]]
beta_nu = -slope([r["L"] for r in m_tc], [r["m"] for r in m_tc]) if len(m_tc) == len(FINE_L) else None

peak = {}
for L in FINE_L:
    pk = max([r for r in fine if r["L"] == L], key=lambda r: r["chi"])
    peak[L] = pk
gamma_nu = slope(list(peak), [peak[L]["chi"] for L in peak])

# ν：由 Tc(L) = Tc + a L^(-1/ν)，用两个交叉点位移近似
# ΔT(16,24) 与 ΔT(24,32) 的比值 = ((1/16)^(1/ν) - (1/24)^(1/ν)) / ((1/24)^(1/ν) - (1/32)^(1/ν))
def solve_nu(tc1, tc2, Tinf=TC):
    num = tc1 - Tinf
    den = tc2 - Tinf
    if num <= 0 or den <= 0:
        return None
    f = lambda nu: ((16.0 ** (-1 / nu) - 24.0 ** (-1 / nu)) /
                    (24.0 ** (-1 / nu) - 32.0 ** (-1 / nu))) - num / den
    lo, hi = 0.3, 3.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return round(0.5 * (lo + hi), 3)

nu_est = solve_nu(tc_coarse_16_24, tc_fine_24_32) if (tc_coarse_16_24 and tc_fine_24_32) else None

# ---- 有限尺度坍缩：用精确指数 vs 平均场指数，比较坍缩残差
def collapse_residual(beta_nu, nu, rows=None):
    """归一化后的曲线间离散度：对每个 T 把 m L^{β/ν} 标准化，再看同一标度变量下的分散程度。"""
    xs, ys = [], []
    for r in (fine if rows is None else rows):
        x = (r["T"] - TC) * r["L"] ** (1.0 / nu)
        y = r["m"] * r["L"] ** beta_nu
        xs.append(x)
        ys.append(y)
    xs = np.array(xs)
    ys = np.array(ys)
    # 以 (T-Tc)L^{1/ν} 分箱，箱内相对标准差
    order = np.argsort(xs)
    xs, ys = xs[order], ys[order]
    bins = np.linspace(xs.min(), xs.max(), 9)
    res = []
    for i in range(len(bins) - 1):
        m = (xs >= bins[i]) & (xs < bins[i + 1])
        if m.sum() >= 3:
            v = ys[m]
            res.append(float(np.std(v) / max(abs(np.mean(v)), 1e-12)))
    return round(float(np.mean(res)), 4) if res else None


res_exact = collapse_residual(0.125, 1.0)
res_mf = collapse_residual(0.25, 0.5)

# 按“可观测尺度”拆开：只用 L=24；用 24+32；用 24+32+48
by_scale = {}
for label, Ls in (("L24", [24]), ("L24_32", [24, 32]), ("L24_32_48", [24, 32, 48])):
    rows = [r for r in fine if r["L"] in Ls]
    by_scale[label] = dict(
        exact=collapse_residual(0.125, 1.0, rows),
        meanfield=collapse_residual(0.25, 0.5, rows),
    )

summary = dict(
    tc_exact=round(TC, 5),
    tc_binder_coarse_16_24=tc_coarse_16_24,
    tc_binder_fine_24_32=tc_fine_24_32,
    tc_binder_fine_32_48=tc_fine_32_48,
    beta_over_nu_measured=None if beta_nu is None else round(beta_nu, 4),
    beta_over_nu_exact=0.125,
    gamma_over_nu_measured=round(gamma_nu, 4),
    gamma_over_nu_exact=1.75,
    nu_measured=nu_est,
    nu_exact=1.0,
    chi_peak={str(L): [peak[L]["T"], round(peak[L]["chi"], 2)] for L in FINE_L},
    m_at_tc={str(r["L"]): round(r["m"], 4) for r in m_tc},
    collapse_residual_exact=res_exact, collapse_residual_meanfield=res_mf,
    collapse_by_scale=by_scale,
)
json.dump(summary, open(os.path.join(DATA, "exp_ising_summary.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\n== summary ==")
print(json.dumps(summary, ensure_ascii=False, indent=1))
