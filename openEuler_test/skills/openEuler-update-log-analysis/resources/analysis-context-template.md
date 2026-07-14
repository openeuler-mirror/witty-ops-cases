# 共享上下文模板（_analysis_context.md）

> 仅周报模式使用。在所有流水线模块报告完成、生成 weekly_summary 之前，先在周根目录生成 `_analysis_context.md`，汇总各流水线元数据与跨流水线案例库匹配结果，供后续分析复用与周报引用。

```markdown
# <周标识> 日志分析共享上下文

## 流水线元数据

| # | 流水线简称 | 日志目录 | 源版本 | 架构 | 执行时间 | 模块 |
|---|---|---|---|---|---|---|
| 1 | arm-2003sp4 | <架构>-<日期>-<时间> | 20.03-LTS-SP4 | aarch64 | YYYY-MM-DD HH:MM | docker,pkgcmd,pkgserver |
| 2 | arm-2203sp4 | ... | 22.03-LTS-SP4 | aarch64 | | |
| 3 | x86-2203sp4 | ... | 22.03-LTS-SP4 | x86_64 | | |
| 4 | x86-2403sp1sp3 | ... | 24.03-SP1+SP3 | x86_64 | | |
| 5 | arm-2403sp1sp3 | ... | 24.03-SP1+SP3 | aarch64 | | |
| 6 | x86-2003sp4 | ... | 20.03-LTS-SP4 | x86_64 | | |

> 所有日志目录在 `/root/log_det/logs/<dir_name>/`，解压后的 all_logs 在 `all_logs/all_logs/openeuler@<version>-<arch>-mugen-oeupdate-<module>-logs/`。

## 案例库匹配结果

案例库路径：`/root/xys/gitcode/witty-ops-cases/openEuler_test/update_test/`

### ✅ 自动拦截（案例库明确匹配）

| 用例 | 模块 | 匹配案例 | 是否问题 | 根因 |
|---|---|---|---|---|
| oe_test_... | pkgcmd | <案例文件> | 是/否 | <根因> |

### ⚠️ 待确认（案例库部分匹配）

| 用例 | 模块 | 匹配案例 | 是否问题 | 根因 |
|---|---|---|---|---|
| oe_test_... | docker | <草稿案例> | 待确认 | <根因> |

### ❌ 未拦截（无案例匹配）— 常见根因模式

| 用例 | 模块 | 根因模式 | 日志特征 |
|---|---|---|---|
| oe_test_... | docker | 容器 NetworkManager 限制 | `NetworkManager is not running` |

### <某版本特有失败模式>（如 20.03-LTS-SP4 docker 失败模式）

<按版本聚合列出大量失败的根因模式与涉及用例清单，供周报聚类引用>

## 报告格式（精简版）

每篇报告保存到 `<周标识>/<序号>-<流水线简称>/<module>_analysis_report.md`。

报告结构（详见 `report-template.md`）：
1. 头部：报告生成时间、流水线名称、源版本/架构、执行时间、执行状态、数据完整性摘要
2. 原始统计：展示该模块的原始统计文件内容
3. 拦截概览：表格展示总失败/✅/⚠️/❌ 数量和占比
4. ✅ 自动拦截：逐条列出，一句话+一行日志（可合并为表格）
5. ⚠️ 待确认：部分匹配案例+检索关键词+AI初步根因+不确定点+关键日志
6. ❌ 未拦截：完整6字段（测试执行上下文、关键日志证据、分析逻辑链、检索记录、根因推断、修复建议）+案例草稿
7. 案例库缺口分析：表格

### 关键规则
- pkgserver：跳过 oe_test_service_restart（总入口）和 cpupower（VM 不支持）
- pkgserver 数据源用 pkgserver.log 的 failed_case（不是 CSV）
- pkgcmd 数据源用 pkgcmd.log（不是 CSV）
- docker 数据源用 CSV
- kernel 数据源用 CSV 备注列
- 连锁失败可合并展示（如 httpd 连锁导致 httpd-init 失败）
- 同根因跨模块用例可引用其他模块报告

## 参考报告

<若部分流水线先完成，可作为其余流水线的格式参考，列出路径>
- `<周标识>/<序号>-<流水线简称>/<module>_analysis_report.md`

上周报告（相同失败模式，可复用根因分析）：
- `<上周标识>/<流水线>/<module>_analysis_report.md`
```
