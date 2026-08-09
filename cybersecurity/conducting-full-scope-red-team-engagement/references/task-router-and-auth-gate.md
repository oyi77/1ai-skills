# Task Router + Case-Init Pattern (Auth-Gated Security Mission Control)

> **Pattern source:** [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) (MIT) — a security task routing pack for AI coding clients (Claude Code, Codex, Cursor, OpenCode). Condensed here as a client-neutral, license-compatible reference. Upstream details: `skills/MASTER-ROUTING.md`, `skills/config/routing.json`, `skills/ops/scope-contract.md`, `skills/ops/evidence-finding-path.md`.

## Why this pattern exists

AI agents given a security/reversing task don't know *which* methodology to open (jadx vs Frida vs IDA vs Burp), where tools live on
the machine, and — critically — whether they are **authorized** to touch the target. The reverse-skill repo solved this with a
three-pillar control loop:

1. **Route first, act second** — every task is classified into a named playbook (R0–R40) before any command runs.
2. **Auth gate before ACT** — a `scope.md` with `auth.status=granted` + a network profile must exist; until then, no target is touched.
3. **Evidence → Finding → Path** — every conclusion is backed by immutable evidence records with reproducible commands.

This is the same discipline as a real engagement RoE (Rules of Engagement), but enforced *by the agent itself* at the file level.

## The control loop

```text
User task
  → routing rules (single source of truth: routing table / routing.json)
  → PRIMARY playbook identified + one-line rationale
  → case-init: generate work/<case>/scope.md (auth + network_profile)
  → [HARD STOP] if auth.status != granted → no target ACT
  → open playbook SKILL.md → tooling check (tool-index, absent tools → bootstrap)
  → execute, appending timeline + workitems
  → conclusions written as Evidence → Finding → Path
  → review + report handoff (evidence graph review, hash verify)
```

## Key mechanics (portable to any repo)

### 1. Single-source routing table

Keep the routing matrix as **data, not prose**. A Markdown table or `routing.json` works; the invariant is:
- every scenario keyword maps to exactly one PRIMARY playbook,
- un-matched input falls back to a catch-all (e.g. "generic reverse R0"),
- ambiguity resolution rule documented (three axes: target type / user intent / toolchain).

### 2. Case contract (scope.md) — the auth gate

Before acting on any target, materialize a per-case scope file:

```markdown
# Case: {name}
- auth:
    legal: written_contract | bug_bounty_program | internal_authorization | lab_only
    status: granted |    # ← HARD GATE: must be granted before any target ACT
- network_profile: lab_only | authorized_target_only |    # controls what you may touch
- asset_types: [ ... ]
- lead_role: lead | specialist
```

Enforce with a guard script that **exits non-zero** unless the gate is satisfied (`case-guard.ps1` semantics: exit code 2 when not ready, ` -Force` degrades to warning only).

### 3. Evidence → Finding → Path chain

Evidence is **immutable, individually-stored, hash-pinned**, and each Finding must cite ≥1 Evidence.

```markdown
### E-{nnn}
- observed_at / source_type (command | screenshot | file | log | memory | network | manual)
- source_ref, content_hash (sha256 of artifact), artifact_path
- repro_command: {exact command, third-party runnable or explicitly offline}
- supersedes: E-{mmm} | none

### F-{nnn}
- severity: critical | high | medium | low | info
- category: vuln | misconfig | design | reverse_algo | bypass | other
- status: candidate | validated | false_positive | accepted_risk
- evidence_ids: [E-...]          # MUST ≥1
- confidence, impact, repro_steps, remediation
```

Design goals honored:
- Evidence records are **case-local files** (`work/<case>/evidence/E-*.md`) with a CLI append helper.
- A **read-only review pass** (`review_case.py --verify-hashes --strict`) verifies scope fields, evidence records, workitem/timeline refs, findings, paths and artifact hash matches **before handoff**.
- The final Path section narrates the chain Evidence → Finding → Path → report, so a reader (or another agent) can follow the reasoning without guesswork.

### 4. Tool index + bootstrap (no guesswork on paths)

- Tool availability is checked against a generated **tool-index** (gitignored, refreshed per platform).
- Missing tools → agent runs a **bootstrap script that installs from a known manifests only** — never guesses paths.
- Smoke test exists: verify + script parse + routing matrix (even with non-ASCII hints).

## Anti-patterns (what this pattern guards against)

| Anti-pattern | Trap |
|---|---|
| Act before authorization | Nothing touched until `scope.md` gate passes |
| Guessing a tool unsupported on host | tool-index / bootstrap replaces guesses |
| Unreproducible findings | every E has a `repro_command` |
| "Trust me" conclusions | Finding must bind ≥1 Evidence with hashes |
| Losing history | Timelines + workitems + handoff graphs are file artifacts |

## Porting checklist

- [ ] Routing table exists as structured config (table or JSON), with fallback rule
- [ ] `scope.md` generation step exists (case-init) before any target interaction
- [ ] Hard guard blocks ACT when `auth.status` not granted (exit non-zero)
- [ ] Evidence format with hash + repro_command + immutable files
- [ ] Finding MUST bind evidence (validated by review script)
- [ ] Read-only review/inspection script exists for pre-handoff verification
- [ ] Tool bootstrap from a manifest, no path guessing

## Attribution

Pattern condensed from `zhaoxuya520/reverse-skill` (MIT, © 2026 zhaoxuya520 — https://github.com/zhaoxuya520/reverse-skill).
Refer to upstream files `MASTER-ROUTING.md`, `skills/ops/scope-contract.md`, `skills/ops/evidence-finding-path.md` for canonical wording.