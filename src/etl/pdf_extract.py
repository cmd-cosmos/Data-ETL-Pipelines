#pylint: skip-file
#type: ignore

import os
import pdfplumber
import argparse

def extract_pdf_text(pdf_path, out_txt_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""

        for page_num, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text()
            if page_text:
                text += f"\n\n-------- PAGE {page_num} --------\n\n"
                text += page_text

    os.makedirs(os.path.dirname(out_txt_path), exist_ok=True)

    with open(out_txt_path, "w", encoding="utf-8") as f:
        f.write(text)
    
    print(f"Extracted text saved to: {out_txt_path}")

if __name__ =="__main__":
    parser = argparse.ArgumentParser(description="Extract text from a PDF.")
    parser.add_argument("--i", required=True, help="Input PDF")
    parser.add_argument("--o", required=False, help="Output PDF")

    args = parser.parse_args()
    if args.o is None:
        base = os.path.splitext(os.path.basename(args.i))[0]
        args.o = f"../../data/processed/{base}.txt"
    
    extract_pdf_text(args.i, args.o)
