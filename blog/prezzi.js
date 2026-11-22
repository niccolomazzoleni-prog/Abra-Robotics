/* Mini card dei prezzi del blog: la posiziona sopra la pagina (position: fixed),
   così non viene tagliata dalle tabelle che scorrono in orizzontale. */
(function () {
  function place(a) {
    var c = a.querySelector('.prezzo-card');
    if (!c) return;
    var r = a.getBoundingClientRect(), w = 220, h = c.offsetHeight || 240;
    var left = Math.min(Math.max(8, r.left + r.width / 2 - w / 2), window.innerWidth - w - 8);
    var top = r.top - h - 10;
    if (top < 8) top = r.bottom + 10;
    c.style.position = 'fixed';
    c.style.left = left + 'px';
    c.style.top = top + 'px';
    c.style.bottom = 'auto';
    c.style.transform = 'none';
  }
  document.querySelectorAll('.article-content a.prezzo').forEach(function (a) {
    a.addEventListener('mouseenter', function () { place(a); });
    a.addEventListener('focus', function () { place(a); });
  });
})();
