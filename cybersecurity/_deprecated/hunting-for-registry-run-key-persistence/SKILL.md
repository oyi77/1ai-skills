---
name: hunting-for-registry-run-key-persistence
description: Detect MITRE ATT&CK T1547.001 registry Run key persistence by analyzing Sysmon Event ID 13 logs and registry
  queries to identify malicious auto-start entries. Use when detecting mitre att&ck t1547.001 registry run key persistence by analyzing.
domain: cybersecurity
subdomain: threat-hunting
tags:
- persistence
- registry-run-keys
- t1547-001
- sysmon
- threat-hunting
- windows-forensics
- mitre-attack
version: '1.0'
author: mahipal
license: Apache-2.0
d3fend_techniques:
- Executable Denylisting
- Execution Isolation
- File Metadata Consistency Validation
- Content Format Conversion
- File Content Analysis
nist_csf:
- DE.CM-01
- DE.AE-02
- DE.AE-07
- ID.RA-05
---
# Hunting for Registry Run Key Persistence

## Overview

Registry Run keys (T1547.001) are one of the most commonly used persistence mechanisms by adversaries. When a program is added to a Run key in the Windows registry, it executes automatically when a user logs in. Attackers abuse keys under `HKLM\Software\Microsoft\Windows\CurrentVersion\Run`, `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`, and their RunOnce counterparts to maintain persistence. Sysmon Event ID 13 (RegistryEvent - Value Set) captures registry value modifications including the target object path, the process that made the change, and the new value. Detection involves monitoring these events for suspicious executables in temp directories, encoded PowerShell commands, LOLBin paths, and processes that do not normally create Run key entries. Chaining Event 13 with Event 1 (Process Creation) and Event 11 (FileCreate) strengthens detection by confirming payload creation and execution.


## When to Use
**Trigger phrases:**
- "hunting for registry run key persistence"
- "Detect MITRE ATT&CK T1547"


- When investigating security incidents that require hunting for registry run key persistence
- When building detection rules or threat hunting queries for this domain
- When SOC analysts need structured procedures for this analysis type
- When validating security monitoring coverage for related attack techniques


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Windows systems with Sysmon installed and configured to log Event ID 13
- Sysmon config with RegistryEvent rules for Run/RunOnce keys
- Python 3.9+ with `json`, `xml.etree.ElementTree`, `re` modules
- SIEM or log aggregator collecting Sysmon logs (Splunk, Elastic, Sentinel)
- Knowledge of legitimate auto-start programs for baseline comparison

## Steps

```python
# Example: IOC detection
import re

IOC_PATTERNS = {
    "ip": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "domain": r"\b[a-z0-9-]+\.[a-z]{2,}\b",
    "hash_md5": r"\b[a-f0-9]{32}\b",
    "hash_sha256": r"\b[a-f0-9]{64}\b",
}

def extract_iocs(text: str) -> dict:
    return {k: re.findall(v, text) for k, v in IOC_PATTERNS.items()}
```

1. Collect Sysmon Event ID 13 logs filtered for Run/RunOnce key paths
2. Parse event XML/JSON for TargetObject, Details (value written), Image (modifying process)
3. Flag entries where the value points to temp directories, AppData, or ProgramData
4. Detect encoded PowerShell commands or script interpreters in registry values
5. Identify LOLBin abuse (mshta.exe, rundll32.exe, regsvr32.exe, wscript.exe)
6. Compare against known-good baseline of legitimate auto-start entries
7. Check if the modifying process (Image) is unusual (cmd.exe, powershell.exe, python.exe)
8. Chain with Event ID 1 to verify if the registered binary was recently created
9. Generate detection report with MITRE ATT&CK mapping and severity scores
10. Produce Sigma/Splunk detection rules from findings

## Expected Output

A JSON report listing suspicious Run key entries with the registry path, value written, modifying process, timestamp, MITRE technique mapping, severity rating, and recommended Sigma detection rules.
## Red Flags

- Performing actions without explicit written authorization from the asset owner
- Testing against production systems without a defined scope and rules of engagement
- Acting on threat intelligence without validating source reliability
- Sharing classified or sensitive indicators without proper handling procedures
- Alerting threat actors to detection capabilities through visible response actions

## Process

1. **Reconnaissance** — Gather target information, identify attack surface, enumerate services
1. **Analysis/Exploitation** — Execute the technique, analyze results, document findings
1. **Reporting** — Document IOCs, write findings, provide remediation recommendations

## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- Results validated against known-good baselines or reference implementations
- Documentation complete enough for another analyst to reproduce findings

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |