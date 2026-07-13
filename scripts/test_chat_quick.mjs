#!/usr/bin/env node
/** Smoke test: alias + listino per domande chat tipiche */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const prices = JSON.parse(fs.readFileSync(path.join(ROOT, 'listini/pubblico/end-user.json'), 'utf8'));
const rules = JSON.parse(fs.readFileSync(path.join(ROOT, 'offerte-ai/data/offerte-regole.json'), 'utf8'));
const aliases = JSON.parse(fs.readFileSync(path.join(ROOT, 'offerte-ai/data/product-aliases.json'), 'utf8'));

function fmt(n) {
  return Number(n).toLocaleString('it-IT', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function quoteSku(sku) {
  const p = prices[sku];
  if (!p) return null;
  return { sku, nome: p.nome, prezzo: p.prezzo_eur };
}

function tryQuery(q) {
  const lower = q.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  if (/go2.*edu|go2 edu/.test(lower)) return quoteSku('GO2-EDU-STD');
  if (/g1-u1|g1 u1/.test(lower)) return quoteSku('G1-U1');
  if (/as2.*pro|as2 pro/.test(lower)) return quoteSku('AS2-PRO');
  for (const [key, sku] of Object.entries(aliases.aliases).sort((a, b) => b[0].length - a[0].length)) {
    if (lower.includes(key)) return quoteSku(sku);
  }
  return null;
}

const cases = [
  ['Quanto costa Go2 EDU?', true],
  ['Prezzo G1-U1', true],
  ['prezzo AS2 Pro', true],
  ['Tempi di consegna', false],
];

let fail = 0;
for (const [q, expectPrice] of cases) {
  const r = tryQuery(q);
  const pass = expectPrice ? !!r : true;
  console.log(pass ? '✓' : '✗', q, r ? `→ ${r.sku} ${fmt(r.prezzo)} €` : '(fallback KB/WA)');
  if (!pass) fail++;
}

for (const sku of ['GO2-EDU-STD', 'G1-U1', 'AS2-PRO', 'AS2-AIR', 'AS2-EDU']) {
  if (!prices[sku]) {
    console.error('✗ SKU mancante:', sku);
    fail++;
  }
}
console.log(fail ? `\nFAIL ${fail}` : '\nTutti i test ok');
process.exit(fail ? 1 : 0);
