# Revisione di produzione, direzione D, round 1

Revisore: produzione e pre-press. Data: 27/10/2026. Materiale: `brand/03-reviews/_anon/D/`.

## Voti

| # | Criterio | Voto | Motivazione |
|-|-|-|-|
| 1 | SVG validi e puliti | 8 | 10 SVG del logo e 6 icone validi; niente `<text>`, `<image>`, font esterni, metadati, `transform`; geometria a rette, file piccoli. Manca un `favicon.svg`: il favicon è il monogramma 100x100 più due PNG. |
| 2 | Leggibilità piccola e monocromia | 8 | Il segno più robusto in piccolo: a 16 px la A piena e il pavimento giallo restano distinti; `simbolo-piccolo.svg` è una vera versione ottica. Mono positivo e negativo corretti. |
| 3 | Contrasti | 7 | I 12 rapporti dichiarati coincidono con il mio ricalcolo. In uso: Fumo `#6F645B` su Velluto 2,74:1 per le didascalie "Prima" e "Dopo" della presentazione (12 px). |
| 4 | Stampabilità | 5 | Biglietto con testo a 3,5 pt (`abrarobotics.com` sul retro) e 4,0 pt (riga del fronte). Velluto su grandi campiture (TAC 262%, dE di ritorno 5,1) è un colore da tinta piatta o da prova colore. PDF del preventivo con font Type 3. |
| 5 | Licenze | 9 | Archivo variabile locale con `OFL.txt`. |
| 6 | Completezza file | 8 | Tutti i deliverable presenti; manca `favicon.svg`; in `_lavoro/processo/` ci sono 9 PNG di prova che non servono alla consegna (cartella da 7,4 MB). |
| 7 | Presentazione senza errori | 9 | 12 pagine: zero errori, zero 404, zero richieste esterne. |

**Voto complessivo: 7,7**

## I 3 problemi più gravi

1. **Testo del biglietto a 3,5 e 4,0 pt.** `applicazioni/biglietto.html` (12 px = 1 mm): `.lbl` a 15 px = 3,5 pt sul retro, `.riga` a 17 px = 4,0 pt sul fronte, in maiuscolo spaziato. In stampa diventa una riga illeggibile, sul retro in Fumo su Carta.
2. **Velluto in grandi superfici.** Hero, post, totem, reel, flight case e fronte del biglietto sono campiture di `#3A1915`. Il CMYK dichiarato 35 85 80 60 torna `#45201D` (dE 4,4) e il ritorno dal gamut è dE 5,1: tra patinata e forex il bordeaux scuro oscilla tra marrone e nero. Serve un riferimento Pantone e una prova per supporto (forex, vinile, carta).
3. **PDF con font Type 3.** L'export offline di `preventivo-cover.html` incorpora Archivo come 26 font Type 3 e nessun TrueType: Chrome non incorpora il variabile come tale. Per il preventivo che il Company Brain manda ai clienti servono istanze statiche.

## Feedback azionabili

1. `applicazioni/biglietto.html`: `.retro .lbl` e `.fronte .riga` almeno a 26 px (6,1 pt); se la riga del fronte non entra, ridurla a "Robotica applicata".
2. `palette.md`: indicare un Pantone per Velluto e Luce, il TAC massimo ammesso per lo stampatore e il CMYK ricco calcolato con un profilo dichiarato; aggiungere il caso del forex del totem.
3. `font/`: aggiungere Archivo statico (Regular, SemiBold, ExtraBold, Condensed ExtraBold se usato) e dichiararlo in `sistema.css` per la stampa; ripetere l'export e verificare che i font risultino TrueType incorporati.
4. `logo/`: creare `favicon.svg` 32x32 dal monogramma con i dettagli ottici di `simbolo-piccolo.svg`, e puntarlo dai `<link rel="icon">`.
5. `presentazione.html`: le didascalie "Prima" e "Dopo" in Fumo su Velluto (2,74:1) vanno in Fumo chiaro `#B5A99C` (6,86:1). La stessa pagina ha un'etichetta "QUINTA" a 5 px: portarla almeno a 11 px.
6. `presentazione.html` copertina: compare "Il futuro in scena" come nome di lavoro; il brief lo ammette solo come nome interno, toglierlo dalla versione che va ai fondatori o marcarlo "nome di lavoro" in corpo minore.
7. Ripulire `_lavoro/processo/` prima della consegna finale, oppure spostarlo fuori dalla cartella della direzione.

## Controlli eseguiti (comandi)

- Validità SVG: `xmllint -noout` su `logo/*.svg` e `icone/*.svg` (16 file, 0 errori).
- Igiene logo: `grep -c` su `<text`, `<image`, font esterni, metadati, `transform=`, `viewBox`.
- Apertura pagine: `node brand/_tools/shot.js <file> brand/03-reviews/D/_prod/<nome>.png 1440 900 1` su 12 pagine: "nessun errore".
- Audit: `node _prod/strumenti/audit.js <cartella D> <out.json> .bv 12`. Dati in `_prod/audit-D.json`. L'audit segnala molti testi Velluto su Velluto (1,00:1) in hero, post, preventivo, reel e totem: sono falsi positivi, il fondo giallo è un elemento fratello con `clip-path`; sugli screenshot il testo è Velluto su Luce, 7,98:1. Anche "Contiene: robot" su Buio (1,13:1) nella livrea è su campitura Luce.
- Colore: `python3 _prod/strumenti/color.py colors.json` (Pillow ImageCms, `Generic CMYK Profile.icc`).
- PDF: `node _prod/strumenti/pdf.js` con rete bloccata; nel PDF 26 `/Subtype /Type3`, nessun TrueType.
- Piccolo formato: `_prod/piccolo-3x-pixel.png`.
- Copy: nessun em dash, en dash, doppio trattino o tilde nel testo visibile e nei `.md`; il post anonimo non contiene SACMI, Imola o ceramica.
- Screenshot guardati: `_prod/foglio-applicazioni-1.png`, `_prod/foglio-applicazioni-2.png`, `_prod/piccolo-3x-pixel.png`.
