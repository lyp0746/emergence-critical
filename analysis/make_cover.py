# -*- coding: utf-8 -*-
"""make_cover.py —《涌现的临界》满版封面。母题：一条在临界点跃变的曲线。"""
import math
import os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "assets", "svg", "cover.svg")


def build():
    W, H = 1000, 1414
    ink = "#e8e6df"; dim = "#9aa0a6"; gold = "#b8862f"
    layers = []
    # 相变曲线：连续上升 + 临界点跃变
    pts = []
    for i in range(0, 101):
        t = i / 100
        x = 120 + t * 760
        y = 760 - 40 * t - (300 if t > 0.52 else 0) - 260 * t * t
        pts.append(f"{x:.0f},{y:.0f}")
    layers.append('<polyline points="' + " ".join(pts) + '" fill="none" stroke="#7d8a99" stroke-width="2"/>')
    # 临界点
    cx = 120 + 0.52 * 760
    cy = 760 - 40 * 0.52 - 260 * 0.52 * 0.52
    layers.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="10" fill="none" stroke="{gold}" stroke-width="2"/>')
    layers.append(f'<line x1="{cx:.0f}" y1="520" x2="{cx:.0f}" y2="1010" stroke="{gold}" stroke-width="1" stroke-dasharray="5,6" opacity="0.6"/>')
    layers.append(f'<text x="{cx:.0f}" y="500" text-anchor="middle" class="sm">临界点</text>')
    # 两侧区域文字
    layers.append(f'<text x="300" y="1010" text-anchor="middle" class="sm">量变</text>')
    layers.append(f'<text x="720" y="1010" text-anchor="middle" class="sm">质变</text>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#0e1117"/><stop offset="0.55" stop-color="#151a23"/><stop offset="1" stop-color="#0b0e14"/>
</linearGradient></defs>
<rect x="0" y="0" width="{W}" height="{H}" fill="url(#bg)"/>
<rect x="0" y="0" width="{W}" height="8" fill="{gold}" opacity="0.85"/>
{chr(10).join(layers)}
<style>
text{{font-family:'Microsoft YaHei','SimHei',Arial,sans-serif;}}
.ttl{{font-size:108px;font-weight:700;letter-spacing:10px;fill:{ink};}}
.sub{{font-size:27px;fill:{dim};letter-spacing:2px;}}
.eng{{font-size:20px;fill:{dim};letter-spacing:1px;}}
.au{{font-size:30px;fill:{ink};letter-spacing:2px;}}
.rule{{stroke:{dim};stroke-width:1;opacity:0.6;}}
.sm{{font-size:20px;fill:#cfd6de;letter-spacing:2px;}}
</style>
<text x="80" y="176" class="eng">THE CRITICALITY OF EMERGENCE</text>
<text x="80" y="300" class="ttl">涌现的临界</text>
<line x1="84" y1="344" x2="700" y2="344" class="rule"/>
<text x="84" y="396" class="sub">为什么有些变化回不去</text>
<text x="84" y="440" class="sub">临界、涌现与形式化的边界</text>
<text x="80" y="1230" class="au">李毅芃　著</text>
<text x="80" y="1282" class="eng">Phase Transitions and the Mechanics of Emergence</text>
<text x="80" y="1324" class="eng">学术专著 · 2026</text>
</svg>
'''
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", OUT)


if __name__ == "__main__":
    build()
