---
name: detecting-rdp-brute-force-attacks
description: Detect RDP brute force attacks by analyzing Windows Security Event Logs for failed authentication patterns (Event
  ID 4625), successful logons after failures (Event ID 4624), NLA failures, and source IP frequency analysis.
domain: cybersecurity
subdomain: threat-detection
tags:
- threat-detection
- rdp
- brute-force
- windows-event-logs
- blue-team
- siem
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- DE.CM-01
- DE.AE-02
- DE.AE-06
- ID.RA-05
---
# Detecting RDP Brute Force Attacks

## Overview

RDP brute force attacks target Windows Remote Desktop Protocol services by attempting rapid credential guessing against exposed RDP endpoints. Detection relies on analyzing Windows Security Event Logs for Event ID 4625 (failed logon with Logon Type 10 or 3) and correlating with Event ID 4624 (successful logon) to identify compromised accounts. This skill covers parsing EVTX files with python-evtx, identifying attack patterns through source IP frequency analysis, detecting NLA bypass attempts, and generating actionable detection reports.


## When to Use
**Trigger phrases:**
- "detecting rdp brute force attacks"
- "Detect RDP brute force attacks by analyzing Windows Security Event Logs for fail"


- When investigating security incidents that require detecting rdp brute force attacks
- When building detection rules or threat hunting queries for this domain
- When SOC analysts need structured procedures for this analysis type
- When validating security monitoring coverage for related attack techniques

## Prerequisites

- Python 3.9+ with `python-evtx`, `lxml` libraries
- Windows Security EVTX log files (exported from Event Viewer or collected via WEF)
- Understanding of Windows authentication Event IDs (4624, 4625, 4776)
- Familiarity with RDP Logon Types (Type 3 for NLA, Type 10 for RemoteInteractive)

## Steps

1. **Scope and authorize** — confirm written authorization and define target boundaries
2. **Reconnaissance** — enumerate targets, services, and potential attack surfaces
3. **Exploitation** — attempt exploitation of identified vulnerabilities within scope
4. **Post-exploitation** — document access level, lateral movement, and data exposure
5. **Report and remediate** — compile findings with reproduction steps and fix recommendations
### Step 1: Export Security Event Logs
Export Windows Security logs to EVTX format using Event Viewer or wevtutil:
```
wevtutil epl Security C:\logs\security.evtx
```

### Step 2: Parse Failed Logon Events
Use python-evtx to parse Event ID 4625 entries, extracting source IP, target username, failure reason (Sub Status), and Logon Type fields.

### Step 3: Analyze Attack Patterns
Identify brute force patterns by:
- Counting failed logons per source IP within time windows
- Detecting username spray attacks (many usernames from one IP)
- Correlating 4625 failures with subsequent 4624 success from same IP

### Step 4: Generate Detection Report
Produce a JSON report with top attacking IPs, targeted accounts, time-based analysis, and compromise indicators.

## Expected Output

JSON report containing:
- Total failed logon events and unique source IPs
- Top attacking IPs ranked by failure count
- Targeted usernames and failure sub-status codes
- Successful logons following brute force attempts (potential compromises)
- Time-series analysis of attack intensity
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
- Exceeding the authorized scope of the engagement
- Leaving persistent access mechanisms without explicit approval
- Causing denial-of-service on production systems during testing
## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- All exploited vulnerabilities documented with reproduction steps
- Scope boundaries confirmed — only authorized targets were tested
- Remediation recommendations included for every finding

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |