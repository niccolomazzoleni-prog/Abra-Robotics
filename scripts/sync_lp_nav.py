#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sostituisce la navbar landing minimale con la navbar sito canonica."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from site_nav import render_site_nav  # noqa: E402

LP_FILES = [
    "lp-cobot.html",
    "lp-cobot-lc.html",
    "en/lp-cobot-en.html",
    "en/lp-cobot-lc-en.html",
]

LP_NAV_RE = re.compile(
    r"  <!-- LP_NAV_START -->.*?  <!-- LP_NAV_END -->\n?",
    re.DOTALL,
)


def prefix_for(rel: str) -> str:
    return "../" if rel.startswith("en/") else ""


def main() -> None:
    updated = 0
    for name in LP_FILES:
        path = ROOT / name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        nav = render_site_nav(prefix_for(name))
        new_text, count = LP_NAV_RE.subn(nav + "\n\n", text, count=1)
        if count and new_text != text:
            path.write_text(new_text, encoding="utf-8")
            print(f"updated {name}")
            updated += 1
    print(f"Done - {updated} file(s) updated")


if __name__ == "__main__":
    main()
