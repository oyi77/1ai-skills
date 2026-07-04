# -*- coding: utf-8 -*-
"""WeChat — Chinese messaging + mini-programs platform.

Backends: wechat-cli (primary), web.wechat.com scraping (fallback).
Auth: QR code login or existing session.
"""

import json
import re
import subprocess
from urllib.parse import urlparse

from agent_reach.utils.process import utf8_subprocess_env

from .base import Channel


class WeChatChannel(Channel):
    name = "wechat"
    description = "WeChat Official Accounts, mini-programs, Moments (中国)"
    backends = ["wechat-cli", "web scraping"]
    tier = 2  # Requires WeChat account + QR code login

    def can_handle(self, url: str) -> bool:
        """Match WeChat URLs and IDs."""
        d = urlparse(url).netloc.lower()
        # WeChat Official Account URLs, mini-program links, or direct WeChat IDs
        return bool(
            "weixin.qq.com" in d
            or "wechat.com" in d
            or re.search(r"^[a-zA-Z0-9_-]{5,20}$", url)  # WeChat ID pattern
        )

    def check(self, config=None):
        """Probe wechat-cli first; fall back to web scraping."""
        result = self._check_wechat_cli()
        if result and result[0] != "fail":
            self.active_backend = "wechat-cli"
            return result

        result = self._check_web_scraping()
        if result and result[0] != "fail":
            self.active_backend = "web scraping (selenium)"
            return result

        self.active_backend = None
        return (
            "fail",
            "WeChat: no working backend available. Install: pipx install wechat-cli && pip install selenium",
        )

    def _check_wechat_cli(self):
        """Check if wechat-cli is installed and authenticated."""
        try:
            result = subprocess.run(
                ["wechat-cli", "--version"],
                capture_output=True,
                text=True,
                timeout=5,
                env=utf8_subprocess_env(),
            )
            if result.returncode == 0:
                return ("ok", f"wechat-cli {result.stdout.strip()}")
            return ("warn", "wechat-cli found but broken. Reinstall: pipx install --force wechat-cli")
        except FileNotFoundError:
            return None
        except subprocess.TimeoutExpired:
            return ("warn", "wechat-cli check timed out")
        except Exception as e:
            return ("warn", f"wechat-cli check failed: {e}")

    def _check_web_scraping(self):
        """Check if Selenium + Chrome available for web.wechat.com."""
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
        """Extract WeChat Official Account or mini-program data."""
        if not self.active_backend:
            self.check()

        if "wechat-cli" in (self.active_backend or ""):
            return self._extract_with_cli(url)
        elif "web scraping" in (self.active_backend or ""):
            return self._extract_with_selenium(url)
        else:
            return [{"error": f"WeChat: {self.active_backend or 'no backend available'}"}]

    def _extract_with_cli(self, url: str) -> list[dict]:
        """Extract using wechat-cli (Official Accounts, mini-programs)."""
        try:
            # Detect if it's an Official Account or mini-program
            wechat_id = self._extract_wechat_id(url)
            if not wechat_id:
                return [{"error": f"Could not extract WeChat ID from {url}"}]

            result = subprocess.run(
                ["wechat-cli", "user", wechat_id, "--format=json"],
                capture_output=True,
                text=True,
                timeout=10,
                env=utf8_subprocess_env(),
            )

            if result.returncode == 0:
                data = json.loads(result.stdout)
                return [
                    {
                        "name": data.get("name"),
                        "type": data.get("type"),  # official_account, mini_program, user
                        "description": data.get("description"),
                        "followers": data.get("followers"),
                        "verification": data.get("verification_status"),
                        "url": url,
                    }
                ]
            return [{"error": f"wechat-cli failed: {result.stderr}"}]
        except json.JSONDecodeError:
            return [{"error": "wechat-cli output not JSON"}]
        except subprocess.TimeoutExpired:
            return [{"error": "wechat-cli timeout"}]
        except Exception as e:
            return [{"error": f"wechat-cli extraction failed: {e}"}]

    def _extract_with_selenium(self, url: str) -> list[dict]:
        """Extract using Selenium (web.wechat.com)."""
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            driver = webdriver.Chrome()
            driver.get(url)

            # Wait for WeChat page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "wechat-account-name"))
            )

            name = driver.find_element(By.CLASS_NAME, "wechat-account-name").text
            description = driver.find_element(By.CLASS_NAME, "wechat-account-desc").text
            followers = driver.find_element(By.CLASS_NAME, "wechat-account-followers").text

            driver.quit()

            return [
                {
                    "name": name,
                    "description": description,
                    "followers": followers,
                    "url": url,
                }
            ]
        except Exception as e:
            return [{"error": f"Selenium extraction failed: {e}"}]

    def _extract_wechat_id(self, url: str) -> str:
        """Extract WeChat ID from URL or raw ID."""
        # Check if URL contains account parameter
        match = re.search(r"account=([a-zA-Z0-9_-]+)", url)
        if match:
            return match.group(1)

        # Check if it's a direct WeChat ID (alphanumeric, 5-20 chars)
        if re.match(r"^[a-zA-Z0-9_-]{5,20}$", url):
            return url

        # Check if it's a short URL with ID
        match = re.search(r"/([a-zA-Z0-9_-]{5,20})$", url)
        return match.group(1) if match else None
