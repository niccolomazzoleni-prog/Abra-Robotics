/* Abra Robotics: comportamenti condivisi delle pagine V13 (tema, reveal, menu, preselezione percorso) */
(function () {
  var root = document.documentElement;

  var themeBtn = document.getElementById('theme');
  if (themeBtn) themeBtn.addEventListener('click', function () {
    var light = root.getAttribute('data-theme') !== 'light';
    if (light) root.setAttribute('data-theme', 'light'); else root.removeAttribute('data-theme');
    try { localStorage.setItem('abra-theme', light ? 'light' : 'dark'); } catch (e) {}
  });

  // Passi "Come lavorare assieme": ciclo automatico
  var steps = [].slice.call(document.querySelectorAll('#collaborazione .none')), cur = 0, timer;
  function on(i) { steps.forEach(function (s, k) { s.classList.toggle('on', k === i); }); cur = i; }
  if (steps.length) {
    timer = setInterval(function () { on((cur + 1) % steps.length); }, 3500);
    steps.forEach(function (s, i) { s.addEventListener('click', function () { on(i); }); });
  }

  // Preselezione del percorso nel form: link interni (data-start) e link da altre pagine (?percorso=)
  var sel = document.getElementById('percorso');
  function preselect(v) { if (sel && v && sel.querySelector('option[value="' + v + '"]')) sel.value = v; }
  document.querySelectorAll('[data-start]').forEach(function (a) {
    a.addEventListener('click', function () { preselect(a.getAttribute('data-start')); });
  });
  try { preselect(new URLSearchParams(location.search).get('percorso')); } catch (e) {}

  // Chiude il menu mobile dopo un click
  document.querySelectorAll('.nav-mobile-panel a').forEach(function (a) {
    a.addEventListener('click', function () { var d = a.closest('details'); if (d) d.removeAttribute('open'); });
  });

  // Reveal on scroll
  var els = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: .12 });
    els.forEach(function (r) { io.observe(r); });
  } else {
    els.forEach(function (r) { r.classList.add('in'); });
  }
})();
