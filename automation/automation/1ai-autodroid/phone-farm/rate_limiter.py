#!/usr/bin/env python3
"""
Phone Farm — Token Bucket Rate Limiter

Per-tenant rate limiting with ASGI middleware integration.
Pure Python, zero external dependencies.
"""

import threading
import time
from typing import Callable, Optional


class TokenBucket:
    """Token bucket rate limiter."""

    def __init__(self, rate: float = 1.67, burst: int = 20):
        """Initialize bucket.

        Args:
            rate: Tokens added per second (~100/min default)
            burst: Maximum bucket capacity
        """
        self.rate = rate
        self.burst = burst
        self.tokens = float(burst)
        self.last_refill = time.monotonic()
        self._lock = threading.Lock()

    def _refill(self):
        """Add tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self.last_refill
        self.tokens = min(self.burst, self.tokens + elapsed * self.rate)
        self.last_refill = now

    def consume(self, tokens: int = 1) -> bool:
        """Try to consume tokens. Returns True if allowed."""
        with self._lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

    @property
    def remaining(self) -> float:
        """Current available tokens."""
        with self._lock:
            self._refill()
            return self.tokens

    @property
    def reset_at(self) -> float:
        """Seconds until bucket is full again."""
        with self._lock:
            if self.tokens >= self.burst:
                return 0.0
            deficit = self.burst - self.tokens
            return deficit / self.rate


class RateLimiter:
    """Manages per-key rate limit buckets with cleanup."""

    def __init__(self, default_rate: float = 1.67, default_burst: int = 20):
        self.default_rate = default_rate
        self.default_burst = default_burst
        self._buckets: dict[str, TokenBucket] = {}
        self._limits: dict[str, tuple[float, int]] = {}
        self._last_access: dict[str, float] = {}
        self._lock = threading.Lock()
        self._cleanup_interval = 600  # 10 minutes

    def _get_bucket(self, key: str) -> TokenBucket:
        """Get or create bucket for key."""
        if key not in self._buckets:
            rate, burst = self._limits.get(key, (self.default_rate, self.default_burst))
            self._buckets[key] = TokenBucket(rate=rate, burst=burst)
        self._last_access[key] = time.monotonic()
        return self._buckets[key]

    def check(self, key: str) -> tuple[bool, dict]:
        """Check if request is allowed. Returns (allowed, headers)."""
        allowed = self._get_bucket(key).consume()
        bucket = self._buckets[key]
        rate, burst = self._limits.get(key, (self.default_rate, self.default_burst))
        headers = {
            "X-RateLimit-Limit": str(burst),
            "X-RateLimit-Remaining": str(int(bucket.remaining)),
            "X-RateLimit-Reset": str(int(bucket.reset_at)),
        }
        return allowed, headers

    def set_limit(self, key: str, rate: float, burst: int):
        """Set custom rate limit for a key."""
        self._limits[key] = (rate, burst)
        if key in self._buckets:
            self._buckets[key] = TokenBucket(rate=rate, burst=burst)

    def cleanup(self):
        """Remove stale buckets (idle > 10 min)."""
        now = time.monotonic()
        with self._lock:
            stale = [
                k
                for k, t in self._last_access.items()
                if now - t > self._cleanup_interval
            ]
            for k in stale:
                del self._buckets[k]
                del self._last_access[k]


# Paths that skip rate limiting
SKIP_PATHS = {
    "/health",
    "/health/ready",
    "/health/live",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/auth/token",
}
SKIP_PREFIXES = ("/dashboard/",)


class RateLimitMiddleware:
    """ASGI middleware for rate limiting."""

    def __init__(
        self,
        app,
        limiter: Optional[RateLimiter] = None,
        key_extractor: Optional[Callable] = None,
    ):
        self.app = app
        self.limiter = limiter or RateLimiter()
        self.key_extractor = key_extractor or self._default_key_extractor

    @staticmethod
    def _default_key_extractor(scope: dict) -> str:
        """Extract rate limit key from ASGI scope (tenant_id)."""
        return scope.get("state", {}).get("tenant_id", "anonymous")

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        path = scope.get("path", "")

        # Skip rate-limited paths
        if path in SKIP_PATHS or any(path.startswith(p) for p in SKIP_PREFIXES):
            await self.app(scope, receive, send)
            return

        key = self.key_extractor(scope)
        allowed, headers = self.limiter.check(key)

        if not allowed:
            body = b'{"detail":"Rate limit exceeded","error":"too_many_requests"}'
            await send(
                {
                    "type": "http.response.start",
                    "status": 429,
                    "headers": [
                        (b"content-type", b"application/json"),
                        (
                            b"retry-after",
                            str(
                                max(1, int(headers.get("X-RateLimit-Reset", 1)))
                            ).encode(),
                        ),
                        (b"x-ratelimit-limit", headers["X-RateLimit-Limit"].encode()),
                        (
                            b"x-ratelimit-remaining",
                            headers["X-RateLimit-Remaining"].encode(),
                        ),
                        (b"x-ratelimit-reset", headers["X-RateLimit-Reset"].encode()),
                    ],
                }
            )
            await send({"type": "http.response.body", "body": body})
            return

        # Inject rate limit headers into response
        async def send_with_headers(message):
            if message["type"] == "http.response.start":
                existing = list(message.get("headers", []))
                existing.extend(
                    [
                        (b"x-ratelimit-limit", headers["X-RateLimit-Limit"].encode()),
                        (
                            b"x-ratelimit-remaining",
                            headers["X-RateLimit-Remaining"].encode(),
                        ),
                        (b"x-ratelimit-reset", headers["X-RateLimit-Reset"].encode()),
                    ]
                )
                message["headers"] = existing
            await send(message)

        await self.app(scope, receive, send_with_headers)


# Global instance
_limiter: Optional[RateLimiter] = None


def get_limiter() -> RateLimiter:
    """Get or create the global rate limiter instance."""
    global _limiter
    if _limiter is None:
        _limiter = RateLimiter()
    return _limiter


if __name__ == "__main__":
    limiter = RateLimiter(default_rate=10, default_burst=5)
    print("Testing rate limiter...")
    for i in range(10):
        allowed, headers = limiter.check("test-key")
        print(
            f"  Request {i + 1}: allowed={allowed}, remaining={headers['X-RateLimit-Remaining']}"
        )
    print("Done!")
