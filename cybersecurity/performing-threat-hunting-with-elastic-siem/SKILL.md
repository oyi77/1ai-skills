---
name: performing-threat-hunting-with-elastic-siem
description: 'Performs proactive threat hunting in Elastic Security SIEM using KQL/EQL queries, detection rules, and Timeline
  investigation to identify threats that evade automated detection. Use when SOC teams need to hunt for specific ATT&CK techniques,
  investigate anomalous behaviors, or validate detection coverage gaps using Elasticsearch and Kibana Security.

  '
domain: cybersecurity
tags:
- soc
- elastic
- siem
- threat-hunting
- kql
- eql
- mitre-attack
- kibana
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
d3fend_techniques:
- Application Protocol Command Analysis
- Network Isolation
- Network Traffic Analysis
- Client-server Payload Profiling
- Network Traffic Community Deviation
nist_csf:
- DE.CM-01
- DE.AE-02
- RS.MA-01
- DE.AE-06
---
# Performing Threat Hunting With Elastic Siem

## Overview

Cybersecurity skill for performing threat hunting with elastic siem. Follows industry best practices and security standards.

## When to Use

Use this skill when:
- SOC teams need to proactively search for threats not caught by existing detection rules
- Threat intelligence reports describe new TTPs requiring validation against historical data
- Red team exercises reveal detection gaps that need hunting query development
- Periodic hunting cadence requires structured hypothesis-driven investigations

**Do not use** for real-time alert triage — that belongs in the Elastic Security Alerts queue with automated detection rules.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Elastic Security 8.x+ with Security app enabled in Kibana
- Data ingestion via Elastic Agent (Endpoint Security integration) or Beats (Winlogbeat, Filebeat, Packetbeat)
- Data normalized to Elastic Common Schema (ECS) field mappings
- User role with `kibana_security_solution` and `read` access to relevant indices
- MITRE ATT&CK framework knowledge for hypothesis generation

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

1. **Plan Operations** — Define objectives, scope, and success criteria for threat hunting operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for threat hunting.
3. **Execute Core Workflow** — Use elastic siem to perform threat hunting operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **elastic siem** — Primary tool for this skill
- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All threat hunting procedures executed completely and documented
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