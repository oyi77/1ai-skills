---
name: conducting-cloud-incident-response
description: 'Responds to security incidents in cloud environments (AWS, Azure, GCP) by performing identity-based containment,
  cloud-native log analysis, resource isolation, and forensic evidence acquisition adapted for ephemeral cloud infrastructure.
  Activates for requests involving cloud incident response, AWS security incident, Azure compromise, GCP breach, cloud forensics,
  or cloud identity compromise.

  '
domain: cybersecurity
tags:
- cloud-IR
- AWS-forensics
- Azure-incident-response
- GCP-security
- identity-containment
subdomain: incident-response
mitre_attack:
- T1078
- T1537
- T1580
- T1525
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- RS.MA-01
- RS.MA-02
- RS.AN-03
- RC.RP-01
---
# Conducting Cloud Incident Response

## When to Use

- Cloud security posture management (CSPM) alerts on unauthorized resource changes
- CloudTrail, Azure Activity Logs, or GCP Audit Logs show suspicious API calls
- Cloud access keys or service principal credentials are suspected compromised
- Unauthorized compute instances, storage buckets, or IAM changes are detected
- A cloud-hosted application is breached and attacker activity spans cloud services

**Do not use** for on-premises-only incidents with no cloud component; use standard enterprise IR procedures.

## Prerequisites

- Cloud-native logging enabled and centralized: AWS CloudTrail (all regions), Azure Activity/Sign-in Logs, GCP Cloud Audit Logs
- IR-specific cloud IAM roles pre-provisioned with read-only forensic access
- Isolated forensic account/subscription/project for evidence preservation
- Cloud incident response runbooks specific to each cloud provider
- Cloud-native security tools: AWS GuardDuty, Azure Defender for Cloud, GCP Security Command Center
- Network traffic logging: VPC Flow Logs (AWS/GCP), NSG Flow Logs (Azure)

## Workflow

1. **Scope the Analysis** — Define what cloud incident response artifacts or data sources to examine and the investigation timeline.
2. **Preserve Evidence** — Create forensic copies of relevant data. Maintain chain of custody documentation.
3. **Extract Key Indicators** — Parse and extract relevant cloud incident response data points from collected artifacts.
4. **Correlate Findings** — Cross-reference extracted data with other sources (threat intel, logs, timelines).
5. **Build Timeline** — Construct a chronological sequence of events related to cloud incident response.
6. **Document Analysis** — Write findings report with evidence, conclusions, and recommendations.

## Tools

- **Forensic Toolkit** — Evidence collection and analysis
- **Timeline Tools** — Chronological event reconstruction
- **Log Analysis Platform** — Centralized log parsing and search

## Verification

- [ ] All cloud incident response procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
