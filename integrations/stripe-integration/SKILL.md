---
name: stripe-integration
description: Integrate Stripe for payments, subscriptions, invoicing, and billing. Handle checkout sessions, webhooks, customer management, and payment method handling. Use when integrateing stripe for payments, subscriptions, invoicing, and billing. handle checkout.
domain: integrations
tags:
- payments
- stripe
- billing
- subscriptions
- checkout
- webhooks
---

# Stripe Integration

## When to Use
**Trigger phrases:**
- "stripe integration"
- "Integrate Stripe for payments, subscriptions, invoicing, and billing"


- When adding payment processing to an application
- When implementing subscription billing or recurring payments
- When building checkout flows or payment forms
- When handling Stripe webhooks for payment events

## When NOT to Use

- For non-Stripe payment gateways (use their specific skills)
- For simple donation pages (use simpler payment widgets)

## Overview

Full Stripe integration covering payments, subscriptions, invoicing, and billing. Handles checkout sessions, customer portal, webhooks, and error handling.

## Workflow

1. **Install SDK** - `npm install stripe` or `pip install stripe`
2. **Configure** - Set API keys (test + live), webhook endpoints
3. **Build checkout** - Create checkout sessions or payment elements
4. **Handle webhooks** - Process payment events (succeeded, failed, refunded)
5. **Manage customers** - Create, update, attach payment methods
6. **Handle errors** - Declined cards, expired tokens, rate limits

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I will handle payments myself" | PCI compliance is complex - Stripe handles it for you |
| "Webhooks are optional" | Without webhooks, you miss failed payments, refunds, and disputes |
| "Test mode is enough" | Always test with real card numbers in live mode before launch |

## Code Example (Node.js)

```javascript
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

const session = await stripe.checkout.sessions.create({
  mode: 'subscription',
  payment_method_types: ['card'],
  line_items: [{ price: 'price_xxx', quantity: 1 }],
  success_url: 'https://example.com/success',
  cancel_url: 'https://example.com/cancel',
});

app.post('/webhook', express.raw({type: 'application/json'}), (req, res) => {
  const sig = req.headers['stripe-signature'];
  const event = stripe.webhooks.constructEvent(req.body, sig, endpointSecret);
  switch (event.type) {
    case 'invoice.payment_succeeded': break;
    case 'invoice.payment_failed': break;
  }
  res.json({received: true});
});
```


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run stripe integration workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] Checkout session creates successfully
- [ ] Payment processes in test mode
- [ ] Webhooks verify signature correctly
- [ ] Failed payments handled gracefully

