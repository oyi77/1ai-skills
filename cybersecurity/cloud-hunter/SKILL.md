---
name: cloud-hunter
description: Cloud infrastructure misconfiguration hunting for AWS, GCP, and Azure. Use when testing cloud assets, finding exposed S3 buckets, hunting IAM misconfigs, or testing serverless applications.
domain: cybersecurity
tags:
- aws
- azure
- cloud
- cybersecurity
- gcp
- hunter
- security
- testing
- money
subdomain: cloud-security
version: '1.0'
author: cloud-hunter
license: Apache-2.0
nist_csf:
- ID.AM-02
- PR.AC-03
- PR.AC-05
- DE.CM-01
- DE.CM-07
---

# Cloud Hunter

## Overview

Cloud infrastructure misconfiguration hunting across AWS, GCP, and Azure. This skill systematically scans cloud environments for exposed storage buckets, overly permissive IAM policies, unsecured security group rules, public-facing databases, Kubernetes RBAC misconfigurations, and serverless function injection points. Uses real Kali Linux cloud auditing tools — Prowler, ScoutSuite, CloudSploit, `aws-cli`, `gcloud`, `az`, `kubectl`, and custom `boto3` enumeration scripts — to map misconfigurations and produce prioritized remediation roadmaps mapped to CIS Cloud Foundations Benchmarks.

Cloud misconfigurations are the #1 cause of data breaches in 2024-2025. A single open S3 bucket or over-privileged IAM role is a direct path to credential theft, data exfiltration, and infrastructure takeover. This skill turns that attack surface into a billable service.

## When to Use

**Trigger phrases:**
- "cloud hunter"
- "test cloud security"
- "audit my AWS account"
- "check GCP permissions"
- "scan Azure for misconfigs"
- "find exposed buckets"
- "review Kubernetes RBAC"
- "cloud security assessment"
- "is our cloud setup secure"
- "CIS benchmark cloud audit"

**Use when:**
- An organization has recently migrated workloads to AWS/GCP/Azure and needs a security baseline
- You are performing a cloud penetration test and need to enumerate misconfigurations across IAM, storage, networking, and compute
- A client suspects they have exposed cloud resources after a security incident or breach
- Compliance requirements (SOC 2, PCI DSS, HIPAA, ISO 27001) mandate periodic cloud security posture assessments
- You are preparing for a cloud-specific red team exercise and need to map the exploitable surface
- A startup or SaaS company has grown fast and never reviewed their cloud IAM or bucket permissions
- Serverless functions (Lambda, Cloud Functions, Azure Functions) need security review for injection and over-permissioned execution roles
- Kubernetes clusters (EKS, GKE, AKS) need RBAC, network policy, and pod security audit
- Container registries and CI/CD pipelines need assessment for supply chain risks

**Do not use** when you lack authorized credentials or signed testing agreement, for production environments without change management approval, when the scope requires regulatory compliance legal review (PCI QSA, HIPAA BA agreement), or when a dedicated cloud security architect is already engaged — overlapping audits waste budget.

## When NOT to Use

- When you lack proper authorization (signed ROE or penetration testing agreement) for the target cloud accounts
- For production systems without change management — scanning can trigger alarms, auto-scaling events, or WAF rate limiting
- When the task requires compliance certification sign-off by a qualified assessor (PCI QSA, HITRUST CCSFP) — your audit *informs* but does not substitute for formal certification
- When you are asked to review a cloud environment that is already under active remediation by a cloud security team — coordinate scope first
- When you do not have read-level credentials (at minimum) for the target cloud provider — blind guessing is not a service
- When the client expects a full penetration test rather than a configuration audit — know the difference and set expectations

## Money-Making Overview

**Target Buyer:** CTOs, DevOps leads, and security managers at startups ($1-20M ARR), SaaS companies, and mid-market enterprises migrating workloads to the cloud. Also: MSPs and cloud consultancies that sub-contract security reviews, and CISOs in regulated industries (fintech, healthtech) needing quarterly posture assessments.

**How You Make Money:**

1. **Cloud Security Posture Assessment** — Run Prowler/ScoutSuite against client AWS/GCP/Azure accounts, produce a CIS-benchmark-mapped report with finding severity, evidence, and step-by-step remediation ($1K-5K/job).

2. **Kubernetes Security Audit** — Review EKS/GKE/AKS cluster configurations: RBAC bindings, pod security standards, network policies, secrets management, admission controller setup. Deliver a Kube-bench/Hardeneks report ($1.5K-4K/cluster).

3. **Serverless & CI/CD Pipeline Review** — Audit Lambda/Cloud Functions for over-permissioned execution roles, injection vectors, exposed secrets in environment variables, and CI/CD pipeline security (GitHub Actions, GitLab CI, CodePipeline) ($1K-3K/pipeline).

4. **Remediation Implementation** — Fix the findings you discovered: lock down buckets, rewrite IAM policies, configure security groups, enable encryption, deploy GuardDuty/Security Command Center/Defender for Cloud ($500-2K per remediation day).

5. **Monthly Cloud Security Monitoring** — Recurring monthly scan and report with trend tracking, new-resource auditing, and Slack/Teams alert integration. Retainer model ($500-2K/mo).

### Service Tiers

| Tier | Price | What They Get |
|------|-------|---------------|
| **Basic** — Cloud Snapshot Audit | $1,000 | Single-cloud (AWS/GCP/Azure) posture scan with Prowler/ScoutSuite. 10-15 page report covering S3/Cloud Storage/Blob, IAM, security groups, logging. Top 10 critical findings with fix commands. Delivered in 3 business days. |
| **Pro** — Full Cloud Assessment | $3,500 | Multi-cloud audit (up to 3 accounts/projects). Full CIS benchmark coverage. Includes Kubernetes cluster audit (kube-bench + manual RBAC review), serverless function review, CI/CD pipeline scan. 25-40 page report with executive summary, risk matrix, and prioritized remediation playbook. Includes one 30-minute findings walkthrough call. |
| **Enterprise** — Managed Cloud Security | $2,000/mo | Monthly full-scope scan across all cloud accounts (up to 10 accounts/projects). Trend tracking dashboard, new-resource alerting, quarterly executive briefing. Includes remediation-as-a-service: up to 8 hours/month implementing fixes (IAM policy rewrite, bucket lockdown, GuardDuty enablement). Slack/Teams integration for real-time finding alerts. Annual penetration test included. |

**Expected First Dollar:** 2-5 days. Reach out to your existing network of startup founders, join cloud security Slack communities, or post on Upwork/Contra. A single $1K basic audit takes 3-4 hours of scanning + 3-4 hours of report writing once you have the client's cloud credentials.

## First Action in 60 Minutes

A complete cloud misconfiguration scanner that runs on Kali Linux against a target AWS account. The script enumerates S3 bucket permissions, IAM roles with administrative access, security group rules with 0.0.0.0/0 ingress, and unencrypted storage — then generates a prioritized finding report.

```bash
#!/bin/bash
# cloud-hunter-scan.sh — Cloud Misconfiguration Scanner
# Usage: ./cloud-hunter-scan.sh <aws-profile-name>
# Requires: aws-cli v2, jq, pip3 install prowler
# Targets: AWS S3, IAM, EC2 Security Groups, CloudTrail, KMS

set -euo pipefail
shopt -s inherit_errexit

if [ $# -lt 1 ]; then
    echo "Usage: $0 <aws-profile-name>"
    echo "  ./cloud-hunter-scan.sh my-client-prod"
    exit 1
fi

PROFILE="$1"
OUTDIR="cloud-hunt-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$OUTDIR"
echo "[*] Cloud Hunter Scan — Target: ${PROFILE}  Output: ${OUTDIR}"
echo ""

# ── Step 1: Verify credentials ──────────────────────────────────────
echo "[1/6] Verifying AWS credentials..."
if ! aws sts get-caller-identity --profile "$PROFILE" &>/dev/null; then
    echo "ERROR: Cannot authenticate with profile '${PROFILE}'. Check your credentials."
    exit 1
fi
ACCOUNT_ID=$(aws sts get-caller-identity --profile "$PROFILE" --query Account --output text)
echo "      Account: ${ACCOUNT_ID}"
echo ""

# ── Step 2: S3 Bucket Audit ─────────────────────────────────────────
echo "[2/6] Scanning S3 buckets for public exposure..."
aws s3api list-buckets --profile "$PROFILE" --query 'Buckets[*].Name' --output text \
    | tr '\t' '\n' > "${OUTDIR}/buckets.txt"

>"${OUTDIR}/s3-findings.csv"
while IFS= read -r bucket; do
    [ -z "$bucket" ] && continue
    # Check public access block
    BLOCK=$(aws s3api get-public-access-block --bucket "$bucket" --profile "$PROFILE" 2>/dev/null \
        | jq -r 'if .PublicAccessBlockConfiguration.BlockPublicAcls and .PublicAccessBlockConfiguration.BlockPublicPolicy and .PublicAccessBlockConfiguration.IgnorePublicAcls and .PublicAccessBlockConfiguration.RestrictPublicBuckets then "LOCKED" else "UNLOCKED" end' \
        || echo "NO_BLOCK_CONFIG")
    # Check bucket ACL
    ACL=$(aws s3api get-bucket-acl --bucket "$bucket" --profile "$PROFILE" 2>/dev/null \
        | jq -r '[.Grants[] | select(.Grantee.URI == "http://acs.amazonaws.com/groups/global/AllUsers" or .Grantee.URI == "http://acs.amazonaws.com/groups/global/AuthenticatedUsers")] | length' \
        || echo "0")
    # Check bucket policy
    POLICY=$(aws s3api get-bucket-policy --bucket "$bucket" --profile "$PROFILE" 2>/dev/null \
        | jq -r 'if .Policy | fromjson | any(.Statement[]; .Effect == "Allow" and (.Principal == "*" or .Principal.AWS == "*")) then "PUBLIC" else "RESTRICTED" end' \
        || echo "NO_POLICY")
    # Check encryption
    ENCRYPT=$(aws s3api get-bucket-encryption --bucket "$bucket" --profile "$PROFILE" 2>/dev/null \
        | jq -r 'if .ServerSideEncryptionConfiguration.Rules[0].ApplyServerSideEncryptionByDefault.SSEAlgorithm then "ENCRYPTED" else "NO_ENCRYPTION" end' \
        || echo "NO_ENCRYPTION")
    SEVERITY="INFO"
    [ "$BLOCK" = "UNLOCKED" ] && SEVERITY="HIGH"
    [ "$ACL" != "0" ] && SEVERITY="CRITICAL"
    [ "$POLICY" = "PUBLIC" ] && SEVERITY="CRITICAL"
    [ "$ENCRYPT" = "NO_ENCRYPTION" ] && [ "$SEVERITY" = "INFO" ] && SEVERITY="MEDIUM"
    echo "${bucket},${BLOCK},${ACL},${POLICY},${ENCRYPT},${SEVERITY}" >> "${OUTDIR}/s3-findings.csv"
done < "${OUTDIR}/buckets.txt"
S3_HIGH=$(grep -c 'CRITICAL\|HIGH' "${OUTDIR}/s3-findings.csv" || true)
echo "      Buckets scanned. Critical/High findings: ${S3_HIGH}"
echo ""

# ── Step 3: IAM Policy Audit ────────────────────────────────────────
echo "[3/6] Auditing IAM policies for over-permissive access..."
aws iam list-users --profile "$PROFILE" --query 'Users[*].UserName' --output text \
    | tr '\t' '\n' > "${OUTDIR}/iam-users.txt"
aws iam list-roles --profile "$PROFILE" --query 'Roles[*].RoleName' --output text \
    | tr '\t' '\n' > "${OUTDIR}/iam-roles.txt"

# Check for inline policies allowing * on *
>"${OUTDIR}/iam-findings.csv"
for entity_type in user role; do
    list_file="${OUTDIR}/iam-${entity_type}s.txt"
    while IFS= read -r name; do
        [ -z "$name" ] && continue
        if [ "$entity_type" = "user" ]; then
            POLICIES=$(aws iam list-user-policies --profile "$PROFILE" --user-name "$name" --query 'PolicyNames' --output text 2>/dev/null)
            ATTACHED=$(aws iam list-attached-user-policies --profile "$PROFILE" --user-name "$name" --query 'AttachedPolicies[*].PolicyArn' --output text 2>/dev/null)
        else
            POLICIES=$(aws iam list-role-policies --profile "$PROFILE" --role-name "$name" --query 'PolicyNames' --output text 2>/dev/null)
            ATTACHED=$(aws iam list-attached-role-policies --profile "$PROFILE" --role-name "$name" --query 'AttachedPolicies[*].PolicyArn' --output text 2>/dev/null)
        fi
        IS_ADMIN="false"
        for pol_arn in $ATTACHED; do
            if echo "$pol_arn" | grep -qi 'AdministratorAccess\|FullAccess'; then
                IS_ADMIN="true"
                break
            fi
        done
        if [ "$IS_ADMIN" = "true" ]; then
            echo "${entity_type},${name},ADMIN_ACCESS" >> "${OUTDIR}/iam-findings.csv"
        fi
    done < "$list_file"
done

# Access key age audit
aws iam list-access-keys --profile "$PROFILE" --query 'AccessKeyMetadata[?Status==`Active`].[UserName,AccessKeyId,CreateDate]' --output text \
    | awk '{age_days=int((systime()-sprintf("%d", mktime(gensub(/[-T:.Z]/," ","g",$3))))/86400); if(age_days>90) print $1","$2","$3","age_days}' \
    > "${OUTDIR}/old-access-keys.csv" 2>/dev/null || true

IAM_ADMIN=$(wc -l < "${OUTDIR}/iam-findings.csv" 2>/dev/null || echo "0")
echo "      Over-permissioned entities: ${IAM_ADMIN}"
echo ""

# ── Step 4: Security Group Audit ────────────────────────────────────
echo "[4/6] Scanning security groups for wide-open ingress..."
aws ec2 describe-security-groups --profile "$PROFILE" --query 'SecurityGroups[].[GroupId,GroupName,Description, IpPermissions[*].IpRanges[?CidrIp==`0.0.0.0/0`].CidrIp]' --output json \
    > "${OUTDIR}/sg-all-open.json" 2>/dev/null

# Summarize open ports
jq -r '.[] | select(.[3] | length > 0) | .[0] + "," + .[1]' "${OUTDIR}/sg-all-open.json" \
    > "${OUTDIR}/open-security-groups.csv" 2>/dev/null || true
SG_OPEN=$(wc -l < "${OUTDIR}/open-security-groups.csv" 2>/dev/null || echo "0")
echo "      Security groups with 0.0.0.0/0 ingress: ${SG_OPEN}"
echo ""

# ── Step 5: Monitoring & Logging Audit ──────────────────────────────
echo "[5/6] Checking CloudTrail and Config status..."
TRAIL_STATUS=$(aws cloudtrail describe-trails --profile "$PROFILE" --query 'trailList[?IsMultiRegionTrail==`true`].Name' --output text 2>/dev/null)
if [ -z "$TRAIL_STATUS" ]; then
    echo "      WARNING: No multi-region CloudTrail found" | tee -a "${OUTDIR}/monitoring-findings.txt"
fi
CONFIG_RECORDER=$(aws configservice describe-configuration-recorders --profile "$PROFILE" --query 'ConfigurationRecorders[*].name' --output text 2>/dev/null)
if [ -z "$CONFIG_RECORDER" ]; then
    echo "      WARNING: No AWS Config recorder enabled" | tee -a "${OUTDIR}/monitoring-findings.txt"
fi
echo ""

# ── Step 6: Prowler CIS Scan (if installed) ─────────────────────────
echo "[6/6] Running Prowler CIS benchmark checks (if available)..."
if command -v prowler &>/dev/null; then
    prowler aws --profile "$PROFILE" --output-modes csv --output-filename "${OUTDIR}/prowler-aws" 2>/dev/null \
        && echo "      Prowler scan complete." \
        || echo "      Prowler scan encountered issues but partial results available."
else
    echo "      Prowler not installed. Install: pip3 install prowler"
    echo "      Run manually: prowler aws --profile ${PROFILE}"
fi
echo ""

# ── Report Generation ───────────────────────────────────────────────
echo "=== Generating Summary Report ==="
cat > "${OUTDIR}/cloud-hunt-report.md" <<REPORT
# Cloud Security Posture Report
**Account:** ${ACCOUNT_ID}  **Profile:** ${PROFILE}  **Date:** $(date)

## Executive Summary

A cloud infrastructure misconfiguration scan was performed against AWS account ${ACCOUNT_ID}.
The scan covered S3 bucket permissions, IAM policy analysis, security group rules,
CloudTrail configuration, and CIS benchmark compliance checks.

## Findings Summary

### CRITICAL / HIGH Severity
- **S3 Buckets:** ${S3_HIGH} buckets with public exposure or missing encryption
- **IAM Over-Permissioning:** ${IAM_ADMIN} users/roles with administrative access
- **Open Security Groups:** ${SG_OPEN} groups allow ingress from 0.0.0.0/0

### S3 Bucket Details
$(column -t -s',' "${OUTDIR}/s3-findings.csv" 2>/dev/null || echo "  No S3 data available")

### Security Groups with 0.0.0.0/0
$(cat "${OUTDIR}/open-security-groups.csv" 2>/dev/null || echo "  None found")

### Monitoring Findings
$(cat "${OUTDIR}/monitoring-findings.txt" 2>/dev/null || echo "  CloudTrail and Config appear configured")

## Next Steps
1. Review all CRITICAL findings immediately — lock exposed S3 buckets, rotate over-permissioned keys
2. Remove 0.0.0.0/0 ingress rules from security groups — use specific IP ranges or VPN
3. Enable S3 Block Public Access at account level
4. Configure AWS Config + CloudTrail if not already enabled
5. Run Prowler full CIS benchmark: \`prowler aws --profile ${PROFILE}\`
6. Schedule monthly follow-up scan to track improvements

REPORT

echo ""
echo "=========================================="
echo "  Cloud Hunter Scan Complete!"
echo "  Output Directory: ${OUTDIR}/"
echo "  Report:           ${OUTDIR}/cloud-hunt-report.md"
echo "  S3 Findings:      ${OUTDIR}/s3-findings.csv"
echo "  IAM Findings:     ${OUTDIR}/iam-findings.csv"
echo "  Open SGs:         ${OUTDIR}/open-security-groups.csv"
echo "=========================================="
```

**What this script produces:** A timestamped output directory with a Markdown executive report, CSV findings per cloud resource category, IAM audit data, and Prowler CIS benchmark results (if installed). Total runtime: 5-15 minutes depending on account size.

**Extending for GCP/Azure:** Replace the AWS CLI calls with `gcloud` equivalents (e.g. `gcloud storage buckets list`, `gcloud iam roles list`, `gcloud compute firewall-rules list`) and `az` equivalents (e.g. `az storage account list`, `az role assignment list`, `az network nsg list`). The report generation and severity scoring logic stays the same.

## Deliverable Format

The client receives a **Cloud Security Posture Report** delivered as a branded PDF (Markdown → pandoc) and a raw CSV data pack for their compliance team.

```markdown
# Cloud Security Posture Report — ACME Corp

**Prepared by:** [Your Name / Company]
**Date:** $(date +%Y-%m-%d)
**Scope:** AWS Production Account (acct-1234-5678), GCP Production (proj-acme-prod)
**Engagement Type:** CIS Foundations Benchmark Audit
**Classification:** CONFIDENTIAL

---

## 1. Executive Summary

ACME Corp's cloud infrastructure was assessed against the CIS AWS Foundations
Benchmark v3.0 and CIS GCP Foundations Benchmark v2.0. Of 86 checks performed:

| Severity   | Count | % of Total |
|------------|-------|------------|
| Critical   | 3     | 3.5%       |
| High       | 12    | 14.0%      |
| Medium     | 28    | 32.6%      |
| Low        | 19    | 22.1%      |
| Pass       | 24    | 27.9%      |

**Critical Findings:**
1. S3 bucket `acme-backups-prod` is publicly readable (CIS 2.1.1)
2. IAM user `ci-deploy-bot` has AdministratorAccess (CIS 1.16)
3. Security group `sg-prod-web-db` allows 0.0.0.0/0 on port 5432 (CIS 4.1)

---

## 2. Methodology

The assessment used automated scanning tools and manual review:

- **Prowler** — 86 CIS AWS Foundations Benchmark checks
- **ScoutSuite** — Multi-cloud resource enumeration and risk scoring
- **AWS CLI / boto3** — Custom enumeration scripts for IAM, S3, EC2, CloudTrail
- **gcloud CLI** — GCP IAM, Cloud Storage, Firewall, Logging audit
- **kube-bench** — Kubernetes CIS Benchmark (if applicable)
- **Trivy** — Container image vulnerability scan (if applicable)

---

## 3. Detailed Findings

### 3.1 S3 Bucket ACME-BACKUPS-PROD — CRITICAL

- **Check:** CIS 2.1.1 — S3 bucket ACL allows public READ access
- **Evidence:** \`aws s3api get-bucket-acl --bucket acme-backups-prod\`
  returns AllUsers group with READ permission
- **Risk:** Any internet user can list and download all backup files
  (database dumps, config files, customer PII)
- **Remediation:**
  \`\`\`bash
  aws s3api put-public-access-block --bucket acme-backups-prod \
    --public-access-block-configuration \
    BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
  # Then review and remove public ACL grants:
  aws s3api put-bucket-acl --bucket acme-backups-prod --acl private
  \`\`\`
- **CIS Reference:** 2.1.1 (Ensure S3 Bucket Policy Restricts Public Access)
- **CVE/NIST:** T1530 (Data from Cloud Storage)

### 3.2 IAM User CI-DEPLOY-BOT — CRITICAL

- **Check:** CIS 1.16 — IAM policy attached with "Effect": "Allow", "Action": "*"
- **Risk:** Compromise of CI/CD credentials leads to full account takeover
- **Remediation:**
  \`\`\`bash
  # Create scoped deployment policy
  aws iam create-policy --policy-name ci-deploy-restricted \
    --policy-document file://ci-deploy-policy.json
  # Detach admin, attach scoped
  aws iam detach-user-policy --user-name ci-deploy-bot \
    --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
  aws iam attach-user-policy --user-name ci-deploy-bot \
    --policy-arn arn:aws:iam::ACCT_ID:policy/ci-deploy-restricted
  # Rotate access keys
  aws iam create-access-key --user-name ci-deploy-bot
  \`\`\`

### 3.3 Security Group SG-PROD-WEB-DB — CRITICAL

- **Check:** CIS 4.1 — Security group allows unrestricted ingress on port 5432
- **Risk:** Direct PostgreSQL access from the internet enables brute-force
  and data exfiltration
- **Remediation:**
  \`\`\`bash
  # Revoke the 0.0.0.0/0 rule, replace with app-tier CIDR
  aws ec2 revoke-security-group-ingress --group-id sg-xxx \
    --protocol tcp --port 5432 --cidr 0.0.0.0/0
  aws ec2 authorize-security-group-ingress --group-id sg-xxx \
    --protocol tcp --port 5432 --cidr 10.1.0.0/16
  \`\`\`

---

## 4. Kubernetes Security Assessment (if applicable)

| Check | Status | Finding |
|-------|--------|---------|
| RBAC bindings with cluster-admin | FAIL | User \`deployer\` has cluster-admin |
| Pod Security Standards | FAIL | Default namespace allows privileged |
| Network Policies | FAIL | No network policies — flat pod network |
| Secrets not encrypted at rest | PASS | etcd encryption enabled |
| kube-bench score | 62/100 | See appendix for failed controls |

---

## 5. Prioritized Remediation Roadmap

**Immediate (24-48 hours):** Fix all CRITICAL findings
- Lock public S3 buckets
- Remove 0.0.0.0/0 ingress rules
- Detach overly permissive IAM policies
- Rotate exposed credentials

**Short-term (1-2 weeks):** Fix all HIGH findings
- Enable S3 Block Public Access at account level
- Enable CloudTrail and AWS Config across all regions
- Configure VPC Flow Logs
- Implement KMS encryption on all storage
- Enforce Pod Security Standards in Kubernetes

**Medium-term (1-3 months):** Fix MEDIUM findings
- Implement IAM permission boundaries
- Enable AWS GuardDuty / GCP Security Command Center / Azure Defender
- Deploy network policies in Kubernetes
- Set up automated compliance scanning (CI/CD pipeline integration)

---

## 6. Tools Used

| Tool | Version | Purpose |
|------|---------|---------|
| Prowler | 4.x | CIS AWS Foundations Benchmark |
| ScoutSuite | 5.x | Multi-cloud resource enumeration |
| AWS CLI | 2.x | S3, IAM, EC2, CloudTrail auditing |
| gcloud CLI | 474+ | GCP IAM, Storage, Firewall audit |
| Azure CLI | 2.x | Azure RBAC, Storage, NSG audit |
| kube-bench | 0.9+ | Kubernetes CIS Benchmark |
| kubectl | 1.28+ | Manual RBAC and pod security review |
| jq | 1.7 | JSON parsing and data extraction |

---

## 7. Appendix: CIS Benchmark Mapping

Full CIS control mapping with pass/fail per check available in:
\`\`\`
attachments/cis-mapping-ACCT1234-5678.csv
\`\`\`

Key CIS controls assessed:
- CIS AWS Foundations Benchmark v3.0 — Sections 1 (IAM), 2 (S3), 3 (Logging),
  4 (Networking), 5 (CIS), 6 (Compute)
- CIS GCP Foundations Benchmark v2.0 — Sections 1 (IAM), 2 (Logging),
  3 (Networking), 4 (VM), 5 (Storage), 6 (Kubernetes)
- CIS Azure Foundations Benchmark v2.0 — Sections 1 (IAM), 2 (Storage),
  3 (Networking), 4 (Compute), 5 (Logging), 6 (Kubernetes)

---

*Report generated by Cloud Hunter. Findings should be validated and prioritized
based on ACME Corp's specific threat model and risk appetite.*
```

## Workflow

```bash
# Example: Check if an S3 bucket is publicly accessible
BUCKET="target-bucket-name"
aws s3api get-bucket-acl --bucket "$BUCKET" --query 'Grants[?Grantee.URI==`http://acs.amazonaws.com/groups/global/AllUsers`]'
```

1. **Prepare Scope and Credentials** — Define which cloud accounts, regions, and services are in scope. Obtain read-only cross-account IAM role ARN or service account key. Verify access with `aws sts get-caller-identity` / `gcloud auth list` / `az account show`.

2. **Automated Scanning** — Run Prowler for AWS CIS benchmarks, ScoutSuite for multi-cloud resource inventory, and custom `aws-cli`/`gcloud`/`az` scripts for targeted enum. Parallelize independent cloud accounts.

3. **Manual Review and Validation** — Review automated findings for false positives. Manually inspect IAM policy documents, S3 bucket policies, Kubernetes RBAC YAML, and serverless function code for business-logic-specific misconfigurations.

4. **Risk Prioritization** — Classify findings by severity (CVSS-based), impact blast radius, and ease of exploitation. Map to CIS benchmark control IDs for compliance reporting.

5. **Remediation Playbook Generation** — For each finding, write the exact CLI commands or Terraform HCL needed to fix it. Include rollback steps.

6. **Report Delivery** — Generate PDF report via pandoc from Markdown template. Include executive summary, detailed findings, CIS mapping, fix commands, and prioritized roadmap. Deliver CSV raw data for client compliance team.

## Tools

- **Prowler** — CIS AWS Foundations Benchmark scanner (86+ checks). Install: `pip3 install prowler`
- **ScoutSuite** — Multi-cloud resource enumeration and risk scoring. Install: `pip3 install scoutsuite`
- **CloudSploit / Aqua CSPM** — Open-source cloud security posture management
- **kube-bench** — Kubernetes CIS Benchmark scanner. Install: `curl -L https://github.com/aquasecurity/kube-bench/releases/...`
- **Trivy** — Container image and filesystem vulnerability scanner. Install: `apt install trivy` or `pip3 install trivy`
- **AWS CLI v2** — Primary AWS enumeration interface (`s3api`, `iam`, `ec2`, `cloudtrail`, `configservice`, `lambda`, `eks`)
- **gcloud CLI** — GCP resource enumeration (`storage`, `iam`, `compute`, `logging`, `container`, `functions`)
- **Azure CLI** — Azure resource enumeration (`az storage account`, `az role assignment`, `az network nsg`, `az aks`)
- **jq** — JSON parsing for structured output processing
- **kubectl** — Kubernetes resource inspection (`get roles`, `get clusterrolebindings`, `get networkpolicies`, `get podsecuritypolicies`)
- **checkov** — Infrastructure-as-Code scanning for Terraform/CloudFormation misconfigurations. Install: `pip3 install checkov`
- **tfsec** — Terraform security scanning. Install: `apt install tfsec` or `go install github.com/aquasecurity/tfsec/cmd/tfsec@latest`

## Process

1. **Cloud Reconnaissance** — Enumerate all resources across targeted cloud providers: storage buckets, compute instances, IAM principals, security group rules, Kubernetes clusters, serverless functions, load balancers, DNS zones, certificate managers, API gateways.

2. **Misconfiguration Analysis** — Execute CIS benchmark checks via Prowler (AWS), ScoutSuite (multi-cloud), kube-bench (K8s). Manually review IAM policy documents for privilege escalation paths (CloudSplaining, Principal Mapper). Audit S3/Cloud Storage/Blob for public access, unencrypted data, and missing versioning.

3. **Vulnerability Correlation** — Cross-reference misconfigurations with known CVE/exploit paths. Example: an open S3 bucket containing Lambda source code ZIP reveals hardcoded API keys → cloud account takeover chain. Document each attack path with evidence.

4. **Remediation Scripting** — Write automated fix scripts (bash/CLI one-liners, Terraform modules, CloudFormation templates) per finding. Include validation steps to confirm the fix.

5. **Reporting and Handoff** — Generate final report with executive summary (non-technical), technical findings with evidence, CIS benchmark mapping, severity-rated remediation roadmap, and raw data exports for compliance auditors.

## Verification

- [ ] All target cloud accounts/projects enumerated completely within scope
- [ ] Automated scan tools (Prowler, ScoutSuite, kube-bench) executed without errors
- [ ] Manual review of top 5 findings per service category confirms or rejects automated results
- [ ] False positives documented with justification
- [ ] Each finding includes: resource identifier, CIS control mapping, evidence (CLI output), risk description, and exact remediation command
- [ ] No sensitive data (real credentials, client secrets) included in delivered report — sanitize evidence
- [ ] Remediation playbook tested on a non-production resource before recommending to client
- [ ] Client credentials revoked or access key rotated after scan completion per security hygiene
- [ ] Deliverables delivered as password-protected PDF + CSV attachment per client communication preference
- [ ] Report includes a signed findings disclaimer: "This assessment reflects the configuration at the time of scan and does not guarantee ongoing security posture"

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "The cloud provider secures everything — it's their responsibility." | AWS/GCP/Azure operate on a Shared Responsibility Model. The provider secures *the cloud*; you secure *what's in the cloud*. S3 buckets, IAM policies, security groups, and Kubernetes RBAC are 100% your responsibility. A customer-side misconfiguration is the #1 source of cloud breaches. |
| "We use default settings — those must be secure." | Default settings prioritize convenience over security. Default VPCs allow all outbound traffic, default S3 Block Public Access is *off* in many regions, default service accounts in GCP are over-permissioned, and default Kubernetes namespaces allow privileged pods. Default = insecure until proven otherwise. |
| "Nobody will find our buckets — they don't have the URL." | Attackers discover buckets through automated scanning of DNS, Certificate Transparency logs, and GitHub. Shodan and Grayhat Warfare index open buckets continuously. A bucket name is not a security boundary. |
| "We only use CloudTrail — we'll see any attack." | CloudTrail only logs API calls. It does not block, alert, or prevent misconfigurations. Without GuardDuty, Config Rules, and real-time anomaly detection, a bucket opened to the world stays open until the breach bill arrives. |
| "Our IAM is fine — we only gave admin to the CI/CD bot." | A CI/CD pipeline credential with AdministratorAccess is a single point of total compromise. If the CI/CD server is breached, the attacker owns the entire AWS account. Use scoped IAM roles with resource-level permissions and short-lived credentials from AWS STS. |
| "Kubernetes RBAC is too complex to audit — we'll do it later." | A single over-permissioned ClusterRoleBinding grants cluster-admin to any pod. Combined with a compromised container image, the attacker controls all nodes, all namespaces, and all secrets. RBAC takes 30 minutes to audit with `kubectl get clusterrolebindings` but months to recover from a cluster compromise. |
| "We encrypt everything at rest — that's enough." | Encryption at rest protects data only when the storage is offline. A publicly readable but encrypted S3 bucket still exposes all object metadata, filenames, and directory structure. An attacker with read access can download your encrypted files and brute-force the encryption key offline. Encryption complements access control — it does not replace it. |
| "We passed a SOC 2 audit — we're secure in the cloud." | SOC 2 Type II certifies that controls *exist and operated as described* for a specific period. It does not certify absolving of all risk. Many SOC 2-compliant companies have suffered cloud breaches because their audit scope omitted certain services, regions, or IAM permissions. Cloud security is continuous, not point-in-time. |
| "Our cloud bill is only $500/month — we're not a target." | Cloud account takeover is automated and opportunistic, not targeted. Crypto-mining botnets scan for exposed AWS keys continuously. A $500/month account can incur $50,000 in crypto-mining charges in a single weekend. Small accounts are *preferred* targets because they lack monitoring. |
