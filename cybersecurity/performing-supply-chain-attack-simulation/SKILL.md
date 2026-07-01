---
name: performing-supply-chain-attack-simulation
description: Simulate and detect software supply chain attacks including typosquatting detection via Levenshtein distance,
  dependency confusion testing against private registries, package hash verification with pip, and known vulnerability scanning
  with pip-audit. Use when working with performing supply chain attack simulation.
domain: cybersecurity
subdomain: application-security
tags:
- supply-chain
- typosquatting
- dependency-confusion
- package-verification
- pip-audit
- PyPI
- software-composition-analysis
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- PR.PS-04
- ID.RA-01
- PR.DS-10
---

# Performing Supply Chain Attack Simulation

## Overview

Software supply chain attacks exploit trust in package registries through typosquatting (registering names similar to popular packages), dependency confusion (publishing higher-version public packages matching private names), and compromised package distribution. This skill detects these attack vectors by computing Levenshtein distance between package names and popular PyPI packages, verifying package integrity via SHA-256 hash comparison, scanning for known CVEs with pip-audit, and testing dependency resolution order for confusion vulnerabilities.


## When to Use
**Trigger phrases:**
- "performing supply chain attack simulation"
- "Simulate and detect software supply chain attacks including typosquatting detect"


- When conducting security assessments that involve performing supply chain attack simulation
- When following incident response procedures for related security events
- When performing scheduled security testing or auditing activities
- When validating security controls through hands-on testing

## Prerequisites

- Python 3.9+ with `pip-audit`, `Levenshtein`, `requests`
- Access to PyPI JSON API (https://pypi.org/pypi/{package}/json)
- Network access for package metadata retrieval


> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Unauthorized use against systems you do not own or have written permission to test is illegal and may violate computer fraud laws.

## Key Detection Areas

1. **Typosquatting** — compare package names against top PyPI packages using edit distance thresholds
2. **Dependency confusion** — check if internal package names exist on public PyPI with higher version numbers
3. **Hash verification** — download packages and verify SHA-256 digests match published hashes
4. **Vulnerability scanning** — audit installed packages against OSV and PyPA advisory databases
5. **Metadata anomalies** — flag packages with suspicious author emails, missing homepages, or very recent first upload dates

## When NOT to Use

- You don't have explicit written authorization to test
- Task is about defense/detection, not offense (use detection skills)
- You need to implement security controls (use implementing-* skills)
- Task requires compliance auditing (use auditing-* skills)
- You're investigating an incident (use incident response skills)
- Target is out of scope for your engagement
- Task is about vulnerability scanning only (use scanning tools)


## Red Flags

- Performing actions without explicit written authorization from the asset owner
- Testing against production systems without a defined scope and rules of engagement
- Exceeding the authorized scope of the engagement
- Leaving persistent access mechanisms without explicit approval
- Causing denial-of-service on production systems during testing

## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- All exploited vulnerabilities documented with reproduction steps
- Scope boundaries confirmed — only authorized targets were tested
- Remediation recommendations included for every finding

## Output

JSON report with risk scores per package, detected attack vectors, hash verification results, and CVE findings.

## Process

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

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |