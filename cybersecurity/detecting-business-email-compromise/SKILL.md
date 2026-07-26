---
name: detecting-business-email-compromise
description: Business Email Compromise (BEC) is a sophisticated fraud scheme where attackers impersonate executives, vendors,
  or trusted partners to trick employees into transferring funds, sharing sensitive data,. Use when working with detecting business email compromise.
domain: cybersecurity
subdomain: phishing-defense
tags:
- phishing
- email-security
- social-engineering
- dmarc
- awareness
- bec
- fraud
version: '1.0'
author: mahipal
license: Apache-2.0
atlas_techniques:
- AML.T0052
- AML.T0088
nist_ai_rmf:
- GOVERN-6.2
- MAP-5.2
d3fend_techniques:
- Restore Object
- Restore Configuration
- Application Configuration Hardening
- Application Hardening
- Disable Remote Access
nist_csf:
- PR.AT-01
- DE.CM-09
- RS.CO-02
- DE.AE-02
---
# Detecting Business Email Compromise

## Overview
Business Email Compromise (BEC) is a sophisticated fraud scheme where attackers impersonate executives, vendors, or trusted partners to trick employees into transferring funds, sharing sensitive data, or changing payment details. Unlike traditional phishing, BEC often contains no malicious links or attachments, relying purely on social engineering. This skill covers detection techniques using email gateway rules, behavioral analytics, and financial process controls.


## When to Use
**Trigger phrases:**
- "detecting business email compromise"
- "Business Email Compromise (BEC) is a sophisticated fraud scheme where attackers "


- When investigating security incidents that require detecting business email compromise
- When building detection rules or threat hunting queries for this domain
- When SOC analysts need structured procedures for this analysis type
- When validating security monitoring coverage for related attack techniques

## Prerequisites
- Email security gateway with BEC detection capabilities
- Understanding of organizational financial processes and approval chains
- Access to email logs and SIEM platform
- Knowledge of social engineering tactics

## Key Concepts

This section covers key concepts for detecting business email compromise.

- Ensure all prerequisites are met before proceeding
- Follow the documented workflow steps in sequence
- Record results and any anomalies encountered during this phase
### BEC Attack Types (FBI IC3 Classification)
1. **CEO Fraud**: Attacker impersonates CEO, requests urgent wire transfer
2. **Account Compromise**: Employee email compromised, used to request payments from vendors
3. **False Invoice Scheme**: Fake invoices from "vendor" with changed bank details
4. **Attorney Impersonation**: Impersonates legal counsel for urgent confidential transfers
5. **Data Theft**: Requests W-2, tax forms, or PII from HR

### Detection Indicators
- Urgency and secrecy language ("confidential", "do not discuss with others")
- New or changed payment instructions
- Executive communication outside normal patterns
- Display name matches executive but email domain differs
- Reply-to address differs from From address
- First-time communication pattern between sender and recipient
- Request for gift cards or cryptocurrency

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

1. **Scope and authorize** — confirm written authorization and define target boundaries
2. **Reconnaissance** — enumerate targets, services, and potential attack surfaces
3. **Exploitation** — attempt exploitation of identified vulnerabilities within scope
4. **Post-exploitation** — document access level, lateral movement, and data exposure
5. **Report and remediate** — compile findings with reproduction steps and fix recommendations
### Step 1: Configure BEC-Specific Email Rules
- Flag emails with VIP display names from external domains
- Detect financial keywords combined with urgency language
- Alert on first-time sender to finance/accounting staff
- Check for Reply-To domain mismatch

### Step 2: Deploy Behavioral Analytics
- Baseline normal communication patterns per user
- Detect anomalous requests (unusual recipient, unusual time, unusual request type)
- Monitor for email forwarding rule changes (T1114.003)

### Step 3: Implement Financial Controls
- Dual-authorization for wire transfers above threshold
- Out-of-band verification for payment detail changes (phone callback)
- Vendor payment change verification process
- Finance team training on BEC red flags

### Step 4: Monitor for Account Compromise
- Detect impossible travel in email login locations
- Alert on email forwarding rule creation
- Monitor for mailbox delegation changes
- Check for inbox rules hiding BEC-related emails

### Step 5: Deploy AI/ML Detection

AI-powered BEC detection uses transformer models (BERT, GPT) and NLP to identify sophisticated impersonation attacks that contain no malicious links or attachments. BERT-based models achieve 98.65% accuracy in BEC detection, with a 25%+ improvement over keyword-based rules.

- **Train NLP Models**: Deploy transformer-based models for email content analysis. Detect urgency/manipulation language patterns, identify mismatches between sender identity and writing style, analyze sentiment shifts indicating social engineering pressure.
- **Configure Behavioral Baselines**: AI learns normal communication patterns (who emails whom, frequency, tone). Establish writing style profiles per user (vocabulary, sentence structure). Map typical request types per role (finance processes payments, HR handles PII). Allow 48-hour baseline learning period on historical data.
- **Set Detection Policies**: VIP impersonation (compare against known executive patterns), vendor impersonation (detect payment change requests from lookalike domains), account compromise (sudden behavior changes), supply chain BEC (trusted partner impersonation). Configure confidence thresholds for auto-block vs. warning vs. analyst review.
- **Integrate Response**: Auto-quarantine high-confidence detections, add warning banners for moderate confidence, route suspicious emails to SOC queue, feed verdicts back into training data for improvement.

## When NOT to Use

- You need to perform the attack to test detection (use performing-* skills)
- Task is about analyzing past incidents (use analyzing-* skills)
- You need to implement detection rules (use implementing-* skills)
- Task is about threat hunting proactively (use hunting-* skills)
- You don't have access to logs or monitoring data
- Task requires incident response (use IR skills)


## Red Flags

- Performing actions without explicit written authorization from the asset owner
- Testing against production systems without a defined scope and rules of engagement
- Exceeding the authorized scope of the engagement
- Leaving persistent access mechanisms without explicit approval
- Causing denial-of-service on production systems during testing

## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- All exploited vulnerabilities documented with reproduction steps
- Scope boundaries confirmed — only authorized targets were tested
- Remediation recommendations included for every finding

## Tools & Resources
- **Microsoft Defender for O365**: Built-in BEC detection + AI Impostor Classifier
- **Proofpoint Email Fraud Defense / Tessian**: AI-powered email security with human layer protection
- **Abnormal Security**: API-based AI email security with behavioral analysis
- **Ironscales**: AI + human-in-the-loop BEC detection
- **Darktrace Email**: Self-learning AI for email threat detection
- **FBI IC3 BEC Advisory**: https://www.ic3.gov/
- **FinCEN BEC Advisory**: Financial institution guidance

## Validation
- BEC detection rules trigger on test scenarios
- Financial controls prevent unauthorized transfers in drills
- Account compromise detection catches simulated attacks
- Reduced BEC susceptibility in awareness assessments
- AI detects BEC test email with no malicious indicators (pure social engineering)
- Writing style analysis identifies impersonation of known executive
- Behavioral baseline flags unusual payment request from compromised account
- Detection rate exceeds traditional rule-based filters by 25%+

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |