---
name: discord-bot
description: Discord Bot. Use when performing discord bot tasks in integrations workflows.
domain: integrations
tags:
- api
- bot
- discord
- integrations
- third-party
- workflow
---
## When to Use

**Trigger phrases:**
- "discord bot"
- "Help me with discord bot"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

## Discord Bot

Build Discord bots

### Usage

```
/discord-bot <task>
```

### Features

- Automated execution
- Error handling
- Result validation

## How to Use

1. Create a Discord application at discord.com/developers/applications
2. Generate a bot token and configure permissions
3. Implement command handlers using discord.js or discord.py
4. Set up event listeners for messages, reactions, and interactions
5. Deploy to a persistent host and monitor rate limits

## Bot Command Structure

```python
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.command(name='status')
async def status(ctx):
    embed = discord.Embed(title="System Status", color=0x00ff00)
    embed.add_field(name="Uptime", value="99.9%")
    await ctx.send(embed=embed)

@bot.slash_command(name='deploy')
async def deploy(ctx, service: str):
    await ctx.respond(f"Deploying {service}...", ephemeral=True)
```

## Common Patterns

- Use slash commands for new bots (prefix commands are deprecated)
- Implement rate limit handling with exponential backoff
- Store persistent state in a database, not in-memory
- Use embeds for rich formatted responses

## When NOT to Use

- When the integration requires admin-level permissions on the target platform
- When the data exchange involves regulated information requiring encryption
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Integration does not handle API errors or service unavailability
- Agent does not verify data consistency across connected systems
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] API errors and service outages are handled with appropriate retry logic
- [ ] Data consistency is verified across all connected systems
- [ ] All required outputs generated
- [ ] Success criteria met

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
