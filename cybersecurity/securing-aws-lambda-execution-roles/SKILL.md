---
name: securing-aws-lambda-execution-roles
description: 'Securing AWS Lambda execution roles by implementing least-privilege IAM policies, applying permission boundaries,
  restricting resource-based policies, using IAM Access Analyzer to validate permissions, and enforcing role scoping through
  SCPs.

  '
domain: cybersecurity
tags:
- cloud-security
- aws
- lambda
- iam
- least-privilege
- execution-roles
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
# Securing Aws Lambda Execution Roles

## When to Use

- When deploying new Lambda functions and defining their IAM execution roles
- When remediating overly permissive Lambda roles discovered during security audits
- When implementing least-privilege access patterns for serverless architectures
- When building reusable IAM templates for Lambda functions across teams
- When Security Hub or Prowler reports Lambda functions with excessive permissions

**Do not use** for securing Lambda function invocation (use resource-based policies and API Gateway authorizers), for Lambda code security (use SAST tools), or for Lambda network security (use VPC configuration and security groups).

## Prerequisites

- IAM permissions for policy creation, role modification, and Access Analyzer operations
- AWS IAM Access Analyzer enabled in the account
- CloudTrail data events enabled for Lambda to capture actual API usage
- Existing Lambda functions to audit and scope permissions for
- Understanding of each function's required AWS service interactions

## Workflow

1. **Define Objectives** — Clarify the goals and scope for aws lambda execution roles.
2. **Gather Resources** — Collect tools, data, and access needed for aws lambda execution roles.
3. **Execute Process** — Carry out aws lambda execution roles operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All aws lambda execution roles procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
