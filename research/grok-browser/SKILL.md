---
name: grok-browser
description: Use Grok's browser capabilities to search the web, analyze pages, and synthesize real-time information.
domain: research
tags:
- analysis
- browser
- grok
- investigation
- research
---
# Grok Browser

## When to Use

**Trigger phrases:**
- "grok browser"
- "Help me with grok browser"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


Query Grok (grok.com) via Chrome browser automation and copy responses.


## When NOT to Use

- When the answer is already known and documented
- For time-sensitive decisions that cannot wait for thorough research
- When the topic is outside your domain of competence


## Overview

Grok Browser enables thorough investigation with structured methodology.

## Workflow

```python
# Example: Source evaluation
def evaluate_source(url: str) -> dict:
    return {
        "authority": check_domain_authority(url),
        "currency": get_last_updated(url),
        "objectivity": detect_bias(url),
        "accuracy": cross_reference(url),
    }
```

1. **Define question** — Clarify the research objective
2. **Gather sources** — Collect primary and secondary data
3. **Analyze** — Apply analytical frameworks to findings
4. **Synthesize** — Combine insights into actionable conclusions
5. **Present** — Deliver findings in clear, compelling format
6. **Archive** — Store research for future reference

## Source Evaluation

- **Authority** — Is the source credible and expert?
- **Currency** — Is the information recent and relevant?
- **Objectivity** — Is there bias or conflict of interest?
- **Accuracy** — Can claims be verified independently?

## Output Format

- Executive summary (1-2 paragraphs)
- Key findings (bullet points)
- Detailed analysis (sections with evidence)
- Recommendations (actionable next steps)
- Sources and methodology

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "First result is good enough" | Deep research finds better answers. Keep digging. |
| "I do not need to verify sources" | Unverified sources lead to wrong conclusions. Always cross-check. |
| "Research is a one-time thing" | Markets change. Research needs to be continuous, not one-off. |

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings