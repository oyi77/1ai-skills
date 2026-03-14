#!/usr/bin/env python3
"""
MANDATORY Pre-Task Check - "Assume You Forgot" Protocol

Run BEFORE starting ANY work to avoid rebuilding existing systems.
"""
import sys
sys.path.insert(0, '/home/openclaw/.openclaw/workspace')

from pathlib import Path
from tools.vector_db_tools import vector_search

def search_memory(query, top_k=3):
    """Search vector memory system"""
    try:
        results = vector_search(query, top_k=top_k)
        return results
    except Exception as e:
        print(f"⚠️  Memory search error: {e}")
        return []

def check_index(query):
    """Quick search through INDEX.md"""
    index_path = Path("memory/INDEX.md")
    if not index_path.exists():
        return None

    with open(index_path) as f:
        content = f.read()

    if query.lower() in content.lower():
        sections = content.split('##')
        for section in sections:
            if query.lower() in section.lower():
                return section.strip()
    return None

def check_skills():
    """List all available skills"""
    skills_dir = Path("skills")
    if not skills_dir.exists():
        return []

    skills = []
    for skill_dir in skills_dir.iterdir():
        if skill_dir.is_dir():
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                skills.append(skill_dir.name)
    return skills

def main():
    if len(sys.argv) < 2:
        print("⚠️  Usage: python3 pre_task_check.py <query>")
        print("   Example: python3 pre_task_check.py memory system")
        sys.exit(1)

    query = sys.argv[1]

    print("=" * 70)
    print("🔍 PRE-TASK CHECK - 'Assume You Forgot' Protocol")
    print("=" * 70)
    print(f"\n📝 Query: {query}\n")

    # Check 1: INDEX.md
    print("1️⃣  Checking memory/INDEX.md...")
    index_result = check_index(query)
    if index_result:
        print("✅ Found in INDEX.md:")
        print("─" * 70)
        print(index_result[:400] + ("..." if len(index_result) > 400 else ""))
        print("─" * 70)
    else:
        print("   ❌ Not found in INDEX.md")

    # Check 2: Vector DB
    print(f"\n2️⃣  Searching vector DB...")
    vector_results = search_memory(query, top_k=3)
    if vector_results:
        print(f"✅ Found {len(vector_results)} related items:")
        for i, r in enumerate(vector_results, 1):
            print(f"\n   {i}. Score: {r['score']:.2f}")
            print(f"      Source: {r['source']}")
            print(f"      Content: {r['content'][:200]}...")
            if r.get('title'):
                print(f"      Title: {r['title']}")
    else:
        print("   ❌ No relevant items in vector DB")

    # Check 3: Skills
    print(f"\n3️⃣  Available skills: {len(check_skills())}")
    skills = check_skills()
    relevant_skills = [s for s in skills if query.lower() in s.lower()]
    if relevant_skills:
        print(f"✅ Related skills:")
        for skill in relevant_skills:
            print(f"   - {skill}")
    else:
        print("   ℹ️  No directly matching skills")

    print("\n" + "=" * 70)
    print("🎯 CONCLUSION:")
    print("=" * 70)
    if index_result or vector_results or relevant_skills:
        print("✅ EXISTING SYSTEMS FOUND - REUSE, DON'T REBUILD")
        print("\n✏️  Action Plan:")
        print("   1. Read the relevant documentation above")
        print("   2. Assess if existing solution meets needs")
        print("   3. Only build NEW if existing is insufficient")
    else:
        print("🚧 NO EXISTING SYSTEMS - YOU CAN BUILD NEW")
        print("\n✅ Safe to proceed with new implementation")

    print("=" * 70)

if __name__ == "__main__":
    main()