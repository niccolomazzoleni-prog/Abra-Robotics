# Changelog direzione D, v2

Risposta alla sintesi del round 1 (`03-reviews/round1-sintesi.md`, media 6,4) e alle cinque review in `03-reviews/D/`.

## Marchio (revisore marchio 5,0; art director; strategia; indicazione 2 dell'orchestratore)

| Cosa è cambiato | In risposta a |
|-|-|
| Tolta la A maiuscola con il trapezio sotto la traversa. Nuovo logotipo "abra" minuscolo disegnato a mano: ogni occhiello è un arco scenico (tetto tondo, base piana), "a" e "b" speculari. Nessun font composto nel marchio. | Orchestratore 1 e 2 (figura sotto la traversa vietata, stessa costruzione di A; A isolata nel campo più affollato dei registri); marchio 1, 2, 3; art director 3 |
| Nuovo simbolo "ab", due portali affiancati: lavora sulla parola e non su una lettera sola, e dice il percorso "da a a b". | Orchestratore 2 (valutare monogramma sull'intera parola) |
| "Robotics" diventa un descrittore separato in Archivo Expanded, fuori dal marchio da depositare. | Marchio, feedback 3 |
| Favicon disegnata a pixel su griglia 16 (`favicon-16.png`, `favicon-32.png`, `favicon.svg`) e mostrata ingrandita 6 volte in `logo/test.png`; silhouette riconoscibile anche in monocromia. | Orchestratore 2; produzione 4 (manca favicon.svg) |
| SVG del logo senza `transform`, generati da geometria (shapely) e validati con xmllint. | Produzione 1 |

## Colore (art director 5 sul colore; orchestratore 1)

| Cosa è cambiato | In risposta a |
|-|-|
| Via Velluto, Luce, Stucco, Paglia, Rame. Nuovo colore firma Magenta di scena `#D6006F`, una gelatina teatrale non usata da A, B, C, E, con Grafite, Carta, Cemento come neutri freddi. | Orchestratore 1 (via ambra, ocra, bruno e rosso di B); art director e marchio (palette sovrapposta a B, associazione calcistica, effetto rétro) |
| CMYK ricalcolati con profilo ICC dichiarato, ritorno in sRGB, Pantone indicativi (226 C, 426 C), TAC della Grafite 280%. | Orchestratore 4; produzione 2 |
| Tabella contrasti nuova; nelle applicazioni nessuna coppia sotto AA (corretti i numeri magenta su Grafite del totem e un'etichetta su Cemento della livrea). | Orchestratore 4; produzione 3 |

## Tipografia e produzione

| Cosa è cambiato | In risposta a |
|-|-|
| Sei istanze statiche di Archivo in `font/` al posto del variabile; `sistema.css` le dichiara in locale; nessun CDN. | Orchestratore 4; produzione 3 (PDF con font Type 3) |
| Due registri: Archivo Bold 700 per documenti e sito, Condensed 800 solo per eventi e social. | Art director, feedback 7 |
| Biglietto con corpo minimo 6,2 pt (26 px a 12 px per mm). | Orchestratore 4; produzione 1 |
| Cartella `_lavoro/processo` eliminata; in `_lavoro/tools` restano solo gli script che generano marchio, favicon, post ed eventi. | Produzione 7 |

## Sistema grafico

| Cosa è cambiato | In risposta a |
|-|-|
| Tolti il cono di luce, il palco trapezoidale e il segno a T. Nuovi elementi: arco scenico (cornice delle immagini, magenta pieno solo nella scena) e pianta dei movimenti (fasi come posizioni su un percorso, da a a b). | Art director 1 e 2 (cono su otto formati, composizione unica); buyer panel 1; strategia 1 e 4 |
| Tolto il trattamento tungsteno seppiato: foto a colori naturali con ombra di contatto. | Buyer panel 2 |
| Icone ridisegnate con un solo punto magenta (la posizione "b"). | Coerenza con il nuovo sistema |

## Applicazioni

| File | Cosa è cambiato | In risposta a |
|-|-|-|
| `hero` | Fondo Carta, headline propria "Guarda il robot lavorare sul tuo caso, prima di investire.", ingresso per i laboratori (SDK, ROS 2, simulatore) e link dedicato, fasi come percorso, arco con il robot e il tragitto da a a b. | Orchestratore 3; strategia 1; buyer panel 4 |
| `preventivo-cover` | Registro sobrio: Carta, titolo all'imperativo "Misura il tempo ciclo dei vasetti a fine linea prima di investire", confronto spostato nel sottotitolo, cella cobot affidata a un integratore partner, fasi come pianta. | Strategia 2 e 3; buyer panel 1; orchestratore 6 |
| `preventivo-interna` | Nuovi colori e titoli, cella cobot con integratore partner, criteri su Rosa. | Strategia 3 |
| `linkedin-sacmi` | Fondo chiaro, robot appoggiato sul pavimento con ombra, bozza marcata "da pubblicare solo con consenso scritto". | Orchestratore 5; art director 6; buyer panel 1 |
| `linkedin-sacmi-anonima` | Senza data, revisione del manuale, ore di assistenza e luogo; elenco generalizzato. | Orchestratore 5; strategia 7; buyer panel 6 |
| `reel-g1` | Battuta senza contrapposizione («Va in lavastoviglie solo la griglia. Le mostro come si smonta?»), pubblico disegnato in scena, G1 in versione su colonna diversa dal ritaglio accovacciato, headline propria. | Orchestratore 5; art director 3; buyer panel 5 |
| `totem` | Pubblico disegnato nell'arco, QR vero verso abrarobotics.com/eventi, scala data da quote sottili al posto delle sagome grigie. | Art director 4; buyer panel 3 |
| `biglietto` | Registro sobrio su Carta, corpi da 6,2 pt in su, filo magenta. | Orchestratore 4 e 6 |
| `livrea` | Flight case Grafite con arco magenta, adesivo mostrato piano e posizione indicata sul robot senza prospettiva sbagliata, targa, dischi a terra "a" e "b". | Art director, slop su adesivo e Go2 sospeso |
| `scheda-laboratorio` (nuovo) | Scheda A4 del pacchetto per i tesisti con percorso di otto settimane. | Strategia 3 e 6 (manca un'applicazione per i laboratori) |

## Presentazione e documenti

- `presentazione.html` riscritta: nessun riferimento al nome di lavoro "Il futuro in scena" in copertina, didascalie con contrasto AA, nessun testo sotto 11 px nel disegno di costruzione. (Produzione 5 e 6; strategia 8)
- Aggiornati `concept.md`, `palette.md`, `tipografia.md`, `sistema-grafico.md`, `foto-video.md`, `motion.md`, `voce.md` e `autocritica.md`; animazione del logo nuova.
