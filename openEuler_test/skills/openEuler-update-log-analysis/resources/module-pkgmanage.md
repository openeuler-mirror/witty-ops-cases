# pkgmanage 模块分析方法

> 数据源与失败用例提取规则。分析前先读 `case-matching.md` 了解拦截三级判定。

## 数据源

主日志：`/root/log_det/logs/<架构>-<日期>-<时间>/pkgmanage_data/pkgmanage.log`

`pkgmanage.log` 按版本分段，每段记录该版本包管理测试失败的包名与失败类型（如 `Check repo number fail`、`install package error`、`Downgrade packages error`），以及失败包清单。

各版本对应的详细日志保存在 `pkgmanage_data/` 下对应版本的 `pkg_manage_folder_0x` 文件夹中。

## 失败用例提取步骤

1. 读 `pkgmanage.log`，按版本分段提取每段的失败包操作（install / downgrade / remove 等）。
2. 对每个失败包，到对应版本的 `pkg_manage_folder_0x` 文件夹找详细日志（路径见 pkgmanage.log 段落内提示或同级目录搜索）。
3. 案例库中记录的"进一步分析建议"所依赖的失败日志，也保存在 `pkgmanage_data/` 中对应版本的 `pkg_manage_folder_0x` 文件夹中，按案例库指示定位。

## 拦截判定要点

- pkgmanage 的典型失败模式：POSTIN scriptlet 失败（包安装成功但 `%post` 脚本尝试创建用户/启动服务，容器/VM 环境不支持）；受保护包拒绝移除；架构数量不对等。
- 同包的多个操作（install / downgrade / 子包 downgrade）若同根因可合并为一个聚类分析。
- 案例库 `pkgmanage/` 子目录下的 `pkgmanage-install-error.md`、`pkgmanage-降级失败.md`、`pkgmanage-remove-Protected.md` 等为泛化案例，需核对日志特征是否吻合。

## 输出

按 `report-template.md` 结构生成 `pkgmanage_analysis_report.md`。原始统计段落展示 CSV 的 pkgmanage 行与 pkgmanage.log 各版本段原文。拦截概览按失败包操作数统计。
