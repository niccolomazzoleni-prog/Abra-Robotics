# Motion. Territorio B, Misura d'uomo

## Principio: il montaggio

Le cose Abra si muovono come pezzi che un tecnico monta sul banco: arrivano una alla volta, si appoggiano e si fermano. Nessun rimbalzo da cartone animato, nessuna dissolvenza lunga, nessun effetto luminoso. Il movimento mostra come è fatta una cosa, poi si ferma e lascia leggere.

## Il logo animato (`logo/animazione.html`)

Sequenza di 2,8 secondi, solo CSS e SVG, senza librerie.

| Tempo | Pezzo | Movimento |
|-|-|-|
| 0,15 s | Asta | Cala dall'alto e si appoggia sulla linea di base |
| 0,55 s | Pancia | Rotola da sinistra e si ferma contro l'asta |
| 1,05 s | Spalla | Ruota attorno al proprio centro, come una leva, e chiude la a |
| 1,30 s | Giunto | La finestra si apre di colpo nel punto di contatto (180 ms) |
| 1,55 s | b, r, a | Salgono dalla linea di base, a 100 ms l'una dall'altra |
| 2,10 s | Robotics | Compare in 700 ms |

Il pulsante "Rivedi il montaggio" riavvia la sequenza. Con `prefers-reduced-motion` il logo appare già montato.

**Segnale di attesa**: la spalla ocra si richiude sull'asta in ciclo (1,4 s), con pancia e asta ferme. Sostituisce gli indicatori di caricamento generici sul sito e nel Company Brain.

## Curva e tempi

- Una sola curva per tutto il sistema, chiamata "appoggio": `cubic-bezier(.22,.8,.24,1)`. Parte decisa e rallenta a lungo, come un pezzo posato con cura.
- Durate: 180 ms per i cambi di stato dell'interfaccia (pulsanti, menu), 400 a 700 ms per gli elementi che entrano in pagina, 2,8 s al massimo per il logo.
- Sfasamento tra elementi in sequenza: 100 ms.

## Applicazioni

- **Sito**: all'apertura della home le forme della composizione entrano con la sequenza del logo (asta, disco, arco), poi il titolo sale dalla linea di base. Allo scorrimento la linea di misura accanto al robot si disegna dall'alto in basso e il cartellino compare quando la linea è completa.
- **Diagramma delle fasi**: i dischi si posano sull'asta da P0 a P5, a 100 ms l'uno dall'altro; l'ultimo è l'asta che si alza.
- **Video e reel**: apertura con il montaggio del simbolo in 1,2 s (solo la a), chiusura con il logo esteso fermo per 2 s. Sottotitoli su cartellino carta che entra dal basso in 300 ms.
- **Totem digitale e schermi in fiera**: ciclo di 20 s con il montaggio del simbolo, il titolo del noleggio e il codice QR fermo per almeno 12 s.

## Cosa evitare

Rimbalzi elastici, parallasse pesante, particelle, scie luminose, glitch, testo che si scrive lettera per lettera, rotazioni 3D del robot, transizioni più lunghe di 1 s nell'interfaccia.
