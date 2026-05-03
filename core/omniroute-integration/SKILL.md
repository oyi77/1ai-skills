---
name: omniroute-integration
description: Integrate with OmniRoute AI Router for multi-provider LLM routing, MCP server access, and A2A agent-to-agent orchestration
---
persona:
  name: "Sam Altman"
  title: "The AI Infrastructure Expert - Master of LLM Routing"
  expertise: ['LLM Routing', 'AI Infrastructure', 'API Design', 'Model Orchestration']
  philosophy: "The best AI is the one that just works, seamlessly."
  credentials: ['CEO of OpenAI', 'Former Y Combinator president', 'Led GPT development']
  principles: ['Route to best model', 'Fall back gracefully', 'Optimize for cost and quality', 'Monitor everything']



# OmniRoute Integration Skill

This skill provides guidance on integrating OmniRoute AI Router with Opencode for enhanced LLM capabilities.

## Overview

OmniRoute is a unified AI proxy/router that routes any LLM through one endpoint with multi-provider support (OpenAI, Anthropic, Gemini, DeepSeek, Groq, xAI, Mistral, Fireworks, Cohere, etc.) featuring:
- **MCP Server** (16+ tools for agent control)
- **A2A v0.3 Protocol** (Agent-to-Agent orchestration)
- **Multi-provider routing** with intelligent load balancing
- **Provider health monitoring** and circuit breaker patterns
- **Cost tracking** and usage analytics
- **Security features** including prompt injection detection
- **API Key Management** with model-level permissions
- **OAuth Token Management** for Claude Code, Codex, Gemini CLI, Copilot, Kiro, Qwen, iFlow

## When to Use

Use this skill when:
- You want to route LLM requests through multiple providers for reliability
- You need access to OmniRoute's MCP server for agent control
- You want to leverage A2A protocol for multi-agent workflows
- You need intelligent load balancing and failover between LLM providers
- You want to monitor provider health and costs
- You're building agentic workflows that benefit from multi-provider access

## Quick Reference

### Service Management
```bash
# Start OmniRoute service
sudo systemctl start omniroute

# Stop OmniRoute service
sudo systemctl stop omniroute

# Check service status
sudo systemctl status omniroute

# View logs
sudo journalctl -u omniroute -f
```

### API Endpoints
OmniRoute runs on port 20128 by default:

**Base URL**: `http://localhost:20128`
**API Version**: v1 (`/api/v1/*`)
**Authentication**: Bearer token (any string works for development)

- **OpenAI-compatible**: `http://localhost:20128/v1` (use with any API key string)
- **Provider Management**: `GET/POST/PUT/DELETE http://localhost:20128/api/v1/providers/`
- **Combos**: `GET/POST http://localhost:20128/api/v1/combos/`
- **Usage Analytics**: `GET http://localhost:20128/api/v1/usage/`
- **Cost Tracking**: `GET http://localhost:20128/api/v1/costs/`
- **Health Checks**: `GET http://localhost:20128/api/v1/health/`
- **Registered Keys API**: `POST http://localhost:20128/api/v1/registered-keys`

### MCP Server
OmniRoute provides an MCP (Model Context Protocol) server with 16 tools:

**Transports:**
- **stdio**: Local IDE integration (Claude Desktop, Cursor, VS Code)
- **SSE**: `/api/mcp/sse`
- **Streamable HTTP**: `/api/mcp/stream`

**Tools Available:**
1. `get_health` - System health status
2. `list_combos` - Available provider combinations
3. `get_combo_metrics` - Combo performance metrics
4. `switch_combo` - Switch active provider combo
5. `check_quota` - Check provider quota/usage
6. `route_request` - Route request through optimal provider
7. `cost_report` - Generate cost reports
8. `list_models_catalog` - Available models across providers
9. `simulate_route` - Simulate routing decision
10. `set_budget_guard` - Configure budget limits
11. `set_resilience_profile` - Configure retry/failover behavior
12. `test_combo` - Test provider combo connectivity
13. `get_provider_metrics` - Individual provider performance
14. `best_combo_for_task` - Recommend optimal combo for task type
15. `explain_route` - Explain routing decision rationale
16. `get_session_snapshot` - Get current session state

### A2A Protocol
OmniRoute implements Agent-to-Agent v0.3 protocol:

**Endpoints:**
- **Agent Card**: `GET /.well-known/agent.json`
- **Message Send**: `POST /api/a2a/tasks`
- **Message Stream**: `POST /api/a2a/tasks/[id]/stream`
- **Task Get**: `GET /api/a2a/tasks/[id]`
- **Task Cancel**: `POST /api/a2a/tasks/[id]/cancel`

**Skills:**
- `smart-routing` - Intelligent LLM provider selection
- `quota-management` - Provider quota monitoring and alerts

## Integration with Opencode

### As an LLM Provider
Configure Opencode to use OmniRoute as an OpenAI-compatible endpoint:
- **Base URL**: `http://localhost:20128`
- **API Key**: Not required (OmniRoute handles auth internally)
- **Models**: Use any model available through OmniRoute's provider network

### Using MCP Server in Opencode
Opencode can connect to OmniRoute's MCP server for enhanced agent capabilities:
1. Configure MCP client to connect to `http://localhost:20128/mcp/stream`
2. Use the 16 available tools for:
   - Dynamic provider switching based on performance
   - Cost-aware model selection
   - Health-aware routing
   - Usage monitoring and alerting

### Using A2A for Multi-Agent Workflows
Leverage OmniRoute's A2A implementation:
1. Register Opencode agents as A2A agents
2. Use smart-routing skill for optimal LLM selection
3. Implement quota management to prevent provider overuse
4. Chain multiple agents with specialized capabilities

## Configuration Files

### Environment Variables
Key environment variables in `/home/openclaw/omniroute-src/start-omniroute.sh`:
- `PORT=20128` - Service port
- `DATA_DIR=/home/openclaw/.config/omniroute` - Data directory
- `JWT_SECRET` - Authentication secret
- Provider-specific OAuth credentials

### Data Directory Structure
- `/home/openclaw/.config/omniroute/storage.sqlite` - Main database (provider connections, combos, usage logs)
- `/home/openclaw/.omniroute/` - Alternative data directory location
- `/home/openclaw/.omniroute/patches/` - OpenClaw patches (25 active)
- `/home/openclaw/.omniroute/db_backups/` - Automatic database backups

## Verification

### Check Service Health
```bash
# With authentication (any string works for development)
curl -s -H "Authorization: Bearer any-string" http://localhost:20128/api/v1/health | jq .
```

### List Available Providers
```bash
curl -s -H "Authorization: Bearer any-string" http://localhost:20128/api/v1/providers | jq .
```

### Test OpenAI-Compatible Endpoint
```bash
# Use with Cursor, Cline, Claude Desktop, Codex, etc.
# Base URL: http://localhost:20128/v1
# API Key: any-string
```

### Check MCP Server Availability
```bash
curl -s http://localhost:20128/.well-known/agent.json | jq .
```

## Troubleshooting

### Service Won't Start
1. Check logs: `sudo journalctl -u omniroute -f`
2. Verify Node.js version: `node -v` (should be v22.22.x)
3. Check port availability: `sudo lsof -i :20128`
4. Verify database integrity: Check `/home/openclaw/.omniroute/storage.sqlite`

### API Returns 404 or Auth Error
1. Verify service is running: `sudo systemctl status omniroute`
2. Use correct endpoint: `/api/v1/` (not `/api/`)
3. Add auth header: `-H "Authorization: Bearer any-string"`
4. Check dashboard at: `http://localhost:20128/dashboard`

### Authentication Required (AUTH_001)
- Version 3.3.x requires API key authentication
- Use `/v1` endpoint for OpenAI-compatible API (accepts any API key string)
- For `/api/v1/*` endpoints, add `-H "Authorization: Bearer your-key"`

### Database Issues
1. Check backup directory: `/home/openclaw/.omniroute/db_backups/`
2. Restore from backup if needed
3. Verify file permissions on storage.sqlite

## Best Practices

1. **Provider Configuration**: Configure multiple providers for redundancy
2. **Health Monitoring**: Regularly check `/api/health` endpoint
3. **Cost Awareness**: Use cost tracking APIs to monitor usage
4. **Load Balancing**: Leverage combo configurations for intelligent routing
5. **Security**: Keep JWT_SECRET and provider credentials secure
6. **Updates**: Regularly pull updates and run database migrations
7. **Backups**: Monitor automatic backups in `/home/openclaw/.omniroute/db_backups/`

## Related Skills
- `using-superpowers` - Always invoke this first
- `dev-browser` - For testing web interfaces
- `git-master` - For version control of configurations
- `automation/n8n` - For workflow integration with A2A
- `mckinsey-research` - For strategic provider evaluation

---
**Remember**: Always check if OmniRoute service is running before attempting to use its features. The integration provides powerful multi-provider LLM capabilities that can significantly enhance Opencode's agent capabilities.