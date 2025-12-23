"""Transfer entity module."""

from datetime import datetime, timezone
from enum import Enum as PyEnum

from sqlalchemy import Column, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from .base import BaseEntity


class TransferStatus(str, PyEnum):
    """Enum for transfer status."""
    PENDING = "PENDING"
    VALIDATED = "VALIDATED"
    REJECTED = "REJECTED"


class Transfer(BaseEntity):
    """Transfer entity representing a transfer between source account and beneficiary."""

    __tablename__ = "transfers"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    amount = Column(Float, nullable=False)
    status = Column(Enum(TransferStatus), default=TransferStatus.PENDING, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    source_account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False, index=True)
    beneficiary_id = Column(UUID(as_uuid=True), ForeignKey("beneficiaries.id"), nullable=False, index=True)
    transaction_id = Column(UUID(as_uuid=True), ForeignKey("transactions.id"), nullable=False, index=True)

    # Relationships
    source_account = relationship("Account", foreign_keys=[source_account_id])
    beneficiary = relationship("Beneficiary", foreign_keys=[beneficiary_id])
    transaction = relationship("Transaction", foreign_keys=[transaction_id])

    def __repr__(self) -> str:
        return f"<Transfer(id={self.id}, amount={self.amount}, status={self.status})>"
