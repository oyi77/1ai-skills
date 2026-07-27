---
name: discord
description: Use when discord Automation Hub — Bot and Webhooks for community management, DevOps notifications, and interactive servers. Monetize through community infrastructure-as-a-service.
domain: integrations
author: mahipal
license: Apache-2.0
subdomain: integrations
tags:
- api
- automation
- bot
- community
- discord
- integrations
- notifications
- third-party
- webhook
- communication
version: 1.0.0
---

# Discord Automation Hub



## When Not to Use

- **Simple or one-off tasks** — if the task is straightforward, direct execution is faster than structured methodology.
- **Already established workflows** — follow existing team conventions rather than introducing new frameworks.
- **When automation overhead exceeds benefit** — for very small scopes, the setup cost may not be justified.


## Dependencies

- Python 3.8+ or Node.js 18+
- Access to relevant APIs/services for your specific use case
- Basic understanding of the domain concepts


## Commands

```bash
# Refer to the skill's usage section for specific commands
# Adapt these to your workflow
```
## Money-Making Overview

Discord has outgrown gaming — it's now the primary community platform for dev tools, DAOs, NFT projects, open-source communities, and online courses. Automating Discord is a growing market:

| Service | ROI Estimate | Market |
|---------|-------------|--------|
| Custom bot development (moderation, economy, utility) | $2K-$10K/bot | Communities, DAOs, online courses |
| DevOps/CI-CD notification integration | $500-$2K/setup + $200-1K/mo | Dev communities, open-source projects |
| Community onboarding & verification bot | $1K-$4K/setup | Paid communities, token-gated servers |
| Webhook-based alert pipeline (server monitoring, crypto, sports) | $300-$1.5K/setup | Traders, gamers, server admins |
| Discord → third-party sync (roles, members, events) | $1K-$5K/integration | Event platforms, e-learning, SaaS |
| Moderation automation & anti-spam | $500-$2K/setup + $200-500/mo | Growing communities (1000+ members) |

**Combined monthly recurring potential: $2K-$8K/client** (community infrastructure retainer).

### Who Pays
- **Web3/DAO projects** — token-gated bots, community management ($2-8K)
- **Online course creators** — student role management, announcements ($500-2K)
- **Open-source maintainers** — release/webhook notification bots ($200-1K/mo)
- **Gaming communities** — custom economy/utility bots ($1-5K/setup)
- **Dev tool companies** — product announcement & support servers ($2-6K)
- **Event organizers** — event → Discord sync, RSVP management ($500-3K)

## Combined Capabilities

| Capability | Scope | Output |
|-----------|-------|--------|
| **Discord Bot** | Full Discord API: messages, slash commands, modals, buttons, select menus, roles, voice, threads, embeds, file uploads, event handlers | Python/JS bot with discord.py or discord.js |
| **Discord Webhooks** | Simple HTTP push notifications: text, rich embeds, files, usernames, avatars, channel routing | curl scripts, embedded webhook URLs |

## Authentication & Setup

```bash
# Mode 1: Bot Token (full bot — interactive commands, events, reactions)
# Create at: https://discord.com/developers/applications → New Application → Bot
export DISCORD_BOT_TOKEN="MTE5xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
# Invite bot with scopes: bot, applications.commands
# https://discord.com/api/oauth2/authorize?client_id=CLIENT_ID&permissions=PERMISSIONS&scope=bot+applications.commands

# Mode 2: Webhook URL (simplest — push notifications only)
# Create in Discord channel: Edit Channel → Integrations → Webhooks → New Webhook
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/123456/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### Required Intents (discord.py / discord.js)

| Intent | Feature |
|--------|---------|
| `message_content` | Read message content (required for commands) |
| `guild_members` | Track member join/leave, manage roles |
| `guild_messages` | Receive message events |
| `message_reactions` | Track reaction events |
| `guilds` | Know which servers the bot is in |

```python
# Shared setup
import os, requests, json

DISCORD_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK_URL")
HEADERS = {
    "Authorization": f"Bot {DISCORD_TOKEN}",
    "Content-Type": "application/json",
}
API = "https://discord.com/api/v10"
```

## Concrete Action Flows

### Flow 1: Webhook Notification (simplest — push from anywhere)

Send rich notifications from any CI/CD, monitoring, or cron job:

```bash
#!/usr/bin/env bash
# discord-notify.sh — Send a rich embed via webhook
# Usage: ./discord-notify.sh "Deploy" "v2.3.1 to production" "3066993" "#deployments"

WEBHOOK_URL="${DISCORD_WEBHOOK_URL}"
TITLE="${1:-Notification}"
DESCRIPTION="${2:-}"
COLOR="${3:-3066993}"  # 3066993=green, 15158332=red, 15105570=yellow
USERNAME="${4:-Deploy Bot}"

curl -s -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d "$(cat <<EOF
{
  "username": "$USERNAME",
  "avatar_url": "https://cdn-icons-png.flaticon.com/512/25/25231.png",
  "embeds": [{
    "title": "$TITLE",
    "description": "$DESCRIPTION",
    "color": $COLOR,
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "footer": {"text": "Automation Hub"}
  }]
}
EOF
)"
```

```python
# Python version — reusable webhook sender
def send_webhook(webhook_url, content=None, embed=None, username=None):
    """Send a message or embed via Discord webhook."""
    payload = {}
    if content:
        payload["content"] = content
    if embed:
        payload["embeds"] = [embed]
    if username:
        payload["username"] = username

    resp = requests.post(webhook_url, json=payload)
    resp.raise_for_status()
    return resp

def build_embed(title, description, color=3066993, fields=None, footer=None):
    """Build a Discord embed dict."""
    embed = {
        "title": title,
        "description": description,
        "color": color,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    if fields:
        embed["fields"] = fields
    if footer:
        embed["footer"] = {"text": footer}
    return embed

# Example: CI/CD deploy notification
send_webhook(
    webhook_url=os.environ["DISCORD_WEBHOOK_URL"],
    embed=build_embed(
        title="Deployment Complete :rocket:",
        description="Version v2.3.1 deployed to production",
        color=3066993,
        fields=[
            {"name": "Branch", "value": "main", "inline": True},
            {"name": "Duration", "value": "2m 34s", "inline": True},
            {"name": "Status", "value": ":white_check_mark: Success", "inline": True},
        ],
        footer="CI/CD Pipeline",
    ),
    username="CI/CD Bot",
)
```

### Flow 2: Discord Bot with Slash Commands (discord.py)

Full bot with interactive commands:

```python
#!/usr/bin/env python3
"""discord-bot.py — Full Discord bot with slash commands."""
import os, discord
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True
intents.guild_members = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name="ping", description="Check bot latency")
async def ping(interaction: discord.Interaction):
    latency = round(client.latency * 1000)
    await interaction.response.send_message(f"Pong! `{latency}ms`")

@tree.command(name="announce", description="Send an announcement to a channel")
@app_commands.describe(channel="Target channel", title="Announcement title", message="Announcement body")
async def announce(interaction: discord.Interaction, channel: discord.TextChannel, title: str, message: str):
    embed = discord.Embed(
        title=title,
        description=message,
        color=discord.Color.blue(),
        timestamp=discord.utils.utcnow(),
    )
    embed.set_footer(text=f"Announced by {interaction.user.display_name}")
    await channel.send(embed=embed)
    await interaction.response.send_message(f":white_check_mark: Announced in {channel.mention}", ephemeral=True)

@tree.command(name="userinfo", description="Get info about a user")
@app_commands.describe(member="The member to look up")
async def userinfo(interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    embed = discord.Embed(
        title=member.display_name,
        color=member.color or discord.Color.default(),
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Joined", value=member.joined_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Roles", value=", ".join(r.mention for r in member.roles[1:]) or "None", inline=False)
    await interaction.response.send_message(embed=embed)

@tree.command(name="embed", description="Send a rich embed message")
@app_commands.describe(title="Embed title", description="Embed description", color="Hex color (e.g. #00ff00)")
async def send_embed(interaction: discord.Interaction, title: str, description: str, color: str = "#3498db"):
    try:
        hex_color = int(color.lstrip("#"), 16)
    except ValueError:
        hex_color = 0x3498db
    embed = discord.Embed(title=title, description=description, color=hex_color, timestamp=discord.utils.utcnow())
    await interaction.response.send_message(embed=embed)

@client.event
async def on_ready():
    await tree.sync()
    print(f"Bot logged in as {client.user}")

client.run(os.environ["DISCORD_BOT_TOKEN"])
```

### Flow 3: DevOps Alert Pipeline (Webhook + Bot)

Route alerts from monitoring tools to Discord channels:

```bash
#!/usr/bin/env bash
# alert-pipeline.sh — Route alerts to Discord with severity routing
set -euo pipefail

WEBHOOK_BASE="${DISCORD_WEBHOOK_URL}"
SEVERITY="${1:-info}"
TITLE="${2:-Alert}"
MESSAGE="${3:-}}

color_map() {
  case "$1" in
    info)    echo "3066993"  ;;  # green
    warning) echo "15105570" ;;  # yellow
    error)   echo "15158332" ;;  # red
    critical) echo "10038562" ;; # dark red
    *)       echo "3066993"  ;;
  esac
}

COLOR=$(color_map "$SEVERITY")
case "$SEVERITY" in
  info)
    CHANNEL="#deployments" ;;
  warning)
    CHANNEL="#ops-warnings" ;;
  error|critical)
    CHANNEL="#incidents" ;;
esac

curl -s -X POST "$WEBHOOK_BASE" \
  -H "Content-Type: application/json" \
  -d "$(cat <<EOF
{
  "username": "Alert Bot ($SEVERITY)",
  "embeds": [{
    "title": "$TITLE",
    "description": "$MESSAGE",
    "color": $COLOR,
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "fields": [
      {"name": "Severity", "value": "$SEVERITY", "inline": true},
      {"name": "Source", "value": "Automation Pipeline", "inline": true}
    ]
  }]
}
EOF
)"
```

### Flow 4: Bot with Buttons and Modals (Interactive)

```python
"""interactive-bot.py — Discord bot with buttons and modals."""
import os, discord
from discord import app_commands, ui

class TicketModal(ui.Modal, title="Create a Support Ticket"):
    subject = ui.TextInput(label="Subject", placeholder="Brief description", max_length=100)
    description = ui.TextInput(label="Description", style=discord.TextStyle.paragraph, placeholder="Describe your issue in detail", max_length=1000)
    priority = ui.TextInput(label="Priority", placeholder="low / medium / high", default="medium", max_length=10)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"Ticket: {self.subject.value}",
            description=self.description.value,
            color={"low": 0x00ff00, "medium": 0xffff00, "high": 0xff0000}.get(self.priority.value.lower(), 0x3498db),
        )
        embed.add_field(name="Priority", value=self.priority.value, inline=True)
        embed.add_field(name="Created by", value=interaction.user.mention, inline=True)

        # Find or create a ticket channel
        category = discord.utils.get(interaction.guild.categories, name="Tickets")
        if category:
            ticket_channel = await interaction.guild.create_text_channel(
                f"ticket-{interaction.user.name}",
                category=category,
                topic=self.subject.value,
            )
            await ticket_channel.send(embed=embed)
            await interaction.response.send_message(f":white_check_mark: Ticket created in {ticket_channel.mention}", ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed)
            await interaction.response.send_message(":white_check_mark: Ticket submitted (no Ticket category found)", ephemeral=True)

class TicketButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Ticket", style=discord.ButtonStyle.primary, emoji=":ticket:")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TicketModal())

@tree.command(name="ticket", description="Open a support ticket")
async def ticket(interaction: discord.Interaction):
    await interaction.response.send_message("Click below to create a ticket:", view=TicketButton())
```

### Flow 5: Welcome & Role Management Bot

Automate server onboarding:

```python
"""welcome-bot.py — Welcome messages and role management."""
import os, discord
from discord import app_commands

intents = discord.Intents.default()
intents.guild_members = True
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

WELCOME_CHANNEL_ID = int(os.environ.get("WELCOME_CHANNEL_ID", "0"))
VERIFIED_ROLE_NAME = "Member"

@client.event
async def on_member_join(member):
    """Send welcome message when a new member joins."""
    if WELCOME_CHANNEL_ID:
        channel = client.get_channel(WELCOME_CHANNEL_ID)
        if channel:
            embed = discord.Embed(
                title=f"Welcome {member.display_name}! :wave:",
                description=(
                    f"Welcome to **{member.guild.name}**!\n\n"
                    "Please check the <#rules-channel> and assign yourself roles in <#roles-channel>.\n"
                    f"Member #{len(member.guild.members)}"
                ),
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow(),
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            await channel.send(embed=embed)

@tree.command(name="role", description="Assign or remove a role")
@app_commands.describe(role="The role to toggle")
async def role(interaction: discord.Interaction, role: discord.Role):
    if role >= interaction.guild.me.top_role:
        await interaction.response.send_message("I cannot assign that role.", ephemeral=True)
        return
    if role in interaction.user.roles:
        await interaction.user.remove_roles(role)
        await interaction.response.send_message(f"Removed {role.mention}", ephemeral=True)
    else:
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f"Added {role.mention}", ephemeral=True)

@tree.command(name="purge", description="Bulk delete messages")
@app_commands.describe(amount="Number of messages to delete (1-100)")
@app_commands.checks.has_permissions(manage_messages=True)
async def purge(interaction: discord.Interaction, amount: int):
    if amount < 1 or amount > 100:
        await interaction.response.send_message("Must be between 1 and 100.", ephemeral=True)
        return
    deleted = await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"Deleted {len(deleted)} messages.", ephemeral=True, delete_after=5)

@client.event
async def on_ready():
    await tree.sync()
    print(f"Welcome bot ready as {client.user}")

client.run(os.environ["DISCORD_BOT_TOKEN"])
```

### Flow 6: Cross-Platform Notification Bridge

Forward alerts from multiple sources to Discord:

```python
#!/usr/bin/env python3
"""bridge-bot.py — Forward alerts from GitHub/GitLab/PagerDuty to Discord."""
import os, json, hmac, hashlib
from flask import Flask, request

app = Flask(__name__)
WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

def send_to_discord(payload):
    requests.post(WEBHOOK_URL, json=payload)

@app.route("/webhook/github", methods=["POST"])
def github_webhook():
    """Receive GitHub webhook events and forward to Discord."""
    event = request.headers.get("X-GitHub-Event", "push")
    payload = request.json

    if event == "push":
        commits = len(payload.get("commits", []))
        embed = {
            "title": f"Push to {payload['ref'].split('/')[-1]}",
            "description": f"{commits} commit(s) by {payload['pusher']['name']}",
            "url": payload["compare"],
            "color": 3066993,
        }
    elif event == "issues":
        action = payload["action"]
        issue = payload["issue"]
        embed = {
            "title": f"Issue {action}: {issue['title']}",
            "url": issue["html_url"],
            "color": 15158332 if action in ("opened",) else 15105570,
        }
    elif event == "release":
        release = payload["release"]
        embed = {
            "title": f"Release: {release['tag_name']}",
            "description": release.get("name", ""),
            "url": release["html_url"],
            "color": 3066993,
        }
    else:
        return "ignored", 200

    send_to_discord({"embeds": [embed]})
    return "ok", 200

@app.route("/webhook/custom", methods=["POST"])
def custom_webhook():
    """Generic webhook receiver — accepts any JSON with title/description."""
    data = request.json
    send_to_discord({
        "username": data.get("username", "Bridge Bot"),
        "embeds": [{
            "title": data.get("title", "Notification"),
            "description": data.get("message", ""),
            "color": data.get("color", 3066993),
            "fields": data.get("fields", []),
        }],
    })
    return "ok", 200

if __name__ == "__main__":
    app.run(port=8080)
```

## First Action in 60 Minutes

```
00:00-05:00 — Go to https://discord.com/developers/applications → New Application → Bot
05:00-10:00 — Copy bot token, enable required intents (message_content, guild_members)
10:00-15:00 — Create a webhook in a test channel (Channel Settings → Integrations → Webhooks)
15:00-20:00 — Test webhook: curl -X POST $WEBHOOK_URL -d '{"content":"Hello"}'
20:00-25:00 — Invite bot to server with bot + applications.commands scope
25:00-35:00 — Run discord.py bot with /ping slash command — verify it responds
35:00-40:00 — Add /embed command to send rich embeds
40:00-45:00 — Add /announce command to post to specific channels
45:00-50:00 — Build DevOps alert pipeline (bash script → webhook)
50:00-55:00 — Test alert pipeline with error, warning, and info severities
55:00-60:00 — Set up a simple webhook bridge for GitHub push events
```

**By the end of 60 minutes:**
- Discord bot running with slash commands
- Webhook URL tested and working
- Rich embeds with fields and colors
- Alert pipeline routing by severity
- GitHub → Discord webhook bridge
- Reusable infrastructure to sell as community automation

## Anti-Rationalization Table

| Rationalization | Reality |
|---------------|---------|
| "Webhooks are enough for everything" | Webhooks are one-way (send only). Bots can read, react, manage roles, and handle interactive components. |
| "I don't need intents" | Without `message_content` intent, your bot cannot read message content (enforced by Discord since Sept 2022). |
| "Embeds add complexity without value" | Rich embeds increase engagement 5x over plain text. Use them for everything beyond simple replies. |
| "Slash commands replaced everything" | Buttons, select menus, and modals create rich interactive flows. Combine them with slash commands. |
| "I'll host the bot on a free tier" | Discord bots disconnect after ~30s of inactivity on most free platforms. Use a proper host or keepalive. |
| "Role management is too risky to automate" | Audit logs + permission checks make it safe. Always validate role hierarchy before assignment. |

## Output Format

```
discord-automation/
├── bot/
│   ├── discord-bot.py          # Full bot with slash commands
│   ├── welcome-bot.py          # Onboarding & role management
│   └── interactive-bot.py      # Buttons, modals, ticket system
├── notifier/
│   ├── discord-notify.sh       # Bash webhook sender
│   └── python-notify.py        # Python embed builder
├── pipeline/
│   └── alert-pipeline.sh       # Severity-based routing
├── bridge/
│   └── bridge-bot.py           # Cross-platform webhook receiver
└── requirements.txt            # discord.py, flask, requests
```

## Verification Checklist

- [ ] Bot token works for slash commands (responds to /ping)
- [ ] Webhook sends properly formatted messages to correct channel
- [ ] Rich embeds display with correct colors, fields, timestamps, footers
- [ ] Slash commands with options (channel, user, role) work correctly
- [ ] Modal submission creates ticket embed in target channel
- [ ] Welcome message fires on member join
- [ ] Role assignment/removal respects role hierarchy
- [ ] Purge command deletes messages and respects permissions
- [ ] Alert pipeline routes correctly by severity level
- [ ] Webhook bridge receives and forwards GitHub events
- [ ] Rate limits: 30 requests/second per bot (webhook: 5/2 seconds)
- [ ] Bot gracefully reconnects on disconnect (discord.py auto-reconnect)
- [ ] Money protocol: deliverable is packaged and billable


## When to Use
Use this skill when working with discord.


## Workflow
See the parent skill for authoritative workflow documentation.
