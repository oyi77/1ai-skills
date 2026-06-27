---
name: validating-backup-integrity-for-recovery
description: Validate backup integrity through cryptographic hash verification, automated restore testing, corruption detection,
  and recoverability checks to ensure backups are reliable for disaster recovery and ransomware response scenarios.
domain: cybersecurity
tags:
- incident-response
- backup
- integrity
- hash-verification
- restore-testing
- disaster-recovery
subdomain: incident-response
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- RS.MA-01
- RS.MA-02
- RS.AN-03
- RC.RP-01
---
# Validating Backup Integrity For Recovery

## When to Use

Use this skill when:
- Verifying backup integrity before relying on backups for ransomware recovery
- Building automated backup validation pipelines that run after each backup job
- Auditing backup infrastructure to confirm recoverability for compliance (SOC 2, ISO 27001, NIST CSF RC.RP-03)
- Detecting silent data corruption (bit rot) in backup storage before a disaster occurs
- Validating that immutable or air-gapped backups have not been tampered with

**Do not use** for initial backup configuration or scheduling. This skill focuses on post-backup validation.

## Prerequisites

- Access to backup storage (local, NAS, S3, Azure Blob, GCS)
- Python 3.9+ with `hashlib` (standard library)
- Backup manifests or baseline hash files for comparison
- Isolated restore environment for restore testing
- Backup tool CLI access (restic, borgbackup, rclone, or vendor-specific)

## Workflow

1. **Define Objectives** — Clarify the goals and scope for backup integrity.
2. **Gather Resources** — Collect tools, data, and access needed for backup integrity.
3. **Execute Process** — Carry out backup integrity operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **recovery** — Primary tool for this skill
- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All backup integrity procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
