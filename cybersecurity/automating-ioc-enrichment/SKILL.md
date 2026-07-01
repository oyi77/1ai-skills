---
name: automating-ioc-enrichment
description: Automates the enrichment of raw indicators of compromise with multi-source threat intelligence context using
  SOAR platforms, Python pipelines, or TIP playbooks to reduce analyst triage time and standardize enrichment outputs. Use
  when building automated enrichment workflows integrated with SIEM alerts, email submission pipelines, or bulk IOC processing
  from threat feeds.
domain: cybersecurity
tags:
- SOAR
- enrichment
- IOC
- Cortex-XSOAR
- Splunk-SOAR
- VirusTotal
- automation
- CTI
- NIST-CSF
subdomain: threat-intelligence
version: 1.0.0
author: team-cybersecurity
license: Apache-2.0
nist_csf:
- ID.RA-01
- ID.RA-05
- DE.CM-01
- DE.AE-02
---
# Automating Ioc Enrichment

## Overview

Cybersecurity skill for automating ioc enrichment. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "automating ioc enrichment"
- "Automates the enrichment of raw indicators of compromise with multi-source threa"


Use this skill when:
- Building a SOAR playbook that automatically enriches SIEM alerts with threat intelligence context before routing to analysts
- Creating a Python pipeline for bulk IOC enrichment from phishing email submissions
- Reducing analyst mean time to triage (MTTT) by pre-populating alert context with VT, Shodan, and MISP data

**Do not use** this skill for fully automated blocking decisions without human review — enrichment automation should inform decisions, not execute blocks autonomously for high-impact actions.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- SOAR platform (Cortex XSOAR, Splunk SOAR, Tines, or n8n) or Python 3.9+ environment
- API keys: VirusTotal, AbuseIPDB, Shodan, and at minimum one TIP (MISP or OpenCTI)
- SIEM integration endpoint for alert consumption
- Rate limit budgets documented per API (VT: 4/min free, 500/min enterprise)

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

1. **Define Objectives** — Clarify the goals and scope for ioc enrichment.
2. **Gather Resources** — Collect tools, data, and access needed for ioc enrichment.
3. **Execute Process** — Carry out ioc enrichment operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run automating ioc enrichment workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All ioc enrichment procedures executed completely and documented
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