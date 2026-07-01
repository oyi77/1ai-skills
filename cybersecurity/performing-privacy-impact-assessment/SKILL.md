---
name: performing-privacy-impact-assessment
description: Automates the Privacy Impact Assessment (PIA) workflow including data flow mapping, privacy risk scoring matrices,
  GDPR Article 35 DPIA and CCPA/CPRA alignment checks, data inventory cataloging, and remediation tracking. Implements the
  NIST Privacy Framework PRAM methodology and ICO DPIA guidance for systematic identification and mitigation of privacy risks
  across processing activities.
domain: cybersecurity
tags:
- privacy
- impact-assessment
- GDPR
- CCPA
- NIST
- DPIA
- data-flow-mapping
- risk-scoring
subdomain: privacy-compliance
version: '1.0'
author: mukul975
license: Apache-2.0
nist_csf:
- GV.PO-01
- PR.DS-01
- GV.OC-05
---
# Performing Privacy Impact Assessment

## Overview

Cybersecurity skill for performing privacy impact assessment. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "performing privacy impact assessment"
- "Automates the Privacy Impact Assessment (PIA) workflow including data flow mappi"


- When launching a new system, product, or processing activity that handles personal data
- When conducting GDPR Article 35 Data Protection Impact Assessments (DPIAs)
- When evaluating CCPA/CPRA compliance for data processing operations
- When performing privacy risk assessments aligned to the NIST Privacy Framework
- When mapping data flows across organizational boundaries and third-party processors
- When building automated privacy governance and assessment pipelines
- When preparing for regulatory audits or demonstrating accountability obligations


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Familiarity with GDPR, CCPA/CPRA, and NIST Privacy Framework concepts
- Access to data processing inventories and system architecture documentation
- Python 3.8+ with required dependencies installed
- Appropriate authorization from the Data Protection Officer (DPO) or privacy team
- Knowledge of organizational data flows and third-party processor relationships

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

1. **Plan Operations** — Define objectives, scope, and success criteria for privacy impact assessment operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for privacy impact assessment.
3. **Execute Core Workflow** — Perform the privacy impact assessment operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Design** — Define interface, identify patterns, plan implementation
1. **Implement** — Write code following existing conventions, add tests
1. **Verify** — Run tests, check integration, validate behavior

## Verification

- [ ] All privacy impact assessment procedures executed completely and documented
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