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
})();
