---
name: mobile-hacking
description: Android and mobile application security testing — emulators, rooting, traffic interception, dynamic instrumentation.
  Use when testing mobile apps for vulnerabilities, reversing APKs, or bypassing security controls on Android.
domain: cybersecurity
author: mahipal
license: Apache-2.0
subdomain: general-cybersecurity
tags:
- cybersecurity
- hacking
- mobile
- security
- testing
- threat-defense
- money


version: 1.0.0
---

# Mobile Hacking Skill

## Overview

Android/mobile security testing workflow covering emulator setup, device rooting, traffic interception, dynamic instrumentation, and bypass techniques. Inspired by YesWeHack Android Lab methodology for bug bounty hunters. Covers the full pipeline from environment setup to detection bypass for authorized mobile security assessments.

## When to Use

**Trigger phrases:**
- "mobile hacking"
- "Mobile app bug bounty programs (HackerOne, Bugcrowd mobile scope)"
- "Android security assessments with explicit authorization"
- "APK reverse engineering and static analysis"

## Money-Making Overview

Mobile application pentesting commands premium rates because every company with an app store presence needs it before launch or after major updates. Fintech, crypto, healthcare, and e-commerce are the highest-paying verticals.

### Buyer Personas
- **Fintech & Banking Apps**: Payment apps, digital wallets, neobanks. Compliance-driven (PCI DSS, PSD2). $5K-8K per engagement.
- **Crypto & DeFi Apps**: Wallet apps, exchange apps, DEX frontends. High attack surface, high budget. $5K-10K.
- **Health & MedTech**: HIPAA-sensitive. Telehealth, fitness tracking, medical data protection. $4K-7K.
- **Startup Mobile Apps**: Pre-launch security review. Budget-conscious but motivated by investor due diligence. $2K-4K.

### Pricing Tiers

| Tier | Scope | Price | Typical Clients |
|------|-------|-------|-----------------|
| **Quick Scan** | Automated static analysis (MobSF) + basic dynamic testing, 4-5 hours | $2K-3K | Pre-seed startups, solo developers |
| **Standard Assessment** | Full static + dynamic analysis, Frida instrumentation, API testing, report | $4K-6K | Series A/B startups, mid-market |
| **Premium** | Full reverse engineering, source-assisted audit, compliance mapping (OWASP MASTG), retest | $7K-10K | Fintech, crypto, regulated industries |

### First-Dollar Timeline
- **Day 1-2**: Client qualification, scope agreement, NDA/SOW signed
- **Day 3**: Environment setup, automated static analysis begins
- **Day 4-10**: Dynamic testing, API reverse engineering, bypass testing
- **Day 11-12**: Report drafting, finding validation, peer review
- **Day 13**: Delivery + debrief call. Payment due Net-15.


## Workflow

### Step 1: Environment Setup

Choose between emulator or physical device based on your target:

**Genymotion** — Lightweight, immediate root, x86 only. ARM translation available but mixed results. Free personal use. Good for quick APK inspection.

**Android Studio AVD** — More accurate emulation. Use `google_apis` images (debuggable, allows `adb root`). Avoid `google_apis_playstore` (not rootable). Launch with `-writable-system` flag for full filesystem access.

**CLI Setup (no Android Studio needed):**
```bash
sdkmanager "cmdline-tools;latest" "platform-tools" "platforms;android-34" "system-images;android-34;google_apis;x86_64"
avdmanager create avd -n test_device -k "system-images;android-34;google_apis;x86_64"
emulator -avd test_device -writable-system
```
Export `ANDROID_HOME` and add `platform-tools` and cmdline-tools > bin to `PATH`.

**Physical Device** — Google Pixel recommended. Easy bootloader unlock, excellent Magisk support, most realistic testing environment.

### Step 2: Rooting and Device Prep

For physical devices, root with Magisk:

1. **Unlock bootloader**: Enable Developer Options -> OEM Unlocking -> `adb reboot bootloader` -> `fastboot flashing unlock`
2. **Get factory image** from https://developers.google.com/android/images, extract `boot.img`
3. **Patch with Magisk**: Install Magisk app -> Select and Patch a File -> choose `boot.img`
4. **Flash patched image**: `adb push magisk_patched-XXXXX.img /sdcard/` then `fastboot flash boot magisk_patched-XXXXX.img`
5. **Verify root**: `adb shell` -> `su` -> `whoami` (should return `root`)

**Key Magisk features:**
- Systemless root (modifies boot partition only, preserves OTA)
- Zygisk (runtime process injection, successor to MagiskHide)
- Modules ecosystem (SSL pinning bypass, SafetyNet evasion, Frida integration)
- Shamiko (advanced root hiding without modifying system)

### Step 3: Traffic Interception

Set up Burp Suite proxy for HTTPS traffic capture:

```bash
adb shell settings put global http_proxy HOST_IP:8082
# Export Burp CA cert in DER format (.cer) from Proxy -> Options -> Import/Export
adb push cacert.cer /data/media/0/Download/
# Install via Settings -> Security -> Install from storage, or:
adb shell am start -a android.intent.action.VIEW -t application/x-x509-ca-cert -d file:///sdcard/Download/cacert.cer
```

Configure Burp listener to bind to all interfaces (`0.0.0.0` on port 8082). For Android 7+ user-installed CAs are not trusted by default — this is where Frida or Magisk modules become necessary.

### Step 4: Dynamic Instrumentation with Frida

Two deployment modes:

**Frida Server** — Binary pushed to rooted device, run manually each session:
```bash
# Download matching arch from https://github.com/frida/frida/releases
adb push frida-server /data/local/tmp/
adb shell "chmod 755 /data/local/tmp/frida-server && /data/local/tmp/frida-server &"
```

**Frida Gadget** — Shared library bundled into APK. Works without root, requires repackaging the APK with the gadget `.so` injected.

**Key scripts:**

SSL Pinning Bypass:
```javascript
Java.perform(function() {
    var TrustManager = Java.registerClass({
        name: 'com.custom.TrustManager',
        implements: [Java.use('javax.net.ssl.X509TrustManager')],
        methods: {
            checkClientTrusted: function(chain, authType) {},
            checkServerTrusted: function(chain, authType) {},
            getAcceptedIssuers: function() { return []; }
        }
    });
    var ctx = Java.use('javax.net.ssl.SSLContext').getInstance('TLS');
    ctx.init(null, [TrustManager.$new()], null);
});
```

Root Detection Bypass:
```javascript
Java.perform(function() {
    var RootChecker = Java.use('com.scottyab.rootbeer.RootBeer');
    RootChecker.isRooted.implementation = function() { return false; };
});
```

Emulator Detection Bypass:
```javascript
Java.perform(function() {
    var Build = Java.use('android.os.Build');
    Build.MODEL.value = 'Pixel 7';
    Build.MANUFACTURER.value = 'Google';
    Build.BRAND.value = 'google';
    Build.HARDWARE.value = 'tensor';
});
```

**Usage:**
```bash
frida -U -f com.target.app -l frida-ssl-unpinning.js --no-pause
```

Community scripts: https://codeshare.frida.re/

### Step 5: Automated Analysis with Medusa

Frida automation framework with 90+ prebuilt modules: https://github.com/Ch0pin/medusa/

Key modules:
- `http_communications/multiple_unpinter` — SSL pinning bypass
- `root_detection/universal_root_detection_bypass` — hide root traces
- `crypto_hooks` — intercept and dump cryptographic keys in real-time

```bash
medusa
> use http_communications/multiple_unpinner
> run com.target.app
```

### Step 6: Detection Bypass

Know what you are bypassing before attempting circumvention:

**Root Detection methods:**
- Binary checks: presence of `su`, `busybox`, `magisk` in PATH
- Package checks: Magisk app package name installed
- System property checks: `ro.debuggable=1`, `ro.secure=0`
- Filesystem checks: writable `/system`, known root files

**Emulator Detection methods:**
- Build properties: `goldfish`, `ranchu`, `generic` in Build.HARDWARE/FINGERPRINT
- Missing hardware: no IMEI, no SIM, no Bluetooth adapter
- Sensor checks: accelerometer/gyroscope returning constant zero
- Filesystem artifacts: `/dev/qemu_pipe`, `/dev/qemu_trace`
- Network artifacts: MAC address `02:00:00:00:00:00`, emulator IP ranges

### Decision Framework

| Scenario | Setup |
|----------|-------|
| Speed, snapshots, rootable images | Emulator (AVD with google_apis) |
| Emulator detection, ARM-only libs | Real device (Magisk-rooted) |
| Quick APK inspection | Genymotion |
| Maximum realism and stealth | Magisk-rooted Google Pixel |

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Red Flags

- Testing apps you do not have explicit written authorization to test
- Distributing modified APKs or repackaged applications
- Extracting user data, credentials, or PII from test devices
- Aggressive instrumentation against production backend services
- Ignoring program scope rules or testing out-of-scope mobile endpoints
- Sharing Frida scripts or findings that expose zero-days without coordination

## Verification

Before claiming a mobile security assessment is complete:

- Traffic interception confirmed working (HTTPS requests visible in Burp)
- SSL pinning successfully bypassed for the target application
- Root and/or emulator detection circumvented (app runs without tamper alerts)
- All findings include PoC screenshots or screen recordings
- Frida hooks documented with script snippets and hook points
- Test environment cleaned after assessment (device wiped, certs removed)
- Findings reported within program scope and safe harbor provisions

## Key References

- Android Factory Images: https://developers.google.com/android/images
- Frida CodeShare: https://codeshare.frida.re/
- Medusa Framework: https://github.com/Ch0pin/medusa/
- Magisk Releases: https://github.com/topjohnwu/Magisk/releases
- scrcpy (device mirroring): https://github.com/Genymobile/scrcpy


## First Action in 60 Minutes

Create a file called `mobile-pentest-quickstart.sh` with this content:

```bash
#!/bin/bash
# mobile-pentest-quickstart.sh
# Prerequisites: adb, java, apktool, jadx
TARGET_APK="$1"
WORK_DIR="$PWD/mobile-test-$(date +%Y%m%d)"
mkdir -p "$WORK_DIR/reports" "$WORK_DIR/decompiled"
cd "$WORK_DIR" || exit 1

echo "[+] Checking environment..."
command -v adb >/dev/null || { echo "adb not found"; exit 1; }
command -v apktool >/dev/null || { echo "apktool not found"; exit 1; }

echo "[+] Decompiling with apktool..."
apktool d -f "$TARGET_APK" -o "decompiled/apktool-out" 2>&1 | tail -3

echo "[+] Converting to Java with jadx..."
if command -v jadx >/dev/null; then
    jadx -d "decompiled/jadx-out" "$TARGET_APK" 2>&1 | tail -3
else
    echo "[!] jadx not installed — skipping Java decompilation"
fi

echo "[+] Extracting manifest..."
cp "decompiled/apktool-out/AndroidManifest.xml" "reports/manifest.xml"

echo "[+] Checking for common issues..."
grep -E 'android\.permission\.(READ_SMS|RECORD_AUDIO|CAMERA|ACCESS_FINE_LOCATION|READ_CONTACTS|READ_CALL_LOG)' \
  "reports/manifest.xml" > "reports/dangerous-permissions.txt" 2>/dev/null
grep -E 'android:exported="true"' "reports/manifest.xml" > "reports/exported-components.txt" 2>/dev/null
grep -E 'android:debuggable="true"' "reports/manifest.xml" > "reports/debuggable.txt" 2>/dev/null
grep -E 'android:allowBackup="true"' "reports/manifest.xml" > "reports/backup-enabled.txt" 2>/dev/null

echo ""
echo "=== Quick Wins ==="
echo "1. Dangerous permissions:   $(wc -l < reports/dangerous-permissions.txt) found"
echo "2. Exported components:     $(wc -l < reports/exported-components.txt)"
echo "3. Debuggable:              $(grep -c . reports/debuggable.txt 2>/dev/null || echo 0)"
echo "4. Backup enabled:          $(grep -c . reports/backup-enabled.txt 2>/dev/null || echo 0)"
echo ""
echo "NEXT: frida -U -f com.target.app -l frida-ssl-unpinning.js --no-pause"
```

Run it: `bash mobile-pentest-quickstart.sh target.apk`

In 60 minutes you'll have a `reports/` directory with the extracted AndroidManifest.xml, dangerous permissions listing, exported components inventory, debuggable flag check, and backup status analysis.

## Deliverable Format

Use this template for every mobile pentest engagement deliverable:

````
MOBILE APPLICATION SECURITY ASSESSMENT REPORT

Client: [Name]
Application: [Package name] v[Version]
Platform: Android / iOS / Both
Date: [Start] - [End]
Tester: [Name]
Classification: CONFIDENTIAL

1. EXECUTIVE SUMMARY
   - Scope: [tested features, endpoints, API versions]
   - Risk Level: Critical / High / Medium / Low
   - Total Findings: X (Y Critical, Z High, ...)
   - One-paragraph bottom line for non-technical stakeholders

2. METHODOLOGY
   - Static analysis (jadx, apktool, MobSF)
   - Dynamic analysis (Frida, Objection)
   - Network traffic analysis (Burp Suite, mitmproxy)
   - Storage analysis (shared_prefs, SQLite, internal storage dump)
   - API testing (authentication, authorization, rate limiting)

3. FINDINGS (per finding)
   - ID, Title, OWASP MASTG reference, CVSS v3 score
   - Affected component / endpoint
   - Steps to reproduce (numbered, exact commands)
   - Screenshot or screen recording
   - Remediation guidance with code example

4. SECURITY CONTROLS ASSESSED
   - Authentication & session management
   - Authorization (IDOR / BOLA checks)
   - Local data storage (SharedPreferences, SQLite, Keystore)
   - Network communication (TLS version, ciphers, pinning)
   - Code hardening (ProGuard, obfuscation, debug flags)
   - Reverse engineering resistance (root/jailbreak detection, tamper detection)

5. APPENDIX
   - Environment and device specs
   - Tool versions
   - Test accounts and data (redacted)
   - Screenshot index
````

Billable deliverable: branded PDF report + CSV findings tracker. Include 30-day retest window in the SOW.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "It's just a v1 MVP, security can wait" | V1 is when architecture decisions freeze. Patching auth in v3 costs 50x more and requires a rewrite. |
| "We use HTTPS so our app is secure" | 90% of mobile vulns are client-side — insecure storage, hardcoded keys, rooted device bypass. HTTPS is table stakes. |
| "Users will not reverse engineer our APK" | Automated repackaging tools can inject malware into your APK in under a minute. ProGuard is trivially reversible. |
| "Our API has rate limiting" | Rate limiting does not stop a Frida hook from dumping encryption keys or intercepting websocket traffic. |
| "We are not a bank, who would attack us?" | Mobile apps get attacked for user data, API credits, business logic abuse, and competitive intelligence. |
| "We will fix it after the app store review" | Once an APK is in the wild, attackers have it permanently. There is no recall button. |
| "Our app does not store sensitive data" | SharedPreferences, SQLite databases, and NSUserDefaults are all readable on any rooted/jailbroken device. |