---
name: decepticon-red-team
description: Autonomous red team agent executing full attack chains with domain specialists. Use when running autonomous red team operations, simulating end-to-end attack chains, or planning engagements with MITRE ATT&CK mapping.
domain: cybersecurity
subdomain: red-teaming
tags:
- red-team
- autonomous
- attack-chain
- mitre-attack
- engagement-planning
---

# Decepticon Red Team

## Overview

Decepticon is an autonomous red team agent that executes full attack chains end-to-end. It operates as an AI-driven adversary simulation platform with domain specialists for Active Directory, cloud, smart contracts, reverse engineering, and analysis. Engagement packages structure operations around RoE, ConOps, and OPPLAN with MITRE ATT&CK mapping.

**Source:** https://github.com/PurpleAILAB/Decepticon
**Architecture:** Modular kill chain with domain-specialist agents
**License:** Open source

## When to Use

- Autonomous red teaming of infrastructure
- Full attack chain simulation from recon to post-exploitation
- Engagement planning with structured packages (RoE, ConOps, OPPLAN)
- MITRE ATT&CK technique mapping and adversary emulation
- Multi-domain assessments (AD + cloud + application)

## Kill Chain Phases

This section covers kill chain phases for decepticon red team.

- Ensure all prerequisites are met before proceeding
- Follow the documented workflow steps in sequence
- Record results and any anomalies encountered during this phase
### 1. Orchestration
Central planning engine that coordinates all phases. Determines attack strategy, allocates resources across domain specialists, and adapts the plan based on findings at each phase.

### 2. Reconnaissance
Automated target discovery and profiling:
- Passive OSINT (DNS, WHOIS, certificate transparency, social media)
- Active enumeration (subdomains, ports, services, technology fingerprinting)
- Attack surface mapping and priority ranking
- Credential harvesting from public breach databases

### 3. Exploitation
Vulnerability exploitation and initial access:
- Web application exploitation (OWASP Top 10)
- Network service exploitation (known CVEs, misconfigurations)
- Phishing payload delivery and social engineering
- Credential-based access (password spraying, default creds)

### 4. Post-Exploitation
Establishing persistence and expanding access:
- Privilege escalation (local and domain)
- Lateral movement across network segments
- Credential harvesting from memory and storage
- Data staging for exfiltration
- Persistence mechanism installation

### 5. Vulnerability Research
Deep-dive vulnerability discovery:
- Custom fuzzing based on discovered services
- Zero-day research on proprietary applications
- Binary analysis and reverse engineering
- Smart contract auditing for DeFi targets

### 6. Domain Specialists

#### Active Directory Specialist
- Kerberoasting and AS-REP roasting
- DCSync and DCShadow attacks
- Delegation abuse (constrained, unconstrained, RBCD)
- Certificate abuse (ESC1-ESC8)
- GPO exploitation and ACL abuse

#### Cloud Specialist
- AWS/GCP/Azure misconfiguration exploitation
- IAM privilege escalation paths
- Metadata service abuse
- Storage bucket enumeration and access
- Serverless function exploitation

#### Smart Contract Specialist
- Solidity vulnerability detection
- Flash loan attack simulation
- Reentrancy, overflow, access control flaws
- DeFi protocol attack path analysis
- Token economics manipulation

#### Reverse Engineering Specialist
- Binary analysis and vulnerability identification
- Malware analysis and capability extraction
- Firmware extraction and analysis
- Protocol reverse engineering
- Obfuscation and packing defeat

#### Analyst Specialist
- Finding correlation and impact assessment
- MITRE ATT&CK technique mapping
- Risk scoring and prioritization
- Detection gap analysis (what would blue team catch?)
- Executive summary generation

## Engagement Packages

This section covers engagement packages for decepticon red team.

- Ensure all prerequisites are met before proceeding
- Follow the documented workflow steps in sequence
- Record results and any anomalies encountered during this phase
### Rules of Engagement (RoE)
Structured boundaries for the operation:
- Authorized targets and IP ranges
- Prohibited actions and data handling rules
- Communication channels and escalation paths
- Working hours and emergency contacts
- Legal authorization references

### Concept of Operations (ConOps)
High-level operational approach:
- Attack strategy and phases
- Resource allocation across specialists
- Timeline and milestones
- Success criteria and abort conditions
- Coordination with blue team (if purple team)

### Operational Plan (OPPLAN)
Detailed execution plan with MITRE ATT&CK mapping:

| Phase | Technique | ATT&CK ID | Specialist | Priority |
|-------|-----------|------------|------------|----------|
| Recon | Active Scanning | T1595 | Orchestrator | High |
| Initial Access | Phishing | T1566 | Social Eng | Medium |
| Execution | Command Scripting | T1059 | Orchestrator | High |
| Persistence | Scheduled Task | T1053 | AD Specialist | Medium |
| Priv Esc | Exploitation | T1068 | RE Specialist | High |
| Lateral Move | Remote Services | T1021 | AD Specialist | High |
| Collection | Data Staged | T1074 | Analyst | Medium |
| Exfil | Exfil Over C2 | T1041 | Orchestrator | Low |

## Installation

```bash
# Install required dependencies
sudo apt-get update && sudo apt-get install -y <tool-name>
```
### Docker
```bash
git clone https://github.com/PurpleAILAB/Decepticon.git
cd Decepticon
docker build -t decepticon .
docker run -it decepticon
```

### Pip
```bash
git clone https://github.com/PurpleAILAB/Decepticon.git
cd Decepticon
pip install -r requirements.txt
python main.py
```

## Workflow Example

```
1. Define engagement: scope, rules, objectives
2. Generate RoE + ConOps + OPPLAN packages
3. Run reconnaissance phase (automated)
4. Review recon findings, adjust OPPLAN
5. Execute exploitation phase (specialist-driven)
6. Post-exploitation and lateral movement
7. Analyst correlates findings with ATT&CK
8. Generate final report with detection gaps
```

## Red Flags

- Autonomous execution requires strict RoE enforcement
- Always verify scope boundaries before exploitation phases
- Smart contract testing must use testnets unless authorized
- Real credentials and data handling must follow engagement rules
- Ensure kill switch / abort mechanism is available at all phases
## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- All exploited vulnerabilities documented with reproduction steps
- Scope boundaries confirmed — only authorized targets were tested
- Remediation recommendations included for every finding
