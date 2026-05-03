# Marketplace Submission Guide

This document provides step-by-step instructions for submitting 1ai-Skills to various AI marketplaces.

## Prerequisites

- GitHub account: https://github.com/oyi77 ✓
- Repository pushed: https://github.com/oyi77/1ai-skills ✓
- Skills verified: 135 skills, 0 credential leaks ✓

---

## ✅ 1. OpenAI GPT Store

**URL:** https://chat.openai.com/gpts/store  
**Requirements:** ChatGPT Plus subscription ($20/month)

### Steps:

1. Log in to ChatGPT with Plus subscription
2. Navigate to "Explore GPTs" → "Create"
3. Click "Create new GPT"
4. Configure:
   - **Name:** 1ai-Skills
   - **Description:** World's largest AI skill ecosystem with 135 world-class expert personas
   - **Instructions:** Paste from `manifests/openai-gpt-store.json` → `gpt_configuration.system_prompt`
5. Upload icon: Use `assets/icon.png` (create if needed)
6. Add Actions (if needed for external APIs)
7. Click "Save" → "Publish to GPT Store"
8. Set visibility: Public
9. Add categories: Productivity, Developer Tools
10. Submit for review

### Time to approval: 1-7 days

---

## ✅ 2. Claude App Store

**URL:** https://console.anthropic.com/ (App publishing section)  
**Requirements:** Anthropic API access

### Steps:

1. Log in to Anthropic Console
2. Navigate to "Apps" or "Publish"
3. Click "Create New App"
4. Fill details:
   - **Name:** 1ai-Skills
   - **Description:** See `manifests/claude-app-store.json`
   - **Instructions:** Paste from manifest `claude_configuration.project_instructions`
5. Configure:
   - Model: claude-3-sonnet-20240229
   - Temperature: 0.7
   - Max tokens: 4096
6. Upload assets:
   - Icon: `assets/icon.png`
   - Banner: `assets/banner.png`
7. Set pricing: Free
8. Add donation link: https://www.tip.md/oyi77
9. Submit for review

### Time to approval: 3-14 days

---

## ✅ 3. LangChain Hub

**URL:** https://smith.langchain.com/hub  
**Requirements:** LangChain account + API key

### Steps:

1. Create LangChain account at https://smith.langchain.com/
2. Generate API key from Settings
3. Install LangChain CLI:
   ```bash
   pip install langchain-cli
   ```
4. Login:
   ```bash
   langchain login
   ```
5. Navigate to repository:
   ```bash
   cd /path/to/1ai-skills
   ```
6. Push to Hub:
   ```bash
   langchain hub push oyi77/1ai-skills --manifest manifests/langchain-hub.yaml
   ```
7. Or use API:
   ```python
   from langchain import hub
   hub.push("oyi77/1ai-skills", "README.md")
   ```
8. Add metadata via web UI
9. Submit for public visibility

### Time to approval: 1-3 days

---

## ✅ 4. Hugging Face

**URL:** https://huggingface.co/spaces  
**Requirements:** Hugging Face account (free)

### Steps:

1. Create HF account: https://huggingface.co/join
2. Create new Space:
   - Go to https://huggingface.co/new-space
   - **Name:** 1ai-skills
   - **License:** MIT
   - **SDK:** Static (or Gradio for demo)
3. Clone the space:
   ```bash
   git clone https://huggingface.co/spaces/oyi77/1ai-skills
   ```
4. Copy repository files:
   ```bash
   cp -r /home/openclaw/.opencode/skills/* /path/to/hf-space/
   ```
5. Add README:
   ```bash
   cp manifests/huggingface-space.md README.md
   ```
6. Commit and push:
   ```bash
   git add .
   git commit -m "Initial release: 135 world-class skills"
   git push
   ```
7. Configure Space settings:
   - Enable "Public"
   - Add tags: ai, skills, personas, productivity
8. Create Collection:
   - Go to https://huggingface.co/collections/new
   - Name: "1ai-Skills Ecosystem"
   - Add all related repos

### Time to publish: Immediate (after push)

---

## 📋 Submission Checklist

### Before Submitting:
- [ ] Verify all 135 skills have SKILL.md
- [ ] Check no API keys/secrets in any files
- [ ] Update version numbers in all manifests
- [ ] Create assets (icon.png, banner.png)
- [ ] Final README review
- [ ] Tag release: `git tag v1.0.0`

### Assets Needed:
- [ ] Icon: 512x512 PNG (create with Canva/Figma)
- [ ] Banner: 1280x640 PNG (for HF/Claude)
- [ ] Screenshots: 3-5 showing skill usage

### Post-Submission:
- [ ] Monitor approval status
- [ ] Respond to reviewer feedback
- [ ] Update README with marketplace badges
- [ ] Announce on social media
- [ ] Track download/stars metrics

---

## 🔗 Quick Links

| Marketplace | URL | Status | Cost |
|-------------|-----|--------|------|
| GitHub | https://github.com/oyi77/1ai-skills | ✅ Live | Free |
| OpenAI GPT Store | https://chat.openai.com/gpts/store | ⏳ Pending | $20/mo |
| Claude App Store | https://console.anthropic.com | ⏳ Pending | API access |
| LangChain Hub | https://smith.langchain.com/hub | ⏳ Pending | Free |
| Hugging Face | https://huggingface.co/spaces | ⏳ Pending | Free |

---

## 💝 Support Development

**Donation:** https://www.tip.md/oyi77

Your support helps maintain and expand this ecosystem of world-class AI skills.

---

**Last Updated:** 2025-05-04  
**Version:** 1.0.0  
**Total Skills:** 135 across 10 categories
