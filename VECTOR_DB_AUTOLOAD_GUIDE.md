# Vector DB Auto-Load Guide

## 🎯 Tujuan
Biar tools Vector DB kepakai **otomatis** tanpa import manual setiap session.

---

## ✅ Cara 1: Session Startup (RECOMMENDED)

### File: `vector_db_startup.py`
Sudah dibuat di `~/.openclaw/workspace/`

### Cara pakai:
Add ke setiap session awal:

```python
exec(open('/home/openclaw/.openclaw/workspace/vector_db_startup.py').read())
```

### Maka tools tersedia:
- `vector_search(query, top_k=5)`
- `vector_index(content, title, source)`
- `vector_chunk(text, max_tokens=500)`
- `vector_status()`

---

## ✅ Cara 2: Import via Python Path

### Add ke session:
```python
import sys
sys.path.insert(0, '/home/openclaw/.openclaw/plugins')
sys.path.insert(0, '/home/openclaw/.openclaw/workspace/tools')

from vector_db_tools import *
```

---

## ✅ Cara 3: Shell Auto-Load

### Jalankan:
```bash
source ~/.openclaw/workspace/vector_db_autoload.sh
```

Maka alias `python3` otomatis load tools.

---

## 🎉 Cara 4: Quick One-Liner

Cara cepat tiap session:

```python
exec("import sys; sys.path.insert(0, '/home/openclaw/.openclaw/plugins'); sys.path.insert(0, '/home/openclaw/.openclaw/workspace/tools'); from vector_db_tools import vector_search, vector_index, vector_chunk, vector_status")
```

---

## 🔄 Cara 5: OpenClaw Plugin (Kalo Support)

Kalo OpenClaw support auto-load plugins:

Tambahkan ke `~/.openclaw/openclaw.json`:
```json
"startup": [
  "exec(open('/home/openclaw/workspace/vector_db_startup.py').read())"
]
```

**Tapi belum tentu support.**

---

## ✅ Recommended: Cara 1 + 4

Cara paling mudah dan reliable:

1. **Startup script** - `vector_db_startup.py`
2. **One-liner** - exec command cepat

---

## 🎯 Cara Pakai Sekarang

**Coba di session ini:**

```python
exec(open('/home/openclaw/.openclaw/workspace/vector_db_startup.py').read())

# Sekarang tools available
results = vector_search("cara trading", top_k=3)
```

---

## 📁 Files Dibuat

| File | Purpose |
|------|---------|
| `tools/vector_db_tools.py` | Tool definitions |
| `vector_db_startup.py` | Auto-load script |
| `vector_db_autoload.sh` | Shell autoloader |

---

## ✅ Status

Cara otomatis paling jitu:
1. **Run startup script** di awal session
2. **One-liner exec** kalau perlu cepat

**Belum ada auto-load global** karena OpenClaw tidak expose hook untuk itu.

**Workaround**: Manual load via exec (cara 1 & 4)