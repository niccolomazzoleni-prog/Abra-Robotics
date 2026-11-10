"""Rifà le pagine categoria (quadrupedi, cobot, AMR, accessori) sul modello di umanoidi.html.

Struttura di ogni pagina, come Umanoidi:
  hero corto (titolo, una frase, numeri senza prezzi "da")
  riga di link alle famiglie
  "Quale ... ti serve?": una scheda per famiglia (foto, nome, una frase, numero di configurazioni)
  una sezione per famiglia con le schede prodotto esistenti (e, per i quadrupedi, le altre configurazioni dal listino)
  poi tutto il resto della pagina (tabelle, guide, video, FAQ) invariato, sotto le famiglie.

I prezzi non sono mai preceduti da "da" / "a partire da": le schede mostrano il prezzo del modello.
Uso: python3 scripts/gen_category_hubs.py   (costruzione iniziale)
     python3 scripts/gen_category_hubs.py --liste   (pagina gia' costruita: aggiorna solo le liste "Altre configurazioni")
"""
import html
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from gen_umanoidi_hub import STYLE, eur, elenco, voce  # noqa: E402

LISTINO = json.loads((ROOT / "listini/pubblico/end-user.json").read_text(encoding="utf-8"))

PAGES = {
    "quadrupedi.html": dict(
        noun="Quale quadrupede ti serve?",
        lead="Quattro famiglie di quadrupedi Unitree, dal Go2 per la didattica al B2 per i carichi pesanti. "
             "Prezzi End-User, IVA esclusa.",
        grid="filters", unit=("configurazione", "configurazioni"),
        move_up=["prezzi", "quale-scegliere", "guide"],   # sezioni di testo che finiscono sotto le famiglie
        families=[
            dict(id="go2", name="Unitree Go2", page="go2.html", sel='[data-family="go2"]', listino=r"^GO2W?-",
                 claim="Il quadrupede compatto per didattica, sviluppo e demo: circa 15 kg, LiDAR 4D, SDK e ROS 2 nelle versioni EDU."),
            dict(id="as2", name="Unitree AS2", page="as2.html", sel='[data-family="as2"]', listino=r"^AS2-",
                 claim="Piattaforma professionale di circa 20 kg, fino a IP54, con più carico e autonomia del Go2."),
            dict(id="a2", name="Unitree A2", page="a2.html", sel='[data-family="a2"]', listino=r"^A2W?-",
                 claim="Quadrupede industriale per ispezioni e trasporto: circa 25 kg di carico, IP56 o IP67, oltre 5 ore di autonomia."),
            dict(id="b2", name="Unitree B2", page="b2.html", sel='[data-family="b2"]', listino=r"^B2W?-",
                 claim="Per carichi pesanti e lavoro all'aperto: oltre 40 kg in camminata, IP67, sale le scale."),
        ]),
    "amr.html": dict(
        noun="Quale AMR ti serve?",
        lead="Robot mobili autonomi per spostare tote, carrelli e pallet tra i reparti, da 200 a 1.500 kg. "
             "Prezzi End-User, IVA esclusa.",
        grid="filters", unit=("modello", "modelli"),
        move_up=[],
        families=[
            dict(id="leggeri", name="AMR leggeri", page=None, sel='[data-family="leggeri"]',
                 claim="AutoXing e Youibot fino a 300 kg: tote, cassette e piccoli carrelli tra postazioni vicine."),
            dict(id="mir", name="MiR", page=None, sel='[data-family="mir"]',
                 claim="La gamma Mobile Industrial Robots da 250 a 1.350 kg, con moduli shelf, hook e pallet e la flotta MiR Fleet."),
            dict(id="pesanti", name="Carichi pesanti", page=None, sel='[data-family="latent"],[data-family="muletti"]',
                 claim="AMR latenti e transpallet autonomi fino a 1.500 kg per pallet e semilavorati pesanti."),
            dict(id="mobile-cobot", name="Manipolatori mobili", page=None, sel='[data-family="mobile-cobot"]',
                 claim="Base AMR con cobot a bordo: il robot si sposta e carica o scarica il pezzo da solo."),
        ]),
    "cobot.html": dict(
        noun="Quale cobot ti serve?",
        lead="Cobot Fairino da 3 a 30 kg, celle di palletizzazione e pinze OnRobot e Robotiq. "
             "Prezzi End-User, IVA esclusa.",
        grid="blocks", unit=("modello", "modelli"),
        move_up=[],
        families=[
            dict(id="cobot", name="Cobot Fairino FR", page=None, sel="#cobot",
                 claim="Bracci a 6 assi da 3 a 30 kg, con controller. La pinza si sceglie a parte."),
            dict(id="palletizzazione", name="Palletizzazione", page=None, sel="#palletizzazione",
                 claim="Workstation modulari e celle chiavi in mano con cobot integrato, per il fine linea."),
            dict(id="pinze", name="Pinze e gripper", page=None, sel="#pinze", img="images/manifattura/fairino-cobot.webp",
                 claim="Pinze a dita e ventose OnRobot e Robotiq da montare sui cobot, scelte sul pezzo da afferrare."),
        ]),
    "accessori.html": dict(
        noun="Quale accessorio ti serve?",
        lead="Mani, batterie, LiDAR, telecomandi, bracci e moduli di calcolo per i robot Unitree. "
             "Prezzi End-User, IVA esclusa.",
        grid="acc", unit=("prodotto", "prodotti"),
        move_up=[],
        families=[
            dict(id="mani", name="Mani e gripper", page=None, sel=0,
                 claim="Mani dexterous Dex3 e Inspire e gripper per umanoidi e bracci Unitree."),
            dict(id="batterie", name="Batterie e alimentazione", page=None, sel=1,
                 claim="Batterie di ricambio e a lunga durata, caricabatterie e stazioni di ricarica."),
            dict(id="sensori", name="Sensori LiDAR e camere", page=None, sel=2,
                 claim="LiDAR 3D e camere di profondità per mappatura, navigazione e percezione."),
            dict(id="controllo", name="Controllo e sviluppo", page=None, sel=3,
                 claim="Telecomandi, moduli di calcolo e strumenti per sviluppare sui robot."),
            dict(id="bracci", name="Bracci robotici", page=None, sel=4,
                 claim="Bracci Unitree Z1 e D1 da montare sui quadrupedi o sul banco."),
        ]),
}

CHIP = ('<a href="{href}" style="padding:6px 12px;border:1px solid var(--gray-200);border-radius:999px;'
        'color:var(--black);text-decoration:none;font-size:.9rem">{name}</a>')


def frag(markup):
    return BeautifulSoup(markup, "html.parser")


def listino_items(rx):
    out = [(k, v) for k, v in LISTINO.items()
           if v.get("categoria") == "UMANOIDI" and re.match(rx, k) and not v.get("prezzo_da") and v.get("prezzo_eur")]
    return sorted(out, key=lambda kv: kv[1]["prezzo_eur"])


def item_link(v):
    return voce(None, v)


def aggiorna_liste(path):
    """Riscrive in una pagina gia' generata le liste "Altre configurazioni" (schede con miniatura) e lo stile,
    senza ricostruire la pagina. Idempotente. Uso: python3 scripts/gen_category_hubs.py --liste"""
    t = (ROOT / path).read_text(encoding="utf-8")
    by_slug = {v["slug"]: v for v in LISTINO.values() if v.get("slug")}
    soup = BeautifulSoup(t, "html.parser")
    for h3 in soup.select("h3.fam-serie"):
        lst = h3.find_next_sibling()
        if lst is None or "fam-list" not in (lst.get("class") or []):
            continue
        slugs = [a["href"].split("/")[-1] for a in lst.select("a[href]")]
        nxt = lst.find_next_sibling()
        if nxt is not None and "fam-more" in (nxt.get("class") or []):
            slugs += [a["href"].split("/")[-1] for a in nxt.select("a[href]")]
            nxt.decompose()
        items = [(None, by_slug[s]) for s in slugs if s in by_slug]
        if len(items) != len(slugs):
            continue
        lst.replace_with(frag(elenco(items)))
    st = soup.select_one("style#hub-style")
    if st is not None:
        st.replace_with(frag(STYLE))
    (ROOT / path).write_text(str(soup), encoding="utf-8")
    print(path, "liste aggiornate")


def first_img(nodes):
    for n in nodes:
        for img in n.select("img"):
            src = img.get("src") or ""
            if src and not src.startswith("data:"):
                return src
    return ""


def senza_da(s):
    """Nessun prezzo preceduto da "da" o "a partire da"."""
    s = s.replace("costano da <strong>2.576 €</strong> (Go2 Air) a oltre", "costano tra <strong>2.576 €</strong> (Go2 Air) e oltre")
    s = s.replace("prezzi da 2.576 € IVA esclusa", "prezzi IVA esclusa")
    s = s.replace("prezzi «da» IVA esclusa", "prezzi IVA esclusa").replace("Cosa include il prezzo «da»?", "Cosa include il prezzo?")
    s = re.sub(r"\(da (\d[\d.]*(?:,\d+)? €)\)", r"(\1 la versione base)", s)
    s = re.sub(r"<td><strong>da (\d[\d.]*(?:,\d+)? €)</strong></td>", r"<td><strong>\1</strong> versione base</td>", s)
    s = re.sub(r"\b(?:[Aa] partire da|[Dd]a)\s+((?:<(?:strong|span|b)[^>]*>\s*)?\d[\d.]*(?:,\d+)?\s*(?:€|&euro;))", r"\1", s)
    return s


def build(path, cfg):
    t = (ROOT / path).read_text(encoding="utf-8")
    soup = BeautifulSoup(t, "html.parser")

    # già generata: rimuovi le parti generate prima di ricostruire
    for old in soup.select("[data-hub]"):
        old.decompose()

    # stile delle famiglie (lo stesso di Umanoidi)
    if not soup.select_one("style#hub-style"):
        soup.head.append(frag(STYLE))

    hero = soup.select_one(".collection-hero")
    lead = hero.select_one("p.lead") or hero.select_one("h1").find_next_sibling("p")
    if lead is not None:
        lead.string = cfg["lead"]
        lead["class"] = "lead"
    for extra in hero.select(".tldr"):
        extra.decompose()
    for d in hero.select(".hero-meta > div"):
        if re.search(r"\b[Dd]a\s*\d", d.get_text(" ")):
            d.decompose()

    # schede prodotto per famiglia
    groups = []
    if cfg["grid"] == "filters":
        grid_sec = soup.select_one(".coll-filters").find_parent("section")
        cards = grid_sec.select(".robot-card")
        for f in cfg["families"]:
            fams = re.findall(r'data-family="([^"]+)"', f["sel"])
            sel = [c for c in cards if c.get("data-family") in fams]
            groups.append([c.extract() for c in sel])
    elif cfg["grid"] == "blocks":
        grid_sec = soup.select_one(".coll-filters").find_parent("section")
        for f in cfg["families"]:
            blk = grid_sec.select_one(f["sel"])
            nodes = [n.extract() for n in blk.find_all(recursive=False) if "hub-block-head" not in (n.get("class") or [])]
            groups.append(nodes)
    else:  # accessori
        grid_sec = soup.select_one(".acc-group").find_parent("section")
        blocks = grid_sec.select(".acc-group")
        for f in cfg["families"]:
            blk = blocks[f["sel"]]
            groups.append([n.extract() for n in blk.find_all(recursive=False) if n.name != "h2"])

    # schede famiglia
    fam_cards, fam_secs, chips = [], [], []
    for f, nodes in zip(cfg["families"], groups):
        extra = listino_items(f["listino"]) if f.get("listino") else []
        shown = " ".join(str(n) for n in nodes)
        extra = [(k, v) for k, v in extra if f'prodotti/{v["slug"]}' not in shown]
        n_cards = sum(len(n.select(".robot-card,.acc-card,.gripper-card")) or (1 if "robot-card" in (n.get("class") or []) else 0)
                      for n in nodes)
        count = n_cards + len(extra)
        img = f.get("img") or first_img(nodes)
        page_link = f'<a class="fam-card-link" href="{f["page"]}">Pagina famiglia</a>' if f["page"] else ""
        chips.append(CHIP.format(href=f["page"] or f'#fam-{f["id"]}', name=f["name"]))
        fam_cards.append(
            f'<article class="fam-card"><a class="fam-card-media" href="#fam-{f["id"]}">'
            f'<img src="{img}" alt="{html.escape(f["name"])}" loading="lazy"></a>'
            f'<div class="fam-card-body"><h3>{f["name"]}</h3><p class="fam-card-claim">{f["claim"]}</p>'
            f'<p class="fam-card-meta"><span>{count} {cfg["unit"][0] if count == 1 else cfg["unit"][1]}</span></p>'
            f'<div class="fam-card-actions"><a class="btn btn-primary" href="#fam-{f["id"]}">Vedi {cfg["unit"][1]}</a>{page_link}</div>'
            f'</div></article>')
        side_btn = f'<a class="btn btn-secondary" href="{f["page"]}">Pagina famiglia {f["name"].replace("Unitree ", "")}</a>' if f["page"] else ""
        sec = frag(
            f'<section class="section fam-section" id="fam-{f["id"]}" data-hub="1"><div class="container">'
            f'<div class="fam-head"><div><h2>{f["name"]}</h2><p class="fam-head-claim">{f["claim"]}</p></div>'
            f'<div class="fam-head-side"><img src="{img}" alt="{html.escape(f["name"])}" loading="lazy">{side_btn}</div></div>'
            f'<div class="fam-body"></div>'
            + (f'<h3 class="fam-serie">Altre configurazioni <span>{len(extra)}</span></h3>'
               + elenco(extra) if extra else "")
            + '<p class="fam-back"><a href="#famiglie">↑ Torna alle famiglie</a></p></div></section>')
        body = sec.select_one(".fam-body")
        if cfg["grid"] == "filters":
            grid = soup.new_tag("div", attrs={"class": "robot-grid"})
            for n in nodes:
                grid.append(n)
            body.append(grid)
        else:
            for n in nodes:
                body.append(n)
        fam_secs.append(sec)

    chips_sec = frag('<section class="section" style="padding:8px 0 0" data-hub="1"><div class="container">'
                     '<div class="hm-fam" style="display:flex;flex-wrap:wrap;gap:8px">' + "".join(chips) + "</div></div></section>")
    nav = frag('<section class="section fam-nav" id="famiglie" data-hub="1"><div class="container">'
               f'<div class="section-header" style="text-align:left;max-width:100%;"><h2>{cfg["noun"]}</h2></div>'
               '<div class="fam-grid">' + "".join(fam_cards) + "</div></div></section>")

    # vecchie righe di link alle famiglie subito sotto l'hero: sostituite dalla nuova
    nxt = hero.find_next_sibling("section")
    if nxt is not None and not nxt.get("data-hub") and len(nxt.get_text(" ", strip=True)) < 120 and nxt.select("a"):
        nxt.decompose()

    # posizione: subito dopo l'hero; il resto della pagina scorre sotto le famiglie
    anchor = hero
    for fr in [chips_sec, nav] + fam_secs:
        node = fr.find("section").extract()
        anchor.insert_after(node)
        anchor = node
    # il blocco con la griglia originale ora è vuoto: via (tiene titoli/filtri inutili)
    if grid_sec is not None:
        grid_sec.decompose()
    # sezioni di solo testo che stavano sopra la griglia: dopo le famiglie
    last = soup.select(".fam-section[data-hub]")[-1]
    for sid in reversed(cfg["move_up"]):
        s = soup.select_one(f"section#{sid}")
        if s is not None:
            last.insert_after(s.extract())

    (ROOT / path).write_text(senza_da(str(soup)), encoding="utf-8")
    print(path, "famiglie:", len(cfg["families"]), "schede:", [len(g) for g in groups])


if __name__ == "__main__":
    if "--liste" in sys.argv:   # pagine gia' generate: aggiorna solo le liste di schede e lo stile
        aggiorna_liste("quadrupedi.html")
    else:
        for p, c in PAGES.items():
            build(p, c)
