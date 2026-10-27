# Motion: Cartamodello (v2)

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
| 0,1 a 0,8 s | Le gambe della A si **tagliano** dal basso verso l'alto, come un pezzo di carta | `clip-path: inset()` animato |
| 0,8 a 1,35 s | La **traversa si cuce** da sinistra a destra: è piena dall'inizio alla fine, mai tratteggiata | `clip-path` da destra |
| 1,3 a 1,7 s | Il **filo in gesso blu esce** dalla gamba destra | `clip-path` |
| 2,1 a 2,45 s | Il filo rientra verso destra, dietro alla b che arriva | `clip-path` inverso |
| 2,2 a 2,9 s | **b, r, a** salgono una alla volta | `transform` con ritardi di 100 ms |

Tutto è CSS e SVG, senza librerie. Con `prefers-reduced-motion` il logotipo appare fermo, senza filo.

## Altri movimenti del sistema

- **Il metro che si stende**: nelle timeline del sito il nastro in gesso blu entra da sinistra a 600 ms; le tacche delle settimane appaiono con lo stesso ritmo.
- **La fase che si firma**: quando una fase viene accettata, il bordo blu si riempie di flanella in 300 ms.
- **Il segno a gesso**: le croci si disegnano con due tratti da 150 ms ciascuno, il secondo con 80 ms di ritardo.
- **Nei reel**: titolo fermo per 1,5 s, poi il pezzo di carta con il robot sale dal basso; il copione si legge come sottotitolo, una riga alla volta.
