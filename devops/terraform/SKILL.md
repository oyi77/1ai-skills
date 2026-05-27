---
name: terraform
description: Infrastructure as Code with Terraform — HCL, modules, state management, providers, workspaces
---

## Overview

Infrastructure as Code using Terraform's HCL language. Covers modules, remote state, providers, workspaces, and drift detection.

## Capabilities

- HCL resource definitions
- Module creation and registry
- Remote state (S3, GCS, Terraform Cloud)
- Provider configuration
- Workspace management
- Import existing resources
- Plan/apply/destroy lifecycle

## When to Use

- Multi-cloud infrastructure
- Repeatable environment provisioning
- Infrastructure version control
- Compliance as code

## Pseudo Code

### EC2 Instance
```hcl
resource "aws_instance" "web" {
  ami           = "ami-0abcdef1234567890"
  instance_type = "t3.micro"
  tags = { Name = "WebServer" }
}

terraform {
  backend "s3" { bucket = "my-tf-state" key = "prod/terraform.tfstate" }
}
```

## Common Patterns

- Remote state with locking
- Use modules for reusability
- terraform plan before apply
- Workspaces for environments
- Import existing resources
