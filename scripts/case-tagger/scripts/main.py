"""案例标签自动分类器"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Set
from collections import Counter

class CaseTagger:
    def __init__(self):
        self.tag_rules = {
            '内核崩溃': {
                'keywords': ['panic', 'oops', '崩溃', '挂死', '卡死', '死机', '重启', 'kernel panic', 'kernel oops'],
                'patterns': ['Kernel panic', 'BUG: unable to handle', 'general protection fault']
            },
            '网络问题': {
                'keywords': ['网络', '网卡', '网口', 'tcp', 'ip', '连接', 'ssh', 'ping', '网络不可达', '网络超时', '网络中断'],
                'patterns': ['network error', 'connection refused', 'no route to host']
            },
            '存储问题': {
                'keywords': ['磁盘', '硬盘', 'nvme', 'raid', 'xfs', '文件系统', '存储', 'io error', 'i/o error', '读写错误'],
                'patterns': ['input/output error', 'filesystem corruption', 'disk full']
            },
            'OOM': {
                'keywords': ['oom', '内存', 'out of memory', '内存溢出', '内存不足', '内存泄漏'],
                'patterns': ['Out of memory', 'OOM killer', 'memory allocation failure']
            },
            '硬件故障': {
                'keywords': ['硬件', 'hardware', 'pcie', 'i2c', 'sas', '故障', '损坏', '异常', '过温', '过热'],
                'patterns': ['hardware error', 'PCIe error', 'thermal error']
            },
            '启动问题': {
                'keywords': ['启动', 'boot', 'grub', 'pxe', '安装', '引导', '启动失败', '启动超时'],
                'patterns': ['boot failed', 'grub error', 'pxe error']
            },
            '驱动问题': {
                'keywords': ['驱动', 'driver', 'module', '模块', '加载失败', '初始化失败'],
                'patterns': ['driver error', 'module failed', 'failed to load']
            },
            'CPU问题': {
                'keywords': ['cpu', '硬锁', '软锁', 'lockup', '过热', '过温', 'cpu error', 'cpu freq'],
                'patterns': ['softlockup', 'hardlockup', 'CPU temperature']
            },
            '服务异常': {
                'keywords': ['服务', 'service', 'daemon', 'systemd', '进程', '进程异常', '服务失败'],
                'patterns': ['service failed', 'daemon died', 'process terminated']
            },
            '性能问题': {
                'keywords': ['性能', '劣化', '缓慢', '卡顿', '延迟', '响应慢', '吞吐量', '性能下降'],
                'patterns': ['performance degradation', 'slow response', 'high latency']
            }
        }

    def tag_file(self, file_path: str) -> Dict:
        path = Path(file_path)
        result = {
            'file_path': str(path),
            'file_name': path.name,
            'tags': set(),
            'confidence': {}
        }

        if not path.exists() or path.suffix.lower() not in ['.txt', '.md']:
            return result

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().lower()

            for tag, config in self.tag_rules.items():
                score = 0
                for keyword in config['keywords']:
                    if keyword.lower() in content:
                        score += 1
                for pattern in config['patterns']:
                    if pattern.lower() in content:
                        score += 2
                if score >= 1:
                    result['tags'].add(tag)
                    result['confidence'][tag] = min(100, score * 10)
        except Exception:
            pass

        return result

    def tag_directory(self, dir_path: str, recursive: bool = True) -> List[Dict]:
        path = Path(dir_path)
        results = []

        if not path.exists() or not path.is_dir():
            return results

        pattern = '**/*' if recursive else '*'
        for file_path in path.glob(pattern):
            if file_path.is_file() and file_path.suffix.lower() in ['.txt', '.md']:
                result = self.tag_file(str(file_path))
                results.append(result)

        return results

    def generate_report(self, results: List[Dict]) -> Dict:
        total = len(results)
        tagged = sum(1 for r in results if r['tags'])
        untagged = total - tagged

        tag_counter = Counter()
        for result in results:
            for tag in result['tags']:
                tag_counter[tag] += 1

        return {
            'total_cases': total,
            'tagged_cases': tagged,
            'untagged_cases': untagged,
            'tagged_rate': f'{tagged/total*100:.1f}%' if total > 0 else '0%',
            'tag_distribution': dict(tag_counter.most_common()),
            'details': results
        }

def print_console_report(report: Dict, verbose: bool = False):
    print('=' * 70)
    print('案例标签自动分类报告')
    print('=' * 70)
    print(f'总案例数: {report["total_cases"]}')
    print(f'已打标签: {report["tagged_cases"]} ({report["tagged_rate"]})')
    print(f'未打标签: {report["untagged_cases"]}')
    print()

    if report['tag_distribution']:
        print('标签分布:')
        for tag, count in report['tag_distribution'].items():
            print(f'  {tag}: {count} 个案例')
        print()

    if verbose and report['untagged_cases'] > 0:
        print('未打标签的案例:')
        for result in report['details']:
            if not result['tags']:
                print(f'  - {result["file_name"]}')
        print()

    print('=' * 70)

def save_report_to_file(report: Dict, output_path: str):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        '# 案例标签自动分类报告',
        '',
        f'总案例数: {report["total_cases"]}',
        f'已打标签: {report["tagged_cases"]} ({report["tagged_rate"]})',
        f'未打标签: {report["untagged_cases"]}',
        '',
    ]

    if report['tag_distribution']:
        lines.append('## 标签分布')
        lines.append('')
        lines.append('| 标签 | 案例数量 |')
        lines.append('|------|----------|')
        for tag, count in report['tag_distribution'].items():
            lines.append(f'| {tag} | {count} |')
        lines.append('')

    if report['untagged_cases'] > 0:
        lines.append('## 未打标签的案例')
        lines.append('')
        for result in report['details']:
            if not result['tags']:
                lines.append(f'- {result["file_name"]}')
        lines.append('')

    if report['tagged_cases'] > 0:
        lines.append('## 案例标签详情')
        lines.append('')
        for result in report['details']:
            if result['tags']:
                lines.append(f'### {result["file_name"]}')
                lines.append(f'**标签**: {"、".join(result["tags"])}')
                if result['confidence']:
                    conf_str = "、".join([f'{tag}: {conf}%' for tag, conf in result['confidence'].items()])
                    lines.append(f'**置信度**: {conf_str}')
                lines.append('')

    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

def main():
    parser = argparse.ArgumentParser(
        description='案例标签自动分类器 - 自动为案例打上标签',
        epilog='示例:\n  python scripts/main.py ../../community_maintenance\n  python scripts/main.py ../../community_maintenance -o report.md -v'
    )

    parser.add_argument('input_dir', help='案例文件所在目录路径')
    parser.add_argument('-o', '--output', help='输出报告文件路径（支持 .md 格式）')
    parser.add_argument('-v', '--verbose', action='store_true', help='显示详细信息')
    parser.add_argument('-r', '--recursive', action='store_true', default=True, help='递归扫描子目录')
    parser.add_argument('--no-recursive', action='store_true', help='不递归扫描子目录')

    args = parser.parse_args()

    input_path = Path(args.input_dir).resolve()
    if not input_path.exists():
        print(f'错误: 输入目录不存在: {input_path}')
        sys.exit(1)

    recursive = not args.no_recursive

    print('正在为案例打标签...')
    tagger = CaseTagger()
    results = tagger.tag_directory(str(input_path), recursive=recursive)

    if not results:
        print('警告: 未找到任何案例文件')
        sys.exit(0)

    report = tagger.generate_report(results)
    print_console_report(report, verbose=args.verbose)

    if args.output:
        save_report_to_file(report, args.output)
        print(f'报告已保存到: {args.output}')

if __name__ == '__main__':
    main()