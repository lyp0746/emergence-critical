# -*- coding: utf-8 -*-
"""make_figures.py —《涌现的临界》插图（确定性生成）。"""
import math
import os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "assets", "svg")
INK = "#1a1a1a"; GRY = "#666"; BLU = "#2f6db0"; GRN = "#2e7d32"
ORG = "#ef6c00"; RED = "#c62828"; GLD = "#b8862f"; PNK = "#8e5a9c"
FONT = "Microsoft YaHei, PingFang SC, SimHei, sans-serif"


def head(w, h, title, sub=None):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{FONT}">',
         f'<rect width="{w}" height="{h}" fill="#ffffff"/>',
         f'<text x="{w/2:.0f}" y="38" text-anchor="middle" font-size="22" font-weight="bold" fill="{INK}">{title}</text>']
    if sub:
        s.append(f'<text x="{w/2:.0f}" y="62" text-anchor="middle" font-size="14" fill="{GRY}">{sub}</text>')
    return s


def txt(x, y, t, size=14, fill=INK, anchor="middle", weight="normal"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" fill="{fill}" font-weight="{weight}">{t}</text>'


def box(x, y, w, h, fill, stroke, rx=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>'


def save(name, parts):
    with open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8") as f:
        f.write("\n".join(parts + ["</svg>"]))
    print("wrote", name + ".svg")


def fig_order():
    W, H = 820, 500
    s = head(W, H, "序参量：什么在“变得有序”？", "η 在临界点从 0 跃变为非 0（或反之）")
    ox, oy, w, h = 110, 400, 620, 300
    s.append(f'<line x1="{ox}" y1="{oy}" x2="{ox+w}" y2="{oy}" stroke="#333" stroke-width="2"/>')
    s.append(f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="{oy-h}" stroke="#333" stroke-width="2"/>')
    s.append(f'<text x="{ox+w/2:.0f}" y="{oy+36}" text-anchor="middle" font-size="14">参数 T →</text>')
    s.append(f'<text x="{ox-58}" y="{oy-h/2:.0f}" text-anchor="middle" font-size="14" transform="rotate(-90 {ox-58} {oy-h/2:.0f})">序参量 η</text>')
    tc = ox + w * 0.55
    s.append(f'<line x1="{tc}" y1="{oy}" x2="{tc}" y2="{oy-h}" stroke="{GLD}" stroke-width="1.6" stroke-dasharray="7,5"/>')
    s.append(txt(tc, oy + 22, "T_c", 13, GLD, weight="bold"))
    # 阶跃
    s.append(f'<path d="M {ox} {oy} L {tc} {oy} L {tc} {oy-h*0.75} L {ox+w} {oy-h*0.75}" fill="none" stroke="{RED}" stroke-width="3.5"/>')
    s.append(txt(ox + 150, oy - 30, "无序相：η = 0", 14, GRY))
    s.append(txt(ox + 470, oy - h * 0.75 - 20, "有序相：η ≠ 0", 14, RED))
    s.append(txt(tc + 16, oy - h * 0.4, "跃变", 13, GLD, anchor="start"))
    save("fig-order-parameter", s)


def fig_symmetry():
    W, H = 820, 460
    s = head(W, H, "对称破缺：微观没变，宏观“选了一个方向”", "临界点前各向同性；临界点后集体对齐")
    # 左：无序
    cx1, cy1 = 230, 260
    s.append(txt(cx1, 110, "临界点前：无序（对称）", 16, BLU, weight="bold"))
    for i, ang in enumerate([0, 45, 90, 135, 180, 225, 270, 315]):
        a = math.radians(ang)
        x = cx1 + 70 * math.cos(a); y = cy1 + 70 * math.sin(a)
        s.append(f'<line x1="{cx1}" y1="{cy1}" x2="{x:.0f}" y2="{y:.0f}" stroke="{BLU}" stroke-width="2"/>')
        s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="{BLU}"/>')
    # 右：有序
    cx2 = 590
    s.append(txt(cx2, 110, "临界点后：对齐（破缺）", 16, RED, weight="bold"))
    for i in range(8):
        x = cx2 - 105 + i * 30
        s.append(f'<line x1="{x}" y1="{cy1+60}" x2="{x}" y2="{cy1-60}" stroke="{RED}" stroke-width="2"/>')
        s.append(f'<circle cx="{x}" cy="{cy1-60}" r="7" fill="{RED}"/>')
        s.append(f'<circle cx="{x}" cy="{cy1+60}" r="7" fill="{RED}"/>')
    s.append(txt(410, 420, "微观相互作用规则完全没变；变的只是“整体选了哪个方向”。", 13, GRY))
    save("fig-symmetry-breaking", s)


def fig_slowing():
    W, H = 820, 480
    s = head(W, H, "临界慢化：崩溃之前，系统会“变慢”", "恢复时间在临界点前发散——这是唯一“事前”可观测的预警")
    ox, oy, w, h = 110, 390, 620, 290
    s.append(f'<line x1="{ox}" y1="{oy}" x2="{ox+w}" y2="{oy}" stroke="#333" stroke-width="2"/>')
    s.append(f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="{oy-h}" stroke="#333" stroke-width="2"/>')
    s.append(f'<text x="{ox+w/2:.0f}" y="{oy+36}" text-anchor="middle" font-size="14">接近临界点的程度 T → T_c</text>')
    s.append(f'<text x="{ox-62}" y="{oy-h/2:.0f}" text-anchor="middle" font-size="14" transform="rotate(-90 {ox-62} {oy-h/2:.0f})">恢复时间 τ_rec</text>')
    tc = ox + w * 0.88
    s.append(f'<line x1="{tc}" y1="{oy}" x2="{tc}" y2="{oy-h}" stroke="{GLD}" stroke-width="1.6" stroke-dasharray="7,5"/>')
    s.append(txt(tc + 4, oy + 22, "T_c", 13, GLD, anchor="start", weight="bold"))
    pts = []
    for i in range(101):
        t = i / 100
        x = ox + w * t * 0.88
        # 1/(1-t) 形状，截断
        y = oy - min(h, 12 + 260 * (1 / (1.02 - t * 0.88) - 1) / 12)
        pts.append((x, max(oy - h, y)))
    s.append('<path d="M ' + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts) + '" fill="none" stroke="{RED}" stroke-width="3.2"/>'.replace("{RED}", RED))
    s.append(txt(ox + 120, oy - 40, "提前预警窗口", 14, GRN, weight="bold"))
    save("fig-critical-slowing", s)


def fig_universality():
    W, H = 820, 460
    s = head(W, H, "标度律与普适类：不同系统，同一组数字？", "把坐标换成标度变量后，不同系统的曲线“坍缩”到一条线上")
    ox, oy, w, h = 110, 380, 620, 280
    s.append(f'<line x1="{ox}" y1="{oy}" x2="{ox+w}" y2="{oy}" stroke="#333" stroke-width="2"/>')
    s.append(f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="{oy-h}" stroke="#333" stroke-width="2"/>')
    s.append(f'<text x="{ox+w/2:.0f}" y="{oy+36}" text-anchor="middle" font-size="14">标度变量 |T − T_c| / T_c →</text>')
    s.append(f'<text x="{ox-58}" y="{oy-h/2:.0f}" text-anchor="middle" font-size="14" transform="rotate(-90 {ox-58} {oy-h/2:.0f})">标度后的 η</text>')
    cols = [BLU, GRN, ORG, PNK]
    for k, col in enumerate(cols):
        pts = []
        for i in range(61):
            t = i / 60
            x = ox + 40 + t * 520
            y = oy - h * (1 - t) ** 0.5 * (0.92 + 0.03 * k)
            pts.append((x, y))
        s.append('<path d="M ' + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts) + f'" fill="none" stroke="{col}" stroke-width="2.4" opacity="0.85"/>')
    s.append(txt(660, 150, "四个不同系统", 13, GRY, anchor="start"))
    s.append(txt(660, 176, "→ 坍缩到一条线", 13, GRY, anchor="start"))
    save("fig-universality", s)


def fig_causal_emergence():
    W, H = 820, 480
    s = head(W, H, "因果涌现：为什么“宏观”有时比“微观”更好用？", "Φ = I_macro − I_micro，在某粗粒化尺度上达到峰值")
    ox, oy, w, h = 110, 390, 620, 290
    s.append(f'<line x1="{ox}" y1="{oy}" x2="{ox+w}" y2="{oy}" stroke="#333" stroke-width="2"/>')
    s.append(f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="{oy-h}" stroke="#333" stroke-width="2"/>')
    s.append(f'<text x="{ox+w/2:.0f}" y="{oy+36}" text-anchor="middle" font-size="14">粗粒化程度（细 → 粗）→</text>')
    s.append(f'<text x="{ox-58}" y="{oy-h/2:.0f}" text-anchor="middle" font-size="14" transform="rotate(-90 {ox-58} {oy-h/2:.0f})">有效信息 Φ</text>')
    pts = []
    for i in range(101):
        t = i / 100
        x = ox + t * w
        # 0 -> peak at 0.45 -> decline
        y = oy - h * (math.exp(-((t - 0.45) ** 2) / 0.05) * 0.85 + 0.05)
        pts.append(f"{x:.1f} {y:.1f}")
    s.append('<path d="M ' + " L ".join(pts) + f'" fill="none" stroke="{GLD}" stroke-width="3.2"/>')
    px = ox + 0.45 * w
    s.append(f'<line x1="{px:.0f}" y1="{oy}" x2="{px:.0f}" y2="{oy-h*0.9:.0f}" stroke="{GLD}" stroke-width="1.4" stroke-dasharray="6,5"/>')
    s.append(txt(px, oy - h * 0.9 - 10, "最优尺度", 14, GLD, weight="bold"))
    s.append(txt(ox + 80, oy - 40, "太细：噪声", 12, GRY))
    s.append(txt(ox + w - 90, oy - 40, "太粗：丢结构", 12, GRY))
    save("fig-causal-emergence", s)


def fig_honesty():
    W, H = 760, 480
    s = head(W, H, "一个反直觉的规律：形式化越高，越容易“过度自信”", "H（诚实性）与 F（形式化程度）大致负相关")
    ox, oy, w, h = 100, 390, 580, 290
    s.append(f'<line x1="{ox}" y1="{oy}" x2="{ox+w}" y2="{oy}" stroke="#333" stroke-width="2"/>')
    s.append(f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="{oy-h}" stroke="#333" stroke-width="2"/>')
    s.append(f'<text x="{ox+w/2:.0f}" y="{oy+36}" text-anchor="middle" font-size="14">形式化程度 F →</text>')
    s.append(f'<text x="{ox-56}" y="{oy-h/2:.0f}" text-anchor="middle" font-size="14" transform="rotate(-90 {ox-56} {oy-h/2:.0f})">诚实性 H</text>')
    data = [("区分的语法", 70, 40, BLU), ("选择的代价", 60, 80, GRN),
            ("错位的时间", 45, 90, ORG), ("遗忘的边界", 40, 75, PNK),
            ("诠释的权衡", 25, 95, RED)]
    for name, f, hh, col in data:
        x = ox + w * f / 100
        y = oy - h * hh / 100
        s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="{col}"/>')
        s.append(txt(x + 10, y - 8, name, 12, col, anchor="start"))
    save("fig-honesty-formality", s)


def fig_five_samples():
    W, H = 820, 500
    s = head(W, H, "五本书，五个位置：从“可以算”到“只能讲”", "横轴：系统复杂性；纵轴：形式化程度")
    ox, oy, w, h = 110, 400, 620, 300
    s.append(f'<line x1="{ox}" y1="{oy}" x2="{ox+w}" y2="{oy}" stroke="#333" stroke-width="2"/>')
    s.append(f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="{oy-h}" stroke="#333" stroke-width="2"/>')
    s.append(f'<text x="{ox+w/2:.0f}" y="{oy+34}" text-anchor="middle" font-size="14">系统复杂性（物理/数学 → 社会/历史）→</text>')
    s.append(f'<text x="{ox-56}" y="{oy-h/2:.0f}" text-anchor="middle" font-size="14" transform="rotate(-90 {ox-56} {oy-h/2:.0f})">形式化程度</text>')
    data = [("区分的语法", 0.12, 0.70, BLU), ("选择的代价", 0.50, 0.60, GRN),
            ("错位的时间", 0.42, 0.45, ORG), ("遗忘的边界", 0.60, 0.40, PNK),
            ("诠释的权衡", 0.88, 0.25, RED)]
    for name, xr, yr, col in data:
        x = ox + w * xr; y = oy - h * yr
        s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="8" fill="{col}"/>')
        s.append(txt(x + 12, y - 8, name, 13, col, anchor="start", weight="bold"))
    s.append(txt(ox + 160, oy - h * 0.82, "可算，但远离现实", 12, GRY))
    s.append(txt(ox + 470, oy - 20, "真实，但难形式化", 12, GRY))
    save("fig-five-samples", s)


def main():
    os.makedirs(OUT, exist_ok=True)
    for f in [fig_five_samples, fig_order, fig_symmetry, fig_slowing,
              fig_universality, fig_causal_emergence, fig_honesty,
              fig_horizon, fig_five_step]:
        f()
    print("done")



def fig_horizon():
    W, H = 860, 500
    s = head(W, H, "形式化的地平线：复杂度越高，能形式化的部分越少", "F(C) = F_min + (F_0 − F_min)·exp(−λC)（模型，非定律）")
    ox, oy, w, h = 110, 410, 640, 310
    s.append(f'<line x1="{ox}" y1="{oy}" x2="{ox+w}" y2="{oy}" stroke="#333" stroke-width="2"/>')
    s.append(f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="{oy-h}" stroke="#333" stroke-width="2"/>')
    s.append(f'<text x="{ox+w/2:.0f}" y="{oy+36}" text-anchor="middle" font-size="14">系统复杂度 C →</text>')
    s.append(f'<text x="{ox-56}" y="{oy-h/2:.0f}" text-anchor="middle" font-size="14" transform="rotate(-90 {ox-56} {oy-h/2:.0f})">可形式化程度 F</text>')
    import math as _m
    pts=[]
    for i in range(101):
        t=i/100
        F=0.2+0.75*_m.exp(-3.2*t)
        x=ox+t*w; y=oy-h*F
        pts.append(f"{x:.1f} {y:.1f}")
    s.append('<path d="M '+ " L ".join(pts) + f'" fill="none" stroke="{GLD}" stroke-width="3.2"/>')
    # mark five books
    marks=[("区分的语法",0.08,0.70,BLU),("选择的代价",0.45,0.42,GRN),
           ("错位的时间",0.62,0.32,ORG),("遗忘的边界",0.72,0.28,PNK),("诠释的权衡",0.92,0.21,RED)]
    for name,xr,F,col in marks:
        x=ox+xr*w; y=oy-h*F
        s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="{col}"/>')
        s.append(txt(x+10,y-8,name,12,col,anchor="start"))
    s.append(txt(ox+w-80, oy-h*0.12, "F_min", 12, GRY))
    save("fig-formalization-horizon", s)


def fig_five_step():
    W, H = 940, 300
    s = head(W, H, "五步诊断流程：拿到一个陌生系统，怎么判断它刚经历了一次质变", None)
    steps=[("1 找序参量","什么量从≈0变非0"),("2 定临界点","一阶跳变还是二阶"),("3 看预警","恢复是否变慢"),("4 算有效信息","宏观是否更好用"),("5 标等级","三中→强，一中→弱")]
    cw, gap = 160, 20
    x0 = (W - (cw*5+gap*4))/2
    for i,(k,v) in enumerate(steps):
        x=x0+i*(cw+gap)
        s.append(box(x,110,cw,90,"#fbfcfe",GLD))
        s.append(txt(x+cw/2,145,k,15,GLD,weight="bold"))
        s.append(txt(x+cw/2,175,v,12,GRY))
        if i<4:
            s.append(f'<line x1="{x+cw}" y1="155" x2="{x+cw+gap}" y2="155" stroke="{GRY}" stroke-width="2" marker-end="url(#ah)"/>')
    s.append('<defs><marker id="ah" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L8,3 L0,6 z" fill="#666"/></marker></defs>')
    s.append(txt(W/2,255,"三个标记都测不到 → 别叫它质变，叫它“退化”或“波动”。",14,GRY))
    save("fig-five-step", s)



if __name__ == "__main__":
    main()
