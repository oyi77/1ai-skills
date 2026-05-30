---
name: analyzing-windows-shellbag-artifacts
description: Analyze Windows Shellbag registry artifacts to reconstruct folder browsing activity, detect access to removable
  media and network shares, and establish user interaction with directories even after deletion using SBECmd and ShellBags
  Explorer.
domain: cybersecurity
subdomain: digital-forensics
tags:
- shellbags
- windows-registry
- sbecmd
- shellbags-explorer
- folder-access
- user-activity
- removable-media
- network-shares
- bagmru
- dfir
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- RS.AN-01
- RS.AN-03
- DE.AE-02
- RS.MA-01
---

# Analyzing Windows Shellbag Artifacts

## Overview

Shellbags are Windows registry artifacts that track how users interact with folders through Windows Explorer, storing view settings such as icon size, window position, sort order, and view mode. From a forensic perspective, Shellbags provide definitive evidence of folder access -- even folders that no longer exist on the system. When a user browses to a folder via Windows Explorer, the Open/Save dialog, or the Control Panel, a Shellbag entry is created or updated in the user's registry hive. These entries persist after folder deletion, drive disconnection, and even across user profile resets, making them invaluable for proving that a user navigated to specific directories on local drives, USB devices, network shares, or zip archives.


## When to Use

- When investigating security incidents that require analyzing windows shellbag artifacts
- When building detection rules or threat hunting queries for this domain
- When SOC analysts need structured procedures for this analysis type
- When validating security monitoring coverage for related attack techniques

## Prerequisites

- Familiarity with digital forensics concepts and tools
- Access to a test or lab environment for safe execution
- Python 3.8+ with required dependencies installed
- Appropriate authorization for any testing activities

## Registry Locations

This section covers registry locations for analyzing windows shellbag artifacts.

- Ensure all prerequisites are met before proceeding
- Follow the documented workflow steps in sequence
- Record results and any anomalies encountered during this phase
### Windows 7/8/10/11

| Hive | Key Path | Stores |
|------|---------|--------|
| NTUSER.DAT | Software\Microsoft\Windows\Shell\BagMRU | Folder hierarchy tree |
| NTUSER.DAT | Software\Microsoft\Windows\Shell\Bags | View settings per folder |
| UsrClass.dat | Local Settings\Software\Microsoft\Windows\Shell\BagMRU | Desktop/Explorer shell |
| UsrClass.dat | Local Settings\Software\Microsoft\Windows\Shell\Bags | Additional view settings |

### BagMRU Structure

The BagMRU key contains a hierarchical tree of numbered subkeys representing the directory structure. Each subkey value contains a Shell Item (SHITEMID) binary blob encoding the folder identity:

- **Root (BagMRU)**: Desktop namespace root
- **BagMRU\0**: Typically "My Computer"
- **BagMRU\0\0**: First drive (e.g., C:)
- **BagMRU\0\0\0**: First subfolder on C:

Each Shell Item contains:
- Item type (folder, drive, network, zip, control panel)
- Short name (8.3 format)
- Long name (Unicode)
- Creation/modification timestamps
- MFT entry/sequence for NTFS folders

## Analysis with EZ Tools

| Tool | Purpose |
|------|---------|
| Platform-specific tools | See the workflow steps for recommended tools |
| Standard utilities | sha256sum, grep, awk for data processing |
### SBECmd (Command Line)

```powershell
# Parse shellbags from a directory of registry hives
SBECmd.exe -d "C:\Evidence\Registry" --csv C:\Output --csvf shellbags.csv

# Parse from a live system (requires admin)
SBECmd.exe --live --csv C:\Output --csvf live_shellbags.csv

# Key output columns:
# AbsolutePath - Full reconstructed path
# CreatedOn - When the folder was first browsed
# ModifiedOn - When view settings were last changed
# AccessedOn - Last access timestamp
# ShellType - Type of shell item (Directory, Drive, Network, etc.)
# Value - Raw shell item data
```

### ShellBags Explorer (GUI)

```powershell
# Launch GUI tool for interactive analysis
ShellBagsExplorer.exe

# Load registry hives: File > Load Hive
# Navigate the tree structure to see folder hierarchy
# Right-click entries for detailed shell item properties
```

## Forensic Investigation Scenarios

**Scenario 1: Standard Analyzing Windows Shellbag Artifacts assessment**
Follow the workflow from initial scoping through execution and validation, documenting each step and its outcome.

**Scenario 2: Emergency Analyzing Windows Shellbag Artifacts response**
Prioritize speed while maintaining accuracy — use pre-configured tools and templates to reduce setup time, but do not skip verification steps.
### Proving USB Device Browsing

```text
Shellbag Path: My Computer\E:\Confidential\Project_Files
ShellType: Directory (on removable volume)
CreatedOn: 2025-03-15 09:30:00 UTC

This proves the user navigated to E:\Confidential\Project_Files
via Windows Explorer, even if the USB drive is no longer connected.
The volume letter E: and directory timestamps can be correlated
with USBSTOR and MountPoints2 registry entries.
```

### Detecting Network Share Access

```text
Shellbag Path: \\FileServer01\Finance\Q4_Reports
ShellType: Network Location
AccessedOn: 2025-02-20 14:15:00 UTC

This proves the user browsed to a network share, even if
the share has been decommissioned or access revoked.
```

### Identifying Deleted Folder Knowledge

```text
Shellbag Path: C:\Users\suspect\Documents\Exfiltration_Staging
ShellType: Directory
CreatedOn: 2025-01-10 08:00:00 UTC

Even though C:\Users\suspect\Documents\Exfiltration_Staging
no longer exists, the Shellbag entry proves the user
created and navigated to this folder.
```

## Limitations

- Shellbags only record folder-level interactions, not individual file access
- Only created through Windows Explorer shell and Open/Save dialogs
- Command-line access (cmd, PowerShell) does not generate Shellbag entries
- Programmatic file access via APIs does not generate Shellbag entries
- Timestamps may reflect view setting changes, not necessarily folder access
- Windows may batch-update Shellbag entries during Explorer shutdown

## When NOT to Use

- You need to perform the attack, not analyze it (use performing-* skills)
- Task is about detection, not analysis (use detecting-* skills)
- You need to implement controls (use implementing-* skills)
- Task is about threat hunting, not post-incident analysis (use hunting-* skills)
- You don't have access to the artifacts/logs to analyze
- Task requires real-time monitoring (use SOC tools)


## Red Flags

- Performing actions without explicit written authorization from the asset owner
- Testing against production systems without a defined scope and rules of engagement
- Exceeding the authorized scope of the engagement
- Leaving persistent access mechanisms without explicit approval
- Causing denial-of-service on production systems during testing

## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- Results validated against known-good baselines or reference implementations
- Documentation complete enough for another analyst to reproduce findings

## References

- Shellbags Forensic Analysis 2025: https://www.cybertriage.com/blog/shellbags-forensic-analysis-2025/
- SANS Shellbag Forensics: https://www.sans.org/blog/computer-forensic-artifacts-windows-7-shellbags
- Magnet Forensics Shellbag Analysis: https://www.magnetforensics.com/blog/forensic-analysis-of-windows-shellbags/
- ShellBags Explorer: https://ericzimmerman.github.io/

## Example Output

```text
$ SBECmd.exe -d "C:\Evidence\Users\jsmith" --csv /analysis/shellbag_output

SBECmd v2.1.0 - ShellBags Explorer (Command Line)
====================================================
Processing hives for user: jsmith
  NTUSER.DAT:  C:\Evidence\Users\jsmith\NTUSER.DAT
  UsrClass.dat: C:\Evidence\Users\jsmith\AppData\Local\Microsoft\Windows\UsrClass.dat

[+] NTUSER.DAT shellbag entries:   456
[+] UsrClass.dat shellbag entries: 1,234
[+] Total shellbag entries:        1,690

--- Folder Access Timeline (Incident Window) ---
Last Accessed (UTC)     | Folder Path                                             | Type        | Access Count
------------------------|---------------------------------------------------------|-------------|-------------
2024-01-15 14:34:05     | C:\Users\jsmith\Downloads                               | File System | 45
2024-01-15 14:36:25     | C:\ProgramData\Updates                                  | File System | 3
2024-01-15 15:05:00     | \\FILESERV01\Finance                                    | Network     | 2
2024-01-15 15:12:30     | \\FILESERV01\Finance\Q4_Reports                          | Network     | 1
2024-01-15 15:30:00     | E:\                                                     | Removable   | 4
2024-01-15 15:30:45     | E:\Backup                                               | Removable   | 3
2024-01-15 15:31:20     | E:\Backup\Corporate_Data                                | Removable   | 2
2024-01-15 16:12:45     | \\FILESERV01\HR\Employees                                | Network     | 1
2024-01-15 16:15:00     | \\FILESERV01\HR\Employees\Records_2024                   | Network     | 1
2024-01-16 02:35:00     | C:\Windows\Temp                                         | File System | 5
2024-01-17 02:44:00     | C:\ProgramData\svc                                     | File System | 2
2024-01-18 01:10:00     | C:\Users\jsmith\AppData\Local\Temp                      | File System | 8

--- Network Share Access ---
  \\FILESERV01\Finance             First: 2023-09-10  Last: 2024-01-15
  \\FILESERV01\Finance\Q4_Reports  First: 2024-01-15  Last: 2024-01-15  (NEW)
  \\FILESERV01\HR\Employees        First: 2024-01-15  Last: 2024-01-15  (NEW)
  \\DC01\SYSVOL                    First: 2023-03-15  Last: 2024-01-16  (anomalous access time)

--- Removable Device Access ---
  E:\ (USB Drive)
    Volume Name:    BACKUP_DRIVE
    First Accessed: 2024-01-15 15:30:00 UTC
    Last Accessed:  2024-01-15 15:45:22 UTC
    Folders Browsed: 3 (E:\, E:\Backup, E:\Backup\Corporate_Data)

--- Deleted/No Longer Existing Paths ---
  C:\ProgramData\Updates\                (folder deleted, shellbag persists)
  C:\ProgramData\svc\                    (folder deleted, shellbag persists)
  C:\Windows\Temp\tools\                 (folder deleted, shellbag persists)

Summary:
  Total unique folders accessed:  1,690
  Network shares accessed:        4 (2 newly accessed during incident)
  Removable media:                1 USB device (data staging suspected)
  Deleted folder evidence:        3 paths (anti-forensics indicator)
  CSV exported to:                /analysis/shellbag_output/
```
