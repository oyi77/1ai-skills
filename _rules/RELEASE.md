---
name: release
version: 1.0.0
severity: mandatory
scope: [ship, deploy]
pairs-with: [gate, plan, reviewer, incident]
description: Versioning, changelog, deployment checklist, and rollback protocol
---

# RELEASE.md — Versioning, Deployment & Rollback

> **Every deploy is a risk event. Manage it as one.**
> No deploy without a rollback plan. No release without a changelog. No version without a bump.

---

## §1 — VERSIONING STANDARD

All repos, rule files, and agent skill files use **Semantic Versioning: MAJOR.MINOR.PATCH**.

```
MAJOR  Breaking change — incompatible API, removed endpoint, company-wide rule overhaul,
       schema migration requiring data transformation, auth model change.
       → Owner approval required. Migration guide mandatory.

MINOR  New feature, new rule, new agent capability — backward compatible.
       → Standard review. Announce in #releases.

PATCH  Bug fix, clarification, typo correction, non-behavioral config tweak.
       → Self-review sufficient. No announcement required.
```

Rules:
- Version MUST be bumped before merging to main — not after.
- NEVER reuse a version number, even after rollback.
- Pre-release: `1.2.0-rc.1`, `2.0.0-beta.3` — not for production deploys.
- Core rule files (this repo) follow the same scheme as code.

---

## §2 — RELEASE TYPES

```
HOTFIX
  Trigger:    SEV1 or SEV2 incident (see INCIDENT.md §2)
  Path:       branch from main → fix → GATE.md GATES 0,4,6,10 → deploy → postmortem within 24h
  Review:     IC (Incident Commander) approval only — no full GATE required mid-incident
  Version:    PATCH bump
  Postmortem: MANDATORY — file within 24h of resolution, reference INCIDENT.md §5

REGULAR
  Trigger:    Planned milestone, sprint cadence, or feature completion
  Path:       all GATE.md gates → REVIEWER.md (COMPLEX) → staging → production
  Review:     Full GATE.md + Reviewer Agent for COMPLEX changes
  Version:    MINOR or PATCH

MAJOR
  Trigger:    Breaking change, company-wide rule change, incompatible API update
  Path:       PRD → PLAN → all GATE.md gates → REVIEWER.md full review →
              owner approval → migration guide → staging → production → announcement
  Review:     Owner approval is non-negotiable — no exceptions
  Version:    MAJOR bump
  Notice:     Announcement must go out BEFORE deploy, not after
```

---

## §3 — RELEASE CHECKLIST

Complete in order. Every step requires a literal receipt. No skipping.

```
[ ] 1. All issues in release milestone are CLOSED
        Bukti: [milestone URL or issue list with all closed]

[ ] 2. All GATE.md gates PASSED (GATE 0–15 or GATE 0,4,6,10 for hotfix)
        Bukti: [gate run output or GATE.md checklist completed]

[ ] 3. CHANGELOG.md updated (§4 format)
        Bukti: [diff of CHANGELOG.md showing new entry]

[ ] 4. Version bumped in all relevant files (package.json, pyproject.toml, rule frontmatter, etc.)
        Bukti: [grep output showing new version string]

[ ] 5. Reviewer Agent APPROVED — mandatory for COMPLEX, recommended for STANDARD
        Bukti: [APPROVED verdict from REVIEWER.md run, PR #N]

[ ] 6. Staging deploy verified — smoke test passed
        Bukti: [smoke test output or screenshot from staging]

[ ] 7. Rollback plan documented and verified (see §5)
        Bukti: [rollback plan written, location noted]

[ ] 8. Production deploy executed
        Bukti: [deploy log, commit hash, timestamp]

[ ] 9. Smoke test in production — all critical paths verified
        Bukti: [smoke test output from production]

[ ] 10. Release announcement posted (#releases channel or GitHub release)
         Bukti: [link to announcement]
```

Gate failure at any step = STOP. Do not proceed to next step until gate is cleared.

---

## §4 — CHANGELOG FORMAT

Every repo MUST maintain a `CHANGELOG.md` at root. Format: [keepachangelog.com](https://keepachangelog.com).

```markdown
# Changelog

## [Unreleased]

## [1.2.0] — 2026-07-04
### Added
- New capability or rule

### Changed
- Modified behavior — describe what changed and why

### Deprecated
- Features/rules that will be removed in a future MAJOR — document the alternative

### Removed
- Features/rules removed this release — was deprecated in prior version

### Fixed
- Bug fixed — reference issue number

### Security
- Vulnerability patched — reference CVE or issue; DO NOT describe the exploit in detail
```

Rules:
- `[Unreleased]` section always exists — merge entries to versioned section at release time.
- Every entry must be human-readable and agent-parseable.
- Security entries MUST always be present even if empty — agents scan this section.
- Reference issue numbers where applicable: `(#123)`.

---

## §5 — ROLLBACK PROTOCOL

**Every deploy MUST have a documented rollback plan written BEFORE deploy begins.**

```
ROLLBACK PLAN TEMPLATE (write this before §3 step 8)

Deploy:       [version, timestamp, what changed]
Trigger:      SEV1/SEV2 after deploy OR IC decision at any time
How to detect: [what signal means rollback is needed — error rate, revenue drop, health check fail]

Rollback steps (in order):
  1. [revert command / git revert SHA / feature flag toggle]
  2. [database down migration if schema changed]
  3. [cache flush if caching changed]
  4. [notify #incidents]
  5. [verify rollback: smoke test command]

Estimated rollback time: [N minutes]
Rollback owner: IC or on-call agent
```

Rules:
- Rollback plan MUST be stored in the PR description or a linked doc before merge.
- Rollback MUST be tested (dry-run or staging) quarterly — log the test result.
- Rollback trigger is always the IC's call — no waiting for data if situation is ambiguous.
- If rollback is impossible (irreversible migration), state that explicitly and require owner approval.
- "Rollback by redeploying old version" is acceptable ONLY if data integrity is unaffected.

---

## §6 — DEPLOYMENT RULES

```
FORBIDDEN
  ✗ Deploy on Friday (unless SEV1 — hotfix only)
  ✗ Deploy without smoke test plan documented
  ✗ Deploy without rollback plan documented (§5)
  ✗ Deploy without CHANGELOG.md updated
  ✗ Deploy without version bump committed
  ✗ Deploy MAJOR release without owner approval
  ✗ Deploy to production before staging verify passes

REQUIRED
  ✓ Deploy during business hours (Mon–Thu preferred) unless emergency
  ✓ At least one monitoring agent active during deploy window
  ✓ Slack/Telegram alert sent to #ops before production deploy begins
  ✓ All automated tests green before deploy trigger
  ✓ Feature flags OFF by default for new risky features
```

---

## §7 — POST-DEPLOY MONITORING

After every production deploy, a **30-minute watch window** is mandatory.

```
WATCH WINDOW PROTOCOL

Duration:   30 minutes minimum after production deploy completes
Watcher:    Monitoring agent or on-call agent — assigned before deploy starts
Signals to watch:
  - Error rate: baseline ± 20% acceptable; >50% spike → consider rollback
  - Latency p99: baseline ± 30% acceptable; >2× → investigate immediately
  - Revenue/conversion signals: any drop >10% vs prior 30min → escalate
  - Health check endpoints: must remain green throughout

At T+30:
  - If all signals nominal → close watch window, post "deploy nominal" to #releases
  - If any signal degraded → extend window, escalate to IC, follow INCIDENT.md

Auto-rollback:
  - Monitoring agent MAY trigger rollback autonomously if: error rate >200% baseline
    AND latency >3× baseline AND duration >5 minutes
  - All autonomous rollbacks → immediate #incidents notification + INCIDENT.md flow
```

---

## §8 — INTEGRATION WITH CORE LOOP

```
PLAN.md  →  GATE.md  →  REVIEWER.md  →  RELEASE.md §3  →  post-deploy §7
                                              ↓
                                       INCIDENT.md (if issues arise)
```

> 🚫 *"I'll document the rollback after" = rollback that never gets written.*
> ✓ *"No rollback plan = no deploy" — non-negotiable.*
