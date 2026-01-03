#!/usr/bin/env python3
"""
Extract tables from PDF files.

Usage:
    extract_tables.py <pdf_path> [--page <page_number>] [--output <output_file>]

Examples:
    extract_tables.py document.pdf
    extract_tables.py document.pdf --page 0
    extract_tables.py document.pdf --output tables.json
"""

import sys
import argparse
import json
from pathlib import Path
from tabula import read_pdf


def extract_tables(file_path: str, page_number: int = None) -> dict:
    """
    Extract tables from PDF file.

    Args:
        file_path: Path to the PDF file
        page_number: Optional page number (1-indexed for tabula) to extract specific page

    Returns:
        Dictionary containing extracted table data
    """
    try:
        # tabula uses 1-based page numbers
        pages_param = page_number + 1 if page_number is not None else 'all'

        tables = read_pdf(file_path, pages=pages_param)

        if not tables:
            return {
                "success": True,
                "message": "No tables found in the PDF",
                "tables": []
            }

        result_tables = []
        for i, table in enumerate(tables):
            # Convert DataFrame to dict for JSON serialization
            result_tables.append({
                "table_number": i + 1,
                "rows": len(table),
                "columns": len(table.columns),
                "column_names": table.columns.tolist(),
                "data": table.values.tolist()
            })

        return {
            "success": True,
            "total_tables": len(result_tables),
            "tables": result_tables
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Error extracting tables: {str(e)}"
        }


def main():
    parser = argparse.ArgumentParser(
        description="Extract tables from PDF files"
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
        help="Output file path (JSON format)"
    )
    parser.add_argument(
        "--format",
        choices=["json", "csv"],
        default="json",
        help="Output format (default: json)"
    )

    args = parser.parse_args()

    # Extract tables
    result = extract_tables(args.pdf_path, args.page)

    if args.output:
        if args.format == "json":
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"Tables extracted and saved to: {args.output}")
        elif args.format == "csv":
            # Save each table as separate CSV
            output_dir = Path(args.output).parent
            output_stem = Path(args.output).stem
            for i, table_info in enumerate(result.get("tables", [])):
                csv_path = output_dir / f"{output_stem}_table_{i+1}.csv"
                import pandas as pd
                df = pd.DataFrame(table_info["data"], columns=table_info["column_names"])
                df.to_csv(csv_path, index=False, encoding='utf-8')
                print(f"Saved: {csv_path}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
