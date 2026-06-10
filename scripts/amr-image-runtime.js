/** Applica override da data/amr-images.json su catalogo AMR, landing manifattura e schede prodotto. */
(function () {
  'use strict';

  var inProduct = /\/prodotti\/amr-/.test(location.pathname);
  var BASE = inProduct ? '../' : '';

  function bust(path) {
    if (!path || path.indexOf('http') === 0 || path.indexOf('data:') === 0) return path;
    return path + (path.indexOf('?') >= 0 ? '&' : '?') + 'v=' + Date.now();
  }

  function resolve(path) {
    if (!path) return '';
    if (path.indexOf('http') === 0) return path;
    return BASE + path.replace(/^\//, '');
  }

  function mergeAssets(catalog, overrides) {
    var map = {};
    catalog.forEach(function (item) {
      map[item.slug] = { slug: item.slug, file: item.file, video: item.video || '' };
    });
    Object.keys(overrides || {}).forEach(function (slug) {
      if (!map[slug]) return;
      if (overrides[slug].file) map[slug].file = overrides[slug].file;
      if ('video' in overrides[slug]) map[slug].video = overrides[slug].video || '';
    });
    return map;
  }

  function insertMedia(container, node) {
    var placeholder = container.querySelector('.robot-media-placeholder');
    var tag = container.querySelector('.robot-media-tag');
    if (placeholder) container.insertBefore(node, placeholder);
    else if (tag && tag.nextSibling) container.insertBefore(node, tag.nextSibling);
    else container.appendChild(node);
  }

  function setImgMedia(container, file, alt) {
    var src = bust(resolve(file));
    var existing = container.querySelector('img, video');
    if (existing && existing.tagName === 'IMG') {
      existing.src = src;
      if (alt) existing.alt = alt;
      existing.style.display = '';
      return;
    }
    if (existing) existing.remove();
    var img = document.createElement('img');
    img.src = src;
    img.alt = alt || '';
    img.loading = 'lazy';
    if (container.classList.contains('robot-media')) {
      img.onerror = function () { container.classList.add('no-img'); };
    }
    insertMedia(container, img);
  }

  function setVideoMedia(container, file, video, alt) {
    var poster = bust(resolve(file));
    var vidSrc = bust(resolve(video));
    var existing = container.querySelector('video');
    if (existing) {
      existing.src = vidSrc;
      existing.setAttribute('poster', poster);
      existing.style.display = '';
      return;
    }
    var img = container.querySelector('img');
    if (img) img.remove();
    var videoEl = document.createElement('video');
    videoEl.src = vidSrc;
    videoEl.setAttribute('poster', poster);
    videoEl.autoplay = true;
    videoEl.loop = true;
    videoEl.muted = true;
    videoEl.playsInline = true;
    insertMedia(container, videoEl);
  }

  function applyToContainer(container, asset, title) {
    if (!container || !asset || !asset.file) return;
    container.classList.remove('no-img');
    if (asset.video) setVideoMedia(container, asset.file, asset.video, title);
    else setImgMedia(container, asset.file, title);
  }

  function applyCatalog(map) {
    document.querySelectorAll('[data-amr-slug]').forEach(function (el) {
      var slug = el.getAttribute('data-amr-slug');
      var asset = map[slug];
      if (!asset) return;
      var titleEl = el.querySelector('h3');
      var title = titleEl ? titleEl.textContent : '';
      var media = el.querySelector('.cat-media.amr-media, .robot-media.amr-media');
      if (media) applyToContainer(media, asset, title);
    });
  }

  function applyProduct(map) {
    var m = location.pathname.match(/amr-([^.]+)\.html$/);
    if (!m) return;
    var asset = map[m[1]];
    if (!asset || !asset.file) return;
    var gallery = document.querySelector('.gallery-main');
    if (!gallery) return;
    var style =
      'max-width:100%;max-height:480px;width:100%;object-fit:contain;padding:24px;' +
      'filter:drop-shadow(0 12px 20px rgba(0,0,0,.12));mix-blend-mode:multiply;';
    if (asset.video) {
      gallery.innerHTML =
        '<video src="' + bust(resolve(asset.video)) + '" poster="' + bust(resolve(asset.file)) +
        '" autoplay loop muted playsinline style="' + style + '"></video>';
    } else {
      var img = document.getElementById('gallery-main-img');
      if (img) img.src = bust(resolve(asset.file));
    }
    var og = document.querySelector('meta[property="og:image"]');
    if (og) {
      try { og.content = new URL(resolve(asset.file), location.origin).href; } catch (_) {}
    }
  }

  Promise.all([
    fetch(BASE + 'data/amr-catalog.json', { cache: 'no-store' }).then(function (r) { return r.json(); }),
    fetch(BASE + 'data/amr-images.json', { cache: 'no-store' }).then(function (r) { return r.ok ? r.json() : {}; })
  ]).then(function (res) {
    var overrides = res[1] || {};
    if (!Object.keys(overrides).length) return;
    var map = mergeAssets(res[0], overrides);
    applyCatalog(map);
    if (inProduct) applyProduct(map);
    document.dispatchEvent(new Event('abra-amr-images-ready'));
  }).catch(function () {});
})();
