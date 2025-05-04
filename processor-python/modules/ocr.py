"""
OCR module for extracting text from PDF pages and images.
"""
import os
import logging
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

class OCRProcessor:
    def __init__(self, config=None):
        self.logger = logging.getLogger(__name__)
        self.tesseract_config = config.get('tesseract_config', '--psm 3') if config else '--psm 3'
        self.dpi = 300  # Default DPI for PDF conversion
        
    def process_image(self, image_path):
        """Extract text from an image using OCR."""
        try:
            self.logger.info(f"Processing image: {image_path}")
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, config=self.tesseract_config)
            self.logger.debug(f"Successfully extracted {len(text.split())} words from image")
            return text.strip()
        except Exception as e:
            self.logger.error(f"OCR processing failed for {image_path}: {str(e)}")
            raise Exception(f"OCR processing failed: {str(e)}")

    def process_pdf(self, pdf_path, output_dir):
        """Process all pages in a PDF file."""
        try:
            self.logger.info(f"Converting PDF to images: {pdf_path}")
            pages = convert_from_path(pdf_path, dpi=self.dpi)
            self.logger.info(f"Found {len(pages)} pages in PDF")
            
            results = []
            for i, page in enumerate(pages):
                self.logger.info(f"Processing page {i+1}/{len(pages)}")
                # Save page as temporary image
                temp_image_path = os.path.join(output_dir, f"page_{i+1}.png")
                page.save(temp_image_path, 'PNG')
                
                # Process the page
                text = self.process_image(temp_image_path)
                results.append({
                    'page_num': i+1,
                    'text': text
                })
                
                # Clean up temporary image
                os.remove(temp_image_path)
                
            return results
        except Exception as e:
            self.logger.error(f"PDF processing failed: {str(e)}")
            raise Exception(f"PDF processing failed: {str(e)}")

    def process_page(self, page_image_path):
        """Process a single PDF page."""
        return self.process_image(page_image_path)
