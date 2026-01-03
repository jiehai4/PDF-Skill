# PDF Reader Skill - API Reference

Complete API documentation for all pdf-reader skill scripts. See the inline help in each script for detailed usage.

## Quick Script Guide

| Script | Purpose | Usage |
|--------|---------|-------|
| `extract_text.py` | Extract text | `python extract_text.py <pdf> [--page N] [--output file]` |
| `extract_images.py` | Extract images | `python extract_images.py <pdf> [--page N] [--output dir]` |
| `extract_tables.py` | Extract tables | `python extract_tables.py <pdf> [--page N] [--format json\|csv]` |
| `analyze_content.py` | NLP analysis | `python analyze_content.py <pdf> <entities\|summary\|keywords>` |
| `get_metadata.py` | PDF metadata | `python get_metadata.py <pdf>` |
| `classify_document.py` | Classify | `python classify_document.py <pdf> <categories>` |
| `calculate_similarity.py` | Compare PDFs | `python calculate_similarity.py <pdf1> <pdf2>` |
| `detect_languages.py` | Detect languages | `python detect_languages.py <pdf>` |
| `advanced_analysis.py` | Advanced stats | `python advanced_analysis.py <pdf>` |

## Installation

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Common Patterns

### Extract and Analyze
```bash
python extract_text.py document.pdf > text.txt
python analyze_content.py document.pdf entities > entities.json
```

### Process Multiple PDFs
```bash
for pdf in *.pdf; do
    python get_metadata.py "$pdf" --output "${pdf%.pdf}_metadata.json"
done
```

### Compare Documents
```bash
python calculate_similarity.py doc1.pdf doc2.pdf
```

## Output Formats

Most scripts support JSON output and file output options. Use `--output` flag to save to file, or output goes to stdout.

## Error Handling

All scripts return `{"success": false, "error": "..."}` on failure. Check the error message for details.

## Performance Tips

- Process large PDFs by page using `--page` parameter
- Advanced analyses use GPU if available
- First run downloads models (5-10 minutes, downloads once)

## See Also

- Run any script with `--help` for detailed usage
- Check inline docstrings in Python files for implementation details
