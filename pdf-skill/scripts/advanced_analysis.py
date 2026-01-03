#!/usr/bin/env python3
"""
Perform advanced text analysis on PDF documents.

Includes: complexity metrics, POS distribution, TF-IDF key phrases.

Usage:
    advanced_analysis.py <pdf_path> [--output <output_file>]

Examples:
    advanced_analysis.py document.pdf
    advanced_analysis.py document.pdf --output analysis.json
"""

import sys
import argparse
import json
import nltk
from pdfminer.high_level import extract_text as pdfminer_extract_text
from collections import Counter

try:
    import spacy
except ImportError:
    print("Error: spacy library not installed. Please install it with:")
    print("pip install spacy")
    sys.exit(1)

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)


def load_spacy_model():
    """Load spacy model, download if necessary"""
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        print("Downloading spacy model 'en_core_web_sm'...")
        import os
        os.system("python -m spacy download en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")
    return nlp


def analyze_advanced(file_path: str) -> dict:
    """
    Perform advanced text analysis on PDF.

    Args:
        file_path: Path to the PDF file

    Returns:
        Dictionary containing advanced analysis results
    """
    try:
        # Extract text from PDF
        text = pdfminer_extract_text(file_path)

        if not text.strip():
            return {
                "success": False,
                "error": "No text content found in PDF"
            }

        # Load spacy model
        nlp = load_spacy_model()
        doc = nlp(text[:10000])  # Limit to first 10k chars for performance

        # Calculate text statistics
        sentences = nltk.sent_tokenize(text)
        words = nltk.word_tokenize(text.lower())

        # Remove punctuation for word count
        from nltk.corpus import stopwords
        stop_words = set(stopwords.words('english'))
        meaningful_words = [w for w in words if w.isalnum() and w not in stop_words]

        # POS distribution
        pos_tags = nltk.pos_tag(words)
        pos_distribution = Counter([pos for word, pos in pos_tags])

        # Extract noun phrases (common phrases)
        noun_phrases = [chunk.text for chunk in doc.noun_chunks]
        top_phrases = Counter(noun_phrases).most_common(10)

        # Calculate readability metrics
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        avg_word_length = sum(len(w) for w in meaningful_words) / len(meaningful_words) if meaningful_words else 0

        # Flesch-Kincaid Grade Level approximation
        complex_words = sum(1 for w in meaningful_words if len(w) > 6)
        fk_grade = (0.39 * (len(words) / len(sentences)) +
                   11.8 * (complex_words / len(meaningful_words)) - 15.59)

        return {
            "success": True,
            "text_statistics": {
                "total_characters": len(text),
                "total_words": len(words),
                "meaningful_words": len(meaningful_words),
                "total_sentences": len(sentences),
                "total_paragraphs": len(text.split('\n\n'))
            },
            "readability_metrics": {
                "avg_sentence_length": round(avg_sentence_length, 2),
                "avg_word_length": round(avg_word_length, 2),
                "flesch_kincaid_grade": round(max(0, fk_grade), 2)
            },
            "pos_distribution": {k: v for k, v in sorted(pos_distribution.items(), key=lambda x: x[1], reverse=True)[:10]},
            "top_noun_phrases": [{"phrase": phrase, "count": count} for phrase, count in top_phrases],
            "entity_types": {
                "PERSON": len([ent for ent in doc.ents if ent.label_ == "PERSON"]),
                "ORG": len([ent for ent in doc.ents if ent.label_ == "ORG"]),
                "GPE": len([ent for ent in doc.ents if ent.label_ == "GPE"]),
                "DATE": len([ent for ent in doc.ents if ent.label_ == "DATE"]),
                "OTHER": len([ent for ent in doc.ents if ent.label_ not in ["PERSON", "ORG", "GPE", "DATE"]])
            }
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Error analyzing PDF: {str(e)}"
        }


def main():
    parser = argparse.ArgumentParser(
        description="Perform advanced text analysis on PDF documents"
    )
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument(
        "--output",
        default=None,
        help="Output file path (JSON format)"
    )

    args = parser.parse_args()

    # Perform analysis
    result = analyze_advanced(args.pdf_path)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Advanced analysis complete. Results saved to: {args.output}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
