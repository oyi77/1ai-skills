"""JWT handling using python-jose."""

import os
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import JWTError, jwt

# JWT settings from environment
JWT_SECRET = os.environ.get("PHONEFARM_JWT_SECRET", "change-me-in-production")
JWT_ALGORITHM = "HS256"
DEFAULT_TOKEN_EXPIRE_SECONDS = 86400  # 24 hours


class JWTHandler:
    """
    JWT token handler using python-jose.
    Provides create and verify operations for JWT tokens.
    """

    def __init__(
        self,
        secret: Optional[str] = None,
        algorithm: str = JWT_ALGORITHM,
        default_expires_in: int = DEFAULT_TOKEN_EXPIRE_SECONDS,
    ):
        """
        Initialize JWT handler.

        Args:
            secret: Secret key for signing tokens. Defaults to PHONEFARM_JWT_SECRET env var.
            algorithm: JWT algorithm (default: HS256).
            default_expires_in: Default token expiration in seconds.
        """
        self.secret = secret or JWT_SECRET
        self.algorithm = algorithm
        self.default_expires_in = default_expires_in

    def create_token(
        self,
        subject: str,
        additional_claims: Optional[dict[str, Any]] = None,
        expires_in: Optional[int] = None,
    ) -> str:
        """
        Create a JWT token.

        Args:
            subject: Subject of the token (typically user_id).
            additional_claims: Additional claims to include in token payload.
            expires_in: Token expiration in seconds. Defaults to default_expires_in.

        Returns:
            Encoded JWT token string.
        """
        now = datetime.now(timezone.utc)
        expires_delta = timedelta(seconds=expires_in or self.default_expires_in)
        expires_at = now + expires_delta

        payload = {
            "sub": subject,
            "iat": now,
            "exp": expires_at,
        }

        if additional_claims:
            payload.update(additional_claims)

        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def verify_token(self, token: str) -> Optional[dict[str, Any]]:
        """
        Verify and decode a JWT token.

        Args:
            token: JWT token string.

        Returns:
            Decoded payload if valid, None if invalid/expired.
        """
        try:
            payload = jwt.decode(
                token,
                self.secret,
                algorithms=[self.algorithm],
            )
            return payload
        except JWTError:
            return None

    def decode_token(self, token: str, verify: bool = True) -> Optional[dict[str, Any]]:
        """
        Decode a JWT token without verification (for inspection).

        Args:
            token: JWT token string.
            verify: Whether to verify signature (default: True).

        Returns:
            Decoded payload or None on error.
        """
        try:
            if verify:
                return self.verify_token(token)
            return jwt.decode(
                token,
                self.secret,
                algorithms=[self.algorithm],
                options={"verify_signature": False},
            )
        except JWTError:
            return None


# Global instance
_jwt_handler: Optional[JWTHandler] = None


def get_jwt_handler() -> JWTHandler:
    """Get or create the global JWT handler instance."""
    global _jwt_handler
    if _jwt_handler is None:
        _jwt_handler = JWTHandler()
    return _jwt_handler
