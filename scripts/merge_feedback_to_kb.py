#!/usr/bin/env python3
"""Merge feedback locale in knowledge markdown + export dataset fine-tuning."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEEDBACK_DIR = ROOT / "offerte-ai" / "data" / "feedback"
KB_DIR = ROOT / "offerte-ai" / "data" / "knowledge"
BUILD = ROOT / "scripts" / "build_knowledge_index.py"


def load_feedback_json(path: Path) -> list[dict]:
    if path.suffix == ".jsonl":
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else data.get("entries", [])


def merge_kb(entries: list[dict]) -> Path:
    KB_DIR.mkdir(parents=True, exist_ok=True)
    out = KB_DIR / f"feedback-{datetime.now(timezone.utc).strftime('%Y%m%d')}.md"
    lines = ["# Knowledge da feedback utente\n"]
    for e in entries:
        q = e.get("question", "").strip()
        body = (e.get("correction") or e.get("answer") or "").strip()
        if not q or not body:
            continue
        lines.append(f"## {q[:120]}\n\n{body}\n")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def export_finetune(entries: list[dict], out: Path) -> int:
    n = 0
    with out.open("w", encoding="utf-8") as f:
        for e in entries:
            if not (e.get("correction") or e.get("rating") == 1):
                continue
            row = {
                "messages": [
                    {"role": "user", "content": e["question"]},
                    {"role": "assistant", "content": e.get("correction") or e["answer"]},
                ],
                "meta": {"id": e.get("id"), "rating": e.get("rating")},
            }
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            n += 1
    return n


def main() -> None:
    FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)
    sources = list(FEEDBACK_DIR.glob("*.json")) + list(FEEDBACK_DIR.glob("*.jsonl"))
    if not sources and len(sys.argv) < 2:
        print("Nessun file in offerte-ai/data/feedback/")
        print("Esporta dal admin o incolla feedback-export.jsonl")
        return

    entries: list[dict] = []
    for p in sources:
        entries.extend(load_feedback_json(p))

    if len(sys.argv) >= 2:
        entries.extend(load_feedback_json(Path(sys.argv[1])))

    kb_path = merge_kb(entries)
    ft_path = FEEDBACK_DIR / "finetune-dataset.jsonl"
    n = export_finetune(entries, ft_path)
    print(f"KB: {kb_path}")
    print(f"Fine-tune: {n} esempi -> {ft_path}")

    if BUILD.exists():
        import subprocess
        subprocess.run([sys.executable, str(BUILD)], check=False)


if __name__ == "__main__":
    main()
