#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifica che tutte le pagine pubbliche abbiano la navbar canonica."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from site_nav import render_site_nav  # noqa: E402

SKIP_DIRS = {"admin", "node_modules", "__pycache__", ".git", ".cursor"}
SKIP_FILES = {
    "checklist.html",
    "restyle-preview.html",
    "catalogo.html",
    "index-zenixa.html",
    "index.backup.html",
    "lp-umanoidi-v1.html",
    "_template.html",
    "_template-compact.html",
}


def extract_nav_hrefs(html: str) -> tuple[str, ...]:
    """Estrae href da navbar + mobile menu (ordine preservato)."""
    start = html.find('<nav class="navbar">')
    if start < 0:
        return ()
    end_marker = html.find('<div class="mobile-menu">', start)
    if end_marker < 0:
        block = html[start : html.find("</nav>", start) + len("</nav>")]
    else:
        depth = 0
        pos = end_marker
        while pos < len(html):
            if html.startswith("<div", pos):
                depth += 1
            elif html.startswith("</div>", pos):
                depth -= 1
                if depth == 0:
                    pos += len("</div>")
                    block = html[start:pos]
                    break
            pos += 1
        else:
            return ()

    hrefs = re.findall(r'href="([^"]+)"', block)
    return tuple(h.replace("../", "") for h in hrefs if "images/" not in h)


def canonical_hrefs() -> tuple[str, ...]:
    return extract_nav_hrefs(render_site_nav(""))


def main() -> int:
    canon = canonical_hrefs()
    failures: list[str] = []

    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if rel.name in SKIP_FILES or rel.name.startswith("_"):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if '<nav class="navbar">' not in text:
            continue

        got = extract_nav_hrefs(text)
        if got != canon:
            failures.append(str(rel))

    if failures:
        print(f"FAIL — {len(failures)} pagina(e) con navbar non allineata:")
        for f in failures[:30]:
            print(f"  {f}")
        if len(failures) > 30:
            print(f"  ... e altre {len(failures) - 30}")
        return 1

    print(f"OK — navbar canonica su tutte le pagine pubbliche ({len(canon)} link)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
