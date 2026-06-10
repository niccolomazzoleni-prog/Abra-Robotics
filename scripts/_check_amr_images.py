#!/usr/bin/env python3
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
AMR = ROOT / "images" / "manifattura" / "amr"


def white_pct(path: Path) -> float:
    im = Image.open(path).convert("RGBA")
    white = total = 0
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b, a = im.getpixel((x, y))
            if a < 10:
                continue
            total += 1
            if r > 235 and g > 235 and b > 235:
                white += 1
    return 100 * white / max(total, 1)


def main() -> None:
    for row in json.loads((ROOT / "data" / "amr-catalog.json").read_text(encoding="utf-8")):
        name = Path(row["file"]).name
        pct = white_pct(AMR / name)
        flag = "OK" if pct < 5 else "WARN"
        print(f"{flag} {row['slug']:18} {name:28} {pct:4.1f}%  {row['title']}")


if __name__ == "__main__":
    main()
