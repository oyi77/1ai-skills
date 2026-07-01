---
name: performing-soc-tabletop-exercise
description: 'Performs tabletop exercises for SOC teams simulating security incidents through discussion-based scenarios to
  test incident response procedures, communication workflows, and decision-making under pressure without impacting production
  systems. Use when organizations need to validate IR playbooks, train analysts, or meet compliance requirements for incident
  response testing.

  '
domain: cybersecurity
tags:
- soc
- tabletop
- exercise
- incident-response
- training
- nist
- playbook-validation
subdomain: soc-operations
mitre_attack:
- T1566
- T1486
- T1078
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- DE.CM-01
- DE.AE-02
- RS.MA-01
- DE.AE-06
---
# Performing Soc Tabletop Exercise

## Overview

Cybersecurity skill for performing soc tabletop exercise. Follows industry best practices and security standards.

## When to Use

**Trigger phrases:**
- "performing soc tabletop exercise"
- "Annual or semi-annual incident response testing is required (NIST, ISO 27001, PC"
- "New SOC analysts need exposure to major incident scenarios in a controlled envir"
- "Updated playbooks need validation before next real incident"


Use this skill when:
- Annual or semi-annual incident response testing is required (NIST, ISO 27001, PCI DSS compliance)
- New SOC analysts need exposure to major incident scenarios in a controlled environment
- Updated playbooks need validation before next real incident
- Cross-functional coordination (SOC, IT, Legal, PR, Executive) needs rehearsal
- Post-incident reviews reveal gaps requiring scenario-based training

**Do not use** as a replacement for technical purple team exercises — tabletop exercises test processes and decision-making, not technical detection capabilities.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Exercise facilitator with incident response experience
- Participant list: SOC analysts (Tier 1-3), SOC manager, IT operations, Legal, HR, Communications
- Conference room or video call with screen sharing capability
- Printed or digital scenario injects with timed release schedule
- Evaluation scorecard for assessing participant responses
- Existing incident response plan and playbooks for reference during exercise

## Workflow

```python
# Example: IOC detection
import re

IOC_PATTERNS = {
    "ip": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "domain": r"\b[a-z0-9-]+\.[a-z]{2,}\b",
    "hash_md5": r"\b[a-f0-9]{32}\b",
    "hash_sha256": r"\b[a-f0-9]{64}\b",
}

def extract_iocs(text: str) -> dict:
    return {k: re.findall(v, text) for k, v in IOC_PATTERNS.items()}
```

1. **Plan Operations** — Define objectives, scope, and success criteria for soc tabletop exercise operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for soc tabletop exercise.
3. **Execute Core Workflow** — Perform the soc tabletop exercise operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Design** — Define interface, identify patterns, plan implementation
1. **Implement** — Write code following existing conventions, add tests
1. **Verify** — Run tests, check integration, validate behavior

## Verification

- [ ] All soc tabletop exercise procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |