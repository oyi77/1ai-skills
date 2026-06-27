---
name: detecting-command-and-control-over-dns
description: Detects command-and-control (C2) communications tunneled through DNS protocol including DNS tunneling tools (Iodine,
  dnscat2, dns2tcp, Cobalt Strike DNS beacon), domain generation algorithms (DGA), encoded payload delivery via TXT/CNAME
  records, and DNS beaconing patterns. Covers Shannon entropy analysis of query subdomains, statistical anomaly detection,
  ML-based DGA classification, passive DNS correlation, and Zeek/Suricata signature development.
domain: cybersecurity
tags:
- dns
- c2
- tunneling
- dga
- network-forensics
- threat-detection
subdomain: network-security
version: 1.0.0
author: mukul975
license: Apache-2.0
nist_csf:
- PR.IR-01
- DE.CM-01
- ID.AM-03
- PR.DS-02
---
# Detecting Command And Control Over Dns

## Overview

Cybersecurity skill for detecting command and control over dns. Follows industry best practices and security standards.

## When to Use

- Investigating suspected DNS tunneling used for C2 communication or data exfiltration
- Analyzing DNS query logs for signs of encoded payloads in subdomain strings
- Classifying domains as DGA-generated vs. legitimate using statistical or ML methods
- Detecting DNS beaconing patterns (regular intervals, consistent query sizes)
- Hunting for Iodine, dnscat2, dns2tcp, Cobalt Strike DNS, or Sliver DNS traffic
- Monitoring TXT record abuse for command delivery or staged payload download
- Building DNS anomaly detection rules for SOC/SIEM deployment

**Do not use** for general DNS performance monitoring or DNS configuration auditing; use DNS health monitoring tools for those. For HTTP/HTTPS-based C2 detection, use network traffic analysis skills focused on web protocols.

**DISCLAIMER**: DNS tunneling tools referenced in this skill (Iodine, dnscat2, dns2tcp) are dual-use. They have legitimate uses (bypassing captive portals, security research) and malicious uses (C2 channels, exfiltration). Only deploy detection in networks you are authorized to monitor. Testing tunneling tools requires explicit authorization.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- DNS query logs from recursive resolver, Zeek/Bro, Suricata, or passive DNS tap
- Python 3.9+ with `numpy`, `scikit-learn`, `pandas`, `tldextract`, and `dnspython`
- Zeek (formerly Bro) with dns.log output or Suricata with DNS EVE JSON logging
- SIEM access (Splunk, Elastic, Microsoft Sentinel) for log correlation
- Passive DNS database access (CIRCL pDNS, Farsight DNSDB, or internal) for enrichment
- Wireshark/tshark for packet-level DNS inspection
- Known-good domain whitelist (Alexa/Tranco top 1M or Majestic Million)

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

1. **Define Detection Scope** — Identify the specific command and control over dns techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for command and control over dns.
3. **Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting command and control over dns indicators.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All command and control over dns procedures executed completely and documented
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