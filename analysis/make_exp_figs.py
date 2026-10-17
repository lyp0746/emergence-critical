# -*- coding: utf-8 -*-
"""make_exp_figs.py —— 把 exp_ising.json / exp_critical.json 画成系列版式的 SVG。

风格与本书其它插图一致：白底、微软雅黑、标题 22、副标题 14、轴色 #333。
所有坐标由数据直接映射，不做手工美化。
"""
import json
import math
import os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "assets", "svg")
INK, GRY = "#1a1a1a", "#666666"
BLU, GRN, ORG, RED, GLD, PNK = "#2f6db0", "#2e7d32", "#ef6c00", "#c62828", "#b8862f", "#8e5a9c"

ising = json.load(open(os.path.join(HERE, "data", "exp_ising.json"), encoding="utf-8"))
isum = json.load(open(os.path.join(HERE, "data", "exp_ising_summary.json"), encoding="utf-8"))
crit = json.load(open(os.path.join(HERE, "data", "exp_critical.json"), encoding="utf-8"))
TC = isum["tc_exact"]


def head(W, H, title, sub=None):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'font-family="Microsoft YaHei, PingFang SC, SimHei, sans-serif">',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<text x="{W/2:.0f}" y="38" text-anchor="middle" font-size="22" font-weight="bold" fill="{INK}">{title}</text>']
    if sub:
        s.append(f'<text x="{W/2:.0f}" y="62" text-anchor="middle" font-size="14" fill="{GRY}">{sub}</text>')
    return s


def txt(x, y, t, size=13, fill=INK, anchor="middle", weight="normal"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}" fill="{fill}" '
            f'font-weight="{weight}">{t}</text>')


def axis(x0, y0, w, h, xlabel, ylabel):
    return [f'<line x1="{x0}" y1="{y0}" x2="{x0+w}" y2="{y0}" stroke="#333" stroke-width="1.8"/>',
            f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0-h}" stroke="#333" stroke-width="1.8"/>',
            txt(x0 + w / 2, y0 + 40, xlabel, 13, GRY),
            f'<text x="{x0-46}" y="{y0-h/2}" text-anchor="middle" font-size="13" fill="{GRY}" '
            f'transform="rotate(-90 {x0-46} {y0-h/2})">{ylabel}</text>']


def save(name, parts):
    open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8").write("\n".join(parts + ["</svg>"]))
    print("wrote", name + ".svg")


# ---------------------------------------------------------------- 图 1：|m| 与 χ
def fig_mchi():
    W, H = 960, 520
    s = head(W, H, "二维 Ising 的数值解：磁化强度与磁化率在 T_c 附近同时“起身”",
             "Metropolis，L=16/24/32，热化 1500 次、每点 4000 次测量；竖线为精确解 T_c=2.26919")
    runs = ising["coarse"]
    Ts = sorted({r["T"] for r in runs})
    cols = {16: BLU, 24: GRN, 32: ORG}
    # 左：|m|
    x0, y0, w, h = 90, 400, 360, 290
    s += axis(x0, y0, w, h, "温度 T", "|m|")
    tmin, tmax = 1.6, 3.2
    for T in [1.6, 2.0, 2.4, 2.8, 3.2]:
        x = x0 + (T - tmin) / (tmax - tmin) * w
        s.append(f'<line x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y0+5}" stroke="#333"/>')
        s.append(txt(x, y0 + 20, f"{T:.1f}", 11, GRY))
    for v in (0, 0.5, 1.0):
        s.append(f'<line x1="{x0-5}" y1="{y0-v*h:.1f}" x2="{x0}" y2="{y0-v*h:.1f}" stroke="#333"/>')
        s.append(txt(x0 - 10, y0 - v * h + 4, f"{v:.1f}", 11, GRY, "end"))
    for j, L in enumerate((16, 24, 32)):
        pts = [(r["T"], r["m"]) for r in runs if r["L"] == L]
        d = " ".join(("M" if i == 0 else "L") + f"{x0+(t-tmin)/(tmax-tmin)*w:.1f},{y0-m*h:.1f}"
                     for i, (t, m) in enumerate(pts))
        s.append(f'<path d="{d}" fill="none" stroke="{cols[L]}" stroke-width="2.2"/>')
        s.append(f'<line x1="{x0+14}" y1="{y0-h+16+j*16:.1f}" x2="{x0+40}" y2="{y0-h+16+j*16:.1f}" stroke="{cols[L]}" stroke-width="2.6"/>')
        s.append(txt(x0 + 46, y0 - h + 20 + j * 16, f"L={L}", 11, cols[L], "start"))
    xc = x0 + (TC - tmin) / (tmax - tmin) * w
    s.append(f'<line x1="{xc:.1f}" y1="{y0}" x2="{xc:.1f}" y2="{y0-h}" stroke="{GLD}" stroke-width="1.4" stroke-dasharray="6,5"/>')
    s.append(txt(xc + 6, y0 - h + 14, "T_c", 12, GLD, "start"))
    # 右：χ
    x1 = 570
    s += axis(x1, y0, w, 290, "温度 T", "磁化率 χ")
    ymax = max(r["chi"] for r in runs)
    for T in [1.6, 2.0, 2.4, 2.8, 3.2]:
        x = x1 + (T - tmin) / (tmax - tmin) * w
        s.append(f'<line x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y0+5}" stroke="#333"/>')
        s.append(txt(x, y0 + 20, f"{T:.1f}", 11, GRY))
    for v in (0, 10, 20):
        if v <= ymax:
            s.append(f'<line x1="{x1-5}" y1="{y0-v/ymax*290:.1f}" x2="{x1}" y2="{y0-v/ymax*290:.1f}" stroke="#333"/>')
            s.append(txt(x1 - 10, y0 - v / ymax * 290 + 4, f"{v}", 11, GRY, "end"))
    for j, L in enumerate((16, 24, 32)):
        pts = [(r["T"], r["chi"]) for r in runs if r["L"] == L]
        d = " ".join(("M" if i == 0 else "L") + f"{x1+(t-tmin)/(tmax-tmin)*w:.1f},{y0-v/ymax*290:.1f}"
                     for i, (t, v) in enumerate(pts))
        s.append(f'<path d="{d}" fill="none" stroke="{cols[L]}" stroke-width="2.2"/>')
        pk = max(pts, key=lambda p: p[1])
        s.append(f'<circle cx="{x1+(pk[0]-tmin)/(tmax-tmin)*w:.1f}" cy="{y0-pk[1]/ymax*290:.1f}" r="4" fill="{cols[L]}"/>')
        s.append(f'<line x1="{x1+14}" y1="{y0-290+16+j*16:.1f}" x2="{x1+40}" y2="{y0-290+16+j*16:.1f}" stroke="{cols[L]}" stroke-width="2.6"/>')
        s.append(txt(x1 + 46, y0 - 290 + 20 + j * 16, f"L={L}（峰 {pk[1]:.1f}）", 11, cols[L], "start"))
    xc2 = x1 + (TC - tmin) / (tmax - tmin) * w
    s.append(f'<line x1="{xc2:.1f}" y1="{y0}" x2="{xc2:.1f}" y2="{y0-290}" stroke="{GLD}" stroke-width="1.4" stroke-dasharray="6,5"/>')
    s.append(txt(xc2 + 6, y0 - 290 + 14, "T_c", 12, GLD, "start"))
    s.append(txt(W / 2, H - 14, "有限尺寸把“尖峰”抹平：L 越大，峰越高、越靠近 T_c——这正是有限尺度标度的入口。", 12, GRY))
    save("fig-exp-ising", s)


# ---------------------------------------------------------------- 图 2：雪崩分布
def fig_avalanche():
    W, H = 900, 520
    s = head(W, H, "临界雪崩：只有“刚刚好”的系统才有幂律",
             "临界分支过程（m=1）的规模分布斜率 ≈ 3/2；偏离临界，尾巴被截断（曲线在 s=50 处归一）")
    x0, y0, w, h = 110, 400, 690, 300
    s += axis(x0, y0, w, h, "雪崩规模 s（对数轴）", "归一化后的密度 n(s)（对数轴）")
    data = crit["avalanche"]
    cols = {"0.9": GRN, "1.0": RED, "1.05": ORG}
    lxmin, lxmax = 1.15, 3.45      # log10(s)
    lymin, lymax = -3.4, 0.35      # log10(density)
    fx = lambda v: x0 + (v - lxmin) / (lxmax - lxmin) * w
    fy = lambda v: y0 - (v - lymin) / (lymax - lymin) * h
    for sv in (10, 100, 1000):
        xv = math.log10(sv)
        s.append(f'<line x1="{fx(xv):.1f}" y1="{y0}" x2="{fx(xv):.1f}" y2="{y0+5}" stroke="#333"/>')
        s.append(txt(fx(xv), y0 + 20, str(sv), 12, GRY))
    for dv in (1, 0.1, 0.01, 0.001):
        yv = math.log10(dv)
        s.append(f'<line x1="{x0-5}" y1="{fy(yv):.1f}" x2="{x0}" y2="{fy(yv):.1f}" stroke="#333"/>')
        s.append(txt(x0 - 10, fy(yv) + 4, f"{dv:g}", 12, GRY, "end"))

    def anchor_interp(cs, ds, s0=50.0):
        for i in range(len(cs) - 1):
            if cs[i] <= s0 <= cs[i + 1]:
                t = (math.log(s0) - math.log(cs[i])) / (math.log(cs[i + 1]) - math.log(cs[i]))
                return math.exp(math.log(ds[i]) + t * (math.log(ds[i + 1]) - math.log(ds[i])))
        return ds[0]

    label_y = {}
    for k, d in data.items():
        cs, ds = d["hist"]["centers"], d["hist"]["density"]
        a0 = anchor_interp(cs, ds)
        pts = [(math.log10(c), math.log10(v / a0)) for c, v in zip(cs, ds) if v > 0]
        dd = " ".join(("M" if i == 0 else "L") + f"{fx(px):.1f},{fy(py):.1f}" for i, (px, py) in enumerate(pts))
        s.append(f'<path d="{dd}" fill="none" stroke="{cols[k]}" stroke-width="2.6"/>')
        # 标签放在右端，避免相互遮挡
        ex, ey = pts[-1]
        s.append(txt(fx(ex) + 6, fy(ey) - 8, f"m={k}", 12, cols[k], "start", "bold"))

    # 参考斜率 −3/2（穿过 s=50, y=1）
    xs = [math.log10(50), math.log10(600)]
    ys = [0.0, -1.5 * (math.log10(600) - math.log10(50))]
    s.append(f'<line x1="{fx(xs[0]):.1f}" y1="{fy(ys[0]):.1f}" x2="{fx(xs[1]):.1f}" y2="{fy(ys[1]):.1f}" '
             f'stroke="{GRY}" stroke-width="1.8" stroke-dasharray="8,5"/>')
    s.append(txt(fx(xs[1]), fy(ys[1]) + 20, "参考斜率 −3/2", 12, GRY, "end"))

    s.append(txt(W / 2, H - 42, "实测幂律指数：m=1.0 → α=1.495（拟合窗口 50–3000）；m=0.9 → 1.786（15–120）；m=1.05 → 2.146（50–3000，9.3% 截断）。", 12, GRY))
    s.append(txt(W / 2, H - 20, "偏离临界时，“幂律”不是消失了，而是被一个指数截断接管——这正是把临界当“开关”会犯的错。", 12, GRY))
    save("fig-exp-avalanche", s)


# ---------------------------------------------------------------- 图 3：渗流
def fig_percolation():
    W, H = 860, 470
    s = head(W, H, "连通性阈值：p 只差 0.05，全局连通的概率从 6% 跳到 81%",
             "二维方格点渗流，L=64，每个 p 做 200 次独立实现；“跨越”=同一连通块触及对边")
    x0, y0, w, h = 100, 380, 660, 270
    s += axis(x0, y0, w, h, "占据概率 p", "出现跨越连通块的概率")
    pts = [(r["p"], r["P_span"]) for r in crit["percolation"]["curve"]]
    xmin, xmax = 0.50, 0.65
    fx = lambda v: x0 + (v - xmin) / (xmax - xmin) * w
    fy = lambda v: y0 - v * h
    for p in (0.50, 0.55, 0.60, 0.65):
        s.append(f'<line x1="{fx(p):.1f}" y1="{y0}" x2="{fx(p):.1f}" y2="{y0+5}" stroke="#333"/>')
        s.append(txt(fx(p), y0 + 20, f"{p:.2f}", 11, GRY))
    for v in (0, 0.5, 1.0):
        s.append(f'<line x1="{x0-5}" y1="{fy(v):.1f}" x2="{x0}" y2="{fy(v):.1f}" stroke="#333"/>')
        s.append(txt(x0 - 10, fy(v) + 4, f"{v:.1f}", 11, GRY, "end"))
    d = " ".join(("M" if i == 0 else "L") + f"{fx(p):.1f},{fy(v):.1f}" for i, (p, v) in enumerate(pts))
    s.append(f'<path d="{d}" fill="none" stroke="{BLU}" stroke-width="2.6"/>')
    for p, v in pts:
        s.append(f'<circle cx="{fx(p):.1f}" cy="{fy(v):.1f}" r="3.4" fill="{BLU}"/>')
    xc = fx(0.5927)
    s.append(f'<line x1="{xc:.1f}" y1="{y0}" x2="{xc:.1f}" y2="{y0-h}" stroke="{RED}" stroke-width="1.5" stroke-dasharray="6,5"/>')
    s.append(txt(xc + 6, y0 - h + 12, "p_c = 0.5927", 12, RED, "start"))
    s.append(txt(W / 2, H - 16, "“阈值”不是比喻：它是一条可以被数出来的线，而且只在这个尺度上才显得陡。", 12, GRY))
    save("fig-exp-percolation", s)


fig_mchi()
fig_avalanche()
fig_percolation()


# ---------------------------------------------------------------- 图 4：FSS 坍缩
def fig_fss():
    W, H = 900, 520
    s = head(W, H, "有限尺度坍缩：用对指数，三条曲线会叠成一条",
             "左：精确指数（β/ν=0.125, ν=1）；右：平均场指数（0.25, 0.5）。同一批数据，两种“折叠”")
    fine = [r for r in ising["fine"]]
    Ls = sorted({r["L"] for r in fine})
    cols = {24: BLU, 32: GRN, 48: ORG}
    TC = isum["tc_exact"]

    def panel(x0, beta_nu, nu, title):
        y0, w, h = 400, 340, 290
        s = axis(x0, y0, w, h, "(T−T_c)·L^(1/ν)", "|m|·L^(β/ν)")
        xs, ys = [], []
        for r in fine:
            xs.append((r["T"] - TC) * r["L"] ** (1.0 / nu))
            ys.append(r["m"] * r["L"] ** beta_nu)
        xmin, xmax = min(xs), max(xs)
        ymin, ymax = min(ys), max(ys)
        pad = 0.05
        xmin -= pad * (xmax - xmin); xmax += pad * (xmax - xmin)
        ymin -= pad * (ymax - ymin); ymax += pad * (ymax - ymin)
        fx = lambda v: x0 + (v - xmin) / (xmax - xmin) * w
        fy = lambda v: y0 - (v - ymin) / (ymax - ymin) * h
        for L in Ls:
            pts = sorted([((r["T"] - TC) * L ** (1.0 / nu), r["m"] * L ** beta_nu)
                          for r in fine if r["L"] == L])
            d = " ".join(("M" if i == 0 else "L") + f"{fx(a):.1f},{fy(b):.1f}" for i, (a, b) in enumerate(pts))
            s.append(f'<path d="{d}" fill="none" stroke="{cols[L]}" stroke-width="2.2"/>')
            s.append(f'<circle cx="{fx(pts[len(pts)//2][0]):.1f}" cy="{fy(pts[len(pts)//2][1]):.1f}" r="3" fill="{cols[L]}"/>')
        for j, L in enumerate(Ls):
            s.append(f'<line x1="{x0+10}" y1="{y0-h+14+j*15:.1f}" x2="{x0+32}" y2="{y0-h+14+j*15:.1f}" stroke="{cols[L]}" stroke-width="2.4"/>')
            s.append(txt(x0 + 38, y0 - h + 18 + j * 15, f"L={L}", 11, cols[L], "start"))
        s.append(txt(x0 + w / 2, y0 + 62, title, 13, INK))
        return s

    s += panel(90, 0.125, 1.0, "精确指数：残差 5.1%")
    s += panel(520, 0.25, 0.5, "平均场指数：残差 5.9%")
    s.append(txt(W / 2, H - 18, "两条都不完美，但“对”的那条叠得更紧——而差距小到只凭肉眼很难判定，这正是 L 不够大时的困境。", 12, GRY))
    save("fig-exp-fss", s)


fig_fss()
