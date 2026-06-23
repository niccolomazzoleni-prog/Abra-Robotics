/**
 * Genera campioni offerta dal pipeline chat.
 * Uso: node scripts/generate_offer_sample.mjs [combo|sorveglianza|go2|all]
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const OFFERTE = path.join(ROOT, 'offerte-ai');

const SCENARIOS = {
  combo: {
    out: 'offerta-pipeline-sorveglianza-go2.html',
    legacy: 'offerta-completa-sorveglianza-go2.html',
    title: 'Preventivo sorveglianza + Go2 EDU — Abra Robotics',
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
    msg: `Preventivo sorveglianza con As2 Pro, A2 Standard, A2 Pro, termocamera, sensori, PoC.`,
  },
  go2: {
    out: 'offerta-go2-edu-rfq.html',
    title: 'Preventivo Go2 EDU',
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

function samplePage({ title, previewHtml, offerId, totals, badge }) {
  return `<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow">
  <title>${title}</title>
  <link href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700,900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/offerte-ai.css">
  <style>
    :root { --accent-text: #7c4dd6; --orange-light: #f3ecff; --radius: 12px; --radius-sm: 8px; --black: #111; --white: #fff; --gray-50: #fafafa; --gray-100: #f5f5f5; --gray-200: #e5e5e5; --gray-600: #525252; --gray-700: #404040; --gray-800: #262626; --font: 'Satoshi', system-ui, sans-serif; }
    body { margin: 0; font-family: var(--font); background: #ece8f4; color: var(--black); -webkit-font-smoothing: antialiased; }
    .sample-toolbar { background: var(--black); color: #fff; padding: 10px 20px; display: flex; flex-wrap: wrap; gap: 12px; align-items: center; justify-content: space-between; font-size: 0.82rem; }
    .sample-toolbar .badge { background: var(--accent-text); color: #fff; font-weight: 700; font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.06em; padding: 4px 10px; border-radius: 999px; }
    .sample-toolbar a, .sample-toolbar button { color: #fff; background: transparent; border: 1px solid rgba(255,255,255,0.35); border-radius: 999px; padding: 6px 14px; font: inherit; font-size: 0.78rem; cursor: pointer; text-decoration: none; }
    .sample-toolbar button:hover, .sample-toolbar a:hover { background: rgba(255,255,255,0.1); }
    .sample-wrap { max-width: 920px; margin: 28px auto 48px; padding: 0 16px; }
    .sample-paper { background: var(--white); border-radius: var(--radius); box-shadow: 0 20px 60px rgba(17,17,17,0.12); padding: 36px 40px; }
    @media (max-width: 640px) { .sample-paper { padding: 22px 18px; } .abra-offer-doc .doc-block-highlight { grid-template-columns: 1fr !important; } }
    @media print { .sample-toolbar { display: none; } body { background: #fff; } .sample-wrap { margin: 0; max-width: none; padding: 0; } .sample-paper { box-shadow: none; border-radius: 0; padding: 0; } }
  </style>
</head>
<body>
  <div class="sample-toolbar">
    <div><span class="badge">${badge}</span> ${offerId} · Totale consigliato <strong>€ ${totals.toLocaleString('it-IT', { minimumFractionDigits: 2 })}</strong></div>
    <div style="display:flex;gap:8px;flex-wrap:wrap">
      <button type="button" onclick="window.print()">Stampa / PDF</button>
      <a href="../offerta.html">Editor offerte</a>
      <a href="../index.html">Lab chat</a>
    </div>
  </div>
  <div class="sample-wrap">
    <div class="sample-paper">
      ${previewHtml}
    </div>
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

  const builder = globalThis.AbraOfferDraft.builder;
  const previewHtml = builder.renderPreviewFragment(offer);
  const totals = builder.recalculate(offer);
  const page = samplePage({
    title: cfg.title,
    previewHtml,
    offerId: offer.id,
    totals: totals.totale,
    badge: 'Generata dal pipeline',
  });

  const outPath = path.join(OFFERTE, 'samples', cfg.out);
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, page, 'utf8');
  if (cfg.legacy) {
    fs.writeFileSync(path.join(OFFERTE, 'samples', cfg.legacy), page, 'utf8');
  }

  console.log(`\n=== ${key} → ${cfg.out} ===`);
  console.log('Totale consigliato €', totals.totale.toFixed(2));
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

const arg = (process.argv[2] || 'combo').toLowerCase();
const keys = arg === 'all' ? Object.keys(SCENARIOS) : [SCENARIOS[arg] ? arg : 'combo'];
for (const key of keys) await generate(key, SCENARIOS[key]);
