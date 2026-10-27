# Sistema grafico: Cartamodello (v3)

Il cartamodello torna visibile, con gli oggetti del mestiere che chiunque riconosce senza spiegazione: **schede numerate, tacche, cartellini**. Stoffe e moda restano fuori: sono gli stessi segni che si trovano su una dima d'officina. Nei testi per i clienti le fasi restano con i nomi del settore.

## 1. I tre gesti fissi

| Gesto | Forma | Significato | Dove compare sempre |
|-|-|-|-|
| **La tacca** | Triangolo a V intagliato nel bordo alto di una scheda, di una fascia o di un oggetto | Nei cartamodelli le tacche dicono quale pezzo si cuce con quale. Da noi **contano le fasi**: una tacca per la P1, due per la P2, e così via. Una sola tacca centrale segna la linea di piega del marchio | Copertina del preventivo (fasi), totem (scheda del robot), livrea (maniglia della cassa e tacca fustellata del biglietto), hero (fasce delle fasi), simbolo |
| **La scheda numerata** | Cartoncino grigio con il numero del pezzo in alto ("1/4", "1/12", "1/6") | Ogni oggetto misurato o documento è un pezzo di un insieme: si sa sempre quanti pezzi compongono il progetto | Scheda del robot (hero, totem), pagina del preventivo, post, targa della cassa |
| **Il cartellino** | Etichetta in gesso blu con foro a sinistra | Un'informazione legata a un oggetto: copione approvato, data della prova generale, numero di cassa | Reel, flight case, totem |

## 2. La regola del gesso e della cucitura

| Stato | Come si disegna |
|-|-|
| Da approvare, ancora da misurare | In gesso: bordo sottile Blu segno (2 px, 0,35 mm in stampa) su fondo chiaro |
| Misurato e firmato | Cucito: flanella piena o linea flanella |

Il tratteggio resta escluso.

## 3. Il metro

Nastro in gesso blu (Pantone 278 C) con tacche flanella. Si usa **solo dove misura qualcosa di vero**, con la scala allineata all'oggetto: G1 da 0 ai piedi a 130 cm alla testa (hero, reel, totem), settimane del preventivo (una tacca = una settimana), millimetri del biglietto. Le schede del robot hanno sotto una griglia a 10 cm, la griglia del tavolo da taglio, allineata al metro.

## 4. Il marchio a piccole dimensioni

- Sotto 24 px solo `logo/favicon-16.svg`, disegnato pixel per pixel (o `favicon-16-mono.svg`).
- Da 24 a 64 px `logo/monogramma.svg`; sopra, `simbolo.svg`, `simbolo-negativo.svg` o `simbolo-bicolore.svg` (tessera in gesso blu con la tacca allineata alla piega).
- Il simbolo è la legatura "ab": a 16 px resta due lettere, diversa da una A isolata (`logo/test.png` la mette accanto a una A generica).

## 5. Il pubblico

Negli eventi il pubblico non si disegna come figure: si segnano **a gesso i posti** dove starà, con croci Blu segno sul pavimento (reel, pianta del totem). È coerente con il mestiere: si segna sul pavimento prima che arrivino le persone.

## 6. Griglia

- Modulo 8 px a schermo, 4 mm in stampa.
- Sito (1440 px): colonna chiara di 820 px con titolo, fasi e azioni; colonna flanella con la scheda del robot e le misure.
- A4: margini 15 mm; fascia di testa in flanella alta 84 mm; il percorso usa una settimana = 24 px (6,35 mm).
- Post 1200 x 1500: margini 72 px. Verticali 1080 x 1920: area sicura 150 px in alto e 110 in basso.

## 7. Iconografia

Sei icone in `icone/`, griglia 24 px, tratto 1,75 px, capi tondi, senza riempimenti né tratteggi: misure (metro avvolgibile), simulazione (cubo e gemello), prova (scheda con tacca e segno a gesso), modello (foglio con angolo piegato), assistenza (cartellino), noleggio (calendario con il giorno segnato).

## 8. Diagrammi e dati

- Le fasi si disegnano in scala sul metro delle settimane; ogni fase porta tante tacche quante il suo numero.
- Ogni fase ha accanto il **numero misurato** che produce e la data in cui arriva.
- Serie: flanella per il valore misurato, Blu segno per il confronto, gesso blu per un solo punto evidenziato.
- Ogni dato inventato porta "Esempio".

## 9. File di sistema

- `assets/sistema.css`: colori v3, sei tagli statici, classi `.cartellino`, `.num`, `.esempio`, `.in-gesso`, `.cucito`.
- `assets/metro.js`: metro SVG allineabile (tacca dello zero a 2 px dall'inizio).
- `_lavoro/geo3.js` e `build-logo-v3.js`: costruzione del marchio; `fav.py`: favicon pixel per pixel.
