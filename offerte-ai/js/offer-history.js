/**
 * Cronologia offerte in localStorage (browser locale).
 */
(function (global) {
  'use strict';

  const STORAGE_KEY = 'abra_offer_history';
  const MAX_ITEMS = 20;

  const SAMPLE_OFFERS = [
    { id: 'OFF-20260623-YSZJ', label: 'Sorveglianza + Go2 (completa)', total: 40260, href: '../offerte-ai/samples/offerta-completa-sorveglianza-go2.html', date: '2026-06-23' },
    { id: 'OFF-20260623-MCQR', label: 'Sorveglianza + Go2 (curata)', total: 40260, href: '../offerte-ai/samples/offerta-curata-sorveglianza-go2.html', date: '2026-06-23' },
    { id: 'OFF-20260623-RYSM', label: 'Sorveglianza As2/A2', total: null, href: '../offerte-ai/samples/offerta-sorveglianza-as2-a2.html', date: '2026-06-23' },
    { id: 'OFF-20260623-FHFD', label: 'Go2 EDU RFQ', total: null, href: '../offerte-ai/samples/offerta-go2-edu-rfq.html', date: '2026-06-23' },
  ];

  function fmt(n) {
    return Number(n).toLocaleString('it-IT', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }

  function load() {
    try {
      const arr = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
      return Array.isArray(arr) ? arr : [];
    } catch {
      return [];
    }
  }

  function save(items) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items.slice(0, MAX_ITEMS)));
  }

  function summarize(offer, builder) {
    const t = builder?.recalculate?.(offer) || { totale: 0, primarySku: '', opzioni: [] };
    const primary = (offer.line_items || []).find(l => l.principale)
      || (offer.line_items || []).find(l => l.robot_gruppo === 'sorveglianza')
      || (offer.line_items || []).find(l => l.opzione_robot);
    return {
      id: offer.id || '—',
      date: offer.data || new Date().toISOString().slice(0, 10),
      client: offer.client?.azienda || offer.client?.contatto || '—',
      template: offer.template_id || 'standard',
      margin: offer.margin_key || 'end_user',
      total: t.totale,
      reference: primary?.nome || t.primarySku || '—',
      robots: (t.opzioni || []).length,
      saved_at: new Date().toISOString(),
    };
  }

  function record(offer, builder) {
    if (!offer?.id) return;
    const entry = summarize(offer, builder);
    const items = load().filter(x => x.id !== entry.id);
    items.unshift(entry);
    save(items);
    return entry;
  }

  function marginLabel(key) {
    return { end_user: 'End-User', partner_a: 'Partner A (−5%)', partner_b: 'Partner B (−10%)' }[key] || key;
  }

  function renderList(container, opts) {
    if (!container) return;
    const local = load();
    const samples = opts?.includeSamples !== false ? SAMPLE_OFFERS : [];
    const rows = [...local, ...samples.filter(s => !local.some(l => l.id === s.id))];

    if (!rows.length) {
      container.innerHTML = '<p class="hint">Nessuna offerta salvata in questo browser.</p>';
      return;
    }

    container.innerHTML = `
      <table class="offer-history-table">
        <thead>
          <tr><th>ID / Data</th><th>Cliente</th><th>Riferimento</th><th>Totale IVA escl.</th><th></th></tr>
        </thead>
        <tbody>
          ${rows.map(r => `
            <tr>
              <td>
                <strong>${r.id}</strong><br>
                <small>${r.date || ''}${r.saved_at ? ' · salvata ' + r.saved_at.slice(0, 16).replace('T', ' ') : ''}</small>
              </td>
              <td>${r.client || '—'}<br><small>${r.label || marginLabel(r.margin)}</small></td>
              <td>${r.reference || '—'}${r.robots > 1 ? `<br><small>${r.robots} configurazioni robot</small>` : ''}</td>
              <td>${r.total != null ? '€ ' + fmt(r.total) : '—'}</td>
              <td>${r.href ? `<a href="${r.href}" target="_blank" rel="noopener">Apri</a>` : ''}</td>
            </tr>`).join('')}
        </tbody>
      </table>`;
  }

  global.AbraOfferHistory = { record, load, renderList, summarize, SAMPLE_OFFERS };
})(typeof window !== 'undefined' ? window : globalThis);
