# Changelog · Direzione A

## v3 · 28/10/2026 · "In squadra" (round 2: media 7,5; marchio 6,2)

### Marchio (priorità 1: lettura "Ab" a 16, 24 e 32 px)
- **Legatura ridisegnata**: la A torna intera, con due aste a pendenza 2 a 1, traversa e vuoto; il suo piede destro poggia sull'asta verticale della b. La squadra diventa il vuoto tra le due lettere (triangolo rettangolo 2 a 1). Risponde a art director, strategia e buyer panel: la mezza A della v2 si leggeva "4b" o "/b".
- **Favicon 16 px ridisegnata pixel per pixel** con la A intera (vuoto 2 × 2 px, traversa) e la squadra visibile; provata a 16, 24, 32 px e su tema scuro in `logo/test.png`.
- **Terzo dettaglio nel logotipo** (revisore marchio, feedback 3): cima della t tagliata ad angolo retto rispetto alla diagonale, oltre a r e R a 2 a 1.
- **Geometria dichiarata non modificabile** in `sistema-grafico.md` come oggetto del deposito.
- Costruzione in `logo/test.html` e animazione rifatte sulla nuova legatura; tolta l'annotazione a 5,5 px segnalata dalla produzione.

### Tipografia (priorità 2)
- Titoli in **IBM Plex Sans Condensed 600** (B612 in grande era goffo), testo in **IBM Plex Sans** (fine della coppia Barlow più verde di MYBOTSHOP), **B612** solo per etichette, quote e cartigli, dove è nato. Tutti statici e locali, licenza OFL nei file `OFL-IBMPlex.txt` e `OFL-B612.txt`; Barlow rimosso dalla cartella.

### Colore (priorità 3)
- **Pantone 348 C obbligatorio** in tinta piatta su tutti i campi pieni stampati; quadricromia solo in digitale con prova colore; RAL 6024 per vinili e vernici.
- **Verde tolto da robot e casse** (revisore marchio, rischio confusione con ISO 7010): targhe adesive e targa di trasparenza in grafite.

### Pubblico e G1 (priorità 4)
- Tolte le sagome uomo e donna da cartello. Il pubblico è rappresentato con il linguaggio della direzione: **linee di vista** alle altezze degli occhi (1600 mm adulto, 1100 mm bambino) e **figure in pianta dello stand** attorno al cerchio di sicurezza.
- **G1 disegnato a tratto** (contorni grafite ricavati dall'immagine ufficiale) in hero, reel e totem, diverso dal ritaglio fotografico usato dalle altre direzioni.
- Reel: battuta del G1 subito sotto il titolo, pianta dello stand, quota a tutta altezza; il vuoto tra titolo e scena è chiuso.

### Flight case (priorità 5)
- Ridisegnato come **tavola tecnica in proiezioni ortogonali** (vista frontale e fianco con quote), cassa in alluminio naturale con la legatura incisa in grafite e un **cartiglio** al posto dell'etichetta. Tolto il rettangolo grigio senza funzione.

### Headline (verbo "Decidi")
- Riscritte tutte: hero "Decidi sul robot dopo averlo visto lavorare sul tuo compito.", preventivo "Decidi alla fine di ogni fase se l'umanoide entra nella linea 3.", fasi "Decidi a ogni passaggio con un criterio firmato e un costo già noto.", post "Decidi i prossimi passi con mappa, simulatore e manuale già consegnati...", reel "Decidi cosa dirà l'umanoide al tuo pubblico, parola per parola.", totem "Decidi la data: il G1 arriva in fiera con il nostro tecnico.", biglietto "Decidi sul robot dopo averlo visto lavorare."
- Post SACMI anonimo: niente "tesi in azienda" né "tesista"; il beneficio è il materiale consegnato al team.

## v2 · 28/10/2026 · "In squadra" (round 1: media 6,9; marchio 5,2)

### Marchio (revisore marchio 5,2, art director, sintesi §2)
- **Simbolo ridisegnato**: la A isolata con il triangolo sotto la traversa è sostituita dalla **legatura Ab** costruita sulla squadra da disegno (asta destra verticale che diventa l'asta della b, diagonale con pendenza 2 a 1, traversa sempre presente). Risponde a: A isolata nel campo più affollato dei registri, triangolo che a 16 px si fonde con le aste, somiglianza con il simbolo della direzione D (figura sotto la traversa), confronto con l'icona "A" di abra.com.
- **Logotipo modificato in modo riconoscibile**: legatura Ab in apertura, terminale della r tagliato a 2 a 1, gamba della R alla stessa pendenza (feedback 3 del revisore marchio).
- **Favicon disegnata pixel per pixel** (`logo/favicon-16.svg`, griglia 16, mostrata ingrandita 8 volte in `logo/test.png`); regola: sotto i 24 px si usa solo questa versione.
- **Monogramma senza quadrato a filetto**: legatura bianca su piastra verde (`monogramma.svg`), più `monogramma-grafite.svg`. Risolve la cornice di 1 px che sfarfallava a 16 px e il formato "lettera nel quadrato".
- `mono-negativo.svg` senza rettangolo di fondo (revisore produzione 5).
- `logo/test.html` e `logo/animazione.html` rifatti sul nuovo segno (l'animazione costruisce l'angolo retto prima della parola).

### Colore (sintesi §1, art director 6, revisore produzione)
- **Colore firma esclusivo verde di misura RAL 6024 con alluminio**, usato come campo pieno nei formati di comunicazione (copertina del preventivo, testata del post, totem, biglietto, monogramma, reel).
- **Giallo eliminato** (vietato per A): il limite dichiarato diventa un tratteggio grafite, come una sezione nel disegno tecnico.
- Aggiunto il **verde profondo** `#0F3A2C` come fondo scuro; tolti il verde chiaro `#3DBB82` (fuori gamma) e la Grafite 80 (Acciaio su Grafite 80 a 4,09 : 1).
- **CMYK ricalcolati** con profilo dichiarato, Pantone e RAL indicativi, tabella dei contrasti con le coppie vietate (Grigio quota su Grafite 2,81 : 1; Grafite su verde 3,39 : 1). Nessuna coppia sotto AA nelle applicazioni.
- Nota esplicita in `palette.md`: la combinazione di colori non è un asset proteggibile.

### Tipografia (sintesi §6, art director 8, strategia 2)
- **B612** (OFL, il carattere degli schermi di cabina Airbus) per titoli e frasi brevi; Barlow resta per testo, dati, etichette. Barlow non è più l'unica voce. Font statici locali, nessuna CDN.

### Applicazioni
- **Hero**: nuova headline propria ("Decidi sul robot con un numero misurato in mano."), diversa da C; tolte le quattro icone generiche; aggiunti tre ingressi per segmento con la riga per i laboratori (SDK, ROS 2, simulatore, manuale, data di consegna scritta). G1 nuovo, in piedi a figura intera, ritagliato da un'altra immagine ufficiale.
- **Preventivo copertina**: tolta la tavola "costruzione del simbolo"; al suo posto la pianta della postazione del cliente con il punto di misura del tempo ciclo e le quote. Testata verde, headline propria.
- **Preventivo interna**: quadratino giallo sostituito dal tratteggio, titoli in B612.
- **Post SACMI anonimo**: tolti data, revisione del manuale, "tesi in azienda", "verbale di consegna"; la headline parla del "tuo team". **Nominativo**: dicitura "da pubblicare solo con il consenso scritto di SACMI", nessun "pubblicato con il consenso".
- **Reel**: fondo alluminio al posto di grafite più verde (vicino a Reply), G1 in piedi in scala con due sagome di visitatori, una sola battuta, triangolo verde a terra come punto d'incontro, quota a tutta altezza, fascia verde con il logotipo.
- **Totem**: testata verde a tutta altezza nella metà superiore ("Umanoide a noleggio, a giornata."), G1 in scala reale con sagome, triangolo verde a pavimento, calendario ridotto.
- **Biglietto**: tolto il righello (motivo assegnato a E), fronte verde con il segno Ab fuori formato e frase all'imperativo, nessun testo sotto 6,1 pt.
- **Livrea**: targhe su piastra verde con la legatura, testo minimo 7 px nello schema con scala dichiarata, giallo tolto dalla targa dati della cassa.
- **Presentazione**: riscritta sulla v2; importo indicato come esempio.

### Voce
- Headline proprie per ogni applicazione, nessuna presa dalla brand platform; aggiunte due headline per gli eventi (data, tecnico, copione).
- Riletti i testi per contrapposizioni e chiusure brevi: rimossa la coppia "prima la prova, poi l'investimento" dal biglietto.

### Non cambiato, con motivo
- Riquadro di controllo, cartiglio e targa dati restano: sono gli elementi più apprezzati da strategia e buyer panel (preventivo interno 8/10).
- Le sei icone restano nel sistema per documenti e manuali, fuori dall'hero.
