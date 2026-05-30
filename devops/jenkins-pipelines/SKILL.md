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

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

The jenkins-pipelines workflow follows a standard pipeline pattern.

Core flow:
```
# jenkins-pipelines primary flow
input = prepare(raw_data)
result = process(input, config={agents, code, credentials, declarative, jenkins})
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
