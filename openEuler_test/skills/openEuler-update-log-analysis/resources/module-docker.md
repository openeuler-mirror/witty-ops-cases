# docker 模块分析方法

> 数据源与失败用例提取规则。分析前先读 `case-matching.md`。

## 数据源

**CSV 为数据源**：`update-results.csv` 中 docker 模块行统计了各版本 docker smoke 套件的用例执行结果（成功数/失败数/跳过数/失败用例清单）。

各失败用例的详细日志在 `all_logs/all_logs/openeuler@<version>-<arch>-mugen-oeupdate-docker-logs/<...>/oe_test_<name>/<timestamp>.log`。

可选辅助日志：`docker_data/` 下的 `check_update.log`（记录容器内待更新的包清单，用于说明"docker smoke 套件验证这些更新不破坏容器基础功能"的上下文）。

## 失败用例提取步骤

1. 从 CSV docker 行提取失败用例清单（逗号分隔的 `oe_test_*` 列表）。
2. 对每个失败用例，到 `all_logs` 的 docker-logs 目录找对应 mugen 日志。
3. docker smoke 失败量大时（20.03-SP4 常有 35-57 个），**按根因聚类合并分析**，不要逐个长篇展开。

## 拦截判定要点

docker 模块失败绝大多数为**容器环境限制**，非包更新质量。常见根因聚类（案例库 `docker/` 子目录）：

- **容器 systemd D-Bus 不可用**：oe_test_dbus, dbus-monitor, dbus-send, localectl_001, dateinfo_001, firewalld, firewalld_server, iscsid, rpcbind, nfs_02, ntp_01, netstat_01, network_001, haproxy, criu → `Failed to connect to bus: Connection refused` / `Job for dbus.service failed`。
- **容器 NetworkManager 不可用**：oe_test_bonding_SCEN_05, bridge-utils_01, network_001, netstat_01 → `NetworkManager is not running` / `Job for NetworkManager.service failed`。
- **容器内核模块不可用**：oe_test_ebtables, ip6tables_01/02 → `modprobe: Permission denied` / `can't initialize ... table 'filter': Table does not exist`。
- **容器 auditd 不可用**：oe_test_grep_001 → `pgrep auditd` 返回非零。
- **容器用户/组管理受限**：oe_test_user_001/002/003, group_001/002, shadow, find, chown_001, umask_002。
- **容器 sudo 受限**：oe_test_sudo, sudo_E, sudo_maxseq。
- **容器网络/工具受限**：oe_test_ssh, basic_ssh_001, curl_02, tcpdump, normal_tcpdump_*, netstat_01。
- **容器 cgroup 受限**：oe_test_libcgroup_01-04。
- **容器 pip/网络超时**：oe_test_python_pip_install, python_urllib3_urlopen_01/02。

匹配策略：
- 案例库已有明确案例（如 `docker-pip3安装失败.txt`、新入库的 `docker-systemd-dbus-connection-refused.md`、`docker-bonding-NetworkManager-not-running.md`）→ ✅ 自动拦截。
- 案例库有草稿但标注"待确认"（`docker-MEMinfo_001失败.md`、`docker-grep_001失败.md`、`docker-localectl_001失败.md`、`docker-ebtables_01失败.md`）→ ⚠️ 待确认。
- 无案例 → ❌ 未拦截，按根因聚类合并产出 1 条通用案例草稿（如 `docker-general-container-restriction.md`）。

## 输出

按 `report-template.md` 结构生成 `docker_analysis_report.md`。原始统计段落展示 CSV docker 行与 check_update.log 摘要。拦截概览按失败用例数统计。✅/⚠️ 可用表格合并展示；❌ 按聚类合并，每聚类给代表日志 + 涉及用例清单 + 案例草稿。
