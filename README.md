# 涌现的临界 · 

> 为什么有些变化回不去：临界、涌现与形式化的边界
>
> **DOI**：10.5281/zenodo.24239580　·　概念 DOI：10.5281/zenodo.23440900　·　301 页 / 6 部分 / 24 章

“量变到质变”为什么听起来像一句口号，而不是一个可检验的命题？本书把它立为这个系列的一个新问题：临界。它给出一个可操作的定义（一次质变＝系统在某个尺度上获得不可由微观无损推出的宏观序，即因果涌现 Φ>0），三个可观测的标记（序参量跃变、临界慢化、有效信息峰值），以及一套可证伪的检验（五个最小验证单元）。前五本书在这本书里不是被诊断的对象，而是五个应用案例：它们检验临界视角的效力，也暴露出它的边界——形式化的地平线。每一条判断都标注证据等级与可反驳条件：结论强度不超过证据强度。卷首《总纲　现实中不存在无限》把临界写成有限尺寸的临界：真实的相变总会被有限的组分与观察窗口抹圆；“回不去”是有限系统关闭旧选项的时间显影。

---

## 本版（2026-11-04）

- **新增 `1.6b` 变分临界**：单位立方三维环面的等周问题——极小区分四类（球、圆管、板、补集），转变体积是**精确数** `4π/81` 与 `1/π`，每处相邻两类同时极小。它**没有任何动力学结构**，却具备临界的全部现象（阈值、共存、类型切换）。据此把“质变”写成一句话：**最优值面连续，最优者的身份跳变**。
- **新增 `1.12b` 预警的可靠性**：SK 自旋玻璃动力学把三件事拆开——`β<1` 全区间有 cutoff（突变）却无临界；`β=1` 混合时间 `n^(2/3)`；`β>1` 从平衡态出发仍是伸展指数（远离临界仍慢）。结论：**突变 ≠ 临界；“临界慢化”既会漏也会误；只有重标度后的普适极限能定位临界点**。
- **修订**：第 1.6 节的三条标记由“并列”改为**分级**（定位级／验证级／参考级）；§1.12 标题去“唯一”。不动编号。
- **规模**：301 页、24 章、6 部分。

## 结构

| 部分 | 标题 | 章数 | 起 → 止 |
|---|---|---:|---|
| 1 | 第一部分　问题、工具与做法 | 4 | 为什么"量变到质变"需要一门科学 → 《区分的语言》：严格相变的应用 |
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
涌现的临界：为什么有些变化回不去：临界、涌现与形式化的边界。李毅芃，2026。10.5281/zenodo.23440900
```

## 系列（九本书）

| 书 | 仓库 |
|---|---|
| 只能选两样 | [knowledge-tradeoffs](https://github.com/lyp0746/knowledge-tradeoffs) |
| 区分的语言 | [distinction-evolution](https://github.com/lyp0746/distinction-evolution) |
| 遗忘的边界 | [capacity-cascade](https://github.com/lyp0746/capacity-cascade) |
| 错位的时间 | [entropy-spiral](https://github.com/lyp0746/entropy-spiral) |
| 选择的代价 | [impossibility-triangle](https://github.com/lyp0746/impossibility-triangle) |
| 诠释的权衡 | [interpretation-tradeoff](https://github.com/lyp0746/interpretation-tradeoff) |
| 心灵的分岔 | [mind-forks](https://github.com/lyp0746/mind-forks) |
| 热点的账单 | [hotspot-bills](https://github.com/lyp0746/hotspot-bills) |

十四篇工作论文与全部条目的 DOI 见 [series-workspace](https://github.com/lyp0746/series-workspace)。

## 许可

正文与图件 CC BY 4.0；脚本 MIT。

<!-- viz-console -->
## 可视化阅读台 ｜ Reading console

这一件配了两个**离线单文件**：双击就能开，断网可用，零外部依赖、零服务器、零 API 账单。
Two offline single-file entries ship with this item. Double-click and it runs — no network, no server, no API bill.

| 入口 | 文件 | 体积 | 里面是什么 |
|---|---|---|---|
| 阅读页 | `assets/emergence-critical-reader.html` | 747 KB | 三档切换（**骨架**＝只留标题与高亮框／**阅读**＝正文全显、表与证据折叠／**全展**＝全部展开，可用 Ctrl+F 搜全书表格）＋ **24 张章末审问卡** |
| 结构地图 | `assets/emergence-critical-explorer.html` | 111 KB | 章际引用的 3D 螺旋、部 × 部矩阵、附录原表台账（按表号/章/单元格搜索）、图件账（SVG 内联，不缺图） |

- **审问卡**四行全部原文摘录，一个字不增写：`带走`（一句话带走／本章小结末句）／`打脸条件`（表 F.1、附录登记簿、或「反例与边界」节首段）／`封顶`（本章标过的 A/B/C 等级，没有就不印）／`动手`（【动手试试】）。右上角一键复制，粘到自己的 AI 里当严苛伴读。
  The audit card quotes four things verbatim — takeaway, falsification condition, evidence ceiling, hands-on prompt — and offers a one-click copy for your own AI, with the discipline written into the clipboard.
- **两页互跳**：阅读页顶部「结构地图 →」，结构地图工具栏「正文阅读页 →」，螺旋上点第 N 章直接落到 `#chN`。
- **已验证**：`375px` 窄屏与桌面均无横向溢出；0 个 JS 报错；三档切换 10–40 ms（纯 CSS class，不遍历 DOM）。
- 本件规模：正文 **24 章**；审问卡 **24 张**。
  Size: **24 chapters**, **24** audit cards.


## 可视化阅读台 / Reading console

`涌现的临界` 每件都有两个入口，**离线单文件、断网可开、零外部依赖**：

| 入口 | 文件 | 里面是什么 |
|---|---|---|
| 阅读页 | [`assets/emergence-critical-reader.html`](assets/emergence-critical-reader.html) | 三档切换（骨架／阅读／全展）＋ 每章末尾「审问卡」（带走／打脸条件／封顶／动手，四行全部原文摘录，可一键复制给自己的 AI 当严苛伴读） |
| 结构地图 | [`assets/emergence-critical-explorer.html`](assets/emergence-critical-explorer.html) | 章际引用的 3D 螺旋、部 × 部矩阵、附录原表台账（可搜）、图件账 |

两个页面顶部互跳；`375px` 窄屏与桌面都验过，0 外部请求。

Every item ships two offline single-file entries: a **reading console** (three density levels + a per-chapter audit card quoting the text verbatim) and a **structure map** (chapter-citation spiral, part × part matrix, appendix ledgers). No server, no external requests — double-click and it runs.

