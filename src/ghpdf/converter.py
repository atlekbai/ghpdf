"""Core conversion functions for ghpdf."""

import io
import re
from pathlib import Path

import markdown
from weasyprint import HTML

STATIC_DIR = Path(__file__).parent / "static"
GITHUB_CSS_PATH = STATIC_DIR / "github.css"

# Page break marker pattern - matches various formats
PAGE_BREAK_PATTERN = re.compile(
    r"^(?:---\s*pagebreak\s*---|<!--\s*pagebreak\s*-->|\\pagebreak)\s*$",
    re.MULTILINE | re.IGNORECASE,
)
PAGE_BREAK_HTML = '<div class="pagebreak"></div>'

# CSS for page numbers
PAGE_NUMBERS_CSS = """
@page {
    @bottom-center {
        content: counter(page);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
        font-size: 11px;
        color: #656d76;
    }
}
"""


def get_github_css() -> str:
    """Load GitHub-style CSS."""
    return GITHUB_CSS_PATH.read_text()


def preprocess_pagebreaks(md_content: str) -> str:
    """Convert page break markers to HTML."""
    return PAGE_BREAK_PATTERN.sub(PAGE_BREAK_HTML, md_content)


def markdown_to_html(md_content: str) -> str:
    """Convert markdown to HTML with extensions."""
    md_content = preprocess_pagebreaks(md_content)

    extensions = [
        "markdown.extensions.fenced_code",
        "markdown.extensions.codehilite",
        "markdown.extensions.tables",
        "markdown.extensions.toc",
        "markdown.extensions.nl2br",
        "markdown.extensions.sane_lists",
        "markdown.extensions.smarty",
        "markdown.extensions.admonition",
        "markdown.extensions.def_list",
        "markdown.extensions.abbr",
        "markdown.extensions.footnotes",
        "markdown.extensions.md_in_html",
    ]

    extension_configs = {
        "markdown.extensions.codehilite": {
            "css_class": "highlight",
            "guess_lang": True,
            "linenums": False,
        },
        "markdown.extensions.toc": {
            "permalink": False,
        },
    }

    md = markdown.Markdown(extensions=extensions, extension_configs=extension_configs)
    return md.convert(md_content)


def create_html_document(body: str, css: str, page_numbers: bool = False) -> str:
    """Create a complete HTML document with styling."""
    extra_css = PAGE_NUMBERS_CSS if page_numbers else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
{css}
{extra_css}
    </style>
</head>
<body>
{body}
</body>
</html>"""


def html_to_pdf(html_content: str) -> bytes:
    """Convert HTML to PDF using WeasyPrint."""
    html = HTML(string=html_content)
    pdf_buffer = io.BytesIO()
    html.write_pdf(pdf_buffer)
    return pdf_buffer.getvalue()


def convert(content: str, page_numbers: bool = False) -> bytes:
    """Convert markdown content to PDF bytes.

    Args:
        content: Markdown text to convert
        page_numbers: Add page numbers at bottom center

    Returns:
        PDF file as bytes
    """
    css = get_github_css()
    html_body = markdown_to_html(content)
    html_document = create_html_document(html_body, css, page_numbers=page_numbers)
    return html_to_pdf(html_document)
