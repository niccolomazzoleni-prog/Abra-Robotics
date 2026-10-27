# Changelog. Territorio B, da v1 a v2

Round 1: media 6,6 (strategia 7,2; art director 5,9; produzione 6,7; buyer panel 7,0; marchio 6,2). Indicazioni vincolanti in `03-reviews/round1-sintesi.md`; review in `03-reviews/B/*-r1.md`.

## Direzione e nome

| Cambio | In risposta a |
|-|-|
| Nome da "Misura d'uomo" a "Montato a vista"; l'idea passa dalla misura umana alla sincerità costruttiva (si vede come è fatto il lavoro prima di firmare) | Strategia, problema 3: la linea umanista confinava con il vicino verbale vietato "robot per le persone" |
| Abbandonato il kit di forme (disco, arco, asta) come decorazione e come fondale; il sistema ora è fatto di pannelli rettangolari separati da un giunto costante | Sintesi, divieto per B "kit geometrico da Bauhaus da startup"; art director, problemi 1 e 2; buyer panel, problema 1 |

## Marchio

| Cambio | In risposta a |
|-|-|
| Nuovo logotipo "abra" disegnato a mano: b e r chiuse, le due a con la pancia staccata dall'asta (giunto 16 su 240, 6,7% dell'altezza x). Il tratto distintivo sta nella forma e regge in monocromia | Sintesi punto 2 (logotipo ridisegnato, lavorare sulla parola intera); marchio, problema 1 e feedback 1 e 3 |
| Marchio a un solo colore (Rosso Abra); niente più tre colori nel simbolo | Marchio: "il segno vive del colore"; art director: arco ocra illeggibile in piccolo |
| "Robotics" in Instrument Sans Bold con altezza x al 46% di quella di "abra"; regola: sotto i 160 px di larghezza solo il logotipo | Art director, feedback 2; produzione, feedback 2 |
| Favicon disegnata pixel per pixel a 16 px (`favicon.svg`) e a 32 px (`favicon-32.svg`), con il giunto di un pixel; confronto v1 e v2 ingrandito in `logo/test.html` | Sintesi punto 2; art director, feedback 1; strategia, feedback 2; produzione, feedback 3 |
| Nuovi file: `simbolo-negativo.svg`, `favicon-32.svg`; tutti gli SVG rigenerati e validati | Completezza |
| Logo animato rifatto: la pancia si ferma prima dell'asta, il giunto resta aperto | Coerenza con il nuovo segno |

## Colore

| Cambio | In risposta a |
|-|-|
| Colore firma esclusivo Rosso Abra con ocra; tolti verderame, avorio caldo e inchiostro bruno; aggiunti Grafite neutra, Grigio Lettera e Carta fredda | Sintesi punto 1 (colore firma, divieto del bruno tipo velluto); art director: palette quasi identica a D |
| Rosso usato in un solo pannello per superficie; nelle pagine contrattuali solo nel marchio e nei filetti | Strategia, feedback 8; buyer panel, problema 1 |
| CMYK ricalcolati con profilo dichiarato, Pantone indicativi per rosso e ocra, rosso scuro eliminato (fuori gamut) | Produzione, problema 3 e feedback 5; sintesi punto 4 |
| Contrasti rifatti; didascalie su pannelli grigi passate a grafite; nessuna coppia sotto AA nelle applicazioni | Produzione, punto 3 e feedback 6; sintesi punto 4 |

## Tipografia

| Cambio | In risposta a |
|-|-|
| Font in locale e statici in `fonts/` con licenze OFL: Instrument Sans (titoli, dati) e Crimson Pro (testo). Nessuna richiesta a Google Fonts in tutte le pagine | Sintesi punto 4; produzione, problema 1 e feedback 1 |
| PDF del preventivo esportati senza rete (`applicazioni/preventivo-cover.pdf`, `preventivo-interna.pdf`): incorporano solo InstrumentSans e CrimsonPro | Produzione, problema 1 |
| Tolti ≤ e ≥, non presenti nel font, per evitare la sostituzione con Helvetica nel PDF | Verifica del PDF offline |
| Eliminato il corsivo rosso finale in ogni titolo; titoli in tondo | Sintesi punto 6; art director, problema tipografico e feedback 3; buyer panel, feedback 4 |

## Applicazioni

| File | Cambio | In risposta a |
|-|-|-|
| `hero` | Titolo proprio: "Guarda il robot lavorare nel tuo reparto prima di firmare l'ordine."; G1 in piedi (nuovo ritaglio da `unitree-g1-03.webp`), cartellino con altezza, massa, carico e batteria marcati "Esempio"; pannello rosso per la manifattura; pulsanti rettangolari grafite, senza pallino | Sintesi punti 3 e 5; buyer panel, feedback 5; strategia, feedback 3; art director, feedback 8 |
| `preventivo-cover` | Metà alta con "Cosa sapete prima di investire" e "Cosa vi resta in mano", dati del progetto e sequenza P0 a P5 | Strategia, feedback 5; buyer panel, feedback 1 |
| `preventivo-interna` | Titolo in tondo, filetto della fase, riga delle firme di chiusura | Buyer panel, feedback 4 |
| `linkedin-sacmi` | Robot su pannello neutro con cartellino delle dimensioni; nessuna forma decorativa; fascia "Da pubblicare solo con consenso scritto di SACMI" | Art director, feedback 6; buyer panel, feedback 2; sintesi punto 5 |
| `linkedin-sacmi-anonimo` | Tolti data, revisione del manuale, MuJoCo e modello del robot; azienda descritta per settore | Strategia, feedback 6; sintesi punto 5 |
| `reel-g1` | Tolti gli archi sonori; scena con pubblico e tecnico in sagoma; dialogo con domanda, risposta e fonte approvata | Art director, feedback 4; buyer panel, feedback 3; sintesi punto 5 |
| `totem` | Totem rettangolare a tre pannelli nella scena dell'evento, in scala, con persone in sagoma | Sintesi punto 5 |
| `biglietto` | Corpo minimo 17 px a 8 px/mm, cioè 6 pt; titolo proprio sul retro | Produzione, problema 3 e feedback 4; sintesi punto 4 |
| `livrea` | Adesivo piatto in posizione quotata su un disegno dall'alto del Go2, lontano dalla marcatura del produttore; flight case senza forme decorative | Art director, feedback 5 |
| `icone/` | Ridisegnate a tratto; tolte le onde sonore | Art director, slop |
| `assets/` | Segnaposto in grigio neutro al posto della bicromia seppia; nuovo G1 in piedi; rimosso il G1 accovacciato | Strategia, feedback 7; sintesi punto 5 |

## Documenti

`concept.md`, `palette.md`, `tipografia.md`, `sistema-grafico.md`, `foto-video.md`, `motion.md`, `voce.md` (regola di confine sul lessico umanista, headline proprie), `autocritica.md`, `presentazione.html` riscritti per la v2. `_strumenti/` contiene i generatori v2 (logotipo, testo in tracciati, sagome, verifica PDF).
