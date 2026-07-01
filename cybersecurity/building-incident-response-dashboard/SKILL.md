---
name: building-incident-response-dashboard
description: 'Builds real-time incident response dashboards in Splunk, Elastic, or Grafana to provide SOC analysts and leadership
  with situational awareness during active incidents, tracking affected systems, containment status, IOC spread, and response
  timeline. Use when IR teams need unified visibility during incident coordination and post-incident reporting.

  '
domain: cybersecurity
tags:
- soc
- dashboard
- incident-response
- splunk
- visualization
- situational-awareness
- metrics
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
# Building Incident Response Dashboard

## Overview

Cybersecurity skill for building incident response dashboard. Follows industry best practices and security standards.

## When to Use

**Trigger phrases:**
- "building incident response dashboard"
- "IR teams need real-time dashboards during active incidents for coordination and"
- "SOC leadership requires operational dashboards showing incident status and analy"
- "Post-incident reviews need visual timelines and impact assessments"


Use this skill when:
- IR teams need real-time dashboards during active incidents for coordination and tracking
- SOC leadership requires operational dashboards showing incident status and analyst workload
- Post-incident reviews need visual timelines and impact assessments
- Executive briefings require high-level incident metrics and trend analysis

**Do not use** for day-to-day SOC monitoring dashboards (use Incident Review instead) — IR dashboards are designed for active incident coordination and management reporting.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- SIEM platform (Splunk with Dashboard Studio, Elastic Kibana, or Grafana)
- Notable event and incident data in SIEM (Splunk ES incident_review index)
- Ticketing system integration (ServiceNow, Jira) for remediation tracking
- Asset and identity lookup tables for context enrichment
- Dashboard publishing access for SOC team and management distribution

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

1. **Assess Requirements** — Evaluate current environment and define incident response dashboard implementation requirements.
2. **Design Architecture** — Plan the incident response dashboard architecture, including components, integrations, and data flows.
3. **Configure Components** — Set up and configure each incident response dashboard component according to best practices.
4. **Test Integration** — Validate that all components work together. Run functional and security tests.
5. **Deploy to Production** — Roll out the implementation with monitoring and rollback capabilities.
6. **Validate and Document** — Verify the implementation meets requirements. Document configuration and runbooks.

## Tools

- **Configuration Management** — Infrastructure as code and automation
- **Monitoring Stack** — Observability and alerting
- **Documentation Platform** — Runbooks and architecture docs


## Process

1. **Reconnaissance** — Gather target information, identify attack surface, enumerate services
1. **Analysis/Exploitation** — Execute the technique, analyze results, document findings
1. **Reporting** — Document IOCs, write findings, provide remediation recommendations

## Verification

- [ ] All incident response dashboard procedures executed completely and documented
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