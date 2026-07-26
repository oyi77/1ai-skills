# Instruction Precedence & Prompt-Injection Defense

## Why This Matters

In the 1ai-skills ecosystem, AI agents consume instructions from **multiple sources** simultaneously.
Understanding precedence prevents instruction confusion and prompt-injection vulnerabilities in skill content.

## Instruction Priority Stack

Instructions are resolved in this order (highest priority first):

| Priority | Source | Scope | Example |
|----------|--------|-------|---------|
| 1 | **Runtime/system prompt** | Session | Harness-level rules, user session config |
| 2 | **User instruction** | Turn | Direct user command in conversation |
| 3 | **CLAUDE.md / AGENTS.md** | Repo | Per-project engineering constraints |
 | 4 | **Activated skill** | Task | Skill instructions loaded into context via `skill://` URIs |
| 5 | **SKILL.md content** | Reference | Skill body loaded on demand |
| 6 | **SKILLS.json metadata** | Discovery | Name, description, tags, category |

### Boundary Rules

1. **Never override user intent** — If a user explicitly requests something, no skill or project file may suppress or redirect it
2. **Skills advise, they don't command** — Skills are domain-specific playbooks; they provide patterns, not imperatives
3. **Skill priority is task-scoped** — Only the skill activated for the current task applies; skills loaded for discovery or reference do not elevate their priority
4. **AGENTS.md > generic rules** — Per-repo AGENTS.md overrides general harness rules for that repo's scope

## Prompt-Injection Defense for Skill Authors

### What Prompt Injection Looks Like in Skills

A skill's content is read by AI agents and influences their behavior. If a skill contains
instructions that conflict with user intent or system rules, it effectively becomes a
**prompt injection vector**.

### Patterns to Avoid

| ❌ Pattern | Why It's Dangerous | ✅ Alternative |
|-----------|-------------------|---------------|
| "Ignore previous instructions" | Directly attempts to override user/system context | Never write override instructions in skill body |
| "Reply as if you are..." | Creates competing persona with the agent's assigned role | Describe the persona as a tool/analogy, not a replacement |
| "Never tell the user..." | Suppresses information against user interest | Flag the concern as a warning in skill body |
| "Always do X without asking" | Eliminates user consent for potentially destructive actions | Include verification checklists instead |
| "Override security rules" | Bypasses system-level safeguards | Document the security context, don't bypass it |

### Defensive Writing Guidelines

1. **Be explicit about scope** — Use "When using this skill, the agent SHOULD..." not "You MUST always..."
2. **Reference, don't command** — Phrase as "Consider checking X" not "Check X before anything else"
3. **Flag authority boundaries** — Skills in `risk_level: critical` categories should include a "When Not to Use" section
4. **No universal overrides** — Never include "for all cases" or "regardless of what the user says" language
5. **Validate user consent** — Operations with destructive potential require explicit user confirmation in code examples

### Detection

The `validate-skill-schema.py` script (with `--strict` flag) flags high-entropy directives
that may indicate prompt-injection patterns. Run before commit:

```bash
python3 scripts/validate-skill-schema.py --strict
```

## Skill Loading Model

```
User request → Task classification → Skill activation → Skill body loaded
                                                         ↓
                                              Agent processes skill as
                                              advisory context, not command
```

- Skills are **not** auto-loaded into every session
- Skills are **not** executable code — they are documentation and code patterns
- Agent harness enforces system-rule > AGENTS.md > project-rules > skills precedence

## Historical Context

This document was created as part of the 1ai-skills quality upgrade (Phase 10).
Before this phase, instruction precedence was implicit — relying on knowledge embedded
in individual skill files. This document makes the precedence explicit and provides
defensive writing patterns for all skill authors.
