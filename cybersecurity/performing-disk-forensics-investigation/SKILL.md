---
name: performing-disk-forensics-investigation
description: >  'Conducts disk forensics investigations using forensic imaging, file system analysis, artifact recovery, and
  timeline reconstruction to support incident response cases. Utilizes tools such as FTK Imager, Autopsy, and The Sleuth Kit
  for evidence acquisition, deleted file recovery, and artifact examination. Activates for requests involving disk forensics,
  hard drive analysis, forensic imaging, file recovery, evidence acquisition, or digital forensic investigation.

  '.
domain: cybersecurity
tags:
- disk-forensics
- forensic-imaging
- evidence-acquisition
- file-recovery
- chain-of-custody
subdomain: incident-response
mitre_attack:
- T1070
- T1027
- T1036
- T1564
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- RS.MA-01
- RS.MA-02
- RS.AN-03
- RC.RP-01
---
# Performing Disk Forensics Investigation

## Overview

Cybersecurity skill for performing disk forensics investigation. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "performing disk forensics investigation"
- "Conducts disk forensics investigations using forensic imaging, file system analy"


- A security incident requires forensic analysis of a system's persistent storage
- Evidence preservation is needed for potential legal proceedings or HR investigations
- Deleted files, browser history, or application artifacts must be recovered
- A timeline of user or adversary activity must be reconstructed from file system metadata
- Malware persistence mechanisms stored on disk need identification and documentation

**Do not use** for volatile evidence (running processes, network connections); use memory forensics with Volatility instead.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Forensic workstation with write-blocking hardware or software (Tableau T35u, Arsenal Image Mounter)
- Forensic imaging software: FTK Imager, Guymager, or dd with dcfldd
- Analysis platform: Autopsy, FTK (Forensic Toolkit), or X-Ways Forensics
- Sufficient storage (2-3x the target drive size for image plus working copies)
- Chain of custody forms and evidence bags for physical media
- Hash verification tools for evidence integrity (SHA-256)

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

1. **Plan Operations** — Define objectives, scope, and success criteria for disk forensics investigation operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for disk forensics investigation.
3. **Execute Core Workflow** — Perform the disk forensics investigation operations following established procedures.
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

- [ ] All disk forensics investigation procedures executed completely and documented
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