---
name: ios-swiftui
description: Use when shipping an iOS app to the App Store — Xcode project setup, signing and provisioning, Info.plist and entitlements, device capability permissions, TestFlight distribution, and App Store review compliance. UI pattern guidance lives in swiftui-patterns.
domain: development
author: oyi77
license: Apache-2.0
subdomain: software-development
tags:
- ios
- xcode
- app-store
- testflight
- code-signing
- provisioning
- swift
version: 1.0.0
category: development
---

# iOS — App Delivery & Platform Integration

Getting a SwiftUI app from code to the App Store. Covers the parts that are iOS-specific and unforgiving: signing, capabilities, permissions, privacy manifests, TestFlight, and review.

**Scope boundary:** UI architecture (state, navigation, composition, animations) is covered by `swiftui-patterns`. This skill starts where the app already builds and needs to ship.

## When to Use

**Trigger phrases:**
- "ship to App Store" · "TestFlight build" · "code signing fails"
- "provisioning profile" · "app rejected by review"
- "Info.plist permission" · "privacy manifest"
- "Xcode archive / export" · "push notification entitlement"

**Use cases:**
- First App Store submission, or fixing a rejected one
- Adding a capability that needs its own entitlement (push, HealthKit, App Groups)
- CI builds that must sign without a human clicking through Xcode
- Privacy-manifest compliance for third-party SDKs

## When NOT to Use

- Writing UI code, managing state, choosing navigation patterns → `swiftui-patterns`
- Android or cross-platform equivalents → use the platform-specific skill
- Backend/API work behind the app → use backend skills
- macOS-only distribution outside the App Store (notarization) → separate notarization flow

## Overview

Four things block more iOS releases than any bug: **signing**, **capabilities**, **privacy declarations**, and **review compliance**. Each fails in a way that only shows up at archive/upload time, so verify them before you build.

## Workflow

### 1. Project and target configuration

```bash
# Verify the built product before archiving — catch identity mistakes early
xcodebuild -project MyApp.xcodeproj -scheme MyApp \
  -configuration Release -destination 'generic/platform=iOS' \
  -showBuildSettings 2>/dev/null \
  | grep -E 'PRODUCT_BUNDLE_IDENTIFIER|DEVELOPMENT_TEAM|CODE_SIGN_STYLE|MARKETING_VERSION'
```

Check:
- **Bundle identifier** matches the App Store Connect record exactly. A mismatch makes the upload attach to the wrong app or fail outright.
- **`MARKETING_VERSION`** (user-visible) and **`CURRENT_PROJECT_VERSION`** (build number) both increment. App Store Connect rejects duplicate build numbers per version.
- **`DEVELOPMENT_TEAM`** is set — an empty team is the most common archive failure.

### 2. Signing and provisioning

Prefer **automatic signing** unless CI requires otherwise.

```bash
# Automatic (Xcode-managed): one account, profiles fetched on demand
# Xcode → Signing & Capabilities → "Automatically manage signing"

# Manual/CI: list what is actually installed before debugging blind
security find-identity -v -p codesigning          # identities
ls ~/Library/MobileDevice/Provisioning\ Profiles/  # installed profiles

# Archive for distribution
xcodebuild archive \
  -project MyApp.xcodeproj -scheme MyApp \
  -configuration Release \
  -archivePath build/MyApp.xcarchive \
  -destination 'generic/platform=iOS'

# Export using an explicit, checked-in ExportOptions.plist
xcodebuild -exportArchive \
  -archivePath build/MyApp.xcarchive \
  -exportPath build/export \
  -exportOptionsPlist ExportOptions.plist
```

`ExportOptions.plist` should pin `method` (`app-store-connect`), team ID, and signing style. Do not leave it to the GUI — CI cannot click.

Common failures and their real cause:

| Error | Actual cause |
|---|---|
| "No profiles for 'com.x' were found" | Profile doesn't include this bundle ID, or the device/CI lacks the cert |
| "Provisioning profile doesn't include signing certificate" | Cert revoked or expired; re-issue |
| "Missing required icon" | Asset catalog not in the target's resources |
| "Invalid binary — unsupported architectures" | Simulator slice in the archive; check `ONLY_ACTIVE_ARCH`/`EXCLUDED_ARCHS` |

### 3. Capabilities and entitlements

Each protected capability needs BOTH an entitlement and an App Store Connect toggle/matching profile:

| Capability | Entitlement key | Extra step |
|---|---|---|
| Push notifications | `aps-environment` | APNs key/cert in the developer portal |
| HealthKit | `com.apple.developer.healthkit` | HealthKit enabled on the App ID |
| App Groups | `com.apple.security.application-groups` | Group created and assigned |
| Sign in with Apple | `com.apple.developer.applesignin` | Enabled on App ID |
| iCloud | `com.apple.developer.icloud-*` | Container created |

If an entitlement is in the file but not on the App ID, the archive succeeds and the **upload** fails. Check both.

### 4. Permissions and privacy manifest

Every permission string must justify itself to the user and survive review:

```xml
<!-- Info.plist — the string is what the user reads. Be specific, not generic. -->
<key>NSCameraUsageDescription</key>
<string>Scan a receipt to log the expense automatically.</string>
```

A vague string ("This app needs camera access") is a routine rejection. Say what the user gets.

**Privacy manifest** (`PrivacyInfo.xcprivacy`) is required when you or a bundled SDK touch certain APIs or collect data. Declare:
- Collected data types and whether they're linked to identity / used for tracking
- `NSPrivacyAccessedAPITypes` with the reason codes for each accessed API (file timestamp, user defaults, disk space, active keyboards)
- Third-party SDK signatures

Run this check before upload:

```bash
# Find privacy manifests bundled into the built app
find build/export -name 'PrivacyInfo.xcprivacy' | head -20
```

### 5. TestFlight, then review

```bash
# Upload (App Store Connect API key; avoid interactive auth in CI)
xcrun altool --upload-app -f build/export/MyApp.ipa -t ios \
  --apiKey "$ASC_KEY_ID" --apiIssuer "$ASC_ISSUER_ID"
```

Order of confidence: internal TestFlight → external TestFlight → App Review. Never submit to review on the same build that has not passed a real device install.

### 6. Review compliance checklist

Most rejections fall into a handful of buckets — check them before submitting:

- **3.1.1 In-App Purchase** — digital goods must use IAP; linking out to an external payment page is a rejection
- **2.1 Completeness** — no placeholder content, dead links, or non-functional demo accounts (provide working test credentials in review notes)
- **5.1.1 Permission purpose strings** — covered above
- **4.2 Minimum functionality** — a thin wrapper around a website gets rejected
- **2.5.1 Private APIs** — any private symbol use is auto-reject
- **1.2 User-generated content** — needs reporting, blocking, and moderation
- **Account deletion (5.1.1(v))** — apps with account creation must offer in-app deletion

Write review notes that state: what the app does, how to reach each core flow, and any test account credentials.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "It builds and runs in the simulator, so it's ready" | Simulator builds exclude signing entirely. Archive for a device before believing it. |
| "I'll fix the rejection when it comes" | Review cycles cost days. The checklist above catches the majority of avoidable rejections in minutes. |
| "Automatic signing means I don't need to think about it" | Automatic signing still needs a valid team, a registered bundle ID, and unexpired certs. |
| "Privacy manifest is Apple bureaucracy" | Missing declarations block upload for the SDK APIs you actually use. It's a build gate, not advice. |
| "The permission string can be generic" | Generic purpose strings are a documented rejection reason. Write what the user gets. |
| "TestFlight internal is enough testing" | External testers find what your team cannot. Both steps are cheap; a rejection is not. |

## Verification

- [ ] `PRODUCT_BUNDLE_IDENTIFIER` matches the App Store Connect record
- [ ] `MARKETING_VERSION` and `CURRENT_PROJECT_VERSION` both incremented, build number unique
- [ ] `DEVELOPMENT_TEAM` set; signing identity and profile present on the build machine
- [ ] Archive exports cleanly with a checked-in `ExportOptions.plist`
- [ ] Every used capability has BOTH the entitlement and the App ID toggle
- [ ] Every permission has a specific, user-facing purpose string
- [ ] `PrivacyInfo.xcprivacy` present, with accessed-API reason codes and SDK signatures
- [ ] Build installed and exercised on a real device, not just the simulator
- [ ] Internal TestFlight passed before external, external before review
- [ ] Review notes include working test credentials and per-flow navigation
