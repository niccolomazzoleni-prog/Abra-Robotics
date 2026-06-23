#!/usr/bin/env python3
"""Raccoglie metriche GitHub e le salva in data/site-stats.json (per admin/statistiche)."""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

OWNER = "niccolomazzoleni-prog"
REPO = "Abra-Robotics"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "site-stats.json"


def gh_get(path: str, token: str) -> dict | list | None:
    url = f"https://api.github.com/repos/{OWNER}/{REPO}{path}"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "abra-collect-site-stats",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print(f"skip {path}: {e.code} (permessi o rate limit)", file=sys.stderr)
        else:
            print(f"skip {path}: {e.code}", file=sys.stderr)
        return None


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not token:
        print("GITHUB_TOKEN mancante", file=sys.stderr)
        return 1

    repo = gh_get("", token) or {}
    views = gh_get("/traffic/views", token) or {}
    clones = gh_get("/traffic/clones", token) or {}
    referrers = gh_get("/traffic/popular/referrers", token) or []
    paths = gh_get("/traffic/popular/paths", token) or []
    runs_payload = gh_get("/actions/runs?per_page=8", token) or {}
    runs = runs_payload.get("workflow_runs") or []

    existing = {}
    if OUT.exists():
        try:
            existing = json.loads(OUT.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass

    payload = {
        "updated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "site": existing.get("site") or {
            "ga_property": "G-T4ZC7CM8RX",
            "meta_pixel": "1478056171004711",
            "contacts_sheet_id": "1XpXE3odenRl9nlkR3Te_-RjNlOA-5PINxpI14uBdvnY",
        },
        "github": {
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("forks_count", 0),
            "open_issues": repo.get("open_issues_count", 0),
            "traffic": {
                "views": views.get("views") or [],
                "clones": clones.get("clones") or [],
            },
            "referrers": referrers if isinstance(referrers, list) else [],
            "paths": paths if isinstance(paths, list) else [],
        },
        "workflows": [
            {
                "name": r.get("name"),
                "status": r.get("status"),
                "conclusion": r.get("conclusion"),
                "updated_at": r.get("updated_at"),
                "html_url": r.get("html_url"),
            }
            for r in runs
        ],
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Scritto {OUT} — {payload['github']['stars']} stelle, {len(payload['github']['referrers'])} referrer")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
