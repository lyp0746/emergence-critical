# 涌现的临界 · 

> 为什么有些变化回不去：临界、涌现与形式化的边界
>
> **DOI**：10.5281/zenodo.23447311　·　概念 DOI：10.5281/zenodo.23440900　·　259 页 / 6 部分 / 25 章

“量变到质变”为什么听起来像一句口号，而不是一个可检验的命题？本书把它立为这个系列的一个新问题：临界。它给出一个可操作的定义（一次质变＝系统在某个尺度上获得不可由微观无损推出的宏观序，即因果涌现 Φ>0），三个可观测的标记（序参量跃变、临界慢化、有效信息峰值），以及一套可证伪的检验（五个最小验证单元）。前五本书在这本书里不是被诊断的对象，而是五个应用案例：它们检验临界视角的效力，也暴露出它的边界——形式化的地平线。每一条判断都标注证据等级与可反驳条件：结论强度不超过证据强度。卷首《总纲　现实中不存在无限》把临界写成有限尺寸的临界：真实的相变总会被有限的组分与观察窗口抹圆；“回不去”是有限系统关闭旧选项的时间显影。

---

## 结构

| 部分 | 标题 | 章数 | 起 → 止 |
|---|---|---:|---|
| 1 | 第一部分　问题、工具与做法 | 4 | 为什么"量变到质变"需要一门科学 → 《区分的语法》：严格相变的应用 |
| 2 | 第二部分　五个出口与形式化的地平线 | 5 | 《遗忘的边界》：可能是相变的应用 → 形式化的地平线：为什么效力会递减 |
| 3 | 第三部分　立论：可验证单元与三条方向 | 5 | 第六种风险：相变与诠释的不可通约 → 认识论方向：不可知的临界 |
| 4 | 第四部分　方向、案例与反驳 | 5 | 实践方向：在无法精确诊断的世界里决策 → 常见误用与反驳 |
| 5 | 第五部分　推导：朗道、伊辛与网络 | 3 | 研究议程：二十个开放问题 → 推导与解析（三）：图拉普拉斯、渗流与复杂网络 |
| 6 | 第六部分　边界与可行域 | 3 | 边界：为什么决定性质的是"边"，不是"里面" → 边界（二）：约束、可行域与 KKT |

每章八段：主提问 → 场景开篇 → 导论 → 机制 → 表/图 → 反例 → 本章小结 → 一句话带走。
每个部分有满栏插图扉页（`assets/svg/part-NN.svg`）、一段部分导语与一段部分小结。

## 证据与自检

- 结论标注 **A/B/C** 证据等级与甲/乙/丙概念等级；结论强度不超过证据强度。
- 可证伪登记簿：`docs/preregistration/checkups.csv`（append-only）。
- 结构校阅：系列 lint 24 条规则，本书 **error 0 / warn 0**（见 `_series/lint/REPORT.md`）。

## 文件

| 路径 | 是什么 |
|---|---|
| `source/` | **唯一正文来源**（HTML）；`book.json` 元数据、`parts.json` 结构 |
| `analysis/` | 图表、统计、抓取脚本（可重跑） |
| `assets/` | 封面、SVG 图、CSS |
| `scripts/build.sh` | audit → 印刷 PDF → 电子版 → EPUB → Markdown |
| `docs/` | 方法、数据来源、缺口与登记簿 |

产物（`output/`、`release/`）不入库，可由 `source/` 重建。

## 引用

```
涌现的临界：为什么有些变化回不去：临界、涌现与形式化的边界。李毅芃，2026。10.5281/zenodo.23447311
```

## 系列（九本书）

| 书 | 仓库 |
|---|---|
| 只能选两样 | [knowledge-tradeoffs](https://github.com/lyp0746/knowledge-tradeoffs) |
| 区分的语法 | [distinction-evolution](https://github.com/lyp0746/distinction-evolution) |
| 遗忘的边界 | [capacity-cascade](https://github.com/lyp0746/capacity-cascade) |
| 错位的时间 | [entropy-spiral](https://github.com/lyp0746/entropy-spiral) |
| 选择的代价 | [impossibility-triangle](https://github.com/lyp0746/impossibility-triangle) |
| 诠释的权衡 | [interpretation-tradeoff](https://github.com/lyp0746/interpretation-tradeoff) |
| 心灵的分岔 | [mind-forks](https://github.com/lyp0746/mind-forks) |
| 热点的账单 | [hotspot-bills](https://github.com/lyp0746/hotspot-bills) |

十四篇工作论文与全部条目的 DOI 见 [series-workspace](https://github.com/lyp0746/series-workspace)。

## 许可

正文与图件 CC BY 4.0；脚本 MIT。
