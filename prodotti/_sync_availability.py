"""
Scrape availability from quadruped.de and write ../availability.json.
Run manually or via GitHub Actions.
"""
import json, re, datetime, sys
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("pip install requests beautifulsoup4", file=sys.stderr)
    sys.exit(1)

PRODUCTS = {
    "g1":   "https://www.quadruped.de/Unitree-G1",
    "g1d":  "https://www.quadruped.de/Unitree-G1D",
    "go2":  "https://www.quadruped.de/QUADRUPED-Go2",
    "go2w": "https://www.quadruped.de/QUADRUPED-Go2W",
    "b2":   "https://www.quadruped.de/QUADRUPED-B2",
    "b2w":  "https://www.quadruped.de/QUADRUPED-B-W",
    "h1":   "https://www.quadruped.de/Unitree-H1-S-Humanoid-Robot",
    "h2":   "https://www.quadruped.de/Unitree-H2-Humanoid-Robot",
    "r1":   "https://www.quadruped.de/Unitree-R1",
    "r1a":  "https://www.quadruped.de/Unitree-R1-A",
}

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AbraBot/1.0)"}

def parse_date_de(text):
    """DD.MM.YYYY → ISO date + 7 days."""
    m = re.search(r'(\d{1,2})\.(\d{1,2})\.(\d{4})', text)
    if not m:
        return None
    d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
    return (datetime.date(y, mo, d) + datetime.timedelta(days=7)).isoformat()

def scrape(url):
    try:
        r = requests.get(url, timeout=20, headers=HEADERS)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text(" ", strip=True)

        if "Sofort verfügbar" in text:
            return {"status": "available", "source": "Sofort verfügbar"}

        m = re.search(r'Verfügbar ab[:\s]+(\d{1,2}\.\d{1,2}\.\d{4})', text)
        if m:
            from_date = parse_date_de(m.group(0))
            return {"status": "date", "source": m.group(0).strip(), "available_from": from_date}

        if "Ausverkauft" in text:
            return {"status": "unavailable", "source": "Ausverkauft"}

        return {"status": "unknown", "source": ""}
    except Exception as e:
        return {"status": "error", "source": str(e)}

def main():
    out = {
        "updated": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "products": {}
    }
    for key, url in PRODUCTS.items():
        result = scrape(url)
        result["url"] = url
        out["products"][key] = result
        status = result["status"]
        extra = f" → {result.get('available_from','')}" if status == "date" else ""
        print(f"  {key:6s} {status}{extra}")

    import os
    dest = os.path.join(os.path.dirname(__file__), "..", "availability.json")
    with open(dest, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"\nScritto: {os.path.abspath(dest)}")

if __name__ == "__main__":
    main()
