"""Transaction entity module."""

from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base import BaseEntity
from sqlalchemy.dialects.postgresql import UUID
import uuid


class TransactionType(str, PyEnum):
    """Enum for transaction types."""
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"
    TRANSFER = "TRANSFER"


class TransactionStatus(str, PyEnum):
    """Enum for transaction status."""
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Transaction(BaseEntity):
    """Transaction entity representing a financial transaction."""
    
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    sender_account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False, index=True)
    beneficiary_id = Column(UUID(as_uuid=True), ForeignKey("beneficiaries.id"), nullable=True, index=True)
    amount = Column(Float, nullable=False)
    reference = Column(String, nullable=True)
    type = Column(Enum(TransactionType), nullable=False)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sender_account = relationship("Account", foreign_keys=[sender_account_id])
    beneficiary = relationship("Beneficiary", foreign_keys=[beneficiary_id])

    def __repr__(self) -> str:
        return f"<Transaction(id={self.id}, type={self.type}, status={self.status}, amount={self.amount})>"