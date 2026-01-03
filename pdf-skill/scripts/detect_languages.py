#!/usr/bin/env python3
"""
Detect languages in PDF documents.

Usage:
    detect_languages.py <pdf_path> [--output <output_file>]

Examples:
    detect_languages.py document.pdf
    detect_languages.py document.pdf --output languages.json
"""

import sys
import argparse
import json
from pdfminer.high_level import extract_text as pdfminer_extract_text

try:
    from langdetect import detect, detect_langs
except ImportError:
    print("Error: langdetect library not installed. Please install it with:")
    print("pip install langdetect")
    sys.exit(1)


def detect_languages(file_path: str) -> dict:
    """
    Detect languages in PDF document.

    Args:
        file_path: Path to the PDF file

    Returns:
        Dictionary containing language detection results
    """
    try:
        # Extract text from PDF
        text = pdfminer_extract_text(file_path)

        if not text.strip():
            return {
                "success": False,
                "error": "No text content found in PDF"
            }

        # Split into paragraphs
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

        # Detect languages
        detected_languages = {}
        language_paragraphs = []

        for i, para in enumerate(paragraphs[:10]):  # Check first 10 paragraphs
            try:
                lang = detect(para)
                if lang not in detected_languages:
                    detected_languages[lang] = 0
                detected_languages[lang] += 1

                language_paragraphs.append({
                    "paragraph_index": i,
                    "language": lang,
                    "text_preview": para[:100] + "..." if len(para) > 100 else para
                })
            except:
                pass

        # Get main language
        main_language = max(detected_languages, key=detected_languages.get) if detected_languages else "unknown"

        return {
            "success": True,
            "main_language": main_language,
            "detected_languages": detected_languages,
            "total_paragraphs_analyzed": min(10, len(paragraphs)),
            "language_distribution": language_paragraphs
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Error detecting languages: {str(e)}"
        }


def main():
    parser = argparse.ArgumentParser(
        description="Detect languages in PDF documents"
    )
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument(
        "--output",
        default=None,
        help="Output file path (JSON format)"
    )

    args = parser.parse_args()

    # Detect languages
    result = detect_languages(args.pdf_path)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Language detection complete. Results saved to: {args.output}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
