# MD2PDF

Markdown to PDF converter with GitHub-style rendering.

## Features

- Convert Markdown to PDF with GitHub-flavored styling
- Syntax highlighting for code blocks
- Support for tables, task lists, footnotes, and more
- REST API for easy integration

## Installation

```bash
uv sync
```

## Usage

### Start the server

```bash
uv run md2pdf
```

Or directly with uvicorn:

```bash
uv run uvicorn md2pdf.main:app --reload
```

The server will start at `http://localhost:8000`.

### API Endpoints

#### `POST /convert`

Convert markdown to PDF.

**Request:**

```json
{
  "markdown": "# Hello World\n\nThis is **bold** text.",
  "filename": "output.pdf"
}
```

**Response:** PDF file download

#### `GET /health`

Health check endpoint.

#### `GET /`

API information.

### Example with curl

```bash
curl -X POST http://localhost:8000/convert \
  -H "Content-Type: application/json" \
  -d '{"markdown": "# Hello\n\nWorld"}' \
  --output document.pdf
```

### Example with Python

```python
import requests

markdown_content = """
# My Document

## Introduction

This is a **sample** markdown document with:

- Lists
- Code blocks
- Tables

```python
def hello():
    print("Hello, World!")
```

| Name | Value |
|------|-------|
| A    | 1     |
| B    | 2     |
"""

response = requests.post(
    "http://localhost:8000/convert",
    json={"markdown": markdown_content, "filename": "my-document.pdf"}
)

with open("my-document.pdf", "wb") as f:
    f.write(response.content)
```

## Supported Markdown Features

- Headings (h1-h6)
- Bold, italic, strikethrough
- Lists (ordered, unordered, nested)
- Task lists
- Code blocks with syntax highlighting
- Inline code
- Tables
- Blockquotes
- Horizontal rules
- Links
- Images
- Footnotes
- Definition lists
- Abbreviations
- Admonitions

## Development

### Run tests

```bash
uv run pytest
```

## License

MIT
