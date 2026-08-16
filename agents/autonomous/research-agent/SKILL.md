---
name: research-agent
description: Use when investigating topics deeply with cross-referenced sources and
  producing evidence-backed findings.
domain: agents
author: oyi77
license: Apache-2.0
subdomain: ai-agents
tags:
- agent
- ai-agent
- automation
- research
- autonomous
version: 1.0.0
category: agents
---


# Research Agent

Quick Reference — see parent for full agent ecosystem.

The Research Agent investigates technical questions by gathering evidence from multiple sources (web, docs, code repositories, logs), cross-referencing claims, and producing a structured recommendation with confidence scores. It compresses what would take a human 2+ hours into 15 minutes by systematically covering evaluation criteria (security, maintenance, community health, compatibility) that ad-hoc research misses.



## When Not to Use

- **Simple or one-off tasks** — if the task is straightforward, direct execution is faster than structured methodology.
- **Already established workflows** — follow existing team conventions rather than introducing new frameworks.
- **When automation overhead exceeds benefit** — for very small scopes, the setup cost may not be justified.


## Dependencies

- Python 3.8+ or Node.js 18+
- Access to relevant APIs/services for your specific use case
- Basic understanding of the domain concepts


## Commands

```bash
# Refer to the skill's usage section for specific commands
# Adapt these to your workflow
```
## Key Responsibilities

- **Multi-source evidence gathering**: Query web search, official docs, GitHub, Stack Overflow, and internal knowledge bases in parallel
- **Cross-reference and verify**: Compare claims across sources; flag contradictions and stale information
- **Structured recommendations**: Produce a ranked output with scores, trade-offs, and a clear decision aligned to project context

## Code Example

```python
"""Minimal research agent pattern — evaluate a library."""

import json, sys, subprocess
from datetime import datetime

def research_library(name: str, criteria: list[str]) -> dict:
    sources = {}

    # Gather from multiple sources (simplified — real agent fetches live data)
    sources["github"] = {"stars": "28k", "last_commit": "2025-11-01", "issues": 42}
    sources["npm"] = {"weekly_downloads": "1.2M", "security_advisories": 0}
    sources["security"] = {"audit_status": "passed", "cves_last_year": 0}

    # Score against criteria
    recommendations = []
    score = sum([
        3 if sources["github"]["stars"].rstrip("k").isdigit() and int(sources["github"]["stars"].rstrip("k")) > 10 else 0,
        2 if sources["npm"]["security_advisories"] == 0 else -2,
        2 if sources["security"]["cves_last_year"] == 0 else -3
    ])

    recommendations.append({
        "library": name,
        "score": min(score, 10),
        "stars": sources["github"]["stars"],
        "maintained": sources["github"]["last_commit"],
        "security": "clean" if sources["security"]["cves_last_year"] == 0 else "has advisories"
    })

    return {
        "query": f"Evaluate {name} for: {', '.join(criteria)}",
        "sources_checked": list(sources.keys()),
        "recommendations": sorted(recommendations, key=lambda x: x["score"], reverse=True),
        "decision": recommendations[0]["library"] if recommendations else None
    }

if __name__ == "__main__":
    result = research_library(sys.argv[1], sys.argv[2:])
    print(json.dumps(result, indent=2))
```

## Checklist

- [ ] At least 3 independent sources checked per claim
- [ ] Recommendations include explicit trade-offs, not just pros
- [ ] Stale or contradictory sources flagged with date and reason
- [ ] Security posture assessed (CVEs, audit status, maintenance activity)
- [ ] Decision mapped to project context (language, framework, scale)

## Workflow

1. **Identify** the task or trigger.
2. **Prepare** inputs and configure parameters.
3. **Execute** the core routine.
4. **Verify** the output against expected results.
5. **Iterate** based on feedback or new data.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I already know which library to use" | Personal familiarity is a bias — measured data on downloads, security audits, and maintenance beats intuition |
| "A quick Google search is enough" | Surface-level results miss security advisories, breaking changes, and community health signals in CHANGELOGs and issue trackers |
| "The first result is the best" | SEO ranking has no correlation with quality or suitability for your specific use case |

## When to Use

Use when evaluating libraries or tools, investigating root causes, performing competitive analysis, checking security posture of dependencies, or exploring unfamiliar technical domains. Do NOT use for opinions, subjective design decisions, or questions better answered by reading your own codebase (use codebase-memory instead).
