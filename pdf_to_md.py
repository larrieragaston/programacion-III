#!/usr/bin/env python3
"""
Extract PDF text to Markdown for course docs.

Prefer embedded text via PyMuPDF; if a page has very little text (likely scanned),
fall back to OCR with pdf2image + Tesseract (same stack as ocr_extract.py).

Always review the .md output: tables, lambda notation, and line breaks may need
manual fixes — same caveat as the Slidev PDF workflow in .cursor/rules/pdf-to-slidev.mdc.

System deps (macOS): brew install tesseract tesseract-lang poppler
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

MIN_CHARS_FOR_TEXT = 50


def title_from_stem(stem: str) -> str:
    return stem.replace("_", " ").replace("-", " ").strip()


def normalize_body(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    for line in lines:
        stripped = line.rstrip()
        if stripped:
            out.append(stripped)
        elif out and out[-1] != "":
            out.append("")
    while out and out[-1] == "":
        out.pop()
    return "\n".join(out)


def escape_angle_brackets_for_vue(text: str) -> str:
    """Vue/VitePress treat `<...>` as HTML; escape so BNF and math survive."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def page_to_markdown_blocks(body: str) -> str:
    """Turn plain text into simple Markdown paragraphs."""
    body = normalize_body(body)
    if not body:
        return "_[página vacía]_\n"
    parts = re.split(r"\n\s*\n+", body)
    joined = "\n\n".join(p.strip() for p in parts if p.strip()) + "\n"
    return escape_angle_brackets_for_vue(joined)


def extract_with_pymupdf(pdf_path: Path) -> list[str]:
    import fitz  # PyMuPDF

    doc = fitz.open(pdf_path)
    pages: list[str] = []
    for i in range(len(doc)):
        pages.append(doc[i].get_text("text") or "")
    doc.close()
    return pages


def ocr_page(pdf_path: Path, page_one_based: int, dpi: int) -> str:
    from pdf2image import convert_from_path
    import pytesseract

    images = convert_from_path(
        str(pdf_path),
        dpi=dpi,
        first_page=page_one_based,
        last_page=page_one_based,
    )
    if not images:
        return ""
    return pytesseract.image_to_string(images[0], lang="spa")


def pdf_to_markdown(
    pdf_path: Path,
    *,
    dpi: int,
    title: str | None,
) -> str:
    pdf_path = pdf_path.resolve()
    pages_text = extract_with_pymupdf(pdf_path)
    stem = pdf_path.stem
    doc_title = escape_angle_brackets_for_vue(title or title_from_stem(stem))
    chunks: list[str] = [f"# {doc_title}\n"]

    for i, raw in enumerate(pages_text, start=1):
        text = (raw or "").strip()
        if len(text) < MIN_CHARS_FOR_TEXT:
            text = ocr_page(pdf_path, i, dpi=dpi).strip()

        chunks.append(f"## Página {i}\n")
        chunks.append(page_to_markdown_blocks(text))

    return "\n".join(chunks) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert PDF to Markdown (text + OCR fallback).")
    parser.add_argument("pdf", type=Path, help="Path to input .pdf")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output .md path (default: stdout only if omitted — use -o)",
    )
    parser.add_argument("--title", help="Override H1 title (default: from filename)")
    parser.add_argument("--dpi", type=int, default=300, help="DPI for OCR rasterization (default: 300)")
    args = parser.parse_args()

    if not args.pdf.is_file():
        print(f"File not found: {args.pdf}", file=sys.stderr)
        return 1

    md = pdf_to_markdown(args.pdf, dpi=args.dpi, title=args.title)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(md, encoding="utf-8")
        print(f"Wrote {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
