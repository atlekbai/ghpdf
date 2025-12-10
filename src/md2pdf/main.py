"""FastAPI server for Markdown to PDF conversion."""

import io
import re
from pathlib import Path

import markdown
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from weasyprint import HTML

app = FastAPI(
    title="MD2PDF",
    description="Markdown to PDF converter with GitHub-style rendering",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = Path(__file__).parent / "static"
GITHUB_CSS_PATH = STATIC_DIR / "github.css"


def get_github_css() -> str:
    """Load GitHub-style CSS."""
    return GITHUB_CSS_PATH.read_text()


# Page break marker pattern - matches various formats
PAGE_BREAK_PATTERN = re.compile(
    r"^(?:---\s*pagebreak\s*---|<!--\s*pagebreak\s*-->|\\pagebreak)\s*$",
    re.MULTILINE | re.IGNORECASE,
)
PAGE_BREAK_HTML = '<div class="pagebreak"></div>'


def preprocess_pagebreaks(md_content: str) -> str:
    """Convert page break markers to HTML."""
    return PAGE_BREAK_PATTERN.sub(PAGE_BREAK_HTML, md_content)


def markdown_to_html(md_content: str) -> str:
    """Convert markdown to HTML with extensions."""
    # Preprocess page breaks before markdown conversion
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
    html_body = md.convert(md_content)

    return html_body


def create_html_document(body: str, css: str) -> str:
    """Create a complete HTML document with styling."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
{css}
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


@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "name": "MD2PDF",
        "description": "Markdown to PDF converter with GitHub-style rendering",
        "version": "1.0.0",
        "endpoints": {
            "POST /convert": "Convert markdown to PDF (raw text body, optional ?filename=)",
            "GET /health": "Health check",
        },
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/convert")
async def convert_markdown_to_pdf(request: Request, filename: str = "document.pdf"):
    """Convert markdown text to a PDF document.

    Accepts raw markdown text in the request body.
    Optional query parameter: filename (default: document.pdf)

    Returns:
        PDF file as response
    """
    body = await request.body()
    md_content = body.decode("utf-8")

    if not md_content.strip():
        raise HTTPException(status_code=400, detail="Markdown content cannot be empty")

    try:
        css = get_github_css()
        html_body = markdown_to_html(md_content)
        html_document = create_html_document(html_body, css)
        pdf_bytes = html_to_pdf(html_document)

        if not filename.endswith(".pdf"):
            filename += ".pdf"

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")


def main():
    """Run the server."""
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
