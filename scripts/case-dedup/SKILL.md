---
name: case-dedup
description: 案例去重检测器，检测内容相似或重复的故障案例，基于标题相似度和内容哈希值比对，生成去重报告。
---

# 案例去重检测器

## 功能概述

本工具用于检测案例库中内容相似或重复的故障案例，基于标题相似度和内容哈希值比对，帮助保持知识库整洁，避免冗余。

### 检测类型

1. **完全重复** - 内容哈希值完全相同（建议删除）
2. **高度相似** - 标题和内容相似度均超过阈值（建议合并）
3. **标题相似** - 标题高度相似但内容差异较大（需人工确认）

## 触发场景

- 定期清理案例库，删除重复案例
- 批量导入案例前的重复检查
- 案例库维护和质量提升
- 发现潜在的案例合并机会

## 执行方式

在 `case-dedup` 目录下运行：

```bash
# 基本用法 - 检测目录中的重复案例
python scripts/main.py <案例目录路径>

# 示例：检测 community_maintenance 目录
python scripts/main.py ../../community_maintenance

# 生成详细报告并保存到文件
python scripts/main.py ../../community_maintenance -o dedup_report.md -v

# 调整相似度阈值
python scripts/main.py ../../community_maintenance --title-threshold 0.9 --content-threshold 0.8

# 不递归扫描子目录
python scripts/main.py ../../community_maintenance --no-recursive
```

## 命令行参数

| 参数 | 说明 | 默认值 |
| `case_dir` | 案例文件所在目录路径（必填） | - |
| `-o, --output` | 输出报告文件路径（可选） | 不保存 |
| `-v, --verbose` | 显示详细信息 | 不显示 |
| `--title-threshold` | 标题相似度阈值 | 0.85 |
| `--content-threshold` | 内容相似度阈值 | 0.75 |
| `--no-recursive` | 不递归扫描子目录 | 递归 |

## 相似度计算

### 标题相似度

使用 Python `difflib.SequenceMatcher` 计算两个标题的相似度：

- 忽略大小写
- 基于字符级别的最长公共子序列

### 内容相似度

基于核心内容（问题现象 + 根因 + 解决方案）计算：

- 将内容按行分割
- 计算行的交集和并集
- 相似度 = 交集大小 / 并集大小

### 内容哈希

使用 MD5 哈希检测完全重复：

1. 去除所有空白字符
2. 转换为小写
3. 计算 MD5 哈希值

## 输出格式

### 控制台输出

================================================================================

案例去重检测报告

================================================================================
总案例数: 332
重复/相似组数: 5
涉及文件数: 10

⚠ 完全重复: 2 组（建议删除）
⚡ 高度相似: 2 组（建议合并）
❓ 标题相似: 1 组（需人工确认）

================================================================================

### 详细模式输出（-v）

详细检测结果:

[1] 完全重复（内容哈希相同）
    相似度: 100.0%
    案例A: CPU过温引发Kernel Panic.txt
           标题: CPU过温引发Kernel Panic...
    案例B: CPU过温引发Kernel Panic_1.txt
           标题: CPU过温引发Kernel Panic...
    原因: 内容完全一致

[2] 高度相似
    相似度: 88.5%
    案例A: 网络连接超时问题.txt
           标题: 网络连接超时导致服务不可用...
    案例B: 网络超时故障分析.txt
           标题: 网络超时导致的服务异常...
    原因: 标题相似度: 85.0%, 内容相似度: 92.0%

### Markdown 报告文件

使用 `-o` 参数保存报告时，生成 Markdown 格式的详细报告，包含：

- 统计摘要
- 重复/相似案例的详细信息
- 文件路径、标题、内核版本
- 相似度和判断依据

## 阈值设置建议

### 保守设置（严格匹配）

```bash
python scripts/main.py ../../community_maintenance --title-threshold 0.95 --content-threshold 0.90
```

- 只检测几乎完全相同的案例
- 误报率低，但可能漏掉一些相似案例

### 宽松设置（发现潜在相似）

```bash
python scripts/main.py ../../community_maintenance --title-threshold 0.75 --content-threshold 0.60
```

- 检测更多潜在的相似案例
- 需要更多人工确认

### 默认设置（平衡）

```bash
python scripts/main.py ../../community_maintenance
```

- 标题阈值：0.85
- 内容阈值：0.75
- 适合大多数场景

## 依赖

本工具仅使用 Python 标准库，无需额外安装依赖。

## 使用示例

### 示例 1：快速检测

```bash
python scripts/main.py ../../community_maintenance
```

快速检测案例库中的重复案例，显示统计摘要。

### 示例 2：生成详细报告

```bash
python scripts/main.py ../../community_maintenance -o dedup_report.md -v
```

生成详细的 Markdown 报告，包含所有重复/相似案例的详细信息。

### 示例 3：严格检测

```bash
python scripts/main.py ../../community_maintenance --title-threshold 0.95 --content-threshold 0.90 -v
```

使用严格的阈值，只检测几乎完全相同的案例。

### 示例 4：检查特定目录

```bash
python scripts/main.py ./new_cases --title-threshold 0.80
```

检查新增案例目录，使用较宽松的阈值发现潜在相似案例。

## 处理建议

### 完全重复

**建议操作**：删除其中一个案例

- 保留更完整的版本
- 保留文件名更规范的版本
- 保留更新日期更近的版本

### 高度相似

**建议操作**：合并为一个案例

- 整合两个案例的优点
- 补充更详细的解决方案
- 更新内核版本信息

### 标题相似

**建议操作**：人工确认

- 检查是否为同一问题的不同表现
- 检查是否为不同场景下的相似问题
- 决定是合并还是分别保留

## 集成建议

### CI/CD 集成

将去重检测集成到 CI/CD 流程中，防止重复案例入库：

```bash
# 在 CI 脚本中添加
python scripts/case-dedup/scripts/main.py ./cases
if [ $? -ne 0 ]; then
    echo "检测到重复案例，请检查并清理"
    exit 1
fi
```

### 定期清理

建议每月或每季度运行一次去重检测，保持案例库整洁。

## 注意事项

1. 工具不会自动删除或修改任何案例文件
2. 所有操作建议都需要人工确认后执行
3. 相似度计算基于文本内容，可能无法识别语义相似但表述不同的案例
4. 对于大型案例库，检测可能需要较长时间

## 性能优化

- 工具会先计算内容哈希，快速识别完全重复的案例
- 相似度计算只在哈希不同的案例之间进行
- 对于大型案例库，建议使用更精确的阈值减少计算量
