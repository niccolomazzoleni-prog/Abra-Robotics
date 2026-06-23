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

  /** Path assoluti dal root del sito — funzionano da /offerte-ai/, /offerte-ai/samples/ e chat. */
  function assetUrl(rel) {
    if (!rel) return '';
    if (/^https?:\/\//i.test(rel)) return rel;
    const clean = String(rel).replace(/^\.\.\//, '').replace(/^\//, '');
    return '/' + clean;
  }

  class OfferBuilder {
    constructor(quoteEngine) {
      this.quote = quoteEngine;
      this.config = null;
      this.vociExtra = [];
      this.catalogIndex = [];
      this.recurringBlocks = [];
      this.productManifest = {};
    }

    setProductManifest(manifest) {
      this.productManifest = manifest || {};
    }

    _productCaption() {
      return '';
    }

    _cleanDisplayTitle(title) {
      return String(title || '')
        .replace(/\s*\(fonte[^)]*\)/gi, '')
        .replace(/\s*—\s*fonte[^\n]*/gi, '')
        .trim();
    }

    renderClientBlock(client) {
      const c = client || {};
      if (!c.azienda && !c.contatto) {
        return `<div class="doc-client"><strong>Cliente</strong><span class="muted">Da compilare</span></div>`;
      }
      return `<div class="doc-client">
          <strong>${escapeHtml(c.azienda || '')}</strong>
          ${c.contatto ? `<span>${escapeHtml(c.contatto)}</span>` : ''}
          ${c.piva ? `<span>P.IVA IT${escapeHtml(String(c.piva).replace(/^IT/i, ''))}</span>` : ''}
          ${c.indirizzo ? `<span>${escapeHtml(c.indirizzo)}</span>` : ''}
          ${c.email ? `<span>${escapeHtml(c.email)}</span>` : ''}
        </div>`;
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
        sorveglianza: 'Applicazione sorveglianza (As2 / A2)',
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
        image_url: m.immagine ? assetUrl(m.immagine) : '',
        caption: '',
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
      const logo = assetUrl(co.logo_url || 'images/logo.png');
      return `
        <div class="doc-header">
          <img class="doc-logo-img" src="${escapeHtml(logo)}" alt="${escapeHtml(co.nome || 'Abra Robotics')}" width="140" height="40">
          <div class="doc-fiscal">
            <strong>${escapeHtml(co.ragione_sociale || co.nome || '')}</strong><br>
            P.IVA ${escapeHtml(co.piva || '')}<br>
            ${escapeHtml(co.indirizzo || '')}<br>
            ${escapeHtml(co.email || '')}${co.telefono ? ' · ' + escapeHtml(co.telefono) : ''}${co.sito ? '<br><a href="' + escapeHtml(co.sito) + '" style="color:#7c4dd6">' + escapeHtml(co.sito.replace(/^https?:\/\//, '')) + '</a>' : ''}
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

    renderRobotHeroHtml(offer) {
      const robots = (offer.line_items || []).filter(l => l.opzione_robot && l.sku);
      if (robots.length < 2) return '';
      const items = robots.map(l => {
        const m = this.productManifest[l.sku] || {};
        const img = assetUrl(m.immagine || '');
        const short = String(l.nome || l.sku).replace(/^Unitree\s+/i, '').split('(')[0].trim();
        const rec = l.principale ? ' rec' : '';
        return `<figure class="${rec.trim()}"><img src="${escapeHtml(img)}" alt="${escapeHtml(l.nome || l.sku)}" loading="lazy"><figcaption>${escapeHtml(short)}</figcaption></figure>`;
      }).join('');
      return `<div class="doc-robot-hero" aria-label="Piattaforme robot quotate">${items}</div>`;
    }

    _partitionLines(offer) {
      const lines = offer.line_items || [];
      return {
        robots: lines.filter(l => l.opzione_robot),
        priced: lines.filter(l => !l.opzione_robot && !l.su_richiesta && Number(l.prezzo_unit) > 0),
        pending: lines.filter(l => !l.opzione_robot && (l.su_richiesta || !Number(l.prezzo_unit))),
      };
    }

    _splitContentBlocks(blocks) {
      const all = blocks || [];
      const isSecondary = b =>
        b.type === 'section' && /finanziament|agevolaz|sgravi|perché|perche|consegna|supporto/i.test(String(b.title || '') + String(b.body || '').slice(0, 80));
      const isIntroBlocco = b =>
        b.type === 'section' && /^Blocco [AB]/i.test(String(b.title || ''));
      return {
        highlights: all.filter(b => b.type === 'highlight'),
        specs: all.filter(b => b.type === 'section' && /specifiche|payload sensori|integrazione software|poc/i.test(String(b.title || ''))),
        introSections: all.filter(b => isIntroBlocco(b)),
        secondary: all.filter(b => isSecondary(b)),
        other: all.filter(b => !['highlight'].includes(b.type) && !isSecondary(b) && !isIntroBlocco(b)
          && !/specifiche|payload sensori|integrazione software|poc/i.test(String(b.title || ''))),
      };
    }

    _recommendedRobot(offer, t) {
      const robots = (offer.line_items || []).filter(l => l.opzione_robot);
      return robots.find(r => r.principale) || robots.find(r => r.robot_gruppo === 'sorveglianza') || robots[0];
    }

    renderConfigSummary(offer, t) {
      const rec = this._recommendedRobot(offer, t);
      if (!rec && !t.gruppi?.length) return '';
      const recName = rec ? String(rec.nome).replace(/^Unitree\s+/i, '') : '—';
      let html = `<section class="doc-config-summary">
        <h2 class="doc-config-summary-title">Riepilogo configurazione</h2>
        <div class="doc-config-rec">
          <span class="doc-config-rec-label">Piattaforma di riferimento</span>
          <strong class="doc-config-rec-name">${escapeHtml(recName)}</strong>
          <span class="doc-config-rec-total">€ ${fmt(t.subtotal)} <small>IVA escl.</small></span>
        </div>`;
      if (t.gruppi?.length) {
        html += t.gruppi.map(g => `
          <div class="doc-config-group">
            <h3 class="doc-config-group-label">${escapeHtml(g.label)} <span class="muted">— scegliere una</span></h3>
            <ul class="doc-config-options">${g.opzioni.map(o => {
              const isRec = rec && o.sku === rec.sku;
              return `<li class="${isRec ? 'is-rec' : ''}"><span>${escapeHtml(o.nome.split('(')[0].trim())}</span><strong>€ ${fmt(o.totale)}</strong></li>`;
            }).join('')}</ul>
          </div>`).join('');
      } else if (t.opzioni?.length > 1) {
        html += `<ul class="doc-config-options">${t.opzioni.map(o =>
          `<li><span>${escapeHtml(o.nome.split('(')[0].trim())}</span><strong>€ ${fmt(o.totale)}</strong></li>`
        ).join('')}</ul>`;
      }
      html += '</section>';
      return html;
    }

    renderCompactLineTable(title, lines, { compact = false } = {}) {
      if (!lines.length) return '';
      const rows = lines.map(l => `
        <tr>
          <td><strong>${escapeHtml(l.nome)}</strong>${l.sku ? `<span class="line-sku">${escapeHtml(l.sku)}</span>` : ''}${compact ? '' : (l.descrizione ? `<span class="line-desc">${escapeHtml(l.descrizione.split(' · ')[0])}</span>` : '')}</td>
          <td class="col-qty">${l.qty}</td>
          <td class="col-price">${this._priceCell(l)}</td>
          <td class="col-price">${this._totalCell(l)}</td>
        </tr>`).join('');
      return `<section class="doc-price-block">
        <h3 class="doc-price-block-title">${escapeHtml(title)}</h3>
        <table class="doc-lines doc-lines-compact"><thead><tr><th>Voce</th><th>Qtà</th><th>Unit.</th><th>Tot.</th></tr></thead><tbody>${rows}</tbody></table>
      </section>`;
    }

    renderRobotAltTable(robots, sharedTotal) {
      if (!robots.length) return '';
      const rows = robots.map(r => `
        <tr class="${r.principale ? 'is-rec' : ''}">
          <td><strong>${escapeHtml(r.nome)}</strong><span class="line-sku">${escapeHtml(r.sku || '')}</span></td>
          <td class="col-price">€ ${fmt(r.prezzo_unit)}</td>
          <td class="col-price"><strong>€ ${fmt(sharedTotal + (r.su_richiesta ? 0 : r.prezzo_totale))}</strong></td>
          <td class="col-note">${r.principale ? 'Consigliata' : 'Alternativa'}</td>
        </tr>`).join('');
      return `<section class="doc-price-block">
        <h3 class="doc-price-block-title">Piattaforme robot — alternative</h3>
        <table class="doc-lines doc-lines-compact"><thead><tr><th>Modello</th><th>Robot</th><th>Totale*</th><th></th></tr></thead><tbody>${rows}</tbody></table>
        <p class="doc-price-note">* Totale indicativo con voci comuni (PoC, spedizione, formazione). Selezionare <strong>una sola</strong> configurazione per blocco.</p>
      </section>`;
    }

    renderPendingSection(pending) {
      if (!pending.length) return '';
      const items = pending.map(l =>
        `<li><strong>${escapeHtml(l.nome)}</strong>${l.descrizione ? `<span>${escapeHtml(l.descrizione.split('.')[0])}</span>` : ''}</li>`
      ).join('');
      return `<section class="doc-pending">
        <h3 class="doc-pending-title">Da definire e quotare</h3>
        <p class="doc-pending-lead">Importi da confermare dopo call tecnica e scelta payload definitivo:</p>
        <ul class="doc-pending-list">${items}</ul>
      </section>`;
    }

    renderNextSteps(offer) {
      return `<section class="doc-next-steps">
        <h3 class="doc-next-steps-title">Prossimi passi</h3>
        <ol class="doc-next-steps-list">
          <li><strong>Conferma configurazione</strong> — selezione robot per ogni blocco alternativo (As2/A2 e/o Go2).</li>
          <li><strong>Call tecnica</strong> — definizione payload sensori, staffa e voci «su richiesta».</li>
          <li><strong>PoC e trasferte</strong> — durata definitiva ingegneria e stima trasferte team.</li>
          <li><strong>Ordine e finanziamenti</strong> — verifica agevolazioni; conferma d'ordine e tempi consegna.</li>
        </ol>
        ${offer.chiusura ? `<p class="doc-next-steps-note">${richText(String(offer.chiusura).split('\n\n')[0])}</p>` : ''}
      </section>`;
    }

    renderProductBlocks(blocks, { highlights, specs, introSections }) {
      let html = '';
      if (introSections.length) {
        html += `<div class="doc-intro-blocs">${introSections.map(b =>
          `<div class="doc-intro-bloc"><strong>${escapeHtml(b.title)}</strong><div>${richText(b.body)}</div></div>`
        ).join('')}</div>`;
      }
      if (highlights.length) {
        html += `<div class="doc-products">${highlights.map(b =>
          `<article class="doc-block doc-block-highlight doc-block-highlight-compact">
            ${b.image_url ? `<div class="doc-block-highlight-img"><img src="${escapeHtml(b.image_url)}" alt="${escapeHtml(b.title || '')}"></div>` : ''}
            <div class="doc-block-highlight-text">
              ${b.title ? `<h3 class="doc-block-title">${escapeHtml(this._cleanDisplayTitle(b.title))}</h3>` : ''}
              <div class="doc-block-body">${richText(b.body)}</div>
            </div>
          </article>`
        ).join('')}</div>`;
      }
      if (specs.length) {
        html += specs.map(b =>
          `<section class="doc-block doc-block-section doc-block-section-compact">
            ${b.title ? `<h3 class="doc-block-title">${escapeHtml(this._cleanDisplayTitle(b.title))}</h3>` : ''}
            <div class="doc-block-body">${richText(b.body)}</div>
          </section>`
        ).join('');
      }
      return html;
    }

    renderSecondaryBlocks(blocks) {
      if (!blocks.length) return '';
      return `<div class="doc-secondary">${blocks.map(b =>
        `<section class="doc-block doc-block-section doc-block-secondary">
          ${b.title ? `<h3 class="doc-block-title">${escapeHtml(b.title)}</h3>` : ''}
          <div class="doc-block-body">${richText(b.body)}</div>
        </section>`
      ).join('')}</div>`;
    }

    renderOfferDocument(offer) {
      const co = this.config?.azienda || {};
      const t = this.recalculate(offer);
      const parts = this._partitionLines(offer);
      const split = this._splitContentBlocks(offer.content_blocks);
      const hasContent = offer.line_items.length || offer.client.azienda || offer.content_blocks?.length;
      if (!hasContent) {
        return '<div class="offer-preview-empty">Aggiungi cliente, righe o sezioni narrative per l\'anteprima</div>';
      }

      return `
        <div class="abra-offer-doc abra-offer-doc--pdf">
        ${this.renderCompanyHeader(co)}
        <div class="doc-topbar">
          <div class="doc-meta">Offerta <strong>${escapeHtml(offer.id)}</strong> · ${escapeHtml(offer.data)} · Valida ${offer.validita_giorni} gg</div>
          ${this.renderClientBlock(offer.client)}
        </div>
        ${offer.intro ? `<div class="doc-intro doc-intro-compact">${richText(offer.intro)}</div>` : ''}
        ${this.renderConfigSummary(offer, t)}
        ${this.renderRobotHeroHtml(offer)}
        ${this.renderProductBlocks(offer.content_blocks, split)}
        ${this.renderRobotAltTable(parts.robots, t.sharedTotal)}
        ${this.renderCompactLineTable('Servizi e voci comuni quotate', parts.priced, { compact: true })}
        ${this.renderPendingSection(parts.pending)}
        <div class="doc-total doc-total-compact">
          Totale configurazione di riferimento: <strong>€ ${fmt(t.subtotal)}</strong>
          <span class="doc-iva-note">${escapeHtml(offer.note_iva)}</span>
        </div>
        ${this.renderNextSteps(offer)}
        ${offer.prompt_extra ? `<div class="doc-extra-compact"><em>${richText(offer.prompt_extra)}</em></div>` : ''}
        ${this.renderSecondaryBlocks(split.secondary)}
        ${offer.condizioni ? `<div class="doc-footer doc-footer-compact">${richText(offer.condizioni)}</div>` : ''}
        </div>`;
    }

    renderPreviewFragment(offer) {
      return this.renderOfferDocument(offer);
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
      const body = this.renderOfferDocument(offer);
      return `<!DOCTYPE html><html lang="it"><head><meta charset="UTF-8">
        <title>Offerta ${escapeHtml(offer.id)} — ${escapeHtml(offer.client.azienda || 'Cliente')}</title>
        <link href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700,900&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="../css/offerte-ai.css">
        <style>
          body{margin:0;padding:24px 28px;background:#fff;font-family:'Satoshi',system-ui,sans-serif}
          @page{margin:14mm 12mm}
          @media print{body{padding:0}.offer-sample-toolbar{display:none}}
        </style></head><body>${body}</body></html>`;
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
