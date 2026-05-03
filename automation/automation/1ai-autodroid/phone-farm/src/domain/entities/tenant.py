"""Domain entity for Tenant."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Tenant:
    """Tenant entity representing a multi-tenant customer."""

    id: str = ""
    name: str = ""
    email: str = ""
    stripe_customer_id: str = ""
    api_key_hash: str = ""
    plan: str = "free"
    rate_limit: float = 100.0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
