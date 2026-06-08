---
name: ai-saas-builder
description: Takes a problem statement and produces a deployable micro-SaaS product
  — landing page, auth, payments, database, API, and billing
domain: development
---


## Overview

An end-to-end pipeline for shipping micro-SaaS products as a solo operator. Takes a problem statement and produces a fully deployed, monetizable SaaS with landing page, authentication, payment integration, and billing. Designed for one-person companies to ship 2-4 products per month.

## Required Tools

- **CLI**: `npx create-t3-app`, `npx create-next-app`, `railway`, `flyctl`, `vercel`
- **Payments**: Stripe API key or Lemon Squeezy API key
- **Database**: Supabase (PostgreSQL), PlanetScale, or Neon
- **Auth**: Clerk, Auth.js, or Supabase Auth
- **Deployment**: Vercel (frontend), Railway/Fly.io (backend)
- **Environment**: Node.js 18+, npm/pnpm

## Capabilities

- Generate product spec from a one-line problem statement
- Select optimal tech stack based on product type
- Scaffold full-stack project with auth, payments, DB
- Generate landing page with pricing tiers
- Integrate Stripe Checkout or Lemon Squeezy for payments
- Deploy to production with CI/CD
- Generate launch checklist (Product Hunt, Twitter, IndieHackers)

## When to Use

- You have a business idea and want to ship a working product fast
- You need to validate a market before investing weeks of development
- You want to build a portfolio of micro-SaaS products for passive income
- A client requests a custom SaaS solution

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The ai-saas-builder workflow follows a standard pipeline pattern.

Core flow:
```
# ai-saas-builder primary flow
input = prepare(raw_data)
result = process(input, config={auth, billing, builder, database, deployable})
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


### Phase 1: Spec Generation

```bash
# Input: problem statement
# Output: structured spec

cat << 'SPEC' > spec.md
# {product_name}

## Problem
{one_sentence_problem}

## Solution
{one_sentence_solution}

## Target User
{user_persona}

## Core Features (MVP)
1. {feature_1} - must have
2. {feature_2} - must have
3. {feature_3} - nice to have

## Monetization
- Free tier: {limits}
- Pro: ${price}/mo
- Enterprise: custom

## Tech Stack
- Frontend: {framework}
- Backend: {api_type}
- Database: {db}
- Auth: {auth_provider}
- Payments: {payment_provider}
- Hosting: {platform}
SPEC
```

### Phase 2: Tech Stack Selection

```python
def select_stack(product_type, requirements):
    """Select optimal stack based on product characteristics."""

    stacks = {
        "crud_app": {
            "framework": "Next.js 14 (App Router)",
            "api": "tRPC or Next.js API Routes",
            "db": "Supabase (PostgreSQL)",
            "auth": "Clerk",
            "payments": "Stripe Checkout",
            "hosting": "Vercel"
        },
        "ai_app": {
            "framework": "Next.js 14",
            "api": "Next.js API Routes + streaming",
            "db": "Supabase + pgvector",
            "auth": "Clerk",
            "payments": "Lemon Squeezy",
            "hosting": "Vercel"
        },
        "marketplace": {
            "framework": "Next.js 14",
            "api": "tRPC",
            "db": "Supabase",
            "auth": "Supabase Auth",
            "payments": "Stripe Connect",
            "hosting": "Vercel"
        },
        "api_product": {
            "framework": "None (API only)",
            "api": "Hono or Fastify",
            "db": "PlanetScale (MySQL)",
            "auth": "API keys + JWT",
            "payments": "Stripe metered billing",
            "hosting": "Fly.io or Railway"
        }
    }

    return stacks.get(product_type, stacks["crud_app"])
```

### Phase 3: Scaffolding

```bash
# Create Next.js project with T3 stack
npx create-t3-app@latest my-saas --tailwind --trpc --prisma --nextAuth

# Or with Supabase
npx create-next-app@latest my-saas --typescript --tailwind --app
cd my-saas
npx supabase init

# Install core dependencies
pnpm add stripe @stripe/stripe-js  # or lemon-squeezy
pnpm add @clerk/nextjs  # or next-auth
pnpm add zod react-hook-form @tanstack/react-query

# Project structure
my-saas/
├── src/
│   ├── app/
│   │   ├── (marketing)/     # Landing page
│   │   ├── (app)/           # Dashboard
│   │   ├── api/             # API routes
│   │   └── layout.tsx
│   ├── components/
│   │   ├── ui/              # Shadcn/ui components
│   │   ├── landing/         # Landing page sections
│   │   └── billing/         # Pricing, checkout
│   ├── lib/
│   │   ├── stripe.ts        # Stripe client
│   │   ├── db.ts            # Database client
│   │   └── auth.ts          # Auth config
│   └── server/
│       ├── routers/         # tRPC routers
│       └── stripe-webhook.ts
├── prisma/
│   └── schema.prisma
└── .env.local
```

### Phase 4: Payment Integration

```typescript
// Stripe Checkout integration
// src/app/api/checkout/route.ts

import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export async function POST(req: Request) {
  const { priceId } = await req.json();

  const session = await stripe.checkout.sessions.create({
    mode: 'subscription',
    payment_method_types: ['card'],
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${process.env.NEXT_PUBLIC_URL}/dashboard?success=true`,
    cancel_url: `${process.env.NEXT_PUBLIC_URL}/pricing`,
  });

  return Response.json({ url: session.url });
}

// Stripe Webhook for subscription events
// src/app/api/webhooks/stripe/route.ts

export async function POST(req: Request) {
  const body = await req.text();
  const sig = req.headers.get('stripe-signature')!;
  const event = stripe.webhooks.constructEvent(body, sig, webhookSecret);

  switch (event.type) {
    case 'checkout.session.completed':
      // Create/update user subscription in DB
      await db.subscription.create({
        data: {
          userId: event.data.object.metadata.userId,
          stripeCustomerId: event.data.object.customer,
          stripeSubscriptionId: event.data.object.subscription,
          status: 'active',
        }
      });
      break;
    case 'customer.subscription.deleted':
      // Mark subscription as cancelled
      await db.subscription.update({
        where: { stripeSubscriptionId: event.data.object.id },
        data: { status: 'cancelled' }
      });
      break;
  }

  return Response.json({ received: true });
}
```

### Phase 5: Deploy

```bash
# Vercel deployment
npx vercel --prod

# Or Railway
railway login
railway init
railway up

# Or Fly.io
flyctl launch
flyctl deploy

# Environment variables (set in platform dashboard)
# STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET
# NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY
# DATABASE_URL, NEXTAUTH_SECRET
# NEXT_PUBLIC_URL
```

### Phase 6: Launch Checklist

```markdown
## Launch Checklist
- [ ] Landing page live with pricing
- [ ] Stripe/Lemon Squeezy checkout working
- [ ] Webhook handling subscription events
- [ ] Auth flow (signup, login, logout)
- [ ] Dashboard with core feature
- [ ] Error pages (404, 500)
- [ ] SEO meta tags + OG image
- [ ] Analytics (Plausible/PostHog)
- [ ] Submit to Product Hunt
- [ ] Post on Twitter/X with demo
- [ ] Post on IndieHackers
- [ ] Submit to relevant directories
- [ ] Set up customer support (Crisp/Intercom)
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| Stripe webhook 400 | Signature mismatch | Verify `STRIPE_WEBHOOK_SECRET` matches Stripe dashboard |
| Auth callback fails | Wrong redirect URI | Check `NEXTAUTH_URL` or Clerk allowed redirects |
| DB connection timeout | Connection pool exhausted | Use Supabase connection pooler (port 6543) |
| Deploy fails | Missing env vars | Check all required env vars are set in platform |
| Payment succeeds but no access | Webhook not firing | Test with `stripe listen --forward-to localhost` |

## Common Patterns

Proven patterns for ai-saas-builder usage.

- **Batch processing**: Process multiple items in parallel for throughput
- **Retry with backoff**: Handle transient failures gracefully
- **Rate limiting**: Respect API limits with configurable delays
- **Logging**: Structured logging for debugging and audit trails


### Freemium with Usage Limits
```typescript
// Check usage before allowing action
const usage = await db.usage.findUnique({ where: { userId } });
if (usage.count >= FREE_TIER_LIMIT) {
  throw new TRPCError({ code: 'FORBIDDEN', message: 'Upgrade to Pro' });
}
```

### Multi-Tenant SaaS
```typescript
// Organization-based access control
const org = await db.organization.findUnique({
  where: { id: input.orgId },
  include: { members: { where: { userId: session.user.id } } }
});
if (!org.members.length) throw new TRPCError({ code: 'FORBIDDEN' });
```

### Landing Page Template
- Hero section with problem/solution
- Feature grid (3-6 features)
- Pricing table (Free/Pro/Enterprise)
- Social proof (testimonials, logos)
- CTA with email capture
- FAQ section

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
