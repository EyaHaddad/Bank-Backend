"""Base entity class with common attributes."""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime

from src.infrastructure.database import Base


class BaseEntity(Base):
    """Base entity class with common attributes."""

    __abstract__ = True

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
    )
