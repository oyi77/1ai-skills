---
name: implementing-mobile-application-management
description: Implements Mobile Application Management (MAM) policies to protect enterprise data on managed and unmanaged mobile
  devices through app-level controls including data loss prevention, selective wipe, app configuration, and containerization.
  Use when securing corporate apps on BYOD devices, implementing Intune App Protection Policies, or enforcing data separation
  between personal and work apps.
domain: cybersecurity
tags:
- mobile-security
- android
- ios
- mam
- enterprise-security
- owasp-mobile
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
# Implementing Mobile Application Management

## When to Use

Use this skill when:
- Deploying enterprise mobile app protection without full device management (MDM)
- Implementing BYOD policies that protect corporate data while respecting personal privacy
- Configuring Microsoft Intune App Protection Policies for iOS and Android
- Enforcing data loss prevention controls on managed mobile applications

**Do not use** when full device management (MDM) is already deployed and sufficient -- MAM adds complexity when MDM already provides the needed controls.

## Prerequisites

- Microsoft Intune or equivalent MAM platform (VMware Workspace ONE, MobileIron)
- Azure AD for identity and conditional access policies
- Intune App SDK integrated into target applications (or Intune App Wrapping Tool)
- Test devices (Android 10+ and iOS 15+)
- Azure AD Premium P1 or P2 licenses for conditional access

## Workflow

1. **Scope the task** — define objectives, boundaries, and success criteria
2. **Gather information** — collect all necessary data and context before proceeding
3. **Execute the core workflow** — follow the domain-specific steps methodically
4. **Validate results** — verify outputs against expected outcomes or baselines
5. **Document findings** — record results, anomalies, and recommendations
### Step 1: Define App Protection Policy Requirements

Classify data sensitivity and define protection tiers:

| Tier | Data Type | Controls |
|------|-----------|----------|
| Tier 1 - Basic | General corporate email | Require PIN, block screenshots |
| Tier 2 - Enhanced | Financial data, HR records | Encrypt app data, restrict cut/copy/paste |
| Tier 3 - High | PII, healthcare, legal | Selective wipe, offline access limits, DLP |

### Step 2: Configure Intune App Protection Policies

**Android App Protection Policy:**
```json
{
    "displayName": "Corporate App Protection - Tier 2",
    "platform": "android",
    "dataProtectionSettings": {
        "allowedDataStorageLocations": ["oneDriveForBusiness", "sharePoint"],
        "blockDataTransferToOtherApps": "managedApps",
        "blockDataTransferFromOtherApps": "managedApps",
        "saveAsBlocked": true,
        "clipboardSharingLevel": "managedAppsWithPasteIn",
        "screenCaptureBlocked": true,
        "encryptAppData": true,
        "backupBlocked": true
    },
    "accessSettings": {
        "pinRequired": true,
        "minimumPinLength": 6,
        "biometricEnabled": true,
        "offlineGracePeriod": 720,
        "offlineWipeInterval": 90
    },
    "conditionalLaunchSettings": {
        "maxOsVersion": "15.0",
        "minOsVersion": "12.0",
        "jailbreakBlocked": true,
        "maxPinRetries": 5
    }
}
```

### Step 3: Implement App Configuration Policies

Deploy managed app configuration for automatic endpoint setup:

```json
{
    "displayName": "Email App Configuration",
    "targetedManagedApps": ["com.microsoft.outlooklite"],
    "settings": [
        {"key": "com.microsoft.outlook.EmailProfile.AccountType", "value": "ModernAuth"},
        {"key": "com.microsoft.outlook.EmailProfile.ServerName", "value": "outlook.office365.com"},
        {"key": "com.microsoft.outlook.EmailProfile.AllowedDomains", "value": "corporate.com"}
    ]
}
```

### Step 4: Deploy Conditional Access Integration

```
Azure AD > Conditional Access > New Policy:
- Users: All users with corporate apps
- Cloud apps: Office 365, custom LOB apps
- Conditions: All platforms
- Grant: Require app protection policy
- Session: App enforced restrictions
```

### Step 5: Test and Validate MAM Controls

Test each policy control on both platforms:

```bash
# Verify data transfer restrictions
1. Open managed app (Outlook)
2. Copy text from email body
3. Attempt paste in unmanaged app (Notes) -- should be blocked
4. Attempt paste in managed app (Teams) -- should work

# Verify selective wipe
1. Enroll test device with MAM
2. Access corporate data in managed apps
3. Trigger selective wipe from Intune portal
4. Verify corporate data removed, personal data intact

# Verify offline grace period
1. Access managed app while connected
2. Disconnect from network
3. After grace period expires, verify app access blocked
```

### Step 6: Monitor and Respond

Configure MAM monitoring dashboards:
- App protection policy assignment status
- Non-compliant device/user reports
- Selective wipe execution logs
- Jailbreak/root detection alerts
- Failed PIN attempt tracking

## Key Concepts

| Term | Definition |
|------|-----------|
| **MAM** | Mobile Application Management - app-level policies without requiring full device enrollment |
| **App Protection Policy** | Set of rules enforcing data protection at the app level (encryption, DLP, access controls) |
| **Selective Wipe** | Removing only corporate data from managed apps while preserving personal data |
| **App Wrapping** | Post-build process applying MAM SDK policies to apps without source code modification |
| **Containerization** | Isolating corporate app data in an encrypted container separate from personal apps |

## When NOT to Use

- You need to test the implementation (use performing-* skills)
- Task is about configuring existing tools (use configuring-* skills)
- You need to analyze security events (use analyzing-* skills)
- Task is about building detection rules (use building-* skills)
- You don't have access to the target environment
- Task requires vendor-specific expertise (consult vendor docs)


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

- **Microsoft Intune**: Cloud-based MAM/MDM platform with app protection policies
- **Intune App SDK**: SDK for integrating MAM controls into custom iOS/Android apps
- **Intune App Wrapping Tool**: Post-compilation tool for applying MAM policies without code changes
- **VMware Workspace ONE**: Alternative MAM platform with app containerization
- **Azure AD Conditional Access**: Policy engine for enforcing MAM enrollment as access condition

## Common Pitfalls

- **SDK version mismatch**: Intune App SDK version must match the policy version. Outdated SDK versions may silently fail to enforce newer policies.
- **iOS managed pasteboard**: iOS enforces paste restrictions through managed pasteboard, which requires the app to opt-in via Intune SDK integration.
- **App wrapping limitations**: Wrapped apps cannot use certain features (push notifications on some platforms). SDK integration is preferred for full functionality.
- **User experience friction**: Overly restrictive policies cause user frustration and shadow IT. Start with Tier 1 and escalate based on data sensitivity.

## Overview

> Section content — see SKILL.md body for full details.
