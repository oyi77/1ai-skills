"""
Base repository for generic CRUD operations.
"""

from typing import Any, Generic, TypeVar

import aiosqlite

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """Generic CRUD repository for any table."""

    def __init__(self, db: aiosqlite.Connection, table: str, pk_column: str = "id"):
        self.db = db
        self.table = table
        self.pk_column = pk_column

    async def create(self, data: dict[str, Any]) -> int:
        """Insert a new record. Returns the row ID."""
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        cursor = await self.db.execute(
            f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})", list(data.values())
        )
        await self.db.commit()
        return cursor.lastrowid

    async def get(self, pk_value: Any) -> dict[str, Any] | None:
        """Get a single record by primary key."""
        cursor = await self.db.execute(
            f"SELECT * FROM {self.table} WHERE {self.pk_column} = ?", (pk_value,)
        )
        row = await cursor.fetchone()
        return dict(row) if row else None

    async def get_all(
        self,
        where: str = "",
        params: list = None,
        order_by: str = "",
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """Get all records with optional filtering and pagination."""
        query = f"SELECT * FROM {self.table}"
        if where:
            query += f" WHERE {where}"
        if order_by:
            query += f" ORDER BY {order_by}"
        query += f" LIMIT ? OFFSET ?"

        params = (params or []) + [limit, offset]
        cursor = await self.db.execute(query, params)
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

    async def update(self, pk_value: Any, data: dict[str, Any]) -> bool:
        """Update a record by primary key. Returns True if updated."""
        if not data:
            return False
        set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
        params = list(data.values()) + [pk_value]
        cursor = await self.db.execute(
            f"UPDATE {self.table} SET {set_clause} WHERE {self.pk_column} = ?", params
        )
        await self.db.commit()
        return cursor.rowcount > 0

    async def delete(self, pk_value: Any) -> bool:
        """Delete a record by primary key. Returns True if deleted."""
        cursor = await self.db.execute(
            f"DELETE FROM {self.table} WHERE {self.pk_column} = ?", (pk_value,)
        )
        await self.db.commit()
        return cursor.rowcount > 0

    async def count(self, where: str = "", params: list = None) -> int:
        """Count records with optional filtering."""
        query = f"SELECT COUNT(*) FROM {self.table}"
        if where:
            query += f" WHERE {where}"
        cursor = await self.db.execute(query, params or [])
        row = await cursor.fetchone()
        return row[0] if row else 0

    async def exists(self, pk_value: Any) -> bool:
        """Check if a record exists by primary key."""
        cursor = await self.db.execute(
            f"SELECT 1 FROM {self.table} WHERE {self.pk_column} = ? LIMIT 1", (pk_value,)
        )
        row = await cursor.fetchone()
        return row is not None

    async def upsert(self, data: dict[str, Any], pk_column: str = None) -> int:
        """Insert or update a record. Returns the row ID."""
        pk = pk_column or self.pk_column
        pk_value = data.get(pk)
        if pk_value and await self.exists(pk_value):
            await self.update(pk_value, data)
            return pk_value
        return await self.create(data)
