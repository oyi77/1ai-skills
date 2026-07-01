---
name: performing-file-carving-with-foremost
description: Recover files from disk images and unallocated space using Foremost's header-footer signature carving to extract
  evidence regardless of file system state. Use when working with performing file carving with foremost.
domain: cybersecurity
tags:
- forensics
- file-carving
- foremost
- data-recovery
- evidence-recovery
- unallocated-space
subdomain: digital-forensics
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- RS.AN-01
- RS.AN-03
- DE.AE-02
- RS.MA-01
---
# Performing File Carving With Foremost

## Overview

Cybersecurity skill for performing file carving with foremost. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "performing file carving with foremost"
- "Recover files from disk images and unallocated space using Foremost's header-foo"

- When recovering files from unallocated disk space or corrupted file systems
- For extracting evidence from formatted or wiped storage media
- When file system metadata is unavailable but raw data sectors contain evidence
- During investigations requiring recovery of specific file types from raw images
- As a complement to file system-based recovery for maximum evidence extraction


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites
- Foremost installed on forensic workstation
- Forensic disk image in raw (dd) format
- Sufficient output storage (potentially larger than source)
- Custom foremost.conf for specialized file types (optional)
- Understanding of file signatures (magic bytes) for target file types
- Scalpel as an alternative for performance-critical carving

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

1. **Plan Operations** — Define objectives, scope, and success criteria for file carving operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for file carving.
3. **Execute Core Workflow** — Use foremost to perform file carving operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **foremost** — Primary tool for this skill
- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Design** — Define interface, identify patterns, plan implementation
1. **Implement** — Write code following existing conventions, add tests
1. **Verify** — Run tests, check integration, validate behavior

## Verification

- [ ] All file carving procedures executed completely and documented
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