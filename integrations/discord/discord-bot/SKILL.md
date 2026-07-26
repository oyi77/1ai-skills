---
name: discord-bot
description: Use when discord Bot — Slash commands, modals, buttons, role management, event handlers, voice, threads, full Discord API integration. See parent skill for all Discord automation capabilities.
domain: integrations
tags:
- api
- bot
- discord
- integrations
version: 1.0.0
---

# Discord Bot

## Quick Reference

The Discord bot sub-skill covers interactive bot development — slash commands, modals, buttons, select menus, role management, voice state tracking, thread management, event handlers, and message reactions. This layers on the parent [Discord Automation Hub](../SKILL.md) which covers the broader bot+webhook ecosystem and money-making protocols.

**Use this when** you need a bot that listens, reacts, and interacts — not just pushes notifications.

## Overview

A Discord bot is an always-on WebSocket client that connects to Discord's Gateway API. Unlike webhooks (one-way push), bots can:
- **Read** messages, reactions, member joins/leaves
- **Respond** with slash commands, modals, buttons, context menus
- **Manage** roles, threads, channels, voice states
- **Handle** 30+ event types (messages, guild updates, voice, typing)

The parent skill's auth setup applies directly: bot token + intents. The parent's `discord-bot.py`, `welcome-bot.py`, and `interactive-bot.py` are the canonical templates.

## Quick Start

### 1. Register and Invite
```bash
# Create at https://discord.com/developers/applications → New Application → Bot
export DISCORD_BOT_TOKEN="MTE5xxxxxxxxxxxxxxxxxxxxxxxxx"
# Invite URL with scopes: bot, applications.commands
# https://discord.com/api/oauth2/authorize?client_id=CLIENT_ID&permissions=8&scope=bot+applications.commands
```

### 2. Enable Gateway Intents
In the Developer Portal → Bot → Privileged Gateway Intents, enable:
- `MESSAGE CONTENT INTENT` — required for reading message content
- `SERVER MEMBERS INTENT` — required for member join/leave events, role management
- `PRESENCE INTENT` — required for presence/status tracking

### 3. Run a Minimal Bot
```python
import os, discord
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name="ping", description="Check latency")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! `{round(client.latency*1000)}ms`")

@client.event
async def on_ready():
    await tree.sync()
    print(f"Ready as {client.user}")

client.run(os.environ["DISCORD_BOT_TOKEN"])
```

This is the minimal viable bot. See the parent skill for the full `/announce`, `/userinfo`, `/embed`, `/ticket`, and `/purge` command suite plus modals, buttons, and welcome message flows.

## Code Snippet: Component Interaction Pattern

```python
# Button + Modal pattern — core interactive flow
class FeedbackModal(ui.Modal, title="Send Feedback"):
    rating = ui.TextInput(label="Rating (1-5)", placeholder="5", max_length=1)
    comment = ui.TextInput(label="Comments", style=discord.TextStyle.paragraph, max_length=500)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Feedback Received", color=discord.Color.green())
        embed.add_field(name="Rating", value=self.rating.value)
        embed.add_field(name="Comment", value=self.comment.value or "None")
        await interaction.response.send_message(embed=embed, ephemeral=True)

class FeedbackButton(discord.ui.View):
    @discord.ui.button(label="Give Feedback", style=discord.ButtonStyle.primary)
    async def on_click(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(FeedbackModal())

@tree.command(name="feedback")
async def feedback(interaction: discord.Interaction):
    await interaction.response.send_message("Click to give feedback:", view=FeedbackButton())
```

## Verification Checklist

- [ ] Bot connects and slash commands sync (`tree.sync()` in `on_ready`)
- [ ] Required intents are enabled in Developer Portal (message_content, guild_members)
- [ ] Bot role is higher than roles it manages (Discord hierarchy enforcement)
- [ ] Ephemeral responses used for user-specific interactions (`ephemeral=True`)
- [ ] Bot reconnects on disconnect (discord.py handles auto-reconnect by default)

## When to Use

Use when discord Bot — Slash commands, modals, buttons, role management, event handlers, voice, threads, full Discord API integration. See parent skill for all Discord automation capabilities.

## Workflow

Execute these steps sequentially:

### 1. Register and Invite
```bash
# Create at https://discord.com/developers/applications → New Application → Bot
export DISCORD_BOT_TOKEN="MTE5xxxxxxxxxxxxxxxxxxxxxxxxx"
# Invite URL with scopes: bot, applications.commands
# https://discord.com/api/oauth2/authorize?client_id=CLIENT_ID&permissions=8&scope=bot+applications.commands
```

### 2. Enable Gateway Intents
In the Developer Portal → Bot → Privileged Gateway Intents, enable:
- `MESSAGE CONTENT INTENT` — required for reading message content
- `SERVER MEMBERS INTENT` — required for member join/leave events, role management
- `PRESENCE INTENT` — required for presence/status tracking

### 3. Run a Minimal Bot
```python
import os, discord
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name="ping", description="Check latency")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! `{round(client.latency*1000)}ms`")

@client.event
async def on_ready():
    await tree.sync()
    print(f"Ready as {client.user}")

client.run(os.environ["DISCORD_BOT_TOKEN"])
```

This is the minimal viable bot. See the parent skill for the full `/announce`, `/userinfo`, `/embed`, `/ticket`, and `/purge` command suite plus modals, buttons, and welcome message flows.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll just use webhooks instead of a full bot" | Webhooks are send-only. Bots are required for reading messages, managing roles, handling reactions, or any two-way interaction. |
| "Slash commands alone are enough for the UI" | Modals and buttons reduce command complexity by 60%+ for multi-field input. Always prefer a modal over 5 required slash options. |
| "The bot will work fine on a free cloud host" | Discord expects <3s response on interactions and disconnects idle WebSocket connections. Use a persistent host with keepalive or a proper VPS. |
