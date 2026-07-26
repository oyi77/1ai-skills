---
name: k8s-deploy
description: Use when kubernetes deployment — merged into docker-devops parent. See ../SKILL.md for money protocol.
domain: devops
tags: [devops, k8s, kubernetes]
version: 1.0.0
---

# K8S Deploy

This skill has been merged into the parent docker-devops skill.

See the comprehensive merged skill at [../SKILL.md](../SKILL.md) for full documentation including money-making protocol, real YAML/Python examples, and orchestration flow.

Key capabilities moved:
- Complete K8s manifest set: Deployment, Service, HPA, ConfigMap, Ingress
- Rolling update strategy with liveness + readiness probes
- GitHub Actions CI/CD workflow (build → push → deploy)
- Full deploy script (`deploy-full-stack.sh`) from compose to k8s rollout
- Kustomize overlay structure for staging/production separation



## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll figure it out as I go" | A structured approach saves time and reduces errors. Follow the workflow in this skill rather than improvising. |
| "I already know this topic" | Familiarity breeds shortcuts. Use the checklist to verify you haven't missed critical steps. |
| "This doesn't apply to my situation" | The patterns here generalize across contexts. Adapt, don't skip — the underlying principles hold. |
| "One more tool will fix it" | Adding complexity rarely solves process gaps. Master the core workflow first. |

## When to Use
Use this skill when working with k8s deploy.


## Workflow
See the parent skill for authoritative workflow documentation.
