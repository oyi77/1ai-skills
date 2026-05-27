---
name: ansible-automation
description: Ansible automation — playbooks, roles, inventory, variables, handlers, Galaxy, AWX
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

- Server configuration management (10-10000+ nodes)
- Application deployment automation
- Infrastructure provisioning workflows
- Compliance and security hardening
- Multi-cloud orchestration

## Pseudo Code

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
```python
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
