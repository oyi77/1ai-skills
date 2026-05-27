---
name: gcp-ops
description: Google Cloud operations — Compute Engine, Cloud Run, BigQuery, Cloud Functions, GKE, IAM
---

## Overview

Google Cloud operations covering Compute Engine, Cloud Run for containers, BigQuery for analytics, Cloud Functions, and GKE for Kubernetes.

## Capabilities

- Compute Engine VM management
- Cloud Run container deployment
- BigQuery SQL analytics
- Cloud Functions serverless
- GKE cluster management
- IAM and service accounts
- Cost management and committed use

## When to Use

- GCP infrastructure management
- Data analytics with BigQuery
- Container workloads on GKE
- Serverless with Cloud Run

## Pseudo Code

### Cloud Run Deploy
```bash
gcloud run deploy my-service   --image gcr.io/project/image   --region us-central1   --allow-unauthenticated   --memory 512Mi
```

## Common Patterns

- Use service accounts with least privilege
- Preemptible VMs for batch work
- BigQuery slots for predictable cost
- Cloud Run concurrency tuning
