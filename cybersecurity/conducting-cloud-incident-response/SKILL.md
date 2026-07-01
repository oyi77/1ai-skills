---
name: conducting-cloud-incident-response
description: 'Responds to security incidents in cloud environments (AWS, Azure, GCP) by performing identity-based containment,
  cloud-native log analysis, resource isolation, and forensic evidence acquisition adapted for ephemeral cloud infrastructure.
  Activates for requests involving cloud incident response, AWS security incident, Azure compromise, GCP breach, cloud forensics,
  or cloud identity compromise.

  '. Use when working with conducting cloud incident response.
domain: cybersecurity
tags:
- cloud-IR
- AWS-forensics
- Azure-incident-response
- GCP-security
- identity-containment
subdomain: incident-response
mitre_attack:
- T1078
- T1537
- T1580
- T1525
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- RS.MA-01
- RS.MA-02
- RS.AN-03
- RC.RP-01
---
# Conducting Cloud Incident Response

## Overview

Cybersecurity skill for conducting cloud incident response. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "conducting cloud incident response"
- "Responds to security incidents in cloud environments (AWS, Azure, GCP) by perfor"


- Cloud security posture management (CSPM) alerts on unauthorized resource changes
- CloudTrail, Azure Activity Logs, or GCP Audit Logs show suspicious API calls
- Cloud access keys or service principal credentials are suspected compromised
- Unauthorized compute instances, storage buckets, or IAM changes are detected
- A cloud-hosted application is breached and attacker activity spans cloud services

**Do not use** for on-premises-only incidents with no cloud component; use standard enterprise IR procedures.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Cloud-native logging enabled and centralized: AWS CloudTrail (all regions), Azure Activity/Sign-in Logs, GCP Cloud Audit Logs
- IR-specific cloud IAM roles pre-provisioned with read-only forensic access
- Isolated forensic account/subscription/project for evidence preservation
- Cloud incident response runbooks specific to each cloud provider
- Cloud-native security tools: AWS GuardDuty, Azure Defender for Cloud, GCP Security Command Center
- Network traffic logging: VPC Flow Logs (AWS/GCP), NSG Flow Logs (Azure)

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

1. **Scope the Analysis** — Define what cloud incident response artifacts or data sources to examine and the investigation timeline.
2. **Preserve Evidence** — Create forensic copies of relevant data. Maintain chain of custody documentation.
3. **Extract Key Indicators** — Parse and extract relevant cloud incident response data points from collected artifacts.
4. **Correlate Findings** — Cross-reference extracted data with other sources (threat intel, logs, timelines).
5. **Build Timeline** — Construct a chronological sequence of events related to cloud incident response.
6. **Document Analysis** — Write findings report with evidence, conclusions, and recommendations.

## Tools

- **Forensic Toolkit** — Evidence collection and analysis
- **Timeline Tools** — Chronological event reconstruction
- **Log Analysis Platform** — Centralized log parsing and search


## Process

1. **Reconnaissance** — Gather target information, identify attack surface, enumerate services
1. **Analysis/Exploitation** — Execute the technique, analyze results, document findings
1. **Reporting** — Document IOCs, write findings, provide remediation recommendations

## Verification

- [ ] All cloud incident response procedures executed completely and documented
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