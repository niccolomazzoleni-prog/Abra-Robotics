/**
 * Genera HTML offerta campione (Go2 EDU RFQ) — stesso pipeline della chat.
 * Uso: node scripts/generate_offer_sample.mjs
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const OFFERTE = path.join(ROOT, 'offerte-ai');
const OUT = path.join(OFFERTE, 'samples', 'offerta-go2-edu-rfq.html');

function loadScript(relPath) {
  let code = fs.readFileSync(path.join(OFFERTE, relPath), 'utf8');
  code = code.replace(
    /}\)\(typeof window !== 'undefined' \? window : globalThis\);/g,
    '})(globalThis);'
  );
  new Function(code)();
}

globalThis.fetch = async (url) => {
  let p = String(url);
  if (p.startsWith('http://127.0.0.1') || p.startsWith('http://localhost')) {
    p = p.replace(/^https?:\/\/[^/]+/, '');
  }
  if (p.startsWith('/offerte-ai/')) p = p.slice('/offerte-ai/'.length);
  if (p.startsWith('/')) p = p.slice(1);
  let abs;
  if (p.startsWith('../')) abs = path.normalize(path.join(OFFERTE, p));
  else abs = path.join(OFFERTE, p);
  if (!fs.existsSync(abs)) {
    return { ok: false, status: 404, json: async () => ({}), text: async () => '' };
  }
  const body = fs.readFileSync(abs, 'utf8');
  return { ok: true, status: 200, json: async () => JSON.parse(body), text: async () => body };
};

const RFQ_MSG = `Siamo interessati all'acquisto di un robot quadrupede Unitree Go2 nella versione EDU e vorremmo ricevere un preventivo formale intestato alla nostra società.

La configurazione di interesse:
- Unitree Go2 EDU PLUS con modulo NVIDIA Jetson Orin NX 16GB (100 TOPS).
- Quotare anche EDU base (Orin Nano) per confronto.

Indicare nel preventivo cosa è incluso, tempi consegna, spedizione, formazione e integrazione PoC.`;

loadScript('js/quote-engine.js');
loadScript('js/offer-builder.js');
loadScript('js/offer-draft.js');

async function main() {
  const quote = new globalThis.AbraQuoteEngine();
  await quote.load('../listini/pubblico/end-user.json', 'data/offerte-regole.json');
  await globalThis.AbraOfferDraft.init(quote);
  const offer = globalThis.AbraOfferDraft.build(RFQ_MSG, quote);
  if (!offer) throw new Error('OfferDraft ha restituito null');

  const builder = globalThis.AbraOfferDraft.builder;
  const previewHtml = builder.renderPreviewFragment(offer);
  const totals = builder.recalculate(offer);

  const page = `<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow">
  <title>Preventivo Go2 EDU — campione Abra</title>
  <link href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700,900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/offerte-ai.css">
  <style>body{background:#f5f5f5;padding:24px}.wrap{max-width:920px;margin:0 auto}</style>
</head>
<body>
  <div class="wrap">
    <p style="font-size:0.82rem;color:#525252;margin-bottom:16px">
      Campione generato automaticamente dal pipeline chat · Totale € ${totals.totale.toLocaleString('it-IT', { minimumFractionDigits: 2 })}
      · <a href="../offerta.html">Apri Crea offerta</a>
    </p>
    ${previewHtml}
  </div>
</body>
</html>`;

  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  fs.writeFileSync(OUT, page, 'utf8');
  console.log('OK:', OUT);
  console.log('Righe:', offer.line_items.length, '| Totale €', totals.totale.toFixed(2));
  offer.line_items.forEach((l) => {
    console.log(`  - ${l.nome || l.sku}: € ${(l.prezzo_unitario || 0).toLocaleString('it-IT')}`);
  });
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
