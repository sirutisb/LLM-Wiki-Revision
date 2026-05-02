"""Extract text from every PDF in raw/ into raw/text/<name>.txt.

Uses PyMuPDF (fitz). Page boundaries are kept as form-feed (\f) so downstream
tooling can reconstruct slide numbers if needed. Re-running is idempotent: it
overwrites whatever is in raw/text/.
"""

from pathlib import Path
import sys
import fitz  # PyMuPDF

ROOT = Path(__file__).parent
RAW = ROOT / "raw"
OUT = RAW / "text"
OUT.mkdir(exist_ok=True)


def extract(pdf_path: Path) -> tuple[int, int]:
    doc = fitz.open(pdf_path)
    pages = []
    for i, page in enumerate(doc, start=1):
        text = page.get_text("text").strip()
        pages.append(f"--- page {i} ---\n{text}")
    doc.close()
    body = "\n\n".join(pages)
    out_path = OUT / (pdf_path.stem + ".txt")
    out_path.write_text(body, encoding="utf-8")
    return len(pages), len(body)


def main() -> int:
    pdfs = sorted(RAW.glob("*.pdf"))
    if not pdfs:
        print("no PDFs found in", RAW)
        return 1
    print(f"extracting {len(pdfs)} PDFs into {OUT}")
    total_pages = 0
    for pdf in pdfs:
        n_pages, n_chars = extract(pdf)
        total_pages += n_pages
        print(f"  {pdf.name:55s}  {n_pages:4d} pages  {n_chars:7d} chars")
    print(f"done. {total_pages} pages total.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
