#!/usr/bin/env python3
"""
post_bridge_client.py — Shared PostBridge API client.

Provides a reusable PostBridgeClient class for all marketing/sales scripts.
Reads API key from env POST_BRIDGE_API_KEY or falls back to the default key.

API reference:
    GET  /social-accounts          → list connected accounts
    POST /posts                    → create/schedule a post
    GET  /posts                    → list posts
    DELETE /posts/{id}             → delete a post
"""

import os
import logging
from typing import Optional

import requests

# ─── Configuration ────────────────────────────────────────────────────────────

POST_BRIDGE_BASE_URL = "https://api.post-bridge.com/v1"
POST_BRIDGE_API_KEY  = os.environ.get("POST_BRIDGE_API_KEY", "REDACTED_POSTBRIDGE_KEY")

log = logging.getLogger("post_bridge_client")


# ─── PostBridgeClient ─────────────────────────────────────────────────────────

class PostBridgeClient:
    """
    Client for the Post Bridge social media API.

    Usage:
        client = PostBridgeClient()

        # Discover connected accounts
        accounts = client.get_accounts()
        # [{"id": "acc_123", "platform": "twitter", "username": "myhandle"}, ...]

        # Post to specific accounts
        result = client.create_post(
            caption="Hello world!",
            account_ids=["acc_123", "acc_456"],
            media_urls=["https://example.com/image.jpg"],
            scheduled_at="2026-03-01T12:00:00Z",  # optional
        )

        # Broadcast to ALL connected accounts
        result = client.broadcast("Big announcement today!")
    """

    def __init__(
        self,
        api_key: str = POST_BRIDGE_API_KEY,
        base_url: str = POST_BRIDGE_BASE_URL,
    ):
        self.api_key  = api_key
        self.base_url = base_url.rstrip("/")
        self.session  = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
        )
        self._accounts_cache: Optional[list] = None

    # ── Account discovery ─────────────────────────────────────────────────────

    def get_accounts(self, use_cache: bool = True) -> list[dict]:
        """
        Return list of connected social accounts.

        Response format:
            [{"id": "acc_xxx", "platform": "twitter", "username": "handle"}, ...]
        """
        if use_cache and self._accounts_cache is not None:
            return self._accounts_cache

        try:
            resp = self.session.get(f"{self.base_url}/social-accounts", timeout=30)
            resp.raise_for_status()
            accounts = resp.json()
            if isinstance(accounts, dict):
                # Some APIs wrap in {"data": [...]}
                accounts = accounts.get("data", accounts.get("accounts", []))
            self._accounts_cache = accounts
            account_list = [f'{a.get("platform")}:{a.get("username")}' for a in accounts]
            log.info(f"📋 Found {len(accounts)} connected accounts: {account_list}")
            return accounts
        except Exception as e:
            log.error(f"Failed to fetch social accounts: {e}")
            return []

    def get_accounts_by_platform(self, platform: str) -> list[dict]:
        """Return accounts filtered by platform name."""
        accounts = self.get_accounts()
        return [a for a in accounts if a.get("platform", "").lower() == platform.lower()]

    def get_all_account_ids(self) -> list[str]:
        """Return IDs of all connected accounts."""
        return [a["id"] for a in self.get_accounts() if "id" in a]

    # ── Post management ───────────────────────────────────────────────────────

    def create_post(
        self,
        caption: str,
        account_ids: list[str],
        media_urls: Optional[list[str]] = None,
        scheduled_at: Optional[str] = None,
    ) -> dict:
        """
        Create (or schedule) a post on one or more social accounts.

        Args:
            caption:      Post text / caption.
            account_ids:  List of social account IDs to post to.
            media_urls:   Optional list of media URLs (images/videos).
            scheduled_at: ISO 8601 datetime string for scheduling (optional).

        Returns:
            API response dict, or {"error": ...} on failure.
        """
        if not account_ids:
            log.warning("create_post called with empty account_ids — skipping")
            return {"error": "No account IDs provided"}

        payload: dict = {
            "caption": caption,
            "social_accounts": account_ids,
        }

        if media_urls:
            payload["media"] = [{"url": url} for url in media_urls]

        if scheduled_at:
            payload["scheduled_at"] = scheduled_at

        try:
            resp = self.session.post(f"{self.base_url}/posts", json=payload, timeout=30)
            resp.raise_for_status()
            result = resp.json()
            log.info(f"✅ Post created | accounts={account_ids} | id={result.get('id', '?')}")
            return result
        except requests.HTTPError as e:
            body = ""
            try:
                body = e.response.text[:200]
            except Exception:
                pass
            log.error(f"create_post HTTP error: {e} | body={body}")
            return {"error": str(e), "body": body}
        except Exception as e:
            log.error(f"create_post failed: {e}")
            return {"error": str(e)}

    def broadcast(
        self,
        caption: str,
        media_urls: Optional[list[str]] = None,
        scheduled_at: Optional[str] = None,
    ) -> dict:
        """
        Broadcast a post to ALL connected social accounts.

        Args:
            caption:      Post text.
            media_urls:   Optional media URLs.
            scheduled_at: Optional ISO 8601 schedule time.

        Returns:
            API response dict.
        """
        account_ids = self.get_all_account_ids()
        if not account_ids:
            log.warning("broadcast: no connected accounts found")
            return {"error": "No connected accounts"}
        log.info(f"📡 Broadcasting to {len(account_ids)} accounts...")
        return self.create_post(caption, account_ids, media_urls, scheduled_at)

    def list_posts(self) -> list[dict]:
        """
        Return list of posts from the API.

        Returns:
            List of post dicts, or [] on error.
        """
        try:
            resp = self.session.get(f"{self.base_url}/posts", timeout=30)
            resp.raise_for_status()
            posts = resp.json()
            if isinstance(posts, dict):
                posts = posts.get("data", posts.get("posts", []))
            log.info(f"📋 Retrieved {len(posts)} posts")
            return posts
        except Exception as e:
            log.error(f"list_posts failed: {e}")
            return []

    def delete_post(self, post_id: str) -> bool:
        """
        Delete a post by ID.

        Args:
            post_id: The post ID to delete.

        Returns:
            True on success, False on failure.
        """
        try:
            resp = self.session.delete(f"{self.base_url}/posts/{post_id}", timeout=30)
            resp.raise_for_status()
            log.info(f"🗑️  Deleted post {post_id}")
            return True
        except Exception as e:
            log.error(f"delete_post({post_id}) failed: {e}")
            return False


# ─── Quick smoke-test ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    import json

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    client = PostBridgeClient()

    print("\n=== Connected Accounts ===")
    accounts = client.get_accounts(use_cache=False)
    print(json.dumps(accounts, indent=2))

    print("\n=== Recent Posts ===")
    posts = client.list_posts()
    print(json.dumps(posts[:3], indent=2))
