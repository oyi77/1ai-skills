---
name: auditing-tls-certificate-transparency-logs
description: Monitors Certificate Transparency (CT) logs to detect unauthorized certificate issuance, discover subdomains
  via CT data, and alert on suspicious certificate activity for owned domains. Uses the crt.sh API and direct CT log querying
  based on RFC 6962 to build continuous monitoring pipelines that catch rogue certificates, track CA behavior, and map the
  external attack surface.
domain: cybersecurity
tags:
- certificate-transparency
- CT-logs
- crt-sh
- subdomain-discovery
- TLS-monitoring
- RFC-6962
subdomain: threat-intelligence
version: 1.0.0
author: mukul975
license: Apache-2.0
nist_csf:
- ID.RA-01
- ID.RA-05
- DE.CM-01
- DE.AE-02
---
# Auditing Tls Certificate Transparency Logs

## Overview

Cybersecurity skill for auditing tls certificate transparency logs. Follows industry best practices and security standards.

## When to Use

- Monitoring owned domains for unauthorized or unexpected certificate issuance by unknown Certificate Authorities
- Discovering subdomains and hidden services through certificates logged in public CT logs
- Detecting phishing infrastructure that uses look-alike domain certificates (typosquatting, homograph attacks)
- Auditing Certificate Authority compliance by verifying all issued certificates appear in CT logs as required by browser policies
- Building continuous certificate monitoring into a security operations pipeline with alerting for new issuances

**Do not use** for attacking or disrupting Certificate Authorities, for scraping CT logs in violation of rate limits or terms of service, or as the sole method of subdomain enumeration without corroborating results through DNS verification.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Python 3.10+ with `requests`, `cryptography`, and `pyOpenSSL` libraries installed
- Network access to crt.sh (HTTPS) and public CT log servers
- A list of domains to monitor (owned domains, brand variations, typosquat candidates)
- SMTP credentials or webhook URL for alerting on new certificate discoveries
- Basic understanding of X.509 certificate structure and TLS certificate chain validation

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

1. **Define Objectives** — Clarify the goals and scope for tls certificate transparency logs.
2. **Gather Resources** — Collect tools, data, and access needed for tls certificate transparency logs.
3. **Execute Process** — Carry out tls certificate transparency logs operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All tls certificate transparency logs procedures executed completely and documented
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