/**
 * Scrive local-ai-config.json (gitignored) per test locale + stampa istruzioni admin.
 * NON committa mai la key nel repo.
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const tokenPath = path.join(process.env.USERPROFILE || process.env.HOME || '', 'Documents', 'token.txt');

if (!fs.existsSync(tokenPath)) {
  console.error('File non trovato:', tokenPath);
  process.exit(1);
}

const openaiApiKey = fs.readFileSync(tokenPath, 'utf8').trim();
if (!openaiApiKey.startsWith('sk-')) {
  console.error('Key OpenAI non valida in token.txt');
  process.exit(1);
}

const cfg = {
  mode: 'openai',
  openaiApiKey,
  openaiModel: 'gpt-5.4-mini',
  maxTokens: 512,
  temperature: 0.3,
};

const out = path.join(ROOT, 'offerte-ai', 'data', 'local-ai-config.json');
fs.writeFileSync(out, JSON.stringify(cfg, null, 2), 'utf8');
console.log('Scritto', out, '(gitignored — solo locale)');

console.log(`
Per abrarobotics.com (stesso browser):
1. Apri https://abrarobotics.com/admin/offerte-ai.html
2. Modalità → OpenAI API
3. Incolla la key da Documents/token.txt
4. Salva configurazione
5. Testa https://abrarobotics.com/offerte-ai/index.html

Locale:
  python -m http.server 8765
  http://127.0.0.1:8765/offerte-ai/index.html
`);
