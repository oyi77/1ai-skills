---
name: implementing-disk-encryption-with-bitlocker
description: 'Implements full disk encryption using Microsoft BitLocker on Windows endpoints to protect data at rest from
  unauthorized access in case of device loss or theft. Use when deploying encryption for compliance requirements, securing
  mobile workstations, or implementing data protection controls across the enterprise. Activates for requests involving BitLocker
  encryption, disk encryption, TPM configuration, or data-at-rest protection.

  '
domain: cybersecurity
tags:
- endpoint
- encryption
- BitLocker
- TPM
- data-protection
- windows-security
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
# Implementing Disk Encryption With Bitlocker

## Overview

Cybersecurity skill for implementing disk encryption with bitlocker. Follows industry best practices and security standards.

## When to Use

Use this skill when:
- Encrypting Windows endpoints to protect data at rest for compliance (PCI DSS, HIPAA, GDPR)
- Deploying BitLocker across enterprise fleet via Intune, SCCM, or GPO
- Configuring TPM-based encryption with PIN or USB startup key for enhanced security
- Managing BitLocker recovery keys in Active Directory or Azure AD

**Do not use** this skill for Linux disk encryption (use LUKS/dm-crypt) or macOS (use FileVault).


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Windows 10/11 Pro, Enterprise, or Education edition
- TPM 2.0 chip (recommended; TPM 1.2 supported with limitations)
- UEFI firmware with Secure Boot enabled (recommended)
- Separate system partition (200 MB minimum, created automatically by Windows installer)
- Active Directory or Azure AD for recovery key escrow

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

1. **Assess Requirements** — Evaluate current environment and define disk encryption implementation requirements.
2. **Design Architecture** — Plan the disk encryption architecture, including components, integrations, and data flows.
3. **Configure Components** — Set up bitlocker for disk encryption according to vendor best practices and security guidelines.
4. **Test Integration** — Validate that all components work together. Run functional and security tests.
5. **Deploy to Production** — Roll out the implementation with monitoring and rollback capabilities.
6. **Validate and Document** — Verify the implementation meets requirements. Document configuration and runbooks.

## Tools

- **bitlocker** — Primary tool for this skill
- **Configuration Management** — Infrastructure as code and automation
- **Monitoring Stack** — Observability and alerting
- **Documentation Platform** — Runbooks and architecture docs

## Verification

- [ ] All disk encryption procedures executed completely and documented
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