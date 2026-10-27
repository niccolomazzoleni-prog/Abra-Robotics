# Autocritica (v3)

Tre punti deboli della direzione C, Nota a margine, dopo la v3, e cosa ho fatto per mitigarli.

## 1. Il marchio parte da un carattere libero

Il logotipo è STIX Two SemiBold ridisegnato: la A con il richiamo e la r con il punto sono proprie, la b e la a restano vicine al disegno originale. Chiunque può comporre "Abra" in STIX e ottenere una parola simile; la protezione sta nella A annotata e nella r.

Mitigazione: le modifiche sono quelle che si vedono anche a 24 px (punto grande nella A, punto staccato della r, spaziatura), e sono documentate in `sistema-grafico.md`. Si deposita il logotipo intero in bianco e nero, il simbolo dopo la ricerca per immagine. Se il cliente vuole più proprietà, il passo successivo è ridisegnare anche b e a con lo stesso contrasto, mantenendo le regole del punto.

## 2. A 16 px il segno è al limite

La favicon disegnata a pixel tiene punto e filo distinti, ma in 16 × 16 la A è sottile e il punto occupa tutta la luce interna: su schermi a bassa densità può leggersi come una A con una macchia.

Mitigazione: punto 3 × 3 staccato di 1 px dalla gamba sinistra, filo di 1 px che attraversa la gamba destra ed esce di 2 px, fondo giallo che stacca il segno nella barra delle schede. Da 32 px si usa il vettore. Da provare su Windows a 100% prima del lancio.

## 3. La direzione vive di note vere, che oggi mancano

Il sistema promette misure, protocolli, revisioni e limiti dichiarati. Nessun progetto misurato prima dell'acquisto è concluso, la scheda limiti non esiste, le foto sono Unitree. Con l'evidenziatore riservato ai dati, le pagine senza numeri veri restano senza giallo.

Mitigazione: tutti i dati inventati portano "Esempio" o "valutazione interna"; i richiami sulle foto cadono solo su componenti reali; il pubblico è disegnato come dati di esempio dichiarati. La prima produzione consigliata resta la scheda limiti del G1 con il protocollo di misura.

## Risolti in v3

- Logotipo staccato dal sistema (v2): il marchio torna nel serif scientifico, con il richiamo dentro la lettera.
- Grassetto sintetico e glifi mancanti nel PDF: Bold dichiarato in stampa, ≤ ≥ → e ✓ eliminati dal testo.
- Testi sotto 6 pt: verificati con controllo automatico su preventivo e biglietto.
- Composizioni comuni alle altre direzioni: flight case come tavola, pubblico come dati, G1 a mezza figura.
