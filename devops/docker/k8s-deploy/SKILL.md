---
name: k8s-deploy
description: Use when kubernetes deployment — merged into docker-devops parent. See ../SKILL.md for money protocol.
domain: devops
tags: [devops, k8s, kubernetes]
version: 1.0.0
---

# K8s Deploy — Quick Reference

**Role:** Kubernetes deployment is the production layer of the container pipeline. This sub-skill covers writing K8s manifests (Deployment, Service, HPA, ConfigMap, Ingress), managing rollouts (rolling update, rollback), configuring probes (liveness, readiness, startup), using Horizontal Pod Autoscalers, and integrating GitOps workflows (ArgoCD/Flux). It assumes you already have containerized applications from the parent Docker skill.

## Quick Start

### 1. Deploy a Stateless App
The minimal deployment + service + ingress for any containerized app:

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  namespace: production
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  selector:
    matchLabels:
      app: app
  template:
    metadata:
      labels:
        app: app
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
      containers:
        - name: app
          image: registry.example.com/app:latest
          ports:
            - containerPort: 3000
              name: http
          livenessProbe:
            httpGet: { path: /health, port: http }
            initialDelaySeconds: 10
            periodSeconds: 15
          readinessProbe:
            httpGet: { path: /ready, port: http }
            initialDelaySeconds: 5
            periodSeconds: 10
          resources:
            requests: { cpu: "250m", memory: "256Mi" }
            limits: { cpu: "500m", memory: "512Mi" }
```

### 2. Quick Rollout & Rollback
Update the image and monitor the rollout:

```bash
kubectl set image deployment/app app=registry.example.com/app:abc123 -n production
kubectl rollout status deployment/app -n production --timeout=5m

# If the rollout is broken, rollback:
kubectl rollout undo deployment/app -n production
kubectl rollout history deployment/app -n production  # see all revisions
```

### 3. Horizontal Pod Autoscaler
Scale pods automatically based on CPU/memory:

```yaml
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

## One Focused Code Snippet — Deploy Status Bash Function

```bash
k8s-status() {
  local ns="${1:-production}"
  echo "=== Deployments ==="
  kubectl get deployments -n "$ns" -o wide
  echo ""
  echo "=== Pods ==="
  kubectl get pods -n "$ns" -o wide --sort-by='.status.startTime'
  echo ""
  echo "=== HPA ==="
  kubectl get hpa -n "$ns"
  echo ""
  echo "=== Recent Events ==="
  kubectl get events -n "$ns" --sort-by='.lastTimestamp' | tail -10
}
```

## Checklist

- [ ] RollingUpdate strategy (not Recreate) configured for zero-downtime deploys
- [ ] Liveness + readiness probes configured on every container — K8s routes traffic based on readiness, restarts on liveness failure
- [ ] Resource requests AND limits set — missing requests → oversubscription; missing limits → runaway pods
- [ ] HPA configured with CPU and memory targets, minReplicas ≥ 2 for HA
- [ ] Security context: runAsNonRoot, no privileged containers, readOnlyRootFilesystem where possible

## When to Use

Use when kubernetes deployment — merged into docker-devops parent. See ../SKILL.md for money protocol.

## Workflow

Execute these steps sequentially:

### 1. Deploy a Stateless App
The minimal deployment + service + ingress for any containerized app:

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  namespace: production
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  selector:
    matchLabels:
      app: app
  template:
    metadata:
      labels:
        app: app
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
      containers:
        - name: app
          image: registry.example.com/app:latest
          ports:
            - containerPort: 3000
              name: http
          livenessProbe:
            httpGet: { path: /health, port: http }
            initialDelaySeconds: 10
            periodSeconds: 15
          readinessProbe:
            httpGet: { path: /ready, port: http }
            initialDelaySeconds: 5
            periodSeconds: 10
          resources:
            requests: { cpu: "250m", memory: "256Mi" }
            limits: { cpu: "500m", memory: "512Mi" }
```

### 2. Quick Rollout & Rollback
Update the image and monitor the rollout:

```bash
kubectl set image deployment/app app=registry.example.com/app:abc123 -n production
kubectl rollout status deployment/app -n production --timeout=5m

# If the rollout is broken, rollback:
kubectl rollout undo deployment/app -n production
kubectl rollout history deployment/app -n production  # see all revisions
```

### 3. Horizontal Pod Autoscaler
Scale pods automatically based on CPU/memory:

```yaml
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Recreate strategy is simpler" | Recreate kills all pods before starting new ones — guaranteed downtime for anything behind a Service. RollingUpdate doesn't cost more and avoids outages. |
| "I'll add probes after it works" | Without probes, K8s sends traffic to a starting container before it's ready. Each request during that window fails. Probes are not optimizations; they're correctness. |
| "HPA is for big deployments only" | HPA costs nothing to configure and prevents the most common outage: a traffic spike hitting fixed replicas. Set min=2 max=10 on every deployment. |

