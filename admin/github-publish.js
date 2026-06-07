/* Pubblica immagini e override su GitHub → trigger rigenerazione sito (Actions). */
window.AbraGithub = (function () {
  'use strict';

  const OWNER = 'niccolomazzoleni-prog';
  const REPO = 'Abra-Robotics';
  const BRANCH = 'main';

  function parseGhError(text) {
    try {
      const j = JSON.parse(text);
      return j.message || text;
    } catch (_) {
      return text;
    }
  }

  function api(path, token, opts = {}) {
    return fetch(`https://api.github.com/repos/${OWNER}/${REPO}${path}`, {
      ...opts,
      headers: {
        Authorization: `Bearer ${token}`,
        Accept: 'application/vnd.github.v3+json',
        'Content-Type': 'application/json',
        ...(opts.headers || {})
      }
    });
  }

  async function getFileSha(path, token) {
    const r = await api(`/contents/${encodeURIComponent(path).replace(/%2F/g, '/')}?ref=${BRANCH}`, token);
    if (r.status === 404) return null;
    if (!r.ok) throw new Error(await r.text());
    return (await r.json()).sha;
  }

  async function putBinary(path, file, message, token) {
    const sha = await getFileSha(path, token);
    const b64 = await new Promise((resolve, reject) => {
      const fr = new FileReader();
      fr.onload = () => resolve(fr.result.split(',')[1]);
      fr.onerror = reject;
      fr.readAsDataURL(file);
    });
    const r = await api(`/contents/${path}`, token, {
      method: 'PUT',
      body: JSON.stringify({
        message,
        content: b64,
        branch: BRANCH,
        ...(sha ? { sha } : {})
      })
    });
    if (!r.ok) throw new Error(`${path}: ${parseGhError(await r.text())}`);
  }

  async function putText(path, text, message, token) {
    const sha = await getFileSha(path, token);
    const b64 = btoa(unescape(encodeURIComponent(text)));
    const r = await api(`/contents/${path}`, token, {
      method: 'PUT',
      body: JSON.stringify({
        message,
        content: b64,
        branch: BRANCH,
        ...(sha ? { sha } : {})
      })
    });
    if (!r.ok) throw new Error(`${path}: ${parseGhError(await r.text())}`);
  }

  async function triggerRegenerate(token) {
    const r = await api('/actions/workflows/regenerate-site.yml/dispatches', token, {
      method: 'POST',
      body: JSON.stringify({ ref: BRANCH })
    });
    if (!r.ok) {
      const msg = parseGhError(await r.text());
      if (/not found|404/i.test(msg)) return;
      throw new Error('Workflow: ' + msg);
    }
  }

  async function publishLive({ jsonObject, allUploads, pendingFiles, onProgress }) {
    const token = window.AbraAdmin && window.AbraAdmin.getGithubToken();
    if (!token) throw new Error('Token GitHub mancante. Esci e rientra inserendo il PAT, oppure incollalo quando richiesto.');

    const uploads = allUploads || Object.entries(pendingFiles || {}).map(([sku, pf]) => ({ sku, ...pf }));
    for (let i = 0; i < uploads.length; i++) {
      const u = uploads[i];
      if (onProgress) onProgress(`Carico immagine ${u.sku} (${i + 1}/${uploads.length})…`);
      await putBinary(u.path, u.file, `admin: immagine ${u.sku}`, token);
    }

    if (onProgress) onProgress('Aggiorno product-images.json…');
    const jsonText = JSON.stringify(jsonObject, null, 2) + '\n';
    await putText('data/product-images.json', jsonText, 'admin: override immagini prodotto', token);

    if (onProgress) onProgress('Avvio rigenerazione catalogo (GitHub Actions)…');
    try {
      await triggerRegenerate(token);
    } catch (_) {
      /* push dei file può già aver triggerato il workflow */
    }

    return true;
  }

  return { publishLive };
})();
