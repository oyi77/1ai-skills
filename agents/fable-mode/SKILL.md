---
name: fable-mode
description: >
  Enforce staged execution discipline on large tasks: written stage plan, parallel sub-agent
  delegation, failable verification at each stage, and skeptical self-review before delivery.
  Use when tasks span multiple files, multiple sources, or multiple sessions. Also triggers
  on "do this thoroughly", "be systematic", "deep work mode", "be thorough".
domain: agents
tags:
  - agent-orchestration
  - execution-discipline
  - sub-agents
  - verification
  - planning
  - self-review
source: https://github.com/mrtooher/fable-mode
stars: 578
---
# Fable Mode — Staged Execution Discipline

A Claude skill that enforces staged execution discipline on large tasks: a written stage plan, parallel delegation where the runtime allows, a failable verification check at each stage, and a skeptical self-review before delivery.

Complements [1ai-rules](~/.1ai/core/RULES.md) engineering protocol — fable-mode shapes the execution procedure, 1ai-rules provides the engineering gates.

## When to Use

**Trigger phrases:**
- "do this thoroughly" · "be systematic" · "deep work mode" · "be thorough"
- "fable mode" · "staged execution" · "systematic approach"
- Tasks spanning multiple files, sources, or sessions
- When the user explicitly asks for disciplined execution

**When NOT to use:**
- Tasks with one obvious approach that fit in a single pass
- Simple edits, quick fixes, single-file changes
- Staging a trivial task wastes effort and buries the answer under ceremony

## Overview

This skill shapes the *procedure* a model follows on complex work. It makes the model decompose before acting, delegate independent sub-work where subagent tooling exists, verify each stage against a failable check rather than a feeling, and critique its own output before delivering it.

**What it does NOT do:** It does not change the underlying model's capability. Coherence across long tasks and genuine self-correction live in the model's weights, not in a prompt. Treat it as a checklist, not a capability transplant.

## Variants

| Variant | Model | Use when |
|---|---|---|
| **fable-mode** (default) | Current model (Opus) | Peak reasoning, complex synthesis |
| **fable-sonnet** | Claude Sonnet | Balanced: strong reasoning, lower cost |
| **fable-haiku** | Claude Haiku | High-volume, cost-sensitive work |

All variants share the same core loop, stage map, verification, and self-critique.

## Process

1. **Stage map** — Write the full stage plan before touching anything. Number stages. Each stage produces one verifiable artifact.
2. **Delegate** — If subagent tooling exists, spawn independent stages concurrently. Keep delegation one level deep.
3. **Verify** — Each stage must define a pass condition that an external artifact satisfies. A check that can fail.
4. **Self-critique** — Read output as a skeptical reviewer. Hunt for real weaknesses. Fix or flag.

## Core Loop

### 1. Stage Map (before touching anything)

Write out the full stage plan before starting. Number the stages. Include a brief expected output for each. This is how you avoid discovering at stage 7 that you made a wrong assumption at stage 2.

Each stage should produce one verifiable artifact. If a stage produces nothing checkable, merge it with the next.

```
Stage 1: [Name] → [Expected output]
Stage 2: [Name] → [Expected output]
...
```

### 2. Delegate Independent Work

First check whether subagent/Agent tooling exists in the current runtime. If it does not, run the stages sequentially.

If subagent tooling is available and stage N and stage M don't depend on each other, spawn them concurrently. Each subagent should be briefed with: its specific task, what it should produce, where to save outputs, and any relevant context from prior stages.

**Good delegation:** "research X while I do Y", "process these 3 files", "verify this independently"

**Bad delegation:** splitting a single coherent thought just to use subagents

Keep delegation one level deep by default.

### 3. Verify with a Check That Can Fail

Each stage must define a pass condition that an external artifact satisfies:

| Acceptable | Not Acceptable |
|---|---|
| A test that runs and passes | "I reviewed it and it looks right" |
| A file that provably exists in expected shape | "It should work" |
| A source actually fetched and read | "I assume the API returns..." |
| An output diffed against the stated spec | "Looks correct to me" |

If a stage genuinely has no failable check, say so explicitly and mark its output as unverified.

**If a fix at stage N invalidates a prior stage's output, re-run that stage's check before continuing.**

### 4. Self-Critique Before Delivery

Before presenting final output, read it as a skeptical reviewer would:

1. Hunt for a real weakness or limitation
2. If one exists, fix it or flag it to the user
3. If genuine checking turns up nothing, say so plainly
4. Do NOT manufacture a weakness to satisfy the ritual

**Before flagging any problem — verify it actually exists.** Grep, diff, run it, or check the source directly. Never report a problem that hasn't been confirmed present. An unverified flag is itself an error.

## Domain-Specific Patterns

### Software Engineering
- Read the entire relevant codebase section before writing a line
- Write tests before (or alongside) implementation
- **Failable check:** tests run; error paths exercised, not just happy path

### Research / Knowledge Work
- Gather sources before synthesizing
- For each load-bearing claim: what's the evidence? what would falsify it?
- **Failable check:** every load-bearing claim traces to a source actually read

### Data Analysis
- Understand the data shape before writing any analysis
- State your hypothesis before computing
- **Failable check:** data quality assertions run against actual data and pass

### Long-Running / Multi-Session Tasks
- Maintain a work log: decisions made, why, what was tried and failed
- At the start of any continuation, re-read the work log before doing anything
- **Failable check:** done criteria are written and testable

## Operational Rules

### Warning Threshold

Across a multi-stage run, minor concerns accumulate. Keep a running count. **At three accumulated warnings, stop and surface all of them to the user at once before continuing.** Three small things pointing the same direction usually mean one real problem.

### Find-and-Replace Safety

When editing files with sed (or any substring replace):
- Always anchor on word boundaries (`\bword\b`, not bare `word`)
- After any sed pass, grep for glued or malformed compound words
- A replace that silently corrupts neighboring tokens is the most common self-inflicted error

## Relation to 1ai-rules

| Fable-mode concept | 1ai-rules equivalent |
|---|---|
| Stage map before execution | ENGINEERING.md §6 Core Loop (READ → THINK → DECIDE → PLAN) |
| Failable verification | VERIFICATION.md §1 Receipt Requirement |
| Self-critique before delivery | ENGINEERING.md §6 REVIEW step |
| Sub-agent delegation | ENGINEERING.md §4 PR Lifecycle |
| Warning threshold | ENGINEERING.md §3 Anti-Thrash (2 failures = stop) |

Fable-mode provides the **execution procedure**. 1ai-rules provides the **engineering gates**. Use both together for maximum discipline.

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "This task is simple enough to skip planning" | If you're wrong about the simplicity, the cost of backtracking is 10x the cost of planning. |
| "I'll verify at the end" | Catching an error at stage 3 is trivial. At stage 8 it's catastrophic. |
| "My introspection is a valid check" | A model that skips verification will also pass its own introspection. Use external artifacts. |
| "Sub-agents are overkill" | Independent work done in parallel is faster AND more reliable than sequential. |
| "Self-critique is just ceremony" | The point is to find real weaknesses before the user does. If none exist, say so. |

## Verification

- [ ] Stage plan written before any execution begins
- [ ] Each stage produces one verifiable artifact
- [ ] Every stage has a failable check (not "looks right to me")
- [ ] Sub-agents briefed with task, expected output, save location
- [ ] Delegation is one level deep (no nested sub-agents)
- [ ] Warning threshold enforced (3 warnings = stop and surface)
- [ ] Self-critique completed before delivery
- [ ] Unverified outputs explicitly marked
