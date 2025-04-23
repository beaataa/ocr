# ocr_standalone.py - Simplified OCR module for image and PDF text extraction

import os
import argparse
import pytesseract
from PIL import Image
import pdf2image
import numpy as np
import cv2

def preprocess_image(img):
    """
    Preprocess image for better OCR results
    
    Args:
        img: numpy array of the image
        
    Returns:
        Preprocessed image
    """
    # Convert to grayscale if it's a color image
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    
    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )
    
    # Perform noise removal
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    
    return opening

def process_image_file(image_path):
    """
    Process a single image file
    
    Args:
        image_path: Path to image file
    
    Returns:
        Extracted text
    """
    try:
        # Load image
        img = cv2.imread(image_path)
        if img is None:
            print(f"Failed to load image: {image_path}")
            return None
        
        # Preprocess image
        preprocessed = preprocess_image(img)
        
        # Save preprocessed image for inspection (optional)
        cv2.imwrite("preprocessed_" + os.path.basename(image_path), preprocessed)
        
        # Perform OCR
        text = pytesseract.image_to_string(preprocessed)
        
        return text
    
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return None

def process_pdf_file(pdf_path, output_folder="extracted_pages"):
    """
    Process a PDF file by converting to images and performing OCR
    
    Args:
        pdf_path: Path to PDF file
        output_folder: Folder to save extracted page images (optional)
        
    Returns:
        List of dictionaries with page numbers and extracted text
    """
    results = []
    
    try:
        # Create output folder if it doesn't exist
        if output_folder:
            os.makedirs(output_folder, exist_ok=True)
        
        # Convert PDF to list of images
        print(f"Converting PDF to images: {pdf_path}")
        images = pdf2image.convert_from_path(pdf_path)
        
        for i, image in enumerate(images):
            page_num = i + 1
            print(f"Processing page {page_num}/{len(images)}")
            
            # Convert PIL Image to numpy array for OpenCV processing
            img_array = np.array(image)
            
            # Preprocess image
            preprocessed = preprocess_image(img_array)
            
            # Save preprocessed image for inspection (optional)
            if output_folder:
                page_filename = f"page_{page_num}.jpg"
                preprocessed_filename = f"preprocessed_page_{page_num}.jpg"
                
                # Save original page
                image.save(os.path.join(output_folder, page_filename))
                
                # Save preprocessed page
                cv2.imwrite(os.path.join(output_folder, preprocessed_filename), preprocessed)
            
            # Perform OCR on preprocessed image
            text = pytesseract.image_to_string(preprocessed)
            
            results.append({
                'page': page_num,
                'text': text
            })
        
        return results
    
    except Exception as e:
        print(f"Error processing PDF {pdf_path}: {e}")
        return []

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Standalone OCR Processor')
    parser.add_argument('--input', required=True, help='Path to input PDF or image file')
    parser.add_argument('--output', default='extracted_text.txt', help='Path to output text file')
    parser.add_argument('--pages', action='store_true', help='Save extracted pages from PDFs')
    parser.add_argument('--pages-dir', default='extracted_pages', help='Directory to save extracted pages')
    args = parser.parse_args()
    
    # Process the input file
    input_path = args.input
    file_ext = os.path.splitext(input_path)[1].lower()
    
    if file_ext == '.pdf':
        results = process_pdf_file(input_path, args.pages_dir if args.pages else None)
        
        # Write results to output file
        with open(args.output, 'w', encoding='utf-8') as f:
            for page_result in results:
                f.write(f"\n\n===== PAGE {page_result['page']} =====\n\n")
                f.write(page_result['text'])
        
        print(f"Extracted text from {len(results)} pages saved to {args.output}")
        
    elif file_ext in ['.jpg', '.jpeg', '.png', '.tiff', '.bmp']:
        text = process_image_file(input_path)
        
        if text:
            # Write results to output file
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(text)
            
            print(f"Extracted text saved to {args.output}")
    else:
        print(f"Unsupported file format: {file_ext}")
        print("Supported formats: PDF, JPG, JPEG, PNG, TIFF, BMP")

if __name__ == "__main__":
    main()