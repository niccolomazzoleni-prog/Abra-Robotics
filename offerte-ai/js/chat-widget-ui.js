/**
 * UI del widget chat pubblico (launcher + pannello) — responsive, accessibile, senza dipendenze.
 * Stili: offerte-ai/css/chat-widget.css (tutto sotto .abra-cw / .abra-cw-launcher).
 */
(function (global) {
  'use strict';

  const doc = global.document;

  function el(tag, attrs, html) {
    const n = doc.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(k => {
      if (k === 'class') n.className = attrs[k];
      else if (attrs[k] !== false && attrs[k] != null) n.setAttribute(k, attrs[k] === true ? '' : attrs[k]);
    });
    if (html != null) n.innerHTML = html;
    return n;
  }

  function escapeHtml(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  const reducedMotion = () => !!(global.matchMedia && global.matchMedia('(prefers-reduced-motion: reduce)').matches);
  const isSheetLayout = () => !!(global.matchMedia && global.matchMedia('(max-width: 600px), (max-height: 520px)').matches);
  const finePointer = () => !!(global.matchMedia && global.matchMedia('(hover: hover) and (pointer: fine)').matches);
  const sleep = ms => new Promise(r => setTimeout(r, ms));

  const ICONS = {
    chat: '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
    close: '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true" focusable="false"><path d="M6 6l12 12M18 6L6 18"/></svg>',
    send: '<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true" focusable="false"><path d="M3.4 20.4l17.45-7.48c.81-.35.81-1.49 0-1.84L3.4 3.6c-.66-.29-1.39.2-1.39.91L2 9.12c0 .5.37.93.87.99L15 12 2.87 13.89c-.5.07-.87.5-.87 1l.01 4.61c0 .71.73 1.2 1.39.91z"/></svg>',
    wa: '<svg viewBox="0 0 24 24" width="15" height="15" fill="currentColor" aria-hidden="true" focusable="false"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.07-.3-.15-1.26-.46-2.39-1.47-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.67-1.61-.92-2.21-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48 0 1.46 1.07 2.88 1.21 3.07.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.7.63.71.23 1.36.2 1.87.12.57-.09 1.76-.72 2.01-1.41.25-.69.25-1.29.17-1.41-.07-.12-.27-.2-.57-.35M12.05 21.79h-.01a9.87 9.87 0 0 1-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 0 1-1.51-5.26c0-5.45 4.44-9.88 9.89-9.88 2.64 0 5.12 1.03 6.99 2.9a9.83 9.83 0 0 1 2.89 6.99c0 5.45-4.44 9.88-9.88 9.88m8.41-18.3A11.82 11.82 0 0 0 12.05 0C5.5 0 .16 5.34.16 11.89c0 2.1.55 4.14 1.59 5.95L.06 24l6.3-1.65a11.88 11.88 0 0 0 5.68 1.45h.01c6.55 0 11.89-5.34 11.89-11.89 0-3.18-1.24-6.17-3.48-8.42"/></svg>',
    calendar: '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true" focusable="false"><rect x="3" y="4.5" width="18" height="17" rx="2"/><path d="M16 2.5v4M8 2.5v4M3 10h18"/></svg>',
    mail: '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true" focusable="false"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 6.5l8.5 6 8.5-6"/></svg>',
  };

  /* ---------- markdown-lite sicuro (grassetto, corsivo, link, elenchi, tabelle) ---------- */

  function safeHref(url, linkBase) {
    const u = String(url || '').trim();
    if (/^(https?:|mailto:|tel:)/i.test(u)) return u;
    if (/^[a-z][a-z0-9+.-]*:/i.test(u)) return null;        // javascript:, data:, …
    if (/^(#|\/)/.test(u)) return u;
    try { return new URL(u, linkBase || global.location.href).href; } catch (_) { return null; }
  }

  function inline(text, linkBase) {
    const links = [];
    let s = String(text).replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (m, label, url) => {
      const href = safeHref(url, linkBase);
      if (!href) return label;
      const ext = /^https?:/i.test(href) && !href.startsWith(global.location.origin);
      const mail = /^(mailto|tel):/i.test(href);
      links.push('<a href="' + escapeHtml(href) + '"' + (ext ? ' target="_blank" rel="noopener noreferrer"' : '') +
        (mail ? '' : '') + '>' + escapeHtml(label) + (ext ? '<span class="abra-cw-sr"> (si apre in una nuova scheda)</span>' : '') + '</a>');
      return '\u0000' + (links.length - 1) + '\u0000';
    });
    s = escapeHtml(s)
      .replace(/(https?:\/\/[^\s<]+[^\s<.,;:!?)])/g, url => {
        links.push('<a href="' + url + '" target="_blank" rel="noopener noreferrer">' + url + '</a>');
        return '\u0000' + (links.length - 1) + '\u0000';
      })
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/(^|[\s(])_(.+?)_(?=$|[\s).,;:!?])/g, '$1<em>$2</em>');
    return s.replace(/\u0000(\d+)\u0000/g, (m, i) => links[Number(i)] || '');
  }

  function formatMessage(text, linkBase) {
    const lines = String(text || '').replace(/\r/g, '').split('\n');
    const out = [];
    let list = null;
    let table = null;
    const flushList = () => { if (list) { out.push('<' + list.tag + '>' + list.items.join('') + '</' + list.tag + '>'); list = null; } };
    const flushTable = () => {
      if (!table) return;
      const rows = table.filter(r => !/^\|?\s*:?-{2,}/.test(r.replace(/\s/g, '')));
      const cells = r => r.replace(/^\||\|$/g, '').split('|').map(c => inline(c.trim(), linkBase));
      const [head, ...body] = rows;
      out.push('<div class="abra-cw-table"><table><thead><tr>' + cells(head).map(c => '<th>' + c + '</th>').join('') +
        '</tr></thead><tbody>' + body.map(r => '<tr>' + cells(r).map(c => '<td>' + c + '</td>').join('') + '</tr>').join('') +
        '</tbody></table></div>');
      table = null;
    };
    for (const raw of lines) {
      const line = raw.trim();
      if (/^\|.*\|$/.test(line)) { flushList(); (table = table || []).push(line); continue; }
      flushTable();
      let m;
      if ((m = line.match(/^(?:[•\-*])\s+(.*)$/))) {
        if (!list || list.tag !== 'ul') { flushList(); list = { tag: 'ul', items: [] }; }
        list.items.push('<li>' + inline(m[1], linkBase) + '</li>');
        continue;
      }
      if ((m = line.match(/^(\d+)[.)]\s+(.*)$/))) {
        if (!list || list.tag !== 'ol') { flushList(); list = { tag: 'ol', items: [] }; }
        list.items.push('<li>' + inline(m[2], linkBase) + '</li>');
        continue;
      }
      flushList();
      if (!line) continue;
      out.push('<p>' + inline(line, linkBase) + '</p>');
    }
    flushList();
    flushTable();
    return out.join('');
  }

  /* ---------- widget ---------- */

  class ChatWidgetUI {
    constructor(opts = {}) {
      this.opts = Object.assign({
        title: 'Assistente Abra',
        subtitle: 'Prezzi, consegne e contatti · risponde subito',
        logoUrl: '',
        linkBase: global.location.href,
        chips: [],
        contact: {},
        onSend: async () => ({ reply: '' }),
        onFirstIntent: () => {},
        onOpen: () => {},
      }, opts);
      this.isOpen = false;
      this.busy = false;
      this._intentFired = false;
      this._lastFocus = null;
      this._build();
      this._bind();
      this._watchObstacles();
    }

    /* DOM */
    _build() {
      const o = this.opts;
      const c = o.contact || {};
      const logo = o.logoUrl ? '<img src="' + escapeHtml(o.logoUrl) + '" alt="" width="40" height="40" decoding="async">' : '';

      this.launcher = el('button', {
        class: 'abra-cw-launcher',
        type: 'button',
        'aria-label': 'Apri l\'assistente Abra: prezzi e informazioni',
        'aria-expanded': 'false',
        'aria-controls': 'abra-cw-panel',
        'aria-haspopup': 'dialog',
      }, '<span class="abra-cw-launcher-ring" aria-hidden="true"></span>' +
        '<span class="abra-cw-launcher-face" aria-hidden="true">' + (logo || ICONS.chat) + '</span>' +
        '<span class="abra-cw-launcher-x" aria-hidden="true">' + ICONS.close + '</span>');
      // compatibilità con selettori esistenti
      this.launcher.classList.add('abra-chat-launcher');

      this.panel = el('div', {
        class: 'abra-cw abra-chat-panel',
        id: 'abra-cw-panel',
        role: 'dialog',
        'aria-modal': 'true',
        'aria-labelledby': 'abra-cw-title',
        'aria-describedby': 'abra-cw-sub',
        hidden: true,
      });
      this.panel.innerHTML =
        '<div class="abra-cw-header">' +
          '<div class="abra-cw-avatar" aria-hidden="true">' + (logo || ICONS.chat) + '</div>' +
          '<div class="abra-cw-heading">' +
            '<h2 class="abra-cw-title" id="abra-cw-title" tabindex="-1">' + escapeHtml(o.title) + '</h2>' +
            '<p class="abra-cw-sub" id="abra-cw-sub"><span class="abra-cw-dot" aria-hidden="true"></span>' + escapeHtml(o.subtitle) + '</p>' +
          '</div>' +
          '<button type="button" class="abra-cw-icon-btn abra-cw-close" aria-label="Chiudi l\'assistente">' + ICONS.close + '</button>' +
        '</div>' +
        '<div class="abra-cw-log" role="log" aria-live="polite" aria-relevant="additions" aria-label="Conversazione" tabindex="0"></div>' +
        '<div class="abra-cw-bottom">' +
          (o.chips.length ? '<div class="abra-cw-chips" role="group" aria-label="Domande rapide">' +
            o.chips.map(ch => '<button type="button" class="abra-cw-chip" data-q="' + escapeHtml(ch.q || ch.label) + '">' + escapeHtml(ch.label) + '</button>').join('') +
          '</div>' : '') +
          '<form class="abra-cw-form" novalidate>' +
            '<label class="abra-cw-sr" for="abra-cw-input">Scrivi la tua domanda</label>' +
            '<textarea id="abra-cw-input" class="abra-cw-input" rows="1" placeholder="Es. quanto costa il G1?" autocomplete="off" enterkeyhint="send" maxlength="1200"></textarea>' +
            '<button type="submit" class="abra-cw-send" aria-label="Invia">' + ICONS.send + '</button>' +
          '</form>' +
          '<div class="abra-cw-links">' +
            (c.waUrl ? '<a class="abra-cw-link abra-cw-link-wa" href="' + escapeHtml(c.waUrl) + '" target="_blank" rel="noopener noreferrer">' + ICONS.wa + '<span>WhatsApp</span></a>' : '') +
            (c.bookingUrl ? '<a class="abra-cw-link" href="' + escapeHtml(c.bookingUrl) + '" target="_blank" rel="noopener noreferrer">' + ICONS.calendar + '<span>Prenota una call</span></a>' : '') +
            '<button type="button" class="abra-cw-link abra-cw-contact-toggle" aria-expanded="false" aria-controls="abra-cw-contact">' + ICONS.mail + '<span>Richiamami</span></button>' +
          '</div>' +
          '<div class="abra-cw-contact" id="abra-cw-contact" hidden>' +
            '<form class="abra-cw-contact-form" novalidate>' +
              '<p class="abra-cw-contact-title">Ti richiamiamo noi</p>' +
              '<input type="text" name="_gotcha" class="abra-cw-hp" tabindex="-1" autocomplete="off" aria-hidden="true">' +
              '<div class="abra-cw-grid">' +
                '<label class="abra-cw-field"><span>Nome *</span><input name="nome" required autocomplete="name"></label>' +
                '<label class="abra-cw-field"><span>Telefono *</span><input name="telefono" type="tel" required autocomplete="tel" inputmode="tel"></label>' +
              '</div>' +
              '<label class="abra-cw-field"><span>Email *</span><input name="email" type="email" required autocomplete="email" inputmode="email"></label>' +
              '<label class="abra-cw-field"><span>Messaggio</span><textarea name="messaggio" rows="2" placeholder="Di cosa hai bisogno?"></textarea></label>' +
              '<p class="abra-cw-contact-err" role="alert" hidden></p>' +
              '<div class="abra-cw-contact-actions">' +
                '<button type="button" class="abra-cw-btn-ghost abra-cw-contact-cancel">Annulla</button>' +
                '<button type="submit" class="abra-cw-btn">Invia richiesta</button>' +
              '</div>' +
              (c.privacyUrl ? '<p class="abra-cw-contact-note">Usiamo i tuoi dati solo per ricontattarti. <a href="' + escapeHtml(c.privacyUrl) + '">Privacy</a></p>' : '') +
            '</form>' +
          '</div>' +
        '</div>';

      this.log = this.panel.querySelector('.abra-cw-log');
      this.form = this.panel.querySelector('.abra-cw-form');
      this.input = this.panel.querySelector('.abra-cw-input');
      this.sendBtn = this.panel.querySelector('.abra-cw-send');
      this.closeBtn = this.panel.querySelector('.abra-cw-close');
      this.titleEl = this.panel.querySelector('.abra-cw-title');
      this.contactBox = this.panel.querySelector('.abra-cw-contact');
      this.contactToggle = this.panel.querySelector('.abra-cw-contact-toggle');
      this.contactForm = this.panel.querySelector('.abra-cw-contact-form');

      doc.body.appendChild(this.launcher);
      doc.body.appendChild(this.panel);
    }

    _bind() {
      const intent = () => {
        if (this._intentFired) return;
        this._intentFired = true;
        try { this.opts.onFirstIntent(); } catch (_) {}
      };
      ['pointerenter', 'focus', 'touchstart'].forEach(ev => this.launcher.addEventListener(ev, intent, { passive: true, once: true }));
      this.launcher.addEventListener('click', () => { intent(); this.toggle(); });
      this.closeBtn.addEventListener('click', () => this.close());

      this.form.addEventListener('submit', e => { e.preventDefault(); this._submit(); });
      this.input.addEventListener('keydown', e => {
        if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) { e.preventDefault(); this._submit(); }
      });
      this.input.addEventListener('input', () => this._autosize());

      this.panel.querySelector('.abra-cw-chips')?.addEventListener('click', e => {
        const b = e.target.closest('.abra-cw-chip');
        if (b) this.send(b.dataset.q);
      });

      this.log.addEventListener('click', e => {
        // link a una sezione della pagina corrente (es. umanoidi.html#fam-g1): chiudi la chat per mostrarla
        const link = e.target.closest('a[href]');
        if (link && link.origin === global.location.origin && link.pathname === global.location.pathname && link.hash) {
          this.close();
          return;
        }
        const b = e.target.closest('[data-cw-action]');
        if (!b) return;
        const act = b.getAttribute('data-cw-action');
        if (act === 'contact') this.openContact();
        else if (act === 'ask') this.send(b.getAttribute('data-q'));
      });

      this.contactToggle.addEventListener('click', () => (this.contactBox.hidden ? this.openContact() : this.closeContact()));
      this.panel.querySelector('.abra-cw-contact-cancel').addEventListener('click', () => this.closeContact(true));
      this.contactForm.addEventListener('submit', e => { e.preventDefault(); this._submitContact(); });

      this.panel.addEventListener('keydown', e => this._onKeydown(e));

      // tastiera virtuale mobile: il pannello segue la visual viewport
      this._onViewport = () => this._syncViewport();
      if (global.visualViewport) {
        global.visualViewport.addEventListener('resize', this._onViewport);
        global.visualViewport.addEventListener('scroll', this._onViewport);
      }
      global.addEventListener('resize', () => { this._syncViewport(); this._updateLift(); }, { passive: true });
    }

    /* barra WhatsApp / banner cookie: il launcher sale sopra */
    _watchObstacles() {
      this._updateLift = () => {
        let lift = 0;
        const vh = global.innerHeight;
        const obstacles = [doc.getElementById('wa-bar'), doc.querySelector('.cookie-banner')];
        for (const o of obstacles) {
          if (!o || o.style.display === 'none' || !o.offsetParent && getComputedStyle(o).position !== 'fixed') continue;
          const r = o.getBoundingClientRect();
          if (!r.height || r.top >= vh || r.bottom < vh - 4) continue;   // non ancorato in basso
          // il banner cookie è centrato: conta solo se si sovrappone alla colonna del launcher
          if (r.right < global.innerWidth - 96) continue;
          lift = Math.max(lift, Math.ceil(vh - r.top));
        }
        const v = lift ? lift + 'px' : '0px';
        doc.documentElement.style.setProperty('--abra-cw-lift', v);
      };
      this._updateLift();
      let raf = 0;
      const schedule = () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(this._updateLift); };
      if (global.MutationObserver) {
        const mo = new MutationObserver(schedule);
        mo.observe(doc.body, { childList: true, attributes: true, attributeFilter: ['class', 'style'] });
        const wa = doc.getElementById('wa-bar');
        if (wa) mo.observe(wa, { attributes: true, attributeFilter: ['style', 'class'] });
        this._mo = mo;
      }
      setTimeout(this._updateLift, 800);
      setTimeout(this._updateLift, 2500);
    }

    _syncViewport() {
      const vv = global.visualViewport;
      if (!this.isOpen || !vv || !isSheetLayout()) {
        this.panel.style.removeProperty('--abra-cw-vvh');
        this.panel.style.removeProperty('--abra-cw-vvtop');
        return;
      }
      this.panel.style.setProperty('--abra-cw-vvh', Math.round(vv.height) + 'px');
      this.panel.style.setProperty('--abra-cw-vvtop', Math.round(vv.offsetTop) + 'px');
      if (doc.activeElement === this.input) this.scrollBottom();
    }

    _autosize() {
      this.input.style.height = 'auto';
      this.input.style.height = Math.min(this.input.scrollHeight, 132) + 'px';
    }

    _focusables() {
      return [...this.panel.querySelectorAll('a[href], button:not([disabled]), textarea:not([disabled]), input:not([disabled]):not([tabindex="-1"]), [tabindex]:not([tabindex="-1"])')]
        .filter(n => n.offsetParent !== null || n === doc.activeElement);
    }

    _onKeydown(e) {
      if (e.key === 'Escape') {
        e.stopPropagation();
        if (!this.contactBox.hidden && this.contactBox.contains(doc.activeElement)) this.closeContact(true);
        else this.close();
        return;
      }
      if (e.key !== 'Tab') return;
      const f = this._focusables();
      if (!f.length) return;
      const idx = f.indexOf(doc.activeElement);   // -1: titolo del dialogo o elemento fuori lista
      if (e.shiftKey && idx <= 0) { e.preventDefault(); f[f.length - 1].focus(); }
      else if (!e.shiftKey && (idx === -1 || idx === f.length - 1)) { e.preventDefault(); f[0].focus(); }
    }

    /* apertura / chiusura */
    toggle() { this.isOpen ? this.close() : this.open(); }

    open() {
      if (this.isOpen) return;
      this.isOpen = true;
      this._lastFocus = doc.activeElement;
      this.panel.hidden = false;
      // forza reflow per l'animazione d'ingresso
      void this.panel.offsetWidth;
      this.panel.classList.add('is-open', 'open');
      this.launcher.classList.add('is-open');
      this.launcher.setAttribute('aria-expanded', 'true');
      this.launcher.setAttribute('aria-label', 'Chiudi l\'assistente Abra');
      doc.documentElement.classList.add('abra-cw-open');
      this._syncViewport();
      this.scrollBottom();
      // su touch non apriamo subito la tastiera: il focus va al titolo del dialogo
      if (finePointer()) this.input.focus({ preventScroll: true });
      else this.titleEl.focus({ preventScroll: true });
      try { this.opts.onOpen(); } catch (_) {}
    }

    close() {
      if (!this.isOpen) return;
      this.isOpen = false;
      this.panel.classList.remove('is-open', 'open');
      this.launcher.classList.remove('is-open');
      this.launcher.setAttribute('aria-expanded', 'false');
      this.launcher.setAttribute('aria-label', 'Apri l\'assistente Abra: prezzi e informazioni');
      doc.documentElement.classList.remove('abra-cw-open');
      const hide = () => { if (!this.isOpen) this.panel.hidden = true; };
      if (reducedMotion()) hide(); else setTimeout(hide, 180);
      this._syncViewport();
      const prev = this._lastFocus;
      const usable = prev && prev !== doc.body && doc.contains(prev) && !this.panel.contains(prev) && prev.focus;
      const back = usable ? prev : this.launcher;
      // il launcher torna visibile solo dopo la rimozione della classe: focus al frame successivo
      requestAnimationFrame(() => back.focus({ preventScroll: true }));
    }

    openContact() {
      if (!this.isOpen) this.open();
      this.contactBox.hidden = false;
      this.contactToggle.setAttribute('aria-expanded', 'true');
      this.panel.classList.add('has-contact');
      const first = this.contactForm.querySelector('[name="nome"]');
      setTimeout(() => first && first.focus(), 30);
    }

    closeContact(refocus) {
      this.contactBox.hidden = true;
      this.contactToggle.setAttribute('aria-expanded', 'false');
      this.panel.classList.remove('has-contact');
      if (refocus) this.contactToggle.focus();
    }

    /* messaggi */
    scrollBottom() {
      const l = this.log;
      l.scrollTop = l.scrollHeight;
    }

    _row(role, html) {
      const row = el('div', { class: 'abra-cw-msg abra-cw-msg-' + role });
      if (role === 'bot') {
        row.appendChild(el('span', { class: 'abra-cw-sr' }, 'Assistente: '));
      } else {
        row.appendChild(el('span', { class: 'abra-cw-sr' }, 'Tu: '));
      }
      const bubble = el('div', { class: 'abra-cw-bubble' }, html);
      row.appendChild(bubble);
      this.log.appendChild(row);
      return row;
    }

    addUser(text) {
      const row = this._row('user', escapeHtml(text).replace(/\n/g, '<br>'));
      this.scrollBottom();
      return row;
    }

    addBot(text, extra = {}) {
      const row = this._row('bot', formatMessage(text, this.opts.linkBase));
      const bubble = row.querySelector('.abra-cw-bubble');
      if (extra.actions && extra.actions.length) {
        const bar = el('div', { class: 'abra-cw-actions' });
        extra.actions.forEach(a => {
          if (a.type === 'contact') {
            bar.appendChild(el('button', { type: 'button', class: 'abra-cw-btn abra-cw-btn-sm', 'data-cw-action': 'contact' }, escapeHtml(a.label || 'Apri il modulo contatto')));
          } else if (a.type === 'ask') {
            bar.appendChild(el('button', { type: 'button', class: 'abra-cw-chip', 'data-cw-action': 'ask', 'data-q': a.q }, escapeHtml(a.label)));
          }
        });
        bubble.appendChild(bar);
      }
      if (extra.card) bubble.appendChild(extra.card);
      // porta in vista l'inizio della risposta (le risposte lunghe si leggono dall'alto)
      if (row.offsetHeight + 16 < this.log.clientHeight) {
        this.scrollBottom();
      } else {
        const top = row.getBoundingClientRect().top - this.log.getBoundingClientRect().top + this.log.scrollTop - 10;
        this.log.scrollTop = Math.max(0, top);
      }
      return row;
    }

    showTyping() {
      this.hideTyping();
      this._typing = el('div', { class: 'abra-cw-msg abra-cw-msg-bot abra-cw-typing', 'aria-hidden': 'true' },
        '<div class="abra-cw-bubble"><span></span><span></span><span></span></div>');
      this.log.appendChild(this._typing);
      this.log.setAttribute('aria-busy', 'true');
      this.scrollBottom();
    }

    hideTyping() {
      if (this._typing) this._typing.remove();
      this._typing = null;
      this.log.removeAttribute('aria-busy');
    }

    _submit() {
      const q = this.input.value.trim();
      if (!q || this.busy) return;
      this.input.value = '';
      this._autosize();
      this.send(q);
    }

    async send(q) {
      q = String(q || '').trim();
      if (!q || this.busy) return;
      if (!this.isOpen) this.open();
      this.busy = true;
      this.sendBtn.disabled = true;
      this.addUser(q);
      this.showTyping();
      const t0 = Date.now();
      let result;
      try {
        result = await this.opts.onSend(q);
      } catch (err) {
        result = { reply: 'Scusa, qualcosa non ha funzionato. Riprova oppure scrivici su WhatsApp.', error: err };
      }
      const wait = reducedMotion() ? 0 : Math.max(0, 450 - (Date.now() - t0));
      if (wait) await sleep(wait);
      this.hideTyping();
      if (typeof result === 'string') result = { reply: result };
      if (result && result.reply) this.addBot(result.reply, result);
      this.busy = false;
      this.sendBtn.disabled = false;
      if (finePointer()) this.input.focus({ preventScroll: true });
    }

    /* modulo contatto */
    async _submitContact() {
      const f = this.contactForm;
      const err = f.querySelector('.abra-cw-contact-err');
      const val = n => (f.querySelector('[name="' + n + '"]')?.value || '').trim();
      err.hidden = true;
      if (val('_gotcha')) return;
      const nome = val('nome');
      const email = val('email');
      const telefono = val('telefono');
      const messaggioRaw = val('messaggio');
      const fail = (msg, name) => {
        err.textContent = msg;
        err.hidden = false;
        const input = f.querySelector('[name="' + name + '"]');
        if (input) { input.setAttribute('aria-invalid', 'true'); input.focus(); }
      };
      f.querySelectorAll('[aria-invalid]').forEach(n => n.removeAttribute('aria-invalid'));
      if (!nome) return fail('Inserisci il tuo nome.', 'nome');
      if (telefono.replace(/\D/g, '').length < 6) return fail('Inserisci un numero di telefono valido.', 'telefono');
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return fail('Inserisci un indirizzo email valido.', 'email');

      const btn = f.querySelector('button[type="submit"]');
      const orig = btn.textContent;
      btn.disabled = true;
      btn.textContent = 'Invio…';
      const payload = {
        nome, email, telefono,
        messaggio: messaggioRaw.length >= 5 ? messaggioRaw : 'Richiesta contatto via chat widget Abra',
        origine: 'Chat Abra',
        pagina: doc.title,
        url: global.location.href,
        timestamp: new Date().toISOString(),
        form_load_time: (typeof global._formLoadTime === 'number' ? global._formLoadTime : Date.now() - 5000),
      };
      try {
        await (this.opts.contact.submit ? this.opts.contact.submit(payload) : Promise.reject(new Error('no endpoint')));
        if (global.fbq) global.fbq('track', 'Lead');
        f.reset();
        this.closeContact();
        this.addBot('**Grazie, ' + nome.split(' ')[0] + '!** Abbiamo ricevuto la tua richiesta: un consulente Abra ti ricontatta entro **2 ore lavorative**.');
        this.input.focus({ preventScroll: true });
      } catch (_) {
        fail('Invio non riuscito. Scrivici a info@abrarobotics.com o su WhatsApp.', 'nome');
      } finally {
        btn.disabled = false;
        btn.textContent = orig;
      }
    }
  }

  ChatWidgetUI.formatMessage = formatMessage;
  global.AbraChatWidgetUI = ChatWidgetUI;
})(typeof window !== 'undefined' ? window : globalThis);
