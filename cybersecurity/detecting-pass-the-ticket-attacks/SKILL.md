---
name: detecting-pass-the-ticket-attacks
description: Detect Kerberos Pass-the-Ticket (PtT) attacks by analyzing Windows Event IDs 4768, 4769, and 4771 for anomalous
  ticket usage patterns in Splunk and Elastic SIEM
domain: cybersecurity
subdomain: threat-detection
tags:
- kerberos
- pass-the-ticket
- active-directory
- splunk
- elastic
- credential-theft
- windows-security
version: '1.0'
author: mahipal
license: Apache-2.0
d3fend_techniques:
- Token Binding
- Execution Isolation
- Restore Access
- Application Protocol Command Analysis
- Process Termination
nist_csf:
- DE.CM-01
- DE.AE-02
- DE.AE-06
- ID.RA-05
---

# Detecting Pass-the-Ticket Attacks

## Overview

Pass-the-Ticket (PtT) is a credential theft technique (MITRE ATT&CK T1550.003) where adversaries steal Kerberos tickets (TGT or TGS) from one system and replay them on another to authenticate without knowing the user's password. This skill teaches detection of PtT attacks by correlating Windows Security Event IDs 4768 (TGT request), 4769 (TGS request), and 4771 (pre-authentication failure) for anomalies such as ticket reuse across different hosts, RC4 encryption downgrades, and unusual service ticket request volumes.


## When to Use
**Trigger phrases:**
- "detecting pass the ticket attacks"
- "Detect Kerberos Pass-the-Ticket (PtT) attacks by analyzing Windows Event IDs 476"


- When investigating security incidents that require detecting pass the ticket attacks
- When building detection rules or threat hunting queries for this domain
- When SOC analysts need structured procedures for this analysis type
- When validating security monitoring coverage for related attack techniques

## Prerequisites

- Windows Domain Controller with advanced audit policy enabled (Audit Kerberos Authentication Service, Audit Kerberos Service Ticket Operations)
- Splunk or Elastic SIEM ingesting Windows Security event logs
- Sysmon deployed on endpoints for supplementary process telemetry
- Python 3.8+ with `requests` library

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

1. Enable Kerberos audit logging on Domain Controllers via Group Policy
2. Forward Event IDs 4768, 4769, and 4771 to SIEM platform
3. Deploy detection rules for RC4 encryption downgrade (TicketEncryptionType 0x17)
4. Create correlation rule for ticket reuse across multiple source IPs
5. Build baseline of normal TGS request volume per user/host
6. Alert on standard deviation anomalies in ticket request patterns
7. Investigate flagged events with enrichment from Active Directory

## Expected Output

JSON report containing detected PtT indicators including anomalous ticket requests, RC4 downgrades, cross-host ticket reuse events, and risk-scored users with MITRE ATT&CK technique mapping.
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
- Capturing traffic on networks without authorization or privacy considerations
- Leaving packet captures containing sensitive data unencrypted on disk
- Deploying inline blocking rules without testing for false positives first
## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- Captures verified as complete with no dropped packets
- Detection rules tested against known-benign traffic for false positive rate
- Alert thresholds validated and tuned to reduce noise

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |