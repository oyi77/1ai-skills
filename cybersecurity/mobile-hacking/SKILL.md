---
name: mobile-hacking
description: Android and mobile application security testing — emulators, rooting, traffic interception, dynamic instrumentation. Use when testing mobile apps for vulnerabilities, reversing APKs, or bypassing security controls on Android.
---

# Mobile Hacking Skill

## Overview

Android/mobile security testing workflow covering emulator setup, device rooting, traffic interception, dynamic instrumentation, and bypass techniques. Inspired by YesWeHack Android Lab methodology for bug bounty hunters. Covers the full pipeline from environment setup to detection bypass for authorized mobile security assessments.

## When to Use

- Mobile app bug bounty programs (HackerOne, Bugcrowd mobile scope)
- Android security assessments with explicit authorization
- APK reverse engineering and static analysis
- Mobile API testing behind app-specific auth flows
- Bypassing SSL pinning to inspect encrypted traffic
- Testing root/emulator detection mechanisms
- Dynamic instrumentation of running Android applications

## The Process

1. **Scope the task** — define objectives, boundaries, and success criteria
2. **Gather information** — collect all necessary data and context before proceeding
3. **Execute the core workflow** — follow the domain-specific steps methodically
4. **Validate results** — verify outputs against expected outcomes or baselines
5. **Document findings** — record results, anomalies, and recommendations
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
