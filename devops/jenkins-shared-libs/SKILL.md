---
name: jenkins-shared-libs
description: Jenkins shared libraries — reusable pipeline code, Groovy vars, resources, global pipeline libraries
domain: devops
tags:
- ci-cd
- devops
- infrastructure
- jenkins
- libs
- pipeline
- shared
---


## Overview

Jenkins shared libraries enable reusable pipeline code across multiple Jenkinsfiles. Libraries contain Groovy scripts (vars/), classes (src/), and resources that pipelines can import via `@Library`.

## Capabilities

- Reusable pipeline steps across projects
- Custom Groovy classes for complex logic
- Resource files (templates, configs) bundled with library
- Global variables as pipeline steps
- Versioned libraries from Git repositories
- Automatic loading with `@Library('my-lib@main')`

## When to Use
**Trigger phrases:**
- "jenkins shared libs"
- "Jenkins shared libraries — reusable pipeline code, Groovy vars, resources, globa"


- Multiple Jenkins pipelines share common steps
- Need standardized CI/CD patterns across teams
- Want to encapsulate complex pipeline logic
- Managing shared configuration across 10+ pipelines

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

The jenkins-shared-libs workflow follows a standard pipeline pattern.

Core flow:
```
# jenkins-shared-libs primary flow
input = prepare(raw_data)
result = process(input, config={code, global, groovy, jenkins, libraries})
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


### Library Structure
```
my-jenkins-lib/
├── vars/
│   ├── buildAndDeploy.groovy    # Pipeline step
│   └── notifySlack.groovy       # Utility step
├── src/
│   └── com/
│       └── mycompany/
│           └── PipelineConfig.groovy  # Shared classes
└── resources/
    └── templates/
        └── Dockerfile.template
```

### vars/buildAndDeploy.groovy
```groovy
def call(Map config = [:]) {
    def environment = config.environment ?: 'staging'
    def dockerImage = config.image ?: 'myapp'

    pipeline {
        agent any
        stages {
            stage('Build') {
                steps {
                    sh "docker build -t ${dockerImage}:${env.BUILD_NUMBER} ."
                }
            }
            stage('Test') {
                steps {
                    sh "docker run --rm ${dockerImage}:${env.BUILD_NUMBER} npm test"
                }
            }
            stage('Deploy') {
                steps {
                    sh "kubectl set image deployment/myapp myapp=${dockerImage}:${env.BUILD_NUMBER}"
                }
            }
        }
        post {
            failure { notifySlack(status: 'FAILED') }
            success { notifySlack(status: 'SUCCESS') }
        }
    }
}
```

### Using in Jenkinsfile
```groovy
@Library('my-jenkins-lib@v2.0') _

buildAndDeploy(
    image: 'mycompany/api',
    environment: 'production'
)
```

### src/ Class Example
```groovy
// src/com/mycompany/PipelineConfig.groovy
package com.mycompany

class PipelineConfig implements Serializable {
    def script
    String dockerRegistry = 'registry.example.com'
    
    PipelineConfig(script) { this.script = script }
    
    def buildImage(String name) {
        script.sh "docker build -t ${dockerRegistry}/${name}:${script.env.BUILD_NUMBER} ."
    }
}
```

## Common Patterns

- **Default params**: `def call(Map config = [:]) { def x = config.get('key', 'default') }`
- **Library versioning**: `@Library('my-lib@v1.2.3')` or `@Library('my-lib@main')`
- **Resource loading**: `libraryResource('templates/Dockerfile.template')`
- **CPS transformation**: Add `@NonCPS` to methods that don't need serialization
- **Test libraries**: Use Jenkins Pipeline Unit for shared lib testing

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