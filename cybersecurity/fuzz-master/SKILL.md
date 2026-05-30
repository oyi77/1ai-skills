---
name: fuzz-master
description: Advanced fuzzing techniques for finding zero-days and hidden vulnerabilities. Use when automated scanners miss bugs, testing custom protocols, finding memory corruption, or hunting for novel attack vectors.
---

# Fuzz Master

Scanners find known bugs. Fuzzing finds unknown bugs. This skill covers advanced fuzzing techniques that find what no one else has found yet — the definition of zero-day.

## When to Use

- Automated scanners found nothing (time to fuzz)
- Testing custom/proprietary protocols
- Finding buffer overflows, crashes, memory corruption
- Hunting zero-days in popular software
- Testing file parsers and data processors
- API endpoint parameter discovery

## The Process

1. **Scope and authorize** — confirm written authorization and define target boundaries
2. **Reconnaissance** — enumerate targets, services, and potential attack surfaces
3. **Exploitation** — attempt exploitation of identified vulnerabilities within scope
4. **Post-exploitation** — document access level, lateral movement, and data exposure
5. **Report and remediate** — compile findings with reproduction steps and fix recommendations
### 1. Web Fuzzing

#### Directory/Path Discovery
```bash
# Wordlist selection matters
# Generic: common.txt, raft-medium-directories.txt
# Technology-specific: asp.txt, php.txt, java.txt
# Custom: combine multiple sources

# Recursive fuzzing
ffuf -u https://target.com/FUZZ -w wordlist.txt -recursion -recursion-depth 3

# Vhost fuzzing
ffuf -u https://target.com -H "Host: FUZZ.target.com" -w subdomains.txt

# Parameter fuzzing
ffuf -u "https://target.com/api?FUZZ=test" -w params.txt -fc 404
ffuf -u "https://target.com/api?test=FUZZ" -w values.txt

# Header fuzzing
ffuf -u https://target.com -H "FUZZ: admin" -w headers.txt
```

#### Response Differential Analysis
```bash
# Find hidden behavior by comparing responses
ffuf -u https://target.com/api -w wordlist.txt \
  -mc all -fc 404 \
  -fl 10  # Filter by line count (find unique responses)

# Match specific patterns
ffuf -u https://target.com -w wordlist.txt \
  -mr "admin|root|password|secret"
```

### 2. API Fuzzing

#### Parameter Discovery
```bash
# Hidden parameters in POST body
ffuf -X POST -u https://target.com/api \
  -d '{"FUZZ": "test"}' \
  -H "Content-Type: application/json" \
  -w params.txt -fc 400

# JSON key fuzzing
ffuf -X POST -u https://target.com/api \
  -d '{"known": "value", "FUZZ": "admin"}' \
  -w params.txt

# GraphQL field discovery
ffuf -X POST -u https://target.com/graphql \
  -d '{"query": "{ user { FUZZ } }"}' \
  -w fields.txt
```

#### HTTP Method Fuzzing
```bash
# Test all HTTP methods
for method in GET POST PUT DELETE PATCH OPTIONS TRACE CONNECT; do
  curl -X $method https://target.com/api/resource
done

# Method override
X-HTTP-Method-Override: DELETE
X-Method-Override: DELETE
_method=PUT
```

### 3. Input Fuzzing

#### Payload Mutation
```
# Generate variations of known payloads
# XSS mutation:
<script>alert(1)</script>
<SCRIPT>alert(1)</SCRIPT>
<script >alert(1)</script>
<script>alert(1)<!--
<svg/onload=alert(1)>
<img src=x onerror=alert(1)>

# SQL injection mutation:
' OR '1'='1
' OR '1'='1'--
' OR '1'='1'/*
' || '1'='1
' OR 1=1
' OR 1=1--
admin'--
```

#### Boundary Testing
```
# Integer boundaries
0, 1, -1, 2147483647, 2147483648, -2147483648, 4294967295

# String boundaries
"", "A"*1, "A"*255, "A"*256, "A"*65535, "A"*1048576

# Array boundaries
[], [null], ["A"*10000], [1]*10000

# Special values
null, undefined, NaN, Infinity, true, false
```

### 4. File Fuzzing

#### Upload Fuzzing
```bash
# File extension bypass
shell.php → shell.php5, shell.phtml, shell.pht, shell.php.jpg
shell.php → shell.php%00.jpg (null byte)
shell.php → shell.php;.jpg (semicolon)
shell.php → shell.php%20 (space)
shell.php → shell.php. (dot)
shell.php → .htaccess (Apache config)

# Content-Type bypass
Content-Type: image/jpeg (for PHP file)
Content-Type: application/octet-stream

# Magic bytes
Add JPEG header: FF D8 FF E0 to PHP file
Add PNG header: 89 50 4E 47 to PHP file

# Double extension
shell.php.jpg → if Apache processes .php
shell.jpg.php → if misconfigured
```

#### Parser Differential
```
# Different parsers interpret same input differently
# JSON: {"a":1,"a":2} → first or second wins?
# XML: <a><b>text</b></a> → different DOMs
# URL: /path/..;/secret → Tomcat vs Nginx
```

### 5. Protocol Fuzzing

#### HTTP/2 Fuzzing
```
# Header order manipulation
# HPACK compression attacks
# Stream multiplexing abuse
# SETTINGS frame manipulation
```

#### WebSocket Fuzzing
```
# Message type fuzzing
# Binary vs text frame switching
# Fragmentation attacks
# Control frame injection
```

### 6. Smart Fuzzing Strategies

#### Coverage-Guided Fuzzing
```bash
# AFL++ (American Fuzzy Lop)
afl-fuzz -i input_dir -o output_dir -- ./target @@

# LibFuzzer (in-process fuzzing)
# Requires instrumented binary

# Honggfuzz
honggfuzz -i input_dir -- ./target ___
```

#### Grammar-Based Fuzzing
```bash
# For structured inputs (JSON, XML, SQL)
# Define grammar, let fuzzer generate valid+mutations

# SQL grammar example
query = select_stmt | insert_stmt | update_stmt | delete_stmt
select_stmt = "SELECT" columns "FROM" table where_clause
```

#### Neural Fuzzing
```
# Use ML to generate better test cases
# Train on existing PoCs
# Generate novel mutations based on code coverage feedback
```

### 7. Crash Analysis

When fuzzer finds a crash:

1. **Reproduce** — Can you trigger it consistently?
2. **Minimize** — What's the smallest input that triggers it?
3. **Classify** — Buffer overflow? Use-after-free? Null deref?
4. **Exploitability** — Can you control execution? RIP/EIP overwrite?
5. **Impact** — RCE? DoS? Information disclosure?

```bash
# Crash deduplication
afl-collect output_dir crashes_dir -- ./target @@

# Minimize test case
afl-tmin -i crash -o minimized -- ./target @@

# Triage crashes
afl-cmin -i output_dir -o minimized_dir -- ./target @@
```

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Red Flags

- Fuzzing production systems without authorization
- Causing denial of service with crash-inducing inputs
- Not reporting crashes that affect availability
- Exploiting crashes without permission
- Fuzzing third-party software without bug bounty scope

## Verification

- Crash is reproducible from clean state
- Minimal input that triggers crash is documented
- Crash type is classified (not just "it crashed")
- Impact is assessed (DoS vs RCE vs info disclosure)
- Report includes crash analysis, not just raw input

## Revenue Potential

Zero-days in popular software pay the most:
- Browser zero-days: $50,000-$250,000
- OS kernel zero-days: $100,000-$500,000
- Popular library zero-days: $10,000-$100,000
- Web app zero-days: $1,000-$50,000
- Protocol zero-days: $50,000-$500,000

## Tools

| Purpose | Tools |
|---------|-------|
| Web fuzzing | ffuf, feroxbuster, gobuster, wfuzz |
| Binary fuzzing | AFL++, honggfuzz, libfuzzer |
| API fuzzing | Burp Intruder, ffuf, RESTler |
| Grammar | Peach, boofuzz, Domato |
| Analysis | GDB, WinDbg, rr, ASAN, MSAN |
| Crash triage | afl-collect, crashwalk, exploitable |
