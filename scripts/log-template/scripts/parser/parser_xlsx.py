from . import register
from .models import ParsedCase

try:
    import openpyxl
except ImportError:
    openpyxl = None


@register(".xlsx")
def parse_xlsx(file_path: str) -> list[ParsedCase]:
    if openpyxl is None:
        raise ImportError("解析 xlsx 需要安装 openpyxl: pip install openpyxl")

    wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
    rows = list(wb.active.iter_rows(values_only=True))
    wb.close()
    if not rows:
        return []

    headers = [str(h) if h is not None else f"列{i + 1}" for i, h in enumerate(rows[0])]
    cases = []
    for row in rows[1:]:
        parts = []
        for i, cell in enumerate(row):
            header = headers[i] if i < len(headers) else f"列{i + 1}"
            if cell is not None and str(cell).strip():
                parts.append(f"{header}: {cell}")
        if parts:
            cases.append("\n".join(parts))
    return [ParsedCase(c) for c in cases]
