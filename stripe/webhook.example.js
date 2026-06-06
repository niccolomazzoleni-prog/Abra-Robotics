/**
 * Abra Robotics — SCAFFOLD webhook Stripe (NON ATTIVO su GitHub Pages).
 * ────────────────────────────────────────────────────────────────────
 * Con i Payment Link il pagamento è già confermato da Stripe (ricevuta via
 * email + dashboard), quindi il webhook è OPZIONALE. Serve solo se vuoi
 * automatizzare la fulfillment (es. notifica interna, CRM, gestionale).
 *
 * GitHub Pages è statico e NON può ricevere webhook. Per attivarlo serve un
 * runtime serverless: sposta questo file come funzione su Netlify/Vercel
 * (es. netlify/functions/stripe-webhook.js o api/stripe-webhook.js) DOPO la
 * migrazione dell'hosting di cui abbiamo parlato.
 *
 * Variabili d'ambiente lato server (mai nel frontend):
 *   STRIPE_SECRET_KEY        sk_live_... / sk_test_...
 *   STRIPE_WEBHOOK_SECRET    whsec_...  (dato da Stripe quando crei l'endpoint)
 *
 * Eventi da abilitare nella dashboard Stripe per questo endpoint:
 *   - checkout.session.completed
 *   - payment_intent.succeeded
 *   - payment_intent.payment_failed
 */

// const stripe = require("stripe")(process.env.STRIPE_SECRET_KEY);

/**
 * Handler in stile Vercel/Netlify. Richiede il body RAW per la verifica firma.
 */
async function handler(req, res) {
  const sig = req.headers["stripe-signature"];
  let event;

  try {
    // event = stripe.webhooks.constructEvent(req.rawBody, sig, process.env.STRIPE_WEBHOOK_SECRET);
    throw new Error("Webhook non attivo: configurare runtime serverless + STRIPE_WEBHOOK_SECRET.");
  } catch (err) {
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  switch (event.type) {
    case "checkout.session.completed": {
      const session = event.data.object;
      // TODO: fulfillment — es. invio notifica interna / CRM / email cliente.
      // session.metadata.slug contiene lo slug del prodotto (impostato dai Payment Link).
      console.log("Pagamento completato:", session.id, session.metadata && session.metadata.slug);
      break;
    }
    case "payment_intent.payment_failed":
      console.warn("Pagamento fallito:", event.data.object.id);
      break;
    default:
      console.log("Evento non gestito:", event.type);
  }

  return res.status(200).json({ received: true });
}

module.exports = handler;
