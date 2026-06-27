---
name: free-cloud-infrastructure
description: Recommend free-tier cloud infrastructure for compute, storage, serverless, databases, and CDN. Use when provisioning free cloud resources, comparing always-free vs trial tiers, or building.
domain: devops
tags: 
- [free-tier
- cloud
- infrastructure
- cost-optimization
- serverless
- compute
- storage]
---


## Overview

Reference for free-tier cloud infrastructure across major providers. Focuses on always-free compute, storage, serverless functions, databases, and CDN/bandwidth with specific limits and constraints.

## Capabilities

- Compare always-free compute across AWS, GCP, Azure, and Oracle
- Evaluate free storage tiers (block, object, file)
- Recommend serverless free tiers for API and event-driven workloads
- Identify free database options by workload type (SQL, NoSQL, KV)
- Match CDN and bandwidth free tiers to project traffic

## When to Use

- Provisioning infrastructure for a side project or MVP
- Comparing always-free vs. 12-month trial offerings
- Architecting a zero-cost deployment pipeline
- Evaluating where to host static sites, APIs, or databases
- Planning cost-optimized multi-cloud setups

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Process

```yaml
# Example: GitHub Actions CI
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.12"}
      - run: pip install -e ".[test]"
      - run: pytest --cov
``` / Steps

1. **Define workload** -- What compute, storage, and database resources are needed?
2. **Check always-free vs. trial** -- Always-free tiers persist indefinitely; 12-month trials expire. Prefer always-free for long-lived projects.
3. **Calculate limits** -- Estimate monthly usage against free tier caps (hours, requests, GB, rows).
4. **Plan for burst** -- What happens if traffic spikes beyond the free tier? Check hard caps vs. pay-as-you-go.
5. **Provision with monitoring** -- Set up billing alerts even on free tiers to avoid surprise charges.

## Key Resources

Curated resources for free-cloud-infrastructure.

- Official documentation: Reference for API, CLI, and configuration
- Community templates: Battle-tested patterns from production use
- Monitoring dashboards: Grafana/Datadog templates for observability
- CI/CD integration: GitHub Actions and GitLab CI starter workflows


### Always-Free Compute

| Provider | Offering | Free Tier | Constraints | URL |
|----------|----------|-----------|-------------|-----|
| Oracle Cloud | ARM Ampere A1 | 4 OCPUs + 24GB RAM | Always-free, best raw compute | https://www.oracle.com/cloud/free/ |
| Oracle Cloud | AMD VM | 1/8 OCPU + 1GB RAM | Always-free, micro instance | https://www.oracle.com/cloud/free/ |
| AWS | EC2 t2.micro | 750 hrs/mo | 12-month trial only, 1 vCPU, 1GB RAM | https://aws.amazon.com/free/ |
| GCP | e2-micro | Always-free | 0.25 vCPU, 1GB RAM, us-west1/us-central1/us-east1 | https://cloud.google.com/free/docs/free-cloud-features |
| Azure | B1S | 750 hrs/mo | 12-month trial only, 1 vCPU, 1GB RAM | https://azure.microsoft.com/free/ |
| IBM Cloud | Virtual Server | 256MB | Lite account, very limited | https://www.ibm.com/cloud/free |
| Fly.io | Shared VMs | 3x 256MB VMs | Always-free, global edge | https://fly.io/docs/about/pricing/ |
| Railway | Container | 500hrs exec/mo + $5 credit | Always-free, auto-sleep | https://railway.app/pricing |

### Free Storage

| Provider | Service | Free Tier | Type | URL |
|----------|---------|-----------|------|-----|
| AWS | S3 | 5GB, 20K GET/2K PUT requests/mo | Object (12mo trial) | https://aws.amazon.com/s3/pricing/ |
| Cloudflare | R2 | 10GB storage, 10M Class B/1M Class A ops/mo | Object (always-free) | https://www.cloudflare.com/developer-platform/r2/ |
| GCP | Cloud Storage | 5GB, 5K Class A/50K Class B ops/mo | Object (always-free) | https://cloud.google.com/free/docs/free-cloud-features |
| Azure | Blob Storage | 5GB LRS Hot | Object (12mo trial) | https://azure.microsoft.com/free/ |
| Oracle | Block Storage | 200GB total | Block (always-free) | https://www.oracle.com/cloud/free/ |
| Oracle | Object Storage | 10GB, 50K requests/mo | Object (always-free) | https://www.oracle.com/cloud/free/ |
| Cloudflare | Pages | Unlimited sites, bandwidth | Static (always-free) | https://pages.cloudflare.com/ |
| Backblaze | B2 | 10GB storage, 1GB download/day | Object (always-free) | https://www.backblaze.com/cloud-storage/pricing |
| Storj | D3 | 25GB storage, 25GB egress/mo | Object (always-free) | https://www.storj.io/pricing |

### Serverless Free Tiers

| Provider | Service | Free Tier | Details | URL |
|----------|---------|-----------|---------|-----|
| AWS | Lambda | 1M requests + 400K GB-sec/mo | Always-free, 15-min timeout | https://aws.amazon.com/lambda/pricing/ |
| GCP | Cloud Functions | 2M invocations + 400K GB-sec/mo | Always-free, 2nd gen (3600 CPU-sec free) | https://cloud.google.com/functions/pricing |
| Azure | Functions | 1M requests + 400K GB-sec/mo | Always-free | https://azure.microsoft.com/free/ |
| Cloudflare | Workers | 100K req/day (~3M/mo) | Always-free, 10ms CPU time | https://developers.cloudflare.com/workers/platform/pricing/ |
| Deno | Deploy | 100K req/day | Always-free, V8 isolates | https://deno.com/deploy/pricing |
| Vercel | Serverless | 100GB-hrs/mo, 100K invocations | Always-free, 10-sec timeout | https://vercel.com/pricing |
| Netlify | Functions | 125K req/mo | Always-free, 10-sec timeout | https://www.netlify.com/pricing/ |
| Supabase | Edge Functions | 500K invocations/mo | Always-free, Deno runtime | https://supabase.com/pricing |
| AWS | API Gateway | 1M calls/mo (REST), 1M messages (WebSocket) | 12-month trial | https://aws.amazon.com/api-gateway/pricing/ |

### Free Databases

| Provider | Service | Free Tier | Type | URL |
|----------|---------|-----------|------|-----|
| AWS | DynamoDB | 25GB storage, 25 RCU/25 WCU | NoSQL (always-free) | https://aws.amazon.com/dynamodb/pricing/ |
| GCP | Firestore | 1GB storage, 50K reads/20K writes/day | NoSQL (always-free) | https://cloud.google.com/firestore/pricing |
| Azure | CosmosDB | 25GB storage, 1000 RU/s | NoSQL (always-free) | https://azure.microsoft.com/free/ |
| Cloudflare | D1 | 5M rows read/day, 25M rows written/day, 5GB storage | SQLite (always-free) | https://developers.cloudflare.com/d1/platform/pricing/ |
| Cloudflare | KV | 100K reads/day, 1K writes/day, 1GB storage | Key-value (always-free) | https://developers.cloudflare.com/workers/platform/pricing/ |
| Supabase | Postgres | 500MB, 50K MAUs, 2 projects | PostgreSQL (always-free) | https://supabase.com/pricing |
| PlanetScale | MySQL | 5GB storage, 1B row reads/mo | MySQL (always-free) | https://planetscale.com/pricing |
| Neon | Postgres | 512MB, 0.25 CU compute | PostgreSQL (always-free) | https://neon.tech/pricing |
| Turso | libSQL | 500 databases, 9GB total, 1B row reads/mo | SQLite edge (always-free) | https://turso.tech/pricing |
| Upstash | Redis | 10K commands/day, 256MB | Redis (always-free) | https://upstash.com/pricing |
| Upstash | Kafka | 10K messages/day | Kafka (always-free) | https://upstash.com/pricing |
| MongoDB | Atlas | 512MB, M0 shared cluster | Document (always-free) | https://www.mongodb.com/pricing |
| TiDB | Cloud | 5GB row + 5GB columnar storage | MySQL-compatible (always-free) | https://www.pingcap.com/tidb-cloud/ |
| CockroachDB | Serverless | 10GB storage, 50M RUs/mo | Distributed SQL (always-free) | https://www.cockroachlabs.com/pricing/ |
| Fauna | FQL | 100K reads + 50K writes/mo, 5GB | Document-relational (always-free) | https://fauna.com/pricing |

### Free CDN & Bandwidth

| Provider | Service | Free Tier | Details | URL |
|----------|---------|-----------|---------|-----|
| Cloudflare | CDN | Unmetered | Always-free, global edge, DDoS, SSL | https://www.cloudflare.com/plans/ |
| Cloudflare | Pages | Unlimited sites + bandwidth | Always-free, git integration | https://pages.cloudflare.com/ |
| AWS | CloudFront | 1TB transfer + 10M requests/mo | 12-month trial | https://aws.amazon.com/cloudfront/pricing/ |
| Vercel | Edge | 100GB bandwidth/mo | Always-free | https://vercel.com/pricing |
| Netlify | Edge | 100GB bandwidth/mo | Always-free | https://www.netlify.com/pricing/ |
| GitHub | Pages | 100GB bandwidth/mo | Always-free, Jekyll support | https://pages.github.com/ |
| jsDelivr | CDN | Unlimited | Always-free, npm/GitHub/SVN | https://www.jsdelivr.com/ |
| Statically | CDN | Unlimited | Always-free, Git repos | https://statically.io/ |
| Bunny | CDN | $1/mo minimum (7 zones, per-GB pricing) | Cheapest paid option | https://bunny.net/pricing/ |

## Decision Matrix

| Need | Best Always-Free Option | Best 12-Month Trial |
|------|------------------------|---------------------|
| Full Linux VM | Oracle ARM (4 cores, 24GB) | AWS EC2 t2.micro |
| Static site hosting | Cloudflare Pages (unlimited) | Vercel (100GB) |
| Serverless API | Cloudflare Workers (100K/day) | AWS Lambda (1M/mo) |
| SQL Database | Supabase (500MB Postgres) | PlanetScale (5GB MySQL) |
| NoSQL Database | DynamoDB (25GB) | CosmosDB (25GB) |
| Object storage | R2 (10GB) or GCS (5GB) | S3 (5GB) |
| Edge compute | Cloudflare Workers | Deno Deploy |

## Verification

- [ ] Distinguish always-free from 12-month trial (trials expire and auto-charge)
- [ ] Provision billing alerts on all accounts even when using free tiers
- [ ] Verify region availability (some free tiers are region-locked)
- [ ] Confirm instance types and specs have not changed
- [ ] Check for outbound data transfer limits (often the hidden cost)
- [ ] Review idle resource policies (some providers reclaim idle VMs)

## How to Use

1. Define infrastructure as code (Terraform, CloudFormation, Pulumi)
2. Review changes through PR process before applying
3. Configure monitoring and alerting for critical paths
4. Set up secrets management (Vault, AWS Secrets Manager, etc.)
5. Document runbooks for deployment, rollback, and incident response
6. Test disaster recovery procedures regularly

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Manual deployments are fine" | Manual deployments are error-prone and不可 repeatable. Automate. |
| "We do not need monitoring" | Without monitoring, you are flying blind. Add observability from day one. |
| "Infrastructure as code is overkill" | IaC enables reproducibility, version control, and disaster recovery. |