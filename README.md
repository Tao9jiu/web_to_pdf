# Web Crawler and PDF Generator

This project provides tools to crawl websites and generate PDF documentation from the crawled urls.

## Overview

This tool is designed to create a single PDF document from web content by recursively crawling all subpages under a specified path while avoiding duplicate pages. By converting web documentation into a PDF format, you can:

- Create offline-accessible documentation
- Generate consistent training data for AI models
- Build searchable knowledge bases
- Prepare content for AI-powered document analysis

## Features

- Crawl websites and collect URLs
- Convert web pages to PDF
- Combine multiple PDFs into a single document
- Customizable crawling paths and output filenames
- AI-assisted processing with customizable prompts

## Installation

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

The easiest way to use this tool is through the `web_to_pdf.py` script:

#### Usage

```bash
python web_to_pdf.py --base-url "https://example.com" --start-path "/docs/" --output "custom_documentation.pdf" --skip-patterns "#_" "?q=" --cookie-accept-button-text "Accept"
```

Command line arguments:
- `--base-url`: Base URL of the website to crawl (default: "https://python.langchain.com")
- `--start-path`: Starting path for crawling (default: "/docs/")
- `--output`: Output PDF filename (default: "documentation.pdf")
