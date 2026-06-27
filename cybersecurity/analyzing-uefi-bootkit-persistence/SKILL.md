---
name: analyzing-uefi-bootkit-persistence
description: Analyzes UEFI bootkit persistence mechanisms including firmware implants in SPI flash, EFI System Partition (ESP)
  modifications, Secure Boot bypass techniques, and UEFI variable manipulation. Covers detection of known bootkit families
  (BlackLotus, LoJax, MosaicRegressor, MoonBounce, CosmicStrand), ESP partition forensic inspection, chipsec-based firmware
  integrity verification, and Secure Boot configuration auditing.
domain: cybersecurity
tags:
- UEFI
- bootkit
- firmware
- Secure-Boot
- chipsec
- ESP
- persistence
subdomain: firmware-security
version: 1.0.0
author: mukul975
license: Apache-2.0
d3fend_techniques:
- Platform Hardening
- Restore Object
- Platform Monitoring
- Firmware Verification
- Firmware Embedded Monitoring Code
nist_csf:
- ID.RA-01
- PR.PS-01
- PR.PS-02
---
# Analyzing Uefi Bootkit Persistence

## When to Use

- A compromised system re-establishes C2 communication after OS reinstallation or disk replacement
- Secure Boot has been tampered with, disabled, or shows unexpected Machine Owner Key (MOK) enrollment
- Firmware integrity verification fails against vendor-provided baselines
- Memory forensics reveals rootkit components loading during early boot phase
- Investigating advanced persistent threat (APT) campaigns known to deploy UEFI implants
- Auditing firmware security posture for enterprise endpoint hardening

**Do not use** for standard MBR-based bootkits on legacy BIOS systems without UEFI; use MBR/VBR bootkit analysis instead.

## Prerequisites

- chipsec framework for SPI flash dumping, UEFI variable inspection, and firmware security modules
- UEFITool / UEFIExtract for firmware volume parsing and DXE driver extraction
- Python 3.8+ with struct, hashlib, subprocess, and os modules
- Bootable Linux live USB for offline analysis (avoid running compromised OS)
- Volatility 3 for memory forensics of boot-phase artifacts
- YARA with UEFI malware rule sets for pattern-based detection
- Access to vendor firmware baselines for integrity comparison

## Workflow

1. **Scope the Analysis** — Define what uefi bootkit persistence artifacts or data sources to examine and the investigation timeline.
2. **Preserve Evidence** — Create forensic copies of relevant data. Maintain chain of custody documentation.
3. **Extract Key Indicators** — Parse and extract relevant uefi bootkit persistence data points from collected artifacts.
4. **Correlate Findings** — Cross-reference extracted data with other sources (threat intel, logs, timelines).
5. **Build Timeline** — Construct a chronological sequence of events related to uefi bootkit persistence.
6. **Document Analysis** — Write findings report with evidence, conclusions, and recommendations.

## Tools

- **Forensic Toolkit** — Evidence collection and analysis
- **Timeline Tools** — Chronological event reconstruction
- **Log Analysis Platform** — Centralized log parsing and search

## Verification

- [ ] All uefi bootkit persistence procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
