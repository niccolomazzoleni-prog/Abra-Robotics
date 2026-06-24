#!/usr/bin/env python3
"""Genera l'indice RAG leggero per offerte-ai da tutte le fonti del sito."""

from __future__ import annotations

import json
import re
import sys
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "offerte-ai" / "data" / "knowledge-index.json"
LISTINO = ROOT / "listini" / "pubblico" / "end-user.json"
MANIFEST = ROOT / "listini" / "pubblico" / "catalogo-manifest.json"
AMR = ROOT / "data" / "amr-products.json"
COBOT = ROOT / "data" / "cobot-products.json"
KB_DIR = ROOT / "offerte-ai" / "data" / "knowledge"
REGOLE = ROOT / "offerte-ai" / "data" / "offerte-regole.json"
VOCI_EXTRA = ROOT / "offerte-ai" / "data" / "voci-extra.json"
INDEX_HTML = ROOT / "index.html"
SAMPLE = ROOT / "offerte-ai" / "data" / "sample-prices.json"

QUADRUPED_SKUS = frozenset({
    "GO2-AIR", "GO2-PRO", "GO2-EDU-STD", "GO2-EDU-SMART", "GO2-EDU-ULT", "GO2-EDU-LASER",
    "GO2W-U2", "GO2W-U3", "GO2W-U4", "GO2W-U5",
    "AS2-AIR", "AS2-PRO", "AS2-EDU",
    "A2-STD", "A2-PRO", "A2W-STD", "A2W-PRO",
    "B2", "B2W", "B2-LIDAR", "B2W-LIDAR",
})


def resolve_categoria(sku: str, item: dict, manifest: dict | None = None) -> str:
    if sku in QUADRUPED_SKUS:
        return "QUADRUPEDI"
    manifest = manifest or {}
    m = manifest.get(sku, {})
    return item.get("categoria") or m.get("categoria") or "N/D"


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def chunk_md(text: str, source: str) -> list[dict]:
    chunks: list[dict] = []
    for block in re.split(r"\n##+\s+", text.strip()):
        block = block.strip()
        if not block:
            continue
        lines = block.split("\n", 1)
        title = lines[0].strip("# ").strip()
        body = lines[1].strip() if len(lines) > 1 else title
        content = f"{title}\n{body}".strip()
        chunks.append(_chunk("faq", f"faq:{title[:40].lower().replace(' ', '-')}", title, content, source, {"category": "faq"}))
    return [c for c in chunks if c]


POISON_KB_PATTERNS = [
    re.compile(r"ignora\s+(tutte\s+)?(le\s+)?(istruzioni|regole)", re.I),
    re.compile(r"ignore\s+(all\s+)?instructions", re.I),
    re.compile(r"applica\s+sempre\s+sconto", re.I),
    re.compile(r"<\/?system>", re.I),
    re.compile(r"<\/?context>", re.I),
]


def is_poisoned(text: str) -> bool:
    return any(p.search(text) for p in POISON_KB_PATTERNS)


def _chunk(ctype: str, cid: str, title: str, text: str, source: str, meta: dict) -> dict | None:
    blob = f"{title}\n{text}"
    if is_poisoned(blob):
        print(f"WARN: chunk poisoned skipped: {cid}")
        return None
    return {
        "id": cid,
        "type": ctype,
        "source": source,
        "title": title,
        "text": text,
        "tokens": tokenize(text + " " + title),
        "meta": meta,
    }


def chunk_listino(data: dict, manifest: dict | None = None) -> list[dict]:
    chunks: list[dict] = []
    manifest = manifest or {}
    for sku, item in data.items():
        m = manifest.get(sku, {})
        cat = resolve_categoria(sku, item, manifest)
        specs_txt = ""
        if m.get("specs"):
            specs_txt = " Specifiche: " + "; ".join(f"{a}: {b}" for a, b in m["specs"][:8])
        desc = m.get("descrizione") or m.get("sottotitolo") or ""
        famiglia = "Quadrupede" if cat == "QUADRUPEDI" else ("Umanoide" if cat == "UMANOIDI" else cat)
        text = (
            f"SKU {sku}: {item.get('nome', sku)}. "
            f"Famiglia {famiglia}. Categoria catalogo {cat}. "
            f"Prezzo End-User {item.get('prezzo_eur')} EUR. "
            f"{desc}{specs_txt} "
            f"{item.get('note', '')}"
        ).strip()
        chunks.append(_chunk(
            "product", f"sku:{sku}", item.get("nome", sku), text,
            "listini/pubblico/end-user.json",
            {
                "sku": sku,
                "prezzo_eur": item.get("prezzo_eur"),
                "categoria": cat,
                "famiglia": famiglia.lower(),
                "slug": item.get("slug") or m.get("slug"),
            },
        ))
    return chunks


def chunk_manifest_only(manifest: dict, listino_skus: set[str]) -> list[dict]:
    chunks: list[dict] = []
    for sku, m in manifest.items():
        if sku in listino_skus:
            continue
        specs_txt = "; ".join(f"{a}: {b}" for a, b in (m.get("specs") or [])[:6])
        text = f"{m.get('titolo', sku)}. {m.get('sottotitolo', '')} {m.get('descrizione', '')} {specs_txt}".strip()
        chunks.append(_chunk(
            "product", f"manifest:{sku}", m.get("titolo", sku), text,
            "listini/pubblico/catalogo-manifest.json",
            {"sku": sku, "categoria": m.get("categoria"), "slug": m.get("slug")},
        ))
    return chunks


def chunk_catalog_list(items: list, source: str, prefix: str) -> list[dict]:
    chunks: list[dict] = []
    for p in items:
        sku = p.get("sku") or p.get("id", "")
        text = (
            f"{p.get('title', sku)} ({p.get('brand', '')}). "
            f"{p.get('subtitle', '')} {p.get('blurb', p.get('description', ''))} "
            f"Prezzo {p.get('price_eur', 'N/D')} EUR. SKU {sku}."
        ).strip()
        chunks.append(_chunk(
            "product", f"{prefix}:{sku}", p.get("title", sku), text, source,
            {"sku": sku, "prezzo_eur": p.get("price_eur"), "categoria": prefix.upper(), "slug": p.get("filename")},
        ))
    return chunks


def chunk_regole(data: dict) -> list[dict]:
    chunks: list[dict] = []
    for bundle in data.get("bundles", []):
        opts = ", ".join(o["label"] for o in bundle.get("options", []))
        text = (
            f"Bundle {bundle['name']} (id {bundle['id']}): {bundle.get('description', '')}. "
            f"Base SKU {bundle.get('base_sku')}. Opzioni: {opts or 'nessuna'}."
        )
        chunks.append(_chunk(
            "bundle", f"bundle:{bundle['id']}", bundle["name"], text,
            "offerte-ai/data/offerte-regole.json",
            {"bundle_id": bundle["id"], "base_sku": bundle.get("base_sku")},
        ))
    return chunks


def chunk_voci_extra(data: dict) -> list[dict]:
    chunks: list[dict] = []
    for v in data.get("voci", []):
        text = f"{v.get('nome', '')}. {v.get('descrizione', '')} Prezzo {v.get('prezzo_eur', 0)} EUR. {v.get('note', '')}"
        chunks.append(_chunk(
            "custom", f"extra:{v.get('id', v.get('nome', '')[:20])}", v.get("nome", "Voce extra"), text.strip(),
            "offerte-ai/data/voci-extra.json",
            {"prezzo_eur": v.get("prezzo_eur"), "source": v.get("source", "manuale")},
        ))
    return chunks


def chunk_faq_index(html: str) -> list[dict]:
    chunks: list[dict] = []
    for block in re.finditer(r'"@type"\s*:\s*"Question"[\s\S]*?"name"\s*:\s*"([^"]+)"[\s\S]*?"text"\s*:\s*"([^"]+)"', html):
        q, a = unescape(block.group(1)), unescape(block.group(2))
        text = f"Domanda: {q}\nRisposta: {a}"
        slug = re.sub(r"[^a-z0-9]+", "-", q.lower())[:50]
        chunks.append(_chunk("faq", f"site-faq:{slug}", q, text, "index.html", {"category": "faq-sito"}))
    return chunks


def main() -> None:
    chunks: list[dict] = []
    listino_data: dict = {}
    manifest_data: dict = {}

    fix_script = ROOT / "scripts" / "fix_product_categories.py"
    if fix_script.exists():
        import subprocess
        subprocess.run([sys.executable, str(fix_script)], check=False, cwd=str(ROOT))

    if LISTINO.exists():
        listino_data = json.loads(LISTINO.read_text(encoding="utf-8"))
    elif SAMPLE.exists():
        print(f"WARN: uso {SAMPLE.name}")
        listino_data = json.loads(SAMPLE.read_text(encoding="utf-8"))

    if MANIFEST.exists():
        manifest_data = json.loads(MANIFEST.read_text(encoding="utf-8"))

    if listino_data:
        chunks.extend(chunk_listino(listino_data, manifest_data))
    if manifest_data:
        chunks.extend(chunk_manifest_only(manifest_data, set(listino_data.keys())))

    if AMR.exists():
        amr = json.loads(AMR.read_text(encoding="utf-8"))
        chunks.extend(chunk_catalog_list(amr if isinstance(amr, list) else amr.get("products", []), "data/amr-products.json", "amr"))

    if COBOT.exists():
        cobot = json.loads(COBOT.read_text(encoding="utf-8"))
        chunks.extend(chunk_catalog_list(cobot if isinstance(cobot, list) else [], "data/cobot-products.json", "cobot"))

    if REGOLE.exists():
        chunks.extend(chunk_regole(json.loads(REGOLE.read_text(encoding="utf-8"))))

    if VOCI_EXTRA.exists():
        chunks.extend(chunk_voci_extra(json.loads(VOCI_EXTRA.read_text(encoding="utf-8"))))

    if KB_DIR.exists():
        for md in sorted(KB_DIR.glob("*.md")):
            chunks.extend(chunk_md(md.read_text(encoding="utf-8"), str(md.relative_to(ROOT))))

    if INDEX_HTML.exists():
        chunks.extend(chunk_faq_index(INDEX_HTML.read_text(encoding="utf-8", errors="ignore")))

    chunks = [c for c in chunks if c]

    payload = {
        "version": 2,
        "generated_by": "scripts/build_knowledge_index.py",
        "chunk_count": len(chunks),
        "sources": {
            "listino_skus": len(listino_data),
            "manifest_skus": len(manifest_data),
        },
        "chunks": chunks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK: {len(chunks)} chunk -> {OUT}")
    print(f"    listino: {len(listino_data)} SKU | manifest: {len(manifest_data)} SKU")


if __name__ == "__main__":
    main()
