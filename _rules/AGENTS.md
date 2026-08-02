---
scope: core
depends_on: []
status: partial
---

# AGENTS.md — core

## Tujuan Folder Ini

Org-wide rules hub: the single source of truth for every agent/human operating in the organization. Contains the protocol docs (ENGINEERING, PLAN, GATE, RULES, QA, REVIEWER, ...), policy docs (SECURITY, FINANCE, COMMS, HIRING, ...), a verification receipt (`VERIFICATION.md`), an anti-pattern catalog, and `checksums.sha256` for integrity. No org-specific content — org overrides live in `/org`.

## Ekspor / Interface Utama

- `RULES.md` — compact one-file rules (injected into every agent session)
- `ENGINEERING.md` — full lifecycle protocol (AUDIT→THINK→...→REVIEW)
- `GATE.md` — pre-ship compliance gate (7 gates + 11 cross-ref checks C1–C11)
- `VERIFICATION.md` — receipt enforcement ("show output or not done")
- `PLAN.md`, `QA.md`, `REVIEWER.md`, `ANTI-PATTERNS.md`, `SURPASS.md`, `DOCS.md`, `LEARN.md`, `MULTI_AGENT.md`, `ROLES.md`, `HIRING.md`, `FINANCE.md`, `COMMS.md`, `SECURITY.md`, `OKR.md`, `DECISION.md`, `INCIDENT.md`, `RELEASE.md` — see root AGENTS.md File map
- Additional docs present: `COST_TRACKING.md`, `HUMAN_ESCALATION.md`, `MEMORY.md`, `PRIORITY.md`, `REGISTRY.md`, `SUBAGENT_MEMORY.md`, `SESSION_TRACING.md`, plus legacy files (`PATTERNS.md`, `DD.md`, `WNN.md`, `NNN.md`, `INDEX.md`, `UX_AUDIT.md`) and `tests/rules/` (rules-engine test fixtures)
- `checksums.sha256` — integrity manifest

## Dependensi Internal

- Depends on: none (self-contained rules)
- Depended by: `/bin`, `/scripts`, `/hooks`, `/test`, `/remediate`, `/templates`, root AGENTS.md — hub of the reference graph (GATE.md: 9 in-edges, REVIEWER.md: 8, ROLES.md: 7)

## Issue Spesifik

- [Medium] **Checksum gap** — [RESOLVED 2026-08-01]: manifest rebuilt to cover all markdown files; `sha256sum -c checksums.sha256` reports OK for every entry.
- [Medium] **Frontmatter inconsistency** — [RESOLVED 2026-08-01]: `COST_TRACKING.md`, `HUMAN_ESCALATION.md`, `MEMORY.md`, `SESSION_TRACING.md`, `SUBAGENT_MEMORY.md` all gained YAML frontmatter (name, version 1.0.0, severity, scope [all]) matching repo convention.
- [Medium] **Dead references** — [RESOLVED 2026-08-01]: `VERIFICATION.md` tak lagi menyebut `RULE_CODING_AGENT`/`RULE_AGENT_REVIEWER.md` (grep = 0 hit); jalur receipt kini memakai QA.md §7 Evidence Requirements (VERIFICATION.md:244), ENGINEERING.md §9 Conflict Resolution (:250), dan QA.md/ENGINEERING.md/SURPASS.md (:12). File legacy (`PATTERNS.md`, `DD.md`, `WNN.md`, `NNN.md`, `INDEX.md`, `UX_AUDIT.md`) masih ada sebagai legacy — lihat Ekspor line 20.
- [Low] Root AGENTS.md File map omits ~23 files that exist in `core/`; the map understates the actual catalog.

## Rekomendasi Perbaikan Scoped

```bash
# [APPLIED 2026-08-01] Rebuild checksum manifest (dilakukan setelah edit AGENTS.md final)
#   cd core && sha256sum *.md > checksums.sha256 && sha256sum -c checksums.sha256
```

```bash
# Verify a dead ref before cleanup (example)
#   grep -rn "RULE_CODING_AGENT" core/        # find all referrers
#   grep -rln "PATTERNS.md\|DD.md" core/      # find referrers of legacy files
```

> Last updated: 2026-08-01 — checksum gap, frontmatter 5 file, dan dead ref VERIFICATION.md di-resolve; manifest regen setelah edit final; [Low] root file map masih open.
