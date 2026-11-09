/* Demo interattive delle dashboard Abra (cartella demo/).
   I link con data-demo aprono la dashboard in un riquadro a tutto schermo sopra la pagina;
   su schermi stretti, o con Ctrl/Cmd, il link apre la pagina della demo come un link normale.
   L'iframe si carica solo al clic e si svuota alla chiusura, così la pagina resta leggera. */
(function () {
  var modal, frame, title, openLink, closeBtn, lastFocus;

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
      '.demo-modal iframe{flex:1;width:100%;border:0;display:block;background:#05070d}';
    document.head.appendChild(css);
    modal = document.createElement('div');
    modal.className = 'demo-modal';
    modal.setAttribute('role', 'dialog');
    modal.setAttribute('aria-modal', 'true');
    var en = document.documentElement.lang === 'en';
    modal.innerHTML = '<div class="dm-box"><div class="dm-bar"><b></b>' +
      '<a target="_blank" rel="noopener">' + (en ? 'Open in a new tab' : 'Apri in una nuova scheda') + ' ↗</a>' +
      '<button type="button">' + (en ? 'Close' : 'Chiudi') + ' ✕</button></div><iframe allow="fullscreen"></iframe></div>';
    title = modal.querySelector('b');
    openLink = modal.querySelector('a');
    closeBtn = modal.querySelector('button');
    frame = modal.querySelector('iframe');
    closeBtn.addEventListener('click', close);
    modal.addEventListener('click', function (e) { if (e.target === modal) close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && modal.classList.contains('open')) close(); });
    document.body.appendChild(modal);
  }

  function open(href, name) {
    if (!modal) build();
    lastFocus = document.activeElement;
    title.textContent = name;
    modal.setAttribute('aria-label', name);
    openLink.href = href;
    frame.title = name;
    frame.src = href;
    modal.classList.add('open');
    document.documentElement.style.overflow = 'hidden';
    closeBtn.focus();
  }

  function close() {
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
