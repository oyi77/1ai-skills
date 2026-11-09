---
name: red-team-privilege-escalation-and-discovery
description: Use when orchestrating privilege escalation and AD discovery during authorized red team engagements, covering Windows/Linux PE tools (LinPEAS, WinPEAS, BeRoot), AD enumeration (Certify, BloodHound, Snaffler, Get-GPPPassword), and defensive access-control bypass (AppLocker, PowerLessShell).
domain: cybersecurity
author: oyi77
version: 1.0.0
category: cybersecurity
tags:
- red-team
- privilege-escalation
- active-directory
- windows-pe
- ad-enum
license: MIT
subdomain: penetration-testing
triggers:
- privilege escalation
- ad discovery
- winpeas
- linpeas
- bloodhound
- certify
- gpppassword
- applocker bypass
---

## Overview

The invariant: escalation is only valid when you have a deterministic reproduction path for the privilege delta and a business-impact story that ties the gain to a tangible asset. Multi-phase escalation — local enumeration, AD trust mapping, ACL abuse pathfinding, and AppLocker bypass — exists to produce that proof.

```
[Phase 1: Local PE Discovery] ──► [Phase 2: AD Trust & ACL Mapping] ──► [Phase 3: Access Control Bypass]
                                                                                │
            [Phase 5: Proof & Escalation Report] ◄── [Phase 4: Escalation Execution] ◄──────────┘
```

The red team escalation operator stays strictly within authorized scope, validates every privilege delta with harmless canaries, and documents the shortest path from the initial access level to the target asset.

## When to Use

- When conducting authorized penetration tests targeting Windows and/or Linux privilege escalation.
- When performing AD enumeration and trust-path analysis for red team exercise objectives.
- When testing for GPP password exposure, ADCS misconfiguration, or ACL abuse paths.
- When bypassing restrictive access controls (AppLocker, constrained PowerShell) for authorized engagement.
- When chaining multiple PE vectors into a deterministic privilege delta that impacts the target objective.

## When NOT to Use

- When conducting defensive hardening or implementing PE remediations (use `cybersecurity/role-security-engineer`).
- When performing routine configuration audits or compliance checks (use `devops/role-devops-sre-engineer`).
- When operating outside explicit written rules of engagement.
- When escalating on systems not included in the authorized scope.

## Deterministic Dispatch Matrix

| Escalation / Discovery Task | Delegated Child Skill | Primary Artifact |
|---|---|---|
| Windows/Linux PE enumeration automation | `cybersecurity/performing-privilege-escalation-on-linux` / `cybersecurity/exploiting-insecure-data-storage-in-mobile` | PE findings with deterministic reproduction steps |
| AD trust mapping and ACL abuse pathfinding | `cybersecurity/exploiting-active-directory-with-bloodhound` | Shortest-path-to-DA graph with verified ACL abuse |
| ADCS certificate service abuse | `cybersecurity/exploiting-active-directory-certificate-services-esc1` | ESC1/ESC2/ESC3/ESC4 exploitation proof |
| AppLocker and restricted shell bypass | `cybersecurity/ultimateapplockerbypasslist` | Bypass reproduction with harmless canary execution |
| PE vulnerability documentation and remediation | `cybersecurity/report-generator` | Structured PE report with CVSS and remediation |

## Workflow

### Phase 1: Local Privilege Escalation Discovery

1. Confirm target is within written RoE scope; record starting privilege level.
2. Run targeted enumeration (WinPEAS/Sherlock on Windows, LinPEAS/lse on Linux) within authorized time windows.
3. Record all misconfigurations: unquoted service paths, weak folder permissions, always-install-elevated, vulnerable drivers.

### Phase 2: AD Trust and ACL Mapping

1. Deploy BloodHound/Snaffler within authorized scope to map AD trust relationships.
2. Run Certify to identify ADCS misconfiguration (ESC1/ESC2/ESC3/ESC4) and verify with harmless certificate requests.
3. Document trust paths to Domain Admin/Enterprise Admin and verify each step in live environment.

### Phase 3: Access Control Bypass Testing

1. When restricted by AppLocker/ConstrainedShell, test against UltimateAppLockerBypassList techniques.
2. Verify bypass with harmless canary commands only (whoami, hostname, touch).
3. Document bypass success and scope implications.

### Phase 4: Escalation Execution and Validation

1. Execute verified escalation path from initial access to target privilege level.
2. Validate each step with canary commands; stop at target achievement.
3. Document full privilege delta chain with timestamps and reproduction commands.

### Phase 5: Proof and Escalation Report

1. Compile privilege delta chain: initial → intermediate → target with deterministic reproduction.
2. Verify all steps are within authorized scope and use non-destructive techniques.
3. Document remediation for each escalation vector with specific code/configuration fixes.

## Anti-Rationalization Table

| Escalation Excuse | Flawed Rationalization | Required Offensive Discipline |
|---|---|---|
| "Just run all PE tools blindly" | "More scans = better escalation." | PE is noisy; use targeted tools per phase. Verify each finding before escalation. |
| "BloodHound shows direct DA access" | "Graph says easy win." | Graph may have stale data. Verify ACL abuse in live environment before escalation. |
| "AppLocker bypass always works" | "List = open door." | Modern environments enforce VHD policies. Test in lab first; validate in production scope. |
| "Get passwords from GPP automatically" | "Legacy policy still everywhere." | GPP creds are legacy. Verify with Get-GPPPassword only in scoped assessment. |
| "Escalate to local admin is enough" | "One admin is sufficient." | Document the target objective. Escalate to the minimum level that proves business impact. |

## Implementation Examples

### WinPEAS/Sherlock Verification Script

```powershell
# Verify WinPEAS output with safe canary
.\WinPEAS.exe -nobanner -quiet | Where-Object { $_ -match "VULN|WEAK|EXPOSED" } | Tee-Object -FilePath peas_finds.txt

# Verify escalation with harmless canary
if (Test-Path "C:\peas_canary.txt") { Remove-Item "C:\peas_canary.txt" -Force }
whoami >> C:\peas_canary.txt
if (Test-Path "C:\peas_canary.txt") {
    Write-Host "CANARY VERIFIED: Escalation path confirmed to $(Get-Content C:\peas_canary.txt)"
    Remove-Item "C:\peas_canary.txt" -Force
}
```

### BloodHound Trust Path Verification

```bash
# Collect AD data within scope
SharpHound.exe -c all --collection-method wmi --domain $DOMAIN

# Verify ACL abuse path with harmless test
# 1. Find path in BloodHound graph
# 2. Test each ACL with canary (e.g., write DAC to test OU modify)
# 3. Document verified path vs. graph path
```

## Verification Checklist

- [ ] Windows PE enumeration complete (WinPEAS, Sherlock, Watson)
- [ ] Linux PE enumeration complete (LinPEAS, lse)
- [ ] AD enum mapped (BloodHound/Snaffler/Get-GPPPassword)
- [ ] ADCS paths validated (Certify)
- [ ] AppLocker bypass list tested against target OS build
- [ ] Results documented with risk ratings
- [ ] All escalation paths verified with harmless canaries
