# Changelog: Cartamodello

## v2, 27/10/2026

Risposta al round 1 (media 6,6; marchio 5,4). Fonti: `brand/03-reviews/round1-sintesi.md` (indicazioni vincolanti dell'orchestratore) e le cinque review in `brand/03-reviews/E/`.

### Marchio
| Modifica | In risposta a |
|-|-|
| La A ha ora una **traversa piena e inclinata di 9 gradi**, visibile a ogni dimensione; la "Λ" della v1 è eliminata | Sintesi §2 (vietata la A senza traversa); art director punto 1; marchio problemi 1 e 2; strategia punto 1 |
| Il tratteggio del simbolo è sostituito da **un solo filo che esce dalla gamba destra**, in gesso blu nelle versioni a colori; l'inclinazione resta per allontanarsi dallo schema Alpine | Marchio feedback 1, 2 e 3; art director "mezzeria stradale" |
| **"bra" disegnate a mano** con superellissi; b e a sono lo stesso pezzo specchiato. Il logotipo non usa più Bricolage, salvo il descrittore "Robotics" | Messaggio dell'orchestratore; sintesi §2 (logotipo ridisegnato); marchio problema 3 |
| **Favicon 16 px ridisegnato pixel per pixel** (traversa su righe intere, filo di 2 pixel) e nuova versione monocroma; mostrati ingranditi x8 in `logo/test.png` | Sintesi §2; produzione punto 2 e feedback 4; marchio feedback 2 |
| `monogramma.svg` ingrossato per 24 a 64 px; regola "sotto 24 px solo favicon-16" | Produzione feedback 4 |
| `viewBox` dei simboli ridotti all'area di rispetto (40 unità) | Produzione criterio 1 |
| Verticale: "Robotics" composto con spaziatura normale e allineato a sinistra | Art director feedback 3; marchio feedback 4 |
| Logo animato rifatto: la traversa si cuce piena, il filo esce e rientra prima delle lettere | Coerenza con il nuovo segno |

### Colore
| Modifica | In risposta a |
|-|-|
| **Giallo eliminato.** Nuovo colore firma: **gesso da sarto blu** `#8FB0E0`, con il Blu segno `#2F5D9E` per le linee su fondo chiaro | Sintesi §1 (colore firma esclusivo, divieto di giallo); art director e strategia (segnaletica di cantiere) |
| CMYK ricalcolati con profilo ICC dichiarato, scarto dE indicato; Flanella come nero ricco; Pantone indicativi per i colori fuori gamut | Sintesi §4; produzione feedback 2 |
| Grafite su Flanella vietata; didascalie su fondo scuro in Gesso o Gesso blu; Esempio su carta in Flanella | Produzione problema 3 |

### Sistema
| Modifica | In risposta a |
|-|-|
| **Tratteggio eliminato ovunque** (marchio, bottoni, fasi, cornici, icone). Nuova regola: "in gesso" (bordo blu sottile) = da approvare; "cucito" (flanella piena) = firmato | Sintesi §1 (vietato il tratteggio da mezzeria); art director punti 5 e 7 |
| Il **metro misura sempre qualcosa di vero**: tacca dello zero allineata con precisione, G1 da 0 a 130 cm dai piedi alla testa, settimane del preventivo coerenti con la tabella, millimetri reali sul biglietto. Tolto dove era decorazione (copertina della presentazione, post LinkedIn) | Messaggio dell'orchestratore; art director (righello a 60 contro 70 cm); buyer panel feedback 5 |
| Frecce di drittofilo, margini tratteggiati e filo diagonale decorativo eliminati | Art director problema 3 |
| Font in **sei istanze statiche TrueType** locali; PDF del preventivo verificato senza font Type 3 | Sintesi §4; produzione feedback 5 |
| Titoli a peso 640 e larghezza 94, meno condensati | Art director feedback 8; strategia feedback 6 |
| Icone senza tratteggio | Coerenza con la nuova regola |

### Copy
| Modifica | In risposta a |
|-|-|
| Fasi con **nomi del settore** nei testi per i clienti: Sopralluogo e assessment, Simulazione, Prova sul robot, Pilota, Consegna. "Imbastitura", "cartamodello" e "pezzo di carta" restano nella logica interna | Messaggio dell'orchestratore; sintesi §6 E; buyer panel problema 1 |
| **Headline propria** dell'hero: "Misura cosa farà il robot nel tuo reparto prima di comprarlo." | Sintesi §3 |
| Hero con una riga per i laboratori (SDK, ROS 2, simulatore, manuale) | Buyer panel feedback 3; strategia feedback 5 |
| Reel: tolta la piastrella (settore ceramico), prodotto di fantasia | Strategia feedback 7 |

### Applicazioni
| File | Modifica | In risposta a |
|-|-|-|
| `preventivo-cover` | Rifatta: le fasi P1 a P5 in scala sul metro delle settimane, rombo di decisione a fine fase, P0 spiegata, cosa resta al cliente | Messaggio dell'orchestratore; buyer panel feedback 2; art director feedback 4 |
| `preventivo-interna` | Nomi delle fasi, barre allineate al metro (28 settimane), bordi in gesso, limiti dichiarati con bordo pieno | Coerenza righelli e numeri |
| `hero` | Headline propria, G1 in piedi (nuovo ritaglio diverso dalle altre direzioni), metro allineato, peso e altezza ufficiali, limiti marcati Esempio, bottone secondario a filo pieno, favicon dichiarato | Sintesi §3 e §5; art director feedback 7; produzione feedback 6 |
| `linkedin-sacmi` | Metro tolto (la foto di tre quarti non si può misurare in lunghezza), ingombro scritto; segnato "Da pubblicare solo con consenso scritto di SACMI" | Art director feedback 5; sintesi §5 |
| `linkedin-anonimo` | Tolti data, revisione del manuale, ore di assistenza e modello del robot | Sintesi §5; buyer panel feedback 6; strategia feedback 8 |
| `reel-g1` | G1 in piedi a figura intera, pubblico a sagome, metro allineato, copione con prodotto di fantasia | Sintesi §5; buyer panel feedback 4 |
| `totem` | Fascia in gesso blu, G1 in piedi con metro allineato, pianta dello stand in scala vera (un quadro = 50 cm, area 300 x 300 cm, pubblico a 100 cm, sagome dall'alto), tecnico dentro l'area | Sintesi §5; righelli coerenti; produzione problema 3 |
| `biglietto` | Testo minimo 26 px = 6,1 pt, cifre del righello 6,4 pt, tacche 0,36 pt; fronte con il solo simbolo, senza filo che attraversa il biglietto | Sintesi §4; produzione problema 1; strategia feedback 2 |
| `livrea` | Niente bande sulla cassa: simbolo grande e cartellino in gesso blu | Art director feedback 6; strategia problema 3 |
| `presentazione.html` | Aggiornata a tutti i punti sopra; tolto il metro decorativo che tagliava il numero 140 | Produzione feedback 7 |

### Non cambiato, di proposito
- Il territorio resta il cartamodello: i revisori lo hanno indicato come il più inatteso del round (art director, originalità 7).
- Il metodo a fasi, la tabella del preventivo interno e il riquadro dei limiti, valutati positivamente dal panel acquirenti.
