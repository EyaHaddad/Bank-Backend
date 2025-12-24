"""Beneficiary schemas - Pydantic models for request/response."""

from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class BeneficiaryBase(BaseModel):
    """Base schema for beneficiary data."""
    name: str = Field(..., min_length=2, max_length=100, description="Beneficiary name")
    bank_name: str = Field(..., min_length=2, max_length=100, description="Bank name")
    iban: str = Field(..., min_length=15, max_length=34, description="IBAN number")
    email: Optional[str] = Field(None, description="Beneficiary email for notifications")


class BeneficiaryCreate(BeneficiaryBase):
    """Schema for creating a new beneficiary."""
    pass


class BeneficiaryUpdate(BaseModel):
    """Schema for updating a beneficiary."""
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="Beneficiary name")
    bank_name: Optional[str] = Field(None, min_length=2, max_length=100, description="Bank name")
    email: Optional[str] = Field(None, description="Beneficiary email")


class BeneficiaryResponse(BeneficiaryBase):
    """Schema for beneficiary response."""
    id: UUID
    user_id: UUID
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {
        "from_attributes": True
    }


class BeneficiaryListResponse(BaseModel):
    """Schema for listing beneficiaries."""
    beneficiaries: list[BeneficiaryResponse]
    total: int
