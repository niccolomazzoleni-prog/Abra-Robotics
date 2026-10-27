# Changelog, direzione C "Nota a margine"

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
