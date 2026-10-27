# Capacità disponibili per il progetto brand

Verificato il 27/10/2026 nella sessione Claude Code (desktop app).

## Skill

**Installate per questo progetto** (`.claude/skills/` del worktree, copiate da repo ufficiali Anthropic e lette prima dell'uso):

| Skill | Fonte | Uso |
|-|-|-|
| canvas-design | anthropics/skills | Metodo "filosofia visiva poi esecuzione"; cartella `canvas-fonts/` con circa 50 font OFL (Instrument, IBM Plex, JetBrains Mono, Geist Mono, Jura, Italiana, Gloock, Big Shoulders...) per rendering offline. Font esclusi dal git. |
| theme-factory | anthropics/skills | Costruzione di temi coerenti (palette e coppie tipografiche) per le applicazioni HTML. |
| algorithmic-art | anthropics/skills | Pattern generativi (utile per sistemi grafici e motion). |
| guideline-generation, brand-voice-enforcement | anthropics/knowledge-work-plugins (Brand Voice) | Struttura della voce di marca e controllo dei testi. |
| competitive-brief, brand-review | anthropics/knowledge-work-plugins (Marketing) | Analisi competitiva e revisione di coerenza di marca. |
| frontend-design.md, seo.md, aeo-geo.md | già nel repo | Regole anti-slop per HTML, SEO. |

Scartata: `brand-guidelines` di anthropics/skills (applica il brand Anthropic, non pertinente).

**Già disponibili a livello utente/plugin**: frontend-design, design:design-critique, design:design-system, design:accessibility-review, design:ux-copy, design:design-handoff, artifact-design, dataviz, anthropic-skills:copywriting, copy-editing, ogilvy, product-marketing, marketing-psychology, pdf, pptx, 21st-ui-explore.

## MCP collegati

| Server | Tool rilevanti | Serve? |
|-|-|-|
| Higgsfield | generate_image (gpt_image_2_5 e altri), generate_video, upscale, remove_background, balance | Sì per mood e mockup fotografici. **Saldo: 0,5 crediti, piano free.** Un'immagine costa circa 0,25 crediti: il saldo copre 2 immagini. Il fabbisogno stimato per la Fase 2 è 25-30 immagini (circa 6,25-7,5 crediti) più eventuali v2. Con la soglia del 30% non è possibile generare nulla senza ricarica. |
| Claude Browser (pane) | navigate, screenshot, read_console | Sì: verifica reale delle presentazioni HTML (reviewer-produzione). |
| Playwright locale (`~/Downloads/prisma-hero/node_modules/playwright`) | screenshot headless | Sì: render a 16/32 px dei loghi, PNG delle applicazioni, controllo errori console. |
| Claude in Chrome | browser reale | Ricerca visiva su siti dei competitor se serve. |
| WebSearch / WebFetch | ricerca | Sì: competitor e ricerca anteriorità marchi (lettura pubblica EUIPO/WIPO). |
| Google Drive (nico@) | search/read | Utile per leggere i preventivi PDF esistenti; non indispensabile. |
| Notion | fetch/search | Il workspace Sales Ops è visibile; nessuna esigenza diretta. |
| Google Slides, HubSpot, ClickUp, Meta Ads, Shopify, Zapier, Slack | | Non servono a questa fase. |
| Figma (plugin design) | | **Richiede autenticazione (/mcp).** |
| Canva | | Non collegato. |

## Strumenti mancanti e beneficio

1. **Crediti Higgsfield** (fondamentale per le immagini): con circa 10 crediti si coprono 4-6 mood per direzione più un mockup fotorealistico ciascuna. Senza, la direzione fotografica resta descritta (shot list, luce, inquadrature) e illustrata con composizioni SVG/HTML costruite a mano sopra i cutout ufficiali Unitree già presenti nel repo, marcati come segnaposto.
2. **Figma MCP**: permetterebbe di consegnare file sorgente modificabili dal designer che curerà le guidelines. Oggi gli SVG scritti a mano sono la fonte; si importano in Figma senza perdita.
3. **Canva MCP**: comodo per template social che il team può editare. Non indispensabile.
4. Nessun rasterizzatore SVG da riga di comando (rsvg, Inkscape, ImageMagick): si sopperisce con Playwright/Chromium.

## Plugin e marketplace

- Configurato solo il marketplace `claude-plugins-official`; plugin abilitato `frontend-design`. Il plugin Design (knowledge-work-plugins) è già attivo.
- Brand Voice e Marketing di knowledge-work-plugins: le skill utili sono state copiate come skill di progetto (l'installazione di un plugin non si carica a sessione in corso).

## Sintesi

| Strumento | Fase | Per fare cosa |
|-|-|-|
| ricerca/ in `~/dev/abra`, Company Brain | 1 | Personas, obiezioni, proof points reali, concorrenza italiana |
| WebSearch / WebFetch | 1, 3 | Competitor esteri, anteriorità marchi |
| competitive-brief, guideline-generation | 1 | Struttura analisi competitiva e piattaforma di voce |
| Subagent di progetto (`.claude/agents/`) | 1, 2, 3 | Strategist, 5 direttori creativi, 5 revisori + finale |
| canvas-design, theme-factory, algorithmic-art, frontend-design | 2 | Filosofia visiva, palette e font, pattern, HTML delle applicazioni |
| Font OFL in canvas-fonts e Google Fonts | 2 | Tipografia con licenza chiara |
| Higgsfield | 2 | Mood e mockup (bloccato dal saldo) |
| Playwright, Claude Browser | 2, 3, 4 | Test 16/32 px, screenshot, verifica presentazioni |
| design-critique, accessibility-review, brand-voice-enforcement | 3 | Revisioni art direction, contrasti WCAG, controllo copy |
| artifact-design, dataviz | 4 | Presentazione finale index.html e confronto punteggi |
