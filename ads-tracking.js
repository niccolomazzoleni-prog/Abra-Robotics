/* Google Ads: gtag, GCLID, conversioni lead e acquisto. */
(function () {
  "use strict";

  var ADS_ID = (window.GOOGLE_ADS_ID || "").trim();
  var LABELS = window.GOOGLE_ADS_LABELS || {};

  function captureGclid() {
    var p = new URLSearchParams(location.search);
    var g = p.get("gclid");
    if (g) {
      try {
        sessionStorage.setItem("abra_gclid", g);
      } catch (_) {}
    }
    return g || (function () {
      try { return sessionStorage.getItem("abra_gclid") || ""; } catch (_) { return ""; }
    })();
  }

  function loadGtag() {
    if (!ADS_ID || window.gtag) return;
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(ADS_ID);
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    window.gtag("config", ADS_ID);
  }

  function conversion(label) {
    if (!ADS_ID || !label || !window.gtag) return;
    window.gtag("event", "conversion", { send_to: ADS_ID + "/" + label });
  }

  window.AbraAds = {
    getGclid: captureGclid,
    trackLead: function () { conversion(LABELS.lead); },
    trackPurchase: function () { conversion(LABELS.purchase); }
  };

  captureGclid();
  loadGtag();

  document.addEventListener("DOMContentLoaded", function () {
    var gclid = captureGclid();
    if (!gclid) return;
    document.querySelectorAll("form").forEach(function (form) {
      if (form.querySelector('input[name="gclid"]')) return;
      var inp = document.createElement("input");
      inp.type = "hidden";
      inp.name = "gclid";
      inp.value = gclid;
      form.appendChild(inp);
    });
  });
})();
