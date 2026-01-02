"""Transfer entity module."""

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .transaction import Transaction, TransactionType


class Transfer(Transaction):
    """Transfer entity representing a transfer between source account and beneficiary."""

    __tablename__ = "transfers"

    # Foreign key linking to the parent Transaction table
    id = Column(UUID(as_uuid=True), ForeignKey("transactions.id"), primary_key=True)
    beneficiary_id = Column(UUID(as_uuid=True), ForeignKey("beneficiaries.id"), nullable=False, index=True)

    # Polymorphic identity for inheritance
    __mapper_args__ = {
        "polymorphic_identity": TransactionType.TRANSFER,
    }

    # Relationships
    beneficiary = relationship("Beneficiary", foreign_keys=[beneficiary_id], cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Transfer(id={self.id}, amount={self.amount}, status={self.status}, beneficiary_id={self.beneficiary_id})>"
