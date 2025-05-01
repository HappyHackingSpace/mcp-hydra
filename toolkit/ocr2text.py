# INFORMATION:
# - Tool: OCR Scanner
# - Description: Optical Character Recognition tool
# - Usage: Extracts text from images and PDF files
# - Parameters: file_path (required) - can be a local file or URL prefixed with @

import cv2
import pytesseract
from pdf2image import convert_from_path
import os
import numpy as np
from typing import Dict, Any
import requests
import tempfile
from urllib.parse import urlparse

# Configure Tesseract path - use system path for Kali Linux
if os.path.exists('/usr/bin/tesseract'):
    pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
elif os.path.exists('/usr/local/bin/tesseract'):
    pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'
elif os.path.exists('C:\\Program Files\\Tesseract-OCR\\tesseract.exe'):
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def download_image(url):
    """Download image from a URL and save to a temporary file"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Get the file extension from the URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        _, ext = os.path.splitext(filename)
        
        if not ext:
            # Default to .png if no extension found
            ext = '.png'
            
        # Create a temporary file with the correct extension
        temp_file = tempfile.NamedTemporaryFile(suffix=ext, delete=False)
        temp_filename = temp_file.name
        
        # Write the image data to the temporary file
        with open(temp_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        return temp_filename
    except Exception as e:
        print(f"Error downloading image: {str(e)}")
        return None

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
    """Execute OCR on a file (image or PDF) or URL"""
    temp_file = None
    
    try:
        # Check if the file_path is a URL (starts with @ or http/https)
        if file_path.startswith('@'):
            url = file_path[1:]  # Remove the @ symbol
            print(f"Downloading image from URL: {url}")
            temp_file = download_image(url)
        elif file_path.startswith(('http://', 'https://')):
            url = file_path
            print(f"Downloading image from URL: {url}")
            temp_file = download_image(url)
            
        if temp_file is None and (file_path.startswith('@') or file_path.startswith(('http://', 'https://'))):
            return {
                "success": False,
                "error": f"Failed to download image from URL: {url}",
                "text": ""
            }
            
        # Use the temp file if a URL was provided
        if temp_file:
            file_path = temp_file
        
        # Check if the file exists
        if not os.path.exists(file_path):
            return {
                "success": False,
                "error": f"File not found: {file_path}",
                "text": ""
            }
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
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
    finally:
        # Clean up temporary file if it was created
        if temp_file and os.path.exists(temp_file):
            try:
                os.unlink(temp_file)
            except:
                pass
