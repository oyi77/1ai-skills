---
name: personal-crm
description: >
  Personal CRM — track contacts from Telegram, email, and other channels.
  SQLite-backed with auto-extraction from conversation context.
  Functions: add, find, list, update contacts with tags and notes.
version: "1.0.0"
author: BerkahKarya AI
tags: [crm, contacts, sales, telegram, sqlite, relationship-management]
---

# Personal CRM

## Overview

Lightweight personal CRM backed by SQLite. Track contacts from any channel (Telegram, email, WhatsApp), tag them, add notes, and find them later. Designed to auto-extract contact info from conversation context.

## Database

Stored at: `skills/sales/personal-crm/data/contacts.db`

### Schema

```sql
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    channel TEXT DEFAULT '',
    last_contact TEXT,
    notes TEXT DEFAULT '',
    tags TEXT DEFAULT '',
    created_at TEXT,
    updated_at TEXT
);
```

## Usage

```bash
# Add a contact
python3 scripts/crm.py add "John Doe" --channel telegram --notes "Met at AI meetup" --tags "lead,ai"

# Find contacts
python3 scripts/crm.py find "John"

# List by tag
python3 scripts/crm.py list --tag lead

# List all contacts
python3 scripts/crm.py list

# Update notes
python3 scripts/crm.py update 1 --notes "Followed up, interested in enterprise plan"

# Auto-extract from conversation text
python3 scripts/crm.py extract "Just spoke with Sarah from TechCorp on WhatsApp about API pricing"
```

## Auto-Extract

The `extract` function uses OmniRoute LLM to parse conversation text and extract:
- Contact name
- Channel (telegram, whatsapp, email, etc.)
- Key notes/context
- Suggested tags

## Functions

| Function | Description |
|----------|-------------|
| `add_contact(name, channel, notes, tags)` | Add a new contact |
| `find_contact(query)` | Search by name (fuzzy) |
| `list_contacts(tag)` | List all or filter by tag |
| `update_notes(id, notes)` | Append notes to a contact |
| `extract_contact(text)` | Auto-extract from conversation text |
