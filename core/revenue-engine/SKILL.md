---
name: revenue-engine
description: Manage revenue pipelines, track Stripe/analytics metrics, and automate financial reporting for SaaS businesses.
domain: core
tags:
- engine
- infrastructure
- memory
- pipeline
- revenue
- self-improvement
---
# Revenue Engine

## When to Use
**Trigger phrases:**
- "revenue engine"
- "Manage revenue pipelines, track Stripe/analytics metrics, and automate financial"


- When the task falls within this skill's domain expertise
- When automated execution saves time over manual work
- When the skill's tools and integrations are available


## When NOT to Use

- When the task can be solved with existing standard libraries
- When the infrastructure is already in place and working
- When the added complexity does not provide measurable benefit


## Overview

Revenue Engine is a foundational core infrastructure skill that provides system foundation capabilities for the agent ecosystem.

## Architecture

- **Input layer** — Receives and validates incoming requests
- **Processing layer** — Core logic for system foundation
- **Output layer** — Formats and delivers results
- **State management** — Maintains context across invocations

## Configuration

- Set up required environment variables and paths
- Configure logging level and output format
- Define resource limits (memory, time, API calls)
- Enable/disable features via configuration flags

## Integration

- Exposes standard interfaces for other skills to consume
- Supports event-driven and request-response patterns
- Compatible with the 1ai-skills hook system
- Logs metrics for the skill performance monitor

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I will add monitoring later" | Without monitoring, you cannot detect failures. Add it from day one. |
| "One model is enough" | Different tasks need different models. Route intelligently. |
| "Premature optimization" | Infrastructure decisions are hard to change later. Design for scale early. |

```python
# Example: Model routing
ROUTES = {
    "code": ["claude-sonnet-4-20250514", "gpt-4o"],
    "vision": ["gemini-2.5-pro", "gpt-4o"],
    "fast": ["gemini-2.5-flash", "gpt-4o-mini"],
}

def route_request(task: str, prompt: str):
    models = ROUTES.get(task, ROUTES["fast"])
    for model in models:
        try:
            return call_model(model, prompt)
        except Exception:
            continue
    raise RuntimeError("All models failed")
```

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings