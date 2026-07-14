# pkgserver 模块分析方法

> 数据源与排除规则。分析前先读 `case-matching.md`。本模块较为特殊。

## 数据源

主日志：`/root/log_det/logs/<架构>-<日期>-<时间>/pkgserver_data/pkgserver.log`

**失败用例以 `pkgserver.log` 中的 `failed_case` 段落为准，不用 CSV**（CSV 只用于了解整体概况）。

`pkgserver.log` 段落结构示例：
```
<version>-<arch>-pkgserver
failed_case:
oe_test_service_httpd
oe_test_service_cpupower
...
all_services:
<service>.service
...
skip_suite:
no skip_suite
failed_install:
no failed_install
```

各失败用例的详细日志在 `all_logs/all_logs/openeuler@<version>-<arch>-mugen-oeupdate-pkgserver-logs/<service>/oe_test_<name>/<timestamp>.log`。

## 排除规则（必执行）

在 `failed_case` 列表上先应用排除，排除的不分析、不计入失败用例数：

| 用例 | 排除原因 | 依据 |
|---|---|---| 
| `oe_test_service_restart` | 批量调度总入口（不是具体服务测试） | 本模块 §2：跳过总入口 |
| `oe_test_service_cpupower` | VM 环境不支持 CPU 频率控制 | 源码 `if ! hostnamectl \| grep Virtualization; then test...; else exit 255; fi` |
| （`oe_test_service_restart` 若未在 failed_case 中列出也跳过） | 总入口 | 同上 |

排除后剩余用例即为本次待分析失败用例。

## 拦截判定要点

- pkgserver 案例库 `pkgserver/` 子目录，典型案例：`pkgserver-IPMI服务测试需要BMC硬件支持.txt`（IPMI/BMC 硬件在 VM 中不可用，标注"是否问题: 否"，"等"字覆盖 bmc-watchdog/ipmidetectd/ipmiseld 等多个 IPMI 服务）。
- httpd 服务启动失败可跨模块匹配 `pkgcmd/pkgcmd-httpd-AH00526-ssl-conf.md`（mod_ssl ssl.conf 证书配置问题）。
- httpd 的连锁服务（httpd-init.service 是 Type=oneshot 的 SSL 初始化前置服务；httpd.socket 依赖 httpd.service）在 httpd 无法启动时必然失败，按"已有关联分析(连锁同根因)"合并处理，引用主用例分析。
- 同一服务在 pkgcmd 与 pkgserver 都失败时（如 radvd），可跨模块引用，pkgserver 报告中注明"同 pkgcmd 模块分析"。

## 输出

按 `report-template.md` 结构生成 `pkgserver_analysis_report.md`。原始统计段落展示 pkgserver.log 的 `failed_case` 与 `all_services` 段落原文，并列表展示排除规则执行情况与排除后待分析用例。✅ 自动拦截用例可用表格合并展示（用例名/拦截类型/匹配案例/根因/关键日志）。
