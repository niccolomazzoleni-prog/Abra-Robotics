#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aggiunge JSON-LD Article alle pagine blog se assente."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOG_DIR = ROOT / "blog"
SITE = "https://abrarobotics.com"
ARTICLE_RE = re.compile(r'<script[^>]+type="application/ld\+json"[^>]*>.*?"@type"\s*:\s*"Article"', re.DOTALL | re.I)


def extract_meta(html: str, name: str) -> str:
    m = re.search(rf'<meta[^>]+name="{name}"[^>]+content="([^"]*)"', html, re.I)
    if m:
        return m.group(1)
    m = re.search(rf'<meta[^>]+content="([^"]*)"[^>]+name="{name}"', html, re.I)
    return m.group(1) if m else ""


def extract_title(html: str) -> str:
    m = re.search(r"<title>([^<]+)</title>", html, re.I)
    return m.group(1).strip() if m else ""


def extract_date(html: str) -> str:
    m = re.search(r'<time[^>]+datetime="([^"]+)"', html, re.I)
    return m.group(1) if m else "2026-07-15"


def build_schema(html: str, slug: str) -> str:
    title = extract_title(html).split("|")[0].strip()
    description = extract_meta(html, "description") or title
    published = extract_date(html)
    url = f"{SITE}/blog/{slug}"
    image_m = re.search(r'<meta[^>]+property="og:image"[^>]+content="([^"]+)"', html, re.I)
    image = image_m.group(1) if image_m else f"{SITE}/images/logo.png"
    data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "datePublished": published,
        "dateModified": published,
        "author": {
            "@type": "Organization",
            "name": "Abra Robotics",
            "url": SITE,
        },
        "publisher": {
            "@type": "Organization",
            "name": "Abra Robotics",
            "logo": {
                "@type": "ImageObject",
                "url": f"{SITE}/images/logo.png",
            },
        },
        "mainEntityOfPage": url,
        "image": image,
        "inLanguage": "it",
    }
    return (
        '  <script type="application/ld+json">\n'
        + json.dumps(data, ensure_ascii=False, indent=2)
        + "\n  </script>"
    )


def main() -> None:
    updated = 0
    for path in sorted(BLOG_DIR.glob("*.html")):
        html = path.read_text(encoding="utf-8")
        if ARTICLE_RE.search(html):
            continue
        schema = build_schema(html, path.name)
        if "</head>" not in html:
            continue
        new_html = html.replace("</head>", schema + "\n</head>", 1)
        path.write_text(new_html, encoding="utf-8")
        print(f"updated {path.name}")
        updated += 1
    print(f"Done - {updated} file(s) updated")


if __name__ == "__main__":
    main()
