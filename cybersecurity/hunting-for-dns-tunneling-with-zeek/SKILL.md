---
name: hunting-for-dns-tunneling-with-zeek
description: Detect DNS tunneling and data exfiltration by analyzing Zeek dns.log for high-entropy subdomain queries, excessive
  query volume, long query lengths, and unusual DNS record types indicating covert channel communication.
domain: cybersecurity
tags:
- threat-hunting
- dns-tunneling
- zeek
- data-exfiltration
- covert-channel
- mitre-t1071-004
- network-monitoring
subdomain: threat-hunting
version: '1.0'
author: mahipal
license: Apache-2.0
d3fend_techniques:
- Application Protocol Command Analysis
- Network Isolation
- Network Traffic Analysis
- Client-server Payload Profiling
- DNS Traffic Analysis
nist_csf:
- DE.CM-01
- DE.AE-02
- DE.AE-07
- ID.RA-05
---
# Hunting For Dns Tunneling With Zeek

## When to Use

- When hunting for data exfiltration over DNS covert channels
- After threat intelligence indicates DNS-based C2 frameworks targeting your industry
- When dns.log shows unusually high query volumes to specific domains
- During investigation of suspected data theft where no HTTP/S exfiltration is found
- When monitoring for tools like iodine, dnscat2, DNSExfiltrator, or DNS-over-HTTPS tunneling

## Prerequisites

- Zeek deployed on network tap or SPAN port capturing DNS traffic
- Zeek dns.log with full query and response fields
- SIEM platform for dns.log analysis (Splunk, Elastic)
- RITA (Real Intelligence Threat Analytics) for automated DNS analysis
- Passive DNS data for historical domain resolution context

## Workflow

1. **Define Detection Scope** — Identify the specific  techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for .
3. **Build Detection Queries** — Write dns tunneling with zeek queries targeting  indicators. Use platform-specific query language for optimal performance.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **dns tunneling with zeek** — Primary tool for this skill
- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All  procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
