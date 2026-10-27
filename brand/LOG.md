# LOG progetto brand identity Abra Robotics

Branch `feat/niccolo-brand-identity`, worktree `~/Abra-Robotics-brand` (il checkout principale resta su main).

## Fase 0: inventario (27/10/2026)

**Fatto**
- Stato attuale in `00-inventory/stato-attuale.md`: tre loghi non coordinati (Nasalization maiuscolo, "Λ" in cerchio, grotesk con pallino arancio), accento viola, Satoshi, fotografia solo Unitree/RoboStore, sito impostato da catalogo per famiglie di robot.
- Capacità in `00-inventory/capacita.md`. Installate come skill di progetto: canvas-design, theme-factory, algorithmic-art (anthropics/skills), guideline-generation, brand-voice-enforcement, competitive-brief, brand-review (knowledge-work-plugins).

**Decisioni**
- Lavoro in un worktree separato per non toccare il checkout main usato da altre sessioni.
- Le fonti strategiche principali sono già pronte: `~/dev/abra/ricerca/` (mappa aziende, organigrammi, obiezioni, interviste simulate, concorrenza, fonti interne del Company Brain).

**Crediti**
- Higgsfield: saldo 0,5 crediti (piano free). Costo stimato per immagine 0,25. Fabbisogno Fase 2: circa 7 crediti. Nessun credito speso.

**Dubbi aperti / da decidere**
- **Serve una ricarica Higgsfield (circa 10 crediti) per i mood fotografici.** Senza, procedo con direzione fotografica descritta e composizioni SVG/HTML su cutout ufficiali come segnaposto.
- Figma MCP non autenticato: utile per consegnare sorgenti modificabili.
- Licenza web di Nasalization (logo attuale) da verificare se il vecchio logo resta online nel frattempo.

## Fase 1: strategia (27/10/2026)

**Fatto**
- `01-strategy/01-competitor.md`: 18 home page rilevate dal vivo (Playwright con Chrome di sistema: font calcolati, colori, screenshot in `01-strategy/img-competitor/`, solo uso interno). Mappa dei cliché visivi e verbali, spazi liberi. Nuovi concorrenti emersi: SIR (Modena, partner italiano di AgiBot) e La Casa degli Umanoidi (Brescia).
- `02-personas.md`, `03-brand-platform.md`, `04-spazi-posizionamento.md`, `05-brief-creativo.md`.

**Decisioni**
- Spazio raccomandato: "Prima la prova" (misura in simulazione e al banco prima dell'investimento). "Il sapere resta a voi" entra come pilastro e prova; "piattaforma giusta" come metodo; eventi come applicazione.
- Architettura del nome: Abra Robotics al primo contatto, Abra dopo, monogramma proprietario anche come adesivo sui robot. Unico nome proprio di servizio: Laboratorio Abra.

**Dubbi aperti**
- Consenso SACMI alla pubblicazione del caso; foto e video propri mancanti.
- Pilastro 4 (SLA, test di rete, dossier CE, sede unica) da produrre prima di comunicarlo.
- Peso del segmento eventi; contenuto e prezzo del noleggio a giornata del G1 da definire.
- Ricerca di anteriorità sul marchio "Abra" (collisioni note: app finanziaria Abra, ABRA Software).

## Fase 1, brief v2 (27/10/2026)
- Brief portato a v2 dopo la revisione strategica (6,5/10) e le correzioni dell'orchestratore: noleggio a giornata del G1 come offerta reale, territorio D ammesso senza acrobazie, applicazioni allineate a `direttore-creativo.md`, voce in nucleo fisso e registro per territorio. Aggiornati anche platform, spazi, competitor (SIR su sir-mo.it, Oversonic) e personas. Dettagli in "Revisione r2" in fondo al brief.

### Revisione del brief
- Round 1 reviewer-strategia: 6,5/10 (brief troppo chiuso sul territorio "documento tecnico", prove deboli, alcune violazioni di copy).
- Round 2: 8,0/10. Brief approvato dal revisore; correzioni minori applicate dall'orchestratore.
- **Da confermare da te (non blocca il lavoro):** promessa "Con Abra sai cosa farà il robot nel tuo caso prima di investire" e posizionamento "Prima la prova". Contenuti e prezzo del noleggio G1. Consenso SACMI alla pubblicazione del caso (per questo il post esiste anche in versione anonima). Prezzi assessment 3.500 euro e digital twin circa 10.000 euro.

## Fase 2: direzioni creative v1 (27/10/2026)

**Fatto**
- Agenti in `.claude/agents/`: brand-strategist, direttore-creativo (uno per territorio), 5 revisori + reviewer-finale, tutti con modello Opus.
- Cinque direzioni consegnate in parallelo, ciascuna completa (concept, logo SVG in 5+ versioni con test 16/32 px, palette WCAG, tipografia OFL, sistema, foto, motion con logo animato, voce, 9 mockup HTML+PNG, presentazione.html, autocritica):
  - **A. Riferimento A** (Precisione industriale): triangolo del riferimento di misura ISO dentro la A; alluminio, grafite, verde "misurato" e giallo "limite dichiarato"; Barlow.
  - **B. Misura d'uomo** (Umanesimo italiano): "a" a doppia pancia montata da tre pezzi con giunto a vista; avorio, rosso `#BB3B26`, ocra, verderame; Newsreader e Hanken Grotesk.
  - **C. Nota a margine** (Laboratorio aperto): A in serif scientifico con richiamo di annotazione al posto del traverso; carta, inchiostro, evidenziatore giallo; STIX Two e DM Mono.
  - **D. Prova generale** (Futuro in scena): A come boccascena con palco ambra; velluto rosso bruno, luce tungsteno, stucco; Archivo in tre larghezze.
  - **E. Cartamodello** (Wildcard): Abra come modellista che prende le misure e consegna il modello; A con traverso a punto d'imbastitura; tela, flanella, giallo metro; Bricolage Grotesque.

**Decisioni**
- Nessuna immagine generata (saldo 0,5 crediti): fotografia descritta con shot list e prompt pronti; robot nei mockup = foto ufficiali Unitree dichiarate come segnaposto. Dati inventati marcati "Esempio". Post SACMI in versione nominativa e anonima.
- Font tutti OFL, costo zero.

**Crediti**: 0 spesi. Stima per completare i mood (5 direzioni x 5 immagini) circa 6-7 crediti.

**Dubbi aperti**
- D ed E condividono un giallo/ambra caldo e il lessico "prova": da verificare nella revisione la distanza reale.
- Immagini G1 disponibili a bassa risoluzione (749 px): servono foto proprie.

## Fase 3: revisione round 1 (27/10/2026)

**Fatto**: cinque revisori indipendenti (strategia, art director, produzione, buyer panel, marchio) su direzioni anonime. Tabella completa in `03-reviews/round1-sintesi.md`.

| Dir. | Strat. | AD | Prod. | Buyer | Marchio | Media |
|-|-|-|-|-|-|-|
| A Riferimento A | 7,5 | 6,7 | 8,0 | 7,2 | 5,2 | 6,9 |
| B Misura d'uomo | 7,2 | 5,9 | 6,7 | 7,0 | 6,2 | 6,6 |
| C Nota a margine | 7,7 | 7,0 | 7,4 | 7,8 | 6,2 | 7,2 |
| D Prova generale | 6,5 | 6,0 | 7,7 | 6,8 | 5,0 | 6,4 |
| E Cartamodello | 7,0 | 6,1 | 7,6 | 7,0 | 5,4 | 6,6 |

**Decisioni**: tutte alla v2. Assegnato a ogni direzione un colore firma esclusivo (il giallo/ocra era in tutte e cinque, B e D quasi identiche); simbolo da rendere proprietario a 16 px (4 su 5 usavano una A maiuscola isolata); headline proprie; font locali statici per i PDF; biglietti sopra 6 pt; post SACMI anonimo davvero anonimo.

**Dubbi aperti**: il revisore marchio segnala rischio alto sul nome "Abra" nelle classi 9 e 42 (ABRA Software, abra.com). Consiglio: depositare prima il marchio figurativo e fare una ricerca di anteriorità professionale prima di depositare la parola. Dettagli in `03-reviews/marchio-nome-abra.md`.

## Fase 3: v2 e revisione round 2 (27/10/2026)

**Fatto**: v2 delle cinque direzioni (interrotte una volta dal limite di utilizzo, riprese alle 15:24), poi round 2 dei cinque revisori. Dettagli in `03-reviews/round2-sintesi.md`.

| Dir. | Strat. | AD | Prod. | Buyer | Marchio (senza nome) | Media |
|-|-|-|-|-|-|-|
| A In squadra | 7,8 | 7,0 | 8,9 | 7,6 | 6,2 (6,8) | 7,5 |
| B Montato a vista | 7,3 | 5,9 | 8,4 | 7,8 | 6,2 (6,8) | 7,1 |
| C Nota a margine | 7,8 | 7,1 | 8,0 | 8,0 | 5,6 (6,0) | 7,3 |
| D Prova generale | 7,0 | 6,1 | 8,6 | 7,8 | 5,2 (5,5) | 6,9 |
| E Cartamodello | 7,3 | 6,9 | 8,6 | 7,8 | 5,6 (6,0) | 7,2 |

**Decisioni: scartate B e D dopo due round.**
- B: l'art director le dà 5,9 in entrambi i round. Correggendosi ha perso il riferimento Olivetti ed è diventata un sito SaaS generico; il logotipo converge con C e a 16 px si legge "@".
- D: ha la media più bassa nei due round, l'idea teatrale si è ridotta a una cornice ad arco, il magenta è vicino a quello di Deutsche Telekom (colore protetto come marchio) e il robot mostrato non è il G1 a noleggio. Il suo logotipo ad archi resta un possibile spunto per un ibrido.
- A, C ed E vanno al round 3 (ultimo), ciascuna con un verbo proprio per le headline.

**Nota sul criterio marchio**: "Abra" prende 4/10 in tutte le direzioni per le anteriorità nelle classi 9 e 42 (ABRA Software, abra.com, e "abrdn" per i logotipi minuscoli). È un vincolo del cliente, quindi riporto anche la media senza quel criterio.

**Crediti**: 0 spesi.

## Fase 3: v3 e round 3 (27/10/2026)

| Dir. | Strat. | AD | Prod. | Buyer | Marchio (senza nome) | Media |
|-|-|-|-|-|-|-|
| A In squadra | 8,2 | 7,4 | 8,6 | 7,8 | 6,2 (6,8) | 7,6 |
| C Nota a margine | 7,7 | 7,6 | 8,7 | 8,2 | 6,2 (6,8) | 7,7 |
| E Cartamodello | 7,3 | 6,6 | 8,6 | 7,6 | 6,2 (6,8) | 7,3 |

**Esito**: raggiunto il limite di 3 round. Nessuna direzione supera la soglia piena; il blocco comune è il revisore marchio (rischio del nome "Abra" e segni basati su lettere). Strategia giudica A "pronta per il cliente", il buyer panel giudica C "pronta". E è peggiorata all'art director per la legatura che si legge "dbra". Dettagli in `03-reviews/round3-sintesi.md`.

**Prossimo passo**: reviewer-finale su A, C, E insieme, poi correzioni bloccanti e Fase 4.

## Revisione finale e correzioni (27/10/2026)

**Fatto**: reviewer-finale in `03-reviews/finale.md`. Matrice di distanza: A e C sono la coppia più distante (2,0); A ed E sono troppo vicine (3,2). Voti "pronta per il cliente": A 7,5, C 7,5, E 5,5.
**Decisioni**: E scartata come direzione (il logotipo si legge "dbra"; correggerlo la avvicinerebbe ad A). La sua copertina del preventivo a timeline ("Quando arrivano i numeri") resta come ibrido da innestare. In presentazione vanno C e poi A; il revisore preferisce C con la timeline di E.
- A v3.1: correzioni bloccanti fatte (reel, totem, verde allineato a Pantone 348 C, favicon, regola dei titoli allentata).
- C v3.1: correzioni bloccanti in corso al momento dello stop per limite di utilizzo.
- `04-final/prossimi-passi.md` scritto.

**Da fare**: chiudere C v3.1, ibrido "C con copertina a timeline", `04-final/index.html` di confronto, raccomandazione finale.
