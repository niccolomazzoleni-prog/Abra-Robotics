/**
 * Test generazione automatica offerta formale (pipeline chat → OfferDraft).
 * Uso: node scripts/test_offer_auto.mjs
 */
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

const RFQ = `Preventivo formale intestato alla società.

Applicazione sorveglianza area confinata con umidità, termocamera e sensori gas.
Quotare As2 Pro, A2 Standard, A2 Pro.
In alternativa anche Go2 EDU Standard e Smart per confronto.
Integrazione PoC standard.`;

loadScript('js/prompt-guard.js');
loadScript('js/kb-search.js');
loadScript('js/quote-engine.js');
loadScript('js/offer-builder.js');
loadScript('js/offer-draft.js');
loadScript('js/llm-providers.js');
loadScript('js/rag-chat.js');

function assert(cond, msg) {
  if (!cond) throw new Error('FAIL: ' + msg);
  console.log('✓', msg);
}

const rag = new globalThis.AbraRAGChat({
  indexUrl: 'data/knowledge-index.json',
  pricesUrl: '../listini/pubblico/end-user.json',
  rulesUrl: 'data/offerte-regole.json',
});
await rag.init();

assert(globalThis.AbraOfferDraft.isFormalRfq(RFQ), 'RFQ riconosciuta');

const offer = globalThis.AbraOfferDraft.build(RFQ, rag.quote);
assert(offer, 'OfferDraft.build restituisce offerta');
assert(offer.line_items.length >= 8, 'Almeno 8 righe (robot + sensori + PoC)');

const skus = offer.line_items.map(l => l.sku).filter(Boolean);
assert(skus.includes('AS2-PRO') && skus.includes('A2-STD') && skus.includes('GO2-EDU-STD'), 'Robot As2/A2 + Go2 presenti');

const blocks = offer.content_blocks || [];
assert(blocks.some(b => /finanziament|agevolaz|Transizione 5/i.test(b.title + b.body)), 'Blocco finanziamenti/sgravi');

const poc = offer.line_items.find(l => /PoC|integrazione software/i.test(l.nome));
assert(poc && poc.prezzo_unit === 19360, 'PoC 22×8×110 = 19360');

const trasf = offer.line_items.find(l => /Trasferte team/i.test(l.nome));
assert(trasf && trasf.su_richiesta, 'Trasferte a parte');

const t = globalThis.AbraOfferDraft.builder.recalculate(offer);
assert(t.gruppi?.length === 2, 'Due blocchi robot (sorveglianza + Go2)');

rag.clearHistory();
const { offerDraft } = await rag.ask(RFQ);
assert(offerDraft, 'rag.ask genera offerDraft automaticamente');
assert(offerDraft.line_items.length === offer.line_items.length, 'Stesso numero righe via chat');

console.log('\n=== Tutti i test offerta automatica OK ===');
console.log('Alternative sorveglianza:', t.gruppi[0].opzioni.map(o => o.nome).join(' | '));
console.log('Go2:', t.gruppi[1].opzioni.map(o => o.nome).join(' | '));
console.log('Totale consigliato €', t.totale.toFixed(2));
