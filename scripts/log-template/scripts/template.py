"""故障案例模板生成：从 txt/md/xlsx/pdf/docx 读取文档，调用大模型生成标准化案例。"""
import argparse
import base64
import json
import sys
from pathlib import Path

from openai import OpenAI

from parser import parse, get_supported_extensions
from parser.models import ParsedCase

SCRIPT_DIR = Path(__file__).parent.resolve()
CONFIG_PATH = SCRIPT_DIR / "config.json"
PROMPT_PATH = SCRIPT_DIR / "prompt.txt"
DEFAULT_OUTPUT_DIR = SCRIPT_DIR / "output"
SKIP_MARKER = "#跳过"
INVALID_CHARS = r'\/:*?"<>|'


def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_prompt():
    with open(PROMPT_PATH, encoding="utf-8") as f:
        return f.read()


def should_skip(result: str) -> bool:
    lines = result.strip().splitlines()
    if not lines:
        return False
    first = lines[0].strip()
    return first == SKIP_MARKER or first.startswith(SKIP_MARKER + " ")


def extract_title(result: str) -> str:
    lines = result.strip().splitlines()
    for i, line in enumerate(lines):
        if line.strip() == "#标题" and i + 1 < len(lines):
            title = lines[i + 1].strip()
            if title:
                for c in INVALID_CHARS:
                    title = title.replace(c, "_")
                return title
    return "未命名案例"


def ensure_unique_path(output_dir: Path, base_name: str, ext: str = ".txt") -> Path:
    path = output_dir / f"{base_name}{ext}"
    if not path.exists():
        return path
    n = 1
    while (path := output_dir / f"{base_name}_{n}{ext}").exists():
        n += 1
    return path


def _is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def collect_files(folder_path: Path, exts: set[str], output_dir: Path) -> list[Path]:
    out = output_dir.resolve()
    files = [
        f for f in folder_path.rglob("*")
        if f.is_file() and f.suffix.lower() in exts and not _is_under(f, out)
    ]
    return sorted(files, key=lambda p: str(p.relative_to(folder_path)).lower())


def build_user_message(prompt_template: str, case: ParsedCase, config: dict):
    prompt = prompt_template.replace("{content}", case.text)
    if not case.images:
        return prompt

    max_images = config.get("max_images", 20)
    images = case.images[:max_images]
    note = f"\n\n【附件图片】共 {len(case.images)} 张，以下为前 {len(images)} 张，请结合图片分析。"
    if len(case.images) > len(images):
        note += f"（另有 {len(case.images) - len(images)} 张未发送，max_images={max_images}）"

    content = [{"type": "text", "text": prompt + note}]
    for img in images:
        if img.label:
            content.append({"type": "text", "text": f"[图片: {img.label}]"})
        b64 = base64.b64encode(img.data).decode("ascii")
        content.append({"type": "image_url", "image_url": {"url": f"data:{img.mime};base64,{b64}"}})
    return content


def generate_template(client, config, prompt_template, case: ParsedCase) -> str:
    try:
        resp = client.chat.completions.create(
            model=config.get("model", "qwen3-max"),
            messages=[{"role": "user", "content": build_user_message(prompt_template, case, config)}],
            extra_body={"enable_thinking": config.get("enable_thinking", False)},
            timeout=config.get("timeout", 180),
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"# 错误\n无法生成模板: {e}"


def resolve_path(path: str) -> Path:
    p = Path(path)
    return (Path.cwd() / p if not p.is_absolute() else p).resolve()


def prepare(args):
    output_dir = resolve_path(args.output) if args.output else DEFAULT_OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    prompt = load_prompt()
    if "{content}" not in prompt:
        print("错误: prompt.txt 中必须包含 {content} 占位符")
        sys.exit(1)
    config = load_config()
    client = OpenAI(api_key=config["api_key"], base_url=config["base_url"])
    return output_dir, config, prompt, client


def process_file(file_path, client, config, prompt, output_dir) -> tuple[int, int]:
    try:
        cases = parse(str(file_path))
    except (ValueError, ImportError) as e:
        print(f"  解析失败: {e}")
        return 0, 0
    if not cases:
        print("  未解析到任何案例内容，跳过")
        return 0, 0

    saved = skipped = 0
    for i, case in enumerate(cases):
        tag = f"[{i + 1}/{len(cases)}]"
        img_hint = f"，含 {len(case.images)} 张图片" if case.images else ""
        print(f"  {tag} 正在调用 AI 生成模板{img_hint}...")
        result = generate_template(client, config, prompt, case)

        if should_skip(result):
            lines = result.strip().splitlines()
            reason = lines[1].strip() if len(lines) > 1 else ""
            print(f"  {tag} 已跳过（文档不合适）{': ' + reason if reason else ''}")
            skipped += 1
            continue
        if result.startswith("# 错误"):
            print(f"  {tag} 生成失败: {result.splitlines()[-1]}")
            skipped += 1
            continue

        out = ensure_unique_path(output_dir, extract_title(result))
        out.write_text(result, encoding="utf-8")
        print(f"  {tag} 已保存: {out.name}")
        saved += 1
    return saved, skipped


def cmd_file(args):
    file_path = resolve_path(args.path)
    if not file_path.exists():
        print(f"错误: 文件不存在 {file_path}")
        sys.exit(1)
    if not file_path.is_file():
        print("错误: 路径不是文件，请使用 folder 子命令处理文件夹")
        sys.exit(1)

    output_dir, config, prompt, client = prepare(args)
    print(f"正在处理文件: {file_path}")
    saved, skipped = process_file(file_path, client, config, prompt, output_dir)
    print(f"\n完成: 保存 {saved} 个，跳过 {skipped} 个\n输出目录: {output_dir}")


def cmd_folder(args):
    folder_path = resolve_path(args.path)
    if not folder_path.exists():
        print(f"错误: 文件夹不存在 {folder_path}")
        sys.exit(1)
    if not folder_path.is_dir():
        print("错误: 路径不是文件夹")
        sys.exit(1)

    output_dir, config, prompt, client = prepare(args)
    exts = set(get_supported_extensions())
    files = collect_files(folder_path, exts, output_dir)
    if not files:
        print(f"错误: 文件夹内没有支持格式的文档\n支持格式: {', '.join(sorted(exts))}")
        sys.exit(1)

    print(f"正在递归处理文件夹: {folder_path}\n找到 {len(files)} 个文件")
    total_saved = total_skipped = 0
    for file_path in files:
        print(f"\n--- {file_path.relative_to(folder_path)} ---")
        saved, skipped = process_file(file_path, client, config, prompt, output_dir)
        total_saved += saved
        total_skipped += skipped
    print(f"\n全部完成: 保存 {total_saved} 个，跳过 {total_skipped} 个\n输出目录: {output_dir}")


def main():
    exts = get_supported_extensions()
    parser = argparse.ArgumentParser(
        description="故障案例模板生成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"支持格式: {', '.join(exts)}",
    )
    parser.add_argument("-o", "--output", metavar="DIR", help="输出目录（默认 scripts/output）")
    sub = parser.add_subparsers(dest="command", required=True)

    p_file = sub.add_parser("file", help="处理单个文件")
    p_file.add_argument("path", help="文件路径")
    p_file.set_defaults(func=cmd_file)

    p_folder = sub.add_parser("folder", help="递归处理文件夹")
    p_folder.add_argument("path", help="文件夹路径")
    p_folder.set_defaults(func=cmd_folder)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
