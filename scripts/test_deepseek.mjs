/**
 * Test connessione DeepSeek API (stesso endpoint della chat).
 * Uso: set DEEPSEEK_API_KEY=sk-... && node scripts/test_deepseek.mjs
 */
import fs from 'fs';

const KEY = process.env.DEEPSEEK_API_KEY || process.env.DEEPSEEK_KEY || '';

async function main() {
  if (!KEY) {
    console.error('DEEPSEEK_API_KEY non impostata.');
    console.error('PowerShell: $env:DEEPSEEK_API_KEY="sk-..."; node scripts/test_deepseek.mjs');
    process.exit(2);
  }

  const res = await fetch('https://api.deepseek.com/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${KEY}`,
    },
    body: JSON.stringify({
      model: 'deepseek-chat',
      max_tokens: 64,
      temperature: 0.2,
      messages: [
        {
          role: 'system',
          content: 'Sei l\'assistente commerciale Abra Robotics. Rispondi in italiano, una frase.',
        },
        { role: 'user', content: 'Rispondi solo: OK DeepSeek Abra' },
      ],
    }),
  });

  const text = await res.text();
  if (!res.ok) {
    console.error('HTTP', res.status, text.slice(0, 400));
    process.exit(1);
  }

  const data = JSON.parse(text);
  const reply = data.choices?.[0]?.message?.content?.trim() || '';
  console.log('OK DeepSeek — risposta:', reply);
  fs.writeFileSync('offerte-ai/data/.deepseek-test-ok', new Date().toISOString(), 'utf8');
}

main().catch((e) => {
  console.error(e.message || e);
  process.exit(1);
});
