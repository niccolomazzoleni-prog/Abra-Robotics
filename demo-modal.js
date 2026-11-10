/* Demo interattive delle dashboard Abra (cartella demo/).
   I link con data-demo aprono la dashboard in un riquadro a tutto schermo sopra la pagina;
   su schermi stretti, o con Ctrl/Cmd, il link apre la pagina della demo come un link normale.
   L'iframe si carica solo al clic e si svuota alla chiusura, così la pagina resta leggera.
   Finché la demo carica i modelli 3D (messaggi {type:'abra-demo', progress, ready} da demo/semplice.js)
   un velo con la barra di avanzamento copre il riquadro. */
(function () {
  var modal, frame, title, openLink, closeBtn, lastFocus, veil, bar, pct, safety;

  function build() {
    var css = document.createElement('style');
    css.textContent =
      '.demo-modal{position:fixed;inset:0;z-index:3000;display:none;align-items:center;justify-content:center;background:rgba(0,0,0,.84);padding:2vh 2vw}' +
      '.demo-modal.open{display:flex}' +
      '.demo-modal .dm-box{display:flex;flex-direction:column;width:min(1680px,100%);height:100%;border-radius:14px;overflow:hidden;background:#05070d;border:1px solid rgba(255,255,255,.16)}' +
      '.demo-modal .dm-bar{display:flex;align-items:center;gap:14px;padding:10px 14px;border-bottom:1px solid rgba(255,255,255,.1);font:13px/1.3 var(--mono,monospace);color:#cfd3dc}' +
      '.demo-modal .dm-bar b{flex:1;color:#fff;font-weight:500}' +
      '.demo-modal .dm-bar a,.demo-modal .dm-bar button{font:inherit;color:#fff;background:none;border:1px solid rgba(255,255,255,.22);border-radius:999px;padding:6px 12px;cursor:pointer;text-decoration:none}' +
      '.demo-modal .dm-bar a:hover,.demo-modal .dm-bar button:hover{border-color:#fff}' +
      '.demo-modal .dm-body{position:relative;flex:1;min-height:0}' +
      '.demo-modal iframe{position:absolute;inset:0;width:100%;height:100%;border:0;display:block;background:#05070d}' +
      '.demo-modal .dm-load{position:absolute;inset:0;z-index:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;padding:24px;background:#000;color:#f5f5f5;text-align:center;font:300 15px/1.5 var(--sans,"Geist",sans-serif);transition:opacity .5s ease,visibility .5s}' +
      '.demo-modal .dm-load.dm-via{opacity:0;visibility:hidden;pointer-events:none}' +
      '.demo-modal .dm-lt{font-size:24px;font-weight:400;letter-spacing:-.025em;line-height:1.15;color:#fff}' +
      '.demo-modal .dm-pb{position:relative;width:min(320px,72vw);height:6px;overflow:hidden;border-radius:999px;background:#1c1c1c}' +
      '.demo-modal .dm-pb i{position:absolute;left:0;top:0;bottom:0;width:0;border-radius:inherit;background:linear-gradient(90deg,#2bc4a8,#2f5bff);transition:width .3s ease}' +
      '.demo-modal .dm-pb.dm-ind i{width:36%;transition:none;animation:dmind 1.25s ease-in-out infinite}' +
      '.demo-modal .dm-pct{min-height:18px;font:500 12px/1.5 var(--mono,monospace);letter-spacing:.12em;text-transform:uppercase;color:#8b8b8b}' +
      '@keyframes dmind{0%{transform:translateX(-100%)}100%{transform:translateX(280%)}}' +
      '@media (prefers-reduced-motion:reduce){.demo-modal .dm-pb i,.demo-modal .dm-load{animation:none!important;transition:none!important}}';
    document.head.appendChild(css);
    modal = document.createElement('div');
    modal.className = 'demo-modal';
    modal.setAttribute('role', 'dialog');
    modal.setAttribute('aria-modal', 'true');
    var en = document.documentElement.lang === 'en';
    modal.innerHTML = '<div class="dm-box"><div class="dm-bar"><b></b>' +
      '<a target="_blank" rel="noopener">' + (en ? 'Open in a new tab' : 'Apri in una nuova scheda') + ' ↗</a>' +
      '<button type="button">' + (en ? 'Close' : 'Chiudi') + ' ✕</button></div>' +
      '<div class="dm-body"><iframe allow="fullscreen"></iframe>' +
      '<div class="dm-load"><div class="dm-lt"></div><div class="dm-pb dm-ind" role="progressbar" aria-valuemin="0" aria-valuemax="100"><i></i></div><div class="dm-pct"></div></div></div></div>';
    title = modal.querySelector('b');
    openLink = modal.querySelector('a');
    closeBtn = modal.querySelector('button');
    frame = modal.querySelector('iframe');
    veil = modal.querySelector('.dm-load');
    bar = modal.querySelector('.dm-pb');
    pct = modal.querySelector('.dm-pct');
    closeBtn.addEventListener('click', close);
    modal.addEventListener('click', function (e) { if (e.target === modal) close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && modal.classList.contains('open')) close(); });
    window.addEventListener('message', function (e) {
      var d = e.data;
      if (!d || e.source !== frame.contentWindow) return;
      if (d.type === 'abra-demo-cta') {   // clic su un invito dentro la demo: si registra solo se il sito ha gtag (il consenso lo gestisce già la home)
        if (typeof window.gtag === 'function') window.gtag('event', 'demo_cta', { demo: String(d.demo || ''), action: String(d.action || '') });
        return;
      }
      if (d.type !== 'abra-demo') return;
      progress(+d.progress || 0, !!d.ready);
    });
    document.body.appendChild(modal);
  }

  // velo di caricamento: la barra segue i byte scaricati dalla demo, sparisce quando la scena è pronta
  function progress(p, ready) {
    clearTimeout(safety);
    if (ready) {
      veil.classList.add('dm-via');
      return;
    }
    var n = Math.round(Math.min(1, p) * 100);
    bar.classList.toggle('dm-ind', n <= 0);
    bar.firstChild.style.width = n > 0 ? n + '%' : '';
    bar.setAttribute('aria-valuenow', n);
    pct.textContent = n > 0 && n < 92 ? (en() ? 'Downloading 3D models · ' : 'Scarico i modelli 3D · ') + n + '%' : (en() ? 'Preparing the scene' : 'Preparo la scena');   // l'ultimo 8% è la scena che si prepara
    safety = setTimeout(function () { veil.classList.add('dm-via'); }, 45000);   // se la demo non risponde il velo non resta
  }
  function en() { return document.documentElement.lang === 'en'; }

  function open(href, name) {
    if (!modal) build();
    lastFocus = document.activeElement;
    title.textContent = name;
    modal.setAttribute('aria-label', name);
    openLink.href = href;
    frame.title = name;
    veil.querySelector('.dm-lt').textContent = name;
    veil.classList.remove('dm-via');
    if (/[?&]vista=semplice/.test(href)) progress(0, false);   // solo la vista semplice comunica l'avanzamento
    else veil.classList.add('dm-via');
    frame.src = href;
    modal.classList.add('open');
    document.documentElement.style.overflow = 'hidden';
    closeBtn.focus();
  }

  function close() {
    clearTimeout(safety);
    modal.classList.remove('open');
    frame.src = 'about:blank';
    document.documentElement.style.overflow = '';
    if (lastFocus) lastFocus.focus();
  }

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[data-demo]');
    if (!a || window.innerWidth < 900 || e.ctrlKey || e.metaKey || e.shiftKey) return;
    e.preventDefault();
    open(a.href, a.getAttribute('data-demo'));
  });
})();
