# PDF-Skill - Advanced PDF Processing MCP Server

<div align="center">

![PDF Processing](https://img.shields.io/badge/PDF%20Processing-Advanced-blue)
![MCP Server](https://img.shields.io/badge/MCP-Server-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

**High-performance PDF document processing with intelligent extraction and NLP analysis**

[Features](#features) • [Quick Start](#quick-start) • [Installation](#installation) • [Usage](#usage) • [Architecture](#architecture)

</div>

---

## Overview

**PDF-Skill** is a high-performance MCP (Model Context Protocol) server for intelligent PDF document processing. It provides comprehensive tools for extracting content, analyzing structure, and performing advanced NLP operations on PDF files.

Whether you need to extract text, images, or tables, classify documents, or perform deep linguistic analysis, PDF-Skill delivers production-ready solutions with automatic memory management and GPU/CPU optimization.

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

### ⚡ Performance Features
- **Lazy Model Loading** - Models load on-demand, not at startup
- **Smart Memory Management** - Automatic unloading of unused models
- **GPU/CUDA Support** - Automatic GPU detection and optimization
- **Quantization** - Dynamic (int8 CPU) and static (float16 GPU) quantization
- **Batch Processing** - Efficient handling of large documents
- **Caching** - LRU caching for frequent operations

### 🔄 Integration
- **MCP Protocol** - Full Model Context Protocol compliance
- **Claude Desktop** - Direct integration with Claude Desktop
- **CLI Support** - Command-line interface for standalone use
- **Python API** - Scriptable Python interface

---

## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/jiehai4/PDF-Skill.git
cd PDF-Skill
```

### 2. Setup Environment
```bash
# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Install dependencies
uv pip install -r pdf-skill/scripts/requirements.txt
```

### 3. Basic Usage
```bash
# Start the MCP server
uv run pdf_reader

# Or run directly
python -m pdf_reader
```

### 4. Process a PDF
```python
from pdf_reader.server import extract_text_from_pdf

# Extract text
text = extract_text_from_pdf("document.pdf")
print(text)
```

---

## Installation

### Requirements
- Python 3.8 or higher
- pip or uv package manager
- 2GB+ RAM (4GB+ recommended for ML models)
- 4GB+ VRAM (optional, for GPU acceleration)

### Step-by-Step Installation

1. **Clone the repository:**
```bash
git clone https://github.com/jiehai4/PDF-Skill.git
cd PDF-Skill
```

2. **Create virtual environment:**
```bash
# Using uv (recommended)
uv venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

3. **Install dependencies:**
```bash
uv pip install -r pdf-skill/scripts/requirements.txt
```

4. **For GPU support (optional):**
```bash
# Install CUDA-enabled PyTorch
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### Verify Installation
```bash
python -c "import pdf_reader; print('✓ PDF-Skill ready!')"
```

---

## Usage

### As MCP Server (Recommended)

#### Claude Desktop Integration
1. Locate config file:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%AppData%/Claude/claude_desktop_config.json`

2. Add configuration:
```json
{
    "mcpServers": {
        "pdf_reader": {
            "command": "uv",
            "args": [
                "--directory",
                "/path/to/PDF-Skill",
                "run",
                "pdf_reader"
            ]
        }
    }
}
```

3. Restart Claude Desktop

#### Start MCP Server
```bash
uv run pdf_reader
```

The server will start and wait for connections from Claude or other MCP clients.

### As Python Library

```python
from pdf_reader.server import (
    extract_text_from_pdf,
    extract_images_from_pdf,
    extract_tables_from_pdf,
    analyze_pdf_content,
    get_pdf_metadata,
    classify_pdf_document,
    calculate_pdf_similarity
)

# Text extraction
text = extract_text_from_pdf("document.pdf")

# Analyze content
entities = analyze_pdf_content("document.pdf", mode="entities")
summary = analyze_pdf_content("document.pdf", mode="summary")
keywords = analyze_pdf_content("document.pdf", mode="keywords")

# Get metadata
metadata = get_pdf_metadata("document.pdf")

# Classify document
categories = ["Report", "Invoice", "Legal Document", "Other"]
classification = classify_pdf_document("document.pdf", categories)

# Calculate similarity
similarity = calculate_pdf_similarity("doc1.pdf", "doc2.pdf")
```

### Command-Line Scripts

PDF-Skill includes standalone Python scripts for direct CLI usage:

```bash
# Extract text from all pages
python pdf-skill/scripts/extract_text.py document.pdf

# Extract images
python pdf-skill/scripts/extract_images.py document.pdf --output ./images

# Extract tables
python pdf-skill/scripts/extract_tables.py document.pdf

# Analyze content
python pdf-skill/scripts/analyze_content.py document.pdf --mode entities

# Get metadata
python pdf-skill/scripts/get_metadata.py document.pdf

# Classify document
python pdf-skill/scripts/classify_document.py document.pdf --categories "Report,Invoice,Legal"

# Detect languages
python pdf-skill/scripts/detect_languages.py document.pdf

# Advanced analysis
python pdf-skill/scripts/advanced_analysis.py document.pdf

# Calculate similarity
python pdf-skill/scripts/calculate_similarity.py doc1.pdf doc2.pdf
```

---

## API Reference

### Core Tools

#### extract_text_from_pdf(file_path, pages=None)
Extract text content from a PDF file.

**Parameters:**
- `file_path` (str): Path to PDF file
- `pages` (list, optional): Specific page numbers to extract. If None, extracts all pages

**Returns:** Extracted text (str)

#### extract_images_from_pdf(file_path, pages=None)
Extract images from PDF with base64 encoding.

**Parameters:**
- `file_path` (str): Path to PDF file
- `pages` (list, optional): Specific page numbers. If None, extracts from all pages

**Returns:** List of base64-encoded images with metadata

#### extract_tables_from_pdf(file_path, pages=None)
Extract structured tables from PDF.

**Parameters:**
- `file_path` (str): Path to PDF file
- `pages` (list, optional): Specific page numbers

**Returns:** Structured table data (dict or DataFrame)

#### analyze_pdf_content(file_path, mode="entities")
Analyze PDF content using NLP.

**Parameters:**
- `file_path` (str): Path to PDF file
- `mode` (str): Analysis mode - "entities", "summary", or "keywords"

**Returns:** Analysis results (dict)

#### classify_pdf_document(file_path, categories)
Zero-shot document classification.

**Parameters:**
- `file_path` (str): Path to PDF file
- `categories` (list): Category labels for classification

**Returns:** Classification results with scores (dict)

#### calculate_pdf_similarity(file_path1, file_path2)
Calculate semantic similarity between two PDFs.

**Parameters:**
- `file_path1` (str): Path to first PDF
- `file_path2` (str): Path to second PDF

**Returns:** Similarity score (float, 0-1)

#### detect_pdf_languages(file_path)
Detect languages in PDF with per-paragraph analysis.

**Parameters:**
- `file_path` (str): Path to PDF file

**Returns:** Language detection results (dict)

---

## Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP Server Interface                      │
│              (Claude Desktop, API Clients)                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                  Tool Handlers (server.py)                   │
│  • extract_text    • extract_images    • extract_tables      │
│  • analyze_content • get_metadata      • classify_document   │
│  • calculate_similarity  • detect_languages  • advanced_analysis│
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              Model Manager (Singleton Pattern)               │
│  • Lazy Loading      • Memory Management   • Device Selection│
│  • Auto-Cleanup      • Quantization        • GPU/CPU Switch  │
└──────────────────────┬──────────────────────────────────────┘
                       │
       ┌───────────────┼───────────────┐
       │               │               │
   ┌───▼──┐        ┌───▼──┐       ┌──▼────┐
   │Spacy │        │Hugging│      │Sentence│
   │      │        │Face   │      │Trans.  │
   │ NLP  │        │Models │      │ Embed  │
   └──────┘        └───────┘      └────────┘
       │               │               │
       └───────────────┼───────────────┘
                       │
       ┌───────────────┼───────────────┐
       │               │               │
   ┌───▼──────┐   ┌───▼──────┐   ┌───▼──────┐
   │PyMuPDF   │   │PDFMiner  │   │Tabula    │
   │          │   │          │   │          │
   │Extract   │   │Table     │   │Table     │
   │          │   │Detect    │   │Parse     │
   └──────────┘   └──────────┘   └──────────┘
```

### Core Components

#### ModelManager (server.py:30-323)
Central singleton for ML model lifecycle management:

- **Lazy Loading**: Models load on first access only
- **Memory Monitoring**: Tracks system memory and unloads least-used models at 80% threshold
- **Auto-Cleanup**: Background thread removes idle models (default: 300s)
- **Device Selection**: Auto-detects CUDA and selects GPU/CPU
- **Quantization**:
  - CPU: Dynamic int8 quantization
  - GPU: Static float16 quantization

**Managed Models:**
1. `spacy` - en_core_web_sm for NLP tasks
2. `classifier` - facebook/bart-large-mnli for zero-shot classification
3. `sentence_transformer` - paraphrase-MiniLM-L6-v2 for similarity

#### Tool Implementation Pattern
Each tool follows:
1. Definition in `handle_list_tools()` with JSON schema
2. Async implementation function
3. Handler in `handle_call_tool()`
4. Error handling with fallback responses

### Configuration

#### ModelManager Settings (server.py:35-36)
```python
_memory_threshold = 0.8     # Unload models at 80% system memory
_max_idle_time = 300        # Unload after 5 minutes of inactivity
```

#### Device Selection
- CUDA GPU if available (4GB+ VRAM)
- CPU with int8 quantization (memory-constrained)
- Automatic fallback on OOM errors

---

## Common Workflows

### Extract and Analyze a Document
```python
from pdf_reader.server import (
    extract_text_from_pdf,
    analyze_pdf_content,
    get_pdf_metadata
)

# Get basic info
metadata = get_pdf_metadata("report.pdf")
print(f"Title: {metadata['title']}, Pages: {metadata['page_count']}")

# Extract and analyze
text = extract_text_from_pdf("report.pdf")
entities = analyze_pdf_content("report.pdf", mode="entities")
summary = analyze_pdf_content("report.pdf", mode="summary")
keywords = analyze_pdf_content("report.pdf", mode="keywords")

print(f"Summary: {summary}")
print(f"Key Entities: {entities}")
print(f"Keywords: {keywords}")
```

### Process Tables from Financial Reports
```python
from pdf_reader.server import extract_tables_from_pdf

tables = extract_tables_from_pdf("financial_report.pdf")
for i, table in enumerate(tables):
    # Convert to CSV or JSON
    table.to_csv(f"table_{i}.csv")
```

### Batch Classification of Multiple Documents
```python
import os
from pdf_reader.server import classify_pdf_document

categories = ["Technical", "Business", "Legal", "Financial"]

for pdf_file in os.listdir("documents/"):
    if pdf_file.endswith(".pdf"):
        result = classify_pdf_document(f"documents/{pdf_file}", categories)
        print(f"{pdf_file}: {result['category']} ({result['score']:.2f})")
```

### Image-Based PDF Handling
```python
from pdf_reader.server import extract_text_from_pdf, extract_images_from_pdf

# Attempt text extraction
text = extract_text_from_pdf("scanned_document.pdf")

# If result is too short, likely image-based
if len(text.strip()) < 100:
    print("⚠️ Image-based PDF detected. Extracting images...")
    images = extract_images_from_pdf("scanned_document.pdf")
    print(f"Extracted {len(images)} images")
    # Use external OCR service for text extraction
```

---

## Performance Optimization

### For Large Documents
```python
# Process specific page ranges instead of entire document
text = extract_text_from_pdf("large_doc.pdf", pages=[0, 1, 2])  # First 3 pages
```

### For Memory-Constrained Systems
- Models use int8 quantization on CPU by default
- Automatic unloading of idle models
- Configurable memory threshold (default: 80%)

### For GPU Acceleration
```bash
# Install CUDA-enabled PyTorch
pip install torch --index-url https://download.pytorch.org/whl/cu118
```
Server auto-detects CUDA and uses GPU for:
- NLP analysis
- Document classification
- Similarity calculation

### Model Memory Management
```python
from pdf_reader.server import ModelManager

manager = ModelManager()
memory_usage = manager.get_model_memory_usage()
print(f"Current model memory: {memory_usage['total']:.2f}MB")
```

---

## Troubleshooting

### "ImportError: No module named 'torch'"
Install dependencies:
```bash
uv pip install -r pdf-skill/scripts/requirements.txt
```

### "CUDA out of memory"
1. Reduce batch size
2. Enable quantization (enabled by default)
3. Increase swap memory
4. Use CPU mode: `CUDA_VISIBLE_DEVICES="" python -m pdf_reader`

### "Text extraction returns empty"
PDF might be image-based (scanned document). Use image extraction instead:
```python
from pdf_reader.server import extract_images_from_pdf
images = extract_images_from_pdf("document.pdf")
```

### Slow initialization
Models load lazily on first access. First call may take 30-60s. Subsequent calls are instant.

### High memory usage
- Models are automatically unloaded after 5 minutes of inactivity
- Check usage with `ModelManager.get_model_memory_usage()`
- Reduce `_max_idle_time` to unload faster

---

## Dependencies

### PDF Processing
- **PyMuPDF** (1.23.8) - Fast PDF reading and rendering
- **pdfminer.six** (20221105) - Text extraction and analysis
- **tabula-py** (2.5.1) - Table extraction
- **pandas** (2.1.4) - Data manipulation

### NLP & Machine Learning
- **spacy** (3.7.2) - Named entity recognition, dependency parsing
- **transformers** (4.36.2) - Hugging Face models
- **torch** (2.1.2) - Deep learning framework
- **sentence-transformers** (2.2.2) - Semantic embeddings
- **scikit-learn** (1.3.2) - ML utilities
- **nltk** (3.8.1) - Text processing
- **langdetect** (1.0.9) - Language detection

### Utilities
- **Pillow** (10.1.0) - Image processing
- **numpy** (1.26.3) - Numerical computing

---

## Configuration

### Environment Variables
```bash
# Use CPU only (disable GPU)
export CUDA_VISIBLE_DEVICES=""

# Set MCP server port
export MCP_PORT=5000
```

### Model Configuration (server.py)
```python
# Adjust memory threshold
ModelManager._memory_threshold = 0.85  # 85% instead of 80%

# Change idle timeout (seconds)
ModelManager._max_idle_time = 600      # 10 minutes instead of 5
```

---

## Development

### Project Structure
```
pdf-skill/
├── scripts/                  # Standalone Python scripts
│   ├── extract_text.py
│   ├── extract_images.py
│   ├── extract_tables.py
│   ├── analyze_content.py
│   ├── get_metadata.py
│   ├── classify_document.py
│   ├── calculate_similarity.py
│   ├── detect_languages.py
│   ├── advanced_analysis.py
│   └── requirements.txt
├── references/              # API documentation
│   ├── api_reference.md
│   └── examples.md
└── README.md               # This file
```

### Running Tests
```bash
# Test basic functionality
python pdf-skill/scripts/extract_text.py sample.pdf

# Test with various PDF types
python pdf-skill/scripts/extract_text.py sample_scanned.pdf
python pdf-skill/scripts/extract_tables.py sample_tables.pdf
```

### Adding New Features
1. Create implementation function in scripts/
2. Add MCP tool definition to handle_list_tools()
3. Add handler to handle_call_tool()
4. Update this README

---

## Known Limitations

- **OCR Not Supported**: Use external OCR for scanned PDFs without extractable text
- **Complex Tables**: May need post-processing for multi-level headers
- **Encrypted PDFs**: Requires password or decryption before processing
- **Language Support**: Entity recognition limited to English (use spacy's other language models for others)
- **Layout Analysis**: Does not preserve exact visual layout (use PyMuPDF blocks for advanced layout detection)

---

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see LICENSE file for details.

---

## Contact & Support

- **Author**: jiehai4
- **Email**: 383942426@qq.com
- **GitHub**: [jiehai4/PDF-Skill](https://github.com/jiehai4/PDF-Skill)
- **Issues**: [GitHub Issues](https://github.com/jiehai4/PDF-Skill/issues)

---

## Acknowledgments

Built with:
- [PyMuPDF](https://pymupdf.readthedocs.io/) for PDF processing
- [Spacy](https://spacy.io/) for NLP
- [Hugging Face Transformers](https://huggingface.co/) for state-of-the-art models
- [Sentence Transformers](https://www.sbert.net/) for semantic embeddings
- [Model Context Protocol](https://modelcontextprotocol.io/) for integration

---

<div align="center">

**Made with ❤️ for PDF enthusiasts and developers**

[⬆ Back to top](#pdf-skill---advanced-pdf-processing-mcp-server)

</div>
