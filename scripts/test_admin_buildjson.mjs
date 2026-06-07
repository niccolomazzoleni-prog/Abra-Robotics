/**
 * Simula buildJson() dell'admin dopo upload file — verifica che il path non si perda.
 */
import { readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const overrides = JSON.parse(readFileSync(join(ROOT, 'data/product-images.json'), 'utf8'));
const manifest = JSON.parse(readFileSync(join(ROOT, 'listini/pubblico/catalogo-manifest.json'), 'utf8'));

function defaultPath(sku) {
  const e = manifest[sku];
  return (overrides[sku] && overrides[sku].path) || (e && e.immagine) || '';
}

function buildJson(pendingFiles, pendingGallery, dirtySkus) {
  const out = JSON.parse(JSON.stringify(overrides));
  Object.keys(out).forEach(sku => delete out[sku]._dirty);
  const skus = new Set([...Object.keys(pendingFiles), ...Object.keys(pendingGallery), ...dirtySkus]);
  skus.forEach(sku => {
    const pathFromPending = pendingFiles[sku] && pendingFiles[sku].path;
    const path = pathFromPending || defaultPath(sku);
    const extraFromPending = (pendingGallery[sku] || []).map(g => g.path);
    const gallery = [...new Set([path, ...extraFromPending].filter(Boolean))];
    out[sku] = { path: path || gallery[0], gallery };
  });
  return out;
}

// Caso che rompeva il publish: GO2-AIR con vecchio override, nuovo upload
const pendingFiles = {
  'GO2-AIR': { path: 'images/prodotti/go2-air.webp' },
  'B2-LIDAR': { path: 'images/prodotti/b2-lidar.webp' }
};
const json = buildJson(pendingFiles, {}, ['GO2-AIR', 'B2-LIDAR']);

let ok = true;
for (const [sku, expected] of Object.entries({
  'GO2-AIR': 'images/prodotti/go2-air.webp',
  'B2-LIDAR': 'images/prodotti/b2-lidar.webp'
})) {
  const got = json[sku]?.path;
  if (got !== expected) {
    console.error(`FAIL ${sku}: atteso ${expected}, got ${got}`);
    ok = false;
  } else {
    console.log(`OK ${sku} → ${got}`);
  }
}
process.exit(ok ? 0 : 1);
