---
name: helm-charts
description: Helm chart development — templates, values, hooks, dependencies, chart testing, repository management
---

## Overview

Helm is the Kubernetes package manager. Charts are templated Kubernetes manifests with configurable values. Supports dependencies, hooks, release management, and chart repositories.

## Capabilities

- Templated Kubernetes manifests with Go templates
- Values-driven configuration
- Chart dependencies and subcharts
- Pre/post install/upgrade hooks
- Release lifecycle management (install/upgrade/rollback)
- Chart testing and repository publishing

## When to Use

- Packaging Kubernetes applications for distribution
- Multi-environment deployments with value overrides
- Complex applications with multiple K8s resources
- Need release history and rollback capabilities
- Sharing reusable K8s packages via repositories

## Pseudo Code

### Chart Structure
```
mychart/
  Chart.yaml          # Metadata + dependencies
  values.yaml         # Default values
  templates/
    deployment.yaml
    service.yaml
    ingress.yaml
    _helpers.tpl      # Template helpers
    NOTES.txt         # Post-install notes
  charts/             # Subcharts
  tests/
    test-connection.yaml
```

### Chart.yaml
```yaml
apiVersion: v2
name: myapp
version: 1.2.0
appVersion: "2.0.0"
description: My application Helm chart
dependencies:
  - name: postgresql
    version: "12.x.x"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled
```

### Template with Values
```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "myapp.selectorLabels" . | nindent 6 }}
  template:
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          ports:
            - containerPort: {{ .Values.service.port }}
          {{- if .Values.resources }}
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          {{- end }}
          envFrom:
            - configMapRef:
                name: {{ include "myapp.fullname" . }}-config
```

### Hooks
```yaml
# templates/job-migrate.yaml
apiVersion: batch/v1
kind: Job
metadata:
  annotations:
    "helm.sh/hook": pre-upgrade
    "helm.sh/hook-weight": "-5"
    "helm.sh/hook-delete-policy": before-hook-creation
spec:
  template:
    spec:
      containers:
        - name: migrate
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          command: ["./migrate", "up"]
      restartPolicy: Never
```

### Commands
```bash
# Install
helm install myapp ./mychart -f values-prod.yaml

# Upgrade
helm upgrade myapp ./mychart -f values-prod.yaml --set image.tag=v2.1

# Rollback
helm rollback myapp 1

# Test
helm test myapp

# Package
helm package ./mychart

# Lint
helm lint ./mychart
```

## Common Patterns

- **_helpers.tpl**: define reusable template snippets
- **Named templates**: `{{ define "name" }}...{{ end }}`
- **Conditional sections**: `{{- if .Values.ingress.enabled }}`
- **Range loops**: `{{- range .Values.env }}`
- **Lookup**: `lookup` function to check existing resources
