# E. Cartamodello (v2)

Territorio wildcard per Abra Robotics. Data: 27/10/2026, revisione v2 dopo il round 1 (vedi `changelog.md`).

## Idea in una frase

Abra lavora come un modellista: prende le misure nel tuo reparto, prova il caso d'uso in simulazione e poi sul robot vero, e alla fine ti consegna il modello, cioè il codice, il simulatore e il manuale per rifarlo da solo.

## Prima di disegnare: quattro territori valutati

Il brief chiede un territorio lontano da A (precisione svizzero tedesca), B (umanesimo Olivetti), C (laboratorio, paper, dati) e D (scena). Ho messo a confronto quattro idee sugli stessi criteri.

| Idea | In breve | Aderenza a "Prima la prova" | Distanza da A, B, C, D | Rischio principale |
|-|-|-|-|-|
| 1. **Lo sportello aperto** | L'automa da salone dell'Ottocento che il prestigiatore apriva prima dello spettacolo per mostrare gli ingranaggi. Abra apre tutti gli sportelli prima di vendere. Usa la magia del nome. | Alta sul "prima", debole sul "cosa ti resta" | Media: il palcoscenico è vicino a D | Il riferimento storico più famoso, il Turco meccanico, era una truffa con un uomo nascosto: racconto pericoloso per un marchio che vende fiducia |
| 2. **Il campo segnato** | Il nastro adesivo sul pavimento del reparto che delimita l'area di prova. Angoli di nastro, frecce, zone. | Alta | Bassa: segnaletica industriale e giallo nero sono vicini ad A e al codice sicurezza | Diventa cartellonistica HSE, nessun calore, difficile per gli eventi |
| 3. **ABRACADABRA a triangolo** | L'amuleto antico in cui la parola perde una lettera per riga fino ad "A": ogni fase P0 a P5 toglie incertezza fino alla risposta. | Media | Alta | Associa la misura a una formula magica: contraddice la promessa e fa sorridere il direttore R&D nel modo sbagliato |
| 4. **Cartamodello** | Il mestiere del modellista e del sarto: misure, imbastitura, prova, cartamodello consegnato. | Altissima, parola per parola | Alta: nessuno dei quattro territori usa materiali e gesti della sartoria | "Sartoriale" è un luogo comune del marketing italiano; la sartoria può sembrare moda |

**Scelta: Cartamodello.** È l'unica idea in cui ogni passo del metodo Abra ha già un corrispettivo nel mestiere. Nella v2 la corrispondenza guida il sistema grafico; **nei testi per i clienti le fasi si chiamano con le parole del settore** (Sopralluogo e assessment, Simulazione, Prova sul robot, Consegna), perché i revisori e il panel acquirenti hanno trovato "imbastitura" incomprensibile.

| Metodo Abra (nome usato nei testi) | Corrispettivo nel mestiere (solo logica interna) | Cosa vede il cliente |
|-|-|-|
| P0 e P1, Sopralluogo e assessment | Le misure | Un report con tempi, pesi, ingombri misurati nel suo reparto |
| P2, Simulazione | L'imbastitura | Il caso d'uso nel modello digitale, provvisorio, che si può ancora correggere |
| P3 e P4, Prova sul robot e pilota | La prova | Il robot vero sul suo pezzo, con criteri scritti prima |
| P5, Consegna e formazione | Il modello | Codice, simulatore e manuale che restano in azienda per rifarlo |

Il posizionamento raccomandato si chiama "Prima la prova". In sartoria la prova è esattamente questo: il momento in cui il capo imbastito si prova addosso prima di tagliare la stoffa buona. E "su misura" traduce alla lettera il positioning di partenza dei fondatori, "custom-made use cases".

Il nome Abra resta un'eco leggera: la magia non entra nel marchio, entra nel gesto del modellista che con un metro e un gesso trasforma un'idea in una forma che sta in piedi. Il mago e gli effetti speciali restano fuori.

## Razionale strategico

1. **Risponde all'insight con un oggetto.** Chi valuta un robot teme di scoprire tardi cosa farà. Il cartamodello è il contrario del "tardi": si misura e si prova prima di tagliare. E risponde anche alla paura di restare senza materiali, perché il modello resta al cliente.
2. **Regge senza robot e con qualunque produttore.** Gli elementi del sistema sono metro, segni a gesso, schede di carta con tacche, rombi di decisione. Nessuno dipende da Unitree o dalla forma del robot: si misura un umanoide come un quadrupede, una base su ruote o un braccio.
3. **Spazio libero nel settore.** Nessun competitor rilevato usa carta, metro o segni di gesso. La palette è una tela grezza con un grigio flanella e il gesso da sarto blu, chiaro e polveroso: lontano dal blu elettrico e dal cobalto del settore, dal viola, dall'arancio da startup, dal rosso su antracite di ANYbotics, e dai colori firma delle altre quattro direzioni.
4. **Dà al sistema una regola semantica.** Ciò che è in gesso (bordo sottile blu) è da approvare e si può cancellare; ciò che è cucito (flanella piena) è misurato e firmato. La stessa regola funziona nel preventivo, nei diagrammi e nel marchio, dove la traversa è cucita e il filo in gesso esce dalla A. Il team di due persone la applica senza un designer.
5. **Regge i tre segmenti cambiando registro.** Manifattura: il preventivo mostra le fasi in scala sul metro delle settimane, con un rombo dove si decide. Laboratorio: il pacchetto per il tesista è il modello consegnato. Eventi: la prova generale con il copione approvato è letteralmente una prova d'abito.

## Il marchio in breve

- **Simbolo**: una A con la **traversa cucita**, piena e inclinata di 9 gradi, che attraversa la gamba destra ed esce come un filo in gesso blu. La traversa è sempre visibile, anche a 16 px: la "Λ" della v1 è eliminata. Il segno è disegnato da zero in SVG.
- **Logotipo**: "Abra" con la stessa A (senza filo esterno) e le lettere **b, r, a disegnate a mano** con superellissi: b e a sono lo stesso pezzo specchiato, come un cartamodello tagliato due volte. "Robotics" segue con spaziatura normale.
- **Piccole dimensioni**: favicon disegnato pixel per pixel su 16 px, monogramma ingrossato da 24 a 64 px.
- **Colore**: tela, flanella, gesso blu (colore firma), blu segno; carta modello, gesso e grafite come secondari. Il giallo della v1 è eliminato.
- **Tipografia**: Bricolage Grotesque in sei tagli statici, titolo a peso 640 e larghezza 94.

## Segmento a cui parla meglio

**Il direttore R&D o operations della manifattura**, che definisce la solidità del marchio. Riconosce subito il linguaggio della misura, del collaudo, del "provare prima di tagliare", e ritrova nel preventivo una tavola di modello con fasi, criteri e costi. Parla molto bene anche al **laboratorio universitario**: il cartamodello consegnato è il pacchetto che fa partire il tesista. Agli **eventi** offre la metafora più naturale di tutte, la prova generale.

## Cosa sacrifica

- **L'effetto tecnologico immediato.** Il robot appare sempre su un pezzo di carta, misurato, senza schermi né render. Chi cerca un fornitore "AI" a colpo d'occhio deve leggere un secondo in più.
- **Il nero e la drammaticità.** La flanella fa da fondo scuro solo per eventi e social; il resto vive su tela chiara. Rinunciamo al lusso del nero pieno.
- **Una parte del calore della sartoria.** Per non scivolare nella moda abbiamo escluso tessuti, macro di stoffa, manichini e forbici in foto. Della sartoria restano gli strumenti e i gesti, mai i vestiti.
- **Il gioco con la magia del nome.** Si sente solo nel filo che esce dalla A. Il mago resta fuori.
