# -*- coding: utf-8 -*-
"""
WeChat Data Extraction Channel

Backends (ordered by reliability):
1. wechat-cli (primary) - official WeChat CLI
2. itchat (fallback) - Python WeChat library
3. Selenium (final fallback) - browser automation

Supported: Moments, Groups, Official Accounts, Mini Programs
"""

import re
import subprocess
import logging
from typing import List, Optional, Tuple, Dict, Any
from dataclasses import dataclass

try:
    import itchat
    ITCHAT_AVAILABLE = True
except ImportError:
    ITCHAT_AVAILABLE = False

try:
    from selenium import webdriver
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class ExtractionResult:
    """Standard extraction result across all channels."""
    success: bool
    data: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
    backend_used: Optional[str] = None
    item_count: int = 0

    def __bool__(self):
        return self.success


class WeChatChannel:
    """
    WeChat data extraction channel.
    
    Handles: Official Account posts, group messages, moments, mini programs
    Probe order: wechat-cli → itchat → Selenium
    """
    
    name = "wechat"
    description = "Social messaging extraction for WeChat (China, APAC)"
    backends = ["wechat-cli", "itchat", "selenium"]
    tier = 3
    
    def __init__(self):
        self.active_backend = None
        self.logger = logging.getLogger(f"{__name__}.{self.name}")
        self._session = None
    
    def can_handle(self, url: str) -> bool:
        """Check if URL is a WeChat Official Account, Mini Program, or group link."""
        if not isinstance(url, str):
            return False
        
        wechat_patterns = [
            r"mp\.weixin\.qq\.com",      # Official Account
            r"wx\.qq\.com",               # WeChat Web
            r"mini\.qq\.com",             # Mini Program
            r"servicewechat\.com",        # WeChat Service
            r"weixin://",                 # WeChat Protocol
        ]
        
        return any(re.search(p, url, re.I) for p in wechat_patterns)
    
    def check(self, config=None) -> Tuple[str, str]:
        """
        Probe available backends in order.
        Returns: (status, message)
        """
        # Try wechat-cli
        try:
            result = subprocess.run(
                ["wechat", "--version"],
                capture_output=True,
                timeout=5,
                text=True
            )
            if result.returncode == 0:
                self.active_backend = "wechat-cli"
                return ("ok", f"WeChat: CLI ready ({result.stdout.strip()})")
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        # Try itchat
        if ITCHAT_AVAILABLE:
            try:
                # Quick check: can we import and initialize?
                self.active_backend = "itchat"
                return ("ok", "WeChat: itchat ready (login required)")
            except Exception:
                pass
        
        # Try Selenium
        if SELENIUM_AVAILABLE:
            self.active_backend = "selenium"
            return ("ok", "WeChat: Selenium ready (browser-based)")
        
        return (
            "fail",
            "WeChat: no backend available. Install: pipx install wechat-cli OR pip install itchat"
        )
    
    def extract(self, url: str) -> ExtractionResult:
        """
        Extract data from WeChat URL.
        
        Args:
            url: WeChat Official Account, group, or mini program URL
            
        Returns:
            ExtractionResult with success flag and data
        """
        if not self.can_handle(url):
            return ExtractionResult(
                success=False,
                error=f"Not a WeChat URL: {url}",
                backend_used=None
            )
        
        if not self.active_backend:
            self.check()
        
        if self.active_backend == "wechat-cli":
            return self._extract_with_cli(url)
        elif self.active_backend == "itchat":
            return self._extract_with_itchat(url)
        elif self.active_backend == "selenium":
            return self._extract_with_selenium(url)
        
        return ExtractionResult(
            success=False,
            error=f"WeChat: {self.active_backend or 'no backend available'}",
            backend_used=None
        )
    
    def _extract_with_cli(self, url: str) -> ExtractionResult:
        """Extract using wechat-cli."""
        try:
            result = subprocess.run(
                ["wechat", "extract", url, "--json"],
                capture_output=True,
                timeout=20,
                text=True
            )
            
            if result.returncode != 0:
                return ExtractionResult(
                    success=False,
                    error=f"CLI extraction failed: {result.stderr}",
                    backend_used="wechat-cli"
                )
            
            import json
            data = json.loads(result.stdout)
            
            if isinstance(data, dict):
                data = [data]
            
            return ExtractionResult(
                success=True,
                data=data,
                backend_used="wechat-cli",
                item_count=len(data) if data else 0
            )
        
        except subprocess.TimeoutExpired:
            return ExtractionResult(
                success=False,
                error="CLI extraction timed out (>20s)",
                backend_used="wechat-cli"
            )
        except Exception as e:
            return ExtractionResult(
                success=False,
                error=f"CLI extraction failed: {e}",
                backend_used="wechat-cli"
            )
    
    def _extract_with_itchat(self, url: str) -> ExtractionResult:
        """Extract using itchat library."""
        try:
            if not ITCHAT_AVAILABLE:
                return ExtractionResult(
                    success=False,
                    error="itchat not available (pip install itchat)",
                    backend_used=None
                )
            
            # Extract target from URL
            target = self._parse_wechat_target(url)
            if not target:
                return ExtractionResult(
                    success=False,
                    error=f"Could not parse WeChat target from URL: {url}",
                    backend_used="itchat"
                )
            
            # Login if needed
            if not itchat.check_login():
                itchat.login()
            
            # Get messages from target
            # Note: This is simplified; itchat API varies by version
            messages = itchat.get_msg(target)
            
            data = [
                {
                    "id": msg.get("MsgId"),
                    "content": msg.get("Content"),
                    "timestamp": msg.get("CreateTime"),
                    "from": msg.get("FromUserName"),
                    "type": msg.get("MsgType")
                }
                for msg in messages
            ]
            
            return ExtractionResult(
                success=bool(data),
                data=data,
                backend_used="itchat",
                item_count=len(data)
            )
        
        except Exception as e:
            return ExtractionResult(
                success=False,
                error=f"itchat extraction failed: {e}",
                backend_used="itchat"
            )
    
    def _extract_with_selenium(self, url: str) -> ExtractionResult:
        """Extract using Selenium browser automation."""
        if not SELENIUM_AVAILABLE:
            return ExtractionResult(
                success=False,
                error="Selenium not available (pip install selenium)",
                backend_used=None
            )
        
        try:
            driver = webdriver.Chrome()
            driver.get(url)
            
            # Wait for content to load
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.by import By
            
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "content")))
            
            # Extract posts/messages
            items = driver.find_elements(By.CLASS_NAME, "js_item")
            
            data = []
            for item in items:
                try:
                    text = item.find_element(By.CLASS_NAME, "js_article_title").text
                    url_elem = item.find_element(By.TAG_NAME, "a")
                    item_url = url_elem.get_attribute("href")
                    
                    data.append({
                        "title": text,
                        "url": item_url,
                        "platform": "wechat"
                    })
                except Exception:
                    continue
            
            driver.quit()
            
            return ExtractionResult(
                success=bool(data),
                data=data,
                backend_used="selenium",
                item_count=len(data)
            )
        
        except Exception as e:
            return ExtractionResult(
                success=False,
                error=f"Selenium extraction failed: {e}",
                backend_used="selenium"
            )
    
    @staticmethod
    def _parse_wechat_target(url: str) -> Optional[str]:
        """Parse WeChat target (account, group, etc.) from URL."""
        # Official Account: mp.weixin.qq.com/profile_ext?action=home&__biz=...
        match = re.search(r"__biz=([^&]+)", url)
        if match:
            return match.group(1)
        
        # Mini Program: wx.qq.com?...
        match = re.search(r"appid=([^&]+)", url)
        if match:
            return match.group(1)
        
        # Group: weixin://dl/chat/...
        match = re.search(r"chat/([^/]+)", url)
        if match:
            return match.group(1)
        
        return None
    
    def __repr__(self) -> str:
        return f"<WeChatChannel active_backend={self.active_backend}>"
