# Revisione di produzione, direzione E, round 2

Revisore: produzione e pre-press. Materiale: `brand/03-reviews/_anon/E/` alla v2 (`changelog.md` letto). Artefatti in `brand/03-reviews/E/_prod/r2/`.

## Voti

| # | Criterio | r1 | r2 | Motivazione r2 |
|-|-|-|-|-|
| 1 | SVG validi e puliti | 8 | 9 | 17 SVG validi; nessun `<text>`, `<image>`, font esterno, metadato o `transform`; `viewBox` dei simboli ridotti all'area di rispetto. |
| 2 | Leggibilità piccola e monocromia | 7 | 8 | La A con traversa piena regge a 16 px; `favicon-16.svg` e `favicon-16-mono.svg` disegnati a pixel. Il filo in gesso blu del `simbolo-negativo.svg` a 16 px è un pixel chiaro appena visibile, accettabile. |
| 3 | Contrasti | 7 | 8 | I 12 rapporti dichiarati coincidono con il mio ricalcolo; Grafite su Flanella ora vietata e non più usata. Resta Grafite `#62666A` sul fondo tavola `#E2DACA` a 4,17:1 nelle didascalie di `biglietto.html` e `totem.html` (12 e 13 px). |
| 4 | Stampabilità | 5 | 8 | Biglietto 6,14 pt minimo e tacche del righello 0,36 pt; CMYK ricalcolati con profilo dichiarato (dE da 0,4 a 1,0 sui neutri), Flanella come nero ricco; Gesso blu fuori gamut (dE 7,3) e Blu segno (dE 4,5) dichiarati con Pantone indicativi. PDF con soli TrueType. |
| 5 | Licenze | 9 | 9 | Sei istanze statiche di Bricolage Grotesque rinominate "Bricolage Grotesque Abra", con `OFL.txt`. Bricolage non dichiara Reserved Font Name, quindi la ridenominazione è corretta. |
| 6 | Completezza file | 8 | 9 | Favicon collegato a `hero.html`, versione mono del favicon aggiunta. |
| 7 | Presentazione senza errori | 9 | 9 | 12 pagine: zero errori, zero 404, zero richieste esterne; il metro tagliato della presentazione è stato tolto. |

**Voto complessivo r2: 8,6** (r1: 7,6)

## Problemi residui

1. **Gesso blu in stampa.** Colore firma fuori dal gamut di quadricromia: il CMYK 40 22 1 0 torna `#90AACC`, più grigio. Fascia del totem, cartellini del flight case e righello del biglietto lo usano in campitura: rendere vincolante il Pantone (2717 C o 658 C da scegliere) per questi supporti e chiedere la prova su forex.
2. **Didascalie di tavola a 4,17:1.** `applicazioni/biglietto.html` e `totem.html`: `body` su `#E2DACA` con didascalie in Grafite. Sono testi della tavola di presentazione, non del supporto stampato, ma il fondo `#E2DACA` non è in palette: usare Tela `#ECE6D8` (4,65:1) oppure Flanella.
3. **File variabile ancora in `fonts/`.** `BricolageGrotesque-VF.ttf` resta accanto alle istanze statiche: nessuna pagina lo carica, ma se il Company Brain lo usa per errore il PDF torna a Type 3. Spostarlo in `_lavoro/`.

## Controlli eseguiti (comandi)

- `xmllint -noout` su `logo/*.svg` e `icone/*.svg`: 17 file, 0 errori. Igiene con `grep -c` su `<text`, `<image`, font esterni, metadati, `transform=`, `viewBox`.
- `node brand/_tools/shot.js <file> brand/03-reviews/E/_prod/r2/<nome>.png 1440 900 1` su 12 pagine: "nessun errore".
- `node r2/strumenti/audit.js <cartella E> r2/audit-E.json .lato 12` (scala di vista 0,62 compensata). I due 1,00:1 su reel e totem sono falsi positivi: la didascalia del segnaposto sta sul pannello Carta modello, fratello del contenitore scuro.
- `python3 r2/strumenti/color.py r2/strumenti/colors2.json` (`r2/colore.txt`).
- `node r2/strumenti/pdf2.js` con rete bloccata: preventivo copertina e interna con sei e quattro istanze Bricolage Grotesque Abra, tutte `FontFile2`, zero Type 3.
- Piccolo formato: `r2/piccolo-3x-pixel.png`.
- Copy: zero em dash, en dash, doppi trattini o tilde; il post anonimo non contiene SACMI, Imola o ceramica.
- Screenshot guardati: `r2/foglio-applicazioni-1.png`, `r2/foglio-applicazioni-2.png`, `r2/piccolo-3x-pixel.png`.
