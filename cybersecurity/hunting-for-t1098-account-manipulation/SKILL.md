---
name: hunting-for-t1098-account-manipulation
description: Hunt for MITRE ATT&CK T1098 account manipulation including shadow admin creation, SID history injection, group
  membership changes, and credential modifications using Windows Security Event Logs. Use when hunting for mitre att&ck t1098 account manipulation including shadow admin.
domain: cybersecurity
subdomain: threat-hunting
tags:
- threat-hunting
- mitre-attack
- t1098
- account-manipulation
- active-directory
- persistence
version: '1.0'
author: mahipal
license: Apache-2.0
d3fend_techniques:
- Token Binding
- Restore Access
- Application Protocol Command Analysis
- Password Authentication
- Biometric Authentication
nist_csf:
- DE.CM-01
- DE.AE-02
- DE.AE-07
- ID.RA-05
---
# Hunting for T1098 Account Manipulation

## Overview

MITRE ATT&CK T1098 (Account Manipulation) covers adversary actions to maintain or expand access to compromised accounts, including adding credentials, modifying group memberships, SID history injection, and creating shadow admin accounts. This skill covers detecting these techniques through Windows Security Event Log analysis (Event IDs 4738, 4728, 4732, 4756, 4670, 5136), correlating group membership changes with privilege escalation indicators, and identifying anomalous account modification patterns.


## When to Use
**Trigger phrases:**
- "hunting for t1098 account manipulation"
- "Hunt for MITRE ATT&CK T1098 account manipulation including shadow admin creation"


- When investigating security incidents that require hunting for t1098 account manipulation
- When building detection rules or threat hunting queries for this domain
- When SOC analysts need structured procedures for this analysis type
- When validating security monitoring coverage for related attack techniques

## Prerequisites

- Windows Security Event Logs (EVTX format) or SIEM access
- Python 3.9+ with `python-evtx`, `lxml` libraries
- Understanding of Active Directory group structure and SID architecture
- Familiarity with MITRE ATT&CK T1098 sub-techniques

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

1. **Scope the task** — define objectives, boundaries, and success criteria
2. **Gather information** — collect all necessary data and context before proceeding
3. **Execute the core workflow** — follow the domain-specific steps methodically
4. **Validate results** — verify outputs against expected outcomes or baselines
5. **Document findings** — record results, anomalies, and recommendations
### Step 1: Parse Account Modification Events
Extract Event IDs 4738 (user account changed), 4728/4732/4756 (member added to security groups), and 5136 (directory service object modified).

### Step 2: Detect Privileged Group Changes
Flag additions to Domain Admins, Enterprise Admins, Schema Admins, Administrators, and Backup Operators groups.

### Step 3: Identify Shadow Admin Indicators
Detect accounts receiving AdminSDHolder protection, direct privilege assignment, or SID history injection.

### Step 4: Correlate with Attack Timeline
Cross-reference account changes with authentication events to identify initial compromise and persistence establishment.

## Expected Output

JSON report with detected account manipulation events, privileged group changes, shadow admin indicators, and timeline correlation.
## When NOT to Use

- You're responding to a known incident (use IR skills)
- Task is about analyzing confirmed malware (use analyzing-* skills)
- You need to implement detection rules (use implementing-* skills)
- Task is about vulnerability scanning (use scanning tools)
- You don't have access to endpoint/network data
- Task requires compliance auditing (use auditing-* skills)


## Red Flags

- Performing actions without explicit written authorization from the asset owner
- Testing against production systems without a defined scope and rules of engagement
- Testing without rate limiting, potentially causing service degradation
- Storing sensitive test data (credentials, tokens) in plain text logs
- Using automated scanners blindly without reviewing results for false positives

## Process

1. **Reconnaissance** — Gather target information, identify attack surface, enumerate services
1. **Analysis/Exploitation** — Execute the technique, analyze results, document findings
1. **Reporting** — Document IOCs, write findings, provide remediation recommendations

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