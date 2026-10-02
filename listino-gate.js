// Listino End-User Unitree: mostra i primi prodotti, il resto dopo una richiesta
// tramite modulo (stesso invio dei form contatti: Google Sheet + mail a gio@/nico@).
// Usato da listino-unitree.html (generato da scripts/genera_catalogo_completo.py).
(function () {
  'use strict';
  const KEY = 'abra-listino-ok';
  const FREE = 8;

  function unlocked() {
    try { return localStorage.getItem(KEY) === '1'; } catch (e) { return false; }
  }
  function rerender() {
    const s = document.getElementById('search');
    if (s) s.dispatchEvent(new Event('input'));
  }

  const CSS = '.listino-gate{margin:24px 0 8px;padding:28px;border:1px solid var(--gray-200,#e5e5e5);border-radius:var(--radius,12px);background:var(--gray-50,#fafafa);display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.3fr);gap:28px;align-items:start}.listino-gate[hidden]{display:none}' +
    '.listino-gate h2{font-size:clamp(1.4rem,3vw,1.9rem);margin:4px 0 8px}' +
    '.listino-gate-count{font-weight:700}' +
    '.listino-gate-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}' +
    '.listino-gate-form label{display:grid;gap:4px;font-size:.9rem;font-weight:500}' +
    '.listino-gate-form input[type=text],.listino-gate-form input[type=email],.listino-gate-form input[type=tel]{font:inherit;padding:10px 12px;border:1px solid var(--gray-200,#e5e5e5);border-radius:8px;background:#fff;width:100%}' +
    '.listino-gate-form .listino-gate-check{display:flex;gap:8px;align-items:flex-start;font-weight:400;font-size:.85rem;margin:14px 0}' +
    '.listino-gate-check input{margin-top:3px;flex-shrink:0}' +
    '.listino-gate-feedback{margin:10px 0 0;font-size:.9rem;color:#b42318}' +
    '@media (max-width:760px){.listino-gate{grid-template-columns:1fr;padding:20px}.listino-gate-grid{grid-template-columns:1fr}.listino-gate .btn{width:100%;justify-content:center}}';

  function buildGate() {
    if (!document.getElementById('listino-gate-css')) {
      const st = document.createElement('style');
      st.id = 'listino-gate-css';
      st.textContent = CSS;
      document.head.appendChild(st);
    }
    const box = document.createElement('section');
    box.className = 'listino-gate';
    box.id = 'listino-completo';
    box.innerHTML =
      '<div class="listino-gate-text">' +
        '<p class="label">Listino completo</p>' +
        '<h2>Vedi tutti i prezzi Unitree</h2>' +
        '<p class="listino-gate-count"></p>' +
        '<p>Compila il modulo: il listino completo si sblocca subito e ti ricontattiamo per eventuali configurazioni o preventivi.</p>' +
      '</div>' +
      '<form class="listino-gate-form" novalidate>' +
        '<div class="listino-gate-grid">' +
          '<label>Nome e cognome<input name="nome" type="text" autocomplete="name" required></label>' +
          '<label>Azienda o ente<input name="azienda" type="text" autocomplete="organization" required></label>' +
          '<label>Email<input name="email" type="email" autocomplete="email" required></label>' +
          '<label>Telefono<input name="telefono" type="tel" autocomplete="tel" required></label>' +
        '</div>' +
        '<input type="hidden" name="messaggio" value="Richiesta listino completo prezzi End-User Unitree">' +
        '<label class="listino-gate-check"><input type="checkbox" name="privacy" value="si" required> Ho letto l\'<a href="privacy-policy.html" target="_blank" rel="noopener">informativa privacy</a> e acconsento a essere ricontattato per questa richiesta.</label>' +
        '<button class="btn btn-primary" type="submit">Mostra il listino completo</button>' +
        '<p class="listino-gate-feedback" role="status"></p>' +
      '</form>';
    const wrap = document.querySelector('.listino-table-wrap');
    wrap.parentNode.insertBefore(box, wrap.nextSibling);
    box.querySelector('form').addEventListener('submit', submit);
    return box;
  }

  async function submit(e) {
    e.preventDefault();
    const form = e.target;
    const fb = form.querySelector('.listino-gate-feedback');
    const consent = form.querySelector('[name="privacy"]');
    if (!consent.checked) { consent.focus(); consent.reportValidity(); return; }
    if (typeof validateContactForm === 'function' && !validateContactForm(form)) return;
    const btn = form.querySelector('[type="submit"]');
    btn.disabled = true;
    btn.textContent = 'Invio in corso...';
    fb.textContent = '';
    try {
      const payload = buildContactPayload(form);
      payload.origine = 'Listino completo Unitree';
      if (typeof RECAPTCHA_SITE_KEY !== 'undefined' && RECAPTCHA_SITE_KEY && window.grecaptcha) {
        try { payload.recaptcha_token = await window.grecaptcha.execute(RECAPTCHA_SITE_KEY, { action: 'contact' }); } catch (_) {}
      }
      await postLeadToGoogleScripts(payload);
      if (window.AbraAds && window.AbraAds.trackLead) window.AbraAds.trackLead();
      if (window.fbq) window.fbq('track', 'Lead');
      try { localStorage.setItem(KEY, '1'); } catch (_) {}
      rerender();
    } catch (err) {
      fb.textContent = 'Invio non riuscito. Scrivici a info@abrarobotics.com e ti mandiamo il listino.';
      btn.disabled = false;
      btn.textContent = 'Mostra il listino completo';
    }
  }

  window.listinoGate = {
    limit(list) {
      return unlocked() ? list : list.slice(0, FREE);
    },
    after(total, shown) {
      let box = document.getElementById('listino-completo');
      const locked = !unlocked() && total > shown;
      if (!locked) { if (box) box.hidden = true; return; }
      if (!box) box = buildGate();
      box.hidden = false;
      box.querySelector('.listino-gate-count').textContent =
        'Stai vedendo ' + shown + ' di ' + total + ' prodotti.';
    },
  };
})();
