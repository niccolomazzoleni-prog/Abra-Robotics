// Conteggio visite senza cookie, attivo anche senza consenso.
// Manda al Company Brain solo pagina, dominio di provenienza e parametri utm:
// niente cookie, niente localStorage, nessun identificativo. Il server salva
// solo conteggi giornalieri (IP e user agent non vengono registrati).
(function () {
  'use strict';
  var ENDPOINT = 'https://brain.gpitton.com/api/visite';
  if (!/(^|\.)abrarobotics\.com$/.test(location.hostname)) return;
  if (navigator.webdriver || !navigator.sendBeacon) return;

  var ref = '';
  try { ref = document.referrer ? new URL(document.referrer).hostname : ''; } catch (e) {}
  var q;
  try { q = new URLSearchParams(location.search); } catch (e) { q = { get: function () { return null; }, has: function () { return false; } }; }
  var data = JSON.stringify({
    p: location.pathname,
    r: ref,
    us: q.get('utm_source') || '',
    um: q.get('utm_medium') || '',
    g: q.has('gclid') || q.has('gbraid') || q.has('wbraid') ? 1 : 0,
  });
  function send() { try { navigator.sendBeacon(ENDPOINT, data); } catch (e) {} }

  // Pagine prerenderizzate dal browser: si contano solo se l'utente le apre davvero.
  if (document.prerendering) document.addEventListener('prerenderingchange', send, { once: true });
  else send();

  // Azioni (clic e invio moduli): stessi principi, si manda solo tipo di azione, pagina
  // e, per i link interni, il percorso di destinazione. Nessun testo digitato, nessun identificativo.
  function action(type, target) {
    try {
      navigator.sendBeacon(ENDPOINT, JSON.stringify({ p: location.pathname, e: type, t: target || '' }));
    } catch (e) {}
  }
  function classify(a) {
    var href = a.getAttribute('href') || '';
    var url;
    try { url = new URL(href, location.href); } catch (e) { return null; }
    var internal = url.hostname === location.hostname;
    var path = internal ? url.pathname : '';
    if (/(^|\.)wa\.me$|whatsapp\./i.test(url.hostname)) return ['whatsapp', ''];
    if (/calendar\.google\.com|calendly\.com/i.test(url.hostname)) return ['chiamata', ''];
    if (url.protocol === 'tel:') return ['telefono', ''];
    if (url.protocol === 'mailto:') return ['email', ''];
    if (a.closest('.product-card')) return a.classList.contains('product-card-link') ? ['preventivo', path] : ['card', path];
    if (a.closest('.article-cta')) return ['cta', path];
    if (internal && (/\/assessment(-en)?\.html$/.test(url.pathname) || /^#(cta-finale|form|contatti)$/.test(url.hash))) return ['preventivo', path];
    return null;
  }
  document.addEventListener('click', function (ev) {
    var a = ev.target && ev.target.closest ? ev.target.closest('a[href]') : null;
    if (!a) return;
    var c = classify(a);
    if (c) action(c[0], c[1]);
  }, true);
  document.addEventListener('submit', function () { action('modulo', ''); }, true);
})();
