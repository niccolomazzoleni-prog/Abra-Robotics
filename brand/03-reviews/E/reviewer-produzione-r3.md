# Revisione di produzione, direzione E, round 3

Revisore: produzione e pre-press. Materiale: `brand/03-reviews/_anon/E/` alla v3 (`changelog.md` letto). Artefatti in `brand/03-reviews/E/_prod/r3/`.

## Voti

| # | Criterio | r1 | r2 | r3 | Motivazione r3 |
|-|-|-|-|-|-|
| 1 | SVG validi e puliti | 8 | 9 | 9 | 17 SVG validi; nessun `<text>`, `<image>`, font esterno, metadato o `transform`. Simbolo e monogramma pesano 11 a 12 KB per un segno semplice: tracciati molto suddivisi, da semplificare ma non un difetto. |
| 2 | Leggibilità piccola e monocromia | 7 | 8 | 8 | `favicon-16.svg` e la versione mono si leggono "ab"; la tacca a V in cima a 16 px sembra due orecchie. Il simbolo pieno a 16 px è affollato: la regola "sotto 24 px solo favicon" va mantenuta. |
| 3 | Contrasti | 7 | 8 | 9 | 12 rapporti dichiarati identici al mio ricalcolo; le didascalie su `#E2DACA` sono sparite. I casi segnalati dall'audit nell'hero (testo chiaro e gesso blu) sono falsi positivi: la colonna flanella è un elemento fratello; sullo screenshot il gesso blu sta su flanella, 6,13:1. |
| 4 | Stampabilità | 5 | 8 | 8 | Biglietto a 6,14 pt e tacche 0,36 pt; preventivi senza testo sotto 6 pt; Gesso blu fuori gamut (dE 8,3) ma con Pantone 278 C vincolante, il cui riferimento sRGB coincide con l'HEX (dE 0,0). |
| 5 | Licenze | 9 | 9 | 9 | Istanze statiche rinominate "Bricolage Grotesque Abra" con OFL; il file variabile è uscito da `fonts/`. |
| 6 | Completezza file | 8 | 9 | 9 | Tutti i deliverable, 9 documenti, 6 icone, favicon colore e mono. |
| 7 | Presentazione senza errori | 9 | 9 | 9 | 12 pagine: zero errori, zero 404, zero richieste esterne, nessun testo tagliato. |

**Voto complessivo r3: 8,7** (r1: 7,6; r2: 8,6)

## Problemi residui

1. **Blu segno e Flanella rispetto ai Pantone indicati.** Blu segno `#3D5A99` contro 7684 C: dE 3,4, accettabile. Flanella `#2F3337` contro 432 C: dE 6,8 (il 432 C è più bluastro). La flanella copre il 40% del sistema, comprese le casse: se si stampa in tinta piatta va scelto un grigio più vicino, altrimenti tenere il nero ricco 81 72 63 40 con prova colore.
2. **Simbolo a 16 px.** La tacca a V di 2 px sopra l'asta si legge come due orecchie; valutare una tacca di un solo pixel nel favicon, oppure toglierla sotto i 24 px.
3. **Peso dei tracciati.** `simbolo.svg` (11,8 KB) e `logotipo-abra.svg` (21,5 KB) hanno archi spezzati in molti segmenti: per l'incisione laser e il plotter da taglio del vinile conviene una versione semplificata con meno nodi.

## Controlli eseguiti (comandi)

- `xmllint -noout` su `logo/*.svg` e `icone/*.svg`: 17 file, 0 errori. Igiene con `grep -c` su `<text`, `<image`, font esterni, metadati, `transform=`, `viewBox`.
- `node brand/_tools/shot.js <file> brand/03-reviews/E/_prod/r3/<nome>.png 1440 900 1` su 12 pagine: "nessun errore".
- `node r3/strumenti/audit3.js <cartella E> r3/audit-E.json .lato 12` (scala di vista compensata). Falsi positivi dell'hero, del reel e del totem verificati sugli screenshot.
- `node r3/strumenti/small-text.js 8 <preventivi>`: nessun testo sotto 6 pt.
- `node r3/strumenti/pdf3.js` con rete bloccata: sei e quattro istanze Bricolage Grotesque Abra, tutte `FontFile2`, zero Type 3; `platfonts.js`: nessun font di sistema.
- `python3 r3/strumenti/color.py r3/strumenti/colors3.json` e confronto Pantone (`r3/strumenti/pantone3.out`; riferimenti sRGB comunemente pubblicati, da confermare su mazzetta).
- Piccolo formato: `r3/piccolo-3x-pixel.png`.
- Copy: zero em dash, en dash, doppi trattini o tilde; il post anonimo non contiene SACMI, Imola o ceramica.
- Screenshot guardati: `r3/foglio-applicazioni-1.png`, `r3/foglio-applicazioni-2.png`, `r3/piccolo-3x-pixel.png`.
