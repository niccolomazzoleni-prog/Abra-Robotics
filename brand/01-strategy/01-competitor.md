# 01. Competitor: posizionamento, codici visivi e tono

Fase 1, brand strategy. Data di rilevazione: 27/10/2026.

## Metodo

- **Home page rilevate dal vivo** con Chromium headless (Playwright, viewport 1440x900, attesa 6 secondi): titolo, H1, font calcolati dal CSS (`getComputedStyle` e `document.fonts`), colori di fondo e dei bottoni, screenshot. Le schermate sono in `img-competitor/home-competitor-1..4.png` e servono solo come riferimento interno di ricerca (contengono loghi di terzi: non vanno usate in nessun mockup).
- **Fonti già pronte** in `/Users/niccolomazzoleni/dev/abra/ricerca/`: 08 (concorrenza italiana e riferimenti B2B esteri), 07 (ascolto mercato), 01 (mappa aziende, partner e concorrenti), 05 (obiezioni). Le cito come [R08], [R07], [R01], [R05].
- **Ricerche web integrative** su integratori italiani di umanoidi e sul noleggio per eventi (link in fondo).
- Limiti: alcune home mostrano un video o un carosello, quindi la schermata coglie un solo fotogramma. Oversonic (certificato non valido) e RobotShop (verifica anti bot) non si sono caricati. Dove descrivo un codice che non ho visto nello screenshot lo segnalo come [da verificare].

## In sintesi

1. Il settore parla con **due voci sole**: la fantascienza dei produttori cinesi (spazio stellato, neon blu, cifre giganti) e il minimalismo da prodotto di consumo dei produttori americani (umanoide bianco su fondo grigio caldo, grotesk svizzero, poche parole in inglese).
2. Chi vende e integra in Italia (Eagleprojects, Generation Robots, Comau, Reply, SIR) usa **blu corporate o arancio da e-commerce** e foto stock di impianti. Nessuno ha un codice riconoscibile legato alla robotica avanzata.
3. Le promesse verbali sono intercambiabili: "robots for humans", "people and robots, together", "il futuro dell'industria", "proven results". Nessuno parla di **misura prima dell'acquisto** né di **cosa resta al cliente** dopo il progetto.
4. Gli spazi liberi più forti: fotografia documentaria in stabilimenti italiani veri, linguaggio da documento tecnico (manuale, rilievo, verbale di prova), palette industriale calda lontana da blu, viola e arancio, tono italiano tecnico e onesto sui limiti.
5. Concorrenza nuova da presidiare: **SIR (Modena)**, integratore storico emiliano a maggioranza cinese, dal 2026 partner italiano di AgiBot per gli umanoidi, e **La Casa degli Umanoidi** (Brescia). Giocano sullo stesso territorio di SACMI e della Packaging Valley.

## 1. Distributori e integratori in Italia ed Europa

| Attore | Posizionamento | Colore | Tipografia | Foto e immagini | Logo | Tono |
|-|-|-|-|-|-|-|
| **Eagleprojects** (Perugia), distributore Unitree "Distributor of the Year" [R08] | Ingegneria per infrastrutture e reti: digital twin, BIM, droni, robot. H1: "Soluzioni smart per monitorare e gestire infrastrutture e reti" | Blu cobalto pieno su metà schermo, azzurro per le fasce numeriche | Figtree (titoli 600) e Inter, entrambi personalizzati | Tralicci e sottostazioni elettriche, foto stock di impianto | Sfera con aquila e lettering largo maiuscolo stile tech | Corporate tecnico, numeri ("2+ Petabyte di dati"), parole chiave in fila |
| **Generation Robots** (Francia, vende in Italia) | E-commerce europeo per ricerca, istruzione, industria. H1: "Robot e soluzioni robotiche per la ricerca, l'istruzione e l'industria" | Blu navy `#114078` e arancio `#FF8401` per i bottoni | Montserrat e Lato | Cutout di prodotto, banner promozionali con percentuali di sconto | Lettering giocoso bicolore | Catalogo e promozioni ("-20%", "offerta speciale") |
| **MYBOTSHOP** (Germania) | Shop, ingegneria, vendita, noleggio e supporto: "Rent a Rob!" | Verde brillante e grigi | Barlow maiuscolo 700 | Render Unitree G1 su fondo grigio | Lettering con robottino nella O | Da negozio, tutto maiuscolo, elenco di servizi |
| **Roboverse Reply** (gruppo Reply) | Integrazione di robotica avanzata nelle grandi aziende; integra Spot e Go2 per le ispezioni di Saipem [R01]. H1: "People and robots, together." | Blu notte `#151F27` e bianco, accento verde `#02D34A` | Font proprietari (sistema Reply) | Scale e ringhiere in cemento, foto atmosferica desaturata | Marchio Reply con omino in corsa | Consulenziale, frasi lunghe con "abilitiamo", "scalabilità", "affidabilità" |
| **SIR S.p.A.** (Modena), integratore dal 1984, maggioranza al gruppo cinese Wolong, partner italiano di AgiBot per gli umanoidi | "Porta i robot umanoidi nel mondo reale": hospitality, sicurezza, pulizia, mani robotiche per l'industria | [da verificare] sito .com in caricamento con navigazione azzurra su bianco | Roboto | [da verificare] | Monogramma "S" in cerchio | Da costruttore di celle, ora con umanoidi e quadrupedi AgiBot |
| **La Casa degli Umanoidi** (Brescia) con 4D Sistemi Informatici | Porta i primi umanoidi nelle imprese artigiane e manifatturiere lombarde, partner tecnologico locale per l'addestramento | n.d. | n.d. | n.d. | n.d. | Divulgativo, forum con Confartigianato |
| **Aispiria** | Distributore esclusivo italiano degli umanoidi UBTech | n.d. | n.d. | n.d. | n.d. | n.d. |

Lettura:
- Nessuno di questi attori costruisce un'identità legata al **metodo** di adozione. Vendono un catalogo (Generation Robots, MYBOTSHOP), un'ingegneria generale (Eagleprojects), una consulenza da grande gruppo (Reply) o un catalogo di umanoidi di un singolo produttore (SIR con AgiBot, Aispiria con UBTech).
- SIR è il concorrente più pericoloso nel medio periodo: è emiliano come SACMI, ha 40 anni di storia, 114 dipendenti a Modena e un produttore di umanoidi alle spalle. Il suo punto debole per un pubblico attento a dati e sicurezza è il legame proprietario con un gruppo cinese, che rende difficile presentarsi come consulente indipendente dalla piattaforma.
- Il noleggio per eventi è servito da operatori non specializzati: MYBOTSHOP in Germania, un robot fotografo a Milano (Scarlett Entertainment), apparizioni singole di umanoidi (Ameca di Engineered Arts a un evento Var Group a Rimini, RoBee di Oversonic al MIMO di Monza). Non ho trovato in Italia un operatore che noleggi umanoidi per brand con un'offerta strutturata.

## 2. Brand globali di robotica umanoide e mobile

| Brand | Posizionamento (H1 o promessa rilevata) | Colore | Tipografia rilevata | Foto e immagini | Logo | Tono |
|-|-|-|-|-|-|-|
| **Unitree** (Cina) | Produttore leader per volumi di quadrupedi e umanoidi. Hero del 27/10: "Unitree A2, Stellar Explorer" | Nero, blu elettrico `#1677FF` per i bottoni, cielo stellato | Open Sans e font di sistema cinesi | Quadrupede su roccia sotto un pianeta, render cinematografico | Lettering corsivo maiuscolo con la "I" spezzata | Epico e spettacolare, specifiche e prodotti, inglese da traduzione |
| **Boston Dynamics** (USA, Hyundai) | "Changing your idea of what robots can do." | Bianco e nero, azzurro `#0693E3` per i bottoni, giallo di Spot nel prodotto | Gotham 700 | Video in hero (non catturato), casi cliente con nome nei contenuti [R08] | Wordmark con figura stilizzata blu | Sicuro di sé, orientato all'automazione pratica, casi DHL e Coca-Cola [R08] |
| **Figure** (USA) | "The future of home help is here." Umanoide generale per casa e fabbrica | Grigio, bianco, nero | PP Neue Machina (display tecnico) e Neue Haas Grotesk | Macro del tessuto della tuta del robot, sfocato | Glifo "F" a segmenti | Manifesto, tutto maiuscolo, pochissime parole |
| **Agility Robotics** (USA) | "Humanoid robots. Proven results." Umanoide industriale Digit | Grigio caldo `#F0EEEB`, quasi nero `#292827`, teal sul robot | Agility Diatype e Diatype Mono (ABC Dinamo) | Robot in primo piano, molto grande | Wordmark con segno a chevron | Industriale e sobrio, prove in esercizio (GXO) [R08] |
| **Apptronik** (USA) | "Robots For Humans". Umanoide Apollo | Bianco, arancio `#F44C1B` per i bottoni | Helvetica Neue 300 | Umanoide bianco in magazzino con cassette | Lettering maiuscolo spaziato | Umanista e generico |
| **1X** (USA, Norvegia) | "NEO Home Robot". Umanoide domestico in vendita con deposito | Bianco caldo `#F7F7F7`, grigi | ABC Diatype | Tre robot rivestiti in maglia su fondo neutro, estetica di prodotto di consumo | "1X" minimale | Da elettronica di consumo, ordina e prenota |
| **ANYbotics** (Svizzera) | "Autonomous robotic inspection solutions". Quadrupede ANYmal per ispezione | Antracite `#171A1D`, rosso per titoli e bottoni | SimplonNorm | Impianto industriale scuro, tubi e valvole | Wordmark con "ANY" grafico | Industriale B2B, benefici operativi (uptime, costi, sicurezza) |
| **Agile Robots** (Germania) | "Driving industries forward". Bracci, mani, AMR, umanoidi, "Physical AI" in menu | Blu ardesia `#292B38`, azzurro polvere | Mont 900 | Bracci robotici bianchi su fondo scuro, desaturati | Lettering maiuscolo con segno | Corporate da grande gruppo |
| **PAL Robotics** (Spagna) | "Service Robotics to Improve People's Life". Umanoidi e robot di servizio per la ricerca | Petrolio scuro `#28303D`, salmone per i bottoni | Plus Jakarta Sans 600 | Video reel in hero | Lettering geometrico largo | Accademico e umanista |
| **Fourier** (Cina) | Robot riabilitativi e umanoidi; hero del 27/10: robot a ruote a doppio braccio in un soggiorno | Nero e beige caldo | Font di sistema | Robot bianco in interno domestico caldo, luce di lampada | Segno grafico astratto | Domestico e rassicurante |
| **AgiBot** (Cina) | Umanoidi generali; hero: "20,000" robot prodotti, arrivo in Italia con SIR | Blu elettrico, vortici di luce, glow | Font di sistema | Tre umanoidi su una pista luminosa futuristica | Wordmark tech con lettere spezzate | Celebrativo, numeri enormi |
| **Generative Bionics** (Genova, spin off IIT) | "Intelligent humanoid robot platforms. Designed in Italy. Built for the real world." Accordi con Eni e Fincantieri [R07] | Nero pieno | Clash Grotesk | Dettaglio del casco del robot in luce radente | Segno a molecola e lettering maiuscolo | Sovranità europea, in inglese, verso investitori e istituzioni [R08] |
| **Comau** (Torino) | "Il futuro dell'industria è la nostra sfida" | Blu Comau pieno, bianco | Helvetica Neue e font proprietario comau2021 | Cella robotizzata in luce blu | Quadrato blu con segno | Istituzionale, Industria 4.0 |
| **Oversonic** (Brianza), umanoide RoBee | Umanoide italiano per industria e sanità, dati tutti on premise [R07] | [da verificare] | [da verificare] | Apparizioni a eventi (MIMO Monza) | [da verificare] | Orgoglio italiano |

Lettura:
- I produttori occidentali competono sull'**oggetto**: il robot è l'eroe, ripreso grande e pulito, quasi sempre senza persone e senza contesto riconoscibile.
- I produttori cinesi competono sullo **spettacolo**: spazio, luce, numeri.
- Gli unici che mostrano un ambiente di lavoro credibile sono Apptronik e Agility (magazzino americano) e ANYbotics (impianto). Nessuno mostra un reparto italiano, un tecnico al lavoro, un banco di prova, un documento.

## 3. Integratori e costruttori italiani: cosa dicono di sé

| Attore | Promessa | Cosa manca rispetto ad Abra |
|-|-|-|
| Comau | Automazione industriale di linea, istituzionale | Nessun contenuto su umanoidi o quadrupedi [R08] |
| Reply Roboverse | Adozione strutturata della robotica avanzata nei grandi gruppi | Prezzo e taglia da grande consulenza; inaccessibile per PMI, laboratori e tesi |
| SIR | Umanoidi AgiBot nel mondo reale, integratore di celle dal 1984 | Indipendenza dalla piattaforma; racconto di casi misurati |
| Eagleprojects | Ingegneria per infrastrutture con droni e robot | Parla a utility e infrastrutture; il R&D manifatturiero resta scoperto [R08] |
| Generative Bionics, Oversonic | Umanoide italiano | Sono produttori: non integrano piattaforme di altri, non fanno tesi o POC su hardware disponibile oggi |
| La Casa degli Umanoidi, Aispiria | Distribuzione di un catalogo di umanoidi | Metodo, simulazione, documentazione |

Dalla ricerca [R08] e [R07]: nessuno dei media italiani letti cita un integratore italiano di umanoidi o quadrupedi; i casi raccontati sono esteri (BMW, Siemens, Sanofi, NTT Data). Lo spazio "integratore che racconta da dentro una fabbrica italiana, con numeri e limiti" è vuoto.

## 4. Cliché visivi del settore da evitare

Oltre a quelli già vietati in `REGOLE.md`, la rilevazione ne aggiunge altri, con chi li usa oggi:

| Cliché | Chi lo usa | Perché evitarlo |
|-|-|-|
| Spazio, pianeti, cieli stellati, robot su rocce lunari | Unitree | È il codice del fornitore: Abra sembrerebbe una sua filiale |
| Pista o vortice di luce blu, glow, numeri giganti luminosi | AgiBot | Estetica "AI" e fantascienza, già bandita |
| Umanoide bianco isolato su fondo grigio caldo, luce da studio | 1X, Figure, Apptronik, Fourier | Linguaggio da prodotto di consumo; con le foto ufficiali Unitree Abra finirebbe identica |
| Macro del materiale del robot, luce radente, nero pieno | Generative Bionics, Figure | Lusso tecnologico rivolto a investitori, lontano da chi decide un POC |
| Robot che sposta cassette in un magazzino americano | Apptronik, Agility | Foto stock della promessa "sostituisce il lavoro", lontana dai casi Abra |
| Blu corporate pieno con foto di impianto stock | Comau, Eagleprojects, Agile Robots | Invisibile: è il colore di default dell'industria |
| Arancio o salmone come colore del bottone | Apptronik, PAL, Generation Robots | Codice e-commerce e startup; Abra ha già usato un pallino arancio |
| Rosso segnaletico su antracite | ANYbotics | Già proprietario del leader europeo dell'ispezione |
| Lettering "techno" largo con lettere spezzate o senza traverso | Unitree, AgiBot, Eagleprojects, PAL, logo attuale Abra (Nasalization) | Generico e datato; la A senza traverso è proprio il problema del logo attuale |
| Grotesk svizzero neutro in un unico peso, tutto maiuscolo e spaziato | Apptronik, Figure, MYBOTSHOP, Agile Robots | Non distingue; è il default della categoria |
| Robot che balla, fa capriole, combatte | Video virali Unitree e cinesi [R07] | Il pubblico B2B italiano è già scettico verso le capriole [R07] |

## 5. Cliché verbali da evitare

- Il robot "per gli umani" o "insieme alle persone": "Robots For Humans" (Apptronik), "People and robots, together" (Reply), "Amplifying humans" (Generative Bionics), "Improve People's Life" (PAL).
- Il futuro: "The future of home help is here" (Figure), "Il futuro dell'industria è la nostra sfida" (Comau), "Driving industries forward" (Agile Robots).
- La meraviglia: "Changing your idea of what robots can do" (Boston Dynamics), "Stellar Explorer" (Unitree).
- La prova generica senza numero: "Proven results" (Agility).
- Il gergo di categoria non tradotto: "general purpose", "embodied AI", "Physical AI" usato come slogan. "Physical AI" resta utile come parola chiave verso i decisori [R07], mai come promessa.
- Le terne di prodotto: "Il robot giusto, configurato, consegnato" (H1 attuale di Abra) appartiene alla stessa famiglia e va superato.
- In italiano: "soluzioni smart", "a 360 gradi", "chiavi in mano", "innovazione", "sfida".

## 6. Spazi visivi e verbali liberi

Sono spazi che nessuno degli attori rilevati occupa. Li offro come terreno ai direttori creativi, senza prescrivere una soluzione.

**Fotografia**
1. **Documentaria in stabilimenti e laboratori italiani**, luce del posto (neon di reparto, finestre a shed), persone vere al lavoro accanto al robot, mani, strumenti, cavi, nastro sul pavimento. Il robot come strumento in scena, a volte fuori fuoco. Oggi nessun competitor mostra un contesto riconoscibile e italiano.
2. **Il banco di prova**: robot fermo e misurato, metro, carrelli, pesi, segni a gesso, tabelle di prova. È l'immagine del metodo.
3. **Il rilievo**: mappe LiDAR e nuvole di punti trattate come disegni di rilievo topografico o tavole tecniche stampate (monocromia, carta), lontane dal glow e dalle particelle.

**Grafica e colore**
4. **Palette industriale calda**, legata a macchine e materiali italiani (grigio macchina, verde o avorio delle macchine utensili, colori della ceramica, carta da disegno, inchiostro). Blu elettrico, viola, arancio, rosso su antracite e grigio caldo da consumer tech sono tutti occupati.
5. **Il linguaggio del documento tecnico**: manuale, scheda limiti, verbale di prova, distinta, numero di revisione, quote. L'oggetto più apprezzato dai clienti di Abra è il manuale tecnico consegnato a SACMI (rev 1.1 con simulatore MuJoCo) [R10]: è un codice visivo nativo e nessuno lo usa.
6. **Tipografia fuori dal grotesk di default**: accoppiate con un carattere da documentazione (monospaziato tecnico, serif da manuale, tipi da segnaletica industriale), sempre con licenza OFL o commerciale dichiarata.

**Tono**
7. **Italiano tecnico e misurato**: numeri, unità di misura, limiti dichiarati. Nessun competitor scrive in italiano con questo registro; i media cercano proprio questa voce [R08].
8. **Il cliente che parla**: tecnici e tesisti citati con ruolo, come fa Agility con GXO (circa sei volte l'engagement dei post aziendali [R08]).

## 7. Minacce da tenere presenti

- **Unitree sta diventando un marchio di consumo** (R1 sotto i 4.000 euro in Italia, Go2 a scaffale da MediaMarkt in Belgio): se Abra si identifica con Unitree eredita sia il prezzo al ribasso sia il rischio reputazionale (lista 1260H del Pentagono, CVE su G1 e Go2 [R05]).
- **AgiBot con SIR** porta in Emilia un'offerta "umanoide più integratore locale" con 40 anni di referenze industriali.
- **Generative Bionics** occupa la narrativa "umanoide italiano" con Eni e Fincantieri, due target della mappa aziende [R07].
- **Reply** presidia le ispezioni con quadrupedi nei grandi gruppi dell'energia (Saipem) [R01].
- **MADE Competence Center** fa da vetrina pubblica di G1 e H2 per le imprese [R07]: è insieme canale, cliente e concorrente nelle demo.

## Fonti

Rilevazione diretta delle home page (27/10/2026): [unitree.com](https://www.unitree.com), [bostondynamics.com](https://bostondynamics.com), [figure.ai](https://www.figure.ai), [agilityrobotics.com](https://www.agilityrobotics.com), [apptronik.com](https://apptronik.com), [1x.tech](https://www.1x.tech), [anybotics.com](https://www.anybotics.com), [agile-robots.com](https://www.agile-robots.com), [pal-robotics.com](https://pal-robotics.com), [fftai.com](https://www.fftai.com), [agibot.com](https://www.agibot.com), [generationrobots.com/it](https://www.generationrobots.com/it/), [eagleprojects.it](https://www.eagleprojects.it), [generativebionics.com](https://www.generativebionics.com), [reply.com/roboverse-reply](https://www.reply.com/roboverse-reply/it), [comau.com](https://www.comau.com/it/), [mybotshop.de](https://www.mybotshop.de), [sir-robotics.com](https://www.sir-robotics.com).

Ricerche integrative:
- SIR e umanoidi: [Forbes Italia, 05/02/2026](https://forbes.it/2026/02/05/cosi-sir-robotics-porta-robot-umanoidi-nel-mondo-reale); [AgiBot, debutto in Italia](https://agibot.com/article/231/detail/39.html); [Il Sole 24 Ore, SIR tra Italia e Cina](https://en.ilsole24ore.com/art/sir-robotics-links-italia-and-china-and-also-handles-e-commerce-shipments-AJstffWB); [Confindustria Emilia](https://www.confindustriaemilia.it/flex/cm/pages/ServeBLOB.php/L/EN/IDPagina/100082).
- La Casa degli Umanoidi e Aispiria: [Il Giorno](https://www.ilgiorno.it/brescia/cronaca/umanoidi-alleati-degli-artigiani-lavori-4910af4d); [Quotidiano.net](https://www.quotidiano.net/economia/made-in-italy/i-robot-umanoidi-escono-dai-2823c897).
- Eventi: [Scarlett Entertainment, robot fotografo Milano](https://scarlettentertainment.com/ae/acts/photo-robot-italy); [Il Resto del Carlino, Ameca a Rimini](https://www.ilrestodelcarlino.it/rimini/cronaca/robot-umano-capitale-innovazione-p0r9h0s9); [TechPrincess, RoBee al MIMO](https://techprincess.it/robee-mimo-2025-oversonic-robotica-intelligenza-artificiale/); [Notebookcheck, prezzi del noleggio di umanoidi](https://www.notebookcheck.it/I-prezzi-del-noleggio-di-robot-umanoidi-crollano-con-la-comparsa-di-piattaforme-dedicate.1421104.0.html).
- Unitree a scaffale: [MediaMarkt Belgio, Go2 Air](https://www.mediamarkt.be/en/product/_unitree-quadruped-go2-air-robot-dog-166563289.html); [BusinessOnline, Unitree R1 in Italia](https://www.businessonline.it/news/abbiamo-provato-unitree-r1-le-nostre-impressioni-sul-robot-umanoide-che-si-pu-comprare-anche-in-italia_n84060.html).
- Ricerca interna: `ricerca/01`, `05`, `07`, `08`, `10`.
