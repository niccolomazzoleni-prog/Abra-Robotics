#!/usr/bin/env python3
"""Merge feedback / quiz esperto in knowledge markdown strutturata + rebuild indice RAG."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEEDBACK_DIR = ROOT / "offerte-ai" / "data" / "feedback"
KB_DIR = ROOT / "offerte-ai" / "data" / "knowledge"
QUIZ_KB = KB_DIR / "faq-quiz-esperto.md"
BUILD = ROOT / "scripts" / "build_knowledge_index.py"

FAMILY_MAP = {
    "quad-sorveglianza": "Quadrupede · sorveglianza",
    "uni-locomozione": "Umanoide · università / ROS2",
    "uni-bimanuale": "Dual-arm · manipolazione",
    "manif-pickplace": "Industrial · pick & place",
    "h2-fullsize": "H2 full-size",
    "g1-r1-lab": "G1 / R1 · lab mono-arm",
    "integrazione-poc": "PoC integrazione software",
    "trap-quad-bimanual": "Training · correggere richiesta errata",
}


def load_feedback_json(path: Path) -> list[dict]:
    if path.suffix == ".jsonl":
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else data.get("entries", [])


def norm_key(text: str) -> str:
    t = re.sub(r"\s+", " ", text.lower().strip())
    return hashlib.sha256(t.encode("utf-8")).hexdigest()[:16]


def family_label(entry: dict) -> str:
    meta = entry.get("scenario_meta") or {}
    sid = meta.get("scenarioId") or meta.get("family") or ""
    for prefix, label in FAMILY_MAP.items():
        if sid.startswith(prefix) or prefix in str(sid):
            return label
    if entry.get("action") == "expert_quiz":
        return meta.get("family") or "Quiz esperto"
    return meta.get("family") or "Feedback commerciale"


def format_quiz_section(entry: dict) -> str | None:
    q = (entry.get("question") or "").strip()
    body = (entry.get("correction") or entry.get("answer") or "").strip()
    if not q or not body or body.startswith("(quiz esperto"):
        return None

    fam = family_label(entry)
    industry = entry.get("industry") or (entry.get("scenario_meta") or {}).get("industry") or ""
    title = q[:100].replace("\n", " ")
    if len(q) > 100:
        title += "…"

    lines = [f"## [{fam}] {title}", ""]
    if industry:
        lines.append(f"**Contesto settore:** {industry}")
    lines.append(f"**Domanda cliente:** {q}")
    lines.append("")
    lines.append("**Risposta consulente Abra:**")
    lines.append("")
    lines.append(body)
    lines.append("")
    return "\n".join(lines)


def format_generic_section(entry: dict) -> str | None:
    q = (entry.get("question") or "").strip()
    body = (entry.get("correction") or entry.get("answer") or "").strip()
    if not q or not body:
        return None
    title = q[:120].replace("\n", " ")
    return f"## {title}\n\n{body}\n"


def existing_keys(path: Path) -> set[str]:
    if not path.exists():
        return set()
    text = path.read_text(encoding="utf-8")
    return {norm_key(m.group(1)) for m in re.finditer(r"\*\*Domanda cliente:\*\*\s*(.+?)(?:\n|$)", text, re.I)}


def merge_quiz(entries: list[dict]) -> tuple[Path, int]:
    KB_DIR.mkdir(parents=True, exist_ok=True)
    seen = existing_keys(QUIZ_KB)
    sections: list[str] = []

    for e in entries:
        if e.get("action") not in ("expert_quiz",) and e.get("model_mode") != "expert-quiz":
            continue
        q = (e.get("question") or "").strip()
        if not q:
            continue
        key = norm_key(q)
        if key in seen:
            continue
        block = format_quiz_section(e)
        if not block:
            continue
        seen.add(key)
        sections.append(block)

    if not sections:
        return QUIZ_KB, 0

    header = (
        "# FAQ da quiz esperto Abra\n\n"
        "Risposte curate dal team commerciale (Lab Training). "
        "Aggiornato automaticamente da `merge_feedback_to_kb.py`.\n\n"
    )
    if QUIZ_KB.exists():
        QUIZ_KB.write_text(QUIZ_KB.read_text(encoding="utf-8").rstrip() + "\n\n" + "\n".join(sections) + "\n", encoding="utf-8")
    else:
        QUIZ_KB.write_text(header + "\n".join(sections) + "\n", encoding="utf-8")
    return QUIZ_KB, len(sections)


def merge_generic(entries: list[dict]) -> Path | None:
    generic = [e for e in entries if e.get("action") not in ("expert_quiz",) and e.get("model_mode") != "expert-quiz"]
    if not generic:
        return None
    out = KB_DIR / f"feedback-{datetime.now(timezone.utc).strftime('%Y%m%d')}.md"
    lines = ["# Knowledge da feedback utente\n"]
    for e in generic:
        block = format_generic_section(e)
        if block:
            lines.append(block)
    if len(lines) <= 1:
        return None
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def export_finetune(entries: list[dict], out: Path) -> int:
    n = 0
    with out.open("w", encoding="utf-8") as f:
        for e in entries:
            body = (e.get("correction") or e.get("answer") or "").strip()
            if not body or body.startswith("(quiz esperto"):
                continue
            if not (e.get("correction") or e.get("rating") == 1):
                continue
            row = {
                "messages": [
                    {"role": "user", "content": e["question"]},
                    {"role": "assistant", "content": body},
                ],
                "meta": {
                    "id": e.get("id"),
                    "rating": e.get("rating"),
                    "action": e.get("action"),
                    "family": family_label(e),
                },
            }
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            n += 1
    return n


def main() -> None:
    FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)
    sources = list(FEEDBACK_DIR.glob("*.json")) + list(FEEDBACK_DIR.glob("*.jsonl"))
    if not sources and len(sys.argv) < 2:
        print("Nessun file in offerte-ai/data/feedback/")
        print("Esporta dal Lab → Scarica pacchetto training → merge_feedback_to_kb.py feedback-export.jsonl")
        return

    entries: list[dict] = []
    for p in sources:
        entries.extend(load_feedback_json(p))

    if len(sys.argv) >= 2:
        entries.extend(load_feedback_json(Path(sys.argv[1])))

    quiz_path, quiz_n = merge_quiz(entries)
    generic_path = merge_generic(entries)
    ft_path = FEEDBACK_DIR / "finetune-dataset.jsonl"
    n = export_finetune(entries, ft_path)

    if quiz_n:
        print(f"Quiz KB: +{quiz_n} sezioni -> {quiz_path}")
    else:
        print(f"Quiz KB: nessuna nuova sezione ({quiz_path.name})")
    if generic_path:
        print(f"Feedback generico: {generic_path}")
    print(f"Fine-tune: {n} esempi -> {ft_path}")

    if BUILD.exists():
        import subprocess
        subprocess.run([sys.executable, str(BUILD)], check=False)


if __name__ == "__main__":
    main()
