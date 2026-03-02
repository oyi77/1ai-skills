#!/usr/bin/env python3
"""
Vector DB Plugin - Status Check
Quick check to see if everything is installed
"""

import sys
import os

print("=" * 60)
print("🔍 Vector DB Plugin - Status Check")
print("=" * 60)
print()

# Check ChromaDB
try:
    import chromadb
    print(f"✅ ChromaDB: {chromadb.__version__}")
    chromadb_ok = True
except ImportError:
    print("❌ ChromaDB: Not installed")
    print("   Run: pip install chromadb")
    chromadb_ok = False

# Check SentenceTransformers
try:
    import sentence_transformers
    print("✅ SentenceTransformers: Installed")
    st_ok = True
except ImportError:
    print("❌ SentenceTransformers: Not installed")
    print("   Run: pip install sentence-transformers")
    st_ok = False

# Check PyPDF2 (optional)
try:
    import PyPDF2
    print("✅ PyPDF2: Installed")
except ImportError:
    print("⚠️  PyPDF2: Optional (for PDF support)")

print()

if chromadb_ok and st_ok:
    print("🎉 All required dependencies installed!")
    print()
    print("Next steps:")
    print("   python3 WORKING_TEST.py")
    print("   bash DEPLOY.sh")
    sys.exit(0)
else:
    print("❌ Some dependencies missing.")
    print()
    print("Install with:")
    print("   pip install chromadb sentence-transformers")
    sys.exit(1)