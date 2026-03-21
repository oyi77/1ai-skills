"""
kling_account_manager.py — Multi-Account Kling Credit Manager

Manages a pool of Kling accounts for credit aggregation and rotation.
Each account accumulates free credits and daily login bonuses.

Accounts stored at: ~/.openclaw/workspace/config/kling_accounts.json
Format: [{"email": "...", "password": "...", "cookie": "...", "credits": 0}]
"""

from __future__ import annotations

import json
import logging
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

logger = logging.getLogger(__name__)

_DEFAULT_ACCOUNTS_FILE = Path(os.path.expanduser("~/.openclaw/workspace/config/kling_accounts.json"))
_LOG_DIR = Path(os.path.expanduser("~/.openclaw/workspace/logs"))
_KLING_BASE = "https://klingai.com"
_LOGIN_ENDPOINT = f"{_KLING_BASE}/api/user/login"
_CREDITS_ENDPOINT = f"{_KLING_BASE}/api/pay/current-credits"
_DAILY_BONUS_ENDPOINT = f"{_KLING_BASE}/api/pay/reward?activity=login_bonus_daily"


class KlingAccountManager:
    """
    Manage multiple Kling accounts for credit pooling and rotation.

    Strategy:
    - Maintain a pool of accounts; each contributes free credits.
    - Daily login bonus is claimed for every account each day.
    - When the active account drops below a threshold, rotate to the next.

    Args:
        accounts_file: Path to the accounts JSON file.
                       Defaults to ~/.openclaw/workspace/config/kling_accounts.json.
    """

    def __init__(self, accounts_file: Optional[str] = None) -> None:
        self._accounts_file = Path(accounts_file) if accounts_file else _DEFAULT_ACCOUNTS_FILE
        self._accounts: List[Dict[str, Any]] = []
        self._active_index: int = 0
        _LOG_DIR.mkdir(parents=True, exist_ok=True)
        self._accounts_file.parent.mkdir(parents=True, exist_ok=True)
        self.load_accounts()

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def load_accounts(self) -> None:
        """Load accounts from JSON file. Creates empty file if not found."""
        if not self._accounts_file.exists():
            logger.info("No accounts file at %s — starting empty.", self._accounts_file)
            self._accounts = []
            return
        try:
            with open(self._accounts_file, "r", encoding="utf-8") as fh:
                self._accounts = json.load(fh)
            logger.info("Loaded %d Kling accounts.", len(self._accounts))
        except (json.JSONDecodeError, OSError) as exc:
            logger.error("Failed to load accounts file: %s", exc)
            self._accounts = []

    def save_accounts(self) -> None:
        """Persist accounts to JSON file."""
        try:
            with open(self._accounts_file, "w", encoding="utf-8") as fh:
                json.dump(self._accounts, fh, indent=2, ensure_ascii=False)
            logger.debug("Saved %d accounts to %s", len(self._accounts), self._accounts_file)
        except OSError as exc:
            logger.error("Failed to save accounts: %s", exc)

    # ------------------------------------------------------------------
    # Account management
    # ------------------------------------------------------------------

    def add_account(self, email: str, password: str) -> bool:
        """
        Add an account, authenticate it, and fetch initial credits.

        Args:
            email:    Account email address.
            password: Account password.

        Returns:
            True if account was added and authenticated successfully.
        """
        # Check for duplicates
        if any(a.get("email") == email for a in self._accounts):
            logger.warning("Account %s already in pool.", email)
            return False

        account: Dict[str, Any] = {
            "email": email,
            "password": password,
            "cookie": "",
            "credits": 0.0,
            "added_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "last_bonus_claimed": None,
            "last_seen": None,
            "active": False,
        }

        # Authenticate
        cookie = self._authenticate(email, password)
        if cookie:
            account["cookie"] = cookie
            account["active"] = True
            credits = self._fetch_credits(cookie)
            account["credits"] = credits
            logger.info("Account %s authenticated. Credits: %.1f", email, credits)
        else:
            logger.warning("Authentication failed for %s — account added but inactive.", email)

        self._accounts.append(account)
        self.save_accounts()
        return bool(cookie)

    def _authenticate(self, email: str, password: str) -> Optional[str]:
        """
        Authenticate with Kling and return the session cookie string.

        Returns:
            Cookie string on success, None on failure.
        """
        try:
            session = requests.Session()
            payload = {"email": email, "password": password, "type": 0}
            resp = session.post(
                _LOGIN_ENDPOINT,
                json=payload,
                headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
            if data.get("code") != 0:
                logger.warning("Login failed for %s: %s", email, data.get("message", "unknown"))
                return None
            # Compose cookie string from session cookies
            cookies = "; ".join(f"{k}={v}" for k, v in session.cookies.items())
            return cookies
        except Exception as exc:  # noqa: BLE001
            logger.error("Authentication error for %s: %s", email, exc)
            return None

    def _fetch_credits(self, cookie: str) -> float:
        """Fetch remaining credits for the given cookie session."""
        try:
            resp = requests.get(
                _CREDITS_ENDPOINT,
                headers={"Cookie": cookie, "User-Agent": "Mozilla/5.0"},
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
            return float(data.get("data", {}).get("remaining_credits", 0))
        except Exception as exc:  # noqa: BLE001
            logger.warning("Could not fetch credits: %s", exc)
            return 0.0

    # ------------------------------------------------------------------
    # Account selection
    # ------------------------------------------------------------------

    def get_best_account(self, min_credits: float = 60.0) -> Optional[Dict[str, Any]]:
        """
        Return the active account with the highest credits above min_credits.

        Args:
            min_credits: Minimum acceptable credits (default 60).

        Returns:
            Account dict or None if no account qualifies.
        """
        self._refresh_credits()
        candidates = [
            a for a in self._accounts
            if a.get("active") and float(a.get("credits", 0)) >= min_credits
        ]
        if not candidates:
            logger.warning("No account with >= %.0f credits.", min_credits)
            return None
        best = max(candidates, key=lambda a: float(a.get("credits", 0)))
        logger.info("Best account: %s (%.1f credits)", best.get("email"), best.get("credits"))
        return best

    def rotate_if_low(
        self,
        current_credits: float,
        threshold: float = 60.0,
    ) -> Optional[Dict[str, Any]]:
        """
        Return a different account if current_credits falls below threshold.

        Args:
            current_credits: Credits remaining on the current account.
            threshold:        Minimum credits before rotation.

        Returns:
            A new account dict if rotation triggered, else None.
        """
        if current_credits >= threshold:
            return None  # No rotation needed
        logger.info("Credits %.1f < threshold %.1f — rotating account.", current_credits, threshold)
        return self.get_best_account(min_credits=threshold)

    def _refresh_credits(self) -> None:
        """Refresh credit balances for all active accounts."""
        for account in self._accounts:
            if not account.get("active") or not account.get("cookie"):
                continue
            credits = self._fetch_credits(account["cookie"])
            account["credits"] = credits
            account["last_seen"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        self.save_accounts()

    # ------------------------------------------------------------------
    # Daily bonuses
    # ------------------------------------------------------------------

    def claim_all_daily_bonuses(self) -> Dict[str, Any]:
        """
        Claim the daily login bonus for every active account.

        Returns:
            dict: {"claimed": [email, ...], "failed": [email, ...], "total_claimed": N}
        """
        claimed: List[str] = []
        failed: List[str] = []
        today = time.strftime("%Y-%m-%d")

        for account in self._accounts:
            if not account.get("active") or not account.get("cookie"):
                continue
            last_claimed = account.get("last_bonus_claimed", "")
            if last_claimed and last_claimed.startswith(today):
                logger.debug("Daily bonus already claimed today for %s", account.get("email"))
                claimed.append(account.get("email", ""))
                continue

            try:
                resp = requests.get(
                    _DAILY_BONUS_ENDPOINT,
                    headers={
                        "Cookie": account["cookie"],
                        "User-Agent": "Mozilla/5.0",
                    },
                    timeout=15,
                )
                resp.raise_for_status()
                data = resp.json()
                if data.get("code") == 0:
                    account["last_bonus_claimed"] = time.strftime("%Y-%m-%dT%H:%M:%S")
                    # Re-fetch credits after bonus
                    account["credits"] = self._fetch_credits(account["cookie"])
                    claimed.append(account.get("email", ""))
                    logger.info("Daily bonus claimed for %s — new credits: %.1f", account.get("email"), account["credits"])
                else:
                    logger.warning("Bonus claim failed for %s: %s", account.get("email"), data.get("message", ""))
                    failed.append(account.get("email", ""))
            except Exception as exc:  # noqa: BLE001
                logger.error("Bonus claim error for %s: %s", account.get("email"), exc)
                failed.append(account.get("email", ""))

        self.save_accounts()
        self._log_operation("claim_daily_bonus", {"claimed": len(claimed), "failed": len(failed)})
        return {"claimed": claimed, "failed": failed, "total_claimed": len(claimed)}

    # ------------------------------------------------------------------
    # Aggregate stats
    # ------------------------------------------------------------------

    def get_total_credits(self) -> float:
        """
        Return total credits across all active accounts.

        Returns:
            Sum of credits for active accounts.
        """
        self._refresh_credits()
        return sum(float(a.get("credits", 0)) for a in self._accounts if a.get("active"))

    def account_summary(self) -> List[Dict[str, Any]]:
        """
        Return a summary of all accounts with masked email.

        Returns:
            List of dicts: {"email_masked", "credits", "active", "last_seen"}
        """
        def _mask(email: str) -> str:
            parts = email.split("@")
            if len(parts) == 2:
                return parts[0][:3] + "***@" + parts[1]
            return email[:6] + "***"

        return [
            {
                "email_masked": _mask(a.get("email", "")),
                "credits": float(a.get("credits", 0)),
                "active": a.get("active", False),
                "last_seen": a.get("last_seen"),
                "last_bonus_claimed": a.get("last_bonus_claimed"),
            }
            for a in self._accounts
        ]

    def remove_account(self, email: str) -> bool:
        """Remove an account from the pool by email."""
        before = len(self._accounts)
        self._accounts = [a for a in self._accounts if a.get("email") != email]
        if len(self._accounts) < before:
            self.save_accounts()
            logger.info("Removed account: %s", email)
            return True
        return False

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------

    def _log_operation(self, operation: str, data: Dict[str, Any]) -> None:
        log_file = _LOG_DIR / "kling_account_manager.log"
        entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "operation": operation,
            **data,
        }
        try:
            with open(log_file, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(entry) + "\n")
        except Exception:  # noqa: BLE001
            pass

    def __repr__(self) -> str:
        return (
            f"<KlingAccountManager accounts={len(self._accounts)} "
            f"total_credits={self.get_total_credits():.0f}>"
        )
