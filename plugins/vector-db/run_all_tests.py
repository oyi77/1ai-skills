#!/usr/bin/env python3
"""
Vector DB Plugin - Comprehensive Test Suite
Run this to test all engines after fixes
"""

import sys
import os

# Add plugin directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    print("=" * 60)
    print("1️⃣  Testing Imports...")
    print("=" * 60)
    
    errors = []
    
    try:
        from shared.engine import VectorEngine, smart_chunk
        print("   ✅ shared.engine imported")
    except Exception as e:
        errors.append(f"shared.engine: {e}")
        print(f"   ❌ shared.engine: {e}")
    
    try:
        from zvec.engine import ZVecEngine
        print("   ✅ zvec.engine imported")
    except Exception as e:
        errors.append(f"zvec.engine: {e}")
        print(f"   ❌ zvec.engine: {e}")
    
    try:
        from pageindex.engine import PageIndexEngine
        print("   ✅ pageindex.engine imported")
    except Exception as e:
        errors.append(f"pageindex.engine: {e}")
        print(f"   ❌ pageindex.engine: {e}")
    
    try:
        from ruvector.engine import RuvectorEngine
        print("   ✅ ruvector.engine imported")
    except Exception as e:
        errors.append(f"ruvector.engine: {e}")
        print(f"   ❌ ruvector.engine: {e}")
    
    return len(errors) == 0, errors

def test_chromadb():
    """Test ChromaDB initialization"""
    print()
    print("=" * 60)
    print("2️⃣  Testing ChromaDB...")
    print("=" * 60)
    
    try:
        import chromadb
        print(f"   ✅ ChromaDB version: {chromadb.__version__}")
        
        # Test PersistentClient
        try:
            client = chromadb.PersistentClient(
                path="/tmp/test_chroma",
                settings=chromadb.config.Settings(anonymized_telemetry=False)
            )
            print("   ✅ PersistentClient works (v0.4+)")
        except AttributeError:
            print("   ⚠️  PersistentClient not available (older version)")
        
        return True, []
    except Exception as e:
        print(f"   ❌ ChromaDB error: {e}")
        return False, [str(e)]

def test_sentence_transformers():
    """Test SentenceTransformers"""
    print()
    print("=" * 60)
    print("3️⃣  Testing SentenceTransformers...")
    print("=" * 60)
    
    try:
        from sentence_transformers import SentenceTransformer
        print("   ✅ SentenceTransformers available")
        return True, []
    except Exception as e:
        print(f"   ❌ SentenceTransformers error: {e}")
        return False, [str(e)]

def test_smart_chunking():
    """Test smart chunking functionality"""
    print()
    print("=" * 60)
    print("4️⃣  Testing Smart Chunking...")
    print("=" * 60)
    
    try:
        from shared.engine import smart_chunk
        
        test_text = """
        # Section 1
        This is some test content.
        
        ## Subsection
        More content here.
        
        # Section 2
        Final section content.
        """
        
        chunks = smart_chunk(test_text, max_tokens=300)
        print(f"   ✅ Chunked into {len(chunks)} parts")
        
        for i, chunk in enumerate(chunks[:3]):  # Show first 3
            print(f"      Part {i+1}: {len(chunk)} chars")
        
        return True, []
    except Exception as e:
        print(f"   ❌ Smart chunking error: {e}")
        return False, [str(e)]

def test_engines():
    """Test each engine initialization"""
    print()
    print("=" * 60)
    print("5️⃣  Testing Engine Initialization...")
    print("=" * 60)
    
    from shared.engine import VectorEngine
    
    try:
        engine = VectorEngine()
        available = list(engine.engines.keys())
        print(f"   ✅ Unified engine loaded")
        print(f"   📍 Available engines: {', '.join(available)}")
        return True, []
    except Exception as e:
        print(f"   ❌ Engine initialization error: {e}")
        return False, [str(e)]

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("🧪 Vector DB Plugin - Test Suite")
    print("=" * 60 + "\n")
    
    results = []
    all_errors = []
    
    # Test 1: Imports
    success, errors = test_imports()
    results.append(("Imports", success))
    all_errors.extend(errors)
    
    # Test 2: ChromaDB
    success, errors = test_chromadb()
    results.append(("ChromaDB", success))
    all_errors.extend(errors)
    
    # Test 3: SentenceTransformers
    success, errors = test_sentence_transformers()
    results.append(("SentenceTransformers", success))
    all_errors.extend(errors)
    
    # Test 4: Smart Chunking
    success, errors = test_smart_chunking()
    results.append(("Smart Chunking", success))
    all_errors.extend(errors)
    
    # Test 5: Engines
    success, errors = test_engines()
    results.append(("Engines", success))
    all_errors.extend(errors)
    
    # Final Report
    print()
    print("=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(1 for _, success in results if success)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status}: {test_name}")
    
    print()
    print(f"Result: {passed_tests}/{total_tests} tests passed")
    
    if all_errors:
        print()
        print("❌ ERRORS:")
        for error in all_errors:
            print(f"   • {error}")
    
    print("=" * 60)
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Plugin is ready.")
        return 0
    else:
        print("⚠️  Some tests failed. Check errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())