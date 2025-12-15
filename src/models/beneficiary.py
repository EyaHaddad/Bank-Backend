"""Beneficiary entity module."""

from sqlalchemy import Column, Integer, String
from .base import BaseEntity
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Beneficiary(BaseEntity):
    __tablename__ = "beneficiaries"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)    
    sender_account_id = Column(Integer)
    name = Column(String)
    bank = Column(String)
    account_number = Column(String)