---
name: detecting-typosquatting-packages-in-npm-pypi
description: Detects typosquatting attacks in npm and PyPI package registries by analyzing package name similarity using Levenshtein
  distance and other string metrics, examining publish date heuristics to identify recently created packages mimicking established
  ones, and flagging download count anomalies where suspicious packages have disproportionately low usage compared to their
  legitimate targets.
domain: cybersecurity
tags:
- typosquatting
- npm
- pypi
- supply-chain
- package-security
- Levenshtein
- dependency-confusion
- malicious-packages
subdomain: supply-chain-security
version: 1.0.0
author: mukul975
license: Apache-2.0
nist_csf:
- GV.SC-01
- GV.SC-03
- GV.SC-06
- GV.SC-07
---
# Detecting Typosquatting Packages In Npm Pypi

## Overview

Cybersecurity skill for detecting typosquatting packages in npm pypi. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "detecting typosquatting packages in npm pypi"
- "Detects typosquatting attacks in npm and PyPI package registries by analyzing pa"


- Auditing project dependencies to identify packages whose names are suspiciously similar to popular libraries
- Proactively scanning package registries for newly published packages that may be typosquats of your organization's packages
- Investigating a suspected supply chain compromise where a developer installed a misspelled package name
- Building automated monitoring that alerts when new packages appear with names close to critical dependencies
- Assessing the risk profile of unfamiliar packages before adding them to a project's dependency tree

**Do not use** as the sole determination of malicious intent; name similarity alone does not prove a package is malicious. Do not use for bulk automated takedown requests without manual review of flagged packages. Do not use against private registries without authorization.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Python 3.9+ with `requests` and `python-Levenshtein` (or `rapidfuzz`) packages installed
- Network access to `https://pypi.org/pypi/<package>/json` (PyPI JSON API) and `https://registry.npmjs.org/<package>` (npm registry API)
- A list of popular or critical packages to monitor (e.g., top 1000 PyPI packages, organization's dependency list)
- Understanding of common typosquatting patterns: character omission, transposition, insertion, substitution, and hyphen/underscore manipulation

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

1. **Define Detection Scope** — Identify the specific typosquatting packages in npm pypi techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for typosquatting packages in npm pypi.
3. **Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting typosquatting packages in npm pypi indicators.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All typosquatting packages in npm pypi procedures executed completely and documented
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