---
name: red-team-resource-development-and-evasion
description: Use when engineering evasion payloads, obfuscating scripts, bypassing EDR hooks, and crafting weaponized delivery documents using Freeze, ScareCrow, Invoke-Obfuscation, Alcatraz, and SharpBlock during authorized red team engagements.
domain: cybersecurity
subdomain: penetration-testing
category: cybersecurity
version: 1.0.0
author: oyi77
license: Apache-2.0
tags:
- red-team
- payload
- evasion
- resource-development
- obfuscation
triggers:
- resource development
- defense evasion
- payload creation
- PowerShell obfuscation
- obfuscator
- msfvenom
- SharpBlock
---

# Red Team Resource Development and Evasion

## Process
1. Scope by threat model.
2. Select tool category index.
3. Validate prerequisites.
4. Execute operational guidance.
5. Verify with checklist.

## Overview

Cybersecurity playbook covering payload generation, source and binary obfuscation, AMSI bypass tradecraft, and endpoint detection and response (EDR) hooking evasion. Designed for technical adversarial emulation within authorized red team engagements.

## When to Use

**Trigger phrases:**
- "engineer evasive red team payload"
- "obfuscate powershell using invoke-obfuscation"
- "bypass edr hooks with freeze or scarecrow"
- "evade amsi and etw inspection"
- "craft delivery document using remoteinjector"

- Engineering custom binary and shellcode loaders designed to bypass static and heuristic detections
- Obfuscating PowerShell, VBScript, and HTA scripts to prevent signature-based execution prevention
- Circumventing API unhooking and userland monitoring implemented by modern enterprise EDRs
- Testing defensive monitoring capabilities against sophisticated Living-off-the-Land (LotL) and template injection tradecraft

## When NOT to Use

- When operating on production systems without explicit authorization for evasive execution
- When analyzing malware samples defensively (use `cybersecurity/role-security-engineer`)
- When deploying untracked payloads that lack embedded shutdown mechanisms or kill-switches

## Prerequisites

- Isolated development laboratory with Windows 10/11 and Linux analysis VMs
- Compilers: Go, GCC/MinGW, Rust, and .NET Developer SDKs
- Testing environment equipped with target EDR agent in audit/monitor mode

## Payload Generation & EDR Evasion

### Freeze Loader
Payload generation tool designed to bypass EDR by:
- Utilizing direct system calls to bypass userland API hooks (e.g., `NtCreateThreadEx`, `NtAllocateVirtualMemory`)
- Encrypting shellcode payloads and executing them via suspended process injection or thread hijacking
- Evading memory scanning by masking payload memory regions during sleep cycles

### ScareCrow
Framework creating payload loaders designed to bypass EDR and Application Control:
- Uses signed Microsoft binaries or sideloading techniques
- Decrypts and executes payloads via custom assembly execution stubs
- Strips suspicious metadata and applies spoofed digital certificates

### SharpBlock
C# tool that executes binaries while blocking userland DLLs injected by EDR vendors:
- Prevents EDR monitoring hooks from being installed in child processes
- Hooks APIs like `LdrLoadDll` within the spawned process to block defensive DLL loading

## Script & Binary Obfuscation

### Invoke-Obfuscation
PowerShell obfuscation framework:
- Applies token-level, AST-level, and encoding-level transformations
- Bypasses string-matching signatures while maintaining functional script parity

### Alcatraz & Mangle
- **Alcatraz:** Binary obfuscator that modifies x64 PE control flow, inserts junk instructions, and encrypts functions.
- **Mangle:** Manipulates compiled executable attributes, string tables, and imports to evade heuristic and static AV signatures.

## Anti-Rationalization Table

| Excuse | Flawed Rationalization | Required Discipline |
|---|---|---|
| "Obfuscated payloads are undetectable" | "Obfuscation hides everything." | Heavy obfuscation increases entropy, which triggers behavioral and heuristic rules; test in a replica lab first. |
| "Bypass AMSI by patching memory directly" | "Direct patching always works." | Memory patching of AMSI triggers memory integrity and ETW alerts in modern OS builds; use unhooked syscalls or alternative runtimes. |
| "Any working payload is good to deliver" | "If it executes, deliver it." | Payloads without kill-dates risk lingering in client environments; always embed hard expiration dates and cleanup logic. |

## Verification Checklist

- [ ] All payloads compiled and tested in an isolated testing lab
- [ ] Direct syscall stubs verified against target operating system build
- [ ] Memory-evasion techniques (sleep masking, unhooking) confirmed functional
- [ ] Hardcoded expiration date (kill-switch) confirmed active in compiled binary
- [ ] Payload hash and compilation metadata logged for the final engagement report
