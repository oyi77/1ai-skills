# Installation

This repository contains a collection of skills for OpenClaw.

## 🤖 For AI Agents

Choose one of the following methods to install:

### Method 1: Clone Repository (Recommended)

Clone the repository directly into your OpenClaw workspace:

```bash
# Linux/macOS
git clone https://github.com/oyi77/1ai-skills.git ~/.openclaw/workspace/skills/1ai-skills

# Windows
git clone https://github.com/oyi77/1ai-skills.git C:\Users\USER\.openclaw\workspace\skills\1ai-skills
```

### Method 2: Copy Skills Folder

If you already have a workspace with other content:

1. Clone this repo to a temporary location
2. Copy the contents of this repo into your workspace's `skills/` directory
3. **IMPORTANT**: Do not overwrite critical files like `.git`, `memory/`, or config files.

```bash
# Example
cp -r 1ai-skills/* ~/.openclaw/workspace/skills/
```

### Method 3: ClawHub CLI

If you have the `clawhub` CLI tool installed:

```bash
clawhub install oyi77/1ai-skills
```

### ✨ Final Step: Initialize

Run the installation script to verify and boot up the system (Works on Windows/Mac/Linux):

```bash
cd ~/.openclaw/workspace/skills/1ai-skills
npm install
```

---

## 👤 For Humans

1. **Navigate to your workspace skills folder**:
   ```bash
   cd ~/.openclaw/workspace/skills
   ```

2. **Clone the repository**:
   ```bash
   git clone https://github.com/oyi77/1ai-skills.git
   ```

3. **Verify installation**:
   ```bash
   ls -l 1ai-skills/SKILL_INDEX.json
   ```

4. **(Optional) Configure Environment**:
   Copy `.env.example` to `.env` inside the `1ai-skills` folder and add your API keys.

---

## 📦 Verified Skills Reference

Once installed, the following skill paths will be available:

- `marketing/social-media-upload`
- `operations/payment-invoicing`
- `core/find-skills`
- `content/grok-video-generation`
- ...and 70+ more.
