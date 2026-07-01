---
name: building-soc-metrics-and-kpi-tracking
description: 'Builds SOC performance metrics and KPI tracking dashboards measuring Mean Time to Detect (MTTD), Mean Time to
  Respond (MTTR), alert quality ratios, analyst productivity, and detection coverage using SIEM data. Use when SOC leadership
  needs operational visibility, continuous improvement tracking, or executive-level reporting on security operations effectiveness.

  '
domain: cybersecurity
tags:
- soc
- metrics
- kpi
- mttd
- mttr
- dashboard
- reporting
- continuous-improvement
subdomain: soc-operations
version: '1.0'
author: mahipal
license: Apache-2.0
nist_ai_rmf:
- MEASURE-2.7
- MAP-5.1
- MANAGE-2.4
atlas_techniques:
- AML.T0070
- AML.T0066
- AML.T0082
nist_csf:
- DE.CM-01
- DE.AE-02
- RS.MA-01
- DE.AE-06
---
# Building Soc Metrics And Kpi Tracking

## Overview

Cybersecurity skill for building soc metrics and kpi tracking. Follows industry best practices and security standards.

## When to Use

**Trigger phrases:**
- "building soc metrics and kpi tracking"
- "SOC leadership needs data-driven visibility into operational performance"
- "Continuous improvement programs require baseline measurements and trend tracking"
- "Executive reporting demands quantified security posture and ROI metrics"


Use this skill when:
- SOC leadership needs data-driven visibility into operational performance
- Continuous improvement programs require baseline measurements and trend tracking
- Executive reporting demands quantified security posture and ROI metrics
- Staffing decisions need objective workload and capacity data
- Compliance audits require documented SOC performance evidence

**Do not use** metrics as punitive measures against analysts — metrics should drive process improvement, not individual performance management.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- SIEM with 90+ days of incident and alert disposition data
- Incident ticketing system (ServiceNow, Jira) with timestamp data for incident lifecycle
- Analyst shift schedules and staffing data
- ATT&CK Navigator for detection coverage tracking
- Dashboard platform (Splunk, Grafana, or Power BI)

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

1. **Assess Requirements** — Evaluate current environment and define soc metrics and kpi tracking implementation requirements.
2. **Design Architecture** — Plan the soc metrics and kpi tracking architecture, including components, integrations, and data flows.
3. **Configure Components** — Set up and configure each soc metrics and kpi tracking component according to best practices.
4. **Test Integration** — Validate that all components work together. Run functional and security tests.
5. **Deploy to Production** — Roll out the implementation with monitoring and rollback capabilities.
6. **Validate and Document** — Verify the implementation meets requirements. Document configuration and runbooks.

## Tools

- **Configuration Management** — Infrastructure as code and automation
- **Monitoring Stack** — Observability and alerting
- **Documentation Platform** — Runbooks and architecture docs


## Process

1. **Design** — Define interface, identify patterns, plan implementation
1. **Implement** — Write code following existing conventions, add tests
1. **Verify** — Run tests, check integration, validate behavior

## Verification

- [ ] All soc metrics and kpi tracking procedures executed completely and documented
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