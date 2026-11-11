---
name: blue-team-digital-forensics-and-incident-response
description: Use when conducting forensic endpoint investigation, disk artifact analysis, partition recovery, and incident response operations using SANS SIFT, Autopsy, The Sleuth Kit, TestDisk, Extundelete, and Recuva to reconstruct adversary activity and restore compromised systems.
domain: cybersecurity
subdomain: incident-response
category: cybersecurity
version: 1.0.0
author: oyi77
license: Apache-2.0
tags:
- digital-forensics
- incident-response
- data-recovery
- autopsy
- sift
- testdisk
triggers:
- digital forensics
- incident response
- data recovery
- autopsy
- sleuth kit
- testdisk
---

# Blue Team Digital Forensics and Incident Response

## Process
1. Scope by threat model.
2. Select tool category index.
3. Validate prerequisites.
4. Execute operational guidance.
5. Verify with checklist.

## Overview

Cybersecurity playbook for digital forensics and incident response (DFIR). Covers raw disk acquisition, file carving, memory analysis, partition and file recovery, and post-incident timeline reconstruction.

```bash
mkdir -p /cases/ir-001 && dd if=/dev/sda of=/cases/ir-001/disk.raw bs=4M conv=noerror,sync
md5sum /cases/ir-001/disk.raw > /cases/ir-001/disk.raw.md5
mmls /cases/ir-001/disk.raw
fls -r -o <offset> /cases/ir-001/disk.raw > /cases/ir-001/timeline.fls
icat -o <offset> /cases/ir-001/disk.raw <inode> > /cases/ir-001/recovered.bin
```

## When to Use

**Trigger phrases:**
- "digital forensics investigation"
- "incident response timeline reconstruction"
- "recover deleted files using testdisk or extundelete"
- "disk image forensics with autopsy or sleuth kit"

- Responding to active or past host compromise requiring formal chain-of-custody evidence
- Reconstructing timeline of adversary actions from raw disk and memory images
- Recovering files deleted by adversaries or ransomware payload execution
- Repairing damaged partition tables and boot sectors after destructive malware attacks
- Generating structured forensic reports for compliance, legal, or management review

## When NOT to Use

- When conducting active offensive penetration testing or lateral movement
- When analyzing live memory on non-compromised development systems without scope
- When modifying source evidence without write-blocking verification

## Prerequisites

- SANS SIFT or equivalent DFIR Linux environment installed
- Physical or hardware write-blocker for raw disk acquisition
- Autopsy 4.x or The Sleuth Kit CLI binaries available
- TestDisk / PhotoRec and Extundelete utilities compiled and accessible

## Forensic Toolkit

### SANS SIFT Workstation
Comprehensive forensic environment featuring:
- Sleuth Kit (`fls`, `mmls`, `blkcat`, `icat`)
- Volatility 3 for memory dump dissection
- RegRipper for NTUSER.DAT and system hive extraction
- Log2timeline / Plaso for super-timeline generation

### Autopsy Platform
Extensible open-source digital forensics graphical interface:
- Automated ingest modules for keyword search, hash lookup, and web history
- Timeline visualization tool for user activity correlation
- Data source processor for raw DD, E01, and VM disk images

### The Sleuth Kit (TSK)
Command-line file system analysis library:
- Examines NTFS, FAT, Ext2/3/4, ISO9660, and UFS volumes
- Extracts raw metadata, directory structures, and deleted inode clusters

## Data Recovery

### TestDisk & PhotoRec
- **TestDisk:** Recovers lost partitions and fixes corrupted partition tables / boot sectors
- **PhotoRec:** File data carver ignoring the filesystem structure to recover raw file headers

### Extundelete
Utility to recover deleted files from an ext3 or ext4 partition using journal logs and inode references.

### Recuva
Windows-based recovery utility for fat/NTFS drives, applicable to uncorrupted storage volumes.

## Anti-Rationalization Table

| IR Excuse | Flawed Rationalization | Required Discipline |
|---|---|---|
| "Just re-image the system to save time" | "Re-imaging restores service fastest." | Erasing the disk destroys critical evidence and leaves root cause unidentified; image first with write-blocker, then re-image. |
| "Analyze evidence directly on the source drive" | "Mounting read-only is safe enough." | Always operate on bit-stream forensic copies (E01/DD) with verified SHA-256 hashes to maintain chain of custody. |
| "Automated timeline tools catch everything" | "Plaso does all the work." | Automated parsers miss bespoke persistence; manually review MFT, Shimcache, and Shellbags for execution confirmation. |

## Verification Checklist

- [ ] Bit-stream disk images verified against original acquisition hash
- [ ] Write-blockers confirmed active during physical acquisition
- [ ] Autopsy ingest modules executed without parsing failures
- [ ] Sleuth Kit timeline cross-referenced against event logs
- [ ] Recovered files scanned for secondary malware infections
- [ ] Chain of custody documentation signed and archived
