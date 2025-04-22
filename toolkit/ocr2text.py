# INFORMATION:
# - Tool: OCR Scanner
# - Description: Optical Character Recognition tool
# - Usage: Extracts text from images and PDF files
# - Parameters: file_path (required)

import cv2
import pytesseract
from pdf2image import convert_from_path
import os
import numpy as np
from typing import Dict, Any

# Configure Tesseract path - use system path for Kali Linux
if os.path.exists('/usr/bin/tesseract'):
    pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
elif os.path.exists('/usr/local/bin/tesseract'):
    pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'

def process_image(img):
    """Process image for better OCR results"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray, img_bin = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    gray = cv2.bitwise_not(img_bin)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
    dilation = cv2.dilate(gray, kernel, iterations=1)
    erosion = cv2.erode(dilation, kernel, iterations=1)

    text = pytesseract.image_to_string(erosion)
    return text

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file using OCR"""
    try:
        # Use poppler_path if on Windows, but we're in Kali Linux so not needed
        images = convert_from_path(pdf_path)
        
        all_text = []
        for i, image in enumerate(images):
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            text = process_image(opencv_image)
            all_text.append(f"=== Page {i+1} ===\n{text}\n")
        
        return "\n".join(all_text)
    except Exception as e:
        return f"Error processing PDF: {str(e)}"

def extract_text_from_image(image_path):
    """Extract text from an image file using OCR"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            return f"Error: Could not read image file {image_path}"
        return process_image(img)
    except Exception as e:
        return f"Error processing image: {str(e)}"

def ExecOcr2Text(file_path: str) -> Dict[str, Any]:
    """Execute OCR on a file (image or PDF)"""
    if not os.path.exists(file_path):
        return {
            "success": False,
            "error": f"File not found: {file_path}",
            "text": ""
        }
    
    file_ext = os.path.splitext(file_path)[1].lower()
    try:
        if file_ext == '.pdf':
            text = extract_text_from_pdf(file_path)
        elif file_ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']:
            text = extract_text_from_image(file_path)
        else:
            return {
                "success": False,
                "error": f"Unsupported file format: {file_ext}",
                "text": ""
            }
            
        return {
            "success": True,
            "error": "",
            "text": text
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "text": ""
        }
