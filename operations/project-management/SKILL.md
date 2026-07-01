---
name: project-management
description: Coordinate sprints, track deadlines, manage tasks, and maintain project documentation with Notion and Slack. Use when working with project management.
domain: operations
tags:
- business-ops
- management
- notion
- operations
- project
- slack
---
# Project Management

## When to Use

**Trigger phrases:**
- "project management"
- "Help me with project management"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


Coordinate tasks, track deadlines, manage sprints, and maintain project documentation.


## When NOT to Use

- For processes that change daily (too much overhead)
- When the team is too small to benefit from SOPs
- For one-time events that will not repeat


## Overview

Project Management streamlines operational efficiency for operational excellence.

## Workflow

```python
# Example: SOP execution tracker
def execute_sop(sop_name: str, steps: list[str]) -> dict:
    results = []
    for i, step in enumerate(steps, 1):
        try:
            result = execute_step(step)
            results.append({"step": i, "status": "ok", "result": result})
        except Exception as e:
            results.append({"step": i, "status": "error", "error": str(e)})
            break
    return {"sop": sop_name, "steps": results}
```

1. **Assess** — Evaluate current state and identify gaps
2. **Design** — Plan improved processes and workflows
3. **Implement** — Roll out changes with team alignment
4. **Measure** — Track operational KPIs
5. **Iterate** — Continuous improvement based on data

## SOP Template

- **Purpose** — Why this process exists
- **Scope** — Who and what it covers
- **Procedure** — Step-by-step instructions
- **Escalation** — When and how to escalate
- **Review** — Schedule for periodic updates

## Key Metrics

- Process completion time
- Error/rework rate
- Team satisfaction scores
- Cost per operation
- SLA compliance rate

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We do not need SOPs" | Without SOPs, quality depends on memory. Document everything. |
| "Manual processes work fine" | Manual processes do not scale and are error-prone. Automate. |
| "Compliance is optional" | Compliance protects you legally. Build it in from the start. |


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run project management workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings