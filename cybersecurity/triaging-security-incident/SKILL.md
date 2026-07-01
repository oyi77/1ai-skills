---
name: triaging-security-incident
description: 'Performs initial triage of security incidents to determine severity, scope, and required response actions using
  the NIST SP 800-61r3 and SANS PICERL frameworks. Classifies incidents by type, assigns priority based on business impact,
  and routes to appropriate response teams. Activates for requests involving incident triage, security alert classification,
  severity assessment, incident prioritization, or initial incident analysis.

  '. Use when working with triaging security incident.
domain: cybersecurity
tags:
- incident-triage
- NIST-800-61
- SANS-PICERL
- severity-classification
- SOC-operations
subdomain: incident-response
mitre_attack:
- T1190
- T1566
- T1078
- T1059
version: 1.0.0
author: mahipal
license: Apache-2.0
d3fend_techniques:
- Executable Denylisting
- Execution Isolation
- File Metadata Consistency Validation
- Content Format Conversion
- File Content Analysis
nist_csf:
- RS.MA-01
- RS.MA-02
- RS.AN-03
- RC.RP-01
---
# Triaging Security Incident

## Overview

Cybersecurity skill for triaging security incident. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "triaging security incident"
- "Performs initial triage of security incidents to determine severity, scope, and "


- A SIEM or EDR alert fires and requires human classification before escalation
- Multiple concurrent alerts arrive and the SOC must prioritize response order
- An end user reports suspicious activity and the incident needs initial categorization
- A threat intelligence feed matches an IOC observed in the environment

**Do not use** for routine vulnerability scanning results or compliance audit findings that do not represent active security incidents.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Access to SIEM platform (Splunk, Elastic, Microsoft Sentinel) with current alert data
- Incident classification taxonomy aligned to NIST SP 800-61r3 categories
- Predefined severity matrix mapping asset criticality to threat type
- Contact roster for escalation paths (Tier 1 through Tier 3 and CIRT)
- Asset inventory with business criticality ratings

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

1. **Define Objectives** — Clarify the goals and scope for security incident.
2. **Gather Resources** — Collect tools, data, and access needed for security incident.
3. **Execute Process** — Carry out security incident operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Reconnaissance** — Gather target information, identify attack surface, enumerate services
1. **Analysis/Exploitation** — Execute the technique, analyze results, document findings
1. **Reporting** — Document IOCs, write findings, provide remediation recommendations

## Verification

- [ ] All security incident procedures executed completely and documented
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