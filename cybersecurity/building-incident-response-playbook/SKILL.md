---
name: building-incident-response-playbook
description: 'Designs and documents structured incident response playbooks that define step-by-step procedures for specific
  incident types aligned with NIST SP 800-61r3 and SANS PICERL frameworks. Covers playbook structure, decision trees, escalation
  criteria, RACI matrices, and integration with SOAR platforms. Activates for requests involving IR playbook creation, incident
  response procedure documentation, response runbook development, or SOAR playbook design.

  '
domain: cybersecurity
tags:
- IR-playbook
- runbook
- NIST-800-61
- SOAR-integration
- response-procedures
subdomain: incident-response
mitre_attack:
- T1190
- T1566
- T1078
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- RS.MA-01
- RS.MA-02
- RS.AN-03
- RC.RP-01
---
# Building Incident Response Playbook

## Overview

Cybersecurity skill for building incident response playbook. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "building incident response playbook"
- "Designs and documents structured incident response playbooks that define step-by"


- Establishing or maturing an incident response program from scratch
- Documenting procedures for a new incident type after a novel attack
- Automating response workflows in a SOAR platform (Cortex XSOAR, Splunk SOAR)
- Preparing for compliance audits requiring documented IR procedures (SOC 2, PCI-DSS, HIPAA)
- Conducting a gap analysis of existing IR capabilities against specific threat scenarios

**Do not use** for one-time ad hoc investigations; playbooks are reusable procedure documents, not case-specific reports.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Organizational risk assessment identifying top incident scenarios by likelihood and impact
- NIST SP 800-61r3 or SANS PICERL framework adopted as the organizational IR standard
- Asset inventory with business criticality ratings and data classification
- RACI chart defining roles: Incident Commander, SOC analysts, system administrators, legal, communications
- Existing detection capabilities inventory (SIEM rules, EDR detections, IDS signatures)
- SOAR platform access if building automated playbooks

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

1. **Assess Requirements** — Evaluate current environment and define incident response playbook implementation requirements.
2. **Design Architecture** — Plan the incident response playbook architecture, including components, integrations, and data flows.
3. **Configure Components** — Set up and configure each incident response playbook component according to best practices.
4. **Test Integration** — Validate that all components work together. Run functional and security tests.
5. **Deploy to Production** — Roll out the implementation with monitoring and rollback capabilities.
6. **Validate and Document** — Verify the implementation meets requirements. Document configuration and runbooks.

## Tools

- **Configuration Management** — Infrastructure as code and automation
- **Monitoring Stack** — Observability and alerting
- **Documentation Platform** — Runbooks and architecture docs

## Verification

- [ ] All incident response playbook procedures executed completely and documented
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