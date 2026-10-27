# Sistema grafico v2: arco scenico e pianta dei movimenti

## 1. Marchio

### Logotipo "abra"
Disegnato a mano su una griglia geometrica (file sorgente `_lavoro/tools/portale.py`): occhio medio 100, ascendente 60, asta 26, raggio esterno 50.
- Ogni occhiello è un **arco scenico**: controforma con tetto a semicerchio e base piana (raggio 23, base a 76), contorno esterno con tetto tondo e base squadrata.
- La "a" ha l'angolo tondo in alto a sinistra e l'asta squadrata a destra; la "b" è speculare. La "r" ha un orecchio ad arco tagliato in verticale. La parola alterna così angoli tondi e squadrati come una fila di quinte.
- Nessuna A maiuscola, nessun font composto: tutta la forma è proprietaria e si deposita come marchio figurativo in bianco e nero.

### Descrittore
"ROBOTICS" in Archivo Expanded SemiBold, alto 0,44 dell'occhio medio, convertito in tracciati. È un descrittore separato: il marchio da depositare è il logotipo "abra" e il simbolo "ab".

### Simbolo "ab"
Le prime due lettere affiancate: due portali, il percorso da a a b. Si usa per avatar, favicon, adesivo sul robot, targa.

### File in `logo/`
`logotipo`, `logotipo-negativo`, `orizzontale`, `orizzontale-negativo`, `verticale`, `verticale-negativo`, `mono-positivo`, `mono-negativo`, `simbolo`, `simbolo-negativo`, `monogramma` (tessera magenta per avatar), `favicon.svg` e `favicon-16.png` / `favicon-32.png` disegnate a pixel su griglia 16, `favicon-16-x6.png` ingrandita per la verifica.

### Regole d'uso
- Area di rispetto: l'altezza dell'asta della "b" sopra l'occhio medio (60 unità) su ogni lato.
- Dimensioni minime: orizzontale 25 mm in stampa e 110 px a schermo; logotipo da solo 14 mm e 64 px; simbolo 6 mm e 16 px (sotto i 24 px solo la favicon a pixel).
- Colori ammessi: Grafite su chiaro, Carta su Grafite, Carta su Magenta. Il descrittore può essere Magenta solo su Carta.
- Unitree e gli altri produttori si citano a testo, mai in un lockup.

## 2. Griglie

| Formato | Margini | Colonne | Note |
|-|-|-|-|
| Web 1440 | 64 px | 12, spazio 24 px | Testo a sinistra, arco scenico a destra |
| A4 | 52 a 56 px (circa 14 mm) | 6 | La pianta delle fasi occupa sempre una fascia intera |
| Social 1080 e 1200 | 72 a 80 px | 6 | Nei reel il testo importante sta tra 280 e 1640 px |
| Totem 80 x 200 cm | 6,4 cm | 4 | Titolo nel terzo alto, arco al centro, chiamata e QR ad altezza di mano |

## 3. Elementi

### L'arco scenico
Finestra con tetto a semicerchio e base piana, la stessa forma degli occhielli. In CSS: `border-radius:50vw 50vw 0 0`. Nei documenti incornicia la foto del robot su fondo Cemento con pavimento più scuro e ombra di contatto; nella scena è riempito di magenta pieno. Al massimo un arco per composizione.

### La pianta dei movimenti
Una linea Grafite da 1,5 a 2 px con posizioni circolari: piene Magenta per ciò che è deciso o fatto, vuote con bordo Grafite per ciò che va ancora deciso. Sotto ogni posizione: numero o nome in Bold, durata o esito in Regular. Si usa per le fasi P0 a P5, per il percorso dei tesisti, per il robot da a a b nelle foto e sul pavimento (dischi in vinile magenta "a" e "b").

### Il pubblico
Nei formati di scena le persone sono sagome disegnate (testa e spalle), in due toni di Grafite davanti all'arco. Nessuna foto di persone prese online.

### Didascalie
Corsivo tra parentesi per limiti, segnaposto ed esempi.

## 4. Iconografia

Sei icone in `icone/`, griglia 48, tratto Grafite 3 px a terminazioni quadrate. Ogni icona ha un solo punto Magenta: la posizione di arrivo "b".

| File | Servizio |
|-|-|
| `misura.svg` | Assessment e misura |
| `simulazione.svg` | Digital twin e simulazione |
| `fasi.svg` | POC a fasi: da un punto pieno grafite a un punto magenta |
| `codice.svg` | Codice consegnato nel repository del cliente |
| `formazione.svg` | Manuale e formazione |
| `evento.svg` | Noleggio per eventi: l'arco scenico con l'interprete |

## 5. Pattern

**Pianta di sala**: griglia di piccoli cerchi Quinta ogni 64 px su Grafite, con due posizioni magenta "a" e "b" unite da un percorso. Per slide di sezione e sfondi di schermi in fiera. Mai nei documenti.

## 6. Diagrammi e dati

- Barre piatte Grafite su Carta; la barra che soddisfa il criterio di accettazione passa in Magenta.
- Il criterio è una linea orizzontale Grafite da 2 px con l'etichetta "Criterio" in Expanded.
- Tempi e fasi: blocchi pieni per le fasi decise, tratteggiati per quelle da decidere.
- Dati di prova sempre con l'etichetta "Esempio".
- Colori delle serie, in ordine: Grafite, Magenta, Fumo chiaro, Rosa. Massimo quattro.
