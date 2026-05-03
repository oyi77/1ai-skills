"""Password hashing and verification using passlib."""

import hashlib
import os
import secrets
from typing import Optional

try:
    from passlib.context import CryptContext

    _PASSLIB_AVAILABLE = True
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
except ImportError:
    _PASSLIB_AVAILABLE = False


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    if _PASSLIB_AVAILABLE:
        return pwd_context.hash(password)
    return _fallback_hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against a stored hash."""
    if _PASSLIB_AVAILABLE:
        return pwd_context.verify(password, password_hash)
    return _fallback_verify(password, password_hash)


def _fallback_hash(password: str) -> str:
    """Fallback hash for development without passlib."""
    salt = os.urandom(32)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    return f"$pbkdf2${salt.hex()}${hashed.hex()}"


def _fallback_verify(password: str, password_hash: str) -> bool:
    """Fallback verification for development without passlib."""
    if not password_hash.startswith("$pbkdf2$"):
        return False
    parts = password_hash.split("$")
    if len(parts) != 3:
        return False
    salt = bytes.fromhex(parts[1])
    stored_hash = parts[2]
    computed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    return computed.hex() == stored_hash


def hash_token(token: str) -> str:
    """Hash a session or reset token for storage."""
    return hashlib.sha256(token.encode()).hexdigest()


def create_session_token() -> str:
    """Create a new session token."""
    return secrets.token_hex(32)


def create_password_reset_token() -> str:
    """Create a password reset token."""
    return secrets.token_hex(32)


def is_passlib_available() -> bool:
    """Check if passlib is available."""
    return _PASSLIB_AVAILABLE
