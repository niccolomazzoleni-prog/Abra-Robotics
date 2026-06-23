/**
 * Genera campioni offerta dal pipeline chat.
 * Uso: node scripts/generate_offer_sample.mjs [combo|sorveglianza|go2|all|curata]
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const OFFERTE = path.join(ROOT, 'offerte-ai');

const NEXSOFT_CLIENT = {
  azienda: 'Nexsoft S.p.A.',
  contatto: 'Olexiy Lysytsya',
  piva: '04157150659',
  indirizzo: 'Via Antonio Amato 20/22, 84131 Salerno (SA)',
  email: 'info@nexsoft.it',
};

const CURATED_INTRO = `Spett.le Nexsoft S.p.A.

Egr. Olexiy Lysytsya,

a seguito del Vostro interesse per un sistema di **sorveglianza e perlustrazione** in area confinata (presenza di umidità, termocamera radiometrica e sensori gas/fumo), Le sottoponiamo un **preventivo strutturato** con due blocchi di piattaforma robotica:

**Blocco A — Sorveglianza industriale:** Unitree **As2 Pro** oppure linea **A2 Standard / A2 Pro** — selezionando *una sola* configurazione tra le alternative quotate.
**Blocco B — Alternativa Go2 EDU:** confronto tra **Standard (Jetson Orin Nano)** e **Smart / EDU+ (Orin NX 100 TOPS)**.

Accessori sensori, integrazione software (PoC), formazione e spedizione sono **condivisi** tra le configurazioni. Prezzi **IVA esclusa**, dazio incluso sul robot.`;

const SCENARIOS = {
  combo: {
    out: 'offerta-pipeline-sorveglianza-go2.html',
    legacy: 'offerta-completa-sorveglianza-go2.html',
    title: 'Preventivo sorveglianza + Go2 EDU — Nexsoft S.p.A.',
    badge: 'Generata dal pipeline',
    badgeClass: '',
    client: NEXSOFT_CLIENT,
    msg: `Richiediamo preventivo formale intestato alla nostra società.

1) APPLICAZIONE SORVEILIANZA: area confinata con possibile umidità, termocamera radiometrica, sensori gas e fumo. 
   Soluzione consigliata As2 / A2 — quotare As2 Pro, A2 Standard e A2 Pro (Unitree ufficiale).

2) ALTERNATIVA GO2 EDU: se orientati a Go2, quotare EDU Standard (Orin Nano) e EDU Smart / PLUS (Orin NX 100 TOPS) per confronto.

Integrazione software / PoC livello standard con ingegneria on-site.
Spedizione Italia.`,
  },
  curata: {
    out: 'offerta-curata-sorveglianza-go2.html',
    title: 'Preventivo sorveglianza As2/A2 + Go2 EDU — Nexsoft S.p.A.',
    badge: 'Versione curata Abra',
    badgeClass: ' badge-curated',
    curatedIntro: true,
    client: NEXSOFT_CLIENT,
    msg: `Richiediamo preventivo formale intestato alla nostra società.

1) APPLICAZIONE SORVEILIANZA: area confinata con possibile umidità, termocamera radiometrica, sensori gas e fumo. 
   Soluzione consigliata As2 / A2 — quotare As2 Pro, A2 Standard e A2 Pro (Unitree ufficiale).

2) ALTERNATIVA GO2 EDU: se orientati a Go2, quotare EDU Standard (Orin Nano) e EDU Smart / PLUS (Orin NX 100 TOPS) per confronto.

Integrazione software / PoC livello standard con ingegneria on-site.
Spedizione Italia.`,
  },
  sorveglianza: {
    out: 'offerta-sorveglianza-as2-a2.html',
    title: 'Preventivo sorveglianza As2 / A2',
    badge: 'Generata dal pipeline',
    msg: `Preventivo sorveglianza con As2 Pro, A2 Standard, A2 Pro, termocamera, sensori, PoC.`,
  },
  go2: {
    out: 'offerta-go2-edu-rfq.html',
    title: 'Preventivo Go2 EDU',
    badge: 'Generata dal pipeline',
    msg: `Preventivo Go2 EDU Standard e Smart Orin NX.`,
  },
};

function loadScript(relPath) {
  let code = fs.readFileSync(path.join(OFFERTE, relPath), 'utf8');
  code = code.replace(/}\)\(typeof window !== 'undefined' \? window : globalThis\);/g, '})(globalThis);');
  new Function(code)();
}

globalThis.fetch = async (url) => {
  let p = String(url);
  if (p.startsWith('/offerte-ai/')) p = p.slice('/offerte-ai/'.length);
  if (p.startsWith('/')) p = p.slice(1);
  const abs = p.startsWith('../') ? path.normalize(path.join(OFFERTE, p)) : path.join(OFFERTE, p);
  if (!fs.existsSync(abs)) return { ok: false, json: async () => ({}) };
  const body = fs.readFileSync(abs, 'utf8');
  return { ok: true, json: async () => JSON.parse(body), text: async () => body };
};

function samplePage({ title, previewHtml, offerId, totals, badge, badgeClass = '', altLink }) {
  return `<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow">
  <title>${title}</title>
  <link href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700,900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/offerte-ai.css">
</head>
<body class="offer-sample-body">
  <div class="offer-sample-toolbar">
    <div><span class="badge${badgeClass}">${badge}</span> ${offerId} · Totale di riferimento <strong>€ ${totals.toLocaleString('it-IT', { minimumFractionDigits: 2 })}</strong></div>
    <div style="display:flex;gap:8px;flex-wrap:wrap">
      <button type="button" onclick="window.print()">Stampa / PDF</button>
      ${altLink || ''}
      <a href="../offerta.html">Editor offerte</a>
      <a href="../index.html">Lab chat</a>
    </div>
  </div>
  <div class="offer-sample-wrap">
    <div class="offer-sample-paper">${previewHtml}</div>
  </div>
</body>
</html>`;
}

async function generate(key, cfg) {
  const quote = new globalThis.AbraQuoteEngine();
  await quote.load('../listini/pubblico/end-user.json', 'data/offerte-regole.json');
  await globalThis.AbraOfferDraft.init(quote);
  const offer = globalThis.AbraOfferDraft.build(cfg.msg, quote);
  if (!offer) throw new Error(`OfferDraft null: ${key}`);

  if (cfg.curatedIntro) offer.intro = CURATED_INTRO;
  else if (cfg.client?.contatto) {
    offer.intro = offer.intro.replace(/^Gentile Cliente,/m, `Spett.le ${cfg.client.azienda || 'Cliente'},\n\nEgr. ${cfg.client.contatto},`);
  }
  if (cfg.client) offer.client = { ...offer.client, ...cfg.client };

  const builder = globalThis.AbraOfferDraft.builder;
  const previewHtml = builder.renderPreviewFragment(offer);
  const totals = builder.recalculate(offer);
  const altLink = key === 'curata'
    ? '<a href="offerta-pipeline-sorveglianza-go2.html">Confronta pipeline</a>'
    : (key === 'combo' ? '<a href="offerta-curata-sorveglianza-go2.html">Confronta curata</a>' : '');

  const page = samplePage({
    title: cfg.title,
    previewHtml,
    offerId: offer.id,
    totals: totals.totale,
    badge: cfg.badge || 'Generata dal pipeline',
    badgeClass: cfg.badgeClass || '',
    altLink,
  });

  const outPath = path.join(OFFERTE, 'samples', cfg.out);
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, page, 'utf8');
  if (cfg.legacy) fs.writeFileSync(path.join(OFFERTE, 'samples', cfg.legacy), page, 'utf8');

  console.log(`\n=== ${key} → ${cfg.out} ===`);
  console.log('Totale di riferimento €', totals.totale.toFixed(2));
  if (totals.gruppi?.length) {
    for (const g of totals.gruppi) {
      console.log(`\n${g.label}:`);
      g.opzioni.forEach(o => console.log(`  • ${o.nome}: € ${o.totale.toLocaleString('it-IT')}`));
    }
  }
}

loadScript('js/quote-engine.js');
loadScript('js/offer-builder.js');
loadScript('js/offer-draft.js');

const arg = (process.argv[2] || 'all').toLowerCase();
const keys = arg === 'all' ? ['combo', 'curata'] : [SCENARIOS[arg] ? arg : 'combo'];
for (const key of keys) await generate(key, SCENARIOS[key]);
