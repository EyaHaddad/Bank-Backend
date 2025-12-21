"""User entity module."""

from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .base import BaseEntity


class User(BaseEntity):
    """User entity representing a user in the system."""

    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    firstname = Column(String, index=True, nullable=False)
    lastname = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    password_hash = Column(String, nullable=False)

    # Relationships
    accounts = relationship("Account", back_populates="user", cascade="all, delete-orphan")
    beneficiaries = relationship("Beneficiary", back_populates="user", cascade="all, delete-orphan")
    otp_codes = relationship("OTP", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, is_active={self.is_active})>"
