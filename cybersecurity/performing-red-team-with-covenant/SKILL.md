---
name: performing-red-team-with-covenant
description: Conduct red team operations using the Covenant C2 framework for authorized adversary simulation, including listener
  setup, grunt deployment, task execution, and lateral movement tracking.
domain: cybersecurity
subdomain: red-team
tags:
- red-team
- c2
- covenant
- adversary-simulation
- penetration-testing
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- ID.RA-01
- GV.OV-02
- DE.AE-07
---
# Performing Red Team Operations with Covenant C2

## Overview

Covenant is a collaborative .NET C2 framework for red teamers that provides a Swagger-documented REST API for managing listeners, launchers, grunts (agents), and tasks. This skill covers automating Covenant operations through its API for authorized red team engagements: creating HTTP/HTTPS listeners, generating binary and PowerShell launchers, deploying grunts, executing tasks on compromised hosts, and tracking lateral movement.


## When to Use

- When conducting security assessments that involve performing red team with covenant
- When following incident response procedures for related security events
- When performing scheduled security testing or auditing activities
- When validating security controls through hands-on testing

## Prerequisites

- Covenant C2 server deployed (Docker or .NET 6)
- Python 3.9+ with `requests` library
- Covenant API token (obtained via /api/users/login)
- Written authorization for red team engagement
- Isolated lab or authorized target environment

## Steps

1. **Scope and authorize** — confirm written authorization and define target boundaries
2. **Reconnaissance** — enumerate targets, services, and potential attack surfaces
3. **Exploitation** — attempt exploitation of identified vulnerabilities within scope
4. **Post-exploitation** — document access level, lateral movement, and data exposure
5. **Report and remediate** — compile findings with reproduction steps and fix recommendations
### Step 1: Authenticate to Covenant API
Obtain a JWT token by posting credentials to /api/users/login endpoint.

### Step 2: Create Listener
Configure an HTTP or HTTPS listener with callback URLs and bind address.

### Step 3: Generate Launcher
Create a binary, PowerShell, or MSBuild launcher tied to the listener for grunt deployment.

### Step 4: Deploy and Manage Grunts
Monitor grunt callbacks, execute tasks, and collect output from compromised hosts.

### Step 5: Document Operations
Generate an operations report documenting all actions, timestamps, and findings.

## Expected Output

JSON report with listener configuration, active grunts, executed tasks, and task output for engagement documentation.
## When NOT to Use

- You don't have explicit written authorization to test
- Task is about defense/detection, not offense (use detection skills)
- You need to implement security controls (use implementing-* skills)
- Task requires compliance auditing (use auditing-* skills)
- You're investigating an incident (use incident response skills)
- Target is out of scope for your engagement
- Task is about vulnerability scanning only (use scanning tools)


## Red Flags

- Performing actions without explicit written authorization from the asset owner
- Testing against production systems without a defined scope and rules of engagement
- Exceeding the authorized scope of the engagement
- Leaving persistent access mechanisms without explicit approval
- Causing denial-of-service on production systems during testing
## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- All exploited vulnerabilities documented with reproduction steps
- Scope boundaries confirmed — only authorized targets were tested
- Remediation recommendations included for every finding
