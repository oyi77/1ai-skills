---
name: binary-breaker
description: Binary exploitation and reverse engineering for finding zero-days in compiled software. Use when analyzing binaries,
  finding memory corruption bugs, reverse engineering firmware, or hunting bugs in C/C++ applications.
domain: cybersecurity
tags:
- binary
- breaker
- cybersecurity
- security
- exploit
- reverse-engineering
- zero-day
- money
---
# Binary Breaker

## Overview

Binary Breaker covers the full lifecycle of binary exploitation and reverse engineering — from static analysis of PE/ELF/Mach-O binaries through dynamic debugging, fuzzing, and exploit development. You analyze compiled software (C/C++/Rust/Go binaries) to find memory corruption vulnerabilities, reverse engineer proprietary formats and protocols, and deliver working proof-of-concept exploits with CVSS-scored findings.

The RTX 2060 SUPER GPU accelerates fuzzing workloads via AFL++ dictionary generation, parallel crash triage, and hashcat-assisted reverse engineering of obfuscated strings. The Kali Linux toolchain — Ghidra headless, pwntools, GDB, radare2, and QEMU — handles every target architecture from x86-64 to ARM/MIPS firmware.

## When to Use

**Trigger phrases:**
- "Analyze this binary for vulnerabilities"
- "Reverse engineer this malware/firmware"
- "Exploit this buffer overflow / use-after-free / format string"
- "Hunt zero-days in closed-source application XYZ"
- "CTF pwn challenge — need a walkthrough or exploit"
- "What does this obfuscated function do?"
- "Crack this license validation / serial check"

**Concrete scenarios:**
- A client's proprietary Windows application crashes on malformed input — find the root cause and assess exploitability
- A CVE report mentions a use-after-free in a popular library version — develop a PoC to verify the fix
- Malware sample uses custom packing — unpack and extract the C2 configuration
- CTF team needs an exploit chain for a heap exploitation challenge
- Firmware update binary contains encrypted strings — identify the crypto routine and recover keys

## When NOT to Use

- When you lack authorized access to test the target binary (no reverse engineering without permission)
- When source code is available and static analysis SAST tools are faster (use Semgrep/CodeQL instead)
- When the bug is already documented with a public CVE — you are validating, not hunting
- When legal or export-control restrictions apply (crypto exports, defense contracts)
- When the binary is trivially decompilable via managed code (C#/.NET — use dnSpy instead)
- When the task is purely about detecting known malware IOCs — use YARA/signatures instead

## Money-Making Overview

**Target Buyer:** Security engineering teams, proprietary software vendors, ICS/OT firmware developers, CTF competition teams, malware analysis firms, bug bounty programs.

**How You Make Money:**
1. **Binary Vulnerability Assessment** — Analyze a closed-source binary for exploitable memory corruption bugs, deliver CVSS-scored findings with PoC. Vendors pay $2K-10K per engagement to harden products before release.
2. **Exploit Development** — Write reliable weaponized exploits for verified vulnerabilities. Bug bounty programs, zero-day brokers, and red teams pay $5K-50K+ per working exploit.
3. **Reverse Engineering as a Service** — Malware analysis, protocol reverse engineering, license algorithm extraction, firmware teardown. Security teams outsource RE at $150-300/hour.

### Service Tiers
| Tier | Price | What They Get |
|------|-------|---------------|
| **Basic** — Binary Triage | $500-1,000 | Automated analysis report: Ghidra headless function listing, strings analysis, dangerous imports (strcpy, gets, sprintf), heuristic CVSS scoring, attack surface summary. 24h turnaround. |
| **Pro** — Vulnerability Assessment | $2,500-5,000 | Full manual RE: decompilation walkthrough, identified memory corruption bugs (buffer overflows, use-after-free, format strings), working PoC exploit per finding, CVSS 3.1 with environmental vectors, remediation guidance, 30-page technical report. 2 rounds of Q&A. |
| **Enterprise** — Zero-Day Retainer | $8,000-15,000/month | Ongoing binary auditing: prioritized bug hunting in critical modules, AFL++/libFuzzer harnesses, exploitability assessment, disclosure-ready advisory drafts, dedicated Slack/Telegram support, 48-hour turnaround on critical findings. |

**Expected First Dollar:** 2-4 weeks (triage of a closed-source Windows app for known dangerous patterns, deliver initial $500-1,000 report).

## First Action in 60 Minutes

Save as `~/tools/binary-triage.py` on Kali Linux. It runs an ELF/PE binary analysis pipeline using Ghidra headless + pwntools + binutils, outputting a structured vulnerability triage report.

```bash
#!/usr/bin/env python3
"""binary-triage.py — ELF/PE binary analysis pipeline. Outputs MD report + CSV + decomp stub."""
import sys, os, subprocess, hashlib, struct, re, json
from pathlib import Path
from datetime import datetime

GHIDRA_HOME = os.environ.get("GHIDRA_HOME", "/opt/ghidra")
PROJECT_DIR = "/tmp/ghidra_projects"
MIN_STR = 6

DANGEROUS = {
    "strcpy": "Buffer overflow — unbounded copy",
    "strcat": "Buffer overflow — unbounded concat",
    "sprintf": "Buffer overflow — unbounded format",
    "gets": "Buffer overflow — unbounded stdin (CWE-20)",
    "scanf": "Format string / overflow if %s used",
    "system": "Command injection via arg control",
    "memcpy": "Overflow if len > dst buffer",
    "free": "Double-free / use-after-free",
    "alloca": "Stack overflow on ctrl size",
}
DANGEROUS_WIN = {
    "lstrcpy": "Buffer overflow (Windows)", "lstrcat": "Buffer overflow (Windows)",
    "wsprintfA": "Buffer overflow (Windows)", "ReadFile": "Overflow if nBytes > buf size",
}

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(65536), b""): h.update(c)
    return h.hexdigest()

def file_type(path):
    with open(path, "rb") as f:
        m = f.read(4)
    if m[:4] == b"\x7fELF": return "elf"
    if m[:2] == b"MZ": return "pe"
    return "raw"

def is_64bit(path):
    with open(path, "rb") as f:
        m = f.read(4)
    if m[:4] == b"\x7fELF":
        f.seek(4); return f.read(1) == b"\x02"
    if m[:2] == b"MZ":
        f.seek(0x3C); e_lfanew = struct.unpack("<I", f.read(4))[0]
        f.seek(e_lfanew + 4); return struct.unpack("<H", f.read(2))[0] == 0x8664
    return False

def ghidra_decompile(target_path, output_dir):
    n = Path(target_path).stem
    sp = os.path.join(PROJECT_DIR, f"{n}_project")
    os.makedirs(PROJECT_DIR, exist_ok=True); os.makedirs(output_dir, exist_ok=True)
    script = os.path.join(GHIDRA_HOME, "support", "analyzeHeadless")
    if not os.path.exists(script): print("[!] Ghidra not found, skipping."); return None
    gs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_ghidra_export.py")
    if not os.path.exists(gs):
        with open(gs, "w") as f:
            f.write("""from ghidra.app.decompiler import DecompInterface
import csv, os
ifc = DecompInterface(); ifc.openProgram(currentProgram)
fm = currentProgram.getFunctionManager()
p = os.path.join(os.environ['OUTPUT_DIR'], os.environ['TARGET_NAME'] + '_functions.csv')
with open(p, 'w', newline='') as c:
    w = csv.writer(c); w.writerow(['Name','Address','BodySize','CC','HasBody'])
    for fn in fm.getFunctions(True):
        b = fn.getBody()
        w.writerow([fn.getName(), hex(fn.getEntryPoint().getOffset()), str(b.getNumAddresses()), fn.getCallingConventionName(), str(b is not None)])
print(f'[Ghidra] Exported to {p}')
""")
    env = os.environ.copy(); env["OUTPUT_DIR"] = output_dir; env["TARGET_NAME"] = n
    r = subprocess.run([script, PROJECT_DIR, n, "-process", target_path, "-noask",
        "-scriptPath", os.path.dirname(os.path.abspath(__file__)), "-postScript", "_ghidra_export.py"],
        capture_output=True, text=True, timeout=300, env=env)
    Path(os.path.join(output_dir, f"{n}_decompiled.c")).write_text(
        f"// Decompiled from {target_path} at {datetime.now().isoformat()}\n// Full decompilation in Ghidra GUI\n")
    return r

def readelf_analysis(path):
    r = {}
    try:
        for cmd, key in [(["readelf","-h",path],"header"), (["readelf","-S",path],"sects"),
            (["readelf","-s",path],"syms"), (["readelf","--dyn-syms",path],"dynsyms"),
            (["readelf","-r",path],"relocs"), (["readelf","-l",path],"phdrs")]:
            o = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            r[key] = o.stdout[:3000]
    except: print("[!] readelf failed")
    return r

def extract_strings(path):
    try:
        r = subprocess.run(["strings","-n",str(MIN_STR),path], capture_output=True, text=True, timeout=60)
        return r.stdout.splitlines()
    except:
        with open(path,"rb") as f: d = f.read()
        return [s.decode("latin-1") for s in re.findall(rb"[\x20-\x7e]{6,}", d)]

def check_mitigations(path, info):
    m = {"NX": "NO", "PIE": "NO", "RELRO": "NO", "Canary": "NO", "FORTIFY": "NO"}
    t = info.get("header","") + info.get("phdrs","")
    if "GNU_STACK" in t:
        m["NX"] = "NO (RWX)" if "RWE" in t else "YES"
    if "ET_DYN" in t: m["PIE"] = "YES"
    if "GNU_RELRO" in t:
        try:
            d = subprocess.run(["readelf","-d",path], capture_output=True, text=True, timeout=15).stdout
            m["RELRO"] = "FULL" if "BIND_NOW" in d else "PARTIAL"
        except: m["RELRO"] = "PARTIAL"
    if "__stack_chk_fail" in t: m["Canary"] = "YES"
    if any("_chk@" in s for s in info.get("dynsyms","").splitlines()): m["FORTIFY"] = "YES"
    return m

def main():
    target = sys.argv[1]
    assert os.path.exists(target), f"Not found: {target}"
    n = Path(target).stem; od = os.path.join(os.getcwd(), f"{n}_analysis")
    os.makedirs(od, exist_ok=True)
    t = file_type(target); arch64 = is_64bit(target)
    print(f"[+] {t.upper()} {arch64 and 'x86-64' or 'x86-32'} SHA256: {sha256_file(target)}")

    info = readelf_analysis(target) if t == "elf" else {}
    strings = extract_strings(target)
    mit = check_mitigations(target, info) if t == "elf" else {}
    interesting = [s for s in strings if any(k in s.lower() for k in
        ["http","key","secret","password","debug","error","license","flag","admin","connect"])]
    dangerous = []
    all_imports = "\n".join(str(v) for v in info.values()) if t == "elf" else ""
    for api,desc in {**DANGEROUS, **DANGEROUS_WIN}.items():
        if api in all_imports: dangerous.append({"api": api, "desc": desc})
    cvss = min(10.0, 5.0 + len(dangerous)*0.5 + sum(0.5 for k,v in mit.items() if "NO" in str(v)))

    ghidra_decompile(target, od)

    report = os.path.join(od, f"{n}_triage_report.md")
    with open(report, "w") as f:
        f.write(f"""# Binary Triage Report: {Path(target).name}

**Type:** {t.upper()} | **Arch:** {'x86-64' if arch64 else 'x86-32'}
**SHA256:** `{sha256_file(target)}` | **Date:** {datetime.now().isoformat()}

## Security Mitigations{' (ELF only)' if t != 'elf' else ''}
""")
        if mit:
            f.write("| Mitigation | Status |\n|---|---|\n")
            f.write("".join(f"| {k} | {v} |\n" for k,v in mit.items()))
        f.write(f"\n**Heuristic CVSS: {cvss}/10.0**\n\n## Dangerous Imports\n")
        if dangerous:
            f.write("| API | Risk |\n|---|---|\n")
            f.write("".join(f"| `{d['api']}` | {d['desc']} |\n" for d in dangerous))
        else: f.write("None detected via static heuristics.\n")
        f.write(f"\n## Interesting Strings ({len(strings)} total)\n")
        if interesting:
            f.write("".join(f"- `{s}`\n" for s in interesting[:40]))
            if len(interesting) > 40: f.write(f"- ... +{len(interesting)-40} more\n")
        f.write(f"""

## Exploit Scaffold
```python
from pwn import *
context.binary = ELF(r"{target}")
# Set OFFSET from cyclic_find() / TARGET_ADDR from gadget search
payload = cyclic(OFFSET) + p64(TARGET_ADDR)
io = process(context.binary.path)
io.sendline(payload); io.interactive()
```

## Artifacts
- Report: {report}
- Functions: {od}/{n}_functions.csv
- Decompiled: {od}/{n}_decompiled.c
- Strings: {len(strings)} extracted | Dangerous: {len(dangerous)} flagged | CVSS: {cvss}/10
""")
    print(f"[+] Report: {report}")

if __name__ == "__main__":
    main()
```

**Usage:**
```bash
python3 binary-triage.py /bin/ls          # Analyze ELF
python3 binary-triage.py app.exe           # Analyze PE (cross-analysis on Kali)
```

**Output:** `./app_analysis/app_triage_report.md` — structured report with mitigations, dangerous imports, interesting strings, pwntools scaffold, and analysis artifacts.

## Deliverable Format

You deliver a structured ZIP archive per engagement:

```
binary_assessment_<target>_<date>/
├── reports/
│   ├── <target>_vulnerability_report.pdf       ← Full report (30+ pages)
│   └── <target>_executive_summary.pdf          ← 2-page management summary
├── exploits/
│   ├── exploit_poc.py                          ← Working PoC (pwntools)
│   └── trigger_input.bin                       ← Minimal crash trigger
├── analysis/
│   ├── ghidra_project/                         ← Reproducible Ghidra project
│   ├── function_listing.csv                    ← All functions with addresses
│   └── strings_analysis.txt                    ← Filtered strings with context
├── cvss/
│   └── cvss_vectors.txt                        ← CVSS 3.1 vectors per finding
└── README.md                                   ← Reproduction instructions
```

### Finding Template (per vulnerability)
```
┌──────────────────────────────────────────────────────────────┐
│ Finding #1: Stack Buffer Overflow in parse_config()          │
├──────────────────────────────────────────────────────────────┤
│ CVE:      [Pending / Reserved]                               │
│ CVSS 3.1: 7.8 High — AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H   │
│ CWE:      CWE-121 (Stack-based Buffer Overflow)              │
│ Target:   parse_config() @ 0x401234 in config_parser section │
├──────────────────────────────────────────────────────────────┤
│ Description: parse_config() copies user input into a 256-byte│
│ stack buffer using strcpy() without length checking.         │
│ Attacker overwrites saved return address for arbitrary code  │
│ execution.                                                   │
├──────────────────────────────────────────────────────────────┤
│ Reproduction:                                                │
│   $ python3 exploits/exploit_poc.py                          │
│   → EIP/RIP control at offset 268 → shell with ROP chain     │
├──────────────────────────────────────────────────────────────┤
│ Remediation:                                                 │
│ • Replace strcpy() with strncpy() or snprintf()              │
│ • Enable -fstack-protector-strong for stack canary           │
│ • Enable Full RELRO + ASLR to reduce exploit reliability     │
├──────────────────────────────────────────────────────────────┤
│ Disclosure: Coordinated disclosure. Embargo: 90 days.        │
└──────────────────────────────────────────────────────────────┘
```

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I need assembler mastery first" | Ghidra's decompiler shows pseudo-C. Read that, trace variables, learn x86-64 one opcode at a time. The first PoC comes from pattern recognition, not reading the Intel manual cover-to-cover. |
| "RE is too time-consuming — I can't bill for it" | A 60-min automated triage produces a $500-1,000 report. Deep manual RE bills $150-300/hr. RE is the differentiator — most engineers can't do it, so you set the price. |
| "Closed-source binaries are black boxes" | Ghidra + pwntools + fuzzing makes closed-source auditing practical. Dangerous patterns like strcpy on attacker data are visible in decompiler output. Some of the highest CVE bounties come from closed-source software. |
| "Format string bugs don't exist in modern code" | They still appear in embedded firmware, legacy OT/ICS code, and IoT binaries. glibc's fortified printf is often disabled in embedded toolchains. |
| "ASLR + NX + RELRO make exploitation impossible" | Each mitigation has known bypasses: ret2libc/ROP for NX, partial RELRO → GOT overwrite, ASLR leaks via format strings, canary leaks via TLS. Missing any one layer makes exploitation viable. |
| "I need IDA Pro ($10K+) for real RE" | Ghidra (NSA, free) matches IDA Pro's decompiler for most targets. Pwntools + GDB+Pwndbg + QEMU handle the full pipeline. IDA Pro only matters for esoteric architectures or heavy obfuscation. |
| "Bug bounty programs don't accept binary findings" | Microsoft, Google, Adobe, VMWare, and hundreds of IoT vendors explicitly scope binary-level vulnerabilities. Average Chromium V8 bug pays $15,000+. |
| "Symbol stripping makes analysis impossible" | Stripped binaries lose function names but preserve code flow. Ghidra recovers boundaries, CFGs, and variable references. Label functions by behavior, not by name. |

## Workflow

```python
"""
PHASE 1: Recon (60 min)
  → run binary-triage.py: type, strings, imports, mitigations, heuristic CVSS

PHASE 2: Static Analysis (4-8 hr)
  → Ghidra decompilation walkthrough, trace input paths
  → Identify reachable dangerous functions, document call chains

PHASE 3: Dynamic Analysis (2-4 hr)
  → GDB + Pwndbg: set breakpoints at dangerous calls, trace data flow
  → Confirm crash reachable, capture register/stack state at crash

PHASE 4: Fuzzing (RTX 2060 SUPER accelerated)
  → AFL++ harness on parsing function, seed corpus from strings
  → Run parallel instances, triage crashes by fault type and offset

PHASE 5: Exploit Development (8-40 hr)
  → Pwntools: cyclic → offset → control flow hijack
  → ROP chain (ROPgadget/ropper), bypass ASLR/NX/RELRO/Canary
  → Iterate to reliable weaponized exploit

PHASE 6: Reporting (2-4 hr)
  → Write CVSS-scored finding per vulnerability
  → Package PoC, reproduction steps, remediation code
  → Submit deliverable ZIP archive
"""
```

## Process

1. **Triage** — Run automated pipeline: SHA-256, type detection, strings, imports, mitigations, heuristic CVSS.
2. **Deep RE** — Ghidra decompilation walkthrough, trace input-to-destination paths, identify reachable dangerous functions.
3. **Verify** — GDB tracing of input-to-crash path, confirm exploitability, document register/stack state at crash.
4. **Exploit** — Develop working PoC: offset calculation via cyclic pattern, ROP chain, mitigation bypass strategy.
5. **Package** — Write per-finding CVSS vectors, remediation guidance, reproduce instructions. ZIP the deliverable.

## Tools

- **Ghidra (headless + GUI)** — Primary decompiler for PE/ELF/Mach-O. Batch analysis via `analyzeHeadless`.
- **Pwntools** — Exploit framework: `cyclic()`/`cyclic_find()`, `ELF()`, `ROP()`, `p64()`/`p32()`, remote/local process I/O.
- **GDB + Pwndbg** — Dynamic debugging: breakpoints, register/stack inspection, crash context analysis.
- **ROPgadget / ropper** — Automated ROP gadget discovery from binary + loaded libraries.
- **AFL++** — Coverage-guided fuzzer; RTX 2060 SUPER handles display/compute loads, freeing CPU for sustained parallel fuzzing.
- **Radare2 / r2pipe** — Lightweight analysis for quick binary inspections.
- **binutils (objdump, readelf, strings)** — Standard structural analysis, symbols, string extraction.
- **QEMU user-mode** — Cross-architecture binary execution for ARM/MIPS firmware RE.

## Prerequisites

- Kali Linux (or Debian-based with security tools)
- Ghidra 11.x+ at `/opt/ghidra` (set `GHIDRA_HOME` if different)
- Python 3.9+ with `pwntools` (`pip install pwntools`)
- GDB with `pwndbg` (`apt install gdb`)
- AFL++ (`apt install afl++`)
- Written authorization to analyze target binary (bug bounty scope or client contract)
- Basic x86/x86-64 assembly literacy (call/ret, stack frame, registers, addressing modes)

## Verification

- [ ] All dangerous imports verified reachable with attacker-controlled input (not dead code)
- [ ] Crash confirmed with minimal payload (not a 1MB fuzz crash)
- [ ] EIP/RIP control confirmed with cyclic pattern; offset documented
- [ ] PoC exploit achieves its objective (crash, info leak, or code execution) on target version
- [ ] Mitigation bypass strategy documented and working (or noted as POC-only)
- [ ] CVSS 3.1 vector calculated per finding with environmental adjustments
- [ ] Remediation code or configuration change provided per finding
- [ ] False positives documented — unreachable or guarded imports flagged as such
- [ ] Deliverable ZIP tested: clean extract, PoC runs, README instructions verified
- [ ] Disclosure timeline agreed with client (embargo period or immediate)
