"""Transaction schemas - Pydantic models for request/response."""

from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class TransactionBase(BaseModel):
    """Base schema for transaction data."""
    amount: float = Field(..., gt=0, description="Transaction amount")
    reference: Optional[str] = Field(None, description="Transaction reference")


class TransactionCreate(TransactionBase):
    """Schema for creating a new transaction."""
    sender_account_id: UUID
    beneficiary_id: Optional[UUID] = None


class TransactionResponse(TransactionBase):
    """Schema for transaction response."""
    id: UUID
    sender_account_id: UUID
    beneficiary_id: Optional[UUID]
    type: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True
