---
name: deploying-active-directory-honeytokens
description: 'Deploys deception-based honeytokens in Active Directory including fake privileged accounts with AdminCount=1,
  fake SPNs for Kerberoasting detection (honeyroasting), decoy GPOs with cpassword traps, and fake BloodHound paths. Monitors
  Windows Security Event IDs 4769, 4625, 4662, 5136 for honeytoken interaction. Use when implementing AD deception defenses
  for detecting lateral movement, credential theft, and reconnaissance.

  '
domain: cybersecurity
tags:
- active-directory
- honeytokens
- kerberoasting
- deception
- detection
- bloodhound
- gpo
subdomain: deception-technology
version: '1.0'
author: mukul975
license: Apache-2.0
nist_csf:
- DE.CM-01
- DE.AE-06
- PR.IR-01
---
# Deploying Active Directory Honeytokens

## When to Use

- When deploying deception-based detection in Active Directory environments
- When detecting Kerberoasting attacks via fake SPN honeytokens (honeyroasting)
- When creating tripwire accounts to detect credential theft and lateral movement
- When building decoy GPOs to detect Group Policy Preference password harvesting
- When creating deceptive BloodHound paths to misdirect and detect attackers
- When supplementing existing AD monitoring with high-fidelity detection signals

## Prerequisites

- Domain Admin or delegated AD administration privileges
- Active Directory domain (Windows Server 2016+ recommended)
- Windows Event Log forwarding to SIEM (Splunk, Sentinel, Elastic)
- PowerShell 5.1+ with ActiveDirectory module
- Group Policy Management Console (GPMC)
- Understanding of AD security, Kerberos, and BloodHound attack paths

## Workflow

1. **Define Objectives** — Clarify the goals and scope for active directory honeytokens.
2. **Gather Resources** — Collect tools, data, and access needed for active directory honeytokens.
3. **Execute Process** — Carry out active directory honeytokens operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All active directory honeytokens procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
