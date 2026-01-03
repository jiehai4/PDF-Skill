#!/usr/bin/env python3
"""
Extract text content from PDF files.

Usage:
    extract_text.py <pdf_path> [--page <page_number>] [--output <output_file>]

Examples:
    extract_text.py document.pdf
    extract_text.py document.pdf --page 0
    extract_text.py document.pdf --output extracted_text.txt
"""

import sys
import argparse
import fitz  # PyMuPDF


def extract_text(file_path: str, page_number: int = None) -> str:
    """
    Extract text from PDF file.

    Args:
        file_path: Path to the PDF file
        page_number: Optional page number (0-indexed) to extract specific page

    Returns:
        Extracted text content
    """
    try:
        doc = fitz.open(file_path)

        if page_number is not None:
            if not (0 <= page_number < len(doc)):
                return f"Error: Page {page_number} out of range. PDF has {len(doc)} pages."
            text = doc[page_number].get_text()
            doc.close()
            return text

        # Extract text from all pages
        text = ""
        for page in doc:
            text += page.get_text() + "\n"
        doc.close()
        return text

    except Exception as e:
        return f"Error extracting text: {str(e)}"


def main():
    parser = argparse.ArgumentParser(
        description="Extract text content from PDF files"
    )
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument(
        "--page",
        type=int,
        default=None,
        help="Page number to extract (0-indexed, optional)"
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output file path (if not specified, prints to stdout)"
    )

    args = parser.parse_args()

    # Extract text
    text = extract_text(args.pdf_path, args.page)

    # Output result
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Text extracted and saved to: {args.output}")
    else:
        print(text)


if __name__ == "__main__":
    main()
