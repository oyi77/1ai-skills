# -*- coding: utf-8 -*-
"""
TikTok Shop Data Extraction Channel

Backends:
1. tiktok-shop-cli (primary) - official SDK
2. Playwright (fallback) - browser automation

Supported regions: Global (US, EU, APAC, LATAM)
"""

import re
import subprocess
import logging
from typing import List, Optional, Tuple
from dataclasses import dataclass

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class ExtractionResult:
    """Standard extraction result across all channels."""
    success: bool
    data: Optional[List[dict]] = None
    error: Optional[str] = None
    backend_used: Optional[str] = None
    item_count: int = 0

    def __bool__(self):
        return self.success


class TikTokShopChannel:
    """
    TikTok Shop product/seller extraction channel.
    
    Detects TikTok Shop URLs and extracts product/seller data.
    Probe order: tiktok-shop-cli → Playwright
    """
    
    name = "tiktok_shop"
    description = "E-commerce extraction for TikTok Shop (global)"
    backends = ["tiktok-shop-cli", "playwright"]
    tier = 2
    
    def __init__(self):
        self.active_backend = None
        self.logger = logging.getLogger(f"{__name__}.{self.name}")
    
    def can_handle(self, url: str) -> bool:
        """Check if URL is a TikTok Shop URL."""
        if not isinstance(url, str):
            return False
        domain = re.search(r"://([^/]+)", url)
        if not domain:
            return False
        d = domain.group(1).lower()
        return "tiktok" in d and ("shop" in url.lower() or "seller" in url.lower())
    
    def check(self, config=None) -> Tuple[str, str]:
        """
        Probe available backends.
        Returns: (status, message)
        """
        # Try tiktok-shop-cli
        try:
            result = subprocess.run(
                ["tiktok-shop", "--version"],
                capture_output=True,
                timeout=5,
                text=True
            )
            if result.returncode == 0:
                self.active_backend = "tiktok-shop-cli"
                return ("ok", f"TikTok Shop: CLI ready ({result.stdout.strip()})")
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        # Try Playwright
        if PLAYWRIGHT_AVAILABLE:
            self.active_backend = "playwright"
            return ("ok", "TikTok Shop: Playwright ready")
        
        return ("fail", "TikTok Shop: no backend available. Install: pipx install tiktok-shop-cli")
    
    def extract(self, url: str) -> ExtractionResult:
        """
        Extract data from TikTok Shop URL.
        
        Args:
            url: TikTok Shop product or seller URL
            
        Returns:
            ExtractionResult with success flag and data
        """
        if not self.can_handle(url):
            return ExtractionResult(
                success=False,
                error=f"Not a TikTok Shop URL: {url}",
                backend_used=None
            )
        
        if not self.active_backend:
            self.check()
        
        if self.active_backend == "tiktok-shop-cli":
            return self._extract_with_cli(url)
        elif self.active_backend == "playwright":
            return self._extract_with_playwright(url)
        
        return ExtractionResult(
            success=False,
            error=f"TikTok Shop: {self.active_backend or 'no backend available'}",
            backend_used=None
        )
    
    def _extract_with_cli(self, url: str) -> ExtractionResult:
        """Extract using tiktok-shop-cli."""
        try:
            result = subprocess.run(
                ["tiktok-shop", "extract", url, "--json"],
                capture_output=True,
                timeout=15,
                text=True
            )
            
            if result.returncode != 0:
                return ExtractionResult(
                    success=False,
                    error=f"CLI extraction failed: {result.stderr}",
                    backend_used="tiktok-shop-cli"
                )
            
            import json
            data = json.loads(result.stdout)
            
            if isinstance(data, dict):
                data = [data]
            
            return ExtractionResult(
                success=True,
                data=data,
                backend_used="tiktok-shop-cli",
                item_count=len(data) if data else 0
            )
        
        except subprocess.TimeoutExpired:
            return ExtractionResult(
                success=False,
                error="CLI extraction timed out (>15s)",
                backend_used="tiktok-shop-cli"
            )
        except Exception as e:
            return ExtractionResult(
                success=False,
                error=f"CLI extraction failed: {e}",
                backend_used="tiktok-shop-cli"
            )
    
    def _extract_with_playwright(self, url: str) -> ExtractionResult:
        """Extract using Playwright (async wrapper)."""
        if not PLAYWRIGHT_AVAILABLE:
            return ExtractionResult(
                success=False,
                error="Playwright not available (pip install playwright)",
                backend_used=None
            )
        
        try:
            # Note: Playwright is async; this is a sync wrapper for simplicity
            import asyncio
            return asyncio.run(self._extract_async(url))
        except Exception as e:
            return ExtractionResult(
                success=False,
                error=f"Playwright extraction failed: {e}",
                backend_used="playwright"
            )
    
    async def _extract_async(self, url: str) -> ExtractionResult:
        """Async extraction with Playwright."""
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            
            try:
                await page.goto(url, timeout=15000)
                
                # Wait for product data
                await page.wait_for_selector(".product-card", timeout=10000)
                
                # Extract products
                products = await page.evaluate("""
                    () => {
                        const cards = document.querySelectorAll('.product-card');
                        return Array.from(cards).map(card => ({
                            title: card.querySelector('.title')?.innerText,
                            price: card.querySelector('.price')?.innerText,
                            seller: card.querySelector('.seller')?.innerText,
                            url: card.href
                        }));
                    }
                """)
                
                return ExtractionResult(
                    success=bool(products),
                    data=products,
                    backend_used="playwright",
                    item_count=len(products)
                )
            
            finally:
                await browser.close()
    
    def __repr__(self) -> str:
        return f"<TikTokShopChannel active_backend={self.active_backend}>"
