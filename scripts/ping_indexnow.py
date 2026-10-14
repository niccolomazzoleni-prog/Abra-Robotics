#!/usr/bin/env python3
"""Notify IndexNow (Bing, Yandex, Seznam, ...) about updated URLs.

Without arguments sends every URL in sitemap.xml (IndexNow accepts up to 10,000 per call);
with arguments sends only those URLs. Bing also feeds ChatGPT and Copilot web search.
Usage: python scripts/ping_indexnow.py [URL ...]"""
from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEY_FILE = "abrarobotics2026indexnowkey.txt"
KEY = (ROOT / KEY_FILE).read_text(encoding="utf-8").strip()
HOST = "abrarobotics.com"


def sitemap_urls() -> list[str]:
    xml = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    return re.findall(r"<loc>(https://abrarobotics\.com/[^<]*)</loc>", xml)


def main(urls: list[str]) -> None:
    urls = urls or sitemap_urls()
    payload = {"host": HOST, "key": KEY, "keyLocation": f"https://{HOST}/{KEY_FILE}", "urlList": urls[:10000]}
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            # 200 = ricevuto, 202 = ricevuto, chiave in verifica
            print(f"IndexNow: {resp.status} per {len(payload['urlList'])} URL")
    except urllib.error.HTTPError as e:
        print(f"IndexNow: errore {e.code} {e.read()[:200]!r}")
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
