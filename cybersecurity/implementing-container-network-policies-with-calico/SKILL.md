---
name: implementing-container-network-policies-with-calico
description: Enforce Kubernetes network segmentation using Calico CNI network policies and global network policies to control
  pod-to-pod traffic, restrict egress, and implement zero-trust microsegmentation.
domain: cybersecurity
subdomain: container-security
tags:
- container-security
- kubernetes
- calico
- network-policy
- microsegmentation
- cni
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- PR.IR-01
- ID.AM-08
- DE.CM-01
---
# Implementing Container Network Policies with Calico

## Overview

Calico provides Kubernetes-native and extended network policy enforcement through its CNI plugin. This skill covers creating and auditing Calico NetworkPolicy and GlobalNetworkPolicy resources to implement pod-to-pod traffic control, namespace isolation, egress restrictions, and DNS-based policy rules using calicoctl and the Kubernetes API.


## When to Use

- When deploying or configuring implementing container network policies with calico capabilities in your environment
- When establishing security controls aligned to compliance requirements
- When building or improving security architecture for this domain
- When conducting security assessments that require this implementation

## Prerequisites

- Kubernetes cluster with Calico CNI installed
- Python 3.9+ with `kubernetes` client library
- calicoctl CLI tool installed and configured
- kubectl access with RBAC permissions for network policy management

## Steps

1. **Scope the task** — define objectives, boundaries, and success criteria
2. **Gather information** — collect all necessary data and context before proceeding
3. **Execute the core workflow** — follow the domain-specific steps methodically
4. **Validate results** — verify outputs against expected outcomes or baselines
5. **Document findings** — record results, anomalies, and recommendations
### Step 1: Audit Existing Network Policies
Use calicoctl and kubectl to inventory current network policies and identify unprotected namespaces.

### Step 2: Implement Default-Deny Policies
Create default-deny ingress and egress policies per namespace as a zero-trust baseline.

### Step 3: Create Workload-Specific Allow Rules
Define granular allow rules for legitimate pod-to-pod and pod-to-service communication.

### Step 4: Validate Policy Enforcement
Test connectivity between pods to verify policies are correctly enforced.

## Expected Output

JSON audit report listing all network policies, unprotected namespaces, policy rule counts, and connectivity test results.
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
- Capturing traffic on networks without authorization or privacy considerations
- Leaving packet captures containing sensitive data unencrypted on disk
- Deploying inline blocking rules without testing for false positives first
## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- Captures verified as complete with no dropped packets
- Detection rules tested against known-benign traffic for false positive rate
- Alert thresholds validated and tuned to reduce noise
