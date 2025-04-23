# OCR Standalone Tool

A Python-based OCR utility for extracting text from PDF documents. Optimized for multi-page PDF processing with basic image preprocessing for improved accuracy.

## Features

- PDF-to-text conversion with page-by-page processing
- Automatic image preprocessing:
  - Grayscale conversion
  - Adaptive thresholding
  - Noise reduction
- Page image extraction option
- Simple command-line interface

## Installation

### 1. System Dependencies

**macOS:**
```bash
brew install tesseract poppler
```

**Windows/Linux:**  
Install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) and [Poppler](https://poppler.freedesktop.org/)

### 2. Python Requirements
```bash
pip install -r requirements.txt
```


## Usage

### Basic PDF Extraction
```bash
python ocr_standalone.py --input=document.pdf --output=output.txt
```

**With page images:**
```bash
python ocr_standalone.py --input=document.pdf --output=output.txt --pages
```

**Arguments:**
- `--input`: Input PDF file (required)
- `--output`: Output text file 
- `--pages`: Save extracted page images

## Best Practices
- Use 300+ DPI scans for best results
- Prefer B&W documents over color
- Inspect `preprocessed_page_XX.jpg` if results are poor

## Limitations
- Optimized for PDFs (image file support limited)
- Struggles with:
  - Complex layouts/tables
  - Handwritten text
  - Low-quality scans
- Processing speed: ~2-5 seconds/page

## Troubleshooting
1. Verify input file quality
2. Check preprocessing results in page images
3. Ensure system dependencies are installed
