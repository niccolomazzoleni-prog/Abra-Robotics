# Preventivi (solo locale)

Questa cartella **non è più pubblicata** su GitHub / GitHub Pages (vedi `.gitignore`).

I file HTML/PDF dei preventivi restano **sul tuo PC** in questa directory. Il sito pubblico continua a funzionare con:

- editor: [`../offerta.html`](../offerta.html)
- listino End-User: `../../listini/pubblico/end-user.json`

## Dove tenere traccia

| Cosa | Dove |
|------|------|
| Preventivi HTML/PDF | Questa cartella (locale) e/o Drive/OneDrive |
| Listini FOB / Gold / margini | `listini/interno/` (già ignorata da git) |
| Backup versione | Opzionale: **seconda repo GitHub privata** solo per `samples/` + `listini/interno/` + `admin/` |

Non ricommittare preventivi nominativi (SACMI, Nexsoft, Marchesini, …) sulla repo del sito pubblico.

## Offerte pronte (locale)

| File | Contenuto |
|------|-----------|
| `Preventivo-H2-Base-assistenza-6m.pdf` | H2 Base + assistenza 6 mesi · € 45.318,34 |
| `Preventivo-Marchesini-AS2-Go2-G1U2.pdf` | Marchesini · AS2 / Go2 / G1-U2 |
| HTML omonimi `.html` | Sorgenti editabili |

Copia anche sul Desktop. Rigenera:

```powershell
python -m http.server 8765
# altro terminale, dalla root repo:
node offerte-ai/samples/_export-offers-pdf.mjs
```
