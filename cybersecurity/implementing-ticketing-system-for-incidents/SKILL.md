---
name: implementing-ticketing-system-for-incidents
description: 'Implements an integrated incident ticketing system connecting SIEM alerts to ServiceNow, Jira, or TheHive for
  structured incident tracking, SLA management, escalation workflows, and compliance documentation. Use when SOC teams need
  formalized incident lifecycle management with automated ticket creation, assignment routing, and resolution tracking.

  '
domain: cybersecurity
tags:
- soc
- ticketing
- servicenow
- jira
- thehive
- incident-management
- sla
- workflow
subdomain: soc-operations
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- DE.CM-01
- DE.AE-02
- RS.MA-01
- DE.AE-06
---
# Implementing Ticketing System For Incidents

## Overview

Cybersecurity skill for implementing ticketing system for incidents. Follows industry best practices and security standards.

## When to Use

Use this skill when:
- SOC teams need to formalize incident tracking beyond SIEM notable event management
- Compliance requirements mandate documented incident lifecycle with timestamps and audit trails
- Multi-team coordination requires ticket-based workflows with assignment and escalation
- SLA tracking needs automated measurement of response and resolution times
- Post-incident reviews require structured data for trend analysis and reporting

**Do not use** for individual alert triage — ticketing is for confirmed incidents requiring multi-step investigation and remediation, not every SIEM alert.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Ticketing platform: ServiceNow ITSM, Jira Service Management, or TheHive
- SIEM integration capability (REST API, webhook, or SOAR connector)
- Incident classification taxonomy (categories, severity levels, escalation paths)
- On-call rotation schedule for analyst assignment
- SLA definitions aligned to incident severity

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

1. **Assess Requirements** — Evaluate current environment and define ticketing system implementation requirements.
2. **Design Architecture** — Plan the ticketing system architecture, including components, integrations, and data flows.
3. **Configure Components** — Set up incidents for ticketing system according to vendor best practices and security guidelines.
4. **Test Integration** — Validate that all components work together. Run functional and security tests.
5. **Deploy to Production** — Roll out the implementation with monitoring and rollback capabilities.
6. **Validate and Document** — Verify the implementation meets requirements. Document configuration and runbooks.

## Tools

- **incidents** — Primary tool for this skill
- **Configuration Management** — Infrastructure as code and automation
- **Monitoring Stack** — Observability and alerting
- **Documentation Platform** — Runbooks and architecture docs

## Verification

- [ ] All ticketing system procedures executed completely and documented
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