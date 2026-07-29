#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SEO audit + fixes for Abra Robotics (crawl/index, on-page uniqueness)."""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://abrarobotics.com"
SKIP_DIRS = {
    "offerte-ai",
    "admin",
    "node_modules",
    "__pycache__",
    ".git",
    "apps-script",
    "listini",
    "stripe",
    "lp-thank-you",
    "lp-thank-you-en",
}
SKIP_FILES = {
    "index.backup.html",
    "index-zenixa.html",
    "restyle-preview.html",
}

# Wrong absolute EN product URLs (missing /en/ prefix)
ABS_BAD_EN = re.compile(r"https://abrarobotics\.com/prodotti/([A-Za-z0-9._-]+-en\.html)")
# Relative bad from root-ish pages
REL_BAD_EN = re.compile(r'(?:href|content)=(["\'])(?:\./)?prodotti/([A-Za-z0-9._-]+-en\.html)\1')

HREFLANG_BLOCK = re.compile(
    r'<link[^>]+hreflang=["\']([^"\']+)["\'][^>]*>|<link[^>]+rel=["\']alternate["\'][^>]*>',
    re.I,
)
HREFLANG_HREF = re.compile(
    r'hreflang=["\']([^"\']+)["\'][^>]*href=["\']([^"\']+)["\']|'
    r'href=["\']([^"\']+)["\'][^>]*hreflang=["\']([^"\']+)["\']',
    re.I,
)
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.I | re.S)
DESC_RE = re.compile(
    r'<meta\s+(?:'
    r'name=["\']description["\']\s+content="([^"]*)"|'
    r'name=["\']description["\']\s+content=\'([^\']*)\'|'
    r'content="([^"]*)"\s+name=["\']description["\']|'
    r'content=\'([^\']*)\'\s+name=["\']description["\']'
    r')\s*/?>',
    re.I,
)
H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.I | re.S)
CANON_RE = re.compile(
    r'<link[^>]+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']|'
    r'<link[^>]+href=["\']([^"\']+)["\'][^>]*rel=["\']canonical["\']',
    re.I,
)
NOINDEX_RE = re.compile(
    r'<meta\s+name=["\']robots["\']\s+content=["\']([^"\']+)["\']',
    re.I,
)
TAG_STRIP = re.compile(r"<[^>]+>")
WS = re.compile(r"\s+")

# Stub redirects for legacy dead URLs from the SE Ranking audit
STUB_REDIRECTS = {
    "g1.html": "umanoidi.html",
    "h2.html": "prodotti/unitree-h2.html",
    "r1.html": "prodotti/unitree-r1-edu.html",
    "software-en.html": "en/index-en.html",
    "en/software-en.html": "en/index-en.html",
}


def iter_html(*, include_stubs: bool = False) -> list[Path]:
    out = []
    for p in ROOT.rglob("*.html"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.name in SKIP_FILES or p.name.startswith("_"):
            continue
        text_head = p.read_text(encoding="utf-8", errors="replace")[:800]
        if not include_stubs and re.search(
            r'http-equiv=["\']refresh["\']', text_head, re.I
        ):
            continue
        out.append(p)
    return sorted(out)


def url_to_path(url: str) -> Path | None:
    if url.startswith(SITE):
        rel = url[len(SITE) :].lstrip("/")
    elif url.startswith("/"):
        rel = url.lstrip("/")
    else:
        return None
    if not rel or rel.endswith("/"):
        rel = (rel or "") + "index.html"
    return ROOT / rel


def path_exists_for_url(url: str) -> bool:
    p = url_to_path(url)
    if p is None:
        return True  # external / relative unresolved — skip
    if p.exists():
        return True
    # directory index
    if p.suffix == "" and (ROOT / str(p.relative_to(ROOT))).is_dir():
        return True
    return False


def fix_bad_en_urls(text: str) -> tuple[str, int]:
    n = 0

    def abs_sub(m: re.Match) -> str:
        nonlocal n
        n += 1
        return f"{SITE}/en/prodotti/{m.group(1)}"

    text = ABS_BAD_EN.sub(abs_sub, text)

    def rel_sub(m: re.Match) -> str:
        nonlocal n
        n += 1
        q = m.group(1)
        return f"href={q}en/prodotti/{m.group(2)}{q}"

    # Only rewrite absolute-style relative from site root; leave ../en/ alone
    text2, n2 = REL_BAD_EN.subn(
        lambda m: f'href={m.group(1)}en/prodotti/{m.group(2)}{m.group(1)}',
        text,
    )
    return text2, n + n2


def extract_hreflang(text: str) -> dict[str, str]:
    pairs: dict[str, str] = {}
    for m in HREFLANG_HREF.finditer(text):
        if m.group(1) and m.group(2):
            pairs[m.group(1)] = m.group(2)
        elif m.group(3) and m.group(4):
            pairs[m.group(4)] = m.group(3)
    return pairs


def page_url(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return SITE + "/"
    if rel.endswith("/index.html"):
        return SITE + "/" + rel[: -len("index.html")].rstrip("/")
    return SITE + "/" + rel


def it_en_pair(path: Path) -> Path | None:
    rel = path.relative_to(ROOT)
    parts = list(rel.parts)
    name = rel.name
    if parts[0] == "en":
        # EN -> IT
        if name.endswith("-en.html"):
            it_name = name[: -len("-en.html")] + ".html"
        else:
            it_name = name
        it_parts = parts[1:]
        if it_parts:
            it_parts[-1] = it_name
        else:
            it_parts = [it_name]
        # special: en/index-en.html -> index.html
        if name == "index-en.html":
            return ROOT / "index.html"
        return ROOT.joinpath(*it_parts)
    else:
        # IT -> EN
        if name == "index.html" and len(parts) == 1:
            return ROOT / "en" / "index-en.html"
        stem = name[: -len(".html")] if name.endswith(".html") else name
        en_name = f"{stem}-en.html"
        return ROOT / "en" / Path(*parts[:-1]) / en_name if len(parts) > 1 else ROOT / "en" / en_name


def ensure_hreflang(path: Path, text: str) -> tuple[str, bool]:
    """Ensure bidirectional hreflang IT/EN with valid targets."""
    pairs = extract_hreflang(text)
    self_url = page_url(path)
    is_en = path.relative_to(ROOT).parts[0] == "en"
    lang_self = "en" if is_en else "it"
    peer = it_en_pair(path)
    peer_url = page_url(peer) if peer and peer.exists() else None

    # Fix any hreflang pointing to missing /prodotti/*-en.html
    changed = False
    new_pairs = dict(pairs)

    for lang, href in list(new_pairs.items()):
        fixed = ABS_BAD_EN.sub(lambda m: f"{SITE}/en/prodotti/{m.group(1)}", href)
        if fixed != href:
            new_pairs[lang] = fixed
            changed = True
            href = fixed
        if href.startswith(SITE) and not path_exists_for_url(href):
            # drop broken
            del new_pairs[lang]
            changed = True

    new_pairs[lang_self] = self_url
    if peer_url:
        new_pairs["en" if not is_en else "it"] = peer_url
    new_pairs["x-default"] = new_pairs.get("it") or self_url

    # If unchanged structurally and already present, skip rewrite unless broken fixed
    if not changed and pairs.get(lang_self) == self_url and (
        not peer_url or pairs.get("en" if not is_en else "it") == peer_url
    ):
        # still rewrite if any target 404
        for href in pairs.values():
            if href.startswith(SITE) and not path_exists_for_url(href):
                changed = True
                break
        if not changed:
            return text, False

    # Build link tags
    order = []
    if "it" in new_pairs:
        order.append("it")
    if "en" in new_pairs:
        order.append("en")
    if "x-default" in new_pairs:
        order.append("x-default")
    for k in new_pairs:
        if k not in order:
            order.append(k)

    block = "\n".join(
        f'<link href="{new_pairs[lang]}" hreflang="{lang}" rel="alternate"/>'
        for lang in order
    )

    # Replace existing hreflang alternate links
    link_re = re.compile(
        r'<link[^>]+hreflang=["\'][^"\']+["\'][^>]*/?>\s*',
        re.I,
    )
    if link_re.search(text):
        text2 = link_re.sub("", text)
        # insert after canonical if present
        canon = re.search(
            r'<link[^>]+rel=["\']canonical["\'][^>]*/?>',
            text2,
            re.I,
        )
        if canon:
            pos = canon.end()
            text2 = text2[:pos] + "\n" + block + text2[pos:]
        else:
            text2 = text2.replace("</head>", block + "\n</head>", 1)
        return text2, True

    # No hreflang yet — inject after canonical or before </head>
    canon = re.search(
        r'<link[^>]+rel=["\']canonical["\'][^>]*/?>',
        text,
        re.I,
    )
    if canon:
        pos = canon.end()
        return text[:pos] + "\n" + block + text[pos:], True
    if "</head>" in text.lower():
        # case-sensitive-ish
        idx = re.search(r"</head>", text, re.I)
        if idx:
            return text[: idx.start()] + block + "\n" + text[idx.start() :], True
    return text, False


def stub_redirect_html(target_rel: str) -> str:
    target = SITE + "/" + target_rel.lstrip("/")
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8"/>
<title>Redirect — Abra Robotics</title>
<link rel="canonical" href="{target}"/>
<meta http-equiv="refresh" content="0;url={target}"/>
<meta name="robots" content="noindex, follow"/>
<script>location.replace({target!r});</script>
</head>
<body>
<p>Pagina spostata. <a href="{target}">Continua su Abra Robotics</a>.</p>
</body>
</html>
"""


def create_stubs() -> list[str]:
    created = []
    for stub, target in STUB_REDIRECTS.items():
        path = ROOT / stub
        path.parent.mkdir(parents=True, exist_ok=True)
        # Only create if missing OR is empty placeholder; don't overwrite real pages
        if path.exists():
            text = path.read_text(encoding="utf-8", errors="replace")
            # overwrite if it looks like a dead/short page or already a redirect
            if len(text) > 2500 and "http-equiv=\"refresh\"" not in text.lower():
                continue
        path.write_text(stub_redirect_html(target), encoding="utf-8")
        created.append(f"{stub} -> {target}")
    # en/ directory index redirect to index-en.html
    en_index = ROOT / "en" / "index.html"
    if not en_index.exists():
        en_index.write_text(stub_redirect_html("en/index-en.html"), encoding="utf-8")
        created.append("en/index.html -> en/index-en.html")

    # Legacy wrong EN product paths: /prodotti/*-en.html -> /en/prodotti/*-en.html
    en_prod = ROOT / "en" / "prodotti"
    if en_prod.is_dir():
        for en_page in sorted(en_prod.glob("*-en.html")):
            wrong = ROOT / "prodotti" / en_page.name
            if wrong.exists():
                # never overwrite a real product page
                existing = wrong.read_text(encoding="utf-8", errors="replace")
                if len(existing) > 2500 and "http-equiv=\"refresh\"" not in existing.lower():
                    continue
            target = f"en/prodotti/{en_page.name}"
            wrong.write_text(stub_redirect_html(target), encoding="utf-8")
            created.append(f"prodotti/{en_page.name} -> {target}")
    return created


def trim_text(s: str, max_len: int) -> str:
    s = WS.sub(" ", TAG_STRIP.sub("", s)).strip()
    if len(s) <= max_len:
        return s
    cut = s[: max_len - 1].rsplit(" ", 1)[0]
    return cut + "…"


def _desc_value(m: re.Match) -> str:
    for g in m.groups():
        if g is not None:
            return g.strip()
    return ""


def fix_title_desc_h1(path: Path, text: str, title_seen: Counter) -> tuple[str, list[str]]:
    notes: list[str] = []
    m = TITLE_RE.search(text)
    if not m:
        notes.append("missing-title")
        return text, notes
    title = WS.sub(" ", TAG_STRIP.sub("", m.group(1))).strip()
    if title in ("%%LANG_TITLE%%", "", "Redirect — Abra Robotics"):
        return text, notes

    parts = path.relative_to(ROOT).parts
    is_en = parts[:1] == ("en",) or path.name.endswith("-en.html")

    # Uniquify: EN pages that share title with IT get language marker;
    # other duplicates get a short filename hint.
    if title_seen[title] > 1:
        if "| Abra" in title:
            core = title.split("| Abra")[0].strip()
        else:
            core = title.replace("| Abra Robotics", "").strip()
        if is_en:
            new_title = trim_text(core, 42) + " | Abra Robotics EN"
        else:
            token = path.stem.replace("-en", "")
            hint = token.replace("-", " ")
            # keep IT titles distinctive vs LP duplicates (e.g. lc vs non-lc)
            if path.stem.endswith("-lc") or "-lc-" in path.name:
                core = trim_text(core, 40) + " (LC)"
            elif hint.lower() not in core.lower():
                short = " ".join(token.split("-")[-2:]) if token.count("-") else token
                if short and short.lower() not in core.lower():
                    core = f"{core} · {short}"
            new_title = trim_text(core, 48) + " | Abra Robotics"
        if new_title != title:
            text = TITLE_RE.sub(f"<title>{new_title}</title>", text, count=1)
            notes.append(f"title->{new_title[:60]}")
            title = new_title

    if len(title) > 60:
        new_title = trim_text(title, 60)
        text = TITLE_RE.sub(f"<title>{new_title}</title>", text, count=1)
        notes.append("title-trimmed")

    dm = DESC_RE.search(text)
    if not dm:
        core = title.replace("| Abra Robotics EN", "").replace("| Abra Robotics", "").strip()
        if is_en:
            desc = f"{core}. Quotes and support in Italy — Abra Robotics."
        else:
            desc = f"{core}. Preventivi e supporto in Italia — Abra Robotics."
        desc = trim_text(desc, 160)
        text = TITLE_RE.sub(
            lambda mm: mm.group(0)
            + f'\n<meta content="{desc}" name="description"/>',
            text,
            count=1,
        )
        notes.append("desc-added")
    else:
        desc = _desc_value(dm)
        if len(desc) > 160:
            new_desc = trim_text(desc, 160)
            text = DESC_RE.sub(
                f'<meta content="{new_desc}" name="description"/>',
                text,
                count=1,
            )
            notes.append("desc-trimmed")

    h1s = H1_RE.findall(text)
    if len(h1s) > 1:
        count = {"n": 0}

        def repl_h1(mm: re.Match) -> str:
            count["n"] += 1
            if count["n"] == 1:
                return mm.group(0)
            inner = mm.group(1)
            attrs = re.match(r"<h1([^>]*)>", mm.group(0), re.I)
            a = attrs.group(1) if attrs else ""
            return f"<h2{a}>{inner}</h2>"

        text = H1_RE.sub(repl_h1, text)
        notes.append(f"h1-collapsed:{len(h1s)}")

    return text, notes


def fix_broken_local_assets(path: Path, text: str) -> tuple[str, list[str]]:
    notes = []
    # script src and img src local
    asset_re = re.compile(
        r"""((?:src|href)=)(["'])(?!https?:|//|#|mailto:|tel:|data:)([^"']+)\2""",
        re.I,
    )
    base = path.parent

    def check(m: re.Match) -> str:
        prefix, q, ref = m.group(1), m.group(2), m.group(3)
        clean = ref.split("?")[0].split("#")[0]
        if not clean or clean.endswith(".html"):
            return m.group(0)
        target = (base / clean).resolve()
        try:
            target.relative_to(ROOT.resolve())
        except ValueError:
            return m.group(0)
        if target.exists():
            return m.group(0)
        # try common fix: missing en/ prefix for js/css from en pages
        alt = None
        if "en" in path.parts and clean.startswith("../") is False:
            pass
        # try from root
        root_try = ROOT / clean.lstrip("/")
        if root_try.exists():
            # compute relative
            try:
                rel = Path(os_relpath(root_try, base))
                notes.append(f"asset-relink:{ref}->{rel.as_posix()}")
                return f"{prefix}{q}{rel.as_posix()}{q}"
            except Exception:
                pass
        return m.group(0)

    import os

    def os_relpath(target: Path, start: Path) -> str:
        return os.path.relpath(str(target), str(start)).replace("\\", "/")

    new_text = asset_re.sub(check, text)
    return new_text, notes


def audit_report() -> dict:
    pages = iter_html()
    titles: Counter = Counter()
    title_map: dict[str, list[str]] = defaultdict(list)
    h1_map: Counter = Counter()
    missing_desc = []
    long_title = []
    long_desc = []
    bad_en = []
    broken_hreflang = []
    multi_h1 = []
    placeholders = []

    for p in pages:
        text = p.read_text(encoding="utf-8", errors="replace")
        rel = str(p.relative_to(ROOT))
        tm = TITLE_RE.search(text)
        title = WS.sub(" ", TAG_STRIP.sub("", tm.group(1))).strip() if tm else ""
        if title:
            titles[title] += 1
            title_map[title].append(rel)
            if len(title) > 60:
                long_title.append(rel)
            if "%%" in title:
                placeholders.append(rel)
        dm = DESC_RE.search(text)
        if not dm:
            missing_desc.append(rel)
        elif len(_desc_value(dm)) > 160:
            long_desc.append(rel)
        h1s = [WS.sub(" ", TAG_STRIP.sub("", h)).strip() for h in H1_RE.findall(text)]
        if len(h1s) > 1:
            multi_h1.append((rel, len(h1s)))
        for h in h1s:
            h1_map[h] += 1
        for m in ABS_BAD_EN.finditer(text):
            bad_en.append((rel, m.group(0)))
        for lang, href in extract_hreflang(text).items():
            if href.startswith(SITE) and not path_exists_for_url(href):
                broken_hreflang.append((rel, lang, href))

    dups = {t: ps for t, ps in title_map.items() if len(ps) > 1}
    return {
        "pages": len(pages),
        "dup_titles": len(dups),
        "dup_title_samples": list(dups.items())[:20],
        "long_title": len(long_title),
        "long_desc": len(long_desc),
        "missing_desc": missing_desc,
        "bad_en": bad_en[:50],
        "bad_en_count": len(bad_en),
        "broken_hreflang": broken_hreflang[:50],
        "broken_hreflang_count": len(broken_hreflang),
        "multi_h1": multi_h1[:30],
        "placeholders": placeholders,
    }


def run_fix() -> None:
    pages = iter_html()
    # first pass titles
    title_seen: Counter = Counter()
    texts: dict[Path, str] = {}
    for p in pages:
        t = p.read_text(encoding="utf-8", errors="replace")
        texts[p] = t
        tm = TITLE_RE.search(t)
        if tm:
            title_seen[WS.sub(" ", TAG_STRIP.sub("", tm.group(1))).strip()] += 1

    stubs = create_stubs()
    print(f"Stubs: {stubs}")

    stats = Counter()
    for p, text in texts.items():
        original = text
        text, n = fix_bad_en_urls(text)
        stats["bad_en_rewrites"] += n
        text, hl_changed = ensure_hreflang(p, text)
        if hl_changed:
            stats["hreflang_fixed"] += 1
        text, notes = fix_title_desc_h1(p, text, title_seen)
        for nte in notes:
            stats[nte.split(":")[0].split("->")[0]] += 1
        text, anotes = fix_broken_local_assets(p, text)
        stats["asset_notes"] += len(anotes)
        if text != original:
            p.write_text(text, encoding="utf-8")
            stats["files_changed"] += 1

    print("Fix stats:", dict(stats))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit", action="store_true")
    ap.add_argument("--fix", action="store_true")
    args = ap.parse_args()
    if args.audit or not args.fix:
        rep = audit_report()
        print("=== AUDIT ===")
        for k, v in rep.items():
            if k.endswith("_samples") or k in ("bad_en", "broken_hreflang", "multi_h1", "missing_desc"):
                print(f"{k}:")
                for item in v if isinstance(v, list) else []:
                    print(" ", item)
                if k == "dup_title_samples":
                    for t, ps in v:
                        print(f"  [{len(ps)}] {t[:70]} -> {ps[:5]}")
            else:
                print(f"{k}: {v}")
    if args.fix:
        run_fix()
        print("=== POST-FIX AUDIT ===")
        rep = audit_report()
        print("pages", rep["pages"], "dup_titles", rep["dup_titles"], "bad_en", rep["bad_en_count"],
              "broken_hl", rep["broken_hreflang_count"], "missing_desc", len(rep["missing_desc"]))


if __name__ == "__main__":
    main()
