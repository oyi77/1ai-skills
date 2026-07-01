---
name: detecting-bluetooth-low-energy-attacks
description: Detects and analyzes Bluetooth Low Energy (BLE) security attacks including sniffing, replay attacks, GATT enumeration
  abuse, and Man-in-the-Middle interception. Uses Ubertooth One and nRF52840 sniffers for packet capture, the bleak Python
  library for GATT service enumeration, and crackle for BLE encryption cracking. Use when assessing IoT device BLE security,
  monitoring for BLE-based attacks on wireless infrastructure, or performing authorized BLE penetration testing.
domain: cybersecurity
tags:
- ble
- bluetooth
- ubertooth
- nrf-sniffer
- gatt
- wireless-security
- iot-security
- replay-attack
subdomain: wireless-security
author: mukul975
version: 1.0.0
license: Apache-2.0
nist_csf:
- PR.IR-01
- DE.CM-01
- ID.AM-03
---
# Detecting Bluetooth Low Energy Attacks

## Overview

Cybersecurity skill for detecting bluetooth low energy attacks. Follows industry best practices and security standards.

## When to Use

**Trigger phrases:**
- "detecting bluetooth low energy attacks"
- "Performing authorized BLE security assessments of IoT devices, medical devices,"
- "Monitoring a wireless environment for BLE-based replay attacks, spoofing, or una"
- "Analyzing BLE packet captures to detect Man-in-the-Middle attacks or pairing exp"


Use this skill when:
- Performing authorized BLE security assessments of IoT devices, medical devices, or smart locks
- Monitoring a wireless environment for BLE-based replay attacks, spoofing, or unauthorized enumeration
- Analyzing BLE packet captures to detect Man-in-the-Middle attacks or pairing exploitation
- Enumerating GATT services and characteristics to identify insecure read/write permissions on BLE peripherals
- Assessing BLE encryption strength and testing for crackable pairing exchanges
- Building BLE intrusion detection capabilities for wireless security monitoring

**Do not use** for intercepting BLE communications without explicit authorization. Do not deploy BLE scanning tools in environments where wireless monitoring is prohibited.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Ubertooth One hardware for passive BLE sniffing, or Nordic nRF52840 USB Dongle with nRF Sniffer firmware
- Python 3.10+ with pip
- bleak library: `pip install bleak` (cross-platform BLE GATT client)
- Wireshark with BLE dissector plugins for packet analysis
- crackle tool for BLE encryption analysis: built from source at github.com/mikeryan/crackle
- ubertooth-btle CLI tools: `apt install ubertooth` (Linux) or build from source
- Bluetooth 4.0+ adapter on the host system for bleak-based scanning
- Linux recommended for full Ubertooth/nRF sniffer support

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

1. **Define Detection Scope** — Identify the specific bluetooth low energy attacks techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for bluetooth low energy attacks.
3. **Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting bluetooth low energy attacks indicators.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis


## Process

1. **Reconnaissance** — Gather target information, identify attack surface, enumerate services
1. **Analysis/Exploitation** — Execute the technique, analyze results, document findings
1. **Reporting** — Document IOCs, write findings, provide remediation recommendations

## Verification

- [ ] All bluetooth low energy attacks procedures executed completely and documented
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