# -*- coding: utf-8 -*-
"""
Shopee E-Commerce Data Extraction Channel

Backends:
1. shopee-cli (primary) - fastest, most reliable
2. Selenium (fallback) - when CLI unavailable

Supported regions: ID, MY, PH, SG, TH, VN
"""

import re
import subprocess
import logging
from typing import List, Optional, Tuple
from dataclasses import dataclass

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

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


class ShopeeChannel:
    """
    Shopee product/shop extraction channel.
    
    Detects Shopee URLs and extracts data using available backends.
    Probe order: shopee-cli → Selenium
    """
    
    name = "shopee"
    description = "E-commerce extraction for Shopee (ID, MY, PH, SG, TH, VN)"
    backends = ["shopee-cli", "selenium"]
    tier = 1
    
    def __init__(self):
        self.active_backend = None
        self.logger = logging.getLogger(f"{__name__}.{self.name}")
    
    def can_handle(self, url: str) -> bool:
        """Check if URL is a Shopee URL."""
        if not isinstance(url, str):
            return False
        domain = re.search(r"://([^/]+)", url)
        if not domain:
            return False
        d = domain.group(1).lower()
        return "shopee" in d and any(
            tld in d for tld in [".co.id", ".com.my", ".com.ph", ".com.sg", ".com.th", ".vn"]
        )
    
    def check(self, config=None) -> Tuple[str, str]:
        """
        Probe available backends.
        Returns: (status, message)
        """
        # Try shopee-cli
        try:
            result = subprocess.run(
                ["shopee-cli", "--version"],
                capture_output=True,
                timeout=5,
                text=True
            )
            if result.returncode == 0:
                self.active_backend = "shopee-cli"
                return ("ok", f"Shopee: shopee-cli ready ({result.stdout.strip()})")
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        # Try Selenium
        if SELENIUM_AVAILABLE:
            try:
                driver = webdriver.Chrome()
                driver.quit()
                self.active_backend = "selenium"
                return ("ok", "Shopee: Selenium ready (Chrome/Chromium)")
            except Exception as e:
                self.logger.debug(f"Selenium probe failed: {e}")
        
        return ("fail", "Shopee: no working backend available. Install shopee-cli: pipx install shopee-cli")
    
    def extract(self, url: str) -> ExtractionResult:
        """
        Extract data from Shopee URL.
        
        Args:
            url: Shopee product or shop URL
            
        Returns:
            ExtractionResult with success flag and data
        """
        if not self.can_handle(url):
            return ExtractionResult(
                success=False,
                error=f"Not a Shopee URL: {url}",
                backend_used=None
            )
        
        if not self.active_backend:
            self.check()
        
        if self.active_backend == "shopee-cli":
            return self._extract_with_cli(url)
        elif self.active_backend == "selenium":
            return self._extract_with_selenium(url)
        
        return ExtractionResult(
            success=False,
            error=f"Shopee: {self.active_backend or 'no backend available'}",
            backend_used=None
        )
    
    def _extract_with_cli(self, url: str) -> ExtractionResult:
        """Extract using shopee-cli."""
        try:
            result = subprocess.run(
                ["shopee-cli", "extract", url, "--json"],
                capture_output=True,
                timeout=10,
                text=True
            )
            
            if result.returncode != 0:
                return ExtractionResult(
                    success=False,
                    error=f"shopee-cli extraction failed: {result.stderr}",
                    backend_used="shopee-cli"
                )
            
            import json
            data = json.loads(result.stdout)
            
            # Normalize: ensure list format
            if isinstance(data, dict):
                data = [data]
            
            return ExtractionResult(
                success=True,
                data=data,
                backend_used="shopee-cli",
                item_count=len(data) if data else 0
            )
        
        except subprocess.TimeoutExpired:
            return ExtractionResult(
                success=False,
                error="shopee-cli extraction timed out (>10s)",
                backend_used="shopee-cli"
            )
        except Exception as e:
            return ExtractionResult(
                success=False,
                error=f"shopee-cli extraction failed: {e}",
                backend_used="shopee-cli"
            )
    
    def _extract_with_selenium(self, url: str) -> ExtractionResult:
        """Extract using Selenium + Chrome."""
        if not SELENIUM_AVAILABLE:
            return ExtractionResult(
                success=False,
                error="Selenium not available (pip install selenium)",
                backend_used=None
            )
        
        driver = None
        try:
            driver = webdriver.Chrome()
            driver.get(url)
            
            # Wait for product data to load
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product")))
            
            # Extract product info (simplified)
            products = []
            product_elements = driver.find_elements(By.CLASS_NAME, "product")
            
            for elem in product_elements:
                try:
                    title = elem.find_element(By.CLASS_NAME, "title").text
                    price = elem.find_element(By.CLASS_NAME, "price").text
                    products.append({
                        "title": title,
                        "price": price,
                        "url": url
                    })
                except:
                    pass
            
            return ExtractionResult(
                success=bool(products),
                data=products,
                backend_used="selenium",
                item_count=len(products)
            )
        
        except Exception as e:
            return ExtractionResult(
                success=False,
                error=f"Selenium extraction failed: {e}",
                backend_used="selenium"
            )
        
        finally:
            if driver:
                driver.quit()
    
    def _extract_product_id(self, url: str) -> Optional[str]:
        """Extract Shopee product ID from URL."""
        match = re.search(r"/p/(\d+)", url)
        return match.group(1) if match else None
    
    def __repr__(self) -> str:
        return f"<ShopeeChannel active_backend={self.active_backend}>"
