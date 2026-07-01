---
name: investigating-insider-threat-indicators
description: 'Investigates insider threat indicators including data exfiltration attempts, unauthorized access patterns, policy
  violations, and pre-departure behaviors using SIEM analytics, DLP alerts, and HR data correlation. Use when SOC teams receive
  insider threat referrals from HR, detect anomalous data movement by employees, or need to build investigation timelines
  for potential insider threats.

  '
domain: cybersecurity
tags:
- soc
- insider-threat
- data-exfiltration
- dlp
- ueba
- investigation
- hr-correlation
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
# Investigating Insider Threat Indicators

## Overview

Cybersecurity skill for investigating insider threat indicators. Follows industry best practices and security standards.

## When to Use

**Trigger phrases:**
- "investigating insider threat indicators"
- "HR refers a departing employee for monitoring during their notice period"
- "DLP alerts indicate bulk data downloads or transfers to personal storage"
- "UEBA detects anomalous access patterns deviating significantly from peer baselin"


Use this skill when:
- HR refers a departing employee for monitoring during their notice period
- DLP alerts indicate bulk data downloads or transfers to personal storage
- UEBA detects anomalous access patterns deviating significantly from peer baselines
- Management reports concerns about an employee accessing sensitive data outside their role

**Do not use** without proper legal authorization — insider threat investigations must be coordinated with HR, Legal, and Privacy teams before monitoring begins.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Legal authorization and HR referral documenting investigation justification
- SIEM with DLP, endpoint, email, proxy, and authentication log sources
- Data Loss Prevention (DLP) system (Microsoft Purview, Symantec, Forcepoint) with policy alerts
- Endpoint monitoring capability (EDR with USB/removable media logging)
- HR data feed providing employment status, notice dates, and access entitlements
- Chain of custody procedures for evidence preservation

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

1. **Define Objectives** — Clarify the goals and scope for insider threat indicators.
2. **Gather Resources** — Collect tools, data, and access needed for insider threat indicators.
3. **Execute Process** — Carry out insider threat indicators operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run investigating insider threat indicators workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All insider threat indicators procedures executed completely and documented
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