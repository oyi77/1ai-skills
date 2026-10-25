---
name: incident
version: 1.0.0
severity: mandatory
scope: [all]
pairs-with: [comms, roles, gate, security]
description: Incident severity levels, response protocol, war room, and postmortem
---

# INCIDENT — Incident Response Protocol

## §1 INCIDENT DEFINITION

An **incident** is any unplanned event that degrades or blocks production service, causes data loss, or violates security — and requires coordinated response outside normal sprint work.

| Category | Is Incident? | Route |
|---|---|---|
| Production service down or degraded | YES | Declare immediately |
| Security breach or suspected breach | YES | Declare immediately → SECURITY.md |
| Data loss or corruption (any amount) | YES | Declare immediately |
| Revenue pipeline blocked | YES | Declare immediately |
| Feature broken in non-critical path | NO | File bug, add to sprint backlog |
| Performance regression < 20% | NO | File bug, priority label |
| Cosmetic or UX issue | NO | File task |

**Declaration threshold:** When in doubt, declare. Downgrading a declared incident is cheaper than missing a real one.

---

## §2 SEVERITY LEVELS

### SEV1 — Critical (Immediate response)
- Production fully down
- Active security breach or confirmed data exfiltration
- Data loss (any production data)
- Payment/revenue pipeline completely blocked
- **Response target:** IC engaged within 5 minutes, human owner notified within 10 minutes

### SEV2 — High (Response within 1 hour)
- Major feature broken affecting >20% of users or flows
- Significant performance degradation (>50% latency increase, error rate >5%)
- Partial outage (some users cannot complete critical flows)
- Suspected but unconfirmed security issue
- **Response target:** IC assigned within 15 minutes, investigation started within 1 hour

### SEV3 — Medium (Response within 24 hours)
- Non-critical feature broken (workaround exists)
- Degraded user experience without total failure
- Integration failure with non-critical external service
- **Response target:** Issue filed and triaged within 4 hours, fix started within 24 hours

### SEV4 — Low (Scheduled fix)
- Minor bug with minimal user impact
- Cosmetic issue
- Non-blocking developer experience issue
- **Response target:** Filed and prioritized in next sprint planning

---

## §3 INCIDENT RESPONSE PROTOCOL

Execute steps in order. Do not skip steps for SEV1/SEV2.

### Step 1 — DETECT
- Source: automated alert (monitoring, error tracking), agent self-report, human report
- Agent receiving alert: immediately assess severity using §2 criteria
- If severity uncertain, assume SEV2 until evidence shows otherwise

### Step 2 — DECLARE
- Create GitHub issue immediately with title: `[INCIDENT][SEV{N}] <short description>`
- Apply labels: `incident`, `sev1`/`sev2`/`sev3`/`sev4`
- Record: detection time, reporter, initial symptoms
- SEV3/SEV4: issue creation is sufficient; proceed to normal workflow

### Step 3 — ASSIGN INCIDENT COMMANDER (IC)
- For SEV1/SEV2: first available agent capable of coordinating declares themselves IC in the issue
- IC has override authority: can halt feature work, reassign agents, roll back deployments
- IC is single point of coordination — no parallel decision chains
- IC identity must be stated in the war room issue (§4)

### Step 4 — NOTIFY
- Follow COMMS.md §5 notification matrix
- **SEV1:** Human owner notified immediately via all available channels — no delay permitted
- **SEV2:** Human owner notified within 15 minutes
- **SEV3/SEV4:** No human interrupt required; update in daily summary
- Notification message must include: severity, affected system, impact, IC name, war room link

### Step 5 — INVESTIGATE
- IC assembles timeline of events leading to incident
- State working hypothesis for root cause in war room issue
- Identify: what changed, when it changed, what monitoring confirms
- Do not conflate hypothesis with confirmed cause — label clearly

### Step 6 — CONTAIN
- Stop the bleeding before fixing root cause
- Preferred actions in order: rollback deploy → disable feature flag → kill switch → scale down affected component
- Containment = incident no longer actively worsening
- State containment action and time in war room issue
- Partial containment is acceptable; document what remains uncontained

### Step 7 — FIX
- Root cause fix only — do not add unrelated changes under cover of incident
- All fix commits reference the incident issue number
- SEV1/SEV2 fixes require second-agent review unless IC certifies solo fix is safe (documented)

### Step 8 — VERIFY
- Confirm fix with concrete evidence: monitoring screenshots, test output, curl responses, error rate graphs
- "Should be fixed" is not verification
- Human confirmation required for SEV1 before declaring resolved

### Step 9 — COMMUNICATE RESOLUTION
- Post resolution update to war room issue
- State: what was fixed, evidence of fix, any remaining risk
- Notify same channels used in Step 4 with resolution message
- Close incident issue only after resolution confirmed

### Step 10 — POSTMORTEM
- **SEV1:** Mandatory within 48 hours of resolution
- **SEV2:** Mandatory within 72 hours of resolution
- **SEV3/SEV4:** Optional, at IC's discretion
- Use template in §5
- Postmortem output filed as separate issue linked to incident issue

---

## §4 WAR ROOM

For SEV1 (and optionally SEV2), the incident GitHub issue is the war room.

**War room rules:**
- Every update, decision, and action posted as comment with timestamp
- IC posts status update every 15 minutes minimum during active SEV1
- No side channels — all incident communication in the war room issue
- Single IC at all times; if IC must hand off, handoff explicitly stated in issue
- No feature discussion, no unrelated work — war room is incident-only
- Checklist in opening comment:
  - [ ] IC assigned
  - [ ] Human notified
  - [ ] Containment achieved
  - [ ] Root cause identified
  - [ ] Fix deployed
  - [ ] Fix verified
  - [ ] Resolution communicated
  - [ ] Postmortem scheduled

---

## §5 POSTMORTEM TEMPLATE

```markdown
## Postmortem: [INCIDENT][SEV{N}] <title>

**Date:** YYYY-MM-DD
**Incident duration:** HH:MM
**Severity:** SEV{N}
**IC:** <agent id>
**Prepared by:** <agent id>

### Timeline
| Time | Event |
|------|-------|
| HH:MM | <event> |

### Root Cause (5 Whys)
1. Why did X happen? → Because Y
2. Why did Y happen? → Because Z
3. ... (continue until systemic cause reached)

**Root cause conclusion:** <one sentence>

### Impact
- Users affected: <number or estimate>
- Revenue impact: <estimate or N/A>
- Data affected: <none / describe>
- Duration of degradation: <HH:MM>

### What Worked
- <detection mechanism caught it>
- <rollback procedure worked as expected>

### What Failed
- <monitoring gap>
- <missing kill switch>
- <slow notification>

### Action Items
| Item | Owner | Deadline | Issue # |
|------|-------|----------|---------|
| <action> | <agent> | YYYY-MM-DD | #N |
```

---

## §6 INCIDENT METRICS

Track monthly in a dedicated metrics issue or dashboard:

| Metric | Definition | Target |
|---|---|---|
| MTTD | Mean time from incident start to detection | < 5 min (SEV1), < 30 min (SEV2) |
| MTTR | Mean time from detection to resolution | < 1 hr (SEV1), < 4 hr (SEV2) |
| Incident rate | Number of SEV1/SEV2 per month | Trending down |
| Postmortem completion | % of required postmortems filed on time | 100% |

Review metrics in monthly OKR review (OKR.md). Negative trends trigger proactive review.

---

## §7 FORBIDDEN DURING INCIDENT

While a SEV1 or SEV2 is active and uncontained:

- **NO** feature work by any agent
- **NO** non-incident commits to production branches
- **NO** deploys unrelated to the incident
- **NO** architectural discussions or planning sessions
- **NO** parallel incident commanders — one IC only
- **NO** resolving the incident without human confirmation (SEV1)

IC has authority to enforce these rules. Any agent defying IC authority during incident is in violation of ROLES.md and must escalate to human owner immediately.

Violations logged in war room and reviewed in postmortem.
