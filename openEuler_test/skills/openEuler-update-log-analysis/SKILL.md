---
name: openEuler-update-log-analysis
description: 下载 Eulerpipeline 测试结果链接中的所有日志包，自动解压并按模块（pkgmanage/kernel/pkgserver/docker/pkgcmd）逐个分析失败用例，结合知识库输出分模块、分版本的详细分析报告。支持全量分析或仅分析指定模块。
license: MIT
compatibility: opencode
metadata:
  category: testing
  domain: openEuler-update
---

## 任务目标
给定一个 Eulerpipeline 测试结果链接（如 `https://eulerpipeline.test.osinfra.cn/crystal/result/update-results/YYYY-MM-DD/vm-2p32g/<version>/<build_id>/`），下载该链接下的所有日志压缩包和 CSV，解压到本地固定路径，然后按模块逐个分析每个失败用例，结合知识库/案例库给出根因分析，最终输出分模块、分版本的详细分析报告(分析一个模块写一篇报告，而不要全部分析完之后一起写报告)。

## 执行模式
在执行具体任务前，先判断用户的意图：

- **全量模式**：用户未明确指定具体模块，或说“全量分析”“全部模块”“都分析一下”时，默认分析全部 5 个模块：pkgmanage、kernel、pkgserver、docker、pkgcmd。
- **定向模式**：用户明确指定模块，例如：“只分析 kernel”“帮我看一下 docker 和 pkgcmd”等时，仅执行用户指定的模块。支持单个或多个模块。

**注意**：无论哪种模式，日志下载与解压步骤都必须完整执行（因为各模块日志可能交叉依赖 `all_logs.tar` 和 `update-results.csv`），但由于有些流水线只执行了部分模块会导致一些文件不存在，忽略即可，后续分析步骤仅针对被指定的模块展开。

## 执行流程

### 1. 日志下载与解压
- 从用户提供的链接中下载以下文件：
  - `all_logs.tar`
  - `ltp.tar`
  - `docker_data.tar`
  - `pkgmanage_data.tar`
  - `pkgserver_data.tar`
  - `update-results.csv`
- 下载目标路径：`/root/log_det/logs/(架构)-(日期)-(时间)/`
- 逐个解压：
  - `all_logs.tar` -> `/root/log_det/logs/(架构)-(日期)-(时间)/all_logs/`
  - `ltp.tar` -> `/root/log_det/logs/(架构)-(日期)-(时间)/ltp/`
  - `docker_data.tar` -> `/root/log_det/logs/(架构)-(日期)-(时间)/docker_data/` 
  - `pkgmanage_data.tar` -> `/root/log_det/logs/(架构)-(日期)-(时间)/pkgmanage_data/`
  - `pkgserver_data.tar` -> `/root/log_det/logs/(架构)-(日期)-(时间)/pkgserver_data/`
- 解压完成后，先读取 `update-results.csv` 了解整体测试概况，同时确认本次需要分析的模块范围（全量或定向）。

### 2. 分模块分析规则

分析报告必须**分模块生成**，每个模块内部**以版本划分**，每个版本里**逐一分析该版本的所有失败用例**，不允许跳过任何失败用例。
分析失败用例时，首先匹配案例库，若找到匹配案例，则直接根据案例分析。若未找到匹配案例，则根据失败日志的特征进行分析。
只有案例库中明确写着非问题的，才算是非问题，**不许自己定义是否为问题**，案例库中未找到明确表示非问题的报错一律视为问题。

#### 2.1 pkgmanage 模块
- 读取 `/root/log_det/logs/(架构)-(日期)-(时间)/pkgmanage_data/pkgmanage.log`，提取各版本包管理测试失败的包名。
- 在各版本对应的 `pkg_manage_folder` 文件夹下找到对应失败的详细日志。
- 结合知识库/案例库对每个失败包进行分析，输出：失败现象、根因推断、参考案例、修复建议。
- pkgmanage相关案例库中记录的进一步分析建议所依赖的失败日志，保存在`/root/log_det/logs/(架构)-(日期)-(时间)/pkgmanage_data/`中对应版本的`pkg_manage_folder_0x` 文件夹中，根据案例库指示进一步分析。

#### 2.2 kernel 模块
- **ltp 测试套**：查看 `update-results.csv` 中 kernel 模块的备注列。
  - 若备注列记录了具体失败的 ltp 用例，到 `/root/log_det/logs/(架构)-(日期)-(时间)/ltp/` 下找到 `ltp.log` 并结合案例库分析。
  - 若备注列未记录具体用例，到 `/root/log_det/logs/(架构)-(日期)-(时间)/all_logs/` 中找到 mugen 日志并结合案例库分析。
- **kernel 测试套**：若 `update-results.csv` 中 kernel 模块的 kernel 测试套失败，直接分析 `all_logs` 中对应的 mugen 日志。
- 每个失败用例都必须给出：失败现象、根因推断、参考案例、修复建议。

#### 2.3 pkgserver 模块
- 读取 `/root/log_det/logs/(架构)-(日期)-(时间)/pkgserver_data/pkgserver.log`，获取`failed_case`中记录的失败用例。
- 该模块较为特殊，`oe_test_service_restart` 用例是总入口用例，无需分析，失败用例以 `pkgserver.log` 中的 `failed_case` 记录为准。
- **跳过 `cpupower` 用例**（不分析）。
- 对于其余失败用例，根据 `pkgserver.log` 中显示的具体用例名，到 `/root/log_det/logs/(架构)-(日期)-(时间)/all_logs/` 中找到对应的 mugen 日志。
- 结合案例库逐一分析失败日志，输出：失败现象、根因推断、参考案例、修复建议。

#### 2.4 docker 模块
- `update-results.csv` 中统计了各版本 docker 模块的用例执行结果。
- 从 `/root/log_det/logs/(架构)-(日期)-(时间)/all_logs/` 中找出所有失败用例对应的具体日志。
- 结合案例库逐一分析，输出：失败现象、根因推断、参考案例、修复建议。

#### 2.5 pkgcmd 模块
- `update-results.csv` 中各版本 pkgcmd 记录了本次所有的转测包。
- 备注列标记了“未找到”表示该包没有对应 mugen 测试套，**跳过**这些条目。
- 对于找到测试套并测试的用例，若结果为失败，到 `/root/log_det/logs/(架构)-(日期)-(时间)/all_logs/` 中找到对应日志。
- 结合案例库逐一分析，输出：失败现象、根因推断、参考案例、修复建议。

### 3. 输出格式要求
- 仅针对本次需要分析的模块生成报告文件（全量则生成 5 个，定向则生成对应模块的报告）保存在 `/root/log_det/reports/(架构)-(日期)-(时间)/` 目录下。
- 报告文件名规范：
  - `pkgmanage_analysis_report.md`
  - `kernel_analysis_report.md`
  - `pkgserver_analysis_report.md`
  - `docker_analysis_report.md`
  - `pkgcmd_analysis_report.md`
- 每个报告内部结构遵循 `resources/report-template.md` 中的模板格式，生成报告前先读取该文件

### 4. 知识库检索规范
- 分析每个失败用例时，优先使用 `rag_search` 工具在相关知识库中检索类似故障。
- 若第一次搜索结果不理想，可调整 `keyword_weight` 并排除不相关 chunk 后重新搜索。
- 将检索到的最相关案例内容整合进“参考案例”中。

## 注意事项
- 绝不跳过任何需要分析的失败用例（pkgserver 的 cpupower 和 pkgcmd 的“未找到”除外）。
- 若日志文件缺失或路径异常，先尝试在同级目录中搜索，再向用户说明。
- 保持报告结构清晰，用例之间逻辑分明。
