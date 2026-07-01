---
name: detecting-shadow-it-cloud-usage
description: Detect unauthorized SaaS and cloud service usage (shadow IT) by analyzing proxy logs, DNS query logs, and netflow
  data using Python pandas for traffic pattern analysis and domain classification. Use when detecting unauthorized saas and cloud service usage (shadow it) by.
domain: cybersecurity
subdomain: cloud-security
tags:
- shadow-IT
- SaaS-discovery
- proxy-logs
- DNS-analysis
- netflow
- cloud-security
- pandas
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.IR-01
- ID.AM-08
- GV.SC-06
- DE.CM-01
---

# Detecting Shadow IT Cloud Usage

## Overview

Shadow IT refers to unauthorized SaaS applications and cloud services used without IT approval. This skill analyzes proxy logs, DNS query logs, and firewall/netflow data to identify unauthorized cloud service usage, classify discovered domains against known SaaS categories, measure data transfer volumes, and flag high-risk services based on security posture and compliance requirements.


## When to Use
**Trigger phrases:**
- "detecting shadow it cloud usage"
- "Detect unauthorized SaaS and cloud service usage (shadow IT) by analyzing proxy "


- When investigating security incidents that require detecting shadow it cloud usage
- When building detection rules or threat hunting queries for this domain
- When SOC analysts need structured procedures for this analysis type
- When validating security monitoring coverage for related attack techniques

## Prerequisites

- Python 3.9+ with `pandas`, `tldextract`
- Proxy logs (Squid, Zscaler, or Palo Alto format) or DNS query logs
- SaaS application catalog/blocklist for classification
- Network firewall logs with FQDN resolution (optional)

## Steps

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

1. Parse proxy access logs and extract destination domains with traffic volumes
2. Parse DNS query logs to identify resolved cloud service domains
3. Aggregate traffic by domain using pandas — total bytes, request counts, unique users
4. Classify domains against known SaaS categories (storage, email, dev tools, AI)
5. Flag unauthorized services not on the approved application list
6. Calculate risk scores based on data volume, user count, and service category
7. Generate shadow IT discovery report with remediation recommendations

## Expected Output

- JSON report listing discovered cloud services with traffic volumes, user counts, risk scores, and approval status
- Top unauthorized services ranked by data exfiltration risk
## When NOT to Use

- You need to perform the attack to test detection (use performing-* skills)
- Task is about analyzing past incidents (use analyzing-* skills)
- You need to implement detection rules (use implementing-* skills)
- Task is about threat hunting proactively (use hunting-* skills)
- You don't have access to logs or monitoring data
- Task requires incident response (use IR skills)


## Red Flags

- Performing actions without explicit written authorization from the asset owner
- Testing against production systems without a defined scope and rules of engagement
- Modifying cloud IAM policies or security groups without approval
- Exposing cloud credentials or secrets in logs or reports
- Running scans that generate excessive API calls and trigger billing alerts

## Process

1. **Reconnaissance** — Gather target information, identify attack surface, enumerate services
1. **Analysis/Exploitation** — Execute the technique, analyze results, document findings
1. **Reporting** — Document IOCs, write findings, provide remediation recommendations

## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- Cloud resource changes reverted or documented as intentional
- IAM policies reviewed for least-privilege compliance after testing
- No residual test resources left running (cost and security check)

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |