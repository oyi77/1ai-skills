---
name: azure-ops
description: Azure operations — Virtual Machines, App Service, Azure Functions, AKS, Cosmos DB, Azure AD
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

## Pseudo Code

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
