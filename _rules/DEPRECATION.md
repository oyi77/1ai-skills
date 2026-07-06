---
name: deprecation
version: 1.0.0
severity: mandatory
scope: [ship, ops, engineering]
pairs-with: [release, engineering, security, incident, gate]
description: Kill protocol for dead features, zombie APIs, stale tools, and orphaned code
---

# DEPRECATION.md — Kill Protocol for Dead Assets

> **Unused code is a liability, not a neutral asset.**
> If it is not earning its keep, schedule its death. If it is a security risk, kill it today.

---

## §1 — DEPRECATION TRIGGERS

An asset (API endpoint, feature, feature flag, internal tool, scheduled job, integration, rule file section) MUST enter the deprecation registry when ANY of the following conditions are met:

```
TRIGGER 1 — UNUSED
  Definition:  Zero invocations / zero active users for 30+ consecutive days
  Evidence:    Analytics, log query, or flag evaluation count = 0 for ≥30 days
  Exception:   Disaster recovery paths and break-glass tools are exempt from this trigger

TRIGGER 2 — REPLACED
  Definition:  Functionality is fully covered by a newer asset with equal or better capability
  Evidence:    New asset is live, tested, and handling 100% of the use case
  Requirement: Migration path from old → new must exist before deprecation is declared

TRIGGER 3 — REVENUE NEGATIVE
  Definition:  Asset costs more to maintain than it generates or enables
  Evidence:    Cost attribution (infra + agent hours) exceeds revenue attribution for 60+ days
  Threshold:   Negative margin confirmed for 2 consecutive billing cycles

TRIGGER 4 — SECURITY RISK
  Definition:  Asset has an unmitigated CVE, exposes attack surface, or fails current security
               standards and cannot be patched within 14 days
  Evidence:    SECURITY.md audit finding, CVE reference, or IC declaration
  Path:        Escalates to §9 Emergency Deprecation — normal timeline does not apply

TRIGGER 5 — OWNER DECISION
  Definition:  Human owner or owning agent explicitly decides the asset no longer fits strategy
  Evidence:    Decision logged in DECISION.md with rationale
  Constraint:  Customer-facing assets still require notice period per §3 regardless of reason
```

Any agent encountering an asset meeting a trigger MUST create a registry entry (§2) within 24 hours. Do not silently ignore it.

---

## §2 — DEPRECATION REGISTRY

Every deprecating asset MUST have one registry entry. Registry lives at `/.1ai/deprecation/registry.md`.

**Entry format:**

```markdown
## [DEP-NNNN] — Asset Name

| Field            | Value                                                      |
|------------------|------------------------------------------------------------|
| id               | DEP-NNNN (auto-increment)                                  |
| asset            | Full path or identifier (e.g. `GET /api/v1/orders/legacy`) |
| type             | api_endpoint | feature | feature_flag | tool | job | rule  |
| trigger          | unused | replaced | revenue_negative | security | owner_decision |
| trigger_evidence | Link to log query, issue, DECISION.md entry, CVE ID        |
| replacement      | Path/identifier of replacement, or `none`                  |
| customer_facing  | yes | no                                                      |
| declared_date    | YYYY-MM-DD                                                 |
| notice_sent_date | YYYY-MM-DD or `n/a`                                        |
| removal_date     | YYYY-MM-DD (target)                                        |
| status           | declared | notified | sunset | removed                     |
| owner_agent      | Agent ID responsible for executing removal                 |
| migration_guide  | URL or `n/a`                                               |
| notes            | Any caveats, blockers, or dependencies                     |
```

Rules:
- `id` is never reused — even after removal, the entry stays with `status: removed`.
- `removal_date` MUST be set at declaration time, not left blank.
- Registry MUST be committed to version control — it is the audit trail.
- A removal with no registry entry is a protocol violation; it becomes a debt item retroactively.

---

## §3 — CUSTOMER-FACING DEPRECATION

Customer-facing = any asset a paying user, external API consumer, or public integration depends on.

**Notice period requirements:**

```
MINOR CHANGE (behavior change, field rename, response format tweak)
  Minimum notice:  30 days before removal
  Communication:   In-app notice + email to affected users + CHANGELOG.md entry

ENDPOINT / FEATURE REMOVAL (the thing stops working)
  Minimum notice:  60 days before removal
  Communication:   Email to all affected users, API consumers, webhook subscribers
                   + deprecation warning in API response headers (§5)
                   + migration guide published before notice is sent

BREAKING API CHANGE (v1 → v2, auth model change, schema overhaul)
  Minimum notice:  90 days before v1 is sunset
  Communication:   All of the above + owner approval required before notice is sent
```

**Communication template (adapt, do not skip fields):**

```
Subject: [BerkahKarya] Deprecation Notice — [Asset Name] — Removal on [DATE]

We are deprecating [asset name] on [removal date].

What is changing:
  [Describe exactly what will stop working]

Why:
  [Honest reason — replaced by X / security / strategic]

What you should do:
  [Concrete migration steps, numbered]
  [Link to migration guide]

Need help?
  [Contact channel — support email or Telegram]

Timeline:
  [Date]: Deprecation warning added to API responses
  [Date]: Final reminder sent
  [Date]: Asset removed / sunset
```

Rules:
- Migration guide MUST be published and linked BEFORE the notice is sent — never send notice to a dead link.
- Send a reminder 14 days before removal date.
- Send a final reminder 3 days before removal date.
- Do not extend removal date more than once without owner approval — repeated extensions erode trust.

---

## §4 — INTERNAL DEPRECATION (NO CUSTOMERS)

Internal assets (internal tools, admin scripts, agent-only APIs, internal feature flags, cron jobs) follow a faster path.

**Required steps — no exceptions:**

```
[ ] 1. Registry entry created (§2) with customer_facing: no
[ ] 2. Owning agent notified via irc broadcast or #ops channel
[ ] 3. Dependent agents identified via grep/codebase scan — zero undiscovered dependents allowed
[ ] 4. All dependents migrated or confirmed no longer dependent
[ ] 5. 7-day hold after dependents cleared — allows any missed dependent to surface
[ ] 6. Removal executed (§7)
[ ] 7. Registry entry updated to status: removed
```

What is NOT required for internal deprecation:
- External communication
- 30/60/90-day notice windows
- Migration guide (but replacement reference in registry is still required if a replacement exists)

The 7-day hold is the minimum — agents MUST NOT skip it because "nothing depends on this."

---

## §5 — API DEPRECATION

APIs require additional signals layered on top of §3 and §4 procedures.

**Versioning:**
- New major API version (v2) MUST be live and stable before v1 deprecation is declared.
- Version in URL path (`/api/v2/`) is the standard — header versioning is secondary.
- Both versions MUST run in parallel for the full notice window.

**Sunset header protocol:**

Add these headers to every response from a deprecated endpoint, starting on declared_date:

```
Deprecation: true
Sunset: <HTTP-date of removal, e.g. Sat, 04 Oct 2026 23:59:59 GMT>
Link: <https://docs.berkahkarya.com/migration/v1-to-v2>; rel="deprecation"
```

- `Sunset` header MUST be a fixed date — not a duration.
- Headers MUST appear on every response, not just errors.
- Monitoring agent MUST alert if deprecated endpoint traffic is still >5% of v2 traffic at T-14 days.

**Backward compatibility window:**

```
Patch-level changes:    No new version required — backward compatible always
Minor additions:        No new version required — additive changes only
Breaking changes:       MAJOR version bump required, v(N-1) kept alive for full notice window
v(N-2) and older:       Can be removed with only 14-day notice IF v(N-1) is already deprecated
```

---

## §6 — FEATURE FLAG CLEANUP

Feature flags accrete silently. Every flag older than 90 days MUST be reviewed.

**Staleness threshold:**

```
< 30 days:    Active development — no action
30–90 days:   Review required — is the rollout complete? Is the flag still toggled?
> 90 days:    Flag is stale — must be REMOVED or JUSTIFIED
> 180 days:   Flag is zombie — removal is mandatory, no justification accepted
```

**Removal criteria (flag MUST be removed when):**
- Feature is 100% rolled out (flag always evaluates to `true`) → bake in the code, delete the flag
- Feature was killed (flag always evaluates to `false`) → delete the flag and the dead code branch
- Rollout completed > 90 days ago with no incidents
- Flag owner cannot be identified after a 7-day inquiry

**Flags that MAY stay beyond 90 days (require explicit justification in registry):**
- Kill switches for emergency rollback of revenue-critical features (justify with incident history)
- A/B tests with documented ongoing experiment — must have end date set

**Removal process:**
1. Set flag to its final value for 48 hours (full true or full false) — watch for errors.
2. Remove the flag evaluation from code + delete the dead branch.
3. Delete the flag from the feature flag service.
4. Remove the registry justification entry if one existed.

---

## §7 — DEAD CODE REMOVAL

**Detection methods (run during §8 cadence review):**

```
Code coverage analysis:   Identify modules/functions with 0% coverage for 60+ days
Import graph analysis:    Find files with no importers — candidates for deletion
API log analysis:         Endpoints with zero calls for 30+ days (§1 Trigger 1)
Feature flag audit:       Dead branches behind always-false flags (§6)
Dependency scan:          Packages listed in package.json / pyproject.toml not imported anywhere
```

**Required review before deletion:**
- Dead code MUST be confirmed dead by a second agent or automated analysis — one agent's conclusion is not sufficient.
- For any file >200 lines, the reviewing agent MUST read it and confirm no hidden side effects (init hooks, global state, event listeners).
- Check git blame: if the code was written in the last 90 days, consult the authoring agent before deleting — it may be in-progress.

**Deletion steps:**
1. Create registry entry (§2) with type: `code` and trigger: `unused`.
2. Open a PR with ONLY the deletion — no mixing dead code removal with feature work.
3. PR description MUST list every file/function removed and the evidence of disuse.
4. Merge to main.
5. **Rollback window: 14 days** — if any runtime error surfaces traceable to the deletion, revert immediately.
6. After 14 days with no incidents, close the registry entry as `status: removed`.

---

## §8 — DEPRECATION REVIEW CADENCE

**Scheduled reviews:**

```
WEEKLY (every Monday, automated)
  - Flag evaluation counts exported and checked against §6 staleness thresholds
  - API endpoint call counts checked for zero-call candidates (Trigger 1)
  - Any candidate meeting a trigger → registry entry created within 24h

MONTHLY (first Monday of month, owning agent)
  - Review all registry entries with status: declared or status: notified
  - Confirm removal_date is still accurate; escalate if slipping
  - Confirm migration guide is still valid for all notified items
  - Report: count of items per status, count overdue

QUARTERLY (first Monday of quarter, owner review)
  - Full dead code scan (§7 detection methods)
  - Full feature flag audit (§6 staleness check)
  - Dependency graph analysis — remove unused packages
  - Owner reviews and approves the removal plan for any MAJOR deprecations
  - Output: updated registry + prioritized removal backlog for next quarter
```

The monthly and quarterly reviews MUST produce a written report committed to `/.1ai/deprecation/reviews/YYYY-MM.md`. An empty report ("nothing to report") is still a valid and required output.

---

## §9 — EMERGENCY DEPRECATION

**Triggers for emergency path:**
- Asset has an actively exploited vulnerability
- Asset is leaking PII or secrets in production right now
- Asset is causing active revenue loss due to malfunction (not just low revenue)
- IC declares emergency in INCIDENT.md

**Expedited protocol (clock starts at declaration):**

```
T+0h    IC or security agent declares emergency deprecation in #incidents
         Registry entry created with trigger: security, status: declared
         Owner notified immediately

T+0h–2h Assess blast radius: how many customers are affected? Is removal safe?
         Two options: (a) kill immediately, (b) kill after 24h customer notice
         If data loss or service disruption for customers → option (b)
         If active attack or active leak → option (a), always

T+2h    If option (a): asset is killed. Affected customers notified after removal,
         not before. Post-facto notice sent within 1h of removal.
         If option (b): 24h notice sent to customers with exact removal timestamp.
         Sunset headers added immediately.

T+24h   Asset removed (option b path)
         Post-mortem opened within 24h (INCIDENT.md §5)
         Registry entry updated to status: removed

Post-mortem must address:
  - Why was this not caught earlier?
  - What detection rule would have caught it sooner?
  - Was there a compensating control gap?
```

Normal notice windows (§3) are suspended for emergency deprecation. Owner approval is required before T+2h assessment, but cannot block asset removal if option (a) is chosen and IC confirms active harm.

---

## §10 — ANTI-PATTERNS

The following behaviors are protocol violations. Any agent observing them MUST file a DECISION.md entry and flag it in the next review.

```
✗ SILENT REMOVAL
  Removing an asset from code or config without a registry entry, without notice,
  and without a PR. This is indistinguishable from an accident and creates ghost failures.

✗ REMOVAL WITHOUT MIGRATION PATH
  Deleting a customer-facing asset with no documented replacement or migration guide.
  "Just stop using it" is not a migration path.

✗ DEPRECATION WITHOUT EVIDENCE
  Declaring Trigger 1 (unused) based on intuition rather than log/analytics evidence.
  The evidence field in the registry MUST have a real link or query result.

✗ INFINITE EXTENSIONS
  Moving removal_date more than once without owner approval. This signals the asset
  is not actually being deprecated — close the entry or get a decision.

✗ MIXING REMOVAL WITH FEATURE WORK
  Including dead code deletion in a PR that also ships new features.
  Dead code removal is always a standalone PR — mixed PRs obscure the audit trail.

✗ SKIPPING THE 7-DAY HOLD (internal) OR NOTICE WINDOW (external)
  "Nothing depends on this" is not a valid reason to skip the hold.
  The hold exists precisely for the cases you didn't think of.

✗ DELETING FEATURE FLAG WITHOUT REMOVING DEAD BRANCH
  Removing a flag from the flag service but leaving the unreachable code branch in place.
  Half-removal creates dead code with no flag evidence trail.

✗ REUSING DEP IDs
  Once assigned, a DEP-NNNN ID belongs to that asset permanently in the registry,
  even after removal. Never reassign.

✗ DEPRECATING WITHOUT OWNER APPROVAL FOR MAJOR EXTERNAL CHANGES
  Any deprecation that affects paying customers and constitutes a breaking change
  requires explicit owner approval before the notice is sent. Agent authority does not
  extend to unilateral breaking changes to customer contracts.
```

---

> 🚫 *"It's probably not used" is not evidence. Check the logs.*
> ✓ *"Zero calls in 30 days, here's the query" — that's a registry entry.*
