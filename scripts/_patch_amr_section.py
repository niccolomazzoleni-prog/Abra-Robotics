from pathlib import Path

root = Path(__file__).resolve().parent.parent
page = root / "manifattura-logistica.html"
frag = (root / "scripts" / "_amr_catalog_fragment.html").read_text(encoding="utf-8")
text = page.read_text(encoding="utf-8")

start_marker = "<!-- SEZIONE 3 - AMR / LOGISTICA INTERNA -->"
end_marker = "<!-- SEZIONE 4 - COBOT -->"
s = text.find(start_marker)
e = text.find(end_marker)
if s < 0 or e < 0:
    raise SystemExit(f"markers not found s={s} e={e}")

chunk = text[s:e]
head_end = chunk.find('      <div class="robot-grid cols-3">')
if head_end < 0:
    raise SystemExit("robot-grid not found in AMR section")
inner_end = chunk.rfind('      <div class="section-cta-row">')
if inner_end < 0:
    raise SystemExit("section-cta-row not found in AMR section")

head = chunk[:head_end]
tail = chunk[inner_end:]
new_chunk = head + frag + "\n\n" + tail
new_text = text[:s] + new_chunk + text[e:]
page.write_text(new_text, encoding="utf-8")
print(f"Patched OK — AMR section now {len(new_chunk)} chars")
