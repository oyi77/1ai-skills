---
name: detecting-qr-code-phishing-with-email-security
description: Detect and prevent QR code phishing (quishing) attacks that bypass traditional email security by embedding malicious
  URLs in QR code images within emails. Use when detecting and prevent qr code phishing (quishing) attacks that bypass.
domain: cybersecurity
subdomain: phishing-defense
tags:
- quishing
- qr-code
- phishing
- email-security
- image-analysis
- ocr
- mobile-security
version: '1.0'
author: mahipal
license: Apache-2.0
atlas_techniques:
- AML.T0052
- AML.T0024
- AML.T0035
nist_ai_rmf:
- MEASURE-2.8
- MAP-5.1
nist_csf:
- PR.AT-01
- DE.CM-09
- RS.CO-02
- DE.AE-02
---
# Detecting QR Code Phishing with Email Security

## Overview
QR code phishing (quishing) is a rapidly growing attack vector where malicious URLs are embedded in QR code images within phishing emails. Quishing incidents grew fivefold from 46,000 to 250,000 between August and November 2025, with credential phishing comprising 89.3% of detected incidents. Traditional email security filters struggle because QR codes cannot be read by humans or standard URL scanners, and when scanned, users typically use personal mobile devices that lack corporate security controls. Attackers have evolved to use split QR codes (two separate images), nested QR codes, and ASCII text-based QR codes to evade detection.


## When to Use
**Trigger phrases:**
- "detecting qr code phishing with email security"
- "Detect and prevent QR code phishing (quishing) attacks that bypass traditional e"


- When investigating security incidents that require detecting qr code phishing with email security
- When building detection rules or threat hunting queries for this domain
- When SOC analysts need structured procedures for this analysis type
- When validating security monitoring coverage for related attack techniques

## Prerequisites
- Email security gateway with image analysis capabilities
- Understanding of QR code structure and encoding
- Mobile device management (MDM) or mobile threat defense solution
- Security awareness training program
- SIEM platform for correlation and alerting

## Key Concepts

This section covers key concepts for detecting qr code phishing with email security.

- Ensure all prerequisites are met before proceeding
- Follow the documented workflow steps in sequence
- Record results and any anomalies encountered during this phase
### Why Quishing Works
1. **Bypasses URL Scanners**: Traditional gateways scan text-based URLs but cannot decode image-embedded URLs
2. **Shifts to Unprotected Devices**: Corporate email arrives on secured systems but QR scan occurs on personal mobile devices
3. **User Trust**: QR codes are normalized in daily life (payments, menus, parking)
4. **Low Detection Rate**: Only 36% of quishing incidents are accurately identified by recipients

### Evasion Techniques (2025)
- **Split QR Codes**: QR code divided into two separate images that look benign individually (Gabagool PhaaS kit)
- **Nested QR Codes**: QR code within a QR code, with first scan leading to intermediate page
- **ASCII QR Codes**: QR rendered as text characters instead of images, bypassing image analysis (12% of attacks in Jan 2026)
- **Styled/Artistic QR Codes**: Custom-designed QR codes with logos that evade pattern matching
- **PDF Attachment QR**: QR code embedded in PDF attachment rather than email body

### Detection Challenges
- Pattern-based detection faces trade-off: aggressive tuning causes false positives, cautious tuning causes misses
- Average similarity score of 0.209 between quishing and legitimate QR emails
- QR codes in image attachments require OCR and deep image processing

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
### Step 1: Enable Image-Based Threat Detection
- Configure email gateway to scan embedded images for QR codes
- Enable OCR processing on image attachments (PNG, JPG, GIF, BMP)
- Deploy multimodal AI that combines image processing, OCR, and NLP analysis
- Configure PDF scanning to detect QR codes within attachments
- Set up detection for ASCII/text-based QR code rendering

### Step 2: Configure QR Code URL Analysis
- Extract URLs from detected QR codes and submit to URL reputation services
- Apply same URL scanning policies to QR-extracted URLs as text-based URLs
- Enable real-time sandbox analysis for QR-decoded destination pages
- Configure time-of-click protection for QR-extracted URLs where possible
- Block known phishing domains extracted from QR codes

### Step 3: Deploy Mobile-Side Protection
- Implement mobile threat defense (MTD) with QR code scanning capability
- Deploy Palo Alto ALFA or equivalent safe-by-design QR scanning
- Configure MDM policies to warn users before opening scanned URLs
- Enable corporate VPN/secure browser for QR-scanned destinations
- Block known credential harvesting domains at the mobile proxy level

### Step 4: Build Detection Rules
- Alert on emails containing only an image and minimal text (common quishing pattern)
- Flag emails with QR code images from external first-time senders
- Detect urgency language combined with QR code presence
- Alert on emails impersonating IT/security team requesting QR scan for MFA setup
- Monitor for common quishing themes: MFA reset, document signing, voicemail notification

### Step 5: Train Users on Quishing Recognition
- Update security awareness program to include QR code phishing scenarios
- Conduct quishing simulation campaigns using controlled QR codes
- Teach users to verify QR destination URLs before entering credentials
- Establish reporting process for suspicious QR code emails
- Distribute guidance on safe QR scanning practices

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
- **Barracuda Multimodal AI**: OCR + deep image processing for QR detection
- **Palo Alto ALFA**: Safe-by-design QR code scanning assessment
- **Microsoft Defender for O365**: QR code detection in email images
- **Proofpoint TAP**: Image-based threat analysis with QR decoding
- **Lookout/Zimperium**: Mobile threat defense with QR scanning

## Validation
- QR code phishing emails detected in controlled testing
- Split QR code and ASCII QR code evasion techniques caught
- QR-extracted URLs submitted to sandbox analysis
- Mobile devices alert on malicious QR destinations
- User reporting rate for quishing simulations exceeds 50%
- False positive rate for QR detection below 1%

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