---
name: conducting-pass-the-ticket-attack
description: Pass-the-Ticket (PtT) is a lateral movement technique that uses stolen Kerberos tickets (TGT or TGS) to authenticate
  to services without knowing the user's password. By extracting Kerberos tickets fro
domain: cybersecurity
subdomain: red-teaming
tags:
- red-team
- adversary-simulation
- mitre-attack
- exploitation
- post-exploitation
- kerberos
- pass-the-ticket
- lateral-movement
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
- ID.RA-01
- GV.OV-02
- DE.AE-07
---
# Conducting Pass-the-Ticket Attack


> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Unauthorized use against systems you do not own or have written permission to test is illegal and may violate computer fraud laws.

## Overview

Pass-the-Ticket (PtT) is a lateral movement technique that uses stolen Kerberos tickets (TGT or TGS) to authenticate to services without knowing the user's password. By extracting Kerberos tickets from memory (LSASS) on a compromised host, an attacker can inject those tickets into their own session to impersonate the ticket owner and access resources as that user.


## When to Use

- When conducting security assessments that involve conducting pass the ticket attack
- When following incident response procedures for related security events
- When performing scheduled security testing or auditing activities
- When validating security controls through hands-on testing

## Prerequisites

- Familiarity with red teaming concepts and tools
- Access to a test or lab environment for safe execution
- Python 3.8+ with required dependencies installed
- Appropriate authorization for any testing activities

## MITRE ATT&CK Mapping

- **T1550.003** - Use Alternate Authentication Material: Pass the Ticket
- **T1003.001** - OS Credential Dumping: LSASS Memory
- **T1558** - Steal or Forge Kerberos Tickets
- **T1021.002** - Remote Services: SMB/Windows Admin Shares

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

1. **Scope and authorize** — confirm written authorization and define target boundaries
2. **Reconnaissance** — enumerate targets, services, and potential attack surfaces
3. **Exploitation** — attempt exploitation of identified vulnerabilities within scope
4. **Post-exploitation** — document access level, lateral movement, and data exposure
5. **Report and remediate** — compile findings with reproduction steps and fix recommendations
### Phase 1: Ticket Extraction
1. Gain local admin access on target workstation
2. Dump Kerberos tickets from LSASS memory using Mimikatz or Rubeus
3. Export tickets in .kirbi format (Mimikatz) or base64 (Rubeus)
4. Identify high-value tickets (Domain Admin TGTs, service tickets to critical systems)

### Phase 2: Ticket Injection
1. Purge existing Kerberos tickets from attacker session
2. Import/inject stolen ticket into current session
3. Verify ticket is loaded and valid
4. Access target resources using injected ticket

### Phase 3: Lateral Movement
1. Access remote systems using the stolen ticket identity
2. Perform actions as the impersonated user
3. Collect additional credentials from accessed systems
4. Document evidence of successful lateral movement

## When NOT to Use

- You don't have authorization for the assessment
- Task is about implementing findings (use implementing-* skills)
- You need to analyze results (use analyzing-* skills)
- Task is about building assessment tools (use building-* skills)
- Target is out of scope
- Task requires compliance certification (use auditing-* skills)


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

## Tools and Resources

| Tool | Purpose | Command |
|------|---------|---------|
| Mimikatz | Ticket export/import | sekurlsa::tickets /export, kerberos::ptt |
| Rubeus | Ticket dumping and injection | dump, ptt, tgtdeleg |
| Impacket ticketConverter | Convert between formats | ticketConverter.py ticket.kirbi ticket.ccache |
| Impacket psexec/smbexec | Remote execution with ticket | KRB5CCNAME=ticket.ccache psexec.py |

## Detection Indicators

- Event ID 4768 with unusual client addresses
- Event ID 4769 service ticket requests from unexpected hosts
- TGT usage from different IP than the TGT was issued to
- Multiple authentications from same ticket across different workstations

## Validation Criteria

- [ ] Kerberos tickets extracted from compromised host
- [ ] Tickets injected into attacker session
- [ ] Lateral movement demonstrated using stolen tickets
- [ ] Evidence captured for reporting

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |