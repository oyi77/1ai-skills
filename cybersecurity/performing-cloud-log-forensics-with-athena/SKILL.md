---
name: performing-cloud-log-forensics-with-athena
description: 'Uses AWS Athena to query CloudTrail, VPC Flow Logs, S3 access logs, and ALB logs for forensic investigation.
  Covers CREATE TABLE DDL with partition projection, forensic SQL queries for detecting unauthorized access, data exfiltration,
  lateral movement, and privilege escalation. Use when investigating AWS security incidents or building cloud-native forensic
  workflows at scale.

  '
domain: cybersecurity
tags:
- cloud
- forensics
- athena
- aws
- cloudtrail
- vpc-flow-logs
- s3
- alb
subdomain: cloud-security
version: '1.0'
author: mukul975
license: Apache-2.0
nist_csf:
- PR.IR-01
- ID.AM-08
- GV.SC-06
- DE.CM-01
---
# Performing Cloud Log Forensics With Athena

## When to Use

- When investigating AWS security incidents that require querying massive volumes of cloud logs
- When performing forensic analysis across CloudTrail, VPC Flow Logs, S3 access logs, and ALB logs
- When building reusable Athena tables with partition projection for ongoing incident response
- When hunting for indicators of compromise across multiple AWS log sources simultaneously
- When creating evidence-grade SQL queries for compliance audits or legal proceedings

## Prerequisites

- AWS account with Athena, S3, and Glue permissions
- CloudTrail configured to deliver logs to an S3 bucket
- VPC Flow Logs enabled and publishing to S3
- S3 server access logging enabled on target buckets
- ALB access logging enabled and publishing to S3
- Python 3.8+ with boto3 installed
- Appropriate IAM permissions for Athena queries and S3 access

## Workflow

1. **Plan Operations** — Define objectives, scope, and success criteria for cloud log forensics operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for cloud log forensics.
3. **Execute Core Workflow** — Use athena to perform cloud log forensics operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **athena** — Primary tool for this skill
- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All cloud log forensics procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
