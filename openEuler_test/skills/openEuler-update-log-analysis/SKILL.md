---
name: openEuler-update-log-analysis
description: 下载并分析 openEuler 升级流水线(Eulerpipeline)日志，按模块生成拦截式分析报告与周报。当用户说"分析日志""日志分析""分析流水线""出周报"或给出 Eulerpipeline 测试结果链接时自动触发。支持全量/定向模块分析、多流水线周报汇总、案例库匹配与缺口分析。
license: MIT
compatibility: opencode
metadata:
  category: testing
  domain: openEuler-update
---

## 任务目标

下载 Eulerpipeline run-view 链接对应的日志包与 CSV，解压到本地，按模块逐个分析失败用例，结合案例库给出拦截式根因分析，输出分模块、分版本的分析报告；多流水线场景额外生成周报与共享上下文文件。

> 全部"怎么做"细节拆在 `resources/` 下，**执行任一步骤前必须先 Read 对应资源文件**按其规则执行，不要凭记忆发挥。路径均相对本 SKILL.md 所在目录。

## 触发与意图

触发词："分析日志""日志分析""分析流水线""出周报"，或用户直贴 Eulerpipeline 链接。判断：

- **是否给链接**：未给链接 → 按 `resources/pipeline-registry.md` 自动解析固定 6 条流水线最新一次 success 运行结果（见下）。给 run-view 链接 → 跳过自动解析直接用。
- **规模**：单流水线模式（一条）/ 周报模式（一周全部 6 条 + 周标识，未给则用执行日期的 ISO 周序如 2026-W28）。
- **模块范围**：未指定或"全量/全部/都分析"→ 5 个模块：pkgmanage、kernel、pkgserver、docker、pkgcmd；明确指定则仅分析指定模块。下载解压步骤无论哪种模式都完整执行；部分流水线只跑部分模块致文件缺失则忽略。

## 自动获取最新日志（未给链接时必做）

读 `resources/pipeline-registry.md`，对固定 6 条流水线逐条：用 webfetch 访问该 workflow 的 run-view 链接（不带 `workflow_exec_id`）查看历史运行 → 取最新一次 success 运行的 `workflow_exec_id` 与日期 → 拼带 exec_id 的 run-view 链接 → webfetch 该页面，定位 **mugen-oeupdate-results 日志按钮** href 得日志下载根 URL。6 条全解析后元数据填入 `_analysis_context.md`。周报 6 条全做；单流水线只做指定那条。失败用注册表示例 exec_id 兜底并向用户确认。

## 执行流程

### 0. 读取规则资源（开始前必做）

- `resources/pipeline-registry.md` —— 固定 6 条流水线 workflow_id/版本/架构/顺序与自动解析方法。
- `resources/download-extract.md` —— 日志下载与解压详细规则。
- `resources/case-matching.md` —— 案例库路径与三级（✅自动拦截/⚠️待确认/❌未拦截）判定铁律。
- `resources/report-template.md` —— 单模块报告结构。
- `resources/weekly-summary-template.md` —— 周报结构（仅周报模式读）。
- `resources/analysis-context-template.md` —— 共享上下文结构（仅周报模式读）。
- 各模块方法（按本次要分析的模块读）：`resources/module-pkgmanage.md`、`module-kernel.md`、`module-pkgserver.md`、`module-docker.md`、`module-pkgcmd.md`。

### 1. 日志下载与解压（每条流水线都做）

按 `resources/download-extract.md` 执行：下载 all_logs.tar/ltp.tar/docker_data.tar/pkgmanage_data.tar/pkgserver_data.tar/update-results.csv 到 `/root/log_det/logs/<架构>-<日期>-<时间>/` 并解压；解压后先读 `update-results.csv` 确认模块范围与版本/架构/状态。

### 2. 分模块分析（一个模块写一篇报告，分析完即落盘）

核心原则：模块内按版本划分，逐个分析所有失败用例，**不许跳过**（各模块文件列出的排除项除外）。每个用例**先匹配案例库**（规则见 `case-matching.md`）：命中且"是否问题:否/是"→✅自动拦截；命中但"待确认"→⚠️待确认；未命中→❌未拦截并产出案例草稿。**判定铁律**：只有案例库明确写"非问题"才算非问题，不许自行定义；未找到明确非问题的报错一律视为问题。按本次要分析的模块逐个遵循 `module-<模块>.md` 执行，分析完即按 `report-template.md` 落盘。

### 3. 输出与目录结构

- 单流水线：`/root/xys/<报告根目录>/<流水线简称>/<module>_analysis_report.md`
- 周报：`/root/xys/<周标识>/<序号>-<流水线简称>/<module>_analysis_report.md`（`<周标识>` 形如 2026-W26；`<序号>`1..N；`<流水线简称>`形如 arm-2003sp4）

报告文件名：`pkgmanage|kernel|pkgserver|docker|pkgcmd`_analysis_report.md。仅对本次要分析的模块生成。

### 4. 周报汇总（仅周报模式）

全部模块报告完成后：按 `analysis-context-template.md` 生成 `_analysis_context.md`；按 `weekly-summary-template.md` 生成 `weekly_summary.md`（总览/各流水线/根因聚类/拦截率矩阵/行动清单/草稿跟踪/报告索引）。需对比上周拦截率趋势并标注本周新入库案例。

## 注意事项

- 绝不跳过任何需分析的失败用例（pkgserver 的 cpupower、pkgcmd 的"未找到"除外）。
- 日志缺失/路径异常时先在同级目录搜索，再向用户说明。
- 连锁失败（同根因）可合并展示但须说明合并理由与涉及用例；同根因跨模块用例可引用其他模块报告避免重复。
- 案例草稿嵌入 ❌ 未拦截段落，格式与案例库 `.md` 一致，便于审核后直接入库。
