/** Applica override immagini dal JSON sul catalogo (anteprima immediata senza rigenerare HTML). */
(function () {
  'use strict';
  fetch('data/product-images.json', { cache: 'no-store' })
    .then(r => (r.ok ? r.json() : {}))
    .then(overrides => {
      document.querySelectorAll('.cat-card[data-sku]').forEach(card => {
        const sku = card.dataset.sku;
        const entry = overrides[sku];
        const path = entry && (entry.path || entry);
        if (!path || typeof path !== 'string') return;
        const img = card.querySelector('.cat-media img');
        if (img) img.src = path;
      });
    })
    .catch(() => {});
})();
