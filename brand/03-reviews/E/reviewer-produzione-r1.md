# Revisione di produzione, direzione E, round 1

Revisore: produzione e pre-press. Data: 27/10/2026. Materiale: `brand/03-reviews/_anon/E/`.

## Voti

| # | Criterio | Voto | Motivazione |
|-|-|-|-|
| 1 | SVG validi e puliti | 8 | 10 SVG del logo e 6 icone validi; niente `<text>`, `<image>`, font esterni, metadati; un `transform` in `verticale.svg`. Il `viewBox` del simbolo ha un margine molto ampio (1166 unità per un segno largo 955), che rimpicciolisce la A quando si usa il file così com'è. |
| 2 | Leggibilità piccola e monocromia | 7 | `favicon-16.svg` è una buona versione ottica. `simbolo.svg` e `monogramma.svg` a 16 px diventano una A sottile con trattini spezzati, il filo si legge come rumore. Mono positivo e negativo corretti. |
| 3 | Contrasti | 7 | I 15 rapporti dichiarati coincidono con il mio ricalcolo. In uso: Grafite `#62666A` su Flanella 2,20:1 per le didascalie dei segnaposto (reel 13 px, totem 7,5 px) e Grafite su `#E2DACA` 4,17:1 per le etichette delle tavole. |
| 4 | Stampabilità | 5 | Biglietto con etichette a 3,5 pt (MAIL, TEL, WEB) e righello a 0,26 pt, al limite. I CMYK dichiarati della Flanella (15 7 0 78, solo nero) e del Giallo metro tornano lontani dagli HEX (dE 9,7 e 14,1); il Giallo è al bordo del gamut (dE 6,7). PDF con font Type 3. |
| 5 | Licenze | 9 | Bricolage Grotesque variabile locale con `OFL.txt`. |
| 6 | Completezza file | 8 | Tutti i deliverable presenti; `hero.html` e le applicazioni non dichiarano il favicon, che invece è previsto. |
| 7 | Presentazione senza errori | 9 | 12 pagine: zero errori, zero 404, zero richieste esterne. Un elemento `.metro-wrap` della presentazione taglia il numero "140" del metro. |

**Voto complessivo: 7,6**

## I 3 problemi più gravi

1. **Biglietto a 3,5 pt.** `applicazioni/biglietto.html` (12 px = 1 mm, poi `scale(.62)` solo per la vista): `.contatti span` a 15 px = 3,5 pt, in maiuscolo spaziato e condensato al 75%. Il righello del retro ha tacche a 0,26 pt: al limite della stampa offset, sotto il limite della stampa digitale su carta naturale.
2. **CMYK dichiarati incoerenti con gli HEX.** Flanella `#2F3337` dichiarata 15 7 0 78 (conversione a solo nero) torna `#41484E`, un grigio azzurro (dE 9,7); Giallo metro 0 21 82 5 torna `#EBBD4E` (dE 14,1). Il Pantone 123 C citato per il giallo è più arancio del `#F2BF2C` di schermo: va verificato su mazzetta.
3. **Grafite su Flanella.** 2,20:1 per tutte le didascalie su fondo scuro (`reel-g1.html`, `totem.html`); sul totem la didascalia è anche a 7,5 px. Il sistema dichiara Grafite solo su fondi chiari, le applicazioni la usano anche su scuro.

## Feedback azionabili

1. `applicazioni/biglietto.html`: `.contatti span` da 15 a 26 px con `font-stretch` 86% invece di 75%; tacche del righello da 0,26 a almeno 0,35 pt (stroke 1,5 px a scala 12).
2. `palette.md`: rifare i CMYK con un profilo dichiarato (FOGRA39 o FOGRA29), costruire la Flanella come nero ricco a quattro colori, scegliere il Pantone del giallo confrontando 123 C, 7408 C e 116 C con il `#F2BF2C`.
3. `assets/sistema.css` e applicazioni scure: per le didascalie su Flanella usare Carta modello `#D9CBAA` (7,93:1) o Gesso; vietare in `palette.md` la coppia Grafite su Flanella (2,20:1).
4. `logo/simbolo.svg` e `monogramma.svg`: ridurre il `viewBox` all'area di rispetto dichiarata e scrivere in `sistema-grafico.md` "sotto 24 px solo `favicon-16.svg`".
5. `fonts/`: aggiungere istanze statiche di Bricolage Grotesque per i pesi usati nel preventivo; l'export PDF offline oggi produce 17 font Type 3 e nessun TrueType.
6. Aggiungere `<link rel="icon" href="../logo/favicon-16.svg">` a `applicazioni/hero.html`, così il mockup del sito mostra il favicon nella scheda.
7. `presentazione.html`: allargare `.metro-wrap` o togliere `overflow:hidden`, il numero 140 del metro risulta tagliato.

## Controlli eseguiti (comandi)

- Validità SVG: `xmllint -noout` su `logo/*.svg` e `icone/*.svg` (16 file, 0 errori).
- Igiene logo: `grep -c` su `<text`, `<image`, font esterni, metadati, `transform=`, `viewBox`.
- Apertura pagine: `node brand/_tools/shot.js <file> brand/03-reviews/E/_prod/<nome>.png 1440 900 1` su 12 pagine: "nessun errore".
- Audit: `node _prod/strumenti/audit.js <cartella E> <out.json> .lato 12` (la scala di vista `.62` è compensata nel calcolo dei pt). Dati in `_prod/audit-E.json`.
- Colore: `python3 _prod/strumenti/color.py colors.json` (Pillow ImageCms, `Generic CMYK Profile.icc`).
- PDF: `node _prod/strumenti/pdf.js` con rete bloccata; nel PDF 17 `/Subtype /Type3`, nessun TrueType.
- Piccolo formato: `_prod/piccolo-3x-pixel.png`.
- Copy: nessun em dash, en dash, doppio trattino o tilde nel testo visibile e nei `.md`; il post anonimo non contiene SACMI, Imola o ceramica.
- Screenshot guardati: `_prod/foglio-applicazioni-1.png`, `_prod/foglio-applicazioni-2.png`, `_prod/piccolo-3x-pixel.png`.
