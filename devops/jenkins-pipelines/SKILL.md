---
name: jenkins-pipelines
description: Jenkins pipeline as code — Declarative/Scripted pipelines, shared libraries, agents, stages, credentials
---

## Overview

Jenkins pipelines define CI/CD workflows as code using Groovy-based DSL. Supports Declarative (structured) and Scripted (flexible) syntax with shared libraries for reuse across projects.

## Capabilities

- Declarative and Scripted pipeline authoring
- Parallel stage execution for faster builds
- Shared library development and versioning
- Credential management with Credentials plugin
- Agent/label-based build node selection
- Blue Ocean visual pipeline editor integration

## When to Use

- CI/CD for Java, Node.js, Python, or polyglot projects
- Complex multi-stage build/test/deploy workflows
- Teams already running Jenkins infrastructure
- Need shared pipeline logic across many repositories
- Enterprise environments with Jenkins + LDAP/RBAC

## Pseudo Code

### Declarative Pipeline
```groovy
// Jenkinsfile
pipeline {
    agent { label 'linux' }
    environment {
        APP_NAME = 'my-app'
        REGISTRY = 'ghcr.io'
    }
    stages {
        stage('Build') {
            steps {
                sh 'npm ci'
                sh 'npm run build'
            }
        }
        stage('Test') {
            parallel {
                stage('Unit Tests') { steps { sh 'npm test' } }
                stage('Lint') { steps { sh 'npm run lint' } }
            }
        }
        stage('Deploy') {
            when { branch 'main' }
            steps {
                sh 'docker build -t $REGISTRY/$APP_NAME:$BUILD_NUMBER .'
                sh 'docker push $REGISTRY/$APP_NAME:$BUILD_NUMBER'
            }
        }
    }
    post {
        always { cleanWs() }
        failure { slackSend channel: '#builds', message: "FAILED: ${env.JOB_NAME}" }
    }
}
```

### Shared Library
```groovy
// vars/deployK8s.groovy
def call(Map config) {
    sh "kubectl set image deployment/${config.app} ${config.container}=${config.image}"
    sh "kubectl rollout status deployment/${config.app}"
}

// Jenkinsfile usage
@Library('my-shared-lib@main') _
deployK8s(app: 'api', container: 'api', image: 'ghcr.io/api:v1')
```

### Credentials Usage
```groovy
stage('Deploy') {
    steps {
        withCredentials([string(credentialsId: 'api-key', variable: 'TOKEN')]) {
            sh 'curl -H "Authorization: Bearer $TOKEN" https://api.example.com/deploy'
        }
        withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
            sh 'kubectl --kubeconfig=$KUBECONFIG apply -f deploy.yaml'
        }
    }
}
```

## Common Patterns

- **Multibranch pipeline**: auto-discovers branches with Jenkinsfile
- **Shared libraries**: reusable pipeline logic in `vars/`, `src/`, `resources/`
- **Parameters**: `parameters { string(name: 'VERSION', defaultValue: 'latest') }`
- **Input gates**: `input message: 'Deploy to production?'`
- **Matrix builds**: `matrix { axes { axis { name 'OS'; values 'linux', 'darwin' } } }`
