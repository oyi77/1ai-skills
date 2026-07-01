---
name: performing-osint-with-spiderfoot
description: Automate OSINT collection using SpiderFoot REST API and CLI for target profiling, module-based reconnaissance,
  and structured result analysis across 200+ data sources
domain: cybersecurity
subdomain: threat-intelligence
tags:
- osint
- spiderfoot
- reconnaissance
- threat-intelligence
- attack-surface
- target-profiling
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- ID.RA-01
- ID.RA-05
- DE.CM-01
- DE.AE-02
---

# Performing OSINT with SpiderFoot

## Overview

SpiderFoot is an open-source OSINT automation tool with 200+ modules that integrates with data sources for threat intelligence and attack surface mapping. This skill uses the SpiderFoot REST API and CLI (sf.py/spiderfoot-cli) to create and manage scans, select modules by use case (footprint, investigate, passive), parse structured results for domains, IPs, email addresses, leaked credentials, and DNS records, and generate target intelligence profiles.


## When to Use
**Trigger phrases:**
- "performing osint with spiderfoot"
- "Automate OSINT collection using SpiderFoot REST API and CLI for target profiling"


- When conducting security assessments that involve performing osint with spiderfoot
- When following incident response procedures for related security events
- When performing scheduled security testing or auditing activities
- When validating security controls through hands-on testing

## Prerequisites

- SpiderFoot 4.0+ installed or SpiderFoot HX cloud account
- Python 3.8+ with requests library
- SpiderFoot server running on default port 5001
- Optional: API keys for VirusTotal, Shodan, HaveIBeenPwned modules

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

1. Connect to SpiderFoot REST API or use CLI interface
2. Create a new scan with target specification (domain, IP, email, name)
3. Select scan modules by use case (all, footprint, investigate, passive)
4. Monitor scan progress via API polling
5. Retrieve and parse scan results by data element type
6. Extract key findings: subdomains, IPs, emails, leaked credentials
7. Generate structured OSINT intelligence report

## Expected Output

JSON report containing OSINT findings organized by data type (domains, IPs, emails, credentials, DNS records), module source attribution, and target profile summary with risk indicators.
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
- Testing without rate limiting, potentially causing service degradation
- Storing sensitive test data (credentials, tokens) in plain text logs
- Using automated scanners blindly without reviewing results for false positives
## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- Vulnerabilities reproduced with proof-of-concept and impact analysis
- False positives filtered out through manual verification
- Fix recommendations include code-level remediation guidance

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |