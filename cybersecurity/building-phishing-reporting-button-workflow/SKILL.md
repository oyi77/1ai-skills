---
name: building-phishing-reporting-button-workflow
description: Implement a phishing report button in email clients with automated triage workflow that analyzes user-reported
  suspicious emails and provides feedback to reporters.
domain: cybersecurity
subdomain: phishing-defense
tags:
- phishing-reporting
- email-security
- incident-response
- security-awareness
- outlook
- microsoft-365
- soar
mitre_attack:
- T1566
- T1204
- T1534
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.AT-01
- DE.CM-09
- RS.CO-02
- DE.AE-02
---
# Building Phishing Reporting Button Workflow

## Overview
A phishing reporting button empowers users to flag suspicious emails directly from their email client, creating a critical feedback loop between end users and the security operations center. Microsoft's built-in Report button is now the recommended approach, replacing the deprecated Report Message and Report Phishing add-ins. When combined with automated triage using SOAR platforms, reported emails can be classified, IOCs extracted, and remediation actions taken within minutes. Organizations with effective phishing reporting programs see 70%+ report rates in phishing simulations.


## When to Use
**Trigger phrases:**
- "building phishing reporting button workflow"
- "Implement a phishing report button in email clients with automated triage workfl"


- When deploying or configuring building phishing reporting button workflow capabilities in your environment
- When establishing security controls aligned to compliance requirements
- When building or improving security architecture for this domain
- When conducting security assessments that require this implementation

## Prerequisites
- Microsoft 365 or Google Workspace with administrative access
- SOAR platform or automation capability (Microsoft Sentinel, Splunk SOAR, Cortex XSOAR)
- Dedicated reporting mailbox for phishing submissions
- Email security gateway with message retraction capability
- Security awareness training platform for feedback loop

## Workflow

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

1. **Scope the task** — define objectives, boundaries, and success criteria
2. **Gather information** — collect all necessary data and context before proceeding
3. **Execute the core workflow** — follow the domain-specific steps methodically
4. **Validate results** — verify outputs against expected outcomes or baselines
5. **Document findings** — record results, anomalies, and recommendations
### Step 1: Deploy Phishing Report Button
- Enable Microsoft built-in Report button via Security & Compliance Center
- Configure user reported settings: route to reporting mailbox and Microsoft
- For third-party: deploy KnowBe4 Phish Alert Button or Cofense Reporter
- Verify button appears in Outlook desktop, web, and mobile clients
- Configure report options: Report Phishing, Report Junk, Report Not Junk

### Step 2: Build Automated Triage Pipeline
- Configure reporting mailbox monitored by SOAR platform
- Auto-extract IOCs from reported emails: URLs, attachments, sender info, headers
- Submit URLs to VirusTotal, URLScan.io for reputation check
- Submit attachments to sandbox for dynamic analysis
- Check sender against known threat intelligence feeds
- Auto-classify: confirmed phishing, spam, simulation, legitimate

### Step 3: Implement Response Actions
- Confirmed phishing: auto-retract from all inboxes, block sender domain
- Confirmed spam: move to junk for all recipients
- Simulation email: mark as correctly reported, credit user
- Legitimate email: return to inbox, notify reporter
- Generate IOC report for threat intelligence team

### Step 4: Create Feedback Loop
- Send automated thank-you response to reporter within 5 minutes
- Include classification result when analysis completes
- Track reporter accuracy and engagement metrics
- Recognize top reporters in monthly security newsletter
- Feed reporting metrics into security awareness training program

### Step 5: Measure and Optimize
- Track mean time to triage (target: under 10 minutes automated)
- Monitor report volume trends and false positive rates
- Measure user reporting rate in phishing simulations
- Report on confirmed threats caught by user reports vs. gateway
- Optimize automation rules based on classification accuracy

## When NOT to Use

- You need to test what you built (use performing-* skills)
- Task is about configuring existing systems (use configuring-* skills)
- You need to analyze the output (use analyzing-* skills)
- Task is about implementing vendor solutions (use implementing-* skills)
- You don't have infrastructure access
- Task requires compliance validation (use auditing-* skills)


## Red Flags

- Performing actions without explicit written authorization from the asset owner
- Testing against production systems without a defined scope and rules of engagement
- Destroying potential evidence during the containment phase
- Failing to document the chain of custody for all collected artifacts
- Communicating incident details over unencrypted or monitored channels

## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- Timeline of events reconstructed with corroborating evidence
- Root cause identified and documented with contributing factors
- Post-incident review completed with lessons learned and action items

## Tools & Resources
- **Microsoft Report Button**: Built-in Outlook phishing reporting
- **Cofense Reporter + Triage**: Enterprise phishing reporting and automated analysis
- **KnowBe4 Phish Alert Button**: Integrated reporting with simulation platform
- **Microsoft Sentinel**: SOAR automation for triage workflow
- **Proofpoint CLEAR**: Closed-loop email analysis and response

## Validation
- Report button visible and functional across all Outlook platforms
- Reported email arrives in dedicated mailbox within 60 seconds
- Automated triage classifies test phishing email correctly
- Auto-retraction removes confirmed phishing from all inboxes
- Reporter receives feedback notification with classification
- Metrics dashboard shows report volume and accuracy trends

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |