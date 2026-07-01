---
name: analyzing-sbom-for-supply-chain-vulnerabilities
description: Parses Software Bill of Materials (SBOM) in CycloneDX and SPDX JSON formats to identify supply chain vulnerabilities
  by correlating components against the NVD CVE database via the NVD 2.0 API. Builds dependency graphs, calculates risk scores,
  identifies transitive vulnerability paths, and generates compliance reports.
domain: cybersecurity
tags:
- SBOM
- CycloneDX
- SPDX
- NVD
- CVE
- supply-chain
- dependency-analysis
- syft
- grype
subdomain: supply-chain-security
version: 1.0.0
author: mukul975
license: Apache-2.0
atlas_techniques:
- AML.T0010
- AML.T0104
nist_ai_rmf:
- GOVERN-5.2
- MAP-1.6
- MANAGE-2.2
- GOVERN-1.1
- GOVERN-4.2
nist_csf:
- GV.SC-01
- GV.SC-03
- GV.SC-06
- GV.SC-07
---
# Analyzing Sbom For Supply Chain Vulnerabilities

## Overview

Cybersecurity skill for analyzing sbom for supply chain vulnerabilities. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "analyzing sbom for supply chain vulnerabilities"
- "Parses Software Bill of Materials (SBOM) in CycloneDX and SPDX JSON formats to i"


- A new regulatory requirement (EO 14028, EU CRA) mandates SBOM analysis for software deliveries
- Security team needs to assess third-party risk by scanning vendor-provided SBOMs
- CI/CD pipeline requires automated vulnerability checks against generated SBOMs
- Incident response needs to determine if a newly disclosed CVE affects deployed software
- Procurement team requires supply chain risk assessment for a software acquisition

**Do not use** for runtime vulnerability scanning of live systems; use container scanning tools (Trivy, Grype CLI) or host-based vulnerability scanners (Nessus, Qualys) instead.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- SBOM file in CycloneDX JSON (v1.4+) or SPDX JSON (v2.3+) format
- Python 3.9+ with requests, networkx, and packaging libraries installed
- NVD API key (free, from https://nvd.nist.gov/developers/request-an-api-key) for higher rate limits
- Network access to NVD API (https://services.nvd.nist.gov/rest/json/cves/2.0)
- Optionally: syft for SBOM generation, grype for cross-validation

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

1. **Scope the Analysis** — Define what sbom artifacts or data sources to examine and the investigation timeline.
2. **Preserve Evidence** — Create forensic copies of relevant data. Maintain chain of custody documentation.
3. **Extract Key Indicators** — Use supply chain vulnerabilities to parse and extract relevant sbom data points from collected artifacts.
4. **Correlate Findings** — Cross-reference extracted data with other sources (threat intel, logs, timelines).
5. **Build Timeline** — Construct a chronological sequence of events related to sbom.
6. **Document Analysis** — Write findings report with evidence, conclusions, and recommendations.

## Tools

- **supply chain vulnerabilities** — Primary tool for this skill
- **Forensic Toolkit** — Evidence collection and analysis
- **Timeline Tools** — Chronological event reconstruction
- **Log Analysis Platform** — Centralized log parsing and search


## Process

1. **Reconnaissance** — Gather target information, identify attack surface, enumerate services
1. **Analysis/Exploitation** — Execute the technique, analyze results, document findings
1. **Reporting** — Document IOCs, write findings, provide remediation recommendations

## Verification

- [ ] All sbom procedures executed completely and documented
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