---
name: detecting-evasion-techniques-in-endpoint-logs
description: 'Detects defense evasion techniques used by adversaries in endpoint logs including log tampering, timestomping,
  process injection, and security tool disabling. Use when investigating suspicious endpoint behavior, building detection
  rules for evasion tactics, or conducting threat hunting for stealthy adversary activity. Activates for requests involving
  evasion detection, defense evasion analysis, log tampering detection, or MITRE ATT&CK TA0005.

  '
domain: cybersecurity
tags:
- endpoint
- edr
- threat-hunting
- defense-evasion
- MITRE-ATT&CK
- detection-engineering
subdomain: endpoint-security
version: 1.0.0
author: mahipal
license: Apache-2.0
d3fend_techniques:
- File Metadata Consistency Validation
- Content Format Conversion
- File Content Analysis
- Platform Hardening
- File Format Verification
nist_csf:
- PR.PS-01
- PR.PS-02
- DE.CM-01
- PR.IR-01
---
# Detecting Evasion Techniques In Endpoint Logs

## Overview

Cybersecurity skill for detecting evasion techniques in endpoint logs. Follows industry best practices and security standards.

## When to Use

**Trigger phrases:**
- "detecting evasion techniques in endpoint logs"
- "Hunting for adversary defense evasion techniques (MITRE ATT&CK TA0005) in endpoi"
- "Building detection rules for common evasion methods (process injection, timestom"
- "Investigating incidents where adversaries disabled or bypassed security tools"


Use this skill when:
- Hunting for adversary defense evasion techniques (MITRE ATT&CK TA0005) in endpoint telemetry
- Building detection rules for common evasion methods (process injection, timestomping, log clearing)
- Investigating incidents where adversaries disabled or bypassed security tools
- Analyzing endpoint logs for indicators of living-off-the-land binary (LOLBin) abuse

**Do not use** this skill for network-level evasion (use network traffic analysis) or for malware reverse engineering.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Sysmon installed and configured with comprehensive logging rules (SwiftOnSecurity or Olaf Hartong config)
- Windows Security Event Log with advanced audit policy enabled
- EDR telemetry (CrowdStrike, SentinelOne, Microsoft Defender for Endpoint)
- SIEM platform for log correlation (Splunk, Elastic, Sentinel)
- MITRE ATT&CK Enterprise matrix for technique reference

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

1. **Define Detection Scope** — Identify the specific evasion techniques in endpoint logs techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for evasion techniques in endpoint logs.
3. **Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting evasion techniques in endpoint logs indicators.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis


## Process

1. **Reconnaissance** — Gather target information, identify attack surface, enumerate services
1. **Analysis/Exploitation** — Execute the technique, analyze results, document findings
1. **Reporting** — Document IOCs, write findings, provide remediation recommendations

## Verification

- [ ] All evasion techniques in endpoint logs procedures executed completely and documented
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