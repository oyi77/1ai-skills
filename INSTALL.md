# Installation

You can install `1ai-skills` into your OpenClaw environment using either natural language instructions (for AI Agents) or manual steps (for Humans).

---

## 🤖 For AI Agents

If you are an AI agent setting up this environment, follow these instructions to install the skills.

### 1. Download Capabilities
Execute the following commands to clone the repository into the standard skills directory:

```bash
mkdir -p workspace/skills
cd workspace/skills
git clone https://github.com/paijo/1ai-skills.git
```

### 2. Configure Activation
Locate the OpenClaw configuration file (typically `config.json`) and update the `skills_paths` to include the new directory.

```json
{
  "skills_paths": [
    "./workspace/skills/1ai-skills"
  ],
  "activation_rules_path": "./workspace/skills/1ai-skills/.skill-activation.json"
}
```

### 3. Verify Installation
Run the skill listing command to confirm the new skills are loaded:

```bash
./openclaw skills list | grep "1ai-skills"
```

---

## 👤 For Humans

If you are manually setting up your OpenClaw environment, follow these steps.

### 1. clone the Repository
Navigate to your OpenClaw workspace and clone the repository:

```bash
# Go to your OpenClaw skills directory
cd ~/openclaw/workspace/skills

# Clone the repo
git clone https://github.com/paijo/1ai-skills.git
```

### 2. Update Configuration
Add the path to your OpenClaw `config.json` file:

```json
{
  "skills_paths": [
    "/absolute/path/to/openclaw/workspace/skills/1ai-skills"
  ],
  "activation_rules_path": "/absolute/path/to/openclaw/workspace/skills/1ai-skills/.skill-activation.json"
}
```

### 3. Set Environment Variables
Copy the example environment file and fill in your API keys:

```bash
cd 1ai-skills
cp .env.example .env
vim .env
```
(See `.env.example` for required keys like `TRIPAY_API_KEY`, `GROK_API_KEY`, etc.)

### 4. Restart OpenClaw
Restart your OpenClaw service to load the new skills.

---

## 🚀 Post-Installation

Once installed, your OpenClaw will have access to:
- **Operations**: Payment links, Invoices (TriPay, Midtrans)
- **Marketing**: Social media scheduler, Analytics
- **Content**: Video generation (Grok, Google), Video editing (FFmpeg)
- **Core**: Skill finder (Auto-discovery)

Test it with a prompt:
> "Find a skill to help me deploy Docker containers"
