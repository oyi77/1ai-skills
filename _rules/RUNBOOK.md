---
name: runbook
version: 1.0.0
severity: mandatory
scope: [ops, infra, monitoring]
pairs-with: [incident, release, security, roles]
description: Daily health checks, failure procedures, scaling, rotation, and operational log requirements for AI-agent-run infrastructure
---

# RUNBOOK — Operational Procedures

> **This file is the ops manual for AI agents running BerkahKarya infrastructure.**
> INCIDENT.md handles declared incidents. RELEASE.md handles deploys. This file covers everything that happens between those events: steady-state operations, failure containment before incident declaration, and procedural receipts.

---

## §1 — DAILY HEALTH CHECKS

Run every day at 07:00 WIB (00:00 UTC). Execute checks in the order listed. Any FAIL result stops the chain — do not skip to later checks until the failing check is resolved or escalated.

### 1.1 Check Order

| # | Check | Tool | Pass Criteria | Fail Action |
|---|-------|------|---------------|-------------|
| 1 | API health endpoints | `curl -sf <url>/health` | HTTP 200, response < 500ms | Escalate to INCIDENT.md SEV2 |
| 2 | Database connectivity | DB ping or SELECT 1 | Response received, no error | Escalate to INCIDENT.md SEV2 |
| 3 | Auth service reachable | Token validation request | Valid token returned | Escalate to INCIDENT.md SEV1 |
| 4 | Storage bucket accessible | List operation on primary bucket | Returns listing without error | Log WARN, check again in 1h |
| 5 | Error rate (last 24h) | Query monitoring dashboard | < 1% error rate on all endpoints | File bug if 1–5%; SEV2 if > 5% |
| 6 | Payment pipeline (if applicable) | Test transaction or webhook ping | Webhook received within 30s | Escalate to INCIDENT.md SEV1 |
| 7 | Scheduled jobs last run | Query job log table / cron dashboard | All jobs ran within expected window | Follow §8 |
| 8 | Certificate expiry | `openssl s_client` or dashboard check | All certs expire > 30 days out | Follow §6 immediately |
| 9 | Secret expiry scan | Check secret manager expiry metadata | No secrets expire within 14 days | Follow §6 immediately |
| 10 | Monitoring service itself | Ping monitoring vendor status page | Monitoring vendor operational | Follow §7 |

### 1.2 Daily Health Check Receipt

After completing all checks, post to the ops log channel (Telegram/Slack `#ops-daily`):

```
[DAILY HEALTH] YYYY-MM-DD 07:00 WIB
Agent: <agent-id>
Checks: 10/10 PASS  (or: N/10 PASS, list FAILs)
Anomalies: <none | description>
Actions taken: <none | link to issue>
```

Absence of this receipt by 08:00 WIB is itself a failure — the monitoring gap procedure (§7) applies.

---

## §2 — DEPLOY FAILURE PROCEDURE

Covers the window after a deploy has been triggered but before the post-deploy watch window (RELEASE.md §7) declares nominal. Does **not** replace INCIDENT.md — if deploy failure causes user impact, declare an incident immediately in parallel.

### 2.1 Detect Deploy Failure

A deploy failure is any of:
- CI/CD pipeline exits non-zero
- Health check endpoint returns non-200 within 5 minutes of deploy completing
- Error rate rises > 50% above baseline within 10 minutes of deploy
- New version not confirmed running (version endpoint still returns old hash)

### 2.2 Partial Deploy — Service Still Running Old Version

Steps in order:

1. **Do not push more code.** Freeze the deploy pipeline immediately.
2. Identify which instances/containers are running old vs new version: query `/version` or check deployment dashboard.
3. If < 50% of instances updated and old version is healthy: roll back the partial fleet to old version using the platform rollback command (e.g., `vercel rollback`, `gcloud run deploy --image=<prev>`, Kubernetes `kubectl rollout undo`).
4. Confirm all instances report old version on `/version`.
5. Run smoke test against old version — confirm pass.
6. Post to `#ops`: "Deploy `<version>` rolled back — partial deploy detected. Old version confirmed running. Root cause investigation started."
7. File GitHub issue: `[DEPLOY-FAIL] <version> partial deploy — <timestamp>`. Label: `deploy-failure`.
8. Investigate root cause before retrying: check deploy logs, infra events, dependency changes.
9. Do not retry until root cause is identified and documented in the issue.

### 2.3 Full Deploy Failure — Service Down

1. Declare incident immediately: INCIDENT.md SEV1 or SEV2 depending on user impact.
2. Trigger rollback: run the rollback plan documented in the PR/release notes (RELEASE.md §5).
3. If rollback plan is missing: use platform emergency rollback (last known good image/commit).
4. Monitor error rate and health check for 5 minutes post-rollback.
5. If rollback restores service: downgrade incident to SEV2, continue investigation.
6. If rollback also fails: maintain SEV1, notify human owner immediately.

### 2.4 Deploy Failure Receipt

```
[DEPLOY-FAIL] <version> — YYYY-MM-DD HH:MM WIB
Agent: <agent-id>
Failure type: partial | full-down | health-check-fail
Rollback executed: yes | no
Rollback result: success | fail | not-needed
Incident declared: yes (SEV{N} #<issue>) | no
Root cause (preliminary): <description>
Issue filed: #<N>
```

---

## §3 — THIRD-PARTY OUTAGE RESPONSE

### 3.1 Detection

Third-party outage signals (any one is sufficient to start the procedure):
- Monitoring alert fires for an integration that routes through an external service
- Error log shows repeated 5xx or timeout from a named external host
- Health check §1 fails for an externally-dependent component
- External vendor posts incident on their status page

### 3.2 Classification

| Dependency Type | Impact if Down | Response |
|---|---|---|
| Payment processor (Stripe, Midtrans) | Revenue blocked | SEV1 — INCIDENT.md immediately |
| Auth provider (Supabase Auth, Clerk) | All users locked out | SEV1 — INCIDENT.md immediately |
| Primary database host | Full service down | SEV1 — INCIDENT.md immediately |
| CDN / static asset host | UI broken for users | SEV2 — INCIDENT.md |
| Email delivery (SendGrid, Resend) | Transactional email fails | SEV3 — monitor, queue retry |
| Analytics / logging vendor | Visibility reduced | SEV4 — log internally, continue |
| Non-critical third-party API | Feature degraded | SEV3 — disable feature, file issue |

### 3.3 Response Steps

1. **Confirm it is external**: check vendor status page (bookmark list in SECURITY.md or ops wiki). Rule out own-infra cause first — check your own logs for the error origin.
2. **Check if workaround exists**: feature flag to disable the affected integration, fallback queue (e.g., queue emails for retry), or cached data serve.
3. **Apply workaround if available**: engage feature flag or fallback, confirm degraded-but-functional state.
4. **Set check interval**: poll vendor status page every 15 minutes until resolved. Log each poll.
5. **Notify if user-facing**: follow COMMS.md notification rules. Do not explain internal vendor details publicly — use "we are experiencing issues with a third-party service."
6. **On vendor recovery**: disable fallback/workaround, verify integration end-to-end, confirm error rate returns to baseline.
7. **File post-outage review issue**: document duration, impact, and whether a fallback should be built if one did not exist.

### 3.4 Third-Party Outage Receipt

```
[3P-OUTAGE] <vendor> — YYYY-MM-DD HH:MM WIB
Agent: <agent-id>
Vendor status page: <url> — <status at detection>
Impact classification: SEV{N}
Workaround applied: <description | none>
User notification sent: yes | no
Vendor resolved at: YYYY-MM-DD HH:MM WIB (or: ongoing)
Post-outage review issue: #<N>
```

---

## §4 — DATABASE MIGRATION FAILURE

### 4.1 Detection

Migration failure is confirmed when any of:
- Migration runner exits non-zero
- Schema version table does not match expected version after run
- Application throws schema mismatch error on startup post-migration
- Data integrity check query (see §4.3) returns unexpected results

### 4.2 Rollback Steps

Execute in order. Do not skip steps.

1. **Stop all application instances immediately.** Do not allow the app to write to a partially-migrated schema — this causes data corruption that may be irreversible.
   - Kubernetes: `kubectl scale deployment <name> --replicas=0`
   - Vercel/serverless: set maintenance mode via environment variable checked at request start
2. **Identify last known good migration version**: query `schema_migrations` table (or equivalent). Note the current version.
3. **Run down migration**: execute `<migration-tool> down` to the last good version. For Prisma: `prisma migrate resolve --rolled-back <migration-name>`. For Flyway: `flyway undo`.
4. **Verify schema version**: re-query version table — must match pre-migration version.
5. **Run data integrity checks** (§4.3).
6. **Restart application instances** pointing to old schema.
7. **Confirm application health**: run health check §1.2 checks 1–4.
8. **Declare incident** if any step fails: INCIDENT.md SEV1.

### 4.3 Data Integrity Verification

Run these queries after every migration or rollback. Adapt table names to the actual schema.

```sql
-- Row count sanity: compare to pre-migration baseline stored in ops log
SELECT table_name, n_live_tup AS row_count
FROM pg_stat_user_tables
ORDER BY table_name;

-- Referential integrity: find orphaned foreign keys (example)
SELECT COUNT(*) FROM orders o
LEFT JOIN users u ON o.user_id = u.id
WHERE u.id IS NULL;
-- Expected: 0

-- Null constraint check on critical columns (example)
SELECT COUNT(*) FROM users WHERE email IS NULL OR id IS NULL;
-- Expected: 0
```

Pre-migration: capture row counts and store in migration issue comment.
Post-rollback: re-run same queries and compare. Any discrepancy = SEV1.

### 4.4 Irreversible Migration

If down migration is impossible (e.g., dropped column with data, no backup):
1. STOP immediately. Do not attempt partial fix.
2. Notify human owner — this is a data loss event.
3. Restore from most recent verified backup.
4. Declare INCIDENT.md SEV1.
5. Document exact data loss window and affected tables.

### 4.5 Migration Failure Receipt

```
[DB-MIGRATION-FAIL] <migration-name> — YYYY-MM-DD HH:MM WIB
Agent: <agent-id>
Migration version attempted: <version>
Rolled back to version: <version>
App instances stopped: yes | no
App instances restarted: yes | no
Integrity check result: PASS | FAIL (details)
Data loss: none | <description>
Incident declared: yes (SEV{N} #<issue>) | no
```

---

## §5 — CAPACITY CEILING PROCEDURE

### 5.1 Capacity Thresholds — Alert Levels

| Resource | Warning (investigate) | Critical (act within 24h) | Emergency (act immediately) |
|---|---|---|---|
| CPU utilization | > 70% sustained 1h | > 85% sustained 30min | > 95% sustained 5min |
| Memory utilization | > 75% sustained 1h | > 88% sustained 30min | > 95% sustained 5min |
| Database connections | > 70% of max_connections | > 85% | > 95% |
| Database storage | > 70% of provisioned | > 85% | > 90% |
| Serverless invocations | > 70% of quota | > 85% | > 95% |
| CDN bandwidth | > 70% of plan limit | > 85% | > 95% |
| API rate limit consumed | > 60% of daily quota by noon | > 80% by noon | > 95% at any time |

### 5.2 Detection

- Monitoring dashboards (Grafana, Datadog, or cloud-native metrics) emit alerts at Warning threshold.
- Daily health checks (§1) include a capacity summary review.
- Agents running scheduled jobs must log resource utilization in the job receipt (§8.4).

### 5.3 Response by Level

**Warning:** Investigate root cause. Is this a traffic spike, a runaway query, a memory leak? File a GitHub issue. No spend authorization needed at this level — optimize first.

**Critical:** 
1. Identify whether this is a spike (temporary) or a trend (structural).
2. If spike: apply rate limiting, queue shedding, or cache warming to absorb load without scaling.
3. If trend: prepare scaling plan (see §5.4). Agent may pre-stage the scaling action but MUST NOT execute it without spend approval.
4. Notify human owner with scaling cost estimate.

**Emergency:**
1. Scale immediately — do not wait for approval when service is at risk.
2. Notify human owner simultaneously (not before, not after — same moment).
3. Use the smallest scaling increment that resolves the emergency.
4. Document the emergency scale event in ops log within 1 hour.

### 5.4 Scaling Decision Rules

An agent MAY scale autonomously (no approval needed) only when ALL of these are true:
- Resource is at Emergency threshold (§5.1)
- Scaling action costs < $50 incremental per month
- Action is reversible within 1 hour
- No prior approval was explicitly denied for this resource in the last 30 days

An agent MUST get human owner approval before scaling when:
- Monthly cost increase > $50
- Action requires contract change (e.g., upgrading database tier)
- Action is irreversible within a sprint cycle
- Owner previously set a budget cap that would be breached

### 5.5 Capacity Scale Receipt

```
[CAPACITY-SCALE] <resource> — YYYY-MM-DD HH:MM WIB
Agent: <agent-id>
Trigger threshold: warning | critical | emergency
Resource utilization at trigger: <N>%
Root cause: spike | trend | leak | unknown
Action taken: <description of scaling action>
Cost delta (monthly est.): $<N>
Owner approval: yes (received HH:MM) | not-required (emergency, <$50) | pending
Reversible: yes | no
Post-scale utilization: <N>%
```

---

## §6 — CERTIFICATE AND SECRET EXPIRY

### 6.1 Detection Schedule

| Asset Type | Check Frequency | Warning Threshold | Critical Threshold |
|---|---|---|---|
| TLS certificates (custom domains) | Daily (§1 check #8) | 30 days to expiry | 14 days to expiry |
| API keys (third-party services) | Daily (§1 check #9) | 14 days to expiry | 7 days to expiry |
| OAuth client secrets | Daily | 14 days to expiry | 7 days to expiry |
| Database passwords (manually rotated) | Weekly | 30 days since last rotation | 60 days since last rotation |
| JWT signing secrets | Weekly | 60 days since last rotation | 90 days since last rotation |
| Deploy tokens / CI secrets | Weekly | 60 days since last rotation | 90 days since last rotation |

### 6.2 Routine Renewal Procedure

For TLS certificates (Let's Encrypt / managed certs):
1. Confirm auto-renewal is enabled on the platform (Vercel, Cloudflare, etc.).
2. If auto-renewal failed: log into platform dashboard, trigger manual renewal.
3. Verify new cert is live: `openssl s_client -connect <domain>:443 -servername <domain> 2>/dev/null | openssl x509 -noout -dates`
4. New expiry must be > 60 days from today.

For API keys and secrets:
1. Generate new secret in the provider dashboard.
2. Add new secret to secret manager / environment config.
3. Deploy new secret to all environments (staging first, then production).
4. Verify service continues to function with new secret (run health checks §1).
5. Revoke old secret in the provider dashboard.
6. Update expiry metadata in ops tracking sheet / secret manager.

### 6.3 Emergency Rotation (Secret Compromised)

Trigger: any indication a secret has been exposed (public repo, log leak, suspicious API usage).

1. Revoke the compromised secret at the source immediately — do not wait for a replacement.
2. Generate a new secret.
3. Deploy new secret to all environments within 30 minutes of revocation.
4. Audit usage logs for the compromised secret — check for unauthorized calls.
5. If unauthorized usage found: declare INCIDENT.md SEV1 and follow SECURITY.md breach protocol.
6. If no unauthorized usage confirmed: file SEV3 incident for record.
7. Post receipt within 1 hour of rotation completing.

### 6.4 Certificate/Secret Rotation Receipt

```
[SECRET-ROTATION] <secret-name> — YYYY-MM-DD HH:MM WIB
Agent: <agent-id>
Rotation type: scheduled | emergency
Trigger: expiry-warning | expiry-critical | compromised | policy
Old secret revoked: yes | no (and why)
New secret deployed to: staging | production | both
Health check post-rotation: PASS | FAIL
Unauthorized usage detected: yes (see incident #<N>) | no
Next scheduled rotation: YYYY-MM-DD
```

---

## §7 — MONITORING GAP RESPONSE

A monitoring gap occurs when the monitoring service itself is unavailable, producing a blind spot where failures cannot be automatically detected.

### 7.1 Detection

Monitoring gap is detected by any of:
- Monitoring vendor status page shows outage
- No alerts have fired in > 2 hours on a normally active system (absence of signal is suspicious)
- Health check (§1 check #10) fails
- Agent cannot reach monitoring dashboard API

### 7.2 Immediate Response Steps

1. **Confirm it is a monitoring gap, not a total system outage.** Directly curl the production health endpoints. If production is up and monitoring is down, proceed. If production is also down, follow INCIDENT.md.
2. **Switch to manual polling.** Every 15 minutes, an agent runs the §1 checks manually and posts results to `#ops` channel until monitoring is restored.
3. **Freeze non-emergency deploys.** Do not deploy while blind — RELEASE.md §6 "at least one monitoring agent active during deploy window" cannot be satisfied.
4. **Notify human owner** if monitoring gap exceeds 1 hour (cannot maintain adequate safety posture alone).
5. **Check monitoring vendor ETA** for restoration. If > 4 hours ETA, evaluate emergency secondary monitoring: UptimeRobot, BetterUptime, or manual cron ping.
6. **On monitoring restoration**: verify all dashboards are receiving data, confirm no alerts were missed by reviewing raw logs for the gap window, resume normal operations.

### 7.3 Manual Poll Script

Run every 15 minutes during a monitoring gap:

```bash
#!/bin/bash
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
for URL in https://<api-host>/health https://<app-host>/health; do
  STATUS=$(curl -sf -o /dev/null -w "%{http_code}" --max-time 10 "$URL")
  echo "$TIMESTAMP $URL => HTTP $STATUS"
done
```

Post output to `#ops` with prefix `[MANUAL-POLL]`.

### 7.4 Monitoring Gap Receipt

```
[MONITORING-GAP] <vendor> — YYYY-MM-DD HH:MM WIB
Agent: <agent-id>
Gap start: YYYY-MM-DD HH:MM WIB
Gap end: YYYY-MM-DD HH:MM WIB (or: ongoing)
Manual polling performed: yes (every 15min) | no (explain)
Deploys frozen: yes | no (explain)
Owner notified: yes (at HH:MM) | not-required (gap < 1h)
Production status during gap: HEALTHY | DEGRADED | UNKNOWN
Any failures detected during gap: none | <description>
```

---

## §8 — SCHEDULED JOB FAILURE

### 8.1 Scheduled Job Registry

Every scheduled job MUST be registered in the ops wiki or a `jobs.md` file at the repo root with:
- Job name
- Schedule (cron expression)
- Expected duration
- Expected output / success signal
- Owner agent
- Retry policy

A job without a registry entry is unauthorized and must be disabled until registered.

### 8.2 Failure Detection

A scheduled job has failed when any of:
- Job exits non-zero
- Job does not start within 5 minutes of scheduled time
- Job runs > 3× its expected duration without completing
- Job completes but output validation fails (e.g., expected rows not written, email not sent)
- No job receipt posted within 10 minutes of expected completion time (§8.4)

### 8.3 Retry and Escalation Policy

| Failure Count | Action |
|---|---|
| 1st failure | Automatic retry after 5-minute backoff |
| 2nd consecutive failure | Automatic retry after 15-minute backoff; post WARNING to `#ops` |
| 3rd consecutive failure | No further automatic retry; escalate to agent-on-call; file GitHub issue `[JOB-FAIL] <job-name>` |
| 3+ failures over 24h | File issue if not already filed; notify human owner in daily summary |
| Revenue-critical job fails once | Escalate immediately — no silent retry; follow INCIDENT.md SEV2 |

Revenue-critical jobs (must be labelled in registry): payment processing, subscription renewal, invoice generation, report delivery to paying customers.

### 8.4 Job Execution Receipt

Every scheduled job MUST post a receipt on completion (success or failure):

```
[JOB] <job-name> — YYYY-MM-DD HH:MM WIB
Status: SUCCESS | FAIL | TIMEOUT
Duration: <Ns>
Output summary: <rows written | emails sent | records processed | etc.>
Retry count this run: 0 | N
Next scheduled run: YYYY-MM-DD HH:MM WIB
Error (if FAIL): <error message or log excerpt>
Issue filed: #<N> | n/a
```

### 8.5 Stuck Job Recovery

If a job is running > 3× expected duration:
1. Check if job is actually doing work (CPU/DB activity) or hung (idle, waiting on lock).
2. If hung: kill the job process. Note: killing a job mid-run may leave partial data. Before killing, check if the job is idempotent (safe to re-run) or requires cleanup.
3. If non-idempotent job was killed mid-run: manually verify and clean up partial state before retrying.
4. File issue documenting the hung state, what was cleaned, and a fix plan.

---

## §9 — ROLLBACK DECISION TREE

This section applies after production deploy only. Pre-deploy rollback planning belongs in RELEASE.md §5.

### 9.1 Decision: Roll Back vs Fix Forward

Answer these questions in order. Stop at the first definitive answer.

```
Q1: Is there active data corruption or data loss?
    YES → ROLLBACK immediately. Do not attempt fix-forward on corrupted data.
    NO  → continue

Q2: Is the error rate > 200% of baseline?
    YES → ROLLBACK unless a targeted fix can be deployed within 15 minutes.
    NO  → continue

Q3: Is revenue completely blocked (payment, checkout, auth broken)?
    YES → ROLLBACK unless a targeted fix can be deployed within 10 minutes.
    NO  → continue

Q4: Has the incident been ongoing > 30 minutes with no fix in sight?
    YES → ROLLBACK. Time-boxed fix-forward attempts expire.
    NO  → continue

Q5: Is the rollback itself risky (schema migration, data dependency)?
    YES → Fix-forward preferred. Assess rollback cost vs fix cost explicitly.
    NO  → Rollback remains an option; decide on fix complexity.

Q6: Is fix-forward complexity LOW (< 30 min, 1 file, no schema)?
    YES → Fix-forward. Deploy immediately.
    NO  → ROLLBACK, then fix in a proper release.
```

### 9.2 Approval Requirements

| Scenario | Approval Required |
|---|---|
| Rollback triggered by autonomous agent (no human present) | Proceed immediately; notify owner within 10 min |
| Rollback during business hours with owner available | Notify owner before executing; proceed if no response within 5 min |
| Fix-forward that changes schema | Owner approval mandatory; no autonomous fix-forward on schema |
| Fix-forward on SEV1 with IC present | IC approval sufficient (INCIDENT.md §3 Step 3) |
| Rollback of a MAJOR release | Owner approval required before rollback; emergency exception if SEV1 |

### 9.3 Rollback Execution

1. Execute the rollback plan from the PR/release notes (RELEASE.md §5).
2. If no rollback plan exists: use platform emergency rollback command. Log that plan was missing — file issue for process gap.
3. Confirm rollback complete: version endpoint, health check, smoke test.
4. Post to `#ops` and incident war room: "Rollback to `<version>` complete. Health check: PASS."
5. Extend post-deploy watch window (RELEASE.md §7) for another 30 minutes from rollback completion.

### 9.4 Rollback Decision Receipt

```
[ROLLBACK-DECISION] <version> → <target-version> — YYYY-MM-DD HH:MM WIB
Agent: <agent-id>
Decision: ROLLBACK | FIX-FORWARD
Decision trigger (Q answer from §9.1): Q<N> — <reason>
Approval: autonomous (owner notified at HH:MM) | owner-approved | IC-approved
Rollback executed at: YYYY-MM-DD HH:MM WIB
Rollback result: SUCCESS | FAIL
Post-rollback health: PASS | FAIL
Watch window extended until: YYYY-MM-DD HH:MM WIB
Incident link: #<N> | n/a
```

---

## §10 — OPERATIONAL LOG REQUIREMENTS

Every procedure in this runbook produces a receipt. This section defines where receipts go, retention, and what constitutes a complete log record.

### 10.1 Where Receipts Are Posted

| Procedure | Primary Location | Secondary Location |
|---|---|---|
| Daily health check (§1) | `#ops-daily` channel | GitHub ops-log issue (weekly digest) |
| Deploy failure (§2) | GitHub issue `[DEPLOY-FAIL]` | `#ops` channel notification |
| Third-party outage (§3) | GitHub issue `[3P-OUTAGE]` | `#ops` channel notification |
| DB migration failure (§4) | GitHub issue `[DB-MIGRATION-FAIL]` | `#ops` channel notification |
| Capacity scale (§5) | GitHub issue `[CAPACITY-SCALE]` | `#ops` channel notification |
| Secret rotation (§6) | GitHub issue `[SECRET-ROTATION]` | Secret manager audit log |
| Monitoring gap (§7) | `#ops` channel (real-time posts) | GitHub issue if gap > 1h |
| Scheduled job (§8) | Job execution log / channel | GitHub issue on failure |
| Rollback decision (§9) | War room issue (INCIDENT.md) | `#ops` channel |

### 10.2 Minimum Fields for a Valid Receipt

A receipt is **invalid** (procedure is considered incomplete) if it is missing any of:
- Timestamp (YYYY-MM-DD HH:MM WIB)
- Executing agent ID
- Outcome (SUCCESS / FAIL / PARTIAL)
- Any required field from the procedure-specific template in the relevant section

An agent posting "done" or "completed" without a structured receipt has not completed the procedure.

### 10.3 Retention

| Log Type | Retention Period | Storage |
|---|---|---|
| Daily health check receipts | 90 days | Ops channel + monthly digest issue |
| Incident and failure receipts | Indefinite | GitHub issues (never close, label `ops-log`) |
| Secret rotation receipts | 1 year minimum | GitHub issues + secret manager audit |
| Capacity scale decisions | 1 year minimum | GitHub issues |
| Job execution receipts | 30 days rolling | Job log table or channel |

### 10.4 Monthly Ops Review

On the first Monday of each month, generate a monthly ops digest issue:

```
[OPS-DIGEST] YYYY-MM — Monthly Operations Review
Agent: <agent-id>

Health checks: <N> run, <N> PASS, <N> FAIL
Deploy failures: <N>
Third-party outages: <N>, total duration <Nh>
DB migrations: <N> run, <N> failed
Capacity events: <N> warning, <N> critical, <N> emergency
Secret rotations: <N> scheduled, <N> emergency
Monitoring gaps: <N>, total duration <Nh>
Job failures: <N> total, <N> escalated
Rollbacks executed: <N>

Top 3 reliability risks identified this month:
1. <risk>
2. <risk>
3. <risk>

Action items:
| Item | Owner | Deadline |
|------|-------|----------|
| <item> | <agent> | YYYY-MM-DD |
```

Link this digest to the monthly OKR review (OKR.md).

---

## §11 — INTEGRATION WITH CORE LOOP

```
RELEASE.md (deploy) → RUNBOOK.md §2 (deploy failure) → INCIDENT.md (if SEV1/SEV2)
                                                              ↑
RUNBOOK.md §1 (daily checks) → anomaly detected → RUNBOOK.md §3/4/5/6/7/8
                                                              ↓
                                                    INCIDENT.md or GitHub issue
```

This file does **not** override INCIDENT.md. When a runbook procedure escalates to an incident:
1. Declare the incident in INCIDENT.md immediately.
2. Continue executing the relevant runbook procedure in parallel.
3. The incident IC takes command of recovery; the runbook provides the technical steps.
4. Runbook receipt is attached to the incident war room issue as a comment.

> 🚫 *"I checked it and it seemed fine" = no receipt = procedure not done.*
> ✓ *Structured receipt posted = procedure complete. No receipt = repeat the check.*
