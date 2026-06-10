#!/usr/bin/env python3
"""Rimuove script inline legacy della WA bar e aggiunge script.js dove manca."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OLD_INLINE = re.compile(
    r"\n?\s*<script>\(function\(\)\{var (?:K=\"abra_wa_bar_closed\"|bar=document\.getElementById\(\"wa-bar\"\)).*?</script>",
    re.DOTALL,
)

LP_WA_TOP = re.compile(
    r"\s*<style>\s*/\* LP: WA bar in cima \*/.*?body\.has-wa-bar\s*\{[^}]*\}\s*</style>",
    re.DOTALL,
)


def script_src(path: Path) -> str:
    depth = len(path.relative_to(ROOT).parts) - 1
    prefix = "../" * depth if depth else ""
    return f'{prefix}script.js'


def main() -> None:
    for path in sorted(ROOT.rglob("*.html")):
        if any(p.startswith(".") for p in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        orig = text
        text = OLD_INLINE.sub("", text)
        text = LP_WA_TOP.sub("", text)
        text = text.replace('class="lp-cobot has-wa-bar"', 'class="lp-cobot"')

        rel = path.relative_to(ROOT)
        needs_js = "script.js" not in text and (
            'id="wa-bar"' in text or rel.parts[0] not in ("admin",)
        )
        if needs_js and "</body>" in text:
            src = script_src(path)
            text = text.replace("</body>", f'  <script src="{src}"></script>\n</body>', 1)

        if text != orig:
            path.write_text(text, encoding="utf-8")
            print(f"updated {rel}")


if __name__ == "__main__":
    main()
