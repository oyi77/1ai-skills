---
name: detecting-azure-lateral-movement
description: Detect lateral movement in Azure AD/Entra ID environments using Microsoft Graph API audit logs, Azure Sentinel
  KQL hunting queries, and sign-in anomaly correlation to identify privilege escalation, token theft, and cross-tenant pivoting.
domain: cybersecurity
subdomain: cloud-security
tags:
- azure
- entra-id
- lateral-movement
- sentinel
- kql
- graph-api
- cloud-security
- threat-hunting
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.IR-01
- ID.AM-08
- GV.SC-06
- DE.CM-01
---

# Detecting Azure Lateral Movement

## Overview

Lateral movement in Azure AD/Entra ID differs from on-premises environments. Attackers pivot through OAuth application consent grants, service principal abuse, cross-tenant access policies, and stolen refresh tokens rather than SMB/RDP connections. Detection requires correlating Microsoft Graph API audit logs, Azure AD sign-in logs, and Entra ID protection risk events using KQL queries in Microsoft Sentinel. This skill covers building detection analytics for common Azure lateral movement techniques including application impersonation, mailbox delegation abuse, and conditional access policy bypasses.


## When to Use

- When investigating security incidents that require detecting azure lateral movement
- When building detection rules or threat hunting queries for this domain
- When SOC analysts need structured procedures for this analysis type
- When validating security monitoring coverage for related attack techniques

## Prerequisites

- Azure subscription with Microsoft Sentinel workspace configured
- Azure AD P2 or Entra ID P2 license for risk-based sign-in detection
- Microsoft Graph API permissions: AuditLog.Read.All, Directory.Read.All, SecurityEvents.Read.All
- Log Analytics workspace ingesting AuditLogs, SigninLogs, and AADServicePrincipalSignInLogs
- Familiarity with KQL (Kusto Query Language)

## Steps

1. **Inventory cloud assets** — enumerate services, roles, and configurations in scope
2. **Assess configurations** — check against security best practices and CIS benchmarks
3. **Test access controls** — verify IAM policies, network ACLs, and security group rules
4. **Validate logging** — ensure audit trails are enabled and properly retained
5. **Document and remediate** — report findings with specific configuration changes needed
### Step 1: Configure Log Ingestion

Enable diagnostic settings to stream Azure AD logs to Log Analytics:
- Sign-in logs (interactive and non-interactive)
- Audit logs (directory changes, app consent)
- Service principal sign-in logs
- Provisioning logs
- Risky users and risk detections

### Step 2: Build Detection Queries

Create KQL analytics rules in Sentinel for:
- Unusual service principal credential additions
- OAuth application consent grants to unknown apps
- Cross-tenant sign-ins from new tenants
- Token replay from different IP/user-agent combinations
- Mailbox delegation changes (FullAccess, SendAs)

### Step 3: Correlate Events

Chain multiple low-confidence indicators into high-confidence lateral movement detections by correlating sign-in anomalies with directory changes within time windows.

### Step 4: Automate Response

Create Sentinel playbooks (Logic Apps) to automatically revoke suspicious OAuth grants, disable compromised service principals, and enforce step-up authentication.

## Expected Output

JSON report containing detected lateral movement indicators, correlated event chains, affected identities, and recommended containment actions with MITRE ATT&CK technique mappings.
## When NOT to Use

- You need to perform the attack to test detection (use performing-* skills)
- Task is about analyzing past incidents (use analyzing-* skills)
- You need to implement detection rules (use implementing-* skills)
- Task is about threat hunting proactively (use hunting-* skills)
- You don't have access to logs or monitoring data
- Task requires incident response (use IR skills)


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
