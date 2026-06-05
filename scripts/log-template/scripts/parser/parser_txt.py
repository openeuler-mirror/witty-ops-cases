from . import register
from .models import ParsedCase


@register(".txt")
def parse_txt(file_path: str) -> list[ParsedCase]:
    with open(file_path, encoding="utf-8") as f:
        content = f.read()
    return [ParsedCase(content)] if content.strip() else []
