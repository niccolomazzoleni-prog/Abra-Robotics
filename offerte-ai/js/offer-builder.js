/**
 * Generatore offerte — catalogo, content blocks, anteprima e PDF.
 */
(function (global) {
  'use strict';

  const fmt = n => Number(n).toLocaleString('it-IT', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const STORAGE_DRAFT = 'abra_offerta_draft';

  function escapeHtml(s) {
    return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function blockId() {
    return 'blk-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 5);
  }

  function nl2br(text) {
    return richText(text);
  }

  function richText(text) {
    let s = escapeHtml(String(text || ''));
    s = s.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    s = s.replace(/\*(.+?)\*/g, '<strong>$1</strong>');
    s = s.replace(/_(.+?)_/g, '<em>$1</em>');
    return s.replace(/\n/g, '<br>');
  }

  class OfferBuilder {
    constructor(quoteEngine) {
      this.quote = quoteEngine;
      this.config = null;
      this.vociExtra = [];
      this.catalogIndex = [];
      this.recurringBlocks = [];
    }

    async load(configUrl, vociUrl, blocchiUrl) {
      const [cRes, vRes, bRes] = await Promise.all([
        fetch(configUrl),
        fetch(vociUrl),
        blocchiUrl ? fetch(blocchiUrl) : Promise.resolve(null),
      ]);
      if (cRes.ok) this.config = await cRes.json();
      if (vRes.ok) this.vociExtra = (await vRes.json()).voci || [];
      if (bRes?.ok) this.recurringBlocks = ((await bRes.json()).blocchi) || [];
      this._buildCatalogIndex();
    }

    _buildCatalogIndex() {
      const items = [];
      for (const [sku, p] of Object.entries(this.quote.prices || {})) {
        items.push({ sku, nome: p.nome, prezzo_eur: p.prezzo_eur, categoria: p.categoria, tipo: 'unitree' });
      }
      for (const v of this.vociExtra) {
        items.push({
          sku: v.id || `extra-${v.nome}`,
          nome: v.nome,
          prezzo_eur: v.prezzo_eur,
          descrizione: v.descrizione,
          tipo: 'extra',
        });
      }
      this.catalogIndex = items;
    }

    searchCatalog(q, limit = 12) {
      const t = q.toLowerCase().trim();
      if (!t) return this.catalogIndex.slice(0, limit);
      return this.catalogIndex.filter(i =>
        i.sku.toLowerCase().includes(t) ||
        i.nome.toLowerCase().includes(t) ||
        (i.categoria || '').toLowerCase().includes(t)
      ).slice(0, limit);
    }

    createEmpty(client = {}) {
      const tpl = this.config?.prompt_templates?.[0] || {};
      return {
        id: `OFF-${new Date().toISOString().slice(0, 10).replace(/-/g, '')}-${Math.random().toString(36).slice(2, 6).toUpperCase()}`,
        data: new Date().toISOString().slice(0, 10),
        validita_giorni: this.config?.default_validita_giorni || 30,
        template_id: tpl.id || 'standard',
        client: { azienda: '', contatto: '', email: '', telefono: '', ...client },
        intro: tpl.intro || '',
        chiusura: tpl.chiusura || '',
        note_iva: this.config?.note_iva_default || 'IVA esclusa',
        condizioni: this.config?.condizioni_default || '',
        prompt_extra: '',
        margin_key: 'end_user',
        line_items: [],
        content_blocks: [],
      };
    }

    /* --- Righe --- */

    addCatalogLine(offer, sku, qty = 1, opts = {}) {
      const p = this.quote.getPrice(sku);
      if (!p) {
        const extra = this.vociExtra.find(v => v.id === sku || v.nome === sku);
        if (extra) return this.addCustomLine(offer, extra.nome, extra.prezzo_eur, qty, extra.descrizione, 'catalogo-extra');
        return false;
      }
      const margin = this.quote.rules.margins?.[offer.margin_key] || 0;
      const prezzo = p.prezzo_eur * (1 + margin / 100);
      const line = {
        tipo: 'catalogo', sku: p.sku, nome: p.nome, descrizione: p.note || '',
        qty, prezzo_unit: prezzo, prezzo_totale: prezzo * qty,
      };
      if (opts.opzione_robot) line.opzione_robot = true;
      if (opts.robot_gruppo) line.robot_gruppo = opts.robot_gruppo;
      if (opts.principale) line.principale = true;
      if (opts.alternativa) {
        line.descrizione = [line.descrizione, 'Alternativa — selezionare una sola configurazione robot'].filter(Boolean).join(' · ');
      }
      offer.line_items.push(line);
      return true;
    }

    addCustomLine(offer, nome, prezzo_eur, qty = 1, descrizione = '', source = 'manuale') {
      const prezzo = parseFloat(String(prezzo_eur).replace(',', '.')) || 0;
      offer.line_items.push({
        tipo: 'custom', sku: '', nome: nome.trim(), descrizione: descrizione.trim(),
        qty: qty || 1, prezzo_unit: prezzo, prezzo_totale: prezzo * (qty || 1), source,
      });
      return true;
    }

    removeLine(offer, index) { offer.line_items.splice(index, 1); }

    recalculate(offer) {
      const lines = offer.line_items || [];
      const robots = lines.filter(l => l.opzione_robot);
      const shared = lines.filter(l => !l.opzione_robot);
      let sharedTotal = 0;
      for (const line of shared) {
        line.prezzo_totale = line.su_richiesta ? 0 : line.prezzo_unit * line.qty;
        if (!line.su_richiesta) sharedTotal += line.prezzo_totale;
      }
      for (const line of robots) {
        line.prezzo_totale = line.su_richiesta ? 0 : line.prezzo_unit * line.qty;
      }
      const opzioni = robots.map(r => ({
        sku: r.sku,
        nome: r.nome,
        totale: sharedTotal + (r.su_richiesta ? 0 : r.prezzo_totale),
      }));

      const GRUPPO_LABEL = {
        sorveglianza: 'Applicazione sorveglianza (As2 / A2 — consigliato)',
        go2: 'Alternativa Go2 EDU (Standard / Smart)',
        default: 'Configurazione robot',
      };
      const byGruppo = new Map();
      for (const r of robots) {
        const g = r.robot_gruppo || 'default';
        if (!byGruppo.has(g)) byGruppo.set(g, []);
        byGruppo.get(g).push(r);
      }
      const gruppi = [...byGruppo.entries()].map(([id, rs]) => ({
        id,
        label: GRUPPO_LABEL[id] || id,
        opzioni: rs.map(r => ({
          sku: r.sku,
          nome: r.nome,
          totale: sharedTotal + (r.su_richiesta ? 0 : r.prezzo_totale),
        })),
      }));

      const primary = robots.find(r => r.principale)
        || robots.find(r => r.robot_gruppo === 'sorveglianza')
        || robots[0];
      const subtotal = primary
        ? sharedTotal + (primary.su_richiesta ? 0 : primary.prezzo_totale)
        : sharedTotal;
      const iva_pct = offer.applica_iva ? (offer.iva_pct || 22) : 0;
      const iva_eur = subtotal * (iva_pct / 100);
      return { subtotal, sharedTotal, opzioni, gruppi, iva_pct, iva_eur, totale: subtotal + iva_eur, count: lines.length };
    }

    applyTemplate(offer, templateId) {
      const tpl = (this.config?.prompt_templates || []).find(t => t.id === templateId);
      if (!tpl) return;
      offer.template_id = templateId;
      offer.intro = tpl.intro;
      offer.chiusura = tpl.chiusura;
    }

    /* --- Content blocks --- */

    _ensureBlocks(offer) {
      if (!Array.isArray(offer.content_blocks)) offer.content_blocks = [];
      return offer.content_blocks;
    }

    addBlock(offer, block) {
      const blocks = this._ensureBlocks(offer);
      blocks.push({ id: blockId(), ...block });
      return blocks[blocks.length - 1];
    }

    removeBlock(offer, id) {
      const blocks = this._ensureBlocks(offer);
      const i = blocks.findIndex(b => b.id === id);
      if (i >= 0) blocks.splice(i, 1);
    }

    moveBlock(offer, index, delta) {
      const blocks = this._ensureBlocks(offer);
      const j = index + delta;
      if (j < 0 || j >= blocks.length) return;
      [blocks[index], blocks[j]] = [blocks[j], blocks[index]];
    }

    insertRecurringBlock(offer, recurringId, library) {
      const lib = library || this.recurringBlocks;
      const src = lib.find(b => b.id === recurringId);
      if (!src) return false;
      const copy = JSON.parse(JSON.stringify(src));
      delete copy.label;
      copy.id = blockId();
      this._ensureBlocks(offer).push(copy);
      return true;
    }

    addProductSheetBlock(offer, sku, manifest) {
      const m = manifest?.[sku];
      if (!m) return false;
      const specs = (m.specs || []).slice(0, 6).map(s => `• ${s[0]}: ${s[1]}`).join('\n');
      this.addBlock(offer, {
        type: 'highlight',
        title: m.titolo || sku,
        body: [m.sottotitolo, m.descrizione, specs].filter(Boolean).join('\n\n'),
        image_url: m.immagine ? '../' + m.immagine.replace(/^\//, '') : '',
        caption: m.categoria || '',
        sku,
      });
      return true;
    }

    renderContentBlocksHtml(blocks, { print = false } = {}) {
      if (!blocks?.length) return '';
      const cls = print ? 'print-block' : 'doc-block';
      return blocks.map(b => {
        if (b.type === 'section') {
          return `<section class="${cls} ${cls}-section">
            ${b.title ? `<h3 class="${cls}-title">${escapeHtml(b.title)}</h3>` : ''}
            <div class="${cls}-body">${richText(b.body)}</div>
          </section>`;
        }
        if (b.type === 'image') {
          return `<figure class="${cls} ${cls}-figure">
            <img src="${escapeHtml(b.image_url)}" alt="${escapeHtml(b.caption || b.title || '')}" loading="lazy">
            ${b.caption ? `<figcaption>${escapeHtml(b.caption)}</figcaption>` : ''}
          </figure>`;
        }
        if (b.type === 'gallery') {
          const imgs = (b.images || []).map(img =>
            `<figure class="${cls}-gallery-item"><img src="${escapeHtml(img.url)}" alt="${escapeHtml(img.caption || '')}"><figcaption>${escapeHtml(img.caption || '')}</figcaption></figure>`
          ).join('');
          return `<section class="${cls} ${cls}-gallery">
            ${b.title ? `<h3 class="${cls}-title">${escapeHtml(b.title)}</h3>` : ''}
            <div class="${cls}-gallery-grid">${imgs}</div>
          </section>`;
        }
        if (b.type === 'highlight') {
          return `<section class="${cls} ${cls}-highlight">
            ${b.image_url ? `<div class="${cls}-highlight-img"><img src="${escapeHtml(b.image_url)}" alt="${escapeHtml(b.title || '')}"></div>` : ''}
            <div class="${cls}-highlight-text">
              ${b.title ? `<h3 class="${cls}-title">${escapeHtml(b.title)}</h3>` : ''}
              <div class="${cls}-body">${richText(b.body)}</div>
              ${b.caption ? `<p class="${cls}-caption">${escapeHtml(b.caption)}</p>` : ''}
            </div>
          </section>`;
        }
        return '';
      }).join('');
    }

    renderCompanyHeader(co) {
      const logo = co.logo_url || '../images/logo.png';
      return `
        <div class="doc-header">
          <img class="doc-logo-img" src="${escapeHtml(logo)}" alt="${escapeHtml(co.nome || 'Abra Robotics')}" width="140" height="40">
          <div class="doc-fiscal">
            <strong>${escapeHtml(co.ragione_sociale || co.nome || '')}</strong><br>
            P.IVA ${escapeHtml(co.piva || '')}<br>
            ${escapeHtml(co.indirizzo || '')}<br>
            ${escapeHtml(co.email || '')}${co.telefono ? ' · ' + escapeHtml(co.telefono) : ''}
          </div>
        </div>`;
    }

    _priceCell(l) {
      if (l.su_richiesta || (l.tipo === 'custom' && !l.prezzo_unit)) return 'Su richiesta';
      return '€ ' + fmt(l.prezzo_unit);
    }

    _totalCell(l) {
      if (l.su_richiesta || (l.tipo === 'custom' && !l.prezzo_totale)) return '—';
      return '€ ' + fmt(l.prezzo_totale);
    }

    renderPreviewFragment(offer) {
      const co = this.config?.azienda || {};
      const t = this.recalculate(offer);
      const hasContent = offer.line_items.length || offer.client.azienda || offer.content_blocks?.length;
      if (!hasContent) {
        return '<div class="offer-preview-empty">Aggiungi cliente, righe o sezioni narrative per l\'anteprima</div>';
      }
      const rows = offer.line_items.map(l => `
        <tr>
          <td><strong>${escapeHtml(l.nome)}</strong>${l.sku ? `<br><small>${escapeHtml(l.sku)}</small>` : ''}${l.descrizione ? `<br><small class="line-desc">${escapeHtml(l.descrizione)}</small>` : ''}</td>
          <td>${l.qty}</td>
          <td>${this._priceCell(l)}</td>
          <td>${this._totalCell(l)}</td>
        </tr>`).join('');
      const blocksHtml = this.renderContentBlocksHtml(offer.content_blocks);
      return `
        <div class="abra-offer-doc">
        ${this.renderCompanyHeader(co)}
        <div class="doc-meta">Offerta <strong>${escapeHtml(offer.id)}</strong> · ${escapeHtml(offer.data)} · Valida ${offer.validita_giorni} gg</div>
        <div class="doc-client">
          <strong>${escapeHtml(offer.client.azienda || 'Cliente — da compilare')}</strong><br>
          ${offer.client.contatto ? escapeHtml(offer.client.contatto) + '<br>' : '<span class="muted">Referente — da compilare</span><br>'}
          ${offer.client.email ? escapeHtml(offer.client.email) : ''}
        </div>
        ${offer.intro ? `<div class="doc-intro">${richText(offer.intro)}</div>` : ''}
        ${blocksHtml}
        ${offer.prompt_extra ? `<div class="doc-intro doc-extra"><em>${richText(offer.prompt_extra)}</em></div>` : ''}
        ${rows ? `<table class="doc-lines"><thead><tr><th>Descrizione</th><th>Qtà</th><th>Unit.</th><th>Tot.</th></tr></thead><tbody>${rows}</tbody></table>` : ''}
        ${t.gruppi?.length > 1
          ? t.gruppi.map(g => `<div class="doc-options"><strong>${escapeHtml(g.label)}</strong> <span class="muted">(scegliere una)</span><ul>${g.opzioni.map(o => `<li>${escapeHtml(o.nome.split('(')[0].trim())}: <strong>€ ${fmt(o.totale)}</strong></li>`).join('')}</ul></div>`).join('')
          : (t.opzioni?.length > 1 ? `<div class="doc-options"><strong>Totali per configurazione robot</strong> <span class="muted">(alternativa — scegliere una)</span><ul>${t.opzioni.map(o => `<li>${escapeHtml(o.nome.split('(')[0].trim())}: <strong>€ ${fmt(o.totale)}</strong></li>`).join('')}</ul></div>` : '')}
        <div class="doc-total">Totale configurazione consigliata: <strong>€ ${fmt(t.subtotal)}</strong> <span class="doc-iva-note">(${escapeHtml(offer.note_iva)})</span></div>
        ${offer.condizioni ? `<div class="doc-footer">${richText(offer.condizioni)}</div>` : ''}
        ${offer.chiusura ? `<div class="doc-footer doc-chiusura">${richText(offer.chiusura)}</div>` : ''}
        </div>`;
    }

    _printStyles() {
      return `
        @import url('https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700,900&display=swap');
        body{font-family:'Satoshi',system-ui,sans-serif;max-width:820px;margin:40px auto;padding:0 28px;color:#111;line-height:1.55}
        h1{font-size:1.5rem;margin:0 0 4px;letter-spacing:-0.02em}
        .meta{color:#525252;font-size:0.88rem;margin-bottom:24px}
        table{width:100%;border-collapse:collapse;margin:24px 0;font-size:0.88rem}
        th,td{border-bottom:1px solid #e5e5e5;padding:10px 8px;text-align:left;vertical-align:top}
        th{font-size:0.68rem;text-transform:uppercase;color:#737373;letter-spacing:0.04em}
        .totals{text-align:right;margin-top:20px}
        .totals .grand{font-size:1.25rem;font-weight:800}
        .block{white-space:pre-wrap;margin:16px 0;font-size:0.92rem}
        .footer{margin-top:28px;padding-top:16px;border-top:1px solid #e5e5e5;font-size:0.82rem;color:#525252}
        .print-block{margin:28px 0;page-break-inside:avoid}
        .print-block-title{font-size:1.05rem;font-weight:800;margin:0 0 8px;letter-spacing:-0.02em}
        .print-block-body{font-size:0.9rem;color:#333}
        .print-block-figure{margin:24px 0;text-align:center}
        .print-block-figure img{max-width:100%;max-height:320px;border-radius:8px}
        .print-block-figure figcaption{font-size:0.78rem;color:#737373;margin-top:8px}
        .print-block-gallery-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin-top:12px}
        .print-block-gallery-item img{width:100%;height:140px;object-fit:cover;border-radius:8px}
        .print-block-gallery-item figcaption{font-size:0.72rem;color:#737373;margin-top:4px}
        .print-block-highlight{display:grid;grid-template-columns:200px 1fr;gap:20px;align-items:start;background:#fafafa;border-radius:12px;padding:16px;border:1px solid #e5e5e5}
        .print-block-highlight-img img{width:100%;border-radius:8px}
        .print-block-caption{font-size:0.75rem;color:#737373;margin-top:8px;text-transform:uppercase;letter-spacing:0.04em}
        .doc-options{margin:20px 0;padding:14px 16px;background:#fafafa;border-radius:10px;border:1px solid #e5e5e5;font-size:0.88rem}
        .doc-options ul{margin:8px 0 0;padding-left:18px}
        .doc-options li{margin:4px 0}
        .muted{color:#737373;font-style:italic}
        @media print{body{margin:0;max-width:none}.print-block{page-break-inside:avoid}}
        @media(max-width:600px){.print-block-highlight{grid-template-columns:1fr}}`;
    }

    toPrintHtml(offer) {
      const co = this.config?.azienda || {};
      const t = this.recalculate(offer);
      const rows = offer.line_items.map((l, i) => `
        <tr>
          <td>${i + 1}</td>
          <td><strong>${escapeHtml(l.nome)}</strong>${l.sku ? `<br><small>${escapeHtml(l.sku)}</small>` : ''}${l.descrizione ? `<br><small>${escapeHtml(l.descrizione)}</small>` : ''}</td>
          <td style="text-align:center">${l.qty}</td>
          <td style="text-align:right">${this._priceCell(l)}</td>
          <td style="text-align:right">${this._totalCell(l)}</td>
        </tr>`).join('');
      const blocksHtml = this.renderContentBlocksHtml(offer.content_blocks, { print: true });
      const header = this.renderCompanyHeader(co);

      return `<!DOCTYPE html><html lang="it"><head><meta charset="UTF-8">
        <title>Offerta ${escapeHtml(offer.id)} — ${escapeHtml(offer.client.azienda || 'Cliente')}</title>
        <style>${this._printStyles()}
        .doc-header{display:flex;justify-content:space-between;align-items:flex-start;gap:24px;margin-bottom:24px;padding-bottom:16px;border-bottom:2px solid #111}
        .doc-logo-img{max-height:56px;width:auto}
        .doc-fiscal{font-size:0.82rem;text-align:right;line-height:1.45}
        </style></head><body>
        ${header}
        <div class="meta">Offerta n. <strong>${escapeHtml(offer.id)}</strong> del ${escapeHtml(offer.data)} · Valida ${offer.validita_giorni} giorni</div>
        <p><strong>Cliente:</strong> ${escapeHtml(offer.client.azienda || '—')}<br>
        ${offer.client.contatto ? `Referente: ${escapeHtml(offer.client.contatto)}<br>` : ''}
        ${offer.client.email ? escapeHtml(offer.client.email) : ''}</p>
        <div class="block">${escapeHtml(offer.intro || '')}</div>
        ${blocksHtml}
        ${offer.prompt_extra ? `<div class="block"><em>${escapeHtml(offer.prompt_extra)}</em></div>` : ''}
        ${rows ? `<table><thead><tr><th>#</th><th>Descrizione</th><th>Qtà</th><th>Prezzo unit.</th><th>Totale</th></tr></thead><tbody>${rows}</tbody></table>` : ''}
        ${t.opzioni?.length > 1 ? `<div class="doc-options"><strong>Totali per configurazione robot</strong> (alternativa — scegliere una)<ul>${t.opzioni.map(o => `<li>${escapeHtml(o.nome)}: € ${fmt(o.totale)}</li>`).join('')}</ul></div>` : ''}
        <div class="totals">
          <div>Subtotale configurazione consigliata: € ${fmt(t.subtotal)}</div>
          ${t.iva_eur ? `<div>IVA ${t.iva_pct}%: € ${fmt(t.iva_eur)}</div>` : ''}
          <div class="grand">Totale: € ${fmt(t.totale)}</div>
          <div style="font-size:0.82rem;color:#737373;margin-top:4px">${escapeHtml(offer.note_iva)}</div>
        </div>
        <div class="block">${escapeHtml(offer.condizioni || '')}</div>
        <div class="block">${escapeHtml(offer.chiusura || '')}</div>
        </body></html>`;
    }

    exportPrint(offer) {
      this.downloadPdf(offer);
    }

    downloadPdf(offer) {
      const html = this.toPrintHtml(offer);
      const w = window.open('', '_blank');
      if (w) {
        w.document.write(html);
        w.document.close();
        w.focus();
        setTimeout(() => w.print(), 400);
        return;
      }
      const iframe = document.createElement('iframe');
      iframe.setAttribute('title', 'Preventivo PDF');
      iframe.style.cssText = 'position:fixed;right:0;bottom:0;width:0;height:0;border:0';
      document.body.appendChild(iframe);
      const doc = iframe.contentDocument || iframe.contentWindow.document;
      doc.open();
      doc.write(html);
      doc.close();
      iframe.contentWindow.focus();
      setTimeout(() => {
        iframe.contentWindow.print();
        setTimeout(() => iframe.remove(), 60000);
      }, 400);
    }

    saveDraft(offer) { sessionStorage.setItem(STORAGE_DRAFT, JSON.stringify(offer)); }

    loadDraft() {
      try {
        const o = JSON.parse(sessionStorage.getItem(STORAGE_DRAFT) || 'null');
        if (o && !Array.isArray(o.content_blocks)) o.content_blocks = [];
        return o;
      } catch { return null; }
    }
  }

  global.AbraOfferBuilder = OfferBuilder;
})(typeof window !== 'undefined' ? window : globalThis);
