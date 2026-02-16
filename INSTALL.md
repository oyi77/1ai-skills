# Installing 1AI-Skills into OpenClaw

## Quick Install (Command Line)

If you are running OpenClaw locally, you can simply link this folder to your OpenClaw configuration.

### Option 1: Update OpenClaw Config

1. Locate your OpenClaw configuration file (usually `~/.openclaw/config.json` or `config.json` in your OpenClaw directory).
2. Add the path to this repository in the `skills_paths` section:

```json
{
  "skills_paths": [
    "/Users/paijo/1ai-skills"
  ],
  "activation_rules_path": "/Users/paijo/1ai-skills/.skill-activation.json"
}
```

### Option 2: Symlink Strategy (Recommended)

Link your skills directory to OpenClaw's skills folder:

```bash
# Assuming OpenClaw is at ~/openclaw
ln -s /Users/paijo/1ai-skills ~/openclaw/skills/1ai
```

---

## Verifying Installation

Once linked, verify OpenClaw can see your skills:

```bash
# List available skills
openclaw skills list

# Should show:
# - marketing/social-media-upload
# - operations/payment-invoicing
# - core/find-skills
# ... and 40+ others
```

---

## Using Your Skills (Prompt Examples)

You can now use natural language to trigger your skills!

### 1. **Content Workflow**
> "Generate a video about AI trends using Grok, then schedule it for X and LinkedIn for tomorrow at 10am."
(Triggers: `content/grok-video-generation` → `marketing/content-scheduler`)

### 2. **Payment & Invoicing**
> "Create an invoice for Client X for Rp 1.500.000 for 'Consulting Service' and send it with a Midtrans payment link."
(Triggers: `operations/payment-invoicing`)

### 3. **Find New Skills**
> "I need help with Docker deployment, do we have a skill for that?"
(Triggers: `core/find-skills` → searches community → installs `docker-expert`)

### 4. **Analytics**
> "Show me my social media growth for this week across all platforms."
(Triggers: `marketing/analytics-dashboard`)

---

## Environment Variables

Make sure to set these in your OpenClaw `.env` file:

```bash
# Social Media
X_API_KEY=...
INSTAGRAM_TOKEN=...
LINKEDIN_TOKEN=...

# Payments
TRIPAY_API_KEY=...
MIDTRANS_SERVER_KEY=...
LYNK_MERCHANT_KEY=...

# AI Services
GROK_API_KEY=...
GOOGLE_AI_KEY=...

# Email
SENDGRID_API_KEY=...
```

---

## Troubleshooting

**Skill not found?**
- Check absolute paths in `config.json`
- Ensure `.skill-activation.json` is valid JSON
- Restart OpenClaw service

**Permission errors?**
- Ensure OpenClaw has read/write access to `/Users/paijo/1ai-skills`
