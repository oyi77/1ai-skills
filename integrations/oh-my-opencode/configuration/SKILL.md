---
name: oh-my-opencode-configuration
description: Comprehensive configuration guide for oh-my-opencode including agent settings, MCP servers, hooks, categories, and advanced options
---

# Oh My OpenCode Configuration

## Overview

This skill provides detailed guidance on configuring oh-my-opencode, covering all configuration options for agents, MCP servers, hooks, categories, and advanced settings.

## Configuration Structure

### Config File Locations

| Level | Location | Priority |
|-------|----------|----------|
| Project | `.opencode/oh-my-opencode.jsonc` | Highest |
| User | `~/.config/opencode/oh-my-opencode.jsonc` | Medium |
| Default | Built-in defaults | Lowest |

### Config Format

oh-my-opencode uses JSONC (JSON with Comments):

```jsonc
{
  // This is a comment
  "agents": { ... },
  "features": { ... },
  "mcp": { ... }
}
```

## Agent Configuration

### Sisyphus Configuration

```jsonc
{
  "agents": {
    "sisyphus": {
      "model": "openai/gpt-4o",
      "temperature": 0.7,
      "maxTokens": 8192,
      "enabled": true,
      "prompt": "You are Sisyphus, an autonomous agent...",
      "permissions": {
        "fileSystem": "restricted",
        "network": true,
        "shell": true
      }
    }
  }
}
```

### Hephaestus Configuration

```jsonc
{
  "agents": {
    "hephaestus": {
      "model": "openai/gpt-4o",
      "temperature": 0.3,
      "maxTokens": 8192,
      "enabled": true,
      "exploreBeforeActing": {
        "parallelAgents": 3,
        "timeout": 60000
      },
      "verification": {
        "lsp": true,
        "tests": true,
        "build": true
      }
    }
  }
}
```

### Oracle Configuration

```jsonc
{
  "agents": {
    "oracle": {
      "model": "anthropic/claude-3-5-sonnet-20241022",
      "temperature": 0.1,
      "maxTokens": 4096,
      "enabled": true,
      "consultationLimit": 3
    }
  }
}
```

### Librarian Configuration

```jsonc
{
  "agents": {
    "librarian": {
      "model": "glm-4",
      "temperature": 0.5,
      "maxTokens": 4096,
      "enabled": true,
      "sources": [
        "official-docs",
        "github",
        "stackoverflow"
      ],
      "search": {
        "maxResults": 5,
        "timeout": 30000
      }
    }
  }
}
```

### Explore Configuration

```jsonc
{
  "agents": {
    "explore": {
      "model": "grok-code-fast",
      "temperature": 0.3,
      "maxTokens": 2048,
      "enabled": true,
      "search": {
        "maxFiles": 20,
        "timeout": 10000
      }
    }
  }
}
```

## Feature Configuration

### Parallel Agents

```jsonc
{
  "features": {
    "parallelAgents": {
      "enabled": true,
      "maxConcurrent": 5,
      "timeout": 120000,
      "failStrategy": "continue"
    }
  }
}
```

### Background Tasks

```jsonc
{
  "features": {
    "backgroundTasks": {
      "enabled": true,
      "maxConcurrent": 3,
      "timeout": 600000,
      "persistence": true
    }
  }
}
```

### Todo Enforcement

```jsonc
{
  "features": {
    "todoEnforcement": {
      "enabled": true,
      "strict": true,
      "autoContinue": true,
      "reminderInterval": 300000
    }
  }
}
```

### Hash-Anchored Editing

```jsonc
{
  "features": {
    "hashAnchoredEdit": {
      "enabled": true,
      "validation": true,
      "autoCorrect": false
    }
  }
}
```

### Comment Checker

```jsonc
{
  "features": {
    "commentChecker": {
      "enabled": true,
      "strictness": "moderate",
      "allowedPatterns": [
        "TODO",
        "FIXME",
        "HACK",
        "NOTE"
      ]
    }
  }
}
```

## MCP Server Configuration

### Built-in MCPs

```jsonc
{
  "mcp": {
    "servers": {
      "websearch": {
        "enabled": true,
        "provider": "exa",
        "apiKey": "${EXA_API_KEY}"
      },
      "context7": {
        "enabled": true,
        "cacheSize": 1000,
        "ttl": 3600
      },
      "grep_app": {
        "enabled": true,
        "timeout": 30000
      }
    }
  }
}
```

### Custom MCPs

```jsonc
{
  "mcp": {
    "servers": {
      "custom-server": {
        "command": "python",
        "args": ["-m", "custom_mcp"],
        "env": {
          "CUSTOM_VAR": "value"
        },
        "enabled": true
      }
    }
  }
}
```

### MCP Groups

```jsonc
{
  "mcp": {
    "groups": {
      "development": ["websearch", "context7", "grep_app"],
      "research": ["websearch", "context7"],
      "minimal": []
    }
  }
}
```

## Category Configuration

### Built-in Categories

```jsonc
{
  "categories": {
    "visual-engineering": {
      "model": "openai/gpt-4o",
      "temperature": 0.7,
      "defaultSkills": ["frontend-ui-ux"]
    },
    "ultrabrain": {
      "model": "anthropic/claude-3-5-sonnet-20241022",
      "temperature": 0.1,
      "defaultSkills": []
    },
    "deep": {
      "model": "openai/gpt-4o",
      "temperature": 0.3,
      "defaultSkills": []
    }
  }
}
```

### Custom Categories

```jsonc
{
  "categories": {
    "backend-api": {
      "model": "openai/gpt-4o",
      "temperature": 0.3,
      "defaultSkills": ["git-master", "playwright"],
      "agents": ["hephaestus"]
    },
    "data-processing": {
      "model": "anthropic/claude-3-5-sonnet-20241022",
      "temperature": 0.2,
      "defaultSkills": [],
      "agents": ["oracle"]
    }
  }
}
```

## Hook Configuration

### Available Hooks

```jsonc
{
  "hooks": {
    "PreToolUse": {
      "enabled": true,
      "handlers": ["logging", "validation"]
    },
    "PostToolUse": {
      "enabled": true,
      "handlers": ["logging", "verification"]
    },
    "UserPromptSubmit": {
      "enabled": true,
      "handlers": ["context-injection"]
    },
    "Stop": {
      "enabled": true,
      "handlers": ["cleanup"]
    }
  }
}
```

### Custom Hooks

```jsonc
{
  "hooks": {
    "PreToolUse": {
      "enabled": true,
      "custom": {
        "my-hook": {
          "script": "./hooks/pre-tool-use.js",
          "timeout": 5000
        }
      }
    }
  }
}
```

### Disabled Hooks

```jsonc
{
  "hooks": {
    "disabled_hooks": [
      "comment-checker",
      "verbose-logging"
    ]
  }
}
```

## LSP Configuration

### Built-in LSP Tools

```jsonc
{
  "lsp": {
    "enabled": true,
    "tools": {
      "diagnostics": true,
      "definition": true,
      "references": true,
      "rename": true,
      "symbols": true
    }
  }
}
```

### Custom LSP Servers

```jsonc
{
  "lsp": {
    "servers": {
      "typescript": {
        "command": "typescript-language-server",
        "args": ["--stdio"],
        "enabled": true
      },
      "python": {
        "command": "pylsp",
        "args": ["--sp-settings", "{\"pylsp\":{\"plugins\":{\"pycodestyle\":{\"enabled\":false}}}"],
        "enabled": true
      }
    }
  }
}
```

## Permission Configuration

### Agent Permissions

```jsonc
{
  "permissions": {
    "agents": {
      "sisyphus": {
        "fileSystem": {
          "allowed": ["src/**/*", "tests/**/*"],
          "denied": [".env", "secrets/**/*"]
        },
        "network": {
          "allowed": true,
          "domains": ["api.github.com"]
        },
        "shell": {
          "allowed": true,
          "commands": ["git", "npm", "docker"]
        }
      }
    }
  }
}
```

### Global Permissions

```jsonc
{
  "permissions": {
    "global": {
      "fileSystem": {
        "default": "read-only",
        "projectRoot": "read-write"
      },
      "network": {
        "default": false,
        "apiKeysRequired": true
      }
    }
  }
}
```

## Theme and UI Configuration

### Theme

```jsonc
{
  "theme": {
    "name": "dark",
    "custom": {
      "primary": "#007AFF",
      "background": "#1E1E1E",
      "foreground": "#FFFFFF"
    }
  }
}
```

### Keybinds

```jsonc
{
  "keybinds": {
    "ctrl+x": "quick-command",
    "ctrl+p": "command-palette",
    "ctrl+f": "find",
    "ctrl+r": "redo",
    "ctrl+z": "undo",
    "tab": "toggle-mode"
  }
}
```

## Environment Configuration

### Environment Variables

```jsonc
{
  "environment": {
    "variables": {
      "OPENAI_API_KEY": "${OPENAI_API_KEY}",
      "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}",
      "GITHUB_TOKEN": "${GITHUB_TOKEN}"
    },
    "passThrough": [
      "PATH",
      "HOME",
      "USER"
    ]
  }
}
```

### Secrets Management

```jsonc
{
  "secrets": {
    "provider": "env-file",
    "files": [
      ".env",
      ".secrets"
    ],
    "required": [
      "OPENAI_API_KEY"
    ]
  }
}
```

## Advanced Configuration

### Truncation

```jsonc
{
  "truncation": {
    "aggressive": {
      "enabled": false,
      "threshold": 0.8,
      "preserve": ["function-signatures", "class-definitions"]
    }
  }
}
```

### Session Persistence

```jsonc
{
  "session": {
    "persistence": {
      "enabled": true,
      "storage": "file",
      "location": "~/.config/opencode/sessions",
      "maxSessions": 50
    },
    "continuity": {
      "enabled": true,
      "maxContextTokens": 100000
    }
  }
}
```

### Experimental Features

```jsonc
{
  "experimental": {
    "autoResume": {
      "enabled": true,
      "maxRetries": 3
    },
    "agentMemory": {
      "enabled": false,
      "storage": "~/.config/opencode/memory"
    }
  }
}
```

## Configuration Profiles

### Profile Structure

```jsonc
{
  "profiles": {
    "development": { ... },
    "production": { ... },
    "research": { ... }
  }
}
```

### Profile Switching

```bash
# Via command
/profile development

# Via environment
export OMO_PROFILE=development

# Via CLI flag
opencode --profile development
```

## Validation and Testing

### Config Validation

```bash
# Validate config file
opencode config validate

# Check specific section
opencode config validate --section agents

# Lint config
opencode config lint
```

### Test Configuration

```bash
# Test agent configuration
opencode config test-agents

# Test MCP servers
opencode config test-mcp

# Test hooks
opencode config test-hooks
```

## Troubleshooting Configuration

### Common Issues

#### Config Not Loading
```bash
# Check file location
ls -la ~/.config/opencode/oh-my-opencode.jsonc

# Validate syntax
cat ~/.config/opencode/oh-my-opencode.jsonc | python3 -m json.tool

# Check permissions
chmod 600 ~/.config/opencode/oh-my-opencode.jsonc
```

#### Agent Not Responding
```bash
# Check agent configuration
opencode config show --section agents

# Verify model settings
opencode config test-model <model-name>
```

#### MCP Server Failing
```bash
# Test MCP connection
opencode mcp test <server-name>

# Check MCP logs
opencode logs --mcp
```

## Quick Reference

| Category | Key Options |
|----------|-------------|
| Agents | model, temperature, maxTokens, permissions |
| Features | parallelAgents, backgroundTasks, todoEnforcement |
| MCP | servers, groups, custom-servers |
| Categories | model, temperature, defaultSkills, agents |
| Hooks | PreToolUse, PostToolUse, UserPromptSubmit, Stop |
| LSP | enabled, tools, servers |
| Permissions | fileSystem, network, shell |
| Theme | name, custom colors |
| Keybinds | shortcut mappings |

## References

- Configuration Docs: https://github.com/code-yeongyu/oh-my-opencode/blob/master/docs/configurations.md
- OpenCode Config: https://opencode.ai/docs/config/
- Agent-Model Matching: https://github.com/code-yeongyu/oh-my-opencode/blob/master/docs/guide/agent-model-matching.md

## Related Skills

- oh-my-opencode: Overall integration
- oh-my-opencode-installation: Setup guide
- oh-my-opencode-agents: Agent usage
- oh-my-opencode-usage: Daily usage
- oh-my-opencode-features: Complete features list
