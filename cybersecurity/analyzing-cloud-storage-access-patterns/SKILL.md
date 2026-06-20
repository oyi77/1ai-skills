---
name: analyzing-cloud-storage-access-patterns
description: Detect abnormal access patterns in AWS S3, GCS, and Azure Blob Storage by analyzing CloudTrail Data Events, GCS
  audit logs, and Azure Storage Analytics. Identifies after-hours bulk downloads, access from new IP addresses, unusual API
  calls (GetObject spikes), and potential data exfiltration using statistical baselines and time-series anomaly detection.
domain: cybersecurity
tags:
- analyzing
- cloud
- storage
- access
subdomain: cloud-security
version: '1.0'
author: mahipal
license: Apache-2.0
atlas_techniques:
- AML.T0024
- AML.T0056
nist_ai_rmf:
- MEASURE-2.7
- MAP-5.1
- MANAGE-2.4
nist_csf:
- PR.IR-01
- ID.AM-08
- GV.SC-06
- DE.CM-01
---


# Analyzing Cloud Storage Access Patterns


## When to Use

- When investigating security incidents that require analyzing cloud storage access patterns
- When building detection rules or threat hunting queries for this domain
- When SOC analysts need structured procedures for this analysis type
- When validating security monitoring coverage for related attack techniques

## Prerequisites

- Familiarity with cloud security concepts and tools
- Access to a test or lab environment for safe execution
- Python 3.8+ with required dependencies installed
- Appropriate authorization for any testing activities

## Instructions

1. Install dependencies: `pip install boto3 requests`
2. Query CloudTrail for S3 Data Events using AWS CLI or boto3.
3. Build access baselines: hourly request volume, per-user object counts, source IP history.
4. Detect anomalies:
   - After-hours access (outside 8am-6pm local time)
   - Bulk downloads: >100 GetObject calls from single principal in 1 hour
   - New source IPs not seen in the prior 30 days
   - ListBucket enumeration spikes (reconnaissance indicator)
5. Generate prioritized findings report.

```bash
python scripts/agent.py --bucket my-sensitive-data --hours-back 24 --output s3_access_report.json
```

## Examples

```bash
# Basic usage example
# Replace with domain-specific commands from the workflow above
```
### CloudTrail S3 Data Event
```json
{"eventName": "GetObject", "requestParameters": {"bucketName": "sensitive-data", "key": "financials/q4.xlsx"},
 "sourceIPAddress": "203.0.113.50", "userIdentity": {"arn": "arn:aws:iam::123456789012:user/analyst"}}
```
## When NOT to Use

- You need to perform the attack, not analyze it (use performing-* skills)
- Task is about detection, not analysis (use detecting-* skills)
- You need to implement controls (use implementing-* skills)
- Task is about threat hunting, not post-incident analysis (use hunting-* skills)
- You don't have access to the artifacts/logs to analyze
- Task requires real-time monitoring (use SOC tools)


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
