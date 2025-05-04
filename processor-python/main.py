"""
Main entry point for the PDF processing pipeline.
"""
import argparse
import json
import os
import logging
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

from modules.ocr import OCRProcessor
from modules.summarizer import Summarizer
from modules.formatter import TextFormatter
from modules.merger import PDFMerger
from modules.utils import setup_logging, clean_tmp_directory, ensure_directory

def load_config(config_path):
    """Load configuration from JSON file."""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load config from {config_path}: {str(e)}")
        return {}

def create_caption_page(output_path, summary_data):
    """Create a professional caption page using ReportLab."""
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceBefore=20,
        spaceAfter=10
    )

    # Add title
    story.append(Paragraph("Document Analysis Report", title_style))
    story.append(Spacer(1, 20))

    # Add summary section
    story.append(Paragraph("Document Summary", heading_style))
    story.append(Paragraph(summary_data['summary'], styles['Normal']))
    story.append(Spacer(1, 20))

    # Add statistics
    story.append(Paragraph("Document Statistics", heading_style))
    stats = f"Total Pages: {summary_data['total_pages']}<br/>"
    stats += f"Total Characters: {summary_data['total_chars']}"
    story.append(Paragraph(stats, styles['Normal']))

    # Build the PDF
    doc.build(story)

def parse_args():
    parser = argparse.ArgumentParser(description='PDF Processing Pipeline')
    parser.add_argument('input_pdf', help='Path to input PDF file')
    parser.add_argument('--output', help='Output path', default='output.pdf')
    parser.add_argument('--config', help='Path to config file', default='../shared/config.json')
    parser.add_argument('--caption-page', help='Generate caption page', action='store_true')
    return parser.parse_args()

def main():
    # Setup
    setup_logging()
    args = parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Initialize components
    ocr = OCRProcessor(config.get('ocr'))
    summarizer = Summarizer(config.get('summarizer'))
    formatter = TextFormatter()  # No config needed
    merger = PDFMerger()
    
    # Ensure tmp directory exists
    tmp_dir = os.path.join(os.path.dirname(__file__), 'tmp')
    clean_tmp_directory(tmp_dir)
    
    try:
        # Process PDF pages
        logging.info(f"Processing PDF: {args.input_pdf}")
        pages = ocr.process_pdf(args.input_pdf, tmp_dir)
        
        # Generate summary
        prompt_path = os.path.join(os.path.dirname(args.config), 'prompts/summarization_prompt.txt')
        summary_data = summarizer.summarize_document(pages, prompt_path)
        
        # Create output directory if needed
        output_dir = os.path.dirname(os.path.abspath(args.output))
        ensure_directory(output_dir)
        
        if args.caption_page:
            # Generate caption page
            caption_pdf = os.path.join(output_dir, 'caption.pdf')
            create_caption_page(caption_pdf, summary_data)
            
            # Merge caption page with original PDF
            merger.add_pdf(caption_pdf)
            merger.add_pdf(args.input_pdf)
            merger.save(args.output)
            
            # Clean up temporary caption page
            os.remove(caption_pdf)
        else:
            # Just copy the original PDF if no caption page is needed
            import shutil
            shutil.copy2(args.input_pdf, args.output)
        
        logging.info(f"Processing complete. Output saved to: {args.output}")
        return 0
        
    except Exception as e:
        logging.error(f"Error processing PDF: {str(e)}")
        return 1

if __name__ == '__main__':
    exit(main())
