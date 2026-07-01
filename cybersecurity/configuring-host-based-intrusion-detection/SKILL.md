---
name: configuring-host-based-intrusion-detection
description: 'Configures host-based intrusion detection systems (HIDS) to monitor endpoint file integrity, system calls, and
  configuration changes for security violations. Use when deploying OSSEC, Wazuh, or AIDE for endpoint monitoring, building
  file integrity monitoring (FIM) policies, or meeting compliance requirements for change detection. Activates for requests
  involving HIDS configuration, file integrity monitoring, OSSEC/Wazuh deployment, or host-based detection.

  '
domain: cybersecurity
tags:
- endpoint
- HIDS
- Wazuh
- OSSEC
- file-integrity-monitoring
- intrusion-detection
subdomain: endpoint-security
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- PR.PS-02
- DE.CM-01
- PR.IR-01
---
# Configuring Host Based Intrusion Detection

## Overview

Cybersecurity skill for configuring host based intrusion detection. Follows industry best practices and security standards.

## When to Use

**Trigger phrases:**
- "configuring host based intrusion detection"
- "Deploying HIDS agents (Wazuh, OSSEC, AIDE) across Windows and Linux endpoints"
- "Configuring file integrity monitoring (FIM) for compliance (PCI DSS 11"
- "Monitoring system configuration changes, rootkit detection, and security policy"


Use this skill when:
- Deploying HIDS agents (Wazuh, OSSEC, AIDE) across Windows and Linux endpoints
- Configuring file integrity monitoring (FIM) for compliance (PCI DSS 11.5, NIST SI-7)
- Monitoring system configuration changes, rootkit detection, and security policy violations
- Integrating HIDS alerts with SIEM platforms for centralized monitoring

**Do not use** this skill for network-based IDS (Suricata, Snort) or for EDR deployment.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Wazuh server (manager) deployed and accessible from endpoints
- Administrative access to target endpoints
- Network connectivity: agents to Wazuh manager on port 1514 (TCP/UDP) and 1515 (TCP enrollment)
- Wazuh dashboard (OpenSearch Dashboards) for alert visualization
- Understanding of critical files/directories to monitor per OS

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

1. **Define Objectives** — Clarify the goals and scope for host based intrusion detection.
2. **Gather Resources** — Collect tools, data, and access needed for host based intrusion detection.
3. **Execute Process** — Carry out host based intrusion detection operations methodically.
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

- [ ] All host based intrusion detection procedures executed completely and documented
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