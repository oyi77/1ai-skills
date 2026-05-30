---
name: payment-integration
description: Payment platform integration — Stripe, Paddle, Lemon Squeezy. Checkout flows, subscriptions, webhooks, billing management
---


## Overview

Payment integration patterns for Stripe, Paddle, and Lemon Squeezy. Covers checkout sessions, subscription management, webhook handling, invoicing, and billing portal setup.

## Capabilities

- Stripe checkout session creation
- Subscription lifecycle (create, upgrade, cancel, renew)
- Webhook signature verification and event handling
- Paddle and Lemon Squeezy integration
- Invoice generation and payment receipts
- Customer portal for self-service billing

## When to Use

- Adding payments to a SaaS product
- Implementing subscription billing
- Handling payment webhooks securely
- Building a billing portal

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The payment-integration workflow follows a standard pipeline pattern.

Core flow:
```
# payment-integration primary flow
input = prepare(raw_data)
result = process(input, config={billing, checkout, flows, integration, lemon})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Stripe checkout session
```typescript
import Stripe from 'stripe';
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

// Create checkout session
const session = await stripe.checkout.sessions.create({
  mode: 'subscription',
  customer: user.stripeCustomerId,
  line_items: [{ price: 'price_pro_monthly', quantity: 1 }],
  success_url: `${BASE_URL}/billing/success?session_id={CHECKOUT_SESSION_ID}`,
  cancel_url: `${BASE_URL}/billing/cancel`,
  metadata: { userId: user.id }
});

return { url: session.url };
```

### Webhook handler
```typescript
import Stripe from 'stripe';

app.post('/webhooks/stripe', express.raw({ type: 'application/json' }), async (req, res) => {
  const sig = req.headers['stripe-signature']!;
  let event: Stripe.Event;

  try {
    event = stripe.webhooks.constructEvent(req.body, sig, process.env.STRIPE_WEBHOOK_SECRET!);
  } catch (err) {
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  switch (event.type) {
    case 'checkout.session.completed':
      await handleCheckoutCompleted(event.data.object);
      break;
    case 'customer.subscription.updated':
      await handleSubscriptionUpdated(event.data.object);
      break;
    case 'customer.subscription.deleted':
      await handleSubscriptionCanceled(event.data.object);
      break;
    case 'invoice.payment_failed':
      await handlePaymentFailed(event.data.object);
      break;
  }

  res.json({ received: true });
});
```

### Paddle integration
```typescript
import { Paddle } from '@paddle/paddle-node-sdk';

const paddle = new Paddle({ apiKey: process.env.PADDLE_API_KEY! });

// Create subscription
const transaction = await paddle.transactions.create({
  items: [{ priceId: 'pri_pro_monthly', quantity: 1 }],
  customerId: user.paddleCustomerId
});

// Webhook verification
app.post('/webhooks/paddle', async (req, res) => {
  const signature = req.headers['paddle-signature']!;
  const event = await paddle.webhooks.unmarshal(req.body, signature);

  switch (event.eventType) {
    case 'subscription.created': break;
    case 'subscription.updated': break;
    case 'transaction.completed': break;
  }

  res.json({ ok: true });
});
```

### Lemon Squeezy integration
```typescript
import { LemonSqueezy } from '@lemonsqueezy/lemonsqueezy.js';

const ls = new LemonSqueezy({ apiKey: process.env.LEMONSQUEEZY_API_KEY! });

// Create checkout
const checkout = await ls.createCheckout({
  storeId: process.env.LEMONSQUEEZY_STORE_ID!,
  variantId: 'variant_pro_monthly',
  customData: { userId: user.id }
});

// Webhook verification
app.post('/webhooks/lemonsqueezy', async (req, res) => {
  const secret = process.env.LEMONSQUEEZY_WEBHOOK_SECRET!;
  const signature = req.headers['x-signature']!;
  const event = ls.webhooks.verify(req.body, signature, secret);

  switch (event.meta.event_name) {
    case 'subscription_created': break;
    case 'subscription_payment_success': break;
    case 'subscription_cancelled': break;
  }

  res.json({ ok: true });
});
```

## Common Patterns

- **Customer portal**: Stripe Billing Portal for self-service management
- **Trial periods**: `subscription_data: { trial_period_days: 14 }`
- **Prorations**: Handle mid-cycle upgrades with proration
- **Idempotency**: Use `idempotency_key` for retry-safe requests
- **Webhook retries**: Always return 2xx quickly, process async

## How to Use

1. Understand the requirement and existing codebase patterns
2. Design the solution with error handling and testability in mind
3. Implement incrementally with tests for each change
4. Verify against expected outcomes (manual and automated)
5. Document usage, edge cases, and integration points
6. Review with team before merging to shared branches

## Red Flags

- **Skipping tests to ship faster**: Untested code breaks in production when you least expect it
- **No error handling in production code**: Unhandled errors crash services and lose user data
- **Hardcoded configuration values**: Hardcoded values prevent environment switching and leak secrets
- **Ignoring security implications**: Missing input validation, auth bypasses, and injection vulnerabilities
- **Over-engineering simple solutions**: Premature abstraction adds complexity without proportional benefit
