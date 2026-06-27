---
name: analyzing-ransomware-payment-wallets
description: 'Traces ransomware cryptocurrency payment flows using blockchain analysis tools such as Chainalysis Reactor,
  WalletExplorer, and blockchain.com APIs. Identifies wallet clusters, tracks fund movement through mixers and exchanges,
  and supports law enforcement attribution. Activates for requests involving ransomware payment tracing, bitcoin wallet analysis,
  cryptocurrency forensics, or blockchain intelligence gathering.

  '
domain: cybersecurity
tags:
- ransomware
- blockchain
- cryptocurrency
- forensics
- threat-intelligence
- bitcoin
subdomain: ransomware-defense
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- PR.DS-11
- RS.MA-01
- RC.RP-01
- PR.IR-01
---
# Analyzing Ransomware Payment Wallets

## Overview

Cybersecurity skill for analyzing ransomware payment wallets. Follows industry best practices and security standards.

## When to Use

- An organization has been hit by ransomware and the ransom note contains a Bitcoin or cryptocurrency wallet address that needs investigation
- Law enforcement or incident responders need to trace where ransom payments flowed after the victim paid
- Threat intelligence analysts are attributing ransomware campaigns by clustering payment infrastructure across incidents
- Investigators need to determine if a ransomware group is reusing wallet infrastructure across multiple victims
- Compliance or legal teams need evidence of fund flows for prosecution, sanctions enforcement, or insurance claims

**Do not use** this skill for live payment interception or to interact directly with ransomware operators. All analysis should be passive and read-only against public blockchain data.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Python 3.8+ with `requests`, `json`, and `hashlib` libraries
- Access to blockchain explorer APIs (blockchain.com, WalletExplorer.com, Blockstream.info)
- Familiarity with Bitcoin transaction model (UTXOs, inputs, outputs, change addresses)
- Understanding of common obfuscation techniques (mixers, tumblers, peel chains, cross-chain swaps)
- Optional: Chainalysis Reactor license for enterprise-grade cluster analysis
- Optional: OXT.me for advanced transaction graph visualization

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

1. **Scope the Analysis** — Define what ransomware payment wallets artifacts or data sources to examine and the investigation timeline.
2. **Preserve Evidence** — Create forensic copies of relevant data. Maintain chain of custody documentation.
3. **Extract Key Indicators** — Parse and extract relevant ransomware payment wallets data points from collected artifacts.
4. **Correlate Findings** — Cross-reference extracted data with other sources (threat intel, logs, timelines).
5. **Build Timeline** — Construct a chronological sequence of events related to ransomware payment wallets.
6. **Document Analysis** — Write findings report with evidence, conclusions, and recommendations.

## Tools

- **Forensic Toolkit** — Evidence collection and analysis
- **Timeline Tools** — Chronological event reconstruction
- **Log Analysis Platform** — Centralized log parsing and search

## Verification

- [ ] All ransomware payment wallets procedures executed completely and documented
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