#!/usr/bin/env python3
"""
Calculate semantic similarity between two PDF documents.

Usage:
    calculate_similarity.py <pdf_path1> <pdf_path2> [--output <output_file>]

Examples:
    calculate_similarity.py document1.pdf document2.pdf
    calculate_similarity.py doc1.pdf doc2.pdf --output similarity.json
"""

import sys
import argparse
import json
import numpy as np
from pdfminer.high_level import extract_text as pdfminer_extract_text

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("Error: sentence-transformers library not installed. Please install it with:")
    print("pip install sentence-transformers")
    sys.exit(1)


def calculate_similarity(file_path1: str, file_path2: str) -> dict:
    """
    Calculate semantic similarity between two PDF documents.

    Args:
        file_path1: Path to the first PDF file
        file_path2: Path to the second PDF file

    Returns:
        Dictionary containing similarity results
    """
    try:
        # Extract text from both PDFs
        text1 = pdfminer_extract_text(file_path1)
        text2 = pdfminer_extract_text(file_path2)

        if not text1.strip() or not text2.strip():
            return {
                "success": False,
                "error": "One or both PDF files have no text content"
            }

        # Load sentence transformer model
        model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

        # Chunk text for better representation
        def chunk_text(text, chunk_size=1000):
            return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

        # Get embeddings
        chunks1 = chunk_text(text1)
        chunks2 = chunk_text(text2)

        embeddings1 = model.encode(chunks1)
        embeddings2 = model.encode(chunks2)

        # Calculate average embeddings
        avg_embedding1 = np.mean(embeddings1, axis=0)
        avg_embedding2 = np.mean(embeddings2, axis=0)

        # Calculate cosine similarity
        similarity = np.dot(avg_embedding1, avg_embedding2) / (
            np.linalg.norm(avg_embedding1) * np.linalg.norm(avg_embedding2)
        )

        return {
            "success": True,
            "similarity_score": float(similarity),
            "document1_chunks": len(chunks1),
            "document2_chunks": len(chunks2),
            "interpretation": get_similarity_interpretation(float(similarity))
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Error calculating similarity: {str(e)}"
        }


def get_similarity_interpretation(score: float) -> str:
    """Get human-readable interpretation of similarity score"""
    if score > 0.8:
        return "Very similar - documents cover similar topics/content"
    elif score > 0.6:
        return "Similar - documents have some overlapping content"
    elif score > 0.4:
        return "Somewhat similar - some shared concepts"
    elif score > 0.2:
        return "Loosely related - minimal overlap"
    else:
        return "Very different - minimal semantic similarity"


def main():
    parser = argparse.ArgumentParser(
        description="Calculate semantic similarity between PDF documents"
    )
    parser.add_argument("pdf_path1", help="Path to the first PDF file")
    parser.add_argument("pdf_path2", help="Path to the second PDF file")
    parser.add_argument(
        "--output",
        default=None,
        help="Output file path (JSON format)"
    )

    args = parser.parse_args()

    # Calculate similarity
    result = calculate_similarity(args.pdf_path1, args.pdf_path2)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Similarity calculation complete. Results saved to: {args.output}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
