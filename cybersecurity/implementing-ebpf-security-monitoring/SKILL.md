---
name: implementing-ebpf-security-monitoring
description: 'Use when implements eBPF-based security monitoring using Cilium Tetragon
  for real-time process execution tracking, network connection observability, file
  access auditing, and runtime enforcement. Covers TracingPolicy CRD authoring with
  kprobe/tracepoint hooks, in-kernel filtering via matchArgs/matchBinaries selectors,
  JSON event export, and integration with SIEM pipelines. Use when building kernel-level
  runtime security observability for Linux hosts or Kubernetes clusters.

  '
domain: cybersecurity
tags:
- implementing
- ebpf
- security
- monitoring
- tetragon
- cilium
- runtime
- observability
subdomain: security-operations
version: '1.0'
author: oyi77
license: Apache-2.0
nist_ai_rmf:
- MEASURE-2.7
- MAP-5.1
- MANAGE-2.4
atlas_techniques:
- AML.T0070
- AML.T0066
- AML.T0082
nist_csf:
- DE.CM-01
- RS.MA-01
- GV.OV-01
- DE.AE-02
category: cybersecurity
---

# Implementing Ebpf Security Monitoring

## Overview

Cybersecurity skill for implementing ebpf security monitoring. Follows industry best practices and security standards.

## When to Use

**Trigger phrases:**
- "implementing ebpf security monitoring"
- "When deploying kernel-level runtime security monitoring on Linux hosts or Kubern"
- "When you need sub-millisecond visibility into process execution, network connect"
- "When traditional userspace monitoring tools introduce unacceptable performance o"


- When deploying kernel-level runtime security monitoring on Linux hosts or Kubernetes clusters
- When you need sub-millisecond visibility into process execution, network connections, and file access
- When traditional userspace monitoring tools introduce unacceptable performance overhead
- When building detection pipelines that require in-kernel filtering before events reach userspace
- When enforcing runtime security policies (kill process, send signal) at the kernel level


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Linux kernel 5.3+ with BTF (BPF Type Format) support enabled
- Kubernetes 1.24+ cluster (for Kubernetes deployment) or standalone Linux host
- Helm 3.x installed (for Kubernetes deployment)
- `kubectl` configured with cluster access
- `tetra` CLI installed for local event streaming
- Python 3.8+ with `requests`, `kubernetes`, `pyyaml` dependencies
- Root or CAP_BPF/CAP_SYS_ADMIN capabilities for eBPF program loading

## Workflow

1. **Define detection objective** — choose one observable behavior (executable from `/tmp`, reverse shell from a web process, or sensitive file read) and map it to ATT&CK and required hooks.
2. **Verify telemetry coverage** — confirm kernel/BTF support and that the collector sees required kprobe/tracepoint events before writing rules.
3. **Write kernel-level detection** — use kprobe/tracepoint hooks plus `matchArgs`/`matchBinaries` filtering to avoid shipping every event to userspace.
4. **Test in isolation** — run the behavior in an authorized lab; confirm expected events without destabilizing the host.
5. **Deploy with canary** — roll out to a small host set; monitor CPU, memory, and verifier/load impact.
6. **Alert and respond** — send PID, PPID, command line, process tree, container ID, and host context to the SIEM; define false-positive handling.
7. **Update or retire** — re-test after kernel/runtime changes and retire detections that no longer add value.

## Tools

- **Tetragon / Cilium** — Kubernetes-aware eBPF runtime security
- **BPF Compiler Collection (BCC)** — eBPF program development
- **bpftrace** — rapid kernel tracing and prototyping
- **bpftool** — inspect BPF programs, maps, and BTF
- **kubectl / tetra CLI** — policy deployment and event streaming

## Verification

- [ ] Kernel/BTF prerequisites verified on every target host
- [ ] TracingPolicy filters events in-kernel; userspace volume bounded
- [ ] Detection tested against a known behavior in an authorized lab
- [ ] Canary rollout shows acceptable CPU/memory/verifier impact
- [ ] Events include process/container context and reach the SIEM
- [ ] False positives documented with narrow, reviewed exclusions
- [ ] Kernel upgrade and retirement plan recorded

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |