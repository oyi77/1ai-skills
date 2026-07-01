---
name: ansible-automation
description: Ansible automation — playbooks, roles, inventory, variables, handlers, Galaxy, AWX. Use when working with ansible automation.
domain: devops
tags:
- ansible
- automation
- ci-cd
- devops
- infrastructure
---


## Overview

Ansible is an agentless automation tool using SSH for configuration management, application deployment, and orchestration. Uses YAML-based playbooks with Jinja2 templating.

## Capabilities

- Agentless automation over SSH
- Declarative playbook authoring in YAML
- Role-based organization and Galaxy sharing
- Jinja2 templating for dynamic configs
- Inventory management (static/dynamic)
- Vault for secrets encryption

## When to Use

**Trigger phrases:**
- "ansible automation"
- "Server configuration management (10-10000+ nodes)"
- "Application deployment automation"
- "Infrastructure provisioning workflows"


- Server configuration management (10-10000+ nodes)
- Application deployment automation
- Infrastructure provisioning workflows
- Compliance and security hardening
- Multi-cloud orchestration

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

The ansible-automation workflow follows a standard pipeline pattern.

Core flow:
```
# ansible-automation primary flow
input = prepare(raw_data)
result = process(input, config={ansible, automation, galaxy, handlers, inventory})
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


### Playbook
```yaml
# site.yml
---
- name: Configure web servers
  hosts: webservers
  become: true
  vars:
    nginx_port: 80
    app_env: production

  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
        update_cache: true

    - name: Deploy nginx config
      template:
        src: templates/nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      notify: Restart nginx

    - name: Ensure nginx running
      service:
        name: nginx
        state: started
        enabled: true

  handlers:
    - name: Restart nginx
      service:
        name: nginx
        state: restarted
```

### Role Structure
```
roles/
  webserver/
    tasks/main.yml
    handlers/main.yml
    templates/nginx.conf.j2
    files/ssl.crt
    defaults/main.yml
    vars/main.yml
    meta/main.yml
```

### Dynamic Inventory
```
# inventory/aws_ec2.yml
plugin: amazon.aws.aws_ec2
regions:
  - us-east-1
keyed_groups:
  - key: tags.Role
    prefix: role
filters:
  tag:Environment: production
```

### Vault Secrets
```bash
ansible-vault create secrets.yml
ansible-vault edit secrets.yml
ansible-playbook site.yml --ask-vault-pass
ansible-playbook site.yml --vault-password-file .vault_pass
```

## Common Patterns

- **Roles**: reusable units of automation
- **Handlers**: triggered on config changes (notify/handlers)
- **Tags**: run subset of tasks (`--tags deploy`)
- **Loops**: `loop: "{{ users }}"` for iteration
- **Conditionals**: `when: ansible_os_family == "Debian"`
- **AWX/Tower**: web UI for playbook execution and RBAC

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