"""Account entity module."""

from enum import Enum as PyEnum
from sqlalchemy import Column, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base import BaseEntity
from sqlalchemy.dialects.postgresql import UUID
import uuid


class AccountStatus(str, PyEnum):
    """Enum for account status."""
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"
    CLOSED = "CLOSED"


class Account(BaseEntity):
    """Account entity representing a bank account in the system."""
    
    __tablename__ = "accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    balance = Column(Float, default=0.0)
    currency = Column(String, default="TND")
    status = Column(Enum(AccountStatus), default=AccountStatus.ACTIVE, nullable=False)
    
    # Relationship to User
    user = relationship("User", back_populates="accounts")

    def __repr__(self) -> str:
        return f"<Account(id={self.id}, user_id={self.user_id}, balance={self.balance}, currency={self.currency}, status={self.status})>"
