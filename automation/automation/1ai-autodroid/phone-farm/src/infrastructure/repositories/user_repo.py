"""User repository for user entity persistence."""

import time
from datetime import datetime
from typing import Any, Optional

import aiosqlite

from src.domain.entities.user import User, UserRole
from src.infrastructure.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User entity operations."""

    def __init__(self, db: aiosqlite.Connection):
        super().__init__(db, table="users", pk_column="id")

    def to_entity(self, row: dict[str, Any]) -> User:
        """Convert database row to User entity."""
        role_str = row.get("role", "user")
        return User(
            id=row.get("id"),
            username=row.get("name", ""),
            email=row.get("email", ""),
            password_hash=row.get("password_hash", ""),
            role=UserRole(role_str) if role_str else UserRole.USER,
            tenant_id=row.get("tenant_id", "default"),
            created_at=self._parse_datetime(row.get("created_at")),
            updated_at=self._parse_datetime(row.get("updated_at")),
        )

    def from_entity(self, user: User) -> dict[str, Any]:
        """Convert User entity to database row dict."""
        data = {
            "email": user.email,
            "password_hash": user.password_hash,
            "name": user.username,
            "role": user.role.value if isinstance(user.role, UserRole) else user.role,
            "tenant_id": user.tenant_id,
            "updated_at": time.time(),
        }
        if user.id is not None:
            data["id"] = user.id
        return {k: v for k, v in data.items() if v is not None}

    def _parse_datetime(self, value: Any) -> Optional[datetime]:
        """Parse datetime from database value."""
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(value)
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                return None
        return None

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email address."""
        cursor = await self.db.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = await cursor.fetchone()
        return self.to_entity(dict(row)) if row else None

    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return await self.get(user_id)

    async def create_user(
        self, email: str, name: str, password_hash: str, role: str = "user"
    ) -> str:
        """Create a new user. Returns user id."""
        import secrets

        user_id = f"user_{secrets.token_hex(8)}"
        now = time.time()
        data = {
            "id": user_id,
            "email": email,
            "name": name,
            "password_hash": password_hash,
            "role": role,
            "tenant_id": "default",
            "credits": 0,
            "created_at": now,
            "updated_at": now,
            "last_login": 0,
            "banned": 0,
        }
        return await self.create(data)

    async def update_last_login(self, user_id: str) -> bool:
        """Update user's last login timestamp."""
        return await self.update(user_id, {"last_login": time.time()})

    async def get_user_with_tenant(self, user_id: str, tenant_id: str = None) -> Optional[User]:
        """Get user with tenant isolation."""
        row = await self.get(user_id)
        if row and tenant_id and row.get("tenant_id") != tenant_id:
            return None
        return self.to_entity(row) if row else None


class SessionRepository(BaseRepository[dict]):
    """Repository for session management."""

    def __init__(self, db: aiosqlite.Connection):
        super().__init__(db, table="sessions", pk_column="id")

    async def create_session(self, user_id: str, token_hash: str, expires_at: float) -> str:
        """Create a new session. Returns session id."""
        import secrets

        session_id = secrets.token_hex(32)
        now = time.time()
        data = {
            "id": session_id,
            "user_id": user_id,
            "token_hash": token_hash,
            "expires_at": expires_at,
            "created_at": now,
        }
        await self.create(data)
        return session_id

    async def get_session(self, session_id: str) -> Optional[dict]:
        """Get session by id. Returns session if valid (not expired)."""
        cursor = await self.db.execute(
            "SELECT * FROM sessions WHERE id = ? AND expires_at > ?",
            (session_id, time.time()),
        )
        row = await cursor.fetchone()
        return dict(row) if row else None

    async def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        return await self.delete(session_id)

    async def delete_expired_sessions(self) -> int:
        """Delete all expired sessions. Returns count of deleted sessions."""
        cursor = await self.db.execute("DELETE FROM sessions WHERE expires_at < ?", (time.time(),))
        await self.db.commit()
        return cursor.rowcount
