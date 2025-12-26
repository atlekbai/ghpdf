# MD2PDF

Markdown to PDF converter with GitHub-style rendering.

## Features

- Convert Markdown to PDF with GitHub-flavored styling
- Syntax highlighting for code blocks
- Support for tables, task lists, footnotes, and more
- Page break support for multi-page documents
- Optional page numbers
- Bulk conversion support
- Stdin/stdout piping

## Installation

```bash
uv sync
```

## Usage

```bash
md2pdf [OPTIONS] [FILES]...
```

### Options

| Flag | Long             | Description                                 |
| ---- | ---------------- | ------------------------------------------- |
| `-o` | `--output`       | Output filename (single file or stdin only) |
| `-O` | `--remote-name`  | Auto-name output (input.md → input.pdf)     |
| `-n` | `--page-numbers` | Add page numbers at bottom center           |
| `-q` | `--quiet`        | Suppress progress output                    |
| `-V` | `--version`      | Show version and exit                       |

### Examples

```bash
# Single file with explicit output
md2pdf README.md -o documentation.pdf

# Auto-name output (README.md → README.pdf)
md2pdf README.md -O

# Bulk convert all markdown files
md2pdf *.md -O

# With page numbers
md2pdf report.md -O -n

# Stdin to file
echo "# Hello World" | md2pdf -o hello.pdf

# Stdin to stdout (for piping)
cat document.md | md2pdf > output.pdf

# Quiet mode for scripting
md2pdf *.md -O -q
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
