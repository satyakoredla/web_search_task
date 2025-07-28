# Web Search Task

This project is a simple web crawler and search tool implemented in Python. It crawls web pages, indexes their content, and allows keyword-based search across the indexed pages.

## Features
- Crawl web pages and follow links
- Index page content for keyword search
- Print search results in a readable format
- Includes unit tests for core functionality

## Usage
1. Run the script to crawl a starting URL and search for a keyword:
   ```bash
   python psc-2.py
   ```
2. The crawler will start at `https://example.com` and search for the keyword `test` by default.

## Testing
Unit tests are included in `psc-2.py`. To run tests:
```bash
python psc-2.py
```

## Requirements
- Python 3.x
- requests
- beautifulsoup4

Install dependencies with:
```bash
pip install requests beautifulsoup4
```

## Author
- satyakoredla

## Repository
- https://github.com/satyakoredla/web_search_task.git
