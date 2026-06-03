from dataclasses import dataclass, field

IMAGE_MIME = {
    "png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
    "gif": "image/gif", "bmp": "image/bmp", "webp": "image/webp",
}
NO_TEXT_HINT = "(文档未提取到文本，请结合附件图片分析)"


@dataclass
class DocumentImage:
    data: bytes
    mime: str
    label: str = ""


@dataclass
class ParsedCase:
    text: str
    images: list[DocumentImage] = field(default_factory=list)
