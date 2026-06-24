/**
 * Test rapido OpenAI API — legge key da env OPENAI_API_KEY o da Documents/token.txt
 */
import fs from 'fs';
import path from 'path';

function readKey() {
  if (process.env.OPENAI_API_KEY?.trim()) return process.env.OPENAI_API_KEY.trim();
  const tokenPath = path.join(process.env.USERPROFILE || process.env.HOME || '', 'Documents', 'token.txt');
  if (fs.existsSync(tokenPath)) return fs.readFileSync(tokenPath, 'utf8').trim();
  throw new Error('Key non trovata: imposta OPENAI_API_KEY o crea Documents/token.txt');
}

const key = readKey();
const model = process.argv[2] || 'gpt-5.4-mini';
const useCompletionTokens = /^gpt-5|^o[3-9]/.test(model);
const payload = {
  model,
  messages: [
    { role: 'system', content: 'Rispondi solo OK in italiano.' },
    { role: 'user', content: 'Test connessione Abra Robotics.' },
  ],
};
if (useCompletionTokens) payload.max_completion_tokens = 16;
else payload.max_tokens = 16;
if (!/^gpt-5\.5/.test(model)) payload.temperature = 0;

const res = await fetch('https://api.openai.com/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${key}`,
  },
  body: JSON.stringify(payload),
});

const body = await res.text();
if (!res.ok) {
  console.error('FAIL', res.status, body.slice(0, 300));
  process.exit(1);
}
const data = JSON.parse(body);
console.log('OK OpenAI', model, '→', data.choices?.[0]?.message?.content?.trim());
