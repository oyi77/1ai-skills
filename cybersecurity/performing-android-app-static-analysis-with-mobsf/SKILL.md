---
name: performing-android-app-static-analysis-with-mobsf
description: Performs automated static analysis of Android applications using Mobile Security Framework (MobSF) to identify
  hardcoded secrets, insecure permissions, vulnerable components, weak cryptography, and code-level security flaws without
  executing the application. Use when assessing Android APK/AAB files for security vulnerabilities before deployment, during
  penetration testing, or as part of CI/CD security gates.
domain: cybersecurity
tags:
- mobile-security
- android
- mobsf
- static-analysis
- owasp-mobile
- penetration-testing
subdomain: mobile-security
author: mahipal
version: 1.0.0
license: Apache-2.0
nist_csf:
- PR.PS-01
- PR.AA-05
- ID.RA-01
- DE.CM-09
---
# Performing Android App Static Analysis with MobSF

## When to Use

Use this skill when:
- Conducting security assessment of Android APK or AAB files before production release
- Integrating automated mobile security scanning into CI/CD pipelines
- Performing initial triage of Android applications during penetration testing engagements
- Reviewing third-party Android applications for supply chain security risks

**Do not use** this skill as a replacement for manual code review or dynamic analysis -- MobSF static analysis catches pattern-based vulnerabilities but misses runtime logic flaws.

## Prerequisites

- MobSF v4.x installed via Docker (`docker pull opensecurity/mobile-security-framework-mobsf`) or local setup
- Target Android APK, AAB, or source code ZIP
- Python 3.10+ for MobSF REST API integration
- JADX decompiler (bundled with MobSF) for Java/Kotlin source recovery
- Network access to MobSF web interface (default: http://localhost:8000)

## Workflow

1. **Scope the task** — define objectives, boundaries, and success criteria
2. **Gather information** — collect all necessary data and context before proceeding
3. **Execute the core workflow** — follow the domain-specific steps methodically
4. **Validate results** — verify outputs against expected outcomes or baselines
5. **Document findings** — record results, anomalies, and recommendations
### Step 1: Deploy MobSF and Obtain API Key

Launch MobSF using Docker for isolated, reproducible scanning:

```bash
docker run -it --rm -p 8000:8000 opensecurity/mobile-security-framework-mobsf:latest
```

Retrieve the REST API key from the MobSF web interface at `http://localhost:8000/api_docs` or from the startup console output. The API key enables programmatic scanning.

### Step 2: Upload APK for Static Analysis

Upload the target APK using the MobSF REST API:

```bash
curl -F "file=@target_app.apk" http://localhost:8000/api/v1/upload \
  -H "Authorization: <API_KEY>"
```

Response includes the `hash` identifier used for subsequent API calls. MobSF automatically decompiles the APK using JADX, extracts the AndroidManifest.xml, and indexes all resources.

### Step 3: Trigger and Retrieve Static Scan Results

Initiate the static scan and retrieve results:

```bash
# Trigger scan
curl -X POST http://localhost:8000/api/v1/scan \
  -H "Authorization: <API_KEY>" \
  -d "scan_type=apk&file_name=target_app.apk&hash=<FILE_HASH>"

# Retrieve JSON report
curl -X POST http://localhost:8000/api/v1/report_json \
  -H "Authorization: <API_KEY>" \
  -d "hash=<FILE_HASH>"
```

### Step 4: Analyze Critical Findings

MobSF static analysis covers these categories mapped to OWASP Mobile Top 10 2024:

**Manifest Analysis (M8 - Security Misconfiguration)**:
- Exported activities, services, receivers, and content providers without permission guards
- `android:debuggable="true"` left enabled
- `android:allowBackup="true"` enabling data extraction via ADB
- Missing `android:networkSecurityConfig` for certificate pinning

**Code Analysis (M1 - Improper Credential Usage)**:
- Hardcoded API keys, passwords, and tokens in Java/Kotlin source
- Insecure SharedPreferences usage for storing sensitive data
- Weak or broken cryptographic implementations (ECB mode, static IV, hardcoded keys)

**Network Security (M5 - Insecure Communication)**:
- Missing certificate pinning configuration
- Custom TrustManagers that accept all certificates
- Cleartext HTTP traffic allowed without exception domains

**Binary Analysis (M7 - Insufficient Binary Protections)**:
- Missing ProGuard/R8 obfuscation
- Native library vulnerabilities (stack canaries, NX bit, PIE)
- Debugger detection absence

### Step 5: Generate and Export Reports

Export findings in multiple formats for stakeholder communication:

```bash
# PDF report
curl -X POST http://localhost:8000/api/v1/download_pdf \
  -H "Authorization: <API_KEY>" \
  -d "hash=<FILE_HASH>" -o report.pdf

# JSON for programmatic processing
curl -X POST http://localhost:8000/api/v1/report_json \
  -H "Authorization: <API_KEY>" \
  -d "hash=<FILE_HASH>" -o report.json
```

### Step 6: Integrate into CI/CD Pipeline

Add MobSF scanning as a build gate:

```yaml
# GitHub Actions example
- name: MobSF Static Analysis
  run: |
    UPLOAD=$(curl -s -F "file=@app/build/outputs/apk/release/app-release.apk" \
      http://mobsf:8000/api/v1/upload -H "Authorization: $MOBSF_API_KEY")
    HASH=$(echo $UPLOAD | jq -r '.hash')
    curl -s -X POST http://mobsf:8000/api/v1/scan \
      -H "Authorization: $MOBSF_API_KEY" \
      -d "scan_type=apk&file_name=app-release.apk&hash=$HASH"
    SCORE=$(curl -s -X POST http://mobsf:8000/api/v1/scorecard \
      -H "Authorization: $MOBSF_API_KEY" -d "hash=$HASH" | jq '.security_score')
    if [ "$SCORE" -lt 60 ]; then exit 1; fi
```

## Key Concepts

| Term | Definition |
|------|-----------|
| **Static Analysis** | Examination of application code and resources without executing the program; catches structural and pattern-based vulnerabilities |
| **APK Decompilation** | Process of recovering Java/Kotlin source from compiled Dalvik bytecode using tools like JADX or apktool |
| **AndroidManifest.xml** | Configuration file declaring app components, permissions, and security attributes; primary target for manifest analysis |
| **Certificate Pinning** | Technique binding an app to specific server certificates to prevent man-in-the-middle attacks via rogue CAs |
| **ProGuard/R8** | Code obfuscation and shrinking tools that make reverse engineering more difficult by renaming classes and removing unused code |

## When NOT to Use

- You don't have explicit written authorization to test
- Task is about defense/detection, not offense (use detection skills)
- You need to implement security controls (use implementing-* skills)
- Task requires compliance auditing (use auditing-* skills)
- You're investigating an incident (use incident response skills)
- Target is out of scope for your engagement
- Task is about vulnerability scanning only (use scanning tools)


## Red Flags

- Performing actions without explicit written authorization from the asset owner
- Testing against production systems without a defined scope and rules of engagement
- Sharing sensitive findings or credentials in unencrypted communications
- Failing to properly scope and contain the assessment before starting

## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- Results validated against known-good baselines or reference implementations
- Documentation complete enough for another analyst to reproduce findings

## Tools & Systems

- **MobSF**: Automated mobile security analysis framework supporting static and dynamic analysis of Android/iOS apps
- **JADX**: Dex-to-Java decompiler for recovering readable source code from Android APK files
- **apktool**: Tool for reverse engineering Android APK files, decoding resources to near-original form
- **Android Lint**: Google's static analysis tool for Android-specific code quality and security issues
- **Semgrep**: Pattern-based static analysis engine with mobile-specific rule packs for custom vulnerability detection

## Common Pitfalls

- **Ignoring false positives**: MobSF flags patterns like `password` in variable names even when not storing actual credentials. Triage all HIGH findings manually before reporting.
- **Missing obfuscated code**: Static analysis accuracy drops significantly against obfuscated apps. Supplement with dynamic analysis for apps using DexGuard or custom packers.
- **Outdated MobSF rules**: Security rules evolve with Android API levels. Ensure MobSF is updated to match the target app's `targetSdkVersion`.
- **Skipping native code analysis**: MobSF analyzes Java/Kotlin but has limited coverage of native C/C++ libraries. Use `checksec` and manual review for `.so` files.

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
