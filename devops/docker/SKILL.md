---
name: docker
description: Use when full-stack DevOps pipeline — Docker Compose for local dev, Dockerfile optimization for production images, Kubernetes deployment for scale. Turn container ops into a service business.
domain: devops
author: mahipal
license: Apache-2.0
subdomain: devops
tags:
  - devops
  - docker
  - compose
  - kubernetes
  - k8s
  - ci-cd
  - dockerfile
  - money-making
version: 1.0.0
---

# DevOps Money Protocol — Compose, Optimize, Deploy



## When Not to Use

- **Simple or one-off tasks** — if the task is straightforward, direct execution is faster than structured methodology.
- **Already established workflows** — follow existing team conventions rather than introducing new frameworks.
- **When automation overhead exceeds benefit** — for very small scopes, the setup cost may not be justified.


## Dependencies

- Python 3.8+ or Node.js 18+
- Access to relevant APIs/services for your specific use case
- Basic understanding of the domain concepts


## Commands

```bash
# Refer to the skill's usage section for specific commands
# Adapt these to your workflow
```
## Money-Making Overview

| Service | Client Price | Your Time | ROI |
|---------|-------------|-----------|-----|
| Docker Compose setup (multi-service) | $500–$1,500 | 1–3 hrs | $300–$500/hr |
| Dockerfile audit & optimization | $300–$1,000 | 30 min–1 hr | $400–$1,000/hr |
| CI/CD pipeline with docker build | $800–$3,000 | 2–5 hrs | $300–$600/hr |
| K8s deployment (single service) | $1,000–$4,000 | 3–8 hrs | $300–$500/hr |
| Full infra (compose→Dockerfile→k8s) | $3,000–$10,000 | 6–15 hrs | $400–$700/hr |

**Target clients:** SaaS startups, agencies, e-commerce teams who have code but no container pipeline. They deploy via SSH and pray. You fix that.

**Delivery model:** Fixed-price per environment (dev/staging/prod) or hourly consulting at $200–$400/hr.

## Combined Capabilities

| Capability | Entry Point | Optimization | Production |
|-----------|------------|-------------|-----------|
| **Docker Compose** | Multi-service YAML | Volume mounts, health checks, networks | Production-ready profiles |
| **Dockerfile** | Working build | Multi-stage, layer caching, distroless | Slim image (<100 MB) |
| **K8s Deployment** | YAML manifests | HPA, resource limits, probes | GitOps (ArgoCD/Flux) |

## Concrete Action Flow

### Phase 1: Docker Compose — Rapid Local Dev (30 min)

```yaml
# docker-compose.yml — multi-service with health checks and volumes
version: "3.9"

x-logging: &default-logging
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: development
    ports:
      - "${PORT:-3000}:3000"
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgres://user:pass@db:5432/app
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 5s
      retries: 3
    logging: *default-logging

  db:
    image: postgres:16-alpine
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=app
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 5s
      timeout: 3s
      retries: 5
    logging: *default-logging

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

volumes:
  pgdata:
  redis-data:
```

```python
#!/usr/bin/env python3
"""compose-init.py — Scaffold docker-compose.yml for client projects."""
import sys, json
from pathlib import Path

TEMPLATES = {
    "web+postgres": {
        "services": ["app", "db"],
        "file": "docker-compose.yml",
    },
    "web+postgres+redis": {
        "services": ["app", "db", "redis"],
        "file": "docker-compose.yml",
    },
    "api+mysql+redis": {
        "services": ["api", "mysql", "redis"],
        "file": "docker-compose.yml",
    },
}

def scaffold_compose(project_type: str, output: str = "."):
    """Scaffold a docker-compose.yml for common stacks."""
    if project_type not in TEMPLATES:
        print(f"Available: {', '.join(TEMPLATES.keys())}")
        sys.exit(1)
    src = Path(__file__).parent / f"templates/{project_type}/docker-compose.yml"
    dst = Path(output) / "docker-compose.yml"
    if src.exists():
        dst.write_text(src.read_text())
        print(f"Wrote {dst}")
    else:
        print(f"Template {project_type} not found. Creating manually.")

if __name__ == "__main__":
    scaffold_compose(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else ".")
```

### Phase 2: Dockerfile Optimization (1 hr)

Key optimization rules:
1. **Multi-stage builds** — Builder stage has dev tools, runtime stage has only binaries
2. **Layer ordering** — Least-changing layers first (deps → config → code)
3. **Distroless base** — No shell, no package manager, smaller attack surface
4. **`.dockerignore`** — Exclude node_modules, .git, .env, __pycache__

```dockerfile
# Dockerfile — Multi-stage production build

# ---- Stage 1: Build ----
FROM node:20-alpine AS builder
WORKDIR /build

# Dependency layer (cached until lockfile changes)
COPY package.json package-lock.json* ./
RUN npm ci --only=production --ignore-scripts

# Source layer (cached until source changes)
COPY . .
RUN npm run build

# ---- Stage 2: Production ----
FROM node:20-alpine AS production
WORKDIR /app

# Add non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy only production artifacts
COPY --from=builder /build/dist ./dist
COPY --from=builder /build/node_modules ./node_modules
COPY --from=builder /build/package.json ./

USER appuser
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', r => process.exit(r.statusCode !== 200 ? 1 : 0))" \
  || exit 1

CMD ["node", "dist/index.js"]
```

```dockerfile
# Alternative: Python with pip
FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt ./
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.12-slim AS production
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY --from=builder /build/requirements.txt ./
COPY src/ ./src
ENV PATH=/root/.local/bin:$PATH
RUN adduser --disabled-password --gecos "" appuser
USER appuser
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```


```python
#!/usr/bin/env python3
"""dockerfile-optimize.py — Analyze and suggest Dockerfile improvements."""
import re, sys
from pathlib import Path


def analyze_dockerfile(path: str) -> list[dict]:
    """Analyze a Dockerfile and return optimization suggestions."""
    content = Path(path).read_text()
    lines = content.split("\n")
    findings = []

    # Check multi-stage
    if content.count("FROM ") > 1:
        stages = re.findall(r"FROM\s+\S+\s+AS\s+(\w+)", content, re.I)
        if len(stages) >= 2:
            findings.append({"severity": "info", "line": 0, "message": f"Multi-stage build with {len(stages)} stages: {', '.join(stages)}"})
    else:
        findings.append({"severity": "warn", "line": 0, "message": "Single-stage build. Use multi-stage to reduce final image size."})

    # Check base image
    for i, line in enumerate(lines, 1):
        m = re.match(r"FROM\s+(\S+)", line)
        if m:
            img = m.group(1)
            if "alpine" not in img and "slim" not in img and "distroless" not in img and "scratch" not in img:
                findings.append({"severity": "warn", "line": i, "message": f"Base image '{img}' is not minimal. Consider alpine/slim/distroless."})
            break

    # Check for user directive
    if "USER appuser" not in content and "USER nobody" not in content:
        findings.append({"severity": "warn", "line": 0, "message": "No non-root USER specified. Container runs as root."})

    # Check for HEALTHCHECK
    if "HEALTHCHECK" not in content:
        findings.append({"severity": "info", "line": 0, "message": "No HEALTHCHECK defined. Consider adding one for orchestration."})

    # Check for .dockerignore
    dockerignore = Path(path).parent / ".dockerignore"
    if not dockerignore.exists():
        findings.append({"severity": "warn", "line": 0, "message": "No .dockerignore found. Build context may include unnecessary files."})

    return findings


def suggest_dockerignore() -> str:
    """Generate a recommended .dockerignore."""
    return """node_modules
.git
.env
.env.*
*.md
Dockerfile
docker-compose*
.gitignore
__pycache__
*.pyc
dist
.build
.editorconfig
.terraform
*.tfstate*
"""


def report_dockerfile(path: str) -> str:
    """Generate a human-readable Dockerfile audit report."""
    findings = analyze_dockerfile(path)
    lines = ["# Dockerfile Audit Report", f"File: {path}", ""]
    errors = [f for f in findings if findings[0] == "error"]
    warnings = [f for f in findings if f["severity"] == "warn"]
    infos = [f for f in findings if f["severity"] == "info"]

    if errors:
        lines.append(f"## Errors ({len(errors)})")
        for f in errors:
            lines.append(f"- [line {f['line']}] {f['message']}")
    if warnings:
        lines.append(f"## Warnings ({len(warnings)})")
        for f in warnings:
            lines.append(f"- [line {f['line']}] {f['message']}")
    if infos:
        lines.append(f"## Info ({len(infos)})")
        for f in infos:
            lines.append(f"- [line {f['line']}] {f['message']}")

    if not findings:
        lines.append("No issues found.")
    return "\n".join(lines)


if __name__ == "__main__":
    print(report_dockerfile(sys.argv[1]))
```

### Phase 3: Image Size Optimization

```bash
#!/usr/bin/env bash
# analyze-image-size.sh — Break down layer sizes for any Docker image
# Usage: ./analyze-image-size.sh my-app:latest

set -euo pipefail
IMAGE="${1:?Usage: $0 image:tag}"

echo "=== Image layers for $IMAGE ==="
docker history --no-trunc --format "table {{.CreatedSince}}\t{{.Size}}\t{{.CreatedBy}}" "$IMAGE" | head -20

echo ""
echo "=== Image size ==="
docker image inspect "$IMAGE" --format '{{.Size}}' | numfmt --to=iec

echo ""
echo "=== Dangling images ==="
docker images -f dangling=true --format "{{.ID}} {{.Repository}}:{{.Tag}} {{.Size}}"

echo ""
echo "=== Recommendations ==="
echo "1. Check for OS packages left by apt-get install without --no-install-recommends"
echo "2. Check for copied files that are not needed at runtime (test data, docs)"
echo "3. Consider distroless base if no shell is needed"
echo "4. Chain RUN commands to reduce layers (apt-get update && apt-get install -y ... && rm -rf /var/lib/apt/lists/*)"
```

### Phase 4: Kubernetes Deployment (2–3 hrs)

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  namespace: production
  labels:
    app: app
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
        fsGroup: 1000
      containers:
        - name: app
          image: ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
          imagePullPolicy: Always
          ports:
            - containerPort: 3000
              name: http
          envFrom:
            - configMapRef:
                name: app-config
            - secretRef:
                name: app-secrets
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
          livenessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 10
            periodSeconds: 15
            timeoutSeconds: 5
          readinessProbe:
            httpGet:
              path: /ready
              port: http
            initialDelaySeconds: 5
            periodSeconds: 10
---
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: app
  namespace: production
spec:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: http
      name: http
  selector:
    app: app
---
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
---
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: production
data:
  NODE_ENV: "production"
  LOG_LEVEL: "info"
---
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app
  namespace: production
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - app.example.com
      secretName: app-tls
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app
                port:
                  name: http
```

### Phase 5: CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Build & Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to K8s
        run: |
          kubectl set image deployment/app app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} -n production
          kubectl rollout status deployment/app -n production --timeout=5m
```

### Phase 6: Full Orchestration

```bash
#!/usr/bin/env bash
# deploy-full-stack.sh — One command: compose → build → push → deploy
# Usage: ./deploy-full-stack.sh <app-name> <env>

set -euo pipefail
APP="${1:?Usage: $0 app-name env}"
ENV="${2:-staging}"
REGISTRY="${REGISTRY:-ghcr.io}/myorg"

echo "===> 1. Docker Compose — Verify local stack"
docker compose up -d --wait
docker compose down

echo "===> 2. Dockerfile — Build & optimize"
docker build --target=production -t "$REGISTRY/$APP:latest" .
docker tag "$REGISTRY/$APP:latest" "$REGISTRY/$APP:$(git rev-parse --short HEAD)"

echo "===> 3. Push"
docker push "$REGISTRY/$APP:latest"
docker push "$REGISTRY/$APP:$(git rev-parse --short HEAD)"

echo "===> 4. Deploy to K8s"
kubectl set image "deployment/$APP" "$APP=$REGISTRY/$APP:$(git rev-parse --short HEAD)" -n "$ENV"
kubectl rollout status "deployment/$APP" -n "$ENV" --timeout=5m

echo "===> 5. Verify"
kubectl get pods -n "$ENV" -l "app=$APP"
echo "Deploy complete: https://$APP.$ENV.example.com"
```

## First Action in 60 Minutes

1. **Add docker-compose.yml** to any project — multi-service with health checks
2. **Write a multi-stage Dockerfile** — builder stage + slim production stage
3. **Run the audit** — `python dockerfile-optimize.py Dockerfile` and fix top 3 issues
4. **Create `.dockerignore`** — copy the template above into the project
5. **Build & measure** — `docker build -t test . && docker image ls | grep test` — target <200 MB
6. **Scaffold K8s manifests** — `deployment.yaml`, `service.yaml`, `hpa.yaml` for the service

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Production Dockerfile is fine" | 9/10 client Dockerfiles are single-stage with full OS images. Shrink from 1.2 GB to 150 MB = $50/mo savings per node. |
| "Compose is just for dev" | Compose with profiles powers CI, e2e tests, and staging environments. |
| "K8s is overkill for small teams" | A 3-node K8s cluster costs $30/mo and eliminates deployment anxiety. Clients pay $3,000+ for that peace of mind. |
| "Volumes are for data" | Named volumes for databases, bind mounts for code. Mixing them is the #1 Docker Compose bug in client projects. |
| "I will add health checks later" | Without health checks, K8s routes traffic to dead pods. Clients lose money. Add them first. |

## Client Deliverable Checklist

- [ ] `docker-compose.yml` with health checks, named volumes, and `.env` support
- [ ] `.dockerignore` excluding build artifacts
- [ ] Multi-stage `Dockerfile` (builder + production) with non-root user
- [ ] `k8s/` directory with deployment, service, hpa, configmap, and ingress manifests
- [ ] GitHub Actions workflow for build, push, and deploy
- [ ] Image size audit report (before/after optimization)
- [ ] Deploy script (`deploy-full-stack.sh`) or GitOps config

## Output Format

```
client-infra/
  compose/
    docker-compose.yml
    .env.example
    .dockerignore
  docker/
    Dockerfile
    dockerfile-optimize.py
  k8s/
    base/
      deployment.yaml
      service.yaml
      configmap.yaml
    overlays/
      staging/
        kustomization.yaml
        ingress.yaml
      production/
        kustomization.yaml
        hpa.yaml
        ingress.yaml
  ci/
    deploy.yml            # GitHub Actions workflow
  scripts/
    deploy.sh
    analyze-image.sh
```

## Verification Checklist

- [ ] `docker compose up -d --wait` starts all services healthily
- [ ] `docker build --target=production -t test .` succeeds with non-root user
- [ ] Image is <200 MB (check: `docker image inspect test --format '{{.Size}}'`)
- [ ] `kubectl apply -f k8s/` creates all resources without errors
- [ ] HPA configured with CPU/memory thresholds
- [ ] Liveness + readiness probes configured on every container
- [ ] Rolling update strategy set (not Recreate)
- [ ] Resource requests and limits set on every container
- [ ] CI/CD pipeline builds and pushes without secrets leak
- [ ] `.dockerignore` excludes node_modules, .git, .env


## When to Use
Use this skill when working with docker.


## Workflow
See the parent skill for authoritative workflow documentation.
