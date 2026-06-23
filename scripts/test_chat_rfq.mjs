/** Test RFQ Go2 EDU + pipeline offerta (offline). */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const OFFERTE = path.join(ROOT, 'offerte-ai');

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

globalThis.localStorage = { getItem: () => null, setItem: () => {} };
globalThis.sessionStorage = {
  getItem(k) { return k === 'abra_ai_config' ? JSON.stringify({ mode: 'offline' }) : null; },
  setItem() {},
};

const MSG = `Preventivo formale sorveglianza area confinata con umidità, termocamera e sensori gas. Confronto As2 Pro, A2 Standard e A2 Pro.`;

loadScript('js/prompt-guard.js');
loadScript('js/kb-search.js');
loadScript('js/quote-engine.js');
loadScript('js/offer-builder.js');
loadScript('js/offer-draft.js');
loadScript('js/llm-providers.js');
loadScript('js/rag-chat.js');

const rag = new globalThis.AbraRAGChat({
  indexUrl: 'data/knowledge-index.json',
  pricesUrl: '../listini/pubblico/end-user.json',
  rulesUrl: 'data/offerte-regole.json',
});
await rag.init();
const { reply, quote, offerDraft } = await rag.ask(MSG);
console.log('=== Chat RFQ (offline) ===');
console.log(reply.slice(0, 400));
console.log('\nQuote lines:', quote?.lines?.map((l) => `${l.label || l.sku}: €${l.price}`).join(' | ') || '—');
if (offerDraft) {
  const t = globalThis.AbraOfferDraft.builder.recalculate(offerDraft);
  console.log('\nOfferta formale:', offerDraft.line_items.length, 'righe · €', t.totale.toFixed(2));
}
