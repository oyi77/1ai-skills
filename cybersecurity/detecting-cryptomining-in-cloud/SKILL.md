---
name: detecting-cryptomining-in-cloud
description: 'This skill teaches security teams how to detect and respond to unauthorized cryptocurrency mining operations
  in cloud environments. It covers identifying cryptomining indicators through compute usage anomalies, network traffic patterns
  to mining pools, GuardDuty CryptoCurrency findings, and runtime process monitoring on EC2, ECS, EKS, and Azure Automation
  workloads.

  '
domain: cybersecurity
tags:
- cryptomining-detection
- cloud-abuse
- resource-hijacking
- guardduty-crypto
- cost-anomaly
subdomain: cloud-security
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- PR.IR-01
- ID.AM-08
- GV.SC-06
- DE.CM-01
---
# Detecting Cryptomining In Cloud

## When to Use

- When cloud billing alerts indicate unexpected compute cost spikes
- When GuardDuty generates CryptoCurrency or Impact finding types
- When investigating compromised IAM credentials that may be used to launch mining instances
- When monitoring container workloads for unauthorized process execution
- When establishing proactive detection controls against resource hijacking attacks

**Do not use** for legitimate cryptocurrency mining operations, for non-cloud mining detection on physical hardware, or for general malware analysis unrelated to mining activity.

## Prerequisites

- Amazon GuardDuty enabled with Runtime Monitoring for EC2, ECS, and EKS
- CloudWatch or Azure Monitor configured for compute utilization alerting
- VPC Flow Logs enabled for network traffic analysis to mining pool IPs
- AWS Cost Anomaly Detection or Azure Cost Management alerts configured

## Workflow

1. **Define Detection Scope** — Identify the specific cryptomining in cloud techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for cryptomining in cloud.
3. **Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting cryptomining in cloud indicators.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All cryptomining in cloud procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
