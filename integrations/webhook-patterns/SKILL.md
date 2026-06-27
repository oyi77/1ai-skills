---
name: webhook-patterns
description: Webhook design and handling — signature verification, retry logic, idempotency, event routing, testing
domain: integrations
tags:
- api
- integrations
- patterns
- testing
- third-party
- webhook
---

## Overview

Design, implement, and consume webhooks — secure signature verification, idempotent processing, retry handling, event routing, and testing strategies.

## Capabilities

- Webhook endpoint design (Express, Fastify, serverless)
- HMAC signature verification (Stripe, GitHub, Shopify)
- Idempotent event processing
- Retry and dead letter handling
- Event routing and filtering
- Testing with ngrok and webhook.site

## When to Use

- Receiving real-time events from SaaS platforms
- Building event-driven integrations between systems
- Processing payment confirmations (Stripe, Paddle)
- Handling CI/CD events (GitHub, GitLab)
- Building notification and alerting systems

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code
```python
# Example workflow for this skill
def execute(input_data):
    # Step 1: Validate input
    if not input_data:
        raise ValueError("Input data is required")

    # Step 2: Process core logic
    result = process(input_data)

    # Step 3: Validate output
    validate_output(result)

    return result
```


### Express Webhook Endpoint

```javascript
const express = require("express");
const crypto = require("crypto");

const app = express();

// Raw body for signature verification
app.post("/webhooks/stripe", express.raw({ type: "application/json" }), (req, res) => {
  const sig = req.headers["stripe-signature"];
  const secret = process.env.STRIPE_WEBHOOK_SECRET;

  // Verify signature
  const expected = crypto.createHmac("sha256", secret).update(req.body).digest("hex");
  if (!crypto.timingSafeEqual(Buffer.from(sig), Buffer.from(expected))) {
    return res.status(401).send("Invalid signature");
  }

  const event = JSON.parse(req.body);

  // Idempotency check
  if (processedEvents.has(event.id)) {
    return res.status(200).send("Already processed");
  }

  // Route event
  switch (event.type) {
    case "payment_intent.succeeded":
      handlePayment(event.data.object);
      break;
    case "customer.subscription.deleted":
      handleCancellation(event.data.object);
      break;
  }

  processedEvents.add(event.id);
  res.status(200).send("OK");
});
```

### GitHub Webhook Verification

```javascript
function verifyGitHub(req, res, next) {
  const signature = req.headers["x-hub-signature-256"];
  const secret = process.env.GITHUB_WEBHOOK_SECRET;
  const hmac = crypto.createHmac("sha256", secret);
  const digest = "sha256=" + hmac.update(req.rawBody).digest("hex");

  if (!crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(digest))) {
    return res.status(401).send("Invalid signature");
  }
  next();
}

app.post("/webhooks/github", verifyGitHub, (req, res) => {
  const event = req.headers["x-github-event"];
  const payload = req.body;

  if (event === "push") {
    handlePush(payload);
  } else if (event === "pull_request") {
    handlePR(payload);
  }

  res.status(200).send("OK");
});
```

### Retry Handler (Consumer Side)

```javascript
async function processWithRetry(event, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      await processEvent(event);
      return;
    } catch (err) {
      if (i === maxRetries - 1) {
        await deadLetterQueue.publish(event);
        console.error(`Failed after ${maxRetries} retries:`, err);
      }
      await sleep(Math.pow(2, i) * 1000); // Exponential backoff
    }
  }
}
```

### Testing with ngrok

```bash
# Expose local server
ngrok http 3000

# Use the ngrok URL as webhook endpoint
# https://abc123.ngrok.io/webhooks/stripe
```

## Common Patterns

- **Signature Verification**: Always verify HMAC before processing
- **Idempotency**: Track processed event IDs to avoid duplicates
- **Async Processing**: Return 200 immediately, process in background
- **Dead Letter Queue**: Store failed events for manual review
- **Event Routing**: Route by event type to dedicated handlers
- **Webhook Testing**: Use ngrok/webhook.site for local development

## How to Use

1. Invoke the skill when relevant domain keywords appear in the request
2. Provide required inputs as specified in the skill definition
3. Review the output for correctness before delivering to the user
4. Combine with related skills for complex multi-step workflows

## Verification

After completing this skill, confirm:

- [ ] Output meets the defined quality and completeness requirements
- [ ] All prerequisites are verified and documented
- [ ] Error handling covers edge cases
- [ ] Results are accurate and actionable

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I will handle auth later" | Retrofitting auth is 10x harder. Build it from day one. |
| "APIs do not change" | APIs change. Version your integrations and handle deprecations. |
| "Webhooks are optional" | Without webhooks, you miss real-time events. They are essential. |