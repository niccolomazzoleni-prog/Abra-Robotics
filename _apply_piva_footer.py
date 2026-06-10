#!/usr/bin/env python3
"""Applica riferimenti P.IVA Niccolò Mazzoleni / Portogruaro nei footer."""
import glob
import re

FOOTER_STD = (
    "© 2026 Abra Robotics di Niccolò Mazzoleni. "
    "Tutti i diritti riservati. P.IVA 04800170278 — Portogruaro (VE)."
)
FOOTER_COMPACT = (
    "© 2026 Abra Robotics di Niccolò Mazzoleni. "
    "P.IVA 04800170278 — Portogruaro (VE)."
)
CONTACT_ADDR = "<p>Viale Trieste 105<br>30026 Portogruaro (VE)</p>"

LEGAL_PROD = """\
    <div class="container footer-bottom">
      <p class="footer-copy">{copy}</p>
      <nav class="footer-legal" aria-label="Note legali">
        <a href="../privacy-policy.html">Privacy</a>
        <a href="../note-legali.html">Note legali</a>
      </nav>
    </div>"""

LEGAL_ROOT = """\
    <div class="container footer-bottom">
      <p class="footer-copy">{copy}</p>
      <nav class="footer-legal" aria-label="Note legali">
        <a href="privacy-policy.html">Privacy</a>
        <a href="note-legali.html">Note legali</a>
      </nav>
    </div>"""

REPLACEMENTS = [
    ("        <p>Italia</p>", "        " + CONTACT_ADDR),
    (
        "&copy; 2026 Abra Robotics di Niccolò Mazzoleni. Tutti i diritti riservati. P.IVA 04800170278.",
        FOOTER_STD,
    ),
    (
        "&copy; 2026 Abra Robotics. Tutti i diritti riservati. P.IVA 04800170278.",
        FOOTER_STD,
    ),
    (
        "&copy; 2026 Abra Robotics. Tutti i diritti riservati. P.IVA [DA COMPLETARE].",
        FOOTER_STD,
    ),
    ("&copy; 2026 Abra Robotics. Tutti i diritti riservati.", FOOTER_STD),
    ("&copy; 2026 Abra Robotics.", FOOTER_COMPACT),
    ("© 2026 Abra Robotics.", FOOTER_COMPACT),
    (
        '<footer class="footer"><div class="container footer-inner"><p>© 2026 Abra Robotics</p></div></footer>',
        '<footer class="footer"><div class="container footer-bottom"><p class="footer-copy">'
        + FOOTER_COMPACT
        + '</p><nav class="footer-legal" aria-label="Note legali"><a href="privacy-policy.html">Privacy</a><a href="note-legali.html">Note legali</a></nav></div></footer>',
    ),
]

COMPACT_FOOTER_RE = re.compile(
    r'<div class="container footer-bottom"><p class="footer-copy">[^<]*</p></div>',
    re.MULTILINE,
)


def patch_file(path: str) -> int:
    t = open(path, encoding="utf-8").read()
    orig = t
    for old, new in REPLACEMENTS:
        t = t.replace(old, new)

    prefix = "../" if path.replace("\\", "/").startswith("prodotti/") else ""
    legal_block = (
        LEGAL_PROD.format(copy=FOOTER_COMPACT)
        if prefix
        else LEGAL_ROOT.format(copy=FOOTER_COMPACT)
    )

    def compact_sub(m):
        inner = m.group(0)
        if "footer-legal" in inner:
            return inner
        return legal_block

    t = COMPACT_FOOTER_RE.sub(compact_sub, t)

    # listino: preserve extra note
    t = t.replace(
        FOOTER_COMPACT + " Listino End-User",
        FOOTER_STD.replace("Tutti i diritti riservati. ", "") + " Listino End-User",
    )
    if "Listino End-User" in t and FOOTER_COMPACT in t and "Listino" in path:
        t = t.replace(
            FOOTER_COMPACT + ". Listino",
            FOOTER_COMPACT + " &middot; Listino",
        )

    if t != orig:
        open(path, "w", encoding="utf-8").write(t)
        return 1
    return 0


n = 0
for pattern in ("*.html", "prodotti/*.html"):
    for f in glob.glob(pattern):
        if "admin" in f.replace("\\", "/") or "scripts" in f.replace("\\", "/"):
            continue
        n += patch_file(f)
print("File aggiornati:", n)
