---
name: fuzz-master
description: Advanced fuzzing techniques for finding zero-days and hidden vulnerabilities. Use when automated scanners miss
  bugs, testing custom protocols, finding memory corruption, or hunting for novel attack vectors.
domain: cybersecurity
author: mahipal
license: Apache-2.0
subdomain: general-cybersecurity
tags:
- cybersecurity
- fuzz
- master
- security
- testing
- threat-defense
- money
version: 1.0.0
---

# Fuzz Master

## Overview

Fuzzing throws unexpected, malformed data at software to make it crash — revealing memory corruption, unhandled exceptions, and logic flaws that static analysis and automated scanners miss. This skill covers **coverage-guided binary fuzzing** (AFL++, LibFuzzer), **API fuzzing** (RESTler, ffuf), **protocol fuzzing** (Boofuzz, Scapy), and **file-format fuzzing** (Radamsa) on a Kali Linux workstation with an RTX 2060 SUPER for parallel multi-instance campaigns.

You are looking for **buffer overflows, use-after-free, integer overflows, null-pointer dereferences, infinite loops, and assertion failures** — the bugs that pay $10K-$100K on ZDI and make vendors panic-fix.

## When to Use

- "Automated scanners found nothing" / "Vulnerability scanners missed it"
- "Test custom/proprietary protocols" / "Reverse engineer protocol and fuzz it"
- "Find buffer overflows, crashes, memory corruption" / "Hunt zero-days"
- "Test file parsers, image decoders, protocol implementations"
- "API endpoint parameter discovery beyond schema"
- "Coverage-guided fuzzing campaign" / "Crash triage and root-cause analysis"

## When NOT to Use

- When automated scanner or manual testing already found the bug
- When the target is a black-box binary you cannot instrument with coverage feedback
- When you lack authorization — fuzzing can crash production systems and corrupt databases
- When the client expects "no false positives" — fuzzing generates noise; triage is part of the deliverable
- For pure informational disclosure without exploit potential

## Money-Making Overview

**Target Buyer:** Software vendors (pre-release QA), DevOps/SRE teams (API security), bug bounty hunters, ISVs shipping parsers/protocol stacks.

**How You Make Money:**
1. **API Fuzzing** — RESTler/ffuf campaigns against client API endpoints. Crash reports with reproduction payloads. ($500-$2K/job)
2. **Binary Fuzzing** — Closed-source binaries (parsers, decoders, daemons) with AFL++ on RTX 2060 SUPER for parallel campaigns. Crashing inputs + root cause. ($1K-$5K/job)
3. **Protocol Fuzzing** — Reverse-engineer custom protocols (IoT, SCADA, gaming, financial) with Boofuzz/Scapy. Wire-format parser bugs. ($2K-$5K/job)
4. **Fuzzing-as-a-Service** — Continuous fuzzing in CI/CD. Weekly crash reports, coverage trends, regression detection. ($2K-$5K/mo retainer)

### Service Tiers

| Tier | Price | What They Get |
|------|-------|---------------|
| **Basic** — API Fuzz | $750 | Single endpoint fuzzed with 4 wordlists (150K+ payloads), crash report with reproducible HTTP requests, coverage heatmap |
| **Pro** — Binary Fuzz | $2,500 | Binary instrumented with AFL++, 24-72hr campaign on 4 parallel instances (RTX 2060 SUPER), 10+ unique crashes triaged, root-cause analysis, PoC inputs |
| **Enterprise** — Retainer | $3,500/mo | Monthly 7-day campaign, CI/CD integration, real-time crash alerts, regression detection, coverage trend reports, Slack notifications |

**Expected First Dollar:** 2-3 weeks (API fuzzing: one spec = one campaign = one report).

## First Action in 60 Minutes — API Fuzzing Pipeline

This script runs a **multi-tool API fuzzing campaign** combining **ffuf** (high-speed discovery) with **custom payload generation** for parameter tampering, type confusion, boundary violations, and injection.

```bash
#!/bin/bash
# api-fuzz-campaign.sh — Usage: ./api-fuzz-campaign.sh <base_url> [endpoint] [outdir]
# Example: ./api-fuzz-campaign.sh https://api.target.com/v1 /users/validate ./fuzz-output
set -euo pipefail
BASE_URL="${1:?Usage: $0 <base_url> [endpoint] [outdir]}"; ENDPOINT="${2:-/api/v1/process}"
OUTDIR="${3:-./fuzz-campaign-$(date +%Y%m%d_%H%M%S)}"; mkdir -p "$OUTDIR"/{payloads,results,crash-reports}

# Phase 1: Generate payload wordlists
echo "[*] Generating payload wordlists..."
cat > "$OUTDIR/payloads/type-confusion.txt" << 'EOF'
null undefined NaN Infinity -Infinity true false [] {} [1] {"a":1}
"" " " "\n" "\t" "\0" "\x00\x00\x00\x00" "\xff\xff\xff\xff"
1 0 -1 2147483647 -2147483648 2147483648 9223372036854775807
1.0 0.0 -0.0 1e-300 1e300 1e99999
EOF
cat > "$OUTDIR/payloads/boundary.txt" << 'EOF'
$(python3 -c "print('A'*10000)") 2>/dev/null
%00 %2500 %252500 ..%252f..%252f ..%c0%ae%c0%ae/
..%ef%bc%8f ..%e0%80%af///..//..//
EOF
cat > "$OUTDIR/payloads/fuzz-injection.txt" << 'EOF'
' OR '1'='1 {$gt: ''} {$ne: ''} [$ne]
'; system('id');-- $(id) `id` | id ; id &
' UNION SELECT NULL -- ' WAITFOR DELAY '0:0:10' --
EOF
cat > "$OUTDIR/payloads/path-traversal.txt" << 'EOF'
../../../etc/passwd ..\..\..\windows\win.ini
....//....//....//etc/passwd file:///etc/passwd
../../../../../../proc/self/maps
EOF

# Phase 2: ffuf campaigns — header, parameter, POST body fuzzing
echo "[*] Running ffuf campaigns..."
ffuf -u "$BASE_URL$ENDPOINT" -H "Content-Type: FUZZ" \
    -w "$OUTDIR/payloads/type-confusion.txt" -mc all -ac \
    -o "$OUTDIR/results/ffuf-content-type.json" -of json -s 2>&1 | tail -3 || true
ffuf -u "$BASE_URL$ENDPOINT?param=FUZZ" \
    -w "$OUTDIR/payloads/boundary.txt" -mc all -ac \
    -o "$OUTDIR/results/ffuf-params.json" -of json -s 2>&1 | tail -3 || true
ffuf -u "$BASE_URL$ENDPOINT" -X POST -H "Content-Type: application/json" \
    -d '{"input":"FUZZ"}' -w "$OUTDIR/payloads/fuzz-injection.txt" -mc all -ac \
    -o "$OUTDIR/results/ffuf-post.json" -of json -s 2>&1 | tail -3 || true

# Phase 3: RESTler setup (generate minimal OpenAPI spec if RESTler not available)
which restler &>/dev/null && echo "[+] RESTler found" || {
    echo "[!] RESTler not found — generating OpenAPI spec for manual use"
}
python3 -c "
import json
spec = {'openapi':'3.0.0','info':{'title':'Fuzz Target','version':'1.0'},
    'paths':{'$ENDPOINT':{
        'get':{'parameters':[{'name':'param','in':'query','schema':{'type':'string'}}],
            'responses':{'200':{'description':'OK'}}},
        'post':{'requestBody':{'content':{'application/json':{'schema':{
            'type':'object','properties':{'input':{'type':'string'}}}}}},
            'responses':{'200':{'description':'OK'}}}}}}
with open('$OUTDIR/payloads/openapi-spec.json','w') as f: json.dump(spec,f,indent=2)
print('[+] OpenAPI spec at $OUTDIR/payloads/openapi-spec.json')
"

# Phase 4: Crash detection & response analysis
echo "[*] Analyzing responses for crash indicators..."
python3 << 'PYEOF'
import json, os, sys, re
from pathlib import Path
outdir = Path(sys.argv[1] if len(sys.argv)>1 else os.environ.get('OUTDIR','.'))
findings = []
re_sev = {'5xx': (r'^5\d{2}$','CRITICAL','Server error — possible crash'),
          'timeout': (r'.*','HIGH','Connection timeout — possible crash'),
          'large_resp': (r'.*','HIGH','Response >50KB — possible info leak')}
for f in sorted((outdir/'results').glob('ffuf-*.json')):
    try:
        data = json.loads(f.read_text())
        for r in data.get('results',[]):
            status,length,url,payload = str(r.get('status','')), r.get('length',0), r.get('url',''), r.get('input',{}).get('FUZZ','')
            if status.startswith('5'): findings.append({'severity':'CRITICAL','status':status,'url':url,'payload':payload[:80],'reason':'Server error — possible unhandled exception'})
            elif length>50000: findings.append({'severity':'HIGH','status':status,'url':url,'length':length,'reason':f'Unusually large response ({length}B)'})
            elif status=='000': findings.append({'severity':'HIGH','status':status,'url':url,'reason':'Connection failed — possible crash'})
    except: pass
report = {'target':os.environ.get('BASE_URL',''),'findings':findings,'total':len(findings)}
(outdir/'crash-reports'/'crash-report.json').write_text(json.dumps(report,indent=2))
print(f'[+] Report: {len(findings)} findings ({sum(1 for f in findings if f["severity"]=="CRITICAL")} critical)')
PYEOF

echo "╔══════════════════════════════════════════════╗"
echo "║  Fuzz campaign complete: $OUTDIR"
echo "╚══════════════════════════════════════════════╝"
echo "Review crash-report.json, then try:"
echo "  afl-fuzz -i corpus -o findings -- ./target @@"
echo "  boofuzz --target host:port --proto tcp"
```

### What This Delivers in 60 Minutes

| Phase | Tool | Duration | Output |
|-------|------|----------|--------|
| Payload generation | heredoc + python3 | 5 min | 4 wordlists (type confusion, boundary, injection, path traversal) |
| Content discovery | ffuf (3 runs) | 15-20 min | JSON results per attack surface |
| RESTler setup | python3 | 10 min | OpenAPI spec for deeper fuzzing |
| Crash triage | Python analyzer | 5 min | Structured crash report with severity scoring |

## Deliverable Format

### Fuzzing Campaign Report

```
┌───────────────────────────────────────────────────────────────────┐
│                    FUZZING CAMPAIGN REPORT                        │
│                    [Client Name] — [Target]                       │
└───────────────────────────────────────────────────────────────────┘

1. EXECUTIVE SUMMARY
   Campaign type:  API / Binary / Protocol
   Target:         [URL / binary / protocol]
   Duration:       [hours]
   Total inputs:   [count]
   Unique crashes: [count] ([CRITICAL/HIGH/MEDIUM/INFO])
   Coverage gain:  [% baseline → % final]

2. CRASH INVENTORY
   ┌──────┬───────────┬──────────────┬───────────────┬──────────┐
   │ ID   │ Severity  │ Location     │ Type          │ Reproduc │
   ├──────┼───────────┼──────────────┼───────────────┼──────────┤
   │ CR1  │ CRITICAL  │ parse_input()│ Null deref    │ 100%     │
   │ CR2  │ HIGH      │ decode_msg() │ Buffer OOB    │ 80%      │
   │ CR3  │ MEDIUM    │ validate()   │ Assert fail   │ 100%     │
   └──────┴───────────┴──────────────┴───────────────┴──────────┘

3. ROOT-CAUSE ANALYSIS (per crash)
   CR1 — Null pointer dereference in parse_input()
   Payload:    {"value": null, "meta": {"tags": []}}
   Stack:      parse_input:284 → lookup_field:92 → strlen(NULL)
   Root cause: Missing null check on value field
   Remediation: Add !value.isNull() guard at line 283
   CVSS v3.1:  7.5 (AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H)

4. COVERAGE ANALYSIS
   Baseline:     ████████████████░░░░░░ 78.2%
   Post-campaign: ██████████████████░░░░ 88.1%  (+9.9pp)
   Uncovered high-risk functions: parseAuthToken(), configLoader()

5. REGRESSION CORPUS
   [5 minimized crashing inputs packaged for CI/CD integration]

6. RECOMMENDATIONS
   [ ] Add null check in parse_input() (1 hr)
   [ ] Enable ASAN/UBSAN in build pipeline (2 days)
   [ ] Fuzz decode_msg() with protocol fuzzer (1 week)
```

### API Fuzzing Quick-Start Checklist

```
[ ] Target identified and authorization confirmed
[ ] OpenAPI spec obtained (or inferred)
[ ] ffuf installed (apt install ffuf)
[ ] RESTler ready (git clone https://github.com/microsoft/restler-fuzzer)
[ ] Wordlists generated or downloaded
[ ] Campaign parameters configured
[ ] Monitoring set up (no crash-blind runs)
[ ] First batch fired
```

## Workflow

### 1. Reconnaissance & Target Analysis
- Identify attack surface: endpoints, input vectors, file parsers, protocol messages
- Acquire or reverse-engineer specification (OpenAPI, protocol docs, Wireshark captures)
- Instrument binary with coverage feedback (AFL++: `afl-clang-fast`, LibFuzzer: `-fsanitize=fuzzer`, ASAN/UBSAN)
- Compile seed corpus from valid inputs (traffic captures, sample files, API responses)

### 2. Fuzzing Campaign Execution
```bash
# Binary fuzzing with AFL++ — 4 parallel instances on RTX 2060 SUPER
afl-fuzz -i corpus/ -o findings/ -M fuzzer1 -- ./target @@
afl-fuzz -i corpus/ -o findings/ -S fuzzer2 -- ./target @@
afl-fuzz -i corpus/ -o findings/ -S fuzzer3 -- ./target @@
afl-fuzz -i corpus/ -o findings/ -S fuzzer4 -- ./target @@

# API fuzzing with RESTler
restler.exe compile --api-spec spec.json
restler.exe fuzz --grammar_file Compile/grammar.py

# Protocol fuzzing with Boofuzz
python3 -c "
from boofuzz import *
session = Session(target=Target(connection=TCPSocketConnection('$HOST', $PORT)))
s_initialize('Message')
s_static(b'\\xaa\\xbb')
s_word(1, endian='>')
s_byte(0x01)
s_random(b'A'*64, max_len=4096)
s_static(b'\\xcc\\xdd')
session.fuzz()
"
```

### 3. Crash Triage & Root Cause Analysis

```bash
# Minimize crashing input
afl-tmin -i crash-001 -o crash-001.min -- ./target @@

# Extract coverage map for crash
afl-showmap -o /dev/null -t 5000 -m 256M -- ./target crash-001 2>&1

# Symbolicate with addr2line
addr2line -e ./target -f -C -i 0x402345 0x403abc

# Deduplicate by stack hash
for crash in findings/default/crashes/*; do
    hash=$(afl-showmap -o /dev/null -t 5000 -m 256M -- ./target "$crash" 2>&1 | md5sum)
    echo "$hash $crash"
done | sort | uniq -w 32
```

### 4. Corpus Distillation & Campaign Optimization

```bash
# Minimize and deduplicate seed corpus
afl-cmin -i corpus/ -o corpus-min/ -- ./target @@

# Merge coverage from multiple fuzzers
mkdir -p merged-coverage
for f in findings/*/queue/*; do
    cp "$f" merged-coverage/ 2>/dev/null
done

# Prune: keep only inputs that increase coverage
afl-cmin -i merged-coverage/ -o final-corpus/ -- ./target @@

# Generate LCOV HTML coverage report
lcov --capture --directory . --output-file coverage.info
genhtml coverage.info --output-directory coverage-report/
```

### 5. Common Fuzzing Strategies by Target Type

| Target Type | Tool | Strategy | Stopping Condition |
|-------------|------|----------|--------------------|
| REST API | RESTler + ffuf | Depth-first stateful fuzzing with garbage mutation | 100K requests or no new 5xx in 10K |
| CLI binary | AFL++ | Coverage-guided with ASAN | 24-72hr or 10 unique crashes |
| Network protocol | Boofuzz | Block-based structure fuzzing | Exhaust all message types |
| File parser | LibFuzzer | In-process coverage-guided with OOM/ubsan | 1B iterations or no new coverage for 6hr |
| Binary (closed-source) | AFL++ QEMU-mode | Whitelist-focus on specific function addresses | 48hr or 5 unique crashes |
| TLS/SSL stack | tls-attacker + afl | Differential analysis + coverage-guided | 6hr per cipher suite |
| JavaScript engine | LibFuzzer + jsfunfuzz | Coverage-guided with ASAN | 72hr minimum |

### 6. Reporting & Delivery
- **Crash report** — JSON + Markdown with per-crash severity, stack trace, payload, root cause
- **Coverage report** — LCOV HTML or CLI coverage delta (pre vs post campaign)
- **Regression corpus** — Minimized crashing inputs packaged for CI/CD pipeline
- **Remediation guidance** — Code-level fixes prioritized by severity with effort estimates

## Tools

| Tool | Purpose | Install |
|------|---------|---------|
| **ffuf** | High-speed HTTP fuzzing | `apt install ffuf` |
| **RESTler** | Stateful REST API fuzzing | `git clone https://github.com/microsoft/restler-fuzzer` |
| **AFL++** | Coverage-guided binary fuzzing | `apt install afl++` |
| **LibFuzzer** | In-process coverage-guided fuzzing | (part of Clang) |
| **Boofuzz** | Network protocol fuzzing | `pip install boofuzz` |
| **Radamsa** | Generative/mutational fuzzing | `apt install radamsa` |
| **Scapy** | Packet-level protocol fuzzing | `apt install python3-scapy` |
| **afl-tmin** | Crash input minimization | (part of AFL++) |
| **GDB** | Crash analysis, backtracing | `apt install gdb` |
| **Valgrind** | Memory error detection | `apt install valgrind` |
| **ASAN/UBSAN** | Compiler sanitizers | `-fsanitize=address,undefined` |
| **nvtop** | GPU monitoring (RTX 2060 SUPER) | `apt install nvtop` |

**RTX 2060 SUPER acceleration:** 4 parallel AFL++ instances without CPU contention. GPU-monitor with `nvtop` — 8GB VRAM handles 4 concurrent fuzzer processes plus corpus minimization.

## Process

1. **Prepare** — Identify target, acquire spec/binary, instrument with coverage, compile seed corpus, set up tmux panes
2. **Execute** — Launch parallel fuzzer instances, monitor coverage growth, rotate wordlists/strategies
3. **Triage** — Collect crashing inputs, minimize each, extract stack trace, deduplicate by call-site hash
4. **Analyze** — Root cause each unique crash, classify severity, estimate CVSS, identify remediation
5. **Report** — Generate campaign report with findings, coverage data, regression corpus, prioritized fixes

## Verification

- [ ] All fuzzing campaigns completed with defined stopping criteria (time/coverage/crashes)
- [ ] Unique crashes deduplicated by stack hash, not input hash
- [ ] Every crash reproduced at least twice
- [ ] Crash inputs minimized with afl-tmin
- [ ] Root cause identified for each unique crash
- [ ] False positives (non-reproducible, environment-specific) tagged and excluded
- [ ] Coverage delta calculated and documented
- [ ] No collateral damage — target system verified operational post-campaign
- [ ] Regression corpus prepared in client-requested format
- [ ] Written authorization confirmed and scoped before any destructive testing

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Fuzzing takes too long — weeks for results" | A 4-instance AFL++ campaign on RTX 2060 SUPER finds crashes in 4-8 hours. Basic API fuzzing with 4 wordlists completes in under an hour. The time objection is from single-instance CPU-only fuzzing. |
| "Automated tools find everything" | Automated scanners find KNOWN vulnerabilities. Fuzzing finds UNKNOWN ones — zero-days, memory corruption, edge-case crashes no signature exists for. Different tools, different results. |
| "My software is too simple to have fuzzing bugs" | Every parser, decoder, deserializer, and network handler has edge cases. SQLite, zlib, and libpng all had critical fuzzing-discovered CVEs. |
| "Coverage-guided fuzzing only works on open source" | AFL++ works on any binary with QEMU mode (no source needed). RTX 2060 SUPER handles QEMU mode with 4x parallelism. |
| "We fix crashes as they're reported by users" | A crash in production means an attacker already found it. Fixing pre-release: $1K cost. Incident response: $250K+. |
| "Crash triage is too much noise" | Stack-hash deduplication + afl-tmin minimization converts 10,000 crashes into 15 unique bugs. Python triage runs in 30 seconds. |
| "Fuzzing is just random data — no skill required" | Wordlist design, coverage feedback analysis, sanitizer configuration, protocol structure definition, and crash root-causing all require deep expertise. The fuzzer generates inputs; the master finds bugs. |
| "We have a CI/CD pipeline, vulnerabilities are caught early" | CI/CD tests VALID inputs. Fuzzing tests INVALID ones — malformed JSON, truncated packets, overflow integers. Different failure domain. |
| "Our fuzzing subscription is too expensive" | $3,500/mo for continuous fuzzing vs $100K average data breach cost. Not fuzzing is the expensive choice. |
| "I need a source code audit, not fuzzing" | Source audits find logic bugs. Fuzzing finds runtime crashes. You need both — but fuzzing is 10x faster at finding exploitable memory corruption. |
