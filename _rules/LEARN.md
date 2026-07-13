---
name: learn
version: 3.2.0
severity: recommended
scope: [post-incident, improvement]
pairs-with: [anti-patterns, engineering]
description: Retrospective and rule update protocol — turning incidents into permanent fixes
---

# LEARN.md — Retrospective & Rule Update Protocol

> **Every incident is a gift — if you learn from it.**
> This protocol ensures every failure becomes a permanent improvement.
> A bug you don't codify is a bug you'll see again.

---

## §1 — WHEN TO RUN THIS PROTOCOL

Trigger the LEARN protocol after:
- A bug that shipped to production
- A bug that was caught in review (close call)
- An AI agent failure (hallucination, overclaim, wrong decomposition)
- A process failure (missed gate, skipped verification)
- A user reports unexpected behavior
- A deployment rollback

---

## §2 — THE RETROSPECTIVE TEMPLATE

After any incident, fill this out:

```markdown
# Retrospective: [incident name]
Date: [YYYY-MM-DD]
Severity: [BLOCKER / HIGH / MEDIUM / LOW]

## What happened
[Factual description — what was observed, not what you think happened]

## Timeline
- [time] — [event]
- [time] — [event]
- [time] — [resolved]

## Root cause
[The actual root cause — not the symptom. Use "5 Whys" if needed.]

## What we learned
[The insight that prevents recurrence]

## Action items
- [ ] Rule update: [which rule file, what change]
- [ ] Enforcement update: [gate/hook/CI change]
- [ ] Anti-pattern: [add AP-NNN to ANTI-PATTERNS.md]
- [ ] Other: [anything else]

## Confidence
[ ] This can't happen again (rule + enforcement in place)
[ ] This is less likely (rule in place, enforcement partial)
[ ] This could happen again (analysis only, no rule yet)
```

---

## §3 — HOW INCIDENTS BECOME RULES

```
INCIDENT
    ↓
RETROSPECTIVE (fill template above)
    ↓
ANALYSIS: Is this a one-off or a pattern?
    ↓
ONE-OFF → Document, close, move on
PATTERN → Add to ANTI-PATTERNS.md
    ↓
Does an existing rule cover this?
    ↓
YES → Update enforcement (gate/hook/CI) to catch it
NO  → Write new rule or add to existing rule
    ↓
Update GATE.md if the rule maps to a pre-ship check
Update REVIEWER.md if the rule maps to a review checklist
    ↓
TEST: Does the new rule/enforcement actually catch the pattern?
    ↓
Commit: "learn: [description]"
```

---

## §4 — RULE UPDATE FORMAT

When updating a rule file based on a retrospective:

1. **Add to the appropriate rule file** — don't create a new file for each incident
2. **Cite the incident** — link to the retrospective or describe it
3. **Update frontmatter version** — bump the patch version
4. **Update ANTI-PATTERNS.md** — add the new anti-pattern entry
5. **Update enforcement** — add to GATE.md if it's a pre-ship check

Commit message format:
```
learn: [rule file] — [what was added/changed]

Ref: [retrospective date or incident description]
```

---

## §5 — WEEKLY SYNTHESIS (optional)

For teams, run a weekly synthesis:

1. Review all retrospectives from the past week
2. Identify patterns across incidents
3. Check if anti-patterns are recurring
4. Update rules proactively (not just reactively)
5. Share findings with the team

---

## §6 — THE LEARNING LOOP

```
     ┌──────────────────────────────────────────┐
     │                                          │
     ▼                                          │
  INCIDENT ──→ RETROSPECTIVE ──→ ANALYSIS ──→ RULE UPDATE
                                               │
                                               ▼
                                          ENFORCEMENT
                                          (gate/hook/CI)
                                               │
                                               ▼
                                          VERIFICATION
                                          (does it catch it?)
                                               │
                                               ▼
                                          ANTI-PATTERN
                                          CATALOG
                                               │
                                               └──── (next incident uses this as baseline)
```

The goal: **the framework gets smarter with every incident.** Each failure makes the next one less likely.

---

> 💡 *"A team that learns from one bug per week is 52x better at the end of the year."*
>
> ⚠️ *"If the same anti-pattern appears twice, the enforcement is broken — not the agent."*
>
> 🚫 *"Closing a retrospective without a rule update is closing a wound without stitches."*

---

## §7 — PROACTIVE LEARNING (no incident required)

The LEARN protocol is not only reactive. Agents MUST also run proactive learning when:

| Trigger | Frequency | Output |
|---|---|---|
| Weekly synthesis of all retrospectives | Every Monday | Append to `logs/learn/weekly-YYYY-WNN.md` |
| Any pattern repeats ≥ 2× in ANTI-PATTERNS.md | On detection | File a rule-update proposal in GitHub Issues with label `rule-improvement` |
| A dependency or tool is replaced or upgraded | On upgrade | Update relevant rule files to reflect new behavior; add migration note |
| An agent produces a PARTIAL or FAIL result 2× in a row on the same task type | On detection | File retrospective, propose enforcement change |
| New technique or pattern proves more effective than the documented approach | On first confirmation | Propose rule update; do not change rules unilaterally — file the issue |

**Proactive retrospective format:** Same template as §2, but set `Severity: INFO` and `What happened:` to "Proactive review — no incident." Fill in `What we learned` and `Action items` normally.

---

## §8 — EXTERNAL SIGNAL INTAKE

Agents learn from the outside world, not just internal failures. External signals MUST be monitored and processed.

### Signal Sources

| Source | What to watch for | Check cadence | Action on signal |
|---|---|---|---|
| Competitor product updates (SURPASS.md §2) | New features, pricing changes, deprecations | Weekly (SURPASS research cycle) | Update FEATURE_MATRIX.md; flag P1 gaps |
| Dependency changelogs (npm/pip/cargo release notes) | Breaking changes, security patches, deprecations | On dependency update or weekly scan | File GitHub Issue: upgrade or mitigate |
| CVE feeds (NIST NVD, GitHub Security Advisories) | Any CVE affecting a dependency in the stack | Daily (Monitoring Agent) | File P0 Issue if CVSS ≥ 7.0; P1 if 4.0–6.9 |
| User feedback (support emails, reviews, social) | Recurring pain points, feature requests, confusion | Weekly | Triage into GitHub Issues; tag `user-feedback` |
| Industry pattern shifts (LLM model updates, platform policy changes) | Anything that changes how a core tool or platform works | Monthly | File a review issue; update relevant rules if behavior changes |

### Intake Protocol
1. **Capture** — Log signal in `logs/learn/external-signals/YYYY-MM-DD.md`: source, date, summary, relevance.
2. **Triage** — Classify: Urgent (act within 24h), Important (act this sprint), Monitor (track, no action yet).
3. **Act** — For Urgent/Important: file a GitHub Issue. For Monitor: add to weekly synthesis.
4. **Close** — Once acted on, mark the signal entry `[PROCESSED]` with a link to the GitHub Issue.

**Do not let signals expire unprocessed.** A signal not triaged within 7 days of capture is an SLA breach — file a LEARN retrospective on the signal itself.
