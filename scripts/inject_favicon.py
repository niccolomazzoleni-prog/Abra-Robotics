#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inserisce o aggiorna i tag favicon nelle pagine HTML pubbliche."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from site_head import render_favicon_links  # noqa: E402

SKIP_DIRS = {"admin", "node_modules", "__pycache__", ".git", ".cursor"}
FAVICON_BLOCK_RE = re.compile(
    r'(?:<link[^>]+(?:favicon|apple-touch-icon)[^>]*>\s*)+',
    re.I,
)


def prefix_for(path: Path) -> str:
    depth = len(path.relative_to(ROOT).parts) - 1
    return "../" * depth if depth else ""


def inject_into_html(text: str, prefix: str) -> str:
    favicon = render_favicon_links(prefix)
    if FAVICON_BLOCK_RE.search(text):
        text = FAVICON_BLOCK_RE.sub(favicon + "\n", text, count=1)
        return text
    for anchor in ('rel="stylesheet"', "rel='stylesheet'", '<link href="style.css"', '<link rel="stylesheet"'):
        idx = text.find(anchor)
        if idx >= 0:
            line_start = text.rfind("\n", 0, idx) + 1
            return text[:line_start] + favicon + "\n" + text[line_start:]
    head_end = text.lower().find("</head>")
    if head_end >= 0:
        return text[:head_end] + favicon + "\n" + text[head_end:]
    return text


def main() -> None:
    updated = 0
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if rel.name.startswith("_"):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        new_text = inject_into_html(text, prefix_for(path))
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            print(f"updated {rel}")
            updated += 1
    print(f"Done - {updated} file(s) updated")


if __name__ == "__main__":
    main()
