#!/usr/bin/env python3
"""案例搜索工具（增强版）- 根据关键词快速搜索案例"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class SearchResult:
    """搜索结果（普通类，兼容 Python 3.6+）"""
    def __init__(self, file_path: str, file_name: str, title: str,
                 kernel_version: str, matched_fields: List[str],
                 match_count: int, preview: str):
        self.file_path = file_path
        self.file_name = file_name
        self.title = title
        self.kernel_version = kernel_version
        self.matched_fields = matched_fields
        self.match_count = match_count
        self.preview = preview


class CaseSearcher:
    """案例搜索器（流式处理）"""

    def __init__(self, case_dir: str):
        self.case_dir = Path(case_dir)
        # 支持的文件扩展名
        self.extensions = ('.txt', '.md')

    def _parse_case(self, file_path: Path) -> Optional[Dict]:
        """解析单个案例文件"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            case = {
                'file_path': str(file_path),
                'file_name': file_path.name,
                'content': content,
                'title': self._extract_field(content, ['#标题', '# 标题', '##标题', '## 标题']),
                'kernel_version': self._extract_field(content, ['#内核版本', '# 内核版本', '##内核版本', '## 内核版本']),
                'phenomenon': self._extract_field(content, ['#问题现象', '# 问题现象', '##问题现象', '## 问题现象']),
                'root_cause': self._extract_field(content, ['#问题根因', '# 问题根因', '#根因', '##问题根因', '## 问题根因', '##根因']),
                'solution': self._extract_field(content, ['#解决方案', '# 解决方案', '##解决方案', '## 解决方案']),
                'tags': self._extract_field(content, ['#标签', '# 标签', '##标签', '## 标签']),
            }

            if not case['title']:
                case['title'] = file_path.stem
            return case

        except Exception:
            return None

    def _extract_field(self, content: str, markers: List[str]) -> str:
        """提取字段内容（支持多种标题格式）"""
        lines = content.split('\n')
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            for marker in markers:
                if line_stripped.startswith(marker):
                    # 检查同一行是否有内容
                    content_start = line_stripped[len(marker):].strip()
                    if content_start:
                        return content_start
                    # 收集后续行直到下一个标题或空行
                    if i + 1 < len(lines):
                        result = []
                        for j in range(i + 1, len(lines)):
                            next_line = lines[j].strip()
                            # 遇到新的标题（以#开头）或连续空行时停止
                            if next_line.startswith('#') or (next_line == '' and result):
                                break
                            if next_line:
                                result.append(next_line)
                        return '\n'.join(result).strip()
        return ""

    def _match_keyword(self, text: str, keyword: str, use_regex: bool, case_sensitive: bool) -> int:
        """返回关键词在文本中的匹配次数"""
        if not text:
            return 0
        if use_regex:
            try:
                flags = 0 if case_sensitive else re.IGNORECASE
                return len(re.findall(keyword, text, flags))
            except re.error:
                return 0
        else:
            if not case_sensitive:
                keyword = keyword.lower()
                text = text.lower()
            return text.count(keyword)

    def _generate_preview(self, case: Dict, matched_fields: List[str],
                         keywords: List[str], use_regex: bool, case_sensitive: bool) -> str:
        """生成更准确的预览片段（在匹配字段中查找上下文）"""
        # 优先从 phenomenon 字段提取预览
        preview_source = case.get('phenomenon', '')
        if not preview_source:
            # 如果 phenomenon 为空，从其他匹配字段中选择第一个非空字段
            for field in matched_fields:
                if field in case and case[field]:
                    preview_source = case[field]
                    break
        if not preview_source:
            preview_source = case.get('content', '')

        if not preview_source:
            return ""

        # 找到第一个关键词出现的位置（所有关键词中最靠前的）
        best_pos = -1
        for keyword in keywords:
            if use_regex:
                try:
                    flags = 0 if case_sensitive else re.IGNORECASE
                    match = re.search(keyword, preview_source, flags)
                    if match and (best_pos == -1 or match.start() < best_pos):
                        best_pos = match.start()
                except re.error:
                    continue
            else:
                search_content = preview_source if case_sensitive else preview_source.lower()
                search_keyword = keyword if case_sensitive else keyword.lower()
                pos = search_content.find(search_keyword)
                if pos != -1 and (best_pos == -1 or pos < best_pos):
                    best_pos = pos

        if best_pos == -1:
            best_pos = 0

        start = max(0, best_pos - 50)
        end = min(len(preview_source), best_pos + 150)
        preview = preview_source[start:end]
        if start > 0:
            preview = '...' + preview
        if end < len(preview_source):
            preview = preview + '...'
        return preview.replace('\n', ' ')

    def search(
        self,
        keywords: List[str],
        search_fields: Optional[List[str]] = None,
        kernel_version: Optional[str] = None,
        use_regex: bool = False,
        case_sensitive: bool = False
    ) -> List[SearchResult]:
        """流式搜索案例（动态遍历目录）"""
        if not keywords:
            return []

        if search_fields is None:
            search_fields = ['title', 'content']

        results = []

        # 遍历目录中的所有支持文件
        for ext in self.extensions:
            for file_path in self.case_dir.rglob(f'*{ext}'):
                if not file_path.is_file():
                    continue

                case = self._parse_case(file_path)
                if not case:
                    continue

                # 内核版本过滤
                if kernel_version and kernel_version.lower() not in case['kernel_version'].lower():
                    continue

                matched_fields = []
                total_matches = 0

                # 对每个关键词在指定字段中计数
                for keyword in keywords:
                    keyword_matches = 0
                    for field in search_fields:
                        field_content = case.get(field, '')
                        if not field_content:
                            continue
                        matches = self._match_keyword(field_content, keyword, use_regex, case_sensitive)
                        if matches > 0:
                            keyword_matches += matches
                            if field not in matched_fields:
                                matched_fields.append(field)
                    total_matches += keyword_matches

                if total_matches > 0:
                    preview = self._generate_preview(case, matched_fields, keywords, use_regex, case_sensitive)
                    results.append(SearchResult(
                        file_path=case['file_path'],
                        file_name=case['file_name'],
                        title=case['title'],
                        kernel_version=case['kernel_version'],
                        matched_fields=matched_fields,
                        match_count=total_matches,
                        preview=preview
                    ))

        # 按匹配次数排序
        results.sort(key=lambda x: x.match_count, reverse=True)
        return results


def print_search_results(results: List[SearchResult], max_results: int = 20):
    """打印搜索结果"""
    if not results:
        print('未找到匹配的案例')
        return

    print('=' * 80)
    print(f'找到 {len(results)} 个匹配案例（显示前 {min(len(results), max_results)} 个）')
    print('=' * 80)
    print()

    for i, result in enumerate(results[:max_results], 1):
        print(f'[{i}] {result.title}')
        print(f'    文件: {result.file_name}')
        if result.kernel_version:
            print(f'    内核版本: {result.kernel_version}')
        print(f'    匹配字段: {", ".join(result.matched_fields)}')
        print(f'    匹配次数: {result.match_count}')
        if result.preview:
            print(f'    预览: {result.preview}')
        print()

    if len(results) > max_results:
        print(f'... 还有 {len(results) - max_results} 个结果未显示')
        print()


def save_results_to_file(results: List[SearchResult], output_path: str):
    """保存搜索结果到文件"""
    from datetime import datetime
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        '# 案例搜索结果',
        '',
        f'搜索时间: {datetime.now().isoformat()}',
        f'找到案例数: {len(results)}',
        '',
    ]

    for i, result in enumerate(results, 1):
        lines.append(f'## [{i}] {result.title}')
        lines.append(f'**文件**: `{result.file_path}`')
        if result.kernel_version:
            lines.append(f'**内核版本**: {result.kernel_version}')
        lines.append(f'**匹配字段**: {", ".join(result.matched_fields)}')
        lines.append(f'**匹配次数**: {result.match_count}')
        if result.preview:
            lines.append(f'**预览**: {result.preview}')
        lines.append('')

    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def main():
    parser = argparse.ArgumentParser(
        description='案例搜索工具 - 根据关键词快速搜索案例',
        epilog='''
示例:
  python scripts/main.py ../../community_maintenance panic
  python scripts/main.py ../../community_maintenance "kernel panic" "oops" -f title,content
  python scripts/main.py ../../community_maintenance "网络.*故障" --regex
  python scripts/main.py ../../community_maintenance oom -k 22.03 -o search_result.md
        '''
    )

    parser.add_argument('case_dir', help='案例文件所在目录路径')
    parser.add_argument('keywords', nargs='+', help='搜索关键词（可多个）')
    parser.add_argument('-f', '--fields', help='搜索字段，逗号分隔（title,content,phenomenon,root_cause,solution,tags）')
    parser.add_argument('-k', '--kernel', help='内核版本过滤')
    parser.add_argument('-r', '--regex', action='store_true', help='使用正则表达式')
    parser.add_argument('-c', '--case-sensitive', action='store_true', help='区分大小写')
    parser.add_argument('-m', '--max', type=int, default=20, help='最大显示结果数（默认20）')
    parser.add_argument('-o', '--output', help='输出结果到文件')

    args = parser.parse_args()

    case_dir = Path(args.case_dir).resolve()
    if not case_dir.exists():
        print(f'错误: 目录不存在: {case_dir}')
        sys.exit(1)

    # 解析搜索字段
    search_fields = None
    if args.fields:
        search_fields = [f.strip() for f in args.fields.split(',')]

    print(f'正在搜索: {" ".join(args.keywords)}')
    print(f'搜索目录: {case_dir}')
    if search_fields:
        print(f'搜索字段: {", ".join(search_fields)}')
    if args.kernel:
        print(f'内核版本: {args.kernel}')
    print()

    searcher = CaseSearcher(str(case_dir))
    results = searcher.search(
        keywords=args.keywords,
        search_fields=search_fields,
        kernel_version=args.kernel,
        use_regex=args.regex,
        case_sensitive=args.case_sensitive
    )

    print_search_results(results, max_results=args.max)

    if args.output:
        save_results_to_file(results, args.output)
        print(f'结果已保存到: {args.output}')


if __name__ == '__main__':
    main()