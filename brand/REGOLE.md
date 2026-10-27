# Regole vincolanti per tutti gli agenti del progetto brand Abra

## Chi è Abra
Startup italiana fondata da Niccolò Mazzoleni (marketing, commerciale, strategia) e Giovanni Pitton (tecnica), 50/50. Distribuisce robot Unitree (umanoidi G1, H1/H2, R1; quadrupedi Go2 e successori; soluzioni industriali) ma il valore sta nei servizi: sviluppo di casi d'uso custom con AI, POC in azienda, programmazione su SDK/API di Unitree e di altre piattaforme, assistenza, consulenza anche a chi ha comprato il robot altrove.
Positioning di partenza: "We help companies adopt robotic solutions and develop custom-made use cases with AI".
Segmenti: (1) università e laboratori R&D; (2) aziende manifatturiere e industriali (POC su postazioni produttive, magazzino, manipolazione); (3) eventi, fiere e brand che vogliono un umanoide che intrattiene e parla del loro marchio (G1 con LLM e RAG, noleggio a giornata).
Canali: sito (tutti i lead arrivano in organico da lì), LinkedIn, Instagram, video ads, preventivi PDF premium via mail.

## Vincoli di posizionamento
- Mai descrivere Abra come "3 famiglie di robot: umanoidi, quadrupedi, cobot".
- Mai presentare Abra come semplice rivenditore Unitree. Unitree è partner tecnologico; l'identità deve reggere anche con altre piattaforme.
- Abra non consegna isole robotiche turn-key: vende robot, sviluppo, POC, servizi.
- Il nome "Abra" resta. Ammesse solo varianti di naming del marchio (Abra, Abra Robotics, monogramma).

## Regole di copy (tutte le lingue, anche nei documenti di lavoro)
- MAI il carattere em dash (—) né il doppio trattino (--). Usa virgola, due punti, punto o parentesi. Vale anche per en dash usato come trattino di inciso.
- MAI la tilde (~): scrivi "circa".
- MAI formule contrapposte: "non X, ma Y", "X, not Y", "il problema non era X, era Y", "niente X. Niente Y.", "meno X, più Y".
- MAI strutture simmetriche che partono dal soggetto: "Più X, più Y", "Gli altri fanno X, noi facciamo Y".
- MAI terne ritmiche "X, Y e Z" usate come slogan; niente coppie di aggettivi da slogan; la parola "concreto" è bandita.
- Headline preferibilmente all'imperativo, e il lettore deve capire cosa ottiene.
- Tono corporate e credibile verso aziende B2B italiane. Niente gergo da startup americana tradotto (no "game changer", "rivoluzionare", "next level", "potenziare", "sbloccare il potenziale", "il futuro è qui", "disruptive").
- Niente chiusure punchy di 2-3 parole tipiche dei testi generati.

## Cliché visivi da evitare
Robot blu elettrico su sfondo nero, cervelli luminosi, mani robotiche che toccano mani umane, circuiti stampati, gradienti viola, effetti neon futuristico, glow, particelle, griglie prospettiche tron, "sguardo del robot" con occhi luminosi, globi di rete.

## Diritti
- Solo font con licenza chiara: Google Fonts / OFL / open source, oppure commerciali con costo e licenza indicati.
- Nessun asset protetto, nessun logo di terzi rielaborato, nessuna foto di persone reali presa online.
- Le immagini ufficiali Unitree nel repo (`images/official/`, cutout `*-nobg.png` in `images/` e `prodotti/`) si possono usare solo come segnaposto nei mockup, dichiarandolo.
- Il logo SACMI non va usato nei mockup: il post LinkedIn cita SACMI solo a parole.

## Tecnica
- Lavori dentro `/Users/niccolomazzoleni/Abra-Robotics-brand` (git worktree, branch feat/niccolo-brand-identity). Non fare commit: li fa l'orchestratore. Non toccare file fuori da `brand/` e `.claude/agents/`.
- Nessun deploy, nessuna pubblicazione, nessuna mail, nessun post.
- Crediti generativi (Higgsfield): saldo attuale 0,5 crediti. NON generare immagini salvo istruzione esplicita dell'orchestratore.
- Font OFL disponibili offline in `.claude/skills/canvas-design/canvas-fonts/`. Per le presentazioni puoi caricare Google Fonts via link, oppure copiare i file .ttf OFL nella tua cartella (con il file OFL).
- Screenshot e controllo errori: `node brand/_tools/shot.js <file.html> <out.png> [w] [h] [fullPage 0|1]` (Playwright con Chrome di sistema, `chromium.launch({channel:'chrome'})`; il Chromium di Playwright non è installato).
