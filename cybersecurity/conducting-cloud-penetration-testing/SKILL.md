---
name: conducting-cloud-penetration-testing
description: 'This skill outlines methodologies for performing authorized penetration testing against AWS, Azure, and GCP
  cloud environments. It covers understanding the shared responsibility model for testing scope, leveraging cloud-specific
  attack tools like Pacu and ScoutSuite, exploiting IAM misconfigurations, testing for SSRF to cloud metadata services, and
  reporting findings aligned to MITRE ATT&CK Cloud matrix.

  '
domain: cybersecurity
tags:
- cloud-pentesting
- offensive-security
- aws-exploitation
- shared-responsibility
- mitre-attack-cloud
subdomain: cloud-security
version: 1.0.0
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
- Token Binding
- Restore Access
- Application Protocol Command Analysis
- Reissue Credential
- Network Isolation
nist_csf:
- PR.IR-01
- ID.AM-08
- GV.SC-06
- DE.CM-01
---
# Conducting Cloud Penetration Testing

## Overview

Cybersecurity skill for conducting cloud penetration testing. Follows industry best practices and security standards.

## When to Use

- When performing authorized security assessments of cloud environments before production deployment
- When validating cloud security controls after a major architectural change or migration
- When compliance requirements mandate annual penetration testing of cloud infrastructure
- When testing incident response readiness by simulating realistic cloud-based attack scenarios
- When assessing lateral movement risk across multi-account or multi-cloud environments

**Do not use** for unauthorized testing against cloud accounts, for testing cloud provider infrastructure itself (covered by the shared responsibility model), or for DDoS simulation without explicit cloud provider approval.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Written authorization from the cloud account owner and scope definition document
- AWS, Azure, or GCP penetration testing policy acknowledgment (AWS no longer requires pre-approval for most services)
- Isolated testing account or explicitly scoped production account with breakglass procedures
- Cloud-specific offensive tooling installed: Pacu (AWS), ScoutSuite, Prowler, CloudFox
- MITRE ATT&CK Cloud matrix for finding classification

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

1. **Scope the Analysis** — Define what cloud penetration testing artifacts or data sources to examine and the investigation timeline.
2. **Preserve Evidence** — Create forensic copies of relevant data. Maintain chain of custody documentation.
3. **Extract Key Indicators** — Parse and extract relevant cloud penetration testing data points from collected artifacts.
4. **Correlate Findings** — Cross-reference extracted data with other sources (threat intel, logs, timelines).
5. **Build Timeline** — Construct a chronological sequence of events related to cloud penetration testing.
6. **Document Analysis** — Write findings report with evidence, conclusions, and recommendations.

## Tools

- **Forensic Toolkit** — Evidence collection and analysis
- **Timeline Tools** — Chronological event reconstruction
- **Log Analysis Platform** — Centralized log parsing and search

## Verification

- [ ] All cloud penetration testing procedures executed completely and documented
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