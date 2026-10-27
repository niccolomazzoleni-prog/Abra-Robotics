# Motion: Cartamodello

## Principi

1. **Il movimento è un gesto di misura.** Ogni animazione imita un gesto del modellista: tagliare un pezzo, passare il filo, stendere il metro, segnare a gesso. Nessun movimento decorativo.
2. **Prima il tratteggio, poi la linea.** Un elemento entra tratteggiato (in prova) e diventa continuo quando il dato è confermato. È la regola del sistema resa visibile nel tempo.
3. **Velocità di laboratorio.** Durate da 300 a 700 ms per gli elementi, al massimo 2,6 s per una sequenza intera. Curva di uscita morbida `cubic-bezier(.2,.7,.2,1)` per ciò che entra, `cubic-bezier(.45,0,.2,1)` per ciò che scorre (il filo, il metro).
4. **Un passo alla volta.** Ritardi costanti di 100 ms tra elementi della stessa famiglia (lettere, voci di elenco, fasi). Mai più di un gruppo in movimento contemporaneamente.
5. **Rimbalzi e rotazioni sono esclusi.** Il robot nei video si muove da solo: la grafica resta ferma mentre lui lavora.
6. **Rispetto di `prefers-reduced-motion`**: con la riduzione attiva il marchio e le pagine appaiono nello stato finale.

## Il logo animato (`logo/animazione.html`)

| Tempo | Gesto | Tecnica |
|-|-|-|
| 0,1 a 0,8 s | Le gambe della A si **tagliano** dal basso verso l'alto, come un pezzo di carta | `clip-path: inset()` animato |
| 0,55 a 1,65 s | Il **filo** entra da sinistra e scorre: i punti spariscono sotto le gambe grazie a un alone color tela | `stroke-dasharray` e `stroke-dashoffset` su una linea a 9 gradi |
| 1,6 s | Il filo si ferma: resta solo il punto nel controforma | cambio di opacità |
| 1,55 a 2,25 s | **b, r, a** salgono una alla volta | `transform` con ritardi di 100 ms |
| 2,1 a 2,6 s | "Robotics" appare | opacità |

Tutto è CSS e SVG, senza librerie: si può usare come intro del sito, chiusura dei video, schermata di caricamento del Company Brain.

## Altri movimenti del sistema

- **Il metro che si stende**: nelle timeline del sito il nastro giallo entra da sinistra a 600 ms; le tacche delle settimane appaiono con lo stesso ritmo.
- **La fase che si firma**: al passaggio del mouse su una fase accettata, il bordo tratteggiato si chiude in linea continua in 300 ms.
- **Il segno a gesso**: le croci si disegnano con due tratti da 150 ms ciascuno, il secondo con 80 ms di ritardo.
- **Nei reel**: titolo fermo per 1,5 s, poi il pezzo di carta con il robot sale dal basso; il copione si legge come sottotitolo, una riga alla volta.
