---
name: packer-images
description: HashiCorp Packer — machine image building, builders, provisioners, post-processors for AWS/GCP/Azure
domain: devops
tags:
- aws
- azure
- ci-cd
- devops
- gcp
- images
- infrastructure
- packer
---


## Overview

Packer automates machine image creation for multiple platforms from a single source configuration. Supports AWS AMI, GCP images, Azure images, Docker, and more.

## Capabilities

- Multi-platform image building (AWS, GCP, Azure, Docker, VirtualBox)
- HCL2 configuration language
- Provisioners (shell, Ansible, Chef, Puppet)
- Post-processors (compress, manifest, Vagrant)
- Image testing with InSpec/Testinfra
- CI/CD integration for automated image pipelines

## When to Use

- Building golden images for cloud deployments
- Immutable infrastructure patterns
- AMI/image creation in CI/CD pipelines
- Standardized base images across teams
- Compliance-hardened images

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

The packer-images workflow follows a standard pipeline pattern.

Core flow:
```
# packer-images primary flow
input = prepare(raw_data)
result = process(input, config={azure, builders, building, hashicorp, image})
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


### AWS AMI
```hcl
# aws-ami.pkr.hcl
packer {
  required_plugins {
    amazon = {
      version = ">= 1.2.0"
      source  = "github.com/hashicorp/amazon"
    }
  }
}

variable "version" {
  type    = string
  default = "1.0.0"
}

source "amazon-ebs" "ubuntu" {
  ami_name      = "myapp-${var.version}-{{timestamp}}"
  instance_type = "t3.micro"
  region        = "us-east-1"
  source_ami_filter {
    filters = {
      name                = "ubuntu/images/*ubuntu-jammy-22.04-amd64-server-*"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    owners      = ["099720109477"]
    most_recent = true
  }
  ssh_username = "ubuntu"
}

build {
  sources = ["source.amazon-ebs.ubuntu"]

  provisioner "shell" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y docker.io nginx",
      "sudo systemctl enable docker nginx"
    ]
  }

  provisioner "file" {
    source      = "configs/nginx.conf"
    destination = "/tmp/nginx.conf"
  }

  provisioner "shell" {
    inline = ["sudo mv /tmp/nginx.conf /etc/nginx/nginx.conf"]
  }

  post-processor "manifest" {
    output     = "manifest.json"
    strip_path = true
  }
}
```

### GCP Image
```hcl
source "googlecompute" "ubuntu" {
  project_id   = "my-project"
  zone         = "us-central1-a"
  image_name   = "myapp-${var.version}-{{timestamp}}"
  source_image = "ubuntu-2204-jammy-v20240101"
  ssh_username = "ubuntu"
}
```

### Ansible Provisioner
```hcl
provisioner "ansible" {
  playbook_file = "ansible/playbook.yml"
  extra_arguments = [
    "--extra-vars", "env=production"
  ]
}
```

### Commands
```bash
# Init (download plugins)
packer init aws-ami.pkr.hcl

# Validate
packer validate aws-ami.pkr.hcl

# Build
packer build -var "version=2.0.0" aws-ami.pkr.hcl

# Build with vars file
packer build -var-file="prod.pkrvars.hcl" aws-ami.pkr.hcl
```

## Common Patterns

- **Source + build**: separate reusable source blocks
- **Variables**: parameterize for environments
- **HCL2 functions**: `timestamp()`, `uuid()`, `upper()`
- **Artifacts**: output manifests for downstream automation
- **CI integration**: build images on release tags

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
