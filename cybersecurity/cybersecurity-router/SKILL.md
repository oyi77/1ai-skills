---
name: cybersecurity-router
description: Use when starting any cybersecurity task — master router that determines the testing phase (Recon/Validation/Exploitation/Post-Exploitation) and routes to the correct specialized skill (Recon, Web/API/Infra/AD/Cloud/Mobile/Binary/Crypto/Forensics/Threat Intel).
domain: cybersecurity
category: cybersecurity
version: 1.0.0
tags:
  - penetration-testing
  - bug-bounty
  - security-assessment
  - red-teaming
  - threat-hunting
  - incident-response
---

# Cybersecurity Router: Master Entry for Security Operations

Master router for 790+ cybersecurity skills. Determines the testing phase, routes to the correct category, and ensures structured methodology over random tool usage.

---

## Anti-Rationalization Table

| Excuse | Reality | Rule |
|--------|---------|------|
| "I'll just run nmap/nuclei/burp" | Random tool usage misses context-specific attack chains | Route by observed behavior, then load specialized skill |
| "I know web/appsec, I don't need a router" | Real engagements chain recon→auth→injection→business logic→privilege escalation | Follow the phase order: Recon → Validation → Exploitation → Post-Exploitation |
| "The scanner found nothing" | Scanners miss business logic, race conditions, auth bypass, second-order vulns | Manual methodology catches what scanners miss |
| "I'll just focus on XSS/SQLi" | Real impact comes from chaining: auth→IDOR→race→RCE | Always consider the full kill chain |
| "AD/Cloud/Mobile is separate" | Modern environments are hybrid — AD connects to cloud, mobile talks to API | Route across domains based on observed attack surface |

---

## When to Use

**Use when:**

- Starting a new penetration test, bug bounty, or security assessment
- Deciding which specialized skill to load first (Recon, Web, API, AD, Cloud, Mobile, Binary, Crypto, Forensics, Threat Intel)
- Routing scattered findings to the correct attack surface skill
- Wanting structured methodology instead of random tool enumeration

**Don't use for:**

- Unauthorized testing (only authorized targets, bug bounty programs, defensive validation)
- Deep exploitation details (drill into category/deep skills after routing)

---
## Workflow

1. **Classify** — Determine target type, identity model, network position, and input/output locations (Phase 1).
2. **Route** — Match observed signals to an attack-surface category using the routing table (Phase 2).
3. **Prioritize** — Test in order: Recon → API/Auth/IDOR → Injection → Business Logic/Race → PrivEsc → Chain (Phase 3).
4. **Load & execute** — Load the category skill, run its workflow, collect evidence.
5. **Report** — Methodology, findings, evidence, impact, remediation — within authorized scope only.


## Operating Model: The Cybersecurity Router

### Phase 1: Recon & Context Validation (Always First)

Collect before testing:

- **Target type**: Web app, REST API, GraphQL, mobile backend, admin panel, payment flow, file upload, GraphQL, thick client, IoT/OT
- **Identity/permission model**: Anonymous, regular user, admin, multi-tenant, service account
- **Network position**: External (internet), Internal (VPN/LAN), Cloud (VPC), Hybrid
- **Input locations**: URL, query params, JSON, headers, cookies, filenames, imported files, templates, reflection points, binary inputs
- **Output locations**: HTML, attributes, JS, PDF, email, logs, background tasks, mobile endpoints, binary responses

### Phase 2: Route by Attack Surface

| Signal | Priority Direction | Load Category Skill |
|--------|-------------------|---------------------|
| New target, unknown surface | Recon & methodology | `recon-automation` |
| REST API, GraphQL, mobile backend | API Security | `api-testing` → `api-destroyer` |
| Login, reset, 2FA, sessions, JWT, OAuth, SAML | Authentication & Authorization | `auth-patterns` → `auth-killer` |
| Input reflects in HTML/JS | XSS / SSTI | `testing-for-xss-vulnerabilities` → `testing-for-xss-vulnerabilities` |
| Server fetches URL/hostname | SSRF | `exploiting-server-side-request-forgery` → `exploiting-server-side-request-forgery` |
| Accepts XML/Office/SVG | XXE | `testing-for-xxe-injection-vulnerabilities` → `testing-for-xxe-injection-vulnerabilities` |
| Path/filename/download controllable | Path Traversal / LFI | `testing-for-broken-access-control` → `testing-for-broken-access-control` |
| Object IDs in APIs | IDOR / BOLA / BFLA | `testing-api-for-broken-object-level-authorization` → `testing-api-for-broken-object-level-authorization` |
| Multi-step: coupons, pricing, inventory | Business Logic | `testing-for-business-logic-vulnerabilities` → `testing-for-business-logic-vulnerabilities` |
| MongoDB/JSON query syntax | NoSQL Injection | `exploiting-nosql-injection-vulnerabilities` → `exploiting-nosql-injection-vulnerabilities` |
| CLI tools, image processing, importers | Command Injection | `exploiting-api-injection-vulnerabilities` → `exploiting-api-injection-vulnerabilities` |
| HTTP parsing anomalies | Request Smuggling | `exploiting-http-request-smuggling` → `exploiting-http-request-smuggling` |
| Node.js `__proto__` controllable | Prototype Pollution | `exploiting-prototype-pollution-in-javascript` → `exploiting-prototype-pollution-in-javascript` |
| PHP weak comparison / 0e hash | Type Juggling | `exploiting-type-juggling-vulnerabilities` → `exploiting-type-juggling-vulnerabilities` |
| Active Directory, domain joined | AD Attacks | `ad-killer` → `ad-killer` |
| Windows host, local admin needed | Windows PrivEsc | `kernel-killer` → `kernel-killer` |
| Linux host, SUID/sudo present | Linux PrivEsc | `kernel-killer` → `kernel-killer` |
| Docker/Kubernetes environment | Container/K8s Security | `hardening-docker-containers-for-production` → `hardening-docker-containers-for-production` |
| Cloud (AWS/Azure/GCP) | Cloud Security | `cloud-hunter` → `cloud-hunter` |
| Mobile app (iOS/Android) | Mobile Security | `mobile-hacking` → `mobile-hacking` |
| Binary/ELF/PE, heap/stack | Binary Exploitation | `binary-breaker` → `binary-breaker` |
| Crypto implementation | Crypto Attacks | `crypto-breaker` → `crypto-breaker` |
| Smart contract/DeFi | Blockchain Security | `web3-auditor` → `web3-auditor` |
| LLM/RAG/prompt injection | AI/ML Security | `ai-hacker` → `ai-hacker` |
| Memory dump, disk image | Forensics | `analyzing-memory-dumps-with-volatility` → `analyzing-memory-dumps-with-volatility` |
| Threat actor profiling | Threat Intel | `analyzing-threat-actor-ttps-with-mitre-attack` → `analyzing-threat-actor-ttps-with-mitre-attack` |

### Phase 3: Testing Priority Order

1. **Recon & Methodology** — `recon-automation`, `bbot-recon`
2. **API Security / Auth / IDOR** — `api-testing`, `api-destroyer`, `auth-killer`, `testing-api-for-broken-object-level-authorization`
3. **Injection Core** — `testing-for-xss-vulnerabilities`, `exploiting-sql-injection-vulnerabilities`, `exploiting-server-side-request-forgery`, `exploiting-template-injection-vulnerabilities`, `testing-for-xxe-injection-vulnerabilities`
4. **Auth & AuthZ** — `auth-killer`, `testing-api-authentication-weaknesses`, `testing-api-for-broken-object-level-authorization`
5. **Business Logic / Race** — `testing-for-business-logic-vulnerabilities`, `exploiting-race-condition-vulnerabilities`
6. **Privilege Escalation / Lateral Movement** — OS/AD/Container/Cloud skills
7. **Post-Exploitation / Persistence** — `ad-killer`, `kernel-killer`, `hardening-docker-containers-for-production`
8. **Chained Exploits / Full Kill Chain** — Combine findings across categories

---

## Core Skill Map (790+ Skills)

### Reconnaissance & Methodology
- `recon-automation` — Automated reconnaissance and attack surface mapping
- `bbot-recon` — BBOT recursive internet scanner
- `analyzing-threat-actor-ttps-with-mitre-attack` — MITRE ATT&CK mapping

### Web Application Security
- `testing-for-xss-vulnerabilities` — Reflected, stored, DOM XSS
- `testing-for-xss-vulnerabilities-with-burpsuite` — Burp Suite XSS validation
- `exploiting-sql-injection-vulnerabilities` — Manual SQLi
- `exploiting-sql-injection-with-sqlmap` — Automated SQLi
- `exploiting-server-side-request-forgery` — SSRF with cloud metadata
- `exploiting-template-injection-vulnerabilities` — SSTI (Jinja2, Twig, etc.)
- `testing-for-xxe-injection-vulnerabilities` — XXE with OOB
- `testing-for-broken-access-control` — IDOR, privilege escalation
- `testing-for-business-logic-vulnerabilities` — Race conditions, price manipulation
- `exploiting-race-condition-vulnerabilities` — Turbo Intruder single-packet
- `exploiting-prototype-pollution-in-javascript` — Prototype pollution
- `exploiting-type-juggling-vulnerabilities` — PHP loose comparison

### API Security
- `api-testing` — REST/GraphQL contract testing
- `api-destroyer` — Aggressive API security testing
- `testing-api-authentication-weaknesses` — Auth bypass, JWT, OAuth
- `testing-api-for-broken-object-level-authorization` — BOLA/IDOR
- `testing-api-for-mass-assignment-vulnerability` — Mass assignment
- `testing-api-security-with-owasp-top-10` — OWASP API Top 10

### Authentication & Authorization
- `auth-killer` — Auth bypass specialist (OAuth, SAML, JWT, SSO, MFA)
- `auth-patterns` — OAuth 2.0, JWT, session management, MFA, RBAC
- `testing-api-authentication-weaknesses` — Auth bypass, token leakage
- `testing-oauth2-implementation-flaws` — OAuth 2.0/OIDC flaws
- `testing-jwt-token-security` — JWT alg confusion, none algorithm
- `testing-for-json-web-token-vulnerabilities` — JWT vulnerabilities

### Active Directory & Windows
- `ad-killer` — AD exploitation (Kerberos, ACL, DCSync, ADCS)
- `analyzing-active-directory-acl-abuse` — ACL abuse paths
- `exploiting-active-directory-with-bloodhound` — BloodHound attack paths
- `exploiting-kerberoasting-with-impacket` — Kerberoasting
- `conducting-domain-persistence-with-dcsync` — DCSync
- `exploiting-nopac-cve-2021-42278-42287` — noPac
- `exploiting-zerologon-vulnerability-cve-2020-1472` — Zerologon

### Linux & Container Security
- `kernel-killer` — Linux/Windows kernel exploitation
- `hardening-docker-containers-for-production` — CIS Docker Benchmark
- `hardening-linux-endpoint-with-cis-benchmark` — CIS Linux
- `analyzing-linux-elf-malware` — Linux malware analysis
- `analyzing-linux-kernel-rootkits` — Kernel rootkits
- `performing-container-escape-detection` — Container escape

### Cloud Security
- `cloud-hunter` — AWS/GCP/Azure misconfiguration hunting
- `aws-ops` / `azure-ops` / `gcp-ops` — Cloud operations
- `auditing-aws-s3-bucket-permissions` — S3 permissions
- `detecting-aws-credential-exposure-with-trufflehog` — Credential exposure
- `detecting-aws-iam-privilege-escalation` — IAM priv esc

### Mobile Security
- `mobile-hacking` — Android/iOS security testing
- `android-jetpack` — Android development
- `ios-swiftui` — iOS development
- `analyzing-android-malware-with-apktool` — APK analysis
- `analyzing-ios-app-security-with-objection` — iOS runtime

### Binary Exploitation (Pwn)
- `binary-breaker` — Binary exploitation & RE
- `reverse-engineering-malware-with-ghidra` — Ghidra RE
- `reverse-engineering-android-malware-with-jadx` — Android RE
- `reverse-engineering-dotnet-malware-with-dnspy` — .NET RE
- `analyzing-heap-spray-exploitation` — Heap spray
- `analyzing-ransomware-encryption-mechanisms` — Ransomware crypto
- `go-rust-reverse` — Go/Rust RE
- `dsl-vm-reverse` — Custom VM/DSL RE

### Cryptography
- `crypto-breaker` — Crypto implementation attacks
- `exploiting-jwt-algorithm-confusion-attack` — JWT alg confusion
- `analyzing-ethereum-smart-contract-vulnerabilities` — Solidity vulns

### Blockchain & Smart Contract
- `web3-auditor` — Smart contract/DeFi auditing
- `smart-contract-exploiter` — Automated vuln scanning
- `defi-incident-analysis` — DeFi incident analysis

### AI/ML & LLM Security
- `ai-hacker` — Prompt injection, model manipulation
- `detecting-ai-model-prompt-injection-attacks` — Prompt injection detection

### Forensics & Incident Response
- `analyzing-memory-dumps-with-volatility` — Volatility memory forensics
- `analyzing-disk-image-with-autopsy` — Autopsy disk forensics
- `performing-disk-forensics-investigation` — Disk forensics
- `performing-endpoint-forensics-investigation` — Endpoint forensics
- `performing-network-forensics-with-wireshark` — Network forensics
- `performing-malware-incident-response` — Malware IR
- `performing-ransomware-response` — Ransomware IR

### Threat Intelligence & Hunting
- `analyzing-threat-actor-ttps-with-mitre-attack` — MITRE ATT&CK mapping
- `analyzing-threat-actor-ttps-with-mitre-navigator` — ATT&CK Navigator
- `hunting-advanced-persistent-threats` — APT hunting
- `hunting-for-cobalt-strike-beacons` — Cobalt Strike detection
- `building-threat-intelligence-platform` — TIP building

---

## High-Value Expert Intuitions

1. **Same filter reused across endpoints** — if one bypassable, similar endpoints usually are too
2. **Parameter names are attack surface** — WAFs often inspect values, not names
3. **Second-order vulns are common** — safe at storage ≠ safe when later read dangerously
4. **BOLA = authenticated but unauthorized** — replay with account A/B switching critical
5. **Older API versions miss patches** — fixing v2 doesn't mean v1 retired
6. **Business logic = highest impact** — scanners miss them, persist longer
7. **Race conditions → one-time actions** — coupons, claims, resets, invites, inventory
8. **JWT: check key/algorithm context first** — verify `alg`, `kid`, JWKS, key source before spraying

---

## Suggested Prompts

- "Plan the testing route for this target using penetration testing methodology"
- "This is a REST API; prioritize BOLA, BFLA, Mass Assignment, and JWT angles"
- "This parameter triggers server-side requests; list key validation points from SSRF perspective"
- "This feature is a payment/coupon/inventory flow; prioritize business logic and race-condition analysis"
- "I only see login and password-reset flows; analyze via Auth Bypass + OAuth/JWT + CSRF"
- "This is a Windows domain environment; prioritize AD enumeration and Kerberos attacks"
- "This is a Kubernetes cluster; prioritize RBAC, SA tokens, and pod escape"

---

## Verification Checklist

- [ ] Target type and identity model identified before testing
- [ ] Recon completed: asset discovery, tech fingerprinting, endpoint inventory
- [ ] Routing decision documented with observed signals
- [ ] Category skill loaded for each identified attack surface
- [ ] Testing follows priority order: Recon → API/Auth/IDOR → Injection → Business Logic → PrivEsc → Chain
- [ ] Business logic and race conditions tested (not just scanner output)
- [ ] JWT/auth attacks verify key/algorithm context before payload spraying
- [ ] Findings chained across categories where applicable
- [ ] All testing within authorized scope only
- [ ] Report includes: methodology, findings, evidence, impact, remediation

---

## References

- **Cybersecurity skills**: 790+ skills in `/cybersecurity/` directory
- **MITRE ATT&CK**: https://attack.mitre.org/
- **OWASP Top 10 / API Top 10**: https://owasp.org/
- **PTES**: http://www.pentest-standard.org/
- **NIST SP 800-115**: Technical Guide to Information Security Testing