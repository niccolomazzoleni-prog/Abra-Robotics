/** Applica override da product-images.json su catalogo e schede prodotto (con galleria). */
(function () {
  'use strict';

  var inProduct = /\/prodotti\//.test(location.pathname);
  var BASE = inProduct ? '../' : '';
  var BUST = '?v=' + Date.now();

  function entryImages(entry) {
    if (!entry) return [];
    if (typeof entry === 'string') return [entry];
    if (Array.isArray(entry.gallery) && entry.gallery.length) return entry.gallery;
    if (entry.path) return [entry.path];
    return [];
  }

  function resolveSrc(path) {
    if (!path || path.indexOf('http') === 0) return path || '';
    if (path.indexOf('prodotti/') === 0) return path.slice('prodotti/'.length);
    return BASE + path;
  }

  function withBust(src) {
    if (!src || src.indexOf('http') !== 0 && src.indexOf('data:') !== 0) {
      return src + (src.indexOf('?') >= 0 ? '&' : '?') + 'v=' + Date.now();
    }
    return src;
  }

  function applyCatalog(overrides) {
    document.querySelectorAll('.cat-card[data-sku]').forEach(function (card) {
      var sku = card.dataset.sku;
      var paths = entryImages(overrides[sku]);
      if (!paths.length) return;
      var img = card.querySelector('.cat-media img');
      if (img) {
        img.src = withBust(resolveSrc(paths[0]));
        img.style.display = '';
        card.querySelector('.cat-media').classList.remove('no-img');
      }
    });
  }

  function applyRobotCards(overrides, slugToSku) {
    document.querySelectorAll('.robot-card').forEach(function (card) {
      var link = card.querySelector('a[href*="prodotti/"]');
      if (!link) return;
      var slug = (link.getAttribute('href') || '').split('/').pop();
      var sku = slugToSku[slug];
      if (!sku) return;
      var paths = entryImages(overrides[sku]);
      if (!paths.length) return;
      var img = card.querySelector('.robot-media img, img');
      if (img) {
        img.src = withBust(resolveSrc(paths[0]));
        img.style.display = '';
        var media = card.querySelector('.robot-media');
        if (media) media.classList.remove('no-img');
      }
    });
  }

  function buildThumbs(galleryEl, paths, alt) {
    var existing = galleryEl.querySelector('.gallery-thumbs');
    if (existing) existing.remove();
    if (paths.length < 2) return;

    var wrap = document.createElement('div');
    wrap.className = 'gallery-thumbs';
    paths.forEach(function (p, i) {
      var thumb = document.createElement('div');
      thumb.className = 'gallery-thumb' + (i === 0 ? ' active' : '');
      thumb.dataset.index = String(i);
      var im = document.createElement('img');
      im.src = withBust(resolveSrc(p));
      im.alt = alt + ' vista ' + (i + 1);
      thumb.appendChild(im);
      wrap.appendChild(thumb);
    });
    galleryEl.appendChild(wrap);
  }

  function applyProduct(overrides, slugToSku) {
    var slug = location.pathname.split('/').pop() || '';
    var sku = slugToSku[slug];
    if (!sku) return;
    var paths = entryImages(overrides[sku]);
    if (!paths.length) return;

    var main = document.getElementById('gallery-main-img');
    var gallery = document.querySelector('.gallery');
    if (!main || !gallery) return;

    var alt = main.getAttribute('alt') || sku;
    main.src = withBust(resolveSrc(paths[0]));
    main.style.display = '';
    buildThumbs(gallery, paths, alt);

    var og = document.querySelector('meta[property="og:image"]');
    if (og) og.content = new URL(resolveSrc(paths[0]), location.origin).href;
  }

  Promise.all([
    fetch(BASE + 'data/product-images.json', { cache: 'no-store' }).then(function (r) { return r.ok ? r.json() : {}; }),
    fetch(BASE + 'listini/pubblico/catalogo-manifest.json', { cache: 'no-store' }).then(function (r) { return r.ok ? r.json() : {}; })
  ]).then(function (res) {
    var overrides = res[0];
    var manifest = res[1];
    var slugToSku = {};
    Object.keys(manifest).forEach(function (sku) {
      var s = manifest[sku].slug || '';
      if (s) slugToSku[s] = sku;
    });
    if (inProduct) applyProduct(overrides, slugToSku);
    else {
      applyCatalog(overrides);
      applyRobotCards(overrides, slugToSku);
    }
    document.dispatchEvent(new Event('abra-images-ready'));
  }).catch(function () {});
})();
