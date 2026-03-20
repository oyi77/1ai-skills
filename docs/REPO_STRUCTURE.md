# Repository Structure & Contribution Rules
> WAJIB DIBACA sebelum edit/tambah file ke repo manapun.
> Last updated: 2026-03-21

---

## 🗺️ Dua Repo, Dua Tujuan

### 1. `oyi77/1ai-workspace` → `/home/openclaw/.openclaw/workspace`

**Isi:** Runtime agent — config, memory, scripts operasional, logs config, agent state.

```
1ai-workspace/
├── AGENTS.md          ← Operating rules (JANGAN HAPUS)
├── SOUL.md            ← Agent identity (JANGAN HAPUS)
├── USER.md            ← User context (JANGAN HAPUS)
├── MEMORY.md          ← Long-term memory index (JANGAN HAPUS)
├── HEARTBEAT.md       ← Heartbeat config (JANGAN HAPUS)
├── DIRECTIVE.md       ← Autonomous directives (JANGAN HAPUS)
├── TOOLS.md           ← Tool configs (JANGAN HAPUS)
├── IDENTITY.md        ← Agent identity (JANGAN HAPUS)
├── memory/            ← Daily memory logs (JANGAN HAPUS)
├── notes/             ← Topic notes (JANGAN HAPUS)
├── config/            ← Service configs
├── scripts/           ← Cron scripts & automation
├── logs/              ← Runtime logs (gitignored)
├── docs/              ← Internal documentation
│   └── REPO_STRUCTURE.md  ← (file ini)
└── skills/ → symlink ke 1ai-skills/
```

**JANGAN masukkan ke repo ini:**
- ❌ Skills baru (masuk ke 1ai-skills)
- ❌ Media files (mp4, mp3, jpg, png)
- ❌ Output files
- ❌ Temporary files
- ❌ Vendor dependencies (node_modules, venv)

---

### 2. `oyi77/1ai-skills` → `/mnt/data/berkahkarya/skills/1ai-skills`

**Isi:** Skills, tools, curated knowledge, documentation.

```
1ai-skills/
├── docs/              ← Documentation & curated resources
│   ├── CURATED_RESOURCES.md   ← Handpicked tools & use cases
│   ├── TOOLS_INVENTORY.md     ← Complete tools list + restore checklist
│   ├── handbook.md
│   └── policies.md
├── skills/            ← OpenClaw-installed skills (clawhub)
│   ├── video-frames/
│   ├── remotion-video-toolkit/
│   └── ...
├── content/           ← Content generation skills & scripts
├── marketing/         ← Marketing automation skills
├── trading/           ← Trading strategies & agents
├── automation/        ← Automation workflows
├── research/          ← Research tools & scripts
├── core/              ← Core agent skills
└── finance/           ← Finance & cashflow tools
```

**JANGAN masukkan ke repo ini:**
- ❌ Runtime config (AGENTS.md, SOUL.md, dll → itu di workspace)
- ❌ Media files besar (mp4, dll)
- ❌ Log files
- ❌ Temporary output files
- ❌ Duplikat dari workspace

---

## ✅ Rules — Wajib Diikuti

### Sebelum menambah file:

1. **Tanya dulu:** "Ini termasuk runtime config atau skill/doc?"
   - Runtime config → `1ai-workspace`
   - Skill/tool/doc → `1ai-skills`

2. **Cek existing:** Sudah ada belum? Jangan duplikat.

3. **Taruh di folder yang tepat:**
   - Skill baru dari clawhub → `1ai-skills/skills/<skill-name>/`
   - Script operasional → `1ai-workspace/scripts/`
   - Memory/notes → `1ai-workspace/memory/` atau `notes/`
   - Dokumentasi → `1ai-skills/docs/` atau `1ai-workspace/docs/`

4. **Commit message format:**
   ```
   feat: add <nama> skill/feature
   fix: <apa yang difix>
   docs: update/add documentation
   chore: cleanup/maintenance
   refactor: restructure tanpa behavior change
   ```

5. **Jangan commit:**
   - Files > 50MB (gunakan `.gitignore`)
   - Credentials atau API keys
   - Output/temp files
   - Log files

### .gitignore wajib include:

```gitignore
# Large media
*.mp4
*.mp3
*.png
*.jpg
*.jpeg
*.gif

# Output
output/
temp/
downloads/
remix_factory/

# Dependencies
node_modules/
venv/
venv-*/
*.pyc
__pycache__/

# Logs
logs/*.log

# Secrets
.env
*.key
credentials/
```

---

## 🔄 Workflow: Tambah Skill Baru

```bash
# 1. Install dari clawhub
cd /home/openclaw/.openclaw/workspace
clawhub install <skill-name>
# → Auto install ke workspace/skills/<skill-name>/

# 2. Commit ke 1ai-workspace (via -f karena skills di .gitignore)
git add -f skills/<skill-name>/
git commit -m "feat: install <skill-name> skill"
git push origin master

# 3. Jika skill ada di 1ai-skills dir struktur, tambah symlink
ln -sf /mnt/data/berkahkarya/skills/1ai-skills/skills/<skill-name> \
       /home/openclaw/.openclaw/workspace/skills/<skill-name>
```

---

## ⚠️ File yang TIDAK BOLEH Dipindah/Dihapus

File-file ini dibaca oleh OpenClaw saat startup dan runtime:

| File | Lokasi | Fungsi |
|------|--------|--------|
| `AGENTS.md` | workspace root | Operating rules |
| `SOUL.md` | workspace root | Agent identity/persona |
| `USER.md` | workspace root | User context |
| `MEMORY.md` | workspace root | Memory index |
| `HEARTBEAT.md` | workspace root | Heartbeat config |
| `DIRECTIVE.md` | workspace root | Autonomous directives |
| `TOOLS.md` | workspace root | Tool configurations |
| `IDENTITY.md` | workspace root | Agent identity |
| `memory/` | workspace | Daily memory logs |
| `scripts/` | workspace | Cron-referenced scripts |
| `config/` | workspace | Service configs |

**Memindah file-file ini AKAN BREAK OpenClaw runtime.**
