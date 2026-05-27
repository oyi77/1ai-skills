---
name: tekton-pipelines
description: Tekton CI/CD pipelines — Tasks, Pipelines, Triggers, Workspaces for Kubernetes-native CI
---

## Overview

Tekton is a Kubernetes-native CI/CD framework. Tasks define individual steps, Pipelines compose Tasks, Triggers respond to events, and Workspaces share data between steps.

## Capabilities

- Kubernetes-native CI/CD primitives
- Reusable Tasks and Pipelines from Tekton Hub
- Event-based triggers with webhooks
- Workspaces for data sharing between steps
- Custom Task types for specialized workloads
- Dashboard for pipeline visualization

## When to Use

- Running CI/CD on Kubernetes clusters
- Need cloud-native, vendor-neutral pipeline definitions
- Want reusable, composable CI/CD building blocks
- Building platform engineering CI/CD foundations

## Pseudo Code

### Task Definition
```yaml
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: build-and-push
spec:
  params:
    - name: image
      type: string
  workspaces:
    - name: source
  steps:
    - name: build
      image: gcr.io/kaniko-project/executor:latest
      args:
        - --dockerfile=$(workspaces.source.path)/Dockerfile
        - --context=$(workspaces.source.path)
        - --destination=$(params.image)
```

### Pipeline Definition
```yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: build-test-deploy
spec:
  params:
    - name: image
      type: string
  workspaces:
    - name: shared-workspace
  tasks:
    - name: clone
      taskRef:
        name: git-clone
      workspaces:
        - name: output
          workspace: shared-workspace
    - name: build
      taskRef:
        name: build-and-push
      runAfter: [clone]
      params:
        - name: image
          value: $(params.image)
      workspaces:
        - name: source
          workspace: shared-workspace
    - name: test
      taskRef:
        name: run-tests
      runAfter: [build]
      workspaces:
        - name: source
          workspace: shared-workspace
```

### Trigger (Webhook)
```yaml
apiVersion: triggers.tekton.dev/v1beta1
kind: TriggerTemplate
metadata:
  name: build-on-push
spec:
  resourcetemplates:
    - apiVersion: tekton.dev/v1beta1
      kind: PipelineRun
      metadata:
        name: build-$(uid)
      spec:
        pipelineRef:
          name: build-test-deploy
        params:
          - name: image
            value: registry.example.com/app:$(tt.params.git-sha)
```

## Common Patterns

- **Task Hub**: `tkn hub search git-clone` — find community Tasks
- **Workspaces**: PVC for persistent data, ConfigMap for config, emptyDir for temp
- **Results**: Tasks can output results consumed by downstream Tasks
- **When expressions**: `when: [{ input: "$(params.run-tests)", operator: in, values: ["true"] }]`
- **Sidecars**: Run services alongside Tasks (e.g., Docker-in-Docker)
