"""OTP entity module for enhanced security."""

from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Enum, Integer
from sqlalchemy.orm import relationship
from .base import BaseEntity
from sqlalchemy.dialects.postgresql import UUID
import uuid


class OTPPurpose(str, PyEnum):
    """Enum for OTP purposes."""
    LOGIN = "LOGIN"
    TRANSACTION = "TRANSACTION"
    PASSWORD_RESET = "PASSWORD_RESET"
    EMAIL_VERIFICATION = "EMAIL_VERIFICATION"
    PHONE_VERIFICATION = "PHONE_VERIFICATION"
    ACCOUNT_ACTIVATION = "ACCOUNT_ACTIVATION"


class OTP(BaseEntity):
    """OTP entity for storing one-time passwords with enhanced security features."""

    __tablename__ = "otps"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    code = Column(String(10), nullable=False)
    purpose = Column(Enum(OTPPurpose), nullable=False)
    is_used = Column(Boolean, default=False, nullable=False)
    attempts = Column(Integer, default=0, nullable=False)
    max_attempts = Column(Integer, default=3, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used_at = Column(DateTime, nullable=True)

    # Relationship to User
    user = relationship("User", back_populates="otp_codes")

    def __repr__(self) -> str:
        return f"<OTP(id={self.id}, user_id={self.user_id}, purpose={self.purpose}, is_used={self.is_used})>"
