---
name: payment-gateways
description: Payment gateway integration — Stripe, Paddle, Lemon Squeezy, dunning, subscription management
---

## Overview

Integrate payment gateways for SaaS billing — Stripe, Paddle, Lemon Squeezy. Handle checkout, webhooks, subscriptions, dunning, tax compliance.

## Capabilities

- Stripe Checkout and Payment Intents
- Paddle and Lemon Squeezy integration
- Subscription lifecycle (create, upgrade, cancel)
- Webhook handling for payment events
- Dunning (failed payment recovery)
- Tax calculation and compliance
- Invoice generation and management

## When to Use

- Building SaaS billing systems
- Implementing subscription management
- Processing one-time payments
- Handling international tax (VAT, GST)
- Recovering failed payments (dunning)

## When NOT to Use

- Task is about payment processing, not gateway integration
- You need to handle disputes or chargebacks (use dispute tools)
- Task requires PCI DSS compliance (use compliance tools)
- You're building a payment processor, not integrating one
- Task is about accounting, not payment collection
- You need to handle crypto payments (use crypto tools)

## Pseudo Code

Implementation patterns for common use cases with this skill.


### Stripe Checkout Session

```javascript
import Stripe from 'stripe'
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY)

const session = await stripe.checkout.sessions.create({
  mode: 'subscription',
  payment_method_types: ['card'],
  line_items: [{ price: 'price_xxx', quantity: 1 }],
  success_url: 'https://app.com/success?session_id={CHECKOUT_SESSION_ID}',
  cancel_url: 'https://app.com/cancel',
  customer_email: user.email,
})

res.redirect(303, session.url)
```

### Stripe Webhook Handler

```javascript
app.post('/webhooks/stripe', express.raw({ type: 'application/json' }), (req, res) => {
  const sig = req.headers['stripe-signature']
  const event = stripe.webhooks.constructEvent(req.body, sig, process.env.STRIPE_WEBHOOK_SECRET)

  switch (event.type) {
    case 'checkout.session.completed':
      handleCheckoutCompleted(event.data.object)
      break
    case 'invoice.payment_failed':
      handlePaymentFailed(event.data.object)
      break
    case 'customer.subscription.deleted':
      handleSubscriptionCanceled(event.data.object)
      break
  }

  res.json({ received: true })
})
```

### Subscription Management

```javascript
// Create subscription
const subscription = await stripe.subscriptions.create({
  customer: customerId,
  items: [{ price: 'price_xxx' }],
  payment_behavior: 'default_incomplete',
  expand: ['latest_invoice.payment_intent'],
})

// Upgrade subscription
await stripe.subscriptions.update(subscriptionId, {
  items: [{ id: itemId, price: 'price_new' }],
  proration_behavior: 'always_invoice',
})

// Cancel subscription
await stripe.subscriptions.update(subscriptionId, {
  cancel_at_period_end: true,
})
```

### Lemon Squeezy Integration

```javascript
// Create checkout
const checkout = await fetch('https://api.lemonsqueezy.com/v1/checkouts', {
  method: 'POST',
  headers: {
    Authorization: `Bearer ${process.env.LEMON_SQUEEZY_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    data: {
      type: 'checkouts',
      attributes: {
        product_id: 12345,
        checkout_data: { email: user.email },
      },
    },
  }),
})
```

### Dunning (Failed Payment Recovery)

```javascript
// Handle failed payment
case 'invoice.payment_failed':
  const customer = event.data.customer
  const attempt = event.data.attempt_count

  if (attempt === 1) {
    sendEmail(customer, 'payment-failed-first')
  } else if (attempt === 3) {
    sendEmail(customer, 'payment-failed-final', { gracePeriod: '3 days' })
  } else if (attempt >= 4) {
    await stripe.subscriptions.update(subscriptionId, { pause_collection: true })
  }
```

## Common Patterns

- **Webhook-first**: Always process events via webhooks, not polling
- **Idempotency**: Use idempotency keys for payment operations
- **Proration**: Handle subscription upgrades with proration
- **Tax compliance**: Use Stripe Tax or Paddle for automatic tax
- **Grace period**: Allow 3-7 days before suspending on failed payment

## Red Flags

- Storing payment card data directly
- Not using PCI-compliant processors
- Missing fraud detection
- Not handling payment failures properly
- Ignoring payment security best practices

## Verification

- [ ] Payment card data is not stored
- [ ] PCI-compliant processors are used
- [ ] Fraud detection is in place
- [ ] Payment failures are handled
- [ ] Security best practices are followed