# Changelog, direzione C "Nota a margine"

## v3.1 · 30/10/2026

Correzioni bloccanti di `03-reviews/finale.md` (sezione C) e nuova regola delle headline.

| Modifica | In risposta a |
|-|-|
| Totem: titolo sull'offerta, "Noleggia il G1 per una giornata, con un tecnico Abra al tuo stand."; la fonte delle risposte scende alla seconda riga ("Ogni risposta cita la fonte che hai approvato.") | Finale C1 |
| Totem: G1 a mezza figura portato alla stessa scala del totem, con quota 132 cm (continua nella parte visibile, tratteggiata in quella non mostrata) | Finale C2 |
| Nuove versioni `logotipo-24-48.svg` e `orizzontale-24-48.svg` con filo raddoppiato (34 unità), usate nella barra del sito, nelle intestazioni dei preventivi e sul fronte del biglietto | Finale C3 |
| Simbolo isolato (`simbolo.svg`, monogramma, favicon vettoriale): filo accorciato a 0,6 diametri del punto oltre la gamba destra, quindi dentro la grazia | Finale C3 |
| `favicon-16.svg`: filo di 2 px per i primi 3 px dopo il punto | Finale C4 |
| Evidenziatore: un solo Pantone, 395 C (3965 C scartato, più saturo e più verde). HEX `#EEE842` confermato fino alla prova colore; si riallinea se lo scarto supera dE 3. Dimensioni minime del simbolo in mm in `sistema-grafico.md` (6 mm in stampa, 10 mm come adesivo) | Finale C5 |
| Retro del biglietto: "Leggi i numeri del robot sul tuo caso prima dell'investimento: codice e manuale restano a te." Il filo del richiamo prosegue fino al testo | Finale C6 |
| Nuova regola delle headline: "Leggi" apre solo hero, copertina del preventivo e retro del biglietto. Post nominativo "Dai al tuo tesista un robot con mappa, simulatore e codice già nella cassa."; post anonimo "Ricevi il robot con mappa, simulatore e codice già pronti."; reel "Ascolta il G1 rispondere ai tuoi visitatori, con la fonte di ogni dato."; totem "Noleggia...". Nessuna coppia della serie apre con lo stesso verbo | Orchestratore, finale §6 |
| `voce.md`, `sistema-grafico.md`, `palette.md`, `presentazione.html`, `logo/test.html` aggiornati; tutti i PNG rigenerati; controllo copy, glifi, corpi minimi e SVG ripassati senza errori | Orchestratore |

## v3.0 · 29/10/2026

Risposta al round 2 (media 7,3; marchio 5,6) e alle indicazioni vincolanti di `03-reviews/round2-sintesi.md`.

### Marchio
| Modifica | In risposta a |
|-|-|
| Abbandonato il logotipo a dischi e aste della v2. Ritorno all'idea della v1, la lettera completata da un richiamo, dentro il serif scientifico del sistema | Orchestratore (segno "disco più asta" troppo elementare e staccato dal sistema); art director, strategia, marchio r2 |
| Logotipo "Abra" ridisegnato su STIX Two SemiBold: A senza traversa con punto (raggio 54) e filo sottile (17, rapporto 1 a 6,4) fino al bordo della grazia; r senza orecchio a goccia, con lo stesso punto e lo stesso filo; spaziatura propria (A b +34, b r -10, r a +10) | Orchestratore (logotipo su misura, non STIX composto); marchio r2 (punto della r come regola, stesso diametro) |
| Simbolo: la A annotata. Il filo è sottile e senza punta, il punto è l'elemento principale: lontano dalle A con freccia | Marchio r1 (Alpine), art director r2 (riportare il richiamo nel segno) |
| `favicon-16.svg` ridisegnato a pixel: A di 12 righe, punto 3 × 3, filo di 1 px che attraversa la gamba destra. Mostrato ingrandito in `logo/test.png` | Orchestratore (richiamo visibile a 16 px, favicon pixel per pixel) |
| Il descrittore "ROBOTICS" si omette sotto i 30 px: nell'intestazione del preventivo interno e sul fronte del biglietto si usa `logotipo.svg` | Produzione r2 (descrittore a 2,7 pt) |
| Animazione: la A sale dal basso tutta intera, con il richiamo; non compare mai senza traversa | Orchestratore r1 (A senza traversa vietata) |

### Produzione
| Modifica | In risposta a |
|-|-|
| `@media print` dichiara anche STIX Two Text Bold: niente grassetto sintetico né Type 3 | Produzione r2, orchestratore |
| Tolti ≤, ≥ e → (assenti in STIX Two Text): "fino a 15 s", "almeno 95%", "max 15 s", "Da rev 1.0 a rev 1.1". Tolta la freccia del flight case. Il segno di spunta "✓" (assente in entrambi i font) sostituito da una spunta disegnata in CSS. Verificata la copertura di tutti i caratteri visibili con i cmap di STIX e DM Mono | Produzione r2 (Georgia-Italic e Lucida nel PDF) |
| Richiami in apice a minimo 8 px (6 pt). Controllo automatico del corpo effettivo su preventivo e biglietto: nessun testo sotto 6 pt | Produzione r2, orchestratore |

### Headline con il verbo "Leggi"
| Applicazione | v3 |
|-|-|
| Hero | Leggi in tre settimane i numeri del robot sul tuo processo. |
| Preventivo | Prelievo dei cartoni a fine linea: leggi fase per fase tempi, errori e costi misurati |
| LinkedIn nominativo | Leggi cosa trova un tesista nella cassa del suo primo robot. |
| LinkedIn anonimo | Leggi cosa c'è nella cassa di un robot pronto dal primo giorno. |
| Reel | Leggi la fonte di ogni risposta che il G1 dà ai tuoi visitatori. |
| Totem | Leggi la fonte di ogni risposta del G1 al tuo stand. (riga sotto: Noleggio a giornata, con un tecnico Abra.) |

### Applicazioni
| File | Modifica | In risposta a |
|-|-|-|
| `linkedin-sacmi-anonimo` | Tolti "tesi in azienda", "tesista", "4D", "EDU", "Go2" nel testo; "quadrupede"; segnaposto dichiarato come "foto ufficiale del costruttore" | Orchestratore, strategia r2 |
| `reel-g1` | G1 a mezza figura ritagliato su fondo inchiostro (niente gradiente grigio), registro con la fonte, pubblico come dati nella pianta dello stand (un cerchio per visitatore, n = 9) | Orchestratore (pubblico e G1 diversi dalle altre direzioni); art director r2 |
| `totem` | Tolti il G1 su fondo grigio e le sagome sovrapposte; pianta dello stand con totem, G1, tecnico e visitatori come cerchi; G1 a mezza figura | Art director r2, orchestratore |
| `livrea` | Flight case ridisegnato come tavola tecnica a filo, con richiami solo su parti reali (maniglia, chiusura, tasca) | Orchestratore (flight case identico in tutte le direzioni) |
| `biglietto` | Retro: il filo del richiamo della A prosegue fino al testo; fronte con logotipo senza descrittore | Marchio, produzione |
| `palette.md` | Regola: giallo mai in bande, strisce oblique o triangoli | Marchio r2 (segnaletica di pericolo) |

### Documenti aggiornati
`concept.md`, `sistema-grafico.md` (Costruzione del marchio v3), `tipografia.md`, `palette.md`, `voce.md`, `motion.md`, `foto-video.md`, `autocritica.md`, `presentazione.html`. Tutti i PNG rigenerati.

## v2.0 · 28/10/2026

Risposta al round 1 (media 7,2; marchio 6,2) e alle indicazioni vincolanti di `03-reviews/round1-sintesi.md`.

### Marchio
| Modifica | In risposta a |
|-|-|
| Nuovo logotipo "abra" disegnato da zero con soli cerchi pieni e aste: ogni lettera è un punto con il suo filo. Abbandonata la A di STIX Two | Orchestratore §2 (logotipo ridisegnato, lavorare sull'intera parola); revisore marchio e art director (segno poco proprietario, logotipo = font composto) |
| Simbolo: la a da sola (punto, strozzatura, asta). Eliminata la A con linea orizzontale sporgente | Revisore marchio (vicinanza con Alpine e con le "A con freccia") |
| `favicon-16.svg` disegnato pixel per pixel, mostrato ingrandito 8x in `logo/test.png`; `favicon.svg` per 32 px e oltre | Orchestratore §2; revisori marchio, produzione e strategia (richiamo che sparisce a 16 px) |
| Lockup con "ROBOTICS" in DM Mono Medium convertito in tracciati, nuovo `logotipo.svg` solo nome | Revisore marchio (secondo dettaglio proprio nel logotipo) |
| Animazione rifatta: ogni lettera traccia il filo e riceve il punto. La "Λ" non compare più, nemmeno per un istante | Orchestratore §2 (A senza traversa vietata a qualunque dimensione) |
| Nessun `transform` residuo negli SVG del marchio | Revisore produzione |

### Colore
| Modifica | In risposta a |
|-|-|
| Evidenziatore da `#E9EC55` (fuori gamut, dE 12,4) a `#EEE842`, ritorno a schermo di CMYK 8 0 90 0; tinta piatta indicativa Pantone 395 C o 3965 C da scegliere su mazzetta | Revisore produzione (stampabilità); art director (giallo acido); orchestratore §4 |
| Tutti i CMYK ricalcolati con profilo dichiarato (Generic CMYK, intento colorimetrico relativo), scarti entro dE 1,8 | Revisore produzione; orchestratore §4 |
| Giallo confermato come colore firma esclusivo con l'inchiostro; esclusi gialli caldi e ocra | Orchestratore §1 |
| Attrezzature (etichetta di inventario, simbolo sul robot, scheda del flight case) su carta bianca: il giallo resta solo nel punto dei richiami adesivi | Revisore strategia (confusione con la segnaletica di sicurezza); revisore marchio (giallo e nero) |
| Numeri di riga ed etichette informative passati da grafite chiara (2,24:1) a grafite (5,76:1) | Revisore produzione; orchestratore §4 |

### Uso dell'evidenziatore e dei richiami
| Modifica | In risposta a |
|-|-|
| Evidenziatore tolto da tutti i titoli (hero, LinkedIn, totem, reel, presentazione). Ora solo su dati: "3 settimane" (hero), "≤ 15 s" (preventivo), "70%" (reel), "circa 2 ore" (totem) | Art director, panel acquirenti, orchestratore §6 |
| Richiami sulle foto solo su componenti fisici nominati: il LiDAR sulla testa del Go2. Simulatore, repository, manuale e limiti spostati in note numerate a margine | Art director (richiami decorativi su zampe e fianchi) |

### Applicazioni
| File | Modifica | In risposta a |
|-|-|-|
| `hero` | Headline propria: "Leggi i numeri del robot sul tuo caso prima di firmare l'ordine."; riga dedicata a università e laboratori (SDK, ROS 2, simulatore, manuale) | Orchestratore §3; panel acquirenti (laboratori non nominati) |
| `preventivo-cover` | Logo più grande, nessuna evidenziazione nella sintesi | Panel acquirenti (segno da ricordare dopo il PDF) |
| `preventivo-interna` | Didascalia corretta: "resta sopra la soglia di 15 s" | Panel acquirenti (ambiguità di "supera") |
| `linkedin-sacmi` | File marcato come bozza nel titolo; piede "Bozza: pubblicare solo con il consenso scritto di SACMI" | Art director, produzione, orchestratore §5 (consenso dichiarato falsamente) |
| `linkedin-sacmi-anonimo` | Tolti data, "questa settimana", revisione del manuale, "due tecnici", ore di assistenza; testo più corto e spazio ripristinato prima della figura | Revisore strategia, art director, orchestratore §5 |
| `reel-g1` | G1 in piedi a figura intera (immagine ufficiale diversa dal ritaglio accovacciato), pubblico in sagome grafiche, due battute leggibili in un secondo, fonte in una nota | Orchestratore §5; panel acquirenti; revisore strategia |
| `totem` | Stessa immagine del G1 in piedi in scala, sagome del pubblico, nota sul limite di batteria "circa 2 ore" marcata come valutazione interna | Orchestratore §5; revisore strategia |
| `biglietto` | Nessun testo sotto 6,1 pt (26 px a 12 px/mm), filetti 0,31 pt, retro con il nuovo simbolo | Revisore produzione; orchestratore §4 |
| `livrea` | Etichetta coerente con il robot mostrato (Go2-001), fondi bianchi, nessun punto giallo decorativo | Art director; revisore strategia |
| `presentazione` | Sezioni idea e marchio riscritte, importo "40.000 euro" tolto, contrasti aggiornati | Revisore strategia; nuovo marchio |

### Produzione
- Font statici ufficiali di STIX Two Text (Regular, SemiBold, Bold, Italic, release stixfonts v2.13) al posto del file variabile, dichiarati anche in `@media print`; DM Mono con fallback ttf. Nessun CDN. (Revisore produzione: 31 font Type 3 nel PDF; orchestratore §4.)
- Il simbolo non deriva più da STIX: decade il problema del Reserved Font Name sul marchio.

### Documenti aggiornati
`concept.md`, `palette.md`, `tipografia.md`, `sistema-grafico.md` (nuova sezione "Costruzione del marchio"), `voce.md` (headline proprie, headline eventi in inglese, registro breve per i social), `foto-video.md`, `motion.md`, `autocritica.md`.
