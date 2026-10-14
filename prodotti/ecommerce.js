/* Abra Robotics — e-commerce schede prodotto
 * 1) Stripe: collega il bottone "Acquista" al Payment Link del prodotto (vedi stripe-config.js).
 * 2) Form "Richiedi informazioni" in alto sulla scheda: invio a Google Apps Script.
 *
 * Sito statico (GitHub Pages, nessun backend): il checkout usa gli Stripe Payment Link,
 * creati nella dashboard Stripe e incollati in stripe-config.js.
 */
(function () {
  "use strict";

  // ── 1. Stripe checkout sul bottone "Acquista" ──────────────────────────────
  function currentSlug() {
    var parts = window.location.pathname.split("/");
    return parts[parts.length - 1] || "";
  }

  function wireStripeTrust(url) {
    var online = document.querySelector(".trust-stripe-online");
    var pending = document.querySelector(".trust-stripe-pending");
    if (url) {
      if (online) online.style.display = "";
      if (pending) pending.style.display = "none";
    } else {
      if (online) online.style.display = "none";
      if (pending) pending.style.display = "";
    }
  }

  // L'acquisto online e' riservato ai clienti con Partita IVA (Condizioni di vendita, art. 2.3):
  // l'avviso compare sotto ogni bottone "Acquista" attivo.
  function addB2bNote(btn) {
    if (btn.nextElementSibling && btn.nextElementSibling.classList.contains("buy-b2b-note")) return;
    var en = (document.documentElement.lang || "").toLowerCase().indexOf("en") === 0;
    var note = document.createElement("p");
    note.className = "buy-b2b-note";
    note.style.cssText = "margin:8px 0 0;font-size:.8rem;line-height:1.4;color:var(--gray-600,#666)";
    note.innerHTML = en
      ? 'Online purchase reserved for customers with a VAT number. <a href="/en/condizioni-di-vendita-en.html">Terms of sale</a> · Private buyer? <a href="#form">Request a quote</a>.'
      : 'Acquisto online riservato a clienti con Partita IVA. <a href="/condizioni-di-vendita.html">Condizioni di vendita</a> · Sei un privato? <a href="#form">Chiedi un preventivo</a>.';
    btn.insertAdjacentElement("afterend", note);
  }

  function wireBuyButtons() {
    var links = (window.STRIPE_PAYMENT_LINKS || {});
    var url = links[currentSlug()] || "";
    var buyBtns = document.querySelectorAll(".buy-btn");
    buyBtns.forEach(function (btn) {
      // GA4: click su Acquista (conversione misurata dal Company Brain)
      btn.addEventListener("click", function () {
        if (window.gtag) window.gtag("event", "begin_checkout", { item_id: currentSlug(), checkout_ready: url ? "si" : "no" });
      });
      if (url) {
        // Payment Link configurato: checkout reale (apre Stripe in nuova scheda)
        btn.setAttribute("href", url);
        btn.setAttribute("target", "_blank");
        btn.setAttribute("rel", "noopener");
        btn.removeAttribute("data-buy-pending");
        btn.removeAttribute("title");
        addB2bNote(btn);
        // Stato loading sul click (il checkout apre in una nuova scheda)
        btn.addEventListener("click", function () {
          var label = btn.textContent;
          btn.classList.add("is-loading");
          btn.setAttribute("aria-busy", "true");
          btn.textContent = "Apertura checkout…";
          setTimeout(function () {
            btn.classList.remove("is-loading");
            btn.removeAttribute("aria-busy");
            btn.textContent = label;
          }, 2500);
        });
      } else {
        // Nessun Payment Link ancora: fallback alla richiesta preventivo
        btn.setAttribute("href", "#form");
        btn.setAttribute("title", "Checkout in attivazione — richiedi un preventivo");
        btn.addEventListener("click", function () {
          console.warn("[Stripe] Payment Link non configurato per", currentSlug(), "→ fallback al form.");
        });
      }
    });
    wireStripeTrust(url);
  }

  document.addEventListener("DOMContentLoaded", function () {
    wireBuyButtons();
  });
})();
