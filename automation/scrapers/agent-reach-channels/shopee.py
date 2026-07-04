# -*- coding: utf-8 -*-
"""Shopee — Indonesia/Southeast Asia e-commerce platform.

Backends: shopee-cli (primary), web scraping (fallback).
Auth: Cookie-based (browser login or shopee-cli).
"""

import json
import re
import subprocess
from urllib.parse import urlparse

from agent_reach.utils.process import utf8_subprocess_env

from .base import Channel


class ShopeeChannel(Channel):
    name = "shopee"
    description = "Shopee products, reviews, seller info (Indonesia/SEA)"
    backends = ["shopee-cli", "web scraping"]
    tier = 2  # Requires authentication or cookies

    def can_handle(self, url: str) -> bool:
        """Match Shopee URLs: shopee.co.id, shopee.com.my, etc."""
        d = urlparse(url).netloc.lower()
        return "shopee" in d and any(tld in d for tld in [".co.id", ".com.my", ".com.ph", ".com.sg", ".com.th", ".vn"])

    def check(self, config=None):
        """Probe shopee-cli first; fall back to web scraping."""
        result = self._check_shopee_cli()
        if result and result[0] != "fail":
            self.active_backend = "shopee-cli"
            return result

        result = self._check_web_scraping()
        if result and result[0] != "fail":
            self.active_backend = "web scraping (selenium)"
            return result

        self.active_backend = None
        return ("fail", "Shopee: no working backend available. Install shopee-cli: pipx install shopee-cli")

    def _check_shopee_cli(self):
        """Check if shopee-cli is installed and usable."""
        try:
            result = subprocess.run(
                ["shopee-cli", "--version"],
                capture_output=True,
                text=True,
                timeout=5,
                env=utf8_subprocess_env(),
            )
            if result.returncode == 0:
                return ("ok", f"shopee-cli {result.stdout.strip()}")
            return ("warn", "shopee-cli found but broken. Reinstall: pipx install --force shopee-cli")
        except FileNotFoundError:
            return None
        except subprocess.TimeoutExpired:
            return ("warn", "shopee-cli check timed out")
        except Exception as e:
            return ("warn", f"shopee-cli check failed: {e}")

    def _check_web_scraping(self):
        """Check if Selenium and Chrome are available for web scraping."""
        try:
            import selenium
            result = subprocess.run(
                ["which", "google-chrome"] if self._is_unix() else ["where", "chrome"],
                capture_output=True,
                timeout=3,
            )
            if result.returncode == 0:
                return ("ok", "selenium + Chrome available")
            return ("warn", "Selenium available but Chrome not found. Install: apt install google-chrome-stable")
        except ImportError:
            return ("warn", "Selenium not installed. Install: pip install selenium")
        except Exception as e:
            return ("warn", f"Web scraping check failed: {e}")

    def _is_unix(self):
        import sys
        return sys.platform in ("linux", "darwin")

    def extract(self, url: str) -> list[dict]:
        """Extract Shopee product/review data."""
        if not self.active_backend:
            self.check()

        if "shopee-cli" in (self.active_backend or ""):
            return self._extract_with_cli(url)
        elif "web scraping" in (self.active_backend or ""):
            return self._extract_with_selenium(url)
        else:
            return [{"error": f"Shopee: {self.active_backend or 'no backend available'}"}]

    def _extract_with_cli(self, url: str) -> list[dict]:
        """Extract using shopee-cli."""
        try:
            product_id = self._extract_product_id(url)
            if not product_id:
                return [{"error": f"Could not extract Shopee product ID from {url}"}]

            result = subprocess.run(
                ["shopee-cli", "product", product_id, "--format=json"],
                capture_output=True,
                text=True,
                timeout=10,
                env=utf8_subprocess_env(),
            )

            if result.returncode == 0:
                data = json.loads(result.stdout)
                return [
                    {
                        "title": data.get("name"),
                        "price": data.get("price"),
                        "rating": data.get("rating"),
                        "reviews": data.get("review_count"),
                        "shop": data.get("shop_name"),
                        "url": url,
                    }
                ]
            return [{"error": f"shopee-cli failed: {result.stderr}"}]
        except json.JSONDecodeError:
            return [{"error": "shopee-cli output not JSON"}]
        except subprocess.TimeoutExpired:
            return [{"error": "shopee-cli timeout"}]
        except Exception as e:
            return [{"error": f"shopee-cli extraction failed: {e}"}]

    def _extract_with_selenium(self, url: str) -> list[dict]:
        """Extract using Selenium + Chrome."""
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            driver = webdriver.Chrome()
            driver.get(url)

            # Wait for product data to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "shopee-product-title"))
            )

            title = driver.find_element(By.CLASS_NAME, "shopee-product-title").text
            price = driver.find_element(By.CLASS_NAME, "shopee-product-price").text
            rating = driver.find_element(By.CLASS_NAME, "shopee-product-rating").text

            driver.quit()

            return [
                {
                    "title": title,
                    "price": price,
                    "rating": rating,
                    "url": url,
                }
            ]
        except Exception as e:
            return [{"error": f"Selenium extraction failed: {e}"}]

    def _extract_product_id(self, url: str) -> str:
        """Extract Shopee product ID from URL."""
        match = re.search(r"/p/(\d+)", url)
        return match.group(1) if match else None
