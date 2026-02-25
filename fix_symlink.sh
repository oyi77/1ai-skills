#!/bin/bash
# VILONA FINAL - SYMLINK FIX

echo "=== VILONA SYMLINK FIX ==="
echo ""

# Cek apakah symlink sudah ada
if [ -L "/home/openclaw/C:/Users/EX PC/.openclaw/workspace" ]; then
    echo "Symlink sudah ada, menghapus..."
    rm -f "/home/openclaw/C:/Users/EX PC/.openclaw/workspace"
fi

# Buat parent folder jika belum ada
mkdir -p "/home/openclaw/C:/Users/EX PC/.openclaw"

# Buat symlink dari forward slash ke folder dengan backslash
ln -s "/home/openclaw/C:\Users\EX PC\.openclaw\workspace" "/home/openclaw/C:/Users/EX PC/.openclaw/workspace"

echo "✅ Symlink dibuat:"
echo "   /home/openclaw/C:/Users/EX PC/.openclaw/workspace -> /home/openclaw/C:\\Users\\EX PC\\.openclaw\\workspace"
echo ""

# Test symlink
echo "=== Testing symlink ==="
ls -la "/home/openclaw/C:/Users/EX PC/.openclaw/workspace/skills/1ai-skills/trading/" | head -20
echo ""

echo "✅ SELESAI!"
