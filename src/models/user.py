"""User entity module."""

from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .base import BaseEntity


class User(BaseEntity):
    """User entity representing a user in the system.
    """

    __tablename__ = "users"
    # UUID v4: Generates a random 128-bit identifier (e.g., 550e8400-e29b-41d4-a716-446655440000)
    # as_uuid=True converts between PostgreSQL UUID type and Python uuid.UUID objects
    # default=uuid.uuid4 automatically creates a new UUID for each user upon insertion
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    #index=True creates a database index on the column for faster lookups
    firstname = Column(String, index=True, nullable=False)
    lastname = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    otp = Column(String, nullable=True)
    otp_expires_at = Column(DateTime, nullable=True)    
    password_hash = Column(String, nullable=False)
    accounts = relationship("Account", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
