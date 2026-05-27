---
name: cloudflare-router
description: Cloudflare Router SKILL. Use when relevant to this domain.
persona:
  name: Matthew Prince
  title: The Edge Network Expert - Master of Global Routing
  expertise:
  - Edge Computing
  - CDN
  - Network Security
  - Global Routing
  philosophy: The network is the computer.
  credentials:
  - CEO of Cloudflare
  - Built one of the largest edge networks
  - Pioneer of serverless edge
  principles:
  - Route to nearest edge
  - Cache aggressively
  - Secure by default
  - Scale globally
---
# Cloudflare Router SKILL

Manage Cloudflare Tunnels, nginx reverse proxies, and DNS records from one place.

## When to Use

- Adding new subdomains pointing to local services
- Managing Cloudflare Tunnel ingress rules
- Generating nginx reverse proxy configs
- Deploying DNS records to Cloudflare
- Monitoring service health and status

## Quick Start

```bash
# Initialize with Cloudflare credentials
cloudflare-router init \
  --token "your-cf-api-token" \
  --zone "your-zone-id" \
  --tunnel "your-tunnel-id" \
  --domain "example.com"

# Add a subdomain mapping
cloudflare-router add api 3002 -d "Backend API"

# Generate configs
cloudflare-router generate

# Deploy DNS records
cloudflare-router deploy

# Check status
cloudflare-router status

# Start web dashboard
cloudflare-router dashboard
```

## MCP Tools

The following MCP tools are available for AI agents:

### cloudflare_router_list_mappings
List all subdomain to port mappings.

### cloudflare_router_add_mapping
Add or update a subdomain mapping.
- `subdomain` (required): Subdomain name (e.g., api, www, admin)
- `port` (required): Local port number to proxy to
- `description` (optional): Description of the service

### cloudflare_router_remove_mapping
Remove a subdomain mapping.
- `subdomain` (required): Subdomain name to remove

### cloudflare_router_toggle_mapping
Enable or disable a subdomain mapping.
- `subdomain` (required): Subdomain name
- `enabled` (required): Enable or disable the mapping

### cloudflare_router_generate
Generate nginx and Cloudflare tunnel configs from current mappings.

### cloudflare_router_deploy
Deploy DNS records to Cloudflare for all enabled mappings.

### cloudflare_router_status
Get system status including nginx, tunnel, and mappings info.

### cloudflare_router_list_dns
List all Cloudflare DNS records for the configured zone.

### cloudflare_router_verify_token
Verify Cloudflare API token is valid.

### cloudflare_router_get_config
Get current Cloudflare Router configuration.

## Configuration

Config is stored in `~/.cloudflare-router/config.yml`:

```yaml
cloudflare:
  api_token: "your-api-token"
  zone_id: "your-zone-id"
  tunnel_id: "your-tunnel-id"
  tunnel_credentials: "/path/to/credentials.json"
  domain: "example.com"

nginx:
  listen_port: 6969
  config_dir: "~/.cloudflare-router/nginx/sites"

server:
  port: 7070
  host: "0.0.0.0"
```

## How It Works

1. **Mappings**: Define subdomain → port mappings in `~/.cloudflare-router/mappings.yml`
2. **Nginx**: Generates nginx configs that proxy requests from subdomains to local ports
3. **Tunnel**: Generates Cloudflare tunnel ingress rules pointing to nginx
4. **DNS**: Creates CNAME records in Cloudflare pointing subdomains to the tunnel

## API Endpoints

When dashboard is running on port 7070:

- `GET /api/config` - Get config (token masked)
- `PUT /api/config` - Update config
- `GET /api/mappings` - List mappings
- `POST /api/mappings` - Add mapping
- `DELETE /api/mappings/:subdomain` - Remove mapping
- `PATCH /api/mappings/:subdomain` - Toggle mapping
- `POST /api/generate/nginx` - Generate nginx configs
- `POST /api/generate/tunnel` - Generate tunnel config
- `POST /api/deploy` - Deploy DNS records
- `POST /api/full-deploy` - Generate + deploy all
- `GET /api/status` - Get status
- `GET /api/dns` - List DNS records
- `GET /api/verify` - Verify token
- `GET /api/docs/swagger.json` - Swagger spec

## Example Workflow

```bash
# 1. Initialize
cloudflare-router init --token "xxx" --zone "yyy" --tunnel "zzz" --domain "example.com"

# 2. Add mappings
cloudflare-router add api 3002 -d "Backend API"
cloudflare-router add app 3000 -d "Frontend App"
cloudflare-router add admin 3001 -d "Admin Panel"

# 3. Generate configs
cloudflare-router generate

# 4. Deploy DNS records
cloudflare-router deploy

# 5. Start tunnel (if not already running)
cloudflared tunnel --config ~/.cloudflare-router/tunnel/config.yml run

# 6. Start nginx (if not already running)
nginx -c ~/.cloudflare-router/nginx/nginx.conf
```

## When NOT to Use

- [TODO: Add specific exclusion cases for this skill]
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- [TODO: Add behavioral signs the skill is being violated]
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] [TODO: Add specific evidence-based checklist items]
- [ ] All required outputs generated
- [ ] Success criteria met

