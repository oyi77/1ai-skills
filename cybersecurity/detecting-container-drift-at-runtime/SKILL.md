---
name: detecting-container-drift-at-runtime
description: Detect unauthorized modifications to running containers by monitoring for binary execution drift, file system
  changes, and configuration deviations from the original container image.
domain: cybersecurity
subdomain: container-security
tags:
- container-drift
- runtime-security
- immutable-containers
- falco
- kubernetes
- container-security
- drift-detection
- microsoft-defender
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- PR.IR-01
- ID.AM-08
- DE.CM-01
---

# Detecting Container Drift at Runtime

## Overview

Container drift occurs when running containers deviate from their original image state through unauthorized file modifications, unexpected binary execution, configuration changes, or package installations. Since containers should be treated as immutable infrastructure, any drift is a potential indicator of compromise. Detection techniques leverage the DIE (Detect, Isolate, Evict) model -- an immutable workload should not change during runtime, so any observed change is potentially evidence of malicious activity.


## When to Use

- When investigating security incidents that require detecting container drift at runtime
- When building detection rules or threat hunting queries for this domain
- When SOC analysts need structured procedures for this analysis type
- When validating security monitoring coverage for related attack techniques

## Prerequisites

- Kubernetes cluster v1.24+ with runtime security tooling
- Falco or Sysdig for runtime drift detection
- Container image registry with image manifests available
- Familiarity with Linux filesystem layers and OverlayFS

## Core Concepts

This section covers core concepts for detecting container drift at runtime.

- Ensure all prerequisites are met before proceeding
- Follow the documented workflow steps in sequence
- Record results and any anomalies encountered during this phase
### Types of Container Drift

1. **Binary drift**: Execution of binaries not present in the original image (downloaded malware, compiled tools)
2. **File drift**: Creation, modification, or deletion of files in the container filesystem
3. **Configuration drift**: Changes to environment variables, mounted secrets, or runtime parameters
4. **Package drift**: Installation of new packages via apt, yum, pip, or npm at runtime
5. **Network drift**: New listening ports or outbound connections not expected for the workload

### Detection Methods

**Image-Based Comparison**: Compare the running container's filesystem against its source image to identify added, modified, or removed files.

**Behavioral Monitoring**: Use eBPF or kernel-level monitoring to detect process execution, file access, and network activity that deviates from expected behavior.

**Digest Verification**: Continuously verify that running container image digests match the approved deployment manifests.

## Implementation with Falco

This section covers implementation with falco for detecting container drift at runtime.

- Ensure all prerequisites are met before proceeding
- Follow the documented workflow steps in sequence
- Record results and any anomalies encountered during this phase
### Detecting New Binary Execution

```yaml
- rule: Drift Detected (Container Image Modified Binary)
  desc: Detect execution of a binary not present in the original container image
  condition: >
    spawned_process and
    container and
    not proc.pname in (container_entrypoint) and
    proc.is_exe_upper_layer = true
  output: >
    Drift detected: new binary executed in container
    (user=%user.name command=%proc.cmdline container=%container.name
     image=%container.image.repository:%container.image.tag
     exe_path=%proc.exepath)
  priority: WARNING
  tags: [container, drift]

- rule: Container Shell Spawned
  desc: Detect interactive shell in a container that should be immutable
  condition: >
    spawned_process and
    container and
    proc.name in (bash, sh, dash, zsh, csh, ksh) and
    not proc.pname in (container_entrypoint)
  output: >
    Shell spawned in container (user=%user.name shell=%proc.name
     container=%container.name image=%container.image.repository)
  priority: WARNING
  tags: [container, drift, shell]
```

### Detecting Package Manager Usage

```yaml
- rule: Package Manager Execution in Container
  desc: Detect use of package managers indicating drift
  condition: >
    spawned_process and
    container and
    proc.name in (apt, apt-get, yum, dnf, apk, pip, pip3, npm, gem, cargo)
  output: >
    Package manager executed in container (user=%user.name
     command=%proc.cmdline container=%container.name
     image=%container.image.repository)
  priority: ERROR
  tags: [container, drift, package-manager]
```

### Detecting File System Modifications

```yaml
- rule: Container File System Write
  desc: Detect writes to container upper layer filesystem
  condition: >
    open_write and
    container and
    fd.typechar = 'f' and
    not fd.name startswith /tmp and
    not fd.name startswith /var/log and
    not fd.name startswith /proc
  output: >
    File write in container (user=%user.name file=%fd.name
     container=%container.name)
  priority: NOTICE
  tags: [container, drift, filesystem]
```

## Implementation with Kubernetes Enforcement

This section covers implementation with kubernetes enforcement for detecting container drift at runtime.

- Ensure all prerequisites are met before proceeding
- Follow the documented workflow steps in sequence
- Record results and any anomalies encountered during this phase
### Read-Only Root Filesystem

Prevent drift by making container filesystems immutable:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: immutable-app
spec:
  template:
    spec:
      containers:
        - name: app
          image: app:v1.0@sha256:abc123...
          securityContext:
            readOnlyRootFilesystem: true
            allowPrivilegeEscalation: false
            runAsNonRoot: true
          volumeMounts:
            - name: tmp
              mountPath: /tmp
            - name: cache
              mountPath: /var/cache
      volumes:
        - name: tmp
          emptyDir:
            sizeLimit: 100Mi
        - name: cache
          emptyDir:
            sizeLimit: 50Mi
```

### Pod Security Standards Enforcement

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

## Image Digest Verification

This section covers image digest verification for detecting container drift at runtime.

- Ensure all prerequisites are met before proceeding
- Follow the documented workflow steps in sequence
- Record results and any anomalies encountered during this phase
### Continuous Digest Monitoring

```bash
#!/bin/bash
# Compare running container digests against approved manifest

NAMESPACE="production"

kubectl get pods -n "$NAMESPACE" -o json | jq -r '
  .items[] |
  .spec.containers[] |
  "\(.image) \(.imageID)"
' | while read IMAGE IMAGE_ID; do
  APPROVED_DIGEST=$(kubectl get deploy -n "$NAMESPACE" -o json | \
    jq -r ".items[].spec.template.spec.containers[] | select(.image==\"$IMAGE\") | .image")

  if [[ "$IMAGE" != *"@sha256:"* ]]; then
    echo "[WARN] Container using mutable tag: $IMAGE"
  fi
done
```

## Microsoft Defender for Containers Integration

For Azure Kubernetes environments, Microsoft Defender provides built-in binary drift detection:

```json
{
  "alertType": "K8S.NODE_ImageBinaryDrift",
  "severity": "Medium",
  "description": "Binary executed that was not part of the original container image",
  "remediationSteps": [
    "Investigate the binary origin and purpose",
    "Check if the container was compromised",
    "Rebuild the container from a clean image",
    "Enable readOnlyRootFilesystem"
  ]
}
```

## Drift Response Playbook

1. **Detect**: Alert fires on drift event (Falco, Defender, Sysdig)
2. **Validate**: Confirm the drift is not from an approved process (init containers, config reloads)
3. **Isolate**: Apply a deny-all NetworkPolicy to the affected pod
4. **Investigate**: Capture container filesystem diff and process list
5. **Evict**: Delete the drifted pod (ReplicaSet will recreate from clean image)
6. **Remediate**: Fix the root cause (patch vulnerability, update image, tighten RBAC)

## When NOT to Use

- You need to perform the attack to test detection (use performing-* skills)
- Task is about analyzing past incidents (use analyzing-* skills)
- You need to implement detection rules (use implementing-* skills)
- Task is about threat hunting proactively (use hunting-* skills)
- You don't have access to logs or monitoring data
- Task requires incident response (use IR skills)


## Red Flags

- Performing actions without explicit written authorization from the asset owner
- Testing against production systems without a defined scope and rules of engagement
- Modifying cloud IAM policies or security groups without approval
- Exposing cloud credentials or secrets in logs or reports
- Running scans that generate excessive API calls and trigger billing alerts

## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- Cloud resource changes reverted or documented as intentional
- IAM policies reviewed for least-privilege compliance after testing
- No residual test resources left running (cost and security check)

## References

- [Container Drift Detection with Falco - Sysdig](https://www.sysdig.com/blog/container-drift-detection-with-falco)
- [Microsoft Defender for Containers Drift Detection](https://techcommunity.microsoft.com/blog/microsoftdefendercloudblog/detect-container-drift-with-microsoft-defender-for-containers/4232044)
- [Ensure Immutability of Containers at Runtime](https://notes.kodekloud.com/docs/Certified-Kubernetes-Security-Specialist-CKS/Monitoring-Logging-and-Runtime-Security/Ensure-Immutability-of-Containers-at-Runtime/)
- [Falco Runtime Security](https://falco.org/)

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |