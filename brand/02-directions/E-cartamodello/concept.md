# E. Cartamodello (v3)

Territorio wildcard per Abra Robotics. Data: 27/10/2026, revisione v3 dopo il round 2 (vedi `changelog.md`).

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
2. **Regge senza robot e con qualunque produttore.** Gli elementi del sistema sono metro, segni a gesso, schede numerate, tacche e cartellini. Nessuno dipende da Unitree o dalla forma del robot: si misura un umanoide come un quadrupede, una base su ruote o un braccio.
3. **Spazio libero nel settore.** Nessun competitor rilevato usa carta, metro o segni di gesso. La palette è una tela grezza con un grigio flanella e il gesso da sarto blu, chiaro e polveroso: lontano dal blu elettrico e dal cobalto del settore, dal viola, dall'arancio da startup, dal rosso su antracite di ANYbotics, e dai colori firma delle altre quattro direzioni.
4. **Dà al sistema segni che il cliente vede.** Le tacche contano le fasi, le schede sono numerate come pezzi di un insieme, i cartellini legano un'informazione all'oggetto. In più, ciò che è in gesso (bordo sottile blu) è da approvare, ciò che è cucito (flanella piena) è firmato. Il team di due persone applica tutto senza un designer.
5. **Regge i tre segmenti cambiando registro.** Manifattura: il preventivo mostra in copertina quando arriva il primo numero misurato (settimana 3) e le fasi in scala sul metro delle settimane. Laboratorio: il pacchetto per il tesista è il modello consegnato. Eventi: la prova generale con il copione approvato è letteralmente una prova d'abito.

## Il marchio in breve

- **Simbolo**: la legatura **"ab"**. La a e la b condividono un'unica asta, che è la **linea di piega** del cartamodello: la pancia della b e l'occhio della a si aprono dai due lati come un pezzo tagliato in doppio. In cima all'asta c'è una **tacca a V**, il segno con cui il modellista indica la piega. A 16 px resta due lettere, lontana da una A isolata.
- **Logotipo**: "abra" minuscolo, interamente disegnato con superellissi, con la stessa legatura ab; "robotics" in Bricolage Grotesque a peso più leggero, con l'altezza x allineata.
- **Piccole dimensioni**: favicon disegnato pixel per pixel su 16 px, anche in monocromia.
- **Colore**: flanella dominante, gesso e tela neutri, cartoncino grigio; gesso blu Pantone 278 C vincolante come colore firma, blu segno 7684 C per le linee.
- **Sistema**: tacche che contano le fasi, schede numerate, cartellini.
- **Tipografia**: Bricolage Grotesque in sei tagli statici.

## Segmento a cui parla meglio

**Il direttore R&D o operations della manifattura**, che definisce la solidità del marchio. Riconosce subito il linguaggio della misura, del collaudo, del "provare prima di tagliare", e ritrova nel preventivo una tavola di modello con fasi, criteri e costi. Parla molto bene anche al **laboratorio universitario**: il cartamodello consegnato è il pacchetto che fa partire il tesista. Agli **eventi** offre la metafora più naturale di tutte, la prova generale.

## Cosa sacrifica

- **L'effetto tecnologico immediato.** Il robot appare sempre su un pezzo di carta, misurato, senza schermi né render. Chi cerca un fornitore "AI" a colpo d'occhio deve leggere un secondo in più.
- **Il nero e la drammaticità.** La flanella fa da fondo scuro solo per eventi e social; il resto vive su tela chiara. Rinunciamo al lusso del nero pieno.
- **Una parte del calore della sartoria.** Per non scivolare nella moda abbiamo escluso tessuti, macro di stoffa, manichini e forbici in foto. Della sartoria restano gli strumenti e i gesti, mai i vestiti.
- **Il gioco con la magia del nome.** Resta fuori dal marchio: la legatura ab parla del mestiere.
