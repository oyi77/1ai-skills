#!/usr/bin/env python3
"""
Vector DB Plugin - Directory Validator
"""

import os
import sys

PLUGIN_DIR = "/home/openclaw/.openclaw/workspace/plugins/vector-db"

REQUIRED_FILES = [
    "manifest.json",
    "__init__.py",
    "README.md",
    "install.sh",
    "test.py",
    "examples_id.py",
    "shared/engine.py",
    "zvec/engine.py",
    "zvec/handler.py",
    "pageindex/engine.py",
    "pageindex/handler.py",
    "ruvector/engine.py",
    "ruvector/handler.py",
]

print("=" * 60)
print("🔍 Vector DB Plugin - Directory Validator")
print("=" * 60)
print()

print(f"📁 Plugin Directory: {PLUGIN_DIR}")
print()

# Check if directory exists
if not os.path.exists(PLUGIN_DIR):
    print("❌ Plugin directory not found!")
    sys.exit(1)

# Check required files
missing = []
present = []

for file in REQUIRED_FILES:
    filepath = os.path.join(PLUGIN_DIR, file)
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        present.append((file, size))
    else:
        missing.append(file)

print("✅ Present Files:")
for file, size in present:
    print(f"   ✓ {file} ({size:,} bytes)")

if missing:
    print()
    print("❌ Missing Files:")
    for file in missing:
        print(f"   ✗ {file}")

print()
print("=" * 60)
if not missing:
    print("🎉 All required files present!")
    print("   Plugin is ready for use.")
else:
    print(f"⚠️  {len(missing)} file(s) missing")
print("=" * 60)