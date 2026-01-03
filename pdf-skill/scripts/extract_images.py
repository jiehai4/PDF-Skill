#!/usr/bin/env python3
"""
Extract images from PDF files with base64 encoding.

Usage:
    extract_images.py <pdf_path> [--page <page_number>] [--output <output_dir>]

Examples:
    extract_images.py document.pdf
    extract_images.py document.pdf --page 0
    extract_images.py document.pdf --output ./images
"""

import sys
import argparse
import base64
import io
import os
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image
import json


def optimize_image(image: Image.Image, max_size: tuple = (1920, 1080)) -> Image.Image:
    """
    Optimize image size while maintaining quality.

    Args:
        image: PIL Image object
        max_size: Maximum dimensions (width, height)

    Returns:
        Optimized PIL Image object
    """
    if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
    return image


def extract_images(file_path: str, page_number: int = None) -> dict:
    """
    Extract images from PDF file.

    Args:
        file_path: Path to the PDF file
        page_number: Optional page number (0-indexed) to extract specific page

    Returns:
        Dictionary containing image data and metadata
    """
    try:
        doc = fitz.open(file_path)
        images_data = []
        pages = [page_number] if page_number is not None else range(len(doc))

        for page_num in pages:
            if page_num >= len(doc):
                continue

            page = doc[page_num]
            image_list = page.get_images()

            for img_index, img_info in enumerate(image_list):
                try:
                    xref = img_info[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]

                    # Convert and optimize image
                    image = Image.open(io.BytesIO(image_bytes))
                    image = optimize_image(image)

                    # Convert to base64
                    buffered = io.BytesIO()
                    image.save(buffered, format="PNG", optimize=True)
                    img_str = base64.b64encode(buffered.getvalue()).decode()

                    images_data.append({
                        "page": page_num,
                        "index": img_index,
                        "size": image.size,
                        "format": "PNG",
                        "base64": img_str
                    })

                except Exception as e:
                    images_data.append({
                        "page": page_num,
                        "index": img_index,
                        "error": str(e)
                    })

        doc.close()

        return {
            "success": True,
            "total_images": len(images_data),
            "images": images_data
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Error extracting images: {str(e)}"
        }


def main():
    parser = argparse.ArgumentParser(
        description="Extract images from PDF files"
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
        help="Output directory to save images (if not specified, outputs JSON to stdout)"
    )

    args = parser.parse_args()

    # Extract images
    result = extract_images(args.pdf_path, args.page)

    if args.output:
        # Create output directory
        os.makedirs(args.output, exist_ok=True)

        # Save images
        for i, img_data in enumerate(result.get("images", [])):
            if "base64" in img_data:
                image_path = Path(args.output) / f"page_{img_data['page']}_img_{img_data['index']}.png"
                with open(image_path, 'wb') as f:
                    f.write(base64.b64decode(img_data["base64"]))
                print(f"Saved: {image_path}")

        # Save metadata
        metadata_path = Path(args.output) / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            # Remove base64 data from metadata for readability
            clean_result = {
                "success": result["success"],
                "total_images": result["total_images"],
                "images": [{k: v for k, v in img.items() if k != "base64"} for img in result.get("images", [])]
            }
            json.dump(clean_result, f, indent=2, ensure_ascii=False)

        print(f"\nImages extracted to: {args.output}")
    else:
        # Output JSON to stdout
        clean_result = {
            "success": result["success"],
            "total_images": result["total_images"],
            "images": [{k: v for k, v in img.items() if k != "base64"} for img in result.get("images", [])]
        }
        print(json.dumps(clean_result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
