---
name: hunting-for-suspicious-scheduled-tasks
description: Hunt for adversary persistence and execution via Windows scheduled tasks by analyzing task creation events, suspicious
  task properties, and unusual execution patterns that indicate T1053.005 abuse.
domain: cybersecurity
tags:
- threat-hunting
- scheduled-tasks
- persistence
- mitre-t1053-005
- windows
- endpoint-detection
subdomain: threat-hunting
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- DE.CM-01
- DE.AE-02
- DE.AE-07
- ID.RA-05
---

# Hunting for Suspicious Scheduled Tasks

## When to Use

- When proactively hunting for persistence mechanisms in Windows environments
- After detecting schtasks.exe or at.exe usage in process creation logs
- When investigating malware that survives reboots and user logoffs
- During incident response to enumerate all persistence on compromised systems
- When Windows Security Event ID 4698 (Scheduled Task Created) fires for unusual tasks

## Prerequisites

- Windows Security Event ID 4698/4699/4702 (Task Created/Deleted/Updated)
- Sysmon Event ID 1 for schtasks.exe process creation with command lines
- Windows Task Scheduler operational log (Microsoft-Windows-TaskScheduler/Operational)
- PowerShell logging for Register-ScheduledTask cmdlet usage
- Access to Task Scheduler XML definitions on endpoints

## Workflow

1. **Enumerate All Scheduled Tasks**: Collect complete task inventory from target systems using `schtasks /query /fo CSV /v` or `Get-ScheduledTask` PowerShell cmdlet.
2. **Monitor Task Creation Events**: Track Event ID 4698 for new task creation, correlating with the creating process and user account context.
3. **Analyze Task Actions**: Examine what each task executes. Flag tasks running scripts (PowerShell, cmd, wscript), binaries from user-writable paths (TEMP, AppData, Downloads), or encoded/obfuscated commands.
4. **Check Task Triggers**: Review trigger conditions. Tasks triggered by system startup, user logon, or short intervals (1-5 minutes) warrant investigation.
5. **Identify Hidden or Disguised Tasks**: Hunt for tasks with names mimicking legitimate Windows tasks, tasks with Security Descriptor modifications hiding them from standard enumeration, or tasks stored in non-standard registry locations.
6. **Correlate with Process Execution**: Match scheduled task execution events with process creation logs to confirm what actually runs.
7. **Baseline and Diff**: Compare current task inventory against known-good baselines to identify new, modified, or unexpected tasks.

## Detection Queries

This section covers detection queries for hunting for suspicious scheduled tasks.

- Ensure all prerequisites are met before proceeding
- Follow the documented workflow steps in sequence
- Record results and any anomalies encountered during this phase
### Splunk -- Scheduled Task Creation
```spl
index=wineventlog EventCode=4698
| spath output=TaskName path=EventData.TaskName
| spath output=TaskContent path=EventData.TaskContent
| where NOT match(TaskName, "(?i)(\\\\Microsoft\\\\|\\\\Windows\\\\)")
| table _time Computer SubjectUserName TaskName TaskContent
```

### Splunk -- Schtasks.exe Suspicious Usage
```spl
index=sysmon EventCode=1 Image="*\\schtasks.exe"
| where match(CommandLine, "(?i)/create")
| where match(CommandLine, "(?i)(powershell|cmd|wscript|cscript|mshta|rundll32|regsvr32|http|https|\\\\temp\\\\|\\\\appdata\\\\)")
| table _time Computer User CommandLine ParentImage
```

### KQL -- Microsoft Sentinel
```kql
SecurityEvent
| where EventID == 4698
| extend TaskName = tostring(EventData.TaskName)
| extend TaskContent = tostring(EventData.TaskContent)
| where TaskContent has_any ("powershell", "cmd.exe", "wscript", "http://", "https://", "\\Temp\\", "\\AppData\\")
| project TimeGenerated, Computer, Account, TaskName, TaskContent
```

## Common Scenarios

1. **Cobalt Strike Persistence**: Creates scheduled tasks via schtasks.exe to execute PowerShell download cradles at user logon intervals.
2. **Ransomware Staging**: Task created to run encryption payload at a future time, often during off-hours for maximum impact.
3. **Hidden Task via SD Modification**: Attacker modifies Security Descriptor of scheduled task to hide it from normal enumeration while maintaining execution.
4. **COM Handler Abuse**: Task uses COM handler rather than direct executable path, making action inspection more complex.
5. **Lateral Movement via Tasks**: Remote scheduled task creation using `schtasks /create /s REMOTE_HOST` for execution on other systems.

## When NOT to Use

- You're responding to a known incident (use IR skills)
- Task is about analyzing confirmed malware (use analyzing-* skills)
- You need to implement detection rules (use implementing-* skills)
- Task is about vulnerability scanning (use scanning tools)
- You don't have access to endpoint/network data
- Task requires compliance auditing (use auditing-* skills)


## Red Flags

- Performing actions without explicit written authorization from the asset owner
- Testing against production systems without a defined scope and rules of engagement
- Acting on threat intelligence without validating source reliability
- Sharing classified or sensitive indicators without proper handling procedures
- Alerting threat actors to detection capabilities through visible response actions

## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- Results validated against known-good baselines or reference implementations
- Documentation complete enough for another analyst to reproduce findings

## Output Format

```
Hunt ID: TH-SCHTASK-[DATE]-[SEQ]
Host: [Hostname]
Task Name: [Full task path]
Action: [Command/Script executed]
Trigger: [Startup/Logon/Timer/Event]
Created By: [User account]
Created From: [Local/Remote]
Creation Time: [Timestamp]
Run As: [Execution account]
Risk Level: [Critical/High/Medium/Low]
```

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
