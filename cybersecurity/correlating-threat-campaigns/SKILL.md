---
name: correlating-threat-campaigns
description: Correlates disparate security incidents, IOCs, and adversary behaviors across time and organizations to identify
  unified threat campaigns, attribute them to common threat actors, and extract shared indicators for improved detection.
  Use when multiple incidents exhibit overlapping indicators, when sector-wide attack campaigns require cross-organizational
  analysis, or when building campaign-level intelligence products.
domain: cybersecurity
tags:
- campaign-analysis
- correlation
- MISP
- ATT&CK
- threat-actor
- intrusion-set
- clustering
- CTI
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
# Correlating Threat Campaigns

## Overview

Cybersecurity skill for correlating threat campaigns. Follows industry best practices and security standards.

## When to Use

Use this skill when:
- Multiple unrelated-appearing incidents share IOCs (same C2 IP, same malware hash, similar TTPs)
- An ISAC partner shares indicators from an incident that match your own historical events
- Building a campaign report linking adversary activity over weeks or months to a single operation

**Do not use** this skill to force correlation based on weak signals — false campaign attribution misleads defenders and wastes resources on incorrect threat models.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- TIP or SIEM with historical indicator and event data (90+ days recommended)
- MISP correlation engine enabled with event sharing configured
- Graph analysis tool (Maltego, Neo4j, or OpenCTI) for relationship visualization
- Reference to MITRE ATT&CK intrusion set and campaign objects for structuring output

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

1. **Define Objectives** — Clarify the goals and scope for threat campaigns.
2. **Gather Resources** — Collect tools, data, and access needed for threat campaigns.
3. **Execute Process** — Carry out threat campaigns operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Research** — Analyze target audience, competitors, and trending topics
1. **Create** — Generate content following brand guidelines and best practices
1. **Publish & Optimize** — Distribute to target platforms, track performance, iterate

## Verification

- [ ] All threat campaigns procedures executed completely and documented
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