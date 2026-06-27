---
name: recovering-deleted-files-with-photorec
description: Recover deleted files from disk images and storage media using PhotoRec's file signature-based carving engine
  regardless of file system damage.
domain: cybersecurity
tags:
- forensics
- file-recovery
- photorec
- file-carving
- data-recovery
- evidence-recovery
subdomain: digital-forensics
version: '1.0'
author: mahipal
license: Apache-2.0
nist_ai_rmf:
- MEASURE-2.7
- MAP-5.1
- MANAGE-2.4
atlas_techniques:
- AML.T0070
- AML.T0066
- AML.T0082
nist_csf:
- RS.AN-01
- RS.AN-03
- DE.AE-02
- RS.MA-01
---
# Recovering Deleted Files With Photorec

## When to Use
- When recovering deleted files from a forensic disk image or storage device
- When the file system is corrupted, formatted, or overwritten
- During investigations requiring recovery of documents, images, videos, or databases
- When file system metadata is unavailable but raw data sectors remain intact
- For recovering files from memory cards, USB drives, and hard drives

## Prerequisites
- PhotoRec installed (part of TestDisk suite)
- Forensic disk image or direct device access (read-only)
- Sufficient output storage space (potentially larger than source)
- Write-blocker if working with original media
- Root/sudo privileges for device access
- Knowledge of target file types for focused recovery

## Workflow

1. **Define Objectives** — Clarify the goals and scope for deleted files.
2. **Gather Resources** — Collect tools, data, and access needed for deleted files.
3. **Execute Process** — Carry out deleted files operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **photorec** — Primary tool for this skill
- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All deleted files procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
