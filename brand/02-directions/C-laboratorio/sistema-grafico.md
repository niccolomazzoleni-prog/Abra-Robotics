# Sistema grafico

Cinque elementi, tutti derivati dalla pagina di un articolo scientifico. Ogni applicazione ne usa almeno tre; nessuna li usa tutti alla stessa intensità.

## 1. Il richiamo (punto, filo, nota)

È il gesto del marchio portato fuori dal marchio.

- **Punto**: cerchio pieno. Su carta è inchiostro; su foto e superfici scure è evidenziatore con anello d'inchiostro (spessore anello pari al 20% del diametro).
- **Filo**: linea continua, mai tratteggiata, spessa un settimo del diametro del punto. Orizzontale, verticale o con un solo gomito a 90 gradi. Mai diagonale, mai curva, mai frecce.
- **Nota**: etichetta in DM Mono maiuscolo (che cosa è) più una riga in STIX (che cosa fa o quanto misura). Se la nota contiene un limite o un dato non verificato, va in corsivo grafite.
- **Proporzioni** a schermo: punto 9 a 15 px, filo 1,25 a 2 px, distanza minima fra nota e filo 10 px.
- **Regole**: massimo quattro richiami per figura; i fili non si incrociano; il punto sta sulla parte reale del robot o sul valore reale del grafico, mai su un'area vuota per bellezza.

## 2. La colonna delle note

Ogni pagina ha una colonna di testo principale e una colonna a margine (destra sul web e nei documenti, sinistra solo sui formati verticali dove manca lo spazio).

- **Web, 1440 px**: margini 56 px, colonna principale 8 colonne, margine 4 colonne su una griglia di 12 da 88 px con canale 24 px. La colonna a margine ospita note, figure, revisioni.
- **A4**: margine sinistro 18 mm (con i numeri di riga a 8 mm dal bordo), colonna principale 128 mm, canale 6 mm, colonna note 44 mm, margine destro 14 mm.
- **Social 1200 x 1500**: margini 72 px, una colonna; le note diventano richiami sulla figura.
- I numeri dei richiami nel testo (apice DM Mono) e nella colonna a margine sono identici e alla stessa altezza quando possibile.

## 3. L'evidenziatore

Una fascia gialla dietro al testo, alta il 62% del corpo, posata sulla parte bassa della riga come un vero tratto di pennarello, con estremità leggermente oblique. Si evidenzia la misura o il beneficio misurabile: "prima di investire", "tempo ciclo ≤ 15 s", "conosce già il tuo stabilimento". Una sola evidenziazione per pagina.

## 4. Revisioni, figure, numeri di riga

- **Revisione**: punto pieno più testo DM Mono, per esempio "rev 1.1 · 27.10.2026". Compare in testata di ogni documento, post e pagina web. Nei documenti le modifiche fra revisioni si annotano a margine con un filetto giallo verticale.
- **Figure e tavole**: ogni immagine è una figura numerata con didascalia ("Fig. 1", "Tav. 7"), anche sui social. La didascalia dice cosa si vede, quando è stato misurato e se l'immagine è un segnaposto.
- **Numeri di riga**: DM Mono 6 a 10 px in grafite chiara nel margine sinistro di preventivi, manuali e hero del sito. Dicono "questo testo è aperto alla revisione" e servono davvero nelle call: "guardate la riga 40".
- **Dicitura Esempio**: etichetta DM Mono maiuscola con filetto, obbligatoria su ogni dato inventato nei mockup.

## 5. La carta a quadretti

Quadretto da 5 mm in rigatura al 55% di opacità. Si usa come banco di prova sotto le figure dei robot, sul retro di documenti e sulle superfici di supporto. Mai sotto i paragrafi, mai sul marchio.

## Iconografia

Sei icone in `icone/`, griglia 24 x 24, tratto 1,5 px con estremità tronche e angoli vivi, un solo punto pieno per icona: il punto misurato. Il tratteggio indica il simulato (cubo del digital twin).

| File | Significato |
|-|-|
| `assessment.svg` | Assessment, misura, tempo |
| `simulazione.svg` | Simulazione e digital twin |
| `codice.svg` | Codice nel repository del cliente |
| `manuale.svg` | Manuale tecnico e documentazione |
| `formazione.svg` | Formazione, tesi in azienda |
| `evento.svg` | Umanoide che parla per eventi |

Dimensioni ammesse: 16, 24, 32, 48 px. Colore: inchiostro su carta, carta su inchiostro. Il punto può diventare giallo solo sopra i 32 px.

## Pattern

L'unico pattern è il quadretto. In alternativa, per superfici grandi (flight case, retro di cartelle), una sequenza regolare di punti di calendario: pieno per i giorni di lavoro, vuoto per i giorni liberi, a ricordare il registro.

## Diagrammi e dati

- **Misurato**: punto pieno inchiostro con barra d'incertezza verticale (cappelli corti).
- **Simulato**: cerchio vuoto in grafite, spostato a sinistra del misurato dello stesso caso.
- **Criterio di accettazione**: linea tratteggiata inchiostro con etichetta "criterio: ≤ 15 s".
- **Zona accettata**: fascia evidenziatore al 50% di opacità.
- **Assi**: solo l'asse dei valori, sottile, con tre etichette al massimo. Griglia in rigatura, due linee.
- **Fasi del progetto**: una linea con un punto per fase; il punto finale è vuoto (ciò che resta da fare). La fascia gialla copre le fasi in cui si misura prima dell'investimento.
- **Calendari e disponibilità**: punti pieni prenotati, vuoti liberi.
- Ogni grafico ha titolo, fonte e data di misura nella didascalia; i valori di esempio lo dichiarano.

## Cose da non fare

Gradienti, ombre colorate, glow, robot a colori su fondo nero, linee bianche su blu, frecce curve, più di un'evidenziazione per pagina, il richiamo usato come decorazione senza nota, il quadretto dietro al testo corrente.
