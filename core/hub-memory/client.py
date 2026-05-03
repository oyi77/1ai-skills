#!/usr/bin/env python3
"""
Centralized Memory Client - Bidirectional Integration

IQ 145 Pattern:
  1. BEFORE any task → query hub for context
  2. INJECT retrieved memories into your thinking
  3. EXECUTE with context
  4. OPTIONALLY write result back to hub

Usage:
    from centralized_memory_client import query_hub, inject_context, add_to_hub
    
    # Step 1: Query BEFORE executing
    memories = query_hub("what do we know about project X?", service="openclaw")
    
    # Step 2: Inject as context
    if memories:
        context = inject_context(memories)
        prompt = f"{context}\n\nNow: {user_request}"
    else:
        prompt = user_request
    
    # Step 3: Execute WITH context
    response = model.generate(prompt)
    
    # Step 4: Optionally commit result
    # add_to_hub(f"Result: {response}", service="openclaw")
"""

import os
import httpx
from typing import Optional, List, Dict, Any

# Configuration
HUB_URL = os.getenv("BERKAHKARYA_HUB_URL", "http://localhost:9099")
DEFAULT_SERVICE = os.getenv("BERKAHKARYA_SERVICE", "openclaw")


def query_hub(
    query: str,
    service: Optional[str] = None,
    limit: int = 5,
    method: str = "hybrid"
) -> List[Dict[str, Any]]:
    """
    Query berkahkarya-hub BEFORE executing ANY task.
    
    This is the "IQ 145" pattern - DON'T GUESS, LOOK IT UP FIRST.
    
    Args:
        query: What to search for
        service: Filter by service (openclaw, omniroute, paperclip, opencode)
        limit: Max results
        method: Search method (hybrid, fts, vector, gbrain)
    
    Returns:
        List of memory dicts with: id, content, source, score, service, metadata
    
    Example:
        memories = query_hub("customer feedback about product", service="openclaw")
        for mem in memories:
            print(f"- {mem['content'][:200]}")
    """
    params = {
        "q": query,
        "limit": limit,
        "method": method
    }
    if service:
        params["service"] = service
    
    try:
        response = httpx.get(f"{HUB_URL}/brain/search", params=params, timeout=10.0)
        if response.status_code == 200:
            data = response.json()
            return data.get("results", [])
        else:
            print(f"⚠️ Hub query failed: {response.status_code}")
            return []
    except Exception as e:
        print(f"⚠️ Hub unreachable: {e}")
        return []


def inject_context(memories: List[Dict[str, Any]], max_items: int = 5) -> str:
    """
    Format retrieved memories as injectable context for AI.
    
    Args:
        memories: Output from query_hub()
        max_items: Maximum memories to include
    
    Returns:
        Formatted string ready to inject into prompt
    
    Example:
        context = inject_context(memories)
        prompt = f"{context}\n\nUser: {message}"
    """
    if not memories:
        return ""
    
    formatted_lines = ["📚 RELEVANT HISTORY:"]
    
    for i, mem in enumerate(memories[:max_items], 1):
        # Get content, truncate if too long
        content = mem.get("content", "")
        if len(content) > 400:
            content = content[:400] + "..."
        
        # Get source service
        service = mem.get("service", mem.get("source", "unknown"))
        
        # Add to formatted output
        formatted_lines.append(f"\n{i}. [{service}] {content}")
    
    return "\n".join(formatted_lines)


def add_to_hub(
    content: str,
    service: str = DEFAULT_SERVICE,
    wing: str = "general",
    room: str = "general",
    tags: Optional[List[str]] = None
) -> Optional[Dict[str, Any]]:
    """
    Write result BACK to hub after task completes.
    
    This enables the bidirectional flow - services can LEARN.
    
    Args:
        content: What to store
        service: Source service name
        wing: Organization category (general, backend, frontend, etc.)
        room: Specific area
        tags: Optional tags
    
    Returns:
        Response dict or None on failure
    
    Example:
        # After completing a task:
        result = add_to_hub(
            content="Fixed bug in payment flow - issue was missing validation",
            service="openclaw",
            wing="backend",
            tags=["bugfix", "payment"]
        )
    """
    data = {
        "content": content,
        "service": service,
        "wing": wing,
        "room": room
    }
    if tags:
        data["tags"] = tags
    
    try:
        response = httpx.post(f"{HUB_URL}/brain/add", json=data, timeout=10.0)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"⚠️ Hub add failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️ Hub add error: {e}")
        return None


def get_hub_stats() -> Dict[str, Any]:
    """
    Get centralized hub statistics.
    
    Returns:
        Dict with gbrain, mempalace, fts5 stats
    """
    try:
        response = httpx.get(f"{HUB_URL}/brain/stats", timeout=5.0)
        if response.status_code == 200:
            return response.json()
        return {}
    except:
        return {}


# Convenience function for quick CLI usage
def main():
    """CLI for quick testing"""
    import sys
    
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "test"
    
    print(f"🔍 Querying hub: {query}")
    results = query_hub(query, limit=3)
    
    if results:
        print(f"\n📚 Found {len(results)} memories:\n")
        for mem in results:
            content = mem.get("content", "")[:150]
            service = mem.get("service", "unknown")
            print(f"  [{service}] {content}...")
    else:
        print("⚠️ No results found")


if __name__ == "__main__":
    main()