# PDF-Skill - Advanced PDF Processing for Claude Code

<div align="center">

![PDF Processing](https://img.shields.io/badge/PDF%20Processing-Advanced-blue)
![Skill Type](https://img.shields.io/badge/Type-Skill-purple)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

**High-performance PDF document processing skill for Claude Code and Claude AI**

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Capabilities](#capabilities) • [Troubleshooting](#troubleshooting)

</div>

---

## Overview

**PDF-Skill** is a standalone skill for Claude Code and Claude AI that provides intelligent PDF document processing capabilities. It enables extraction of text, images, and tables, plus advanced NLP analysis features directly within your AI IDE.

This skill processes PDFs with automatic dependency management and intelligent model loading, making it easy to work with PDF documents in your AI workflows.


---

## Features

### 📄 Content Extraction
- **Text Extraction** - Extract all text or specific page ranges
- **Image Extraction** - Base64-encoded images with optimization
- **Table Extraction** - Structured table data conversion to CSV/JSON/DataFrame
- **Metadata Extraction** - PDF properties (title, author, dates, page count)

### 🧠 NLP & Analysis
- **Entity Recognition** - Identify people, organizations, locations, and more
- **Content Analysis** - Automatic summarization and keyword extraction
- **Document Classification** - Zero-shot classification into custom categories
- **Language Detection** - Multi-language support with per-paragraph analysis
- **Advanced Analysis** - Text complexity metrics, POS distribution, TF-IDF phrases
- **Similarity Calculation** - Semantic similarity between PDFs using embeddings

### ⚡ Smart Features
- **Lazy Model Loading** - Models load on-demand when first used
- **Automatic Memory Management** - Unloads unused models automatically
- **GPU/CUDA Support** - Auto-detects and uses GPU when available
- **Quantization** - Optimized memory usage with dynamic quantization
- **Background Cleanup** - Idle models removed after 5 minutes
- **LRU Caching** - Frequent operations cached for speed

---

## Installation

### Step 1: Clone Repository
```bash
git clone https://github.com/jiehai4/PDF-Skill.git
```

### Step 2: Install Skill
Copy the `pdf-skill` folder to your Claude Code skills directory:

```bash
   /.claude/skill/pdf-skill
```

### Step 3: Verify Installation
The skill will be automatically available in Claude Code. On first use, dependencies will be configuration automatically.

---

## Usage

### In Claude Code

Once installed, the PDF-Skill becomes available in Claude Code. Use it by asking Claude to process PDFs:

```
User: "Extract all text from this PDF and summarize the content"
→ Claude uses the skill to extract and analyze the PDF
→ Returns the extracted text and summary

User: "What tables are in this PDF?"
→ Claude uses the skill to extract tables
→ Returns structured table data

User: "Classify this document - is it a report, invoice, or contract?"
→ Claude uses the skill with classification
→ Returns the classification result
```

### Available Operations

**Text Extraction**
```
Extract text from document.pdf
Extract text from pages 1-5 of document.pdf
```

**Image Extraction**
```
Extract all images from document.pdf
Get images from the first page of document.pdf
```

**Table Extraction**
```
Extract tables from document.pdf
Convert PDF tables to CSV format
```

**Content Analysis**
```
Summarize the content of document.pdf
Extract key entities from document.pdf
Find important keywords in document.pdf
```

**Metadata**
```
Get metadata from document.pdf
How many pages are in document.pdf?
```

**Classification & Analysis**
```
Classify this document (Report/Invoice/Legal)
Compare similarity between two PDFs
Detect languages in document.pdf
Analyze text complexity in document.pdf
```

---

## Capabilities

### Text Extraction
Extracts text content from PDFs with support for:
- Full document extraction
- Specific page ranges
- Text-based PDFs (scanned PDFs require external OCR)

### Image Extraction
- Extracts images with base64 encoding
- Optimized file sizes
- Metadata for each image (page number, dimensions)

### Table Extraction
- Converts tables to structured formats
- Supports multiple table formats
- Preserves table relationships

### Content Analysis (Three Modes)
1. **Entities** - Named entity recognition (people, organizations, locations, etc.)
2. **Summary** - Automatic document summarization
3. **Keywords** - Key term and phrase extraction

### Document Classification
- Zero-shot classification
- Custom category support
- Confidence scores for each classification

### Language Detection
- Multi-language support
- Per-paragraph language analysis
- Confidence scores

### Advanced Analysis
- Lexical complexity metrics
- Part-of-speech (POS) distribution
- TF-IDF phrase extraction
- Text readability analysis

### Similarity Calculation
- Semantic similarity between PDFs
- Uses transformer embeddings
- Similarity scores (0-1 range)

---

## Dependencies

The skill automatically manages its own dependencies on first use. Required packages include:

**PDF Processing**
- PyMuPDF (fitz) - Fast PDF reading and rendering
- pdfminer.six - Text extraction and analysis
- tabula-py - Table extraction
- pandas - Data manipulation

**NLP & Machine Learning**
- spacy - Named entity recognition
- transformers - Hugging Face models
- torch - Deep learning framework
- sentence-transformers - Semantic embeddings
- scikit-learn - ML utilities
- nltk - Text processing
- langdetect - Language detection

**Utilities**
- Pillow - Image processing
- numpy - Numerical computing


---

## Performance Characteristics

### Model Loading
- **First Use**: ~30-60 seconds (models download and load)
- **Subsequent Uses**: Instant (cached models)
- **Idle Timeout**: Models unload after 5 minutes of inactivity

### Memory Usage
- **Monitoring**: Automatic memory pressure tracking
- **Auto-Cleanup**: Models unload when system memory exceeds 80%
- **Quantization**: Models use int8 (CPU) or float16 (GPU) quantization to reduce memory
- **GPU Support**: Auto-detects CUDA; uses GPU with 4GB+ VRAM

### Processing Time
- **Small PDFs** (<100 pages): < 5 seconds
- **Large PDFs** (1000+ pages): Recommend processing page ranges
- **NLP Operations**: Fastest on GPU, acceptable on CPU

---

## Common Workflows

### Extract and Understand a Document
```
User: "Extract text from report.pdf and give me a summary, key entities, and important keywords"

Claude will:
1. Extract text using extract_text
2. Analyze with mode="summary" to get overview
3. Analyze with mode="entities" to extract key information
4. Analyze with mode="keywords" to find important terms
5. Present all results in organized format
```

### Process Financial Reports
```
User: "Extract all tables from financial_report.pdf and convert to CSV"

Claude will:
1. Extract tables using extract_tables
2. Convert to CSV format
3. Provide the structured data for further analysis
```

### Classify Documents
```
User: "Classify these PDFs - are they Technical, Business, Legal, or Financial documents?"

Claude will:
1. Analyze each PDF
2. Classify using provided categories
3. Return classification results with confidence scores
```

### Compare Documents
```
User: "How similar are doc1.pdf and doc2.pdf?"

Claude will:
1. Calculate semantic similarity using embeddings
2. Return similarity score (0-1)
3. Provide insights about document relationship
```

---

## Handling Image-Based PDFs

Some PDFs are created by scanning paper documents rather than containing extractable text.

### Detection
If text extraction returns minimal or no text, the PDF is likely image-based. Options:

1. **Extract Images** - Get visual content from the PDF
2. **External OCR** - Use services like:
   - Google Cloud Vision API
   - Amazon Textract
   - Azure Computer Vision
   - Adobe Acrobat OCR
   - EasyOCR (open-source)

### Recommendation
Let Claude detect image-based PDFs and suggest appropriate solutions automatically.

---

## Troubleshooting



### "Text Extraction Returns Empty"
PDF is likely image-based (scanned document):
```
→ Try image extraction instead
→ Use external OCR service for text
```

### "Slow on First Use"
Expected behavior - models are loading:
```
First call: ~30-60 seconds (model download + loading)
Subsequent calls: < 5 seconds (instant)
```

### "Out of Memory Error"
Models are unloading due to memory pressure:
```
Solutions:
1. Close other applications
2. Process smaller page ranges
3. Wait 5+ minutes for idle model unloading
4. Reduce system memory usage
```

### "GPU/CUDA Not Working"
The skill will automatically fall back to CPU:
```
For GPU support:
1. Install CUDA-capable GPU drivers
2. Skill auto-detects CUDA if available
3. Falls back to CPU quantization if not available
```

---

## Project Structure

```
pdf-skill/
├── SKILL.md                    # Skill documentation
├── scripts/                    # Standalone Python scripts
│   ├── extract_text.py         # Text extraction
│   ├── extract_images.py       # Image extraction
│   ├── extract_tables.py       # Table extraction
│   ├── analyze_content.py      # Content analysis (entities/summary/keywords)
│   ├── get_metadata.py         # Metadata extraction
│   ├── classify_document.py    # Document classification
│   ├── calculate_similarity.py # PDF similarity
│   ├── detect_languages.py     # Language detection
│   ├── advanced_analysis.py    # Advanced text analysis
│   └── requirements.txt        # Python dependencies
└── references/
    └── api_reference.md        # Detailed API documentation
```

---

## Implementation Details

### Model Manager (Singleton Pattern)
The skill uses a centralized Model Manager for intelligent model lifecycle:

- **Lazy Loading**: Models load only on first use
- **Memory Monitoring**: Tracks system memory and unloads least-used models when threshold (80%) is exceeded
- **Auto-Cleanup**: Background thread removes idle models (default: 300 seconds)
- **Device Selection**: Automatically selects CPU or GPU based on CUDA availability
- **Quantization Support**:
  - Dynamic quantization for CPU (int8)
  - Static quantization for GPU (float16)

### Managed Models
1. **spacy** - en_core_web_sm for NLP (entities, dependencies, POS)
2. **classifier** - facebook/bart-large-mnli for zero-shot classification
3. **sentence_transformer** - paraphrase-MiniLM-L6-v2 for similarity

---

## Development

### For Developers
If you want to integrate PDF-Skill into your own Claude Code setup:

1. Clone and place in `~/.claude/skills/pdf-skill`
2. Skill becomes available automatically
3. Claude can invoke all operations

### Adding Custom Operations
To extend the skill:
1. Add new script to `scripts/` directory
2. Follow the same parameter/output patterns
3. Update `SKILL.md` documentation
4. Test with Claude Code

---

## License

This project is licensed under the MIT License - see LICENSE file for details.

---

## Acknowledgments

Built with:
- [PyMuPDF](https://pymupdf.readthedocs.io/) for PDF processing
- [Spacy](https://spacy.io/) for NLP
- [Hugging Face Transformers](https://huggingface.co/) for state-of-the-art models
- [Sentence Transformers](https://www.sbert.net/) for semantic embeddings
- [Claude Code](https://claude.com/claude-code) skill framework

---

<div align="center">

**Made with ❤️ for PDF enthusiasts and developers**

[⬆ Back to top](#pdf-skill---advanced-pdf-processing-for-claude-code)

</div>
