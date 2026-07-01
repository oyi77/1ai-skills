---
name: performing-endpoint-forensics-investigation
description: 'Performs digital forensics investigation on compromised endpoints including memory acquisition, disk imaging,
  artifact analysis, and timeline reconstruction. Use when investigating security incidents, collecting evidence for legal
  proceedings, or analyzing endpoint compromise scope. Activates for requests involving endpoint forensics, memory analysis,
  disk forensics, or incident investigation.

  '
domain: cybersecurity
tags:
- endpoint
- forensics
- memory-analysis
- disk-imaging
- incident-investigation
- Volatility
subdomain: endpoint-security
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- PR.PS-02
- DE.CM-01
- PR.IR-01
---
# Performing Endpoint Forensics Investigation

## Overview

Cybersecurity skill for performing endpoint forensics investigation. Follows industry best practices and security standards.

## When to Use

**Trigger phrases:**
- "performing endpoint forensics investigation"
- "Investigating a confirmed or suspected endpoint compromise requiring forensic an"
- "Collecting volatile and non-volatile evidence for incident response or legal pro"
- "Analyzing memory dumps for malware, injected code, or credential theft artifacts"


Use this skill when:
- Investigating a confirmed or suspected endpoint compromise requiring forensic analysis
- Collecting volatile and non-volatile evidence for incident response or legal proceedings
- Analyzing memory dumps for malware, injected code, or credential theft artifacts
- Reconstructing attacker timelines from endpoint artifacts (prefetch, shimcache, amcache)

**Do not use** this skill for live threat hunting (use EDR/SIEM) or network forensics.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Forensic workstation with analysis tools (Volatility 3, KAPE, Autopsy, Eric Zimmerman tools)
- Write-blocker for disk imaging (hardware or software)
- Secure evidence storage with chain-of-custody documentation
- Memory acquisition tool (WinPMEM, FTK Imager, Magnet RAM Capture)
- Administrative access to the target endpoint (or physical access)

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

1. **Plan Operations** — Define objectives, scope, and success criteria for endpoint forensics investigation operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for endpoint forensics investigation.
3. **Execute Core Workflow** — Perform the endpoint forensics investigation operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Reconnaissance** — Gather target information, identify attack surface, enumerate services
1. **Analysis/Exploitation** — Execute the technique, analyze results, document findings
1. **Reporting** — Document IOCs, write findings, provide remediation recommendations

## Verification

- [ ] All endpoint forensics investigation procedures executed completely and documented
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