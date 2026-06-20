---
name: implementing-aws-macie-for-data-classification
description: Implement Amazon Macie to automatically discover, classify, and protect sensitive data in S3 buckets using machine
  learning and pattern matching for PII, financial data, and credentials detection.
domain: cybersecurity
subdomain: cloud-security
tags:
- aws
- macie
- data-classification
- s3
- pii
- sensitive-data
- dlp
- compliance
version: '1.0'
author: mahipal
license: Apache-2.0
atlas_techniques:
- AML.T0043
- AML.T0018
nist_ai_rmf:
- GOVERN-1.1
- GOVERN-4.2
- MAP-2.3
- MEASURE-2.7
- MEASURE-2.5
nist_csf:
- PR.IR-01
- ID.AM-08
- GV.SC-06
- DE.CM-01
---

# Implementing AWS Macie for Data Classification

## Overview

Amazon Macie is a fully managed data security and privacy service that uses machine learning and pattern matching to discover and protect sensitive data in Amazon S3. Macie automatically evaluates your S3 bucket inventory on a daily basis and identifies objects containing PII, financial information, credentials, and other sensitive data types. It provides two discovery approaches: automated sensitive data discovery for broad visibility and targeted discovery jobs for deep analysis.


## When to Use

- When deploying or configuring implementing aws macie for data classification capabilities in your environment
- When establishing security controls aligned to compliance requirements
- When building or improving security architecture for this domain
- When conducting security assessments that require this implementation

## Prerequisites

- AWS account with S3 buckets containing data to classify
- IAM permissions for Macie service configuration
- AWS Organizations setup (for multi-account deployment)
- S3 buckets in supported regions

## Enable Macie

This section covers enable macie for implementing aws macie for data classification.

- Ensure all prerequisites are met before proceeding
- Follow the documented workflow steps in sequence
- Record results and any anomalies encountered during this phase
### Via AWS CLI

```bash
# Enable Macie in the current account/region
aws macie2 enable-macie

# Verify Macie is enabled
aws macie2 get-macie-session

# Enable automated sensitive data discovery
aws macie2 update-automated-discovery-configuration \
  --status ENABLED
```

### Via Terraform

```hcl
resource "aws_macie2_account" "main" {}

resource "aws_macie2_classification_export_configuration" "main" {
  depends_on = [aws_macie2_account.main]

  s3_destination {
    bucket_name = aws_s3_bucket.macie_results.id
    key_prefix  = "macie-findings/"
    kms_key_arn = aws_kms_key.macie.arn
  }
}
```

## Configure Discovery Jobs

This section covers configure discovery jobs for implementing aws macie for data classification.

- Ensure all prerequisites are met before proceeding
- Follow the documented workflow steps in sequence
- Record results and any anomalies encountered during this phase
### Create a classification job for specific buckets

```bash
aws macie2 create-classification-job \
  --job-type ONE_TIME \
  --name "pii-scan-production-buckets" \
  --s3-job-definition '{
    "bucketDefinitions": [{
      "accountId": "123456789012",
      "buckets": [
        "production-data-bucket",
        "customer-records-bucket"
      ]
    }]
  }' \
  --managed-data-identifier-selector ALL
```

### Create a scheduled recurring job

```bash
aws macie2 create-classification-job \
  --job-type SCHEDULED \
  --name "weekly-sensitive-data-scan" \
  --schedule-frequency-details '{
    "weekly": {
      "dayOfWeek": "MONDAY"
    }
  }' \
  --s3-job-definition '{
    "bucketDefinitions": [{
      "accountId": "123456789012",
      "buckets": ["all-data-bucket"]
    }],
    "scoping": {
      "includes": {
        "and": [{
          "simpleScopeTerm": {
            "comparator": "STARTS_WITH",
            "key": "OBJECT_KEY",
            "values": ["uploads/", "documents/"]
          }
        }]
      }
    }
  }'
```

## Custom Data Identifiers

This section covers custom data identifiers for implementing aws macie for data classification.

- Ensure all prerequisites are met before proceeding
- Follow the documented workflow steps in sequence
- Record results and any anomalies encountered during this phase
### Create a custom identifier for internal IDs

```bash
aws macie2 create-custom-data-identifier \
  --name "internal-employee-id" \
  --description "Matches internal employee ID format EMP-XXXXXX" \
  --regex "EMP-[0-9]{6}" \
  --severity-levels '[
    {"occurrencesThreshold": 1, "severity": "LOW"},
    {"occurrencesThreshold": 10, "severity": "MEDIUM"},
    {"occurrencesThreshold": 50, "severity": "HIGH"}
  ]'
```

### Create identifier for project codes

```bash
aws macie2 create-custom-data-identifier \
  --name "project-code-identifier" \
  --description "Matches project codes in format PRJ-XXXX-XX" \
  --regex "PRJ-[A-Z]{4}-[0-9]{2}" \
  --keywords '["project", "code", "initiative"]' \
  --maximum-match-distance 50
```

## Allow Lists

This section covers allow lists for implementing aws macie for data classification.

- Ensure all prerequisites are met before proceeding
- Follow the documented workflow steps in sequence
- Record results and any anomalies encountered during this phase
### Create an allow list to suppress false positives

```bash
aws macie2 create-allow-list \
  --name "test-data-exclusions" \
  --description "Exclude known test data patterns" \
  --criteria '{
    "regex": "TEST-[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}"
  }'
```

## Managed Data Identifiers

Macie provides 300+ managed data identifiers covering:

| Category | Examples |
|----------|---------|
| **PII** | SSN, passport numbers, driver's license, date of birth, names, addresses |
| **Financial** | Credit card numbers, bank account numbers, SWIFT codes |
| **Credentials** | AWS secret keys, API keys, SSH private keys, OAuth tokens |
| **Health** | HIPAA identifiers, health insurance claim numbers |
| **Legal** | Tax identification numbers, national ID numbers |

## Findings Management

This section covers findings management for implementing aws macie for data classification.

- Ensure all prerequisites are met before proceeding
- Follow the documented workflow steps in sequence
- Record results and any anomalies encountered during this phase
### List findings

```bash
# Get sensitive data findings
aws macie2 list-findings \
  --finding-criteria '{
    "criterion": {
      "severity.description": {
        "eq": ["High"]
      },
      "category": {
        "eq": ["CLASSIFICATION"]
      }
    }
  }' \
  --sort-criteria '{"attributeName": "updatedAt", "orderBy": "DESC"}' \
  --max-results 25
```

### Get finding details

```bash
aws macie2 get-findings \
  --finding-ids '["finding-id-1", "finding-id-2"]'
```

### Export findings to Security Hub

```bash
# Macie automatically publishes findings to Security Hub
# Verify integration:
aws macie2 get-macie-session --query 'findingPublishingFrequency'
```

## EventBridge Integration for Automated Response

```json
{
  "source": ["aws.macie"],
  "detail-type": ["Macie Finding"],
  "detail": {
    "severity": {
      "description": ["High", "Critical"]
    }
  }
}
```

### Lambda function for automated remediation

```python
import boto3
import json

s3 = boto3.client('s3')
sns = boto3.client('sns')

def lambda_handler(event, context):
    finding = event['detail']
    severity = finding['severity']['description']
    bucket = finding['resourcesAffected']['s3Bucket']['name']
    key = finding['resourcesAffected']['s3Object']['key']
    sensitive_types = [d['type'] for d in finding.get('classificationDetails', {}).get('result', {}).get('sensitiveData', [])]

    if severity in ['High', 'Critical']:
        # Tag the object for review
        s3.put_object_tagging(
            Bucket=bucket,
            Key=key,
            Tagging={
                'TagSet': [
                    {'Key': 'macie-finding', 'Value': severity},
                    {'Key': 'sensitive-data', 'Value': ','.join(sensitive_types)},
                    {'Key': 'requires-review', 'Value': 'true'}
                ]
            }
        )

        # Notify security team
        sns.publish(
            TopicArn='arn:aws:sns:us-east-1:123456789012:security-alerts',
            Subject=f'Macie {severity} Finding: {bucket}/{key}',
            Message=json.dumps({
                'bucket': bucket,
                'key': key,
                'severity': severity,
                'sensitive_data_types': sensitive_types,
                'finding_id': finding['id']
            }, indent=2)
        )

    return {'statusCode': 200}
```

## Multi-Account Deployment

This section covers multi-account deployment for implementing aws macie for data classification.

- Ensure all prerequisites are met before proceeding
- Follow the documented workflow steps in sequence
- Record results and any anomalies encountered during this phase
### Designate Macie administrator account

```bash
# From the management account
aws macie2 enable-organization-admin-account \
  --admin-account-id 111111111111
```

### Add member accounts

```bash
# From the administrator account
aws macie2 create-member \
  --account '{"accountId": "222222222222", "email": "security@example.com"}'
```

## Monitoring Macie Operations

This section covers monitoring macie operations for implementing aws macie for data classification.

- Ensure all prerequisites are met before proceeding
- Follow the documented workflow steps in sequence
- Record results and any anomalies encountered during this phase
### Usage statistics

```bash
aws macie2 get-usage-statistics \
  --filter-by '[{"comparator": "GT", "key": "accountId", "values": []}]' \
  --sort-by '{"key": "accountId", "orderBy": "ASC"}'
```

### Classification job status

```bash
aws macie2 list-classification-jobs \
  --filter-criteria '{"includes": [{"comparator": "EQ", "key": "jobStatus", "values": ["RUNNING"]}]}'
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

## References

- AWS Macie Documentation: https://docs.aws.amazon.com/macie/
- AWS Macie Pricing
- Supported File Types for Macie Analysis
- GDPR and CCPA Compliance with Macie

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
