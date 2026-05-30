---
name: implementing-syslog-centralization-with-rsyslog
description: Configure rsyslog for centralized log collection with TLS encryption, custom templates, and log rotation. Generates
  server and client configuration files with GnuTLS stream drivers, x509 certificate authentication, per-host log segregation,
  and reliable queue settings for high-availability syslog infrastructure.
domain: cybersecurity
subdomain: security-operations
tags:
- implementing
- syslog
- centralization
- with
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- DE.CM-01
- RS.MA-01
- GV.OV-01
- DE.AE-02
---


# Implementing Syslog Centralization with Rsyslog


## When to Use

- When deploying or configuring implementing syslog centralization with rsyslog capabilities in your environment
- When establishing security controls aligned to compliance requirements
- When building or improving security architecture for this domain
- When conducting security assessments that require this implementation

## Prerequisites

- Familiarity with security operations concepts and tools
- Access to a test or lab environment for safe execution
- Python 3.8+ with required dependencies installed
- Appropriate authorization for any testing activities

## Instructions

1. Install dependencies: `pip install jinja2 paramiko`
2. Generate TLS certificates for rsyslog server and clients using OpenSSL.
3. Run the agent to generate rsyslog server and client configurations:
   - Server: TLS listener on port 6514, per-host directory output, JSON-format templates
   - Client: TLS forwarding with disk-assisted queues for reliability
4. Deploy configurations to servers via SSH (paramiko).
5. Validate TLS connectivity and log delivery.

```bash
python scripts/agent.py --server-ip 10.0.0.1 --clients 10.0.0.10,10.0.0.11 --ca-cert ca.pem --output syslog_report.json
```

## Examples

```bash
# Basic usage example
# Replace with domain-specific commands from the workflow above
```
### Server Configuration (TLS)
```
module(load="imtcp" StreamDriver.Name="gtls" StreamDriver.Mode="1"
       StreamDriver.Authmode="x509/name")
input(type="imtcp" port="6514")
template(name="PerHostLog" type="string" string="/var/log/remote/%HOSTNAME%/%PROGRAMNAME%.log")
*.* ?PerHostLog
```

### Client Configuration (Reliable Forwarding)
```
action(type="omfwd" target="10.0.0.1" port="6514" protocol="tcp"
       StreamDriver="gtls" StreamDriverMode="1"
       StreamDriverAuthMode="x509/name"
       queue.type="LinkedList" queue.filename="fwdRule1"
       queue.maxdiskspace="1g" queue.saveonshutdown="on"
       action.resumeRetryCount="-1")
```
## When NOT to Use

- You need to test the implementation (use performing-* skills)
- Task is about configuring existing tools (use configuring-* skills)
- You need to analyze security events (use analyzing-* skills)
- Task is about building detection rules (use building-* skills)
- You don't have access to the target environment
- Task requires vendor-specific expertise (consult vendor docs)


## Red Flags

- Performing actions without explicit written authorization from the asset owner
- Testing against production systems without a defined scope and rules of engagement
- Sharing sensitive findings or credentials in unencrypted communications
- Failing to properly scope and contain the assessment before starting
## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- Results validated against known-good baselines or reference implementations
- Documentation complete enough for another analyst to reproduce findings
