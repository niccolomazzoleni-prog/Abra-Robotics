# Motion: Cartamodello (v3)

## Principi

1. **Il movimento è un gesto di misura.** Ogni animazione imita un gesto del modellista: tagliare un pezzo, passare il filo, stendere il metro, segnare a gesso. Nessun movimento decorativo.
2. **Prima il gesso, poi la cucitura.** Un elemento entra con il bordo sottile in blu segno (da approvare) e diventa pieno in flanella quando il dato è confermato. È la regola del sistema resa visibile nel tempo.
3. **Velocità di laboratorio.** Durate da 300 a 700 ms per gli elementi, al massimo 2,6 s per una sequenza intera. Curva di uscita morbida `cubic-bezier(.2,.7,.2,1)` per ciò che entra, `cubic-bezier(.45,0,.2,1)` per ciò che scorre (il filo, il metro).
4. **Un passo alla volta.** Ritardi costanti di 100 ms tra elementi della stessa famiglia (lettere, voci di elenco, fasi). Mai più di un gruppo in movimento contemporaneamente.
5. **Rimbalzi e rotazioni sono esclusi.** Il robot nei video si muove da solo: la grafica resta ferma mentre lui lavora.
6. **Rispetto di `prefers-reduced-motion`**: con la riduzione attiva il marchio e le pagine appaiono nello stato finale.

## Il logo animato (`logo/animazione.html`)

| Tempo | Gesto | Tecnica |
|-|-|-|
| 0,1 a 0,7 s | L'**asta comune si taglia** dal basso: è la linea di piega | `clip-path: inset()` |
| 0,7 a 1 s | In cima compare la **tacca** in gesso blu | opacità |
| 1 a 1,6 s | La **b e la a si aprono dalla piega**, verso destra e verso sinistra, come un pezzo tagliato in doppio | `clip-path` dai due lati |
| 1,7 a 2,3 s | **r e a** salgono una alla volta | `transform` con ritardi di 100 ms |

Tutto è CSS e SVG, senza librerie. Con `prefers-reduced-motion` il logotipo appare fermo.

## Altri movimenti del sistema

- **Il metro che si stende**: nelle timeline del sito il nastro in gesso blu entra da sinistra a 600 ms; le tacche delle settimane appaiono con lo stesso ritmo.
- **La fase che si firma**: quando una fase viene accettata, il bordo blu si riempie di flanella in 300 ms.
- **Il segno a gesso**: le croci dei posti del pubblico si disegnano con due tratti da 150 ms ciascuno.
- **La tacca**: quando una fase viene accettata, una nuova tacca si intaglia nella fascia in 200 ms.
- **Nei reel**: titolo fermo per 1,5 s, poi il pezzo di carta con il robot sale dal basso; il copione si legge come sottotitolo, una riga alla volta.
