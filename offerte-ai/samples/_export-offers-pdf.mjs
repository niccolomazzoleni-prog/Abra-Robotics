/**
 * Esporta i preventivi H2 e Marchesini in PDF A4 (Chrome headless / Playwright).
 * Uso: node offerte-ai/samples/_export-offers-pdf.mjs
 * Richiede server locale: python -m http.server 8765  (root repo)
 */
import { spawn } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath, pathToFileURL } from 'url';
import http from 'http';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, '..', '..');
const chromePath =
  process.env.CHROME_PATH ||
  'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

const BASE = process.env.OFFER_BASE || 'http://127.0.0.1:8765';

const jobs = [
  {
    url: `${BASE}/offerte-ai/samples/offerta-h2-base-assistenza-6m.html`,
    pdf: path.join(__dirname, 'Preventivo-H2-Base-assistenza-6m.pdf'),
    desktop: path.join(process.env.USERPROFILE || '', 'Desktop', 'Preventivo-H2-Base-assistenza-6m.pdf'),
  },
  {
    url: `${BASE}/offerte-ai/samples/offerta-marchesini-as2-go2-g1u2.html`,
    pdf: path.join(__dirname, 'Preventivo-Marchesini-AS2-Go2-G1U2.pdf'),
    desktop: path.join(process.env.USERPROFILE || '', 'Desktop', 'Preventivo-Marchesini-AS2-Go2-G1U2.pdf'),
  },
];

function waitUrl(url, attempts = 40) {
  return new Promise((resolve, reject) => {
    let n = 0;
    const tick = () => {
      n += 1;
      const req = http.get(url, (res) => {
        res.resume();
        if (res.statusCode && res.statusCode < 500) resolve();
        else if (n >= attempts) reject(new Error(`HTTP ${res.statusCode} for ${url}`));
        else setTimeout(tick, 250);
      });
      req.on('error', () => {
        if (n >= attempts) reject(new Error(`Server non raggiungibile: ${url}`));
        else setTimeout(tick, 250);
      });
    };
    tick();
  });
}

async function exportWithPlaywright(job) {
  const { chromium } = await import('playwright');
  const browser = await chromium.launch({
    headless: true,
    executablePath: fs.existsSync(chromePath) ? chromePath : undefined,
  });
  const context = await browser.newContext({ viewport: { width: 1100, height: 1400 } });
  // Sblocca gate offerte (offer-auth.js) prima del load
  await context.addInitScript(() => {
    sessionStorage.setItem('abra_offers_until', String(Date.now() + 8 * 60 * 60 * 1000));
  });
  const page = await context.newPage();
  await page.goto(job.url, { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForSelector('.abra-offer-doc', { timeout: 15000 });
  // Rimuovi eventuale gate residuo
  await page.evaluate(() => {
    document.getElementById('offer-gate')?.remove();
    document.body.style.overflow = '';
    const wrap = document.querySelector('.offer-sample-wrap');
    if (wrap) wrap.style.visibility = '';
  });

  // Inline local images so PDF never misses logos/product shots
  await page.evaluate(async () => {
    const imgs = [...document.querySelectorAll('.offer-sample-paper img, .abra-offer-doc img')];
    for (const img of imgs) {
      const src = img.getAttribute('src') || '';
      if (!src || src.startsWith('data:')) continue;
      try {
        const abs = new URL(src, location.href).href;
        const res = await fetch(abs);
        if (!res.ok) continue;
        const blob = await res.blob();
        const dataUrl = await new Promise((resolve, reject) => {
          const r = new FileReader();
          r.onload = () => resolve(r.result);
          r.onerror = reject;
          r.readAsDataURL(blob);
        });
        img.setAttribute('src', dataUrl);
        img.removeAttribute('loading');
      } catch (_) {}
    }
    await Promise.all(
      [...document.images].map(
        (img) =>
          new Promise((resolve) => {
            if (img.complete && img.naturalWidth > 0) return resolve();
            img.onload = () => resolve();
            img.onerror = () => resolve();
            setTimeout(resolve, 3000);
          })
      )
    );
  });

  // Hide toolbar for PDF
  await page.addStyleTag({
    content: `
      .offer-sample-toolbar { display: none !important; }
      body.offer-sample-body { background: #fff !important; }
      .offer-sample-wrap { margin: 0 !important; padding: 0 !important; max-width: none !important; animation: none !important; }
      .offer-sample-paper { box-shadow: none !important; border-radius: 0 !important; padding: 0 !important; }
      .offer-sample-paper::before { display: none !important; }
    `,
  });

  await page.emulateMedia({ media: 'print' });
  await page.pdf({
    path: job.pdf,
    format: 'A4',
    printBackground: true,
    preferCSSPageSize: true,
    margin: { top: '10mm', bottom: '10mm', left: '9mm', right: '9mm' },
  });
  await browser.close();
}

function exportWithChromeCli(job) {
  return new Promise((resolve, reject) => {
    if (!fs.existsSync(chromePath)) {
      reject(new Error('Chrome non trovato'));
      return;
    }
    const args = [
      '--headless=new',
      '--disable-gpu',
      '--no-pdf-header-footer',
      '--disable-extensions',
      `--print-to-pdf=${job.pdf}`,
      job.url,
    ];
    const child = spawn(chromePath, args, { stdio: 'ignore' });
    child.on('error', reject);
    child.on('exit', (code) => {
      if (code === 0 && fs.existsSync(job.pdf)) resolve();
      else reject(new Error(`Chrome exit ${code} for ${job.url}`));
    });
  });
}

async function main() {
  for (const job of jobs) {
    await waitUrl(job.url);
  }

  let mode = 'chrome-cli';
  try {
    await import('playwright');
    mode = 'playwright';
  } catch (_) {
    // fallback
  }

  const results = [];
  for (const job of jobs) {
    if (mode === 'playwright') await exportWithPlaywright(job);
    else await exportWithChromeCli(job);

    if (job.desktop) {
      try {
        fs.copyFileSync(job.pdf, job.desktop);
      } catch (_) {}
    }
    const st = fs.statSync(job.pdf);
    results.push({
      pdf: job.pdf,
      desktop: fs.existsSync(job.desktop) ? job.desktop : null,
      bytes: st.size,
      mode,
    });
  }
  console.log(JSON.stringify({ ok: true, results }, null, 2));
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
