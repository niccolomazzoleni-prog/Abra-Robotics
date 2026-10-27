# Motion v2. Territorio B, Montato a vista

## Principio: il montaggio

Le cose Abra si muovono come pezzi posati sul banco: arrivano una alla volta, si fermano nella loro posizione e lasciano leggere. Il giunto non si chiude mai: la pancia della a si ferma prima dell'asta. Niente rimbalzi, scie, effetti luminosi.

## Il logo animato (`logo/animazione.html`)

Solo CSS e SVG, 2,8 secondi.

| Tempo | Pezzo | Movimento |
|-|-|-|
| 0,15 s | Asta della prima a | Cala dall'alto e si appoggia sulla linea di base |
| 0,55 s | Pancia | Scorre da sinistra e si ferma a 16 unità dall'asta: il giunto resta aperto |
| 1,05 s | Spalla | Ruota attorno al proprio centro e chiude la lettera |
| 1,60 s | b, r, a | Salgono dalla linea di base a 100 ms l'una dall'altra |
| 2,20 s | Robotics | Compare in 600 ms |

Il pulsante "Rivedi il montaggio" riavvia la sequenza; con `prefers-reduced-motion` il logo appare già montato.

**Segnale di attesa**: la pancia della a torna in posizione contro il giunto, in ciclo da 1,2 s. Sostituisce gli indicatori di caricamento generici sul sito e nel Company Brain.

## Curva e tempi

- Curva unica "appoggio": `cubic-bezier(.22,.8,.24,1)`.
- 180 ms per i cambi di stato dell'interfaccia, da 400 a 600 ms per i pannelli che entrano, 2,8 s al massimo per il logo.
- Sfasamento tra elementi in sequenza: 100 ms.

## Applicazioni

- **Sito**: i pannelli dell'hero entrano in ordine di lettura (navigazione, testo, foto, segmenti) con un giunto che si apre di 12 px; il cartellino del robot compare per ultimo.
- **Pagina delle fasi**: i blocchi P0 a P5 si posano da sinistra; la fase in corso prende il filetto rosso.
- **Video e reel**: apertura con il montaggio della a in 1,2 s; sottotitoli in pannelli bianchi che entrano dal basso in 300 ms; chiusura con il marchio esteso fermo per 2 s.
- **Schermi in fiera**: ciclo di 20 s con il montaggio del simbolo, il titolo del noleggio e il codice QR fermo per almeno 12 s.

## Cosa evitare

Rimbalzi elastici, parallasse pesante, particelle, glitch, testo battuto lettera per lettera, rotazioni 3D del robot, transizioni più lunghe di un secondo nell'interfaccia.
