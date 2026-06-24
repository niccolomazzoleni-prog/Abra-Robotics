/**
 * Verifica regole anti-bot e campi obbligatori (allineate a script.js + apps-script/Code.gs)
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

function trimField(v) {
  return String(v || '').replace(/^\s+|\s+$/g, '');
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function normalizeContactData(data) {
  data = data || {};
  if (trimField(data._gotcha) || trimField(data.website) || trimField(data.company_url)) return null;
  const nome = trimField(data.nome);
  const email = trimField(data.email);
  const messaggio = trimField(data.messaggio);
  const azienda = trimField(data.azienda) || trimField(data.istituzione);
  const telefono = trimField(data.telefono);
  if (!nome && !email && !messaggio && !telefono && !azienda) return null;
  if (!nome || !email) return null;
  if (!isValidEmail(email)) return null;
  return { nome, email, messaggio, azienda, telefono };
}

function validateClientForm(form) {
  if (form._gotcha?.trim()) return false;
  if (!form.nome?.trim() || !form.email?.trim()) return false;
  if (!isValidEmail(form.email.trim())) return false;
  const required = form._required || [];
  return required.every((f) => String(form[f] || '').trim());
}

const cases = [
  { name: 'bot honeypot', data: { nome: 'Bot', email: 'a@b.it', _gotcha: 'spam' }, expect: null },
  { name: 'POST vuoto (solo url)', data: { url: 'https://abrarobotics.com', pagina: 'x' }, expect: null },
  { name: 'senza nome', data: { email: 'a@b.it', messaggio: 'ciao' }, expect: null },
  { name: 'senza email', data: { nome: 'Mario', messaggio: 'ciao' }, expect: null },
  { name: 'email invalida', data: { nome: 'Mario', email: 'no-email' }, expect: null },
  { name: 'lead valido minimo', data: { nome: 'Mario Rossi', email: 'mario@nexsoft.it' }, expect: 'ok' },
  { name: 'lead completo', data: { nome: 'Olexiy', email: 'info@nexsoft.it', azienda: 'Nexsoft', messaggio: 'RFQ As2' }, expect: 'ok' },
];

let pass = 0;
for (const c of cases) {
  const r = normalizeContactData(c.data);
  const ok = (c.expect === null && r === null) || (c.expect === 'ok' && r !== null);
  console.log(ok ? 'PASS' : 'FAIL', c.name);
  if (ok) pass++;
}

const clientOk = validateClientForm({ nome: 'Mario', email: 'a@b.it', _required: ['nome', 'email'] });
const clientFail = validateClientForm({ nome: '', email: 'a@b.it', _required: ['nome', 'email'] });
console.log(clientOk && !clientFail ? 'PASS' : 'FAIL', 'validazione client-side (nome+email)');
if (clientOk && !clientFail) pass++;

const script = fs.readFileSync(path.join(ROOT, 'script.js'), 'utf8');
const checks = [
  ['honeypot _gotcha', /injectContactHoneypots|_gotcha/],
  ['validateContactForm', /validateContactForm/],
  ['required nome email', /!nome \|\| !email/],
  ['no-cors POST', /mode:\s*['"]no-cors['"]/],
];
for (const [label, re] of checks) {
  const ok = re.test(script);
  console.log(ok ? 'PASS' : 'FAIL', 'script.js —', label);
  if (ok) pass++;
}

const gs = fs.readFileSync(path.join(ROOT, 'apps-script', 'Code.gs'), 'utf8');
const gsChecks = [
  ['server honeypot', /normalizeContactData/],
  ['reject empty', /!nome && !email && !messaggio/],
  ['email format', /isValidEmail/],
];
for (const [label, re] of gsChecks) {
  const ok = re.test(gs);
  console.log(ok ? 'PASS' : 'FAIL', 'Code.gs —', label);
  if (ok) pass++;
}

console.log(`\nTotale: ${pass} check OK`);
process.exit(pass >= cases.length + 1 + checks.length + gsChecks.length ? 0 : 1);
