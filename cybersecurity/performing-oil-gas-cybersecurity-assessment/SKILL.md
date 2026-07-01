---
name: performing-oil-gas-cybersecurity-assessment
description: This skill covers conducting cybersecurity assessments specific to oil and gas facilities including upstream
  (exploration/production), midstream (pipeline/transport), and downstream (refining/distribution) operations. It addresses
  SCADA systems controlling pipeline operations, DCS for refinery process control, safety instrumented systems for hazardous
  processes, remote terminal units at unmanned wellhead sites, and compliance with API 1164, TSA Pipeline Security Directives,
  IEC 62443, and NIS...
domain: cybersecurity
tags:
- ot-security
- ics
- scada
- industrial-control
- iec62443
- oil-gas
- pipeline-security
- api1164
subdomain: ot-ics-security
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- PR.IR-01
- DE.CM-01
- ID.AM-05
- GV.OC-02
---
# Performing Oil Gas Cybersecurity Assessment

## Overview

Cybersecurity skill for performing oil gas cybersecurity assessment. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "performing oil gas cybersecurity assessment"
- "This skill covers conducting cybersecurity assessments specific to oil and gas f"


- When conducting a cybersecurity assessment of a refinery, pipeline, or production facility
- When preparing for TSA Pipeline Security Directive compliance (SD-01, SD-02)
- When assessing cybersecurity posture against API Standard 1164 (Pipeline SCADA Security)
- When evaluating the security of remote wellhead SCADA systems and satellite communications
- When a merger, acquisition, or regulatory audit requires a comprehensive OT security evaluation

**Do not use** for IT-only corporate network assessments of oil and gas companies, for physical security assessments without a cyber component, or for environmental compliance assessments.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Written authorization from facility management and operations team
- Understanding of oil and gas operations (upstream, midstream, downstream processes)
- Familiarity with API 1164, TSA SD-01/SD-02, IEC 62443, and NIST CSF
- Passive monitoring tools for OT network traffic capture
- Access to network diagrams, SCADA architecture documentation, and safety studies (HAZOP)

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

1. **Plan Operations** — Define objectives, scope, and success criteria for oil gas cybersecurity assessment operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for oil gas cybersecurity assessment.
3. **Execute Core Workflow** — Perform the oil gas cybersecurity assessment operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All oil gas cybersecurity assessment procedures executed completely and documented
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