---
name: detecting-serverless-function-injection
description: >  Detects and prevents code injection attacks targeting serverless functions (AWS Lambda, Azure Functions, Google
  Cloud Functions) through event source poisoning, malicious layer injection, runtime command execution, and IAM privilege
  escalation via function modification. The analyst combines static analysis of function code, CloudTrail event correlation,
  runtime behavior monitoring, and IAM policy auditing to identify injection vectors across the expanded serverless attack
  surface includi.
domain: cybersecurity
tags:
- serverless-security
- Lambda-injection
- event-source-poisoning
- OWASP-serverless
- IAM-escalation
- CloudTrail
subdomain: cloud-security
version: 1.0.0
author: mukul975
license: Apache-2.0
nist_csf:
- PR.IR-01
- ID.AM-08
- GV.SC-06
- DE.CM-01
---
# Detecting Serverless Function Injection

## Overview

Cybersecurity skill for detecting serverless function injection. Follows industry best practices and security standards.

## When to Use

**Trigger phrases:**
- "detecting serverless function injection"
- "Use when working with detecting serverless function injection"


- Auditing Lambda/Cloud Functions for code injection vulnerabilities where unsanitized event data flows into dangerous runtime functions (`eval`, `exec`, `child_process.exec`, `os.system`)
- Investigating incidents where an attacker modified function code or layers to establish persistence or exfiltrate data from the serverless environment
- Detecting privilege escalation paths where an adversary with `lambda:UpdateFunctionCode` and `iam:PassRole` can assume higher-privilege execution roles
- Analyzing event source poisoning attacks where malicious payloads are injected through S3 object uploads, SQS messages, DynamoDB stream records, or API Gateway requests that trigger function execution
- Building detection rules for SOC teams monitoring serverless workloads for unauthorized function modifications, layer additions, and suspicious invocation patterns

**Do not use** for load testing or denial-of-service simulation against serverless functions, for testing against production functions processing live customer data without explicit authorization, or for modifying IAM policies in shared accounts without change management approval.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- AWS account access with read permissions for Lambda, CloudTrail, IAM, CloudWatch Logs, and EventBridge
- AWS CLI v2 configured with appropriate credentials and region
- CloudTrail enabled with Data Events for Lambda (captures `Invoke` events) and Management Events (captures `UpdateFunctionCode`, `UpdateFunctionConfiguration`, `CreateFunction`)
- Python 3.9+ with `boto3`, `bandit` (Python SAST), and `semgrep` for static analysis
- Access to function source code or deployment packages for static analysis
- CloudWatch Logs Insights access for querying Lambda execution logs

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

1. **Define Detection Scope** — Identify the specific serverless function injection techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.
2. **Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for serverless function injection.
3. **Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting serverless function injection indicators.
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

- [ ] All serverless function injection procedures executed completely and documented
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