#!/usr/bin/env python3
"""
Classify PDF documents into specified categories using zero-shot classification.

Usage:
    classify_document.py <pdf_path> <categories> [--output <output_file>]

Categories should be comma-separated.

Examples:
    classify_document.py document.pdf "report,proposal,invoice"
    classify_document.py document.pdf "legal,technical,marketing" --output classification.json
"""

import sys
import argparse
import json
from pdfminer.high_level import extract_text as pdfminer_extract_text

try:
    from transformers import pipeline
except ImportError:
    print("Error: transformers library not installed. Please install it with:")
    print("pip install transformers torch")
    sys.exit(1)


def classify_document(file_path: str, categories: list) -> dict:
    """
    Classify PDF document into specified categories.

    Args:
        file_path: Path to the PDF file
        categories: List of category strings

    Returns:
        Dictionary containing classification results
    """
    try:
        # Extract text from PDF
        text = pdfminer_extract_text(file_path)

        if not text.strip():
            return {
                "success": False,
                "error": "No text content found in PDF"
            }

        # Load zero-shot classification pipeline
        classifier = pipeline("zero-shot-classification",
                            model="facebook/bart-large-mnli")

        # Classify document
        result = classifier(text[:512], categories, multi_label=False)  # Use first 512 chars

        return {
            "success": True,
            "labels": result["labels"],
            "scores": [float(score) for score in result["scores"]],
            "top_label": result["labels"][0],
            "top_score": float(result["scores"][0])
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Error classifying document: {str(e)}"
        }


def main():
    parser = argparse.ArgumentParser(
        description="Classify PDF documents using zero-shot classification"
    )
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument(
        "categories",
        help="Comma-separated list of categories (e.g., 'legal,technical,marketing')"
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output file path (JSON format)"
    )

    args = parser.parse_args()

    # Parse categories
    categories = [cat.strip() for cat in args.categories.split(",")]

    # Classify document
    result = classify_document(args.pdf_path, categories)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Classification complete. Results saved to: {args.output}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
