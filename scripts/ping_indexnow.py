#!/usr/bin/env python3
"""Notify IndexNow (Bing et al.) about key updated URLs."""
from __future__ import annotations

import json
import ssl
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEY = (ROOT / "abrarobotics2026indexnowkey.txt").read_text(encoding="utf-8").strip()
HOST = "abrarobotics.com"
URLS = [
    f"https://{HOST}/",
    f"https://{HOST}/as2.html",
    f"https://{HOST}/h2.html",
    f"https://{HOST}/umanoidi.html",
    f"https://{HOST}/quadrupedi.html",
    f"https://{HOST}/llms.txt",
    f"https://{HOST}/sitemap.xml",
    f"https://{HOST}/blog/unitree-as2-italia.html",
    f"https://{HOST}/blog/unitree-h2-italia.html",
    f"https://{HOST}/prodotti/unitree-as2-pro.html",
    f"https://{HOST}/prodotti/unitree-as2-w.html",
    f"https://{HOST}/prodotti/unitree-h2.html",
    f"https://{HOST}/prodotti/unitree-h2-d.html",
    f"https://{HOST}/prodotti/unitree-h2-plus.html",
]


def main() -> None:
    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": f"https://{HOST}/{KEY}.txt"
        if not KEY.endswith(".txt")
        else f"https://{HOST}/abrarobotics2026indexnowkey.txt",
        "urlList": URLS,
    }
    # key file on site is abrarobotics2026indexnowkey.txt
    payload["keyLocation"] = f"https://{HOST}/abrarobotics2026indexnowkey.txt"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    ctx = ssl._create_unverified_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
            print("IndexNow status", resp.status, resp.read()[:200])
    except Exception as e:
        print("IndexNow error", e)


if __name__ == "__main__":
    main()
