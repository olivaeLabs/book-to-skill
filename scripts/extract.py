#!/usr/bin/env python3
"""
Extract text from a document file for book-to-skill processing.
Backward-compatible entrypoint wrapper.
"""

import os
import sys

# Force UTF-8 stdout/stderr so extracted text, the attribution line's separators
# and the dependency-check glyphs (✓ / ✗) don't raise UnicodeEncodeError on Windows
# consoles that default to a legacy code page (e.g. GBK / cp936).
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

# Ensure the project root directory (where the 'book_to_skill' package lives) is in sys.path
# so the modular package can be imported reliably regardless of the working directory.
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, str(repo_root))

# Auto re-exec into local .venv if present and not already active
venv_python = os.path.join(repo_root, ".venv", "bin", "python3")
if os.path.isfile(venv_python) and os.path.abspath(sys.executable) != os.path.abspath(venv_python) and not os.environ.get("VIRTUAL_ENV"):
    os.execv(venv_python, [venv_python] + sys.argv)

from book_to_skill.cli import main

if __name__ == "__main__":
    main()
