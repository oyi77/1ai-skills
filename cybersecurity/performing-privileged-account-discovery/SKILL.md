---
name: performing-privileged-account-discovery
description: Discover and inventory all privileged accounts across enterprise infrastructure including domain admins, local
  admins, service accounts, database admins, cloud IAM roles, and application admin account
domain: cybersecurity
subdomain: identity-access-management
tags:
- iam
- identity
- access-control
- privileged-access
- discovery
- inventory
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.AA-01
- PR.AA-02
- PR.AA-05
- PR.AA-06
---
# Performing Privileged Account Discovery

## Overview
Discover and inventory all privileged accounts across enterprise infrastructure including domain admins, local admins, service accounts, database admins, cloud IAM roles, and application admin accounts. Covers automated scanning, risk classification, and onboarding to PAM.


## When to Use

- When conducting security assessments that involve performing privileged account discovery
- When following incident response procedures for related security events
- When performing scheduled security testing or auditing activities
- When validating security controls through hands-on testing

## Prerequisites

- Familiarity with identity access management concepts and tools
- Access to a test or lab environment for safe execution
- Python 3.8+ with required dependencies installed
- Appropriate authorization for any testing activities

## Objectives
- Implement comprehensive performing privileged account discovery capability
- Establish automated discovery and monitoring processes
- Integrate with enterprise IAM and security tools
- Generate compliance-ready documentation and reports
- Align with NIST 800-53 access control requirements

## Security Controls
| Control | NIST 800-53 | Description |
|---------|-------------|-------------|
| Account Management | AC-2 | Lifecycle management |
| Access Enforcement | AC-3 | Policy-based access control |
| Least Privilege | AC-6 | Minimum necessary permissions |
| Audit Logging | AU-3 | Authentication and access events |
| Identification | IA-2 | User and service identification |

## Verification
- [ ] Implementation tested in non-production environment
- [ ] Security policies configured and enforced
- [ ] Audit logging enabled and forwarding to SIEM
- [ ] Documentation and runbooks complete
- [ ] Compliance evidence generated
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
- Sharing sensitive findings or credentials in unencrypted communications
- Failing to properly scope and contain the assessment before starting
