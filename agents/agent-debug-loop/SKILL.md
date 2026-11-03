---
name: agent-debug-loop
description: Use when an agent run fails repeatedly, consumes tokens without progress, loops on the same tools, or drifts away from the intended task. Structured self-debugging workflow using capture, diagnosis, contained recovery, and introspection reports.
domain: agents
subdomain: orchestration
category: agents
version: 1.0.0
author: oyi77
license: Apache-2.0
tags:
- debugging
- agent-harness
- context-management
- loop-detection
- self-improvement
triggers:
- agent loop
- agent stuck
- agent failing
- debug agent
- tool call limit
- context overflow
argument-hint: "[failure description]"
---

# Agent Debug Loop (Introspection)

## Overview

Systematic self-debugging for AI agent failures. Captures state before retrying blindly, diagnoses against known failure patterns, applies contained recovery actions, and produces a structured human-readable report. This is a workflow skill, not a hidden runtime—it teaches the agent to debug itself before escalating to a human.

## When to Use

**Trigger phrases:**
- "agent loop", "agent stuck", "agent failing", "debug agent"
- "tool call limit", "context overflow", "repeated retries"

Use directly when:
- Maximum tool-call / loop-limit failures reached.
- Repeated retries produce no forward progress.
- Context growth or prompt drift degrades output quality.
- File-system or environment state mismatches expectations.
- Tool failures are likely recoverable via diagnosis + smaller corrective action.

## When NOT to Use

- Feature verification after code changes → use `test-agent` or `verification-loop` pattern.
- Framework-specific bugs where a narrower skill already exists.
- Runtime promises the current harness cannot enforce automatically.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll just retry the same approach harder." | Blind retries burn tokens and worsen context pressure. Capture state first, then change one variable. |
| "The tool must be broken." | Most tool failures are state mismatches (wrong cwd, stale file hash, missing dependency), not tool bugs. Verify assumptions before blaming the tool. |
| "I can keep everything in memory and figure it out." | Agents have no persistent memory across compaction. Write the failure capture to disk (`local://` or artifact) so recovery survives context loss. |
| "One more attempt will fix it." | If two identical attempts failed, the third will too. Switch strategy or escalate. |

## Workflow

### Phase 1: Failure Capture

Before recovering, record the failure precisely:

```markdown
## Failure Capture
- Session / task:
- Goal in progress:
- Error type + message:
- Last successful step:
- Last failed tool / command:
- Repeated pattern seen:
- Context pressure indicators (loop count, token estimate):
- Environment assumptions to verify:
```

Persist this to `local://agent-failure-capture.md` or an artifact so it survives compaction.

### Phase 2: Root-Cause Diagnosis

Match the failure to a known pattern:

| Pattern | Symptom | Likely Cause |
|---|---|---|
| **Stale anchor** | Edit tool hash mismatch | File changed since last read; re-read before editing |
| **Path confusion** | ENOENT on existing file | Wrong cwd, symlink, or relative-path assumption |
| **Dependency gap** | Import/module error | Missing install, virtualenv, or PATH entry |
| **Context bloat** | Degraded reasoning, repetition | Oversized pasted logs, duplicated plans, runaway notes |
| **Tool misuse** | Invalid arguments | Misread schema; re-check tool docs |
| **State race** | Intermittent pass/fail | Concurrent writer, unlocked shared file |
| **Loop lock** | Same 3 steps repeat | No exit condition; plan lacks termination check |

Verify each assumption empirically—run one diagnostic command per hypothesis rather than guessing.

### Phase 3: Contained Recovery

Apply the smallest corrective action that breaks the pattern:

1. **Reset context**: Trim oversized notes; drop duplicated plans.
2. **Re-anchor state**: Fresh `read` of target files; confirm cwd and branch.
3. **Reduce scope**: Split the failing step into two smaller verifiable sub-steps.
4. **Switch strategy**: Different tool, different approach, or delegate to a subagent with clean context.
5. **Escalate cleanly**: If two recovery attempts fail, stop and hand off with the capture report attached.

### Phase 4: Introspection Report

Produce a structured report:

```markdown
## Agent Introspection Report
- Failure class: [pattern from Phase 2]
- Evidence: [commands run + outputs]
- Recovery applied: [what changed]
- Outcome: [resolved / still blocked]
- Prevention: [rule or checklist item to avoid recurrence]
```

## Verification

- [ ] Failure captured to persistent artifact before any retry
- [ ] Root cause matched to a known pattern with evidence
- [ ] Exactly one variable changed per recovery attempt
- [ ] Escalation triggered after two failed recovery attempts
- [ ] Prevention rule recorded (via `learn` or managed-skill update)