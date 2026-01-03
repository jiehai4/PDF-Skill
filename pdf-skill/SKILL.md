---
name: pdf-reader
description: High-performance PDF document processing with text extraction, image extraction, table recognition, and NLP analysis. Use when you need to extract content from PDF files, analyze document structure, or process PDF content in any way (text extraction, image extraction, table extraction, entity recognition, summarization, keyword extraction, document classification, language detection, or advanced text analysis).
---

# PDF Reader

## Overview

PDF Reader is a high-performance PDF document processing skill that enables intelligent extraction and analysis of PDF content. It provides tools for extracting text, images, and tables, plus advanced NLP capabilities like entity recognition, summarization, keyword extraction, and document classification.

## Quick Start

To process a PDF file, you'll typically:

1. **Extract what you need** - Choose from text, images, tables, or metadata
2. **Analyze the content** - Use NLP to extract entities, summaries, or keywords
3. **Process the results** - Format and use the extracted data

Example workflow:
```
User: "Extract text and key information from this PDF"
→ Use extract_text.py to get text content
→ Use analyze_content.py with "entities" mode to extract important information
→ Format and present the results
```

## Core Capabilities

### 1. Text Extraction
Extract all text from a PDF or specific pages using `scripts/extract_text.py`.

**When to use:** Accessing PDF content for analysis, searching, or display

**What it provides:**
- Complete text from all pages
- Option to extract specific page ranges
- Handles both text-based and scanned PDFs

### 2. Image Extraction
Extract all images from a PDF with base64 encoding using `scripts/extract_images.py`.

**When to use:** Getting graphics, diagrams, or visual content from PDFs

**What it provides:**
- All images from specified pages
- Base64-encoded format for easy transmission
- Optimized file sizes

### 3. Table Extraction
Extract structured tables from PDFs using `scripts/extract_tables.py`.

**When to use:** Processing tabular data from PDFs (financial reports, data tables, etc.)

**What it provides:**
- Tables converted to structured format
- Preserves table structure and layout
- Can be converted to CSV, JSON, or pandas DataFrames

### 4. Content Analysis
Analyze PDF content using NLP with three modes in `scripts/analyze_content.py`:

- **entities**: Extract named entities (people, organizations, locations, etc.)
- **summary**: Generate concise summaries of the document
- **keywords**: Extract key terms and phrases

### 5. Document Metadata
Extract metadata about the PDF using `scripts/get_metadata.py`.

**What it provides:**
- Title, author, subject, creator
- Creation and modification dates
- Page count
- File size information

### 6. Document Classification
Classify documents into specified categories using `scripts/classify_document.py`.

**When to use:** Organizing documents or determining document type

### 7. Document Similarity
Calculate similarity between two PDFs using `scripts/calculate_similarity.py`.

### 8. Language Detection
Detect languages used in the document with `scripts/detect_languages.py`.

### 9. Advanced Analysis
Perform detailed linguistic analysis with `scripts/advanced_analysis.py`.

## Common Workflows

### Extract and Analyze a Document
```
1. Call extract_text.py to get the full text
2. Call analyze_content.py with "summary" to get an overview
3. Call analyze_content.py with "entities" to extract key information
4. Present results to user in organized format
```

### Process Structured Data from Tables
```
1. Call extract_tables.py to get table data
2. Convert extracted tables to CSV or JSON
3. Optionally call classify_document.py to categorize the document
```

### Batch Process Multiple PDFs
```
1. For each PDF:
   - Extract text with extract_text.py
   - Get metadata with get_metadata.py
   - Analyze with analyze_content.py
2. Aggregate results across all PDFs
```

## Handling Image-Based PDFs (图片堆叠型PDF)

### Problem Identification

Some PDFs are created by scanning paper documents or directly stacking images instead of containing selectable text. These PDFs cannot have their text extracted using standard text extraction methods.

**Signs that a PDF is image-based:**
- Text extraction returns empty or minimal text
- The extracted text doesn't match what you see visually in the document
- The document looks like scanned pages or screenshots
- Text extraction contains garbled characters or random symbols

### Detection Strategy

**Step 1: Attempt text extraction**
```
python extract_text.py suspicious_document.pdf
```

**Step 2: Check the result**
- If text is empty or much shorter than expected → likely image-based
- If text doesn't match visual content → likely image-based
- If text is coherent and matches content → proceed normally

**Step 3: Verify with image extraction**
```
python extract_images.py suspicious_document.pdf --page 0
```
- If page contains images → confirm it's image-based

### Recommended Workflow for Image-Based PDFs

**When you detect an image-based PDF, follow this protocol:**

1. **Immediately notify the user** with a clear message:
   ```
   ⚠️ Image-Based PDF Detected

   This PDF appears to be made up of scanned images or screenshots
   rather than editable text. Standard text extraction cannot be used.

   Recommendation: Use image extraction to retrieve the visual content.
   ```

2. **Request user confirmation** (if applicable):
   ```
   Would you like me to:
   A) Extract all images from the PDF
   B) Extract images from specific pages only
   C) Provide alternative solutions
   ```

3. **Execute image extraction**:
   ```bash
   # Extract all images
   python extract_images.py document.pdf --output ./extracted_images

   # Or extract from specific pages
   python extract_images.py document.pdf --page 0 --output ./page_images
   ```

4. **Present results to user**:
   - List extracted images with metadata (size, page number, format)
   - Provide base64-encoded images for viewing/processing
   - Suggest next steps (e.g., manual review, external OCR service)

### Alternative Solutions for Image-Based PDFs

When text extraction fails, offer these options:

**Option 1: Image Extraction + Viewer**
- Extract all images and display them
- User can review visual content directly
- Best for quick visual inspection

**Option 2: External OCR Services** (mention to user)
- Google Lens / Cloud Vision API
- Amazon Textract
- Azure Computer Vision
- Adobe Acrobat OCR
- EasyOCR (open-source Python library)

**Option 3: Manual Processing**
- If document is important, suggest manual transcription
- Or use specialized document digitization services

### Code Pattern for AI to Follow

```python
# Pseudo-code for AI decision logic
result = extract_text(pdf_file)

if len(result.strip()) < 100:  # Suspiciously low text
    print("⚠️ ALERT: Likely image-based PDF detected")
    print(f"Text extracted: {len(result)} characters")
    print("\nRecommended action: Use image extraction instead")

    # Ask user before proceeding
    user_wants_images = ask_user("Extract images instead? (yes/no)")

    if user_wants_images:
        images = extract_images(pdf_file)
        print(f"Extracted {len(images)} images from PDF")
        return images
    else:
        return {"error": "Cannot process this PDF without OCR support"}
```

### Summary: Decision Tree

```
User uploads PDF
    ↓
Attempt extract_text()
    ↓
Is result meaningful?
    ├─ YES → Process normally, continue with analysis
    └─ NO → Image-based PDF detected
              ↓
              Notify user immediately
              ↓
              Ask: Extract images?
              ├─ YES → extract_images() → display results
              └─ NO → Suggest external OCR options
```

## Implementation Notes

### Setting Up Dependencies

Before using this skill, you need to install required dependencies:

```bash
pip install -r requirements.txt
```

Key dependencies include:
- PyMuPDF (fitz) - PDF reading and rendering
- pdfminer.six / tabula-py - Table extraction
- spacy - Named entity recognition
- transformers - Document classification and summarization
- sentence-transformers - Document similarity

### Running Scripts

Each script in the `scripts/` directory is designed to be:
- Self-contained and easy to execute
- Properly documented with parameter descriptions
- Capable of handling common PDF edge cases

### Performance Considerations

- **Large PDFs**: For very large documents (1000+ pages), consider processing page ranges rather than the entire document
- **Scanned PDFs**: Text extraction works best on text-based PDFs. Scanned PDFs may require OCR
- **GPU Support**: Advanced analysis features can utilize GPU if available (CUDA)
- **Memory Management**: The skill includes automatic model memory management to prevent out-of-memory errors

## References

See `references/api_reference.md` for detailed API documentation for all extraction and analysis functions.

## Resources

This skill includes bundled resources for PDF processing:

### scripts/
Executable Python scripts for specific PDF operations:
- `extract_text.py` - Extract text content from PDFs
- `extract_images.py` - Extract and encode images
- `extract_tables.py` - Extract structured table data
- `analyze_content.py` - NLP-based content analysis
- `get_metadata.py` - Extract PDF metadata
- `classify_document.py` - Zero-shot document classification
- `calculate_similarity.py` - Calculate semantic similarity between PDFs
- `detect_languages.py` - Language detection
- `advanced_analysis.py` - Advanced text analysis

### references/
Reference documentation:
- `api_reference.md` - Complete API reference with all parameters and examples
- `requirements.txt` - Python package dependencies

### assets/
Sample files and data (if provided)
