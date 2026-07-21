/**
 * Esporta preventivo SACMI come HTML self-contained (immagini base64) + PDF.
 */
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, '..', '..');
const chromePath = process.env.CHROME_PATH ||
  'C:\\\\Program Files\\\\Google\\\\Chrome\\\\Application\\\\chrome.exe';

const mime = {
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.png': 'image/png',
  '.webp': 'image/webp',
  '.svg': 'image/svg+xml',
  '.gif': 'image/gif',
};

function fileToDataUri(absPath) {
  if (!fs.existsSync(absPath)) return null;
  const ext = path.extname(absPath).toLowerCase();
  const b64 = fs.readFileSync(absPath).toString('base64');
  return `data:${mime[ext] || 'application/octet-stream'};base64,${b64}`;
}

function resolveAsset(src) {
  if (!src || src.startsWith('data:') || /^https?:\/\//i.test(src)) return src;
  const clean = String(src).replace(/^\//, '').replace(/^\.\.\//, '');
  const candidates = [
    path.join(root, clean),
    path.join(__dirname, clean),
    path.join(root, 'offerte-ai', clean),
  ];
  for (const c of candidates) {
    const uri = fileToDataUri(c);
    if (uri) return uri;
  }
  return src;
}

const browser = await chromium.launch({ headless: true, executablePath: chromePath });
const page = await browser.newPage({ viewport: { width: 1100, height: 1400 } });

// Usa il generatore live (path assoluti funzionano su localhost)
await page.goto('http://127.0.0.1:8765/offerte-ai/samples/_gen-sacmi-preventivo.html', {
  waitUntil: 'networkidle',
});
await page.waitForFunction(() => document.documentElement.dataset.ready === '1', { timeout: 60000 });

// Forza logo cliente + logo Abra a data-URI lato file system (affidabile)
const sacmiLogo = fileToDataUri(path.join(root, 'images', 'clienti', 'sacmi-logo.jpg'));
const abraLogo = fileToDataUri(path.join(root, 'images', 'logo.png'))
  || fileToDataUri(path.join(root, 'images', 'logo.webp'));

await page.evaluate(({ sacmiLogo, abraLogo }) => {
  if (sacmiLogo) {
    document.querySelectorAll('img.doc-client-logo, img[alt*="SACMI"]').forEach(img => {
      img.src = sacmiLogo;
      img.removeAttribute('loading');
    });
    if (window.__OFFER__?.client) window.__OFFER__.client.logo_url = sacmiLogo;
  }
  if (abraLogo) {
    document.querySelectorAll('img.doc-logo-img').forEach(img => {
      img.src = abraLogo;
      img.removeAttribute('loading');
    });
  }
  // Risolvi anche le altre immagini prodotto dal DOM corrente via fetch→blob non disponibile offline;
  // lasciamo gli URL http per il PDF da localhost.
}, { sacmiLogo, abraLogo });

// Attendi caricamento immagini
await page.evaluate(async () => {
  const imgs = [...document.images];
  await Promise.all(imgs.map(img => {
    if (img.complete && img.naturalWidth > 0) return Promise.resolve();
    return new Promise(resolve => {
      img.onload = () => resolve();
      img.onerror = () => resolve();
      setTimeout(resolve, 4000);
    });
  }));
});

const data = await page.evaluate(() => ({
  offer: window.__OFFER__,
  totals: window.__TOTALS__,
  paperHtml: document.getElementById('paper')?.innerHTML || '',
}));

// Inline TUTTE le immagini del paper via fetch dal server locale
const inlined = await page.evaluate(async () => {
  const paper = document.getElementById('paper');
  if (!paper) return '';
  const imgs = [...paper.querySelectorAll('img')];
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
    } catch (_) {}
  }
  return paper.innerHTML;
});

const cssPath = path.join(root, 'offerte-ai', 'css', 'offerte-ai.css');
const css = fs.readFileSync(cssPath, 'utf8');

const subtotal = Number(data.totals.subtotal).toLocaleString('it-IT', {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});

const standalone = `<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Preventivo ${data.offer.id} — SACMI × Abra Robotics</title>
  <link href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700,900&display=swap" rel="stylesheet">
  <style>
${css}
body.offer-sample-body { background: #e8e8e8; margin: 0; }
.offer-sample-toolbar {
  position: sticky; top: 0; z-index: 10; display: flex; justify-content: space-between;
  align-items: center; gap: 12px; flex-wrap: wrap; padding: 10px 16px;
  background: #111; color: #fff; font-size: 0.85rem;
}
.offer-sample-toolbar .badge {
  display: inline-block; padding: 2px 8px; border-radius: 999px;
  background: #7c4dd6; font-size: 0.7rem; font-weight: 800; margin-right: 8px;
}
.offer-sample-toolbar button, .offer-sample-toolbar a {
  color: #fff; background: transparent; border: 1px solid #555; padding: 6px 10px;
  border-radius: 6px; text-decoration: none; font: inherit; cursor: pointer;
}
.offer-sample-wrap { padding: 24px 12px 48px; }
.offer-sample-paper {
  max-width: 820px; margin: 0 auto; background: #fff; padding: 28px 32px;
  box-shadow: 0 8px 30px rgba(0,0,0,.12);
}
.doc-client-logo { width: 150px !important; max-height: 96px !important; object-fit: contain !important; }
.doc-client.has-logo { align-items: center !important; gap: 16px !important; }
@media print {
  .offer-sample-toolbar { display: none !important; }
  body.offer-sample-body { background: #fff; }
  .offer-sample-wrap { padding: 0; }
  .offer-sample-paper { box-shadow: none; max-width: none; padding: 0; }
}
  </style>
</head>
<body class="offer-sample-body">
  <div class="offer-sample-toolbar">
    <div><span class="badge">Preventivo SACMI</span> ${data.offer.id} · Rif. <strong>€ ${subtotal}</strong></div>
    <div><button type="button" onclick="window.print()">Stampa / PDF</button></div>
  </div>
  <div class="offer-sample-wrap">
    <div class="offer-sample-paper">${inlined}</div>
  </div>
</body>
</html>`;

const outHtml = path.join(__dirname, 'offerta-sacmi-go2-coprogettazione.html');
const outDesktopHtml = path.join(process.env.USERPROFILE || '', 'Desktop', 'offerta-SACMI-preventivo.html');
const outPdf = path.join(process.env.USERPROFILE || '', 'Desktop', 'Preventivo-SACMI-Abra-Robotics.pdf');
const outPdfRepo = path.join(__dirname, 'Preventivo-SACMI-Abra-Robotics.pdf');

fs.writeFileSync(outHtml, standalone, 'utf8');
fs.writeFileSync(outDesktopHtml, standalone, 'utf8');

// PDF da HTML self-contained (file://) così il logo c'è sempre
const pdfPage = await browser.newPage();
await pdfPage.setContent(standalone, { waitUntil: 'networkidle' });
await pdfPage.emulateMedia({ media: 'print' });
await pdfPage.pdf({
  path: outPdf,
  format: 'A4',
  printBackground: true,
  margin: { top: '12mm', bottom: '12mm', left: '10mm', right: '10mm' },
});
fs.copyFileSync(outPdf, outPdfRepo);

// Verifica logo presente
const hasLogo = standalone.includes('data:image') && standalone.includes('doc-client-logo');
const logoOk = await pdfPage.evaluate(() => {
  const img = document.querySelector('img.doc-client-logo');
  return !!(img && img.src.startsWith('data:') && img.naturalWidth > 0);
});

console.log(JSON.stringify({
  id: data.offer.id,
  subtotal: data.totals.subtotal,
  hasLogoInHtml: hasLogo,
  logoRendered: logoOk,
  sacmiLogoBytes: sacmiLogo ? sacmiLogo.length : 0,
  outHtml,
  outDesktopHtml,
  outPdf,
  outPdfRepo,
}, null, 2));

await browser.close();
