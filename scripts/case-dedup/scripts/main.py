#!/usr/bin/env python3
"""案例去重检测器（简化版）"""

import argparse
import hashlib
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
from difflib import SequenceMatcher
from datetime import datetime


class CaseDedupDetector:
    def __init__(self, title_thresh=0.85, content_thresh=0.75):
        self.title_thresh = title_thresh
        self.content_thresh = content_thresh
        self.cases = []

    def load_cases(self, case_dir: str, recursive: bool = True):
        path = Path(case_dir)
        if not path.exists():
            return
        pattern = '**/*' if recursive else '*'
        for file_path in path.glob(pattern):
            if file_path.is_file() and file_path.suffix.lower() in ('.txt', '.md'):
                case = self._parse_case(file_path)
                if case:
                    self.cases.append(case)

    def _parse_case(self, file_path: Path) -> dict:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # 标题提取
            title = self._extract_field(content, ['#标题', '# 标题', '##标题', '## 标题']) or file_path.stem
            # 内核版本
            kernel = self._extract_field(content, ['#内核版本', '# 内核版本', '##内核版本', '## 内核版本'])
            # 核心内容（现象+根因+方案）
            core_parts = []
            for marker in [
                ['#问题现象', '# 问题现象', '##问题现象', '## 问题现象'],
                ['#问题根因', '# 问题根因', '#根因', '##问题根因', '## 问题根因', '##根因'],
                ['#解决方案', '# 解决方案', '##解决方案', '## 解决方案']
            ]:
                part = self._extract_field(content, marker)
                if part:
                    core_parts.append(part)
            core = '\n'.join(core_parts)

            # 标准化哈希
            def h(t): return hashlib.md5(re.sub(r'\s+', '', t.lower()).encode()).hexdigest()
            return {
                'path': str(file_path),
                'name': file_path.name,
                'title': title,
                'kernel': kernel,
                'core': core,
                'title_hash': h(title),
                'content_hash': h(core)
            }
        except Exception:
            return None

    def _extract_field(self, content: str, markers: List[str]) -> str:
        lines = content.split('\n')
        for i, line in enumerate(lines):
            line = line.strip()
            for m in markers:
                if line.startswith(m):
                    rest = line[len(m):].strip()
                    if rest:
                        return rest
                    # 收集后续行直到下一个标题或空行
                    if i + 1 < len(lines):
                        result = []
                        for j in range(i+1, len(lines)):
                            nxt = lines[j].strip()
                            if nxt.startswith('#') or (nxt == '' and result):
                                break
                            if nxt:
                                result.append(nxt)
                        return '\n'.join(result).strip()
        return ""

    def detect_duplicates(self) -> List[dict]:
        dup = []
        checked = set()

        # 1. 精确哈希匹配
        hash_groups = {}
        for i, c in enumerate(self.cases):
            h = c['content_hash']
            hash_groups.setdefault(h, []).append(i)
        for indices in hash_groups.values():
            if len(indices) > 1:
                for i in range(len(indices)):
                    for j in range(i+1, len(indices)):
                        idx1, idx2 = indices[i], indices[j]
                        if (idx1, idx2) not in checked:
                            checked.add((idx1, idx2))
                            dup.append({
                                'case1': self.cases[idx1],
                                'case2': self.cases[idx2],
                                'sim': 1.0,
                                'type': '完全重复',
                                'reason': '内容哈希相同'
                            })

        # 2. 标题+内容相似度
        for i in range(len(self.cases)):
            for j in range(i+1, len(self.cases)):
                if (i, j) in checked:
                    continue
                c1, c2 = self.cases[i], self.cases[j]
                t_sim = SequenceMatcher(None, c1['title'].lower(), c2['title'].lower()).ratio()
                if t_sim >= self.title_thresh:
                    # 内容相似度（基于行Jaccard）
                    lines1 = set(l.strip().lower() for l in c1['core'].split('\n') if l.strip())
                    lines2 = set(l.strip().lower() for l in c2['core'].split('\n') if l.strip())
                    c_sim = len(lines1 & lines2) / len(lines1 | lines2) if (lines1 | lines2) else 0.0

                    if c_sim >= self.content_thresh:
                        checked.add((i, j))
                        dup.append({
                            'case1': c1, 'case2': c2,
                            'sim': (t_sim + c_sim) / 2,
                            'type': '高度相似',
                            'reason': f'标题:{t_sim:.1%} 内容:{c_sim:.1%}'
                        })
                    elif t_sim >= 0.95:
                        checked.add((i, j))
                        dup.append({
                            'case1': c1, 'case2': c2,
                            'sim': t_sim,
                            'type': '标题相似（需确认）',
                            'reason': f'标题相似度 {t_sim:.1%}'
                        })

        dup.sort(key=lambda x: x['sim'], reverse=True)
        return dup

    def generate_report(self, dup: List[dict]) -> dict:
        exact = sum(1 for d in dup if d['type'] == '完全重复')
        high = sum(1 for d in dup if d['type'] == '高度相似')
        title = sum(1 for d in dup if d['type'] == '标题相似（需确认）')
        files = {d['case1']['path'] for d in dup} | {d['case2']['path'] for d in dup}
        return {
            'total': len(self.cases),
            'groups': len(dup),
            'exact': exact,
            'high': high,
            'title': title,
            'files': len(files),
            'duplicates': dup
        }


def print_report(report: dict, verbose: bool):
    print('=' * 80)
    print('案例去重检测报告')
    print('=' * 80)
    print(f"总案例数: {report['total']}")
    print(f"重复/相似组数: {report['groups']}")
    print(f"涉及文件数: {report['files']}\n")
    print(f"⚠ 完全重复: {report['exact']} 组（建议删除）")
    print(f"⚡ 高度相似: {report['high']} 组（建议合并）")
    print(f"❓ 标题相似: {report['title']} 组（需人工确认）\n")

    if verbose and report['duplicates']:
        print('详细检测结果:\n')
        for i, d in enumerate(report['duplicates'][:20], 1):
            print(f"[{i}] {d['type']}")
            print(f"    相似度: {d['sim']:.1%}")
            print(f"    案例A: {d['case1']['name']} - {d['case1']['title'][:60]}")
            print(f"    案例B: {d['case2']['name']} - {d['case2']['title'][:60]}")
            print(f"    原因: {d['reason']}\n")
        if len(report['duplicates']) > 20:
            print(f"... 还有 {len(report['duplicates'])-20} 组未显示\n")
    print('=' * 80)


def save_report(report: dict, output: str):
    lines = [
        '# 案例去重检测报告',
        f'生成时间: {datetime.now().isoformat()}\n',
        '## 统计摘要',
        f'- 总案例数: {report["total"]}',
        f'- 重复/相似组数: {report["groups"]}',
        f'- 涉及文件数: {report["files"]}',
        f'- 完全重复: {report["exact"]} 组',
        f'- 高度相似: {report["high"]} 组',
        f'- 标题相似: {report["title"]} 组\n'
    ]
    if report['duplicates']:
        lines.append('## 详细检测结果\n')
        for i, d in enumerate(report['duplicates'], 1):
            lines.extend([
                f'### [{i}] {d["type"]}',
                f'**相似度**: {d["sim"]:.1%}',
                '',
                '**案例A**:',
                f'- 文件: `{d["case1"]["path"]}`',
                f'- 标题: {d["case1"]["title"]}',
                f'- 内核版本: {d["case1"]["kernel"] or "未知"}',
                '',
                '**案例B**:',
                f'- 文件: `{d["case2"]["path"]}`',
                f'- 标题: {d["case2"]["title"]}',
                f'- 内核版本: {d["case2"]["kernel"] or "未知"}',
                '',
                f'**判断依据**: {d["reason"]}\n'
            ])
    Path(output).write_text('\n'.join(lines), encoding='utf-8')


def main():
    p = argparse.ArgumentParser(description='案例去重检测器')
    p.add_argument('case_dir', help='案例目录')
    p.add_argument('-o', '--output', help='输出报告文件')
    p.add_argument('-v', '--verbose', action='store_true', help='详细输出')
    p.add_argument('--title-threshold', type=float, default=0.85, help='标题相似度阈值')
    p.add_argument('--content-threshold', type=float, default=0.75, help='内容相似度阈值')
    p.add_argument('--no-recursive', action='store_true', help='不递归子目录')
    args = p.parse_args()

    dir_path = Path(args.case_dir).resolve()
    if not dir_path.exists():
        print(f'错误: 目录不存在: {dir_path}')
        sys.exit(1)

    print('正在加载案例...')
    detector = CaseDedupDetector(args.title_threshold, args.content_threshold)
    detector.load_cases(str(dir_path), recursive=not args.no_recursive)

    if not detector.cases:
        print('警告: 未找到案例文件')
        sys.exit(0)

    print(f'已加载 {len(detector.cases)} 个案例')
    print('正在检测重复...')
    duplicates = detector.detect_duplicates()
    report = detector.generate_report(duplicates)

    print_report(report, args.verbose)
    if args.output:
        save_report(report, args.output)
        print(f'报告已保存: {args.output}')

    if report['groups'] > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()