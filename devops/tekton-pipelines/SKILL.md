---
name: tekton-pipelines
description: Tekton CI/CD pipelines — Tasks, Pipelines, Triggers, Workspaces for Kubernetes-native CI. Use when working with tekton pipelines.
domain: devops
tags:
- ci-cd
- devops
- infrastructure
- kubernetes
- pipeline
- pipelines
- tekton
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

**Trigger phrases:**
- "tekton pipelines"
- "Running CI/CD on Kubernetes clusters"
- "Need cloud-native, vendor-neutral pipeline definitions"
- "Want reusable, composable CI/CD building blocks"


- Running CI/CD on Kubernetes clusters
- Need cloud-native, vendor-neutral pipeline definitions
- Want reusable, composable CI/CD building blocks
- Building platform engineering CI/CD foundations

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

The tekton-pipelines workflow follows a standard pipeline pattern.

Core flow:
```
# tekton-pipelines primary flow
input = prepare(raw_data)
result = process(input, config={kubernetes, native, pipelines, tasks, tekton})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


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

## How to Use

1. Define infrastructure as code (Terraform, CloudFormation, Pulumi)
2. Review changes through PR process before applying
3. Configure monitoring and alerting for critical paths
4. Set up secrets management (Vault, AWS Secrets Manager, etc.)
5. Document runbooks for deployment, rollback, and incident response
6. Test disaster recovery procedures regularly

## Red Flags

- **Infrastructure changes without review**: Unreviewed changes cause outages — use PRs for infra code
- **No rollback strategy**: Every deployment needs a tested rollback plan before it runs
- **Secrets in configuration files**: Secrets in YAML/JSON get committed to version control
- **Missing monitoring and alerting**: Without monitoring, outages go undetected until users report them
- **No documentation for runbooks**: Without runbooks, on-call engineers waste time re-discovering procedures

## Verification

- [ ] Skill output matches expected behavior

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Manual deployments are fine" | Manual deployments are error-prone and不可 repeatable. Automate. |
| "We do not need monitoring" | Without monitoring, you are flying blind. Add observability from day one. |
| "Infrastructure as code is overkill" | IaC enables reproducibility, version control, and disaster recovery. |