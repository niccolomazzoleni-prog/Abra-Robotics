/* Video delle applicazioni: il file si collega solo quando il video si avvicina allo schermo (data-src),
   e un solo video alla volta resta in riproduzione. */
(function () {
  if (window.__vlib) return; window.__vlib = 1;
  function load(v) { var s = v.getAttribute('data-src'); if (s) { v.src = s; v.removeAttribute('data-src'); } }
  function init() {
    var vids = document.querySelectorAll('.vlib-card video[data-src]');
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (x) { if (x.isIntersecting) { load(x.target); io.unobserve(x.target); } });
      }, { rootMargin: '300px 0px' });
      vids.forEach(function (v) { io.observe(v); });
    } else { vids.forEach(load); }
    document.addEventListener('play', function (ev) {
      document.querySelectorAll('.vlib-card video').forEach(function (v) { if (v !== ev.target && !v.paused) v.pause(); });
    }, true);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
