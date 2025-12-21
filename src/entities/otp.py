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
    LOGIN = "LOGIN"                      # Two-factor authentication at login
    TRANSACTION = "TRANSACTION"          # Verify sensitive transactions
    PASSWORD_RESET = "PASSWORD_RESET"    # Password reset verification
    EMAIL_VERIFICATION = "EMAIL_VERIFICATION"  # Verify email address
    PHONE_VERIFICATION = "PHONE_VERIFICATION"  # Verify phone number
    ACCOUNT_ACTIVATION = "ACCOUNT_ACTIVATION"  # Activate new account


class OTP(BaseEntity):
    """OTP entity for storing one-time passwords with enhanced security features.
    
    Storing OTPs in a separate table provides:
    - Better audit trail of all OTP attempts
    - Support for multiple active OTPs per user (different purposes)
    - Easy cleanup of expired OTPs
    - Rate limiting by counting attempts
    - Better security by separating auth data from user profile
    """
    
    __tablename__ = "otps"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    code = Column(String(10), nullable=False)  # The actual OTP code
    purpose = Column(Enum(OTPPurpose), nullable=False)  # What the OTP is for
    is_used = Column(Boolean, default=False, nullable=False)  # Has this OTP been used
    attempts = Column(Integer, default=0, nullable=False)  # Number of verification attempts
    max_attempts = Column(Integer, default=3, nullable=False)  # Max allowed attempts
    expires_at = Column(DateTime, nullable=False)  # When the OTP expires
    created_at = Column(DateTime, default=datetime.utcnow)
    used_at = Column(DateTime, nullable=True)  # When the OTP was successfully used
    
    # Relationship to User
    user = relationship("User", back_populates="otp_codes")

    def is_valid(self) -> bool:
        """Check if OTP is still valid (not expired, not used, attempts not exceeded)."""
        if self.is_used:
            return False
        if self.attempts >= self.max_attempts:
            return False
        if datetime.utcnow() > self.expires_at:
            return False
        return True

    def verify(self, code: str) -> bool:
        """Verify the OTP code and update attempts counter."""
        self.attempts += 1
        if not self.is_valid():
            return False
        if self.code == code:
            self.is_used = True
            self.used_at = datetime.utcnow()
            return True
        return False

    def __repr__(self) -> str:
        return f"<OTP(id={self.id}, user_id={self.user_id}, purpose={self.purpose}, is_used={self.is_used})>"
