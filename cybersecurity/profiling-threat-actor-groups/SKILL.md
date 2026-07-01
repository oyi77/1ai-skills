---
name: profiling-threat-actor-groups
description: Develops comprehensive threat actor profiles for APT groups, criminal organizations, and hacktivist collectives
  by aggregating TTP documentation, historical campaign data, tooling fingerprints, and attribution indicators from multiple
  intelligence sources. Use when briefing executives on sector-specific threats, updating threat model assumptions, or prioritizing
  defensive controls against specific adversaries.
domain: cybersecurity
tags:
- MITRE-ATT&CK
- threat-actor
- APT
- CrowdStrike
- Mandiant
- attribution
- kill-chain
- NIST-CSF
subdomain: threat-intelligence
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- ID.RA-01
- ID.RA-05
- DE.CM-01
- DE.AE-02
---
# Profiling Threat Actor Groups

## Overview

Cybersecurity skill for profiling threat actor groups. Follows industry best practices and security standards.

## When to Use

**Trigger phrases:**
- "profiling threat actor groups"
- "Updating the organization's threat model with profiles of adversary groups recen"
- "Preparing an executive briefing on APT groups that align with geopolitical event"
- "Enabling SOC analysts to understand attacker objectives and TTPs to improve dete"


Use this skill when:
- Updating the organization's threat model with profiles of adversary groups recently observed targeting your sector
- Preparing an executive briefing on APT groups that align with geopolitical events affecting your business
- Enabling SOC analysts to understand attacker objectives and TTPs to improve detection tuning

**Do not use** this skill for real-time incident attribution — attribution during active incidents should be deprioritized in favor of containment. Profile refinement occurs post-incident.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Access to MITRE ATT&CK Groups database (https://attack.mitre.org/groups/)
- Commercial threat intelligence subscription (Mandiant Advantage, CrowdStrike Falcon Intelligence, or Recorded Future)
- Sector-specific ISAC membership for targeted intelligence (FS-ISAC, H-ISAC, E-ISAC)
- Structured profile template (see workflow below)

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

1. **Define Objectives** — Clarify the goals and scope for threat actor groups.
2. **Gather Resources** — Collect tools, data, and access needed for threat actor groups.
3. **Execute Process** — Carry out threat actor groups operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run profiling threat actor groups workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All threat actor groups procedures executed completely and documented
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