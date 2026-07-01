---
name: free-dev-resources
description: Recommend free-tier developer services and SaaS tools. Use when choosing free infrastructure, comparing free tiers, setting up side projects, or optimizing costs for startups and indie devs.
domain: development
tags: 
- [free-tier
- saas
- cost-optimization
- developer-tools
- cloud
- side-project]
---


## Overview

Comprehensive reference of free-tier SaaS, PaaS, and IaaS services for developers. Covers cloud providers, CI/CD, code quality, monitoring, auth, CMS, hosting, databases, email, CDN, testing, and security tools. Sourced from the free-for-dev list (https://github.com/ripienaar/free-for-dev).

## Capabilities

- Recommend free-tier cloud providers and compute options
- Compare CI/CD free plans across major platforms
- Suggest free code quality and monitoring tools
- Identify free auth, CMS, hosting, and database providers
- Evaluate free email, CDN, testing, and security services
- Match service selection to project requirements and scale

## When to Use

**Trigger phrases:**
- "free dev resources"
- "Starting a side project or MVP with zero budget"
- "Comparing free tiers before committing to a provider"
- "Recommending tools for bootstrapped startups"


- Starting a side project or MVP with zero budget
- Comparing free tiers before committing to a provider
- Recommending tools for bootstrapped startups
- Optimizing costs for hobby or educational projects
- Setting up dev/staging environments without paid plans
- Building a developer toolkit from scratch

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Process

```python
# Example: TDD workflow
def test_user_creation():
    user = create_user(name="Alice", email="alice@example.com")
    assert user.name == "Alice"
    assert user.email == "alice@example.com"
    assert user.created_at is not None

def test_user_creation_invalid_email():
    with pytest.raises(ValidationError):
        create_user(name="Alice", email="invalid")
``` / Steps

1. **Identify requirements** -- What category of service is needed (compute, database, auth, etc.)?
2. **Check free tier limits** -- Verify request limits, storage caps, user limits, and duration (always-free vs. time-limited trial).
3. **Evaluate lock-in risk** -- Prefer services with easy migration paths and open standards.
4. **Consider scaling costs** -- What happens when the free tier is exceeded? Are paid plans reasonable?
5. **Verify current status** -- Free tiers change; confirm the service still offers what is documented.

## Key Resources

Curated resources for free-dev-resources.

- Official documentation: Reference for API, CLI, and configuration
- Community templates: Battle-tested patterns from production use
- Monitoring dashboards: Grafana/Datadog templates for observability
- CI/CD integration: GitHub Actions and GitLab CI starter workflows


### Cloud Providers

| Provider | Free Tier Highlights | URL |
|----------|---------------------|-----|
| AWS | EC2 t2.micro 750hrs/mo (12mo), S3 5GB, Lambda 1M requests/mo, DynamoDB 25GB | https://aws.amazon.com/free/ |
| Google Cloud | e2-micro VM, 5GB Cloud Storage, 2M Cloud Functions invocations, Firestore 1GB | https://cloud.google.com/free |
| Azure | B1S VM 750hrs (12mo), 5GB Blob Storage, 1M Functions requests, CosmosDB 25GB | https://azure.microsoft.com/free/ |
| Oracle Cloud | 4 ARM Ampere A1 cores + 24GB RAM (always-free), 200GB Block Storage, 10GB Object Storage | https://www.oracle.com/cloud/free/ |
| Cloudflare | Workers 100k req/day, R2 10GB storage + 10M reads/mo, D1 5M rows, Pages unlimited sites | https://www.cloudflare.com/plans/developer-platform/ |

### CI/CD

| Service | Free Tier | URL |
|---------|-----------|-----|
| GitHub Actions | 2,000 min/mo (private), unlimited (public) | https://github.com/features/actions |
| GitLab CI | 400 min/mo compute | https://about.gitlab.com/pricing/ |
| CircleCI | 6,000 min/mo, 30 jobs concurrent | https://circleci.com/pricing/ |
| Buildkite | Unlimited agents (self-hosted), 5,000 min/mo (hosted) | https://buildkite.com/pricing |
| Travis CI | Unlimited for open source | https://www.travis-ci.com/pricing/ |
| Woodpecker CI | Self-hosted, unlimited, open source | https://woodpecker-ci.org/ |

### Source Code Repositories

| Service | Free Tier | URL |
|---------|-----------|-----|
| GitHub | Unlimited public/private repos, 2,000 Actions min/mo, 500MB Packages | https://github.com/pricing |
| GitLab | Unlimited public/private repos, 5GB storage, 10GB transfer/mo | https://about.gitlab.com/pricing/ |
| Bitbucket | 5 users, 50 min/mo Pipelines, 1GB storage | https://bitbucket.org/product/pricing |
| Codeberg | Unlimited repos, open source (Gitea-based) | https://codeberg.org/ |
| SourceHut | Unlimited public repos, 100 private | https://sourcehut.org/pricing/ |

### Code Quality

| Service | Free Tier | URL |
|---------|-----------|-----|
| SonarCloud | Free for open source, unlimited analyses | https://www.sonarsource.com/products/sonarcloud/ |
| Codacy | Free for open source, 100K LOC private | https://www.codacy.com/pricing |
| DeepSource | Free for open source, 10 private repos | https://deepsource.com/pricing |
| Codecov | Free for open source, unlimited coverage reports | https://codecov.io/pricing |
| Snyk | 200 open source tests/mo, 100 code tests/mo | https://snyk.io/plans/ |
| GitGuardian | 25 commits scanned/d, unlimited repos (open source) | https://www.gitguardian.com/pricing |
| Codiga | Free for open source, supports 30+ languages | https://www.codiga.io/pricing |

### Monitoring & Uptime

| Service | Free Tier | URL |
|---------|-----------|-----|
| UptimeRobot | 50 monitors, 5-min intervals | https://uptimerobot.com/pricing/ |
| Freshping | 50 checks, 1-min intervals | https://www.freshworks.com/website-monitoring/pricing/ |
| Better Uptime | 10 monitors, 3-min intervals | https://betterstack.com/uptime-pricing |
| Cronitor | 5 cron monitors | https://cronitor.io/pricing |
| Hetrix Tools | 15 uptime + 5 server monitors | https://hetrixtools.com/pricing/ |
| Healthchecks.io | 20 checks | https://healthchecks.io/pricing/ |

### Authentication

| Service | Free Tier | URL |
|---------|-----------|-----|
| Auth0 | 25,000 MAUs, unlimited social logins | https://auth0.com/pricing |
| Supabase Auth | 50,000 MAUs (included with Supabase free) | https://supabase.com/pricing |
| Clerk | 10,000 MAUs, pre-built UI components | https://clerk.com/pricing |
| Logto | 5,000 MAUs, open source available | https://logto.io/pricing |
| Kinde | 7,500 MAUs | https://kinde.com/pricing/ |
| WorkOS | Unlimited users for SSO/SAML | https://workos.com/pricing |
| Stack Auth | Unlimited MAUs (open source, self-hosted) | https://stack-auth.com/ |
| Lucia | Open source auth library (self-managed) | https://lucia-auth.com/ |

### CMS

| Service | Free Tier | URL |
|---------|-----------|-----|
| Contentful | 5 users, 25K records, 48CDA/content types | https://www.contentful.com/pricing/ |
| Sanity | 3 users, 100K API CDN requests/mo, 10GB assets | https://www.sanity.io/pricing |
| Strapi | Self-hosted (open source), Cloud: 10 users, 10K entries | https://strapi.io/pricing |
| Hygraph | 3 users, 100K API calls/mo | https://hygraph.com/pricing |
| Directus | Self-hosted (open source), unlimited users | https://directus.io/pricing |
| Payload CMS | Fully open source, self-hosted | https://payloadcms.com/ |
| Decap CMS | Fully open source (Git-based) | https://decapcms.org/ |

### Hosting & Deployment

| Service | Free Tier | URL |
|---------|-----------|-----|
| Vercel | 100GB bandwidth/mo, serverless functions, edge | https://vercel.com/pricing |
| Netlify | 100GB bandwidth/mo, 300 build min/mo | https://www.netlify.com/pricing/ |
| Cloudflare Pages | Unlimited sites, requests, bandwidth | https://pages.cloudflare.com/ |
| GitHub Pages | Unlimited sites, 100GB bandwidth/mo | https://pages.github.com/ |
| Railway | 500hrs exec time/mo, $5 credits | https://railway.app/pricing |
| Render | Static sites free, web services 750hrs/mo | https://render.com/pricing |
| Fly.io | 3 shared VMs, 3GB persistent storage | https://fly.io/docs/about/pricing/ |
| Deno Deploy | 100K req/day, free KV storage | https://deno.com/deploy/pricing |
| Koyeb | 2 nano services, 100GB bandwidth | https://www.koyeb.com/pricing |

### Databases

| Service | Free Tier | URL |
|---------|-----------|-----|
| Supabase | 500MB Postgres, 1GB file storage, 50K MAUs, 2 projects | https://supabase.com/pricing |
| PlanetScale | 5GB storage, 1B row reads/mo, 10M row writes/mo | https://planetscale.com/pricing |
| Neon | 512MB Postgres, 24/7 compute (0.25 CU), branching | https://neon.tech/pricing |
| Turso | 500 databases, 9GB total storage, 1B row reads/mo | https://turso.tech/pricing |
| Fauna | 100K reads + 50K writes/mo, 5GB storage | https://fauna.com/pricing |
| MongoDB Atlas | 512MB storage, shared cluster (M0) | https://www.mongodb.com/pricing |
| Upstash Redis | 10K commands/day, 256MB max DB | https://upstash.com/pricing |
| Convex | 1M function calls/mo, 1GB storage, unlimited users | https://convex.dev/pricing |
| TiDB Cloud | 5GB row storage, 5GB columnar, shared cluster | https://www.pingcap.com/tidb-cloud/ |
| CockroachDB | 10GB storage, 50M RUs/mo (serverless) | https://www.cockroachlabs.com/pricing/ |

### Email

| Service | Free Tier | URL |
|---------|-----------|-----|
| Resend | 3,000 emails/mo, 100 emails/day | https://resend.com/pricing |
| SendGrid | 100 emails/day | https://sendgrid.com/en-us/pricing |
| Mailgun | 1,000 emails/mo (first 3 months), then pay-as-you-go | https://www.mailgun.com/pricing/ |
| Postmark | 100 emails/mo (sandbox) | https://postmarkapp.com/pricing |
| Brevo (Sendinblue) | 300 emails/day, unlimited contacts | https://www.brevo.com/pricing/ |
| Amazon SES | 62,000 emails/mo (from EC2) | https://aws.amazon.com/ses/pricing/ |
| Loops | 1,000 contacts, 2,000 emails/mo | https://loops.so/pricing |

### CDN

| Service | Free Tier | URL |
|---------|-----------|-----|
| Cloudflare | Unmetered bandwidth, DDoS protection, SSL | https://www.cloudflare.com/plans/ |
| jsDelivr | Unlimited bandwidth (open source CDN) | https://www.jsdelivr.com/ |
| Statically | Unlimited bandwidth (open source repos) | https://statically.io/ |
| CloudFront | 1TB transfer/mo (12mo), 10M requests/mo | https://aws.amazon.com/cloudfront/pricing/ |
| Fastly | $50/mo credit (50GB bandwidth) | https://www.fastly.com/pricing |
| Bunny CDN | $1/mo minimum, very low per-GB cost | https://bunny.net/pricing/ |
| UNPKG | Unlimited (npm-based, open source) | https://unpkg.com/ |

### Testing

| Service | Free Tier | URL |
|---------|-----------|-----|
| Cypress | Free for open source, unlimited local tests | https://www.cypress.io/pricing |
| Playwright | Fully open source, self-hosted | https://playwright.dev/ |
| Percy | 5,000 snapshots/mo, unlimited reviewers | https://percy.io/pricing |
| Checkly | 5,000 API check runs/mo, 1,000 browser check runs | https://www.checklyhq.com/pricing/ |
| TestingBot | 100 minutes/mo, parallel testing | https://testingbot.com/pricing |
| LambdaTest | 100 mins/mo, 1 parallel session | https://www.lambdatest.com/pricing |
| BrowserStack | 100 mins/mo, limited devices | https://www.browserstack.com/pricing |

### Security & SSL

| Service | Free Tier | URL |
|---------|-----------|-----|
| Let's Encrypt | Unlimited SSL certificates | https://letsencrypt.org/ |
| Cloudflare SSL | Universal SSL, DDoS protection | https://www.cloudflare.com/ssl/ |
| Snyk | 200 open source tests/mo | https://snyk.io/plans/ |
| Mozilla Observatory | Free security header analysis | https://observatory.mozilla.org/ |
| SSL Labs | Free SSL server testing | https://www.ssllabs.com/ssltest/ |
| Security Headers | Free header analysis | https://securityheaders.com/ |
| Socket.dev | Free for open source, dependency risk analysis | https://socket.dev/pricing |
| Aikido Security | 10 repos, SAST/SCA/IaC scanning | https://www.aikido.dev/pricing |

## Verification

- [ ] Service is still offering a free tier (check URL)
- [ ] Free tier limits match the project's expected usage
- [ ] No hidden costs (bandwidth overages, per-seat charges)
- [ ] Migration path exists if the service is discontinued
- [ ] Terms of service allow the intended use case
- [ ] Service is not a time-limited trial when always-free is needed

## How to Use

1. Understand the requirement and existing codebase patterns
2. Design the solution with error handling and testability in mind
3. Implement incrementally with tests for each change
4. Verify against expected outcomes (manual and automated)
5. Document usage, edge cases, and integration points
6. Review with team before merging to shared branches

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Tests slow me down" | Bugs slow you down 10x more. Tests are speed, not overhead. |
| "I will refactor later" | Technical debt compounds. Refactor as you go. |
| "It works on my machine" | If it is not in CI, it does not work. Ship proof, not claims. |