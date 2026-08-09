# Field Journal: Reusable Lessons-Per-Case (Learning Loop)

> **Pattern source:** [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) (MIT) — `skills/field-journal/`
> directory. A per-case "experience index" that makes every completed engagement a permanent, retrievable lesson for future
> agents. This reference documents the structure so it can be recreated on any working repo.

## When to use

- After completing a security/reversing/pentest case with non-trivial steps, a working methodology, or a hard-won fix
- At the start of a new task, to check "have we seen this before?"
- As the evidence/history layer alongside a router (see `task-router-and-auth-gate.md` in the red-team umbrella skill)

## Pattern anatomy

```
field-journal/
├── _index.md                  # searchable catalog (dated entries, scenario labels)
├── 2026-07-22_electron-bytenode-task.md   # real case entries, dated filename
├── ...
└── CONTRIBUTE-BACK.md         # rule: what gets written back upstream, what stays in-repo
```

### 1. `_index.md` — the lookup surface

New tasks begin by reading the index, not the entries. The index is organized **by scenario category** (APK/Android, Web/API,
binary/firmware, mobile, phishing…), each entry a link with a short title. This gives the agent a zero-cost pulse of "we have
done this before; read `2026-07-22*`."

### 2. Single entry format (fixed fields keep entries comparable)

```markdown
# YYYY-MM-DD title-of-experience

## Scenario
binary-analysis | web-pentest | mobile | firmware | …

## Goal
## Scope (anonymized)     # NEVER store raw credentials/targets/private data
## Roles
## Full execution chain  # numbered steps: what worked, what didn't
## Result / lessons      # the actual reusable knowledge
## Pitfalls
## Commands / evidence reference (optional file paths)
```

### 3. Anonymization is mandatory
The upstream `anonymization.md` defines this: entries cross environments, so company names, hosts, credentials, and private data
are redacted. Evidence commands stay, secrets don't.

## Anti-patterns this guards against

| Anti-pattern | What the journal does |
|---|---|
| Repeat mistakes on every engagement | Each case stores the pitfall once, indexed by scenario |
| Knowledge stuck in a single conversation | Entries are files — durable, searchable, shareable |
| Journal becomes noise | Deduplicate by scenario; seed cases marked `[seed]`, real cases by date |
| Private data leaks into shared notes | Anonymization pass before a field-journal commit |

## Porting checklist

- [ ] Create `field-journal/_index.md` with scenario buckets
- [ ] Establish single-entry template (goal, scope, chain, lessons)
- [ ] Tokenization/anonymization rule for all entries
- [ ] New case: append `YYYY-MM-DD_<theme>.md`, update index
- [ ] New task start: read index → load matching entry before planning

## Attribution

Pattern condensed from `zhaoxuya520/reverse-skill` (MIT, © 2026 zhaoxuya520 — https://github.com/zhaoxuya520/reverse-skill).
Upstream reference files: `skills/field-journal/_index.md`, `skills/field-journal/anonymization.md`, `skills/CONTRIBUTING.md`.