---
name: hack-skills
description: Use when starting web application testing, API security assessment, bug bounty hunting, or authorized penetration testing. Master router that determines testing phase (Recon/Validation/PrivEsc/Chain) and routes to the correct vulnerability category skill (XSS, SQLi, SSRF, IDOR, JWT, API, Auth, etc.).
category: cybersecurity
domain: cybersecurity
tags:
  - hacking
  - penetration-testing
  - bug-bounty
  - web-security
  - api-security
  - vulnerability-assessment
  - security-testing
  - methodology
version: 1.0.0
---

# HackSkills: Master Router for Security Testing

Master entry router for HackSkills — a curated knowledge base of 101 offensive security skills covering web, API, auth, injection, file access, business logic, infrastructure, OS privilege escalation, Active Directory, mobile, binary exploitation, reverse engineering, cryptography, blockchain, AI/ML security, and forensics.

Built for bug bounty, penetration testing, CTF competitions, and authorized security research.

---

## Anti-Rationalization Table

| Excuse | Reality | Rule |
|--------|---------|------|
| "I'll just spray payloads from memory" | Random payloads miss context-specific bypasses and chain opportunities | Route by observed behavior, then load specialized skill |
| "XSS/SQLi/SSRF are all I need" | Real engagements chain auth→IDOR→race→RCE; single-category testing leaves gaps | Follow the phase order: Recon → API/Auth/IDOR → Injection → Business Logic → Chain |
| "The scanner found nothing" | Scanners miss business logic, race conditions, second-order, and auth bypass | Manual methodology catches what scanners miss |
| "JWT attacks are just alg=none" | Real JWT attacks involve key confusion, JWKS abuse, claim tampering, kid manipulation | Verify alg/kid/JWKS/key source first, then choose attack vector |
| "BOLA is just changing IDs" | BOLA requires systematic testing across 8 categories with ORM filter chain analysis | Load IDOR skill for structured testing matrix |
| "I don't need recon, I know the target" | Asset discovery reveals shadow APIs, old versions, and forgotten endpoints | Always start with recon-for-sec |

---

## When to Use

**Use when:**

- Starting a new bug bounty target or penetration test engagement
- Deciding whether to load XSS / SQLi / SSRF / IDOR / JWT / API tracks first
- Routing scattered findings to the correct attack surface skill
- Wanting AI to miss fewer critical test points in security work
- Needing a structured methodology instead of random payload enumeration

**Don't use for:**

- Unauthorized testing (use only on authorized targets, bug bounty programs, defensive validation)
- Deep exploitation details (drill into category/deep topic skills after routing)

---

## Operating Model: The HackSkills Router

### Phase 1: Recon & Context Validation (Always First)

Collect before testing:

- **Target type**: classic web, REST API, mobile backend, admin panel, payment flow, file upload, GraphQL
- **Identity/permission model**: anonymous, regular user, admin, multi-tenant
- **Input locations**: URL, query params, JSON, headers, cookies, filenames, imported files, templates, reflection points
- **Output locations**: HTML, attributes, JS, PDF, email, logs, background tasks, mobile endpoints

### Phase 2: Route by Observed Behavior

| Signal | Priority Direction | Load Skill |
|--------|-------------------|------------|
| Input reflects into HTML / JS | XSS / SSTI | `xss-cross-site-scripting`, `ssti-server-side-template-injection` |
| Server fetches URL / hostname | SSRF | `ssrf-server-side-request-forgery` |
| Accepts XML / Office / SVG | XXE | `xxe-xml-external-entity` |
| Path, filename, download controllable | Path Traversal / LFI | `path-traversal-lfi` |
| Many object IDs in APIs | IDOR / BOLA / BFLA | `idor-broken-object-authorization` |
| Login, reset, 2FA, sessions | Auth Bypass / JWT / OAuth | `authbypass-authentication-flaws`, `jwt-oauth-token-attacks` |
| Multi-step: coupons, pricing, inventory | Business Logic | `business-logic-vulnerabilities` |
| MongoDB / JSON query syntax | NoSQL Injection | `nosql-injection` |
| CLI tools, image processing, importers | Command Injection | `cmdi-command-injection` |
| HTTP parsing anomalies | Request Smuggling | `request-smuggling` |
| Node.js `__proto__` controllable | Prototype Pollution | `prototype-pollution` |
| PHP weak comparison / 0e hash | Type Juggling | `type-juggling` |
| Repeated params / WAF-app mismatch | HTTP Parameter Pollution | `http-parameter-pollution` |
| One-time ops (coupon/reset/invite) | Race Condition | `race-condition` |
| XML/XSLT processing | XSLT Injection | `xslt-injection` |
| `.git/.svn/.env` accessible | Insecure SCM | `insecure-source-code-management` |
| CSV/Excel export | CSV Formula Injection | `csv-formula-injection` |
| WebSocket upgrades | WebSocket Security | `websocket-security` |
| Internal package names | Dependency Confusion | `dependency-confusion` |

### Phase 3: Testing Priority Order

1. **Recon / Methodology** — `recon-for-sec` → `recon-and-methodology`
2. **API Security / Auth / IDOR** — `api-sec` → `api-authorization-and-bola`, `api-auth-and-jwt-abuse`, `idor-broken-object-authorization`
3. **Injection Core** — `injection-checking` → `xss-cross-site-scripting`, `sqli-sql-injection`, `ssrf-server-side-request-forgery`, `ssti-server-side-template-injection`, `xxe-xml-external-entity`
4. **Business Logic / Race** — `business-logic-vuln` → `business-logic-vulnerabilities`, `race-condition`
5. **Chained Exploits / PrivEsc** — OS/AD/container/mobile skills based on target

---

## Workflow

1. **Install** — `npx skills add yaklang/hack-skills` or clone the repo
2. **Start with Recon** — Load `recon-for-sec` to map assets, tech stack, endpoints
3. **Route by Signal** — Use the Phase 2 table to select category skill(s)
4. **Drill Deep** — Load specific deep topic skill(s) for exploit details
5. **Chain & Escalate** — Combine findings across categories for max impact
6. **Report** — Document findings with reproduction steps, impact, remediation

---

## Core Skill Map (101 Deep Topic Skills)

### Reconnaissance & Methodology
- `recon-and-methodology` — Methodology framework, Java middleware fingerprint matrix, leak detection checklist
- `insecure-source-code-management` — `.git/.svn/.hg/.bzr` recovery, backup file patterns
- `dependency-confusion` — npm/pip/gem hijacking, manifest identification

### API Security
- `api-recon-and-docs` — API discovery, OpenAPI/Swagger, hidden endpoints
- `api-authorization-and-bola` — BOLA/BFLA, mass assignment, object-level authz
- `api-auth-and-jwt-abuse` — JWT attacks, API key abuse, token manipulation
- `graphql-and-hidden-parameters` — GraphQL introspection, batching, hidden params

### Authentication & Authorization
- `authbypass-authentication-flaws` — Password reset 22-pattern matrix, captcha bypass 20 methods, insecure randomness
- `jwt-oauth-token-attacks` — JWT alg confusion, key confusion, claim tampering, JWKS abuse
- `oauth-oidc-misconfiguration` — OAuth flow hijacking, OIDC misconfiguration
- `saml-sso-assertion-attacks` — SAML assertion manipulation, SSO bypass
- `idor-broken-object-authorization` — 8-category IDOR testing, ORM filter chain leaks (Django/Prisma/Ransack)

### Injection Attacks
- `xss-cross-site-scripting` — Polyglot payloads, WAF bypass by vendor, CSP bypass, DOM clobbering, CSS injection
- `sqli-sql-injection` — DB2/Cassandra/BigQuery/SQLite specifics, SQLite RCE, WAF bypass matrix
- `ssrf-server-side-request-forgery` — Cloud metadata 6-platform matrix, DNS rebinding, Gopher/Redis RCE chain
- `ssti-server-side-template-injection` — 15+ engine coverage, blind SSTI, Flask PIN calculation
- `cmdi-command-injection` — WAF bypass, PHP disable_functions 6 bypass paths, component RCE
- `nosql-injection` — Blind extraction scripts, aggregation pipeline injection, $where JS execution
- `xxe-xml-external-entity` — Local DTD injection (17+ paths), blind XXE, OOB exfiltration
- `deserialization-insecure` — Java/PHP/Python/.NET/Node.js chains
- `prototype-pollution` — Express black-box probing, EJS/Kibana gadget chains
- `type-juggling` — PHP loose comparison, magic hash, HMAC 0e brute-force
- `http-parameter-pollution` — Server behavior matrix (9 platforms), HPP+WAF bypass
- `xslt-injection` — 3 RCE chains (PHP/Java/.NET), EXSLT file write
- `csv-formula-injection` — DDE/rundll32, Google Sheets IMPORT* exfiltration
- `expression-language-injection` — SpEL, OGNL, Java EL injection with RCE
- `jndi-injection` — JNDI/LDAP/RMI, Log4Shell patterns
- `crlf-injection` — Header injection, HTTP response splitting
- `request-smuggling` — CL.TE/TE.CL/TE.TE, HTTP/2 downgrade, client-side desync
- `ghost-bits-cast-attack` — Java char-to-byte narrowing WAF bypass (Black Hat Asia 2026)

### File & Path Attacks
- `path-traversal-lfi` — LFI-to-RCE 7 paths, PHP wrapper matrix, pearcmd 4 methods
- `upload-insecure-files` — Success rate formula, editor path matrix, validation defect taxonomy

### Business Logic & Session
- `business-logic-vulnerabilities` — Payment manipulation matrix (10 attacks), state machine bypass
- `race-condition` — TOCTOU, HTTP/1.1 last-byte sync, HTTP/2 single-packet, Turbo Intruder templates
- `csrf-cross-site-request-forgery` — JSON CSRF, multipart upload CSRF, CSPT2CSRF
- `clickjacking` — Frame-based attacks, X-Frame-Options/CSP bypass
- `cors-cross-origin-misconfiguration` — Origin reflection, null origin, subdomain trust
- `open-redirect` — Redirect chain abuse, tabnabbing
- `web-cache-deception` — Path confusion, cache key manipulation

### Advanced Web Security
- `subdomain-takeover` — Dangling DNS, cloud fingerprinting, verification bypass
- `waf-bypass-techniques` — Encoding chains, chunked transfer, vendor-specific matrices
- `csp-bypass-advanced` — Script gadgets, base-uri abuse, JSONP, trusted CDN, strict-dynamic
- `http-host-header-attacks` — Password reset poisoning, cache poisoning, routing SSRF
- `dangling-markup-injection` — HTML injection without JS, CSP-safe data theft
- `dns-rebinding-attacks` — Internal network access, TTL manipulation, SOP bypass
- `email-header-injection` — SMTP header injection, phishing via injected headers
- `http2-specific-attacks` — H2 smuggling, HPACK attacks, stream multiplexing abuse
- `prototype-pollution-advanced` — Server-side gadget chains, framework-specific PP→RCE
- `401-403-bypass-techniques` — Path normalization, verb tampering, header-based bypass

### Infrastructure & Network
- `unauthorized-access-common-services` — Reverse proxy misconfig, service exposure
- `insecure-source-code-management` — VCS recovery, backup file patterns
- `dependency-confusion` — Supply chain hijacking, scope/namespace defense
- `websocket-security` — CSWSH, Origin validation, wsrepl tooling
- `network-protocol-attacks` — ARP/DNS/LLNMR/DHCP/IPv6 poisoning
- `tunneling-and-pivoting` — SSH tunnels, chisel/ligolo-ng, DNS/ICMP tunneling
- `reverse-shell-techniques` — Multi-language shells, encrypted, staged/stageless

### Linux & Container Security
- `linux-privilege-escalation` — SUID/SGID, kernel exploits, sudo, cron, capabilities, NFS
- `container-escape-techniques` — Docker socket, privileged escape, cgroup breakout, runc vulns
- `linux-security-bypass` — SELinux/AppArmor/seccomp/namespace/LD_PRELOAD
- `linux-lateral-movement` — SSH keys, credential reuse, NFS/cron persistence
- `kubernetes-pentesting` — PSP bypass, RBAC abuse, SA token theft, etcd, kubelet API

### Windows & Active Directory
- `windows-privilege-escalation` — Token manipulation, service misconfig, DLL hijack, UAC, Potato
- `active-directory-kerberos-attacks` — Kerberoast, AS-REP roast, Golden/Silver Ticket, delegation
- `active-directory-acl-abuse` — DCSync, WriteDACL/GenericAll, BloodHound
- `active-directory-certificate-services` — ESC1–ESC8, Shadow Credentials, CA persistence
- `ntlm-relay-coercion` — PetitPotam, PrinterBug, relay chains, WebDAV
- `windows-lateral-movement` — PsExec, WMI, WinRM, DCOM, PtH/PtT, RDP hijacking
- `windows-av-evasion` — AMSI bypass, ETW patching, API unhooking, LOLBins, obfuscation

### macOS Security
- `macos-security-bypass` — Gatekeeper, TCC, SIP, LaunchAgent, quarantine
- `macos-process-injection` — Dylib injection, task_for_pid, XPC, Electron injection

### Mobile Security
- `android-pentesting-tricks` — APK analysis, Frida, Intent, root detection, WebView
- `ios-pentesting-tricks` — IPA analysis, ObjC runtime, jailbreak bypass, Keychain
- `mobile-ssl-pinning-bypass` — Frida/Objection scripts, network security config

### Binary Exploitation (Pwn)
- `stack-overflow-and-rop` — Buffer overflow, ROP, ret2libc, SROP, stack pivoting
- `heap-exploitation` — UAF, double free, tcache poisoning, fastbin, House of series
- `format-string-exploitation` — Read/write primitives, GOT overwrite, FORTIFY bypass
- `kernel-exploitation` — Kernel ROP, ret2usr, SMEP/SMAP/KPTI bypass, modprobe_path
- `browser-exploitation-v8` — V8 JIT bugs, type confusion, OOB, sandbox escape
- `sandbox-escape-techniques` — Browser sandbox, seccomp, IPC, kernel for sandbox breakout
- `binary-protection-bypass` — ASLR/NX/PIE/Canary/RELRO bypass, info leak exploitation
- `arbitrary-write-to-rce` — GOT/__free_hook, FSOP, _IO_FILE, exit handler

### Reverse Engineering
- `anti-debugging-techniques` — ptrace, timing, self-modifying, anti-VM, exception-based
- `code-obfuscation-deobfuscation` — Control flow flattening, opaque predicates, OLLVM/Themida/VMProtect
- `symbolic-execution-tools` — angr, Z3, Triton for vuln discovery, constraint solving
- `vm-and-bytecode-reverse` — Custom VM/bytecode, Python/Java/.NET decompilation

### Cryptography Attacks
- `rsa-attack-techniques` — Wiener, Boneh-Durfee, Hastad, Coppersmith, padding oracle
- `symmetric-cipher-attacks` — Padding oracle, bit-flipping, ECB cut-paste, MITM
- `lattice-crypto-attacks` — LLL/BKZ, Hidden Number Problem, NTRU, CVP/SVP
- `hash-attack-techniques` — Length extension, birthday, collision, bcrypt/scrypt/argon2
- `classical-cipher-analysis` — Frequency analysis, Vigenère/Kasiski, Hill, Enigma

### Blockchain & Smart Contract
- `smart-contract-vulnerabilities` — Reentrancy (4), integer overflow, delegatecall, flash loan
- `defi-attack-patterns` — Flash loan oracle manipulation, MEV sandwich, governance, bridge

### AI/ML & LLM Security
- `llm-prompt-injection` — Direct/indirect injection, RAG poisoning, tool abuse, MCP risks
- `ai-ml-security` — Pickle RCE, adversarial examples, data poisoning, model extraction

### Forensics & Steganography
- `memory-forensics-volatility` — Volatility framework, process/network analysis, malware
- `steganography-techniques` — LSB, format analysis, zsteg/stegsolve/steghide, EXIF
- `traffic-analysis-pcap` — Wireshark/tshark, protocol dissection, stream reconstruction

---

## High-Value Expert Intuitions

1. **Same filter reused across pages** — if one bypassable, similar pages usually are too
2. **Parameter names are attack surface** — WAFs often inspect values, not names
3. **Second-order vulns are common** — safe at storage ≠ safe when later read dangerously
4. **BOLA = authenticated but unauthorized** — replay with account A/B switching critical
5. **Older API versions miss patches** — fixing v2 doesn't mean v1 retired
6. **Business logic = highest impact** — scanners miss them, persist longer
7. **Race conditions → one-time actions** — coupons, claims, resets, invites, inventory
8. **JWT: check key/algorithm context first** — verify `alg`, `kid`, JWKS, key source before spraying

---

## Suggested Prompts

- "Plan the testing route for this target using bug bounty methodology"
- "This is a REST API; prioritize BOLA, BFLA, Mass Assignment, and JWT angles"
- "This parameter triggers server-side requests; list key validation points from SSRF perspective"
- "This feature is a payment/coupon/inventory flow; prioritize business logic and race-condition analysis"
- "I only see login and password-reset flows; analyze via Auth Bypass + OAuth/JWT + CSRF"

---

## Installation

```bash
# Via npx (preferred)
npx skills add yaklang/hack-skills

# Or raw URL
curl -fsSL https://raw.githubusercontent.com/yaklang/hack-skills/main/skills-hack/SKILL.md

# Offline ZIP (AES-256, password: hack-skills)
curl -fsSLO https://oss-qn.yaklang.com/hack-skills/latest/hack-skills.zip
7z x -phack-skills hack-skills.zip
```

---

## Verification Checklist

- [ ] Target type and identity model identified before testing
- [ ] Recon completed: asset discovery, tech fingerprinting, endpoint inventory
- [ ] Routing decision documented with observed signals
- [ ] Category skill loaded for each identified attack surface
- [ ] Testing follows priority order: Recon → API/Auth/IDOR → Injection → Business Logic → Chain
- [ ] Business logic and race conditions tested (not just scanner output)
- [ ] JWT/auth attacks verify key/algorithm context before payload spraying
- [ ] Findings chained across categories where applicable
- [ ] All testing within authorized scope only

---

## References

- **Source Repository**: https://github.com/yaklang/hack-skills
- **Web UI**: https://skills.hackbenchmark.com (search, filter, copy install commands)
- **Offline ZIP**: https://oss-qn.yaklang.com/hack-skills/latest/hack-skills.zip (password: `hack-skills`)
- **Primary Sources**: PayloadsAllTheThings, PentesterSpecialDict, Dictionary-Of-Pentesting, Hello-CTF, ctf-wiki, hacktricks, public CVE advisories
- **Sister Projects**: Yak Skills (yaklang/yak-skills), Training Materials (yaklang/yaklang-ai-training-materials), Benchmark (hackbenchmark.com)