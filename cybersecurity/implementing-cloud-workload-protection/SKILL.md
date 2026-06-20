---
name: implementing-cloud-workload-protection
description: 'Implements cloud workload protection using boto3 and google-cloud APIs for runtime security monitoring, process
  anomaly detection, and file integrity checking on EC2/GCE instances. Scans for cryptomining, reverse shells, and unauthorized
  binaries. Use when building runtime security controls for cloud compute workloads.

  '
domain: cybersecurity
tags:
- implementing
- cloud
- workload
- protection
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

# Implementing Cloud Workload Protection


## When to Use

- When deploying or configuring implementing cloud workload protection capabilities in your environment
- When establishing security controls aligned to compliance requirements
- When building or improving security architecture for this domain
- When conducting security assessments that require this implementation

## Prerequisites

- Familiarity with cloud security concepts and tools
- Access to a test or lab environment for safe execution
- Python 3.8+ with required dependencies installed
- Appropriate authorization for any testing activities

## Instructions

Monitor cloud workloads for runtime threats by checking process lists, network
connections, file integrity, and resource utilization anomalies.

```python
import boto3

ssm = boto3.client("ssm")
# Run command on EC2 instances to check for suspicious processes
response = ssm.send_command(
    InstanceIds=["i-1234567890abcdef0"],
    DocumentName="AWS-RunShellScript",
    Parameters={"commands": ["ps aux | grep -E 'xmrig|minerd|cryptonight'"]},
)
```

Key protection areas:
1. Process monitoring for cryptominers and reverse shells
2. File integrity monitoring on critical system files
3. Network connection auditing for C2 callbacks
4. Resource utilization anomaly detection (CPU spikes)
5. Unauthorized binary detection via hash comparison

## Examples

```python
# Check for unauthorized outbound connections
ssm.send_command(
    InstanceIds=instances,
    DocumentName="AWS-RunShellScript",
    Parameters={"commands": ["ss -tlnp | grep ESTABLISHED"]},
)
```
## When NOT to Use

- You need to test the implementation (use performing-* skills)
- Task is about configuring existing tools (use configuring-* skills)
- You need to analyze security events (use analyzing-* skills)
- Task is about building detection rules (use building-* skills)
- You don't have access to the target environment
- Task requires vendor-specific expertise (consult vendor docs)


## Red Flags

- Performing actions without explicit written authorization from the asset owner
- Testing against production systems without a defined scope and rules of engagement
- Modifying cloud IAM policies or security groups without approval
- Exposing cloud credentials or secrets in logs or reports
- Running scans that generate excessive API calls and trigger billing alerts
## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- Cloud resource changes reverted or documented as intentional
- IAM policies reviewed for least-privilege compliance after testing
- No residual test resources left running (cost and security check)

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
