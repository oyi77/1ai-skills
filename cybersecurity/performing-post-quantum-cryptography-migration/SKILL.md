---
name: performing-post-quantum-cryptography-migration
description: Assesses organizational readiness for post-quantum cryptography migration per NIST FIPS 203/204/205 standards.
  Performs cryptographic inventory scanning to identify quantum-vulnerable algorithms (RSA, ECDH, ECDSA), evaluates hybrid
  TLS configurations with X25519MLKEM768, and validates CRYSTALS-Kyber (ML-KEM) and CRYSTALS-Dilithium (ML-DSA) readiness.
  Implements crypto-agility assessment using oqs-provider for OpenSSL.
domain: cybersecurity
tags:
- post-quantum
- PQC
- CRYSTALS-Kyber
- ML-KEM
- ML-DSA
- FIPS-203
- FIPS-204
- hybrid-TLS
- crypto-agility
subdomain: cryptography
version: '1.0'
author: mukul975
license: Apache-2.0
nist_csf:
- PR.DS-01
- PR.DS-02
- PR.DS-10
---
# Performing Post Quantum Cryptography Migration

## Overview

Cybersecurity skill for performing post quantum cryptography migration. Follows industry best practices and security standards.

## When to Use

- When assessing organizational readiness for the NIST post-quantum cryptography transition
- When building a cryptographic inventory to identify quantum-vulnerable algorithms across infrastructure
- When evaluating hybrid TLS 1.3 configurations using X25519MLKEM768 key exchange
- When testing CRYSTALS-Kyber (ML-KEM) and CRYSTALS-Dilithium (ML-DSA) algorithm support
- When implementing crypto-agility to support both classical and post-quantum algorithms
- When preparing migration roadmaps aligned with NIST IR 8547 deprecation timelines
- When configuring oqs-provider with OpenSSL 3.x for post-quantum algorithm support


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Python 3.8+ with `cryptography`, `requests`, `pyOpenSSL` libraries
- OpenSSL 3.0+ (3.5+ recommended for native ML-KEM/ML-DSA support)
- oqs-provider for OpenSSL (for hybrid TLS testing with older OpenSSL)
- Network access to target servers for TLS assessment
- Administrative access for infrastructure scanning
- Familiarity with PKI, TLS, and cryptographic protocols

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

1. **Plan Operations** — Define objectives, scope, and success criteria for post quantum cryptography migration operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for post quantum cryptography migration.
3. **Execute Core Workflow** — Perform the post quantum cryptography migration operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All post quantum cryptography migration procedures executed completely and documented
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