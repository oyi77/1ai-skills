"""
memory-system — Resilient 4-layer hierarchical memory for autonomous agents.

Quick start:
    from skills.memory_system.scripts import MemoryManager
    mm = MemoryManager()
    mm.store("User prefers XAUUSD scalping", importance=0.9, tags=["trading"])
    results = mm.search("trading preferences", top_k=5)
"""

from .memory_manager import MemoryManager

__all__ = ["MemoryManager"]
__version__ = "1.0.0"
