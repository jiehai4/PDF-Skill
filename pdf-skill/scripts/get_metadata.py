#!/usr/bin/env python3
"""
Extract metadata from PDF files.

Usage:
    get_metadata.py <pdf_path> [--output <output_file>]

Examples:
    get_metadata.py document.pdf
    get_metadata.py document.pdf --output metadata.json
"""

import sys
import argparse
import json
import fitz  # PyMuPDF
from pathlib import Path


def get_pdf_metadata(file_path: str) -> dict:
    """
    Extract metadata from PDF file.

    Args:
        file_path: Path to the PDF file

    Returns:
        Dictionary containing PDF metadata
    """
    try:
        doc = fitz.open(file_path)
        metadata = doc.metadata

        # Get file info
        file_path_obj = Path(file_path)
        file_stats = file_path_obj.stat()

        result = {
            "success": True,
            "file_info": {
                "name": file_path_obj.name,
                "size_bytes": file_stats.st_size,
                "created_timestamp": file_stats.st_ctime,
                "modified_timestamp": file_stats.st_mtime
            },
            "metadata": {
                "title": metadata.get("title", "Unknown"),
                "author": metadata.get("author", "Unknown"),
                "subject": metadata.get("subject", "Unknown"),
                "keywords": metadata.get("keywords", "Unknown"),
                "creator": metadata.get("creator", "Unknown"),
                "producer": metadata.get("producer", "Unknown"),
                "creation_date": str(metadata.get("creationDate", "Unknown")),
                "modification_date": str(metadata.get("modDate", "Unknown"))
            },
            "document_info": {
                "page_count": len(doc),
                "is_encrypted": doc.is_encrypted,
                "is_pdf": doc.is_pdf
            }
        }

        doc.close()
        return result

    except Exception as e:
        return {
            "success": False,
            "error": f"Error reading PDF metadata: {str(e)}"
        }


def main():
    parser = argparse.ArgumentParser(
        description="Extract metadata from PDF files"
    )
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument(
        "--output",
        default=None,
        help="Output file path (JSON format)"
    )

    args = parser.parse_args()

    # Get metadata
    result = get_pdf_metadata(args.pdf_path)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Metadata extracted and saved to: {args.output}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
