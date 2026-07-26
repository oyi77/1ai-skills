---
name: review-agent
description: Use when read code changes with adversarial intent to find bugs, security holes, logic errors, and performance traps.
domain: agents
tags:
  - agent
  - ai-agent
  - automation
  - review
  - autonomous
version: 1.0.0
---

# Review Agent

Quick Reference — see parent for full agent ecosystem.

The Review Agent reads diffs with adversarial intent — assuming every line could hide a bug, security hole, or performance trap. It classifies findings by severity (P1–P3) and provides concrete fix recommendations, not vague warnings. Unlike human reviewers who fatigue after 20 minutes, the Review Agent checks every changed line systematically against classifiers for injection, logic errors, concurrency bugs, and convention violations.

## Key Responsibilities

- **Adversarial analysis**: Read every changed line as if it is wrong — look for injection, logic errors, off-by-one, race conditions, and undefined behavior
- **Severity-ranked findings**: Report issues as P1 (blocking), P2 (should fix), P3 (consider) with clear reproduction steps and fix recommendations
- **Context-aware checks**: Understand the project's conventions, framework patterns, and dependency versions to flag real issues — not boilerplate complaints

## Code Example

```python
"""Minimal review agent pattern — analyze a diff."""

import json, sys

def review_diff(diff_text: str) -> dict:
    findings = []
    lines = diff_text.split("\n")

    for i, line in enumerate(lines):
        if line.startswith("+") and "eval(" in line:
            findings.append({
                "file": "unknown", "line": i, "severity": "P1",
                "type": "Code injection",
                "finding": "eval() called with dynamic input",
                "recommendation": "Replace with safe parser or AST-based evaluation"
            })
        if line.startswith("+") and "password" in line.lower() and "=" in line:
            findings.append({
                "file": "unknown", "line": i, "severity": "P1",
                "type": "Secret exposure",
                "finding": "Password literal in source code",
                "recommendation": "Move to environment variable or secrets manager"
            })
        if line.startswith("+") and "raw(" in line.lower():
            findings.append({
                "file": "unknown", "line": i, "severity": "P2",
                "type": "SQL injection risk",
                "finding": "Raw SQL without parameterization",
                "recommendation": "Use parameterized query or ORM"
            })

    return {
        "findings": findings,
        "summary": f"{len([f for f in findings if f['severity'] == 'P1'])} P1, "
                   f"{len([f for f in findings if f['severity'] == 'P2'])} P2",
        "verdict": "blocked" if any(f["severity"] == "P1" for f in findings) else "approved"
    }

if __name__ == "__main__":
    diff = sys.stdin.read()
    result = review_diff(diff)
    print(json.dumps(result, indent=2))
```

## Checklist

- [ ] All P1/P2 findings resolved or explicitly acknowledged with risk acceptance
- [ ] Security patterns checked: injection, secrets, auth bypass, CSRF, XSS
- [ ] Logic verified: null checks, boundary conditions, error paths
- [ ] Performance reviewed: N+1 queries, unnecessary allocations, sync I/O in hot path
- [ ] Convention compliance: naming, imports, error handling matches surrounding code

## Workflow

1. **Identify** the task or trigger.
2. **Prepare** inputs and configure parameters.
3. **Execute** the core routine.
4. **Verify** the output against expected results.
5. **Iterate** based on feedback or new data.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I wrote it carefully, no bugs" | Authors are blind to their own assumptions — adversarial review catches what you did not think to check |
| "This is just a small change" | Small changes in critical paths (auth, payments, serialization) cause the highest-impact bugs |
| "The tests pass, so it is correct" | Tests cover what you thought of. Review finds what you did not think of |

## When to Use

Use before every PR merge, after any refactoring, when auditing security-sensitive code (auth, payments, PII), and as a pre-deploy safety gate. Do NOT use as a substitute for running tests, for generated/boilerplate code where patterns are strictly mechanical, or when the agent cannot access the full diff context.
