# Listini Abra Robotics — Unitree

## Struttura

```
listini/
├── README.md
├── schema.json
├── pubblico/
│   ├── end-user.json           ← committabile (solo End-User, pubblicabile=true)
│   └── catalogo-manifest.json  ← contenuti tecnici + immagini (no prezzi Gold)
└── interno/listino-master.csv  ← gitignored (Gold + End-User completi)
```

## Visibilità pubblico vs interno

| Risorsa | Pubblico sul sito | Contiene prezzi Gold |
|---------|-------------------|----------------------|
| `catalogo-unitree.html` | Sì | No |
| `listino-unitree.html` | Sì | No |
| `prodotti/*.html` | Sì | No |
| `listini/pubblico/end-user.json` | Sì (fetch) | No |
| `listini/pubblico/catalogo-manifest.json` | Sì (generazione) | No |
| `admin/listini.html` | No (`noindex`, `robots.txt`) | Sì (upload CSV) |
| `listini/interno/` | No (gitignored) | Sì |

**Regola:** sul sito pubblico compaiono **solo prezzi End-User**. I prezzi **Gold** restano in CSV locale / upload su admin.

## Fonti listino partner (PDF ufficiali)

| PDF | Contenuto |
|-----|-----------|
| `25112025_ListinoUmanoidi_Partner.pdf` | G1, R1, **H2 AIR/EDU + accessori H2** (H1 solo in PDF, non sul sito) |
| `08102025_ListinoQuadrupedi_Partner.pdf` | Go2, Go2W, B2, A2, accessori quadrupedi |

Sync automatico: `python scripts/import_listino_partner.py` (colonna **PREZZO AL PUBBLICO** → End-User).

## Regole prezzi

- **End-User** (pubblico sul sito): include spedizione + dazio doganale 3,7%
- **Gold** (distributore): solo in `interno/` — **mai** committare
- Valori **indicativi**, soggetti a cambio EUR/USD
- Ogni ordine va confermato con **preventivo aggiornato**

## Workflow

1. Aggiornare `listini/interno/listino-master.csv` (locale)
2. Aggiornare contenuti tecnici in `scripts/catalogo_contenuti.py` se necessario
3. Eseguire: `python scripts/build_catalogo_manifest.py`
4. Eseguire: `python scripts/genera_catalogo_completo.py` (schede + catalogo + listino)
5. Oppure solo prezzi: `python scripts/genera_prezzi.py`
6. Verificare in locale prima del push
7. Committare: `pubblico/`, `scripts/`, HTML aggiornati — **non** `interno/`

## Gestione immagini prodotto

| Risorsa | Ruolo |
|---------|-------|
| `data/product-images.json` | Override SKU → percorso immagine (+ URL Unitree opzionale) |
| `admin/immagini.html` | UI interna: import file, anteprima, export ZIP/JSON |
| `scripts/publish_images.py` | Scarica URL, applica ZIP export, rigenera catalogo |

### Workflow immagini

1. Apri `admin/immagini.html` in locale (`http://localhost:8765/admin/immagini.html`)
2. Importa immagine per SKU oppure incolla URL Unitree
3. **Salva nel progetto** (Chrome/Edge + cartella collegata) oppure **Esporta ZIP**
4. Da terminale: `python scripts/publish_images.py` (o `--from-zip export.zip`)
5. Commit + push: includere `images/`, `data/product-images.json`, HTML rigenerati

## Stripe Payment Link (GitHub Pages)

Architettura statica: nessun backend. Il checkout usa **Stripe Payment Link** creati nella dashboard Stripe.

| File | Ruolo |
|------|-------|
| `prodotti/stripe-config.js` | Mappa `filename.html` → URL `https://buy.stripe.com/...` |
| `prodotti/ecommerce.js` | Collega `.buy-btn` al Payment Link; fallback a `#form` se link vuoto |

### Attivazione checkout

1. In Stripe Dashboard → **Payment Links** → crea un link per SKU (o per famiglia prodotto)
2. Apri `prodotti/stripe-config.js`
3. Incolla l'URL nel valore corrispondente, es. `"unitree-go2w-u3.html": "https://buy.stripe.com/..."`
4. Link vuoto `""` = bottone "Acquista ora" rimanda al form preventivo
5. Opzionale: sostituisci `pk_live_DA_COMPLETARE` solo se usi Stripe Elements (non necessario con Payment Link)

### UX trust badge

- Link configurato → mostra "Acquista online (Stripe)"
- Link assente → mostra "Pagamento online disponibile su richiesta"

## Decisioni aperte (vedi colonna `note` nel CSV)

| Tema | Stato |
|------|-------|
| Go2 EDU+ sito → SMART vs ULTIMATE | SMART (€15.450) |
| G1 Base sito → G1 AIR | Confermato |
| H2 sul sito vs H1 nel listino | **H2 AIR/EDU pubblici** — H1 rimosso dal sito |
| G1-04 = typo G1-U4? | Segnalato in note |
| GO2W-U1 Gold €235 | Sospetto, non pubblicabile |
