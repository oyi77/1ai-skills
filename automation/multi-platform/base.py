# -*- coding: utf-8 -*-
"""
1ai-Ecosystem Multi-Platform Channel Abstraction

Ported from: https://github.com/Panniantong/Agent-Reach
Base class for unified data extraction across 19+ platforms.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import os
import json


@dataclass
class ExtractionResult:
    """Normalized extraction result across all platforms."""
    
    platform: str                      # e.g., "shopee", "tiktok", "youtube"
    url: str                           # original URL
    title: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None       # username, channel name, seller
    author_id: Optional[str] = None    # internal platform ID
    created_at: Optional[str] = None   # ISO 8601
    updated_at: Optional[str] = None   # ISO 8601
    
    engagement: Dict[str, Any] = None  # likes, comments, shares, views
    data: Dict[str, Any] = None        # platform-specific fields
    
    source_backend: Optional[str] = None  # which backend extracted this
    extraction_time_ms: float = 0.0
    error: Optional[str] = None
    
    def __post_init__(self):
        if self.engagement is None:
            self.engagement = {}
        if self.data is None:
            self.data = {}
    
    def to_dict(self) -> dict:
        """Convert to JSON-serializable dict."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Serialize to JSON."""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


class Channel(ABC):
    """
    Base class for multi-platform data extraction.
    
    Each channel represents a platform (YouTube, Twitter, GitHub, etc.)
    and provides:
      - can_handle(url) -> does this URL belong to this platform?
      - check(config) -> is the upstream tool installed and configured?
      - extract(url) -> extract structured data from URL
    
    Backend routing semantics:
      - `backends` is an ORDERED list: [preferred, fallback1, fallback2, ...]
      - check() sets self.active_backend to the working backend (or None)
      - Users can override backend via config key `<channel>_backend`
      - ordered_backends() respects user override by reordering list
    """
    
    # MUST override in subclass
    name: str = None                   # e.g., "shopee"
    description: str = None            # e.g., "Shopee products (Indonesia/SEA)"
    backends: List[str] = []           # e.g., ["shopee-cli", "web scraping"]
    tier: int = 0                      # 0=zero-config, 1=free key, 2=auth required
    
    # Set by check()
    active_backend: Optional[str] = None
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.active_backend = None
    
    @abstractmethod
    def can_handle(self, url: str) -> bool:
        """
        Return True if this channel can handle the given URL.
        
        Example:
          def can_handle(self, url: str) -> bool:
              return "shopee.co.id" in url or "shopee.com.my" in url
        """
        pass
    
    def ordered_backends(self) -> List[str]:
        """
        Get backends in order: user override (if set) takes precedence.
        
        Config key: <channel>_backend (env var: <CHANNEL>_BACKEND)
        """
        override = self.config.get(
            f"{self.name}_backend"
        ) or os.getenv(f"{self.name.upper()}_BACKEND")
        
        candidates = list(self.backends)
        
        if override:
            # Move override to front
            for i, b in enumerate(candidates):
                if b == override or b.startswith(override):
                    candidates.insert(0, candidates.pop(i))
                    break
        
        return candidates
    
    def check(self, config: Optional[Dict[str, Any]] = None) -> Tuple[str, str]:
        """
        Check if this channel's upstream tool is available.
        
        Returns:
          (status, message) where status is 'ok', 'warn', 'off', or 'error'
        
        Subclasses MUST override and probe backends to set self.active_backend.
        """
        if config:
            self.config = config
        
        # Default: first backend is active (override in subclass for real probing)
        self.active_backend = self.backends[0] if self.backends else "builtin"
        
        backend_names = ", ".join(self.backends) if self.backends else "builtin"
        return "ok", f"Backends: {backend_names}"
    
    @abstractmethod
    def extract(self, url: str) -> Optional[ExtractionResult]:
        """
        Extract structured data from URL using active_backend.
        
        Returns:
          ExtractionResult on success
          None or ExtractionResult with error field on failure
        """
        pass
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} active_backend={self.active_backend}>"
