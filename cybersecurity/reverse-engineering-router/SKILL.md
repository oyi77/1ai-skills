---
name: reverse-engineering-router
description: Use when starting any reverse engineering task — master router that classifies the target artifact and routes to the correct specialized RE skill (native binaries, Android, iOS, JavaScript, firmware, .NET, malware behavior, forensics).
domain: cybersecurity
category: cybersecurity
version: 1.0.0
author: oyi77
license: Apache-2.0
subdomain: reverse-engineering
tags:
  - reverse-engineering
  - binary-analysis
  - malware-analysis
  - firmware-analysis
  - mobile-security
  - router
depends_on:
  - cybersecurity-router
triggers:
  - "reverse engineer"
  - "analyze binary"
  - "decompile"
  - "disassemble"
  - "reverse engineering"
  - "unpack firmware"
  - "analyze apk"
  - "analyze malware"
  - "firmware extraction"
  - "binary analysis"
---

# Reverse Engineering Router: Master Entry for RE Operations

Determines the artifact type, selects the correct specialized reverse engineering skill, and enforces methodology before tooling. All 48 RE skills in the catalog are reachable through this router.

## Overview

reverse-engineering-router is the master entry for reverse engineering work: it classifies the target artifact (file format, architecture, platform), routes to the correct specialized skill, and ensures structured methodology over random tool usage. It maps 48 reverse-engineering skills into a deterministic decision tree.

## When NOT to Use

- Authorized testing already scoped to a single deep technique — load the specialized skill directly (e.g., known Android malware: load `reverse-engineering-android-malware-with-jadx`)
- Source code analysis — use static analysis tools instead (Semgrep, CodeQL)
- No artifact available (requirements-only tasks)

## Verification

- Feed the router a scenario for each artifact class (native binary, Android APK, iOS app, JavaScript bundle, firmware image, .NET assembly, packed binary, malware sample) and confirm it routes to the correct specialist skill each time.
- Verify fallback to `reverse-engineer-anything-with-rea` for unknown/ambiguous artifacts

## Anti-Rationalization Table

| Excuse | Reality | Rule |
|---|---|---|
| "I'll just open it in Ghidra" | Without identifying the format first, you'll waste hours on wrong architecture or wrong tool | Route by artifact signature first |
| "The decompiler will figure it out" | A PE binary opened as ELF produces garbage; wrong platform = wrong results | Verify file type before tool selection |
| "I'll try all tools" | Trial-and-error is not a methodology; it produces incomplete coverage | Use the routing table below |

---

## Routing Decision Table

The routing table is a lookup, not judgment-by-hand. Model it as data so the same decision is repeatable.

```python
ROUTING_TABLE = [
    # (matchers, primary_skill, fallback_skill)
    ({"ext": [".apk", ".dex", ".aab", ".smali"], "magic": ["PK\\x03\\x04"]},
     "reverse-engineering-android-malware-with-jadx",
     "analyzing-android-malware-with-apktool"),
    ({"ext": [".ipa", ".app"], "magic": ["Mach-O"]},
     "reverse-engineering-ios-app-with-frida",
     "analyzing-ios-app-security-with-objection"),
    ({"ext": [".exe", ".dll", ".sys"], "magic": ["MZ"]},
     "binary-breaker",
     "reverse-engineering-malware-with-ghidra"),
    ({"ext": [".so", ".bin", ".elf"], "magic": ["\\x7fELF"]},
     "analyzing-linux-elf-malware",
     "reverse-engineering-malware-with-ghidra"),
    ({"ext": [".js", ".mjs", ".ts", ".wasm"], "magic": []},
     "js-reverse",
     "dsl-vm-reverse"),
    ({"ext": [".bin", ".img", ".hex"], "magic": ["U-Boot", "squashfs", "cramfs", "jffs2"]},
     "performing-firmware-extraction-with-binwalk",
     "performing-firmware-malware-analysis"),
    ({"ext": [".exe", ".dll"], "magic": ["MZ"], "dotnet": True},
     "reverse-engineering-dotnet-malware-with-dnspy",
     "reverse-engineering-malware-with-ghidra"),
    ({"keywords": ["packed", "upx", "obfuscated", "stripped"]},
     "analyzing-packed-malware-with-upx-unpacker",
     "reverse-engineering-malware-with-ghidra"),
    ({"keywords": ["cobalt strike", "beacon", "c2"]},
     "analyzing-cobalt-strike-beacon-configuration",
     "reverse-engineering-malware-with-ghidra"),
    ({"keywords": ["agent tesla", "rat config"]},
     "extracting-config-from-agent-tesla-rat",
     "reverse-engineering-malware-with-ghidra"),
    ({"keywords": ["ransomware", "encryption routine"]},
     "reverse-engineering-ransomware-encryption-routine",
     "analyzing-ransomware-encryption-mechanisms"),
    ({"keywords": ["sandbox evasion", "anti-vm", "anti-debug"]},
     "analyzing-malware-sandbox-evasion-techniques",
     "performing-automated-malware-analysis-with-cape"),
    ({"keywords": ["yara", "ioc extraction", "malware triage"]},
     "performing-malware-triage-with-yara",
     "performing-malware-ioc-extraction"),
    ({"keywords": ["network traffic", "pcap", "covert channel"]},
     "analyzing-network-traffic-of-malware",
     "analyzing-network-covert-channels-in-malware"),
    ({"keywords": ["memory dump", "volatility", "forensics"]},
     "performing-memory-forensics-with-volatility3-plugins",
     "analyzing-disk-image-with-autopsy"),
    ({"keywords": ["go binary", "golang", "pclntab"]},
     "go-rust-reverse",
     "analyzing-golang-malware-with-ghidra"),
    ({"keywords": ["rust binary", "panic strings"]},
     "reverse-engineering-rust-malware",
     "go-rust-reverse"),
    ({"keywords": ["browser extension", "crx", "xpi"]},
     "browser-extension-reverse",
     "js-reverse"),
    ({"keywords": ["powershell", "obfuscated"]},
     "deobfuscating-powershell-obfuscated-malware",
     "deobfuscating-javascript-malware"),
    ({"keywords": ["plc", "s7comm", "ot", "ics"]},
     "performing-plc-firmware-security-analysis",
     "performing-firmware-malware-analysis"),
    ({"ext": [".pdf"], "keywords": ["peepdf", "malicious pdf", "stream"]},
     "analyzing-malicious-pdf-with-peepdf",
     "reverse-engineer-anything-with-rea"),
    ({"keywords": ["heap spray", "heap exploitation"]},
     "analyzing-heap-spray-exploitation",
     "performing-binary-exploitation-analysis"),
    ({"keywords": ["rootkit", "kernel module", "lkm", "vmlinux"]},
     "analyzing-linux-kernel-rootkits",
     "analyzing-linux-elf-malware"),
    ({"keywords": ["fuzzing", "afl", "harness", "crash triage"]},
     "performing-fuzzing-with-aflplusplus",
     "binary-breaker"),
    ({"keywords": ["persistence", "autoruns", "registry run"]},
     "analyzing-malware-persistence-with-autoruns",
     "performing-static-malware-analysis-with-pe-studio"),
    ({"keywords": ["supply chain", "malicious package", "typosquatting"]},
     "analyzing-supply-chain-malware-artifacts",
     "reverse-engineer-anything-with-rea"),
    ({"keywords": ["malware pipeline", "automated submission"]},
     "building-automated-malware-submission-pipeline",
     "performing-automated-malware-analysis-with-cape"),
    ({"keywords": ["virustotal", "hash enrichment", "reputation"]},
     "performing-malware-hash-enrichment-with-virustotal",
     "performing-malware-ioc-extraction"),
    ({"keywords": ["iot", "embedded device", "uart", "jtag"]},
     "performing-iot-security-assessment",
     "performing-firmware-extraction-with-binwalk"),
    ({"keywords": ["thick client", "fat client", "wpf", "electron"]},
     "performing-thick-client-application-penetration-test",
     "reverse-engineering-dotnet-malware-with-dnspy"),
    ({"keywords": ["prefetch", "windows execution artifact", "shimcache"]},
     "analyzing-windows-prefetch-with-python",
     "analyzing-malware-persistence-with-autoruns"),
]

def route(artifact_info: dict) -> tuple[str, str]:
    """Return (primary_skill, fallback_skill) or (None, 'reverse-engineer-anything-with-rea')"""
    for matchers, primary, fallback in ROUTING_TABLE:
        if all(artifact_info.get(k) in v for k, v in matchers.items() if k != "keywords"):
            if "keywords" not in matchers or any(kw in artifact_info.get("text", "").lower() for kw in matchers["keywords"]):
                return primary, fallback
    return None, "reverse-engineer-anything-with-rea"
```

---

## When to Use

**Use when:**

- Starting a new reverse engineering task with an artifact (binary, APK, firmware, etc.)
- You have a file but don't know which specialized RE skill applies
- You need a structured methodology before diving into tools
- The task involves multiple RE domains and you need coordination

**Don't use for:**

- Unauthorized reverse engineering (only authorized targets, bug bounty programs, defensive validation)
- Pure source code review tasks
- When you already know the exact skill needed

---

## Workflow

1. **Classify Artifact** — Identify file type via extension, magic bytes, and keywords from user prompt
2. **Route** — Look up in routing table above; if ambiguous or no match, route to `reverse-engineer-anything-with-rea`
3. **Execute** — Invoke the primary skill with artifact context; if primary fails or is unavailable, use fallback
4. **Iterate** — If deeper analysis needed, the primary skill can invoke sub-skills per its own workflow

---

## Skill Map (48 Skills)

### Native Binary Analysis (ELF / PE / Mach-O)
- `binary-breaker` — Binary exploitation & RE for zero-days
- `reverse-engineering-malware-with-ghidra` — Ghidra-based malware RE
- `analyzing-linux-elf-malware` — Linux ELF malware (botnets, cryptominers, rootkits)
- `analyzing-golang-malware-with-ghidra` — Go malware with Ghidra
- `go-rust-reverse` — Go/Rust binary RE (pclntab, symbol recovery)
- `reverse-engineering-rust-malware` — Rust malware RE
- `analyzing-packed-malware-with-upx-unpacker` — UPX/packed binary unpacking
- `performing-static-malware-analysis-with-pe-studio` — PE static analysis
- `performing-binary-exploitation-analysis` — Binary exploitation analysis

### .NET / Managed Code
- `reverse-engineering-dotnet-malware-with-dnspy` — .NET malware with dnSpy

### Android / Mobile
- `reverse-engineering-android-malware-with-jadx` — Android malware with JADX
- `analyzing-android-malware-with-apktool` — Android malware with Apktool
- `performing-android-app-static-analysis-with-mobsf` — MobSF static analysis
- `performing-dynamic-analysis-of-android-app` — Frida/Objection dynamic analysis
- `testing-android-intents-for-vulnerabilities` — Android IPC intent testing
- `detecting-mobile-malware-behavior` — Mobile malware behavior detection

### iOS / macOS
- `reverse-engineering-ios-app-with-frida` — iOS app with Frida
- `analyzing-ios-app-security-with-objection` — iOS with Objection

### JavaScript / Web / WASM
- `js-reverse` — Frontend JavaScript RE (signing, anti-bot)
- `dsl-vm-reverse` — Custom DSL/VM reverse engineering
- `browser-extension-reverse` — Browser extension RE
- `deobfuscating-javascript-malware` — JS malware deobfuscation
- `deobfuscating-powershell-obfuscated-malware` — PowerShell deobfuscation

### PDF / Document Malware
- `analyzing-malicious-pdf-with-peepdf` — PDF malware with peepdf

### Exploitation & Kernel Analysis
- `analyzing-heap-spray-exploitation` — Heap spray exploitation
- `analyzing-linux-kernel-rootkits` — Linux kernel rootkit analysis
- `performing-fuzzing-with-aflplusplus` — AFL++ fuzzing for zero-days

### Malware Enrichment & Supply Chain
- `analyzing-malware-persistence-with-autoruns` — Autoruns persistence analysis
- `analyzing-supply-chain-malware-artifacts` — Supply chain malware artifacts
- `building-automated-malware-submission-pipeline` — Automated submission pipeline

### Host Artifact Analysis
- `analyzing-windows-prefetch-with-python` — Windows Prefetch execution artifacts

### IoT / Thick Client
- `performing-iot-security-assessment` — IoT device RE and security assessment
- `performing-thick-client-application-penetration-test` — Thick client RE

### Firmware / Embedded / OT
- `performing-firmware-extraction-with-binwalk` — Firmware extraction with Binwalk
- `performing-firmware-malware-analysis` — Firmware malware analysis
- `performing-plc-firmware-security-analysis` — PLC/OT firmware security

### Malware Behavior & Configuration
- `performing-automated-malware-analysis-with-cape` — CAPE sandbox analysis
- `analyzing-cobalt-strike-beacon-configuration` — Cobalt Strike beacon config
- `extracting-config-from-agent-tesla-rat` — Agent Tesla RAT config
- `reverse-engineering-ransomware-encryption-routine` — Ransomware encryption RE
- `analyzing-ransomware-encryption-mechanisms` — Ransomware encryption analysis
- `analyzing-malware-sandbox-evasion-techniques` — Sandbox evasion analysis
- `analyzing-network-covert-channels-in-malware` — Covert channel analysis
- `performing-malware-ioc-extraction` — IOC extraction
- `performing-malware-triage-with-yara` — YARA-based triage

### Network & Forensics
- `analyzing-network-traffic-of-malware` — Network traffic analysis
- `performing-memory-forensics-with-volatility3-plugins` — Memory forensics

### Unified Artifact Evidence (REA Integration)
- `reverse-engineer-anything-with-rea` — REA MCP/CLI artifact evidence workflow

---

## Core Skill References

All skills above exist in `cybersecurity/` category and are registered in `SKILLS.json`.

### Deliberately Out of Scope

These RE-adjacent skills are reachable through `cybersecurity-router` but are **response/defense** workflows, not reverse engineering. This router does not claim them:

- `conducting-malware-incident-response` — incident response lifecycle, not artifact analysis
- `implementing-ransomware-kill-switch-detection` — defensive detection control
- `investigating-ransomware-attack-artifacts` — forensic investigation, not RE

---

## Operating Model

### Phase 1: Artifact Identification (Always First)

Collect before analysis:
- File extension and magic bytes (`file`, `xxd`, `binwalk`)
- Architecture (`file`, `readelf -h`, `objdump -f`)
- Platform hints from user prompt (keywords, context)
- Packing/obfuscation detection (entropy, `upx -l`, `peid`)

### Phase 2: Route by Artifact Class

Use the routing table above. Exact match wins; keyword match is secondary.

### Phase 3: Execute Specialized Skill

Invoke the primary skill. If primary fails (tool unavailable, unsupported format), use fallback.

### Phase 4: Deepen or Iterate

The specialized skill handles its own deepening. If new artifacts discovered, re-enter Phase 1.

---

## High-Value Expert Intuitions

1. **Magic bytes never lie** — extension can be wrong; always verify with `file` and hex dump
2. **Packing is the norm, not exception** — assume packed; unpacking first saves hours
3. **Platform dictates toolchain** — Android ≠ iOS ≠ Linux ≠ Windows ≠ firmware
4. **Fallback is a feature** — `reverse-engineer-anything-with-rea` prevents dead ends for unknown artifacts
5. **REA for evidence preservation** — when behavior must be cited, use `reverse-engineer-anything-with-rea` for evidence IDs and snapshots

---

## Suggested Prompts

- "Route this reverse engineering task: I have a suspicious ELF binary"
- "I need to analyze an APK for malware — which skill?"
- "Route this: firmware image from IoT device, need extraction and analysis"
- "Classify this binary and tell me the right RE skill"

---

## Verification Checklist

- [ ] Artifact type identified via magic bytes before tool selection
- [ ] Routing table lookup returns a primary skill for the artifact
- [ ] Fallback skill specified for every primary
- [ ] Primary skill exists in SKILLS.json and passes lint
- [ ] All 39 mapped skills are current catalog entries

---

## References

- **Cybersecurity parent router**: `cybersecurity-router` (routes to this skill for Binary/ELF/PE cases)
- **REA integration**: `reverse-engineer-anything-with-rea` (artifact evidence backend)
- **All skills**: 39 skills in `cybersecurity/` category with `reverse-engineering` tag
- **Schema**: `depends_on` links children → this router; `triggers` define activation phrases