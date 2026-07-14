# pkgcmd 模块分析方法

> 数据源与排除规则。分析前先读 `case-matching.md`。

## 数据源

主日志：`/root/log_det/logs/<架构>-<日期>-<时间>/all_logs/all_logs/openeuler@<version>-<arch>-mugen-oeupdate-pkgcmd-logs/pkgcmd.log`

**以 `pkgcmd.log` 为数据源，不用 CSV**（CSV 只用于了解整体概况）。

`pkgcmd.log` 按转测包分段，每段记录：
```
<package> 用例已执行
成功 N 个
跳过 M 个
失败 K 个
failed：oe_test_<a> oe_test_<b> ...
```

各失败用例的详细日志在 `all_logs/.../pkgcmd-logs/<package>/oe_test_<name>/<timestamp>.log`。

## 失败用例提取步骤

1. 读 `pkgcmd.log`，按包分段提取每个包的失败用例清单。
2. CSV 中各版本 pkgcmd 行的**备注列**标记了"未找到"表示该包没有对应 mugen 测试套 → **跳过这些条目，不分析**。在报告原始统计段落列出跳过的包清单。
3. 对找到测试套且结果为失败的用例，到 `all_logs` 的 pkgcmd-logs 目录找对应 mugen 日志。
4. 同包多个失败用例同根因时合并为一个聚类分析。

## 拦截判定要点

pkgcmd 案例库 `pkgcmd/` 子目录，典型案例：

- `pkgcmd-httpd-AH00526-ssl-conf.md`（mod_ssl ssl.conf 证书配置问题，是否问题: 是）—— httpd.service restart 看似返回 0 但 status 非 active，或 `Job for httpd.service failed`。连锁导致 `oe_test_httpd_invalid_configuration_recover` 也失败。
- `pkgcmd-openssl-sm2-pubkey-permission.md`（`openssl ec -pubout` 默认权限 600≠测试预期 644，是否问题: 是）。
- `pkgcmd-docker-engine-loopback...md`（loopback 设备耗尽）。
- 新入库：`pkgcmd-ffmpeg-ffplay-no-display.md`、`pkgcmd-jq-inputline-4095-line-number-mismatch.md`、`pkgcmd-pkgserver-radvd-service-start-fail.md`、`pkgcmd-multipathd-dm-multipath-modprobe-fail.md`。

常见根因模式：
- 服务启动前提不满足（radvd 需 IPv6 转发；multipathd 需 dm_multipath 内核模块；fsidd.service 在旧版本不存在）。
- 无头环境无视频设备（ffmpeg ffplay 需 SDL/`/dev/dri`）。
- 工具版本行为差异（jq input_line_number 行号报告）。
- httpd 连锁失败（见 pkgserver 同根因，可跨模块引用）。

跨模块：pkgcmd 与 pkgserver 共享 radvd、multipathd、httpd 等服务测试，同根因用例可跨模块引用同一案例。

## 输出

按 `report-template.md` 结构生成 `pkgcmd_analysis_report.md`。原始统计段落展示 pkgcmd.log 各包段原文（仅展示有失败的包）+ 跳过的"未找到"包清单。拦截概览按失败用例数统计。✅ 可表格合并；❌ 逐用例或聚类给完整 6 字段 + 案例草稿。
