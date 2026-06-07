#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sostituisce navbar + mobile-menu nelle pagine HTML statiche root."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from site_nav import render_site_nav  # noqa: E402

STATIC_PAGES = [
    "index.html",
    "manifattura-logistica.html",
    "universita-ricerca.html",
    "assessment.html",
    "finanziamenti.html",
    "chi-siamo.html",
    "privacy-policy.html",
    "cookie-policy.html",
    "note-legali.html",
    "condizioni-di-vendita.html",
    "lp-amr.html",
    "lp-quadrupedi.html",
    "lp-umanoidi.html",
    "r1-d.html",
    "grazie.html",
]

HAND_BUILT_PRODUCTS = [
    "prodotti/unitree-g1.html",
    "prodotti/unitree-go2-edu-plus.html",
    "prodotti/unitree-h2.html",
    "prodotti/unitree-r1-edu.html",
]


SECTION_MARKERS = (
    "\n  <!-- Hero -->",
    "\n  <!-- HERO",
    "\n  <header class=\"hero\"",
    "\n  <header class=\"page-hero\"",
    "\n  <header class=\"lpv-hero\"",
    "\n  <header class=\"collection-hero\"",
    "\n  <section class=\"collection-hero\"",
    "\n  <section class=\"product-hero\"",
    "\n  <section class=\"lp-hero\"",
    "\n  <main class=\"ty\"",
    "\n  <main ",
    "\n  <div class=\"legal-content\"",
    "\n  <section id=\"form\"",
    "\n  <section class=\"thank-you\"",
)


def replace_nav_block(text: str, nav_html: str) -> str | None:
    """Sostituisce navbar + mobile-menu fino alla sezione contenuto successiva."""
    start = text.find("  <!-- Navbar -->")
    if start < 0:
        start = text.find('  <nav class="navbar">')
    if start < 0:
        return None

    end = -1
    for marker in SECTION_MARKERS:
        pos = text.find(marker, start + 10)
        if pos >= 0 and (end < 0 or pos < end):
            end = pos
    if end < 0:
        return None

    return text[:start] + nav_html.rstrip() + "\n\n" + text[end + 1 :]


def sync_file(path: Path, prefix: str = "") -> bool:
    nav = render_site_nav(prefix)
    text = path.read_text(encoding="utf-8")
    new_text = replace_nav_block(text, nav)
    if new_text is None or new_text == text:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    updated = 0
    for name in STATIC_PAGES:
        p = ROOT / name
        if p.is_file() and sync_file(p, ""):
            print(f"updated {name}")
            updated += 1
    for name in HAND_BUILT_PRODUCTS:
        p = ROOT / name
        if p.is_file() and sync_file(p, "../"):
            print(f"updated {name}")
            updated += 1
    print(f"Done — {updated} file(s) updated")


if __name__ == "__main__":
    main()
