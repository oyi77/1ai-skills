# Disk Layout — BerkahKarya Server

## Disks
| Device | Size | Mount | Type | Purpose |
|--------|------|-------|------|---------|
| /dev/sdb2 | 110GB SSD | / | OS drive | Code, config, services, DB |
| /dev/sda  | 916GB HDD | /mnt/data | Data drive | Media, assets, generated content |

## Auto-mount
fstab: `UUID=11489cec-a5f7-4870-824f-9f27c4500fb4 /mnt/data ext4 defaults,nofail,x-systemd.device-timeout=30s 0 2`

## Symlink Map (workspace → /mnt/data)

| Workspace Path | Real Path on HDD |
|---|---|
| workspace/remix_factory/ | /mnt/data/media/remix_factory/ |
| workspace/content_suite/output/ | /mnt/data/media/content_suite_output/ |
| workspace/animated_cartoon/ | /mnt/data/media/animated_cartoon/ |
| workspace/berkahkarya-compro/ | /mnt/data/berkahkarya/assets/berkahkarya-compro/ |
| workspace/public/ | /mnt/data/berkahkarya/assets/public/ |
| workspace/videos/ | /mnt/data/berkahkarya/media/videos/ |
| workspace/autopilot_affiliate_engine/ | /mnt/data/berkahkarya/media/autopilot_affiliate_engine/ |
| workspace/images/ | /mnt/data/berkahkarya/media/images/ |
| workspace/fonts/ | /mnt/data/berkahkarya/fonts/fonts/ |
| workspace/generated_posts/ | /mnt/data/berkahkarya/generated/generated_posts/ |
| workspace/training_samples/ | /mnt/data/berkahkarya/generated/training_samples/ |
| workspace/skills/1ai-skills/ | /mnt/data/berkahkarya/skills/1ai-skills/ |

## Rule: Apa yang WAJIB di SSD (/)
- Code (scripts/, skills SKILL.md, content_suite/*.py)
- Config (.env, AGENTS.md, SOUL.md, MEMORY.md)
- Services (MetaClaw, paperclip, tg-monitor)
- Databases (supabase configs, .vilona/)
- Memory (memory/*.md, notes/*.md)
- Logs (logs/)

## Rule: Apa yang WAJIB di HDD (/mnt/data)
- Video files (.mp4, .avi, .mov) > 10MB
- Image assets (.png, .jpg) > 50MB total
- Generated content (bulk posts, training data)
- Git repos yang jarang diubah (1ai-skills)
- Archived/historical data
- Downloads, source files

## Pattern untuk direktori baru
```bash
# Setiap dir baru > 50MB atau expected grow large:
mkdir -p /mnt/data/berkahkarya/{category}/{dir_name}
mv workspace/{dir_name} /mnt/data/berkahkarya/{category}/
ln -sfn /mnt/data/berkahkarya/{category}/{dir_name} workspace/{dir_name}
```
