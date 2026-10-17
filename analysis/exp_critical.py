# -*- coding: utf-8 -*-
"""exp_critical.py —— 三个“临界”的数值实验（本书新增，可复算）。

实验一：临界分支过程（Galton–Watson）的雪崩规模分布。
        临界（m=1）时理论幂律指数 3/2；偏离临界（m≠1）时出现指数截断。
        *拟合注意*：对数分箱后每箱计数 ∝ s·n(s)，故直接拟合 log(计数) 得到的是 α+1；
        本脚本已除以箱宽，再做拟合，避免把 -1.5 误读成 -0.5。
实验二：临界慢化（AR(1)）：恢复时间 τ=1/(1-a)，方差放大 1/(1-a²)；
        并给出一个“坏消息”：预警信号变强，但不告诉你什么时候。
实验三：二维方格点渗流（site percolation）：连通（跨越）概率在 p_c≈0.5927 附近陡升。

输出：data/exp_critical.json
"""
import json
import os

import numpy as np
from scipy import ndimage
from scipy.signal import lfilter

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")
os.makedirs(DATA, exist_ok=True)
SEED = 424242
rng = np.random.default_rng(SEED)
out = {"seed": SEED}

# ---------------------------------------------------------------- 实验一
def avalanche_sizes(m, n=200000, cutoff=20000):
    """集合式（ensemble）分支过程：一次迭代推进所有雪崩，避免逐个体循环。

    每个雪崩维护一个 frontier（当前代个体数）；每代用一次 Poisson 抽样生成下一代，
    因此总调用次数 ≈ 最大代数（~10^2），而不是总后代数（可达 10^6）。
    """
    size = np.zeros(n, dtype=np.int64)
    frontier = np.ones(n, dtype=np.int64)
    active = frontier > 0
    while active.any():
        size[active] += frontier[active]
        frontier[active] = rng.poisson(m * frontier[active])
        frontier[size >= cutoff] = 0
        active = frontier > 0
    return np.minimum(size, cutoff)


def fit_density(sizes, lo=20, hi=800, bins=14):
    """对数分箱 → 除以箱宽 → 拟合 log 密度 vs log s，得到幂律指数 α（n(s)∝s^-α）。"""
    x = sizes[(sizes >= lo) & (sizes <= hi)]
    if len(x) < 100:
        return None, None
    edges = np.geomspace(lo, hi, bins)
    h, _ = np.histogram(x, bins=edges)
    widths = np.diff(edges)
    dens = h / widths
    centers = np.sqrt(edges[:-1] * edges[1:])
    ok = dens > 0
    alpha = -float(np.polyfit(np.log(centers[ok]), np.log(dens[ok]), 1)[0])
    return round(alpha, 3), {
        "centers": [round(float(c), 2) for c in centers[ok]],
        "density": [float(round(d, 3)) for d in dens[ok]],
    }


av = {}
for m in (0.9, 1.0, 1.05):
    s = avalanche_sizes(m)
    lo, hi = {0.9: (15, 120), 1.0: (50, 3000), 1.05: (50, 3000)}[m]
    alpha, hist = fit_density(s, lo=lo, hi=hi)
    frac_cut = float((s >= 20000).mean())
    av[str(m)] = dict(mean_size=round(float(s.mean()), 2), max_size=int(s.max()),
                      alpha=alpha, fit_window=[lo, hi],
                      censored_fraction=round(frac_cut, 4), hist=hist)
    print("avalanche m=%.1f mean=%.2f max=%d alpha=%s censored=%.3f"
          % (m, s.mean(), s.max(), alpha, frac_cut))
out["avalanche"] = av

# ---------------------------------------------------------------- 实验二
def slack(a, steps=300000, burn=20000):
    noise = rng.normal(size=steps)
    x = lfilter([1.0], [1.0, -a], noise)[burn:]
    v = float(x.var())
    xc = x - x.mean()
    ac = np.correlate(xc, xc, mode="full")[len(xc) - 1:]
    ac /= ac[0]
    idx = np.where(ac < np.exp(-1))[0]
    tau = int(idx[0]) if len(idx) else len(ac)
    return tau, v, [round(float(v_), 4) for v_ in ac[:30]]


sl = {}
for a in (0.90, 0.95, 0.99, 0.995):
    tau, v, ac = slack(a)
    sl[str(a)] = dict(tau=tau, var=round(v, 3), var_theory=round(1 / (1 - a * a), 3),
                      tau_theory=round(1 / (1 - a), 2), ac=ac)
    print("AR a=%.3f tau=%d (th %.1f) var=%.2f (th %.2f)"
          % (a, tau, 1 / (1 - a), v, 1 / (1 - a * a)))
out["slowing"] = sl

# ---------------------------------------------------------------- 实验三
def spanning(occ):
    lab, n = ndimage.label(occ)
    if n == 0:
        return False
    # 跨越：某个连通块同时触及左右，或同时触及上下
    left = set(lab[:, 0]) - {0}
    right = set(lab[:, -1]) - {0}
    top = set(lab[0, :]) - {0}
    bottom = set(lab[-1, :]) - {0}
    return bool((left & right) or (top & bottom))


def percolation(L=64, trials=200):
    ps = [round(0.50 + 0.01 * i, 2) for i in range(16)]
    res = []
    for p in ps:
        hits = sum(spanning(rng.random((L, L)) < p) for _ in range(trials))
        res.append(dict(p=p, P_span=round(hits / trials, 3)))
    return res

pc = percolation()
out["percolation"] = dict(L=64, trials=200, curve=pc)
for r in pc:
    print("percolation p=%.2f P_span=%.3f" % (r["p"], r["P_span"]))

json.dump(out, open(os.path.join(DATA, "exp_critical.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("wrote data/exp_critical.json")
