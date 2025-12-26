# ghpdf

A CLI tool to convert Markdown files to PDF with GitHub-style rendering.

<img src="https://github.com/user-attachments/assets/94126b34-0ef5-4f1c-8e69-de8e4d22f3ce" alt="Sample PDF output" width="400">

## Installation

```bash
pip install ghpdf
```

Or with [pipx](https://pipx.pypa.io/) (recommended for CLI tools):

```bash
pipx install ghpdf
```

## Quick Start

```bash
# Convert a file
ghpdf README.md -o output.pdf

# Auto-name output (README.md → README.pdf)
ghpdf README.md -O
```

## Usage

```bash
ghpdf [OPTIONS] [FILES]...
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
ghpdf README.md -o documentation.pdf

# Auto-name output (README.md → README.pdf)
ghpdf README.md -O

# Bulk convert all markdown files
ghpdf *.md -O

# With page numbers
ghpdf report.md -O -n

# Stdin to file
echo "# Hello World" | ghpdf -o hello.pdf

# Stdin to stdout (for piping)
cat document.md | ghpdf > output.pdf

# Quiet mode for scripting
ghpdf *.md -O -q
```

## Features

- GitHub-flavored markdown styling
- Syntax highlighting for code blocks
- Tables, task lists, footnotes, and more
- Page break support
- Optional page numbers
- Bulk conversion
- Stdin/stdout piping

### Supported Markdown

Headings, bold, italic, strikethrough, lists, task lists, code blocks, inline code, tables, blockquotes, horizontal rules, links, images, footnotes, definition lists, abbreviations, and admonitions.

### Page Breaks

Insert page breaks using any of these formats:

```
---pagebreak---
<!-- pagebreak -->
\pagebreak
```

## License

MIT
