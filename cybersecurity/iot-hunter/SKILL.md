---
name: iot-hunter
description: IoT and embedded device security testing — firmware analysis, hardware interfaces, protocol exploitation. Use
  when testing IoT devices, extracting firmware, analyzing embedded systems, or finding hardware vulnerabilities. Use when working with iot hunter.
domain: cybersecurity
tags:
- cybersecurity
- hunter
- iot
- security
- testing
- threat-defense
- money
- firmware
- hardware
- embedded
---

# IoT Hunter

## Overview

IoT and embedded devices are the fastest-growing attack surface in modern networks. Smart cameras, door locks, medical devices, industrial sensors, and home automation hubs ship with woefully inadequate security — hardcoded credentials, unencrypted storage, debug ports left open in production, and firmware that hasn't been reviewed since the prototype phase. This skill covers the full IoT security testing lifecycle: firmware extraction and reverse engineering, hardware interface probing (UART, JTAG, SPI, I2C), wireless protocol analysis (BLE, Zigbee, Z-Wave, Wi-Fi, MQTT, CoAP), and runtime manipulation to identify vulnerabilities that could lead to device compromise, privilege escalation, or network pivoting.

**Capabilities:**
- Firmware extraction and analysis (binwalk, firmware-mod-kit, unblob)
- Hardware debugging via UART/JTAG/SPI (bus pirate, J-Link, logic analyzer)
- Static and dynamic binary analysis (Ghidra, radare2, checksec)
- Wireless protocol auditing (BLE, Zigbee, Wi-Fi, LoRa)
- Application-layer protocol fuzzing (MQTT, CoAP, HTTP, RTSP, Modbus)
- Cryptographic material recovery (hardcoded keys, certs, flash extraction)
- Boot integrity and secure boot bypass assessment
- Physical interface identification (UART pinout, JTAG boundary scan)

## When to Use

**Trigger phrases:**
- "iot hunter" / "firmware analysis" / "firmware extraction"
- "hardware hacking" / "JTAG debugging" / "UART console"
- "smart device security" / "medical device testing"
- "IoT penetration test" / "reverse engineer firmware"

**Appropriate scenarios:**
- Pre-launch security assessment of a new IoT product
- Post-purchase vulnerability analysis of consumer smart devices
- Medical device security evaluation (FDA pre-market submissions)
- Industrial IoT (IIoT) / SCADA sensor security testing
- Bug bounty hunting on IoT products
- Red team hardware-assisted initial access (rogue device deployment)

## When NOT to Use

- When you lack physical access to the device (most hardware testing requires it)
- When the firmware is encrypted and you have no key extraction path
- For locked-down devices with active secure boot and signed firmware updates — testable but scope is narrower
- When you lack proper authorization for destructive or invasive testing
- On medical devices or safety-critical systems without proper lab isolation and liability coverage

## Prerequisites

**Hardware (recommended):**
- USB UART adapter (CP2102 or CH340G, ~$5)
- JTAG adapter (Bus Pirate v3.6, J-Link EDU Mini)
- Logic analyzer (24MHz 8-channel Saleae clone, ~$15)
- SOP8/SOIC8 clip + flash programmer (CH341A, ~$10)
- Multimeter with continuity/voltage mode
- Screwdriver set, spudger, tweezers, hot air station (optional)

**Software (Kali Linux / apt/pip):**
- `binwalk`, `firmware-mod-kit`, `unblob` — firmware extraction
- `Ghidra` / `radare2` — binary reverse engineering
- `bettercap` — BLE and Wi-Fi MITM testing
- `wireshark` / `tshark` — protocol capture and analysis
- `python3 + scapy` — protocol fuzzing and packet crafting
- `aircrack-ng` / `hashcat` — Wi-Fi PSK cracking (GPU on RTX 2060 SUPER)
- `mqtt-malaria` / `mqtt-pwn` — MQTT security testing
- `flashrom` / `esptool` — SPI flash reading (ESP chips)
- `checksec` (pwntools) — binary security mitigation detection
- `nmap` — network service discovery

## Money-Making Overview

**Target Buyer:** IoT device manufacturers launching connected products, smart home companies doing pre-launch QA, medical device firms preparing for FDA/CE submissions, industrial automation vendors needing pen testing on sensors/gateways.

**How You Make Money:**

1. **Firmware Security Assessment** — Extract, unpack, and audit firmware for hardcoded credentials, backdoors, CVEs, and cryptographic leaks. Deliver finding-by-finding report with CVSS scores. ($2K-$5K/job)

2. **Hardware Interface & Physical Testing** — Identify and exploit UART, JTAG, SPI flash interfaces to gain root shell, dump firmware, extract keys, or bypass secure boot. ($3K-$8K/job)

3. **Network Protocol & Wireless Assessment** — Audit BLE, Zigbee, Wi-Fi, MQTT, CoAP for replay, cleartext, weak pairing, injection, missing auth. ($2K-$5K/job)

### Service Tiers

| Tier | Price | What They Get |
|------|-------|---------------|
| **Basic** — Firmware Quick-Scan | $1,500 | Automated binwalk + firmwalker + strings analysis of provided firmware; CVSS-scored findings for hardcoded creds, known CVEs, and exposed secrets. Report in 48 hours. No physical access. |
| **Pro** — Full IoT Assessment | $5,000 | Physical device + full lab: firmware extraction, UART/JTAG probing, BLE/Wi-Fi sniffing, protocol fuzzing, root shell attempt. Detailed report with PoC videos, CVEs, remediation roadmap. Includes 30-day retest. |
| **Enterprise** — Embedded Security Partnership | $3,500/mo | Quarterly full assessments on up to 3 SKUs, continuous firmware monitoring (supply chain dep scanning), secure boot/SBoM review, code signing pipeline audit, on-call for zero-day disclosures. |

**Expected First Dollar:** 2-4 weeks (acquire hardware tools, find client on Upwork or local IoT manufacturer outreach, deliver one Basic firmware scan)

## First Action in 60 Minutes

The following script performs an automated firmware analysis pipeline: extract filesystem, search for credentials/keys/CVEs/backdoors, run entropy analysis to detect encrypted or compressed regions. Save as `iot-firmware-analyze.sh`.

```bash
#!/bin/bash
# iot-firmware-analyze.sh — IoT Firmware Analysis Pipeline
# Usage: ./iot-firmware-analyze.sh firmware.bin [output_dir]
# Deps: binwalk, strings, firmwalker, unblob, python3
# Install: sudo apt install binwalk python3-pip && pip3 install unblob

set -euo pipefail
[ $# -lt 1 ] && { echo "Usage: $0 <firmware.bin> [output_dir]"; exit 1; }

FIRMWARE="$1"
OUTDIR="${2:-iot-fw-analyze-$(date +%Y%m%d-%H%M%S)}"
[ ! -f "$FIRMWARE" ] && { echo "Error: firmware file not found"; exit 1; }
mkdir -p "$OUTDIR"/{extracted,reports}
echo "[*] Target: $FIRMWARE ($(du -h "$FIRMWARE" | cut -f1)) Output: $OUTDIR"

# Step 1: Entropy analysis (detects encryption/compression)
echo "[*] Step 1: Entropy analysis..."
python3 -c "
import struct, sys, math
with open('$FIRMWARE', 'rb') as f: data = f.read()
for i in range(0, len(data), 4096):
    block = data[i:i+4096]
    if len(block) < 64: continue
    e = 0.0
    for b in range(256):
        p = block.count(b) / len(block)
        if p > 0: e -= p * math.log2(p)
    bar = '#' * int(e/8*50) + '.' * (50 - int(e/8*50))
    print(f'  0x{i:08x} ({i//1024}K): {e:5.2f}/8.0 |{bar}|')
" > "$OUTDIR/reports/entropy.txt"
echo "  -> Entropy report saved"

# Step 2: binwalk scan
echo "[*] Step 2: binwalk signature scan..."
binwalk -B -M -n "$FIRMWARE" > "$OUTDIR/reports/binwalk-scan.txt" 2>/dev/null || true

# Step 3: Automated extraction
echo "[*] Step 3: Firmware extraction..."
command -v unblob &>/dev/null && unblob -e "$OUTDIR/extracted" "$FIRMWARE" 2>/dev/null || true
binwalk -er -C "$OUTDIR/extracted" "$FIRMWARE" 2>/dev/null || true

# Step 4: String extraction and high-value pattern search
echo "[*] Step 4: String analysis..."
strings -n 8 "$FIRMWARE" > "$OUTDIR/reports/all-strings.txt"
echo "  -> $(wc -l < "$OUTDIR/reports/all-strings.txt") strings extracted"

grep -ai 'BEGIN.*RSA.*PRIVATE\|BEGIN.*EC.*PRIVATE\|BEGIN.*OPENSSH.*PRIVATE' \
    "$OUTDIR/reports/all-strings.txt" > "$OUTDIR/reports/secrets-private-keys.txt" 2>/dev/null || true
echo "  -> Private keys: $(wc -l < "$OUTDIR/reports/secrets-private-keys.txt")"

grep -Eai '(password|passwd|secret|token|api[_-]?key)' "$OUTDIR/reports/all-strings.txt" \
    | grep -E '.{6,}' > "$OUTDIR/reports/secrets-credentials.txt" 2>/dev/null || true
echo "  -> Credential strings: $(wc -l < "$OUTDIR/reports/secrets-credentials.txt")"

grep -Eai 'https?://[a-z0-9._-]+' "$OUTDIR/reports/all-strings.txt" \
    > "$OUTDIR/reports/network-urls.txt" 2>/dev/null || true
grep -Eao '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' "$OUTDIR/reports/all-strings.txt" \
    | grep -v '^0\.\|^127\.' > "$OUTDIR/reports/network-ips.txt" 2>/dev/null || true
grep -Eai '(CVE-|backdoor|shell|root|admin)' "$OUTDIR/reports/all-strings.txt" \
    > "$OUTDIR/reports/cve-hints.txt" 2>/dev/null || true

# Step 5: firmwalker
command -v firmwalker &>/dev/null && firmwalker "$OUTDIR/extracted" \
    "$OUTDIR/reports/firmwalker.txt" 2>/dev/null && echo "  -> firmwalker done" || true

# Step 6: File type analysis
if [ -d "$OUTDIR/extracted" ]; then
    find "$OUTDIR/extracted" -type f -exec file {} \; > "$OUTDIR/reports/extracted-filetypes.txt" 2>/dev/null
    find "$OUTDIR/extracted" -name "*busybox*" -o -name "*dropbear*" -o -name "*telnet*" \
        -o -name "*sbin/*" 2>/dev/null | head -50 > "$OUTDIR/reports/firmware-binaries.txt" || true
    echo "  -> ELF binaries: $(find "$OUTDIR/extracted" -type f -exec file {} \; | grep -ci 'elf' 2>/dev/null || echo 0)"
    find "$OUTDIR/extracted" -name "*.conf" -o -name "*.cfg" -o -name "passwd" -o -name "shadow" \
        -o -name "*.pem" -o -name "*.key" -o -name "*.cert" 2>/dev/null \
        > "$OUTDIR/reports/config-files.txt" || true
    echo "  -> Config/cert/key files: $(wc -l < "$OUTDIR/reports/config-files.txt")"
fi

# Summary
echo "============================================"
echo " IoT FIRMWARE ANALYSIS COMPLETE"
echo " Output: $OUTDIR/reports/"
ls -1 "$OUTDIR/reports/"
echo "============================================"
echo "Next: 1) Review secrets-credentials.txt 2) Check private keys"
echo "3) Analyze CVE hints 4) Inspect entropy for encrypted regions"
echo "5) Run Ghidra on key ELFs 6) Connect UART/JTAG for shell"
```

## Deliverable Format

The output is a structured **IoT Security Assessment Report** delivered as PDF + artifacts tarball. Save as `iot-security-report.md` per engagement.

```markdown
# IoT Security Assessment Report

**Client:** [Company Name]  **Device:** [Product, model, firmware version]
**Assessment Date:** YYYY-MM-DD  **Assessor:** [Your name]
**Classification:** CONFIDENTIAL

---

## Executive Summary
[2-3 paragraph summary: what was tested, key findings, overall risk level,
top 3 remediation priorities. Written for C-level readers.]

**Risk Level:** [Critical / High / Medium / Low]
**Total Findings:** X (Y Critical, Z High, W Medium, V Low)

---

## 1. Firmware Analysis

### 1.1 Extraction Details
| Detail | Result |
|--------|--------|
| File type | [TRX / UBI / SquashFS / raw binary] |
| Extraction method | [binwalk -er / unblob / manual] |
| Filesystem type | [SquashFS / JFFS2 / UBIFS / CramFS / initramfs] |
| Root access default? | [Yes/No] |

### 1.2 Hardcoded Credentials & Secrets
| Service | Username | Password | Severity |
|---------|----------|----------|----------|
| SSH/Telnet root | [user] | [pass] | Critical |
| Web UI admin | [user] | [pass] | Critical |
| API token / PSK | [key id] | [value] | High |

- [ ] Private TLS keys found  [ ] API tokens / cloud keys found
- [ ] Pre-shared keys for BLE/Wi-Fi  [ ] Firmware signing keys discovered

### 1.3 Known Vulnerable Components
| Component | Version | CVE(s) | CVSS |
|-----------|---------|--------|------|
| BusyBox | [ver] | CVE-XXXX | 7.5 |
| OpenSSL | [ver] | CVE-XXXX | 9.8 |
| Dropbear | [ver] | CVE-XXXX | 5.3 |

### 1.4 Entropy Analysis
[Summary: encrypted/compressed regions flagged, hidden partitions identified]

---

## 2. Hardware Interface Testing

### 2.1 Physical Access Summary
| Interface | Present? | Access Obtained? | Notes |
|-----------|----------|------------------|-------|
| UART | Yes/No | Root shell / Boot log | TX/RX at [voltage]V, [baud] |
| JTAG/SWD | Yes/No | Boundary scan / Debug | Pins identified, locked? |
| SPI Flash | Yes/No | Dumped / Protected | [chip, size, protection] |
| I2C | Yes/No | Device enumeration | Addresses: [list] |

### 2.2 UART Console Findings
- Baud rate: [115200/57600/9600]  —  Root shell without auth: [Yes/No]
- Boot log leaked kernel pointers: [Yes/No]  —  U-Boot recovery shell: [Yes/No]

### 2.3 JTAG / Flash Findings
- JTAG unlocked? [Yes/No]  —  Secure boot bypass via debug? [Yes/No]
- Flash chip: [vendor, part, capacity]  —  Read-protection: [None/Level 1/Level 2]
- Partitions extracted: [list with sizes and content descriptions]

---

## 3. Wireless & Protocol Testing

### 3.1 BLE
- GATT services: [N]  —  Pairing: [Just Works / Passkey / LE Secure]
- Write/notify without auth: [Yes/No]  —  Replay attack: [Yes/No]

### 3.2 Wi-Fi
- Encryption: [WPA2/WPA3/open]  —  PSK cracked: [Yes/No]
- WPS: [Enabled/Pixie Dust vulnerable]  —  Deauth attack: [Yes/No]

### 3.3 Zigbee / Z-Wave (if applicable)
- Network key extracted: [Yes/No]  —  Unencrypted commands: [Yes/No]
- OTA unauthenticated: [Yes/No]  —  Permit-join persistent: [Yes/No]

### 3.4 Network Services
| Port | Protocol | Service | Vulnerabilities |
|------|----------|---------|----------------|
| 22/tcp | SSH | Dropbear [ver] | Known CVE, default creds |
| 80/tcp | HTTP | lighttpd [ver] | Directory listing, XSS |
| 1883/tcp | MQTT | Mosquitto [ver] | Anonymous subscribe/publish |
| 554/tcp | RTSP | [service] | Unauthenticated stream |

### 3.5 MQTT Testing
- Anonymous connect: [Yes/No]  —  Subscribe `#` allowed: [Yes/No]
- Publish to command topics: [Yes/No]  —  TLS enforced: [Yes/No]

### 3.6 Fuzzing Results
- MQTT invalid CONNECT: [Crash / No response / Correct]
- CoAP large payload: [Crash / No response / Correct]
- HTTP CRLF injection: [Vulnerable / Not vulnerable]

---

## 4. Findings Summary

| ID | Finding | Severity | CVSS 3.1 | Status |
|----|---------|----------|----------|--------|
| FW-001 | Hardcoded root credentials | Critical | 9.8 | Unpatched |
| HW-001 | UART exposed, root shell no auth | Critical | 9.0 | Unpatched |
| NW-001 | MQTT anonymous subscribe | High | 7.5 | Unpatched |
| NW-002 | BLE Just Works pairing (MITM) | High | 6.5 | Unpatched |
| FW-002 | OpenSSL 1.0.2 known CVEs | High | 7.5 | Vendor notified |
| NW-003 | Telnet enabled on port 23 | High | 7.0 | Unpatched |

---

## 5. Remediation Roadmap

| Timeline | Actions |
|----------|--------|
| **Immediate (0-30d)** | Remove hardcoded creds; lock UART console; add MQTT auth; patch OpenSSL/BusyBox/Dropbear; disable telnet |
| **Short-term (30-90d)** | Blow JTAG fuses; implement secure boot + signed updates; BLE Secure Connections; TLS on all services |
| **Long-term (90d+)** | Hardware-backed secure element; firmware signing pipeline with revocation; bug bounty program; quarterly re-assessment |

---

## 6. Methodology & Artifacts

**Tools:** binwalk, unblob, firmwalker, Ghidra v11.1, Bus Pirate v3.6, Saleae logic analyzer, CH341A, bettercap, Wireshark, nRF Connect, aircrack-ng, hashcat (RTX 2060 SUPER ~500 KH/s WPA2), nmap, mqtt-malaria, scapy, checksec, pwntools, flashrom.

**Artifacts tarball:** `iot-assessment-artifacts-[date].tar.gz`
Contains: entropy.txt, binwalk-scan.txt, all-strings.txt, secrets-credentials.txt, private-keys.txt, cve-hints.txt, firmwalker.txt, ble-sniff.pcapng, mqtt.log, uart-console.log, flash-dump.bin, jtag-scan.txt, extracted-filetypes.txt, config-files.txt.

---

**End of Report**
```

## Anti-Rationalization Table

| Rationalization | Reality |
|----------------|---------|
| "IoT devices are cheap, not worth testing" | A $35 smart camera on your office network is a pivot point to the entire corporate LAN. Device cost is irrelevant — network access is priceless to an attacker. |
| "No one would hack my lightbulb" | IoT botnets (Mirai, 60+ variants) are built entirely from compromised lightbulbs, cameras, and routers. Your lightbulb is a node in someone's DDoS army. |
| "Firmware is just embedded software — no one finds bugs" | Real examples: hardcoded RSA keys in home routers, empty root passwords on medical infusion pumps, telnet backdoors in baby monitors. Every firmware dump reveals something. |
| "Physical access is required so it's not a real threat" | Attackers buy the same device off Amazon, dump firmware in their lab, build exploits, then weaponize them. A single exploited device sells for $500-$5000 on exploit markets. |
| "Our device uses encryption so it's secure" | Encryption at rest is useless when the key is stored in the same flash next to the encrypted data — which is exactly what most IoT devices do. |
| "Secure boot makes firmware attacks impossible" | Secure boot only checks the boot chain at startup. It doesn't protect against runtime exploits, side-channel key extraction, or flash desoldering. |
| "It's just a prototype, we'll harden it for production" | Production firmware is almost always the prototype with minimum changes. Hardcoded debug creds and open UARTs persist to retail units in 80% of assessments. |
| "Our cloud API validates everything — the device itself doesn't matter" | A compromised device sends fabricated sensor data and ignores cloud commands. The device validates firmware, controls actuators, and stores local state — cloud is not a substitute. |

## Workflow / Process

### Phase 1: Reconnaissance & Information Gathering

1. **Device teardown** — Remove casing, photograph PCB, identify ICs and pinouts (datasheet lookup)
2. **Identify debug interfaces** — Probe PCB for UART (TX/RX/GND), JTAG (TCK/TMS/TDI/TDO), SWD (SWDIO/SWCLK), SPI flash pads
3. **Determine flash type** — Serial NOR/NAND, SPI, eMMC, or raw NAND; identify chip markings
4. **Network discovery** — Connect device to isolated network, nmap for open ports and services
5. **Wireless discovery** — Scan BLE advertisements, Zigbee channels, Wi-Fi AP/station modes
6. **Firmware acquisition** — Download from manufacturer, capture OTA update, dump from SPI/JTAG, or MITM mobile companion app
7. **Firmware enumeration** — binwalk signature scan, entropy analysis, filesystem extraction

### Phase 2: Firmware Reverse Engineering

1. **Filesystem extraction** — Unpack SquashFS, JFFS2, UBIFS, CramFS, initramfs, or proprietary formats
2. **Credential hunting** — Search for hardcoded passwords, API keys, tokens, certificates, pre-shared keys
3. **Vulnerability scanning** — Version-check all bundled libraries (OpenSSL, Dropbear, BusyBox, curl) against CVE databases
4. **Binary analysis** — Load ELF/ARM/MIPS/RISC-V binaries into Ghidra; check for insecure sprintf, system(), exec()
5. **Backdoor detection** — Look for hidden telnetd, debug endpoints, vendor backdoors, hardcoded upgrade URLs
6. **Firmware signing check** — Validate firmware update signature scheme and public key storage location

### Phase 3: Hardware Interfacing

1. **UART console access** — Connect USB-UART adapter at 115200/57600/9600 baud; sweep common rates; try default creds; interrupt U-Boot for recovery shell
2. **JTAG/SWD probing** — Scan JTAG chain with bus pirate or J-Link; if IDCODE readable, attempt boundary scan, flash read, register dump
3. **SPI flash dumping** — Attach SOP8/SOIC8 clip to CH341A; dump flash (verify with second read); analyze partition layout
4. **Side-channel opportunities** — Power analysis for timing attacks; EMF probing for key extraction (advanced)
5. **Voltage/clock glitching** — Fault injection on secure boot (requires oscilloscope + pulse generator — advanced)
6. **RTC/NVRAM inspection** — Read battery-backed memory for stored credentials, session tokens, pairing data

### Phase 4: Wireless & Protocol Testing

1. **BLE** — Enumerate GATT services/characteristics with bettercap/nRF Connect; test read/write without auth; observe pairing for MITM; capture packets for offline analysis
2. **Wi-Fi** — WPA2 handshake capture with airodump-ng + PSK cracking on RTX 2060 SUPER (~500 KH/s); WPS Pixie Dust; deauth to force reconnect
3. **Zigbee/Z-Wave** — Capture network key during pairing; replay commands; scan for open permit-join windows
4. **MQTT/CoAP** — Subscribe to topics without auth; publish to command topics; fuzz payload fields; check TLS enforcement
5. **HTTP/HTTPS** — Fuzz web interface; test LFI/RFI, command injection, CSRF, session hijacking, default creds
6. **Mobile app API** — Intercept companion app with Burp Suite; test pairing APIs, device ID enumeration

### Phase 5: Exploitation & Reporting

1. **Develop PoC** — Write exploits (Python+scapy for network, Bash for UART, Python for MQTT, C for local priv esc)
2. **Document CVSS** — Score each finding using CVSS 3.1 with attack vector, complexity, privileges, scope
3. **Generate report** — Compile executive summary, technical findings, remediation roadmap, artifacts archive
4. **Remediation retest** — After vendor patch window, retest to confirm fixes (Pro tier)

## Tools

- **Firmware extraction & analysis:** binwalk, unblob, firmware-mod-kit, JeFF (JFFS2 extractor), ubi_reader
- **Binary analysis:** Ghidra, radare2, objdump, readelf, checksec (pwntools)
- **Strings & pattern matching:** strings, grep/ripgrep, firmwalker, binblade
- **Hardware probing:** Bus Pirate v3.6, Segger J-Link, Saleae logic analyzer, CH341A SPI programmer, USB-serial (CP2102/FT232)
- **Wireless/BLE:** bettercap, bluepy, nRF Connect, gatttool, Wireshark, Ubertooth One
- **Wi-Fi:** aircrack-ng suite, hashcat (RTX 2060 SUPER), hcxdumptool, Wifite
- **Zigbee:** zigbee2mqtt, Killerbee, TI CC2531 sniffer, Z-Fuzz
- **Protocol testing:** mqtt-malaria, mqtt-pwn, scapy, Burp Suite Community Edition
- **Flash analysis:** flashrom, esptool (ESP chips), nanddump
- **Password cracking:** hashcat (GPU on RTX 2060 SUPER), John the Ripper
- **Python libs:** scapy, bluepy, pyserial, intelhex, pyelftools

### Environment Setup

```bash
# Core tools
sudo apt install -y binwalk firmware-mod-kit python3-pip radare2 nmap wireshark aircrack-ng hashcat bluez
pip3 install unblob cstruct pyserial bluepy scapy paho-mqtt mqtt-malaria intelhex
# Ghidra: download from ghidra-sre.org — the NSA decompiler, essential for binary RE
```

## Verification

- [ ] Firmware extracted to filesystem (verified with `file` / `ls`)
- [ ] Credentials and secrets catalogued (hardcoded, default, embedded)
- [ ] Known vulnerable library versions cross-referenced with CVE database
- [ ] UART console accessed (or reason documented why not possible)
- [ ] Wireless protocols captured and analyzed (BLE, Wi-Fi, Zigbee)
- [ ] Open network ports enumerated and service versions identified
- [ ] Each finding has confirmed PoC (not theoretical)
- [ ] CVSS 3.1 base score calculated for every vulnerability
- [ ] Selected high-severity findings reproduced on a second unit (if available)
- [ ] Remediation recommendations include short-term and long-term options
- [ ] Report generated with executive summary and technical detail
- [ ] Artifacts packaged for client delivery (tarball with reports and captures)
