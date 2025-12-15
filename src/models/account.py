"""Account entity module."""

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseEntity
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Account(BaseEntity):
    __tablename__ = "accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)    
    sender_account_id = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    balance = Column(Float, default=0.0)
    currency = Column(String, default="TND")
    user = relationship("User", back_populates="accounts")
