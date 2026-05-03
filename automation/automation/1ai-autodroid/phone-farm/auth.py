#!/usr/bin/env python3
"""
Phone Farm — Authentication Module
Supports JWT tokens and API keys for securing the REST API.
"""

import base64
import hashlib
import hmac
import json
import os
import secrets
import time
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Optional


# =============================================================================
# JWT Implementation (zero external dependencies, HS256 only)
# =============================================================================


class JWT:
    """
    Minimal JWT encoder/decoder using HMAC-SHA256.
    No external dependencies required.
    """

    def __init__(self, secret: str):
        self.secret = secret.encode("utf-8")

    def _base64url_encode(self, data: bytes) -> str:
        """Base64 URL-safe encoding without padding."""
        return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")

    def _base64url_decode(self, data: str) -> bytes:
        """Base64 URL-safe decoding with padding."""
        pad = 4 - (len(data) % 4)
        if pad != 4:
            data += "=" * pad
        return base64.urlsafe_b64decode(data)

    def _sign(self, message: str) -> str:
        """HMAC-SHA256 signature."""
        return hmac.new(
            self.secret, message.encode("utf-8"), hashlib.sha256
        ).hexdigest()

    def encode(self, payload: dict, expires_in: int = 86400) -> str:
        """
        Encode a payload into a JWT token.

        Args:
            payload: Dictionary containing claims
            expires_in: Token validity in seconds (default: 24 hours)

        Returns:
            JWT token string
        """
        # Add expiration if not already set
        if "exp" not in payload:
            payload["exp"] = int(time.time()) + expires_in

        # Add issued-at time
        if "iat" not in payload:
            payload["iat"] = int(time.time())

        # Header
        header = {"alg": "HS256", "typ": "JWT"}
        header_encoded = self._base64url_encode(
            json.dumps(header, separators=(",", ":")).encode("utf-8")
        )

        # Payload
        payload_encoded = self._base64url_encode(
            json.dumps(payload, separators=(",", ":")).encode("utf-8")
        )

        # Signature
        signature = self._sign(f"{header_encoded}.{payload_encoded}")
        signature_encoded = self._base64url_encode(signature.encode("utf-8"))

        return f"{header_encoded}.{payload_encoded}.{signature_encoded}"

    def decode(self, token: str) -> Optional[dict]:
        """
        Decode and validate a JWT token.

        Args:
            token: JWT token string

        Returns:
            Decoded payload if valid, None if invalid/expired
        """
        try:
            parts = token.split(".")
            if len(parts) != 3:
                return None

            header_encoded, payload_encoded, signature_encoded = parts

            # Verify signature
            expected_signature = self._sign(f"{header_encoded}.{payload_encoded}")
            expected_sig_bytes = self._base64url_encode(
                expected_signature.encode("utf-8")
            )

            if not hmac.compare_digest(signature_encoded, expected_sig_bytes):
                return None

            # Decode payload
            payload = json.loads(self._base64url_decode(payload_encoded))

            # Check expiration
            if "exp" in payload and payload["exp"] < int(time.time()):
                return None

            return payload

        except (ValueError, json.JSONDecodeError, Exception):
            return None


# =============================================================================
# API Key Manager
# =============================================================================


class APIKey:
    """Represents a single API key."""

    def __init__(
        self,
        key_id: str,
        key_prefix: str,
        key_hash: str,
        name: str,
        role: str,
        created_at: int,
        expires_at: Optional[int] = None,
        revoked: bool = False,
    ):
        self.key_id = key_id
        self.key_prefix = key_prefix
        self.key_hash = key_hash
        self.name = name
        self.role = role
        self.created_at = created_at
        self.expires_at = expires_at
        self.revoked = revoked

    def to_dict(self) -> dict:
        return {
            "key_id": self.key_id,
            "key_prefix": self.key_prefix,
            "name": self.name,
            "role": self.role,
            "created_at": self.created_at,
            "expires_at": self.expires_at,
            "revoked": self.revoked,
        }


class APIKeyManager:
    """
    Manages API keys for the phone farm.
    Supports create, validate, revoke, and list operations.
    """

    def __init__(self, storage_path: Optional[str] = None):
        """
        Initialize the API key manager.

        Args:
            storage_path: Path to store API keys JSON file
        """
        self._keys: dict[str, APIKey] = {}
        self._storage_path = storage_path or os.environ.get(
            "PHONEFARM_API_KEYS_PATH", "/tmp/phonefarm_api_keys.json"
        )
        self._load_keys()

    def _load_keys(self) -> None:
        """Load keys from storage file."""
        if os.path.exists(self._storage_path):
            try:
                with open(self._storage_path, "r") as f:
                    data = json.load(f)
                    for key_id, key_data in data.items():
                        self._keys[key_id] = APIKey(**key_data)
            except (json.JSONDecodeError, Exception):
                pass

    def _save_keys(self) -> None:
        """Save keys to storage file."""
        try:
            data = {key_id: key.to_dict() for key_id, key in self._keys.items()}
            with open(self._storage_path, "w") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def _hash_key(self, api_key: str) -> str:
        """Hash an API key for secure storage."""
        return hashlib.sha256(api_key.encode("utf-8")).hexdigest()

    def create_key(
        self, name: str, role: str = "operator", expires_in: Optional[int] = None
    ) -> tuple[str, APIKey]:
        """
        Create a new API key.

        Args:
            name: Human-readable name for the key
            role: Role for the key (operator, viewer, admin)
            expires_in: Expiration in seconds (None = never expires)

        Returns:
            Tuple of (full_api_key, APIKey object)
        """
        key_id = secrets.token_hex(8)
        full_key = f"pf_{secrets.token_hex(32)}"
        key_hash = self._hash_key(full_key)

        created_at = int(time.time())
        expires_at = created_at + expires_in if expires_in else None

        api_key_obj = APIKey(
            key_id=key_id,
            key_prefix=full_key[:12] + "...",
            key_hash=key_hash,
            name=name,
            role=role,
            created_at=created_at,
            expires_at=expires_at,
        )

        self._keys[key_id] = api_key_obj
        self._save_keys()

        return full_key, api_key_obj

    def validate_key(self, api_key: str) -> Optional[APIKey]:
        """
        Validate an API key.

        Args:
            api_key: The full API key string

        Returns:
            APIKey object if valid, None if invalid/revoked/expired
        """
        if not api_key or not api_key.startswith("pf_"):
            return None

        key_hash = self._hash_key(api_key)

        for key_id, key_obj in self._keys.items():
            if key_obj.key_hash == key_hash:
                # Check if revoked
                if key_obj.revoked:
                    return None
                # Check if expired
                if key_obj.expires_at and key_obj.expires_at < int(time.time()):
                    return None
                return key_obj

        return None

    def revoke_key(self, key_id: str) -> bool:
        """
        Revoke an API key.

        Args:
            key_id: The key ID to revoke

        Returns:
            True if revoked, False if not found
        """
        if key_id in self._keys:
            self._keys[key_id].revoked = True
            self._save_keys()
            return True
        return False

    def list_keys(self, include_revoked: bool = False) -> list[dict]:
        """
        List all API keys.

        Args:
            include_revoked: Include revoked keys in the list

        Returns:
            List of key dictionaries
        """
        result = []
        for key_obj in self._keys.values():
            if not include_revoked and key_obj.revoked:
                continue
            result.append(key_obj.to_dict())
        return result

    def delete_key(self, key_id: str) -> bool:
        """
        Permanently delete an API key.

        Args:
            key_id: The key ID to delete

        Returns:
            True if deleted, False if not found
        """
        if key_id in self._keys:
            del self._keys[key_id]
            self._save_keys()
            return True
        return False


# =============================================================================
# Auth Instance and Helper Functions
# =============================================================================

_jwt_secret = os.environ.get("PHONEFARM_JWT_SECRET", "change-me-in-production")
_jwt_instance = JWT(_jwt_secret)
_api_keys_instance: Optional[APIKeyManager] = None


def get_api_keys() -> APIKeyManager:
    """Get or create the global API key manager instance."""
    global _api_keys_instance
    if _api_keys_instance is None:
        _api_keys_instance = APIKeyManager()
    return _api_keys_instance


def get_jwt() -> JWT:
    """Get the global JWT instance."""
    return _jwt_instance


def create_token(
    user_id: str, role: str = "operator", tenant_id: str = "default"
) -> str:
    payload = {"sub": user_id, "role": role, "tenant_id": tenant_id}
    return _jwt_instance.encode(payload)


def verify_token(token: str) -> Optional[dict]:
    """
    Verify a JWT token.

    Args:
        token: JWT token string

    Returns:
        Decoded payload if valid, None otherwise
    """
    return _jwt_instance.decode(token)


# =============================================================================
# FastAPI Auth Decorator
# =============================================================================


def require_auth(role: str = "viewer"):
    """
    FastAPI dependency for JWT/API key authentication.

    Args:
        role: Minimum required role (admin > operator > viewer)

    Returns:
        FastAPI dependency function

    Usage:
        @app.get("/devices")
        def list_devices(user = require_auth("viewer")):
            ...
    """
    role_levels = {"viewer": 0, "operator": 1, "admin": 2}

    def dependency(request):
        """Auth dependency for FastAPI."""
        tenant_id = "default"

        # Try JWT first (Authorization: Bearer <token>)
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
            payload = _jwt_instance.decode(token)
            if payload:
                user_role = payload.get("role", "viewer")
                tenant_id = payload.get("tenant_id", "default")
                if role_levels.get(user_role, 0) >= role_levels.get(role, 0):
                    return {**payload, "tenant_id": tenant_id}

        # Try API Key (X-API-Key header)
        api_key = request.headers.get("X-API-Key")
        if api_key:
            key_obj = get_api_keys().validate_key(api_key)
            if key_obj:
                user_role = key_obj.role
                # Look up tenant by API key hash via tenant module
                try:
                    from tenant import get_tenant_by_api_key_hash

                    key_hash = hashlib.sha256(api_key.encode("utf-8")).hexdigest()
                    tenant_obj = get_tenant_by_api_key_hash(key_hash)
                    if tenant_obj:
                        tenant_id = tenant_obj["id"]
                except Exception:
                    pass
                if role_levels.get(user_role, 0) >= role_levels.get(role, 0):
                    return {
                        "sub": key_obj.key_id,
                        "role": user_role,
                        "key_name": key_obj.name,
                        "tenant_id": tenant_id,
                    }

        # No valid auth found
        from fastapi import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing authentication",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return dependency


# =============================================================================
# Convenience Functions for CLI
# =============================================================================


def cli_create_key(
    name: str, role: str = "operator", expires_days: Optional[int] = None
):
    """
    CLI helper to create an API key.

    Args:
        name: Name for the key
        role: Role for the key
        expires_days: Days until expiration (None = never)
    """
    expires_in = expires_days * 86400 if expires_days else None
    key, key_obj = get_api_keys().create_key(name, role, expires_in)
    print(f"API Key created: {key}")
    print(f"Key ID: {key_obj.key_id}")
    print(f"Role: {key_obj.role}")
    print(f"Save this key - it cannot be retrieved again!")


def cli_list_keys():
    """CLI helper to list API keys."""
    keys = get_api_keys().list_keys()
    if not keys:
        print("No API keys found.")
        return
    print(f"{'Name':<20} {'ID':<20} {'Role':<10} {'Created':<12} {'Status'}")
    print("-" * 70)
    for k in keys:
        created = datetime.fromtimestamp(k["created_at"]).strftime("%Y-%m-%d")
        status = "revoked" if k["revoked"] else "active"
        print(
            f"{k['name']:<20} {k['key_id']:<20} {k['role']:<10} {created:<12} {status}"
        )


def cli_revoke_key(key_id: str):
    """CLI helper to revoke an API key."""
    if get_api_keys().revoke_key(key_id):
        print(f"Key {key_id} revoked.")
    else:
        print(f"Key {key_id} not found.")


# =============================================================================
# Main (for CLI testing)
# =============================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("PhoneFarm Auth Module")
        print("Usage: auth.py <command> [args]")
        print("Commands:")
        print("  create-key <name> [role] [days]  - Create API key")
        print("  list-keys                        - List API keys")
        print("  revoke-key <key_id>              - Revoke API key")
        print("  create-token <user_id> [role]    - Create JWT token")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "create-key":
        name = sys.argv[2] if len(sys.argv) > 2 else "cli-key"
        role = sys.argv[3] if len(sys.argv) > 3 else "operator"
        days = int(sys.argv[4]) if len(sys.argv) > 4 else None
        cli_create_key(name, role, days)
    elif cmd == "list-keys":
        cli_list_keys()
    elif cmd == "revoke-key":
        key_id = sys.argv[2] if len(sys.argv) > 2 else None
        if key_id:
            cli_revoke_key(key_id)
        else:
            print("Error: key_id required")
    elif cmd == "create-token":
        user_id = sys.argv[2] if len(sys.argv) > 2 else "test-user"
        role = sys.argv[3] if len(sys.argv) > 3 else "operator"
        print(create_token(user_id, role))
    else:
        print(f"Unknown command: {cmd}")
