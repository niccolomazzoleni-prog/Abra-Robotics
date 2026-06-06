/* Protezione area admin — password + sessione (8 h). */
(function () {
  'use strict';

  const AUTH_URL = '../data/admin-auth.json';
  const SESSION_KEY = 'abra_admin_until';
  const GH_TOKEN_KEY = 'abra_gh_token';
  const SESSION_MS = 8 * 60 * 60 * 1000;

  window.AbraAdmin = {
    getGithubToken() {
      return sessionStorage.getItem(GH_TOKEN_KEY) || '';
    },
    setGithubToken(token) {
      if (token) sessionStorage.setItem(GH_TOKEN_KEY, token);
      else sessionStorage.removeItem(GH_TOKEN_KEY);
    },
    logout() {
      sessionStorage.removeItem(SESSION_KEY);
      sessionStorage.removeItem(GH_TOKEN_KEY);
      location.reload();
    },
    isUnlocked() {
      return Date.now() < Number(sessionStorage.getItem(SESSION_KEY) || 0);
    },
    unlock() {
      sessionStorage.setItem(SESSION_KEY, String(Date.now() + SESSION_MS));
    }
  };

  async function sha256(text) {
    const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
    return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, '0')).join('');
  }

  function gateHtml(needsSetup) {
    return `
      <div id="admin-gate" style="position:fixed;inset:0;z-index:9999;background:var(--gray-50);display:flex;align-items:center;justify-content:center;padding:24px;">
        <form id="admin-login-form" style="width:100%;max-width:400px;background:#fff;border:1px solid var(--gray-200);border-radius:12px;padding:28px;">
          <p class="label">Area interna</p>
          <h2 style="margin:8px 0 16px;font-size:1.5rem;">${needsSetup ? 'Imposta password admin' : 'Accedi all\'admin'}</h2>
          <p style="color:var(--gray-600);font-size:0.88rem;line-height:1.5;margin-bottom:20px;">
            ${needsSetup
              ? 'Prima configurazione: scegli una password (min. 8 caratteri). Servirà anche un token GitHub per pubblicare sul sito live.'
              : 'Inserisci la password admin. Per pubblicare le immagini sul sito live serve un token GitHub (memorizzato solo in questa sessione).'}
          </p>
          <label style="display:block;font-size:0.78rem;font-weight:700;margin-bottom:6px;">Password</label>
          <input type="password" id="admin-pwd" required minlength="8" style="width:100%;padding:10px 12px;border:1px solid var(--gray-200);border-radius:8px;margin-bottom:14px;font:inherit;">
          ${needsSetup ? `
            <label style="display:block;font-size:0.78rem;font-weight:700;margin-bottom:6px;">Conferma password</label>
            <input type="password" id="admin-pwd2" required minlength="8" style="width:100%;padding:10px 12px;border:1px solid var(--gray-200);border-radius:8px;margin-bottom:14px;font:inherit;">
          ` : ''}
          <label style="display:block;font-size:0.78rem;font-weight:700;margin-bottom:6px;">Token GitHub (per pubblicare live)</label>
          <input type="password" id="admin-gh" placeholder="ghp_… o github_pat_…" style="width:100%;padding:10px 12px;border:1px solid var(--gray-200);border-radius:8px;margin-bottom:8px;font:inherit;">
          <p style="font-size:0.75rem;color:var(--gray-500);margin-bottom:16px;">Crea un <a href="https://github.com/settings/tokens" target="_blank" rel="noopener">Personal Access Token</a> con permesso <strong>Contents: Read and write</strong> sul repo Abra-Robotics.</p>
          <button type="submit" class="btn btn-primary" style="width:100%;">${needsSetup ? 'Salva e accedi' : 'Accedi'}</button>
          <p id="admin-login-err" style="color:#b91c1c;font-size:0.82rem;margin-top:12px;display:none;"></p>
        </form>
      </div>`;
  }

  async function publishAuthHash(hash, token) {
    const path = 'data/admin-auth.json';
    const content = JSON.stringify({ password_sha256: hash }, null, 2) + '\n';
    const b64 = btoa(unescape(encodeURIComponent(content)));
    let sha = null;
    const get = await fetch(`https://api.github.com/repos/niccolomazzoleni-prog/Abra-Robotics/contents/${path}`, {
      headers: { Authorization: `Bearer ${token}`, Accept: 'application/vnd.github+json' }
    });
    if (get.ok) sha = (await get.json()).sha;
    const put = await fetch(`https://api.github.com/repos/niccolomazzoleni-prog/Abra-Robotics/contents/${path}`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token}`, Accept: 'application/vnd.github+json', 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: 'admin: imposta password',
        content: b64,
        branch: 'main',
        ...(sha ? { sha } : {})
      })
    });
    if (!put.ok) throw new Error(await put.text());
  }

  async function initGate() {
    if (window.AbraAdmin.isUnlocked()) return;

    const auth = await fetch(AUTH_URL).then(r => r.json()).catch(() => ({}));
    const needsSetup = !auth.password_sha256;

    document.body.insertAdjacentHTML('afterbegin', gateHtml(needsSetup));
    document.body.style.overflow = 'hidden';

    document.getElementById('admin-login-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const err = document.getElementById('admin-login-err');
      err.style.display = 'none';
      const pwd = document.getElementById('admin-pwd').value;
      const gh = document.getElementById('admin-gh').value.trim();

      try {
        if (needsSetup) {
          const pwd2 = document.getElementById('admin-pwd2').value;
          if (pwd !== pwd2) throw new Error('Le password non coincidono.');
          if (!gh) throw new Error('Serve il token GitHub per salvare la password sul repo.');
          const hash = await sha256(pwd);
          await publishAuthHash(hash, gh);
        } else {
          const hash = await sha256(pwd);
          if (hash !== auth.password_sha256) throw new Error('Password errata.');
        }
        if (gh) window.AbraAdmin.setGithubToken(gh);
        window.AbraAdmin.unlock();
        document.getElementById('admin-gate').remove();
        document.body.style.overflow = '';
      } catch (ex) {
        err.textContent = ex.message || 'Errore accesso';
        err.style.display = 'block';
      }
    });
  }

  document.addEventListener('DOMContentLoaded', initGate);
})();
