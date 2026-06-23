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
    out: 'offerta-completa-sorveglianza-go2.html',
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

async function generate(key, cfg) {
  const quote = new globalThis.AbraQuoteEngine();
  await quote.load('../listini/pubblico/end-user.json', 'data/offerte-regole.json');
  await globalThis.AbraOfferDraft.init(quote);
  const offer = globalThis.AbraOfferDraft.build(cfg.msg, quote);
  if (!offer) throw new Error(`OfferDraft null: ${key}`);

  const builder = globalThis.AbraOfferDraft.builder;
  const previewHtml = builder.renderPreviewFragment(offer);
  const totals = builder.recalculate(offer);
  const outPath = path.join(OFFERTE, 'samples', cfg.out);

  const page = `<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow">
  <title>${cfg.title}</title>
  <link href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700,900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/offerte-ai.css">
  <style>body{background:#f5f5f5;padding:24px}.wrap{max-width:920px;margin:0 auto}</style>
</head>
<body>
  <div class="wrap">
    <p style="font-size:0.82rem;color:#525252;margin-bottom:16px">
      Pipeline chat · <strong>${key}</strong> · Totale consigliato € ${totals.totale.toLocaleString('it-IT', { minimumFractionDigits: 2 })}
      · <a href="../offerta.html">Crea offerta</a>
    </p>
    ${previewHtml}
  </div>
</body>
</html>`;

  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, page, 'utf8');
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
