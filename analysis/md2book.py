# -*- coding: utf-8 -*-
"""md2book.py — 把 book-src/*.md 转成 source/*.html（为《涌现的临界》定制）。"""
import os
import re

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(HERE, "book-src")
OUT = os.path.join(HERE, "source")

FILES = [
    ("00_前言.md", "front_intro.html", "前言　从“如何取舍”到“何时变天”", None),
    ("01_问题.md", "ch01.html", None, "ch1"),
    ("02_工具.md", "ch02.html", None, "ch2"),
    ("03_标记.md", "ch03.html", None, "ch3"),
    ("04_流程.md", "ch04.html", None, "ch4"),
    ("05_区分的语法.md", "ch05.html", None, "ch5"),
    ("06_遗忘的边界.md", "ch06.html", None, "ch6"),
    ("07_错位的时间.md", "ch07.html", None, "ch7"),
    ("08_选择的代价.md", "ch08.html", None, "ch8"),
    ("09_诠释的权衡.md", "ch09.html", None, "ch9"),
    ("10_地平线.md", "ch10.html", None, "ch10"),
    ("11_不可通约.md", "ch11.html", None, "ch11"),
    ("12_陷阱.md", "ch12.html", None, "ch12"),
    ("13_验证.md", "ch13.html", None, "ch13"),
    ("14_边界.md", "ch14.html", None, "ch14"),
    ("15_核心发现.md", "ch15.html", None, "ch15"),
    ("16_认识论.md", "ch16.html", None, "ch16"),
    ("17_实践.md", "ch17.html", None, "ch17"),
    ("18_新战场.md", "ch18.html", None, "ch18"),
    ("19_经典对标.md", "ch19.html", None, "ch19"),
    ("20_文献综述.md", "ch20.html", None, "ch20"),
    ("21_十案例.md", "ch21.html", None, "ch21"),
    ("23_误用.md", "ch22.html", None, "ch22"),
    ("24_议程.md", "ch23.html", None, "ch23"),
    ("26_问答.md", "ch24.html", None, "ch24"),
    ("25_朗道.md", "ch25.html", None, "ch25"),
    ("26_伊辛.md", "ch26.html", None, "ch26"),
    ("27_拉普拉斯.md", "ch27.html", None, "ch27"),
    ("28_边界.md", "ch28.html", None, "ch28"),
    ("29_标度.md", "ch29.html", None, "ch29"),
    ("30_KKT.md", "ch30.html", None, "ch30"),


    ("08_结语.md", "back_epilogue.html", None, "epilogue"),
    ("09_附录.md", "appendix_a.html", None, "apxA"),
]


def inline(t):
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    return t


def box_class(text):
    if "多想一层" in text:
        return "box box-more1"
    if "再想一层" in text:
        return "box box-more2"
    if "给专家的注" in text:
        return "box box-expert"
    if "动手试试" in text or "陷阱" in text:
        return "box box-do"
    if "一句话带走" in text:
        return "box box-takeaway"
    if "人的尺度" in text:
        return "case"
    return "box"


def heading(level, text):
    text = inline(text)
    if level == 1:
        return f'<h2 class="chapter">{text}</h2>'
    if level == 2:
        m = re.match(r"\s*(\d+)\.(\d+)", re.sub(r"<[^>]+>", "", text))
        if m:
            return f'<h3 id="sec{m.group(1)}-{m.group(2)}">{text}</h3>'
        return f"<h3>{text}</h3>"
    if level == 3:
        return f"<h4>{text}</h4>"
    return f"<h5>{text}</h5>"


def parse_table(rows):
    def cells(r):
        r = r.strip().strip("|")
        return [c.strip() for c in r.split("|")]
    head = cells(rows[0])
    body = [cells(r) for r in rows[2:]]
    out = ['<table class="nat">']
    out.append("<tr>" + "".join(f'<th class="l">{inline(c)}</th>' for c in head) + "</tr>")
    for r in body:
        out.append("<tr>" + "".join(f'<td class="l">{inline(c)}</td>' for c in r) + "</tr>")
    out.append("</table>")
    return "\n".join(out)


def _wrap_para(t):
    m = re.match(r"(?:<strong>)?【(.+?)】(?:</strong>)?", t)
    if m and any(k in m.group(1) for k in ("陷阱", "一句话带走", "给专家的注")):
        return f'<div class="{box_class(m.group(1))}"><p>{t}</p></div>'
    return f"<p>{t}</p>"


def parse_blocks(lines):
    out, i, n = [], 0, len(lines)
    while i < n:
        raw = lines[i].rstrip()
        s = raw.strip()
        if not s:
            i += 1
            continue
        if re.fullmatch(r"[-*_]{3,}", s):
            i += 1
            continue
        m = re.match(r"\[\[FIG:([^|\]]+)(?:\|([^\]]*))?\]\]", s)
        if m:
            name, cap = m.group(1).strip(), (m.group(2) or "").strip()
            cap_html = f'<div class="cap"><b>{cap}</b></div>' if cap else ""
            out.append(f'<img class="fig" src="assets/svg/{name}.svg" alt="{cap}">{cap_html}')
            i += 1
            continue
        m = re.match(r"(#{1,4})\s+(.*)", s)
        if m:
            out.append(heading(len(m.group(1)), m.group(2)))
            i += 1
            continue
        if s.startswith(">"):
            blk, first = [], s
            while i < n and lines[i].strip().startswith(">"):
                blk.append(re.sub(r"^\s*>\s?", "", lines[i]).rstrip())
                i += 1
            out.append(f'<div class="{box_class(first + " " + " ".join(blk[:2]))}">{parse_blocks(blk)}</div>')
            continue
        if s.startswith("|"):
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(lines[i])
                i += 1
            out.append(parse_table(rows))
            continue
        if re.match(r"\s*[-*]\s+", raw):
            items = []
            while i < n and re.match(r"\s*[-*]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*]\s+", "", lines[i]).rstrip())
                i += 1
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>")
            continue
        if re.match(r"\s*\d+\.\s+", raw):
            items = []
            while i < n and re.match(r"\s*\d+\.\s+", lines[i]):
                items.append(re.sub(r"^\s*\d+\.\s+", "", lines[i]).rstrip())
                i += 1
            out.append("<ol>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ol>")
            continue
        para = [s]
        i += 1
        while i < n:
            nxt = lines[i].strip()
            if (not nxt or nxt.startswith(("#", ">", "|", "[[FIG"))
                    or re.fullmatch(r"[-*_]{3,}", nxt)
                    or re.match(r"\s*[-*]\s+", lines[i])
                    or re.match(r"\s*\d+\.\s+", lines[i])):
                break
            para.append(nxt)
            i += 1
        out.append(_wrap_para(inline(" ".join(para))))
    return "\n".join(out)


def main():
    os.makedirs(OUT, exist_ok=True)
    for fname, outname, title_override, anchor in FILES:
        p = os.path.join(SRC, fname)
        if not os.path.exists(p):
            print("skip missing", fname)
            continue
        lines = open(p, encoding="utf-8").read().split("\n")
        if title_override and lines and lines[0].startswith("# "):
            lines[0] = "# " + title_override
        html = parse_blocks(lines)
        open(os.path.join(OUT, outname), "w", encoding="utf-8").write(html + "\n")
        print("wrote", outname, len(html), "bytes")


if __name__ == "__main__":
    main()
