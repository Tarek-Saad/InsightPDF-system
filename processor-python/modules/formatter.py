"""
Text formatting and styling module.
"""
import re

class TextFormatter:
    def __init__(self, config=None):
        self.default_format = {
            'paragraph_spacing': 2,
            'line_spacing': 1.5
        }
        if config:
            self.default_format.update(config)
    
    def format_text(self, text, format_options=None):
        """Format text according to specified options."""
        if format_options is None:
            format_options = self.default_format
            
        # Split into paragraphs
        paragraphs = text.split('\n\n')
        
        # Apply formatting
        formatted_paragraphs = [p.strip() for p in paragraphs]
        
        # Join with specified spacing
        result = ('\n' * format_options['paragraph_spacing']).join(formatted_paragraphs)
        
        return result
