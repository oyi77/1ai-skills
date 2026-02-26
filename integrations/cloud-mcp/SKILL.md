---
name: cloud-mcp
description: MCP servers for cloud infrastructure. Connect AI agents to AWS, GCP, and Azure for deployment, management, and infrastructure automation.
---

# Cloud MCP Skill

## Overview

MCP servers enabling AI agents to interact with major cloud providers (AWS, GCP, Azure) for deployment, infrastructure management, and cloud operations.

**Supported Providers**: AWS, Google Cloud, Microsoft Azure  
**Use Cases**: Deployments, infrastructure management, cloud monitoring

---

## When to Use

- Deploy applications to cloud
- Manage infrastructure
- Monitor cloud resources
- Automate scaling
- Cost optimization
- Security management

---

## AWS MCP Setup

### Installation
```json
{
  "mcpServers": {
    "aws": {
      "command": "npx",
      "args": ["-y", "mcp-aws"],
      "env": {
        "AWS_ACCESS_KEY_ID": "${AWS_ACCESS_KEY_ID}",
        "AWS_SECRET_ACCESS_KEY": "${AWS_SECRET_ACCESS_KEY}",
        "AWS_REGION": "us-east-1"
      }
    }
  }
}
```

### AWS Tools
```typescript
// List S3 buckets
aws.s3.listBuckets()

// Upload file to S3
aws.s3.uploadFile({
  bucket: "my-bucket",
  key: "uploads/file.txt",
  body: "file content"
})

// List EC2 instances
aws.ec2.describeInstances({
  Filters: [{ Name: "instance-state-name", Values: ["running"] }]
})

// Create Lambda function
aws.lambda.createFunction({
  FunctionName: "my-function",
  Runtime: "nodejs18.x",
  Handler: "index.handler",
  Code: { ZipFile: buffer }
})

// Get CloudWatch metrics
aws.cloudwatch.getMetricStatistics({
  Namespace: "AWS/EC2",
  MetricName: "CPUUtilization",
  Period: 3600,
  StartTime: new Date(Date.now() - 86400000),
  EndTime: new Date(),
  Statistics: ["Average"]
})
```

---

## GCP MCP Setup

### Installation
```json
{
  "mcpServers": {
    "gcp": {
      "command": "npx",
      "args": ["-y", "mcp-gcp"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/credentials.json"
      }
    }
  }
}
```

### GCP Tools
```typescript
// List Compute Engine instances
gcp.compute.listInstances({
  project: "my-project",
  zone: "us-central1-a"
})

// Deploy to Cloud Run
gcp.run.deploy({
  project: "my-project",
  location: "us-central1",
  image: "gcr.io/my-project/container:latest"
})

// Get Cloud Storage buckets
gcp.storage.listBuckets({
  project: "my-project"
})

// Deploy Cloud Function
gcp.functions.deploy({
  entryPoint: "helloHttp",
  runtime: "nodejs18",
  source: "."
})
```

---

## Azure MCP Setup

### Installation
```json
{
  "mcpServers": {
    "azure": {
      "command": "npx",
      "args": ["-y", "mcp-azure"],
      "env": {
        "AZURE_SUBSCRIPTION_ID": "${AZURE_SUBSCRIPTION_ID}",
        "AZURE_TENANT_ID": "${AZURE_TENANT_ID}",
        "AZURE_CLIENT_ID": "${AZURE_CLIENT_ID}",
        "AZURE_CLIENT_SECRET": "${AZURE_CLIENT_SECRET}"
      }
    }
  }
}
```

### Azure Tools
```typescript
// List VMs
azure.compute.listVMs({
  resourceGroup: "my-rg"
})

// Deploy container instance
azure.container.create({
  resourceGroup: "my-rg",
  name: "my-container",
  image: "nginx:latest"
})

// Get storage account keys
azure.storage.listKeys({
  resourceGroup: "my-rg",
  accountName: "mystorage"
})

// List App Services
azure.web.listApps({
  resourceGroup: "my-rg"
})
```

---

## Use Cases

### 1. Auto-Scaling
```
Trigger: High CPU
Action: 
  1. Check current instances
  2. Scale up
  3. Monitor metrics
```

### 2. Deployment Pipeline
```
Trigger: Git push
Action:
  1. Build container
  2. Push to registry
  3. Deploy to cloud
  4. Run health check
```

### 3. Cost Monitoring
```
Schedule: Daily
Action:
  1. Get cost by service
  2. Compare to budget
  3. Alert if overspending
```

### 4. Backup Management
```
Schedule: Daily backup
Action:
  1. Create snapshot
  2. Verify backup
  3. Log results
```

### 5. Incident Response
```
Trigger: Alert
Action:
  1. Get affected resources
  2. Check logs
  3. Restart if needed
  4. Notify team
```

---

## Infrastructure as Code

### Generate Terraform
```typescript
// Generate Terraform from current state
terraform.generate({
  provider: "aws",
  resources: ["ec2", "s3", "rds"]
})
```

### Plan Changes
```typescript
terraform.plan({
  template: mainTf,
  variables: { environment: "prod" }
})
```

### Apply Changes
```typescript
terraform.apply({
  template: mainTf,
  variables: { environment: "prod" },
  autoApprove: false
})
```

---

## Integration with 1ai-skills

### With CI/CD
```
code-reviewer → cloud-mcp → deploy
     ↓              ↓
  Review       Deploy to AWS/GCP/Azure
```

### With Monitoring
```
skill-performance-monitor → cloud-mcp → auto-scale
       ↓                      ↓
  Detect issue            Scale resources
```

### With Security
```
vulnerability-scanner → cloud-mcp → remediate
        ↓                    ↓
  Find issues           Fix automatically
```

---

## Best Practices

### Do's
✅ Use IAM roles with minimal permissions  
✅ Enable logging and monitoring  
✅ Use infrastructure as code  
✅ Regular security audits  

### Don'ts
❌ Don't expose credentials  
❌ Don't use root accounts  
❌ Don't skip cost monitoring  

---

## Version History

- **v1.0** (2026-02-27) - Initial creation
  - AWS, GCP, Azure support

---

## Related Skills

- [automation](/skills/automation) - Workflow automation
- [deployment](/skills/deployment) - Deployment pipelines
- [security](/skills/security) - Cloud security
