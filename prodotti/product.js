/* ──────────────────────────────────────────────
   Shared product-page behaviour (Abra Robotics)
   Used by every Unitree humanoid product page.
   Gallery reads image sources from the thumbnails
   in the DOM, so no per-page image array is needed.
─────────────────────────────────────────────── */

/* ── Gallery Slider (dopo image-runtime.js se presente) ── */
(function () {
  function initGallery() {
    const mainImg = document.getElementById('gallery-main-img');
    const thumbs = Array.from(document.querySelectorAll('.gallery-thumb'));
    if (!mainImg || !thumbs.length) return;

    const images = thumbs.map(t => t.querySelector('img').getAttribute('src'));
    let current = 0;

    function setImage(index) {
      current = (index + images.length) % images.length;
      mainImg.classList.add('fade');
      setTimeout(() => {
        mainImg.src = images[current];
        mainImg.classList.remove('fade');
      }, 150);
      thumbs.forEach((t, i) => t.classList.toggle('active', i === current));
    }

    const prev = document.getElementById('gallery-prev');
    const next = document.getElementById('gallery-next');
    if (prev) prev.addEventListener('click', () => setImage(current - 1));
    if (next) next.addEventListener('click', () => setImage(current + 1));
    thumbs.forEach((t, i) => t.addEventListener('click', () => setImage(i)));
  }

  document.addEventListener('abra-images-ready', initGallery);
  initGallery();
})();

/* ── Animated Counters ── */
(function () {
  function easeOutCubic(t) { return 1 - Math.pow(1 - t, 3); }
  function animateCounter(el, target, duration) {
    const start = performance.now();
    (function update(now) {
      const p = Math.min((now - start) / duration, 1);
      el.textContent = Math.round(easeOutCubic(p) * target);
      if (p < 1) requestAnimationFrame(update);
      else el.textContent = target;
    })(performance.now());
  }
  const statsEl = document.getElementById('stats-section');
  if (!statsEl) return;
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.querySelectorAll('.counter').forEach(c =>
        animateCounter(c, parseInt(c.dataset.target, 10), 1800)
      );
      obs.unobserve(entry.target);
    });
  }, { threshold: 0.5 });
  obs.observe(statsEl);
})();

/* ── Parallax Collage ── */
(function () {
  const colA = document.getElementById('parallax-col-a');
  const colB = document.getElementById('parallax-col-b');
  const container = document.getElementById('parallax-container');
  if (!colA || !colB || window.matchMedia('(max-width: 768px)').matches) return;

  let ticking = false;
  window.addEventListener('scroll', () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      const center = container.getBoundingClientRect().top + container.offsetHeight / 2 - window.innerHeight / 2;
      colA.style.transform = `translateY(${center * -0.06}px)`;
      colB.style.transform = `translateY(${40 + center * -0.03}px)`;
      ticking = false;
    });
  }, { passive: true });
})();

/* ── Lazy Video Autoplay ── */
(function () {
  const videos = document.querySelectorAll('.feature-video[data-src]');
  if (!videos.length) return;
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const video = entry.target;
      const poster = video.nextElementSibling;
      if (entry.isIntersecting) {
        if (!video.src) { video.src = video.dataset.src; video.load(); }
        video.play().then(() => { if (poster) poster.classList.add('hidden'); }).catch(() => {});
      } else {
        video.pause();
      }
    });
  }, { threshold: 0.4 });
  videos.forEach(v => obs.observe(v));
})();

/* ── Scroll fade-in ── */
(function () {
  const els = document.querySelectorAll('.feature-card, .product-stat, .step, .parallax-img-wrap, .key-spec, .spec-mini-card, .comp-model-card');
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('visible'); obs.unobserve(entry.target); }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  els.forEach((el) => {
    const siblings = Array.from(el.parentElement.children).filter(c => c.classList[0] === el.classList[0]);
    const idx = siblings.indexOf(el);
    el.style.opacity = '0';
    el.style.transform = 'translateY(24px)';
    el.style.transition = `opacity 0.6s ease ${idx * 0.1}s, transform 0.6s ease ${idx * 0.1}s`;
    obs.observe(el);
  });
})();

/* ── Availability sync ──────────────────────────────────────────────────────
   Legge ../availability.json (aggiornato da GitHub Actions ogni mattina).
   Aggiorna il buy-box solo quando quadruped.de è vantaggioso rispetto alla
   nostra filiera standard (4-6 settimane):
     - "available" (Sofort verfügbar) → prodotto in stock, consegna nei tempi normali
     - "date" con data entro 6 settimane → quadruped più veloce, mostra la data
     - "date" con data oltre 6 settimane → la nostra filiera è più rapida, non toccare
     - "unavailable" (Ausverkauft) → segnala indisponibilità
──────────────────────────────────────────────────────────────────────────── */
(function () {
  const FAMILIES = [
    [/unitree-g1d|unitree-g1-d/, 'g1d'],
    [/unitree-g1/,               'g1'],
    [/unitree-go2w/,             'go2w'],
    [/unitree-go2/,              'go2'],
    [/unitree-b2w/,              'b2w'],
    [/unitree-b2/,               'b2'],
    [/unitree-h2/,               'h2'],
    [/unitree-h1/,               'h1'],
    [/unitree-r1/,               'r1'],
  ];

  function getFamily() {
    const path = location.pathname.toLowerCase();
    for (const [re, key] of FAMILIES) if (re.test(path)) return key;
    return null;
  }

  function fmtDate(iso) {
    return new Date(iso).toLocaleDateString('it-IT', { day: 'numeric', month: 'long', year: 'numeric' });
  }

  function setDeliveryText(deliveryLi, text) {
    if (!deliveryLi) return;
    const ico = deliveryLi.querySelector('.bp-ico');
    if (ico && ico.nextSibling && ico.nextSibling.nodeType === 3)
      ico.nextSibling.textContent = text;
  }

  function applyStatus(info) {
    const badge = document.querySelector('.buy-box-stock');
    if (!badge) return;
    const nodes = badge.childNodes;
    const textNode = nodes[nodes.length - 1];
    const deliveryLi = [...document.querySelectorAll('.buy-box-perks li')]
      .find(li => li.textContent.includes('Consegna stimata'));

    badge.classList.remove('status-date', 'status-unavailable');

    if (info.status === 'available') {
      // Sofort verfügbar: prodotto in stock — rimuovi stima consegna, non applicabile
      if (textNode && textNode.nodeType === 3) textNode.textContent = ' Disponibile';
      if (deliveryLi) deliveryLi.remove();

    } else if (info.status === 'date') {
      // Mostra la data solo se è entro 6 settimane da oggi (altrimenti la nostra filiera è più rapida)
      const sixWeeksFromNow = new Date();
      sixWeeksFromNow.setDate(sixWeeksFromNow.getDate() + 42);
      const availDate = new Date(info.available_from);

      if (availDate <= sixWeeksFromNow) {
        const d = fmtDate(info.available_from);
        badge.classList.add('status-date');
        if (textNode && textNode.nodeType === 3) textNode.textContent = ' Dal ' + d;
        setDeliveryText(deliveryLi, ' Prima disponibilità stimata: ' + d);
      }
      // altrimenti: non toccare nulla, la nostra filiera 4-6 sett. è più rapida

    } else if (info.status === 'unavailable') {
      badge.classList.add('status-unavailable');
      if (textNode && textNode.nodeType === 3) textNode.textContent = ' Non disponibile';
      setDeliveryText(deliveryLi, ' Verifica disponibilità con il nostro team');
    }
  }

  const family = getFamily();
  if (!family) return;
  const base = location.pathname.includes('/prodotti/') ? '../' : './';
  fetch(base + 'availability.json')
    .then(r => r.json())
    .then(data => {
      const info = data.products && data.products[family];
      if (info) applyStatus(info);
    })
    .catch(() => {/* silent fail — HTML statico come fallback */});
})();
