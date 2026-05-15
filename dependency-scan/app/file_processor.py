"""
File Processor Module
Handles uploaded files — images and data files.
Uses Pillow for image processing.
Pillow 9.0.0 has known CVEs related to image parsing.
"""

from PIL import Image
import io
import os


def process_upload(uploaded_file) -> dict:
    """
    Process an uploaded file.
    Supports: images (PNG, JPEG), CSV data files.

    CVE NOTE: Pillow 9.0.0 is affected by CVE-2023-44271 —
    a crafted image file can cause excessive memory allocation,
    leading to denial of service. Fixed in Pillow 10.0.1+.

    In this application, image processing is used for resizing
    employee profile photos in financial reports — low-severity
    context but the DoS risk is real if the endpoint is accessible.
    """

    filename = uploaded_file.filename
    if not filename:
        return {"error": "Empty filename"}

    file_ext = os.path.splitext(filename)[1].lower()

    if file_ext in ['.png', '.jpg', '.jpeg']:
        return _process_image(uploaded_file, filename)
    elif file_ext == '.csv':
        return _process_csv(uploaded_file, filename)
    else:
        return {"error": f"Unsupported file type: {file_ext}"}


def _process_image(file_obj, filename: str) -> dict:
    """Process an image file using Pillow."""
    try:
        file_content = file_obj.read()
        img = Image.open(io.BytesIO(file_content))

        original_size = img.size
        # Resize to thumbnail
        img.thumbnail((256, 256))
        resized_size = img.size

        return {
            "type": "image",
            "filename": filename,
            "original_size": f"{original_size[0]}x{original_size[1]}",
            "resized_to": f"{resized_size[0]}x{resized_size[1]}",
            "format": img.format,
            "mode": img.mode,
            "status": "processed"
        }
    except Exception as e:
        return {"error": f"Image processing failed: {str(e)}"}


def _process_csv(file_obj, filename: str) -> dict:
    """Process a CSV data file."""
    try:
        content = file_obj.read().decode('utf-8')
        lines = content.strip().split('\n')
        row_count = len(lines) - 1  # subtract header
        return {
            "type": "csv",
            "filename": filename,
            "rows": row_count,
            "headers": lines[0] if lines else "",
            "status": "processed"
        }
    except Exception as e:
        return {"error": f"CSV processing failed: {str(e)}"}
