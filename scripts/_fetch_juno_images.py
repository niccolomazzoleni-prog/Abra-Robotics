import re
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "images" / "manifattura" / "amr"
UA = {"User-Agent": "Mozilla/5.0"}

def dl(name, url):
    data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25).read()
    (OUT / name).write_bytes(data)
    print(name, len(data))

dl("juno-plus.webp", "https://cdn.prod.website-files.com/67a0d1e7d87774056a9a207f/67a0d1e7d87774056a9a2247_junoplus-p-1600.webp")

for path in ["/en/lieferroboter/junobot-lift", "/en/lieferroboter/juno-lift", "/en/lieferroboter/juno-bot-lift"]:
    try:
        html = urllib.request.urlopen(
            urllib.request.Request(f"https://www.ef-robotics.de{path}", headers=UA), timeout=20
        ).read().decode("utf-8", "replace")
        imgs = [u for u in re.findall(r"https://cdn\.prod\.website-files\.com/[^\"'\s>]+\.webp", html) if "lift" in u.lower() or "juno" in u.lower()]
        print(path, imgs[:5])
        for u in imgs:
            if "lift" in u.lower() and "p-1600" in u:
                dl("juno-lift.webp", u)
                break
    except Exception as e:
        print(path, e)
