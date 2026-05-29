---
name: detecting-aws-cloudtrail-anomalies
description: Detect unusual API call patterns in AWS CloudTrail logs using boto3, statistical baselining, and behavioral analysis
  to identify credential compromise, privilege escalation, and unauthorized resource access.
domain: cybersecurity
subdomain: cloud-security
tags:
- cloud-security
- aws
- cloudtrail
- anomaly-detection
- threat-detection
- boto3
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.IR-01
- ID.AM-08
- GV.SC-06
- DE.CM-01
---
# Detecting AWS CloudTrail Anomalies

## Overview

AWS CloudTrail records API calls across AWS services. This skill covers querying CloudTrail events with boto3's `lookup_events` API, building statistical baselines of normal API activity, detecting anomalies such as unusual event sources, geographic anomalies, high-frequency API calls, and first-time API usage patterns that indicate compromised credentials or insider threats.


## When to Use

- When investigating security incidents that require detecting aws cloudtrail anomalies
- When building detection rules or threat hunting queries for this domain
- When SOC analysts need structured procedures for this analysis type
- When validating security monitoring coverage for related attack techniques

## Prerequisites

- Python 3.9+ with `boto3` library
- AWS credentials with CloudTrail read permissions (cloudtrail:LookupEvents)
- Understanding of AWS IAM and common API patterns
- CloudTrail enabled in target AWS account (management events at minimum)

## Steps

1. **Inventory cloud assets** — enumerate services, roles, and configurations in scope
2. **Assess configurations** — check against security best practices and CIS benchmarks
3. **Test access controls** — verify IAM policies, network ACLs, and security group rules
4. **Validate logging** — ensure audit trails are enabled and properly retained
5. **Document and remediate** — report findings with specific configuration changes needed
### Step 1: Query CloudTrail Events
Use boto3 CloudTrail client's lookup_events to retrieve recent API activity with pagination.

### Step 2: Build Activity Baseline
Aggregate events by user, source IP, event source, and event name to establish normal behavior patterns.

### Step 3: Detect Anomalies
Flag unusual patterns: new event sources per user, first-time API calls, geographic IP changes, high error rates, and sensitive API usage (IAM, KMS, S3 policy changes).

### Step 4: Generate Detection Report
Produce a JSON report with anomaly scores, top suspicious users, and recommended investigation actions.

## Expected Output

JSON report with event statistics, baseline deviations, anomalous users/IPs, sensitive API calls, and error rate analysis.
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
