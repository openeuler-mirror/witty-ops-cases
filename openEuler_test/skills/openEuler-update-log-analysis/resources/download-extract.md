# 日志下载与解压

> SKILL.md 执行流程第 1 步的详细规则。每条流水线都做。

## 日志下载根 URL 的取得

由 SKILL.md 的"自动获取最新日志"或用户直给的 run-view 链接得到。该根 URL 形如：

```
https://eulerpipeline.test.osinfra.cn/log/result/mugen-oeupdate-results/<YYYY-MM-DD>/vm-2p32g/openeuler-<version>-<arch>/<ssh-key-prefix>/<build_id>/
```

其中 `<YYYY-MM-DD>`、`openeuler-<version>-<arch>`、`<ssh-key-prefix>`、`<build_id>` 四段**必须从 run-view 页面 mugen-oeupdate-results 日志按钮的 href 原样提取**，不可从 workflow 元数据推导——尤其 `<ssh-key-prefix>` 是测试主机 SSH 公钥前缀，每次环境不同。

## 下载文件清单

在根 URL 末尾追加文件名下载（不存在的跳过并记录到数据完整性摘要）：

| 文件 | 解压到 |
|---|---|
| `all_logs.tar` | `.../all_logs/` |
| `ltp.tar` | `.../ltp/` |
| `docker_data.tar` | `.../docker_data/` |
| `pkgmanage_data.tar` | `.../pkgmanage_data/` |
| `pkgserver_data.tar` | `.../pkgserver_data/` |
| `update-results.csv` | 不解压，直接读 |

下载目标根路径（按架构-日期-时间命名，与 CSV/链接元数据对齐）：

```
/root/log_det/logs/<架构>-<日期>-<时间>/
```

例如 `aarch64-2026-06-30-140546`。

> 周报模式下：所有日志目录都在 `/root/log_det/logs/<dir_name>/`，解压后的 all_logs 在 `all_logs/all_logs/openeuler@<version>-<arch>-mugen-oeupdate-<module>-logs/`。

## 取不到文件 URL 时的兜底

- 直接追加文件名返回 404 或被拦 → 先 webfetch 日志结果界面页面，从页面列出的下载链接中取各文件实际 URL。
- ⚠️ eulerpipeline.test.osinfra.cn 部署 CloudWAF，webfetch/curl 可能被拦（返回 HTTP 418 "访问被拦截"）。被拦时**不要**构造 `/crystal/result/update-results/...` 这类旧路径（已废弃，日志实际在 `/log/result/mugen-oeupdate-results/...`）；改为在能访问该站的环境预置日志到本地 `/root/log_det/logs/`，或向用户索要 cookie/鉴权。

## 解压后必做

先读 `update-results.csv` 了解整体测试概况，确认本次要分析的模块范围（全量/定向）以及各模块对应的版本、架构、执行状态。
