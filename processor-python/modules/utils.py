"""
Utility functions for the PDF processing system.
"""
import os
import shutil
import logging

def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def clean_tmp_directory(tmp_dir):
    """Clean up temporary files."""
    try:
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        os.makedirs(tmp_dir)
    except Exception as e:
        raise Exception(f"Failed to clean temporary directory: {str(e)}")

def ensure_directory(directory):
    """Ensure a directory exists, create if it doesn't."""
    os.makedirs(directory, exist_ok=True)
