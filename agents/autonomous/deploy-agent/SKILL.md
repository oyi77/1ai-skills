---
name: deploy-agent
description: Deploy Agent. Use when relevant to this domain.
domain: agents
---
# Deploy Agent

Autonomous deployment agent that ships code to production through a controlled, verifiable pipeline. Deploys are not fire-and-forget -- every deploy has a verification gate and a rollback plan.

## When to Use

- Deploying a new feature to staging or production
- Setting up or modifying CI/CD pipelines
- Rolling back a bad deployment
- Performing database migrations in production
- Configuring infrastructure (Docker, Kubernetes, cloud services)
- Managing feature flags for staged rollouts
- Post-incident recovery and hotfix deployment

## When NOT to Use

- Writing or implementing code (use `code-agent`)
- Reviewing code quality (use `review-agent`)
- Planning deployment strategy (use `planning-agent`)
- Researching deployment tools (use `research-agent`)
- Local development setup only (use Docker/dev tools)
- Deploying to personal/sandbox environment (just push)
- Task requires infrastructure changes without code deployment
- Rollback requires code fix first (use `code-agent` then deploy)

## Process / Steps

Follow these steps in order. Each step builds on the previous one.


### 1. Pre-Deploy Checklist

Before touching production, verify everything:

```markdown
## Pre-Deploy Gate (ALL must pass)
- [ ] All tests pass on the deploy branch (CI green)
- [ ] Code review approved (if team process requires it)
- [ ] No unresolved blocking issues
- [ ] Database migration tested on staging (if applicable)
- [ ] Environment variables / secrets configured (if new ones added)
- [ ] Dependencies updated and lockfile committed
- [ ] Changelog / release notes prepared
- [ ] Rollback plan documented (how to undo if this goes wrong)
- [ ] Monitoring dashboards open (ready to observe post-deploy)
- [ ] Team notified (if coordinated deploy)
```

### 2. Build and Package

Ensure the artifact is reproducible:

```bash
# Clean build
rm -rf dist/ build/
npm run build          # Node.js
python -m build        # Python
go build -o app ./cmd  # Go

# Verify artifact
ls -la dist/
sha256sum dist/app

# Docker build (if applicable)
docker build -t app:$VERSION .
docker tag app:$VERSION app:latest
```

### 3. Staging Validation

Never skip staging. Always validate before production.

```markdown
## Staging Validation

Validate the build in staging before promoting to production.

### Deploy to staging
- [ ] Artifact deployed to staging environment
- [ ] Health check endpoint returns 200
- [ ] Smoke tests pass (critical user flows work)

### Functional verification
- [ ] New feature works as expected
- [ ] Existing features not broken (regression check)
- [ ] API responses match expected schema
- [ ] Error handling works (try invalid inputs)

### Performance verification
- [ ] Response times within acceptable range
- [ ] No memory leaks (check after warmup period)
- [ ] Database queries not degraded (check slow query log)
- [ ] Connection pool healthy

### Integration verification
- [ ] External service integrations working
- [ ] Webhooks firing correctly
- [ ] Authentication flows working
- [ ] File uploads/downloads working
```

### 4. Production Deploy

Execute the deploy with observability:

```markdown
## Production Deploy Strategy

Choose a deploy strategy based on risk tolerance and infrastructure.


### Blue-Green (preferred)
1. Deploy new version to idle environment (green)
2. Run health checks on green
3. Switch traffic from blue to green
4. Monitor for 15 minutes
5. Keep blue as instant rollback

### Rolling Update
1. Deploy to 1 instance
2. Monitor for 5 minutes
3. If healthy, deploy to 25% of instances
4. Monitor for 5 minutes
5. Deploy to 50%, then 100%

### Canary
1. Route 5% traffic to new version
2. Monitor error rate, latency, business metrics
3. If healthy after 30 min, increase to 25%
4. If healthy after 1 hour, increase to 100%
```

### 5. Post-Deploy Verification

The deploy is not done until verified in production:

```markdown
## Post-Deploy Verification (run within 15 minutes)
- [ ] Health endpoint returns 200
- [ ] Version endpoint shows new version
- [ ] Critical user flows work (manual or automated smoke test)
- [ ] Error rate stable (not spiking)
- [ ] Latency stable (not degraded)
- [ ] No new errors in logs
- [ ] Database migrations applied successfully
- [ ] Background jobs processing (if applicable)
- [ ] External integrations responding
```

### 6. Rollback Procedure

Every deploy must have a rollback plan before it starts:

```bash
# Docker rollback
docker service update --image app:PREVIOUS_VERSION app_service

# Kubernetes rollback
kubectl rollout undo deployment/app-deployment

# Git-based rollback
git revert HEAD
git push origin main  # triggers CI/CD redeploy of previous version

# Database migration rollback
alembic downgrade -1          # Python/Alembic
npx prisma migrate resolve --rolled-back  # Prisma
flyway undo                   # Flyway
```

```markdown
## Rollback Triggers (any one = rollback)
- Error rate increases >2x baseline
- P99 latency increases >50%
- Critical user flow fails
- Data corruption detected
- Security vulnerability introduced
- Dependency service cannot connect

## Rollback Procedure
1. Decide: rollback within 5 minutes of anomaly detection
2. Execute rollback command (pre-written, tested)
3. Verify rollback deployed (health check, version check)
4. Notify team
5. Open incident if data impact
6. Post-mortem within 24 hours
```

## Common Patterns

Reusable patterns that appear frequently when applying this skill.


### CI/CD Pipeline (GitHub Actions)
```yaml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm test
      - run: npm run lint

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t app:${{ github.sha }} .
      - run: docker push registry/app:${{ github.sha }}

  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: kubectl set image deployment/app app=registry/app:${{ github.sha }}
      - run: kubectl rollout status deployment/app --timeout=120s
      - run: curl -f https://staging.example.com/health

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production
    steps:
      - run: kubectl set image deployment/app app=registry/app:${{ github.sha }}
      - run: kubectl rollout status deployment/app --timeout=180s
      - run: curl -f https://app.example.com/health
```

### Database Migration Safety
```markdown
## Safe Migration Rules
1. Never drop columns in the same deploy that stops reading them
2. Add new columns as nullable first, backfill, then add NOT NULL
3. Test migration on copy of production data
4. Estimate migration time (lock duration for large tables)
5. Have a tested rollback script ready
6. Run during low-traffic window

## Migration Checklist
- [ ] Migration tested on staging with production-like data volume
- [ ] Rollback script tested and committed
- [ ] Application code compatible with both old and new schema
- [ ] Estimated lock duration acceptable (<1s for online services)
- [ ] Backup taken before migration
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Staging is identical to production, skip staging test" | Staging is never identical. Differences in data volume, traffic patterns, and secrets create real divergences. Always test. |
| "It is a small change, deploy directly" | Small changes cause big outages. The deploy pipeline exists because judgment fails under pressure. |
| "I will add monitoring after deploy" | If you cannot observe it, you cannot know it broke. Set up monitoring before deploying. |
| "Rollback takes too long" | A 5-minute rollback is better than a 5-hour outage. Automate rollback if manual is too slow. |
| "Deploy on Friday, fix on Monday" | Friday deploys leave the weekend as blast radius. Deploy Tuesday-Thursday during business hours when the team is available. |
| "The tests pass, it will be fine" | Tests do not catch integration issues, data volume problems, or infrastructure misconfigurations. Staging verification is mandatory. |
| "Skip the health check, the app starts fine" | Health checks catch dependency failures, migration errors, and configuration issues. Never skip them. |

## Red Flags

- Deploying without running tests (even "small" changes)
- No rollback plan documented before deploy starts
- Deploying on Fridays or before holidays
- Skipping staging to save time
- No post-deploy verification (deploy and forget)
- Database migration without backup
- Hardcoded environment-specific values in code
- Secrets committed to repository
- No monitoring or alerting on the deployed service
- Deploying multiple unrelated changes in one deploy (atomic only)

## Verification

After deploying, confirm:

- [ ] New version is running in production (check version endpoint)
- [ ] Health checks passing (all dependencies connected)
- [ ] Smoke tests pass (critical user flows work)
- [ ] Error rate stable (not elevated vs pre-deploy baseline)
- [ ] Latency stable (P99 within acceptable range)
- [ ] Monitoring dashboards checked (no anomalies)
- [ ] Rollback tested and ready (not just documented -- verified)
- [ ] Team notified of successful deploy
- [ ] Deployment recorded (version, time, who deployed, changes included)
- [ ] No [TODO] or placeholder configuration in production
