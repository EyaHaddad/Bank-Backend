"""Transaction entity module."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from .base import BaseEntity
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Transaction(BaseEntity):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)    
    sender_account_id = Column(Integer)
    beneficiary_account = Column(String)
    amount = Column(Float)
    reference = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)