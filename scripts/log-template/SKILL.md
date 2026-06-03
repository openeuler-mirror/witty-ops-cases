---
name: log-template
description: 从 txt/md/xlsx/pdf/docx 故障文档生成标准化故障案例模板，支持 PDF/DOCX 内嵌图片的多模态大模型解析。当用户需要故障案例生成或者提到故障案例、故障文档、标准化模板等时使用。
---

# 故障案例模板生成

## 触发场景

- 用户有故障分析文档需要标准化
- 用户提到故障案例、故障文档、标准化模板
- 用户需要将零散故障文档转化为统一格式的知识库
- 用户有含截图/图表的 PDF 或 Word 故障报告

## 执行方式

在 log-template 目录下运行（或确保 scripts/ 可访问）：

```bash
# 处理单个文件
python scripts/template.py file <文件路径>

# 递归处理文件夹（含子目录）
python scripts/template.py folder <文件夹路径>

# 指定输出目录（默认 scripts/output，运行时自动创建，无需预置样例文件）
python scripts/template.py -o <输出目录> file <路径>
python scripts/template.py -o <输出目录> folder <路径>
```

## 支持格式

| 格式 | 解析方式 |
|------|----------|
| txt, md | 全文作为一个案例 |
| pdf, docx | 全文作为一个案例，提取内嵌图片；PDF 文本过少时额外渲染页面截图 |
| xlsx | 第一行表头，每行一个案例（列名: 值） |

pdf/docx 含图片时会以多模态方式发送给大模型，需配置支持视觉能力的模型（如 qwen3-vl-max）。

## 输出模板格式

生成结果包含以下字段：

- **#标题**：简明故障名称
- **#内核版本**：如 2403sp2，无则写「未知」
- **#问题现象**：可观测现象、日志特征、服务异常
- **#问题根因**：根本原因
- **#解决方案**：可操作的解决措施

模型在文档不合适时会输出 `#跳过`，脚本会识别并跳过该条，不写入文件。

## 依赖

```bash
pip install -r scripts/requirements.txt
```

需安装：openai, openpyxl, pymupdf, python-docx

## 配置

- **scripts/config.json**：api_key、base_url、model、timeout、max_images 等
- **scripts/prompt.txt**：提示词模板，必须包含 `{content}` 占位符

| 配置项 | 说明 |
|--------|------|
| model | 建议使用支持视觉的多模态模型（处理 pdf/docx 图片） |
| max_images | 单次请求最多发送的图片数，默认 20 |

修改 prompt 或 config 后无需改代码，脚本启动时自动加载。

## 示例

```bash
python scripts/template.py file ./故障分析.pdf
python scripts/template.py folder ./docs -o ./output
```
