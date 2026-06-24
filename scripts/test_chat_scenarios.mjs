/**
 * Test 10 domande tipo cliente — quote engine + OpenAI (se key disponibile).
 */
import fs from 'fs';
import path from 'path';

const ROOT = path.resolve(import.meta.dirname, '..');
const fmt = (n) => Number(n).toLocaleString('it-IT', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

function readKey() {
  if (process.env.OPENAI_API_KEY?.trim()) return process.env.OPENAI_API_KEY.trim();
  const p = path.join(process.env.USERPROFILE || '', 'Documents', 'token.txt');
  if (fs.existsSync(p)) return fs.readFileSync(p, 'utf8').trim();
  return '';
}

const prices = JSON.parse(fs.readFileSync(path.join(ROOT, 'listini/pubblico/end-user.json'), 'utf8'));
const aliases = JSON.parse(fs.readFileSync(path.join(ROOT, 'offerte-ai/data/product-aliases.json'), 'utf8'));
const rules = JSON.parse(fs.readFileSync(path.join(ROOT, 'offerte-ai/data/offerte-regole.json'), 'utf8'));
rules.aliases = aliases.aliases;
rules.compare_sets = aliases.compare_sets;
const kb = JSON.parse(fs.readFileSync(path.join(ROOT, 'offerte-ai/data/knowledge-index.json'), 'utf8'));

function normalize(t) {
  return String(t || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
}

function kbSearch(q, limit = 3) {
  const qt = normalize(q).split(/\W+/).filter(w => w.length > 2);
  const scored = kb.chunks.map(c => {
    const text = normalize(c.text + ' ' + c.title);
    let s = 0;
    for (const w of qt) if (text.includes(w)) s++;
    return { ...c, score: s };
  }).filter(c => c.score > 0).sort((a, b) => b.score - a.score);
  return scored.slice(0, limit);
}

function wantsPriceRanking(lower) {
  return /ordine\s+(di\s+)?costo|ordinat[oi]?\s+per\s+prezzo|dal\s+piu\s+economico|metti\s+in\s+ordine|confronto\s+prezz|lista\s+prezzi/.test(lower)
    || (/confront|ordine|classifica/.test(lower) && /prezz|costo|econom/.test(lower));
}

function quoteCompareSet(setId, opts = {}) {
  const skus = rules.compare_sets[setId] || [];
  const lines = skus.map(sku => {
    const p = prices[sku];
    if (!p) return null;
    return { sku, nome: p.nome, prezzo_finale: p.prezzo_eur };
  }).filter(Boolean);
  if (opts.ranked) lines.sort((a, b) => a.prezzo_finale - b.prezzo_finale);
  return { lines, ranked: !!opts.ranked, family_label: opts.family_label || setId };
}

function tryAutoQuote(text) {
  const lower = normalize(text);
  if (wantsPriceRanking(lower)) {
    if (/\bg1\b|prodotti g1/.test(lower)) return quoteCompareSet('g1-gamma', { ranked: true, family_label: 'Unitree G1' });
    if (/\bas2\b|as\s*2/.test(lower)) return quoteCompareSet('as2-gamma', { ranked: true, family_label: 'Unitree As2' });
    if (/\bgo2\b/.test(lower)) return quoteCompareSet('go2-edu-duo', { ranked: true, family_label: 'Go2 EDU' });
  }
  if (/go2.*edu|go2 edu/.test(lower) && /confront|standard|smart|plus/.test(lower)) {
    return quoteCompareSet('go2-edu-duo', { ranked: true, family_label: 'Go2 EDU' });
  }
  const skus = Object.keys(prices).filter(s => lower.includes(s.toLowerCase()));
  if (skus.length) {
    return { lines: skus.map(sku => ({ sku, nome: prices[sku].nome, prezzo_finale: prices[sku].prezzo_eur })) };
  }
  if (/\bas2\b|as\s*2/.test(lower) && /\bpro\b/.test(lower)) {
    const p = prices['AS2-PRO'];
    return { lines: [{ sku: 'AS2-PRO', nome: p.nome, prezzo_finale: p.prezzo_eur }] };
  }
  if (/mir250|mir 250|mir-250/.test(lower)) {
    const sku = Object.keys(prices).find(s => /MIR250|MIR-250/i.test(s));
    if (sku) return { lines: [{ sku, nome: prices[sku].nome, prezzo_finale: prices[sku].prezzo_eur }] };
  }
  if (/g1-u1|g1 u1/.test(lower) && /g1-u2|g1 u2|differenz|confront/.test(lower)) {
    return quoteCompareSet('g1-gamma', { ranked: true, family_label: 'G1 (estratto)' });
  }
  return null;
}

function formatQuote(q) {
  if (!q?.lines?.length) return '';
  if (q.ranked) {
    return q.lines.map((l, i) => `${i + 1}. ${l.nome} (${l.sku}) — € ${fmt(l.prezzo_finale)} IVA escl.`).join('\n');
  }
  return q.lines.map(l => `• ${l.nome} (${l.sku}): € ${fmt(l.prezzo_finale)} IVA escl.`).join('\n');
}

const QUESTIONS = [
  'mi metti in ordine di costo i prodotti g1',
  'quanto costa il Go2 EDU per una università?',
  'prezzo As2 Pro per sorveglianza industriale',
  'MiR250 quanto costa?',
  'quali sono i tempi di consegna per un umanoide G1?',
  'posso usare finanziamenti Industria 4.0 per un robot?',
  'mi serve un preventivo formale per sorveglianza con As2 e termocamera',
  'confronto Go2 EDU standard vs smart, prezzi',
  'quale G1 consigliate per laboratorio universitario di ricerca?',
  'differenza di prezzo tra G1-U1 e G1-U2',
];

async function askOpenAI(question, quoteBlock, kbHits, key) {
  const ctx = [
    quoteBlock ? `=== PREVENTIVO UFFICIALE ===\n${quoteBlock}\n=== FINE ===` : '',
    kbHits.length ? '=== KB ===\n' + kbHits.map((h, i) => `[${i + 1}] ${h.title}\n${h.text.slice(0, 400)}`).join('\n\n') : '',
  ].filter(Boolean).join('\n\n');
  const body = {
    model: 'gpt-5.4-mini',
    max_completion_tokens: 400,
    temperature: 0.3,
    messages: [
      {
        role: 'system',
        content: 'Sei assistente commerciale Abra Robotics. Usa SOLO prezzi dal PREVENTIVO UFFICIALE se presente. Italiano, conciso, professionale. Non dire che mancano prezzi se sono nel preventivo.',
      },
      { role: 'user', content: `${ctx}\n\nDomanda cliente:\n${question}` },
    ],
  };
  const res = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${key}` },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error?.message || res.statusText);
  return data.choices?.[0]?.message?.content?.trim() || '';
}

function grade(question, quote, reply, kbHits) {
  const issues = [];
  const ok = [];
  if (/ordine.*costo|ordine di costo/.test(normalize(question))) {
    if (quote?.ranked && quote.lines.length >= 10) ok.push('Lista G1 completa ordinata');
    else issues.push('Manca classifica prezzi G1 dal listino');
  }
  if (/as2.*pro|as2 pro/.test(normalize(question)) && !/29900|29\.900|29,900/.test(reply + formatQuote(quote))) {
    if (quote?.lines?.some(l => l.sku === 'AS2-PRO')) ok.push('Prezzo As2 Pro presente');
    else issues.push('Prezzo As2 Pro (€29.900) non citato');
  }
  if (/mir250/.test(normalize(question))) {
    if (quote?.lines?.length || /€|eur/i.test(reply)) ok.push('Risposta prezzo MiR');
    else issues.push('MiR250: prezzo assente o SKU non trovato in listino');
  }
  if (/preventivo formale|termocamera/.test(normalize(question))) {
    if (/preventivo|offerta|pdf|voci|integrazione/i.test(reply)) ok.push('Propone percorso offerta');
    else issues.push('Non propone preventivo/offerta formale');
  }
  if (/finanziament|industria 4/.test(normalize(question))) {
    if (/credito|iperammortamento|4\.0|transizione|agevol/i.test(reply)) ok.push('Cita agevolazioni');
    else issues.push('Non cita finanziamenti/4.0');
  }
  if (/tempi.*consegna|consegna/.test(normalize(question))) {
    if (/settiman|4-6|4–6|8 sett|giorni/i.test(reply)) ok.push('Indica tempi consegna');
    else issues.push('Tempi consegna non chiari');
  }
  if (/non posso inventare|mancano|non ho.*prezzi|inviami.*listino|blocco preventivo ufficiale/i.test(reply)) {
    issues.push('Risposta evasiva — chiede dati che abbiamo già');
  }
  if (!reply && !quote) issues.push('Nessuna risposta');
  if (kbHits.length === 0 && !quote) issues.push('KB vuota per la query');
  return { pass: issues.length === 0, ok, issues };
}

const key = readKey();
const results = [];

for (let i = 0; i < QUESTIONS.length; i++) {
  const q = QUESTIONS[i];
  const quote = tryAutoQuote(q);
  const quoteBlock = formatQuote(quote);
  const kbHits = kbSearch(q);
  let reply = '';
  let mode = 'offline';

  if (quote?.ranked) {
    reply = `**Gamma ${quote.family_label}** (listino End-User, dal più economico):\n\n${quoteBlock}`;
    mode = 'deterministic-rank';
  } else if (key) {
    try {
      reply = await askOpenAI(q, quoteBlock, kbHits, key);
      mode = 'openai';
    } catch (e) {
      reply = quoteBlock || kbHits.map(h => h.title).join(', ') || e.message;
      mode = 'error-fallback';
    }
  } else {
    reply = quoteBlock || kbHits.slice(0, 2).map(h => `**${h.title}**\n${h.text.slice(0, 200)}`).join('\n\n');
    mode = 'offline-only';
  }

  const g = grade(q, quote, reply, kbHits);
  results.push({ n: i + 1, q, mode, reply: reply.slice(0, 500), quote: quoteBlock.slice(0, 300), grade: g });
  process.stdout.write(`\n--- ${i + 1}/10 ${g.pass ? 'OK' : 'WARN'} ---\n${q}\n`);
}

const reportPath = path.join(ROOT, 'scripts', 'chat-scenarios-report.json');
fs.writeFileSync(reportPath, JSON.stringify(results, null, 2));
console.log('\nReport:', reportPath);
console.log('Pass:', results.filter(r => r.grade.pass).length, '/', results.length);
