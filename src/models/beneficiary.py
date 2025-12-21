"""Beneficiary entity module."""

from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseEntity
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Beneficiary(BaseEntity):
    """Beneficiary entity representing a payment beneficiary."""

    __tablename__ = "beneficiaries"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    bank_name = Column(String, nullable=False)
    iban = Column(String, nullable=False)
    email = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False, nullable=False)

    # Relationship to User
    user = relationship("User", back_populates="beneficiaries")

    def __repr__(self) -> str:
        return f"<Beneficiary(id={self.id}, name={self.name}, iban={self.iban}, is_verified={self.is_verified})>"
