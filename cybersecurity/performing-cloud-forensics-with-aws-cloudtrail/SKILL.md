---
name: performing-cloud-forensics-with-aws-cloudtrail
description: Perform forensic investigation of AWS environments using CloudTrail logs to reconstruct attacker activity, identify
  compromised credentials, and analyze API call patterns.
domain: cybersecurity
tags:
- cloud-security
- aws
- cloudtrail
- forensics
- incident-response
- dfir
- boto3
- s3
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

# Performing Cloud Forensics with AWS CloudTrail

## When to Use

- When investigating suspected AWS account compromise
- After detecting unauthorized API calls or credential exposure
- During incident response involving cloud infrastructure
- When analyzing S3 data exfiltration or IAM privilege escalation
- For post-incident forensic timeline reconstruction

## Prerequisites

- AWS account with CloudTrail enabled (management and data events)
- IAM permissions for cloudtrail:LookupEvents, s3:GetObject, athena:StartQueryExecution
- boto3 Python SDK installed
- CloudTrail logs delivered to S3 with optional Athena table configured
- AWS CLI configured with appropriate credentials

## Workflow

1. **Scope Investigation**: Identify timeframe, affected accounts, and compromised credentials.
2. **Query CloudTrail**: Use boto3 lookup_events or Athena to retrieve relevant API events.
3. **Filter by Indicators**: Search for suspicious user agents, source IPs, and event names.
4. **Reconstruct Timeline**: Build chronological sequence of attacker actions from API calls.
5. **Analyze Access Patterns**: Identify data access, IAM changes, and resource modifications.
6. **Identify Persistence**: Check for new IAM users, access keys, roles, or Lambda functions.
7. **Generate Report**: Produce forensic timeline with findings and remediation steps.

## Key Concepts

| Concept | Description |
|---------|-------------|
| LookupEvents | CloudTrail API to query management events (last 90 days) |
| Athena Queries | SQL queries against CloudTrail logs in S3 for historical analysis |
| User Agent Analysis | Identify tool signatures (AWS CLI, SDK, console, custom) |
| AccessKeyId | Track activity by specific IAM access key |
| EventName | AWS API action name (e.g., GetObject, CreateUser, AssumeRole) |
| sourceIPAddress | Origin IP of API call for geolocation analysis |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| boto3 CloudTrail client | Programmatic CloudTrail event lookup |
| AWS Athena | SQL-based analysis of CloudTrail S3 logs |
| AWS CLI | Command-line CloudTrail queries |
| jq | JSON processing for CloudTrail event parsing |
| CloudTrail Lake | Advanced event data store with SQL query support |

## When NOT to Use

- You don't have explicit written authorization to test
- Task is about defense/detection, not offense (use detection skills)
- You need to implement security controls (use implementing-* skills)
- Task requires compliance auditing (use auditing-* skills)
- You're investigating an incident (use incident response skills)
- Target is out of scope for your engagement
- Task is about vulnerability scanning only (use scanning tools)


## Red Flags

- Performing actions without explicit written authorization from the asset owner
- Testing against production systems without a defined scope and rules of engagement
- Failing to use write-blockers when acquiring forensic evidence
- Not verifying hash integrity before and after imaging
- Modifying original evidence during analysis

## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- Hash values computed and verified match between source and image
- Chain of custody log complete with timestamps and examiner names
- Analysis tools and versions documented for reproducibility

## Output Format

```
Forensic Report: AWS-IR-[DATE]-[SEQ]
Account: [AWS Account ID]
Timeframe: [Start] to [End]
Compromised Credentials: [Access Key IDs]
Suspicious Events: [Count]
Source IPs: [List of attacker IPs]
Actions Taken: [API calls by attacker]
Data Accessed: [S3 objects, secrets, etc.]
Persistence Mechanisms: [New users, keys, roles]
```

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
