---
name: detecting-compromised-cloud-credentials
description: 'Detecting compromised cloud credentials across AWS, Azure, and GCP by analyzing anomalous API activity, impossible
  travel patterns, unauthorized resource provisioning, and credential abuse indicators using GuardDuty, Defender for Identity,
  and SCC Event Threat Detection.

  '
domain: cybersecurity
tags:
- cloud-security
- credential-compromise
- threat-detection
- guardduty
- incident-response
- anomaly-detection
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
# Detecting Compromised Cloud Credentials

## When to Use

- When investigating alerts about unusual cloud API activity from unfamiliar locations
- When building detection rules for credential theft and abuse across cloud environments
- When responding to notifications from cloud providers about exposed credentials
- When monitoring for credential stuffing or brute force attacks against cloud identities
- When assessing the scope of a credential compromise after initial detection

**Do not use** for preventing credential compromise (use MFA, credential rotation, and secrets management), for detecting application-level credential theft (use application security monitoring), or for endpoint credential harvesting detection (use EDR tools).

## Prerequisites

- AWS GuardDuty enabled across all accounts and regions
- Azure Defender for Identity and Entra ID Protection configured
- GCP Security Command Center with Event Threat Detection enabled
- CloudTrail, Azure Activity Log, and GCP Audit Log centralized for analysis
- SIEM integration for cross-cloud correlation of credential abuse indicators
- Threat intelligence feeds for known malicious IP ranges

## Workflow

1. **Define Detection Scope** — Identify the specific compromised cloud credentials techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for compromised cloud credentials.
3. **Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting compromised cloud credentials indicators.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis

## Verification

- [ ] All compromised cloud credentials procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
