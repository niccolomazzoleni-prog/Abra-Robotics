/**
 * Pagina Crea offerta — UI + sync form ↔ offer model.
 */
(function () {
  'use strict';

  const fmt = n => Number(n).toLocaleString('it-IT', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  let quote, builder, offer, manifest = {}, blocchiLib = [];

  function esc(s) {
    return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function ensureBlocks(offer) {
    if (!Array.isArray(offer.content_blocks)) offer.content_blocks = [];
    return offer.content_blocks;
  }

  async function mergeCatalogPrices() {
    for (const url of ['../data/amr-products.json', '../data/cobot-products.json']) {
      try {
        const res = await fetch(url);
        if (!res.ok) continue;
        const arr = await res.json();
        for (const p of arr) {
          quote.prices[p.sku] = {
            nome: p.title,
            prezzo_eur: p.price_eur,
            note: p.blurb || p.subtitle || '',
            categoria: url.includes('amr') ? 'AMR' : 'COBOT',
          };
        }
      } catch (_) {}
    }
    const sessionVoci = JSON.parse(sessionStorage.getItem('abra_voci_extra_session') || '[]');
    for (const v of sessionVoci) builder.vociExtra.push(v);
    builder._buildCatalogIndex();
  }

  function syncFormToOffer() {
    offer.client = {
      azienda: document.getElementById('c-azienda').value,
      contatto: document.getElementById('c-contatto').value,
      email: document.getElementById('c-email').value,
      telefono: document.getElementById('c-tel').value,
    };
    offer.margin_key = document.getElementById('c-margin').value;
    offer.intro = document.getElementById('c-intro').value;
    offer.prompt_extra = document.getElementById('c-prompt-extra').value;
    offer.condizioni = document.getElementById('c-condizioni').value;
    offer.chiusura = document.getElementById('c-chiusura').value;
    builder.applyTemplate(offer, document.getElementById('c-template').value);
    offer.intro = document.getElementById('c-intro').value || offer.intro;
    offer.chiusura = document.getElementById('c-chiusura').value || offer.chiusura;
  }

  function syncOfferToForm() {
    document.getElementById('c-azienda').value = offer.client.azienda || '';
    document.getElementById('c-contatto').value = offer.client.contatto || '';
    document.getElementById('c-email').value = offer.client.email || '';
    document.getElementById('c-tel').value = offer.client.telefono || '';
    document.getElementById('c-margin').value = offer.margin_key || 'end_user';
    document.getElementById('c-intro').value = offer.intro || '';
    document.getElementById('c-prompt-extra').value = offer.prompt_extra || '';
    document.getElementById('c-condizioni').value = offer.condizioni || '';
    document.getElementById('c-chiusura').value = offer.chiusura || '';
    if (offer.template_id) document.getElementById('c-template').value = offer.template_id;
  }

  function renderPreview() {
    syncFormToOffer();
    document.getElementById('live-preview').innerHTML = builder.renderPreviewFragment(offer);
  }

  function renderLines() {
    const tbody = document.getElementById('lines-body');
    tbody.innerHTML = offer.line_items.map((l, i) => `
      <tr>
        <td>
          <strong>${esc(l.nome)}</strong>
          ${l.sku ? `<br><small>${esc(l.sku)}</small>` : ''}
          ${l.descrizione ? `<br><small>${esc(l.descrizione)}</small>` : ''}
          ${l.tipo === 'custom' ? ' <span class="tag-custom">custom</span>' : ''}
          ${l.sku && manifest[l.sku] ? `<br><button type="button" class="btn-link-sm btn-sheet" data-sku="${esc(l.sku)}">+ Scheda prodotto</button>` : ''}
        </td>
        <td><input type="number" min="1" value="${l.qty}" data-idx="${i}" class="qty-inp" style="width:60px"></td>
        <td>${l.su_richiesta || !l.prezzo_unit ? 'Su richiesta' : '€ ' + fmt(l.prezzo_unit)}</td>
        <td>${l.su_richiesta || !l.prezzo_totale ? '—' : '€ ' + fmt(l.prezzo_totale)}</td>
        <td><button type="button" class="btn-del" data-idx="${i}">×</button></td>
      </tr>`).join('') || '<tr><td colspan="5" class="lines-empty">Cerca un prodotto o aggiungi voce custom</td></tr>';

    tbody.querySelectorAll('.btn-del').forEach(b => b.addEventListener('click', () => {
      builder.removeLine(offer, +b.dataset.idx);
      renderLines();
    }));
    tbody.querySelectorAll('.qty-inp').forEach(inp => inp.addEventListener('change', () => {
      offer.line_items[+inp.dataset.idx].qty = Math.max(1, +inp.value || 1);
      renderLines();
    }));
    tbody.querySelectorAll('.btn-sheet').forEach(btn => btn.addEventListener('click', () => {
      if (builder.addProductSheetBlock(offer, btn.dataset.sku, manifest)) {
        renderBlocks();
        renderPreview();
        AbraUI.toast('Scheda prodotto aggiunta', 'ok');
      }
    }));

    const t = builder.recalculate(offer);
    document.getElementById('totals-box').innerHTML =
      `<div>Subtotale: <strong>€ ${fmt(t.subtotal)}</strong></div>` +
      `<div class="grand">Totale: <strong>€ ${fmt(t.totale)}</strong> <span class="iva-note">(${esc(offer.note_iva)})</span></div>`;
    renderPreview();
  }

  function blockTypeLabel(type) {
    return { section: 'Testo', image: 'Immagine', gallery: 'Galleria', highlight: 'Highlight' }[type] || type;
  }

  function renderBlocks() {
    ensureBlocks(offer);
    const list = document.getElementById('blocks-list');
    if (!offer.content_blocks.length) {
      list.innerHTML = '<p class="blocks-empty">Aggiungi sezioni testo, immagini o blocchi ricorrenti per un\'offerta più parlante.</p>';
      return;
    }
    list.innerHTML = offer.content_blocks.map((b, i) => `
      <article class="block-card" data-id="${esc(b.id)}">
        <div class="block-card-head">
          <span class="block-type-tag">${blockTypeLabel(b.type)}</span>
          <strong>${esc(b.title || b.caption || 'Senza titolo')}</strong>
          <div class="block-card-actions">
            <button type="button" class="btn-icon" data-act="up" data-idx="${i}" title="Su" ${i === 0 ? 'disabled' : ''}>↑</button>
            <button type="button" class="btn-icon" data-act="down" data-idx="${i}" title="Giù" ${i === offer.content_blocks.length - 1 ? 'disabled' : ''}>↓</button>
            <button type="button" class="btn-icon btn-icon-del" data-act="del" data-id="${esc(b.id)}" title="Elimina">×</button>
          </div>
        </div>
        <div class="block-card-body">
          ${b.type === 'section' || b.type === 'highlight' ? `<p class="block-preview-text">${esc((b.body || '').slice(0, 120))}${(b.body || '').length > 120 ? '…' : ''}</p>` : ''}
          ${b.image_url ? `<img class="block-thumb" src="${esc(b.image_url)}" alt="" loading="lazy" onerror="this.classList.add('img-broken')">` : ''}
          ${b.type === 'gallery' && b.images?.length ? `<div class="block-gallery-thumb">${b.images.slice(0, 3).map(img => `<img src="${esc(img.url)}" alt="" loading="lazy">`).join('')}${b.images.length > 3 ? `<span>+${b.images.length - 3}</span>` : ''}</div>` : ''}
        </div>
        <details class="block-edit">
          <summary>Modifica</summary>
          <div class="block-edit-fields">
            <label>Titolo<input type="text" data-field="title" data-id="${esc(b.id)}" value="${esc(b.title || '')}"></label>
            ${b.type !== 'gallery' ? `<label>Testo<textarea rows="2" data-field="body" data-id="${esc(b.id)}">${esc(b.body || '')}</textarea></label>` : ''}
            ${b.type === 'image' || b.type === 'highlight' ? `
              <label>URL immagine<input type="url" data-field="image_url" data-id="${esc(b.id)}" value="${esc(b.image_url || '')}" placeholder="../images/..."></label>
              <label>Didascalia<input type="text" data-field="caption" data-id="${esc(b.id)}" value="${esc(b.caption || '')}"></label>
              <label class="file-upload-label">Carica file<input type="file" accept="image/*" data-upload="${esc(b.id)}"></label>
            ` : ''}
            ${b.type === 'gallery' ? `<p class="block-hint">Modifica le URL immagini nel JSON bozza o ricrea la galleria.</p>` : ''}
          </div>
        </details>
      </article>`).join('');

    list.querySelectorAll('[data-field]').forEach(el => {
      el.addEventListener('input', () => {
        const blk = offer.content_blocks.find(x => x.id === el.dataset.id);
        if (blk) blk[el.dataset.field] = el.value;
        renderBlocks();
        renderPreview();
      });
    });
    list.querySelectorAll('[data-upload]').forEach(inp => {
      inp.addEventListener('change', () => {
        const file = inp.files?.[0];
        if (!file) return;
        if (file.size > 800000) return AbraUI.toast('Immagine troppo grande (max ~800 KB)', 'warn');
        const reader = new FileReader();
        reader.onload = () => {
          const blk = offer.content_blocks.find(x => x.id === inp.dataset.upload);
          if (blk) { blk.image_url = reader.result; renderBlocks(); renderPreview(); AbraUI.toast('Immagine caricata', 'ok'); }
        };
        reader.readAsDataURL(file);
      });
    });
    list.querySelectorAll('[data-act]').forEach(btn => {
      btn.addEventListener('click', () => {
        const act = btn.dataset.act;
        if (act === 'del') {
          builder.removeBlock(offer, btn.dataset.id);
        } else {
          builder.moveBlock(offer, +btn.dataset.idx, act === 'up' ? -1 : 1);
        }
        renderBlocks();
        renderPreview();
      });
    });
  }

  function bindEvents() {
    document.querySelectorAll('#c-azienda,#c-contatto,#c-email,#c-tel,#c-intro,#c-prompt-extra,#c-condizioni,#c-chiusura').forEach(el => {
      el.addEventListener('input', renderPreview);
    });

    document.getElementById('search-prod').addEventListener('input', () => {
      const searchInp = document.getElementById('search-prod');
      const searchRes = document.getElementById('search-results');
      const q = searchInp.value.trim();
      if (q.length < 2) { searchRes.innerHTML = ''; return; }
      searchRes.innerHTML = builder.searchCatalog(q).map(h => `
        <button type="button" class="hit" data-sku="${esc(h.sku)}">
          ${esc(h.nome)} <small>${esc(h.sku)} · € ${fmt(h.prezzo_eur || 0)}</small>
        </button>`).join('') || '<p class="no-hit">Nessun risultato</p>';
      searchRes.querySelectorAll('.hit').forEach(btn => btn.addEventListener('click', () => {
        offer.margin_key = document.getElementById('c-margin').value;
        builder.addCatalogLine(offer, btn.dataset.sku, 1);
        searchInp.value = '';
        searchRes.innerHTML = '';
        renderLines();
        AbraUI.toast('Prodotto aggiunto', 'ok');
      }));
    });

    document.getElementById('btn-add-custom').addEventListener('click', () => {
      const nome = document.getElementById('custom-nome').value.trim();
      const prezzo = document.getElementById('custom-prezzo').value;
      if (!nome || !prezzo) return AbraUI.toast('Nome e prezzo obbligatori', 'warn');
      builder.addCustomLine(offer, nome, prezzo, +document.getElementById('custom-qty').value || 1,
        document.getElementById('custom-desc').value, 'manuale');
      ['custom-nome', 'custom-desc', 'custom-prezzo'].forEach(id => document.getElementById(id).value = '');
      renderLines();
      AbraUI.toast('Voce custom aggiunta', 'ok');
    });

    document.getElementById('c-template').addEventListener('change', () => {
      builder.applyTemplate(offer, document.getElementById('c-template').value);
      document.getElementById('c-intro').value = offer.intro;
      document.getElementById('c-chiusura').value = offer.chiusura;
      renderPreview();
    });

    document.getElementById('btn-save-draft').addEventListener('click', () => {
      syncFormToOffer();
      builder.saveDraft(offer);
      AbraUI.toast('Bozza salvata', 'ok');
    });

    document.getElementById('btn-export').addEventListener('click', () => {
      syncFormToOffer();
      builder.exportPrint(offer);
    });

    document.getElementById('btn-add-section').addEventListener('click', () => {
      builder.addBlock(offer, {
        type: 'section',
        title: document.getElementById('new-section-title').value.trim() || 'Sezione',
        body: document.getElementById('new-section-body').value.trim(),
      });
      document.getElementById('new-section-title').value = '';
      document.getElementById('new-section-body').value = '';
      renderBlocks();
      renderPreview();
      AbraUI.toast('Sezione aggiunta', 'ok');
    });

    document.getElementById('btn-add-image').addEventListener('click', () => {
      const url = document.getElementById('new-image-url').value.trim();
      if (!url) return AbraUI.toast('Inserisci URL immagine', 'warn');
      builder.addBlock(offer, {
        type: 'image',
        title: '',
        image_url: url,
        caption: document.getElementById('new-image-caption').value.trim(),
      });
      document.getElementById('new-image-url').value = '';
      document.getElementById('new-image-caption').value = '';
      renderBlocks();
      renderPreview();
    });

    document.getElementById('new-image-file').addEventListener('change', e => {
      const file = e.target.files?.[0];
      if (!file) return;
      if (file.size > 800000) return AbraUI.toast('Max ~800 KB per bozza locale', 'warn');
      const reader = new FileReader();
      reader.onload = () => {
        builder.addBlock(offer, {
          type: 'image',
          image_url: reader.result,
          caption: document.getElementById('new-image-caption').value.trim() || file.name,
        });
        document.getElementById('new-image-caption').value = '';
        e.target.value = '';
        renderBlocks();
        renderPreview();
        AbraUI.toast('Immagine aggiunta', 'ok');
      };
      reader.readAsDataURL(file);
    });

    document.getElementById('recurring-select').addEventListener('change', e => {
      const id = e.target.value;
      if (!id) return;
      if (builder.insertRecurringBlock(offer, id, blocchiLib)) {
        renderBlocks();
        renderPreview();
        AbraUI.toast('Blocco ricorrente inserito', 'ok');
      }
      e.target.value = '';
    });
  }

  async function init() {
    AbraUI.mountNav('offerta');
    quote = new AbraQuoteEngine();
    builder = new AbraOfferBuilder(quote);

    await quote.load('../listini/pubblico/end-user.json', 'data/offerte-regole.json')
      .catch(() => quote.load('data/sample-prices.json', 'data/offerte-regole.json'));
    await builder.load('data/offerte-config.json', 'data/voci-extra.json');
    await mergeCatalogPrices();

    try {
      manifest = await fetch('../listini/pubblico/catalogo-manifest.json').then(r => r.json());
    } catch (_) { manifest = {}; }

    try {
      blocchiLib = (await fetch('data/blocchi-ricorrenti.json').then(r => r.json())).blocchi || [];
    } catch (_) { blocchiLib = []; }

    const tplSel = document.getElementById('c-template');
    tplSel.innerHTML = (builder.config?.prompt_templates || []).map(t =>
      `<option value="${t.id}">${esc(t.label)}</option>`).join('');

    const recSel = document.getElementById('recurring-select');
    recSel.innerHTML = '<option value="">— Inserisci blocco ricorrente —</option>' +
      blocchiLib.map(b => `<option value="${esc(b.id)}">${esc(b.label)}</option>`).join('');

    const chatDraftRaw = sessionStorage.getItem('abra_offer_draft');
    if (chatDraftRaw) {
      try {
        offer = JSON.parse(chatDraftRaw);
        if (!Array.isArray(offer.content_blocks)) offer.content_blocks = [];
        sessionStorage.removeItem('abra_offer_draft');
        sessionStorage.removeItem('abra_chat_quote_prefill');
        builder.saveDraft(offer);
        AbraUI.toast('Preventivo completo importato dalla chat', 'ok');
      } catch (_) {
        offer = builder.createEmpty();
      }
    } else {
      const draft = builder.loadDraft();
      offer = draft || builder.createEmpty();
      if (!draft) {
        document.getElementById('c-condizioni').value = offer.condizioni;
        builder.applyTemplate(offer, 'standard');
      }
      const chatPrefill = sessionStorage.getItem('abra_chat_quote_prefill');
      if (chatPrefill) {
        try {
          const p = JSON.parse(chatPrefill);
          if (p.full) {
            sessionStorage.removeItem('abra_chat_quote_prefill');
          } else {
            if (p.margin_key) offer.margin_key = p.margin_key;
            for (const sku of p.skus || []) builder.addCatalogLine(offer, sku, 1);
            sessionStorage.removeItem('abra_chat_quote_prefill');
            AbraUI.toast('Righe importate dalla chat', 'ok');
          }
        } catch (_) {}
      }
    }

    ensureBlocks(offer);
    syncOfferToForm();
    bindEvents();
    renderBlocks();
    renderLines();
  }

  if (window.AbraAdmin?.whenUnlocked) window.AbraAdmin.whenUnlocked(init);
  else init();
})();
