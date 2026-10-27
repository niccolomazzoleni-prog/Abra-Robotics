# Revisione di produzione, direzione C, round 2

Revisore: produzione e pre-press. Materiale: `brand/03-reviews/_anon/C/` alla v2 (`changelog.md` letto). Artefatti in `brand/03-reviews/C/_prod/r2/`.

## Voti

| # | Criterio | r1 | r2 | Motivazione r2 |
|-|-|-|-|-|
| 1 | SVG validi e puliti | 8 | 9 | 15 SVG validi; nessun `<text>`, `<image>`, font esterno, metadato; tolto il `transform` di `verticale.svg`; marchio costruito con soli cerchi e aste, non più dal glifo STIX. |
| 2 | Leggibilità piccola e monocromia | 6 | 7 | `favicon-16.svg` a pixel si legge come "a"; il simbolo pieno a 16 px è una macchia con asta. Il descrittore "ROBOTICS" è alto il 23% del lockup: nell'intestazione di `preventivo-interna.html` (lockup 15,9 px) le maiuscole sono 3,7 px, cioè 2,7 pt in stampa, illeggibili. |
| 3 | Contrasti | 7 | 9 | I 11 rapporti dichiarati coincidono con il mio ricalcolo; numeri di riga ed etichette passati a Grafite. Nelle applicazioni nessun testo sotto AA (l'unico 1,00:1 sul totem è il falso positivo del testo ruotato, verificato a occhio). |
| 4 | Stampabilità | 5 | 6 | Risolti biglietto (6,14 pt, filetti 0,47 pt) ed evidenziatore: il CMYK 8 0 90 0 riconvertito dà esattamente `#EEE842`, quindi il colore è riproducibile. Restano nel PDF del preventivo un font di sistema e font Type 3 (vedi problemi), richiami in apice a 3,5 e 4,0 pt e il descrittore a 2,7 pt. |
| 5 | Licenze | 8 | 7 | Font OFL locali e statici, simbolo non più derivato da STIX. Però il PDF di `preventivo-interna` incorpora `Georgia-Italic`, font di sistema Apple non ridistribuibile: è lo stesso difetto che in r1 avevo segnalato a un'altra direzione. |
| 6 | Completezza file | 9 | 9 | Tutti i deliverable, più `favicon-16.svg` e `logotipo.svg`. |
| 7 | Presentazione senza errori | 9 | 9 | 12 pagine: zero errori, zero 404, zero richieste esterne. |

**Voto complessivo r2: 8,0** (r1: 7,4)

## Problemi residui

1. **Glifi mancanti in STIX Two Text.** `preventivo-interna.html` usa "≤" (3 volte), "≥" e "→". STIX Two Text non li contiene: con la rete bloccata Chrome ripiega su Georgia (td.c, span.evid "Tempo ciclo simulato ≤ 15 s") e su Lucida Grande (aside.margine, div.nt), e Georgia-Italic finisce incorporato nel PDF. Rilevato con `CSS.getPlatformFontsForNode` (`r2/strumenti/platfonts.js`). Correzione: scrivere "fino a 15 s", "almeno", oppure aggiungere STIX Two Math (OFL) solo per quei caratteri con `unicode-range`.
2. **Grassetto sintetico in stampa.** In `abra-c.css` il blocco `@media print` dichiara STIX Regular, SemiBold e Italic ma non il Bold 700. Il testo a 700 in stampa viene ingrossato da Chrome e esportato come Type 3: 3 font Type 3 nella copertina, 1 nell'interna. Aggiungere la riga `@font-face` del Bold anche lì.
3. **Corpi minimi nel preventivo.** Descrittore "ROBOTICS" a 2,7 pt nell'intestazione interna e 5,9 pt in copertina; richiami in apice `sup.rif` a 3,5 e 4,0 pt. Portare il lockup dell'intestazione ad almeno 26 px oppure usare `logotipo.svg` senza descrittore sotto i 30 px, e i richiami a 8 px (6 pt).

## Controlli eseguiti (comandi)

- `xmllint -noout` su `logo/*.svg` e `icone/*.svg`: 15 file, 0 errori. Igiene con `grep -c` su `<text`, `<image`, font esterni, metadati, `transform=`, `viewBox`.
- `node brand/_tools/shot.js <file> brand/03-reviews/C/_prod/r2/<nome>.png 1440 900 1` su 12 pagine: "nessun errore".
- `node r2/strumenti/audit.js <cartella C> r2/audit-C.json .card 12`.
- `node r2/strumenti/small-text.js 8 <preventivi>`: elenco dei testi sotto 6 pt nelle pagine A4.
- `python3 r2/strumenti/color.py r2/strumenti/colors2.json` (`r2/colore.txt`). Nota: il giro HEX, CMYK, HEX dell'evidenziatore dà dE 10,2 per un limite della tabella inversa del profilo; la conversione diretta del CMYK dichiarato restituisce `#EEE842` con dE 0,0, che è il dato che conta.
- `node r2/strumenti/pdf2.js` con rete bloccata: copertina con DMMono, STIXTwoText Regular, SemiBold, Italic e 3 Type 3; interna con in più `Georgia-Italic` e 1 Type 3.
- `node r2/strumenti/platfonts.js` e `combos.js`: font di piattaforma per nodo e combinazioni peso e stile contro i font caricati.
- `node r2/strumenti/logoh.js` e `bbox.js`: altezza del lockup nelle pagine e proporzione del descrittore (37 su 161 unità).
- Piccolo formato: `r2/piccolo-3x-pixel.png`.
- Copy: zero em dash, en dash, doppi trattini o tilde; il post anonimo non contiene SACMI, Imola o ceramica; la versione nominativa ora dice "Bozza: pubblicare solo con il consenso scritto di SACMI".
- Screenshot guardati: `r2/foglio-applicazioni-1.png`, `r2/foglio-applicazioni-2.png`, `r2/preventivo-interna-offline.png`.
