# Brief creativo: identità di marca Abra Robotics (v2)

Per tutti i direttori creativi. Data: 27/10/2026, revisione r2. Documenti di supporto in `brand/01-strategy/` (competitor, personas, brand platform, spazi). Regole vincolanti in `brand/REGOLE.md`. Territori in `brand/02-directions/TERRITORI.md`.

## Contesto

Abra Robotics è una startup italiana di due fondatori (Niccolò Mazzoleni, commerciale e strategia; Giovanni Pitton, tecnica). Fornisce robot avanzati di diversi produttori e forme, oggi soprattutto Unitree. Il valore di Abra sta nei servizi che accompagnano il robot: assessment, simulazione e digital twin, POC a fasi, sviluppo software con l'AI, formazione, assistenza, noleggio a giornata di un umanoide che parla per eventi e fiere. Il primo ordine vinto è SACMI: un quadrupede per una tesi in azienda, accompagnato da manuale tecnico, simulatore MuJoCo, repository di codice e mappatura LiDAR. La consegna fisica è prevista il 29/10/2026.

## Problema di marca

Oggi Abra sembra un rivenditore Unitree: tre loghi scollegati (uno in un font da fantascienza con la A senza traverso), accento viola da estetica AI, solo foto ufficiali Unitree, sito organizzato per famiglie di robot. Il marchio tace sul metodo, cioè sulla ragione per cui un cliente dovrebbe scegliere Abra anziché comprare la stessa scatola altrove.

## Obiettivo

Un'identità che faccia percepire Abra come il partner tecnico serio a cui affidare il primo progetto di robotica avanzata, che resti riconoscibile con robot di qualunque produttore e che il team di due persone possa applicare da solo.

## Pubblico, in ordine di peso

1. **Direttore R&D o operations di un'azienda manifatturiera** (packaging, ceramica, automotive, tipo SACMI). **Definisce la solidità del marchio.** Ha già robot industriali, è scettico sugli umanoidi, deve portare un numero alla direzione. Spesso arriva tramite un suo tecnico o un tesista.
2. **Responsabile di laboratorio universitario.** **Porta volume** e fa da ponte verso le aziende. Compra con fondi vincolati, confronta tre offerte, vuole i tesisti operativi in poche settimane.
3. **Event o brand manager** che noleggia per una giornata il G1 che parla del marchio (LLM e RAG sui contenuti del cliente). **È l'applicazione più visibile del metodo.** Data fissa, paura della figuraccia davanti al cliente. Attenzione: questa persona è in gran parte ipotesi da validare con 3 a 5 interviste vere.

Accanto a loro: ufficio acquisti, HSE, IT/OT, tesisti. Leggono documenti più che post.

## Insight

Chi valuta un robot avanzato teme di scoprire troppo tardi cosa farà davvero nel proprio contesto, e di restare senza materiali quando il fornitore se n'è andato.

## Promessa

**Con Abra sai cosa farà il robot nel tuo caso prima di investire, e ti resta in mano ciò che serve per andare avanti.**

| Segmento | Cosa sa prima | Cosa gli resta |
|-|-|-|
| Manifattura | Un numero misurato da portare in direzione, con il costo di ogni fase | Codice nel suo repository, simulatore, digital twin, documentazione |
| Laboratorio | Specifiche reali, tempi di consegna, pacchetto di sviluppo | SDK, ROS 2, simulatore e manuale pronti per i tesisti |
| Eventi | Prova generale con copione e base di conoscenza approvati prima della data | Copione e base di conoscenza approvati, video dell'evento |

Posizionamento raccomandato (in attesa di approvazione dei fondatori): "Prima la prova". Abra è il partner di robotica applicata che sviluppa casi d'uso su misura con l'AI e li misura in simulazione e su robot vero prima dell'investimento, per fasi con criteri scritti, sulla piattaforma adatta al compito, lasciando al cliente codice e documentazione.

## Prove, con i limiti da rispettare

- Metodo a fasi P0 a P5 con criteri di accettazione in ogni offerta industriale.
- SACMI: Go2 con LiDAR, simulatore MuJoCo, manuale rev 1.1, repository GitHub condiviso con i tecnici del cliente. Il nome si usa solo con consenso scritto; il logo SACMI mai.
- Raccomandazioni indipendenti: base su ruote consigliata al posto dell'umanoide quando era più sicura e certificabile.
- Prezzi pubblici: listino online. Assessment da 3.500 euro solo se confermato dai fondatori.
- Limiti dichiarati: payload continuativo del G1 sotto i 2 kg per braccio e batteria circa 2 ore. Sono valutazioni di Abra da prove interne senza protocollo scritto: nei mockup vanno marcate come esempio.

Oggi **nessun progetto "misurato prima dell'acquisto" è concluso**: la promessa si mostra come metodo. Mancano foto e video propri, scheda limiti, casi studio, un laboratorio da visitare: il sistema deve prevedere dove andranno.

**Regola per i mockup**: numeri di prova, verbali, criteri di accettazione e citazioni inventati portano la dicitura "Esempio". Nessun mockup deve sembrare un documento reale di un cliente reale. L'importo di 245.000 euro citato sotto resta fuori da ogni mockup.

## Personalità e voce

**Nucleo fisso, uguale per tutti i territori**: l'ingegnere di fiducia. Franchezza sui limiti (si dicono nella stessa pagina delle prestazioni), numeri con unità di misura, un fatto verificabile per ogni promessa, italiano chiaro, regole di copy di `REGOLE.md`.

**Registro variabile, che ogni territorio declina a modo suo**: può essere asciutto come una targa dati, colto e caldo come un'edizione Olivetti, annotato come un quaderno di laboratorio, scandito come una regia teatrale, oppure altro per il wildcard. In ogni caso il nucleo fisso vale per tutti.

## Mandatory

- Nome: **Abra**. Ammesse solo le varianti Abra, Abra Robotics, monogramma. "Abra Robotics" al primo contatto; "Abra" dopo. Il monogramma sostituisce la "Λ" attuale e l'emoji del mago, e regge a 16 e 32 px e come adesivo sul robot.
- Abra non va presentata come rivenditore Unitree, né per "3 famiglie di robot", né come fornitore di isole turn key. Unitree è partner tecnologico: citato a testo, mai in lockup.
- Il sistema funziona senza un robot nell'immagine e con robot di qualunque produttore.
- Font con licenza chiara (Google Fonts, OFL, open source o commerciali con costo e licenza), utilizzabili anche nel web e incorporati nei PDF. Font OFL in `.claude/skills/canvas-design/canvas-fonts/`.
- Immagini ufficiali Unitree solo come segnaposto dichiarato. Nessuna foto di persone reali presa online, nessun logo di terzi rielaborato. Nessuna immagine generata senza istruzione esplicita.
- **Produzione**: sito statico in HTML e CSS senza framework; preventivi generati come HTML e convertiti in PDF dal Company Brain, con logo e font incorporati; post e caroselli prodotti dal team con modelli semplici (HTML o editor online). Lingue: italiano principale, inglese per i contatti internazionali e per la sezione `/en` del sito.
- **Regole di copy, ovunque, anche nei mockup**: niente em dash, doppio trattino, en dash come inciso, tilde; niente contrapposizioni ("non X, ma Y" e simili); niente simmetrie ("più X, più Y", "gli altri fanno X, noi Y"); niente terne ritmiche da slogan né coppie di aggettivi; la parola "concreto" è bandita; niente gergo da startup tradotto; niente chiusure punchy di 2 o 3 parole; nessuna enfasi verbale sul futuro. Headline all'imperativo con il beneficio esplicito. "Il futuro in scena" è il nome di lavoro di un territorio e non diventa copy.

## Cosa evitare

- I cliché di `REGOLE.md`: blu elettrico su nero, glow, neon, particelle, griglie tron, circuiti, cervelli luminosi, mani che si toccano, occhi luminosi, globi di rete, gradienti viola.
- Acrobazie del robot: balli, capriole, combattimenti, effetto sorpresa. Sono invece ammessi regia, luce reale, scala, ritmo, allestimento e presenza scenica.
- Verbale: "robot per gli umani", "persone e robot insieme", "il futuro di", "soluzioni smart", "a 360 gradi", "chiavi in mano", "Physical AI" come slogan.
- **Il vicino già occupato, territorio per territorio** (dalla rilevazione in `01-competitor.md`):
  - A, precisione: griglia svizzera con mono tecnico e grigio caldo è Agility (Diatype Mono); antracite con rosso e grotesk tecnico è ANYbotics.
  - B, umanesimo: salmone e "migliorare la vita delle persone" è PAL Robotics; robot bianco in un interno domestico beige è Fourier.
  - C, laboratorio: catalogo per la ricerca è Generation Robots; il digital twin in blu cobalto è Eagleprojects; il blu da cianotipia si avvicina a Comau.
  - D, scena: spazio stellato è Unitree; piste e vortici di luce sono AgiBot; nero pieno con luce radente è Generative Bionics; macro di materiale da moda è Figure.
  - E, wildcard: la magia del nome si può usare; l'emoji del mago e gli effetti speciali restano esclusi.

## Opportunità e spunti liberi

Gli spazi liberi rilevati in `01-competitor.md §6` sono opportunità da cogliere a scelta: palette industriale calda, tipografia fuori dal grotesk di default, fotografia documentaria in reparti italiani, linguaggio del documento tecnico. Un territorio può legittimamente scegliere una palette fredda o una griglia svizzera, se evita il vicino occupato. Altri stimoli, uno per famiglia:
- precisione: targhe dati di macchina, quote, tolleranze;
- umanesimo: la tradizione Olivetti, il colore pittorico, le persone al centro dell'immagine;
- laboratorio: quaderni, versioni, note a margine, l'errore visibile;
- scena: la scala di un umanoide in un padiglione, il taglio di luce di un palco, il ritmo di un allestimento culturale;
- wildcard: la tensione tra il nome Abra (magia) e la promessa (misura).

## Applicazioni richieste

1. Hero della home.
2. Preventivo premium: copertina e una pagina interna, cioè la pagina delle fasi con i criteri di accettazione.
3. Post LinkedIn sulla consegna del Go2 a SACMI, in versione nominativa e in versione anonima (pronta finché manca il consenso scritto, senza dettagli che rendano riconoscibile il cliente).
4. Copertina di un reel Instagram sulla demo del G1 che parla con il pubblico.
5. Biglietto da visita.
6. Stand o totem per il noleggio del G1.
7. Badge o livrea per robot e flight case.
8. Avatar social e favicon.

Facoltativo: copertina e doppia pagina del manuale tecnico consegnato al cliente.

## Criteri di successo

- **Test dei 5 secondi** con 5 persone del target per direzione, su hero e copertina del preventivo: almeno 4 su 5 dicono che Abra prova o misura il robot prima dell'investimento e nominano cosa si ottiene.
- **Eventi**: sul totem, almeno 4 su 5 capiscono che si noleggia l'umanoide a giornata con un tecnico e come chiedere una data.
- **Laboratorio**: sull'hero o sul preventivo, almeno 4 su 5 capiscono che il robot arriva con un pacchetto di sviluppo per i tesisti.
- **Sostituzione**: togliendo ogni robot e sostituendo Unitree con un altro produttore il sistema resta riconoscibile.
- **Leggibilità**: il monogramma si legge a 16 px e come adesivo sul dorso di un Go2.
- **Coerenza**: lo stesso sistema serve l'offerta da 245.000 euro per un POC industriale e il totem di un evento senza cambiare identità; il registro può cambiare.
- **Conformità**: zero elementi della lista "Cosa evitare", zero violazioni di copy al controllo automatico e alla rilettura.
- **Producibilità**: hero in HTML e CSS con font web, preventivo convertibile in PDF con font incorporati, post realizzabili dal team con modelli.

## Revisione r2

Modifiche richieste dalla revisione strategica (`03-reviews/brief/reviewer-strategia-r1.md`, voto 6,5) e dall'orchestratore.
- Contesto: tolto l'elenco per famiglie; riscritta la frase "X, ma Y" come affermazione diretta; corretto lo stato SACMI (consegna fisica il 29/10/2026); aggiunto il noleggio a giornata del G1 come offerta reale voluta dai fondatori.
- Pubblico: gerarchia dichiarata (manifattura per la solidità, laboratori per il volume, eventi come applicazione); persona eventi segnalata come ipotesi.
- Insight riformulato come tensione unica; promessa con "prima di investire" e tabella "cosa sa prima / cosa gli resta" per segmento.
- Prove: dichiarato che nessun caso misurato prima dell'acquisto è concluso; prezzi condizionati alla conferma dei fondatori; payload del G1 indicato come valutazione interna senza protocollo; regola "Esempio" per i mockup; versione anonima del post SACMI.
- Voce divisa in nucleo fisso e registro variabile per territorio; "nessuna enfasi sul futuro" spostata tra le regole verbali; "Il futuro in scena" resta nome di lavoro.
- Cosa evitare: vietate solo le acrobazie del robot, ammessi regia, luce, scala e presenza scenica; aggiunto il vicino già occupato per ogni territorio.
- Spunti creativi aperti alle cinque famiglie; spazi liberi presentati come opportunità.
- Applicazioni allineate a `.claude/agents/direttore-creativo.md`; manuale facoltativo. Il canale Instagram è coperto dalla copertina del reel.
- Vincoli di produzione e lingue aggiunti; criteri di successo resi misurabili, con un criterio per eventi e uno per laboratorio; "senza cambiare registro" diventato "senza cambiare identità".
- Grafia unica "POC" in tutti i documenti.
- Fuori dal brief: `03-brand-platform.md` (insight con prove separate tra CRM, simulate ed esterne; pilastro 4 rinominato "Un laboratorio in Italia e responsabilità scritte"; tolta "misura, nessun trucco"; headline laboratori "in poche settimane"; offerta eventi; stato di approvazione), `04-spazi-posizionamento.md` (gerarchia, territorio D ammesso, stato di approvazione), `01-competitor.md` (SIR sul sito corretto sir-mo.it, Oversonic rilevato, ricerca sul noleggio per eventi, quinta schermata).
- Non chiuso: l'approvazione dei fondatori sul posizionamento e una mappatura visiva di noleggiatori italiani per eventi, che due ricerche non hanno trovato.

## Note dell'orchestratore (dopo revisione r2, voto 8,0)

- Posizionamento "Prima la prova" e promessa: proposta in attesa del sì dei fondatori. I direttori la trattano come fissa; se cambia, si adattano i testi, non i sistemi visivi.
- Totem e materiali eventi: tecnico incluso, trasporto e prezzo del noleggio sono contenuti d'offerta da definire; nei mockup vanno marcati "Esempio".
- Payload e batteria del G1 sono valutazioni interne: nei mockup solo come "Esempio", mai come dato pubblico finché non esiste la scheda limiti.
