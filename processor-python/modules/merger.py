"""
PDF merging and manipulation module.
"""
from PyPDF2 import PdfMerger

class PDFMerger:
    def __init__(self):
        self.merger = PdfMerger()
    
    def add_pdf(self, pdf_path, pages=None):
        """Add a PDF file to the merger."""
        try:
            self.merger.append(pdf_path, pages=pages)
        except Exception as e:
            raise Exception(f"Failed to add PDF {pdf_path}: {str(e)}")
    
    def save(self, output_path):
        """Save the merged PDF to the specified path."""
        try:
            self.merger.write(output_path)
            self.merger.close()
        except Exception as e:
            raise Exception(f"Failed to save merged PDF: {str(e)}")
