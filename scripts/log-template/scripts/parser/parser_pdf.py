from . import register
from .models import DocumentImage, IMAGE_MIME, NO_TEXT_HINT, ParsedCase

try:
    import fitz
except ImportError:
    fitz = None

SCAN_TEXT_THRESHOLD = 50


@register(".pdf")
def parse_pdf(file_path: str) -> list[ParsedCase]:
    if fitz is None:
        raise ImportError("解析 pdf 需要安装 pymupdf: pip install pymupdf")

    doc = fitz.open(file_path)
    text_parts, images, seen = [], [], set()
    try:
        for page_num, page in enumerate(doc, start=1):
            if text := page.get_text().strip():
                text_parts.append(f"--- 第{page_num}页 ---\n{text}")
            for idx, img_info in enumerate(page.get_images(full=True), start=1):
                xref = img_info[0]
                if xref in seen:
                    continue
                seen.add(xref)
                try:
                    item = doc.extract_image(xref)
                except Exception:
                    continue
                mime = IMAGE_MIME.get(item.get("ext", "png"))
                if mime:
                    images.append(DocumentImage(item["image"], mime, f"PDF第{page_num}页内嵌图{idx}"))

        full_text = "\n\n".join(text_parts)
        if len(full_text.strip()) < SCAN_TEXT_THRESHOLD:
            images = [
                DocumentImage(page.get_pixmap(dpi=150).tobytes("png"), "image/png", f"PDF第{n}页截图")
                for n, page in enumerate(doc, start=1)
            ]
    finally:
        doc.close()

    if not full_text.strip() and not images:
        return []
    if not full_text.strip():
        full_text = NO_TEXT_HINT
    return [ParsedCase(full_text, images)]
