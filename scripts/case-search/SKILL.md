---
name: case-search
description: 案例搜索工具，根据关键词快速搜索案例，支持标题、内容、标签等多维度搜索，支持正则表达式和内核版本过滤。
---

# 案例搜索工具

## 功能概述

本工具用于根据关键词快速搜索故障案例，支持多维度搜索（标题、内容、标签等），支持正则表达式和内核版本过滤，帮助快速定位相似故障。

### 搜索维度

1. **标题搜索** - 搜索案例标题
2. **内容搜索** - 搜索案例全文内容
3. **现象搜索** - 搜索问题现象字段
4. **根因搜索** - 搜索问题根因字段
5. **解决方案搜索** - 搜索解决方案字段
6. **标签搜索** - 搜索案例标签
7. **内核版本过滤** - 按内核版本筛选

## 触发场景

- 遇到新故障，搜索历史相似案例
- 按关键词查找特定类型的问题
- 按内核版本查找相关问题
- 快速定位特定硬件或软件的故障

## 执行方式

在 `case-search` 目录下运行：

```bash
# 基本用法 - 搜索关键词
python scripts/main.py <案例目录> <关键词>

# 示例：搜索包含 "panic" 的案例
python scripts/main.py ../../community_maintenance panic

# 搜索多个关键词
python scripts/main.py ../../community_maintenance "kernel panic" oops

# 只在标题中搜索
python scripts/main.py ../../community_maintenance panic -f title

# 使用正则表达式
python scripts/main.py ../../community_maintenance "网络.*故障" --regex

# 按内核版本过滤
python scripts/main.py ../../community_maintenance oom -k 22.03

# 保存搜索结果到文件
python scripts/main.py ../../community_maintenance panic -o search_result.md

# 显示更多结果
python scripts/main.py ../../community_maintenance panic -m 50
```

## 命令行参数

| 参数 | 说明 | 默认值 |
| `case_dir` | 案例文件所在目录路径（必填） | - |
| `keywords` | 搜索关键词，可指定多个（必填） | - |
| `-f, --fields` | 搜索字段，逗号分隔 | title,content |
| `-k, --kernel` | 内核版本过滤 | 不过滤 |
| `-r, --regex` | 使用正则表达式 | 不使用 |
| `-c, --case-sensitive` | 区分大小写 | 不区分 |
| `-m, --max` | 最大显示结果数 | 20 |
| `-o, --output` | 输出结果到文件 | 不保存 |

### 支持的搜索字段

- `title` - 案例标题
- `content` - 案例全文
- `phenomenon` - 问题现象
- `root_cause` - 问题根因
- `solution` - 解决方案
- `tags` - 案例标签

## 输出格式

### 控制台输出

================================================================================

找到 15 个匹配案例（显示前 15 个）

================================================================================

[1] CPU过温引发Kernel Panic
    文件: CPU过温引发Kernel Panic.txt
    内核版本: 22.03 SP4
    匹配字段: title,content
    匹配次数: 3
    预览: ...系统在高负载运行过程中，CPU2因温度超过安全阈值，触发"Kernel panic - not syncing: Fatal hardware error!"错误...

[2] 920B NVMe测试触发内核hard lockup问题
    文件: 920B NVMe测试触发内核hard lockup问题.txt
    内核版本: 22.03 SP4
    匹配字段: content
    匹配次数: 2
    预览: ...在NVMe硬盘压力测试过程中，系统触发hard lockup，内核日志显示"Watchdog detected hard LOCKUP on cpu"...

### Markdown 报告文件

使用 `-o` 参数保存报告时，生成 Markdown 格式的详细报告，包含：

- 搜索时间和参数
- 所有匹配案例的详细信息
- 文件路径、内核版本、匹配字段
- 预览内容

## 搜索技巧

### 1. 多关键词搜索

```bash
# 搜索同时包含 "kernel" 和 "panic" 的案例
python scripts/main.py ../../community_maintenance kernel panic
```

### 2. 正则表达式搜索

```bash
# 搜索以 "CPU" 开头的案例
python scripts/main.py ../../community_maintenance "^CPU" --regex -f title

# 搜索包含数字的案例
python scripts/main.py ../../community_maintenance "\d+" --regex
```

### 3. 指定字段搜索

```bash
# 只在标题和现象中搜索
python scripts/main.py ../../community_maintenance oom -f title,phenomenon

# 只在解决方案中搜索
python scripts/main.py ../../community_maintenance "升级内核" -f solution
```

### 4. 组合过滤

```bash
# 搜索 22.03 版本的内核崩溃问题
python scripts/main.py ../../community_maintenance panic -k 22.03 -f title,content
```

### 5. 区分大小写搜索

```bash
# 区分大小写搜索 "OOM"
python scripts/main.py ../../community_maintenance OOM --case-sensitive
```

## 依赖

本工具仅使用 Python 标准库，无需额外安装依赖。

## 使用示例

### 示例 1：快速搜索

```bash
python scripts/main.py ../../community_maintenance panic
```

快速搜索所有包含 "panic" 的案例。

### 示例 2：精确搜索标题

```bash
python scripts/main.py ../../community_maintenance "CPU" -f title
```

只在案例标题中搜索包含 "CPU" 的案例。

### 示例 3：按内核版本查找

```bash
python scripts/main.py ../../community_maintenance "网络" -k 24.03
```

搜索 24.03 内核版本中与网络相关的案例。

### 示例 4：保存搜索结果

```bash
python scripts/main.py ../../community_maintenance "oom" "内存" -o oom_cases.md -m 100
```

搜索 OOM 相关案例，最多显示 100 个结果，并保存到文件。

### 示例 5：使用正则表达式

```bash
python scripts/main.py ../../community_maintenance "(panic|oops|崩溃)" --regex
```

使用正则表达式搜索包含 panic、oops 或 崩溃 的案例。

## 搜索结果排序

搜索结果按匹配次数从高到低排序，匹配次数越多的案例越相关。

## 注意事项

1. 搜索不区分大小写（除非使用 `--case-sensitive`）
2. 多个关键词之间是"与"关系（同时满足）
3. 正则表达式语法遵循 Python re 模块
4. 预览内容显示关键词前后 50 个字符
5. 默认最多显示 20 个结果

## 性能优化

- 工具会在启动时加载所有案例文件到内存
- 搜索速度取决于案例数量和关键词复杂度
- 对于大型案例库，建议使用更精确的关键词

## 扩展开发

如需添加新的搜索功能，可以修改 `scripts/main.py`：

1. 添加新的搜索字段
2. 实现自定义排序算法
3. 添加模糊匹配功能
4. 支持更多输出格式
