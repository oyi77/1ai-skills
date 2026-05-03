#!/usr/bin/env python3
"""User authentication helpers - password hashing and verification."""

import hashlib
import os
import secrets
import time
from pathlib import Path

# Try to use passlib, fall back to simple hash if not available
try:
    from passlib.context import CryptContext

    _PASSLIB_AVAILABLE = True
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
except ImportError:
    _PASSLIB_AVAILABLE = False


def hash_password(password: str) -> str:
    """Hash a password using bcrypt (or fallback SHA256)."""
    if _PASSLIB_AVAILABLE:
        return pwd_context.hash(password)
    # Fallback: simple salted hash (NOT secure, for dev only)
    salt = os.urandom(32)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    return f"$pbkdf2${salt.hex()}${hashed.hex()}"


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against a stored hash."""
    if _PASSLIB_AVAILABLE:
        return pwd_context.verify(password, password_hash)
    # Fallback verification
    if password_hash.startswith("$pbkdf2$"):
        parts = password_hash.split("$")
        if len(parts) != 3:
            return False
        salt = bytes.fromhex(parts[1])
        stored_hash = parts[2]
        computed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
        return computed.hex() == stored_hash
    return False


def hash_token(token: str) -> str:
    """Hash a session or reset token for storage."""
    return hashlib.sha256(token.encode()).hexdigest()


def create_session_token() -> str:
    """Create a new session token."""
    return secrets.token_hex(32)


def create_password_reset_token() -> str:
    """Create a password reset token."""
    return secrets.token_hex(32)


if __name__ == "__main__":
    # Test password hashing
    pw = "TestPassword123"
    hashed = hash_password(pw)
    print(f"Hash: {hashed}")
    print(f"Verify correct: {verify_password(pw, hashed)}")
    print(f"Verify wrong: {verify_password('WrongPassword', hashed)}")
