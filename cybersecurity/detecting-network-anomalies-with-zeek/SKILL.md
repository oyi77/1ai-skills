---
name: detecting-network-anomalies-with-zeek
description: 'Deploys and configures Zeek (formerly Bro) network security monitor to passively analyze network traffic, generate
  structured logs, detect anomalous behavior, and create custom detection scripts for threat hunting and incident response.

  '
domain: cybersecurity
tags:
- network-security
- zeek
- network-monitoring
- anomaly-detection
- threat-hunting
subdomain: network-security
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.IR-01
- DE.CM-01
- ID.AM-03
- PR.DS-02
---
# Detecting Network Anomalies With Zeek

## Overview

Cybersecurity skill for detecting network anomalies with zeek. Follows industry best practices and security standards.

## When to Use

- Deploying passive network security monitoring at key network choke points for continuous visibility
- Generating structured connection, DNS, HTTP, SSL, and file transfer logs for SIEM ingestion and threat hunting
- Writing custom Zeek scripts to detect organization-specific threats, policy violations, or beaconing behavior
- Performing retrospective analysis on network metadata to investigate security incidents
- Complementing IDS solutions with protocol-level metadata analysis that signature-based tools may miss

**Do not use** as a replacement for inline IDS/IPS that can actively block traffic, for monitoring encrypted payloads without TLS inspection, or on endpoints where host-based agents are more appropriate.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Zeek 6.0+ installed from source or package manager (`zeek --version`)
- Network interface configured on a span port, network tap, or virtual switch mirror for passive capture
- Sufficient disk storage for log files (estimate 1-5 GB/day per 100 Mbps of monitored traffic)
- Familiarity with Zeek's scripting language for writing custom detections
- Log aggregation system (Splunk, Elastic, Graylog) for centralized analysis

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

1. **Define Detection Scope** — Identify the specific network anomalies techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for network anomalies.
3. **Build Detection Queries** — Write zeek queries targeting network anomalies indicators. Use platform-specific query language for optimal performance.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **zeek** — Primary tool for this skill
- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All network anomalies procedures executed completely and documented
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