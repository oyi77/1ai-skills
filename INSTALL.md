# Installation

The standard installation method is to place this repository inside your OpenClaw `skills` directory.

> **Target Directory**: `~/.openclaw/workspace/skills/1ai-skills`

---

## 🤖 For AI Agents

Execute these exact commands to install:

```bash
# 1. Ensure skills directory exists
mkdir -p ~/.openclaw/workspace/skills

# 2. Clone repository directly into it
cd ~/.openclaw/workspace/skills
git clone https://github.com/paijo/1ai-skills.git

# 3. Verify installation
ls -l ~/.openclaw/workspace/skills/1ai-skills/SKILL_INDEX.json
```

*OpenClaw will automatically detect skills in this directory. No config changes needed.*

---

## 👤 For Humans

### Step 1: Install
Open your terminal and run:

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/paijo/1ai-skills.git
```

### Step 2: Configure Environment
Copy the environment file and add your keys:

```bash
cd 1ai-skills
cp .env.example .env
nano .env  # or use your favorite editor
```

### Step 3: Reload OpenClaw
Restart your OpenClaw instance to load the new skills.

---

## 🔍 Verification

To confirm everything is working, ask OpenClaw:

> "List all available skills from 1ai-skills"

Or run the CLI command:
```bash
openclaw skills list
```

---

## 📦 What gets installed?
- **Operations**: `payment-invoicing` (TriPay, Midtrans)
- **Marketing**: `social-media-upload`, `analytics-dashboard`
- **Content**: `grok-video-generation`, `google-flow`
- **Core**: `find-skills` (Auto-discovery)
- **Development**: `systematic-debugging`, `test-driven-development`
- ...and 40+ more!
