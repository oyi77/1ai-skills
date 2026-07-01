---
name: detecting-cloud-threats-with-guardduty
description: 'This skill teaches security teams how to deploy and operationalize Amazon GuardDuty for continuous threat detection
  across AWS accounts and workloads. It covers enabling protection plans for S3, EKS, EC2 runtime monitoring, and Lambda,
  interpreting finding severity levels, and building automated response workflows using EventBridge and Lambda.

  '
domain: cybersecurity
tags:
- amazon-guardduty
- threat-detection
- aws-security
- runtime-monitoring
- cloud-soc
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
# Detecting Cloud Threats With Guardduty

## Overview

Cybersecurity skill for detecting cloud threats with guardduty. Follows industry best practices and security standards.

## When to Use

**Trigger phrases:**
- "detecting cloud threats with guardduty"
- "Use when working with detecting cloud threats with guardduty"


- When establishing continuous threat detection for new or existing AWS accounts
- When investigating GuardDuty findings related to compromised instances, credential abuse, or data exfiltration
- When building automated incident response playbooks triggered by GuardDuty findings
- When extending threat coverage to container workloads running on EKS, ECS, or Fargate
- When enabling malware scanning for EBS volumes attached to suspicious EC2 instances

**Do not use** for Azure or GCP threat detection (see securing-azure-with-microsoft-defender or auditing-gcp-security-posture), for static code analysis, or for compliance posture monitoring (see implementing-aws-security-hub).


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- AWS account with GuardDuty administrative permissions (guardduty:*)
- AWS CloudTrail, VPC Flow Logs, and DNS query logs enabled (GuardDuty consumes these automatically)
- AWS Organizations configured if deploying GuardDuty across a multi-account estate
- EventBridge and Lambda configured for automated response workflows

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

1. **Define Detection Scope** — Identify the specific cloud threats techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for cloud threats.
3. **Build Detection Queries** — Write guardduty queries targeting cloud threats indicators. Use platform-specific query language for optimal performance.
4. **Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.
5. **Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.
6. **Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.

## Tools

- **guardduty** — Primary tool for this skill
- **SIEM Platform** — Central log aggregation and query execution
- **Sigma Rules** — Vendor-agnostic detection rule format
- **MITRE ATT&CK Navigator** — Technique mapping and coverage analysis


## Process

1. **Reconnaissance** — Gather target information, identify attack surface, enumerate services
1. **Analysis/Exploitation** — Execute the technique, analyze results, document findings
1. **Reporting** — Document IOCs, write findings, provide remediation recommendations

## Verification

- [ ] All cloud threats procedures executed completely and documented
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