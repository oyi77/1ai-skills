<!-- Parent: ../AGENTS.md -->
<!-- Regenerate via: bash scripts/audit-skills.sh -->

# cybersecurity/

## Purpose
779 security skills across 26 subdomains. Each skill is a self-contained `SKILL.md` with YAML frontmatter (`name`, `description`, `domain: cybersecurity`, `subdomain`, `tags`, optional `author`/`persona`).

**For agents**: grep this file for a subdomain that matches the task, then load only those specific skill dirs. Do NOT walk the whole `cybersecurity/` tree — it will blow context.

## Subdomain Map (filter by `subdomain:` frontmatter)

| Subdomain | Skills | Use For |
|---|---:|---|
| `cloud-security` | 63 | AWS/GCP/Azure posture, IAM misconfig, S3, KMS, control plane |
| `threat-hunting` | 56 | Proactive search, SIEM queries, MITRE ATT&CK, behavioral analytics |
| `threat-intelligence` | 50 | IOC enrichment, APT attribution, dark web, leak sites, CTI feeds |
| `network-security` | 43 | Firewall, IDS/IPS, packet capture, NetFlow, DNS analysis |
| `web-application-security` | 42 | OWASP Top 10, XSS, SQLi, SSRF, business logic |
| `malware-analysis` | 39 | Static/dynamic reversing, sandbox, YARA, unpacking |
| `digital-forensics` | 37 | Disk imaging, memory, registry, browser, mobile artifacts |
| `soc-operations` | 33 | Runbooks, escalation, alert triage, ticketing |
| `identity-access-management` | 33 | OAuth, SAML, MFA, JIT, lifecycle, IGA |
| `container-security` | 29 | Kubernetes, image scanning, runtime, admission control |
| `security-operations` | 28 | SOAR, automation, metrics, SLA |
| `ot-ics-security` | 28 | Modbus, DNP3, SCADA, Purdue model, ICS-CERT |
| `api-security` | 28 | OAuth/JWT, rate limit, schema validation, API gateway |
| `incident-response` | 26 | NIST 800-61, IR playbooks, evidence chain, communications |
| `vulnerability-management` | 25 | Scanner ops, SLA, prioritization (EPSS/CVSS), patching |
| `red-teaming` | 24 | Adversary emulation, C2, OPSEC, evasion |
| `penetration-testing` | 20 | Network/app pentest methodology, reporting |
| `zero-trust-architecture` | 17 | Microsegmentation, identity-based access, policy engines |
| `endpoint-security` | 17 | EDR, host hardening, application control |
| `devsecops` | 17 | SAST/DAST/SCA, CI/CD security, IaC scanning |
| `phishing-defense` | 15 | DMARC/DKIM/SPF, secure email gateway, user training |
| `cryptography` | 15 | Algorithm selection, key management, HSM, PKI |
| `ransomware-defense` | 13 | Backup integrity, recovery, decryption, negotiation |
| `mobile-security` | 13 | iOS/Android static + dynamic, Frida, MASVS |
| `threat-detection` | 7 | Detection engineering, Sigma rules, ATT&CK coverage |
| `compliance-governance` | 4 | SOC 2, ISO 27001, NIST CSF, audit prep |

## Other Smaller Subdomains
`application-security` (4), `supply-chain-security` (3), `deception-technology` (3), `wireless-security` (2), `red-team` (2), `privacy-compliance` (2), `offensive-security` (2), `identity-and-access-management` (2), `ai-security` (2), `zero-trust` (1), `social-engineering-defense` (1), `purple-team` (1), `ot-security` (1), `identity-security` (1), `governance-risk-compliance` (1), `firmware-security` (1), `firmware-analysis` (1), `data-protection` (1), `blockchain-security` (1)

> Some subdomains have near-duplicate names (e.g. `red-team` vs `red-teaming`, `zero-trust` vs `zero-trust-architecture`, `identity-and-access-management` vs `identity-access-management`). Reconciliation is a known cleanup target — agents should grep both spellings when searching.

## Skill Structure
Each skill lives at `cybersecurity/<skill-name>/SKILL.md`. Some skills bundle additional artifacts:
```
cybersecurity/<skill-name>/
├── SKILL.md              # required, YAML frontmatter
├── references/           # optional: workflows.md, standards.md, api-reference.md
├── scripts/              # optional: agent.py, process.py
├── assets/               # optional: templates
└── LICENSE               # optional: per-skill license
```

## For AI Agents

### Discovery (CRITICAL — do not skip)
1. Identify the subdomain from the task.
2. `grep -l "subdomain: <name>" cybersecurity/*/SKILL.md` to list candidates.
3. Read frontmatter (first ~20 lines) of candidates to pick the right one.
4. Only then read the full SKILL.md body.

### DO NOT
- Walk all 754 skill dirs.
- Load `cybersecurity/` recursively into context.
- Assume a skill exists without grepping first — many adjacent topics have dedicated skills.

## Validation
All 754 skills verified:
- ✅ Start with `---` YAML frontmatter
- ✅ Have `name`, `description`, `domain: cybersecurity`, `subdomain` fields
- ✅ Consistent naming (`<verb>-<noun>-<context>` slug)
