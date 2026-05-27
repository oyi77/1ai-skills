---
name: jenkins-shared-libs
description: Jenkins shared libraries — reusable pipeline code, Groovy vars, resources, global pipeline libraries
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

- Multiple Jenkins pipelines share common steps
- Need standardized CI/CD patterns across teams
- Want to encapsulate complex pipeline logic
- Managing shared configuration across 10+ pipelines

## Pseudo Code

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
