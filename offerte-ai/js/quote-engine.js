/**
 * Motore offerte deterministico — i prezzi NON passano dall'LLM.
 */
(function (global) {
  'use strict';

  const fmt = n => Number(n).toLocaleString('it-IT', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

  class QuoteEngine {
    constructor() {
      this.prices = {};
      this.rules = { bundles: [], margins: {} };
      this.ready = false;
    }

    async load(pricesUrl, rulesUrl) {
      const aliasUrl = String(rulesUrl || '').replace(/offerte-regole\.json$/i, 'product-aliases.json');
      const [pRes, rRes, aRes] = await Promise.all([
        fetch(pricesUrl),
        fetch(rulesUrl),
        fetch(aliasUrl).catch(() => ({ ok: false })),
      ]);
      if (pRes.ok) this.prices = await pRes.json();
      if (rRes.ok) this.rules = await rRes.json();
      if (aRes?.ok) {
        const aliasData = await aRes.json();
        this.rules.aliases = aliasData.aliases || {};
        this.rules.compare_sets = aliasData.compare_sets || {};
      }
      this.ready = true;
    }

    getPrice(sku) {
      const item = this.prices[sku];
      if (!item) return null;
      return { sku, nome: item.nome, prezzo_eur: item.prezzo_eur, note: item.note || '' };
    }

    findSkusInText(text) {
      const upper = text.toUpperCase();
      return Object.keys(this.prices).filter(sku => upper.includes(sku));
    }

    calculateLineItems(skus, marginKey = 'end_user') {
      const margin = this.rules.margins?.[marginKey] || 0;
      const lines = [];
      let subtotal = 0;

      for (const sku of skus) {
        const p = this.getPrice(sku);
        if (!p) continue;
        const adj = p.prezzo_eur * (1 + margin / 100);
        lines.push({ ...p, prezzo_finale: adj });
        subtotal += adj;
      }
      return { lines, subtotal, margin_pct: margin };
    }

    calculateBundle(bundleId, selectedOptionSkus = [], marginKey = 'end_user') {
      const bundle = (this.rules.bundles || []).find(b => b.id === bundleId);
      if (!bundle) return { error: 'Bundle non trovato' };

      let baseSku = bundle.base_sku;
      const skus = [baseSku];

      for (const opt of bundle.options || []) {
        const sel = selectedOptionSkus.includes(opt.sku);
        if (opt.required || sel) {
          if (opt.replaces_base) {
            skus[0] = opt.sku;
          } else {
            skus.push(opt.sku);
          }
        }
      }

      const quote = this.calculateLineItems([...new Set(skus)], marginKey);
      let discount = 0;
      for (const rule of bundle.discount_rules || []) {
        if (quote.lines.length >= (rule.min_items || 2)) {
          if (rule.type === 'percent') discount = Math.max(discount, quote.subtotal * (rule.value / 100));
        }
      }

      return {
        bundle_id: bundleId,
        bundle_name: bundle.name,
        ...quote,
        discount_eur: discount,
        total_eur: quote.subtotal - discount,
        note_iva: this.rules.note_iva || 'IVA esclusa',
      };
    }

    formatQuote(quote) {
      if (quote.error) return quote.error;
      const lines = quote.lines.map(l =>
        `• ${l.nome} (${l.sku}): € ${fmt(l.prezzo_finale)}`
      ).join('\n');
      let out = `**${quote.bundle_name || 'Preventivo'}**\n${lines}\n`;
      if (quote.discount_eur) out += `Sconto bundle: -€ ${fmt(quote.discount_eur)}\n`;
      out += `**Totale: € ${fmt(quote.total_eur || quote.subtotal)}** (${quote.note_iva})`;
      return out;
    }

    tryAutoQuote(userText) {
      const skus = this.findSkusInText(userText);
      if (skus.length) {
        return this.calculateLineItems(skus);
      }
      const lower = userText.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');

      const aliasHit = this._matchAlias(lower);
      if (aliasHit) {
        if (aliasHit.compare) return this._quoteCompareSet(aliasHit.compare);
        return this.calculateLineItems([aliasHit.sku]);
      }

      if (/as2|as 2|a2s/.test(lower)) {
        if (/confront|entramb|quot.*entramb|air.*pro|pro.*edu/.test(lower)) {
          return this._quoteCompareSet('as2-gamma');
        }
        if (/\bair\b/.test(lower)) return this.calculateLineItems(['AS2-AIR']);
        if (/\bedu\b/.test(lower)) return this.calculateLineItems(['AS2-EDU']);
        return this.calculateLineItems(['AS2-PRO']);
      }

      if (/go2.*edu|go2 edu/.test(lower)) {
        if (/confront|entramb|plus|smart|orin nx|orin nano|base/.test(lower)) {
          return this._quoteCompareSet('go2-edu-duo');
        }
        return this.calculateBundle('go2-edu-starter');
      }

      for (const b of this.rules.bundles || []) {
        if (lower.includes(b.id.replace(/-/g, ' ')) || lower.includes(b.name.toLowerCase().slice(0, 12))) {
          return this.calculateBundle(b.id);
        }
      }
      if (/g1.*edu|g1 edu|g1-u1/.test(lower)) return this.calculateBundle('g1-edu-lab');
      return null;
    }

    _matchAlias(lower) {
      const aliases = this.rules.aliases || {};
      const keys = Object.keys(aliases).sort((a, b) => b.length - a.length);
      for (const key of keys) {
        if (lower.includes(key)) return { sku: aliases[key] };
      }
      return null;
    }

    _quoteCompareSet(setId) {
      const sets = this.rules.compare_sets || {};
      const skus = sets[setId];
      if (!skus?.length) return null;
      const quote = this.calculateLineItems(skus);
      quote.bundle_name = quote.lines.length > 1 ? `Confronto configurazioni` : quote.bundle_name;
      return quote;
    }
  }

  global.AbraQuoteEngine = QuoteEngine;
})(typeof window !== 'undefined' ? window : globalThis);
