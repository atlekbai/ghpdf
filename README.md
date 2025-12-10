# MD2PDF

Markdown to PDF converter with GitHub-style rendering.

## Features

- Convert Markdown to PDF with GitHub-flavored styling
- Syntax highlighting for code blocks
- Support for tables, task lists, footnotes, and more
- Page break support for multi-page documents
- Optional page numbers
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

Convert markdown to PDF. Send raw markdown text in the request body.

**Query Parameters:**
- `filename` (optional): Output filename (default: `document.pdf`)
- `page_numbers` (optional): Add page numbers at bottom center (default: `false`)

**Response:** PDF file download

#### `GET /health`

Health check endpoint.

#### `GET /`

API information.

### Example with curl

```bash
# Simple conversion
curl -X POST http://localhost:8000/convert \
  --data-binary "# Hello World" \
  --output document.pdf

# With custom filename
curl -X POST "http://localhost:8000/convert?filename=my-doc.pdf" \
  --data-binary @README.md \
  --output my-doc.pdf

# From stdin
echo "# Hello" | curl -X POST http://localhost:8000/convert \
  --data-binary @- \
  --output document.pdf

# With page numbers
curl -X POST "http://localhost:8000/convert?page_numbers=true" \
  --data-binary @README.md \
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
    data=markdown_content,
    params={"filename": "my-document.pdf"}
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
- Page breaks

### Page Breaks

Insert page breaks using any of these formats:

```markdown
---pagebreak---
```

```markdown
<!-- pagebreak -->
```

```markdown
\pagebreak
```

## Development

### Run tests

```bash
uv run pytest
```

## License

MIT
