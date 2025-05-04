"""
Text summarization module using NLP techniques.
"""
import logging
import json
from pathlib import Path
from transformers import pipeline

class Summarizer:
    def __init__(self, config=None):
        self.logger = logging.getLogger(__name__)
        
        # Load configuration
        if config:
            self.model_name = config.get('model_name', 'facebook/bart-large-cnn')
            self.max_length = config.get('max_length', 130)
            self.min_length = config.get('min_length', 30)
        else:
            self.model_name = 'facebook/bart-large-cnn'
            self.max_length = 130
            self.min_length = 30
        
        self.logger.info(f"Initializing summarizer with model: {self.model_name}")
        try:
            self.summarizer = pipeline("summarization", model=self.model_name)
            self.logger.info("Summarizer initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize summarizer: {str(e)}")
            raise
        
    def summarize(self, text, max_length=None, min_length=None):
        """Generate a summary of the given text."""
        if not text.strip():
            self.logger.warning("Empty text provided for summarization")
            return ""

        max_length = max_length or self.max_length
        min_length = min_length or self.min_length

        self.logger.info(f"Summarizing text of length {len(text)} characters")
        try:
            summary = self.summarizer(text, max_length=max_length, min_length=min_length)
            result = summary[0]['summary_text']
            self.logger.info(f"Successfully generated summary of length {len(result)} characters")
            return result
        except Exception as e:
            self.logger.error(f"Summarization failed: {str(e)}")
            raise Exception(f"Summarization failed: {str(e)}")

    def summarize_document(self, pages, prompt_path=None):
        """Summarize a multi-page document."""
        self.logger.info(f"Summarizing document with {len(pages)} pages")
        
        # Load custom prompt if provided
        prompt = ""
        if prompt_path and Path(prompt_path).exists():
            try:
                with open(prompt_path, 'r') as f:
                    prompt = f.read().strip() + "\n\n"
            except Exception as e:
                self.logger.warning(f"Failed to load prompt from {prompt_path}: {str(e)}")
        
        # Combine all pages
        full_text = "\n\n".join(page['text'] for page in pages)
        
        # Generate summary
        summary = self.summarize(prompt + full_text)
        
        return {
            'summary': summary,
            'total_pages': len(pages),
            'total_chars': len(full_text)
        }
