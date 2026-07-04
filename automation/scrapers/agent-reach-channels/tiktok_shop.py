# -*- coding: utf-8 -*-
"""TikTok Shop — TikTok's integrated e-commerce platform.

Backends: tiktok-shop-cli (primary), web scraping via Playwright (fallback).
Auth: Cookie-based (TikTok account login).
"""

import json
import re
import subprocess
from urllib.parse import urlparse

from agent_reach.utils.process import utf8_subprocess_env

from .base import Channel


class TikTokShopChannel(Channel):
    name = "tiktok_shop"
    description = "TikTok Shop products, live streams, seller metrics"
    backends = ["tiktok-shop-cli", "web scraping (Playwright)"]
    tier = 2  # Requires TikTok account login

    def can_handle(self, url: str) -> bool:
        """Match TikTok Shop URLs."""
        d = urlparse(url).netloc.lower()
        return "tiktok.com" in d and ("/shop/" in url or "/live/" in url or "seller" in url.lower())

    def check(self, config=None):
        """Probe tiktok-shop-cli first; fall back to Playwright."""
        result = self._check_tiktok_cli()
        if result and result[0] != "fail":
            self.active_backend = "tiktok-shop-cli"
            return result

        result = self._check_playwright()
        if result and result[0] != "fail":
            self.active_backend = "Playwright"
            return result

        self.active_backend = None
        return (
            "fail",
            "TikTok Shop: no working backend available. Install: pipx install tiktok-shop-cli && pip install playwright",
        )

    def _check_tiktok_cli(self):
        """Check if tiktok-shop-cli is installed."""
        try:
            result = subprocess.run(
                ["tiktok-shop-cli", "--version"],
                capture_output=True,
                text=True,
                timeout=5,
                env=utf8_subprocess_env(),
            )
            if result.returncode == 0:
                return ("ok", f"tiktok-shop-cli {result.stdout.strip()}")
            return ("warn", "tiktok-shop-cli found but broken. Reinstall: pipx install --force tiktok-shop-cli")
        except FileNotFoundError:
            return None
        except subprocess.TimeoutExpired:
            return ("warn", "tiktok-shop-cli check timed out")
        except Exception as e:
            return ("warn", f"tiktok-shop-cli check failed: {e}")

    def _check_playwright(self):
        """Check if Playwright is installed."""
        try:
            import playwright
            return ("ok", "Playwright available")
        except ImportError:
            return ("warn", "Playwright not installed. Install: pip install playwright && playwright install chromium")
        except Exception as e:
            return ("warn", f"Playwright check failed: {e}")

    def extract(self, url: str) -> list[dict]:
        """Extract TikTok Shop data (products, live streams, metrics)."""
        if not self.active_backend:
            self.check()

        if "tiktok-shop-cli" in (self.active_backend or ""):
            return self._extract_with_cli(url)
        elif "Playwright" in (self.active_backend or ""):
            return self._extract_with_playwright(url)
        else:
            return [{"error": f"TikTok Shop: {self.active_backend or 'no backend available'}"}]

    def _extract_with_cli(self, url: str) -> list[dict]:
        """Extract using tiktok-shop-cli."""
        try:
            product_id = self._extract_product_id(url)
            if not product_id:
                return [{"error": f"Could not extract TikTok Shop product ID from {url}"}]

            result = subprocess.run(
                ["tiktok-shop-cli", "product", product_id, "--format=json"],
                capture_output=True,
                text=True,
                timeout=10,
                env=utf8_subprocess_env(),
            )

            if result.returncode == 0:
                data = json.loads(result.stdout)
                return [
                    {
                        "title": data.get("title"),
                        "price": data.get("price"),
                        "sales": data.get("sales_count"),
                        "rating": data.get("rating"),
                        "shop": data.get("shop_name"),
                        "seller_id": data.get("seller_id"),
                        "url": url,
                    }
                ]
            return [{"error": f"tiktok-shop-cli failed: {result.stderr}"}]
        except json.JSONDecodeError:
            return [{"error": "tiktok-shop-cli output not JSON"}]
        except subprocess.TimeoutExpired:
            return [{"error": "tiktok-shop-cli timeout"}]
        except Exception as e:
            return [{"error": f"tiktok-shop-cli extraction failed: {e}"}]

    def _extract_with_playwright(self, url: str) -> list[dict]:
        """Extract using Playwright."""
        try:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(url)
                page.wait_for_load_state("networkidle")

                # Extract product data
                title = page.locator("[data-test-id='product-title']").first.text_content()
                price = page.locator("[data-test-id='product-price']").first.text_content()
                sales = page.locator("[data-test-id='sales-count']").first.text_content()

                browser.close()

                return [
                    {
                        "title": title,
                        "price": price,
                        "sales": sales,
                        "url": url,
                    }
                ]
        except Exception as e:
            return [{"error": f"Playwright extraction failed: {e}"}]

    def _extract_product_id(self, url: str) -> str:
        """Extract TikTok Shop product ID from URL."""
        match = re.search(r"product/(\d+)", url)
        return match.group(1) if match else None
