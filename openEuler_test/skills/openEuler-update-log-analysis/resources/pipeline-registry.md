# 流水线注册表（固定 6 条）

> Update 版本测试固定流水线，每周执行最新结果。`workflow_id` 固定不变，`workflow_exec_id` 每次运行变化。用户说"分析日志""出周报"但未给链接时，**用本注册表自动解析最新结果**，不要反问用户要链接。

## 固定流水线清单

| # | 流水线简称 | 源版本 | 架构 | workflow_id | run-view 链接 |
|---|---|---|---|---|---|
| 1 | arm-2003sp4 | 20.03-LTS-SP4 | aarch64 | workflow.376512239215050754 | https://eulerpipeline.test.osinfra.cn/run-view?workflow_id=workflow.376512239215050754 |
| 2 | x86-2003sp4 | 20.03-LTS-SP4 | x86_64 | workflow.376511066688978945 | https://eulerpipeline.test.osinfra.cn/run-view?workflow_id=workflow.376511066688978945 |
| 3 | arm-2203sp4 | 22.03-LTS-SP4 | aarch64 | workflow.376517285801623556 | https://eulerpipeline.test.osinfra.cn/run-view?workflow_id=workflow.376517285801623556 |
| 4 | x86-2203sp4 | 22.03-LTS-SP4 | x86_64 | workflow.376514451123208195 | https://eulerpipeline.test.osinfra.cn/run-view?workflow_id=workflow.376514451123208195 |
| 5 | arm-2403sp1sp3 | 24.03-LTS-SP1+SP3 | aarch64 | workflow.371300966416252930 | https://eulerpipeline.test.osinfra.cn/run-view?workflow_id=workflow.371300966416252930 |
| 6 | x86-2403sp1sp3 | 24.03-LTS-SP1+SP3 | x86_64 | workflow.371301803934875652 | https://eulerpipeline.test.osinfra.cn/run-view?workflow_id=workflow.371301803934875652 |

> run-view 链接去掉 `workflow_exec_id` 参数即进入该 workflow 的运行历史视图，可看到历次运行列表。

## 周报模式流水线顺序与目录命名

周报按以下顺序编号，目录名为 `<序号>-<流水线简称>`：

| 序号 | 目录名 | workflow_id |
|---|---|---|
| 1 | 1-arm-2003sp4 | workflow.376512239215050754 |
| 2 | 2-arm-2203sp4 | workflow.376517285801623556 |
| 3 | 3-x86-2203sp4 | workflow.376514451123208195 |
| 4 | 4-x86-2403sp1sp3 | workflow.371301803934875652 |
| 5 | 5-arm-2403sp1sp3 | workflow.371300966416252930 |
| 6 | 6-x86-2003sp4 | workflow.376511066688978945 |

## 自动解析最新结果（必做）

对每条流水线，获取本周最新运行结果与日志下载根 URL 的步骤：

1. 用 webfetch 访问该 workflow 的 run-view 链接（不带 `workflow_exec_id`）查看历史运行：
   `https://eulerpipeline.test.osinfra.cn/run-view?workflow_id=<workflow_id>`
2. 该页面展示历史运行列表（"历史运行"），从中选取**最新一次成功(success)的运行**，取出其 `workflow_exec_id` 与执行日期，拼出带 exec_id 的 run-view 链接：
   `https://eulerpipeline.test.osinfra.cn/run-view?workflow_id=<workflow_id>&workflow_exec_id=<workflow_exec_id>`
3. webfetch 该带 exec_id 的 run-view 页面，在页面中找到 **mugen-oeupdate-results 日志按钮**，其 href 即日志结果界面 URL（**日志下载根 URL**），形如：
   `https://eulerpipeline.test.osinfra.cn/log/result/mugen-oeupdate-results/<YYYY-MM-DD>/vm-2p32g/openeuler-<version>-<arch>/<ssh-key-prefix>/<build_id>/`
4. 从该 URL 原样提取 4 段（**不可从 workflow 元数据推导，必须从按钮链接提取**）：
   - `<YYYY-MM-DD>`：执行日期。
   - `openeuler-<version>-<arch>`：版本-架构段，版本用连字符（如 `openeuler-24.03-LTS-SP3-x86_64`、`openeuler-22.03-LTS-SP4-aarch64`）。注意注册表"源版本"列是升级路径描述（如 `24.03-LTS-SP1+SP3` 表示 SP1→SP3），此处的 `<version>` 是**目标版本**（SP3），二者不直接相等。
   - `<ssh-key-prefix>`：测试主机 SSH 公钥前缀（如 `ssh-rsaAAAAB3NzaC1yc2EAAAADAQABAAABAQDRy`），每次环境不同，无法构造。
   - `<build_id>`：运行 build id（数字串，如 `26070805071908700`）。
5. 6 条流水线全部解析完成后，把元数据（含日志下载根 URL）填入 `_analysis_context.md` 的流水线元数据表，再进入下载解压流程。

> 若 webfetch 无法直接拿到结构化运行列表，尝试访问带某 `workflow_exec_id` 的 run-view 页面，从页面内的"历史运行/最新运行"链接中提取最新 exec_id；或直接用用户给出的（注册表里示例的）exec_id 作为兜底，并向用户确认是否为本周最新。
>
> ⚠️ eulerpipeline.test.osinfra.cn 部署 CloudWAF，webfetch/curl 可能被拦（返回 HTTP 418 "访问被拦截"）。被拦时不要尝试构造 `/crystal/result/update-results/...` 这类旧路径（已废弃，日志实际在 `/log/result/mugen-oeupdate-results/...`）；改为在能访问该站的环境预置日志到 `/root/log_det/logs/`，或向用户索要 cookie/鉴权。

## 兜底：用户直接给链接

用户直接粘贴一条或多条 run-view 链接（含 `workflow_exec_id`）时，跳过第 1-2 步（历史运行选取），直接从第 3 步开始：webfetch 该 run-view 页面，找 mugen-oeupdate-results 日志按钮拿日志下载根 URL，按 SKILL.md 流程执行。

> 用户也可能直接粘贴日志结果界面 URL（`/log/result/mugen-oeupdate-results/...`），此时该 URL 即日志下载根 URL，直接进入下载解压，无需再点按钮。

## 示例（真实数据，供兜底与校验）

以下为 2026-07-08 的一次真实运行，演示 run-view 链接 → 日志下载根 URL 的对应关系：

| 项 | 值 |
|---|---|
| 流水线 | #6 x86-2403sp1sp3 |
| workflow_id | workflow.371301803934875652 |
| run-view 链接（含 exec_id） | `https://eulerpipeline.test.osinfra.cn/run-view?workflow_id=workflow.371301803934875652&workflow_exec_id=workflow_exec.388861008925425677` |
| 点击 mugen-oeupdate-results 日志按钮后跳转 | `https://eulerpipeline.test.osinfra.cn/log/result/mugen-oeupdate-results/2026-07-08/vm-2p32g/openeuler-24.03-LTS-SP3-x86_64/ssh-rsaAAAAB3NzaC1yc2EAAAADAQABAAABAQDRy/26070805071908700/` |

> 据此可校验解析逻辑：日期 `2026-07-08`、版本-架构段 `openeuler-24.03-LTS-SP3-x86_64`（注意目标是 SP3，非注册表"源版本"的 SP1+SP3）、ssh-key 段 `ssh-rsaAAAAB3NzaC1yc2EAAAADAQABAAABAQDRy`、build_id `26070805071908700`，均从按钮链接提取，不可构造。
