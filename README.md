# InsightPDF System

A comprehensive PDF processing system that includes OCR, summarization, formatting, and merging capabilities.

## Project Structure

```
├── processor-python/     # Python document processing engine
│   ├── modules/         # Core processing modules
│   ├── main.py         # Entry script
│   ├── requirements.txt
│   └── tmp/            # Temporary processing directory
├── shared/             # Shared configurations and prompts
└── README.md
```

## Setup

1. Install the required dependencies:
```bash
cd processor-python
pip install -r requirements.txt
```

2. Configure the system by modifying `shared/config.json`

## Usage

Run the main processing script:
```bash
python main.py [options]
```
