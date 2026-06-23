/* Browser knowledge base RAG — documenti, indice, test ricerca. */
(function () {
  'use strict';

  const GH_EDIT = 'https://github.com/niccolomazzoleni-prog/Abra-Robotics/edit/main/offerte-ai/data/knowledge/';
  const KB_FILES = [
    'faq-sorveglianza-quadrupedi.md',
    'prodotti-as2.md',
    'prodotti-a2.md',
    'listino-integrazione-poc.md',
    'faq-vendita.md',
    'faq-prezzi-spedizione.md',
  ];
  const INDEX_URL = '../offerte-ai/data/knowledge-index.json';
  const KB_BASE = '../offerte-ai/data/knowledge/';

  function el(id) { return document.getElementById(id); }

  function esc(s) {
    return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function isCustomKbSource(src) {
    return String(src || '').includes('knowledge');
  }

  function groupBySource(chunks) {
    const map = {};
    for (const c of chunks) {
      const key = c.source || '(unknown)';
      map[key] = (map[key] || 0) + 1;
    }
    return Object.entries(map).sort((a, b) => b[1] - a[1]);
  }

  function renderKpis(index) {
    const chunks = index.chunks || [];
    const custom = chunks.filter((c) => isCustomKbSource(c.source));
    el('kb-kpis').innerHTML = [
      { v: index.chunk_count || chunks.length, l: 'Chunk totali indice' },
      { v: custom.length, l: 'Chunk da knowledge/' },
      { v: KB_FILES.length, l: 'File Markdown editabili' },
      { v: (index.sources && index.sources.listino_skus) || '—', l: 'SKU listino indicizzati' },
    ].map((k) => `
      <div class="kpi">
        <div class="kpi-value">${k.v}</div>
        <div class="kpi-label">${k.l}</div>
      </div>`).join('');
  }

  function renderSources(index) {
    const rows = groupBySource(index.chunks || []);
    el('kb-sources').innerHTML = rows.length
      ? `<table class="kb-table"><thead><tr><th>Fonte</th><th>Chunk</th><th>Tipo</th></tr></thead><tbody>
        ${rows.map(([src, n]) => {
          const custom = isCustomKbSource(src);
          return `<tr>
            <td><code>${esc(src.replace(/\\/g, '/'))}</code></td>
            <td>${n}</td>
            <td>${custom ? 'Knowledge aggiuntiva' : 'Automatico (listino/sito)'}</td>
          </tr>`;
        }).join('')}
      </tbody></table>`
      : '<p class="stats-empty">Indice vuoto.</p>';
  }

  async function loadMdFiles(index) {
    const root = el('kb-docs');
    root.innerHTML = '<p class="hint">Caricamento documenti…</p>';
    const chunks = index.chunks || [];
    const parts = [];

    for (const file of KB_FILES) {
      const srcPath = `offerte-ai/data/knowledge/${file}`;
      const chunkCount = chunks.filter((c) => String(c.source || '').replace(/\\/g, '/').includes(file)).length;
      let text = '';
      try {
        const r = await fetch(KB_BASE + file + '?t=' + Date.now());
        text = r.ok ? await r.text() : '(file non trovato)';
      } catch {
        text = '(errore caricamento)';
      }
      parts.push(`
        <details class="kb-doc" open>
          <summary>
            <strong>${esc(file)}</strong>
            <span class="kb-doc-meta">${chunkCount} chunk nell'indice</span>
          </summary>
          <div class="kb-doc-actions">
            <a class="btn btn-sm" href="${GH_EDIT}${file}" target="_blank" rel="noopener">Modifica su GitHub</a>
            <button type="button" class="btn btn-sm btn-secondary" data-copy="${esc(file)}">Copia path</button>
          </div>
          <pre class="kb-md-preview">${esc(text)}</pre>
        </details>`);
    }
    root.innerHTML = parts.join('');
    root.querySelectorAll('[data-copy]').forEach((btn) => {
      btn.addEventListener('click', () => {
        navigator.clipboard.writeText('offerte-ai/data/knowledge/' + btn.dataset.copy);
        btn.textContent = 'Copiato!';
        setTimeout(() => { btn.textContent = 'Copia path'; }, 1500);
      });
    });
  }

  async function runSearch() {
    const q = el('kb-search-q').value.trim();
    if (!q) return;
    const kb = new AbraKBSearch();
    await kb.load(INDEX_URL);
    const res = kb.search(q, 8);
    el('kb-search-out').innerHTML = res.length
      ? res.map((r, i) => `
        <article class="kb-hit">
          <header><strong>${i + 1}. ${esc(r.title)}</strong>
            <span class="kb-hit-src">${esc((r.source || '').replace(/\\/g, '/'))}</span></header>
          <p>${esc((r.text || '').slice(0, 420))}${(r.text || '').length > 420 ? '…' : ''}</p>
        </article>`).join('')
      : '<p class="stats-empty">Nessun chunk trovato per questa query.</p>';
  }

  async function boot() {
    let index = { chunks: [], chunk_count: 0 };
    try {
      const r = await fetch(INDEX_URL + '?t=' + Date.now());
      index = await r.json();
    } catch (e) {
      el('kb-kpis').innerHTML = `<p class="stats-empty">${e.message}</p>`;
      return;
    }
    renderKpis(index);
    renderSources(index);
    await loadMdFiles(index);

    el('btn-kb-search').addEventListener('click', runSearch);
    el('kb-search-q').addEventListener('keydown', (e) => {
      if (e.key === 'Enter') runSearch();
    });
  }

  document.addEventListener('DOMContentLoaded', boot);
})();
