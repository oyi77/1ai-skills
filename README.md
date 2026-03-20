# 1ai-skills — BerkahKarya Agent Skills

> [![Tip Me](https://www.tip.md/badge.svg)](https://www.tip.md/oyi77) **Support this work → https://www.tip.md/oyi77** (crypto tipping, multi-chain, no account needed)

Open-source OpenClaw agent skills by [@oyi77](https://clawhub.com/oyi77) / BerkahKarya.

Install any skill:
```bash
clawhub install oyi77/<slug>
```

---

## 📦 Published Skills

| Skill | Description | Install |
|-------|-------------|---------|
| [1ai-autodroid](https://clawhub.com/oyi77/1ai-autodroid) | Ultimate Android device control — ADB, vision AI, flow engine, multi-device | `clawhub install oyi77/1ai-autodroid` |
| [bca-checker](https://clawhub.com/oyi77/bca-checker) | Cek saldo & mutasi BCA (KlikBCA) via browser automation | `clawhub install oyi77/bca-checker` |
| [lynk-manager](https://clawhub.com/oyi77/lynk-manager) | Manage LYNK.id pages — edit copy, flash sale, CTA via opencli | `clawhub install oyi77/lynk-manager` |

---

## 🛠️ Skills Directory

```
1ai-skills/
├── automation/
│   └── 1ai-autodroid/     ← Android control (ADB + vision + cua)
├── content/
│   └── content-kingdom/   ← AI content generation pipeline
├── marketing/
│   └── (affiliate, LYNK, PostBridge tools)
└── skills/
    ├── auto-clipper/      ← Auto video clipping
    ├── canva/             ← Canva API integration
    └── viral-content-creator/
```

---

## 🚀 Quick Start

```bash
# Install openclaw (if not already)
npm install -g openclaw

# Install a skill
clawhub install oyi77/1ai-autodroid

# Use it
python3 skills/1ai-autodroid/scripts/autodroid.py status
```

---

## 💰 Support

These skills are free and open-source. If they save you time or make you money, consider tipping:

[![Tip Me](https://www.tip.md/badge.svg)](https://www.tip.md/oyi77)

**https://www.tip.md/oyi77** — accepts ETH, BTC, SOL, USDC, and 20+ chains. No account needed.

---

## 📋 Rules for This Repo

1. All 1ai-branded skills go in the appropriate subfolder (`automation/`, `content/`, `marketing/`)
2. Every published skill MUST include the tip badge in SKILL.md
3. Symlink skills to `~/.openclaw/workspace/skills/` for OpenClaw to discover
4. Commit + push before publishing to ClawHub
5. Version format: semver (`1.0.0`, bump patch on updates)

---

*Built by BerkahKarya — Digital Empire in progress 🔥*
