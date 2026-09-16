import os
from pathlib import Path

def default_output_dir() -> Path:
    """Per-run work directory, unique to this process.

    The PID is part of the name so two extractions running at the same time
    cannot overwrite each other.

    Defaults to a local workspace '.work' directory to comply with 'No /tmp'
    guidelines and isolate artifacts from shared system temp directories.
    Can be configured via BOOK_SKILL_WORKDIR_BASE or overridden completely
    by BOOK_SKILL_WORKDIR.
    """
    base_dir = Path(os.environ.get("BOOK_SKILL_WORKDIR_BASE") or (Path.cwd() / ".work"))
    return base_dir / f"book_skill_work-{os.getpid()}"


# `or` rather than a get() default: BOOK_SKILL_WORKDIR set to an empty string
# would otherwise become Path(""), i.e. the current directory — which the run
# would then populate and chmod to 0700.
OUTPUT_DIR = Path(os.environ.get("BOOK_SKILL_WORKDIR") or default_output_dir())
OUTPUT_TEXT = OUTPUT_DIR / "full_text.txt"
OUTPUT_META = OUTPUT_DIR / "metadata.json"

WORDS_PER_TOKEN = 0.75  # approximate (Latin / whitespace-delimited text)
# CJK scripts carry little or no whitespace, so word-splitting under-counts them
# by orders of magnitude. Count CJK codepoints directly against this
# chars-per-token ratio instead (see estimate_tokens in utils.py).
CJK_CHARS_PER_TOKEN = 1.5  # approximate for cl100k-style tokenizers

TEXT_EXTENSIONS = {".txt", ".text", ".md", ".markdown", ".rst", ".adoc", ".asciidoc"}
HTML_EXTENSIONS = {".html", ".htm", ".xhtml"}
CALIBRE_EBOOK_EXTENSIONS = {".mobi", ".azw", ".azw3"}
SUPPORTED_EXTENSIONS = {
    ".pdf", ".epub", ".docx", ".rtf",
    *TEXT_EXTENSIONS,
    *HTML_EXTENSIONS,
    *CALIBRE_EBOOK_EXTENSIONS,
}

PYTHON_DEPENDENCIES = {
    "pdf_inspector": "pdf-inspector>=1.15,<2",
    "docling": "docling",
    "pypdf": "pypdf",
    "pdfminer": "pdfminer.six",
    "ebooklib": "ebooklib",
    "bs4": "beautifulsoup4",
    "docx": "python-docx",
    "striprtf": "striprtf",
    "trafilatura": "trafilatura",
}


def supported_formats_message() -> str:
    return ", ".join(sorted(SUPPORTED_EXTENSIONS))
