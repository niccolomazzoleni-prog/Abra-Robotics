"""Barra in alto, menu e footer tradotti per le pagine delle lingue (de fr es pl nl cs sv da no fi).

Le pagine delle lingue usano il menu del sito inglese: le voci restano link alle pagine inglesi
(dove non esiste una pagina nella lingua), ma etichette, barra in alto e footer sono tradotti,
il logo porta alla home della lingua, Prezzi/Listino portano ai modelli con prezzi della lingua e
Finanziamenti agli incentivi del paese.

Uso:
    python scripts/lingue_chrome.py            # applica a tutte le pagine delle 10 lingue
    from lingue_chrome import localize_chrome   # dai generatori
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANGS = ("de", "fr", "es", "pl", "nl", "cs", "sv", "da", "no", "fi")

KEYS = ("Products", "Cobots", "AMR", "Quadrupeds", "Humanoids", "Accessories", "Full catalog", "Price list",
        "Prices", "Find the right robot", "Financing", "For whom", "Manufacturing & Logistics",
        "Universities & Research", "About us", "Book a call", "Navigation", "Contact", "Italy")

T = {
    "de": ("Produkte|Cobots|AMR|Vierbeiner|Humanoide|Zubehör|Gesamtkatalog|Preisliste|Preise|Passenden Roboter finden|Finanzierung|Branchen|Fertigung & Logistik|Hochschulen & Forschung|Über uns|Gespräch buchen|Navigation|Kontakt|Italien",
           "Unitree Roboter mit Lieferung aus Italien · Support auf Englisch",
           "Angewandte Robotik für Unternehmen, Hochschulen und Forschungseinrichtungen. Hardware, Software nach Maß, Schulung und technischer Support.",
           "Alle Rechte vorbehalten."),
    "fr": ("Produits|Cobots|AMR|Quadrupèdes|Humanoïdes|Accessoires|Catalogue complet|Liste de prix|Prix|Trouver le bon robot|Financement|Secteurs|Industrie & logistique|Universités & recherche|Qui sommes-nous|Réserver un appel|Navigation|Contact|Italie",
           "Robots Unitree livrés depuis l'Italie · support en anglais",
           "Robotique appliquée pour les entreprises, les universités et les centres de recherche. Matériel, logiciel sur mesure, formation et support technique dédié.",
           "Tous droits réservés."),
    "es": ("Productos|Cobots|AMR|Cuadrúpedos|Humanoides|Accesorios|Catálogo completo|Tarifa de precios|Precios|Encontrar el robot adecuado|Financiación|Sectores|Industria y logística|Universidades e investigación|Quiénes somos|Reservar una llamada|Navegación|Contacto|Italia",
           "Robots Unitree con envío desde Italia · soporte en inglés",
           "Robótica aplicada para empresas, universidades y centros de investigación. Hardware, software a medida, formación y soporte técnico dedicado.",
           "Todos los derechos reservados."),
    "pl": ("Produkty|Coboty|AMR|Roboty czworonożne|Humanoidy|Akcesoria|Pełny katalog|Cennik|Ceny|Znajdź odpowiedniego robota|Finansowanie|Branże|Produkcja i logistyka|Uczelnie i badania|O nas|Umów rozmowę|Nawigacja|Kontakt|Włochy",
           "Roboty Unitree z wysyłką z Włoch · wsparcie po angielsku",
           "Robotyka stosowana dla firm, uczelni i instytutów badawczych. Sprzęt, oprogramowanie na zamówienie, szkolenia i wsparcie techniczne.",
           "Wszelkie prawa zastrzeżone."),
    "nl": ("Producten|Cobots|AMR|Vierpotige robots|Humanoïden|Accessoires|Volledige catalogus|Prijslijst|Prijzen|Vind de juiste robot|Financiering|Sectoren|Productie & logistiek|Universiteiten & onderzoek|Over ons|Plan een gesprek|Navigatie|Contact|Italië",
           "Unitree-robots geleverd vanuit Italië · ondersteuning in het Engels",
           "Toegepaste robotica voor bedrijven, universiteiten en onderzoeksinstellingen. Hardware, software op maat, training en technische ondersteuning.",
           "Alle rechten voorbehouden."),
    "cs": ("Produkty|Coboty|AMR|Čtyřnozí roboti|Humanoidi|Příslušenství|Kompletní katalog|Ceník|Ceny|Najděte správného robota|Financování|Obory|Výroba a logistika|Univerzity a výzkum|O nás|Domluvit hovor|Navigace|Kontakt|Itálie",
           "Roboti Unitree s dodáním z Itálie · podpora v angličtině",
           "Aplikovaná robotika pro firmy, univerzity a výzkumné instituce. Hardware, software na míru, školení a technická podpora.",
           "Všechna práva vyhrazena."),
    "sv": ("Produkter|Cobotar|AMR|Fyrbenta robotar|Humanoider|Tillbehör|Hela katalogen|Prislista|Priser|Hitta rätt robot|Finansiering|Branscher|Tillverkning & logistik|Universitet & forskning|Om oss|Boka ett samtal|Navigering|Kontakt|Italien",
           "Unitree-robotar levererade från Italien · support på engelska",
           "Tillämpad robotik för företag, universitet och forskningsinstitut. Hårdvara, skräddarsydd mjukvara, utbildning och teknisk support.",
           "Alla rättigheter förbehållna."),
    "da": ("Produkter|Cobots|AMR|Firbenede robotter|Humanoider|Tilbehør|Hele kataloget|Prisliste|Priser|Find den rigtige robot|Finansiering|Brancher|Produktion & logistik|Universiteter & forskning|Om os|Book et opkald|Navigation|Kontakt|Italien",
           "Unitree-robotter leveret fra Italien · support på engelsk",
           "Anvendt robotteknologi til virksomheder, universiteter og forskningsinstitutioner. Hardware, skræddersyet software, træning og teknisk support.",
           "Alle rettigheder forbeholdes."),
    "no": ("Produkter|Cobots|AMR|Firbeinte roboter|Humanoider|Tilbehør|Hele katalogen|Prisliste|Priser|Finn riktig robot|Finansiering|Bransjer|Produksjon & logistikk|Universiteter & forskning|Om oss|Bestill en samtale|Navigasjon|Kontakt|Italia",
           "Unitree-roboter levert fra Italia · støtte på engelsk",
           "Anvendt robotikk for bedrifter, universiteter og forskningsinstitusjoner. Maskinvare, skreddersydd programvare, opplæring og teknisk støtte.",
           "Alle rettigheter forbeholdt."),
    "fi": ("Tuotteet|Cobotit|AMR|Nelijalkaiset robotit|Humanoidit|Lisävarusteet|Koko luettelo|Hinnasto|Hinnat|Löydä oikea robotti|Rahoitus|Toimialat|Valmistus ja logistiikka|Yliopistot ja tutkimus|Tietoa meistä|Varaa puhelu|Navigointi|Yhteystiedot|Italia",
           "Unitree-robotit toimitettuna Italiasta · tuki englanniksi",
           "Sovellettua robotiikkaa yrityksille, yliopistoille ja tutkimuslaitoksille. Laitteet, räätälöity ohjelmisto, koulutus ja tekninen tuki.",
           "Kaikki oikeudet pidätetään."),
}

EN_TOP = "Unitree Italy distribution chain"
EN_DESC = "Applied robotics for companies, universities and research institutions. Hardware, custom software, training and dedicated technical support."
EN_COPY = "All rights reserved."
# link inglesi che hanno un equivalente nella lingua
LOCAL = {
    r"(?:\.\./|/)en/index-en\.html": "/{c}/",
    r"(?:\.\./|/)en/listino-unitree-en\.html": "/{c}/#models",
    r"(?:\.\./|/)en/finanziamenti-en\.html": "/{c}/#incentives",
}


def _labels(seg: str, code: str) -> str:
    names = dict(zip(KEYS, T[code][0].split("|")))
    for en, loc in names.items():
        esc = re.escape(en.replace("&", "&amp;"))
        seg = re.sub(rf">(\s*){esc}(\s*)(<|$)", lambda m: f">{m.group(1)}{loc.replace('&', '&amp;')}{m.group(2)}{m.group(3)}", seg)
        # bottoni dei menu a tendina: "Products <span class="nav-caret">"
        seg = re.sub(rf">(\s*){esc} <span", lambda m: f">{m.group(1)}{loc.replace('&', '&amp;')} <span", seg)
    for pat, tgt in LOCAL.items():
        seg = re.sub(rf'href="{pat}', f'href="{tgt.format(c=code)}', seg)
    return seg


def localize_chrome(html: str, code: str) -> str:
    if code not in T:
        return html
    _, top, desc, copy = T[code]
    html = html.replace(f"<p>{EN_TOP}</p>", f"<p>{top}</p>", 1)

    def region(pattern: str, s: str) -> str:
        return re.sub(pattern, lambda m: _labels(m.group(0), code), s, count=1, flags=re.S)

    html = region(r'<nav class="navbar">.*?</nav>', html)
    html = region(r'<footer class="footer">.*?</footer>', html)
    html = html.replace(EN_DESC, desc).replace(EN_COPY, copy)
    return html


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    n = 0
    for code in LANGS:
        for p in sorted((ROOT / code).rglob("*.html")):
            s = p.read_text(encoding="utf-8")
            if 'http-equiv="refresh"' in s[:5000]:
                continue
            t = localize_chrome(s, code)
            if t != s:
                p.write_text(t, encoding="utf-8")
                n += 1
    print(f"pagine aggiornate: {n}")


if __name__ == "__main__":
    main()
