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

## When to Use

- Deploying passive network security monitoring at key network choke points for continuous visibility
- Generating structured connection, DNS, HTTP, SSL, and file transfer logs for SIEM ingestion and threat hunting
- Writing custom Zeek scripts to detect organization-specific threats, policy violations, or beaconing behavior
- Performing retrospective analysis on network metadata to investigate security incidents
- Complementing IDS solutions with protocol-level metadata analysis that signature-based tools may miss

**Do not use** as a replacement for inline IDS/IPS that can actively block traffic, for monitoring encrypted payloads without TLS inspection, or on endpoints where host-based agents are more appropriate.

## Prerequisites

- Zeek 6.0+ installed from source or package manager (`zeek --version`)
- Network interface configured on a span port, network tap, or virtual switch mirror for passive capture
- Sufficient disk storage for log files (estimate 1-5 GB/day per 100 Mbps of monitored traffic)
- Familiarity with Zeek's scripting language for writing custom detections
- Log aggregation system (Splunk, Elastic, Graylog) for centralized analysis

## Workflow

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
