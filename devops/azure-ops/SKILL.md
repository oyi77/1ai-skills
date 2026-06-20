---
name: azure-ops
description: Azure operations — Virtual Machines, App Service, Azure Functions, AKS, Cosmos DB, Azure AD
domain: devops
tags:
- azure
- ci-cd
- devops
- infrastructure
- ops
---


## Overview

Azure operations covering VMs, App Service, Functions, AKS, Cosmos DB, and Azure AD for identity management.

## Capabilities

- Virtual Machine management
- App Service web hosting
- Azure Functions serverless
- AKS Kubernetes clusters
- Cosmos DB multi-model
- Azure AD identity
- ARM/Bicep templates

## When to Use

- Azure cloud management
- Enterprise identity with Azure AD
- .NET application hosting
- Hybrid cloud scenarios

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

The azure-ops workflow follows a standard pipeline pattern.

Core flow:
```
# azure-ops primary flow
input = prepare(raw_data)
result = process(input, config={azure, cosmos, functions, machines, operations})
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


### Azure CLI Deploy
```bash
az webapp create -g MyRG -p MyPlan -n MyApp --runtime "NODE:18-lts"
az functionapp create -g MyRG -p MyPlan -n MyFunc --runtime node
```

## Common Patterns

- Managed identities over secrets
- Azure Policy for compliance
- Resource locks for production
- Reserved instances for savings

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
