# kernel 模块分析方法

> 数据源、决策树与失败用例提取规则。分析前先读 `case-matching.md`。

## 数据源

- `update-results.csv` 中 kernel 模块行的**备注列**（记录 LTP 失败用例清单）。
- `/root/log_det/logs/<架构>-<日期>-<时间>/ltp/ltp.log` 及 `ltp/openeuler@<version>-<arch>-kernel-ltp/results/LTP_RUN_ON-*.log`。
- `/root/log_det/logs/<架构>-<日期>-<时间>/all_logs/all_logs/openeuler@<version>-<arch>-mugen-oeupdate-kernel-logs/` 下 mugen 日志。

## 决策树（先判定是否需要分析）

1. 读 CSV，看是否有 kernel 模块行。
2. 看 `all_logs` 中是否有 `mugen-oeupdate-kernel-logs` 目录。
3. 看 `ltp/` 目录是否非空（含 ltp.log）。

判定：

- **CSV 中有 kernel 行** 或 **all_logs 有 kernel 目录** 或 **ltp 非空** → 按 LTP 用例 + kernel 测试套分别分析。
- **CSV 无 kernel 行 且 all_logs 无 kernel 目录 且 ltp 为空** → 记录"本次流水线未测试 kernel 模块"，跳过分析。报告只需写头部 + 数据完整性摘要 + 一句结论 + 空拦截概览（全部 0）。

## 失败用例提取步骤

### LTP 测试套
- 备注列记录了具体失败的 LTP 用例 → 到 `ltp/` 下找 `ltp.log`，结合 LTP results log 取每个用例的 TFAIL 行。
- 备注列未记录具体用例 → 到 `all_logs` 中找 mugen 日志（`oe_test_ltp`），结合案例库分析。

### kernel 测试套
- CSV 中 kernel 模块的 kernel 测试套失败 → 直接分析 `all_logs` 中对应的 mugen 日志。

## 拦截判定要点

- kernel 案例库 `kernel/` 子目录下有大量 `kernel-ltp执行<用例>失败.txt`，按 LTP 用例名精确匹配。
- 常见非问题模式：OLK 内核未支持某系统调用（`__NR_file_setattr`）、openEuler 自研特性未适配 LTP（`/proc/dirty/dirty_list`）、硬件不支持（Kunpeng920 无 CPU boost）、内核未编译模块（`CONFIG_LOCK_TORTURE_TEST`）、测试用例设计不严谨（cpuset_memory_spread 概率性失败）。
- 多个 LTP 用例同根因（如 memcg/cpuset 系列）合并为一个聚类分析。
- 同一失败用例在 SP1 与 SP3 都出现时，SP3 段落可引用 SP1 分析，仅列差异。

## 输出

按 `report-template.md` 结构生成 `kernel_analysis_report.md`。按版本（SP1/SP3）分章节，每版本下列 ✅ 自动拦截与 ❌ 未拦截用例。原始统计段落展示 CSV 备注列与 LTP results 实际失败列表。
