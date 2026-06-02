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

  function wireBuyButtons() {
    var links = (window.STRIPE_PAYMENT_LINKS || {});
    var url = links[currentSlug()] || "";
    var buyBtns = document.querySelectorAll(".buy-btn");
    buyBtns.forEach(function (btn) {
      if (url) {
        // Payment Link configurato: checkout reale
        btn.setAttribute("href", url);
        btn.setAttribute("target", "_blank");
        btn.setAttribute("rel", "noopener");
        btn.removeAttribute("data-buy-pending");
      } else {
        // Nessun Payment Link ancora: fallback a richiesta preventivo
        btn.setAttribute("href", "#form");
        btn.setAttribute("title", "Checkout in attivazione — richiedi un preventivo");
      }
    });
  }

  // ── 2. Form "Richiedi informazioni" (box in alto) ───────────────────────────
  // Stesso endpoint del form principale del sito (configura GOOGLE_SCRIPT_URL).
  var GOOGLE_SCRIPT_URL = (window.GOOGLE_SCRIPT_URL || "INSERISCI_QUI_IL_TUO_URL_APPS_SCRIPT");

  function wireQuoteForms() {
    document.querySelectorAll(".quote-form-top").forEach(function (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var btn = form.querySelector("button[type=submit]");
        var fb = form.querySelector(".quote-form-feedback");
        var original = btn ? btn.textContent : "";
        if (btn) { btn.disabled = true; btn.textContent = "Invio..."; }
        if (fb) { fb.className = "quote-form-feedback"; fb.textContent = ""; }

        var payload = Object.fromEntries(new FormData(form).entries());
        payload.prodotto = form.getAttribute("data-product") || document.title;

        fetch(GOOGLE_SCRIPT_URL, {
          method: "POST",
          mode: "no-cors",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        }).then(function () {
          if (fb) { fb.className = "quote-form-feedback success"; fb.textContent = "Richiesta inviata! Ti ricontattiamo entro 12 ore."; }
          form.reset();
        }).catch(function () {
          if (fb) { fb.className = "quote-form-feedback error"; fb.textContent = "Errore. Scrivi a info@abrarobotics.com."; }
        }).finally(function () {
          if (btn) { btn.disabled = false; btn.textContent = original; }
        });
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    wireBuyButtons();
    wireQuoteForms();
  });
})();
