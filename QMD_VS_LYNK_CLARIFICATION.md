# ❓ QMD vs LYNK Skill - Clarification

## Pertanyaan:

> "bukannya kita pakai QMD ya?"

---

## Jawaban:

**TIDAK.** LYNK skill yang kita buat hari ini TIDAK memakai QMD.

---

## Apa itu QMD?

**QMD = Quick Micro-Document**
- Tool untuk memory optimization
- QMicro-based semantic search system
- Terdapat di: https://github.com/qmd/qmd

**Status di sistem ini:**
- ❌ **BLOCKED** - Tidak bisa dipasang
- Problem: Missing dependencies (bun, unzip) + environment restrictions
- Error: `Permission denied` di container/sandbox
- Lihat: `memory/2026-03-02.md` (Memory Optimization section)

---

## Apa yang Dipakai LYNK Skill?

**LYNK skill menggunakan:**

### 1. **Plain JSON Storage:**
```python
# File: skills/lynk/config.json
{
  "lynk_url": "https://lynk.id/jendralbot",
  "products": {
    "Belanja Duit Balik": {
      "link": "https://lynk.id/jendralbot/kkjk0mv1vg7o",
      "price": 0
    },
    ...
  }
}
```

### 2. **Local File Storage:**
```
skills/lynk/data/lynk_YYYY-MM-DD.json       # Daily data
skills/lynk/data/lynk_latest.json             # Latest
skills/lynk/reports/report_YYYY-MM-DD.txt   # Reports
```

### 3. **Python (bukan QMD):**
```python
skills/lynk/lynk.py  # Python script (executable)
```

---

## Apa yang Dipakai untuk Semantic Search?

**Vector DB (bukan QMD):**

**Location:** `~/.openclaw/vector-cache/`

**Engines:**
- **ZVec** - Untuk English text
- **Ruvector** - Untuk Indonesian text
- **PageIndex** - Page indexing

**Auto-load via SOUL.md:**
```python
exec(open('workspace/vector_db_startup.py').read())
```

**Functions yang tersedia:**
- `vector_search(query, top_k=5)` - Semantic search
- `vector_index(content, title, source)` - Index documents
- `vector_chunk(text, max_tokens=500)` - Smart chunking
- `vector_detect_language(text)` - ID/EN detection

---

## Perbedaan:

| Feature | QMD | Vector DB (Yang Dipakai) |
|---------|-----|---------------------------|
| **Type** | QMicro-based | Multi-engine (ZVec, PageIndex, Ruvector) |
| **Installation** | ❌ BLOCKED | ✅ WORKING |
| **Semantic Search** | Yes | Yes |
| **Storage** | QMicro database | File cache |
| **Use Case** | General memory retrieval | Document semantic search |
| **LYNK Skill** | ❌ Tidak pakai | ✅ Pakai (file-based JSON) |

---

## Kenapa Tidak Pakai QMD?

**Reasons:**

1. **Environment Restrictions**
   - Container/sandbox tidak izin install `bun`, `unzip`
   - `sudo apt-get` gagal: Permission denied

2. **Blocker Dependencies**
   - `bun` missing
   - `unzip` missing

3. **Kerja Pakai Vector DB**
   - Vector DB sudah WORKING ✅
   - Tidak butuh QMD
   - LYNK skill pakai file-based storage lebih simple

---

## Konfirmasi:

**QMD:**
- Status: ❌ BLOCKED
- Tidak bisa dipasang di environment ini
- Tidak digunakan oleh LYNK skill

**LYNK Skill:**
- Status: ✅ WORKING
- Storage: JSON files + text reports
- Tidak pakai QMD

**Semantic Search:**
- Status: ✅ WORKING
- Tool: Vector DB (ZVec, PageIndex, Ruvector)
- Auto-load di setiap sesi

---

**Jawaban: TIDAK, kita tidak pakai QMD. Lynk skill menggunakan file-based JSON, semantic search pakai Vector DB.**