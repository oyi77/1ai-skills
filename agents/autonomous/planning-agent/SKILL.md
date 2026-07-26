---
name: planning-agent
description: Use when decompose complex tasks into executable steps with dependencies, risk assessment, and verification criteria.
domain: agents
tags:
  - agent
  - ai-agent
  - automation
  - planning
  - autonomous
version: 1.0.0
---

# Planning Agent

Quick Reference — see parent for full agent ecosystem.

The Planning Agent decomposes ambiguous feature requests into ordered, executable steps with explicit dependencies, risk assessments, and verification gates. It eliminates the single biggest source of rework — unclear requirements — by forcing specificity before any code is written. Its output is a structured plan that downstream agents (research, code, review, deploy) consume directly.

## Key Responsibilities

- **Break down features**: Convert natural-language requirements into a step graph with clear inputs, outputs, and dependencies
- **Identify risks early**: Flag ambiguous requirements, missing context, breaking changes, and parallelization opportunities before implementation starts
- **Define verification gates**: Specify acceptance criteria and test conditions for every step so completion is measurable

## Code Example

```python
"""Minimal planning agent pattern — decompose a feature request."""

import json, sys

def plan(feature_request: str) -> dict:
    # In practice, this calls an LLM. Here we show the output shape.
    steps = [
        {
            "name": "auth-setup",
            "type": "implementation",
            "files": ["src/auth/provider.py", "src/auth/config.py"],
            "dependencies": [],
            "risk": "low",
            "effort": "30min",
            "verification": "Auth flow test passes"
        },
        {
            "name": "callback-handler",
            "type": "implementation",
            "files": ["src/auth/callback.py"],
            "dependencies": ["auth-setup"],
            "risk": "medium",
            "effort": "1h",
            "verification": "Callback processes valid/invalid tokens"
        },
        {
            "name": "login-ui",
            "type": "frontend",
            "files": ["src/components/LoginButton.tsx"],
            "dependencies": ["auth-setup", "callback-handler"],
            "risk": "low",
            "effort": "45min",
            "verification": "Login flow E2E passes in Playwright"
        }
    ]

    return {
        "feature": feature_request,
        "steps": steps,
        "dependencies": ["auth-setup → callback-handler → login-ui"],
        "risks": [
            {"description": "Provider OAuth scope changes", "mitigation": "Pin API version in config"}
        ],
        "estimated_time": "2h 15min",
        "parallelizable": ["auth-setup can start immediately"],
        "total_files": 3,
        "total_tests": 3
    }

if __name__ == "__main__":
    result = plan(" ".join(sys.argv[1:]))
    print(json.dumps(result, indent=2))
```

## Checklist

- [ ] Every step has a clear owner, dependencies, and verification gate
- [ ] Risks identified and mitigated — not just listed
- [ ] Parallelization opportunities explicitly noted
- [ ] Estimated effort is per-step, not a single number
- [ ] Acceptance criteria are testable (pass/fail, not subjective)

## Workflow

1. **Identify** the task or trigger.
2. **Prepare** inputs and configure parameters.
3. **Execute** the core routine.
4. **Verify** the output against expected results.
5. **Iterate** based on feedback or new data.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I will figure it out as I code" | Coding without a plan guarantees at least one full rewrite when you discover a missing dependency |
| "A rough outline is enough" | Vague steps produce vague code. Each step must name the files it touches and the test that proves it works |
| "Planning takes too long" | A 30-minute plan eliminates 4+ hours of rework from mid-implementation surprises |

## When to Use

Use when starting any feature touching 3+ files, handling ambiguous requirements, coordinating multiple agents, or estimating delivery timelines. Do NOT use for trivial one-line changes, real-time system commands, or tasks where the user has already provided an explicit step-by-step spec.
