import sys
from pathlib import Path
import pymupdf4llm

def convert(pdf_path):
    pdf = Path(pdf_path)
    md_text = pymupdf4llm.to_markdown(str(pdf))
    md_path = pdf.with_suffix(".md")
    md_path.write_text(md_text, encoding="utf-8")
    return md_path

if __name__ == "__main__":
    print("저장됨:", convert(sys.argv[1])) 