# SKILL: lynk-manager

> [![Tip Me](https://www.tip.md/badge.svg)](https://www.tip.md/oyi77) — If this skill saves you time, tip: **https://www.tip.md/oyi77**

## Description
Manage LYNK.id pages via browser automation or via the opencli "lynk" CLI — edit text blocks, update product links, manage block visibility, and monitor page content. Use when updating LYNK page copy, flash sale text, CTAs, or any block content on lynk.id.

---

## New: opencli Integration (Preferred)

When the `opencli lynk` command family is available, prefer it over direct browser automation. The typical pattern:

```bash
# Update a specific text block from an HTML template
python skills/lynk-manager/scripts/lynk_update_copy.py parenting hero
python skills/lynk-manager/scripts/lynk_update_copy.py parenting social
python skills/lynk-manager/scripts/lynk_update_copy.py parenting urgency
```

This script:
- Maps logical keys (e.g. `parenting hero`) → concrete LYNK product + block IDs
- Points to an HTML template under `skills/lynk-manager/templates/`
- Calls:
  ```bash
  opencli lynk update-text \
    --product-id <PRODUCT_ID> \
    --block-id   <BLOCK_ID>   \
    --file       <TEMPLATE_PATH>
  ```

Use this flow when:
- You want to roll out new copy to multiple LYNK products quickly
- You want reproducible, version-controlled templates instead of editing in the browser

> NOTE: `scripts/lynk_update_copy.py` ships with placeholder block IDs. After the first manual run where you confirm the right TEXT blocks, update `MAPPING` in that script with the real block IDs.

---


## Trigger Phrases
- "update LYNK page"
- "edit text block di LYNK"
- "ubah copy LYNK"
- "update flash sale LYNK"
- "manage lynk.id page"
- "edit konten LYNK"

---

## Prerequisites

### Browser Tab
- **Profile:** `openclaw`
- **LYNK Admin Tab targetId:** `52304E3ADEE500922EC9218675D69770`
- **LYNK Page (jendralbot):** `https://lynk.id/admin/my-lynks/home`

> ⚠️ ALWAYS check existing tabs first before opening new ones. Old tabs persist, new tabs may die.

```javascript
// Step 1: Verify tab is correct
browser tabs → look for lynk.id tab
// Step 2: Verify URL before trusting any action result
// If response URL is NOT lynk.id → action went to wrong tab
```

### Credentials
- **Username/email:** stored in browser session (already logged in)
- **Page slug:** `jendralbot` → `https://lynk.id/jendralbot`

---

## Core Concepts

### LYNK Page Structure
LYNK pages are composed of **blocks** rendered as `<li class="mb-2 wp">` elements.

Block types visible in admin:
- `TEXT` — Free text/HTML content block
- Product blocks — Link blocks with title, price, image
- Divider, Social, etc.

### Block States
- **Active:** `class="mb-2  wp"` (visible on public page)
- **Hidden:** `class="mb-2 block-inactive wp"` (hidden from public)

---

## Critical Pattern: Editing TEXT Blocks

### ⚠️ The Problem
- TEXT blocks do NOT have `href` links in the DOM
- Clicking "..." button opens delete/hide menu (NOT edit)
- Edit is triggered only by clicking the block row itself
- LYNK uses Vue/React router → click triggers `history.pushState`, not a page load

### ✅ The Solution: Router Intercept Pattern

```javascript
// Step 1: Set up router intercept BEFORE clicking
window._navUrls = [];
const origPush = history.pushState.bind(history);
history.pushState = function(s,t,u) { window._navUrls.push(u); return origPush(s,t,u); };

// Step 2: Click the TEXT block row
const allPs = Array.from(document.querySelectorAll('p')).filter(p => p.textContent.trim() === 'TEXT');
const li = allPs[0].closest('li');
const cursor = li.querySelector('[class*=cursor]');
(cursor || li).click();

// Step 3: Read the navigation URL
window._navUrls[0]
// OR check document.location.href if router already navigated
```

### Edit URL Pattern
```
https://lynk.id/admin/text/<full-block-id>
```
- Use `li.id` attribute (NOT `data-block-id`) — `li.id` contains the full routing ID
- Example: `https://lynk.id/admin/text/6984b6cd9cc82e6d20f03b00-9027-7319838250-1770305229764`

### Navigate Directly to Edit
Once you have the edit URL:
```javascript
browser navigate targetId=52304E3ADEE500922EC9218675D69770 url=<edit-url>
```

---

## Workflow: Find All TEXT Blocks

```javascript
// Run this on https://lynk.id/admin/my-lynks/home
() => {
  const allLis = Array.from(document.querySelectorAll('li.mb-2'));
  return allLis.map((li, i) => {
    const p = li.querySelector('p');
    const text = p ? p.textContent.trim().slice(0, 30) : '?';
    const isHidden = li.classList.contains('block-inactive');
    return i + ': [' + (isHidden ? 'HIDDEN' : 'ACTIVE') + '] ' + text + ' | li.id=' + li.id;
  }).join('\n');
}
```

---

## Workflow: Get Edit URL for Specific TEXT Block

```javascript
// Run on https://lynk.id/admin/my-lynks/home
() => {
  window._navUrls = [];
  const origPush = history.pushState.bind(history);
  history.pushState = function(s,t,u) { window._navUrls.push(u); return origPush(s,t,u); };

  const textPs = Array.from(document.querySelectorAll('p')).filter(p => p.textContent.trim() === 'TEXT');
  // Click the Nth TEXT block (0-indexed):
  const N = 0;
  const li = textPs[N]?.closest('li');
  if (li) {
    const cursor = li.querySelector('[class*=cursor]');
    (cursor || li).click();
  }
  return 'clicked, check _navUrls';
}

// Then:
() => window._navUrls.join('\n') || document.location.href
```

---

## Workflow: Edit TEXT Block Content

```javascript
// Run on the edit page: https://lynk.id/admin/text/<block-id>
() => {
  const editor = document.querySelector('.ql-editor, [contenteditable=true]');
  if (!editor) return 'no editor found';

  // Read current content
  return editor.innerHTML;
}

// Update content:
() => {
  const editor = document.querySelector('.ql-editor, [contenteditable=true]');
  editor.focus();
  document.execCommand('selectAll', false, null);
  document.execCommand('delete', false, null);

  editor.innerHTML = '<p><strong>🔥 New Content Here</strong></p><p>More text...</p>';
  editor.dispatchEvent(new Event('input', { bubbles: true }));
  return 'updated';
}

// Save (click Update button):
() => {
  const updateBtn = Array.from(document.querySelectorAll('button'))
    .find(b => b.textContent.trim() === 'Update');
  if (updateBtn) { updateBtn.click(); return 'clicked Update'; }
  return 'Update button not found';
}

// Close success modal:
() => {
  const closeBtn = Array.from(document.querySelectorAll('button'))
    .find(b => b.textContent.trim() === 'Close');
  if (closeBtn) { closeBtn.click(); return 'closed'; }
  return 'no close btn';
}
```

---

## Workflow: Full Edit Flow (Step by Step)

1. **Navigate to admin home**
   ```
   browser navigate targetId=52304E3ADEE500922EC9218675D69770 url=https://lynk.id/admin/my-lynks/home
   ```

2. **Set router intercept & click target TEXT block**
   ```javascript
   // (use evaluate with targetId)
   window._navUrls = [];
   history.pushState = function(s,t,u) { window._navUrls.push(u); return origPush(s,t,u); };
   // click target TEXT block li
   ```

3. **Get edit URL**
   ```javascript
   window._navUrls[0] || document.location.href
   ```

4. **Navigate to edit URL**
   ```
   browser navigate targetId=... url=<edit-url>
   ```

5. **Read & update editor content**

6. **Click Update button → verify success toast**

7. **Close modal → back to home**

---

## Known TEXT Blocks on jendralbot

| Block | li.id (prefix) | Description | State |
|-------|----------------|-------------|-------|
| Header flash sale | `6984b6cd9cc82e6d20f03b00` | Flash sale intro + bullet points | Active |
| Jasa video | `699d637830b03b9fcfe07857` | Video production service text | **Hidden** |
| CTA footer | `69b34858d2c63432a6eb89cf` | Closing CTA flash sale | Active |

> Note: Full li.id includes timestamp suffix. Always intercept via click → navUrls to get exact current ID.

---

## Workflow: Toggle Block Visibility (Show/Hide)

Use the "..." menu on any block:
```javascript
() => {
  const allLis = Array.from(document.querySelectorAll('li.mb-2'));
  const target = allLis[N]; // N = block index
  const menuBtn = target.querySelector('[class*=more], [class*=dots], button:last-child');
  if (menuBtn) { menuBtn.click(); return 'opened menu'; }
  return 'no menu btn found';
}
// Then click Hide/Show option in menu
```

---

## Workflow: Check Public Page

```javascript
// Open public LYNK page to verify changes
browser navigate targetId=... url=https://lynk.id/jendralbot
// Take screenshot to verify live content
```

---

## Common Gotchas

### 1. Wrong Tab
- `act` tool sometimes routes to wrong tab even with explicit targetId
- **Fix:** Always check `response.url` — if not `lynk.id`, wrong tab was used
- **Fix:** Use `evaluate` with explicit targetId instead of `act` when possible

### 2. Edit URL format
- `?id=<id>&fk_page_id=home` → WRONG (opens Add New, not Edit)
- `/admin/text/<full-id>` → CORRECT (opens Edit for existing block)

### 3. `history.pushState` not captured
- If `_navUrls` is empty after click, the router may have already navigated
- Check `document.location.href` instead — it shows the current URL after navigation

### 4. Multiple TEXT blocks
- `querySelectorAll('p')` filtering for `TEXT` text will find all TEXT block labels
- Use index `[0]`, `[1]`, `[2]` to target specific blocks
- Always verify which block you're editing by reading `editor.innerHTML` first

### 5. Block ID uniqueness
- `li.id` and `data-block-id` are DIFFERENT values
- For edit URL routing, use `li.id` (the `id` attribute of the `<li>` element)
- `data-block-id` on inner elements may be an older/different ID

---

## Flash Sale Copy Templates

### Header Block (Full)
```html
<p><strong>🔥 FLASH SALE — Berakhir [WAKTU]!</strong></p>
<p>Semua tools AI dijual <strong>IDR 75.000</strong> saja (aslinya IDR 250K–499K).</p>
<p>⏰ Harga naik kembali normal [TANGGAL] — stok terbatas!</p>
<p>✅ Sudah dipakai 500+ seller Indonesia</p>
<p>✅ Langsung aktif, tidak perlu install</p>
<p>✅ Garansi uang kembali 7 hari</p>
<p>🚨 <strong>Jangan tunggu, harga naik [TANGGAL] jam [JAM]!</strong></p>
<p>👇 <strong>Pilih tools yang kamu butuhkan:</strong></p>
```

### CTA Footer (Short)
```html
<p><strong>🔥 FLASH SALE — Berakhir [WAKTU]!</strong> Semua produk AI harga spesial <strong>IDR 75.000</strong>. Stok terbatas. <strong>Klik sekarang sebelum harga naik!</strong> ⏰</p>
```

---

## Analytics & Monitoring

- **Dashboard:** https://lynk.id/admin/analytics
- **Public page:** https://lynk.id/jendralbot
- **Key metrics:** Clicks per product, total views, conversion rate

---

*Last updated: 2026-03-14 | Learned from live session editing jendralbot page*
