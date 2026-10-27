# 02. Personas

Fase 1, brand strategy. Data: 27/10/2026.

Tre personas sintetiche, una per segmento. Ogni scheda separa ciò che viene da **dati reali** (CRM, mail e call nel Company Brain, sintetizzati in `ricerca/10-fonti-interne.md`, citato [R10]) da ciò che viene dalle **interviste simulate** (`ricerca/06-*`, citate [R06-n] con il numero dell'intervista) e dalle mie **ipotesi**, marcate [IPOTESI]. Nomi e dettagli biografici sono inventati. Nessuna persona reale è descritta.

Le altre ricerche citate: [R02] organigrammi, [R03] maturità, [R04] budget e incentivi, [R05] obiezioni, [R07] ascolto mercato, [R09] palcoscenici.

## Il quadro comune

- **Chi apre la porta non è chi firma.** In azienda scrive un tecnico (Smart Factory & ICT Manager, Hw & Sw Design Manager, referente di progetto e tirocinio); poi decidono una riunione investimenti, un'amministrazione o l'ufficio acquisti [R10 §6], [R02 §1].
- **Le domande vere sono operative**: tempo ciclo, batteria, consegna, condizioni di pagamento, prese elettriche [R10 §8].
- **Vedere il robot fa avanzare la trattativa**: visita in sede, demo e video sono la richiesta più frequente dopo il prezzo [R10 §8].
- **Il valore percepito sta in ciò che resta**: manuale, simulatore, repository [R10 §4.3].
- **Il tema "fornitore cinese" arriva come requisito tecnico** (CE, rappresentante UE, niente cloud del produttore, firmware); nessun cliente lo ha posto per iscritto come obiezione [R10 §5].

## Persona 1. La responsabile di laboratorio universitario

**Prof.ssa Chiara Rinaldi**, 49 anni, professoressa associata di robotica, responsabile di un laboratorio in un dipartimento di ingegneria (centro Italia). Coordina due dottorandi, una decina di tesisti l'anno, un progetto europeo e due convenzioni con aziende del territorio.

**Base nei dati**: responsabile di laboratorio Univaq (offerta H2 Plus da 109.125 euro), ricercatore Unipd (Go2 Edu Plus con LiDAR, chiede MePA), Aarhus (accessori, "one time or subscription?"), MADE (ricambi G1 su fondi NextGenEU), Fraunhofer Italia persa per "documentazione ufficiale" più completa [R10 §2.2, §2.3]. Ticket mediano della ricerca circa 27.600 euro [R10 §2.1]. Profilo arricchito con [R06-33] (professore che collabora con le aziende) e [R06-31] (ricercatrice di Competence Center).

| Voce | Contenuto |
|-|-|
| **Contesto** | Compra con fondi vincolati (CUP, progetti europei, residui PNRR in chiusura) e con scadenze di rendicontazione [R04 §5.5], [R10 §2.2]. Sa esattamente quale modello vuole: altezza, mani, LiDAR, ROS 2. Il robot serve a ricerca, tesi e visibilità del laboratorio. Valuta tre preventivi per lo stesso hardware. |
| **Cosa la convince** | Un'offerta completa al primo invio: dati fiscali, garanzia, tempi di consegna scritti, abilitazione MePA, documenti per la rendicontazione. Un pacchetto software che fa partire i tesisti in settimane: manuale in italiano, repository che gira, simulatore (il modello SACMI) [R10 §4.2]. Uno scambio con le aziende: "Portatemi un problema industriale vero e io vi porto due tesisti" [R06-33, simulata]. |
| **Cosa la spaventa** | Ritardi che fanno saltare la rendicontazione. Un robot che arriva e resta nell'armadio perché nessuno sa programmarlo. Un fornitore che si presenta come esperto di ricerca senza esserlo [R06-33]. Pagare più di un altro rivenditore per la stessa scatola: sull'hardware nudo compra sul prezzo [R05 §11]. |
| **Come decide** | Decide lei sul budget del laboratorio, ma passa da ufficio acquisti, MePA o affidamento diretto con confronto di offerte [R10 §5 punto 8]. Tempi da 1 a 3 mesi. Il suo voto pesa anche fuori: tesisti e aziende partner seguono le sue scelte [R02 §3.12]. |
| **Dove ci incontra** | Ricerca Google per modello e prezzo ("unitree h2 price", "unitree ros2") [R10 §7.1]; risposte di ChatGPT (due lead su sei con origine nota) [R10 §7.3]; colleghi e conferenze (I-RIM, ERF); MePA; LinkedIn per verificare chi siamo. |
| **Cosa deve vedere in 5 secondi** | Che Abra fornisce il robot con un pacchetto di sviluppo pronto per la ricerca (SDK, ROS 2, simulatore, manuale), con prezzo e tempi chiari, e che lavora già con università e aziende. |

**Frase guida** [IPOTESI]: "Il robot lo trovo ovunque. Mi serve chi lo fa funzionare entro il semestre e mi dà le carte giuste."

**Ruolo nella strategia di marca**: è la porta più frequente (volume alto, ticket basso) e il ponte verso le aziende, come nel caso SACMI nato da una tesi [R10 §4.3]. Il marchio deve reggere nel suo mondo: rigore, documentazione, nessuna spettacolarizzazione.

## Persona 2. Il direttore operations e R&D di un'azienda manifatturiera (tipo SACMI)

**Ing. Marco Ferrari**, 52 anni, Direttore R&D e Industrializzazione in un gruppo emiliano di macchine automatiche (circa 800 milioni di fatturato, stabilimenti in Italia e all'estero). Ha sotto di sé l'ufficio tecnico, un laboratorio prototipi e un Innovation Manager. Riporta all'AD.

**Base nei dati**: SACMI (tesi con Go2, manuale, MuJoCo, digital twin, SLAM; frizioni solo amministrative; il tecnico pensa già a LiDAR propri e "bracci") [R10 §4]; PM SPA (5.000 pezzi al giorno, ciclo 15 s "al netto di ricariche"), Bucci ("siamo ancora in fase esplorativa"), NTK ("riunione investimenti"), Montemaggi ("prima di firmare vorrei visitare la vostra sede"), Sogefi (buyer come interlocutore), ATS (chi possiede il software) [R10 §2.2, §5]. Profilo arricchito con [R06-1] (Head of R&D packaging), [R06-6] (Direttore Tecnico con POC fallito), [R06-21] (CTO), [R06-17] (Direttore Tecnico costruttore di macchine per ceramica).

| Voce | Contenuto |
|-|-|
| **Contesto** | Ha già robot industriali e cobot in casa: sa tutto di celle, sicurezza e payback [R03 §3]. Umanoidi e quadrupedi li conosce da video e fiere, con forte curiosità e forte scetticismo [R03 §3]. I suoi clienti (ceramica, packaging) iniziano a chiedere cosa farà con la "Physical AI" [R07 §2]. Nel suo gruppo un POC di AMR si è fermato due anni fa perché nessuno in reparto se ne è preso carico [R03 §5], [R06 blocchi 2 e 5]. |
| **Cosa lo convince** | Un percorso a fasi con costi e criteri di accettazione scritti, in cui la prima fase costa poco e gli dà un numero da portare all'AD (assessment da 3.500 a 5.000 euro, digital twin circa 10.000 euro) [R10 §3]. La simulazione prima dell'acquisto, con confronto onesto tra umanoide, cobot e base su ruote [R05 §12]. Codice, manuale e simulatore che restano all'azienda anche se il fornitore sparisse [R05 §8]. Un caso di un'azienda come la sua, con il tecnico del cliente che ne parla. Un laboratorio da visitare, sempre lo stesso [R05 §8]. L'iperammortamento 2026-2028 per la parte hardware interconnessa [R04 §5.2]. |
| **Cosa lo spaventa** | Un altro POC che finisce in un angolo [R06-6]. Una startup che fra due anni non c'è più [R05 §8]. Diventare "fabbricante dell'insieme" con il Regolamento Macchine dal 20 gennaio 2027 [R05 §3]. Un robot cinese collegato alla rete di stabilimento: il CISO e l'IT/OT lo fermano [R05 §6]. Fare brutta figura con l'AD per aver portato un giocattolo. |
| **Come decide** | Sotto i 30 a 50 mila euro firma lui o il suo budget di funzione (tesi, assessment, primo POC). Sopra serve AD o comitato investimenti, con HSE, IT/OT e acquisti come veti [R06 blocco 1 punto 5], [R02 §4]. Budget dell'anno dopo deciso tra ottobre e dicembre [R02 §4]. Tempi da 3 a 12 mesi. |
| **Dove ci incontra** | Tramite un suo tecnico o un tesista che ci ha trovati online [R10 §6]; fiere SPS Italia e MECSPE; MADE e BI-REX; Innovation Post; passaparola di distretto e filiera dei fornitori [R09], [R06 blocco 2 punto 4]; LinkedIn la sera [R06-1]. |
| **Cosa deve vedere in 5 secondi** | Che Abra porta un robot avanzato nel suo reparto partendo da una misura (simulazione e prove), che ha già lavorato in un'azienda come la sua, e che cosa ottiene alla fine di ogni fase. |

**Frase guida** [IPOTESI, ispirata a R06-1 e R06-6]: "Che cammini l'ho visto in fiera. Adesso voglio sapere cosa farebbe nel mio reparto, quanto costa scoprirlo e cosa mi resta in mano."

**Due figure che lo accompagnano** e che il marchio deve servire con materiali propri:
- **Il tecnico sponsor** (referente di progetto, Smart Factory Manager, tesista): apre la porta, porta i numeri, ha bisogno di materiali da girare al capo [R10 §8 Persona A e B].
- **Il buyer o l'ufficio acquisti**: chiede offerta "semi ufficiale" con forbice di costi, condizioni di pagamento, documenti per l'albo fornitori [R10 §8 Persona C], [R02 §3.8].

**Ruolo nella strategia di marca**: è il cliente con il ticket più alto (POC da 110.000 a 245.000 euro [R10 §2.1]) e quello per cui il marchio deve trasmettere solidità. È anche il più sensibile al tema Unitree: il marchio deve reggere se domani la piattaforma cambia.

## Persona 3. La event e brand manager che noleggia un umanoide

**Giulia Conti**, 38 anni, Head of Brand Experience in un'agenzia di eventi milanese che lavora per marchi di automotive, moda e tecnologia (in alternativa: brand manager in azienda che organizza la propria presenza in fiera).

**Base nei dati**: è il segmento con meno dati e più rumore. Richieste reali: NEXA Italia (G1 per advertising, vuole noleggio lungo o leasing, Abra oggi non lo offre), Multimedia Industry (G1 in conto visione 3 mesi, persa come "non adatto"), QBT Sagl per il Vittoriale (G1 con app ologramma, il Presidente vuole vedere il robot prima), Proptonomy (robot per una fiera a Lione, trovato altrove), TEF in Turkmenistan (scelto un rivenditore più veloce), producer di agenzia che chiede "video reference" sui gesti e quali "mosse" o "balli" sono preimpostati [R10 §2.2, §2.3, §5]. Circa un terzo dei lead è fuori target, molti dagli eventi [R10 §8]. Il resto della scheda è [IPOTESI] da validare con 3 a 5 interviste vere.

| Voce | Contenuto |
|-|-|
| **Contesto** | Lavora su date fisse e immovibili: lancio di prodotto, stand in fiera, convention, evento in un luogo storico. Cerca un momento che faccia fotografare e parlare del marchio. Vuole un umanoide che accoglie, risponde e racconta il prodotto del cliente in italiano e in inglese (G1 con LLM e RAG sui contenuti del brand). Budget da evento, speso in giornate. |
| **Cosa la convince** | Una data confermata per iscritto e un prezzo a giornata tutto compreso (trasporto, tecnico in presenza, assicurazione, prove) [IPOTESI]. Video non montati del robot che parla del marchio di un cliente precedente. Un copione e una base di conoscenza approvati prima dell'evento, con risposte controllate. Possibilità di vederlo dal vivo prima (come il Presidente del Vittoriale [R10 §5]). Formula di noleggio o leasing per chi vuole un robot ricorrente (NEXA) [R05 §11]. |
| **Cosa la spaventa** | Che il robot cada, si blocchi o scarichi la batteria davanti al pubblico e al cliente. Che dica una cosa sbagliata sul marchio o fuori luogo (allucinazione dell'LLM). La sicurezza del pubblico in uno spazio affollato e le responsabilità civili [IPOTESI]. Le regole sulla privacy se il robot ascolta e riprende; la trasparenza verso chi parla con un'IA, obbligatoria dal 2 agosto 2026 (AI Act art. 50) [R05 §4]. Un fornitore che non risponde il giorno prima. |
| **Come decide** | Decide lei o il suo account con il cliente finale, in tempi brevi (2 a 6 settimane) e spesso sul preventivo più rapido e chiaro [R10 §2.3, TEF e Proptonomy]. Confronta con alternative non robotiche (ologrammi, installazioni). Chiede pagamenti a evento concluso o con anticipo ridotto [R10 §2.3, Multimedia Industry]. |
| **Dove ci incontra** | Ricerca Google e ChatGPT ("noleggio robot umanoide evento"), Instagram e reel di altri eventi, LinkedIn, passaparola tra agenzie, fiere di settore eventi [IPOTESI]. |
| **Cosa deve vedere in 5 secondi** | Il robot al lavoro in un evento vero, che parla di un marchio, con persone intorno; che il servizio è a giornata con tecnico incluso; come chiedere una data. |

**Frase guida** [IPOTESI]: "Il robot deve fare bella figura al mio cliente. Se sbaglia, la figuraccia è mia."

**Ruolo nella strategia di marca** e tensione da gestire: è il segmento più visibile (foto, reel, pubblico largo) e quello che più rischia di spingere Abra verso il robot come spettacolo, che il pubblico B2B guarda con sospetto [R07 §3 punto 6], [R08 §1.5]. Il marchio deve servirla con lo stesso registro degli altri due segmenti: affidabilità provata, copione controllato, tecnico presente. Il contenuto che nasce dagli eventi va mostrato come prova di sviluppo AI su misura (LLM e RAG sui contenuti del cliente), con il robot al lavoro tra le persone.

## Cosa hanno in comune le tre personas (utile per il brief)

| Bisogno | Ricercatrice | Direttore R&D | Event manager |
|-|-|-|-|
| Vedere prima di firmare | Demo, video tecnici | Visita in laboratorio, prova nel suo reparto | Robot dal vivo, video non montati |
| Sapere i limiti | Specifiche reali, ROS 2 | Tempo ciclo, batteria, payload misurati | Autonomia, cosa può e non può dire |
| Cosa resta | Repository, manuale per i tesisti | Codice, simulatore, digital twin, documenti | Copione, base di conoscenza, video dell'evento |
| Paura principale | Ritardi e robot inutilizzato | POC che si ferma, fornitore che sparisce | Figuraccia davanti al cliente |
| Chi blocca | Ufficio acquisti, MePA | AD, comitato, HSE, IT/OT, acquisti | Cliente finale, budget |

Il denominatore comune è uno: **togliere il rischio di scoprire troppo tardi cosa il robot sa fare davvero**. È la base dell'insight nel brief.

## Da validare con interviste vere (priorità)

1. Event manager: 3 a 5 interviste con agenzie e brand manager prima di investire in comunicazione per questo segmento.
2. Direttore R&D: chi ha detto no per ultimo nei progetti passati e perché [R05, domande finali].
3. Responsabile di laboratorio: quanto pesa il pacchetto software rispetto al prezzo hardware nel confronto tra offerte (caso Fraunhofer).
