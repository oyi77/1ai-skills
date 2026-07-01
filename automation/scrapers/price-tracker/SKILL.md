---
name: price-tracker
description: Track price changes automatically across e-commerce sites. Get alerts when prices drop below your target. Use when tracking price changes automatically across e-commerce sites. get alerts when.
domain: automation
tags:
- automation
- price
- productivity
- tracker
- workflow
---
# Price Tracker

## When to Use

**Trigger phrases:**
- "price tracker"
- "Help me with price tracker"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


## When NOT to Use

- For one-off tasks that will never repeat
- When the process requires human judgment at every step
- When the cost of automation exceeds the cost of manual execution


## Overview

Price Tracker automates workflow automation to reduce manual effort and increase reliability.

## Workflow

```python
# Example: Workflow automation
import schedule
import time

def run_workflow():
    data = fetch_data()
    processed = transform(data)
    deliver(processed)

schedule.every().hour.do(run_workflow)
while True:
    schedule.run_pending()
    time.sleep(60)
```

1. **Define triggers** — Set up events or schedules that initiate the automation
2. **Configure inputs** — Specify data sources and parameters
3. **Design pipeline** — Define the sequence of automated steps
4. **Add error handling** — Set up retries, alerts, and fallback paths
5. **Test end-to-end** — Validate the full automation with realistic data
6. **Deploy and monitor** — Activate and track performance

## Configuration

- Set trigger conditions (schedule, webhook, event)
- Define input validation rules
- Configure notification channels for alerts
- Set retry policies and timeout limits

## Best Practices

- Start with simple automations and iterate
- Add logging at every step for debugging
- Use idempotent operations where possible
- Test with edge cases before deploying

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Manual is faster for one-off tasks" | One-off tasks become recurring. Automate early, save time later. |
| "I will add error handling later" | You never do. Handle errors from day one. |
| "Automation is overkill" | If you do it twice, automate it. If you do it daily, it is critical infrastructure. |


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run price tracker workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings