/* Vista semplice delle demo (?vista=semplice), usata dalle card del sito: resta la scena con le
   azioni principali, i pannelli da esperti si nascondono (CSS html.semplice in ogni pagina).
   Una riga spiega cosa si sta guardando, "Vista completa" toglie il filtro.
   Con &rec=1 (registrazioni per le card) spariscono anche la riga e i pannelli.
   Va caricato nel <head> dopo window.DEMO_SEMPLICE, così la classe c'è prima del primo disegno. */
(function () {
  var q = new URLSearchParams(location.search);
  if (q.get('vista') !== 'semplice') return;
  var rec = q.get('rec') === '1';
  var root = document.documentElement;
  root.classList.add('semplice');
  if (rec) root.classList.add('rec');
  var cfg = window.DEMO_SEMPLICE || {};

  var css = document.createElement('style');
  css.textContent =
    '.vs-info{font:13px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;color:#e9ebef;background:rgba(5,7,13,.94);' +
    'border:1px solid rgba(255,255,255,.18);border-radius:12px;padding:12px 14px;max-width:440px;pointer-events:auto}' +
    '.vs-info.vs-float{position:fixed;left:14px;top:62px;z-index:40}' +
    '.vs-info.vs-inline{max-width:none;margin:0 0 12px}' +
    '.vs-info p{margin:0 0 8px}' +
    '.vs-info .vs-row{display:flex;gap:14px;align-items:center;font-size:12.5px}' +
    '.vs-info a{color:#fff}' +
    '.vs-info button{margin-left:auto;background:none;border:0;color:#aab;font:inherit;cursor:pointer;padding:2px 4px}' +
    '@media (max-width:700px){.vs-info.vs-float{left:10px;right:10px;top:56px;max-width:none}}';
  document.head.appendChild(css);

  function pronto(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  pronto(function () {
    (cfg.nascondiSezioni || []).forEach(function (titolo) {
      [].forEach.call(document.querySelectorAll('.eyebrow.sec'), function (el) {
        if (el.textContent.trim().toLowerCase().indexOf(titolo) === 0) {
          el.style.display = 'none';
          if (el.nextElementSibling) el.nextElementSibling.style.display = 'none';
        }
      });
    });
    if (!rec && cfg.testo) {
      var box = document.createElement('div');
      var completa = new URL(location.href);
      completa.searchParams.delete('vista');
      box.className = 'vs-info ' + (cfg.dentro ? 'vs-inline' : 'vs-float');
      box.innerHTML = '<p></p><div class="vs-row"><a href="' + completa.pathname + completa.search + '">Vista completa</a>' +
        '<button type="button" aria-label="Chiudi">✕</button></div>';
      box.querySelector('p').textContent = cfg.testo;
      box.querySelector('button').addEventListener('click', function () { box.remove(); });
      var dove = cfg.dentro && document.querySelector(cfg.dentro);
      if (dove) dove.insertBefore(box, dove.firstChild);
      else document.body.appendChild(box);
    }
    if (cfg.avvio) setTimeout(function () { cfg.avvio(rec); }, cfg.ritardo || 1500);
  });
})();
