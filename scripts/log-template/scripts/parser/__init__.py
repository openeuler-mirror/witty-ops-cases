import os

from .models import ParsedCase

_parsers = {}


def register(ext: str):
    def decorator(fn):
        _parsers[ext.lower()] = fn
        return fn
    return decorator


def parse(file_path: str) -> list[ParsedCase]:
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in _parsers:
        raise ValueError(f"不支持的文件格式: {ext}，当前支持: {sorted(_parsers)}")
    return _parsers[ext](file_path)


def get_supported_extensions() -> list[str]:
    return sorted(_parsers)


from .parser_txt import parse_txt
from .parser_md import parse_md
from .parser_xlsx import parse_xlsx
from .parser_pdf import parse_pdf
from .parser_docx import parse_docx
