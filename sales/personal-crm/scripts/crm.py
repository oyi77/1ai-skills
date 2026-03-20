#!/usr/bin/env python3
"""Personal CRM - SQLite-based contact management."""
import sqlite3, sys, json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DB_PATH = DATA_DIR / "contacts.db"


def _get_db():
    """Get database connection, create schema if needed."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            channel TEXT DEFAULT 'unknown',
            username TEXT,
            last_contact TEXT,
            notes TEXT DEFAULT '',
            tags TEXT DEFAULT '',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    return conn


def add_contact(name, channel="unknown", username="", notes="", tags=""):
    """Add a new contact."""
    conn = _get_db()
    conn.execute(
        "INSERT INTO contacts (name, channel, username, last_contact, notes, tags) VALUES (?, ?, ?, ?, ?, ?)",
        (name, channel, username, datetime.now().isoformat(), notes, tags),
    )
    conn.commit()
    contact_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return f"Contact added: {name} (ID: {contact_id})"


def find_contact(query):
    """Search contacts by name, username, notes, or tags."""
    conn = _get_db()
    rows = conn.execute(
        "SELECT * FROM contacts WHERE name LIKE ? OR username LIKE ? OR notes LIKE ? OR tags LIKE ?",
        (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"),
    ).fetchall()
    conn.close()
    if not rows:
        return "No contacts found."
    return _format_contacts(rows)


def list_contacts(tag=None):
    """List all contacts, optionally filtered by tag."""
    conn = _get_db()
    if tag:
        rows = conn.execute("SELECT * FROM contacts WHERE tags LIKE ?", (f"%{tag}%",)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM contacts ORDER BY last_contact DESC").fetchall()
    conn.close()
    if not rows:
        return "No contacts found."
    return _format_contacts(rows)


def get_contact(contact_id):
    """Get a single contact by ID."""
    conn = _get_db()
    row = conn.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,)).fetchone()
    conn.close()
    if not row:
        return f"Contact ID {contact_id} not found."
    return _format_contact(row)


def update_notes(contact_id, notes):
    """Update notes for a contact."""
    conn = _get_db()
    conn.execute(
        "UPDATE contacts SET notes = ?, last_contact = ? WHERE id = ?",
        (notes, datetime.now().isoformat(), contact_id),
    )
    conn.commit()
    affected = conn.execute("SELECT changes()").fetchone()[0]
    conn.close()
    if affected == 0:
        return f"Contact ID {contact_id} not found."
    return f"Notes updated for contact ID {contact_id}."


def _format_contact(row):
    return (
        f"ID: {row['id']} | {row['name']}\n"
        f"  Channel: {row['channel']} | Username: {row['username']}\n"
        f"  Tags: {row['tags']}\n"
        f"  Last contact: {row['last_contact']}\n"
        f"  Notes: {row['notes']}"
    )


def _format_contacts(rows):
    return "\n".join(_format_contact(row) for row in rows)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Personal CRM")
    parser.add_argument("--action", choices=["add", "find", "list", "get", "update_notes"], required=True)
    parser.add_argument("--name", help="Contact name")
    parser.add_argument("--channel", default="unknown", help="Channel (telegram/wa/email)")
    parser.add_argument("--username", default="", help="Username on channel")
    parser.add_argument("--notes", default="", help="Notes about contact")
    parser.add_argument("--tags", default="", help="Comma-separated tags")
    parser.add_argument("--query", help="Search query")
    parser.add_argument("--id", type=int, help="Contact ID")
    parser.add_argument("--tag", help="Filter by tag")
    args = parser.parse_args()

    if args.action == "add":
        print(add_contact(args.name, args.channel, args.username, args.notes, args.tags))
    elif args.action == "find":
        print(find_contact(args.query))
    elif args.action == "list":
        print(list_contacts(args.tag))
    elif args.action == "get":
        print(get_contact(args.id))
    elif args.action == "update_notes":
        print(update_notes(args.id, args.notes))
