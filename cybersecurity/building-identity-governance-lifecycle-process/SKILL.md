---
name: building-identity-governance-lifecycle-process
description: 'Builds comprehensive identity governance and lifecycle management processes including joiner-mover-leaver automation,
  role mining, access request workflows, periodic recertification, and orphaned account remediation using IGA platforms. Activates
  for requests involving identity lifecycle management, JML processes, role-based access provisioning, or identity governance
  program design.

  '. Use when working with building identity governance lifecycle process.
domain: cybersecurity
tags:
- identity-governance
- lifecycle-management
- JML
- access-provisioning
- RBAC
- IGA
subdomain: identity-access-management
version: '1.0'
author: mahipal
license: Apache-2.0
nist_ai_rmf:
- GOVERN-1.1
- GOVERN-1.7
- MAP-1.1
nist_csf:
- PR.AA-01
- PR.AA-02
- PR.AA-05
- PR.AA-06
---
# Building Identity Governance Lifecycle Process

## Overview

Cybersecurity skill for building identity governance lifecycle process. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "building identity governance lifecycle process"
- "Builds comprehensive identity governance and lifecycle management processes incl"


- Organization lacks automated joiner-mover-leaver (JML) processes for identity management
- Access provisioning is manual and takes days, creating productivity loss and security gaps
- Former employees retain access to systems after termination (orphaned accounts)
- Role explosion has created thousands of roles with unclear ownership and overlapping entitlements
- Compliance requirements mandate documented identity lifecycle processes (SOX, HIPAA, GDPR)
- No centralized visibility into who has access to what across the enterprise

**Do not use** for single-application user management; identity governance addresses cross-system lifecycle management requiring correlation of authoritative HR sources with downstream application provisioning.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Authoritative HR system (Workday, SAP SuccessFactors, BambooHR) as identity source of truth
- IGA platform (SailPoint, Saviynt, One Identity) or Microsoft Entra ID Governance
- Active Directory and/or Azure AD as primary directory services
- Application connectors for target systems requiring automated provisioning
- Defined organizational role structure and reporting hierarchy
- Stakeholder buy-in from HR, IT, security, and business unit managers

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

1. **Assess Requirements** — Evaluate current environment and define identity governance lifecycle process implementation requirements.
2. **Design Architecture** — Plan the identity governance lifecycle process architecture, including components, integrations, and data flows.
3. **Configure Components** — Set up and configure each identity governance lifecycle process component according to best practices.
4. **Test Integration** — Validate that all components work together. Run functional and security tests.
5. **Deploy to Production** — Roll out the implementation with monitoring and rollback capabilities.
6. **Validate and Document** — Verify the implementation meets requirements. Document configuration and runbooks.

## Tools

- **Configuration Management** — Infrastructure as code and automation
- **Monitoring Stack** — Observability and alerting
- **Documentation Platform** — Runbooks and architecture docs


## Process

1. **Design** — Define interface, identify patterns, plan implementation
1. **Implement** — Write code following existing conventions, add tests
1. **Verify** — Run tests, check integration, validate behavior

## Verification

- [ ] All identity governance lifecycle process procedures executed completely and documented
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