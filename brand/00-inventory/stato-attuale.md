# Stato attuale del brand Abra Robotics

Rilevato il 27/10/2026 dal repo del sito (`Abra-Robotics`, branch main d22fb8d7), dal Company Brain e dalla ricerca di mercato in `~/dev/abra/ricerca/`. È il punto di partenza da superare.

## Marchi in uso (tre, non coordinati)

| File | Cosa è | Dove si usa | Note |
|-|-|-|-|
| `images/logo.png` (740x230) | Logotipo "ABRA ROBOTICS" in Nasalization, maiuscolo, nero | Navbar del sito, favicon SVG (font incorporato in base64) | Font sci-fi anni 2000 molto diffuso (Typodermic). Le A senza traverso ricordano il lettering di molti brand tech e di Unitree stessa. Nessun simbolo proprietario. |
| `images/logo-icon.png` (512) | "Λ" bianca su cerchio nero | Avatar social, apple-touch-icon | È solo la A di Nasalization: non registrabile come segno distintivo forte. |
| `images/logo-full.png` (2000) | "Abra Robotics" in grotesk bold minuscolo con pallino arancio | Versione recente non adottata ovunque | Più contemporaneo, ma il pallino arancio è un codice molto comune (startup SaaS). |
| Company Brain `public/abra-logo.png` | Logo impilato ABRA / ROBOTICS | Interfaccia interna | Favicon del sito e del Brain ora è un'emoji mago (Noto): non è un asset di brand. |

Copie di riferimento in `img/`.

## Palette (style.css del sito)

- `--black #0a0a0a`, `--white #ffffff`, grigi `#525252 #a3a3a3 #e5e5e5 #f5f5f5`.
- Accento viola: `#b37eff` (chiamato ancora `--orange` nel CSS, residuo di una palette precedente arancio), `#9a5cf0`, `#7c4dd6`, `#6535c0`, fondo `#f0e8ff`.
- Rosso `#dc2626` per errori.
- Le linee guida del progetto (CLAUDE.md) bloccano: nero/bianco, viola "con parsimonia", glassmorphism, ispirazione Sanity.io.
- Rischio: il viola è uno dei cliché da evitare indicati nel brief (gradienti viola, estetica "AI").

## Tipografia

- **Satoshi** 400/500/700/900 (Fontshare, ITF Free Font License, uso commerciale gratuito) su tutto il sito.
- **Nasalization** (Typodermic) solo nel logotipo: licenza desktop gratuita, l'incorporamento web e nel favicon va verificato con la licenza Typodermic.
- **Manrope** (OFL) nel Company Brain.

## Immagini e video

- Fotografie e render ufficiali Unitree (`images/official/`, `videos/official/`) e immagini prodotto da RoboStore (alcune ancora con watermark). Nessuna fotografia propria di Abra in azienda o in laboratorio.
- `images/hero-robots.png`, video hero `hero-bg-desktop.mp4` (robot su sfondo scuro).
- Unico logo cliente: `images/clienti/sacmi-logo.jpg`.
- Cutout con sfondo rimosso per le card collection (`-nobg.png`).

## Testi e posizionamento comunicato

- Title home: "Robot Unitree in Italia: prezzi G1, H2, AS2, Go2". H1: "Il robot giusto, configurato, consegnato." Il sito oggi parla soprattutto da catalogo (350 prodotti con prezzi pubblici, listino, categorie umanoidi/quadrupedi/cobot/AMR/accessori).
- Servizi citati: hardware, assessment e POC, sviluppo software custom (ERP/MES, AI), formazione, finanziamenti e incentivi.
- Chi siamo: "Robotica applicata, fatta in Italia"; valori "approccio dal processo", "hardware best-in-class", "supporto dopo il go-live"; "parte della filiera di distribuzione di Unitree Italia".
- Problemi rispetto ai vincoli del brief: il sito si presenta per famiglie di robot e da rivenditore Unitree (title, H1, navigazione). Compare anche "celle chiavi in mano" per i cobot, in contrasto con il vincolo "niente turn-key". Ci sono formule contrapposte ("Niente progetti calati dall'alto. Niente vendite spinte.") e trattini lunghi in vari testi.

## Prove reali disponibili (da `ricerca/10-fonti-interne.md`)

- SACMI (Imola): trattativa vinta, 23.250 €. Go2 per una tesi in azienda con manuale tecnico, simulatore MuJoCo, digital twin dello stabilimento con LiDAR, SLAM e navigazione autonoma.
- 23 trattative in fase di preventivo (circa 1,44 M€ complessivi; ticket mediano circa 54 k€). POC industriali con ticket medio circa 111 k€.
- Repository proprietari GitHub inclusi con robot e formazione (citati nella pagina università).
- Preventivi premium generati dal Company Brain con grafica "brand Abra" (logo e font incorporati).

## Cosa salvare e cosa superare

- Da salvare: il nome, l'impostazione sobria in bianco e nero, la trasparenza dei prezzi, il metodo (chiamata, proposta, deployment).
- Da superare: tre loghi diversi, font del logo da fantascienza e non distintivo, viola da estetica AI, assenza di un simbolo proprietario, fotografia tutta presa da Unitree, comunicazione da catalogo per famiglie di prodotto.
