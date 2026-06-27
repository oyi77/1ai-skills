---
name: detecting-s3-data-exfiltration-attempts
description: 'Detecting data exfiltration attempts from AWS S3 buckets by analyzing CloudTrail S3 data events, VPC Flow Logs,
  GuardDuty findings, Amazon Macie alerts, and S3 access patterns to identify unauthorized bulk downloads and cross-account
  data transfers.

  '
domain: cybersecurity
tags:
- cloud-security
- aws
- s3
- data-exfiltration
- guardduty
- macie
- threat-detection
subdomain: cloud-security
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.IR-01
- ID.AM-08
- GV.SC-06
- DE.CM-01
---
# Detecting S3 Data Exfiltration Attempts

## When to Use

- When GuardDuty detects anomalous S3 access patterns such as bulk downloads from unusual IPs
- When investigating suspected data breach involving S3-stored sensitive data
- When building detection rules for S3 data loss prevention monitoring
- When responding to Macie alerts about sensitive data being accessed or moved
- When compliance requires monitoring and logging of all access to classified data stores

**Do not use** for preventing data exfiltration (use S3 bucket policies, VPC endpoints, and SCPs), for data classification (use Amazon Macie discovery jobs), or for network-level exfiltration detection (use VPC Flow Logs with network analysis tools).

## Prerequisites

- CloudTrail configured with S3 data event logging (`GetObject`, `PutObject`, `CopyObject`)
- GuardDuty enabled with S3 Protection feature activated
- Amazon Macie enabled for sensitive data discovery in target buckets
- CloudWatch Logs or Athena for querying CloudTrail logs at scale
- VPC endpoint policies configured for S3 access monitoring

## Workflow

1. **Define Detection Scope** — Identify the specific s3 data exfiltration attempts techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for s3 data exfiltration attempts.
3. **Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting s3 data exfiltration attempts indicators.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All s3 data exfiltration attempts procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
