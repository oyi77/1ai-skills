---
name: implementing-honeytokens-for-breach-detection
description: 'Deploys canary tokens and honeytokens (fake AWS credentials, DNS canaries, document beacons, database records)
  that trigger alerts when accessed by attackers. Uses the Canarytokens API and custom webhook integrations for breach detection.
  Use when building deception-based early warning systems for intrusion detection.

  '
domain: cybersecurity
tags:
- implementing
- honeytokens
- for
- breach
subdomain: security-operations
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- DE.CM-01
- RS.MA-01
- GV.OV-01
- DE.AE-02
---

# Implementing Honeytokens for Breach Detection


## When to Use

- When deploying or configuring implementing honeytokens for breach detection capabilities in your environment
- When establishing security controls aligned to compliance requirements
- When building or improving security architecture for this domain
- When conducting security assessments that require this implementation

## Prerequisites

- Familiarity with security operations concepts and tools
- Access to a test or lab environment for safe execution
- Python 3.8+ with required dependencies installed
- Appropriate authorization for any testing activities

## Instructions

Deploy honeytokens across critical systems to detect unauthorized access. Each token
type alerts via webhook when triggered by an attacker.

```python
import requests

# Create a DNS canary token via Canarytokens
resp = requests.post("https://canarytokens.org/generate", data={
    "type": "dns",
    "email": "soc@company.com",
    "memo": "Production DB server honeytoken",
})
token = resp.json()
print(f"DNS token: {token['hostname']}")
```

Token types to deploy:
1. AWS credential files (~/.aws/credentials) with canary keys
2. DNS tokens embedded in configuration files
3. Document beacons (Word/PDF) in sensitive file shares
4. Database honeytoken records in user tables
5. Web bugs in internal wiki/documentation pages

## Examples

```python
# Generate a fake AWS credentials file with canary token
aws_creds = f"[default]\naws_access_key_id = {canary_key_id}\naws_secret_access_key = {canary_secret}\n"
with open("/opt/backup/.aws/credentials", "w") as f:
    f.write(aws_creds)
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
