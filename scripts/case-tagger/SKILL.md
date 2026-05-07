---
name: case-tagger
description: 案例标签自动分类器，基于规则匹配和关键词提取，自动为案例打上标签（如：内核崩溃、网络问题、存储问题、OOM、硬件故障等），支持生成标签分布报告。
---

# 案例标签自动分类器

## 功能概述

本工具用于自动为故障案例文件打上标签，基于规则匹配和关键词提取，支持多种标签类型，便于按类别浏览和筛选案例。

### 支持的标签类型

| 标签 | 描述 |
| 内核崩溃 | 内核崩溃、oops、系统挂死等问题 |
| 网络问题 | 网络连接、网卡、TCP/IP 相关问题 |
| 存储问题 | 磁盘、文件系统、RAID 相关问题 |
| OOM | 内存溢出、内存不足问题 |
| 硬件故障 | 硬件损坏、PCIe 错误、过温等问题 |
| 启动问题 | 系统启动、GRUB、PXE 相关问题 |
| 驱动问题 | 驱动加载失败、模块初始化失败 |
| CPU问题 | CPU 硬锁、软锁、过温等问题 |
| 服务异常 | 系统服务、进程异常问题 |
| 性能问题 | 性能劣化、响应缓慢等问题 |

## 触发场景

- 批量为案例库添加标签
- 新案例入库前自动打标签
- 了解案例库的标签分布情况
- 按标签筛选和管理案例

## 执行方式

在 `case-tagger` 目录下运行：

```bash
# 基本用法 - 为目录下的案例打标签
python scripts/main.py <案例目录路径>

# 示例：为 community_maintenance 目录打标签
python scripts/main.py ../../community_maintenance

# 生成详细报告并保存到文件
python scripts/main.py ../../community_maintenance -o tag_report.md -v

# 不递归扫描子目录
python scripts/main.py ../../community_maintenance --no-recursive

# 只显示简要信息
python scripts/main.py ../../community_maintenance -v
```

## 命令行参数

| 参数 | 说明 | 默认值 |

| `input_dir` | 案例文件所在目录路径（必填） | - |
| `-o, --output` | 输出报告文件路径（可选，支持 .md 格式） | 不保存 |
| `-v, --verbose` | 显示详细信息 | 不显示 |
| `-r, --recursive` | 递归扫描子目录 | 开启 |
| `--no-recursive` | 不递归扫描子目录 | - |

## 标签识别规则

### 内核崩溃

- **关键词**：panic、oops、崩溃、挂死、卡死、死机、重启、kernel panic、kernel oops
- **模式**：Kernel panic、BUG: unable to handle、general protection fault

### 网络问题

- **关键词**：网络、网卡、网口、tcp、ip、连接、ssh、ping、网络不可达、网络超时、网络中断
- **模式**：network error、connection refused、no route to host

### 存储问题

- **关键词**：磁盘、硬盘、nvme、raid、xfs、文件系统、存储、io error、i/o error、读写错误
- **模式**：input/output error、filesystem corruption、disk full

### OOM

- **关键词**：oom、内存、out of memory、内存溢出、内存不足、内存泄漏
- **模式**：Out of memory、OOM killer、memory allocation failure

### 硬件故障

- **关键词**：硬件、hardware、pcie、i2c、sas、故障、损坏、异常、过温、过热
- **模式**：hardware error、PCIe error、thermal error

### 启动问题

- **关键词**：启动、boot、grub、pxe、安装、引导、启动失败、启动超时
- **模式**：boot failed、grub error、pxe error

### 驱动问题

- **关键词**：驱动、driver、module、模块、加载失败、初始化失败
- **模式**：driver error、module failed、failed to load

### CPU问题

- **关键词**：cpu、硬锁、软锁、lockup、过热、过温、cpu error、cpu freq
- **模式**：softlockup、hardlockup、CPU temperature

### 服务异常

- **关键词**：服务、service、daemon、systemd、进程、进程异常、服务失败
- **模式**：service failed、daemon died、process terminated

### 性能问题

- **关键词**：性能、劣化、缓慢、卡顿、延迟、响应慢、吞吐量、性能下降
- **模式**：performance degradation、slow response、high latency

## 输出格式

### 控制台输出

======================================================================

案例标签自动分类报告

======================================================================
总案例数: 332
已打标签: 328 (98.8%)
未打标签: 4

标签分布:
  内核崩溃: 156 个案例
  网络问题: 76 个案例
  硬件故障: 125 个案例
  驱动问题: 123 个案例
  启动问题: 151 个案例

======================================================================

### 详细模式输出（-v）

未打标签的案例:

- 无标签案例.txt
- 测试案例.txt

### Markdown 报告文件

使用 `-o` 参数保存报告时，生成 Markdown 格式的详细报告，包含：

- 统计摘要
- 标签分布表
- 未打标签的案例列表
- 案例标签详情（包含置信度）

## 依赖

本工具仅使用 Python 标准库，无需额外安装依赖。

## 使用示例

### 示例 1：快速标签分类

```bash
python scripts/main.py ../../community_maintenance
```

快速为所有案例打标签，显示标签分布统计。

### 示例 2：生成详细报告

```bash
python scripts/main.py ../../community_maintenance -o tag_report.md -v
```

生成详细的 Markdown 报告文件，包含所有案例的标签详情。

### 示例 3：检查新案例

```bash
python scripts/main.py ./new_cases -o new_cases_tags.md
```

为新增案例打标签并生成报告。

## 置信度计算

工具会为每个标签计算置信度（0-100%）：

- 每个关键词匹配 +1 分
- 每个模式匹配 +2 分
- 置信度 = min(100, 分数 × 10)

置信度越高，表示标签匹配越准确。

## 扩展开发

如需添加新的标签类型，可以修改 `scripts/main.py` 中的 `tag_rules` 字典：

```python
self.tag_rules = {
    '新标签': {
        'keywords': ['关键词1', '关键词2'],
        'patterns': ['模式1', '模式2']
    },
    # 其他标签...
}
```

## 注意事项

1. 工具会为每个案例匹配多个标签（如果符合多个标签规则）
2. 置信度仅供参考，不代表绝对准确性
3. 对于内容较少的案例，可能无法准确打标签
4. 工具会自动忽略非 .txt 和 .md 文件

## 质量建议

- 案例描述应包含具体的错误信息和现象，便于标签识别
- 对于复杂案例，可能需要手动调整标签
- 定期更新标签规则，以适应新的故障类型
