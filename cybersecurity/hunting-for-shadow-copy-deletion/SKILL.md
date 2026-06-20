---
name: hunting-for-shadow-copy-deletion
description: Hunt for Volume Shadow Copy deletion activity that indicates ransomware preparation or anti-forensics by monitoring
  vssadmin, wmic, and PowerShell shadow copy commands.
domain: cybersecurity
tags:
- threat-hunting
- mitre-attack
- shadow-copy
- ransomware
- anti-forensics
- t1490
- proactive-detection
subdomain: threat-hunting
version: '1.0'
author: mahipal
license: Apache-2.0
d3fend_techniques:
- Platform Hardening
- Restore Object
- Restore Configuration
- Restore Software
- Software Update
nist_csf:
- DE.CM-01
- DE.AE-02
- DE.AE-07
- ID.RA-05
---

# Hunting For Shadow Copy Deletion

## When to Use

- When proactively hunting for indicators of hunting for shadow copy deletion in the environment
- After threat intelligence indicates active campaigns using these techniques
- During incident response to scope compromise related to these techniques
- When EDR or SIEM alerts trigger on related indicators
- During periodic security assessments and purple team exercises

## Prerequisites

- EDR platform with process and network telemetry (CrowdStrike, MDE, SentinelOne)
- SIEM with relevant log data ingested (Splunk, Elastic, Sentinel)
- Sysmon deployed with comprehensive configuration
- Windows Security Event Log forwarding enabled
- Threat intelligence feeds for IOC correlation

## Workflow

1. **Formulate Hypothesis**: Define a testable hypothesis based on threat intelligence or ATT&CK gap analysis.
2. **Identify Data Sources**: Determine which logs and telemetry are needed to validate or refute the hypothesis.
3. **Execute Queries**: Run detection queries against SIEM and EDR platforms to collect relevant events.
4. **Analyze Results**: Examine query results for anomalies, correlating across multiple data sources.
5. **Validate Findings**: Distinguish true positives from false positives through contextual analysis.
6. **Correlate Activity**: Link findings to broader attack chains and threat actor TTPs.
7. **Document and Report**: Record findings, update detection rules, and recommend response actions.

## Key Concepts

| Concept | Description |
|---------|-------------|
| T1490 | Inhibit System Recovery |
| T1486 | Data Encrypted for Impact |
| T1485 | Data Destruction |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| CrowdStrike Falcon | EDR telemetry and threat detection |
| Microsoft Defender for Endpoint | Advanced hunting with KQL |
| Splunk Enterprise | SIEM log analysis with SPL queries |
| Elastic Security | Detection rules and investigation timeline |
| Sysmon | Detailed Windows event monitoring |
| Velociraptor | Endpoint artifact collection and hunting |
| Sigma Rules | Cross-platform detection rule format |

## Common Scenarios

1. **Scenario 1**: Ransomware deleting shadow copies before encryption
2. **Scenario 2**: vssadmin delete shadows /all /quiet pre-encryption
3. **Scenario 3**: WMIC shadowcopy delete via PowerShell
4. **Scenario 4**: bcdedit disabling recovery mode before impact

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
- Failing to use write-blockers when acquiring forensic evidence
- Not verifying hash integrity before and after imaging
- Modifying original evidence during analysis

## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- Hash values computed and verified match between source and image
- Chain of custody log complete with timestamps and examiner names
- Analysis tools and versions documented for reproducibility

## Output Format

```
Hunt ID: TH-HUNTIN-[DATE]-[SEQ]
Technique: T1490
Host: [Hostname]
User: [Account context]
Evidence: [Log entries, process trees, network data]
Risk Level: [Critical/High/Medium/Low]
Confidence: [High/Medium/Low]
Recommended Action: [Containment, investigation, monitoring]
```

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
